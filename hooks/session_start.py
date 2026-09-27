"""Emit a short Plugin orientation without selecting or persisting a Stage."""

import json
from pathlib import Path


def main() -> None:
    entry = Path(__file__).resolve().parents[1] / "skills/queue-agent/SKILL.md"
    context = (
        "Queue Agent supports data -> queue model -> policy. "
        "Stage 1 delivers a documented queue model and its corresponding "
        "simulator from data and a system description; Stage 2 first confirms "
        "the problem definition, then selects, evaluates, tunes, or designs policies. "
        "For a queueing task, read the entry skill at "
        f"{json.dumps(str(entry))}. "
        "Choose the next step from the user's current request and available "
        "artifacts; these are capabilities, not a mandatory sequence. "
        "Shared literature and "
        "discussion can be used independently."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
