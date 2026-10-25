"""Queue-aware optimistic backfilling for multiserver-job queues.

This file is a standard-library port of the evaluated two-parameter policy.
One call decides which waiting jobs start now:

    starts = choose(state, memory)

`state` is a dictionary with these keys:

- ``time``: the current time.
- ``capacity``: the total number of servers, ``n``.
- ``free``: the number of servers that are free now, ``F``.
- ``waiting``: waiting jobs. Each job has ``id``, ``arrival``, ``width``,
  ``estimate`` (the runtime request), and ``class_id``.
- ``running``: running jobs. Each job has ``width``, ``estimate``, and
  ``elapsed`` (the time since the job started).
- ``classes``: public class profiles, keyed by class identifier. The policy
  reads only the ``mean`` field of each profile. The mapping can be empty.

The result lists the IDs of the waiting jobs to start now, in scan order. Their
total width is at most ``free``. The policy keeps no state between calls, and
it ignores ``memory``. In the evaluation, the simulator started the returned
jobs and called the policy again at the same time, with those jobs listed as
running, until a call returned no job.

The calendar compares floating-point times exactly, as the evaluated code does.
If ``time + duration`` rounds to ``time``, the admission test has no interval to
check and raises ``ValueError``. This can occur only with very large clock
values and very short planning durations.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

# The two policy parameters. Both belong to the packing repair.
COMPARISON_FACTOR = 2.0  # kappa: request limit, relative to the first fitting job
GAIN_THRESHOLD = 1.0 / 8.0  # eta: minimum packing gain, as a fraction of capacity

# Numerical safeguards, not tuned parameters.
EPS = 1e-9  # floor for log inputs, durations, and running-job residuals
SUBSET_TOTAL_LIMIT = 4096  # stop once the number of reachable totals exceeds this
NEVER = float("inf")


def priority_order(
    waiting: list[dict[str, Any]],
    capacity: int,
    free: int,
    width_counts: Counter,
) -> list[dict[str, Any]]:
    """Sort by log(request) - log(width/capacity) - log(count) + gap.

    Arrival time and then ID break equal-score ties.
    """

    def key(job: dict[str, Any]) -> tuple[Any, ...]:
        width = job["width"]
        gap = (free - width) / capacity if width <= free else 1.0
        return (
            math.log(max(job["estimate"], EPS))
            - math.log(width / capacity)
            - math.log(width_counts[width])
            + gap,
            job["arrival"],
            job["id"],
        )

    return sorted(waiting, key=key)


def _maxfill(widths: list[int], available: int) -> list[int]:
    """Return the first-discovered fullest subset among the jobs searched.

    The reachable-total cutoff can stop the scan early when available >= 4096.
    It does not bind in the evaluated grid, where capacity <= 512.
    """
    if not widths or available <= 0:
        return []
    reachable = {0: 0}
    for index, width in enumerate(widths):
        if width > available:
            continue
        for total in sorted(reachable, reverse=True):
            candidate = total + width
            if candidate <= available and candidate not in reachable:
                reachable[candidate] = reachable[total] | (1 << index)
        if len(reachable) > SUBSET_TOTAL_LIMIT:
            break
    mask = reachable[max(reachable)]
    return [index for index in range(len(widths)) if (mask >> index) & 1]


def repair_packing(
    ordered: list[dict[str, Any]],
    capacity: int,
    free: int,
    comparison_factor: float = COMPARISON_FACTOR,
    gain_threshold: float = GAIN_THRESHOLD,
) -> list[dict[str, Any]]:
    """Move a better-filling subset of comparable jobs to the front, if one exists."""
    fitting = [job for job in ordered if job["width"] <= free]
    if len(fitting) < 2 or sum(job["width"] for job in fitting) <= free:
        return ordered
    greedy, remaining = 0, free
    for job in fitting:
        if job["width"] <= remaining:
            greedy += job["width"]
            remaining -= job["width"]
    cutoff = comparison_factor * max(fitting[0]["estimate"], EPS)
    eligible = [job for job in fitting if job["estimate"] <= cutoff]
    picked = _maxfill([job["width"] for job in eligible], free)
    gain = sum(eligible[index]["width"] for index in picked) - greedy
    if gain >= gain_threshold * capacity and picked and len(picked) < len(fitting):
        promoted = {eligible[index]["id"] for index in picked}
        return [job for job in ordered if job["id"] in promoted] + [
            job for job in ordered if job["id"] not in promoted
        ]
    return ordered


def planning_duration(
    job: dict[str, Any],
    capacity: int,
    width_counts: Counter,
    classes: dict[str, Any],
) -> float:
    """Return the duration that a waiting job occupies in this call's calendar.

    The value is request * mean / (request + mean), discounted by the number
    of waiting jobs with the same width. If the
    class profile or its mean is missing, the request replaces the mean.
    """
    profile = classes.get(job["class_id"]) if classes else None
    mean = profile.get("mean", job["estimate"]) if profile else job["estimate"]
    duration = job["estimate"] * mean / (job["estimate"] + mean)
    count = width_counts[job["width"]]
    if count > 1:
        duration *= float(count) ** (-(job["width"] / capacity))
    return max(duration, EPS)


class Calendar:
    """Planned free servers as a step function: ``free`` plus changes at or before t."""

    def __init__(self, state: dict[str, Any]) -> None:
        self.now = state["time"]
        self.free = state["free"]
        self.delta: dict[float, int] = {}
        for job in state["running"]:
            # Running jobs release their servers at the end of their raw request.
            release = self.now + max(job["estimate"] - job["elapsed"], EPS)
            self.delta[release] = self.delta.get(release, 0) + job["width"]

    def _profile(self):
        level = self.free
        yield self.now, level
        for time in sorted(self.delta):
            level += self.delta[time]
            yield time, level

    def place(self, start: float, duration: float, width: int) -> None:
        """Subtract ``width`` on the half-open interval [start, start + duration)."""
        for time, sign in ((start, -width), (start + duration, width)):
            total = self.delta.get(time, 0) + sign
            if total:
                self.delta[time] = total
            else:
                self.delta.pop(time, None)

    def minimum(self, duration: float) -> float:
        """Return the fewest planned free servers on [now, now + duration)."""
        limit = self.now + duration
        return min(level for time, level in self._profile() if time < limit)

    def earliest(self, width: int, duration: float) -> float:
        """Return the first change time at which the whole interval fits."""
        profile = list(self._profile())
        for index, (start, level) in enumerate(profile):
            if level < width:
                continue
            limit = start + duration
            if all(
                time >= limit or later >= width
                for time, later in profile[index + 1 :]
            ):
                return start
        return NEVER


def choose(
    state: dict[str, Any],
    memory: dict[str, Any],
    *,
    comparison_factor: float = COMPARISON_FACTOR,
    gain_threshold: float = GAIN_THRESHOLD,
) -> list[Any]:
    """Return the IDs of the waiting jobs to start now."""
    del memory  # The policy keeps no state between calls.
    waiting = state["waiting"]
    if not waiting:
        return []
    capacity, free, now = state["capacity"], state["free"], state["time"]
    width_counts = Counter(job["width"] for job in waiting)

    ordered = repair_packing(
        priority_order(waiting, capacity, free, width_counts),
        capacity,
        free,
        comparison_factor,
        gain_threshold,
    )

    calendar = Calendar(state)
    available, starts = free, []
    for job in ordered:
        width = job["width"]
        duration = planning_duration(job, capacity, width_counts, state["classes"])
        if width <= available and calendar.minimum(duration) >= width:
            starts.append(job["id"])
            available -= width
            calendar.place(now, duration, width)
        else:
            # Every job that cannot start receives a provisional reservation.
            start = calendar.earliest(width, duration)
            if start != NEVER:
                calendar.place(start, duration, width)

    if not starts and not state["running"]:
        # Guard retained from the evaluated code for an idle pool.
        for job in ordered:
            if job["width"] <= free:
                return [job["id"]]
    return starts
