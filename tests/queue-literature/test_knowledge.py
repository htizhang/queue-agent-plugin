"""Structural checks for the queue-literature knowledge notes."""

import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED_NOTES = {
    "knowledge-foundations.md": (
        ("Mechanism", "Applicability", "Evidence", "Use in this Plugin"),
        frozenset(
            {
                "scully_harchol_balter_2021_gittins",
                "van_mieghem_1995_gc_mu",
            }
        ),
    ),
    "modeling-call-center-primitives.md": (
        ("Method and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"brown_et_al_2005_call_center"}),
    ),
    "modeling-fitted-distribution-tests.md": (
        ("Method and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"babu_rao_2004_fitted_gof"}),
    ),
    "modeling-partial-event-logs.md": (
        ("Method and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"sutton_jordan_2011_queue_inference"}),
    ),
    "policy-backfilling.md": (
        ("Mechanism and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"mualem_feitelson_2001_backfilling"}),
    ),
    "policy-c-mu.md": (
        ("Mechanism", "Applicability", "Evidence", "Use in this Plugin"),
        frozenset({"scully_harchol_balter_2021_gittins"}),
    ),
    "policy-generalized-c-mu.md": (
        ("Mechanism", "Applicability", "Evidence", "Use in this Plugin"),
        frozenset({"van_mieghem_1995_gc_mu"}),
    ),
    "policy-gittins.md": (
        ("Mechanism", "Applicability", "Evidence", "Use in this Plugin"),
        frozenset({"scully_harchol_balter_2021_gittins"}),
    ),
    "policy-maximum-pressure.md": (
        ("Mechanism and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"dai_lin_2005_maximum_pressure"}),
    ),
    "policy-reentrant-stage-priority.md": (
        ("Mechanism and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"dai_weiss_1996_reentrant_stability"}),
    ),
    "policy-reentrant-wipload-release.md": (
        ("Mechanism and applicability", "Evidence", "Use in this Plugin"),
        frozenset({"qi_et_al_2007_wipload_release"}),
    ),
    "policy-srpt.md": (
        ("Mechanism", "Applicability", "Evidence", "Use in this Plugin"),
        frozenset({"scully_harchol_balter_2021_gittins"}),
    ),
}
FIXTURE_SECTIONS = ("Mechanism", "Evidence", "Use in this Plugin")
FIXTURE_NOTES = {
    "note.md": (FIXTURE_SECTIONS, frozenset({"source.one"})),
}
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
AUDIT_NOTE_ROW = re.compile(
    rf"^\|\s*(?:{'|'.join(re.escape(field) for field in AUDIT_NOTE_FIELDS)})\s*\|",
    re.M,
)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.M)
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
SOURCE_LINK = re.compile(r"\[([^\]\n]+)\]\(sources\.json\)")


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
    notes = {"note.md": note()} if notes is None else notes
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
    def assert_knowledge(self, repo_root, expected_notes=EXPECTED_NOTES):
        repo_root = repo_root.resolve()
        skill = repo_root / "skills" / "queue-literature" / "SKILL.md"
        references = skill.parent / "references"
        missing = sorted(
            name for name in expected_notes if not (references / name).is_file()
        )
        self.assertFalse(missing, f"missing expected notes: {', '.join(missing)}")

        notes = {}
        expected_source_ids = set()
        for name, (expected_sections, expected_sources) in expected_notes.items():
            path = references / name
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, r"\A#\s+\S", f"{name}: missing title")
            audit_fields = AUDIT_NOTE_ROW.findall(text)
            self.assertFalse(
                audit_fields,
                f"{name}: audit fields are not part of a plain knowledge note",
            )
            sections = tuple(HEADING.findall(text))
            self.assertEqual(
                expected_sections,
                sections,
                f"{name}: changed scientific sections",
            )
            cited = frozenset(SOURCE_LINK.findall(text))
            missing_citations = sorted(expected_sources - cited)
            self.assertFalse(
                missing_citations,
                f"{name}: missing citations: {', '.join(missing_citations)}",
            )
            unexpected_citations = sorted(cited - expected_sources)
            self.assertFalse(
                unexpected_citations,
                (
                    f"{name}: changed citation targets: "
                    f"{', '.join(unexpected_citations)}"
                ),
            )
            notes[name] = (path, text, cited)
            expected_source_ids.update(expected_sources)

        payload = json.loads((references / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual({"sources"}, set(payload), "sources.json: bad top-level shape")
        records = payload["sources"]
        self.assertIsInstance(records, list, "sources.json: sources must be a list")
        source_ids = [record.get("id") for record in records]
        self.assertTrue(all(isinstance(item, str) and item for item in source_ids))
        self.assertEqual(
            len(source_ids), len(set(source_ids)), f"duplicate source IDs: {source_ids}"
        )

        dois = []
        for record in records:
            self.assertIsInstance(record, dict, f"bad source: {record}")
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
                self.assertIsInstance(record["doi"], str)
                doi = re.sub(r"^doi:\s*", "", record["doi"].strip().lower())
                dois.append(
                    re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi).rstrip("/")
                )
        self.assertEqual(len(dois), len(set(dois)), f"duplicate DOIs: {dois}")
        registry_ids = set(source_ids)

        for path, _, cited in notes.values():
            for source_id in cited:
                self.assertIn(
                    source_id, registry_ids, f"{path.name}: unknown source {source_id}"
                )
        self.assertEqual(
            expected_source_ids,
            registry_ids,
            "sources.json: changed source IDs",
        )

        documents = [skill] + [item[0] for item in notes.values()]
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
        for path, _, _ in notes.values():
            self.assertIn(
                path.resolve(), skill_targets, f"topic map does not link {path.name}"
            )

    def assert_bad(
        self,
        pattern,
        *,
        expected_notes=FIXTURE_NOTES,
        **fixture,
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            write_fixture(root, **fixture)
            with self.assertRaisesRegex(AssertionError, pattern):
                self.assert_knowledge(
                    root,
                    expected_notes=expected_notes,
                )

    def test_valid_fixtures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            write_fixture(root)
            self.assert_knowledge(
                root,
                expected_notes=FIXTURE_NOTES,
            )

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
                "note.md": note().replace(
                    "## Mechanism", f"{audit_table}\n\n## Mechanism"
                )
            },
        )
        self.assert_bad(
            "audit source fields",
            sources=[source(reviewed_on="2026-09-25")],
        )

    def test_content_and_link_regressions(self):
        self.assert_bad(
            "unknown source",
            notes={"note.md": note(source_ids=("missing",))},
            expected_notes={
                "note.md": (FIXTURE_SECTIONS, frozenset({"missing"})),
            },
        )
        self.assert_bad(
            "missing citations",
            notes={
                "note.md": note().replace("[source.one](sources.json)", "source.one")
            },
        )
        self.assert_bad(
            "changed scientific sections",
            notes={"note.md": note().replace("## Evidence", "## Support")},
        )
        self.assert_bad("missing locators", sources=[source(locators=[])])
        self.assert_bad("broken link", notes={"note.md": note(extra="[x](missing.md)")})
        self.assert_bad(
            "escapes repository",
            notes={"note.md": note(extra="[x](../../../../outside.md)")},
        )
        self.assert_bad("topic map does not link", skill_links=[])
        self.assert_bad("missing expected notes", expected_notes=EXPECTED_NOTES)

    def test_repository(self):
        self.assert_knowledge(Path(__file__).resolve().parents[2])
