# Queue Agent Plugin: References and Design Decisions

This document contains the confirmed design decisions and their reasons
(Section 1), external standards, projects, and suggestions (Sections 2 to 6),
and open questions (Section 7). Upstream projects inform the design; they are
not adopted as a whole.

## 1. Confirmed decisions

### Repository and documentation

- Use English for all repository content.
- Release original repository content under the [MIT license](../LICENSE).
  Bundled and adapted third-party material keeps its own copyright notices and
  license terms.
- Provide an English visual guide and workflow diagrams for readers. Keep them
  separate from runtime skill instructions: they explain the available routes,
  not a compulsory sequence or a new orchestration layer. The guide runs locally
  without a build step or external assets; the SVG diagrams also render on GitHub.

### Packaging and installation

- The repository root is one package, `queue-agent`, version `0.1.0`. It has a
  portable root `plugin.json`, compatibility manifests in
  `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, and native
  catalogs in `.claude-plugin/marketplace.json` and
  `.agents/plugins/marketplace.json`. It provides six skills and a SessionStart
  hook, with no MCP server, app, or separate service.
- Each catalog selects the repository root (`./`). Skills, literature notes, and
  Discovery Lab resources stay together, so their relative links work in the
  installed cache. Packaging does not change when an agent may read the
  Discovery Lab.
- Users install with each host's native marketplace-add and plugin-install
  commands, combined into one copyable shell line. There is no custom installer,
  new runtime dependency, or host configuration overlay. See
  [Getting started](getting-started.md) for the installation and lifecycle
  commands.
- Each host discovers `hooks/hooks.json` at its default location. The manifests
  do not also declare it, because Claude adds declared hook paths to the default
  file rather than replacing it. The hook needs `python3`; explicit skill
  selection works without it. Codex hook trust is separate from plugin
  enablement.
- Validate manifests and installation in isolated host profiles, not in a
  developer's working configuration. Installation and component-discovery
  checks do not establish the quality of an agent's research results.
- Bump all three manifest versions together for each published package change.
  Claude caches releases by version, so a catalog refresh alone does not replace
  an installed release whose version is unchanged.
- Distribution uses these repository catalogs. It is separate from a hosted
  website or an official host directory listing.

References: [OpenAI packaging and catalog format](https://developers.openai.com/plugins/build/plugins),
[Claude manifest and component paths](https://code.claude.com/docs/en/plugins/manifest-reference),
[Claude marketplace paths](https://code.claude.com/docs/en/plugin-marketplaces),
and [Claude installation](https://code.claude.com/docs/en/discover-plugins).

### Two-Stage overview

Users work with their own coding agent; Claude Code and Codex are the intended
hosts.

- **Stage 1, queue modeling:** deliver a documented queue model and its
  corresponding executable simulator from data and a system description, with
  replaceable policies and checks that the implementation matches the model.
- **Stage 2, policy design:** confirm the queue family, objective, and
  constraints with the user, then select, evaluate, tune, or design policies
  according to their needs. Keep that problem definition fixed unless the user
  explicitly authorizes a change.

The Plugin first gives the agent this task map: **data → queue model → policy**.
The user's current task determines where to start; not every request runs both
Stages.

The user and the host agent direct the research. The Plugin supplies reusable
domain knowledge, methods, tools, and cases, and the host agent organizes the
work with its own tools and delegation. The queueing community can contribute
further knowledge and capabilities.

### Entry and task routing

- [queue-agent](../skills/queue-agent/SKILL.md) is the entry skill. It selects
  the current task from the latest request and the available artifacts, rather
  than storing one Stage for the whole session.
- A usable model, simulator, or specified model family can start directly at
  Stage 2. Building its evaluator does not itself require Stage 1 inference from
  historical data. Requests to assess or revise model-data agreement use Stage 1.
- Literature questions and discussion are valid standalone tasks; the overview
  does not automatically start implementation or experiments.
- A short SessionStart orientation points to the entry skill. Detailed guidance
  stays in the skills, with no workflow engine or persistent Stage state. Host
  hook approval remains separate.

### Stage 1 modeling

- [queue-modeling](../skills/queue-modeling/SKILL.md) guides building,
  calibrating, and validating a queue model and its corresponding executable
  simulator from data and a system description.
- Deliver both a self-contained model description and a runnable implementation.
  The description states the structure, dynamics, stochastic mechanisms,
  parameters, assumptions, and policy decision interface. Keep it consistent
  with the simulator and configuration, and validate that correspondence.
  The representation and file layout remain task-dependent.
- The simulator generates trajectories and accepts policy decisions, so it can
  support subsequent policy evaluation. Its handoff includes the fitted
  configuration, execution instructions, and concise validation results alongside
  the model description.
- Encourage a separate validation subagent, where the host supports it, to work
  from the original evidence and run checks. Feedback should identify concrete
  discrepancies and supporting results; the main agent integrates the feedback
  and revises the model.
- Leave the representation, simulation tools, agent allocation, and iteration
  schedule to the host agent and the user's task.
- Reuse queue-literature and its local knowledge. Keep runtime instructions
  focused on the modeling task and useful resources.

### Stage 2 policy design

- [queue-policy](../skills/queue-policy/SKILL.md) is the overall Stage 2 skill,
  not a workflow limited to discovering new algorithms.
- Before execution, summarize the queue family, objective, and constraints from
  the Stage 1 handoff, user input, and conversation. Ask only about unresolved
  decisions, then obtain explicit user confirmation of the problem definition.
  Reuse confirmation already given rather than asking again. An unanswered
  question leaves execution pending, including in unattended runs.
- Keep the confirmed definition in the task's working notes and pass it to any
  workers. All three parts remain fixed unless the user explicitly authorizes a
  change. Update the affected definition, evaluator, metrics, and baselines after
  a change, without reopening decisions that remain unchanged.
- This is an instruction-level workflow in queue-policy, not a new skill, MCP
  service, or permission hook. Use a host question tool when available, with
  ordinary conversation as the fallback. The approach follows the guidance to
  define questions and stopping conditions in [OpenAI's skill documentation](https://developers.openai.com/plugins/build/skills#define-the-workflow-boundary)
  and the interactive clarification pattern in [Claude Code's best practices](https://code.claude.com/docs/en/best-practices#let-claude-interview-you).
- Combine the user's needs and queue structure to choose adoption, comparison,
  parameter tuning, or policy design. These approaches can be combined without
  making every task a broad discovery campaign.
- A missing simulator does not prevent direct Stage 2 entry. When simulation is
  needed, build an evaluator for the specified model rather than requiring new
  operational logs or repeating Stage 1 identification.
- For policy discovery, target the fixed family's shared structure and evaluate
  representative allowed instances. Keep policy structure separate from parameter
  values, allowing tuning for a particular queue without changing the family.
- Keep discovery guidance in the conditional
  [Policy Discovery reference](../skills/queue-policy/references/policy-discovery.md),
  reached from queue-policy, rather than a separate skill. Development subagents
  own autonomous inner iterations; the main agent integrates evidence, adapts
  research directions and support in outer iterations, and verifies results.
  Reuse useful trials without fixing team sizes, round counts, or tools. Both
  loops retain the confirmed definition.
- Refine promising policies through task-appropriate simplification, component
  ablation, and parameter sensitivity checks. Prefer simpler rules when evaluation
  supports practically negligible performance differences; retain useful complexity
  without a fixed parameter limit. Check the final algorithm against the closest
  literature, including changes introduced by simplification or combination.
- Make comparison checks concrete: decision-time information access, faithful
  baseline implementations, justified parameter selection, and evidence from the
  final evaluated version. Keep explanations aligned with the evaluated code and
  parameter values, and explain mechanisms and important result patterns for
  readers outside the development process. These checks belong to the skill and
  its discovery reference; they do not make every Stage 2 task a research
  campaign. See the [refinement checks](../tests/queue-policy/refinement-scenarios.md).
- Use shared queue-literature knowledge and an optional external pointer to
  [SimOpt](https://github.com/simopt-admin/simopt) and its
  [solver documentation](https://simopt.readthedocs.io/en/latest/solvers.html) for
  simulation-based tuning. The host inspects current methods and decides what
  fits; SimOpt is neither bundled nor a required backend.
- Deliver the requested policy or recommendation, applicable family, parameters,
  and performance evidence, plus implementation/evaluator artifacts when those
  are part of the task. Host tools, delegation, and iteration remain flexible.

### Shared literature

- [queue-literature](../skills/queue-literature/SKILL.md) is one shared skill
  for both Stages, not a separate literature agent.
- Adapt useful search, synthesis, and citation guidance from existing
  open-source skills, preserving upstream attribution and licensing. Add
  queue-specific guidance about model assumptions, observations, policies,
  objectives, baseline applicability, and theoretical results.
- Use the host's available search and reading tools. Paper Search MCP is an
  optional candidate when academic retrieval is missing; Zotero is optional for
  an existing library. Neither is a fixed dependency.
- Scale the work to the question; do not require figures, a complete report, a
  fixed backend, or running both Stages.

The skill's [attribution](../skills/queue-literature/NOTICE.md) records the
upstream sources, adaptations, and MIT notice. See also the
[optional tool references](../skills/queue-literature/references/tool-options.md)
and [review cases](../tests/queue-literature/scenarios.md).

### Shared writing

- [asd-ste100](../skills/asd-ste100/SKILL.md) is an independent shared skill
  for English model descriptions, policy explanations, and reports in both
  Stages, separate from queue-literature.
- Default these deliverables to STE-flavored prose. Preserve technical terms,
  equations, assumptions, numerical results, citations, and claim strength.
  Explain the system and decision for readers outside the development process.
- Point to it from the overall entry and both Stage delivery steps. Do not add
  a hook that rewrites every response.
- Preserve the upstream license and record the pinned source and adaptations in
  [NOTICE.md](../skills/asd-ste100/NOTICE.md). Use the included linter as optional
  language feedback, not as proof of scientific correctness or readability.
- The writing skill does not expand either Stage's research scope.

### Local knowledge

- Keep local knowledge under queue-literature, shared by both Stages: focused
  Markdown handbook notes, a topic map in the skill, and one JSON source
  registry. JSON keeps the integrity checks dependency-free. Other skills link
  to the same files inside the package instead of keeping their own copies; a
  plugin-root directory would need path handling in each consuming skill, and a
  separate knowledge skill would add discovery and routing.
- Ship the knowledge inside the package, with links that stay within it. The
  installed copy is versioned content; task findings belong in the user's
  workspace.
- Use ordinary host file reading and keyword search. Do not introduce a vector
  knowledge base, embeddings, or a new retrieval service; add a search helper
  only if observed lookup failures justify one.
- Keep Stage and topic discovery in the skill's topic map. Notes use handbook
  prose for assumptions, results, limitations, and citations rather than
  per-note IDs, aliases, review status, dates, or migration origin.
- Keep stable note paths and source IDs. Limit source records to bibliographic
  identity, useful claim locators, and a concise version qualifier when citation
  identity requires it. Preserve scientifically meaningful unverified or
  secondhand scope in the note prose.
- State each claim at the strength that its source supports. Confidence labels
  inherited from earlier material do not count as verification.

The standards define where supporting files live and how a skill links them,
not a schema for scientific notes; the note format is this project's choice.
The small index with deeper files follows the pattern, not the schema or
behavior, of Anthropic's memory-management skill. References:
[Agent Skills](https://agentskills.io/specification),
[Claude skills](https://code.claude.com/docs/en/skills),
[Agent Plugins](https://agent-plugins.org/specification),
[Claude plugin root and data directories](https://code.claude.com/docs/en/plugins/manifest-reference),
and the [memory-management skill](https://github.com/anthropics/knowledge-work-plugins/blob/da38ec1ee89d41e5380e652a97382695003396e7/productivity/skills/memory-management/SKILL.md).

The [local knowledge collection](knowledge-base-expansion.md) describes the
current coverage and checks, and [sources and provenance](knowledge-base-migration.md)
describes where the notes' content and adapted guidance come from.

### Community contributions and Discovery Lab

Keep core skills focused on reusable research workflows. Community content has
two contribution paths, rather than making each algorithm or topic a new skill:

1. **Literature knowledge:** extend the content under `queue-literature` with
   existing literature, classical algorithms, modeling methods, applicability
   conditions, and practical knowledge supported by sources.
2. **Agent-discovered policies:** contribute new methods discovered through LLM
   agent research to a separate results component called
   **Discovery Lab**. Entries explain the method, its relationship to prior work,
   implementation, and evaluation evidence. This is not a general algorithm
   catalog; classical methods belong in the literature knowledge base and may
   be cited as references or baselines in discovery entries.

#### Research access: explicit opt-in

Discovery Lab is not part of the agent's default knowledge base. Keep its
contents out of default literature retrieval and loading. Treat entries as
exploratory research results; their experimental evidence does not substitute
for scientific peer review.

- Consult Discovery Lab only after the user explicitly requests the design of
  a new algorithm. A generic request to improve performance is not sufficient.
- Ordinary modeling, adoption or comparison of existing policies, and tuning
  parameters of a fixed policy do not activate this resource.
- Once enabled, explore relevant entries as research leads, mechanisms to adapt,
  or ideas to combine. Evaluate their applicability and performance for the
  current confirmed problem; previous experiments do not establish performance
  in the user's setting.
- Discovery provenance defines the collection, not publication status alone.
  Later peer review of an entry does not automatically change this access rule.

#### Optional contribution workflow

A separate, optional `queue-contribute` skill is activated when the user asks
to contribute. It helps the user's own agent choose one or both contribution
paths, prepare the relevant material, check it, and submit a PR under the user's
authorization. Maintainers decide whether to merge the contribution; repository
review does not itself constitute scientific peer review.

Contribution is separate from Stage 1 and Stage 2 execution. Completing research
does not automatically publish user data, code, or findings. Preparing a requested
contribution is not permission to use Discovery Lab as default research knowledge.

#### Layout and boundaries

[`discovery-lab/`](../discovery-lab/index.md) is a plain resource directory with
two entries. Each entry has `policy.md`, a portable implementation, and compact
archived evidence with runnable checks; there is no shared simulator interface
or runtime service. The research-time access rule lives in `queue-policy`;
`queue-literature` searches only its own references, and `queue-agent` routes
requested contributions to [`queue-contribute`](../skills/queue-contribute/SKILL.md).
The [Lab access](../tests/queue-policy/lab-access-scenarios.md) and
[contribution](../tests/queue-contribute/scenarios.md) review cases cover these
boundaries.

## 2. Official standards

| Layer | Purpose | Primary reference |
| --- | --- | --- |
| **Skill** | Explain when and how to perform a task, with optional references, scripts, and templates. | [Agent Skills specification](https://agentskills.io/specification) |
| **MCP** | Connect a host to tools, resources, and prompt templates; it does not define the research workflow. | [MCP server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts) |
| **Plugin** | Package reusable components. Installation, permissions, and interaction remain host-specific. | [Agent Plugins specification](https://agent-plugins.org/specification) |

**A Plugin does not require an MCP server.** Skills can use local scripts; MCP is useful when a standardized tool interface is needed. [OpenAI skills guide](https://developers.openai.com/plugins/build/skills)

Agent Plugins 1.0.0 defines a root `plugin.json`, fixed `skills/`, and optional `mcp.json`, with namespaced client extensions. It standardizes the package, not every host's behavior. [Specification](https://agent-plugins.org/specification)

OpenAI recommends this format for new packages while retaining `.codex-plugin/plugin.json` for compatibility. Existing scaffolds and tutorials may use older layouts. [OpenAI packaging guide](https://developers.openai.com/plugins/build/plugins)

Claude Code documents `.claude-plugin/plugin.json`. A portable standard does not establish that both hosts support every configuration identically. [Claude manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)

## 3. Shared content and host-specific behavior

| Component | Documented behavior | Implication |
| --- | --- | --- |
| `skills/<name>/SKILL.md` | Both hosts support this organization. | Maintain shared domain methods. |
| `references/`, `scripts/`, `assets/` | Agent Skills permits supporting knowledge, executable scripts, and templates. | Package queueing references and helpers with explicit dependencies. |
| Manifest | Codex recommends root `plugin.json`; Claude documents `.claude-plugin/plugin.json` and permits omission in some standard-layout loading paths. | Separate host entry points from shared content; do not just rename manifests. |
| MCP configuration | Portable packages use `mcp.json`; Claude defaults to `.mcp.json`. Portable entries declare a transport `type`. | Reuse interfaces while checking each host's configuration. |
| Commands, subagents, hooks | Claude declarations are not automatically executable in Codex. OpenAI recommends converting reusable behavior to skills and adapting hooks. | Avoid binding essential domain capabilities to one host's orchestration features. |
| Installation and permissions | Hosts manage installation, approval, and updates. Codex hook trust is separate from Plugin enablement. | Installation alone does not establish that every component can run. |

Sources: [Agent Skills](https://agentskills.io/specification), [Claude reference](https://code.claude.com/docs/en/plugins/manifest-reference), [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), and [Claude-to-OpenAI migration](https://developers.openai.com/plugins/guides/submit-claude-plugin). The migration guide concerns OpenAI's submission flow: its public-HTTPS requirement is not a prohibition on local tools in local Plugins.

Two details to retain:

- Root `extensions.com.openai`, when present, replaces the OpenAI-specific compatibility overlay rather than merging with it. Portable skills and MCP still use fixed paths. [Precedence rules](https://developers.openai.com/plugins/build/plugins#add-openai-specific-metadata)
- Claude does not load a Plugin-root `CLAUDE.md` as instruction context. Put runtime guidance in skills, and keep experiment outputs outside the versioned installation directory. [Claude reference](https://code.claude.com/docs/en/plugins/manifest-reference)

### Entry guidance and session context

Skill names and descriptions are available for selection, but full instructions
are loaded when a skill is selected. An entry skill alone is not an always-loaded
system prompt. [OpenAI skill activation](https://developers.openai.com/plugins/concepts/skills)

Claude Code and Codex both document SessionStart command hooks returning
`hookSpecificOutput` with `hookEventName: "SessionStart"` and
`additionalContext`. This is the shared output shape used by the orientation
source. It adds task guidance, not authority to override the host or the user.
[Claude hooks](https://code.claude.com/docs/en/hooks#sessionstart),
[Codex hooks](https://learn.chatgpt.com/docs/hooks#sessionstart)

The hook command accepts `CLAUDE_PLUGIN_ROOT` or `PLUGIN_ROOT`, quotes the
resolved path, and requires `python3`. Claude documents the former; Codex
documents its own root variable and the Claude-compatible alias. The source
checks cover this portable path, not automatic activation: platform support and
hook trust still determine whether the installed hook runs.
[Claude Plugin reference](https://code.claude.com/docs/en/plugins-reference),
[OpenAI Plugin packaging](https://developers.openai.com/plugins/build/plugins)

## 4. Creation, testing, and distribution references

Native packaging and isolated installation checks use the references below.
Model-call evaluations and official directory submission are separate tasks;
the supported user commands are in [Getting started](getting-started.md).

| Task | Official entry point | Distinction |
| --- | --- | --- |
| Write a skill | [Agent Skills specification](https://agentskills.io/specification); `skills-ref validate ./my-skill` | Format validation does not establish scientific correctness. |
| Package a Plugin | [Build an Agent Plugin](https://agent-plugins.org/plugin-authors/build-an-agent-plugin) | A server is optional. |
| Check a Claude package | `claude plugin validate ./my-plugin`; [reference](https://code.claude.com/docs/en/plugins/manifest-reference) | Static checks still need task-level testing. |
| Try it locally in Claude | `claude --plugin-dir ./my-plugin`; [creation guide](https://code.claude.com/docs/en/plugins/create) | Local testing does not require publication. |
| Evaluate behavior in Claude | `claude plugin eval .`; [Plugin evals](https://code.claude.com/docs/en/plugin-evals) | With/without-Plugin comparisons make real model calls. |
| Distribute for Claude | [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace); [reference](https://code.claude.com/docs/en/plugins/marketplace-reference) | The marketplace catalog is not the Plugin manifest. |
| Distribute locally for Codex | `codex plugin marketplace add ./local-marketplace-root`; [packaging guide](https://developers.openai.com/plugins/build/plugins) | The repository catalog is `.agents/plugins/marketplace.json`; the Plugin has its own directory. |
| Enable and test in OpenAI clients | Local-install and repository-enablement sections of the [packaging guide](https://developers.openai.com/plugins/build/plugins) | Follow the actual client version's supported route. |
| Publish publicly | [OpenAI submission guide](https://developers.openai.com/plugins/guides/submit-claude-plugin) | Local use, team distribution, and public submission are separate flows. |

## 5. Projects worth studying

These lessons are interpretations, not decisions to adopt entire projects.

| Project | Observed approach | Useful lesson |
| --- | --- | --- |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Scientific skills, a portable manifest, and contribution conventions. | Community-maintained domain knowledge, methods, and supporting tools. |
| [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) | Domain packages combining skills, commands, and MCP through a marketplace. | Organize expertise and user entry points without replacing the host runtime. |
| [Hugging Face Skills](https://github.com/huggingface/skills) | Skills guide existing ML tools; a curated marketplace uses `hf-cli` as an entry point. | Separate guidance from implementation and load specialized capabilities as needed. |
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | A research application with execution stages, state, experiment loops, and skills. | Reuse ideas about records and feedback, not necessarily its pipeline architecture. |

Read K-Dense's [contribution guide](https://github.com/K-Dense-AI/scientific-agent-skills/blob/49c6e97775eaa18ba791bebe23162a70ae601c18/CONTRIBUTING.md), Hugging Face's [marketplace](https://github.com/huggingface/skills/blob/80f9fa530e46f4ae642fcb9e1725bad0e1979395/.claude-plugin/marketplace.json), and the Knowledge Work Plugins [marketplace](https://github.com/anthropics/knowledge-work-plugins/blob/da38ec1ee89d41e5380e652a97382695003396e7/.claude-plugin/marketplace.json).

For community governance, inspect enforced workflows rather than README invitations alone. Anthropic's repository closes most external PRs and directs contributors through a submission route: useful packaging, but not automatically our contribution model. [PR workflow](https://github.com/anthropics/knowledge-work-plugins/blob/da38ec1ee89d41e5380e652a97382695003396e7/.github/workflows/close-external-prs.yml)

Check licenses and dependencies per skill or resource. K-Dense, for example, documents separate terms for vendored Anthropic document skills. [K-Dense README](https://github.com/K-Dense-AI/scientific-agent-skills#readme)

Reviewed revisions: K-Dense `49c6e97775ea`, Hugging Face `80f9fa530e46`, Knowledge Work Plugins `da38ec1ee89d`, AutoResearchClaw `be4ba4755bf1`. AutoResearchClaw's [host-facing skill](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/.claude/skills/researchclaw/SKILL.md) invokes a separate runtime: a skill entry point does not itself imply a Plugin-centered architecture.

### Documentation patterns

Three established repositories informed the presentation, not the research
workflow. The linked revisions identify the material reviewed.

| Source | Pattern used here | Boundary |
| --- | --- | --- |
| [Anthropic Skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44) | Small skill folders with instructions and supporting resources; separate explanations of source content and host use. | No assumption that one host's installation route works in another. |
| [Superpowers](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | An overview that explains the workflow before sending readers to focused guidance. | Queue Agent keeps task-dependent entry points, not a mandatory development sequence. |
| [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin/tree/1522cc36e14b5c2c44afcdb5793370bd4ac8d418) | A readable skill map and separate contribution and detailed-use documentation. | No import of its orchestration, tools, configuration, or agent count. |

These are organizational references; their source code and visual assets are
not bundled.

### Remote literature retrieval options

These findings, as of 2026-09-26, concern remote academic retrieval that would
not require users to install a local MCP server. They are research findings, not
a decision to replace Paper Search MCP or to deploy a service; the package
configures no MCP server.

| Option | Evidence and access | Implication for the Plugin |
| --- | --- | --- |
| [Paper Search MCP](https://github.com/openags/paper-search-mcp) | MIT; unreleased `main` supports Streamable HTTP, but released PyPI 0.1.4 is stdio-only. Neither supplies native bearer-token/OAuth authorization. Its [Smithery listing](https://smithery.ai/servers/openags/paper-search-mcp) advertises an older hosted deployment. | HTTP support does not itself supply a maintained public endpoint. Keep it as an option, but do not bundle the advertised URL as a verified working default. |
| [Ai2 Asta Scientific Corpus MCP](https://allenai.org/asta/resources/mcp) | Official hosted endpoint: `https://asta-tools.allen.ai/mcp/v1`. A live anonymous check completed initialization, listed eight tools, and successfully called `search_paper_by_title` for a known paper. Ai2 documents optional API keys for higher rate limits. | Lowest-friction **tested** alternative for discovery, citation lookup, and available text snippets. A hosted service is not proof that its server implementation is open source; that license was not established. |
| [Official OpenAlex MCP](https://github.com/ourresearch/openalex-mcp-server) | MIT; publishes `https://mcp.openalex.org/mcp`. Current source requires OAuth and uses the consenting user's OpenAlex account/budget. No authenticated end-to-end check was performed. | Strong candidate when open-source implementation and first-party hosting both matter. It requires user sign-in, not local server installation. |

Remote file handling also needs care: Paper Search download tools return paths
on the server, not files on the user's machine. Its supported `read_*` tools
return extracted text instead. A local-server configuration cannot simply be
relabelled as remote while assuming identical file access.

Smithery documents a separate authenticated Connect flow. For registry servers,
create a connection with `server: "openags/paper-search-mcp"`, rather than
hard-coding its deployment URL. The resulting endpoint belongs to a user's
namespace/connection; it is not one anonymous URL for every Plugin user. This
route remains untested without Smithery authorization. A connection in mock mode
does not test the real upstream server. [Connect guide](https://smithery.ai/docs/use/connect),
[connection API](https://smithery.ai/docs/api-reference/connect/create-or-update-connection)

**Selection guidance, not an adopted dependency:** prefer Asta for the smallest
currently demonstrated remote setup; prefer official OpenAlex if an open-source
server is required and one-time OAuth is acceptable. Retain Paper Search as an
optional multi-source connector. None guarantees access to every paper's full
text; discovery and snippets do not replace reading the cited source.

OpenAlex's README contains stale claims about anonymous access and all tools
being read-only. The pinned source requires an account and also registers
profile-curation tools. A literature integration should use only the required
retrieval capabilities, not authorize account/profile changes. Source inspection
does not establish which revision is deployed. [Auth implementation](https://github.com/ourresearch/openalex-mcp-server/blob/aab76e65ba44a57e9dd3023a737df61d737c126a/src/index.ts),
[tool registration](https://github.com/ourresearch/openalex-mcp-server/blob/aab76e65ba44a57e9dd3023a737df61d737c126a/src/server.ts)

The Asta check was a direct MCP call, not a test through an installed Plugin.

## 6. Testing whether the Plugin helps

Test **activation** separately from **task quality**. Cover direct and indirect requests, incomplete inputs, requests that should not activate the skill, and edge cases. [OpenAI skill testing](https://developers.openai.com/plugins/build/skills#test-the-skill)

Possible applications to Queue Agent, not an adopted test plan:

1. **Behavior:** discussion-only requests should not launch experiments; modeling and evaluation requests should locate relevant guidance and tools.
2. **Computation:** check simulations, policy feasibility, and metrics on small known cases, separately from language quality.
3. **Compatibility:** try the same small task in both hosts, checking dependencies, paths, and outputs.
4. **Contributions:** include sources, scope, dependencies, and a minimal example; rerun relevant checks after changes.

Keep the main skill concise and load detailed references as needed. [Progressive disclosure](https://agentskills.io/specification#progressive-disclosure)

Claude's official eval tool supplies a with/without-Plugin comparison by default. Its default MCP mocks do not replace end-to-end tests of real computational tools. [Plugin evals](https://code.claude.com/docs/en/plugin-evals)

## 7. Open design questions

- Which computations need local scripts, and which benefit from MCP?
- Which remote literature service, if any, should the package configure?
  Section 5 compares the current options.
- How should task quality be compared with and without the Plugin? Section 6
  lists possible checks.

## Source notes

External sources in this file were consulted between 2026-09-25 and 2026-10-24.
Official documentation and upstream files take precedence over search snippets
and generated summaries. Pinned links identify the revisions reviewed; unpinned
pages may have changed since. Section 3 summarizes host documentation; it does
not test every behavior that it describes.
