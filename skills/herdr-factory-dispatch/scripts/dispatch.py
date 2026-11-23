#!/usr/bin/env python3
"""Launch a batch of Factory jobs in the caller's Herdr session."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
from typing import Optional
import uuid


MAX_PARALLEL_CHILDREN = 10
MANAGED_NAME_PREFIX = "hp-"
LEGACY_MANAGED_NAME = re.compile(r"[a-z][a-z0-9_-]{0,23}-[0-9a-f]{7}")


@dataclass(frozen=True)
class Job:
    name: str
    mode: str
    prompt: str
    issue: Optional[str] = None
    kind: str = "codex"
    base: str = "HEAD"


class IssueLedger:
    """Keep one launch record per Issue across this repository's worktrees."""

    def __init__(self, git_dir):
        self.path = git_dir / "herdr-parallel-issues.sqlite3"
        with self.connect() as database:
            database.execute("CREATE TABLE IF NOT EXISTS issues (issue TEXT PRIMARY KEY, launch TEXT NOT NULL)")

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def reserve(self, record):
        with self.connect() as database:
            inserted = database.execute(
                "INSERT OR IGNORE INTO issues (issue, launch) VALUES (?, ?)",
                (record["issue"], json.dumps(record)),
            ).rowcount
            if inserted:
                return None
            row = database.execute("SELECT launch FROM issues WHERE issue = ?", (record["issue"],)).fetchone()
            return self.existing_receipt(row)

    def find(self, issue):
        with self.connect() as database:
            row = database.execute("SELECT launch FROM issues WHERE issue = ?", (issue,)).fetchone()
            return self.existing_receipt(row) if row else None

    @staticmethod
    def existing_receipt(row):
        previous = json.loads(row[0])
        return dict(previous, recorded_state=previous["state"], state="existing_issue")

    def save(self, record):
        with self.connect() as database:
            database.execute(
                "UPDATE issues SET launch = ? WHERE issue = ?",
                (json.dumps(record), record["issue"]),
            )


class CommandError(RuntimeError):
    def __init__(self, detail):
        super().__init__(detail[:1000])
        try:
            self.code = json.loads(detail)["error"]["code"]
        except (ValueError, KeyError, TypeError):
            self.code = None


def run(args, timeout):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise CommandError(detail or f"command exited with {result.returncode}")
    return result.stdout


def session_lock_path(herdr):
    status = json.loads(run([herdr, "status", "server", "--json"], 10))
    if not status.get("running") or not status.get("socket"):
        raise RuntimeError("Could not resolve the running Herdr session for the launch limit.")
    socket = Path(status["socket"]).resolve()
    lock_dir = Path.home() / ".cache" / "herdr-parallel"
    lock_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    return lock_dir / f"{hashlib.sha256(os.fsencode(socket)).hexdigest()}.lock"


def available_slots(herdr):
    try:
        agents = json.loads(run([herdr, "agent", "list"], 10))["result"]["agents"]
        if not isinstance(agents, list):
            raise ValueError("invalid agent list")
        live_children = set()
        for agent in agents:
            name = agent.get("name") or ""
            if name.startswith(MANAGED_NAME_PREFIX) or (
                agent.get("agent") == "codex" and LEGACY_MANAGED_NAME.fullmatch(name)
            ):
                live_children.add(agent["terminal_id"])
    except (AttributeError, KeyError, TypeError, ValueError) as error:
        raise RuntimeError("Could not read Herdr's agent list for the launch limit.") from error
    return max(0, MAX_PARALLEL_CHILDREN - len(live_children))


def issue_identity(value):
    if not isinstance(value, str):
        raise ValueError("Issue ID must be text such as #123 or ENG-123")
    match = re.fullmatch(r"(?:([A-Z][A-Z0-9]*)-|#?)([0-9]+)", value.strip().upper())
    if not match or not int(match[2]):
        raise ValueError(f"invalid Issue ID {value!r}; use #123 or ENG-123")
    project, number = match[1], int(match[2])
    return f"{project}-{number}" if project else f"#{number}"


