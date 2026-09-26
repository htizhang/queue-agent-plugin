"""Structural checks for the queue-literature knowledge notes."""

import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED_NOTE_FILENAMES = {
    "knowledge-foundations.md",
    "modeling-call-center-primitives.md",
    "modeling-censoring-truncation.md",
    "modeling-event-log-semantics.md",
    "modeling-fitted-distribution-tests.md",
    "modeling-log-identifiability.md",
    "modeling-model-adequacy-validation.md",
    "modeling-partial-event-logs.md",
    "modeling-state-and-dynamics.md",
    "modeling-system-description-primitives.md",
    "modeling-time-varying-arrivals.md",
    "policy-backfilling.md",
    "policy-c-mu.md",
    "policy-evaluation-paired-crn.md",
    "policy-generalized-c-mu.md",
    "policy-gittins.md",
    "policy-load-balancing.md",
    "policy-maximum-pressure.md",
    "policy-reentrant-stage-priority.md",
    "policy-reentrant-wipload-release.md",
    "policy-srpt.md",
}
FIXTURE_NOTE_NAME = "modeling-fixture.md"
FIXTURE_NOTE_FILENAMES = {FIXTURE_NOTE_NAME}
AUDIT_NOTE_FIELDS = {
    "ID",
    "Kind",
    "Stage relevance",
    "Aliases",
    "Sources",
    "Review",
    "Reviewed on",
    "Legacy origin",
}
REQUIRED_SOURCE_FIELDS = {
    "id",
    "title",
    "authors",
    "year",
    "url",
    "doi",
    "locators",
}
OPTIONAL_SOURCE_FIELDS = {"version"}
AUDIT_SOURCE_FIELDS = {"reading_depth", "reviewed_on", "legacy_keys", "note"}
NOTE_FILENAME = re.compile(r"(?:knowledge|modeling|policy)-.+\.md")
TITLE = re.compile(r"\A#\s+\S[^\n]*\r?\n")
SUBHEADING = re.compile(r"^#{2,6}\s+.*$", re.M)
AUDIT_NOTE_ROW = re.compile(
    rf"^\|\s*(?:{'|'.join(re.escape(field) for field in AUDIT_NOTE_FIELDS)})\s*\|",
    re.M,
)
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
SOURCE_LINK = re.compile(r"\[([^\]\n]+)\]\(sources\.json\)")
PROSE_WORD = re.compile(r"[A-Za-z][A-Za-z'-]+")


def local_links(path, repo_root):
    targets = []
    for raw in LINK.findall(path.read_text(encoding="utf-8")):
        destination = raw.strip()
        if destination.startswith("<"):
            destination = destination[1 : destination.find(">")]
        else:
            destination = destination.split(maxsplit=1)[0]
        if not destination or destination.startswith(("#", "//")):
            continue
        parsed = urlsplit(destination)
        if parsed.scheme:
            if parsed.scheme == "file":
                raise ValueError(f"{path.name}: link escapes repository: {raw}")
            continue
        target = (path.parent / unquote(parsed.path)).resolve()
        try:
            target.relative_to(repo_root.resolve())
        except ValueError:
            raise ValueError(f"{path.name}: link escapes repository: {raw}")
        targets.append((raw, target))
    return targets


def source(source_id="source.one", doi="10.1000/example", **changes):
    record = {
        "id": source_id,
        "title": "Fixture source",
        "authors": ["A. Author"],
        "year": 2020,
        "url": "https://example.test/paper",
        "doi": doi,
        "locators": ["Section 1"],
    }
    record.update(changes)
    return record


def note(source_ids=("source.one",), extra=""):
    citations = " ".join(f"[{item}](sources.json)" for item in source_ids)
    return f"""# Fixture Note

## Mechanism

Fixture mechanism.

## Evidence

Fixture claim {citations}. {extra}

## Use in this Plugin

Fixture use.
"""


def write_fixture(root, notes=None, sources=None, skill_links=None):
    notes = {FIXTURE_NOTE_NAME: note()} if notes is None else notes
    sources = [source()] if sources is None else sources
    references = root / "skills" / "queue-literature" / "references"
    references.mkdir(parents=True)
    for name, text in notes.items():
        (references / name).write_text(text, encoding="utf-8")
    (references / "sources.json").write_text(
        json.dumps({"sources": sources}), encoding="utf-8"
    )
    if skill_links is None:
        skill_links = [f"references/{name}" for name in notes]
    links = "\n".join(f"- [note]({item})" for item in skill_links)
    (root / "skills" / "queue-literature" / "SKILL.md").write_text(
        f"# Queue Literature\n\n{links}\n", encoding="utf-8"
    )


