# Local Knowledge Collection

The `queue-literature` skill bundles **21 handbook notes and 48 source records**
for both Stages. Its [topic map](../skills/queue-literature/SKILL.md) groups the
notes by Stage, so the agent reads only what the current question needs and
searches further when the notes leave a material gap. The notes are a starting
point, not complete or current coverage of the literature.

## Coverage

- **Stage 1 (ten notes):** system descriptions and queue primitives; queue state
  and event dynamics; model adequacy and validation; event semantics and
  finite-window accounting; what logs identify; inference from partial logs;
  arrival, service, and patience primitives; time-varying arrivals; censoring
  and truncation; fitted-distribution tests.
- **Stage 2 (nine notes):** c-mu, generalized c-mu, SRPT, Gittins, load
  balancing, maximum pressure, backfilling, reentrant stage priority, and
  WIPLOAD release.
- **Shared (two notes):** model-policy fit and paired common-random-number
  evaluation.

## Layout

```text
skills/queue-literature/
  SKILL.md              # topic map that links every note
  NOTICE.md             # attribution and license notice
  assets/
    card-template.md    # template for new notes
  references/
    knowledge-*.md      # handbook notes
    modeling-*.md
    policy-*.md
    sources.json        # source registry
    tool-options.md     # optional retrieval tools, not a note
tests/queue-literature/
  test_knowledge.py     # note inventory and structural checks
  scenarios.md          # expected agent behavior
```

Each topic-map row lists the terms, aliases, and notation variants that keyword
search should match, such as `c-mu`, `cμ`, and `cµ`. Discovery terms and Stage
context live in the topic map, so notes have no metadata header.

A note explains a mechanism or method, where it applies, and what supports it,
with formulas and worked examples where useful. Each substantive claim cites a
registry record by its source ID, linked to `sources.json`, with a section,
theorem, or other locator. The
[template](../skills/queue-literature/assets/card-template.md) gives the
structure. A source record describes one cited work and version: `id`,
`title`, `authors`, `year`, `url`, `doi`, `locators`, and an optional `version`
qualifier when a citation would otherwise be ambiguous.

The notes are original, simulator-neutral summaries. They cite papers and
textbooks but do not reproduce them; [sources and provenance](knowledge-base-migration.md)
describes where their content and the adapted guidance come from. The
Discovery Lab is a separate collection and is not part of literature lookup.

The installed collection is versioned content. Agents save task findings in the
user's workspace, and reusable additions arrive as pull requests that follow the
literature path in [CONTRIBUTING.md](../CONTRIBUTING.md).

## Checks and limits

[`test_knowledge.py`](../tests/queue-literature/test_knowledge.py) checks every
note and source record. Each expected note must exist, have a title, a
substantive body, and at least one registry citation, and be linked from the
topic map. Local links must resolve inside the repository. Each source record
must be complete, cited by a note, and unique by ID and DOI. Audit metadata,
such as review status, review dates, reading depth, and legacy identifiers, is
rejected. Regression fixtures cover missing notes, titles, bodies, and
citations; broken or escaping links; unknown, uncited, or duplicate sources;
duplicate DOIs; missing locators; and reintroduced audit metadata.

These checks establish structure and reference integrity, not scientific
correctness. Scientific support comes from the cited sources at their stated
locators; contributors check claims against those sources and report the checks
in the pull request.

The [scenarios](../tests/queue-literature/scenarios.md) define the expected agent
behavior with the notes: for example, answering an established question
offline, refusing to transfer a theorem outside its assumptions, recognizing a
coverage gap, and declining to certify novelty.
