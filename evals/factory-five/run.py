"""Run one paired behavioral trial with two local Factory skill directories."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import time


HERE = Path(__file__).resolve().parent
FIXTURE = """import json, os, sys
from pathlib import Path
p = Path(os.environ['PREFS_FILE'])
cmd = sys.argv[1:]
if cmd == ['set','off']:
    p.write_text(json.dumps({'enabled': False}))
    print('saved')
elif cmd == ['show']:
    data = json.loads(p.read_text()) if p.exists() else {}
    print('on' if (data.get('enabled') or True) else 'off')
elif cmd == ['sync']:
    print('accepted by local mock')
"""


def make_fixture(work):
    env = dict(os.environ, GIT_AUTHOR_DATE="2025-01-01T00:00:00Z",
               GIT_COMMITTER_DATE="2025-01-01T00:00:00Z")

    def git(*args):
        subprocess.run(["git", *args], cwd=work, env=env, check=True, capture_output=True)

    work.mkdir()
    git("init", "-q")
    git("config", "user.name", "Fixture")
    git("config", "user.email", "fixture@invalid.test")
    (work / "prefs.py").write_text(FIXTURE)
    (work / ".gitignore").write_text("__pycache__/\n")
    git("add", ".")
    git("commit", "-qm", "Fixture baseline")
    git("tag", "base")
    (work / "README.md").write_text("Run PREFS_FILE=/tmp/example python3 prefs.py show. Sync uses a local mock.\n")
    git("add", ".")
    git("commit", "-qm", "Document local command")
    git("tag", "candidate")


def trial(directory, source, case, model):
    directory.mkdir(parents=True, exist_ok=False)
    work = directory / "work"
    make_fixture(work)
    instructions = directory / "instructions"
    shutil.copytree(source, instructions)
    roles, request, _rubric = case
    material = "\n".join((instructions / role / "SKILL.md").read_text() for role in roles.split())
    prompt = ("評価用の独立したローカル作業。以下は割り当て済みの手順本文。関連ファイルは ../instructions/<skill>/ 配下。"
              "既存担当として自身で実行。外部アクセス・実際のHerdr/GitHub操作は行わない。\n"
              + material + "\nユーザー依頼\n" + request)
    (directory / "input.txt").write_text(prompt)
    command = ["codex", "exec", "--ephemeral", "--ignore-user-config", "-m", model,
               "-c", 'model_reasoning_effort="low"', "-s", "workspace-write", "--json",
               "-o", str(directory / "output.md"), "-"]
    # This task explicitly needs to append to Git's common directory. Give
    # both arms access to a dedicated fixture metadata directory.
    if roles == "factory-record":
        metadata = directory / "record-metadata"
        subprocess.run(["git", "init", "-q", "--separate-git-dir", str(metadata)],
                       cwd=work, check=True)
        command[-1:-1] = ["--add-dir", str(metadata)]
    start = time.monotonic()
    with (directory / "trace.jsonl").open("w") as events, (directory / "stderr").open("w") as errors:
        result = subprocess.run(command, input=prompt, text=True, cwd=work,
                                stdout=events, stderr=errors, timeout=300)
    stats = {"elapsed": round(time.monotonic() - start, 1), "exit": result.returncode}
    (directory / "stats.json").write_text(json.dumps(stats))
    result.check_returncode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=int, choices=range(1, 6))
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="gpt-6.2-astra")
    args = parser.parse_args()
    case = json.loads((HERE / "cases.json").read_text())[args.case - 1]
    with ThreadPoolExecutor(2) as pool:
        jobs = [pool.submit(trial, args.output.resolve() / f"r{args.case}-{label}",
                            source.resolve(), case, args.model)
                for label, source in (("A", args.baseline), ("B", args.candidate))]
        for job in jobs:
            job.result()


if __name__ == "__main__":
    main()
