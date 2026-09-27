# Queue Agent Plugin: References and Design Decisions

Last updated: 2026-09-26. Confirmed decisions, external references, and open
questions are kept separate. Upstream examples are not automatically our
implementation plan.

## 1. Confirmed decisions

### Repository and development

- Develop incrementally in the standalone, private [queue-agent-plugin repository](https://github.com/htizhang/queue-agent-plugin).
- Use English for all repository content.
- Discuss one workflow step at a time. Once confirmed, record it here and implement the agreed scope.
- The repository contains the overview, references, and skill source files, not an installable Plugin. No legacy runtime implementation or experiment data is included.

### Two-Stage overview

Users interact with their own coding agent, with Claude Code and Codex as the intended hosts:

- **Stage 1 — Queue modeling:** deliver a documented queue model and its corresponding executable simulator from data and a system description, with replaceable policies and checks that the implementation matches the model.
- **Stage 2 — Policy design:** design, evaluate, and improve queue policies for a model or model family.

The Plugin first gives the agent this task map: **data → queue model → policy**. The user's current task determines where to start; not every request must run both Stages.

Research direction remains with the user and host agent. The Plugin supplies reusable domain knowledge, methods, tools, and cases rather than a separate, fixed agent framework. The queueing community can contribute additional capabilities and knowledge.

### Overall entry and task routing

- Implement [queue-agent](../skills/queue-agent/SKILL.md) as the overall entry
  skill. Select the current task from the latest request and available artifacts,
  rather than storing one Stage for the whole session.
- A usable model, simulator, or specified model family can start directly at
  Stage 2. Building its evaluator does not itself require Stage 1 inference from
  historical data. Requests to assess or revise model-data agreement use Stage 1.
- Literature questions and discussion are valid standalone tasks; the overview
  does not automatically start implementation or experiments.
- Add a short SessionStart orientation that points to the entry skill. Keep
  detailed guidance in skills, with no fixed workflow engine or persistent Stage
  state. This is source content only: packaging, installation, and host hook
  approval remain separate.

### Stage 1 modeling capability

- Implement [queue-modeling](../skills/queue-modeling/SKILL.md) as guidance for
  building, calibrating, and validating a queue model and its corresponding
  executable simulator from data and a system description.
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
- Reuse the existing queue-literature skill and its local knowledge. Keep runtime
  instructions focused on the modeling task and useful resources.
- Add skill source content and behavioral checks; host packaging and installation
  remain separate steps.

### Shared literature capability

- Implement [queue-literature](../skills/queue-literature/SKILL.md) as one shared skill for both Stages, not a separate literature agent.
- Adapt the useful search, synthesis, and citation guidance from existing open-source skills; preserve upstream attribution and licensing. Add queue-specific guidance about model assumptions, observations, policies, objectives, baseline applicability, and theoretical results.
- Use the host's available search and reading tools. Paper Search MCP is an optional candidate when academic retrieval is missing; Zotero is optional for an existing library. These are not fixed dependencies.
- Scale the work to the question; do not require figures, a complete report, a fixed backend, or running both Stages.
- This step adds source files only. Do not install the skill or alter local agent/MCP configuration. Existing CC and Kiro sessions may be used for temporary behavioral tests without installing the Plugin.

Implementation sources, adaptation details, and the upstream MIT notice are recorded in the skill's [attribution](../skills/queue-literature/NOTICE.md). See [optional tool references](../skills/queue-literature/references/tool-options.md) and [test scenarios](../tests/queue-literature/scenarios.md).

### Knowledge reuse: current scope

- Migrate a small, source-checked slice of the earlier knowledge base under the
  existing `queue-literature` skill, shared by Stage 1 and Stage 2.
- Store scientific content as focused Markdown handbook notes, with a short topic
  map and one JSON source registry. JSON keeps integrity checks dependency-free;
  there is no duplicate YAML copy of the notes.
- Use ordinary host file reading and keyword search. Do not introduce a vector
  knowledge base, embeddings, or a new retrieval service.
- Keep Stage and topic discovery in the skill's topic map. Notes use handbook
  prose for assumptions, results, limitations, and citations rather than
  per-note IDs, aliases, review status, dates, or migration origin.
- Keep stable note paths and source IDs. Limit runtime source records to
  bibliographic identity, useful claim locators, and a concise version qualifier
  when citation identity requires it. Preserve scientifically meaningful
  unverified or secondhand scope in the note prose.
- Rewrite overbroad claims rather than treating old confidence labels as
  verification. Do not import the old runtime, experiments, or agent framework.
- Do not install the Plugin or change local agent/MCP configuration. Use existing
  local CC and codex-x for source-loaded checks and independent review.

See [migration and provenance](knowledge-base-migration.md) for the implemented
slice, legacy audit findings, and deferred material. Host packaging remains a
separate step.

The user also approved knowledge construction through multiple local CC research
leads using `research` and `research-deep`, with parent interaction, external
source supplementation, and codex-x review when available. These are development
tools, not required dependencies of the delivered skill. See the
[first expansion](knowledge-base-expansion.md) for the prepared additions and
remaining verification scope.

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

The source command accepts `CLAUDE_PLUGIN_ROOT` or `PLUGIN_ROOT`, quotes the
resolved path, and requires `python3`. Claude documents the former; Codex
documents its own root variable and the Claude-compatible alias. This checks a
portable source path, not automatic activation: packaging, platform support, and
hook trust still need host-level verification.
[Claude Plugin reference](https://code.claude.com/docs/en/plugins-reference),
[OpenAI Plugin packaging](https://developers.openai.com/plugins/build/plugins)

## 4. Creation, testing, and distribution references

These commands are references for future implementation; they have not been used to create or install this Plugin.

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

Upstream HEADs at review: K-Dense `49c6e97775ea`, Hugging Face `80f9fa530e46`, Knowledge Work Plugins `da38ec1ee89d`, AutoResearchClaw `be4ba4755bf1`. AutoResearchClaw's [host-facing skill](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/.claude/skills/researchclaw/SKILL.md) invokes a separate runtime: a skill entry point does not itself imply a Plugin-centered architecture.

## 6. Testing whether the Plugin helps

Test **activation** separately from **task quality**. Cover direct and indirect requests, incomplete inputs, requests that should not activate the skill, and edge cases. [OpenAI skill testing](https://developers.openai.com/plugins/build/skills#test-the-skill)

Possible applications to Queue Agent, not yet an agreed test plan:

1. **Behavior:** discussion-only requests should not launch experiments; modeling and evaluation requests should locate relevant guidance and tools.
2. **Computation:** check simulations, policy feasibility, and metrics on small known cases, separately from language quality.
3. **Compatibility:** try the same small task in both hosts, checking dependencies, paths, and outputs.
4. **Contributions:** include sources, scope, dependencies, and a minimal example; rerun relevant checks after changes.

Keep the main skill concise and load detailed references as needed. [Progressive disclosure](https://agentskills.io/specification#progressive-disclosure)

Claude's official eval tool supplies a with/without-Plugin comparison by default. Its default MCP mocks do not replace end-to-end tests of real computational tools. [Plugin evals](https://code.claude.com/docs/en/plugin-evals)

## 7. Open design questions

- Validate both hosts initially, or start with one while preserving the other's adaptation boundary?
- Which capabilities should be independently callable in each Stage, and what model and evidence should pass between them?
- Which computations need local scripts, and which benefit from MCP?
- Should community contributions be skills, model-family cases, tools, or a combination?

We will discuss these individually. Shared content with host-specific adaptation is a supported direction, not a finalized layout, skill catalog, or execution workflow.

## Review scope

The review combined Exa search, Firecrawl and official-document retrieval, and Context7 cross-checks. Three local agents covered Claude documentation, cross-host standards, and upstream examples; two Firecrawl Pro tasks covered interoperability and testing/maintenance. Their completed results were reconciled against primary sources.

Official documentation and upstream files take precedence over snippets and generated suggestions. Compatibility findings are documentation-based, not installation tests. Unpinned links may change after the review date.
