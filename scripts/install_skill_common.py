from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

from doctrine_common import REPO_ROOT, DoctrineError


SKILL_NAME = "agent-doctrine-router"
PACKAGE_SOURCE = REPO_ROOT / "package" / SKILL_NAME
REQUIRED_MODULE = Path("modules/core.md")
IGNORED_NAMES = {".skill-source", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc"}
IGNORED_DIRS = {"__pycache__"}


def check_no_symlinks(path: Path) -> None:
    for item in path.rglob("*"):
        if item.is_symlink():
            raise DoctrineError(f"symlink is not allowed in skill package: {item}")


def package_files(root: Path) -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.name in IGNORED_NAMES or path.suffix in IGNORED_SUFFIXES:
            continue
        if path.is_file():
            files[relative] = path.read_bytes()
    return files


def check_snapshot_matches_source(source: Path, snapshot: Path) -> None:
    source_files = package_files(source)
    snapshot_files = package_files(snapshot)
    if source_files != snapshot_files:
        missing = sorted(
            str(path) for path in source_files.keys() - snapshot_files.keys()
        )
        extra = sorted(
            str(path) for path in snapshot_files.keys() - source_files.keys()
        )
        changed = sorted(
            str(path)
            for path in source_files.keys() & snapshot_files.keys()
            if source_files[path] != snapshot_files[path]
        )
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"extra: {', '.join(extra)}")
        if changed:
            details.append(f"changed: {', '.join(changed)}")
        raise DoctrineError(f"staged skill snapshot differs from source ({'; '.join(details)})")


def install_skill(provider: str, skills_root: Path) -> Path:
    source = PACKAGE_SOURCE.resolve()
    if not (source / "SKILL.md").is_file():
        raise DoctrineError(f"missing skill source: {source / 'SKILL.md'}")
    if not (source / REQUIRED_MODULE).is_file():
        raise DoctrineError(f"missing routed skill module: {source / REQUIRED_MODULE}")
    check_no_symlinks(source)
    root = skills_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink():
        raise DoctrineError(f"refusing to install into symlink skills root: {root}")
    target = root / SKILL_NAME
    if target.exists() and target.is_symlink():
        raise DoctrineError(f"refusing to replace symlink target: {target} -> {target.readlink()}")
    if target.exists() and not target.is_dir():
        raise DoctrineError(f"refusing to replace non-directory skill target: {target}")
    if target.exists() and target.resolve() == source:
        raise DoctrineError("source and install target resolve to the same path")
    new_target = root / f".{SKILL_NAME}.new"
    if new_target.exists():
        shutil.rmtree(new_target)
    shutil.copytree(
        source,
        new_target,
        symlinks=False,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )
    check_snapshot_matches_source(source, new_target)
    (new_target / ".skill-source").write_text(str(REPO_ROOT) + "\n", encoding="utf-8")
    old_stash: Path | None = None
    try:
        if target.exists():
            stash_root = Path(tempfile.mkdtemp(prefix=f"{SKILL_NAME}-old-"))
            old_stash = stash_root / SKILL_NAME
            shutil.move(str(target), str(old_stash))
        os.replace(new_target, target)
    except Exception:
        if old_stash and old_stash.exists() and not target.exists():
            shutil.move(str(old_stash), str(target))
        raise
    finally:
        if new_target.exists():
            shutil.rmtree(new_target)
        if old_stash:
            shutil.rmtree(old_stash.parent, ignore_errors=True)
    print(f"installed {provider} skill: {target}")
    print(f"source: {source}")
    return target


def main_for(provider: str, default_root: Path, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Install {SKILL_NAME} for {provider}.")
    parser.add_argument("--skills-root", type=Path, default=default_root)
    args = parser.parse_args(argv)
    try:
        install_skill(provider, args.skills_root)
    except DoctrineError as exc:
        parser.error(str(exc))
    return 0
