# Local Knowledge Collection

The `queue-literature` skill contains **20 handbook notes and 46 source records**.
Its [topic map](../skills/queue-literature/SKILL.md) separates Stage 1, Stage 2,
and shared material so the agent can read only what the current question needs.

## Coverage

- **Stage 1 — nine notes:** queue state and event dynamics; model adequacy and
  validation; event semantics and finite-window accounting; what logs identify;
  inference from partial logs; arrival, service and patience primitives;
  time-varying arrivals; censoring and truncation; fitted-distribution tests.
- **Stage 2 — nine notes:** c-mu, generalized c-mu, SRPT, Gittins, load balancing,
  maximum pressure, backfilling, reentrant stage priority, and WIPLOAD release.
- **Shared — two notes:** model-policy fit and paired common-random-number
  evaluation.

The notes retain mechanisms, formulas, assumptions, worked examples, and
claim-specific source references. Source records contain bibliographic identity,
useful locators, and version distinctions where necessary. Per-note audit tables,
review dates, reading-depth fields, and migration identifiers are not part of the
knowledge delivered to an agent.

## Validation and scope

Content and reference checks cover every note, topic-map link, source citation,
and local link. Regression fixtures exercise missing notes, broken or escaping
links, unknown or duplicate sources, duplicate DOIs, missing locators, and
reintroduced audit metadata. Scientific review additionally corrected several
inference and theorem-applicability statements; structural tests do not prove
scientific correctness.

The collection is simulator-neutral and imports no legacy runtime code. It
contains no full-text papers, research transcripts, experiment data, or credentials.
Incomplete drafts remain outside this repository. Further literature collection
is stopped for this update.

No Plugin installation or host configuration was performed. Earlier direct-load
smoke checks apply to the versions they tested, not to automatic host activation
or the entire expanded collection.
