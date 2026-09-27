"""Verify the archived mean-response projection and reproduce its aggregates."""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any


DATA = Path(__file__).with_name("archived_mean_response.json")
COMPARATORS = (
    "easy_wfp3",
    "selective_reservation",
    "uniform_calendar",
    "selective_duration",
    "constant_discount_ablation",
)
SOURCE_HASHES = {
    "paired_analysis_sha256": (
        "820efb9f6c4ef592f4065c9197a8c26928580e1e304d3ebf17f45b74a5600441"
    ),
    "protocol_sha256": (
        "d5166ecda499a4c32436fe9bb858983f451208e8d8a60575d47a4348c49bca7a"
    ),
    "simulation_result_sha256": (
        "81d8929f1f7dd828f2312c65a1223e44c5ec5f8a19cdc752b9376ca7e7cc5dbb"
    ),
}
ABS_TOL = 5e-15


def close(actual: float, expected: float, label: str) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=ABS_TOL):
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")


def bootstrap_interval(ratios: list[float]) -> list[float]:
    rng = random.Random(20260920)
    samples = sorted(
        statistics.fmean(rng.choices(ratios, k=len(ratios))) for _ in range(10_000)
    )
    return [samples[249], samples[9749]]


def verify(data: dict[str, Any], include_bootstrap: bool) -> int:
    if data["status"] != "archived_projection":
        raise AssertionError("evidence must be marked archived_projection")
    if data["metric"] != "mean_response":
        raise AssertionError("unexpected metric")
    for source, expected_hash in SOURCE_HASHES.items():
        if data["source"].get(source) != expected_hash:
            raise AssertionError(f"{source}: hash does not match frozen provenance")

    seeds = data["seeds"]
    if len(seeds) != 20 or len(set(seeds)) != 20:
        raise AssertionError("expected 20 unique seeds")
    if set(data["grids"]) != {"capacity", "width"}:
        raise AssertionError("expected capacity and width grids")

    values_checked = 0
    for grid_name, grid in data["grids"].items():
        if grid["cases"] != (45 if grid_name == "capacity" else 36):
            raise AssertionError(f"{grid_name}: unexpected case count")
        comparisons = grid["comparisons"]
        if tuple(comparisons) != COMPARATORS:
            raise AssertionError(f"{grid_name}: unexpected comparator order")

        for comparator in COMPARATORS:
            item = comparisons[comparator]
            ratios = item["seed_ratios"]
            reported = item["reported"]
            if len(ratios) != len(seeds):
                raise AssertionError(f"{grid_name}/{comparator}: ratio count")
            if not all(math.isfinite(value) and value > 0 for value in ratios):
                raise AssertionError(f"{grid_name}/{comparator}: invalid ratio")

            ratio = statistics.fmean(ratios)
            reduction = 100.0 * (1.0 - ratio)
            wins = sum(value < 1.0 for value in ratios)
            close(ratio, reported["ratio"], f"{grid_name}/{comparator}/ratio")
            close(
                reduction,
                reported["reduction_percent"],
                f"{grid_name}/{comparator}/reduction",
            )
            if wins != reported["seed_blocks_won"]:
                raise AssertionError(f"{grid_name}/{comparator}: seed-win count")
            if (ratio < 1.0) != (reduction > 0.0):
                raise AssertionError(f"{grid_name}/{comparator}: direction")
            if ratio >= 1.0:
                raise AssertionError(
                    f"{grid_name}/{comparator}: expected candidate-lower direction"
                )

            if include_bootstrap:
                interval = bootstrap_interval(ratios)
                for index, value in enumerate(interval):
                    close(
                        value,
                        reported["ratio_ci95"][index],
                        f"{grid_name}/{comparator}/ratio_ci95[{index}]",
                    )
                reduction_interval = [
                    100.0 * (1.0 - interval[1]),
                    100.0 * (1.0 - interval[0]),
                ]
                for index, value in enumerate(reduction_interval):
                    close(
                        value,
                        reported["reduction_ci95"][index],
                        f"{grid_name}/{comparator}/reduction_ci95[{index}]",
                    )

            values_checked += len(ratios)
            print(
                f"{grid_name:8} {comparator:28} "
                f"ratio={ratio:.17g} reduction={reduction:.17g}% "
                f"seed_blocks={wins}/{len(ratios)}"
            )
    return values_checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="also reproduce the archived 10,000-resample confidence intervals",
    )
    args = parser.parse_args()
    data = json.loads(DATA.read_text())
    values_checked = verify(data, args.bootstrap)
    suffix = " including bootstrap intervals" if args.bootstrap else ""
    print(f"Verified {values_checked} archived seed ratios{suffix}.")


if __name__ == "__main__":
    main()
