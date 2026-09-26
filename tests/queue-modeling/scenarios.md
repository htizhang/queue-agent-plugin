# Queue Modeling: Behavioral Checks

These scenarios test source-loaded instructions, not installed-host discovery.
Give the evaluating agent the request, skill path, and task inputs, but not the
reviewer checks. Put any generated models or test outputs in a temporary task
workspace.

## A. Build a small model with replaceable policies

### Request

Use queue-modeling to build a small simulator from a fully observed, single-server
FCFS event log and system description. Each record has arrival, service-start,
and departure times in minutes and a job class. Service is nonpreemptive. Keep
the implementation small; make the dispatch rule replaceable and report what
you actually checked. Work locally with available tools.

### Reviewer checks

- Uses service-start to departure durations for service observations and fits or
  resamples arrivals separately.
- Delivers executable code, configuration, and a working run command.
- Keeps dispatch replaceable and limits policy observations to available
  information; does not automatically launch a policy-search campaign.
- Runs checks of resource capacity, event order, and agreement with the data.
- When delegation is available, gives a validator the original inputs and
  executable candidate and integrates its evidence rather than just its verdict.

## B. Review a candidate against an observed trace

### Request

Use queue-modeling to validate the supplied candidate simulator against the
system description and event log. The candidate supports FCFS and shortest-job
first, with job size known at arrival. Diagnose disagreements using actual runs.
Review only: do not edit the candidate, search online, or install anything.

### Fixture and reviewer checks

Use a three-job, one-server nonpreemptive case with arrivals `(0, 1, 2)`, known
service requirements `(4, 3, 1)`, and observed FCFS starts `(0, 4, 7)` and departures
`(4, 7, 8)`. The candidate mistakenly calibrates service as departure minus arrival.
Keep this paragraph out of the evaluation prompt; supply the raw CSV and code.

- Runs the candidate, compares its trace with observations, and localizes the
  service-time error using records and code.
- Separates this deterministic implementation check from a claim about fitted
  stochastic behavior or general model adequacy.
- Exercises both policy paths, respects nonpreemption and the stated size
  information, and provides reproducible feedback without editing the code.

## C. Discuss an underdetermined model

### Request

We only record arrival and departure timestamps and a customer category. We
have no service starts or staffing history. Discuss what model we can build;
do not implement anything yet.

### Reviewer checks

- Separates observed sojourn times from service requirements and identifies the
  material missing information without inventing a unique fitted model.
- Explains useful working assumptions or alternatives and asks only focused
  questions that change the model.
- Respects discussion-only scope and consults relevant bundled knowledge when
  needed rather than launching an implementation or a broad literature review.

## Verification record: 2026-09-26

- Skill format, repository-local links, English content, and whitespace checks
  passed. The seven existing queue-literature content tests also passed.
- A source-loaded codex-x agent (`openai.gpt-5.6-sol`, requested max effort)
  completed B. Its tool log confirms both policy executions. It identified the
  calibration error, reported the incorrect FCFS departures `(4, 10, 16)`, and
  derived the correct SJF order and timing from the supplied observations.
  It respected the read-only scope and returned reproducible feedback.
- A and C are defined scenarios, not completed live-agent tests. This check did
  not exercise automatic skill discovery, host-managed validator spawning, or
  end-to-end simulator construction. No Plugin was installed.
