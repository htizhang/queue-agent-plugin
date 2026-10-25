"""Recompute the archived mean-response comparisons from the bundled projection.

The script reads archived_mean_response.json and runs no simulation. It
recomputes seed ratios, point estimates, and 95% Student-t intervals with the
Python standard library, then checks them against the archived analysis values.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

DATA = Path(__file__).with_name("archived_mean_response.json")
RATIO_TOL = 1e-13  # absolute tolerance for seed and configuration ratios
PERCENT_TOL = 1e-10  # absolute tolerance for percentages
DEFAULT = (2.0, 0.125)


def t975(df: int = 7) -> float:
    """Return the 0.975 quantile of Student's t with 7 degrees of freedom."""
    assert df == 7

    def cdf(x: float) -> float:
        # Closed form for odd degrees of freedom.
        theta = math.atan(x / math.sqrt(df))
        c = math.cos(theta)
        inner = c + (2 / 3) * c**3 + (8 / 15) * c**5
        return 0.5 + (theta + math.sin(theta) * inner) / math.pi

    low, high = 0.0, 10.0
    for _ in range(200):
        middle = (low + high) / 2
        if cdf(middle) < 0.975:
            low = middle
        else:
            high = middle
    return (low + high) / 2


T975 = t975()


def summarize(ratios: list[float]) -> tuple[float, list[float]]:
    """Return the change and its 95% interval, in percent."""
    mean = statistics.fmean(ratios)
    half = T975 * (statistics.stdev(ratios) / math.sqrt(len(ratios)))
    return 100 * (mean - 1), [100 * (mean - half - 1), 100 * (mean + half - 1)]


def pairs(first: list[float], second: list[float], label: str):
    if len(first) != len(second):
        raise AssertionError(f"{label}: length mismatch")
    return zip(first, second)


def close(actual: float, expected: float, tol: float, label: str) -> float:
    error = abs(actual - expected)
    if not error <= tol:
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")
    return error


def check_summary(ratios, archived, label, worst):
    change, interval = summarize(ratios)
    worst["percent"] = max(worst["percent"], close(change, archived["change_pct"], PERCENT_TOL, label))
    for index in range(2):
        worst["percent"] = max(worst["percent"], close(
            interval[index], archived["ci95_pct"][index], PERCENT_TOL, f"{label} interval"))
    return change, interval


def in_group(config: dict, group: str) -> bool:
    if group == "all":
        return True
    field, value = group.split(":")
    if field in ("capacity", "load_target"):
        return config[field] == float(value)
    return config[field] == value


