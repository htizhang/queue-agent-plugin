# Queue-aware optimistic backfilling

> **Discovery Lab status:** This policy came from agent-assisted research. It
> is a research lead, not a peer-reviewed baseline. Its evidence applies to the
> configurations and comparators in [the evaluation note](evaluation/README.md).

## Problem

A cluster has `n` identical servers and one shared waiting queue. Job `j`
arrives at time `a_j` and needs `k_j` servers at the same time. This number is
its **width**. The job is rigid and nonpreemptive: once it starts, it holds
exactly `k_j` servers until it completes. At arrival, the scheduler receives a
**runtime request** `ŝ_j`, such as a user's runtime limit. The job also belongs
to a class `z_j`. Each class has a public profile that gives its population mean
service time `m_z`.

At each decision, the scheduler chooses waiting jobs to start now. Their total
width must not exceed the `F` servers that are free. The scheduler does not see
actual durations or future arrivals. The objective is mean response time over
a set of scored jobs that does not depend on the policy. Response time is the
time from arrival to completion. Every job must eventually complete.

## Inputs and output

The implementation exposes one callback:

```python
starts = choose(state, memory)
```

| Field of `state` | Contents |
| --- | --- |
| `time` | The current time `t`. |
| `capacity` | The number of servers `n`. |
| `free` | The number of servers that are free now, `F`. |
| `waiting` | Waiting jobs, each with `id`, `arrival`, `width`, `estimate` (the runtime request), and `class_id`. |
| `running` | Running jobs, each with `width`, `estimate`, and `elapsed`, the time since the job started. |
| `classes` | Class profiles keyed by class identifier. The policy reads only `mean`. The mapping can be empty. |

The result is a list of waiting-job IDs to start now, in scan order. Their total
width is at most `F`. Requests and class means must be positive. Job IDs must be
unique and of one comparable type, because they break the last ties. If a
class profile or its mean is missing, the request replaces the mean. The policy
keeps no state between calls, and it ignores `memory` and all other fields.

The scheduler calls the policy at each arrival and completion. After a call
returns jobs, the scheduler starts them and calls again at the same time. The
new jobs then appear as running jobs with zero elapsed time. Calls repeat until
one returns no job. The evaluation used this calling rule.

## How the policy works

A strict priority order can leave servers idle. If the first job does not fit,
later jobs that do fit must wait. Backfilling starts such later jobs on the idle
servers, but it must decide how much to protect the jobs that it skips. One
call of this policy has four steps:

1. **Rank** the waiting jobs. The score favors short requests, wide jobs,
   widths with many waiting jobs, and jobs that fit the free servers tightly.
2. **Repair** a poor packing. If a group of jobs with comparable requests fills
   clearly more of the free servers, move that group to the front.
3. **Plan** a duration for each waiting job. It is shorter than the request,
   and it is shorter again when many waiting jobs share the job's width.
4. **Admit** jobs with a calendar of planned free servers. Start a job only if
   it fits now and its planned interval keeps clear of earlier reservations.
   Give every other job a reservation.

The policy is **queue-aware** because the number of waiting jobs of each width
affects both the order and the planning durations. It is **optimistic** because
it plans with durations shorter than the requests, which allows more
backfilling. The cost is weaker protection: a job still runs for its actual
duration and can delay the jobs that the plan meant to protect.

Scores, the repaired order, planning durations, the calendar, and reservations
exist only inside one call. They never change how long a job runs.

## Policy

### 1. Priority order

Let `q_k` be the number of waiting jobs of width `k`. The count groups jobs by
width, whether or not they share a class, and it includes job `j` itself. Let
`x_j = k_j / n` be the width fraction. The fit term is

```math
g_j=\begin{cases}(F-k_j)/n, & k_j\le F,\\ 1, & k_j>F.\end{cases}
```

The policy sorts the waiting jobs by increasing

```math
\psi_j=\log\hat s_j-\log x_j-\log q_{k_j}+g_j ,
```

with natural logarithms and the request floored at `1e-9`. Ties break by
arrival time and then by job ID. The four terms have unit weights:

- `log ŝ_j`: a shorter request moves the job forward.
- `-log x_j`: a wider job moves forward, because many servers must be free
  together before it can start.
- `-log q_{k_j}`: a larger backlog at the job's width moves the job forward.
- `g_j`: among jobs that fit now, a tighter fit moves the job forward. A job
  that does not fit receives the largest value, 1.

The counts and fit terms stay constant during the call. Waiting time does not
enter the score, except through the arrival-time tie-break.

### 2. Packing repair

Let `B` be the jobs, in priority order, whose width is at most `F`, and let `b`
be the first of them. A first-fit scan through `B` adds each job that still
fits in the remaining free servers. Let `G` be the total width that it adds.
The eligible jobs are

```math
E=\{j\in B:\hat s_j\le\kappa\,\hat s_b\}.
```

An integer subset-sum search over `E`, in priority order, finds a subset `P`
with the largest total width that is at most `F`. For each reachable total, the
search keeps the first subset that it finds. The policy moves `P` to the front
only if

