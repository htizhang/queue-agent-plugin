"""Portable queue-aware optimistic backfilling policy.

This is the decision-relevant slice of the frozen evaluated implementation.
Research-only counters, ablation switches, and filesystem-dependent loaders were
removed because they do not affect this policy's actions.

Natural interface retained from the original evaluator:

    starts = choose(state, memory)

`state` is a dictionary containing time, capacity, free, waiting, running, and
classes. Waiting jobs provide id, arrival, width, estimate, and class_id.
Running jobs additionally provide elapsed. The return value is a list of job
IDs to start now. `memory` is accepted for evaluator compatibility but the
deployed policy is memoryless across calls.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any


ALPHA = 1.1
BETA = 0.8
GAMMA = 0.85
ESTIMATE_SPAN = 2.5
PACKING_GAIN_FRACTION = 0.10
PLANNING_SCALE = 0.35
MAX_OPTIMISM = 3.0
MAX_RESERVATIONS = 6

EPS = 1e-9
BIG = float("inf")

Job = dict[str, Any]
Plan = tuple[list[float], list[float]]


def _reference_duration(state: dict[str, Any]) -> float:
    reference = sum(
        profile.get("probability", 0.0) * profile.get("mean", 1.0)
        for profile in state.get("classes", {}).values()
    )
    return reference or 1.0


def planning_duration(
    job: Job,
    capacity: int,
    width_counts: Counter[int] | dict[int, int],
) -> float:
    """Return the queue-aware duration used for admission and reservation."""
    most_common = max(width_counts.values())
    level = 1.0 + (MAX_OPTIMISM - 1.0) * (width_counts[job["width"]] / most_common)
    remaining = capacity - job["width"]
    exponent = min(1.0, job["width"] / remaining) if remaining > 0 else 1.0
    return job["estimate"] * PLANNING_SCALE * level ** (-exponent)


def _priority_order(
    waiting: list[Job],
    capacity: int,
    free: int,
    reference: float,
) -> list[Job]:
    class_counts = Counter(job["class_id"] for job in waiting)

    def key(job: Job) -> tuple[float, float, Any]:
        estimate = max(job["estimate"], EPS)
        width_fraction = job["width"] / capacity
        gap = (free - job["width"]) / capacity if job["width"] <= free else 1.0
        score = (
            math.log(estimate / reference)
            - ALPHA * math.log(width_fraction)
            - BETA * math.log(class_counts[job["class_id"]])
            + GAMMA * gap
        )
        return score, job["arrival"], job["id"]

    return sorted(waiting, key=key)


def _maxfill(widths: list[int], available: int) -> list[int]:
    """Return the first-discovered maximum-width subset from priority order."""
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
        if len(reachable) > 4096:
            break
    mask = reachable[max(reachable)]
    return [index for index in range(len(widths)) if (mask >> index) & 1]


def _repair_packing(
    ordered: list[Job],
    capacity: int,
    free: int,
) -> list[Job]:
    fitting = [job for job in ordered if job["width"] <= free]
    if len(fitting) < 2 or sum(job["width"] for job in fitting) <= free:
        return ordered

    greedy = 0
    remaining = free
    for job in fitting:
        if job["width"] <= remaining:
            greedy += job["width"]
            remaining -= job["width"]

    cutoff = ESTIMATE_SPAN * max(fitting[0]["estimate"], EPS)
    eligible = [job for job in fitting if job["estimate"] <= cutoff]
    picked = _maxfill([job["width"] for job in eligible], free)
    gain = sum(eligible[index]["width"] for index in picked) - greedy

    if (
        gain >= PACKING_GAIN_FRACTION * capacity
        and picked
        and len(picked) < len(fitting)
    ):
        promoted_ids = {eligible[index]["id"] for index in picked}
        return [job for job in ordered if job["id"] in promoted_ids] + [
            job for job in ordered if job["id"] not in promoted_ids
        ]
    return ordered


def _plan_from_running(state: dict[str, Any]) -> Plan:
    now = state["time"]
    free = state["free"]
    releases: dict[float, int] = {}
    for job in state["running"]:
        residual = max(job["estimate"] - job["elapsed"], EPS)
        release = now + residual
        if release <= now:
            release = now + EPS
        releases[release] = releases.get(release, 0) + job["width"]

    times = [now]
    capacities = [free]
    for release in sorted(releases):
        free += releases[release]
        times.append(release)
        capacities.append(free)
    return times, capacities


def _plan_place(
    plan: Plan,
    start: float,
    duration: float,
    width: int,
) -> Plan:
    """Subtract width from a step-function plan over [start, start+duration)."""
    times, capacities = plan
    end = start + duration
    new_times: list[float] = []
    new_capacities: list[float] = []

    for index, (time, free) in enumerate(zip(times, capacities)):
        next_time = times[index + 1] if index + 1 < len(times) else BIG
        if next_time <= start:
            new_times.append(time)
            new_capacities.append(free)
            continue
        if time < start:
            new_times.append(time)
            new_capacities.append(free)
            new_times.append(start)
            new_capacities.append(free - width)
        elif time < end:
            new_times.append(time)
            new_capacities.append(free - width)
        else:
            new_times.append(time)
            new_capacities.append(free)
            continue
        if next_time > end > max(time, start):
            new_times.append(end)
            new_capacities.append(free)

    compact_times = [new_times[0]]
    compact_capacities = [new_capacities[0]]
    for time, free in zip(new_times[1:], new_capacities[1:]):
        if time <= compact_times[-1] + 1e-12:
            compact_capacities[-1] = min(compact_capacities[-1], free)
        elif free == compact_capacities[-1]:
            continue
        else:
            compact_times.append(time)
            compact_capacities.append(free)
    return compact_times, compact_capacities


def _plan_minimum(plan: Plan, duration: float) -> float:
    times, capacities = plan
    limit = times[0] + duration
    minimum = capacities[0]
    for time, free in zip(times[1:], capacities[1:]):
        if time >= limit:
            break
        minimum = min(minimum, free)
    return minimum


def _plan_earliest(plan: Plan, width: int, duration: float) -> float:
    times, capacities = plan
    for index, start in enumerate(times):
        if capacities[index] < width:
            continue
        limit = start + duration
        if all(
            time >= limit or capacities[later] >= width
            for later, time in enumerate(times[index + 1 :], start=index + 1)
        ):
            return start
    return BIG


def choose(state: dict[str, Any], memory: dict[str, Any]) -> list[Any]:
    """Choose waiting job IDs to start immediately."""
    del memory
    waiting = state["waiting"]
    if not waiting:
        return []

    capacity = state["capacity"]
    free = state["free"]
    now = state["time"]
    reference = _reference_duration(state)
    width_counts = Counter(job["width"] for job in waiting)

    ordered = _priority_order(waiting, capacity, free, reference)
    ordered = _repair_packing(ordered, capacity, free)

    plan = _plan_from_running(state)
    available = free
    reservations = 0
    starts: list[Any] = []

    for job in ordered:
        width = job["width"]
        duration = planning_duration(job, capacity, width_counts)
        if width <= available and _plan_minimum(plan, duration) >= width:
            starts.append(job["id"])
            available -= width
            plan = _plan_place(plan, now, duration, width)
        elif reservations < MAX_RESERVATIONS:
            start = _plan_earliest(plan, width, duration)
            if start == BIG:
                start = now + 1e7 * (1.0 + reference)
            plan = _plan_place(plan, start, duration, width)
            reservations += 1

    if not starts and not state["running"]:
        for job in ordered:
            if job["width"] <= free:
                return [job["id"]]
    return starts
