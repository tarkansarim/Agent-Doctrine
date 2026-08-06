from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from doctrine_common import REPO_ROOT, PROVIDER_SPECS, DoctrineError, load_manifest, output_path, render


@dataclass(frozen=True)
class UnmanagedSection:
    label: str
    content: str


@dataclass(frozen=True)
class ExternalManagedBlock:
    owner: str
    start: str
    end: str


USERLEVEL_BACKUP_PATTERNS = (
    re.compile(r".*\.bak$"),
    re.compile(r".*\.old$"),
    re.compile(r".*~$"),
    re.compile(r".*\.orig$"),
    re.compile(r".*\.[0-9]{8}.*"),
)


def external_managed_blocks(provider: str) -> list[ExternalManagedBlock]:
    path = REPO_ROOT / "source" / "external-managed-blocks.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        entries = payload["providers"][provider]
    except (FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise DoctrineError(f"invalid external managed-block registry: {path}") from exc
    blocks = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise DoctrineError(f"invalid external managed-block entry for {provider}: {entry!r}")
        owner = entry.get("owner")
        start = entry.get("start")
        end = entry.get("end")
        if not all(isinstance(value, str) and value for value in (owner, start, end)):
            raise DoctrineError(f"invalid external managed-block entry for {provider}: {entry!r}")
        blocks.append(ExternalManagedBlock(owner, start, end))
    return blocks


def external_managed_spans(existing: str, blocks: list[ExternalManagedBlock]) -> list[tuple[int, int]]:
    spans = []
    for block in blocks:
        start_count = existing.count(block.start)
        end_count = existing.count(block.end)
        if start_count != end_count:
            raise DoctrineError(f"target has unmatched {block.owner} managed markers")
        if start_count > 1:
            raise DoctrineError(f"target has multiple {block.owner} managed blocks")
        if start_count == 0:
            continue
        start_index = existing.index(block.start)
        end_index = existing.index(block.end, start_index)
        if end_index <= start_index:
            raise DoctrineError(f"target has reversed {block.owner} managed markers")
        spans.append((start_index, end_index + len(block.end)))
    spans.sort()
    for previous, current in zip(spans, spans[1:]):
        if current[0] < previous[1]:
            raise DoctrineError("target has overlapping registered external managed blocks")
    return spans


def mask_external_managed_blocks(existing: str, spans: list[tuple[int, int]]) -> str:
    if not spans:
        return existing
    parts = []
    cursor = 0
    for start, end in spans:
        parts.append(existing[cursor:start])
        parts.append("".join("\n" if char == "\n" else " " for char in existing[start:end]))
        cursor = end
    parts.append(existing[cursor:])
    return "".join(parts)


def registered_external_blocks(existing: str, provider: str) -> list[str]:
    spans = external_managed_spans(existing, external_managed_blocks(provider))
    return [existing[start:end].strip() for start, end in spans]


def userlevel_backup_artifacts(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.iterdir()
        if any(pattern.match(path.name) for pattern in USERLEVEL_BACKUP_PATTERNS)
    )


def managed_block(provider: str) -> tuple[str, str, str]:
    manifest = load_manifest(provider)
    block = output_path(provider).read_text(encoding="utf-8")
    expected = render(provider)
    if block != expected:
        raise DoctrineError(
            f"{output_path(provider)} is stale; run scripts/generate_{provider}.py first"
        )
    return manifest["managed_start"], manifest["managed_end"], block


def unmanaged_sections(
    existing: str,
    start: str,
    end: str,
    *,
    external_blocks: list[ExternalManagedBlock] | None = None,
) -> list[UnmanagedSection]:
    spans = external_managed_spans(existing, external_blocks or [])
    existing_without_external = mask_external_managed_blocks(existing, spans)
    start_count = existing.count(start)
    end_count = existing.count(end)
    if start_count != end_count:
        raise DoctrineError("target has unmatched Agent-Doctrine managed markers")
    if start_count > 1:
        raise DoctrineError("target has multiple Agent-Doctrine managed blocks")
    if start_count == 0:
        stripped = existing_without_external.strip()
        if not stripped:
            return []
        return [UnmanagedSection("entire file (no Agent-Doctrine managed block)", stripped)]

    start_index = existing.index(start)
    end_index = existing.index(end, start_index) + len(end)
    sections = []
    before = existing_without_external[:start_index].strip()
    after = existing_without_external[end_index:].strip()
    if before:
        sections.append(UnmanagedSection("before Agent-Doctrine managed block", before))
    if after:
        sections.append(UnmanagedSection("after Agent-Doctrine managed block", after))
    return sections


def format_unmanaged_report(provider: str, target: Path, sections: list[UnmanagedSection]) -> str:
    display = PROVIDER_SPECS[provider]["display"]
    lines = [
        f"{display} target contains unmanaged non-empty doctrine outside Agent-Doctrine source: {target}",
        "Agent-Doctrine cannot treat this as normal install-time preservation because user-level doctrine must be recoverable from source.",
        "Choose one explicit resolution:",
        "  1. adopt/import the unmanaged doctrine into Agent-Doctrine source, regenerate, validate, then reinstall",
        "  2. discard unmanaged deployed doctrine with --discard-unmanaged",
        "  3. keep it only as a temporary unmanaged exception with --allow-unmanaged-exception",
        "Unmanaged sections:",
    ]
    for index, section in enumerate(sections, 1):
        lines.extend(
            [
                f"--- unmanaged section {index}: {section.label} ---",
                section.content,
                f"--- end unmanaged section {index} ---",
            ]
        )
    return "\n".join(lines)


def adopted_section_token(section: UnmanagedSection) -> str:
    digest = hashlib.sha256(section.content.encode("utf-8")).hexdigest()
    return f"Adopted install SHA256: `{digest}`"


def sections_are_adopted(sections: list[UnmanagedSection], block: str) -> bool:
    normalized_block = block.lower()
    return bool(sections) and all(adopted_section_token(section).lower() in normalized_block for section in sections)


def adoption_manifest_hashes(provider: str) -> set[str]:
    manifest = load_manifest(provider)
    live_adoption = manifest.get("live_adoption")
    if not isinstance(live_adoption, dict):
        return set()
    manifest_rel = live_adoption.get("manifest")
    if not isinstance(manifest_rel, str) or not manifest_rel:
        return set()
    manifest_path = REPO_ROOT / "source" / provider / manifest_rel
    if not manifest_path.is_file():
        return set()
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    hashes = set()
    for key in (
        "adopted_install_sha256",
        "reply_verbosity_relay_adopted_install_sha256",
    ):
        value = data.get(key)
        if isinstance(value, str) and value:
            hashes.add(value.lower())
    return hashes


def sections_are_adopted_by_sidecar(provider: str, sections: list[UnmanagedSection]) -> bool:
    hashes = adoption_manifest_hashes(provider)
    return bool(sections) and bool(hashes) and all(
        hashlib.sha256(section.content.encode("utf-8")).hexdigest().lower() in hashes
        for section in sections
    )


def merge_managed_block(
    existing: str,
    start: str,
    end: str,
    block: str,
    *,
    discard_unmanaged: bool = False,
    external_blocks: list[str] | None = None,
) -> str:
    start_count = existing.count(start)
    end_count = existing.count(end)
    if start_count != end_count:
        raise DoctrineError("target has unmatched Agent-Doctrine managed markers")
    if start_count > 1:
        raise DoctrineError("target has multiple Agent-Doctrine managed blocks")
    if discard_unmanaged:
        preserved = [item for item in (external_blocks or []) if item]
        if not preserved:
            return block
        return block.rstrip() + "\n\n" + "\n\n".join(preserved) + "\n"
    if start_count == 0:
        prefix = existing.rstrip()
        if prefix:
            return prefix + "\n\n" + block
        return block
    start_index = existing.index(start)
    end_index = existing.index(end, start_index) + len(end)
    merged = existing[:start_index] + block.rstrip() + existing[end_index:]
    return merged.rstrip() + "\n"


def install_provider(
    provider: str,
    target_root: Path | None = None,
    target_file: Path | None = None,
    *,
    allow_unmanaged_exception: bool = False,
    discard_unmanaged: bool = False,
) -> Path:
    if allow_unmanaged_exception and discard_unmanaged:
        raise DoctrineError("--allow-unmanaged-exception and --discard-unmanaged are mutually exclusive")
    spec = PROVIDER_SPECS[provider]
    root = (target_root or spec["default_root"]).expanduser()
    target = (target_file.expanduser() if target_file else root / spec["filename"]).resolve()
    if target.name != spec["filename"]:
        raise DoctrineError(f"{provider} target must be named {spec['filename']}: {target}")
    if target.exists() and target.is_symlink():
        raise DoctrineError(f"refusing to replace symlink target: {target} -> {target.readlink()}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.parent.is_symlink():
        raise DoctrineError(f"refusing to install into symlink directory: {target.parent}")
    backup_artifacts = userlevel_backup_artifacts(root)
    if backup_artifacts:
        formatted = "\n".join(f"  - {path}" for path in backup_artifacts)
        raise DoctrineError(
            f"refusing to install with backup artifacts inside user-level provider root {root}:\n"
            f"{formatted}\n"
            "Move them to a cache/backup path outside the provider root first."
        )
    start, end, block = managed_block(provider)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    registered_blocks = external_managed_blocks(provider)
    sections = unmanaged_sections(existing, start, end, external_blocks=registered_blocks)
    adopted_unmanaged = sections_are_adopted(sections, block) or sections_are_adopted_by_sidecar(provider, sections)
    if sections and not allow_unmanaged_exception and not discard_unmanaged and not adopted_unmanaged:
        raise DoctrineError(format_unmanaged_report(provider, target, sections))
    merged = merge_managed_block(
        existing,
        start,
        end,
        block,
        discard_unmanaged=discard_unmanaged or adopted_unmanaged,
        external_blocks=registered_external_blocks(existing, provider),
    )
    tmp = target.with_name(f".{target.name}.agent-doctrine-new")
    try:
        tmp.write_text(merged, encoding="utf-8")
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()
    return target


def parser_for(provider: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"Install generated {provider} doctrine.")
    parser.add_argument("--target-root", type=Path, default=None)
    parser.add_argument("--target-file", type=Path, default=None)
    decision = parser.add_mutually_exclusive_group()
    decision.add_argument(
        "--allow-unmanaged-exception",
        action="store_true",
        help="Temporarily preserve unmanaged non-empty deployed doctrine outside Agent-Doctrine markers.",
    )
    decision.add_argument(
        "--discard-unmanaged",
        action="store_true",
        help="Discard unmanaged non-empty deployed doctrine and install only the Agent-Doctrine managed block.",
    )
    return parser


def main_for(provider: str, argv: list[str] | None = None) -> int:
    parser = parser_for(provider)
    args = parser.parse_args(argv)
    try:
        target = install_provider(
            provider,
            args.target_root,
            args.target_file,
            allow_unmanaged_exception=args.allow_unmanaged_exception,
            discard_unmanaged=args.discard_unmanaged,
        )
    except DoctrineError as exc:
        parser.error(str(exc))
    print(f"installed {provider} doctrine: {target}")
    print(f"source: {output_path(provider)}")
    if args.allow_unmanaged_exception:
        print("unmanaged doctrine exception: preserved temporarily by explicit request")
    if args.discard_unmanaged:
        print("unmanaged doctrine: discarded by explicit request")
    return 0
