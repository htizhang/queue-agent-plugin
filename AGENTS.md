# Contributor instructions

## Purpose

Queue Agent Plugin supports interactive queueing research in the user's coding
agent: Stage 1 delivers a documented queue model and its corresponding simulator
from data and a system description; Stage 2 confirms the queue family, objective,
and constraints with the user, then selects, evaluates, tunes, or designs
policies. Keep that problem definition fixed unless the user explicitly
authorizes a change.

## Incremental development

- Use English for all repository content, including documentation, comments, and
  user-facing Plugin instructions.
- Develop one user-confirmed workflow step at a time. Respect discussion-only
  requests; do not implement unconfirmed steps.
- Record confirmed design decisions in `docs/references.md`, separately from
  external references, suggestions, and open questions. State each decision as
  the current design and its reason.
- Do not turn the two-Stage overview into a mandatory run-everything pipeline.
- Do not assume a particular model schema, simulator, SDK, or host integration
  before that choice is confirmed.
- Keep changes focused. Add only material that the change needs and that may be
  redistributed here; keep credentials, private data, and bulky experiment
  artifacts out of the repository.
- Keep reusable workflows in skills, established knowledge in `queue-literature`,
  and agent-discovered methods in `discovery-lab/`. Keep research-time Lab access
  conditional on explicit new-algorithm intent, as defined in `queue-policy`.
- Preserve the repository's visibility unless the user explicitly requests a change.
- For manifest, catalog, or release changes, follow
  [Packaging and releases](CONTRIBUTING.md#packaging-and-releases).
- Verify changed behavior with the smallest applicable checks; land changes
  through a pull request to `main`.

This file guides repository work. It is not the installed Plugin's runtime entry
point; runtime packaging is defined by the repository manifests and native
catalogs.
