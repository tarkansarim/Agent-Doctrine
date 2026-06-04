from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from doctrine_common import REPO_ROOT
from validate_common import validate_installed_skill_root, validate_skill_source


SKILL_NAME = "agent-doctrine-router"
SOURCE_PACKAGE = REPO_ROOT / "package" / SKILL_NAME
DEFAULT_CODEX_SKILLS_ROOT = Path.home() / ".codex" / "skills"
IGNORED_NAMES = {".skill-source", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc"}
IGNORED_DIRS = {"__pycache__"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if path.name in IGNORED_NAMES or path.suffix in IGNORED_SUFFIXES:
            continue
        if path.is_symlink():
            hashes[str(rel)] = "SYMLINK"
            continue
        if path.is_file():
            hashes[str(rel)] = sha256_file(path)
    return hashes


def verify(skills_root: Path) -> tuple[dict, list[str]]:
    installed = skills_root.expanduser().resolve() / SKILL_NAME
    errors: list[str] = []

    for violation in validate_skill_source():
        errors.append(f"source: {violation.path}: {violation.message}")
    for violation in validate_installed_skill_root(skills_root.expanduser()):
        errors.append(f"installed: {violation.path}: {violation.message}")

    if not SOURCE_PACKAGE.is_dir():
        errors.append(f"source package missing: {SOURCE_PACKAGE}")
    if not installed.is_dir():
        errors.append(f"installed package missing: {installed}")

    source_hashes: dict[str, str] = {}
    installed_hashes: dict[str, str] = {}
    if SOURCE_PACKAGE.is_dir() and installed.is_dir():
        source_hashes = tree_hashes(SOURCE_PACKAGE)
        installed_hashes = tree_hashes(installed)
        missing = sorted(set(source_hashes) - set(installed_hashes))
        extra = sorted(set(installed_hashes) - set(source_hashes))
        changed = sorted(
            rel for rel in set(source_hashes) & set(installed_hashes)
            if source_hashes[rel] != installed_hashes[rel]
        )
        if missing:
            errors.append(f"installed package missing source file(s): {', '.join(missing)}")
        if extra:
            errors.append(f"installed package has extra file(s): {', '.join(extra)}")
        if changed:
            errors.append(f"installed package differs from source file(s): {', '.join(changed)}")

    source_marker = installed / ".skill-source"
    marker_value = source_marker.read_text(encoding="utf-8").strip() if source_marker.is_file() else ""
    if marker_value != str(REPO_ROOT):
        errors.append(f".skill-source must equal {REPO_ROOT}; got {marker_value!r}")

    report = {
        "skill": SKILL_NAME,
        "source_package": str(SOURCE_PACKAGE),
        "installed_package": str(installed),
        "skill_source_marker": marker_value,
        "source_file_count": len(source_hashes),
        "installed_file_count": len(installed_hashes),
        "matches_source": not errors,
        "checked_only_codex_skill_root": True,
        "does_not_install_generated_agents_block": True,
        "errors": errors,
    }
    return report, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the installed Codex agent-doctrine-router skill is a source snapshot."
    )
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_CODEX_SKILLS_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report, errors = verify(args.skills_root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif errors:
        print("Codex router install verification failed")
        for error in errors:
            print(f"ERROR  {error}")
    else:
        print("Codex router install verification passed")
        print(f"source:    {report['source_package']}")
        print(f"installed: {report['installed_package']}")
        print(f"files:     {report['installed_file_count']}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
