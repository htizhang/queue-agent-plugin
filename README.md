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
and confirm each workflow step before implementing it. The initial repository
contains the agreed overview and reference material, not an installable Plugin.

Detailed workflows, host packaging, and tool integrations are not implemented yet.
No implementation, experiment data, or credentials from the earlier research
repository are included.

## Documentation

- [References and confirmed design decisions](docs/references.md)
- [Contributor instructions](AGENTS.md)
