# Queue Literature: Behavioral Checks

These small, synthetic cases test instruction behavior, not scientific findings.
They require no network retrieval, datasets, or installed Plugin. For an explicit
loading check, ask the host to read `skills/queue-literature/SKILL.md`, then give it
only the relevant request and source cards below, without the reviewer checks.
Keep the host read-only and write any run artifacts outside the skill directory.

For a separate routing check, expose only the skill name and description, then
ask whether it fits each request.

A passing case meets its listed checks. It does not verify every other deduction
in the answer. The cases are not a literature benchmark or an estimate of the
skill's benefit, and they do not test automatic discovery, installed-host
behavior, or live retrieval.

## A. Stage 1: observations and model choice

### Request

We have arrival and departure timestamps, a job-class label, and a known count
of four servers; no service-start timestamps. Based only on the supplied source
cards, which modeling approach is applicable and what remains unknown? Keep this
to a short literature-based recommendation, not fitting or coding.

### Source cards (fictional, not real publications)

- **S1, Methods section:** Model M estimates service distributions from individual
  service-start and completion pairs. Each job occupies one server; servers are
  identical. It assumes arrivals and service requirements are independent.
- **S2, Methods section:** Model N fits the observed arrival-to-departure
  distribution directly as a total-time predictor. It does not decompose waiting
  and service and does not estimate a queue's latent service distribution.

### Reviewer checks

- Separates total time from service time and identifies the missing starts or
  additional identification assumptions.
- Does not conclude that the observations establish an M/M/4 queue, identical
  servers, or independence.
- Can recommend N for total-time prediction without presenting it as full queue
  identification; describes what M would require.
- Grounds conclusions in S1/S2, invents no real citations, and runs no fitting.

## B. Stage 2: baseline applicability and prior art

### Request

Our model has jobs arriving over time. Each job needs k processors simultaneously
for an estimated duration, cannot be preempted, and has no future-arrival
information. We minimize mean response time. Our proposed rule combines the
reservation mechanism in P1 with the waiting-age preference in P2. Based only
on these cards, identify useful baselines and explain what we can say about the
combination. Do not run experiments or conduct an external search.

### Source cards (fictional, not real publications)

- **P1, Algorithm section:** An online nonpreemptive multi-processor-job policy
  reserves a start time for the first waiting job using declared duration upper
  bounds. Other jobs can start only when that reservation is preserved. It reports
  mean response time. The card gives no universal performance guarantee.
- **P2, Algorithm section:** An online policy on the same simultaneous-resource
  model ranks currently feasible jobs by waiting age. It makes no reservation.
  It reports mean response time.
- **P3, Theorem section:** An offline preemptive scheduler, knowing all release
  times and exact processing requirements in advance, has a makespan bound.
- **P4, Abstract only:** A method combines a reservation with a queue-state-based
  ranking. The abstract gives no ranking formula or information assumptions.

### Reviewer checks

- Treats P1/P2 as relevant comparators but notes P1 needs upper bounds, whereas
  the target only says estimates; requires clarification or a disclosed adaptation.
- Distinguishes a scheduling priority from the response-time evaluation metric.
- Does not treat P3 as a directly comparable online baseline or transfer its
  makespan guarantee to response time.
- Recognizes the proposed combination's component overlap with P1/P2 and the
  unresolved close match with P4; does not claim proven novelty from four cards.
- Does not silently change the family or objective, search, or simulate.

## C. Non-trigger and scope checks

Using only the skill description, distinguish these requests:

- "Find papers about inferring service distributions from partial event logs."
  Literature guidance applies (Stage 1).
- "Which published routing policies fit a network with finite buffers?"
  Literature guidance applies (Stage 2).
- "Rename this output file."
  The skill is unnecessary.
- "Implement FCFS in this already-specified simulator; no research needed."
  The skill is unnecessary.

## D. Local knowledge: an established policy question

### Request

Use the bundled knowledge only; do not search online. We have one server,
independent Poisson class arrivals, independent exponential service with known
class rates, load below one, and zero-overhead preempt-resume. We minimize
long-run mean linear class holding cost. What does c-mu prescribe and what does
the bundled source establish? Distinguish waiting age from attained service.

### Reviewer checks

- Reads the local c-mu card and source registry rather than inventing citations.
- Gives descending c_i times mu_i; identifies the single-server, information,
  cost, and preemption scope of the recorded result.
- Does not claim this session read a primary PDF merely because the card was
  previously source-checked.
- Does not call the web, install anything, or run a simulation.

