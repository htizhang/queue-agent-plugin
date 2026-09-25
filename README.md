# Queue Agent Plugin

Interactive queueing research through the user's own coding agent, with Claude Code
and Codex as the intended hosts.

**Data → queue model → policy.**

## Confirmed overview

- **Stage 1 — Queue modeling:** build and check a queue model from data and a
  system description.
- **Stage 2 — Policy design:** design, evaluate, and improve queue policies for
  a queue model or model family.

The Plugin first gives the agent this overall task map. The user's current task
determines where to start; not every request needs to run both Stages.

## Development status

This is a private, standalone repository under incremental design. We will discuss
and confirm each workflow step before implementing it. The repository currently
contains the agreed overview, reference material, and the first shared skill,
not an installable Plugin.

Host packaging and tool integrations are not implemented yet.
No implementation, experiment data, or credentials from the earlier research
repository are included.

## Shared skills

- [queue-literature](skills/queue-literature/SKILL.md): source-grounded literature
  work for Stage 1 modeling and Stage 2 policy design. It adapts selected
  open-source review guidance, adds queue-specific questions, and uses available
  host tools rather than requiring a particular search provider.

The skill is source content in this repository. Nothing is installed or
configured on the user's machine by adding it. See its
[attribution](skills/queue-literature/NOTICE.md) and
[behavioral checks](tests/queue-literature/scenarios.md).

## Documentation

- [References and confirmed design decisions](docs/references.md)
- [Contributor instructions](AGENTS.md)
