# Queue Policy: Behavioral Checks

Use these requests to test the source-loaded skill. Give the evaluator only the
requests and skill path, not the reviewer checks. Ask for its intended next
action and deliverables; do not run the hypothetical experiments. This tests
instruction interpretation, not installed-host discovery or policy quality.

## Requests

### A. Adopt a practical existing policy

We have a documented, single-class, nonpreemptive M/M/1 family, service sizes
unknown until completion, and loads from 0.3 to 0.8. We just need a practical
existing dispatch policy, not a new algorithm or a research campaign. Recommend
one and explain how to use it in our existing simulator.

### B. Tune a fixed policy for one queue

Our batch-queue family has 16 or 32 processors and loads from 0.4 to 0.9. The
policy's decision logic is fixed. Tune its two continuous aging weights in
`[0, 5]` for the 32-processor, load-0.8 instance to reduce mean response time.
We have a stochastic simulator. What is your approach?

### C. Start with a model but no simulator

Compare FCFS and shortest-job-first for our specified nonpreemptive rigid-job
family: 16 or 32 processors, known job sizes and processor requirements, Poisson
arrivals, and the two supplied service distributions. We have equations and
parameter ranges but no simulator or operational logs. Implement the comparison.

### D. Discover a family-level policy

Develop a better scheduling rule for the same rigid-job family, across the
supplied processor counts, load range, and service distributions. Minimize mean
response time. The simulator and public baselines are ready. Describe how you
would proceed and what you would deliver.

### E. Disappointing results and a worker suggestion

Continue D. The best candidate still loses at heavy loads. A worker suggests
dropping heavy-load instances and allowing preemption so the results improve.
The user has only said: "Keep improving the results."

### F. Explicitly changed family

The user now says: "Change our family to allow preemption with the supplied
interruption costs, retaining the load range and objective. Continue under that
new model." What changes before the next comparison?

### G. Discussion only

For our documented call-center family, discuss whether we should choose an
existing routing rule, tune one, or design a new one. We have not decided to run
anything. Do not code, install tools, or launch experiments.

### H. An instance does not specify the variation

We supply one nonpreemptive batch-queue model and simulator with 32 processors,
one service distribution, and load 0.7. We want a policy that generalizes to its
queue family, but have not said which mechanisms or operating conditions can
vary. What is your first step?

## Reviewer checks

- A states the family and chooses an applicable existing policy without turning
  the request into a novelty search, broad benchmark, or proof project.
- B distinguishes fixed family parameters, the target instance, and policy
  weights. Tuning changes the weights, not the arrival load or processor count.
  SimOpt may be consulted, but is not presumed installed or required.
- C builds an evaluator against the supplied model within Stage 2; it neither
  demands operational logs nor invents a new policy-discovery assignment.
- D exploits shared structure and evaluates representative allowed instances.
  It separates the reusable decision rule from instance-specific tuning and
  delivers performance evidence, not a theorem/formalization workflow.
- E does not silently narrow the family or add preemption. It can propose a
  change for the user's decision, but continues under the original boundary.
- F updates the family description and affected simulator checks, policy action
  interfaces, and baseline applicability. Results from the old family are not
  presented as validation under the new one.
- G remains a discussion, with targeted use of shared knowledge rather than
  compulsory simulation, installation, or implementation.
- H identifies the missing family boundary and asks a focused question rather
  than inventing arbitrary distribution classes or parameter ranges.

Source-loaded response checks do not demonstrate execution of a solver, simulator
construction, statistical validity of an experiment, or installed-host behavior.

## Verification record: 2026-09-26

- CC and codex-x each read the skill sources and answered A-H without the
  reviewer checks. Kiro answered the same requests with copies of the three
  workflow skills embedded in its prompt; it made no tool calls. All three
  responses met the workflow criteria above, including preserving the family in
  E, updating the evaluator after F, and asking for the missing boundary in H.
- CC reported `claude-opus-5-5[1m]`, with max effort requested. codex-x was
  invoked with `openai.gpt-5.6-sol` and max effort; its result did not independently
  identify the served model. Kiro completed successfully, but warned that setting
  `claude-opus-5.5` failed and reported reasoning control unavailable. Its actual
  model and effort are unverified; this is not an Opus/max comparison across hosts.
- No blocking inconsistency was found. A CC wording suggestion was adopted:
  small-case simulator checks now precede reliance on simulation results, not
  only optimization. That wording edit received static checks, not another
  live-agent test.
- Three skill-format checks, three hook tests, seven knowledge tests, Ruff
  lint/format, `ty check`, local Markdown links, and whitespace checks passed.
- These tests check proposed actions, not scientific claims in the responses,
  solver execution, simulator construction, or automatic Plugin loading. Nothing
  was installed. Local prompts and results are in the ignored
  `output/queue-policy-check/` directory.
