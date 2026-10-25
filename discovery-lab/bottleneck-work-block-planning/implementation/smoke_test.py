"""Deterministic checks for the portable bottleneck-work block planner.

Run from this entry's directory with Python 3.10 or later:

    python3 implementation/smoke_test.py

The fixtures use small numbers, so each expected choice can be checked by hand.
An independent brute-force oracle in this file enumerates every block order.
These checks test the policy logic. They do not rerun the simulation study.
"""

from __future__ import annotations

import copy
import itertools
import math
import random
import unittest
from types import MappingProxyType

from policy import BETA, make_policy

BOTTLENECK = 0
OTHER = 1
SYMMETRIC_AB = {"A": {"A": 0.0, "B": 1.0}, "B": {"A": 1.0, "B": 0.0}}


# ---------------------------------------------------------------- state builders


def route(*operations):
    """Each operation is (station, mean service) or (station, mean service, recipe)."""
    result = []
    for operation in operations:
        entry = {"station": operation[0], "mean_service": float(operation[1])}
        if len(operation) > 2:
            entry["recipe"] = operation[2]
        result.append(entry)
    return tuple(result)


def products(**routes):
    share = 1.0 / len(routes)
    return {
        name: {"probability": share, "route": path} for name, path in routes.items()
    }


def make_state(
    catalog, setup, recipe, waiting, *, station=BOTTLENECK, bottleneck=BOTTLENECK
):
    """Build a simulator-shaped state with one nonempty queue.

    ``waiting`` holds (job id, product, operation index, station arrival).
    """
    queue = []
    for job_id, product, operation, arrival in waiting:
        path = catalog[product]["route"]
        current = path[operation]
        job_recipe = current.get("recipe")
        immediate = (
            setup[recipe][job_recipe] if recipe is not None and job_recipe else 0.0
        )
        queue.append(
            {
                "id": job_id,
                "product": product,
                "operation": operation,
                "network_arrival": arrival,
                "station_arrival": arrival,
                "expected_current": current["mean_service"],
                "expected_remaining": sum(
                    op["mean_service"] for op in path[operation:]
                ),
                "recipe": job_recipe,
                "setup_cost": immediate,
            }
        )
    return {
        "now": 100.0,
        "bottleneck": bottleneck,
        "setup": setup,
        "stations": tuple(
            {
                "id": index,
                "servers": 1,
                "free": 1,
                "recipe": recipe if index == bottleneck else None,
                "run_length": 0,
            }
            for index in (BOTTLENECK, OTHER)
        ),
        "products": catalog,
        "queues": {
            index: tuple(queue) if index == station else ()
            for index in (BOTTLENECK, OTHER)
        },
        "running": (),
    }


