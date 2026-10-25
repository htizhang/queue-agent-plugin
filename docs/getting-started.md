# Getting started

Queue Agent is an installable plugin for Claude Code and Codex. Version `0.1.0`
packages six skills and a startup hook. It adds no MCP server, app, or separate
service.

## What you need

- Git for native installation or cloning. The [source-use fallback](#source-use-fallback)
  also works from a downloaded ZIP without Git.
- An installed Claude Code or Codex CLI. Configure its normal account login,
  model, and tool permissions separately from plugin installation.
- Your research material: for example, event logs, a system description, a
  model specification, an existing simulator, or papers.

The startup hook needs `python3`; the skills remain usable without it. The
skills require no particular simulator, programming language, search provider,
or number of subagents. The agent uses the tools that your host makes
available.

## 1. Install the plugin

These one-line examples are for macOS and Linux. PowerShell 7 also supports
`&&`; in older shells, run the two commands separately.

For Claude Code:

```sh
claude plugin marketplace add htizhang/queue-agent-plugin && claude plugin install queue-agent@queue-agent
```

For Codex:

```sh
codex plugin marketplace add htizhang/queue-agent-plugin && codex plugin add queue-agent@queue-agent
```

Each command adds the repository's `queue-agent` catalog and installs
`queue-agent@queue-agent`. Both hosts use user scope by default.

## 2. Load the plugin and start a task

Start your coding agent in the directory that holds your research material.
Keep task inputs and generated results in that workspace, not in the plugin
installation cache, so that updates and removal do not affect your work.

For Claude Code, start a new session or run `/reload-plugins` in the current
session. Invoke the entry skill:

```text
/queue-agent:queue-agent
```

For Codex, start a new session. Choose `queue-agent` in the skills menu, or ask:

```text
Use the queue-agent skill to <describe the task>.
```

The entry skill selects a starting point from your request and the available
files. Then the agent follows the linked skill for Stage 1, Stage 2, literature,
writing, or contribution.

The package also includes a SessionStart hook, `hooks/hooks.json`. At session
start, it adds a short orientation and the local path of the entry skill to the
agent's context. It does not choose or store a Stage. The hook needs `python3`,
uses no network, and writes no state. In Codex, trusting the hook is a separate
decision from installing the plugin; review the hook before you trust it. If
the hook is not trusted or does not load, select the entry skill explicitly as
shown above; the full workflow stays available.

## 3. Describe the task

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

**Results depend on your host and model.** The same request can play out
differently with another host, model, or set of tools.

## Update or remove the plugin

For Claude Code, update the catalog and installed plugin:

```sh
claude plugin marketplace update queue-agent
claude plugin update queue-agent@queue-agent
```

Uninstall the plugin, and optionally remove its catalog:

```sh
claude plugin uninstall queue-agent@queue-agent
claude plugin marketplace remove queue-agent --scope user
```

For Codex, upgrade the catalog, then add the plugin again to refresh the
installed version:

```sh
codex plugin marketplace upgrade queue-agent
codex plugin add queue-agent@queue-agent
```

Remove the plugin, and optionally remove its catalog:

```sh
codex plugin remove queue-agent@queue-agent
codex plugin marketplace remove queue-agent
```

After an update, start a new session. In Claude Code you can also use
`/reload-plugins`.

## Source-use fallback

If native plugin installation is unavailable, clone the repository:

```sh
git clone https://github.com/htizhang/queue-agent-plugin.git
cd queue-agent-plugin
pwd
```

Note the absolute path that `pwd` prints. Without Git, use **Code → Download
ZIP** on the GitHub repository page and extract the archive. To update a clone,
run `git pull`. To record which instructions you used, save the output of
`git rev-parse --short HEAD` with your results.

Start the agent in your research workspace, not in the clone. Name the entry
skill by its absolute path:

```text
Read /absolute/path/to/queue-agent-plugin/skills/queue-agent/SKILL.md and
follow it for this task. Resolve its relative links inside that clone, and read
the linked files when you need them. Keep all outputs in this workspace.

Task: <the result you want, the files to use, and any limits>
```

This fallback reads the skills from source. It does not install the plugin or
run the startup hook, and the agent reaches the other skills only through the
entry skill's links. Some hosts ask for permission before they read files
outside the workspace. Answer that request in your host as usual.

## View the diagrams and the guide

The SVG diagrams render directly on GitHub:
[overview](assets/overview.svg), [Stage 1](assets/stage-1.svg), and
[Stage 2](assets/stage-2.svg).

The [visual guide](guide.html) is a static HTML page. GitHub shows its source
code, not the page, and there is no hosted version. Open the file from a clone
or ZIP download of this repository. It needs no server, build step, or network
connection.

| System | Command from the repository root |
| --- | --- |
| macOS | `open docs/guide.html` |
| Linux | `xdg-open docs/guide.html` |
| Windows | `start docs\guide.html` |

You can also drag the file into a browser window.

## Next steps

- Read the [entry skill](../skills/queue-agent/SKILL.md), then the skill for
  your task.
- See the [README](../README.md) for the skill map and project status.
- See the [design decisions](references.md) for the reasons behind the workflow.
- To share a literature note or a discovered policy, read
  [CONTRIBUTING.md](../CONTRIBUTING.md).
