# Queue Agent Plugin

Interactive queueing research with your own coding agent:
**data → queue model → policy**. Queue Agent is a plugin for Claude Code and
Codex.

- **Stage 1, queue modeling:** build a documented queue model and a
  corresponding executable simulator from data and a system description.
- **Stage 2, policy design:** confirm the queue family, objective, and
  constraints with you, then select, evaluate, tune, or design policies.

You choose the task, and not every task needs both Stages. The agent works with
the tools that your host provides. To install the plugin with a one-line
command, see the [Quick start](#quick-start).

![Queue Agent research workflow. Stage 1 turns data and a system description into a documented queue model and its matching simulator. Stage 2 starts from these outputs or an existing model, confirms the problem, and adopts, compares, tunes, or designs a policy. New designs undergo mechanism analysis, simplification, and reevaluation. Both Stages use queueing literature and reader checks.](docs/assets/overview.svg)

The diagrams for [Stage 1](docs/assets/stage-1.svg) and
[Stage 2](docs/assets/stage-2.svg) also render on GitHub. The
[visual guide](docs/guide.html) is a static HTML page, which GitHub shows as
source code. To read it, open `docs/guide.html` from a local copy of this
repository in a web browser.

## What you supply and what you get

| You supply | You get back | Skill |
| --- | --- | --- |
| Event logs or other observations, and a description of the system | A documented queue model and a simulator that implements it, with a fitted configuration, run instructions, a replaceable policy interface, validation results, and open issues | [queue-modeling](skills/queue-modeling/SKILL.md) |
| A simulator that does not match your data | Reproducible discrepancies, then a revised model and simulator | [queue-modeling](skills/queue-modeling/SKILL.md) |
| A model, a simulator, or a specified model family, and a goal for its policies | First, a summary of the queue family, objective, and constraints for you to confirm. Then a recommendation, comparison, tuned parameters, or new policy, with code and performance evidence at the depth you request | [queue-policy](skills/queue-policy/SKILL.md) |
| A literature question | A source-grounded answer that separates what each source establishes from inference | [queue-literature](skills/queue-literature/SKILL.md) |
| A draft model description, policy explanation, or report | Clearer English with the same equations, results, and claim strength | [asd-ste100](skills/asd-ste100/SKILL.md) |
| Research that you choose to share | A checked contribution, submitted as a pull request only when you authorize it | [queue-contribute](skills/queue-contribute/SKILL.md) |

## Quick start

You need Git and an installed Claude Code or Codex CLI, with your usual login
and model already set up. These one-line examples are for macOS and Linux;
PowerShell 7 also supports `&&`, and older shells can run the two commands
separately.

For Claude Code:

```sh
claude plugin marketplace add htizhang/queue-agent-plugin && claude plugin install queue-agent@queue-agent
```

Start a new session in your research workspace, or run `/reload-plugins` in the
current session. Invoke the entry skill with `/queue-agent:queue-agent`.

For Codex:

```sh
codex plugin marketplace add htizhang/queue-agent-plugin && codex plugin add queue-agent@queue-agent
```

Start a new session in your research workspace. Choose `queue-agent` in the
skills menu, or ask: `Use the queue-agent skill to <describe the task>.`

In either host, state the result you want and the files to use, for example:

```text
Build a queue model and a simulator from data/events.csv and notes/system.md,
so that we can compare dispatch rules later.
```

[Getting started](docs/getting-started.md#3-describe-the-task) has more example
requests and the commands to update or remove the plugin.

Both hosts install to user scope by default. Keep task inputs and generated
results in your research workspace, not in the plugin installation cache.

The package contains the six skills and a startup hook,
[hooks/hooks.json](hooks/hooks.json). At session start, the hook adds a short
orientation and the local path of the entry skill to the agent's context. It
needs `python3`, uses no network, writes no state, and does not choose a Stage.
In Codex, trusting the hook is a separate decision from installing the plugin;
review the hook before you trust it. Without the hook, select the `queue-agent`
entry skill explicitly; all skills still work.

### Source-use fallback

If your host cannot install plugins, clone this repository or download its ZIP
file. Start your agent in your research workspace and ask it to read
`skills/queue-agent/SKILL.md` from the clone by its absolute path.
[Getting started](docs/getting-started.md#source-use-fallback) gives the
exact request. This reads the skills from source; it installs nothing and does
not run the startup hook.

## How the work proceeds

- **Start from your task.** The Stages are capabilities, not a required
  sequence. An existing model or a specified family can go directly to Stage 2,
  with or without a simulator. The agent builds an evaluator only when the task
  needs simulation.
- **Stage 1 delivers two corresponding artifacts.** The model description and
  the simulator stay consistent. Independent validation runs the simulator
  against the evidence, preferably in a separate subagent when the host
  supports one. Its feedback can revise the model or the implementation.
- **Stage 2 confirms the problem first.** The agent confirms the queue family,
  objective, and constraints with you, or reuses your explicit confirmation.
  The definition then stays fixed until you change it.
- **The work matches the need.** Adoption, comparison, tuning, and new design
  are separate options that can be combined. A request to adopt or tune a
  policy does not become a discovery campaign. New policy design targets the
  shared structure of the confirmed family, and parameter values can still be
  tuned for one instance.
- **Comparisons use common rules.** The agent compares policies on the same
  objective, feasible actions, and information assumptions. Baselines follow
  their sources and receive a justified tuning setup. The agent prefers a
  simpler policy when the evidence shows a negligible difference. A flat
  parameter response in one instance does not establish one setting for the
  whole family. Before delivery, the agent compares a new rule with the closest
  published methods.
- **Both Stages share literature and writing support.** They use the literature
  skill for modeling assumptions, baselines, and theoretical results, and the
  writing skill for explanations and reports.
- **Some resources are opt-in.** During research, the Discovery Lab opens only
  when you explicitly ask for a new algorithm. Contribution starts only when you ask.
- **The host decides how.** The skills prescribe no simulator, model schema,
  search provider, or number of subagents.

## Skills

| Skill | Role | Review cases |
| --- | --- | --- |
| [queue-agent](skills/queue-agent/SKILL.md) | **Entry point.** Chooses Stage 1, Stage 2, literature, writing, or contribution from your request and the available artifacts. | [Routing](tests/queue-agent/scenarios.md) |
| [queue-modeling](skills/queue-modeling/SKILL.md) | **Stage 1.** Builds, calibrates, and validates a queue model and its simulator, with independent, executable feedback. The agent chooses the representation and tools. | [Modeling](tests/queue-modeling/scenarios.md) |
| [queue-policy](skills/queue-policy/SKILL.md) | **Stage 2.** Confirms the problem definition, prepares an evaluator when needed, then adopts, compares, tunes, or designs policies. New policy work follows its [Policy Discovery](skills/queue-policy/references/policy-discovery.md) reference. [SimOpt](https://github.com/simopt-admin/simopt) is an optional external resource, not a bundled backend. | [Policy](tests/queue-policy/scenarios.md), [discovery](tests/queue-policy/discovery-scenarios.md), [refinement](tests/queue-policy/refinement-scenarios.md) |
| [queue-literature](skills/queue-literature/SKILL.md) | **Shared.** Source-grounded literature work for both Stages, with the search tools of your host. Local notes cover model abstraction, state and dynamics, validation, arrival and service inference, incomplete logs, and censoring. They also cover classical scheduling, network control, backfilling, and paired evaluation. | [Literature](tests/queue-literature/scenarios.md) |
| [asd-ste100](skills/asd-ste100/SKILL.md) | **Shared.** English writing guidance for model descriptions, policy explanations, and reports. It preserves scientific meaning and uses a document-only reader check for substantial deliverables. Its optional linter checks language patterns, not comprehension. | [Writing](tests/asd-ste100/scenarios.md) |
| [queue-contribute](skills/queue-contribute/SKILL.md) | **Optional.** When you ask to contribute, prepares a literature note, a Discovery Lab entry, or both. It publishes only within the scope that you authorize. | [Contribution](tests/queue-contribute/scenarios.md) |

A review case is a request with expected behaviors. An agent reads the skill
and proposes its actions, and a reviewer compares them with the checks. Review
cases test the interpretation of instructions, not an installed host.

## Discovery Lab

The [Discovery Lab](discovery-lab/index.md) holds policies discovered through
LLM-agent research, separate from established literature. Its entries are
[queue-aware optimistic backfilling](discovery-lab/queue-aware-backfilling/policy.md)
for multiserver jobs with simultaneous resource requirements, and
[bottleneck-work block planning](discovery-lab/bottleneck-work-block-planning/policy.md)
for reentrant networks with sequence-dependent setups. Each entry has a method
description, portable code, and compact evaluation evidence with runnable
checks.

The Lab is not part of the agent's default knowledge. During research, it is read only
when you explicitly ask for a new algorithm. Modeling, adoption, comparison,
tuning, and general performance improvement do not open it
([access checks](tests/queue-policy/lab-access-scenarios.md)). Entries are
research leads to evaluate in your setting. Their evidence covers the stated
configurations and comparators. It does not show that a policy wins on other
workloads, and repository review is not peer review.

A separate, requested contribution can also read the relevant Lab material to
prepare an entry or update; see [Contributing](CONTRIBUTING.md).

## Project status

Version `0.1.0`, released under the MIT License. The plugin has a portable
Agent Plugins 1.0 manifest and native manifests for Claude Code and Codex; the
plugin and both native catalogs are named `queue-agent`. The repository holds
six skills, the startup hook, local literature notes, two Discovery Lab entries,
review cases, and dependency-free checks. Manifest validation and installation
tests for both hosts in isolated profiles are release checks; see
[Packaging and releases](CONTRIBUTING.md#packaging-and-releases).

## Checks

The repository checks need only Python 3.10 or later and its standard library.
They cover package identity and contents, the literature-note contract and
reference integrity, the hook from source, and the writing skill and its
linter. Other checks cover documentation links, the Discovery Lab fixtures,
and the archived comparisons. They do not establish theorem correctness,
reader comprehension, installed-host compatibility, or research quality. The
Lab checks do not rerun the original simulation campaigns. See
[the commands](CONTRIBUTING.md#run-the-checks).

## Contributing

Contributions are opt-in pull requests. Established literature goes into the
queue-literature notes, and agent-discovered policies go into the Discovery
Lab. Workflow, documentation, and visual changes have their own paths. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Documentation

- [Getting started](docs/getting-started.md): installation, updates and
  removal, the source-use fallback, and example requests.
- [Visual guide](docs/guide.html), opened locally, and the
  [overview](docs/assets/overview.svg), [Stage 1](docs/assets/stage-1.svg), and
  [Stage 2](docs/assets/stage-2.svg) diagrams.
- [References and design decisions](docs/references.md).
- [Local knowledge collection](docs/knowledge-base-expansion.md) and its
  [provenance](docs/knowledge-base-migration.md).
- [Contributing](CONTRIBUTING.md), and the
  [instructions for coding agents](AGENTS.md) that develop this repository.

## License

Original repository content is released under the [MIT License](LICENSE).
Adapted third-party material keeps its own notices: see
[queue-literature](skills/queue-literature/NOTICE.md) and
[asd-ste100](skills/asd-ste100/NOTICE.md). The literature notes cite papers but
do not reproduce them.
