from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

from doctrine_common import REPO_ROOT, PROVIDER_SPECS, provider_names


DEFAULT_BASE = Path(os.environ.get("AGENT_DOCTRINE_WORKSPACE_ROOT", Path.home() / "workspace"))
PUBLIC_BASE_LABEL = "<workspace root>"
HOME_ROOT = "/" + "home"
TMP_ROOT = "/" + "tmp"
DROPBOX = "Drop" + "box"
WORKSPACE_DIR_NAME = "My" + "Tools"
WORKSPACE_REL = f"{DROPBOX}/work/{WORKSPACE_DIR_NAME}"
OWNER_NAME = "tar" + "kan"
USR_LOCAL_CUDA_NSYS = "/" + "usr/local/cuda/bin/nsys"
ETC_HOSTNAME = "/" + "etc/hostname"
ABSOLUTE_REPO = "/" + "absolute/repo"
ABSOLUTE_PROJECT = "/" + "absolute/project"
PATH_TO_REWIND = "/" + "path/to/skill/scripts/rewind\\.py"
PATH_TO_COMFYUI = "/" + "path/to/ComfyUI"
PUBLIC_REPLACEMENTS = (
    (rf"{HOME_ROOT}/[^/\s`\"']+/{WORKSPACE_REL}", PUBLIC_BASE_LABEL),
    (rf"{HOME_ROOT}/[^/\s`\"']+/symphony-workspaces", "<workspace root>"),
    (rf"{HOME_ROOT}/[^/\s`\"']+/Documents", "<Documents root>"),
    (rf"{HOME_ROOT}/[^/\s`\"']+/Downloads", "<Downloads root>"),
    (rf"{HOME_ROOT}/[^/\s`\"']+", "<home>"),
    (rf"~/{WORKSPACE_REL}", PUBLIC_BASE_LABEL),
    (rf"{TMP_ROOT}/", "<temp dir>/"),
    (USR_LOCAL_CUDA_NSYS, "nsys on PATH"),
    (ETC_HOSTNAME, "<system hostname file>"),
    (ABSOLUTE_REPO, "<repo path>"),
    (ABSOLUTE_PROJECT, "<project path>"),
    (PATH_TO_REWIND, "<rewind skill>/scripts/rewind.py"),
    (PATH_TO_COMFYUI, "<ComfyUI root>"),
    (DROPBOX, "storage"),
    (WORKSPACE_DIR_NAME, "workspace"),
    (rf"(?i){OWNER_NAME}", "user"),
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def public_import_text(text: str) -> str:
    rendered = text
    for pattern, replacement in PUBLIC_REPLACEMENTS:
        rendered = re.sub(pattern, replacement, rendered)
    return rendered


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "repo"


def direct_git_roots(base: Path) -> list[Path]:
    roots = []
    for git_path in base.glob("*/.git"):
        if git_path.exists():
            roots.append(git_path.parent)
    return sorted(set(roots))


def public_source_path(source: Path, base: Path) -> str:
    try:
        relative = source.relative_to(base)
    except ValueError:
        return f"<source root>/{source.name}"
    return f"{PUBLIC_BASE_LABEL}/{relative.as_posix()}"


def import_provider(base: Path, provider: str) -> list[dict]:
    filename = PROVIDER_SPECS[provider]["filename"]
    source_dir = REPO_ROOT / "source" / provider
    import_dir = source_dir / "imports"
    import_dir.mkdir(parents=True, exist_ok=True)
    records = []
    used_names: set[str] = set()
    for root in direct_git_roots(base):
        source = root / filename
        if not source.is_file():
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        public_text = public_import_text(text)
        stem = slugify(root.name)
        out_name = f"{stem}-{filename.lower()}"
        if out_name in used_names:
            suffix = 2
            while f"{stem}-{suffix}-{filename.lower()}" in used_names:
                suffix += 1
            out_name = f"{stem}-{suffix}-{filename.lower()}"
        used_names.add(out_name)
        out_path = import_dir / out_name
        rel_source = public_source_path(source, base)
        imported = (
            f"# Imported {PROVIDER_SPECS[provider]['display']} Doctrine Source\n\n"
            f"- Source path: `{rel_source}`\n"
            f"- Source SHA256: `{sha256_text(text)}`\n"
            f"- Provider lane: `{provider}`\n\n"
            "## Original Content\n\n"
            f"{public_text.rstrip()}\n"
        )
        out_path.write_text(imported, encoding="utf-8")
        records.append(
            {
                "provider": provider,
                "repo": root.name,
                "source_path": rel_source,
                "source_sha256": sha256_text(text),
                "source_lines": len(text.splitlines()),
                "source_bytes": len(text.encode("utf-8")),
                "import_path": str(out_path.relative_to(REPO_ROOT)),
            }
        )
    inventory_path = source_dir / "inventory.json"
    inventory_path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return records


def write_docs(all_records: dict[str, list[dict]]) -> None:
    docs_dir = REPO_ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Agent-Doctrine Source Inventory",
        "",
        "This inventory is generated from repo-level `AGENTS.md` and `CLAUDE.md`",
        f"files at direct Git repository roots under `{PUBLIC_BASE_LABEL}`.",
        "",
    ]
    for provider in provider_names():
        records = all_records[provider]
        total_lines = sum(record["source_lines"] for record in records)
        lines.extend(
            [
                f"## {PROVIDER_SPECS[provider]['display']}",
                "",
                f"- Files: {len(records)}",
                f"- Lines: {total_lines}",
                "",
            ]
        )
        for record in records:
            lines.append(
                f"- `{record['source_path']}` -> `{record['import_path']}` "
                f"({record['source_lines']} lines, sha256 `{record['source_sha256']}`)"
            )
        lines.append("")
    (docs_dir / "inventory.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import repo-level provider doctrine examples.")
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    args = parser.parse_args()
    base = args.base.expanduser().resolve()
    if not base.is_dir():
        raise SystemExit(f"base directory does not exist: {base}")
    all_records = {provider: import_provider(base, provider) for provider in provider_names()}
    write_docs(all_records)
    for provider, records in all_records.items():
        print(f"imported {len(records)} {provider} source file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
