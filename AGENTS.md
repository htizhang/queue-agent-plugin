# Contributor instructions

## Purpose

Queue Agent Plugin supports interactive queueing research in the user's coding
agent: Stage 1 builds a queue model from data and a system description; Stage 2
designs, evaluates, and improves policies for a model or model family.

## Incremental development

- Use English for all repository content, including documentation, comments, and
  user-facing Plugin instructions.
- Develop one user-confirmed workflow step at a time. Respect discussion-only
  requests; do not implement unconfirmed steps.
- Record confirmed decisions in `docs/references.md`, separately from external
  references, suggestions, and open questions.
- Do not turn the two-Stage overview into a mandatory run-everything pipeline.
- Do not assume a particular model schema, simulator, SDK, or host integration
  before that choice is confirmed.
- Keep changes focused. Do not import unrelated implementation, datasets,
  experiment artifacts, or credentials from other repositories.
- Preserve private visibility unless the user explicitly requests a change.
- Verify changed behavior with the smallest applicable checks; land changes
  through a pull request to `main`.

This file guides repository work. It is not the installed Plugin's runtime entry
point; runtime packaging will be designed separately.
