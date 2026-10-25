"""Bottleneck-work block planning with a fixed setup weight.

Standalone extraction of the evaluated policy. It needs only the Python 3.10+
standard library:

    choose = make_policy()               # evaluated setup weight, beta = 8
    job_id = choose(state, station_id)   # identifier of one waiting job

The callback reads these state fields:

- ``state["bottleneck"]``: the setup-sensitive station, or ``None``.
- ``state["setup"][r][r2]``: setup time from recipe ``r`` to recipe ``r2``.
- ``state["stations"][station_id]["recipe"]``: the installed recipe.
- ``state["products"][product]["route"]``: operations with ``station`` and
  ``mean_service``.
- ``state["queues"][station_id]``: waiting jobs with ``id``, ``product``,
  ``operation`` (route index), ``recipe``, ``station_arrival``, and
  ``expected_current``.

It returns an identifier only. It does not modify the state, perform a setup,
or start service. The setup weight affects the virtual plan only, so physical
setups keep their matrix durations. The callback keeps no history between calls.
"""

from __future__ import annotations

import math

BETA = 8.0
"""Evaluated setup weight; the sensitivity grid ranges from 1 to 32."""


def _arrival_order(job):
    return job["station_arrival"], job["id"]


def _bottleneck_work(state, station_id, job):
    """Mean work left for the job at this station, including later returns."""
    route = state["products"][job["product"]]["route"]
    return sum(
        operation["mean_service"]
        for operation in route[job["operation"] :]
        if operation["station"] == station_id
    )


def make_policy(beta=BETA):
    """Return a dispatch callback that uses setup weight ``beta``.

    ``beta`` must be finite and at least 1, as in the evaluated source.
    """
    if not math.isfinite(beta) or beta < 1.0:
        raise ValueError("beta must be finite and at least 1")

    def choose(state, station_id):
        queue = state["queues"][station_id]
        if not queue:
            raise ValueError(f"no job is waiting at station {station_id!r}")
        if station_id != state["bottleneck"]:
            # Setup-free station: shortest expected processing time (SEPT).
            return min(
                queue, key=lambda job: (job["expected_current"], *_arrival_order(job))
            )["id"]
        if len(queue) == 1:
            return queue[0]["id"]
        return _first_job_of_best_plan(state, station_id, queue, beta)["id"]

    return choose


def _first_job_of_best_plan(state, station_id, queue, beta):
    """Minimize the virtual completion cost, then return the first job.

    Each block adds waiting * beta * setup + (waiting - count) * work.
    Station arrival and ID break ties. The subset search grows exponentially
    with the number of job types; the tested layouts have at most seven.
    """
    setup = state["setup"]
    current = state["stations"][station_id]["recipe"]
    try:
        from_current = setup[current]
    except KeyError:
        raise KeyError(
            f"no setup row for the installed recipe {current!r}. "
            "A queue of two or more jobs cannot be planned."
        ) from None

    # One block per job type. The recipe follows from the product and operation.
    types = {}
    for job in queue:
        key = job["recipe"], job["product"], job["operation"]
        types.setdefault(key, []).append(job)
    blocks = [
        (
            recipe,
            len(jobs),
            sum(_bottleneck_work(state, station_id, job) for job in jobs),
            min(jobs, key=_arrival_order),
        )
        for (recipe, _, _), jobs in types.items()
    ]

    everything = (1 << len(blocks)) - 1
    memo = {}

    def rest(planned, last, waiting):
        """Smallest cost the unplanned blocks add, starting from recipe ``last``."""
        if planned == everything:
            return 0.0
        key = planned, last
        if key not in memo:
            row = setup[last]
            memo[key] = min(
                waiting * beta * row[recipe]
                + (waiting - count) * work
                + rest(planned | 1 << index, recipe, waiting - count)
                for index, (recipe, count, work, _) in enumerate(blocks)
                if not planned >> index & 1
            )
        return memo[key]

    total = len(queue)

    def first_block_key(index):
        recipe, count, work, first = blocks[index]
        score = (
            total * beta * from_current[recipe]
            + (total - count) * work
            + rest(1 << index, recipe, total - count)
        )
        return score, *_arrival_order(first)

    return blocks[min(range(len(blocks)), key=first_block_key)][3]