def verify(data: dict) -> list[str]:
    if data["status"] != "archived_projection" or data["objective"] != "mean_response":
        raise AssertionError("unexpected status or objective")
    seeds = data["design"]["seeds"]
    if len(seeds) != 8 or len(set(seeds)) != 8:
        raise AssertionError("expected eight distinct seeds")
    configs = [dict(zip(data["configuration_fields"], row)) for row in data["configurations"]]
    ids = [config["id"] for config in configs]
    if len(configs) != 81 or len(set(ids)) != 81:
        raise AssertionError("expected 81 distinct configurations")
    expected_sizes = {"grid:workload_type": 45, "grid:width_mix": 36, "capacity:32": 27,
                      "capacity:128": 27, "capacity:512": 27, "load_target:0.55": 27,
                      "load_target:0.75": 27, "load_target:0.9": 27, "requests:exact": 63,
                      "requests:conservative": 18}
    for group, size in expected_sizes.items():
        if sum(in_group(config, group) for config in configs) != size:
            raise AssertionError(f"{group}: unexpected group size")

    runs = data["mean_response"]
    for name, rows in runs.items():
        values = [value for row in rows for value in row]
        if len(rows) != 81 or len(values) != 648:
            raise AssertionError(f"{name}: expected 81 x 8 values")
        if not all(math.isfinite(value) and value > 0 for value in values):
            raise AssertionError(f"{name}: invalid mean response")

    def seed_ratios(candidate: str, comparator: str, group: str) -> list[float]:
        members = [index for index, config in enumerate(configs) if in_group(config, group)]
        return [math.exp(statistics.fmean(
            math.log(runs[candidate][index][seed] / runs[comparator][index][seed])
            for index in members)) for seed in range(len(seeds))]

    worst = {"ratio": 0.0, "percent": 0.0}
    lines = []
    raw = {}
    for item in data["raw_comparisons"]:
        key = (item["candidate"], item["comparator"], item["group"])
        label = "{} vs {} [{}]".format(*key)
        ratios = seed_ratios(*key)
        for actual, expected in pairs(ratios, item["archived"]["seed_ratios"], label):
            worst["ratio"] = max(worst["ratio"], close(actual, expected, RATIO_TOL, label))
        change, interval = check_summary(ratios, item["archived"], label, worst)
        raw[key] = ratios
        lines.append(f"{label}: change {change:+.3f}% [{interval[0]:+.3f}%, {interval[1]:+.3f}%], "
                     f"lower in {sum(r < 1 for r in ratios)}/8 seeds")

    for item in data["per_configuration"]:
        candidate, comparator = item["candidate"], item["comparator"]
        changes = [100 * math.expm1(statistics.fmean(
            math.log(runs[candidate][index][seed] / runs[comparator][index][seed])
            for seed in range(len(seeds)))) for index in range(len(configs))]
        lower = sum(change < 0 for change in changes)
        if lower != item["archived"]["configurations_lower"]:
            raise AssertionError(f"{candidate} vs {comparator}: configuration count")
        close(max(changes), item["archived"]["max_configuration_change_pct"], PERCENT_TOL,
              f"{candidate} vs {comparator}: least favorable configuration")
        lines.append(f"{candidate} vs {comparator}: lower in {lower}/81 configurations; "
                     f"least favorable configuration {max(changes):+.3f}%")

    groups = data["seed_ratio_comparisons"]
    published = {}
    for item in groups["published_baselines"]:
        published[item["name"]] = check_summary(item["seed_ratios"], item, item["label"], worst)[0]
    strongest = max(published, key=published.get)
    if strongest != "easy_wfp3" or len(published) != 14:
        raise AssertionError("EASY-WFP3 should be the strongest of 14 published baselines")
    easy = next(i for i in groups["published_baselines"] if i["name"] == "easy_wfp3")
    for actual, expected in pairs(raw["proposed", "easy_wfp3", "all"], easy["seed_ratios"], "EASY-WFP3"):
        close(actual, expected, RATIO_TOL, "EASY-WFP3 seed ratios")
    lines.append(f"published baselines: strongest is EASY-WFP3; reductions "
                 f"{-max(published.values()):.3f}% to {-min(published.values()):.3f}%")

    controls = {item["name"]: check_summary(item["seed_ratios"], item, item["name"], worst)[0]
                for item in groups["forecast_controls"]}
    best = max(controls, key=controls.get)
    if len(controls) != 26 or best != "easy_wfp3__harmonic__calendar" or max(controls.values()) >= 0:
        raise AssertionError("forecast controls: unexpected strongest control or sign")
    matched = next(i for i in groups["forecast_controls"] if i["name"] == best)
    for actual, expected in pairs(raw["proposed", "forecast_easy_wfp3", "all"],
                                  matched["seed_ratios"], best):
        close(actual, expected, RATIO_TOL, "forecast-assisted EASY-WFP3 seed ratios")
    lines.append(f"forecast-assisted controls: all 26 favor the proposed policy; reductions "
                 f"{-max(controls.values()):.3f}% to {-min(controls.values()):.3f}%")

    grid = {}
    for item in groups["sensitivity"]:
        setting = (item["comparison_factor"], item["gain_threshold"])
        label = "sensitivity kappa={:g} eta={:g}".format(*setting)
        change = check_summary(item["vs_default"]["seed_ratios"], item["vs_default"], label, worst)[0]
        gain = -check_summary(item["vs_forecast_easy_wfp3"]["seed_ratios"],
                              item["vs_forecast_easy_wfp3"], label + " vs forecast", worst)[0]
        grid[setting] = (change, gain)
        if setting == DEFAULT and item["vs_default"]["seed_ratios"] != [1.0] * 8:
            raise AssertionError("the default setting must equal itself")
        if setting == DEFAULT:
            for actual, expected in pairs(raw["proposed", "forecast_easy_wfp3", "all"],
                                          item["vs_forecast_easy_wfp3"]["seed_ratios"], label):
                close(actual, expected, RATIO_TOL, "default vs forecast seed ratios")
        if setting[1] == 0.5:
            for actual, expected in pairs(raw["no_packing_repair", "proposed", "all"],
                                          item["vs_default"]["seed_ratios"], label):
                close(actual, expected, RATIO_TOL, label + " equals no packing repair")
    if len(grid) != 25:
        raise AssertionError("expected a 5 x 5 sensitivity grid")
    nearby = {s: v for s, v in grid.items() if s[0] in (1.5, 2.0, 3.0) and s[1] in (0.0625, 0.125, 0.25)}
    for name, subset in (("full_grid", grid), ("nearby_3x3", nearby)):
        archived = groups["sensitivity_ranges"][name]
        if archived["settings"] != len(subset):
            raise AssertionError(f"{name}: setting count")
        for key, value in (("min_change_pct", min(c for c, _ in subset.values())),
                           ("max_change_pct", max(c for c, _ in subset.values())),
                           ("min_gain_vs_matched_pct", min(g for _, g in subset.values())),
                           ("max_gain_vs_matched_pct", max(g for _, g in subset.values()))):
            close(value, archived[key], PERCENT_TOL, f"{name} {key}")
    positive = [v for s, v in grid.items() if s[1] > 0]
    zero = [c for s, (c, _) in grid.items() if s[1] == 0]
    lines.append(f"sensitivity, eta > 0 ({len(positive)} settings): change "
                 f"{min(c for c, _ in positive):+.3f}% to {max(c for c, _ in positive):+.3f}%; "
                 f"reduction vs forecast-assisted EASY-WFP3 {min(g for _, g in positive):.3f}% "
                 f"to {max(g for _, g in positive):.3f}%")
    lines.append(f"sensitivity, eta = 0 (5 settings): change {min(zero):+.3f}% to {max(zero):+.3f}%")

    single = data["single_configuration"]
    index = ids.index(single["configuration"])
    default = single["mean_response"]["default"]
    if default != runs["proposed"][index]:
        raise AssertionError("single configuration: default runs differ")
    for name, expected in single["archived_change_pct"].items():
        values = single["mean_response"][name]
        change = 100 * math.expm1(statistics.fmean(
            math.log(x / y) for x, y in pairs(values, default, name)))
        close(change, expected, PERCENT_TOL, f"single configuration {name}")
        lines.append(f"{single['configuration']} {name}: change {change:+.3f}%")

    lines.append(f"largest deviation from archived values: ratios {worst['ratio']:.1e}, "
                 f"percentages {worst['percent']:.1e}")
    return lines


def main() -> None:
    for line in verify(json.loads(DATA.read_text())):
        print(line)
    print("Verified the archived projection. No simulation was run.")


if __name__ == "__main__":
    main()