def load_jobs():
    raw_jobs = json.load(sys.stdin)
    if not isinstance(raw_jobs, list) or not raw_jobs:
        raise ValueError("expected a non-empty JSON array of jobs")

    jobs = []
    for index, item in enumerate(raw_jobs, 1):
        if not isinstance(item, dict):
            raise ValueError(f"job {index} must be an object")
        name, mode, prompt = (item.get(key) for key in ("name", "mode", "prompt"))
        kind = item.get("kind", "codex")
        base = item.get("base", "HEAD")
        if kind not in ("codex", "claude"):
            raise ValueError(f"job {index} kind must be codex or claude")
        if not isinstance(base, str) or not re.fullmatch(r"HEAD|[0-9a-f]{40}|[0-9a-f]{64}", base):
            raise ValueError(f"job {index} base must be HEAD or a full commit ID")
        issue = None
        if "issue" in item:
            issue = issue_identity(item["issue"])
            if mode not in (None, "write"):
                raise ValueError(f"Issue {issue} must be assigned to one implementation session")
            name, mode = f"issue-{issue.replace('#', 'gh-').lower()}", "write"
        else:
            if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{0,23}", name):
                raise ValueError(f"job {index} needs a lowercase name of at most 24 characters")
            if mode not in ("read", "verify"):
                raise ValueError(f"job {name} mode must be read or verify; implementation requires an Issue or task ID")
        if not isinstance(prompt, str) or not prompt.strip() or "\0" in prompt:
            raise ValueError(f"job {name} needs a non-empty prompt without NUL bytes")
        jobs.append(Job(name, mode, prompt, issue, kind, base))

    if len({(job.issue, job.name) for job in jobs}) != len(jobs):
        raise ValueError("use one job per Issue and unique names within a batch")
    return jobs


def prepare(herdr, repo, commit, job, ledger):
    if job.issue:
        identity = f"{ledger.path.parent}\0{job.issue}".encode()
        suffix = hashlib.sha256(identity).hexdigest()[:7]
    else:
        suffix = uuid.uuid4().hex[:7]
    name_width = 24 - len(MANAGED_NAME_PREFIX)
    agent_name = f"{MANAGED_NAME_PREFIX}{job.name[:name_width]}-{suffix}"
    branch = f"herdr/{job.name[:24]}-{suffix}"
    result = {"job": job.name, "agent": agent_name, "mode": job.mode, "kind": job.kind,
              "branch": branch, "base_commit": commit}
    command = ["worktree", "create", "--cwd", repo, "--branch", branch, "--base", commit]

    if job.issue:
        result.update(issue=job.issue, herdr_session=os.environ.get("HERDR_SESSION") or "default", state="reserved")
        previous = ledger.reserve(result)
        if previous is not None:
            return previous

    try:
        response = json.loads(run([herdr, *command, "--label", job.name, "--no-focus"], 30))
        pane = response["result"]["root_pane"]
        result.update(pane_id=pane["pane_id"], state="prepared")
        if pane.get("terminal_id"):
            result["terminal_id"] = pane["terminal_id"]
        if pane.get("cwd"):
            result["cwd"] = pane["cwd"]
        worktree = Path(result["cwd"]).resolve()
        actual_branch = run(["git", "-C", str(worktree), "symbolic-ref", "--short", "HEAD"], 5).strip()
        if worktree == Path(repo).resolve() or actual_branch != branch:
            raise ValueError("Herdr did not return the worktree for the reserved branch")
        git_dir = run(["git", "-C", str(worktree), "rev-parse", "--absolute-git-dir"], 5).strip()
        Path(git_dir, "local-software-factory-worker").touch()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, KeyError, TypeError) as error:
        result.update(state="prepare_failed", error=describe_error(error))
    if job.issue:
        ledger.save(result)
    return result


def describe_error(error):
    if isinstance(error, subprocess.TimeoutExpired):
        return "Herdr command timed out. Inspect the named agent or branch before retrying."
    return str(error)


def find_session_id(herdr, result):
    try:
        agents = json.loads(run([herdr, "agent", "list"], 5))["result"]["agents"]
        for agent in agents:
            if result.get("terminal_id"):
                matches = agent.get("terminal_id") == result["terminal_id"]
            else:
                matches = agent.get("pane_id") == result["pane_id"]
            if matches:
                session = agent.get("agent_session") or {}
                if session.get("agent") == result["kind"] and session.get("kind") == "id":
                    return session.get("value")
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired, KeyError, TypeError):
        return None


def start_agent(command):
    # Herdr can return the pane before the interactive shell reaches its prompt.
    # A busy refusal confirms the start did not run. Other errors need inspection.
    for attempt in range(6):
        try:
            return run(command, 70)
        except CommandError as error:
            if error.code != "agent_pane_busy" or attempt == 5:
                raise
            time.sleep(0.5)