```math
\sum_{j\in P}k_j-G\ge\eta\,n .
```

The repair also follows these rules:

- It does nothing when fewer than two jobs fit, or when all fitting jobs fit
  together.
- It needs a nonempty `P` with fewer jobs than `B`.
- It keeps the relative order within `P` and within the other jobs.
- It changes the order only. The calendar still decides which jobs start.

The request filter stops the search from filling servers with jobs that would
hold them much longer than job `b`. The threshold `η` stops reorderings for
small packing gains.

### 3. Planning durations

Each waiting job receives the planning duration

```math
d_j=\max\left\{\frac{\hat s_j\,m_{z_j}}{\hat s_j+m_{z_j}}\;q_{k_j}^{-x_j},\;10^{-9}\right\}.
```

The first factor is the **harmonic expression** of the request and the class
mean. It is close to the mean when the request is much longer, and close to
the request when the request is much shorter. It is always smaller than both
inputs, and it equals half of their value when they are equal.

The second factor is a **count discount**. Many waiting jobs can share one
width. If the calendar protected each of them for its full duration, later jobs
could wait even when they fit now. The discount loosens that protection as the
backlog grows. Wide jobs receive a stronger discount, because each of their
reservations blocks a larger share of the servers. When only one job of a width
is waiting, the factor is 1.

For example, a request of 120 seconds and a class mean of 60 seconds give a
harmonic expression of 40 seconds. With four waiting jobs of the same width,
the planning duration is 38.3 seconds for `x_j = 1/32`, 20.0 seconds for
`x_j = 1/2`, and 14.1 seconds for `x_j = 3/4`.

### 4. Admission with a provisional calendar

The calendar `C(u)` gives the planned number of free servers at each time
`u ≥ t`. It starts at `F`. Each running job `ℓ` with elapsed time `e_ℓ` adds its
width back at `t + max(ŝ_ℓ − e_ℓ, 1e-9)`, the end of its raw request. Running
jobs receive neither the harmonic expression nor the count discount, because
the policy cannot change them.

Placing a job of width `k` at time `u` for duration `d` subtracts `k` from the
calendar on the half-open interval `[u, u + d)`. The scan visits the repaired
order and tracks `f`, the servers that are actually free and not yet given to
this call's starts. At first, `f = F`. Job `j` starts now only if

```math
k_j\le f\qquad\text{and}\qquad\min_{u\in[t,\,t+d_j)}C(u)\ge k_j .
```

The first condition is physical capacity. The second protects the intervals
that the scan placed earlier. If the job starts, the policy reduces `f` by `k_j`
and places `[t, t + d_j)`. Otherwise, it places the job at its earliest
feasible time. This time is the first of `t` and the calendar's change times at
which `C` stays at or above `k_j` throughout the planned interval. A reservation
uses no free servers now.

Every job that fails the start test receives a reservation when one exists,
not only the first blocked job. The calendar is rebuilt at each call, so a
reservation is not a promised start time.

### 5. Idle-pool guard

Suppose that a call starts no job and that no job is running. The policy then
returns the first job in the repaired order whose width is at most `F`. This
guard comes from the evaluated code. When no job is running, the calendar
starts flat at `F`. A job wider than `F` then finds no feasible reservation, so
the scan always starts the first job that fits. The guard therefore does not
change decisions.

### Pseudocode

```text
Input: time t, capacity n, free servers F, waiting and running jobs, class means
Output: list A of waiting jobs to start now

 1. If no job is waiting, return [].
 2. Count q_k, the waiting jobs of each width k.
 3. Sort the waiting jobs by (psi_j, arrival time, job ID).
 4. Apply the packing repair with kappa and eta. Call the result L.
 5. Build calendar C from F and the raw remaining requests of running jobs.
 6. Set f = F and A = [].
 7. For each job j in L:
 8.     Compute d_j.
 9.     If k_j <= f and C has at least k_j free servers throughout [t, t + d_j):
10.         Append j to A, set f = f - k_j, and place j on [t, t + d_j).
11.     Else:
12.         Let u be the first of t and the change times of C at which
            C keeps at least k_j free servers throughout [u, u + d_j).
13.         If such a u exists, place j on [u, u + d_j).
14. If A is empty and no job is running:
15.     Return the first job in L with width at most F, if one exists.
16. Return A.
```

### Parameters

Both parameters belong to the packing repair. The study set both values before
the evaluation runs.

| Parameter | Meaning | Value |
| --- | --- | ---: |
| κ, comparison factor | Largest eligible request, relative to the request of the first fitting job | 2 |
| η, gain threshold | Smallest packing gain that justifies a reorder, as a fraction of `n` | 1/8 |

Two numerical safeguards are not tuned parameters. The policy floors log
inputs, planning durations, and running-job residuals at `1e-9`. The subset-sum
search stops once it has more than 4,096 reachable totals. This cutoff cannot
bind when `F` is at most 4,095. The evaluated capacities were at most 512.

