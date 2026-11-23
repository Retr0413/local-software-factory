#!/usr/bin/env python3
"""Route ordinary Issue implementation prompts to the Factory coordinator."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


ISSUE_URL = r"https://github\.com/[\w.-]+/[\w.-]+/issues/[1-9]\d*"
ISSUE_ID = r"(?:#[1-9]\d*|[A-Z][A-Z0-9]*-[1-9]\d*)"
ISSUE_TARGET = rf"(?:{ISSUE_URL}|{ISSUE_ID})"
ISSUE_LIST = rf"{ISSUE_TARGET}(?:\s*(?:と|,|、|and)\s*{ISSUE_TARGET})*"
JP = re.compile(
    rf"(?:普通に\s*)?(?:(?:この|その)?\s*(?:Issue|イシュー|課題)(?:\s*{ISSUE_LIST})?|{ISSUE_LIST})"
    r"\s*(?:を\s*実装\s*(?:して(?:\s*(?:ください|下さい))?|を\s*お願いします)|の\s*実装\s*を\s*お願いします)"
    r"\s*[。.!！]?",
    re.IGNORECASE,
)
EN = re.compile(rf"(?:please\s+)?implement\s+(?:(?:the|this|these)\s+)?issues?(?:\s+{ISSUE_LIST})?\s*[.!]?",
                re.IGNORECASE)


def matches(prompt):
    lines = unicodedata.normalize("NFKC", prompt).strip().splitlines()
    if not lines:
        return False
    first = lines[0].strip()
    return bool(JP.fullmatch(first) or EN.fullmatch(first))


def is_worker(cwd):
    try:
        git_dir = subprocess.check_output(
            ["git", "-C", cwd, "rev-parse", "--absolute-git-dir"],
            stderr=subprocess.DEVNULL, text=True, timeout=1,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return False
    return Path(git_dir, "local-software-factory-worker").is_file()


def route(event):
    if not isinstance(event, dict) or event.get("hook_event_name") != "UserPromptSubmit":
        return
    prompt = event.get("prompt")
    if not isinstance(prompt, str) or not matches(prompt) or event.get("permission_mode") == "plan":
        return
    cwd = event.get("cwd")
    if isinstance(cwd, str) and is_worker(cwd):
        return
    if os.environ.get("HERDR_ENV") == "1" and os.environ.get("HERDR_WORKSPACE_ID"):
        skill = Path(__file__).resolve().parents[1] / "skills" / "factory-orchestrate" / "SKILL.md"
        context = (
            "Use the Local Software Factory as the coordinator for this Issue implementation. "
            f"Read and follow {skill}. Resolve the Issue from the request or conversation before dispatch. "
            "Assign one existing or new implementation session per Issue through Herdr. "
            "Honor the user's full request, including any restriction to planning or explanation."
        )
    else:
        context = (
            "The Issue implementation request selected Local Software Factory. "
            "The coordinator must run in the intended Herdr pane. "
            "Tell the user to submit the request there and keep implementation pending."
        )
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}


if __name__ == "__main__":
    try:
        result = route(json.load(sys.stdin))
    except (ValueError, UnicodeError):
        result = None
    if result:
        print(json.dumps(result))