## E. Local knowledge: information and action mismatch

### Request

Use the bundled knowledge only; do not search online. Our jobs each occupy
several processors at once, cannot be preempted, and have only noisy duration
estimates. Does the local SRPT or Gittins theorem certify optimal mean response
time for this system? What would need adapting?

### Reviewer checks

- Finds the SRPT and Gittins cards and rejects transfer of their exact guarantees.
- Separates simultaneous-resource jobs from one-server jobs, unavailable
  preemption from a feasible dispatch rule, and noisy predictions from exact
  remaining size or a modeled service-time distribution.
- Keeps the Gittins card's distinctions in any explanation: nonclairvoyant
  means using only the declared current and past states, not necessarily
  unknown sizes, and jobs with equal attained service can have different
  indices under different class-conditional size laws.
- May suggest disclosed heuristic adaptations, not a hidden family change.

## F. Local knowledge: a genuine Stage 1 coverage gap

### Request

Use only this skill's bundled knowledge; no web or fitting. We have arrival and
departure timestamps but no service starts, selective logging of only slow jobs,
and suspected self-exciting arrivals. Which bundled procedure jointly identifies
the service distribution and arrival model under these conditions? If no such
procedure is bundled, tell me directly.

### Reviewer checks

- Recognizes the observation mismatch with the partial-task inference card and
  that the call-center note is not a joint estimator for this observation scheme
  and arrival model. No such general procedure is supplied by these cards.
- Does not treat arrival-to-departure observations as service samples or invent
  a local method/source. Can state what evidence or literature would be needed.

## G. Local knowledge: current prior art needs more evidence

### Request

Can the bundled knowledge establish that nobody has published my new
state-dependent scheduling index as of today? Do not conduct the external
search now; explain whether the local material settles the question.

### Reviewer checks

- Does not turn a small dated reference collection into a novelty certificate.
- Explains that mechanism comparison and current external literature are needed,
  while respecting the request not to start that search now.

## H. Expanded Stage 1: inspect before transferring

### Request

Use only the bundled cards. Can I apply the partial-log method to a dataset that
keeps only slow tasks and has no count of unlogged traffic? Separately, can I
estimate patience from abandoned callers alone?

### Reviewer checks

- Finds both modeling cards and distinguishes their observation assumptions.
- Identifies the missing workload counts and different logging mechanism.
- Recognizes the censoring information contributed by served callers and the
  conditional-independence assumption; does not declare patience identified.

## I. Expanded Stage 2: throughput versus delay

### Request

Use only the maximum-pressure card. Does its recorded theorem prove finite
steady-state mean response time for arbitrary nonpreemptive multiprocessor jobs?

### Reviewer checks

- States the actual pathwise rate-stability conclusion, rather than upgrading it
  to finite expected delay or positive recurrence.
- Identifies the action/structure mismatch and the separate nonpreemptive scope.

## J. Expanded Stage 2: reservation details

### Request

Use only the backfilling card. Must an EASY backfill job always finish before
the first queued job starts? Can I replace runtime bounds with predictions
without changing reservation guarantees?

### Reviewer checks

- Distinguishes the finish-before-start condition from the spare-capacity case.
- Identifies missing runtime-bound enforcement instead of certifying predictions.

## K. Fitted-model checking

### Request

I fitted an exponential mean on these same observations. Can I use ordinary
fixed-parameter KS cutoffs? Explain the bundled bootstrap alternative and whether
it applies unchanged to censored, dependent event records.

### Reviewer checks

- Finds the fitted-distribution card; refits on each simulated sample.
- States the iid continuous-family and asymptotic regularity scope, rather than
  promising an exact test for dependent or censored records.

## L. Reentrant stage-priority scope

### Request

Our fab is nonpreemptive, has finite buffers and sequence-dependent setups.
Does the bundled FBFS/LBFS result prove its stability and minimum cycle time?

### Reviewer checks

- Distinguishes a feasible heuristic adaptation from the paper's preemptive,
  infinite-buffer single-route theorem.
- Separates positive Harris recurrence from cycle-time optimality and does not
  reverse the fluid-to-stochastic stability implication.

## M. Release versus dispatch

### Request

For WIPLOAD, the remaining-work allowance exactly equals an external lot's
nominal full-route work. Does the recorded gate admit it? Does the policy also
specify how stations dispatch jobs?

### Reviewer checks

- Includes equality in the release condition.
- Separates the release gate and external priority from station dispatch.
- Describes the cited comparisons as simulation evidence, not universal dominance.
