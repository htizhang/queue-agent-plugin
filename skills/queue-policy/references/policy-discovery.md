# Policy Discovery

Delegate concrete policy development to subagents. Give each a self-contained
research task and room to iterate independently. The main agent coordinates the
work, integrates findings, and verifies the final results.

Use this guidance for the new or improved policy branch of Queue Policy, after
its [problem confirmation](../SKILL.md#confirm-the-problem-definition) and any
needed evaluator preparation. That confirmed definition governs both loops;
the parent skill's change-authorization rule applies throughout.
This workflow does not itself activate Discovery Lab; follow the parent skill's
[Discovery Lab access rule](../SKILL.md#discovery-lab-access).

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
- The parent's [comparison guidance](../SKILL.md#evaluate-and-improve-policies)
  and, for refinement work, the [checks below](#refine-promising-candidates),
  supplied as instructions or accessible references.
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

## Refine promising candidates

Treat simplification as policy development, not just code cleanup. Once a
candidate is promising, let workers test removing components, consolidating
rules, or fixing parameters whose tuning may be unnecessary. Preserve the
original for comparison. Use representative instances within the confirmed
family, including regimes where each mechanism is expected to matter.

Choose checks that answer the unresolved question:

- **Component ablation:** remove or replace a mechanism to assess its contribution.
  State whether the remaining parameters were held fixed or retuned; these test
  different questions. Check combinations when interactions could explain the gain.
- **Parameter sensitivity:** vary values over a relevant range to see where
  performance changes. A flat response near one value in one instance does not
  establish that the parameter can be fixed across the family. Compare fixed and
  tuned values over the intended operating range before making that claim.

Prefer the simpler policy when performance differences are practically negligible
for the task and the evaluation supports that conclusion. Account for noise using
the parent skill's comparison guidance; an inconclusive comparison alone does
not establish equivalence. Retain a component when its supported benefit warrants
the complexity, and explain that tradeoff. Let the evidence determine the useful
parameter count. Keep these checks proportional to the uncertainty and task,
rather than requiring an exhaustive ablation grid or sensitivity sweep.

## Check the final algorithm against literature

For new or improved policies, use [queue-literature](../../queue-literature/SKILL.md)
to compare the final decision rule with the closest applicable methods. Revisit
the comparison after simplification or combination changes the rule; an early
search about a different candidate is not a check of the delivered algorithm.

Compare mechanisms, inputs, parameterizations, and applicability, including
whether different-looking formulas make the same decisions. Cite sources for
borrowed components and describe the specific modification or combination.
Improvements can build on established methods; every component need not be new.
If the final rule matches a known method, report that relation and its measured
performance. Distinguish a supported difference from an unverified novelty claim;
an unsuccessful search alone does not establish novelty.

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
- Assigning a simplification or mechanism-checking task when a promising policy
  has accumulated rules whose contributions are unclear.

These are options, not a mandatory sequence. Share findings that help workers
without turning every inner iteration into a main-agent approval step. Repair
evaluation defects against the agreed model and rerun affected comparisons
before relying on them.

## Verify and conclude

The main agent owns the final comparison: reproduce promising results under a
consistent evaluation setup, check feasibility, and assess performance across
the requested family rather than only the cases selected by a worker. Apply the
parent skill's [comparison guidance](../SKILL.md#evaluate-and-improve-policies)
to the final implementation and chosen values, including any simplifications.
Bring the supported component and parameter findings and the final
literature comparison into the handoff at the depth the user requested.

Continue while there is a concrete, useful next investigation within the user's
scope and available resources. Conclude when the requested outcome has adequate
evidence, the user stops the work, or further progress needs a decision or
resource that is unavailable. If gains remain unconvincing, return the best
supported result, what was tried, and the unresolved obstacle rather than
claiming improvement or repeating the same search indefinitely.

Deliver through the parent skill's policy-and-evidence handoff. The division of
responsibilities matters; a fixed number of workers, rounds, or synchronization
points does not.
