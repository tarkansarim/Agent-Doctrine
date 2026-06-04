from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

from doctrine_common import REPO_ROOT, PROVIDER_SPECS, DoctrineError, load_manifest, output_path, render


@dataclass(frozen=True)
class UnmanagedSection:
    label: str
    content: str


def managed_block(provider: str) -> tuple[str, str, str]:
    manifest = load_manifest(provider)
    block = output_path(provider).read_text(encoding="utf-8")
    expected = render(provider)
    if block != expected:
        raise DoctrineError(
            f"{output_path(provider)} is stale; run scripts/generate_{provider}.py first"
        )
    return manifest["managed_start"], manifest["managed_end"], block


def unmanaged_sections(existing: str, start: str, end: str) -> list[UnmanagedSection]:
    start_count = existing.count(start)
    end_count = existing.count(end)
    if start_count != end_count:
        raise DoctrineError("target has unmatched Agent-Doctrine managed markers")
    if start_count > 1:
        raise DoctrineError("target has multiple Agent-Doctrine managed blocks")
    if start_count == 0:
        stripped = existing.strip()
        if not stripped:
            return []
        return [UnmanagedSection("entire file (no Agent-Doctrine managed block)", stripped)]

    start_index = existing.index(start)
    end_index = existing.index(end, start_index) + len(end)
    sections = []
    before = existing[:start_index].strip()
    after = existing[end_index:].strip()
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
) -> str:
    start_count = existing.count(start)
    end_count = existing.count(end)
    if start_count != end_count:
        raise DoctrineError("target has unmatched Agent-Doctrine managed markers")
    if start_count > 1:
        raise DoctrineError("target has multiple Agent-Doctrine managed blocks")
    if discard_unmanaged:
        return block
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
    start, end, block = managed_block(provider)
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    sections = unmanaged_sections(existing, start, end)
    adopted_unmanaged = sections_are_adopted(sections, block) or sections_are_adopted_by_sidecar(provider, sections)
    if sections and not allow_unmanaged_exception and not discard_unmanaged and not adopted_unmanaged:
        raise DoctrineError(format_unmanaged_report(provider, target, sections))
    merged = merge_managed_block(existing, start, end, block, discard_unmanaged=discard_unmanaged or adopted_unmanaged)
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
