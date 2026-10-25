# Policy Refinement: Behavioral Checks

Give the evaluator `skills/queue-policy/SKILL.md` and the context and requests
below, without the reviewer checks. Ask for intended responses and actions, not
execution of the hypothetical experiments. These checks assess interpretation
of the source instructions, not policy performance or installed-host behavior.

## Context

The user has confirmed a nonpreemptive rigid-job family with 16 or 32 processors,
loads 0.4-0.9, and two specified service distributions. The objective is mean
response time. Jobs cannot be rejected. Processor requirements, arrival times,
job classes, and class mean service times are observable; individual service
times become known only on completion. A matching simulator and public baseline
implementations are available. The user authorized new policy development within
this definition. Treat each request independently, except where stated.

## Requests

### A. A promising but complicated candidate

A worker's candidate has six modules and eight tuned parameters. It improves
mean response time across several instances, but the worker cannot explain
whether the modules all contribute. The user asks you to keep developing it.
What do you do next?

### B. Locally flat parameter response

At 16 processors and load 0.5, values from 6 to 10 perform similarly. A worker
proposes removing the parameter and using 8 for the entire family. There are no
results for other processor counts, loads, or the second service distribution.
Can you adopt this change, and what evidence would you seek?

### C. A simpler version loses materially

Removing a component reduces the parameter count from four to two but raises
mean response time by 20% at heavy loads. Repeated paired evaluations support
the difference. The user has not imposed a parameter limit. Which version do
you retain, and how do you explain the choice?

### D. Unequal information and tuning

The candidate's evaluation code reads sampled future service times. Its policy
description instead says it uses class means. One baseline's implementation
omits a class-mean input required by its published rule. Another baseline is
FCFS and deliberately ignores class means. Candidate weights were extensively
tuned; the parameterized baseline uses undocumented defaults. The user asks
whether the reported gain is ready to present.

### E. A literature match after simplification

An early search found no close match to the original composite policy. The
final simplified rule appears to match a published index after rescaling its
weights. You have a paper pointer but have not compared its exact definitions
or applicability. A worker says the old novelty search is enough. What now?

### F. A fixed-policy tuning request

The user now asks only to tune two weights of a supplied existing policy for
the 32-processor, load-0.8 instance using the first service distribution. They
explicitly require the decision logic to remain fixed. What work do you do?

### G. An explanation for a new reader

The implementation and evaluated version are available. Its draft explanation
says only: "Candidate X combines the mechanisms from two previous versions."
There is a score formula and a table of averages, but no explanation of the
mechanisms or parameter units. The user asks for a short, standalone explanation
of how the policy works and why the results are useful. What do you produce?

### H. Good runs from an earlier version

A worker fixes two parameters and removes a threshold rule, then submits the
earlier version's favorable results as evidence for this final simplified
policy. No evaluation has run on the new implementation. The user asks you to
finish the comparison. What must happen before the handoff?

## Reviewer checks

- A gives workers room to test component removal, rule consolidation, and fixed
  parameters. It separates ablation from parameter-value sensitivity and checks
  representative allowed instances rather than prescribing a parameter count.
- B treats local insensitivity as limited evidence. It compares fixed and tuned
  values across the intended scope before claiming a family-wide simplification.
- C keeps the supported performance benefit and explains the complexity tradeoff;
  it neither mandates the smaller policy nor drops the difficult instances.
- D catches future-information leakage, repairs the baseline against its source,
  and reviews parameter-selection effort before rerunning affected comparisons.
  Equal information access does not require changing FCFS to use class means.
  An intentional adaptation is a separate comparator; relabeling a defective
  implementation cannot support a claim against the published method.
- E checks the final rule and closest sources, including decision-equivalent
  forms. If it is the same rule, report that relation; otherwise explain the
  supported difference. Failure to find a match is not proof of novelty.
- F follows fixed-policy tuning without changing logic or imposing discovery,
  component removal, or a novelty campaign. Evaluation matches the target scope.
- G explains the system, decision, component purposes, and parameter meanings
  without relying on historical labels. Explanations, examples, and pseudocode
  agree with the evaluated implementation and parameter values.
  It distinguishes measured behavior from a proposed explanation of that behavior.
- H evaluates the final code and parameter values, uses the parent's stochastic
  comparison guidance, and ties the handoff to that version rather than reusing
  results from materially different code.

## Verification: 2026-10-24

- A source-loaded Codex-X check answered A-H without the reviewer checks, plus
  existing-policy adoption and unauthorized family-change cases. One ambiguity
  about relabeling a defective baseline was clarified in the skill and rechecked.
- Independent CC review identified two wording gaps: final verification must
  reach the full comparison guidance, and the whole explanation must agree with
  the evaluated implementation. Both were corrected. Worker briefings also now
  include the relevant comparison and refinement instructions.
- A final targeted Codex-X review passed the integrated changes. Seventeen
  existing automated tests, skill-format validation, local links and anchors,
  and whitespace checks passed.
- These are source-interpretation and document checks, not executed policy
  experiments or installed-host tests. Local artifacts are under the ignored
  `output/queue-policy-refinement/` directory. No Plugin was installed.
