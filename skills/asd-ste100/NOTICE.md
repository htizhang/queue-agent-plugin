# Upstream source and local adaptations

This skill incorporates [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill),
version 0.4.0, at commit
[`c7b11cd9258708909d8574c8176d4c70969c8b29`](https://github.com/danyuchn/asd-ste100-skill/tree/c7b11cd9258708909d8574c8176d4c70969c8b29).
Imported on 2026-10-24. The upstream MIT license and copyright notice are
preserved in [LICENSE](LICENSE).

## Included files

- `SKILL.md`: upstream instructions, with the local changes listed below.
- `references/writing-rules.md`: upstream rule summary, with the short quotation
  of Rule 8.1 replaced by a paraphrase.
- `examples/before-after.md`: unchanged upstream illustrations.
- `examples/linter-edge-cases.md`: unchanged upstream linter fixture.
- `scripts/ste-lint.py`: dependency-free linter and its self-tests, with two
  explicit non-null checks for static type analysis.
- `LICENSE`: unchanged upstream license.

The upstream README and standalone Plugin/marketplace manifests are omitted.
This copy is a skill within Queue Agent, not a nested Plugin or a global install.

## Local changes

The skill description adds queue model explanations, policy explanations, and
reports as activation cases. The new **Use in Queue Agent** section defaults
these deliverables to STE-flavored writing. It preserves scientific meaning,
technical distinctions, the requested language, and artifact format. It also
requires checked examples and a source-to-rewrite comparison. Other upstream
instructions are unchanged except that **Source and Scope** replaces the quoted
ASD copyright passage with a short distinction between the skill's MIT license
and the official standard. No standard or controlled dictionary is bundled.
The upstream version field is stored as
`metadata.upstream-version` for portable skill frontmatter validation.

The linter makes two existing invariants explicit: a matched list conjunction
has a line index, and a recognized blockquote has a prefix match. These checks
allow local type analysis without changing the lint rules or CLI interface.

The Plugin entry skill and both Stage delivery steps point here. There is no new
hook, runtime dependency, or automatic rewrite of every response. Behavioral
review cases and source checks are in [tests/asd-ste100](../../tests/asd-ste100/scenarios.md).

This is a third-party adaptation, not the official ASD standard or a certified
compliance checker. The upstream repository does not include the official
controlled dictionary. A clean linter result does not establish meaning
preservation, scientific correctness, or reader comprehension.
