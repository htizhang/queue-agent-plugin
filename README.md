# Queue Agent Plugin

Interactive queueing research through the user's own coding agent, with Claude Code
and Codex as the intended hosts.

**Data → queue model → policy.**

## Confirmed overview

- **Stage 1 — Queue modeling:** build and check an executable queue simulator
  from data and a system description, with replaceable policies.
- **Stage 2 — Policy design:** design, evaluate, and improve queue policies for
  a queue model or model family.

The Plugin first gives the agent this overall task map. The user's current task
determines where to start; not every request needs to run both Stages.

## Development status

This is a private, standalone repository under incremental design. We will discuss
and confirm each workflow step before implementing it. The repository currently
contains the agreed overview, reference material, skill source files, and a
startup-orientation hook source,
not an installable Plugin.

Host packaging and tool integrations are not implemented yet.
No runtime implementation, experiment data, or credentials from the earlier
research repository are included. Selected knowledge is migrated as reviewed,
simulator-neutral reference notes, not as framework code.

## Skills

- [queue-agent](skills/queue-agent/SKILL.md): the overall entry point. Choose
  Stage 1, Stage 2, or shared literature/discussion from the current request and
  available artifacts. An existing model or specified family can go directly to
  Stage 2. See the [routing checks](tests/queue-agent/scenarios.md).

- [queue-modeling](skills/queue-modeling/SKILL.md): Stage 1 simulator construction,
  calibration, and validation. It guides the host agent to use independent
  validation subagents when available and iterate on executable feedback. The
  agent chooses the representation, simulation tools, and task-specific checks.
  See the [behavioral checks](tests/queue-modeling/scenarios.md).

- [queue-literature](skills/queue-literature/SKILL.md): source-grounded literature
  work for Stage 1 modeling and Stage 2 policy design. It adapts selected
  open-source review guidance, adds queue-specific questions, and uses available
  host tools rather than requiring a particular search provider. Its local
  references cover system-to-model abstraction, queue state and event dynamics,
  model validation, arrival and service inference, incomplete logs, and censoring,
  alongside classical scheduling, network control, backfilling, and paired simulation evaluation;
  established questions can be answered without repeating an online search.

These skills are source content in this repository. Nothing is installed or
configured on the user's machine by adding them. For queue-literature, see its
[attribution](skills/queue-literature/NOTICE.md) and
[behavioral checks](tests/queue-literature/scenarios.md).

## Startup orientation

The source in [hooks/hooks.json](hooks/hooks.json) provides a short SessionStart
orientation and points to the queue-agent skill. It does not assign or persist
the current Stage; the agent determines that from the conversation. The helper
uses Python 3's standard library, with no network access or state files.

The hook uses the documented context-output shape shared by Claude Code and
Codex. Host packaging, hook enablement/trust, and installed-host testing remain
separate steps. Adding these files does not enable a hook on this machine.

## Documentation

- [References and confirmed design decisions](docs/references.md)
- [Contributor instructions](AGENTS.md)
- [Knowledge migration and provenance](docs/knowledge-base-migration.md)

## Checks

Run the dependency-free content checks from the repository root:

```sh
python3 -m unittest discover -s tests/queue-literature -p 'test_*.py'
python3 -m unittest discover -s tests/queue-agent -p 'test_*.py'
```

These check the plain-note contract, reference integrity, and source-level hook
execution, not theorem correctness or installed-host compatibility.
