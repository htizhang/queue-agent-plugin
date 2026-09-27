"""Frozen congestion-priced lookahead policy.

Create a fresh policy with ``make_policy()`` for every independent replication.
The returned callback accepts the archived public state mapping and a station
identifier, then returns one waiting job identifier.

This is a focused extraction of source SHA-256
36f4e9194591a6ec20cd737606586560e5d1c511225090225c75085a70efa738,
instantiated with closing weight 1 and the residual-queue closing basis.
"""

from __future__ import annotations

from typing import Any, TypedDict


class _Occupancy(TypedDict):
    busy: float
    span: float
    end: float | None
    n: int


DEPTH = 3
PER_RECIPE = 3
TAIL_WEIGHT = 1.0
CLOSING_WEIGHT = 1.0
PRICE_SCALE = 1.0
PRICE_EXPONENT = 1.0
PRICE_FLOOR = 1.0
PRICE_CAP = 32.0
RHO_PRIOR = 0.80
PRIOR_OPERATIONS = 50.0
ROUTE_WEIGHT = 0.10


def _fifo(job):
    return job["station_arrival"], job["id"]


def _station_work(state, station_id, job):
    route = state["products"][job["product"]]["route"]
    return sum(
        operation["mean_service"]
        for operation in route[job["operation"] :]
        if operation["station"] == station_id
    )


def _operation_mean(state, station_id):
    work = 0.0
    visits = 0.0
    for product in state["products"].values():
        probability = product["probability"]
        for operation in product["route"]:
            if operation["station"] == station_id:
                work += probability * operation["mean_service"]
                visits += probability
    return work / visits if visits > 0.0 else 1.0


def make_policy():
    """Return a fresh stateful policy callback."""

    tracker: dict[Any, _Occupancy] = {}

    def occupancy(state, station_id):
        estimate = tracker.get(station_id)
        if estimate is None:
            unit = _operation_mean(state, station_id)
            estimate = _Occupancy(
                busy=RHO_PRIOR * PRIOR_OPERATIONS * unit,
                span=PRIOR_OPERATIONS * unit,
                end=None,
                n=0,
            )
            tracker[station_id] = estimate
        if estimate["span"] > 0.0:
            return estimate["busy"] / estimate["span"]
        return RHO_PRIOR

    def observe(state, station_id, job, servers):
        occupancy(state, station_id)
        estimate = tracker[station_id]
        now = state["now"]
        work = job["setup_cost"] + job["expected_current"]
        if estimate["end"] is None:
            end = now + work
            grown = work
        else:
            end = max(now, estimate["end"]) + work
            grown = end - estimate["end"]
        estimate["busy"] += work / servers
        estimate["span"] += grown
        estimate["end"] = end
        estimate["n"] += 1

    def shadow_price(state, station_id):
        headroom = 1.0 - occupancy(state, station_id)
        if headroom <= 0.0:
            return PRICE_CAP
        beta = PRICE_SCALE / (headroom**PRICE_EXPONENT)
        if beta < PRICE_FLOOR:
            return PRICE_FLOOR
        return PRICE_CAP if beta > PRICE_CAP else beta

    def plan(state, station_id):
        queue = list(state["queues"][station_id])
        current_recipe = state["stations"][station_id].get("recipe")
        beta = shadow_price(state, station_id)

        def planning_work(job):
            own = _station_work(state, station_id, job)
            other = max(0.0, job["expected_remaining"] - own)
            return own + ROUTE_WEIGHT * other

        if current_recipe is None:
            return min(queue, key=lambda job: (planning_work(job), *_fifo(job)))["id"]
        if len(queue) == 1:
            return queue[0]["id"]

        setup = state["setup"]
        by_recipe = {}
        for job in queue:
            by_recipe.setdefault(job["recipe"], []).append(job)

        pool = []
        for jobs in by_recipe.values():
            pool.extend(
                sorted(jobs, key=lambda job: (planning_work(job), *_fifo(job)))[
                    :PER_RECIPE
                ]
            )

        queue_size = len(queue)
        items = [(job, job["recipe"], planning_work(job)) for job in pool]
        horizon = min(DEPTH, len(items))

        counts = {recipe: len(jobs) for recipe, jobs in by_recipe.items()}
        exits = {
            recipe: sum(
                count * setup[recipe][target] for target, count in counts.items()
            )
            for recipe in setup
        }

        def closing_cost(recipe, chain):
            total = exits[recipe]
            remaining = queue_size
            for selected_recipe in chain:
                total -= setup[recipe][selected_recipe]
                remaining -= 1
            return total / remaining if remaining > 0 else 0.0

        best_key = None
        best_first = None

        def search(recipe, clock, score, step, used, first, chain):
            nonlocal best_key, best_first
            if step >= horizon:
                end = clock + CLOSING_WEIGHT * beta * closing_cost(recipe, chain)
                total = score + TAIL_WEIGHT * (queue_size - step) * end
                key = (total, *_fifo(first))
                if best_key is None or key < best_key:
                    best_key = key
                    best_first = first
                return

            for index, (job, next_recipe, duration) in enumerate(items):
                if used & (1 << index):
                    continue
                next_clock = clock + beta * setup[recipe][next_recipe] + duration
                search(
                    next_recipe,
                    next_clock,
                    score + next_clock,
                    step + 1,
                    used | (1 << index),
                    first if step else job,
                    chain + (next_recipe,),
                )

        search(current_recipe, 0.0, 0.0, 0, 0, None, ())
        if best_first is None:
            return min(
                queue,
                key=lambda job: (
                    _station_work(state, station_id, job),
                    *_fifo(job),
                ),
            )["id"]
        return best_first["id"]

    def choose(state, station_id):
        job_id = plan(state, station_id)
        if station_id == state["bottleneck"]:
            job = next(
                job for job in state["queues"][station_id] if job["id"] == job_id
            )
            servers = max(1, state["stations"][station_id]["servers"])
            observe(state, station_id, job, servers)
        return job_id

    setattr(choose, "tracker", tracker)
    return choose
