"""Deterministic regression checks for the portable policy.

The 300-state table records decisions from the evaluated source. Hand-built
fixtures also check mechanisms and parameter overrides. The checks use only
the standard library and this directory.
They test decisions, not performance.
"""

from __future__ import annotations

import copy
import math
import random
import unittest
from collections import Counter

from policy import choose, planning_duration


def job(job_id, width, estimate, class_id, arrival=0.0):
    return {"id": job_id, "arrival": arrival, "width": width,
            "estimate": estimate, "class_id": class_id}


def running(job_id, width, estimate, elapsed):
    return {"id": job_id, "width": width, "estimate": estimate, "elapsed": elapsed}


def state(capacity, free, waiting, running_jobs=(), classes=None, time=0.0):
    return {"time": time, "capacity": capacity, "free": free, "waiting": list(waiting),
            "running": list(running_jobs), "classes": classes or {}}


def start_jobs(current, starts):
    """Return the state after the caller starts the jobs at the same time."""
    chosen = set(starts)
    started = [item for item in current["waiting"] if item["id"] in chosen]
    return dict(
        current,
        free=current["free"] - sum(item["width"] for item in started),
        waiting=[item for item in current["waiting"] if item["id"] not in chosen],
        running=current["running"] + [dict(item, elapsed=0.0) for item in started],
    )


def repeated_calls(test, current, limit=100):
    """Call the policy at one time until it starts no job, as the evaluator did."""
    batches = []
    for _ in range(limit):
        if not current["waiting"]:
            break
        before = copy.deepcopy(current)
        starts = choose(current, {})
        test.assertEqual(current, before, "the policy must not modify its input")
        waiting = {item["id"]: item for item in current["waiting"]}
        test.assertEqual(len(starts), len(set(starts)))
        test.assertTrue(all(item in waiting for item in starts))
        test.assertLessEqual(sum(waiting[item]["width"] for item in starts), current["free"])
        if not starts:
            break
        batches.append(starts)
        current = start_jobs(current, starts)
    return batches


# Seeded states for the recorded-decision check. Keep this generator unchanged:
# it uses only random.Random.random, which is stable across Python versions.
ESTIMATES = (1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0)


