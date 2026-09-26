# Reusing the Legacy Knowledge Base

Review date: 2026-09-25. **Research and proposal only; no knowledge or runtime code has been migrated.**

## Recommendation

Reuse the scientific content, not the QueueResearcher runtime. Start with a small,
shared collection of readable local files: a short topic index, focused knowledge
cards, and a source registry. Both Stages can consult it through the host agent.
No vector database, embeddings, always-on server, or new agent framework is needed.

Start under the existing `queue-literature` skill, which already serves both
Stages. Add local knowledge lookup to its evidence-reading guidance rather than
introducing another skill just to hold files. It would not run another agent or
require an online literature search for every question. The layout and card
format below are recommendations, not confirmed implementation choices.

## 1. What the old repository actually contains

Inspected source: the local `queue-research` checkout, whose configured origin is
`Efan404/queue-research`, at `a0dc5cc97021ac55700dbe2ddf3cf21523bb48b0`.
GitHub did not resolve that commit during this review; legacy file references
below identify the local snapshot, not a verified online copy.

| Layer | Current content | Migration value |
| --- | --- | --- |
| `docs/policy_science_kb/cards/policy_cards.yaml` | 45 cards across 37 family labels; 75 top-level evidence-claim rows and 29 nested negative-result rows with citations; 5 cards are dedicated to negative results. | Policy mechanisms, assumptions, required information/actions, guarantees, and counterexamples. |
| `docs/policy_science_kb/sources/source_inventory.yaml` | 93 source records, not necessarily distinct works. Card, claim, and nested negative-result source keys resolve. | Bibliographic identity, URLs/DOIs, and existing verification notes. |
| `docs/policy_science_kb/sources/textbook_foundations.md` | A categorized guide to queueing textbooks and monographs. | Starting references for model families, terminology, and validation formulas. |
| `src/queue_researcher/knowledge_base.py` and `retrieval.py` | JSON persistence, local text indexing, keyword retrieval, and citation records. | Useful requirements and test ideas, not a necessary runtime dependency. |
| `src/queue_researcher/part2/policy_kb/` | Typed cards, loading, evidence checks, and bridges into the old policy system. | Preserve scientific checks; leave framework integration behind. |
| Case Bank and experiment archives | Run-specific observations, failure labels, and evaluation records. | Potential future reviewed case studies, not automatically shared scientific knowledge. |

These counts come from parsing the current files, not copying the README.
The legacy corpus under `docs/policy_science_kb/` is mostly about policy design.
Its textbook guide is **not yet a substantive
Stage 1 library of identification and estimation methods**. Shared access does
not imply equal content coverage; Stage 1 notes need separate, source-grounded additions.

### Review issues to carry forward

- **27 source records explicitly say `revision_source_inventory_unverified`.**
  Other records range from metadata checks to primary-page or author-PDF checks.
  Finding a valid DOI does not establish that a theorem was read or its conditions checked.
- There are duplicate and conflicting identities. Two Chen-Yao 2001 records have
  the same ISBN (`9780387951669`); two records for the 2020 generalized c-mu/h paper
  give different DOIs. Reconcile these against authoritative sources and preserve
  old-key aliases. Do not count 93 records as 93 independently verified works.
- Some claims need substantive rewriting, not just field renaming. For example,
  the FIFO-instability card moves from a constructed counterexample to a broad
  necessity claim about equal service-time means. Its nested warning must not be
  promoted without rereading the cited result (`policy_cards.yaml:2733-2779`).
  This is a flagged scope issue, not a new theorem established by this audit.
- The README still describes 32 cards and 57 sources. The saved machine-check
  artifact describes 45 cards and 91 sources. Neither is a fresh certificate for
  the current corpus.
- Four card implementation-status values are outside the descriptive YAML
  schema's enum. The Python model accepts a string here; loading the files is not
  equivalent to enforcing that enum. Do not carry the historical `pass: true`
  into a new validation report.
- Preserve negative results and their exact scopes. They help prevent incorrect
  generalization; they are not universal bans on the corresponding policy families.

Consequently, do not copy the entire YAML corpus verbatim and present it as
reviewed knowledge. It is a useful topic-and-source inventory from which to
rebuild a reviewed slice. This review checks migration readiness and file
consistency; it does not reverify all listed publications or endorse every claim.

## 2. What external standards and templates support

