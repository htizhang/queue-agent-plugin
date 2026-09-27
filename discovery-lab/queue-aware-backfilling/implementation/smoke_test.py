"""Deterministic regression checks for the portable policy."""

from __future__ import annotations

import math
import unittest
from collections import Counter

from policy import PLANNING_SCALE, choose, planning_duration


def job(
    job_id: int,
    width: int,
    estimate: float,
    class_id: str,
) -> dict:
    return {
        "id": job_id,
        "arrival": 0.0,
        "width": width,
        "estimate": estimate,
        "class_id": class_id,
    }


class QueueAwareBackfillingSmokeTest(unittest.TestCase):
    def test_queue_count_controls_planning_duration(self) -> None:
        candidate = job(1, 4, 9.0, "a")
        common = planning_duration(candidate, 12, Counter({4: 3, 2: 1}))
        rare = planning_duration(candidate, 12, Counter({4: 1, 2: 3}))

        expected_common = 9.0 * PLANNING_SCALE * 3.0**-0.5
        self.assertTrue(math.isclose(common, expected_common))
        self.assertLess(common, rare)

    def test_packing_repair_promotes_two_width_four_jobs(self) -> None:
        state = {
            "time": 0.0,
            "capacity": 8,
            "free": 8,
            "waiting": [
                job(1, 6, 1.0, "wide"),
                job(2, 4, 1.0, "narrow-a"),
                job(3, 4, 1.0, "narrow-b"),
            ],
            "running": [],
            "classes": {},
        }

        self.assertEqual(choose(state, {}), [2, 3])

    def test_shortened_window_backfills_before_raw_running_release(self) -> None:
        pivot = job(1, 10, 1.0, "pivot")
        first = job(2, 4, 6.0, "backfill")
        second = job(3, 4, 6.0, "backfill")
        state = {
            "time": 0.0,
            "capacity": 10,
            "free": 4,
            "waiting": [pivot, first, second],
            "running": [
                {
                    **job(90, 6, 2.0, "running"),
                    "elapsed": 0.0,
                }
            ],
            "classes": {},
        }

        window = planning_duration(
            first,
            state["capacity"],
            Counter(item["width"] for item in state["waiting"]),
        )
        self.assertLess(window, 2.0)
        self.assertGreater(first["estimate"] * PLANNING_SCALE, 2.0)
        self.assertEqual(choose(state, {}), [2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
