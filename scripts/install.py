#!/usr/bin/env python3
"""Register the same Factory skills and prompt hook in the two local CLIs."""

import argparse
import json
import os
from pathlib import Path
import shlex
import sys
from tempfile import NamedTemporaryFile


ROOT = Path(__file__).resolve().parents[1]


def configuration():
    codex = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    claude = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    return {
        "codex": (Path.home() / ".agents" / "skills", codex / "hooks.json"),
        "claude": (claude / "skills", claude / "settings.json"),
    }


def settings_with_hook(path):
    settings = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    groups = settings.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    command = shlex.join([sys.executable, str(ROOT / "hooks" / "user_prompt_submit.py")])
    hook = {"type": "command", "command": command, "timeout": 3}
    if not any(existing.get("command") == command for group in groups for existing in group["hooks"]):
        groups.append({"hooks": [hook]})
    return settings


def save_settings(path, settings):
    path = path.resolve()
    content = json.dumps(settings, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and json.loads(path.read_text(encoding="utf-8")) == settings:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=path.parent, mode="w", encoding="utf-8", delete=False) as temporary:
        temporary.write(content)
        staged = Path(temporary.name)
    try:
        if path.exists():
            staged.chmod(path.stat().st_mode & 0o777)
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def install(targets):
    locations = configuration()
    skills = sorted(path.parent for path in (ROOT / "skills").glob("*/SKILL.md"))
    plans = []
    for target in targets:
        destination, config = locations[target]
        settings = settings_with_hook(config)
        for skill in skills:
            link = destination / skill.name
            if (link.exists() or link.is_symlink()) and not (link.is_symlink() and link.resolve() == skill):
                raise ValueError(f"existing Skill at {link}")
        plans.append((target, destination, config, settings))

    for target, destination, config, settings in plans:
        destination.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            link = destination / skill.name
            if not link.is_symlink():
                link.symlink_to(skill, target_is_directory=True)
        save_settings(config, settings)
        print(f"{target}: {len(skills)} skills, hook in {config}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("both", "codex", "claude"), default="both")
    selected = parser.parse_args().client
    try:
        install(("codex", "claude") if selected == "both" else (selected,))
    except (OSError, ValueError, AttributeError, KeyError, TypeError) as error:
        sys.exit(f"Factory installation: {error}")