def seeded_state(seed: int) -> dict:
    """Return a small state with integer-valued times, ties, and shared widths."""
    rng = random.Random(seed)

    def pick(values):
        return values[int(rng.random() * len(values))]

    capacity = pick((4, 6, 8, 10, 12, 16, 32))
    widths = sorted({1, 2, 3, capacity // 4, capacity // 2, 3 * capacity // 4,
                     capacity - 1, capacity} - {0})
    classes = {name: {"mean": pick(ESTIMATES[:7])} for name in "abcd"[: 1 + int(rng.random() * 4)]}
    now = float(int(rng.random() * 50))
    running, used = [], 0
    for index in range(int(rng.random() * 5)):
        width = pick(widths)
        if used + width <= capacity:
            used += width
            estimate = pick(ESTIMATES)
            running.append({"id": 1000 + index, "width": width, "estimate": estimate,
                            "elapsed": float(int(rng.random() * (estimate + 2)))})
    free = capacity - used
    count = 1 + int(rng.random() * 12)
    ids = list(range(100, 100 + count))
    for k in range(count - 1, 0, -1):
        j = int(rng.random() * (k + 1))
        ids[k], ids[j] = ids[j], ids[k]
    waiting = [{"id": ids[k], "arrival": now - pick((0, 1, 2, 3, 5, 8)), "width": pick(widths),
                "estimate": pick(ESTIMATES), "class_id": pick(sorted(classes))}
               for k in range(count)]
    if rng.random() < 0.35 and count >= 3 and free >= 4:
        # A short wide job, then equal-width jobs that fill the free pool exactly.
        k = pick((2, 2, 3))
        wide = free // 2 + 1
        waiting[0].update(width=wide, estimate=pick((1.0, 2.0)))
        for item in waiting[1 : 1 + k]:
            item.update(width=free // k, estimate=pick((2.0, 3.0, 4.0)))
        for item in waiting[1 + k :]:
            item["width"] = min(capacity, free - wide + 1 + int(rng.random() * 4))
    return {"time": now, "capacity": capacity, "free": free, "waiting": waiting,
            "running": running, "classes": classes}


# Recorded source decisions for seeds 0-299, one token per seed. A token lists
# the batches of one repeated-call sequence: "/" separates calls, "," separates
# job IDs, and "-" means that the first call started no job.
RECORDED = """
100 - 100 100 101/102 100 105 101 104 - - 104,103 105 100/101 100 - 102 100 100
100,102 - - 100 101,102 101 - 103,101 105 102 100 102,105 100,101 103 107,102 106
103 111 - 101,100 - - 100 - - 100 101/103 101,102 100 105 100 100,103 100 100 -
106,105,101 100 101,107,105 104 104,105 102,109 109 - - - 101 107,101 - - - - 107
100 - 100 107,102 100 - 103,101 103,107,102 102,103 109 105,101 101 - - - 100
106,100 - - - - - 100 100,104 100 101 100 105/103 106,101 - - - 106/103 100,102 -
101 103 101 - 103 104 102,100 - 103 - 102 108 106 100,103 - 105 - - 101,100
109,104,106/103 100,101 - 100,101 101 101 103/102 - 107/104 - - 102/101 - 107 105
102/105,104 - 103 - 100,104 - 105,107/100 100 100,103 - 101 104 - - - 105 105/100 -
- - - - - 101,102 100,101 - - 101 - - 100/101 106 101,100 - - - 101,103 102 106 102
101,100 102,100,103,101 101 - - 101,100/104 - 100 - - - 107 - - - - - 105 - - - 101
- - - - - 100 102 101 100 102,103 - 104 101/110 - - 102,101 - 100 103 106 100 - -
108,105 - 101 107,100 - - - 104 - - 100 103,102,106 - 105,102 - - 101 - 100 - -
100,101 110 - - 103,102 100,105 108 - 107 102 101,100 110 100 105 100 101/104
105/103 - - - - 101/107 100 103,102 - - 100,102,101 105,107 109 - 102,103 100,102
101,104,103,102 - - 100 100,103 - - 109 100 100 100 105 - - - - - 101 100,101 100
106 -
"""


def worked_example():
    return state(8, 4, [job(1, 6, 12.0, "A", -2.0), job(2, 2, 22.0, "B", -1.0),
                        job(3, 2, 22.0, "B", 0.0)],
                 [running(9, 4, 10.0, 0.0)], {"A": {"mean": 12.0}, "B": {"mean": 22.0}})


class PlanningDurationTest(unittest.TestCase):
    def test_harmonic_expression_and_count_discount(self):
        # Request 120 and class mean 60 give 40, as in the description.
        classes = {"c": {"mean": 60.0}}
        alone = job(1, 4, 120.0, "c")
        self.assertEqual(planning_duration(alone, 8, Counter({4: 1}), classes), 40.0)
        self.assertEqual(planning_duration(alone, 8, Counter({4: 4}), classes), 20.0)
        for width, capacity in ((1, 32), (1, 8), (3, 4)):
            item = job(1, width, 120.0, "c")
            expected = 40.0 * 4.0 ** (-width / capacity)
            actual = planning_duration(item, capacity, Counter({width: 4}), classes)
            self.assertTrue(math.isclose(actual, expected, rel_tol=1e-15))

    def test_missing_mean_uses_the_request(self):
        item = job(1, 2, 10.0, "unknown")
        self.assertEqual(planning_duration(item, 8, Counter({2: 1}), {}), 5.0)
        self.assertEqual(planning_duration(item, 8, Counter({2: 1}), {"unknown": {}}), 5.0)

    def test_duration_floor(self):
        item = job(1, 2, 1e-12, "c")
        self.assertEqual(planning_duration(item, 8, Counter({2: 1}), {"c": {"mean": 1.0}}), 1e-9)


class DecisionTest(unittest.TestCase):
    def test_worked_example(self):
        current = worked_example()
        self.assertTrue(all(j["arrival"] <= current["time"] for j in current["waiting"]))
        counts = Counter(item["width"] for item in current["waiting"])
        durations = [planning_duration(item, 8, counts, current["classes"])
                     for item in current["waiting"]]
        self.assertEqual(durations[0], 6.0)
        self.assertTrue(math.isclose(durations[1], 11.0 * 2.0 ** -0.25, rel_tol=1e-15))
        self.assertLess(durations[1], 10.0)  # ends before job 1's reservation
        self.assertEqual(choose(current, {}), [2, 3])

    def test_packing_repair_promotes_two_width_four_jobs(self):
        current = state(8, 8, [job(1, 5, 2.0, "A"), job(2, 4, 4.0, "B", 1.0),
                               job(3, 4, 4.0, "B", 2.0)],
                        classes={"A": {"mean": 2.0}, "B": {"mean": 4.0}})
        self.assertEqual(choose(current, {}), [2, 3])

    def test_counts_group_jobs_by_width_not_class(self):
        current = state(4, 4, [job(1, 2, 2.0, "x"), job(2, 2, 2.0, "y", 1.0),
                               job(3, 4, 4.0, "z", 2.0)],
                        classes={"x": {"mean": 2.0}, "y": {"mean": 6.0}, "z": {"mean": 4.0}})
        self.assertEqual(choose(current, {}), [1, 2])

    def test_every_blocked_job_receives_a_reservation(self):
        blocked = [job(k, 3, 8.0, "w", float(k)) for k in range(1, 7)]
        seventh = job(7, 4, 8.0, "w", 7.0)
        long_job = job(8, 1, 40.0, "n", 8.0)
        classes = {"w": {"mean": 8.0}, "n": {"mean": 40.0}}
        busy = [running(9, 3, 10.0, 0.0)]
        # The seventh reservation blocks the long width-one job.
        self.assertEqual(choose(state(4, 1, blocked + [seventh, long_job], busy, classes), {}), [])
        self.assertEqual(choose(state(4, 1, blocked + [long_job], busy, classes), {}), [8])

    def test_planning_intervals_are_half_open(self):
        # Job 2 plans [0, 10). Job 1's reservation starts at 10, so they do not overlap.
        current = state(8, 4, [job(1, 6, 12.0, "A"), job(2, 4, 30.0, "B", 1.0)],
                        [running(9, 4, 10.0, 0.0)], {"A": {"mean": 12.0}, "B": {"mean": 15.0}})
        self.assertEqual(choose(current, {}), [2])

    def test_thresholds_are_inclusive_and_adjustable(self):
        # Request 6 equals 2 * 3, and a gain of 1 server equals 8 / 8.
        current = state(8, 8, [job(1, 5, 6.0, "A", -5.0), job(2, 4, 3.0, "A", -5.0)],
                        classes={"A": {"mean": 3.0}})
        self.assertEqual(choose(current, {}), [1])
        self.assertEqual(choose(current, {}, comparison_factor=1.0), [2])
        self.assertEqual(choose(current, {}, gain_threshold=0.25), [2])

    def test_subset_search_keeps_the_first_discovered_subset(self):
        current = state(16, 16, [job(1, 9, 1.0, "a")]
                        + [job(k, 8, 2.0, "b", float(k)) for k in (2, 3)]
                        + [job(k, 4, 2.0, "c", float(k)) for k in (4, 5, 6, 7)],
                        classes={"a": {"mean": 1.0}, "b": {"mean": 2.0}, "c": {"mean": 2.0}})
        self.assertEqual(choose(current, {}), [2, 3])

    def test_ties_break_by_arrival_then_id(self):
        jobs = [job(6, 3, 4.0, "A", -2.0), job(5, 3, 4.0, "A", -1.0)]
        classes = {"A": {"mean": 4.0}}
        self.assertEqual(choose(state(4, 4, jobs, classes=classes), {}), [6])
        same_arrival = [dict(item, arrival=-1.0) for item in jobs]
        self.assertEqual(choose(state(4, 4, same_arrival, classes=classes), {}), [5])

    def test_physical_fit_is_checked_with_the_calendar(self):
        # At this clock value the overdue job's release rounds to the current time.
        now = 1e12
        current = state(8, 7, [job(1, 2, 2.0, "A", now - 100.0), job(2, 6, 3.0, "A", now - 10.0)],
                        [running(9, 1, 16.0, 20.5)], {"A": {"mean": 4.0}}, time=now)
        self.assertEqual(choose(current, {}), [2])

    def test_repeated_calls_at_the_same_time(self):
        current = state(8, 8, [job(100, 2, 1.0, "0", -8.0), job(101, 8, 16.0, "1", -3.0),
                               job(108, 3, 8.0, "0", -8.0)],
                        classes={"0": {"mean": 8}, "1": {"mean": 6}})
        self.assertEqual(repeated_calls(self, current), [[100], [108]])

    def test_empty_queue(self):
        self.assertEqual(choose(state(4, 4, []), {}), [])

    def test_seeded_states_match_recorded_source_decisions(self):
        tokens = RECORDED.split()
        self.assertEqual(len(tokens), 300)
        for seed, token in enumerate(tokens):
            batches = repeated_calls(self, seeded_state(seed))
            actual = "/".join(",".join(str(item) for item in batch) for batch in batches)
            with self.subTest(seed=seed):
                self.assertEqual(actual or "-", token)


if __name__ == "__main__":
    unittest.main(verbosity=2)
