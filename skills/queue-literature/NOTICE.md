# Upstream Attribution

The general literature-search, synthesis, and citation guidance in this skill is
adapted from these K-Dense Scientific Agent Skills at commit
`49c6e97775eaa18ba791bebe23162a70ae601c18`:

- [literature-review, version 1.8](https://github.com/K-Dense-AI/scientific-agent-skills/blob/49c6e97775eaa18ba791bebe23162a70ae601c18/skills/literature-review/SKILL.md)
- [citation-management, version 2.1](https://github.com/K-Dense-AI/scientific-agent-skills/blob/49c6e97775eaa18ba791bebe23162a70ae601c18/skills/citation-management/SKILL.md)

Both skills declare MIT licensing. The upstream
[license](https://github.com/K-Dense-AI/scientific-agent-skills/blob/49c6e97775eaa18ba791bebe23162a70ae601c18/LICENSE.md)
is reproduced below for the adapted material; this notice does not assign a
license to the rest of the repository.

## Adaptation

Retained: question-led search, source checking, synthesis across papers, citation
identity checks, and search provenance when needed.

Changed: added queue-specific model, observation, control, and baseline guidance;
made the depth depend on the user's question; removed mandatory figures, fixed
database counts, backend-specific commands, and a compulsory report pipeline.
No upstream scripts, model services, or additional skills are bundled or required.

## Local knowledge

The bundled knowledge notes are original, source-grounded summaries. They do not
copy textbook or paper text. Original scientific sources and version-specific
locators are listed in [the source registry](references/sources.json). The MIT
notice below covers the adapted K-Dense guidance, not the cited papers or the
rest of this repository.

## Upstream MIT License

Copyright (c) 2025 K-Dense Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
