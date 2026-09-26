# From a System Description to Queue Primitives

A queue model specifies what waits, which resources it needs, how work enters and
leaves, and which decisions are possible. Start with these facts, then choose
distributions and notation. A label such as `G/G/c` does not specify resource
compatibility, feedback, observations, or the controller's information.

## Choose the system boundary and the unit of work

Define the customer or job around the outcome of interest: a call, a hospital
visit, a production lot, or a computing job. Distinguish a whole customer journey
from one station visit. A job can require several resources simultaneously or
split into parallel tasks; preserve that structure rather than forcing it into
an ordinary multi-server queue where each job occupies one server.

Record the following primitives. The classical arrival, service, discipline,
capacity, and waiting-room distinctions are described by Adan and Resing,
Section 3.1 ([adan_resing_2015_queueing_systems](sources.json)); the decision and
observation distinctions below are modeling synthesis.

| Primitive | What the model must specify |
| --- | --- |
| Stations and resources | Where work waits; resources used at each step; server counts, speeds, availability, compatibility, and simultaneous resource requirements. Overlapping skill sets need an eligibility relation, not necessarily disjoint pools. |
| Classes | Attributes that affect service, patience, routing, feasibility, costs, or policy decisions. A station visit can change class. |
| Offered arrivals | Times and attributes of requests presented to the system, including rejected requests; time variation and dependence, not just a mean rate. |
| Service work | Required work and its units; how allocated capacity converts work into elapsed time; setup, interruptions, and resource-release rules. |
| Waiting and exits | Waiting-room limits, balking before joining, abandonment after joining, rejection, routing, retrials, and later returns. |
| Operating rule | The observed sequencing, routing, batching, and preemption rules, including exceptions and tie-breaking. Do not assume FCFS without evidence. |
| Information and control | What the controller observes at each decision; which actions are permitted; physical limits versus rules that a policy may change. |
| Population and horizon | Open entry/exit versus a closed circulating population; any finite-source constraint; initial state, observation window, and end-of-horizon treatment. |
| Outcomes | What is counted and averaged: customer wait, completion time, abandonment, throughput, or cost; for which population and over which horizon. |

An **external** arrival crosses the chosen boundary. An **exogenous** input has a
law unaffected by the modeled state or control; external does not imply
exogenous. Likewise, an open system may have state-dependent demand. A finite
source limits who can generate another request; its input law must describe that
mechanism, rather than automatically assuming a Poisson stream.

Gans, Koole, and Mandelbaum distinguish blocked or abandoning callers who retry
from served callers who return, and distinguish trunk-line capacity from agent
capacity (Sections 2.2–2.4,
[gans_koole_mandelbaum_2003_call_centers](sources.json)). These distinctions
generalize: waiting space, service capacity, and feedback are different model
components. Ending a study at midnight does not make tomorrow's returning
customers independent of today's service.

## Avoid losing structure during abstraction

**Work is not elapsed time.** Intrinsic required work can be i.i.d. even when
processing speed depends on congestion. Completion then depends on accumulated
allocated processing, not only time since service started. For exclusive,
uninterrupted service at unit speed, required work equals the occupied-resource
duration. Include after-work if it prevents the resource taking another job:
call-center handle time includes talk, hold, and wrap-up time (Section 2.3,
[gans_koole_mandelbaum_2003_call_centers](sources.json)). Customer departure and
resource release need not coincide; see [event-log semantics](modeling-event-log-semantics.md).

**Merging input streams is not the same as merging classes.** Independent
homogeneous Poisson streams superpose to a Poisson stream with the sum of their
rates (Section 2.6, [adan_resing_2015_queueing_systems](sources.json)). This alone
does not justify dropping class labels. Aggregation must preserve the joint
service, patience, routing, and eligibility behavior relevant to the outcomes
and candidate controls. Matching marginal service distributions is insufficient
when, for example, service work and patience are correlated through class.

**Unknown is not independent.** An invisible queue does not establish i.i.d.
patience; a missing service-size field does not establish a particular size
distribution. Specify stochastic assumptions separately from observations and
from the information available to a policy. Balking or admission control can
make the admitted stream state-dependent even when offered demand is exogenous.

## Worked formulation: a permit counter

This is an original modeling illustration, not an empirical finding.

**Description.** Four interchangeable clerks handle new permits (N) and renewals
(R), 08:00–16:00. There are 30 waiting places, separate from the service desks.
Renewals have nonpreemptive priority, with FCFS within each class. Some waiting
applicants leave. Clerks finish filing after the applicant leaves and only then
become available. Logs contain ticket, call, and customer-close timestamps; some
applicants return on a later day.

**Model choices.**

- One job is one ticket's work through filing completion; customer departure is
  recorded separately. There is one station with four unit-speed servers.
- Offered class-`k` arrivals follow independent NHPPs with rates `lambda_k(t)`
  during opening hours. This is a proposed assumption, not a consequence of the
  description. Later-day return demand is absorbed into these rates only as an
  explicit approximation; there are no modeled same-day retries.
- Exclusive service occupies one clerk continuously through filing, with
  requirement `S_k ~ G_k`, i.i.d. within class and independent of the arrival
  processes. Work requirements are unknown to the controller before service.
- An arrival starts service if possible, otherwise waits if a place is free;
  it is rejected when all four clerks and all 30 waiting places are occupied.
  Thus at most 34 unfinished jobs are present, counting filing work.
- Conditional on class, patience has cdf `F_k` and is independent of service
  work, arrival times, and other jobs' patience. Abandonment occurs only before
  service; there is no additional voluntary balking below the cap. These are
  assumptions to check, not facts
  established by the lobby being visible.
- The model reproduces the observed priority rule. If sequencing is the
  authorized control, alternatives may select among waiting jobs using observed
  classes and waiting ages; staffing and the physical waiting-room cap remain
  fixed. Service is nonpreemptive and a free clerk takes a waiting job immediately.
- The system starts empty. Admissions end at 16:00, but clerks remain until all
  admitted jobs finish or abandon; waiting applicants retain their abandonment
  clocks during this drain period.

**Observation gaps.** Ticket-to-close time includes waiting and excludes filing;
it is neither an intrinsic-work sample nor the job's full sojourn under this
boundary. Consecutive call times can contain idle time. Use verified resource
release records or an explicit observation model rather than treating those gaps
as service samples. Ticket logs also omit rejected demand unless rejection is
recorded separately. Served waits give lower bounds on patience, not completed
patience observations. See [censoring and truncation](modeling-censoring-truncation.md)
and [time-varying arrivals](modeling-time-varying-arrivals.md).

**Load check.** If peak offered rates are `lambda_N = 20/hour` and
`lambda_R = 25/hour`, with mean occupied-clerk requirements of 9 and 4 minutes,

`a = 20 × 9/60 + 25 × 4/60 = 14/3`, and `rho = a/4 = 7/6 ≈ 1.17`.

These are offered-load diagnostics, not realized utilization. If those rates
were held indefinitely, the corresponding infinite-buffer model without
abandonment would receive more work than four clerks could process. A peak hour
does not establish instability of the finite-day model: losses, abandonment,
initial backlog, and later demand matter. Keep the time profile and both classes.

The resulting description is a two-class, time-varying, four-server queue with
finite waiting space and general patience. It is more informative than a bare
Kendall label. Next specify its [state and event dynamics](modeling-state-and-dynamics.md)
and check its [adequacy against observations](modeling-model-adequacy-validation.md).
