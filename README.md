# Queue Agent Plugin

Interactive queueing research with your own coding agent:
**data → queue model → policy**. Claude Code and Codex are the intended
hosts.

- **Stage 1, queue modeling:** build a documented queue model and a
  corresponding executable simulator from data and a system description.
- **Stage 2, policy design:** confirm the queue family, objective, and
  constraints with you, then select, evaluate, tune, or design policies.

You choose the task, and not every task needs both Stages. The agent works with
the tools that your host provides.

> **Status: source preview.** You can use the skills now by asking your agent
> to read them from a local clone. There is no Plugin manifest, marketplace
> entry, or installation command yet. See
> [Getting started](docs/getting-started.md) and
> [Project status](#project-status).

![Entry routes diagram. Your request goes to the queue-agent entry skill, which chooses a starting point. Data and a system description lead to Stage 1, queue modeling, which returns a documented model and its simulator. A model, simulator, or family can go directly to Stage 2, policy design, which returns a policy or recommendation with evidence. The Discovery Lab opens only for explicit new-algorithm requests. Literature questions and writing go to shared skills, and contribution is opt-in.](docs/assets/overview.svg)

The diagrams for [Stage 1](docs/assets/stage-1.svg) and
[Stage 2](docs/assets/stage-2.svg) also render on GitHub. The
[visual guide](docs/guide.html) is a static HTML page, which GitHub shows as
source code. To read it, clone or download this repository and open
`docs/guide.html` in a web browser. It needs no server, build step, or network
connection.

## What you supply and what you get

| You supply | You get back | Skill |
| --- | --- | --- |
| Event logs or other observations, and a description of the system | A documented queue model and a simulator that implements it, with a fitted configuration, run instructions, a replaceable policy interface, validation results, and open issues | [queue-modeling](skills/queue-modeling/SKILL.md) |
| A simulator that does not match your data | Reproducible discrepancies, then a revised model and simulator | [queue-modeling](skills/queue-modeling/SKILL.md) |
| A model, a simulator, or a specified model family, and a goal for its policies | First, a summary of the queue family, objective, and constraints for you to confirm. Then a recommendation, comparison, tuned parameters, or new policy, with code and performance evidence at the depth you request | [queue-policy](skills/queue-policy/SKILL.md) |
| A literature question | A source-grounded answer that separates what each source establishes from inference | [queue-literature](skills/queue-literature/SKILL.md) |
| A draft model description, policy explanation, or report | Clearer English with the same equations, results, and claim strength | [asd-ste100](skills/asd-ste100/SKILL.md) |
| Research that you choose to share | A checked contribution, submitted as a pull request only when you authorize it | [queue-contribute](skills/queue-contribute/SKILL.md) |

## Try it from source

1. Clone this repository
   (`git clone https://github.com/htizhang/queue-agent-plugin.git`), or
   download it as a ZIP file from GitHub.
2. Start your coding agent in your research workspace, not in the clone.
3. Start the session with a request that names the entry skill by its absolute
   path:

```text
Read /absolute/path/to/queue-agent-plugin/skills/queue-agent/SKILL.md and
follow it for this task. Resolve its relative links inside that clone, and read
the linked files when you need them. Keep all outputs in this workspace.

Task: Build a queue model and a simulator from data/events.csv and
notes/system.md, so that we can compare dispatch rules later.
```

This is manual source use, not an installation. It changes no settings on your
machine, and your host's file access and permissions stay under your control.
Behavior can differ between hosts and models. The
[getting-started guide](docs/getting-started.md) gives more examples and the
limits of this mode.

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
| [asd-ste100](skills/asd-ste100/SKILL.md) | **Shared.** English writing guidance for model descriptions, policy explanations, and reports. It uses STE-flavored prose and keeps scientific meaning and necessary terms. Its optional, dependency-free linter checks language patterns, not scientific correctness. No hook applies it automatically. | [Writing](tests/asd-ste100/scenarios.md) |
| [queue-contribute](skills/queue-contribute/SKILL.md) | **Optional.** When you ask to contribute, prepares a literature note, a Discovery Lab entry, or both. It publishes only within the scope that you authorize. | [Contribution](tests/queue-contribute/scenarios.md) |

A review case is a request with expected behaviors. An agent reads the skill
and proposes its actions, and a reviewer compares them with the checks. Review
cases test the interpretation of instructions, not an installed host.

## Discovery Lab

The [Discovery Lab](discovery-lab/index.md) holds policies discovered through
LLM-agent research, separate from established literature. Its entries are
[queue-aware optimistic backfilling](discovery-lab/queue-aware-backfilling/policy.md)
for multiserver jobs with simultaneous resource requirements, and
[congestion-priced lookahead](discovery-lab/congestion-priced-lookahead/policy.md)
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

- **Available:** six skills, a startup-hook source, local literature notes, two
  Discovery Lab entries, review cases, and dependency-free checks.
- **Not available yet:** a Plugin manifest, a marketplace entry, or an
  installation command for any host. Host packaging will be designed
  separately. Cloning this repository installs or enables nothing.
- **Startup hook:** [hooks/hooks.json](hooks/hooks.json) defines a short
  SessionStart orientation that points to the entry skill. It does not choose
  or store a Stage. When enabled, it includes the local entry-skill path in the
  agent's context. It needs only Python 3, uses no network, and writes no
  state files. It follows the hook output format that Claude Code and Codex
  document. Packaging, hook approval, and installed-host tests are separate
  steps.
- **Tested so far:** automated source checks, and source-loaded reviews in
  which an agent reads a skill and proposes its next actions. These do not
  establish automatic skill discovery, hook loading, installed-host
  compatibility, or the quality of research results.
- **Development:** one confirmed workflow step at a time. The
  [design decisions](docs/references.md) record each agreed step.

## Checks

The repository checks need only Python 3.10 or later and its standard library.
They cover the literature-note contract and reference integrity, the hook from
source, and the writing skill and its linter. Other checks cover documentation
links, the Discovery Lab fixtures, and the archived comparisons. They do not
establish theorem correctness, reader comprehension, or installed-host
compatibility. The Lab checks do not rerun the original simulation campaigns.
See [the commands](CONTRIBUTING.md#run-the-checks).

## Contributing

Contributions are opt-in pull requests. Established literature goes into the
queue-literature notes, and agent-discovered policies go into the Discovery
Lab. Workflow, documentation, and visual changes have their own paths. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Documentation

- [Getting started](docs/getting-started.md): source use, example requests, and
  limits.
- [Visual guide](docs/guide.html), opened locally, and the
  [overview](docs/assets/overview.svg), [Stage 1](docs/assets/stage-1.svg), and
  [Stage 2](docs/assets/stage-2.svg) diagrams.
- [References and design decisions](docs/references.md).
- [Local knowledge collection](docs/knowledge-base-expansion.md) and
  [knowledge migration and provenance](docs/knowledge-base-migration.md).
- [Contributing](CONTRIBUTING.md), and the
  [instructions for coding agents](AGENTS.md) that develop this repository.

## License

Original repository content is released under the [MIT License](LICENSE).
Adapted third-party material keeps its own notices: see
[queue-literature](skills/queue-literature/NOTICE.md) and
[asd-ste100](skills/asd-ste100/NOTICE.md). The literature notes cite papers but
do not reproduce them.
