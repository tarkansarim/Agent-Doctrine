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


HOOK_PACKAGE = REPO_ROOT / "package" / "claude-build-verify"
HOOK_FILENAME = "agent-doctrine-build-verify.py"
HOOK_SOURCE = HOOK_PACKAGE / "build_verify.py"
HOOK_MATCHER = "Write|Edit"

# Claude Code hook timeout (ms): must exceed the hook's internal build timeout
# (600s default) plus buffer. 660s = 660000ms.
HOOK_TIMEOUT_MS = 660_000
HOOK_STATUS_MESSAGE = "C++/CUDA build verification"

# Legacy command substring used to identify the old ad-hoc hook registration
# so it can be replaced during install.
_LEGACY_HOOK_MARKERS = (
    "build-verify.py",
    "agent-doctrine-build-verify.py",
)


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
                "timeout": HOOK_TIMEOUT_MS,
                "statusMessage": HOOK_STATUS_MESSAGE,
            }
        ],
    }


def _is_build_verify_hook(hook: Any, hook_target: Path) -> bool:
    if not isinstance(hook, dict):
        return False
    cmd = hook.get("command", "")
    if not isinstance(cmd, str):
        return False
    return any(marker in cmd for marker in _LEGACY_HOOK_MARKERS)


def without_existing_build_verify(entries: Any, hook_target: Path) -> list[Any]:
    if not isinstance(entries, list):
        return []
    filtered = []
    for entry in entries:
        if not isinstance(entry, dict):
            filtered.append(entry)
            continue
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            filtered.append(entry)
            continue
        remaining = [h for h in hooks if not _is_build_verify_hook(h, hook_target)]
        if remaining:
            updated = dict(entry)
            updated["hooks"] = remaining
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
    (hooks_dir / ".build-verify-source").write_text(str(REPO_ROOT) + "\n", encoding="utf-8")
    os.replace(new_target, hook_target)

    settings_path = root / "settings.json"
    settings = load_settings(settings_path)
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        hooks = {}

    post_tool = without_existing_build_verify(hooks.get("PostToolUse"), hook_target)
    post_tool.append(hook_entry(hook_target))
    hooks["PostToolUse"] = post_tool
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
    parser = argparse.ArgumentParser(
        description="Install the Agent-Doctrine Claude build-verify hook."
    )
    parser.add_argument("--target-root", type=Path, default=Path.home() / ".claude")
    args = parser.parse_args(argv)
    try:
        hook_target, settings_path = install_hook(args.target_root)
    except DoctrineError as exc:
        parser.error(str(exc))
    print(f"installed Claude build-verify hook: {hook_target}")
    print(f"updated Claude settings: {settings_path}")
    print(f"source: {HOOK_SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
