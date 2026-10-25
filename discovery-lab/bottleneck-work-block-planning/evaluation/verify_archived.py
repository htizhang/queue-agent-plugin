"""Verify the archived flow-time projection and recompute its reported values.

From this entry's directory:

    python3 evaluation/verify_archived.py              # Python 3.10+ standard library
    python3 evaluation/verify_archived.py --bootstrap  # also needs NumPy

The default check recomputes every pooled mean, reduction, and configuration
count from the stored configuration means and seed means. It also checks the
archived interval signs that the evaluation note cites, but it does not
recompute the intervals. With --bootstrap, NumPy regenerates the archived
bootstrap draws and recomputes all 41 intervals.

No simulation runs. Every number is an archived research result.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

DATA = Path(__file__).with_name("archived-flow-means.json")
SOURCE_SHA256 = {
    "frozen_policy_source": (
        "e59db7f85bfdb2380d96a324708aa20d8dcc6089b067c84c84f57291d35576bf"
    ),
    "simulator": "30aa55a9bfd713146aa3de7203c4e04248a34d3861f045733a8ea8c4fdf5cf0f",
    "family_generator": (
        "94732ffa0062cacda24732da559bb922eb820422ca3d83ea0ab2fc43c793534d"
    ),
    "baseline_rules": (
        "5a52f1acd4de98c7c9b5d38e2a9bfb4cc018d8be7d0611165625715e4c11a630"
    ),
    "validation_runner": (
        "8c9834833ea8462aa21234d7c089e38ea5026be536f8718d4b593f5f927b8b1a"
    ),
    "study_design": (
        "543b15663fac248303eb27f9882efeaf6043d88147b947f5393e2c5cd486ebec"
    ),
    "current_only_selection": (
        "e36990aeea98bf19a3d93eb1e4cc03cc3bd900b66ccc10fc14801bcf3d4a4038"
    ),
    "raw_validation_rows": (
        "a79d0168c6b8482067351616d759e0e6a4f696410f7c70b0a63574653821990a"
    ),
    "analysis_script": (
        "12d1327293cade542438dd0542ce1542ff211d74015936e471b6285ea8c26a1e"
    ),
    "analysis_summary": (
        "59aa1cb83991eb6e7e6c69e409bfcc22006dfc268f3e1c2eae2f95c61ed349ed"
    ),
    "configuration_means_table": (
        "4de00b42dde2ab8ab39fc46adef9edabd5b71bd798a13cf001b07d663ec6fc2d"
    ),
}
PROPOSED = "remaining:8"
PRIMARY = "public:PR_normalized"
BOOTSTRAP_SEED = 1011
BOOTSTRAP_DRAWS = 20_000
BOOTSTRAP_DESCRIPTION = (
    "numpy.random.default_rng(1011).integers(0, 16, size=(20000, 16))"
)
MEAN_REL_TOL = (
    1e-12  # Archived means used NumPy summation; this file uses statistics.fmean.
)
PERCENT_ABS_TOL = 1e-9
TIE = 1e-10  # Configuration gains within +-1e-10 percent count as ties, as archived.


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def valid_values(values, count, label):
    require(
        len(values) == count, f"{label}: expected {count} values, found {len(values)}"
    )
    require(
        all(isinstance(v, float) and math.isfinite(v) and v > 0.0 for v in values),
        f"{label}: values must be positive finite numbers",
    )


class Evidence:
    def __init__(self, data):
        self.data = data
        self.policies = data["policies"]
        self.configurations = data["design"]["configurations"]
        self.layouts = data["design"]["layouts"]
        self.worst_mean = 0.0
        self.worst_percent = 0.0

    def layout_of(self, configuration):
        return configuration.split("_k")[0]

    def indices(self, scope):
        if scope == "all":
            return list(range(len(self.configurations)))
        return [
            i for i, c in enumerate(self.configurations) if self.layout_of(c) == scope
        ]

    def pooled(self, spec, scope):
        means = self.policies[spec]["configuration_means"]
        return statistics.fmean(means[i] for i in self.indices(scope))

    def seed_means(self, spec, scope):
        if scope == "all":
            return self.policies[spec]["seed_means"]
        return self.data["layout_seed_means"][scope][spec]

    def check_mean(self, actual, expected, label):
        require(
            math.isclose(actual, expected, rel_tol=MEAN_REL_TOL, abs_tol=0.0),
            f"{label}: {actual!r} != {expected!r}",
        )
        self.worst_mean = max(self.worst_mean, abs(actual - expected) / expected)

    def check_percent(self, actual, expected, label):
        require(
            math.isclose(actual, expected, rel_tol=0.0, abs_tol=PERCENT_ABS_TOL),
            f"{label}: {actual!r} != {expected!r}",
        )
        self.worst_percent = max(self.worst_percent, abs(actual - expected))

    def counts(self, candidate, reference, scope):
        a = self.policies[candidate]["configuration_means"]
        b = self.policies[reference]["configuration_means"]
        gains = [100.0 * (1.0 - a[i] / b[i]) for i in self.indices(scope)]
        return [
            sum(g > TIE for g in gains),
            sum(abs(g) <= TIE for g in gains),
            sum(g < -TIE for g in gains),
        ]


def verify_structure(evidence):
    data = evidence.data
    require(
        data["status"] == "archived_projection",
        "evidence must be marked archived_projection",
    )
    require(
        data["source_sha256"] == SOURCE_SHA256,
        "source hashes do not match the frozen provenance",
    )
    require(
        data["aggregation"]["bootstrap_draws"] == BOOTSTRAP_DESCRIPTION,
        "bootstrap description changed",
    )
    seeds = data["design"]["seeds"]
    require(len(seeds) == len(set(seeds)) == 16, "expected 16 unique seeds")
    require(
        not set(seeds) & set(data["design"]["development_seeds"]),
        "validation seeds were used in development",
    )
    configurations = evidence.configurations
    require(
        len(configurations) == len(set(configurations)) == 27,
        "expected 27 unique configurations",
    )
    for layout in evidence.layouts:
        require(
            len(evidence.indices(layout)) == 9, f"{layout}: expected 9 configurations"
        )
    require(len(evidence.policies) == 22, "expected 22 policies")
    for spec, policy in evidence.policies.items():
        valid_values(policy["configuration_means"], 27, f"{spec} configuration means")
        valid_values(policy["seed_means"], 16, f"{spec} seed means")
        # Both marginals average the same 432 run values.
        evidence.check_mean(
            evidence.pooled(spec, "all"), policy["mean"], f"{spec} from configurations"
        )
        evidence.check_mean(
            statistics.fmean(policy["seed_means"]), policy["mean"], f"{spec} from seeds"
        )
    for layout, group in data["layout_seed_means"].items():
        for spec, values in group.items():
            valid_values(values, 16, f"{layout}/{spec} seed means")
            evidence.check_mean(
                statistics.fmean(values),
                evidence.pooled(spec, layout),
                f"{layout}/{spec}",
            )


def verify_comparisons(evidence):
    comparisons = evidence.data["comparisons"]
    require(len(comparisons) == 31, "expected 31 comparisons")
    for c in comparisons:
        label = f"{c['group']}/{c['scope']}/{c['candidate']} vs {c['reference']}"
        candidate = evidence.pooled(c["candidate"], c["scope"])
        reference = evidence.pooled(c["reference"], c["scope"])
        evidence.check_percent(
            100.0 * (1.0 - candidate / reference), c["reduction_percent"], label
        )
        require(
            evidence.counts(c["candidate"], c["reference"], c["scope"])
            == c["configurations_won_tied_lost"],
            f"{label}: configuration counts changed",
        )
        intervals = [c["ci95_percent"]] + (
            [c["ci99_5_bonferroni_percent"]] if c["group"] == "baseline" else []
        )
        for low, high in intervals:
            require(low <= high, f"{label}: interval bounds are reversed")
    return comparisons


def find(comparisons, group, reference, scope="all", candidate=PROPOSED):
    (match,) = [
        c
        for c in comparisons
        if (c["group"], c["scope"], c["candidate"], c["reference"])
        == (group, scope, candidate, reference)
    ]
    return match


def verify_cited_claims(evidence, comparisons):
    """Each assertion matches a statement in the evaluation note."""
    policies = evidence.policies
    baselines = [c for c in comparisons if c["group"] == "baseline"]
    require(len(baselines) == 10, "expected ten baselines")
    lowest = min((c["reference"] for c in baselines), key=lambda s: policies[s]["mean"])
    require(lowest == PRIMARY, "normalized PR is no longer the lowest baseline mean")
    for c in baselines:
        require(
            c["ci95_percent"][0] > 0.0, f"{c['reference']}: 95% interval reaches zero"
        )
        require(
            c["ci99_5_bonferroni_percent"][0] > 0.0,
            f"{c['reference']}: 99.5% interval reaches zero",
        )
    require(
        find(comparisons, "baseline", PRIMARY)["configurations_won_tied_lost"]
        == [23, 0, 4],
        "PR counts",
    )
    lost = {
        layout: find(comparisons, "layout", PRIMARY, layout)[
            "configurations_won_tied_lost"
        ][2]
        for layout in evidence.layouts
    }
    require(
        lost == {"mask2x2": 4, "mask3x2": 0, "mask2x3": 0},
        "losses to normalized PR moved layout",
    )

    for spec in ("current:8", "current:6"):
        require(
            find(comparisons, "ablation", spec)["reduction_percent"] > 0.0,
            f"{spec}: aggregate sign",
        )
        require(
            find(comparisons, "layout", spec, "mask3x2")["reduction_percent"] < 0.0,
            f"{spec}: mask3x2 sign",
        )
    low, high = find(comparisons, "layout", "current:8", "mask3x2")["ci95_percent"]
    require(low < 0.0 < high, "matched three-station interval no longer includes zero")
    require(
        find(comparisons, "layout", "current:6", "mask3x2")["ci95_percent"][1] < 0.0,
        "selected interval",
    )

    sensitivity = {
        int(c["candidate"].split(":")[1]): c
        for c in comparisons
        if c["group"] == "sensitivity"
    }
    require(
        min(sensitivity, key=lambda b: policies[f"remaining:{b}"]["mean"]) == 12,
        "lowest validation weight",
    )
    require(
        all(abs(sensitivity[b]["reduction_percent"]) < 0.66 for b in (6, 12, 16)),
        "nearby weights",
    )

    development = evidence.data["design"]["development_means"]
    for key, chosen in (
        ("bottleneck_work_planner", 8),
        ("current_operation_only_planner", 6),
    ):
        curve = {int(b): v for b, v in development[key].items()}
        require(
            min(curve, key=lambda b: (curve[b], b)) == chosen,
            f"{key}: development selection",
        )


def bootstrap(evidence, comparisons):
    try:
        import numpy as np
    except ImportError:
        raise SystemExit(
            "--bootstrap needs NumPy. "
            "The default check needs only the standard library."
        ) from None
    draws = np.random.default_rng(BOOTSTRAP_SEED).integers(
        0, 16, size=(BOOTSTRAP_DRAWS, 16)
    )
    worst, checked = 0.0, 0
    for c in comparisons:
        a = np.array(evidence.seed_means(c["candidate"], c["scope"]))
        b = np.array(evidence.seed_means(c["reference"], c["scope"]))
        samples = 100 * (1 - a[draws].mean(axis=1) / b[draws].mean(axis=1))
        targets = [([0.025, 0.975], c["ci95_percent"])]
        if c["group"] == "baseline":
            targets.append(([0.0025, 0.9975], c["ci99_5_bonferroni_percent"]))
        for quantiles, archived in targets:
            recomputed = np.quantile(samples, quantiles).tolist()
            for actual, expected in zip(recomputed, archived, strict=True):
                require(
                    math.isclose(
                        actual, expected, rel_tol=0.0, abs_tol=PERCENT_ABS_TOL
                    ),
                    f"{c['group']}/{c['scope']}/{c['reference']}: interval "
                    f"{actual!r} != {expected!r}. NumPy {np.__version__} may draw "
                    "differently from the archived NumPy 1.26.4.",
                )
                worst = max(worst, abs(actual - expected))
            checked += 1
    print(
        f"Bootstrap: recomputed {checked} archived intervals with NumPy "
        f"{np.__version__}. Largest difference: {worst:.3g} percentage points."
    )


def interval(bounds):
    return f"[{bounds[0]:.2f}%, {bounds[1]:.2f}%]"


def report(evidence, comparisons):
    policies = evidence.policies
    print("Baseline panel: reduction = 100 * (1 - proposed mean / baseline mean)")
    header = f"{'Mean flow':>10} {'Reduction':>10}  {'95% interval':18} Won/27  99.5%"
    print(f"  {'Baseline':28} {header}")
    print(f"  {'Proposed policy, beta=8':28} {policies[PROPOSED]['mean']:10.3f}")
    for c in sorted(
        (c for c in comparisons if c["group"] == "baseline"),
        key=lambda c: policies[c["reference"]]["mean"],
    ):
        reference = policies[c["reference"]]
        print(
            f"  {reference['label']:28} {reference['mean']:10.3f} "
            f"{c['reduction_percent']:9.2f}%  {interval(c['ci95_percent']):18} "
            f"{c['configurations_won_tied_lost'][0]:6}  "
            f"{interval(c['ci99_5_bonferroni_percent'])}"
        )
    print("Current-operation-only ablation")
    for c in (c for c in comparisons if c["group"] == "ablation"):
        reference = policies[c["reference"]]
        print(
            f"  {reference['label']:64} {reference['mean']:10.3f} "
            f"{c['reduction_percent']:6.2f}%  {interval(c['ci95_percent']):18} "
            f"{c['configurations_won_tied_lost'][0]}/27"
        )
    print("By layout: reduction and configurations won of 9")
    for layout, name in evidence.layouts.items():
        cells = []
        for spec in (PRIMARY, "current:8", "current:6"):
            c = find(comparisons, "layout", spec, layout)
            cells.append(
                f"{c['reduction_percent']:6.2f}% {interval(c['ci95_percent'])} "
                f"{c['configurations_won_tied_lost'][0]}"
            )
        print(
            f"  {name:28} vs PR normalized {cells[0]} | vs current beta=8 {cells[1]} "
            f"| vs current beta=6 {cells[2]}"
        )
    print(
        "Setup-weight sensitivity: change = 100 * (F_beta / F_8 - 1), positive is worse"
    )
    development = evidence.data["design"]["development_means"][
        "bottleneck_work_planner"
    ]
    for c in (c for c in comparisons if c["group"] == "sensitivity"):
        beta = c["candidate"].split(":")[1]
        # Negate the archived orientation. Adding 0.0 turns -0.0 into +0.0.
        change = -c["reduction_percent"] + 0.0
        low, high = (-bound + 0.0 for bound in reversed(c["ci95_percent"]))
        print(
            f"  beta={beta:>2} development {development[beta]:8.3f} validation "
            f"{policies[c['candidate']]['mean']:8.3f} change {change:+7.2f}% "
            f"[{low:+.2f}%, {high:+.2f}%]"
        )
    diagnostics = evidence.data["diagnostics"]
    changeovers = ", ".join(
        f"{k} {v:,.0f}" for k, v in diagnostics["mean_changeovers_per_run"].items()
    )
    print(
        f"Archived diagnostics, not recomputed: mean changeovers per run: {changeovers}"
    )
    adverse = diagnostics["runs_with_measured_jobs_left_at_arrival_shutdown"]
    print(
        f"  runs with measured jobs left when arrivals stopped: {adverse}, "
        f"largest backlog {diagnostics['largest_measured_backlog_at_arrival_shutdown']}"
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="also recompute the archived intervals with NumPy",
    )
    args = parser.parse_args()
    evidence = Evidence(json.loads(DATA.read_text(encoding="utf-8")))
    verify_structure(evidence)
    comparisons = verify_comparisons(evidence)
    verify_cited_claims(evidence, comparisons)
    report(evidence, comparisons)
    if args.bootstrap:
        bootstrap(evidence, comparisons)
    stored = sum(
        len(p["configuration_means"]) + len(p["seed_means"])
        for p in evidence.policies.values()
    )
    print(
        "ARCHIVED projection verified: 22 policies x 432 runs "
        f"(27 configurations x 16 seeds), {stored} stored policy means, "
        "31 comparisons."
    )
    print(
        "Largest recomputation differences: pooled mean "
        f"{evidence.worst_mean:.2g} relative, reduction "
        f"{evidence.worst_percent:.2g} percentage points."
    )


if __name__ == "__main__":
    main()
