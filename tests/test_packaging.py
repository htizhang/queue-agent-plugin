"""Package contracts for the same runtime files on both native hosts."""

import json
from pathlib import Path
import re
import subprocess
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json")
SKILLS = {"queue-agent", "queue-modeling", "queue-policy", "queue-literature", "queue-contribute", "asd-ste100"}


class PackagingTests(unittest.TestCase):
    def read(self, path):
        return json.loads((ROOT / path).read_text())

    def test_manifests_share_identity_version_and_license(self):
        manifests = [self.read(path) for path in MANIFESTS]
        for manifest in manifests:
            self.assertEqual(manifest["name"], "queue-agent")
            self.assertEqual(manifest["version"], manifests[0]["version"])
            self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
            self.assertEqual(manifest["license"], "MIT")
            self.assertEqual(manifest["author"]["name"], "htizhang")
            self.assertEqual(manifest["repository"], "https://github.com/htizhang/queue-agent-plugin")
            for field in ("description", "homepage", "keywords"):
                self.assertEqual(manifest[field], manifests[0][field])

    def test_portable_manifest_uses_fixed_component_locations(self):
        manifest = self.read("plugin.json")
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        for field in ("skills", "hooks", "mcpServers", "apps", "interface"):
            self.assertNotIn(field, manifest)
        interface = manifest["extensions"]["com.openai"]["interface"]
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertEqual(interface["displayName"], "Queue Agent")
        self.assertEqual(interface["category"], "Productivity")
        self.assertEqual(interface, self.read(".codex-plugin/plugin.json")["interface"])

    def test_catalogs_select_the_complete_root(self):
        for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
            with self.subTest(catalog=path):
                catalog = self.read(path)
                self.assertEqual(catalog["name"], "queue-agent")
                (entry,) = catalog["plugins"]
                self.assertEqual(entry["name"], "queue-agent")
                source = entry["source"]
                self.assertEqual(source if isinstance(source, str) else source["path"], "./")
        entry = self.read(".agents/plugins/marketplace.json")["plugins"][0]
        self.assertEqual(entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})
        self.assertEqual(entry["category"], "Productivity")

    def test_all_six_skills_and_shared_resources_are_in_package(self):
        self.assertEqual({p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}, SKILLS)
        self.assertTrue((ROOT / "discovery-lab/index.md").is_file())
        self.assertTrue((ROOT / "skills/queue-literature/references/sources.json").is_file())
        self.assertEqual(self.read(".codex-plugin/plugin.json")["skills"], "./skills/")

    def test_hooks_are_discovered_once_without_automatic_trust(self):
        # Both hosts discover hooks/hooks.json; Claude declarations are additive.
        for path in MANIFESTS:
            manifest = self.read(path)
            self.assertNotIn("hooks", manifest)
            self.assertNotIn("hooks", manifest.get("extensions", {}).get("com.openai", {}))
        groups = self.read("hooks/hooks.json")["hooks"]["SessionStart"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]["hooks"]), 1)
        for path in MANIFESTS:
            self.assertNotRegex((ROOT / path).read_text(), r"trust|approval|dangerously|bypass")

    def test_runtime_links_stay_inside_the_package(self):
        tracked = {
            ROOT / name
            for name in subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
            if name
        }
        documents = list((ROOT / "skills").rglob("*.md")) + list((ROOT / "discovery-lab").rglob("*.md"))
        for path in documents:
            # Inline-code examples are not live links.
            text = re.sub(r"`[^`\n]+`", "", path.read_text())
            for link in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                with self.subTest(file=path.relative_to(ROOT), link=link):
                    self.assertTrue(target.is_relative_to(ROOT))
                    self.assertTrue(target.exists())
                    self.assertTrue(
                        target in tracked or target.is_dir() and any(p.is_relative_to(target) for p in tracked),
                        "Linked resources must ship with the Git package",
                    )

    def test_git_package_has_no_machine_artifacts(self):
        files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
        forbidden = ("output/", "runs/", "tmp/", ".env", ".claude/settings", ".codex/config")
        self.assertNotIn("CLAUDE.md", files)
        self.assertFalse(any(path.startswith(forbidden) for path in files))
        artifacts = {".DS_Store", ".venv", "__pycache__"}
        self.assertFalse(any(artifacts.intersection(Path(path).parts) for path in files))


if __name__ == "__main__":
    unittest.main()
