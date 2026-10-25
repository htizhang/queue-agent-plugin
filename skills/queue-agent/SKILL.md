---
name: queue-agent
description: Orient queueing research around data, executable queue models, and policies. Use to start a Queue Agent task, choose between modeling and policy design, or reassess the next step when the user's goal or available model changes.
---

# Queue Agent

Support interactive queueing research: **data → queue model → policy**.

- **Stage 1 — Queue modeling:** deliver a documented queue model and its
  corresponding executable simulator from data and a system description,
  with replaceable policies and checks that the implementation matches the model.
- **Stage 2 — Policy design:** confirm the problem definition, then select,
  evaluate, tune, or design policies according to the user's needs.

These are capabilities, not a mandatory sequence. Use the user's latest request
and the available artifacts to determine the current task.

## Choose the starting point

| Current need | Starting point |
| --- | --- |
| Infer a queue model from observations, or revise its mechanisms or calibration against data | Stage 1: use [queue-modeling](../queue-modeling/SKILL.md). |
| Select, evaluate, tune, or design policies for an existing model, simulator, or specified model family | Stage 2: use [queue-policy](../queue-policy/SKILL.md), beginning with its problem-definition confirmation step. |
| Answer a literature question, explain queueing concepts, or discuss a research direction | Address that question; use [queue-literature](../queue-literature/SKILL.md) when domain evidence is needed. |
| Write or clarify an English model description, policy explanation, or report | Use the shared [asd-ste100](../asd-ste100/SKILL.md) writing skill. Editing a deliverable does not itself start modeling or policy experiments. |
| Contribute knowledge or an agent-discovered method to the Plugin | When the user asks to contribute, use [queue-contribute](../queue-contribute/SKILL.md); this is separate from running either Stage. |

A specified mathematical model may still need an executable evaluator for
Stage 2. Implementing that evaluator does not require inferring a new model from
historical data. Conversely, the mere presence of a simulator does not establish
that it represents the user's system: if the task is to assess or repair that
agreement, use Stage 1.

Inspect the supplied artifacts enough to establish what is usable. Clarify only
missing information that would materially change the next step. For an
end-to-end request, build on what is already available and move between Stages
as needed; do not repeat completed modeling work merely to follow the diagram.

## Keep the task aligned

Briefly state the starting point and immediate goal when beginning or changing
tasks. Reassess from the conversation as the goal or evidence changes, rather
than keeping a fixed Stage label for the whole session. A discussion-only
request stays a discussion; unrelated tasks do not need queueing workflows.

Reuse the shared literature skill for relevant modeling assumptions, baseline
policies, evaluation methods, or applicability of published results. Load the
needed local notes first and seek external sources when they leave a material gap.

Use the host agent's available tools and delegation. This overview does not
prescribe a simulator, model schema, or separate orchestration framework.

## Write for the user

Deliver explanations that a reader can understand without the development
conversation. When writing or revising English explanations and reports for
either Stage, use [asd-ste100](../asd-ste100/SKILL.md). It defaults to
STE-flavored prose and preserves scientific meaning. The Stage skills still
own the required deliverables and evidence checks.