def read_only(value):
    if isinstance(value, dict):
        return MappingProxyType({key: read_only(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(read_only(item) for item in value)
    return value


# ---------------------------------------------------------------- fixtures


def report_example():
    """The worked example: one A job with long return work, two short B jobs."""
    catalog = products(
        PA=route((0, 1, "A"), (1, 2), (0, 19, "A")),
        PB=route((0, 4, "B"), (1, 2)),
    )
    waiting = [(1, "PA", 0, 0.0), (2, "PB", 0, 2.0), (3, "PB", 0, 1.0)]
    return make_state(catalog, SYMMETRIC_AB, "A", waiting), BOTTLENECK


def setup_free_station():
    catalog = products(
        R=route((0, 1, "A"), (1, 2), (0, 30, "A")),
        S=route((0, 1, "B"), (1, 3)),
        T=route((0, 1, "A"), (1, 2)),
    )
    waiting = [
        (11, "S", 1, 0.0),
        (12, "R", 1, 4.0),
        (13, "T", 1, 4.0),
        (10, "T", 1, 6.0),
    ]
    return make_state(catalog, SYMMETRIC_AB, "A", waiting, station=OTHER), OTHER


def route_reentry():
    catalog = products(
        RET=route((0, 2, "A"), (1, 5), (0, 9, "B")),
        FIN=route((0, 2, "A"), (1, 30)),
    )
    waiting = [(21, "RET", 0, 0.0), (22, "FIN", 0, 1.0)]
    return make_state(catalog, SYMMETRIC_AB, "A", waiting), BOTTLENECK


def same_recipe_blocks():
    catalog = products(
        P=route((0, 2, "A"), (1, 4), (0, 18, "B")),
        Q=route((0, 5, "B"), (1, 1), (0, 3, "A")),
        S=route((0, 4, "B"), (1, 2)),
    )
    waiting = [
        (31, "P", 0, 0.0),
        (32, "Q", 2, 5.0),
        (33, "S", 0, 1.0),
        (34, "S", 0, 2.0),
    ]
    return make_state(catalog, SYMMETRIC_AB, "A", waiting), BOTTLENECK


ASYMMETRIC_ABC = {
    "A": {"A": 0.0, "B": 3.0, "C": 1.0},
    "B": {"A": 1.0, "B": 0.0, "C": 1.0},
    "C": {"A": 1.0, "B": 1.0, "C": 0.0},
}


def transpose(matrix):
    return {row: {column: matrix[column][row] for column in matrix} for row in matrix}


def two_recipe_choice(setup):
    catalog = products(PA=route((0, 5, "A")), PB=route((0, 5, "B")))
    waiting = [(41, "PA", 0, 0.0), (42, "PB", 0, 1.0)]
    return make_state(catalog, setup, "C", waiting), BOTTLENECK


def asymmetric():
    return two_recipe_choice(ASYMMETRIC_ABC)


def asymmetric_transposed():
    return two_recipe_choice(transpose(ASYMMETRIC_ABC))


def asymmetric_symmetrized():
    setup = copy.deepcopy(ASYMMETRIC_ABC)
    setup["A"]["B"] = 1.0
    return two_recipe_choice(setup)


def tie_states(waiting):
    catalog = products(X=route((0, 3, "A")), Y=route((0, 3, "A")))
    return make_state(catalog, SYMMETRIC_AB, "A", waiting), BOTTLENECK


def tie_by_arrival():
    return tie_states([(50, "X", 0, 2.0), (60, "Y", 0, 1.0)])


def tie_by_identifier():
    return tie_states([(60, "Y", 0, 1.0), (50, "X", 0, 1.0)])


def tie_within_block():
    return tie_states(
        [(72, "X", 0, 5.0), (70, "X", 0, 5.0), (73, "X", 0, 4.0), (71, "X", 0, 4.0)]
    )


def recipe_b_backlog(count):
    catalog = products(LONG=route((0, 6, "A")), SHORT=route((0, 1, "B")))
    waiting = [(81, "LONG", 0, 0.0)]
    waiting += [(82 + index, "SHORT", 0, 1.0 + index) for index in range(count)]
    return make_state(catalog, SYMMETRIC_AB, "A", waiting), BOTTLENECK


def three_b_jobs():
    return recipe_b_backlog(3)


def four_b_jobs():
    return recipe_b_backlog(4)


LOOKAHEAD_SETUP = {
    "A": {"A": 0.0, "B": 1.0, "C": 2.0},
    "B": {"A": 1.0, "B": 0.0, "C": 6.0},
    "C": {"A": 1.0, "B": 1.0, "C": 0.0},
}


def cheap_first_change():
    catalog = products(PB=route((0, 1, "B")), PC=route((0, 1, "C")))
    waiting = [
        (91, "PB", 0, 0.0),
        (92, "PC", 0, 1.0),
        (93, "PC", 0, 2.0),
        (94, "PC", 0, 3.0),
    ]
    return make_state(catalog, LOOKAHEAD_SETUP, "A", waiting), BOTTLENECK


def missing_recipe(count):
    catalog = products(PA=route((0, 2, "A")), PB=route((0, 1, "B")))
    waiting = [(101, "PA", 0, 0.0), (102, "PB", 0, 1.0)][:count]
    return make_state(catalog, SYMMETRIC_AB, None, waiting), BOTTLENECK


def missing_recipe_single():
    return missing_recipe(1)


def missing_recipe_pair():
    return missing_recipe(2)


# (name, builder, beta, expected job id or exception type).
FIXTURES = (
    ("report_example", report_example, 8.0, 3),
    ("setup_free_station", setup_free_station, 8.0, 12),
    ("route_reentry", route_reentry, 8.0, 22),
    ("same_recipe_blocks", same_recipe_blocks, 8.0, 32),
    ("asymmetric", asymmetric, 8.0, 42),
    ("asymmetric_transposed", asymmetric_transposed, 8.0, 41),
    ("asymmetric_symmetrized", asymmetric_symmetrized, 8.0, 41),
    ("tie_by_arrival", tie_by_arrival, 8.0, 60),
    ("tie_by_identifier", tie_by_identifier, 8.0, 50),
    ("tie_within_block", tie_within_block, 8.0, 71),
    ("three_b_jobs", three_b_jobs, 8.0, 81),
    ("four_b_jobs", four_b_jobs, 8.0, 82),
    ("three_b_jobs_beta_1", three_b_jobs, 1.0, 82),
    ("cheap_first_change", cheap_first_change, 8.0, 92),
    ("missing_recipe_single", missing_recipe_single, 8.0, 101),
    ("missing_recipe_pair", missing_recipe_pair, 8.0, KeyError),
)


# ---------------------------------------------------------------- independent oracle


def blocks_of(state, station_id):
    groups = {}
    for job in state["queues"][station_id]:
        path = state["products"][job["product"]]["route"]
        work = sum(
            op["mean_service"]
            for op in path[job["operation"] :]
            if op["station"] == station_id
        )
        groups.setdefault((job["recipe"], job["product"], job["operation"]), []).append(
            (job, work)
        )
    blocks = []
    for (recipe, product, operation), members in groups.items():
        first = min(
            (job for job, _ in members),
            key=lambda job: (job["station_arrival"], job["id"]),
        )
        blocks.append(
            {
                "recipe": recipe,
                "product": product,
                "operation": operation,
                "count": len(members),
                "work": sum(work for _, work in members),
                "first": first,
            }
        )
    return blocks


def order_cost(state, station_id, blocks, order, beta):
    """K_beta for one complete block order, summed from the first block."""
    setup = state["setup"]
    last = state["stations"][station_id]["recipe"]
    waiting = sum(block["count"] for block in blocks)
    cost = 0.0
    for index in order:
        block = blocks[index]
        cost += (
            waiting * beta * setup[last][block["recipe"]]
            + (waiting - block["count"]) * block["work"]
        )
        waiting -= block["count"]
        last = block["recipe"]
    return cost


def brute_force_choice(state, station_id, beta):
    blocks = blocks_of(state, station_id)
    candidates = []
    for order in itertools.permutations(range(len(blocks))):
        first = blocks[order[0]]["first"]
        cost = order_cost(state, station_id, blocks, order, beta)
        candidates.append((cost, first["station_arrival"], first["id"]))
    return min(candidates)[2]


def cost_by_products(state, station_id, beta, sequence):
    blocks = blocks_of(state, station_id)
    order = [
        next(i for i, block in enumerate(blocks) if block["product"] == name)
        for name in sequence
    ]
    return order_cost(state, station_id, blocks, order, beta)


def virtual_completions(state, station_id, beta, sequence):
    """Virtual completion times: job j lasts w_j, a changeover lasts beta * S."""
    setup = state["setup"]
    last = state["stations"][station_id]["recipe"]
    clock = 0.0
    times = []
    blocks = {block["product"]: block for block in blocks_of(state, station_id)}
    for name in sequence:
        block = blocks[name]
        clock += beta * setup[last][block["recipe"]]
        for _ in range(block["count"]):
            clock += block["work"] / block["count"]
            times.append(clock)
        last = block["recipe"]
    return times


# ---------------------------------------------------------------- tests


class BlockPlanningSmokeTest(unittest.TestCase):
    def choose(self, builder, beta=BETA):
        state, station_id = builder()
        return make_policy(beta)(state, station_id)

    def test_report_worked_example(self):
        state, station_id = report_example()
        # w = 1 + 19 = 20 for the A job and 4 for each B job; beta * S = 8.
        self.assertEqual(cost_by_products(state, station_id, 8.0, ["PA", "PB"]), 56.0)
        self.assertEqual(cost_by_products(state, station_id, 8.0, ["PB", "PA"]), 40.0)
        # Total virtual completion time exceeds K by the same 32 units for both orders.
        self.assertEqual(
            virtual_completions(state, station_id, 8.0, ["PA", "PB"]),
            [20.0, 32.0, 36.0],
        )
        self.assertEqual(
            virtual_completions(state, station_id, 8.0, ["PB", "PA"]),
            [12.0, 16.0, 44.0],
        )
        # The policy starts the B job that arrived first (id 3), not the first listed.
        self.assertEqual(make_policy()(state, station_id), 3)

    def test_setup_free_station_uses_sept_with_fifo_ties(self):
        # Jobs 12 and 13 share the smallest mean (2) and arrival (4); id 12 wins.
        # Job 12 still has 30 units of bottleneck work left. SEPT ignores it.
        self.assertEqual(self.choose(setup_free_station), 12)
        state, station_id = setup_free_station()
        least_remaining = min(
            state["queues"][station_id], key=lambda job: job["expected_remaining"]
        )
        self.assertEqual(least_remaining["id"], 13)

    def test_planning_work_counts_only_bottleneck_returns(self):
        state, station_id = route_reentry()
        works = {
            block["product"]: block["work"] for block in blocks_of(state, station_id)
        }
        # RET returns to the bottleneck (2 + 9). FIN has 30 units elsewhere only.
        self.assertEqual(works, {"RET": 11.0, "FIN": 2.0})
        self.assertEqual(cost_by_products(state, station_id, 8.0, ["RET", "FIN"]), 11.0)
        self.assertEqual(cost_by_products(state, station_id, 8.0, ["FIN", "RET"]), 2.0)
        self.assertEqual(self.choose(route_reentry), 22)

    def test_same_recipe_types_are_separate_blocks(self):
        state, station_id = same_recipe_blocks()
        recipes = sorted(
            (block["product"], block["recipe"], block["work"])
            for block in blocks_of(state, station_id)
        )
        self.assertEqual(recipes, [("P", "A", 20.0), ("Q", "A", 3.0), ("S", "B", 8.0)])
        # Best plan: Q (A), then S (B), then P (A): 9 + 32 + 8 = 49.
        self.assertEqual(
            cost_by_products(state, station_id, 8.0, ["Q", "S", "P"]), 49.0
        )
        self.assertEqual(self.choose(same_recipe_blocks), 32)
        self.assertEqual(brute_force_choice(state, station_id, 8.0), 32)
        # One block per recipe would merge P and Q and start job 31 instead:
        # A then B costs 2 * 23 + 2 * 8 = 62, and B then A costs 48 + 16 = 64.
        merged = {}
        for block in blocks_of(state, station_id):
            group = merged.setdefault(
                block["recipe"],
                {
                    "recipe": block["recipe"],
                    "count": 0,
                    "work": 0.0,
                    "first": block["first"],
                },
            )
            group["count"] += block["count"]
            group["work"] += block["work"]
            group["first"] = min(
                group["first"],
                block["first"],
                key=lambda job: (job["station_arrival"], job["id"]),
            )
        merged = list(merged.values())
        costs = {
            tuple(merged[i]["recipe"] for i in order): order_cost(
                state, station_id, merged, order, 8.0
            )
            for order in itertools.permutations(range(len(merged)))
        }
        self.assertEqual(costs, {("A", "B"): 62.0, ("B", "A"): 64.0})
        self.assertEqual(
            next(group for group in merged if group["recipe"] == "A")["first"]["id"], 31
        )

    def test_setup_asymmetry_prices_the_later_changeover(self):
        # From C, both changeovers cost 1. The later one costs 3 (A to B) or 1 (B to A).
        self.assertEqual(self.choose(asymmetric), 42)
        self.assertEqual(self.choose(asymmetric_transposed), 41)
        # With equal costs the scores tie at 29, and the earlier arrival wins.
        self.assertEqual(self.choose(asymmetric_symmetrized), 41)

    def test_tie_rules(self):
        self.assertEqual(self.choose(tie_by_arrival), 60)
        self.assertEqual(self.choose(tie_by_identifier), 50)
        self.assertEqual(self.choose(tie_within_block), 71)

    def test_every_waiting_job_counts(self):
        # Stay on A while 3 B jobs wait (42 < 43). Change to B when 4 wait (56 > 52).
        # The choice depends on how many B jobs wait, so the plan counts every job.
        self.assertEqual(self.choose(three_b_jobs), 81)
        self.assertEqual(self.choose(four_b_jobs), 82)

    def test_full_plan_differs_from_one_block_lookahead(self):
        state, station_id = cheap_first_change()
        blocks = blocks_of(state, station_id)
        setup, current, waiting = state["setup"], "A", len(state["queues"][station_id])

        def first_block_only(block):
            score = (
                waiting * 8.0 * setup[current][block["recipe"]]
                + (waiting - block["count"]) * block["work"]
            )
            return score, block["first"]["station_arrival"], block["first"]["id"]

        # Looking one block ahead prefers the cheap change to B (35 < 67).
        self.assertEqual(min(map(first_block_only, blocks))[2], 91)
        # The full plan sees that B then C costs 179, while C then B costs 75.
        self.assertEqual(cost_by_products(state, station_id, 8.0, ["PB", "PC"]), 179.0)
        self.assertEqual(cost_by_products(state, station_id, 8.0, ["PC", "PB"]), 75.0)
        self.assertEqual(self.choose(cheap_first_change), 92)

    def test_fixed_setup_weight(self):
        self.assertEqual(BETA, 8.0)
        self.assertEqual(self.choose(three_b_jobs, beta=1.0), 82)
        for value in (0.5, 0.0, -1.0, math.nan, math.inf):
            with self.subTest(beta=value), self.assertRaises(ValueError):
                make_policy(value)
        # The callback keeps no history: earlier calls do not change later choices.
        used = make_policy()
        for _, builder, beta, expected in FIXTURES:
            if beta == BETA and expected is not KeyError:
                used(*builder())
        for name, builder, beta, expected in FIXTURES:
            if beta == BETA and expected is not KeyError:
                with self.subTest(fixture=name):
                    self.assertEqual(used(*builder()), make_policy()(*builder()))

    def test_missing_current_recipe(self):
        # The evaluated simulator always installs a recipe. Without one, a single
        # waiting job is still forced. Two or more jobs cannot be planned.
        self.assertEqual(self.choose(missing_recipe_single), 101)
        with self.assertRaises(KeyError):
            self.choose(missing_recipe_pair)

    def test_empty_queue_is_rejected(self):
        for builder in (report_example, setup_free_station):
            state, station_id = builder()
            state["queues"][station_id] = ()
            with self.subTest(station=station_id), self.assertRaises(ValueError):
                make_policy()(state, station_id)

    def test_inputs_are_not_modified(self):
        for name, builder, beta, expected in FIXTURES:
            if expected is KeyError:
                continue
            with self.subTest(fixture=name):
                state, station_id = builder()
                before = copy.deepcopy(state)
                self.assertEqual(make_policy(beta)(state, station_id), expected)
                self.assertEqual(state, before)
                self.assertEqual(
                    make_policy(beta)(read_only(state), station_id), expected
                )

    def test_all_fixtures(self):
        for name, builder, beta, expected in FIXTURES:
            with self.subTest(fixture=name):
                if expected is KeyError:
                    with self.assertRaises(KeyError):
                        self.choose(builder, beta)
                else:
                    self.assertEqual(self.choose(builder, beta), expected)

    def test_matches_brute_force_on_random_queues(self):
        rng = random.Random(20261025)
        checked = 0
        for _ in range(300):
            state, station_id, beta = random_state(rng)
            expected = brute_force_choice(state, station_id, beta)
            self.assertEqual(make_policy(beta)(state, station_id), expected)
            shuffled = dict(state)
            queue = list(state["queues"][station_id])
            rng.shuffle(queue)
            shuffled["queues"] = {**state["queues"], station_id: tuple(queue)}
            self.assertEqual(make_policy(beta)(shuffled, station_id), expected)
            checked += 1
        self.assertEqual(checked, 300)


def random_state(rng):
    """A small random queue with integer data, so all costs are exact."""
    recipes = "ABCD"[: rng.randint(2, 4)]
    setup = {
        row: {
            column: 0.0 if row == column else float(rng.randint(0, 4))
            for column in recipes
        }
        for row in recipes
    }
    catalog = {}
    for name in ("P", "Q", "R"):
        path = [(0, rng.randint(1, 6), rng.choice(recipes))]
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.5:
                path.append((1, rng.randint(1, 5)))
            path.append((0, rng.randint(1, 6), rng.choice(recipes)))
        catalog[name] = route(*path)
    catalog = products(**catalog)
    visits = [
        (name, index)
        for name, product in catalog.items()
        for index, op in enumerate(product["route"])
        if op["station"] == BOTTLENECK
    ]
    rng.shuffle(visits)
    visits = visits[: rng.randint(1, 6)]
    identifiers = rng.sample(range(1, 1000), rng.randint(2, 9))
    waiting = [
        (job_id, *rng.choice(visits), float(rng.randint(0, 3)))
        for job_id in identifiers
    ]
    beta = float(rng.choice((1, 2, 8)))
    return make_state(catalog, setup, rng.choice(recipes), waiting), BOTTLENECK, beta


if __name__ == "__main__":
    unittest.main(verbosity=2)
