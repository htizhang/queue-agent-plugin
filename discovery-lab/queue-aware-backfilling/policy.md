# Queue-aware optimistic backfilling

> **Discovery Lab status:** This is agent-discovered exploratory research. It is
> not a peer-reviewed authoritative baseline, and the reported experiments do
> not establish a universal state-of-the-art result.

## Problem and objective

The policy addresses an online rigid multiserver-job queue with one pool of
`n` identical resource units. Job `j` arrives at `a_j`, requires `k_j` units
simultaneously, and runs nonpreemptively for an unknown duration `s_j`. At
arrival, the scheduler receives an estimate `e_j` satisfying `s_j <= e_j` in
the evaluated model.

At each arrival or completion, the policy observes:

- free capacity and the waiting and running jobs;
- each job's arrival, width, runtime estimate, and class;
- elapsed time for running jobs; and
- public class probabilities and mean service times.

It may start any feasible subset of waiting jobs. It does not observe future
arrivals or unfinished jobs' actual durations. The objective is mean response
time,

```math
\frac{1}{|J|}\sum_{j\in J}(c_j-a_j),
```

for a fixed scored cohort that is drained to completion.

## Policy

The policy combines a queue-dependent priority, a local packing repair, and an
advisory capacity calendar. All quantities below are recomputed at each policy
call.

### 1. Priority order

Let `f` be current free capacity, `q_z` the number of waiting class-`z` jobs,
and

```math
\bar{s}=\sum_z p_z\mu_z.
```

Each waiting job receives

```math
P_j =
\log(e_j/\bar{s})
- 1.1\log(k_j/n)
- 0.8\log q_{z_j}
+ 0.85\,\ell_j,
```

where

```math
\ell_j =
\begin{cases}
(f-k_j)/n, & k_j\le f,\\
1, & k_j>f.
\end{cases}
```

Sort by increasing `(P_j, a_j, id_j)`. The terms favor short estimates, wide
jobs, backlogged classes, and jobs that leave a smaller immediate gap.
`\bar{s}` only makes the duration term dimensionless; as a common positive
factor, it does not change the order.

### 2. Packing repair

Let `F` be the priority-ordered jobs that individually fit in the current free
capacity. Greedily scan `F`, admitting each job that still fits, and call the
resulting used width `G`.

When at least two jobs fit but all of `F` cannot start together:

1. Let `j*` be the first job in `F`.
2. Keep only jobs whose estimate is at most 2.5 times `j*`'s estimate.
3. Use subset-sum dynamic programming to find a subset `B` with maximum total
   width no greater than `f`.
4. If `width(B) - G >= 0.10 n`, stably move `B` to the front of the priority
   order.

The repair changes order only. The calendar still decides whether each promoted
job may start.

### 3. Queue-aware planning durations

Let `m_k` be the number of waiting jobs of width `k`, and let
`m_max = max_k m_k`. For job `j`, define

```math
g_j = 1 + 2\frac{m_{k_j}}{m_{\max}},
\qquad
h_j =
\begin{cases}
\min\{1,k_j/(n-k_j)\}, & k_j<n,\\
1, & k_j=n.
\end{cases}
```

Its planning duration is

```math
d_j = 0.35\,e_j\,g_j^{-h_j}.
```

Common waiting widths therefore receive more optimistic, shorter planning
windows. The width exponent makes the extra shortening stronger for wide jobs.
This duration is used only for planning; it neither changes nor predicts the
job's actual service.

### 4. Advisory calendar

Build a step-function calendar from running jobs. A running job `r` is planned
to release at

```math
t+\max(e_r-\operatorname{elapsed}_r,10^{-9}).
```

Running-job estimates are not shortened. Scan the repaired order:

- Start a job now only when it fits both actual free capacity and the calendar
  throughout `[t, t+d_j)`, then subtract its width over that interval.
- Otherwise, for at most six blocked jobs, reserve the earliest interval of
  length `d_j` with enough planned capacity.
- Continue scanning after blocked or unreserved jobs, so later jobs may
  backfill.

The reservations are rebuilt on the next call; they are planning devices, not
persistent start-time guarantees. Once started, a job keeps its actual capacity
until completion. If no jobs are running and the scan starts nothing, the first
feasible job in the repaired order starts as a deadlock guard.

```text
order <- priority(waiting)
order <- max-fill repair(order, free, estimate span=2.5, gain=0.10*n)
calendar <- raw estimated releases of running jobs
starts <- []

for job in order:
    d <- 0.35 * estimate * queue_width_level(job)^(-width_exponent(job))
    if job fits actual free capacity and calendar for [now, now+d):
        start job and place it in the calendar
    else if fewer than 6 reservations have been placed:
        reserve its earliest calendar interval of length d

return starts, with an empty-pool fallback if needed
```

## Applicability and limits

This policy is a research lead for a single homogeneous resource dimension,
rigid simultaneous requirements, nonpreemptive service, and useful upper-bound
runtime estimates. The reported tests used 32, 128, and 512 units and synthetic
workloads with exact or conservatively loose estimates.

Applicability is untested for multiple resource dimensions, placement
constraints, preemption, malleable jobs, inaccurate estimates that are not
upper bounds, or objectives that prioritize tails or fairness. The subset-sum
routine is exact at the tested capacities; its portable implementation retains
the original 4,096-reachable-total guard for larger instances. The experiments
drained every workload, but they do not prove stochastic stability or
starvation freedom.

## Relation to published baselines

The policy combines mechanisms related to established work without claiming
that their combination is literature-wide novel:

- Its provisional reservations and backfilling are related to EASY and
  conservative backfilling, but it protects up to six advisory calendar entries
  rather than EASY's protected head-job reservation
  ([Mu'alem and Feitelson, 2001](https://doi.org/10.1109/71.932708)).
- Its subset selection resembles the local packing goal of the Lookahead
  Optimizing Scheduler, but uses a duration-bounded maximum-fill repair and a
  material-gain trigger
  ([Shmueli and Feitelson, 2005](https://doi.org/10.1016/j.jpdc.2005.05.003)).
- Its deliberately shortened planning windows are related to prediction-based
  backfilling's separation of scheduling durations from execution limits, but
  here the shortening is a deterministic function of the current width
  histogram
  ([Tsafrir, Etsion, and Feitelson, 2007](https://doi.org/10.1109/TPDS.2007.70606)).
- EASY-WFP3 is an important evaluated comparator. WFP3 prioritizes
  `k_j(wait_j/e_j)^3`; this policy instead couples the priority above with
  packing repair and a queue-aware calendar
  ([Tang et al., 2009](https://doi.org/10.1109/CLUSTR.2009.5289206)).

See [evaluation/README.md](evaluation/README.md) for the bounded evidence and
its generalization limits.
