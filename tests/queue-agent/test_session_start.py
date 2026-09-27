"""Source-level hook checks; these do not install or invoke a Plugin host."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "hooks/session_start.py"


class SessionStartTests(unittest.TestCase):
    def read_context(self, result: subprocess.CompletedProcess[str]) -> str:
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"hookSpecificOutput"})
        output = payload["hookSpecificOutput"]
        self.assertEqual(set(output), {"hookEventName", "additionalContext"})
        self.assertEqual(output["hookEventName"], "SessionStart")
        self.assertIsInstance(output["additionalContext"], str)
        self.assertTrue(output["additionalContext"].strip())
        return output["additionalContext"]

    def test_hook_points_to_existing_entry_from_unrelated_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as workspace:
            context = self.read_context(
                subprocess.run(
                    [sys.executable, str(SCRIPT)],
                    cwd=workspace,
                    input="{}",
                    text=True,
                    capture_output=True,
                    check=False,
                )
            )
            self.assertEqual(list(Path(workspace).iterdir()), [])
        entry = ROOT / "skills/queue-agent/SKILL.md"
        self.assertTrue(entry.is_file())
        self.assertIn(json.dumps(str(entry)), context)

    def test_lifecycle_events_do_not_choose_or_persist_task_state(self) -> None:
        contexts = []
        with tempfile.TemporaryDirectory() as workspace:
            for source in ("startup", "resume", "clear", "compact", "fork"):
                contexts.append(
                    self.read_context(
                        subprocess.run(
                            [sys.executable, str(SCRIPT)],
                            cwd=workspace,
                            input=json.dumps(
                                {
                                    "hook_event_name": "SessionStart",
                                    "source": source,
                                    "cwd": workspace,
                                    "transcript_path": str(
                                        Path(workspace) / "absent.jsonl"
                                    ),
                                }
                            ),
                            text=True,
                            capture_output=True,
                            check=False,
                        )
                    )
                )
            self.assertEqual(list(Path(workspace).iterdir()), [])
        self.assertEqual(len(set(contexts)), 1)

    def test_configured_command_supports_both_root_variables_and_spaces(self) -> None:
        config = json.loads((ROOT / "hooks/hooks.json").read_text())
        (group,) = config["hooks"]["SessionStart"]
        self.assertNotIn("matcher", group)
        (handler,) = group["hooks"]
        self.assertEqual(handler["type"], "command")
        with tempfile.TemporaryDirectory() as workspace:
            root = Path(workspace) / "Queue Plugin"
            (root / "hooks").mkdir(parents=True)
            shutil.copyfile(SCRIPT, root / "hooks/session_start.py")
            shutil.copytree(ROOT / "skills/queue-agent", root / "skills/queue-agent")
            before = sorted(root.rglob("*"))
            for variable in ("CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT"):
                with self.subTest(variable=variable):
                    env = dict(os.environ)
                    env.pop("CLAUDE_PLUGIN_ROOT", None)
                    env.pop("PLUGIN_ROOT", None)
                    env[variable] = str(root)
                    context = self.read_context(
                        subprocess.run(
                            ["/bin/sh", "-c", handler["command"]],
                            cwd=workspace,
                            env=env,
                            input="{}",
                            text=True,
                            capture_output=True,
                            check=False,
                            timeout=handler["timeout"],
                        )
                    )
                    entry = (root / "skills/queue-agent/SKILL.md").resolve()
                    self.assertIn(json.dumps(str(entry)), context)
            self.assertEqual(sorted(root.rglob("*")), before)


if __name__ == "__main__":
    unittest.main()