class KnowledgeTests(unittest.TestCase):
    def assert_knowledge(
        self,
        repo_root,
        expected_note_filenames=EXPECTED_NOTE_FILENAMES,
    ):
        repo_root = repo_root.resolve()
        skill = repo_root / "skills" / "queue-literature" / "SKILL.md"
        references = skill.parent / "references"
        note_paths = sorted(
            path
            for path in references.glob("*.md")
            if NOTE_FILENAME.fullmatch(path.name)
        )
        note_names = {path.name for path in note_paths}
        missing = sorted(expected_note_filenames - note_names)
        self.assertFalse(missing, f"missing expected notes: {', '.join(missing)}")
        self.assertTrue(note_paths, "no knowledge notes discovered")

        notes = []
        cited_source_ids = set()
        for path in note_paths:
            text = path.read_text(encoding="utf-8")
            title = TITLE.match(text)
            self.assertIsNotNone(title, f"{path.name}: missing plain-note title")
            body = text[title.end() :].strip() if title else ""
            prose = SUBHEADING.sub("", body)
            prose = SOURCE_LINK.sub("", prose)
            self.assertGreaterEqual(
                len(PROSE_WORD.findall(prose)),
                5,
                f"{path.name}: missing substantive body",
            )
            audit_fields = AUDIT_NOTE_ROW.findall(text)
            self.assertFalse(
                audit_fields,
                f"{path.name}: audit fields are not part of a plain knowledge note",
            )
            cited = set(SOURCE_LINK.findall(text))
            self.assertTrue(cited, f"{path.name}: missing bibliography citation")
            cited_source_ids.update(cited)
            notes.append((path, cited))

        payload = json.loads((references / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual({"sources"}, set(payload), "sources.json: bad top-level shape")
        records = payload["sources"]
        self.assertIsInstance(records, list, "sources.json: sources must be a list")
        self.assertTrue(
            all(isinstance(record, dict) for record in records),
            "sources.json: source records must be objects",
        )
        source_ids = [record.get("id") for record in records]
        self.assertTrue(all(isinstance(item, str) and item for item in source_ids))
        self.assertEqual(
            len(source_ids), len(set(source_ids)), f"duplicate source IDs: {source_ids}"
        )

        dois = []
        for record in records:
            fields = set(record)
            missing_fields = sorted(REQUIRED_SOURCE_FIELDS - fields)
            self.assertFalse(
                missing_fields,
                f"{record.get('id')}: missing source fields: {missing_fields}",
            )
            audit_fields = sorted(AUDIT_SOURCE_FIELDS & fields)
            self.assertFalse(
                audit_fields,
                f"{record['id']}: audit source fields: {audit_fields}",
            )
            unsupported = sorted(
                fields - REQUIRED_SOURCE_FIELDS - OPTIONAL_SOURCE_FIELDS
            )
            self.assertFalse(
                unsupported,
                f"{record['id']}: unsupported source fields: {unsupported}",
            )
            self.assertIsInstance(record["title"], str)
            self.assertTrue(record["title"])
            self.assertTrue(
                isinstance(record["authors"], list)
                and record["authors"]
                and all(
                    isinstance(author, str) and author for author in record["authors"]
                ),
                f"{record['id']}: bad authors",
            )
            if record["year"] is not None:
                self.assertIsInstance(record["year"], int)
            self.assertIsInstance(record["url"], str)
            self.assertTrue(record["url"])
            locators = record["locators"]
            self.assertTrue(
                isinstance(locators, list)
                and locators
                and all(isinstance(item, str) and item for item in locators),
                f"{record['id']}: missing locators",
            )
            if "version" in record:
                self.assertTrue(
                    isinstance(record["version"], str) and record["version"],
                    f"{record['id']}: empty version qualifier",
                )
            if record["doi"] is not None:
                self.assertTrue(
                    isinstance(record["doi"], str) and record["doi"],
                    f"{record['id']}: bad DOI",
                )
                doi = re.sub(r"^doi:\s*", "", record["doi"].strip().lower())
                dois.append(
                    re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi).rstrip("/")
                )
        self.assertEqual(len(dois), len(set(dois)), f"duplicate DOIs: {dois}")
        registry_ids = set(source_ids)

        for path, cited in notes:
            for source_id in cited:
                self.assertIn(
                    source_id, registry_ids, f"{path.name}: unknown source {source_id}"
                )
        uncited = sorted(registry_ids - cited_source_ids)
        self.assertFalse(
            uncited, f"sources.json: uncited sources: {', '.join(uncited)}"
        )

        documents = [skill] + [path for path, _ in notes]
        skill_targets = set()
        for document in documents:
            try:
                links = local_links(document, repo_root)
            except ValueError as error:
                self.fail(str(error))
            for raw, target in links:
                self.assertTrue(target.exists(), f"{document.name}: broken link {raw}")
            if document == skill:
                skill_targets = {target for _, target in links}
        for path, _ in notes:
            self.assertIn(
                path.resolve(), skill_targets, f"topic map does not link {path.name}"
            )

    def assert_bad(
        self,
        pattern,
        *,
        expected_note_filenames=FIXTURE_NOTE_FILENAMES,
        **fixture,
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            write_fixture(root, **fixture)
            with self.assertRaisesRegex(AssertionError, pattern):
                self.assert_knowledge(
                    root,
                    expected_note_filenames=expected_note_filenames,
                )

    def test_valid_fixtures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            write_fixture(root)
            self.assert_knowledge(
                root,
                expected_note_filenames=FIXTURE_NOTE_FILENAMES,
            )

    def test_undated_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            write_fixture(root, sources=[source(year=None)])
            self.assert_knowledge(root, expected_note_filenames=FIXTURE_NOTE_FILENAMES)

    def test_duplicate_source_ids_and_dois(self):
        self.assert_bad(
            "duplicate source IDs",
            sources=[source(), source(doi="10.1000/other")],
        )
        self.assert_bad(
            "duplicate DOIs",
            sources=[
                source("source.one", "10.1000/shared"),
                source("source.two", "https://doi.org/10.1000/SHARED"),
            ],
        )

    def test_plain_notes_reject_audit_metadata(self):
        audit_table = """| Field | Value |
| --- | --- |
| Review | source-checked |"""
        self.assert_bad(
            "audit fields",
            notes={
                FIXTURE_NOTE_NAME: note().replace(
                    "## Mechanism", f"{audit_table}\n\n## Mechanism"
                )
            },
        )
        self.assert_bad(
            "audit source fields",
            sources=[source(reviewed_on="2026-09-25")],
        )

    def test_newly_discovered_notes_are_validated(self):
        self.assert_bad(
            "unknown source",
            notes={
                FIXTURE_NOTE_NAME: note(),
                "policy-new.md": note(source_ids=("missing",)),
            },
        )
        self.assert_bad(
            "topic map does not link modeling-new.md",
            notes={
                FIXTURE_NOTE_NAME: note(),
                "modeling-new.md": note(),
            },
            skill_links=[f"references/{FIXTURE_NOTE_NAME}"],
        )

    def test_content_and_link_regressions(self):
        self.assert_bad(
            "unknown source",
            notes={FIXTURE_NOTE_NAME: note(source_ids=("missing",))},
        )
        self.assert_bad(
            "missing bibliography citation",
            notes={
                FIXTURE_NOTE_NAME: note().replace(
                    "[source.one](sources.json)", "source.one"
                )
            },
        )
        self.assert_bad(
            "missing plain-note title",
            notes={FIXTURE_NOTE_NAME: note().replace("# Fixture Note", "Fixture Note")},
        )
        self.assert_bad(
            "missing substantive body",
            notes={
                FIXTURE_NOTE_NAME: "# Empty Note\n\n[source.one](sources.json)\n",
            },
        )
        self.assert_bad("missing locators", sources=[source(locators=[])])
        self.assert_bad(
            "uncited sources",
            sources=[
                source(),
                source("source.two", "10.1000/other"),
            ],
        )
        self.assert_bad(
            "broken link",
            notes={FIXTURE_NOTE_NAME: note(extra="[x](missing.md)")},
        )
        self.assert_bad(
            "escapes repository",
            notes={FIXTURE_NOTE_NAME: note(extra="[x](../../../../outside.md)")},
        )
        self.assert_bad("topic map does not link", skill_links=[])
        self.assert_bad(
            "missing expected notes",
            expected_note_filenames=EXPECTED_NOTE_FILENAMES,
        )

    def test_repository(self):
        self.assert_knowledge(Path(__file__).resolve().parents[2])
