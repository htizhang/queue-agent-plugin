"""Deterministic regression fixtures for the frozen policy."""

from __future__ import annotations

import unittest

from policy import make_policy


def _closing_state():
    setup = {
        "A": {"A": 0.0, "B": 10.0, "C": 6.0},
        "B": {"A": 10.0, "B": 0.0, "C": 5.0},
        "C": {"A": 6.0, "B": 5.0, "C": 0.0},
    }
    products = {
        "pa": {
            "probability": 0.5,
            "route": ({"station": 0, "mean_service": 1.0, "recipe": "A"},),
        },
        "pb": {
            "probability": 0.5,
            "route": ({"station": 0, "mean_service": 1.0, "recipe": "B"},),
        },
    }
    jobs = []
    for offset in range(9):
        jobs.append(
            {
                "id": 100 + offset,
                "product": "pa",
                "operation": 0,
                "station_arrival": float(offset + 1),
                "expected_current": 1.0,
                "expected_remaining": 1.0,
                "recipe": "A",
                "setup_cost": 6.0,
            }
        )
    for offset in range(3):
        jobs.append(
            {
                "id": 200 + offset,
                "product": "pb",
                "operation": 0,
                "station_arrival": float(offset),
                "expected_current": 1.0,
                "expected_remaining": 1.0,
                "recipe": "B",
                "setup_cost": 5.0,
            }
        )
    return {
        "now": 0.0,
        "bottleneck": 0,
        "setup": setup,
        "stations": ({"id": 0, "servers": 1, "recipe": "C"},),
        "products": products,
        "queues": {0: tuple(jobs)},
    }


def _setup_free_reentrant_state():
    products = {
        "returner": {
            "probability": 0.5,
            "route": (
                {"station": 0, "mean_service": 1.0},
                {"station": 1, "mean_service": 2.0},
                {"station": 0, "mean_service": 10.0},
            ),
        },
        "finisher": {
            "probability": 0.5,
            "route": ({"station": 0, "mean_service": 3.0},),
        },
    }
    jobs = (
        {
            "id": 1,
            "product": "returner",
            "operation": 0,
            "station_arrival": 0.0,
            "expected_current": 1.0,
            "expected_remaining": 13.0,
            "recipe": None,
            "setup_cost": 0.0,
        },
        {
            "id": 2,
            "product": "finisher",
            "operation": 0,
            "station_arrival": 1.0,
            "expected_current": 3.0,
            "expected_remaining": 3.0,
            "recipe": None,
            "setup_cost": 0.0,
        },
    )
    return {
        "now": 0.0,
        "bottleneck": 1,
        "setup": {},
        "stations": (
            {"id": 0, "servers": 1, "recipe": None},
            {"id": 1, "servers": 1, "recipe": None},
        ),
        "products": products,
        "queues": {0: jobs, 1: ()},
    }


def _fifo_state():
    products = {
        "p": {
            "probability": 1.0,
            "route": ({"station": 0, "mean_service": 1.0, "recipe": "A"},),
        }
    }
    jobs = (
        {
            "id": 8,
            "product": "p",
            "operation": 0,
            "station_arrival": 5.0,
            "expected_current": 1.0,
            "expected_remaining": 1.0,
            "recipe": "A",
            "setup_cost": 0.0,
        },
        {
            "id": 7,
            "product": "p",
            "operation": 0,
            "station_arrival": 2.0,
            "expected_current": 1.0,
            "expected_remaining": 1.0,
            "recipe": "A",
            "setup_cost": 0.0,
        },
    )
    return {
        "now": 0.0,
        "bottleneck": 0,
        "setup": {"A": {"A": 0.0}},
        "stations": ({"id": 0, "servers": 1, "recipe": "A"},),
        "products": products,
        "queues": {0: jobs},
    }


class FrozenPolicyRegression(unittest.TestCase):
    def test_closing_cost_selects_the_lower_continuation_orientation(self):
        policy = make_policy()
        state = _closing_state()

        # For equal processing times, the closed orientation costs are
        # 12*6 + 3*10 = 102 for A first and 12*5 + 9*10 = 150 for B first.
        self.assertLess(12 * 6 + 3 * 10, 12 * 5 + 9 * 10)
        self.assertEqual(policy(state, 0), 100)
        self.assertEqual(
            policy.tracker[0],
            {"busy": 47.0, "span": 57.0, "end": 7.0, "n": 1},
        )

    def test_setup_free_choice_counts_later_returns(self):
        policy = make_policy()
        self.assertEqual(policy(_setup_free_reentrant_state(), 0), 2)

    def test_equal_scores_use_station_arrival_then_identifier(self):
        policy = make_policy()
        self.assertEqual(policy(_fifo_state(), 0), 7)

    def test_factories_do_not_share_tracker_state(self):
        first = make_policy()
        second = make_policy()
        first(_fifo_state(), 0)
        self.assertTrue(first.tracker)
        self.assertEqual(second.tracker, {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
