"""Regression checks for routing, installation, and Herdr startup."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = load("factory_hook", "hooks/user_prompt_submit.py")
installer = load("factory_install", "scripts/install.py")
dispatch = load("factory_dispatch", "skills/herdr-factory-dispatch/scripts/dispatch.py")


class PromptRouting(unittest.TestCase):
    def test_plain_implementation_requests(self):
        for prompt in (
            "普通にIssueを実装して下さい。",
            "Issue #15 と #16 を実装してください。",
            "この Issue の実装をお願いします。",
            "#15を実装して",
            "Implement issue https://github.com/example/project/issues/15.",
        ):
            with self.subTest(prompt=prompt):
                self.assertTrue(hook.matches(prompt))

    def test_other_intents_pass_through(self):
        for prompt in (
            "Issue #15 の実装方法を説明してください。",
            "Issue #15 を実装しないでください。",
            "「Issueを実装してください。」という入力をテストする",
            "HerdrでIssue実装 #15",
            "/factory-orchestrate #15",
        ):
            with self.subTest(prompt=prompt):
                self.assertFalse(hook.matches(prompt))

    @patch.dict(os.environ, {"HERDR_ENV": "1", "HERDR_WORKSPACE_ID": "w-example"})
    def test_route_excludes_workers_and_plan_mode(self):
        with tempfile.TemporaryDirectory() as repo:
            subprocess.run(["git", "init", "-q", repo], check=True)
            event = {"hook_event_name": "UserPromptSubmit", "prompt": "Issue #15 を実装して", "cwd": repo}
            context = hook.route(event)["hookSpecificOutput"]["additionalContext"]
            self.assertIn("factory-orchestrate/SKILL.md", context)
            self.assertIsNone(hook.route({**event, "permission_mode": "plan"}))
            Path(repo, ".git", "local-software-factory-worker").touch()
            self.assertIsNone(hook.route(event))


class Install(unittest.TestCase):
    def test_repeat_install_preserves_existing_hooks_on_both_clients(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            config_paths = {
                "codex": (folder / "codex-skills", folder / "hooks.json"),
                "claude": (folder / "claude-skills", folder / "settings.json"),
            }
            old = {"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "existing-hook"}]}]}}
            for _, config in config_paths.values():
                config.write_text(json.dumps(old))
            with patch.object(installer, "configuration", return_value=config_paths):
                installer.install(("codex", "claude"))
                installer.install(("codex", "claude"))
            for skills, config in config_paths.values():
                groups = json.loads(config.read_text())["hooks"]["UserPromptSubmit"]
                self.assertEqual(groups[0], old["hooks"]["UserPromptSubmit"][0])
                self.assertEqual(len(groups), 2)
                self.assertTrue((skills / "factory-orchestrate" / "SKILL.md").is_file())


class Dispatch(unittest.TestCase):
    def test_only_explicit_busy_refusal_is_retried(self):
        busy = dispatch.CommandError(json.dumps({"error": {"code": "agent_pane_busy"}}))
        with patch.object(dispatch, "run", side_effect=[busy, "ready"]) as run, patch.object(dispatch.time, "sleep"):
            self.assertEqual(dispatch.start_agent(["herdr"]), "ready")
            self.assertEqual(run.call_count, 2)

        with patch.object(dispatch, "run", side_effect=subprocess.TimeoutExpired(["herdr"], 70)) as run:
            with self.assertRaises(subprocess.TimeoutExpired):
                dispatch.start_agent(["herdr"])
            run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
