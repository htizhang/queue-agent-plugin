---
name: queue-agent
description: Orient queueing research around data, executable queue models, and policies. Use to start a Queue Agent task, choose between modeling and policy design, or reassess the next step when the user's goal or available model changes.
---

# Queue Agent

Support interactive queueing research: **data → queue model → policy**.

- **Stage 1 — Queue modeling:** deliver a documented queue model and its
  corresponding executable simulator from data and a system description,
  with replaceable policies and checks that the implementation matches the model.
- **Stage 2 — Policy design:** design, evaluate, and improve policies for a queue
  model or model family.

These are capabilities, not a mandatory sequence. Use the user's latest request
and the available artifacts to determine the current task.

## Choose the starting point

| Current need | Starting point |
| --- | --- |
| Infer a queue model from observations, or revise its mechanisms or calibration against data | Stage 1: use [queue-modeling](../queue-modeling/SKILL.md). |
| Develop or evaluate policies for an existing model, simulator, or specified model family | Stage 2: work directly from that model and the requested objective. |
| Answer a literature question, explain queueing concepts, or discuss a research direction | Address that question; use [queue-literature](../queue-literature/SKILL.md) when domain evidence is needed. |

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
policies, evaluation methods, or theoretical questions. Load the needed local
notes first and seek external sources when they leave a material gap.

Use the host agent's available tools and delegation. This overview does not
prescribe a simulator, model schema, or separate orchestration framework. For
Stage 2, work with those capabilities and the applicable shared knowledge.
