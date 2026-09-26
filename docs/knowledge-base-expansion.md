# Knowledge Expansion: First Prepared Batch

Prepared on 2026-09-25. This batch extends the original migration rather than
porting more legacy runtime code.

## Additions

| Card | Stage |
| --- | --- |
| [Partial event logs](../skills/queue-literature/references/modeling-partial-event-logs.md) | Stage 1 |
| [Arrival, service and patience inference](../skills/queue-literature/references/modeling-call-center-primitives.md) | Stage 1 |
| [Maximum pressure](../skills/queue-literature/references/policy-maximum-pressure.md) | Stage 1, Stage 2 |
| [Backfilling](../skills/queue-literature/references/policy-backfilling.md) | Stage 1, Stage 2 |

Each addition has a canonical source record and relevant-text locators. No
full-text papers are bundled. These are compact starting points, not a completed
survey of either Stage.

## Construction and review

Two local CC leads each launched an Opus research subagent to build topic outlines.
The parent used those outlines for source selection and read the primary material
behind these four cards. Exa supplied useful discovery and text retrieval.
A Firecrawl agent response lacked successful retrieval and contained incorrect
metadata; it was excluded as scientific evidence.

After an initial permission interruption, both CC leads resumed deep research.
A codex-x reviewer completed two review rounds on these four cards. The revisions
make the inference model's distributional assumptions explicit, tighten the
maximum-pressure theorem's action assumptions, identify an author-hosted
backfilling manuscript, and add the experimental-model citation locators.
The parent checked those corrections against the primary text. This batch adds
no installation or host-configuration changes.

The original structural suite covers the expanded source registry, card identities
and topic-map links. New behavioral scenarios are specified but have not been run
in an agent. Prior smoke-test records apply to the earlier versions only.

## Remaining work

Continue the approved deep-research items and review new cards as they become
ready. Routing, reentrant control, arrival diagnostics and fitted-model testing
are being researched separately; informative censoring still needs more than the
two modeling notes supplied here. Run the new behavioral scenarios before
claiming host-agent behavior has been validated.