def launch(herdr, job, result, ledger):
    if result["state"] != "prepared":
        return result

    agent_name = result["agent"]
    if job.kind == "codex":
        permission = "read-only" if job.mode == "read" else "workspace-write"
        options = ["--sandbox", permission, "-c", "agents.enabled=false"]
    else:
        options = ["--permission-mode", "default"]
        disallowed = ["Agent", "Task"]
        if job.mode == "read":
            options += ["--tools", "Read,Glob,Grep"]
            disallowed += ["Bash", "Edit", "Write", "MultiEdit", "NotebookEdit", "mcp__*"]
        options += ["--disallowedTools", *disallowed]
    if job.issue:
        result["state"] = "starting"
        ledger.save(result)
    try:
        start_agent([
            herdr, "agent", "start", agent_name, "--kind", job.kind, "--pane", result["pane_id"],
            "--timeout", "60000", "--", *options,
        ])
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        result.update(state="start_failed", error=describe_error(error))
        if job.issue:
            ledger.save(result)
        return result

    role = {"write": "factory-implement", "read": "factory-investigate", "verify": "factory-verify"}[job.mode]
    skill = Path(__file__).resolve().parents[2] / role / "SKILL.md"
    prompt = (
        f"Assigned Factory worker. Read {skill} and carry out the task below in this worktree. "
        "Report to the coordinator.\n\n" + job.prompt
    )
    if job.issue:
        prompt = (
            f"You are the sole implementation owner of {job.issue} in this worktree. Keep fixes in this "
            "conversation and send requests for supporting work to the coordinator. Report changes, tests, "
            "and blockers.\n\n" + prompt
        )
        result["state"] = "sending_prompt"
        ledger.save(result)
    try:
        run([herdr, "agent", "prompt", agent_name, prompt], 15)
        result["state"] = "prompt_submitted"
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        result.update(state="prompt_unconfirmed", error=describe_error(error))
    if job.issue:
        ledger.save(result)
        session_id = find_session_id(herdr, result)
        if session_id:
            result[f"{job.kind}_session_id"] = session_id
            ledger.save(result)
    return result


def prepare_batch(herdr, repo, commits, jobs, ledger, slots):
    results = []
    for job in jobs:
        if slots:
            result = prepare(herdr, repo, commits[job.base], job, ledger)
            if result["state"] == "prepared":
                slots -= 1
        else:
            result = ledger.find(job.issue) if job.issue else None
            if result is None:
                result = {"job": job.name, "state": "capacity_limit", "limit": MAX_PARALLEL_CHILDREN}
                if job.issue:
                    result["issue"] = job.issue
        results.append(result)
    return results


def main():
    workspace_id = os.environ.get("HERDR_WORKSPACE_ID")
    if os.environ.get("HERDR_ENV") != "1" or not workspace_id:
        raise ValueError("run the dispatcher from the coordinator pane in the intended Herdr session")

    jobs = load_jobs()
    herdr = os.environ.get("HERDR_BIN_PATH") or "herdr"
    repo = run(["git", "rev-parse", "--show-toplevel"], 10).strip()
    current_git_dir = run(["git", "rev-parse", "--absolute-git-dir"], 10).strip()
    if Path(current_git_dir, "local-software-factory-worker").exists():
        raise ValueError("dispatch is reserved for the Factory coordinator")
    commits = {base: run(["git", "rev-parse", "--verify", base + "^{commit}"], 10).strip()
               for base in {job.base for job in jobs}}
    git_dir = run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], 10).strip()
    ledger = IssueLedger(Path(git_dir).resolve())

    with session_lock_path(herdr).open("a") as lock:
        # Keep the inventory and startup under one lock across parent processes.
        fcntl.flock(lock, fcntl.LOCK_EX)
        slots = available_slots(herdr)
        prepared = prepare_batch(herdr, repo, commits, jobs, ledger, slots)
        with ThreadPoolExecutor(max_workers=MAX_PARALLEL_CHILDREN) as pool:
            pending = [pool.submit(launch, herdr, job, result, ledger) for job, result in zip(jobs, prepared)]
            results = [future.result() for future in pending]

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(item["state"] in ("prompt_submitted", "existing_issue") for item in results) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, sqlite3.Error, subprocess.TimeoutExpired) as error:
        print(describe_error(error), file=sys.stderr)
        sys.exit(2)
