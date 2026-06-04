from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

from doctrine_common import REPO_ROOT, DoctrineError


SKILL_NAME = "agent-doctrine-router"
PACKAGE_SOURCE = REPO_ROOT / "package" / SKILL_NAME


def check_no_symlinks(path: Path) -> None:
    for item in path.rglob("*"):
        if item.is_symlink():
            raise DoctrineError(f"symlink is not allowed in skill package: {item}")


def install_skill(provider: str, skills_root: Path) -> Path:
    source = PACKAGE_SOURCE.resolve()
    if not (source / "SKILL.md").is_file():
        raise DoctrineError(f"missing skill source: {source / 'SKILL.md'}")
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
    shutil.copytree(source, new_target, symlinks=False, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
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
