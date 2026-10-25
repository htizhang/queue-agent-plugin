# Getting started

This guide explains how to use Queue Agent from a local copy of this
repository. You ask your coding agent to read the skill files directly. This is
a source preview, not an installation. The repository has no Plugin manifest or
installation command yet, and these steps change no settings on your machine.

## What you need

- A coding agent that can read local files, such as Claude Code or Codex. For
  implementation tasks, the agent must also edit files and run code in your
  workspace.
- A local copy of this repository.
- Your research material: for example, event logs, a system description, a
  model specification, an existing simulator, or papers.

The skills require no particular simulator, programming language, search
provider, or number of subagents. The agent uses the tools that your host makes
available. Your host's file access, permission prompts, and tool settings stay
under your control.

## 1. Get a local copy

```sh
git clone https://github.com/htizhang/queue-agent-plugin.git
cd queue-agent-plugin
pwd
```

Note the absolute path that `pwd` prints. Without Git, use **Code → Download
ZIP** on the GitHub repository page and extract the archive. The extracted
folder has the name `queue-agent-plugin-main`.

The skills change as development continues. To get updates, run `git pull` in
the clone. To record which instructions you used, keep the commit identifier
with your results:

```sh
git rev-parse --short HEAD
```

## 2. Optional: view the diagrams and the guide

The SVG diagrams render directly on GitHub:
[overview](assets/overview.svg), [Stage 1](assets/stage-1.svg), and
[Stage 2](assets/stage-2.svg).

The [visual guide](guide.html) is a static HTML page. GitHub shows its source
code, not the page, and there is no hosted version. Open the file from your
local copy. It needs no server, build step, or network connection.

| System | Command from the clone |
| --- | --- |
| macOS | `open docs/guide.html` |
| Linux | `xdg-open docs/guide.html` |
| Windows | `start docs\guide.html` |

You can also drag the file into a browser window.

## 3. Start the agent in your research workspace

Start your coding agent in the directory that holds your research material, not
in the clone. The skills tell the agent to keep generated files in your task
workspace. The clone supplies the instructions.

The `AGENTS.md` file in the clone has rules for developing this repository, not
for research use. Some hosts load that file automatically when they start in
the clone.

## 4. Name the entry skill in your first request

Start the session with a request in this form. Replace the path with the
absolute path of your clone.

```text
Read /absolute/path/to/queue-agent-plugin/skills/queue-agent/SKILL.md and
follow it for this task. Resolve its relative links inside that clone, and read
the linked files when you need them. Keep all outputs in this workspace.

Task: <the result you want, the files to use, and any limits>
```

The entry skill selects a starting point from your task and the available
files. Then the agent follows the linked skill for Stage 1, Stage 2, literature,
writing, or contribution. Some hosts ask for permission before they read files
outside the workspace. Answer that request in your host as usual.

## 5. Describe the task

State the result you want, the files to use, and any limits, such as
"discussion only" or "do not install anything". The agent asks focused
questions only about gaps that would change the next step. These examples show
typical starting points.

### Build a model from data (Stage 1)

```text
Task: Build a queue model and a simulator from data/events.csv and
notes/system.md, so that we can compare dispatch rules later.
```

The agent first checks event meanings, units, missing events, and censoring. You
receive a documented queue model and a simulator that implements it. The
simulator has a replaceable policy interface, a fitted configuration, and run
instructions. The delivery also includes validation results and open issues.
When your host supports subagents, the skill prefers a separate validator that
runs the simulator against the original evidence. Use the same Stage when an
existing simulator does not match your data.

### Compare policies for a specified model (Stage 2)

```text
Task: Compare FCFS and shortest-job-first for the model in model.md.
We have no simulator and no operational logs.
```

The agent summarizes the queue family, objective, and constraints, and asks you
to confirm them. Then, if the task needs simulation, it builds an evaluator for
the specified model and checks it on small cases. You receive the comparison on
the stated instances, the code that produced it, and its limits. A Stage 2 task
does not require Stage 1 or new data.

### Tune a fixed policy (Stage 2)

```text
Task: Keep this policy's decision logic. Tune its two weights for the
32-processor, load-0.8 instance.
```

After the confirmation step, you receive the tuned values, the selection
method, and an evaluation on fresh replications where needed. The decision
logic and the problem definition stay unchanged.

### Design a new algorithm (Stage 2)

```text
Task: Design a new scheduling algorithm for this family, and evaluate it
against the published baselines.
```

After confirmation, the agent organizes development work. If the host supports
subagents, they receive independent research tasks, and the main agent steers
and verifies the results. Workers can run several trials without asking after
each one, and the main agent can start further rounds. State any resource or
stopping limits in your request. Because you asked for a new algorithm, the agent can
also read relevant Discovery Lab entries as optional leads. You receive policy
code, a standalone explanation, and comparisons on representative instances of
the family. Ablation checks what changes when a component is removed; sensitivity
analysis checks what changes when a parameter varies. The agent also compares the
final rule with the closest published methods. If gains are not convincing, it
reports the best supported result and what it tried.

### Ask a literature question

```text
Task: Explain the difference between sojourn times and service requirements,
with sources. Do not write code.
```

The agent reads the relevant local note first and searches further only for a
material gap. You receive a source-grounded answer that states which sources
the agent read. A discussion request does not start experiments.

### Improve a written explanation

```text
Task: Rewrite model.md for a new collaborator. Keep the equations unchanged.
```

The shared writing skill keeps assumptions, equations, results, and the strength
of each claim. It changes the language, not the model.

## What to expect

**Stage 2 starts with a confirmation.** Before experiments, the agent states
the queue family, the objective, and the constraints, and asks you to confirm
them. It reuses a confirmation that you already gave in the conversation. Then
the definition stays fixed until you change it. Poor results or a worker
suggestion do not change it. In an unattended run, the agent returns its
question and does not start experiments. To continue without a pause, state all
three parts in your request, confirm them explicitly, and ask the agent to
proceed.

**The Discovery Lab is opt-in.** During research, the agent reads the
[Discovery Lab](../discovery-lab/index.md) only when you explicitly ask for a
new algorithm. Requests to adopt, compare, or tune policies, or to improve
performance in general, do not open it. Lab entries are exploratory leads with
bounded evidence, not established results.

**Results stay in your workspace.** Contribution to this repository is a
separate task that starts only when you ask. A requested Lab contribution can
read the relevant entries to prepare a change. See
[CONTRIBUTING.md](../CONTRIBUTING.md).

**The skills are instructions, not permissions.** They tell the agent to stay
within your requested scope and to use tools that your host already provides.
The literature and contribution workflows include explicit checks on sharing
private material. Review the data sent to external tools; your host's permission
settings are the actual controls.

## Limits of this mode

- Reading skill files by path is a manual preview. It is not automatic skill
  discovery or an installed Plugin.
- The startup hook in `hooks/` does not run. Your first request names the entry
  skill instead.
- Results depend on your host, model, and tool access. The review cases in
  `tests/` check how an agent interprets the instructions. They do not show host
  compatibility or the quality of research results.
- Host packaging and installation are separate future steps.

## Next steps

- Read the [entry skill](../skills/queue-agent/SKILL.md), then the skill for
  your task.
- See the [README](../README.md) for the skill map and project status.
- See the [design decisions](references.md) for the reasons behind the workflow.
- To share a literature note or a discovered policy, read
  [CONTRIBUTING.md](../CONTRIBUTING.md).
