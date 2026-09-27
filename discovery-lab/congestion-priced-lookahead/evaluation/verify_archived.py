"""Verify the bundled ARCHIVED candidate-versus-normalized-PR projection."""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path


ARTIFACT = Path(__file__).with_name("archived-paired-comparison.json")
SOURCE_SHA256 = "0300764dbbe599a372e8b19d33cd9773c45e581c6437ac8289a146e2c9fe80d8"
CANDIDATE_SPEC = "p:shadow_close_v1/close=1.0,close_basis=rest"
REFERENCE_SPEC = "l:PR/b=16,units=mean"

EXPECTED_CANDIDATE_MEAN = 192.84124744879773
EXPECTED_REFERENCE_MEAN = 204.9489619184429
EXPECTED_REDUCTION_PERCENT = 5.907672991514493
EXPECTED_CONFIGURATIONS = 27
EXPECTED_SEEDS = 8
EXPECTED_PAIRS = 216
EXPECTED_LOWER = 199
EXPECTED_EQUAL = 0
EXPECTED_HIGHER = 17
EXPECTED_CONFIGURATION_MEANS_LOWER = 27
COMPARISON_TOLERANCE = 1e-10


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def require_close(actual, expected, label):
    require(
        math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-12),
        f"{label}: expected {expected!r}, got {actual!r}",
    )


def main():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    source = data["source"]
    projection = source["field_projection"]

    require(data["artifact_status"] == "ARCHIVED", "artifact status changed")
    require(source["file"] == "fresh.json", "source filename changed")
    require(source["sha256"] == SOURCE_SHA256, "source hash changed")
    require(source["source_records"] == 4104, "source record count changed")
    require(source["projected_records"] == 432, "projection record count changed")
    require(
        projection
        == {
            "row_filter": [CANDIDATE_SPEC, REFERENCE_SPEC],
            "pair_key": ["case", "seed"],
            "value": "mean_flow",
            "validity_filter": "valid == true",
        },
        "field projection changed",
    )
    require(data["candidate_spec"] == CANDIDATE_SPEC, "candidate spec changed")
    require(data["reference_spec"] == REFERENCE_SPEC, "reference spec changed")

    seeds = data["seeds"]
    configurations = data["configurations"]
    require(len(seeds) == EXPECTED_SEEDS, "unexpected seed count")
    require(len(set(seeds)) == EXPECTED_SEEDS, "seed identifiers are not unique")
    require(
        len(configurations) == EXPECTED_CONFIGURATIONS,
        "unexpected configuration count",
    )
    require(
        len({record["id"] for record in configurations}) == EXPECTED_CONFIGURATIONS,
        "configuration identifiers are not unique",
    )

    candidate_values = []
    reference_values = []
    configuration_means_lower = 0
    for record in configurations:
        candidate = record["candidate_mean_flow"]
        reference = record["normalized_pr_mean_flow"]
        require(len(candidate) == len(seeds), f"{record['id']}: candidate length")
        require(len(reference) == len(seeds), f"{record['id']}: reference length")
        require(
            all(
                isinstance(value, (int, float)) and math.isfinite(value) and value > 0.0
                for value in candidate + reference
            ),
            f"{record['id']}: invalid mean-flow value",
        )
        candidate_values.extend(candidate)
        reference_values.extend(reference)
        if (
            statistics.fmean(candidate)
            < statistics.fmean(reference) - COMPARISON_TOLERANCE
        ):
            configuration_means_lower += 1

    require(len(candidate_values) == EXPECTED_PAIRS, "candidate pair count")
    require(len(reference_values) == EXPECTED_PAIRS, "reference pair count")

    candidate_mean = statistics.fmean(candidate_values)
    reference_mean = statistics.fmean(reference_values)
    reduction_percent = 100.0 * (reference_mean - candidate_mean) / reference_mean

    lower = sum(
        candidate < reference - COMPARISON_TOLERANCE
        for candidate, reference in zip(candidate_values, reference_values)
    )
    equal = sum(
        abs(candidate - reference) <= COMPARISON_TOLERANCE
        for candidate, reference in zip(candidate_values, reference_values)
    )
    higher = sum(
        candidate > reference + COMPARISON_TOLERANCE
        for candidate, reference in zip(candidate_values, reference_values)
    )

    require_close(
        candidate_mean,
        EXPECTED_CANDIDATE_MEAN,
        "candidate aggregate mean",
    )
    require_close(
        reference_mean,
        EXPECTED_REFERENCE_MEAN,
        "normalized PR aggregate mean",
    )
    require_close(
        reduction_percent,
        EXPECTED_REDUCTION_PERCENT,
        "aggregate reduction percent",
    )
    require(
        (lower, equal, higher) == (EXPECTED_LOWER, EXPECTED_EQUAL, EXPECTED_HIGHER),
        "paired direction counts changed",
    )
    require(
        configuration_means_lower == EXPECTED_CONFIGURATION_MEANS_LOWER,
        "configuration-level direction count changed",
    )

    print("ARCHIVED paired comparison verified")
    print(
        f"pairs: {EXPECTED_PAIRS} "
        f"({EXPECTED_CONFIGURATIONS} configurations x {EXPECTED_SEEDS} seeds)"
    )
    print(f"candidate mean: {candidate_mean!r}")
    print(f"normalized PR mean: {reference_mean!r}")
    print(f"candidate reduction: {reduction_percent!r}%")
    print(f"paired lower/equal/higher: {lower}/{equal}/{higher}")
    print(
        "configuration means lower: "
        f"{configuration_means_lower}/{EXPECTED_CONFIGURATIONS}"
    )


if __name__ == "__main__":
    main()
