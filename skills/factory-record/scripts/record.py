#!/usr/bin/env python3
"""Append a Factory outcome to the local repository's shared record."""

from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys


def already_recorded(stream, entry):
    stream.seek(0)
    for line in stream:
        previous = json.loads(line)
        if (previous.get("task"), previous.get("event_id")) != (entry["task"], entry["event_id"]):
            continue
        previous.pop("recorded_at", None)
        if previous != entry:
            raise ValueError("this task and event_id already identify a different report")
        return True
    return False


def main():
    entry = json.load(sys.stdin)
    if not isinstance(entry, dict) or not all(
        isinstance(entry.get(key), str) and entry[key].strip() for key in ("task", "outcome")
    ):
        raise ValueError("pass a JSON object with task and outcome")
    deduplicate = "event_id" in entry
    if deduplicate and not (isinstance(entry["event_id"], str) and entry["event_id"].strip()):
        raise ValueError("event_id must be a nonempty string")
    entry.pop("recorded_at", None)
    git_dir = subprocess.check_output(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], text=True, timeout=5,
    ).strip()
    directory = Path(git_dir) / "local-software-factory"
    directory.mkdir(mode=0o700, exist_ok=True)
    path = directory / "runs.jsonl"
    mode = os.O_RDWR if deduplicate else os.O_WRONLY
    with os.fdopen(os.open(path, os.O_CREAT | os.O_APPEND | mode, 0o600), "a+" if deduplicate else "a", encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        if not deduplicate or not already_recorded(stream, entry):
            stream.write(json.dumps({**entry, "recorded_at": datetime.now(timezone.utc).isoformat()}, ensure_ascii=False) + "\n")
            stream.flush()
    print(path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        sys.exit(f"Factory record: {error}")
