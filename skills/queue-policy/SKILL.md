---
name: queue-policy
description: Select, evaluate, tune, or design policies for a queue model or model family. Use for Stage 2 work from a Stage 1 handoff or a user-supplied model, including preparing a missing simulator for policy evaluation.
---

# Queue Policy

Find a policy suited to the user's queue and objective. New algorithm discovery
is one possible task, not the default. Respect discussion-only requests; perform
implementation and experiments when they are part of the requested work.

## First establish and fix the queue family

Start from the Stage 1 model and simulator, or the user's model or model-family
specification. A simulator is optional at entry. Identify the family before
selecting algorithms or starting experiments:

- Shared system structure and mechanisms: jobs, resources, arrival and service
  processes, routing, and relevant features such as abandonment or preemption.
- Control boundaries: decision timing, information available to the policy,
  feasible actions, and operational constraints.
- Permitted variation: which model parameters or operating conditions may vary,
  and their intended ranges. Distinguish these from tunable policy parameters.

State this scope concisely alongside the objective and any supplied target
instance. Use the supplied boundaries; a single instance does not establish an
arbitrary range of other systems. Ask when an ambiguity would materially change
the family or next action. Keep the agreed scope with the task's working notes.

Once established, keep the family fixed unless the user explicitly requests a
change. Poor results or a worker's suggestion do not authorize expanding,
narrowing, or replacing it. Propose a scope change to the user if warranted;
otherwise continue within the agreed family. Varying instances within its stated
ranges or tuning a policy is not a family change. If the user changes the family,
update affected evaluators and baseline choices before drawing new comparisons.

## Choose the work the problem needs

Combine the user's goal with the queue's structure and applicable existing
methods. Use [queue-literature](../queue-literature/SKILL.md) for relevant local
knowledge first, extending the search when a material question remains open.

| Need | Approach |
| --- | --- |
| An established policy already meets the need | Adopt or explain it, checking applicability. |
| Several applicable policies need comparison | Evaluate and select among them on the user's objective. |
| A policy structure is fixed but its parameter values are not | Tune those parameters for the target queue or requested operating range. |
| The user wants a new method, or existing methods need improvement | Improve or design a policy within the fixed family. |

Combine these approaches when useful. A family definition does not oblige an
adoption or tuning request to become a broad policy-discovery campaign.

## Prepare an evaluator when needed

Inspect an existing simulator's agreement with the model, policy interface,
observable information, and performance measurements. If simulation is needed
and no simulator exists, construct one for the specified model. This is Stage 2
evaluator preparation, not a requirement to collect logs or repeat Stage 1.

Keep system dynamics, replaceable policies, and objective measurements separate.
Check model-implementation agreement and action feasibility with small cases
before relying on simulation results. If a check fails, repair
the implementation against the fixed model rather than silently redefining it.
An applicable analytical evaluation can suffice for a simpler request.

## Evaluate and improve policies

For policy discovery, seek a decision rule that exploits the family's shared
structure. Develop and evaluate it across representative instances within the
agreed variation, rather than optimizing only one fixed configuration. Retain
useful candidates and their results so subsequent iterations build on prior work.

Compare policies using the same objective, feasible actions, and information
assumptions. Account for stochastic noise with repeated runs and shared random
inputs where appropriate; the literature skill's evaluation note explains paired
comparisons. Use fresh evaluation replications after tuning when needed to avoid
mistaking search noise for improvement. Report which instances were tested.

Keep policy structure distinct from parameter values. A family-level policy can
retain the same decision logic while its parameters are tuned for a particular
queue; one parameter vector need not suit every instance. Describe what is shared
and what was adapted.

For simulation-based parameter optimization, consult the external
[SimOpt repository](https://github.com/simopt-admin/simopt) and its
[solver documentation](https://simopt.readthedocs.io/en/latest/solvers.html).
Use available host tools to inspect current algorithms and implementations,
checking their fit to the variables, constraints, noise, and available gradient
information. SimOpt is an optional resource, not a bundled dependency or required
backend. Its optimization solver is distinct from the queue policy being tuned.

Let the host choose tools, delegation, and iteration schedules. Give any workers
the same family boundary, objective, and requested scope; integrate their feedback
without allowing an unrequested change of problem.

## Deliver the policy and performance evidence

Return the policy or recommendation at the level requested, its applicable
family, parameter meanings and chosen values, and the evidence supporting its
use. For implementation tasks, include runnable policy code or a reusable
implementation reference, concise execution instructions, and any new or revised
simulator. Explain the decision logic and relevant performance comparisons,
including material limitations for the target use.

Finish when the requested recommendation, comparison, tuning, or implementation
is supported by the checks performed. Distinguish simulated performance from
established published guarantees. Deriving new theoretical results and formal
proofs is outside this skill's scope.
