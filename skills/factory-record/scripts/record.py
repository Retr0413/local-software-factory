#!/usr/bin/env python3
"""Append a Factory outcome to the local repository's shared record."""

from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    entry = json.load(sys.stdin)
    if not isinstance(entry, dict) or not all(
        isinstance(entry.get(key), str) and entry[key].strip() for key in ("task", "outcome")
    ):
        raise ValueError("pass a JSON object with task and outcome")
    git_dir = subprocess.check_output(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], text=True, timeout=5,
    ).strip()
    directory = Path(git_dir) / "local-software-factory"
    directory.mkdir(mode=0o700, exist_ok=True)
    path = directory / "runs.jsonl"
    with os.fdopen(os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o600), "a", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.write(json.dumps({**entry, "recorded_at": datetime.now(timezone.utc).isoformat()}, ensure_ascii=False) + "\n")
        stream.flush()
    print(path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        sys.exit(f"Factory record: {error}")
