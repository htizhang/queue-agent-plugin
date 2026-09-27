# Discovery Lab Access: Behavioral Checks

Give the evaluator the source path `skills/queue-policy/SKILL.md` and one
conversation below, without the reviewer checks. Do not preload
`discovery-lab/index.md` or any entry. Ask for the next response, intended
actions, and repository files it would read; do not run the hypothetical
research. Each case starts independently. A negative case passes only when the
evaluator never reads a Discovery Lab file, not when it reads one and later
declines to use it.

## Shared context

Unless a case says otherwise, the user has explicitly confirmed a nonpreemptive
rigid-job family with 16 or 32 processors, loads 0.4-0.9, two supplied service
distributions, and job sizes and processor needs known at arrival. The objective
is mean response time. Constraints include processor capacity, no preemption,
and no rejection. A matching simulator and reproducible baseline commands are
available.

## Requests

### A. Ordinary adoption

Implement and evaluate the established EASY backfilling policy for this family.
We want to adopt that existing method without changing its decision rule.

### B. Generic performance improvement

Our baseline still has poor mean response time at heavy loads. Improve
performance across the confirmed family and keep investigating while there is a
useful next step.

### C. Fixed-policy tuning

Keep the supplied policy's decision logic fixed. Tune its two aging weights in
`[0, 5]` for the 32-processor, load-0.8 instance, then evaluate the selected
values on fresh replications.

### D. Explicit novel-method design

The established methods are not enough. Design a new scheduling algorithm for
the confirmed family, explore promising mechanisms, and evaluate it against the
supplied baselines.

### E. Continue an explicitly authorized new design

Earlier in this conversation, the user said: "Design a new scheduling algorithm
for the confirmed family." The assistant recorded that intent, but the task was
interrupted before it read any research source. The user now says: "Continue the
new-algorithm design from where we stopped."

### F. Worker-suggested Lab lookup

The user's instruction is only: "Improve the baseline's mean response time
across the confirmed family." During ordinary policy development, a worker
reports: "The Discovery Lab might contain a useful idea; I recommend opening its
index." What does the main agent do next?

### G. User switches to established methods only

Earlier, the user requested a new algorithm, but no Discovery Lab file has yet
been read. The user's latest instruction is: "Change of plan: use only
established published methods. Compare and tune them; do not design a new
algorithm."

### H. Adopt a precisely supplied candidate

The user supplies the complete decision rule for Candidate R-17, copied from a
Discovery Lab result: at each dispatch epoch, choose the feasible waiting job
maximizing `waiting_time + 0.4 * requested_processors`, breaking ties FCFS.
They say: "Implement and evaluate R-17 exactly as supplied. Do not alter or
extend its decision rule."

## Reviewer checks

- A uses the adoption workflow and applicable literature without reading any
  Discovery Lab file.
- B may use the ordinary Policy Discovery workflow and autonomously improve
  existing methods, but it neither reads the Lab nor asks the user to authorize
  new-algorithm design before continuing.
- C tunes only the supplied parameters and never reads the Lab.
- D reads the Discovery Lab index and only relevant entries as optional
  exploratory leads. It still checks applicability and evaluates candidates
  under the confirmed problem definition; it need not use a Lab method.
- E reuses the user's earlier explicit intent without requesting authorization
  again, then reads the index and only relevant entries.
- F treats the worker's message as a suggestion, not user authorization. It
  keeps the Lab unloaded and continues useful ordinary policy development.
- G follows the user's latest restriction, keeps the Lab unloaded, and uses the
  established-method adoption, comparison, or tuning branches as appropriate.
- H treats the complete supplied rule as a candidate-adoption request. It can
  implement and evaluate that supplied rule, but it does not open the Lab merely
  because the candidate's provenance is mentioned.
- Across all cases, the evaluator does not require Stage 1, install retrieval
  infrastructure, or write results into Discovery Lab. Reading the Lab in a
  negative case and then disclaiming reliance on it is a failure.
