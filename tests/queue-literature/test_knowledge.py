"""Small structural checks for the queue-literature knowledge cards."""

import datetime
import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


EXPECTED_CARDS = {
    "knowledge-foundations.md": "foundations.model-policy-fit",
    "policy-c-mu.md": "policy.c_mu_linear_priority",
    "policy-generalized-c-mu.md": "policy.generalized_c_mu_age_delay",
    "policy-gittins.md": "policy.gittins_unknown_size",
    "policy-srpt.md": "policy.srpt_size_based",
    "modeling-partial-event-logs.md": "modeling.partial_event_logs",
    "modeling-call-center-primitives.md": "modeling.call_center_primitives",
    "policy-maximum-pressure.md": "policy.maximum_pressure_network",
    "policy-backfilling.md": "policy.easy_conservative_backfilling",
}
CARD_FIELDS = {
    "ID",
    "Kind",
    "Stage relevance",
    "Aliases",
    "Sources",
    "Review",
    "Reviewed on",
    "Legacy origin",
}
SOURCE_FIELDS = {
    "id",
    "title",
    "authors",
    "year",
    "url",
    "doi",
    "reading_depth",
    "locators",
    "reviewed_on",
    "legacy_keys",
    "note",
}
DEPTHS = {"relevant-full-text", "abstract-only", "metadata-only"}
ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$")
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
SOURCE_LINK = re.compile(r"\[([^\]\n]+)\]\(sources\.json\)")


def card_fields(text):
    rows = []
    for line in text.split("\n## ", 1)[0].splitlines():
        match = ROW.match(line)
        if match and match.group(1) not in {"Field", "---"}:
            rows.append((match.group(1).strip(), match.group(2).strip()))
    return rows, dict(rows)


def valid_date(value):
    try:
        return datetime.date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


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
        "reading_depth": "relevant-full-text",
        "locators": ["Section 1"],
        "reviewed_on": "2026-09-25",
        "legacy_keys": ["legacy.source"],
        "note": "Inspected fixture version 1.",
    }
    record.update(changes)
    return record


def card(card_id="policy.test", source_ids=("source.one",), extra=""):
    citations = " ".join(f"[{item}](sources.json)" for item in source_ids)
    return f"""# Fixture Card

| Field | Value |
| --- | --- |
| ID | {card_id} |
| Kind | policy |
| Stage relevance | Stage 1, Stage 2 |
| Aliases | fixture |
| Sources | {", ".join(source_ids)} |
| Review | source-checked |
| Reviewed on | 2026-09-25 |
| Legacy origin | synthetic fixture |

## Evidence

Fixture claim {citations}. {extra}
"""


def write_fixture(root, cards=None, sources=None, skill_links=None):
    cards = {"card.md": card()} if cards is None else cards
    sources = [source()] if sources is None else sources
    references = root / "skills" / "queue-literature" / "references"
    references.mkdir(parents=True)
    for name, text in cards.items():
        (references / name).write_text(text, encoding="utf-8")
    (references / "sources.json").write_text(
        json.dumps({"sources": sources}), encoding="utf-8"
    )
    if skill_links is None:
        skill_links = [f"references/{name}" for name in cards]
    links = "\n".join(f"- [card]({item})" for item in skill_links)
    (root / "skills" / "queue-literature" / "SKILL.md").write_text(
        f"# Queue Literature\n\n{links}\n", encoding="utf-8"
    )


