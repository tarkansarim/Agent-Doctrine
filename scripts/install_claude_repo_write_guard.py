from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import tempfile
from pathlib import Path
from typing import Any

from doctrine_common import REPO_ROOT, DoctrineError


HOOK_PACKAGE = REPO_ROOT / "package" / "claude-repo-write-guard"
HOOK_FILENAME = "agent-doctrine-repo-write-guard.py"
HOOK_SOURCE = HOOK_PACKAGE / "repo_write_guard.py"
HOOK_MATCHER = "Write|Edit"


def load_settings(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DoctrineError(f"invalid Claude settings JSON {path}: {exc}") from exc
    if not isinstance(settings, dict):
        raise DoctrineError(f"Claude settings must be a JSON object: {path}")
    return settings


def command_for(hook_target: Path) -> str:
    return f"python3 {shlex.quote(str(hook_target))}"


def hook_entry(hook_target: Path) -> dict[str, Any]:
    return {
        "matcher": HOOK_MATCHER,
        "hooks": [
            {
                "type": "command",
                "command": command_for(hook_target),
            }
        ],
    }


def without_existing_guard(entries: Any, hook_target: Path) -> list[Any]:
    if not isinstance(entries, list):
        return []
    command = command_for(hook_target)
    filtered = []
    for entry in entries:
        if not isinstance(entry, dict):
            filtered.append(entry)
            continue
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            filtered.append(entry)
            continue
        remaining_hooks = [
            hook
            for hook in hooks
            if not (
                isinstance(hook, dict)
                and hook.get("type") == "command"
                and hook.get("command") == command
            )
        ]
        if remaining_hooks:
            updated = dict(entry)
            updated["hooks"] = remaining_hooks
            filtered.append(updated)
    return filtered


def install_hook(target_root: Path) -> tuple[Path, Path]:
    source = HOOK_SOURCE.resolve()
    if not source.is_file():
        raise DoctrineError(f"missing hook source: {source}")
    root = target_root.expanduser().resolve()
    if root.exists() and root.is_symlink():
        raise DoctrineError(f"refusing to install into symlink Claude root: {root}")
    hooks_dir = root / "hooks" / "agent-doctrine"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    if hooks_dir.is_symlink():
        raise DoctrineError(f"refusing to install into symlink hooks directory: {hooks_dir}")

    hook_target = hooks_dir / HOOK_FILENAME
    new_target = hooks_dir / f".{HOOK_FILENAME}.new"
    shutil.copy2(source, new_target)
    new_target.chmod(0o755)
    (hooks_dir / ".repo-write-guard-source").write_text(str(REPO_ROOT) + "\n", encoding="utf-8")
    os.replace(new_target, hook_target)

    settings_path = root / "settings.json"
    settings = load_settings(settings_path)
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        hooks = {}
    pre_tool = without_existing_guard(hooks.get("PreToolUse"), hook_target)
    pre_tool.append(hook_entry(hook_target))
    hooks["PreToolUse"] = pre_tool
    settings["hooks"] = hooks

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".settings.json.", dir=settings_path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(settings, handle, indent=2)
            handle.write("\n")
        os.replace(tmp_path, settings_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
    return hook_target, settings_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install the Agent-Doctrine Claude repo write guard hook.")
    parser.add_argument("--target-root", type=Path, default=Path.home() / ".claude")
    args = parser.parse_args(argv)
    try:
        hook_target, settings_path = install_hook(args.target_root)
    except DoctrineError as exc:
        parser.error(str(exc))
    print(f"installed Claude repo write guard: {hook_target}")
    print(f"updated Claude settings: {settings_path}")
    print(f"source: {HOOK_SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
