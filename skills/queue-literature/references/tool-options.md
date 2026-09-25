# Reusable Literature Tools

These are optional routes, not dependencies or an installation checklist.
Use the user's available tools and authorized access. Inspect their current
interfaces rather than assuming a particular command or MCP tool name.

| Need | Reusable option | Scope |
| --- | --- | --- |
| Discovery and reading | Existing host web search, browser, paper reader, or configured services such as Exa or Firecrawl | Search and fetch primary sources using what is already available. Supplied PDFs can be read locally. |
| Academic discovery | [Paper Search MCP](https://github.com/openags/paper-search-mcp) (MIT) | MCP or CLI/skill access to sources including arXiv, Semantic Scholar, OpenAlex, and Crossref; available full text depends on the source. |
| Citation utilities | [K-Dense citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/49c6e97775eaa18ba791bebe23162a70ae601c18/skills/citation-management/SKILL.md) (MIT) | Metadata lookup, DOI-to-BibTeX conversion, deduplication, and citation checks, if these utilities are already available. They are not bundled here. |
| An existing paper collection | [Zotero MCP](https://github.com/54yyyu/zotero-mcp) (MIT) | Read/search an authorized personal or team library and its annotations. Optional; a literature task does not require Zotero. |

Metadata services help find and identify papers; a metadata result is not evidence
that the full paper was read. Prefer publisher, author, institutional repository,
or open-access copies. If full text cannot be retrieved, identify that limit
rather than inferring detailed methods or proofs from a search snippet.

Open-source licensing of a connector does not make every backing service free or
credential-free. Keep installation, authentication, account changes, library
mutations, and uploads outside the literature task unless separately authorized.
If tools are missing, explain the missing capability and offer an optional setup
route; do not silently install a backend.

Tool capabilities were reviewed on 2026-09-25 from the linked upstream sources.
These projects are references only: none is vendored or configured by this skill.
