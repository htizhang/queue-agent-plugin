---
name: queue-policy
description: Select, evaluate, tune, or design policies for a queue model or model family. Use for Stage 2 work from a Stage 1 handoff or a user-supplied model, including preparing a missing simulator for policy evaluation.
---

# Queue Policy

Find a policy suited to the user's queue and objective. New algorithm discovery
is one possible task, not the default. Respect discussion-only requests; perform
implementation and experiments when they are part of the requested work.

## Confirm the problem definition

Before Stage 2 execution, establish the user's confirmed problem definition.
A simulator is optional at entry; start from the Stage 1 handoff or user input.

1. **Read and summarize.** Use the supplied artifacts and conversation to identify:
   - **Queue family:** shared structure and mechanisms, permitted model or
     operating-condition variation and ranges, and any target instance.
     Distinguish these from policy parameters; one instance does not define an
     arbitrary range of other systems.
   - **Objective:** the performance measure to optimize and its direction,
     including weights or aggregation when these affect what counts as better.
   - **Constraints:** decision timing, observable information, feasible actions,
     and operational requirements the policy must satisfy.
2. **Clarify the gaps.** Ask short, focused questions about missing or ambiguous
   decisions, building on what the user has already supplied. Offer alternatives
   and a recommendation when helpful, marked as proposals for the user to choose.
   Use the host's interactive question tool when available; otherwise ask in
   ordinary conversation and wait for a reply.
3. **Confirm, then proceed.** Present a concise family/objective/constraints
   summary and ask whether to proceed under it. Completion means the user has
   explicitly confirmed all three, not merely that the agent has filled them in.
   An explicit selection and instruction to proceed already present in the
   conversation counts; reuse it without asking again while the definition is
   unchanged. An unanswered question remains pending, including in unattended
   runs: return the pending question rather than starting implementation or
   experiments. Discussion and input inspection can continue without starting
   execution. Record the confirmed definition in the task's working notes, then
   continue with the requested work.

Keep this confirmed problem definition fixed unless the user explicitly
authorizes a change. Policy redesign and parameter tuning stay within it;
poor results or worker suggestions do not authorize changing the family,
objective, or constraints. Propose a change if warranted and wait for the user's
decision. When the user authorizes a change, update that part of the working
definition and affected evaluator mechanics, metrics, and baselines; clarify any
unresolved consequences without reopening unchanged decisions.

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

## Discovery Lab access

When and only when the user explicitly asks to design a new algorithm, read the
[Discovery Lab index](../../discovery-lab/index.md) and then only relevant
entries. Reuse that intent throughout the continuing new-design task rather than
asking for authorization again.

Until that intent is present, keep the Lab index and entries out of context and
retrieval. Stage 1 work, adopting or comparing policies, fixed-policy tuning,
generic performance improvement, adopting a specified candidate, and suggestions
from the agent or its workers stay on their ordinary workflows. Continue normal
policy improvement without asking the user to approve new-algorithm design. If
the user later limits the task to established methods, stop accessing the Lab.

When active, treat Lab policies as optional exploratory leads. Check their
applicability and evaluate them under the confirmed family, objective, and
constraints. Lab access requires neither using a Lab method nor running Stage 1,
and it does not authorize writing results back; contribution requires a separate
user request.

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

For new or improved policy development, read
[Policy Discovery](references/policy-discovery.md) before delegating research or
implementing candidates. It guides independent subagent development and the main
agent's research iterations, including candidate simplification and a literature
check of the final algorithm. Adoption, comparison, and fixed-policy tuning do
not require this discovery workflow.

Compare policies using the same objective, feasible actions, and information
assumptions:

- State which inputs are available at each decision, distinguishing known
  quantities, estimates, and future realizations. Check the policy code against
  this information boundary, not only its description. Equal access does not
  require every policy to use every observable.
- Check published baseline implementations and parameter definitions against
  their sources; repair defects before using the results. A claim against a
  published rule requires a source-faithful implementation using its required
  available inputs. Label intentional adaptations as separate comparators, not
  replacements for that rule.
- Describe how candidate and baseline parameters were chosen. Give applicable
  baselines a justified tuning setup rather than comparing a tuned candidate
  against arbitrary defaults; disclose differences that affect the comparison.

Account for stochastic noise with repeated runs and shared random inputs where
appropriate; the literature skill's evaluation note explains paired comparisons.
Use fresh evaluation replications after tuning when needed to avoid mistaking
search noise for improvement. Rerun affected comparisons after policy or
evaluator changes, and tie reported results to the final code and parameter
values. Report which instances were tested.

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
the confirmed problem definition and requested scope, and integrate their
feedback within that definition.

## Deliver the policy and performance evidence

For English policy explanations and reports, use the shared
[asd-ste100](../asd-ste100/SKILL.md) writing skill.

Return the policy or recommendation at the level requested, its applicable
family, and the evidence supporting its use. For implementation tasks, include
runnable policy code or a reusable implementation reference, concise execution
instructions, and any new or revised simulator. Explain the decision logic and
relevant performance comparisons, including material limitations for the target use.

Make the explanation self-contained for a reader outside the development process.
For each major component, explain the decision it affects, the problem it
addresses, and why it might help. Define parameter meanings, units where
applicable, chosen values, and how they were selected. Use a checked example or
pseudocode when it clarifies the mechanism. Keep the explanation, examples, and
pseudocode consistent with the evaluated code and parameter values.
Explain important patterns in the results, distinguishing measured effects from
proposed explanations. Use descriptive names and explain the policy without
requiring access to trial history; retain version identifiers where useful for
reproducibility. Match the depth and format to the request.

Finish when the requested recommendation, comparison, tuning, or implementation
is supported by the checks performed. Distinguish simulated performance from
established published guarantees.
