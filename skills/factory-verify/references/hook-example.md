# 実例　Issue 実装依頼の振り分け

このリポジトリを対象とした例。受入条件は「Herdr の統括で通常の Issue 実装依頼を拾う」「実装方法を尋ねただけなら拾わない」の2つ。QA の worktree は子セッションとしてマークされているため、入力イベントの作業ディレクトリには一時的な Git リポジトリを使う。Hook スクリプト自体は検証する候補から実行する。

候補のルートで次を実行する。対象 SHA を依頼と照合してから、2つの入力を試す。

```sh
git rev-parse HEAD
python3 - <<'PY'
import json
import os
from pathlib import Path
import subprocess
import tempfile

hook = Path("hooks/user_prompt_submit.py").resolve()
cases = [
    ("Issue #15 を実装してください。", True),
    ("Issue #15 の実装方法を説明してください。", False),
]
with tempfile.TemporaryDirectory() as project:
    subprocess.run(["git", "init", "-q", project], check=True)
    env = dict(os.environ, HERDR_ENV="1", HERDR_WORKSPACE_ID="example")
    for prompt, expected in cases:
        event = {"hook_event_name": "UserPromptSubmit", "prompt": prompt, "cwd": project}
        result = subprocess.run(
            ["python3", str(hook)], input=json.dumps(event), text=True,
            capture_output=True, env=env, check=True,
        )
        output = json.loads(result.stdout) if result.stdout.strip() else {}
        context = output.get("hookSpecificOutput", {}).get("additionalContext", "")
        print(prompt, "統括へ振り分け" if context else "追加指示なし")
        if expected:
            assert "factory-orchestrate/SKILL.md" in context
        else:
            assert not output
PY
```

報告には、各入力に対する実測、候補 SHA、実行したディレクトリを載せる。ここで観測するのは Hook の標準出力。実装セッションの起動まで受入条件に含まれる場合は、Herdr から実際にペインと担当の応答を確認した結果を別の行に載せる。起動を試していなければ、その行は未確認になる。
