"""Offline documentation integrity checks; not a host-compatibility test."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "docs/getting-started.md",
    ROOT / "docs/references.md",
    ROOT / "docs/guide.html",
    *sorted((ROOT / "discovery-lab").rglob("*.md")),
]


class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class DocumentationTests(unittest.TestCase):
    def test_reader_entry_points_exist_and_use_english(self):
        for path in DOCS:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text()
                self.assertTrue(text.strip())
                self.assertNotRegex(text, r"[\u3400-\u4dbf\u4e00-\u9fff]")

    def test_local_links_resolve(self):
        for path in DOCS:
            text = path.read_text()
            if path.suffix == ".html":
                parser = GuideParser()
                parser.feed(text)
                links = [
                    attrs[key]
                    for _, attrs in parser.elements
                    for key in ("href", "src")
                    if key in attrs
                ]
            else:
                links = re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text)
            for link in links:
                target = urlsplit(link)
                if target.scheme or target.netloc:
                    continue
                destination = (path.parent / unquote(target.path)).resolve() if target.path else path
                with self.subTest(path=path.relative_to(ROOT), link=link):
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.exists())
                    if destination.suffix == ".html" and target.fragment:
                        parser = GuideParser()
                        parser.feed(destination.read_text())
                        ids = {attrs["id"] for _, attrs in parser.elements if "id" in attrs}
                        self.assertIn(unquote(target.fragment), ids)

    def test_guide_has_readable_document_structure(self):
        parser = GuideParser()
        parser.feed((ROOT / "docs/guide.html").read_text())
        tags = [tag for tag, _ in parser.elements]
        self.assertIn("main", tags)
        self.assertIn("title", tags)
        self.assertEqual(tags.count("h1"), 1)
        self.assertTrue(any(tag == "html" and attrs.get("lang") == "en" for tag, attrs in parser.elements))
        self.assertTrue(any(tag == "meta" and attrs.get("name") == "viewport" for tag, attrs in parser.elements))

    def test_guide_does_not_require_remote_assets(self):
        text = (ROOT / "docs/guide.html").read_text()
        parser = GuideParser()
        parser.feed(text)
        for tag, attrs in parser.elements:
            # Ordinary outbound citation/navigation links are allowed.
            if tag == "a":
                continue
            for key in ("src", "href"):
                if key in attrs:
                    with self.subTest(tag=tag, resource=attrs[key]):
                        self.assertFalse(urlsplit(attrs[key]).netloc)
        self.assertNotRegex(text, r"@import\b|url\(\s*['\"]?(?:https?:)?//")

    def test_svg_diagrams_are_standalone_and_described(self):
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for name in ("overview", "stage-1", "stage-2"):
            with self.subTest(diagram=name):
                path = ROOT / "docs/assets" / f"{name}.svg"
                tree = ET.parse(path)
                root = tree.getroot()
                self.assertIn("viewBox", root.attrib)
                for element in ("title", "desc"):
                    description = root.find(f"svg:{element}", ns)
                    if description is None:
                        self.fail(f"Missing SVG {element}")
                    self.assertTrue("".join(description.itertext()).strip())
                self.assertTrue(root.findall(".//svg:text", ns))
                self.assertFalse(root.findall(".//svg:script", ns))
                for element in root.iter():
                    for key, value in element.attrib.items():
                        if key.split("}")[-1] in {"href", "src"}:
                            self.assertTrue(value.startswith("#"), "SVG assets must be self-contained")


if __name__ == "__main__":
    unittest.main()
