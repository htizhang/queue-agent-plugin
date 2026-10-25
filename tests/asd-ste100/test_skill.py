"""Source and CLI checks, not installed-host or reader-comprehension tests."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/asd-ste100"
LINTER = SKILL / "scripts/ste-lint.py"


class WritingSkillTests(unittest.TestCase):
    def test_skill_identity_and_provenance(self):
        source = (SKILL / "SKILL.md").read_text()
        self.assertTrue(source.startswith("---\nname: asd-ste100\n"))
        self.assertRegex(source, r"(?m)^description: .+")
        self.assertIn("Use **STE-flavored**", source)
        notice = (SKILL / "NOTICE.md").read_text()
        self.assertIn("c7b11cd9258708909d8574c8176d4c70969c8b29", notice)
        self.assertIn("danyuchn/asd-ste100-skill", notice)
        license_text = (SKILL / "LICENSE").read_text()
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Dustin Yuchen Teng", license_text)

    def test_runtime_assets_are_bundled_without_a_nested_plugin(self):
        for relative in (
            "references/writing-rules.md",
            "examples/before-after.md",
            "examples/linter-edge-cases.md",
            "scripts/ste-lint.py",
        ):
            with self.subTest(relative=relative):
                self.assertTrue((SKILL / relative).is_file())
        self.assertFalse((SKILL / ".claude-plugin").exists())
        self.assertFalse((SKILL / ".git").exists())
        self.assertFalse((SKILL / "hooks").exists())

    def test_entry_and_both_stages_reach_the_shared_skill(self):
        for name in ("queue-agent", "queue-modeling", "queue-policy"):
            with self.subTest(name=name):
                entry = ROOT / "skills" / name / "SKILL.md"
                self.assertIn("(../asd-ste100/SKILL.md)", entry.read_text())

    def test_local_document_links_resolve(self):
        documents = [
            ROOT / "README.md",
            ROOT / "docs/references.md",
            ROOT / "tests/asd-ste100/scenarios.md",
            *(ROOT / "skills").glob("*/SKILL.md"),
            *SKILL.rglob("*.md"),
        ]
        for document in set(documents):
            for link in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", document.read_text()):
                target = urlsplit(link)
                if target.scheme or target.netloc or not target.path:
                    continue
                resolved = (document.parent / unquote(target.path)).resolve()
                with self.subTest(document=str(document), link=link):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists())

    def run_linter(self, *args, text=""):
        with tempfile.TemporaryDirectory() as workspace:
            result = subprocess.run(
                [sys.executable, str(LINTER), *args],
                input=text,
                text=True,
                capture_output=True,
                cwd=workspace,
                timeout=30,
                check=False,
            )
            self.assertEqual(list(Path(workspace).iterdir()), [])
        self.assertEqual(result.stderr, "", result.stderr)
        return result

    def test_upstream_selftests(self):
        result = self.run_linter("--selftest")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("selftest OK", result.stdout)

    def test_linter_accepts_clear_prose_and_preserves_uncertainty(self):
        result = self.run_linter(
            "--json",
            text="The policy may reduce mean flow time in the tested family. "
            "The comparison may have failed.\n",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["violations"], [])

    def test_linter_reports_a_structural_problem(self):
        result = self.run_linter(
            "--json",
            text="The policy selects a job; the server starts its operation.\n",
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        findings = json.loads(result.stdout)["violations"]
        self.assertIn("semicolon", {finding["rule"] for finding in findings})


if __name__ == "__main__":
    unittest.main()