## Worked examples

**Calendar and count discount.** Take `n = 8` servers. Set the time origin at
the current decision, `t = 0`. One running job holds four servers, and its request ends at time 10. Thus `F = 4`, and the
calendar shows 4 free servers before time 10 and 8 afterward.

| Job | Width | Request | Class mean | Arrival |
| --- | ---: | ---: | ---: | ---: |
| J1 | 6 | 12 | 12 | −2 |
| J2 | 2 | 22 | 22 | −1 |
| J3 | 2 | 22 | 22 | 0 |

1. **Rank.** The counts are `q_6 = 1` and `q_2 = 2`. J1 does not fit, so
   `ψ = log 12 − log(6/8) − log 1 + 1 ≈ 3.77`. J2 and J3 each have
   `ψ = log 22 − log(2/8) − log 2 + 2/8 ≈ 4.03`. The order is J1, J2, J3, and
   arrival time breaks the tie between J2 and J3.
2. **Repair.** J2 and J3 fit together in the four free servers, so the repair
   does nothing.
3. **Plan.** J1 has `d = 12 × 12 / 24 = 6`. J2 and J3 each have
   `d = (22 × 22 / 44) × 2^(−1/4) = 11 × 0.841 ≈ 9.25`.
4. **Admit.** J1 needs six servers but only four are free, so the calendar
   reserves it on `[10, 16)`. J2 fits, and its interval `[0, 9.25)` ends before
   the reservation starts, so J2 starts. J3 fits in the last two free servers,
   and its interval also ends before 10, so it starts too.

The call returns J2 and J3. Without the count discount, J2 and J3 would each
plan `[0, 11)`. J2 would still start, but J3 would then conflict with J1's
reservation on `[10, 11)` and wait. The discount admits the backlog of two
narrow jobs now. The cost appears if J2 and J3 run for their full requests:
J1 then cannot start at time 10.

**Packing repair.** Take `n = F = 8` with no running job. Three jobs wait, with
widths 5, 4, and 4 and requests 2, 4, and 4. The width-five job scores about
1.54 and each width-four job about 1.89, so the width-five job is first. The
first-fit scan adds only that job, so `G = 5`. With `κ = 2`, all three jobs are
eligible, because no request exceeds 4. The two width-four jobs fill all eight
servers, a gain of 3 servers, which exceeds `ηn = 1`. The repair moves them to
the front. The scan then starts both of them and reserves the width-five job.

## Applicability and limits

The evaluation covered one pool of identical servers, rigid nonpreemptive jobs,
synthetic workloads, and capacities of 32, 128, and 512. Requests were exact or
conservative upper bounds, and every policy received exact population class
means. No test covered multiple resource types, placement constraints,
preemption, or malleable jobs. No test covered requests that underestimate,
class means estimated from data, or objectives other than mean response time.

Planning durations are not upper bounds on actual durations. Reservations
therefore do not give the hard protection of backfilling with upper-bound
requests. Waiting time does not raise a job's priority. Every evaluated run
completed all of its jobs, but this does not show that waits stay bounded in
other workloads. Above `F = 4,095` servers, the subset-sum cutoff can stop the
repair before it finds the best subset.

## Relation to published methods

These relations place the mechanisms in context. The entry does not claim that
their combination is new across the literature.

- **EASY and conservative backfilling**
  ([Mu'alem and Feitelson, 2001](https://doi.org/10.1109/71.932708)). Like
  conservative backfilling, the scan reserves every blocked job. The
  reservations use shortened planning durations and last for one call only.
- **Lookahead Optimizing Scheduler**
  ([Shmueli and Feitelson, 2005](https://doi.org/10.1016/j.jpdc.2005.05.003)).
  LOS uses dynamic programming to fill the free processors. Here, a subset-sum
  search is a selective repair with a request filter and a gain threshold.
- **Prediction-based backfilling**
  ([Tsafrir, Etsion, and Feitelson, 2007](https://doi.org/10.1109/TPDS.2007.70606)).
  That work separates the runtime used for scheduling from the user's limit.
  Here, the planning duration is a deterministic function of the request, the
  class mean, and the count of waiting jobs of the same width.
- **WFP3**
  ([Tang et al., 2009](https://doi.org/10.1109/CLUSTR.2009.5289206)). EASY with
  WFP3 priority, `k_j (w_j / ŝ_j)^3` for waiting time `w_j`, was the strongest
  published comparator in the evaluation.

## Implementation and checks

[`implementation/policy.py`](implementation/policy.py) needs Python 3.9 or later
and only the standard library. It implements `choose(state, memory)` with the
default parameters. It also accepts the keyword arguments `comparison_factor`
and `gain_threshold` for sensitivity checks. From this entry's directory, run
the regression test:

```bash
python3 implementation/smoke_test.py
```

The test checks decisions on deterministic states, including decisions
recorded from the evaluated source. It does not measure performance. See
[evaluation/README.md](evaluation/README.md) for the archived results and their
limits.
