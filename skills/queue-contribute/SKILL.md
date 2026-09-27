---
name: queue-contribute
description: Contribute source-backed queueing literature knowledge, an agent-discovered policy, or both to the Queue Agent Plugin repository through a pull request. Use when the user asks to contribute or to prepare a contribution.
---

# Queue Contribute

Help the user contribute to the Queue Agent Plugin repository. Contribution is
opt-in: this workflow starts from the user's request to contribute. Finished
research, good results, and saved artifacts stay in the user's workspace unless
the user asks to contribute them.

## Establish the contribution

From the request, conversation, and artifacts, determine:

- **Material:** what to contribute, and which path below it takes.
- **Destination:** the repository and base branch that will receive it.
- **Scope:** how far to go, whether a local draft, a local commit, a pushed
  branch, or a pull request.

Ask focused questions only where an ambiguity would change the contribution.
When you select the material from a broad request, have the user confirm that
selection before publication.

### Choose the path by provenance

| Material | Path and home |
| --- | --- |
| Existing literature: published or classical methods, modeling and identification methods, assumptions and applicability conditions, citations, and source-supported practical knowledge | **Literature knowledge:** a note and its source records under `skills/queue-literature/references/` |
| A new policy discovered through LLM agent research | **Agent-discovered policy:** an entry under `discovery-lab/` |

Provenance decides the path, not publication status: an agent-discovered policy
remains a Discovery Lab entry after publication or peer review. If the prior-work
comparison shows that a discovered policy matches a published method, tell the
user; the published method belongs to the literature path, with its original
sources. Ask when provenance is unclear or the material fits neither path.

Literature contributions extend the shared notes rather than adding a topic
skill. For a mixed contribution, prepare each part in its own home with its own
checks.

## Work in the destination checkout

- Identify the destination from the user's instruction and the checkout's
  remotes, such as a fork as `origin` and the maintainers' repository as
  `upstream`. Ask when they conflict or are missing.
- Make changes on a new branch from the base in a Git checkout of the
  destination, using its current guides and templates. An installed Plugin copy
  is versioned content, not a place to write contributions; without a checkout,
  ask which repository or fork to use.
- Leave unrelated modified and untracked files as they are: unstaged,
  unreverted, and unstashed. When they obstruct the work, ask or use a separate
  worktree.
- Bring over only what the contribution needs: its explanation, indispensable
  code, and compact evidence. The request covers the material it names; ask
  before adding other user data, such as raw traces or private notes. When
  evidence relies on data that cannot be published, ask how to proceed, for
  example with a public or synthetic fixture.

## Prepare literature knowledge

For the literature path, use [queue-literature](../queue-literature/SKILL.md): its topic map shows current
coverage, so extend an existing note when it covers the topic. Follow its
[note template](../queue-literature/assets/card-template.md), and give each new
note a topic-map row.

- Check every substantive claim against its cited source at the stated locator,
  and apply queue-literature's citation guidance to each source record.
- Run the knowledge checks in `tests/queue-literature/` and update their note
  inventory when adding a note. They check structure, not science, so report
  the source checks separately.

A literature-only contribution draws only on queue-literature and the literature
itself.

## Prepare an agent-discovered policy

For the discovery path, follow the [contribution guide](../../discovery-lab/CONTRIBUTING.md)
for the entry's contents and checks, and check the
[index](../../discovery-lab/index.md) for an existing entry to update rather than
duplicate. Relate the method to the closest known methods using
queue-literature's prior-art guidance, and report where baselines win as well as
where the method does.

Read only the Lab material this entry needs. That reading serves the
contribution; later research reaches the Lab only through
[queue-policy's access rule](../queue-policy/SKILL.md#discovery-lab-access).

## Review the change set

Stage the contribution's files by path. Before committing or publishing, inspect
the status and the diff against the base for unrelated files, private data,
credentials or access details, absolute local paths, and bulky artifacts. Rerun
the path's checks after the final edits with the tools already available, report
any that cannot run, and fix the contribution when one fails.

## Publish only as authorized

- A request to submit a specified contribution authorizes pushing its branch and
  opening a pull request to the destination.
- Draft-only, no-push, or no-PR requests stop before the excluded step. When the
  request leaves the scope open, prepare the draft and ask before pushing.
- Keep the pull request concise: what it adds and where, the checks and their
  results, evidence limits, and open questions for maintainers.
- Use the Git and GitHub capabilities the host already has. Do not merge or
  enable auto-merge; leave merging to maintainers. Their review is not scientific
  peer review, so describe the
  contribution by the checks actually performed. Keep repository visibility,
  credentials, and local configuration unchanged.
- If access or authentication fails, stop there and leave authentication to the
  user.

## Finish

Report the prepared files, the checks and their results, and the pull request
link or other published state. When stopping before publication, leave the
branch and pull request text ready and name the remaining step. The work is
complete when the checked change set has reached the authorized scope, or is
ready at the step that needs the user.