class KnowledgeTests(unittest.TestCase):
    def assert_knowledge(self, repo_root, expected=EXPECTED_CARDS):
        repo_root = repo_root.resolve()
        skill = repo_root / "skills" / "queue-literature" / "SKILL.md"
        references = skill.parent / "references"
        missing = sorted(name for name in expected if not (references / name).is_file())
        self.assertFalse(missing, f"missing expected cards: {', '.join(missing)}")

        card_paths = sorted(
            path
            for path in references.glob("*.md")
            if re.search(r"^\|\s*ID\s*\|", path.read_text(encoding="utf-8"), re.M)
        )
        cards = {}
        ids = []
        for path in card_paths:
            text = path.read_text(encoding="utf-8")
            rows, fields = card_fields(text)
            self.assertEqual(len(rows), len(fields), f"{path.name}: duplicate fields")
            self.assertEqual(CARD_FIELDS, set(fields), f"{path.name}: bad card fields")
            self.assertTrue(all(fields.values()), f"{path.name}: empty card field")
            self.assertEqual("source-checked", fields["Review"], path.name)
            self.assertTrue(valid_date(fields["Reviewed on"]), f"{path.name}: bad date")
            stages = {item.strip() for item in fields["Stage relevance"].split(",")}
            self.assertTrue(
                stages <= {"Stage 1", "Stage 2"}, f"{path.name}: bad stages"
            )
            cards[path.name] = (path, text, fields)
            ids.append(fields["ID"])
        self.assertEqual(len(ids), len(set(ids)), f"duplicate card IDs: {ids}")
        self.assertTrue(set(expected) <= set(cards), "expected card lacks ID metadata")
        for name, expected_id in expected.items():
            self.assertEqual(expected_id, cards[name][2]["ID"], f"{name}: changed ID")

        payload = json.loads((references / "sources.json").read_text(encoding="utf-8"))
        self.assertEqual({"sources"}, set(payload), "sources.json: bad top-level shape")
        records = payload["sources"]
        source_ids = [record.get("id") for record in records]
        self.assertTrue(all(isinstance(item, str) and item for item in source_ids))
        self.assertEqual(
            len(source_ids), len(set(source_ids)), f"duplicate source IDs: {source_ids}"
        )
        dois = []
        for record in records:
            self.assertTrue(SOURCE_FIELDS <= set(record), f"bad source: {record}")
            self.assertIn(record["reading_depth"], DEPTHS, "bad reading_depth")
            locators = record["locators"]
            self.assertTrue(
                isinstance(locators, list)
                and locators
                and all(isinstance(item, str) and item for item in locators),
                f"{record['id']}: missing locators",
            )
            self.assertTrue(valid_date(record["reviewed_on"]), "bad source review date")
            if record["doi"] is not None:
                self.assertIsInstance(record["doi"], str)
                doi = re.sub(r"^doi:\s*", "", record["doi"].strip().lower())
                dois.append(
                    re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi).rstrip("/")
                )
        self.assertEqual(len(dois), len(set(dois)), f"duplicate DOIs: {dois}")
        registry_ids = set(source_ids)

        for path, text, fields in cards.values():
            listed = {
                item.strip() for item in fields["Sources"].split(",") if item.strip()
            }
            cited = set(SOURCE_LINK.findall(text))
            for source_id in listed | cited:
                self.assertIn(
                    source_id, registry_ids, f"{path.name}: unknown source {source_id}"
                )
            for source_id in listed:
                self.assertIn(
                    f"[{source_id}](sources.json)",
                    text,
                    f"{path.name}: source {source_id} lacks an exact claim link",
                )
            self.assertTrue(
                cited <= listed, f"{path.name}: citation absent from header"
            )

        documents = [skill] + [item[0] for item in cards.values()]
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
        for path, _, _ in cards.values():
            self.assertIn(
                path.resolve(), skill_targets, f"topic map does not link {path.name}"
            )

    def assert_bad(self, pattern, *, expected=None, **fixture):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            write_fixture(root, **fixture)
            with self.assertRaisesRegex(AssertionError, pattern):
                expected = {"card.md": "policy.test"} if expected is None else expected
                self.assert_knowledge(root, expected)

    def test_valid_fixtures(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            cards = {name: card(card_id) for name, card_id in EXPECTED_CARDS.items()}
            write_fixture(root, cards=cards)
            self.assert_knowledge(root)

    def test_duplicate_ids_and_dois(self):
        self.assert_bad(
            "duplicate card IDs",
            cards={"a.md": card(), "b.md": card()},
            expected={"a.md": "policy.test", "b.md": "policy.test"},
        )
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

    def test_content_and_link_regressions(self):
        self.assert_bad(
            "unknown source", cards={"card.md": card(source_ids=("missing",))}
        )
        self.assert_bad(
            "lacks an exact claim link",
            cards={
                "card.md": card().replace("[source.one](sources.json)", "source.one")
            },
        )
        self.assert_bad("missing locators", sources=[source(locators=[])])
        self.assert_bad(
            "bad reading_depth", sources=[source(reading_depth="full-text")]
        )
        self.assert_bad("broken link", cards={"card.md": card(extra="[x](missing.md)")})
        self.assert_bad(
            "escapes repository",
            cards={"card.md": card(extra="[x](../../../../outside.md)")},
        )
        self.assert_bad("topic map does not link", skill_links=[])
        self.assert_bad("missing expected cards", expected=EXPECTED_CARDS)

    def test_repository(self):
        self.assert_knowledge(Path(__file__).resolve().parents[2])
