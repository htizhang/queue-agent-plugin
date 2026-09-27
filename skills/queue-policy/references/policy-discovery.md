# Policy Discovery

Delegate concrete policy development to subagents. Give each a self-contained
research task and room to iterate independently. The main agent coordinates the
work, integrates findings, and verifies the final results.

Use this guidance for the new or improved policy branch of Queue Policy, after
its [problem confirmation](../SKILL.md#confirm-the-problem-definition) and any
needed evaluator preparation. That confirmed definition governs both loops;
the parent skill's change-authorization rule applies throughout.

## Organize the research

Seek reusable decision logic that exploits the family's shared structure,
evaluated across representative instances within the agreed variation. Keep
instance-specific parameter tuning distinct from changing that logic.

Choose research tasks that explore meaningfully different hypotheses when
parallel work is useful. A task can be open-ended, or start from an existing
policy, a structural observation, or an earlier candidate. Give enough direction
to make the task productive without prescribing the answer or every experiment.

Supply each development subagent with:

- The confirmed problem definition and requested outcome, including what may
  vary across instances and what the policy can observe and control.
- The model, runnable evaluator and policy interface, applicable baselines, and
  instructions for reproducing comparisons under the common evaluation setup.
- Relevant existing candidates, results, and explanations of unsuccessful
  attempts, with paths to the artifacts needed to continue them.
- Useful knowledge or literature pointers, available tools, and any user-set
  resource or stopping limits.

Let the host choose team size, tools, research directions, and review timing for
the task. Workers need not take the same approach or complete the same number of
iterations. Use separate candidate artifacts so one worker's edits do not
overwrite another's. If delegation is unavailable, explain this and perform the
same development and review responsibilities sequentially within the host's
capabilities.

## Inner iterations: subagents develop policies

Each development subagent owns an iterative research task, not just a one-shot
code change. Let it form hypotheses, implement candidates, evaluate them, inspect
where they succeed or fail, and revise its approach without waiting for the main
agent to supply feedback after every trial. Follow the parent skill's
[comparison guidance](../SKILL.md#evaluate-and-improve-policies).

Build on previous trials when useful: refine a candidate, reuse a mechanism, or
combine complementary ideas. Keep enough history to recover useful candidates
and understand why the next attempt differs. Record candidate code or parameters,
evaluation conditions and results, and the key lesson; a fixed archive format or
an exhaustive transcript is unnecessary.

At useful checkpoints, return the strongest candidates with reproducible
evidence, relevant failures, remaining questions, and a proposed next direction.
Raise blockers or discoveries that affect other workers when they arise.

## Outer iterations: the main agent steers the research

Review findings across workers and instances. Ask what is limiting progress:
the candidate mechanism, missing context or knowledge, a defect in the evaluator
or baseline implementation, noisy comparisons, or an exhausted search direction.
Check evidence before deciding which explanation fits. Disappointing results
alone establish neither that the problem is impossible nor that it needs to be
redefined.

Adapt the next research step to that diagnosis. Useful options include:

- Letting a productive worker continue from its existing candidates and history.
- Giving a worker missing model details, a relevant paper, or access to an
  available skill or tool that addresses a specific obstacle.
- Redirecting effort toward a neglected mechanism or difficult permitted
  operating regime while retaining evaluation across the agreed scope.
- Asking workers to test whether complementary ideas combine well, or obtaining
  an independent check of a promising result.

These are options, not a mandatory sequence. Share findings that help workers
without turning every inner iteration into a main-agent approval step. Repair
evaluation defects against the agreed model and rerun affected comparisons
before relying on them.

## Verify and conclude

The main agent owns the final comparison: reproduce promising results under a
consistent evaluation setup, check feasibility, and assess performance across
the requested family rather than only the cases selected by a worker. Apply the
parent skill's treatment of stochastic noise and post-tuning evaluation.

Continue while there is a concrete, useful next investigation within the user's
scope and available resources. Conclude when the requested outcome has adequate
evidence, the user stops the work, or further progress needs a decision or
resource that is unavailable. If gains remain unconvincing, return the best
supported result, what was tried, and the unresolved obstacle rather than
claiming improvement or repeating the same search indefinitely.

Deliver through the parent skill's policy-and-evidence handoff. The division of
responsibilities matters; a fixed number of workers, rounds, or synchronization
points does not.
