# Contributing

Queue Agent accepts contributions as pull requests to `main`. Maintainers decide
what to merge. Repository review is not scientific peer review.

Contribution is opt-in. Research that you run with these skills stays in your
workspace until you decide to share part of it. To use the skills, start with
the [README](README.md).

## Choose the path

| What you add or change | Where it goes | Follow |
| --- | --- | --- |
| Knowledge from existing literature: published or classical methods, modeling and identification methods, assumptions, applicability conditions, and citations | A note and its source records in `skills/queue-literature/references/` | [Literature knowledge](#literature-knowledge) |
| A policy discovered through LLM-agent research | An entry in `discovery-lab/` | [Agent-discovered policies](#agent-discovered-policies) |
| The behavior of a skill | `skills/<name>/` and its review cases in `tests/<name>/` | [Workflow changes](#workflow-changes) |
| The README, getting-started guide, visual guide, or diagrams | `README.md`, `docs/`, and `docs/assets/` | [Documentation and visuals](#documentation-and-visuals) |
| The plugin manifests, catalogs, or package version | `plugin.json`, `.claude-plugin/`, `.codex-plugin/`, and `.agents/plugins/` | [Packaging and releases](#packaging-and-releases) |

Provenance decides the path, not publication status. An agent-discovered policy
stays in the Discovery Lab after publication. If a discovered policy matches a
published method, the published method belongs to the literature path, with its
original sources. For a mixed contribution, prepare each part in its own home,
with its own checks.

Your coding agent can prepare either research path with the
[queue-contribute](skills/queue-contribute/SKILL.md) skill. Work in a Git
checkout of this repository or of your fork, and ask the agent to read
`skills/queue-contribute/SKILL.md` there. The agent pushes a branch or opens a
pull request only when your request includes that step.

## Literature knowledge

- Read the topic map in [queue-literature](skills/queue-literature/SKILL.md).
  Extend an existing note when it covers the topic.
- For a new note, follow the
  [note template](skills/queue-literature/assets/card-template.md). Start the
  file name with `modeling-`, `policy-`, or `knowledge-`. Add a topic-map row,
  and add the file name to the note inventory in
  [test_knowledge.py](tests/queue-literature/test_knowledge.py).
- Add each source to the
  [source registry](skills/queue-literature/references/sources.json) with its
  bibliographic identity and locators. In the note, cite it by its source ID,
  linked to `sources.json`, as the existing notes do.
- Check every substantive claim against its source at the stated locator. Write
  in your own words. Do not copy long passages or add paper files.
- The knowledge test checks structure, not science. Report your source checks
  separately in the pull request.

## Agent-discovered policies

Follow the [Discovery Lab contribution guide](discovery-lab/CONTRIBUTING.md).
It defines the entry layout (`policy.md`, `implementation/`, and `evaluation/`)
and the checks. Check the [index](discovery-lab/index.md) for an existing entry
to update before you add a new one.

Relate the method to the closest published methods, and report where baselines
win as well as where the method wins. Make only the novelty and performance
claims that your sources and tests support. Keep archived results separate
from checks that you ran for the contribution.

## Workflow changes

The skills are runtime instructions, so a change to a skill changes agent
behavior. Propose one workflow change at a time, and open an issue to discuss
it before a large edit.

- Keep these design boundaries unless the change explicitly proposes to revise
  them:
  - The two Stages are capabilities, not a required sequence.
  - Stage 2 confirms the queue family, objective, and constraints, and keeps
    them fixed until the user changes them.
  - The Discovery Lab opens only for explicit new-algorithm design.
  - Contribution starts only when the user asks.
  - The host chooses tools, delegation, and iteration.
- Do not add a required simulator, model schema, SDK, service, or host
  integration before the maintainers agree to that choice.
- Update the review cases in `tests/<name>/`. A review case gives an agent the
  skill and a request, without the reviewer checks, and compares the proposed
  actions with those checks. Record what you ran and its limits.
- When you change adapted upstream material, such as `asd-ste100` or the
  general guidance in `queue-literature`, update the local changes that its
  `NOTICE.md` records.
- Record each design decision and its reason in
  [docs/references.md](docs/references.md), apart from external references and
  open questions.
- [AGENTS.md](AGENTS.md) gives the same rules to coding agents that work on this
  repository.

## Documentation and visuals

The README, the [getting-started guide](docs/getting-started.md), the
[visual guide](docs/guide.html), and the [diagrams](docs/assets/) explain the
skills. They do not add rules. When a skill changes, update the documents that
describe it.

- Keep the visual guide a standalone page: no server, build step, or external
  assets. Its content stays readable without JavaScript.
- Keep each SVG diagram self-contained, with a title and a description, so that
  it renders on GitHub.

## Packaging and releases

- Keep the `queue-agent` name and the version identical in `plugin.json`,
  `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json`. Keep the
  catalog names in `.claude-plugin/marketplace.json` and
  `.agents/plugins/marketplace.json` aligned with that name.
- Bump all three manifest versions for a published package change. Claude uses
  the version to detect updates; refreshing the catalog is not a replacement
  for a version bump.
- Before a release, validate the manifests with the current native CLIs and
  test installation and loading for both hosts in isolated host profiles.
  Record the commands and results without changing personal host
  configuration.

## Requirements for every contribution

- **English:** write all repository content in English.
- **Attribution:** cite the source of each claim. Keep upstream copyright and
  license notices with adapted material, and record the pinned source, as the
  [queue-literature](skills/queue-literature/NOTICE.md) and
  [asd-ste100](skills/asd-ste100/NOTICE.md) notices do. Add only material that
  may be redistributed here.
- **No secrets or private data:** do not include credentials, tokens, `.env`
  files, private or personal data, or machine-specific absolute paths. Also
  omit bulky artifacts, such as raw traces or search histories. When evidence
  depends on data that cannot be published, ask the maintainers before you
  publish anything. A public or synthetic fixture can be an alternative.
- **Focused changes:** change only what the contribution needs, and leave
  unrelated files as they are.
- **Supported claims:** state results at the strength that the evidence
  supports, and name the checks that you ran.

## Run the checks

Run these commands from the repository root. They need only Python 3.10 or
later and its standard library.

```sh
python3 -m unittest discover -s tests/queue-literature -p 'test_*.py'
python3 -m unittest discover -s tests/queue-agent -p 'test_*.py'
python3 -m unittest discover -s tests/asd-ste100 -p 'test_*.py'
python3 -m unittest discover -s tests -p test_packaging.py
python3 -m unittest discover -s tests -p 'test_documentation.py'
```

These check the literature-note contract and reference integrity, the startup
hook from source, the bundled writing skill and linter, package identity and
contents, and documentation links and structure. They do not establish theorem
correctness, reader comprehension, or installed-host compatibility. Before a
release, also run the native validation in
[Packaging and releases](#packaging-and-releases).

Each Discovery Lab entry documents a policy smoke test and an archived-evidence
check in its evaluation note:

```sh
python3 discovery-lab/queue-aware-backfilling/implementation/smoke_test.py
python3 discovery-lab/queue-aware-backfilling/evaluation/verify_archived.py
python3 discovery-lab/bottleneck-work-block-planning/implementation/smoke_test.py
python3 discovery-lab/bottleneck-work-block-planning/evaluation/verify_archived.py
```

These checks test the portable policies and recompute the bundled
comparisons. They do not rerun the original simulation campaigns. The
backfilling verifier also recomputes its Student-t intervals. With NumPy
available, add `--bootstrap` to the block-planning verifier to recompute its
bootstrap intervals.

## Open a pull request

1. Create a branch from `main` in your fork or checkout.
2. Commit only the files of the contribution. Review the diff for unrelated
   files and for the items in the requirements above.
3. Open a pull request to `main`. State what it adds and where, the checks that
   you ran and their results, the limits of the evidence, and open questions
   for the maintainers.

## License

Original repository content is released under the [MIT License](LICENSE).
Bundled and adapted third-party material keeps its own notices.
