#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


DEFAULT_WORKSPACE_ROOT = Path.home() / "workspace"
DEFAULT_CLAUDE_ROOT = Path.home() / ".claude"
BLOCK_EXIT_CODE = 2


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


def resolve_path(raw_path: str, cwd: Path) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = cwd / path
    return path.resolve(strict=False)


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def direct_repo_under(path: Path, root: Path) -> Path | None:
    if not is_relative_to(path, root):
        return None
    relative = path.relative_to(root)
    if not relative.parts:
        return None
    return root / relative.parts[0]


def claude_memory_root(claude_root: Path) -> Path:
    return claude_root / "projects"


def is_claude_memory_path(path: Path, claude_root: Path) -> bool:
    projects = claude_memory_root(claude_root).resolve(strict=False)
    if not is_relative_to(path, projects):
        return False
    relative = path.relative_to(projects)
    return len(relative.parts) >= 3 and relative.parts[1] == "memory"


def active_repo_from_env(env: dict[str, str], workspace_root: Path) -> Path | None:
    raw_path = env.get("AGENT_DOCTRINE_ACTIVE_REPO")
    if raw_path:
        resolved = Path(raw_path).expanduser().resolve(strict=False)
        repo = direct_repo_under(resolved, workspace_root)
        if repo is not None:
            return repo
        if is_relative_to(resolved, workspace_root):
            return resolved

    raw_name = env.get("AGENT_DOCTRINE_ACTIVE_REPO_NAME")
    if raw_name:
        name = raw_name.strip().strip("/")
        if name and "/" not in name:
            return (workspace_root / name).resolve(strict=False)
    return None


def active_repo_from_cwd(cwd: Path, workspace_root: Path) -> Path | None:
    return direct_repo_under(cwd.resolve(strict=False), workspace_root)


def git_dir_from_marker(marker: Path) -> Path | None:
    if marker.is_dir():
        return marker
    if not marker.is_file():
        return None
    try:
        text = marker.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return None
    prefix = "gitdir:"
    if not text.lower().startswith(prefix):
        return None
    raw_path = text[len(prefix) :].strip()
    git_dir = Path(raw_path).expanduser()
    if not git_dir.is_absolute():
        git_dir = marker.parent / git_dir
    return git_dir.resolve(strict=False)


def common_git_dir(git_dir: Path) -> Path:
    common_dir_file = git_dir / "commondir"
    if not common_dir_file.is_file():
        return git_dir
    try:
        raw_path = common_dir_file.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return git_dir
    common_dir = Path(raw_path).expanduser()
    if not common_dir.is_absolute():
        common_dir = git_dir / common_dir
    return common_dir.resolve(strict=False)


def git_config_value(config_path: Path, section: str, key: str) -> str | None:
    if not config_path.is_file():
        return None
    try:
        lines = config_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    current_section: str | None = None
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            continue
        if current_section != section or "=" not in line:
            continue
        raw_key, raw_value = line.split("=", 1)
        if raw_key.strip() == key:
            return raw_value.strip()
    return None


def git_origin_from_cwd(cwd: Path) -> str | None:
    current = cwd.resolve(strict=False)
    for candidate in (current, *current.parents):
        marker = candidate / ".git"
        git_dir = git_dir_from_marker(marker)
        if git_dir is None:
            continue
        origin = git_config_value(git_dir / "config", 'remote "origin"', "url")
        if origin is not None:
            return origin
        return git_config_value(common_git_dir(git_dir) / "config", 'remote "origin"', "url")
    return None


def local_path_from_origin(origin: str) -> Path | None:
    parsed = urlparse(origin)
    if parsed.scheme == "file":
        return Path(unquote(parsed.path)).expanduser().resolve(strict=False)
    if parsed.scheme or parsed.netloc or ":" in origin:
        return None
    return Path(origin).expanduser().resolve(strict=False)


def active_repo_from_git_origin(cwd: Path, workspace_root: Path) -> Path | None:
    origin = git_origin_from_cwd(cwd)
    if origin is None:
        return None
    origin_path = local_path_from_origin(origin)
    if origin_path is None:
        return None
    if origin_path.suffix == ".git":
        origin_path = origin_path.with_suffix("")
    return direct_repo_under(origin_path, workspace_root)


def target_paths_from_payload(payload: dict[str, Any]) -> list[str]:
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = payload.get("input")
    if not isinstance(tool_input, dict):
        tool_input = payload

    paths: list[str] = []
    for key in ("file_path", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            paths.append(value)
    return paths


def decide_path(
    target: Path,
    *,
    cwd: Path,
    workspace_root: Path,
    claude_root: Path,
    env: dict[str, str],
) -> Decision:
    if is_claude_memory_path(target, claude_root):
        return Decision(True, "target is under Claude project memory")

    target_repo = direct_repo_under(target, workspace_root)
    if target_repo is None:
        return Decision(True, "target is outside the workspace root")

    active_repo = (
        active_repo_from_env(env, workspace_root)
        or active_repo_from_cwd(cwd, workspace_root)
        or active_repo_from_git_origin(cwd, workspace_root)
    )
    if active_repo is not None and target_repo == active_repo.resolve(strict=False):
        return Decision(True, "target is in the active workspace repo")

    if active_repo is None:
        return Decision(
            False,
            f"target is in workspace repo {target_repo.name}, but no active workspace repo could be determined",
        )
    return Decision(
        False,
        f"target is in workspace repo {target_repo.name}, outside active repo {active_repo.name}",
    )


def should_check_tool(payload: dict[str, Any]) -> bool:
    tool_name = payload.get("tool_name") or payload.get("tool")
    return tool_name in {"Write", "Edit"}


def load_payload(stdin_text: str) -> dict[str, Any]:
    try:
        payload = json.loads(stdin_text or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid PreToolUse JSON payload: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("PreToolUse JSON payload must be an object")
    return payload


def block_message(target: Path, reason: str) -> str:
    return (
        "Agent-Doctrine repo write guard blocked this Write/Edit.\n"
        f"Target: {target}\n"
        f"Reason: {reason}.\n"
        "Do not edit another workspace repo directly from this task. File or update a Plane ticket "
        "for that repo with the intended durable change, evidence, and project tag, then work from "
        "a task-owned checkout for that repo."
    )


def main() -> int:
    env = dict(os.environ)
    cwd = Path.cwd().resolve(strict=False)
    workspace_root = Path(env.get("AGENT_DOCTRINE_WORKSPACE_ROOT", DEFAULT_WORKSPACE_ROOT)).expanduser().resolve(strict=False)
    claude_root = Path(env.get("CLAUDE_CONFIG_DIR", DEFAULT_CLAUDE_ROOT)).expanduser().resolve(strict=False)

    try:
        payload = load_payload(sys.stdin.read())
    except ValueError as exc:
        print(f"Agent-Doctrine repo write guard error: {exc}", file=sys.stderr)
        return BLOCK_EXIT_CODE

    if not should_check_tool(payload):
        return 0

    raw_paths = target_paths_from_payload(payload)
    if not raw_paths:
        print("Agent-Doctrine repo write guard blocked Write/Edit with no target path.", file=sys.stderr)
        return BLOCK_EXIT_CODE

    for raw_path in raw_paths:
        target = resolve_path(raw_path, cwd)
        decision = decide_path(
            target,
            cwd=cwd,
            workspace_root=workspace_root,
            claude_root=claude_root,
            env=env,
        )
        if not decision.allowed:
            print(block_message(target, decision.reason), file=sys.stderr)
            return BLOCK_EXIT_CODE
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