| Source | What it establishes | What we should reuse |
| --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | A skill has a `SKILL.md`; `references/` supports on-demand documentation, and `assets/` can hold templates and structured resources. | A small entry point with focused supporting files, rather than a complete corpus pasted into instructions. |
| [Claude skill documentation](https://code.claude.com/docs/en/skills) | Skills can link supporting files and explain when to read them. | Explicit navigation and selective reading. Files are not useful merely because they exist somewhere in the repository. |
| [Agent Plugins specification, sections 4 and 7](https://agent-plugins.org/specification) | Bundled package paths stay inside the Plugin root; skills have a defined discovery location. | Ship the knowledge with the Plugin. Do not depend on an adjacent old repository, an absolute developer path, or an outward symlink. |
| [Claude manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) | The installed Plugin root and persistent Plugin data are different locations; the root can change on update. | Treat shipped references as versioned content. Save task findings outside the installed reference collection. |
| [Anthropic memory-management example](https://github.com/anthropics/knowledge-work-plugins/blob/da38ec1ee89d41e5380e652a97382695003396e7/productivity/skills/memory-management/SKILL.md) | A first-party example uses a small working index plus deeper Markdown files in the user's working directory. | The small-index/deeper-files pattern, not its workplace-memory schema, automatic account scans, or `CLAUDE.md` writing behavior. |

**These standards do not prescribe a scientific knowledge-card schema or a search
algorithm.** Our evidence fields and shared-knowledge organization are application
design choices. The Anthropic example is a useful template, not a universal KB standard.

There is also no blanket prohibition on sharing files between skills inside one
Plugin. The packaging problem is reaching outside the distributed package, or
assuming another skill has been installed when a skill is distributed alone.
Host compatibility still needs testing; documentation is not an installation test.

## 3. Proposed organization

For the first slice, keep the knowledge with the existing shared skill:

```text
skills/
  queue-literature/
    SKILL.md                 # Existing guidance plus a short local topic map
    references/
      tool-options.md        # Already present
      knowledge-foundations.md
      policy-c-mu.md
      policy-srpt.md
      negative-priority-instability.md
      ...                    # Focused cards, directly linked from the topic map
    assets/
      sources.yaml           # One canonical bibliographic registry
      card-template.md
```

The filenames illustrate organization, not approved scientific content. In this
proposal, Markdown cards hold the substantive knowledge; structured source records
retain citation metadata. There is no second manually maintained YAML copy of
every card. The short topic map lives in `SKILL.md` and uses tags/aliases such as
`c-mu`, `cμ`, `SRPT`, and `M/M/1` to help the host find relevant files.

Other options remain viable as the Plugin grows:

- **Plugin-root `knowledge/`:** one shared corpus, but each consuming skill needs
  explicit path handling; an individually copied skill would lose that dependency.
- **A separate `queue-knowledge` skill:** gives a broader collection its own
  entry point, but adds discovery and routing to a Plugin that currently has only
  one skill. Revisit when concrete additional consumers justify it.

This initial location does not make the content exclusive to literature review
or either Stage. Other Plugin skills can later read the same files through
explicit within-package references; they should not keep duplicate corpora.
Cross-skill discovery and paths must be tested rather than assumed automatic.
The existing skill remains useful for supplied papers and external research even
when the local collection has no relevant entry.

### Minimum content of a card

Keep a small common header: stable ID, title, kind, Stage relevance, tags/aliases,
source keys, review status, and origin. Preserve the legacy ID in origin metadata
if an ID changes. Add a review date only for work actually reviewed on that date.

The body should answer:

1. **What does this say?** A model fact, identification method, policy mechanism,
   theorem, empirical finding, or negative result.
2. **When does it apply?** Assumptions, observations or controller information,
   available actions, objective, and important exclusions.
3. **What supports each substantive claim?** Source key plus section, theorem,
   page, algorithm, or experiment when available; otherwise state what was inspected.
4. **How is it useful here?** A short explanation, with adaptation ideas clearly
   separated from source results.

Use kind-specific sections rather than forcing modeling notes to have policy
actions. Keep citation-identity checks, claim verification, and applicability to
the current task separate. Historical confidence labels may be retained as
provenance, but should not automatically authorize recommendations.

## 4. Keep, adapt, and leave behind

| Legacy material | Treatment |
| --- | --- |
| Policy description, assumptions, contraindications, objective, required state/actions | Preserve the scientific meaning; review overly broad statements against cited sources. |
| Stable card/source IDs and claim-to-source links | Preserve; maintain an explicit mapping for renamed or merged entries. |
| Bibliographic metadata and verification notes | Preserve and normalize without upgrading the stated evidence quality. |
| Textbook foundations | Rewrite into shared reference guidance; distinguish a reading list from a verified formula or modeling procedure. |
| `implementation_status`, `simulation_v2_affordance`, old Stage labels, `ModelSpec`/`ObjectiveSpec` references | Replace with simulator-neutral requirements where there is scientific content. Keep old implementation details only in migration provenance, not general knowledge. |
| `candidate_generator_hint` | Keep genuinely reusable design ideas; remove instructions specific to the old Policy Scientist, EOH operator, or pipeline. |
| Loader/model imports, discovery bridges, automatic recommendation gates, agent orchestration | Do not import into the initial Plugin KB. |
| Run logs, raw Case Bank records, benchmark data, experiment archives, old validation reports | Do not bulk-import. A useful future case needs its own reviewed summary and evidence. |

The old Python loader imports `part2.stage34`; its card models also convert into
old candidate contracts. A direct code copy would reintroduce the architecture
we are trying to leave behind.
Source: `src/queue_researcher/part2/policy_kb/loader.py:14-21` and
`src/queue_researcher/part2/policy_kb/models.py:9-14,86-95`.

The generic retrieval primitives also should not be copied uncritically:
`answer_query` concatenates snippets rather than synthesizing an answer; JSON
persistence overwrites the entire file and is documented as single-writer only.
The local indexer reads text/Markdown, not the policy YAML corpus. A small live
check also found that a query `M/M/1` becomes `mm1`, but a record containing only
the raw notation in its snippet can be missed; queries `cμ` and `cµ` tokenize to
an empty set. Preserve useful citation/search tests, not these behaviors.
Source: `src/queue_researcher/retrieval.py:43-100,143-159,194-230` and
`src/queue_researcher/knowledge_base.py:54-69`.

## 5. How the agent would use it

1. Start with the user's question and supplied material. Consult the local topic
   map when existing queueing knowledge is relevant.
2. Read only the relevant cards and source records. The host's existing file
   reading and keyword search are enough initially; no custom retrieval service
   or Python dependency is needed just to read them.
3. Check assumptions against the current task. Return a concise answer with
   source attribution, not an automatic report or recommendation pipeline.
4. Use `queue-literature` and available external tools for missing evidence,
   disputed claims, recent developments, or a requested novelty/landscape review.
   A cached bibliography does not settle what is new today.

Separate **bundled shared knowledge** from **project findings**. New task notes
belong in the user's chosen workspace, when saving them is requested. Useful
findings can later be proposed as reviewed repository contributions; do not
silently append agent-generated claims to the installed KB.

## 6. Smallest useful migration, after the design is confirmed

1. Start with one classical policy card, such as c-mu, and verify its exact
   assumptions and result against the primary source. Then add a size/preemption-
   sensitive policy such as SRPT or Gittins, and relevant foundational guidance.
   Attach reviewed limits to the affected policy; retain separate negative-result
   cards only where a distinct result warrants one. Defer problematic network
   instability/admission cards until their source claims have been checked.
2. Convert that slice to readable cards and the source registry; record source
   commit, old card IDs, changed wording, and review status. Preserve attribution
   and check reuse terms for any copied third-party text; do not bundle textbook PDFs.
3. Add a short topic map and local lookup guidance to `queue-literature`.
   Do not add a manifest, MCP server, or runtime framework as
   an incidental dependency of this content step.
4. Check unique IDs, resolvable source links (including nested negative-result
   citations), complete claim mappings and limitations, file paths, and separation
   of scientific requirements from old implementation restrictions.
5. Run small temporary host-agent checks without installing on this machine:
   known-topic lookup without web access; recognizing a policy's unavailable
   preemption/size information; recognizing missing Stage 1 content; and handing
   off a genuinely current-literature question. These are behavior checks, not
   proof of installed-package compatibility.
6. Expand the corpus after the slice works. Test actual host packaging separately
   when installation/distribution becomes an approved step. Add a standalone
   search helper only if observed lookup failures justify one.

For community contributions, the initial unit can simply be a focused card plus
its source records and a reviewable explanation of assumptions. No new database
service or agent framework is required to contribute useful queueing knowledge.

## Review boundary

The evidence combines direct inspection of legacy files, read-only consistency
checks, Firecrawl retrieval of the Agent Skills standard, Exa retrieval of the
first-party template and packaging documentation, and Context7 documentation
cross-checks. Two completed independent local-agent reviews covered content and
runtime coupling. The content review sampled 20 of 45 cards, including all five
dedicated negative-result cards; its literature-recall objections were treated
as review leads, not verified paper results. The parent checked the reported
identity conflicts, nested citations, and representative card wording locally.

The code review favored a verbatim YAML reference import for minimal change;
the content review favored reviewed Markdown rewrites. The recommendation here
keeps the minimal existing-skill location but adopts a small, source-checked
rewrite because preserving old wording unchanged would also preserve its errors.
External standards support the file-based pattern; the particular content layout,
card format, and migration sequence remain proposals.
