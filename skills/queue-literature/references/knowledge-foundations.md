# Model-Policy Fit

| Field | Value |
| --- | --- |
| ID | foundations.model-policy-fit |
| Kind | foundations |
| Stage relevance | Stage 1, Stage 2 |
| Aliases | model fit, policy fit, result transfer, Kendall notation, information model, exact size, size estimate, attained service, waiting age |
| Sources | scully_harchol_balter_2021_gittins, van_mieghem_1995_gc_mu |
| Review | source-checked |
| Reviewed on | 2026-09-25 |
| Legacy origin | queue-research a0dc5cc: adapted from docs/policy_science_kb/sources/textbook_foundations.md and new synthesis |

## Mechanism

A source's guarantee applies only when the target meets its assumptions on
five points:

1. **System:** stations, servers, jobs needing several servers at once,
   arrival and service processes, classes, load.
2. **Observations:** what the data record, and when.
3. **Control:** feasible actions, especially preemption and its overhead.
4. **Information:** what the controller knows at each decision.
5. **Objective:** exact cost, averaging or horizon, exact or asymptotic
   optimality.

Kendall notation (A/S/c and extensions) omits information, actions, costs, and
simultaneous-server needs. An M/G/1 scheduler that knows remaining sizes and
one that knows only attained service face different job models
([scully_harchol_balter_2021_gittins](sources.json), Section III, Examples
III.1-III.2).

## Applicability

Keep these information models apart:

- **Exact remaining size:** known before completion; a duration logged at
  completion is hindsight.
- **Size estimate:** a noisy prediction, not an exact size or a bound.
- **Service distribution plus attained service:** a known size law and each
  job's service so far.
- **Waiting age:** time spent waiting, not service received.

| Card | Decision-time information | Reviewed result |
| --- | --- | --- |
| [c-mu](policy-c-mu.md) | class service rates and linear cost rates | exact; class-weighted mean response time |
| [Generalized c-mu](policy-generalized-c-mu.md) | class service rates, marginal delay cost, each class's oldest waiting age | heavy-traffic asymptotic; finite-horizon convex delay cost |
| [SRPT](policy-srpt.md) | exact remaining sizes | exact; mean response time |
| [Gittins](policy-gittins.md) | job state such as attained service; known job model and holding costs | exact; mean holding cost |

All four concern one station, each job using one server at a time; the cards
give full models. No Stage 1 estimation, censoring, nonhomogeneous-Poisson, or
model-validation procedure is included.

## Evidence

Source results: in [scully_harchol_balter_2021_gittins](sources.json) (arXiv
v1), a job's state encodes all the scheduler knows and stays fixed while the
job waits (Sections III, III.A). Theorem V.1 is exact: Gittins minimizes
equilibrium mean holding cost among policies using only current and past
system states, within the model and premises of Sections III.A-III.G. In the
1994-10-25 manuscript of [van_mieghem_1995_gc_mu](sources.json), cost is
nondecreasing convex in time in system over a finite horizon, waiting jobs'
service times are unobservable, and optimality is heavy-traffic asymptotic
(Section 2).

Interpretation (this guide's synthesis): the checklist and table. Theorem V.1
compares policies within one job model; on our reading of Sections III.A and
III.F, an estimate would have to be job state with a known conditional size
law, so raw-estimate ranking inherits no guarantee. Since a waiting job's
holding cost is fixed, costs growing with waiting time lie outside Theorem V.1;
convex delay cost is the generalized c-mu setting.

## Use in this Plugin

Stage 1: record the five points for the intended policy question, separating
decision-time information from values revealed later; leave unknowns open.
Stage 2: check all five before citing a guarantee. Jobs needing several
servers, unavailable preemption, or noisy estimates instead of exact sizes make
a policy a disclosed adaptation or heuristic baseline, evaluated on the target
objective; report missing state or actions as a gap. This small, dated
collection cannot establish current novelty.
