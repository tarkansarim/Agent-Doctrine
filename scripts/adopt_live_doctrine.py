from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from doctrine_common import PROVIDER_SPECS, REPO_ROOT, DoctrineError, load_manifest, provider_names


ADOPTED_SNAPSHOT_DIR = "adopted"
ADOPTION_MANIFEST = "adopted/adoption-manifest.json"
REPLY_VERBOSITY_START = "<!-- BEGIN: reply-verbosity (managed by install.sh) -->"
REPLY_VERBOSITY_END = "<!-- END: reply-verbosity (managed by install.sh) -->"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def live_target(provider: str, target_root: Path | None, target_file: Path | None) -> Path:
    spec = PROVIDER_SPECS[provider]
    if target_file is not None:
        target = target_file.expanduser().resolve()
    else:
        root = (target_root or spec["default_root"]).expanduser()
        target = (root / spec["filename"]).resolve()
    if target.name != spec["filename"]:
        raise DoctrineError(f"{provider} target must be named {spec['filename']}: {target}")
    return target


def decode_doctrine_bytes(provider: str, path: Path, data: bytes) -> tuple[str, str]:
    if not data.strip():
        raise DoctrineError(f"{provider} doctrine file is empty: {path}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DoctrineError(f"{provider} doctrine file is not UTF-8: {path}: {exc}") from exc
    return text, sha256_bytes(data)


def existing_snapshot(provider: str) -> Path | None:
    manifest = load_manifest(provider)
    live_adoption = manifest.get("live_adoption")
    if not isinstance(live_adoption, dict):
        return None
    snapshot = live_adoption.get("snapshot")
    if not isinstance(snapshot, str) or not snapshot:
        return None
    return REPO_ROOT / "source" / provider / snapshot


def read_live_file(provider: str, target: Path) -> tuple[str, bytes, str]:
    if not target.is_file():
        raise DoctrineError(f"{provider} live doctrine file does not exist: {target}")
    data = target.read_bytes()
    text, source_sha256 = decode_doctrine_bytes(provider, target, data)
    manifest = load_manifest(provider)
    if manifest["managed_start"] in text or manifest["managed_end"] in text:
        snapshot = existing_snapshot(provider)
        if snapshot is None or not snapshot.is_file():
            raise DoctrineError(
                f"{provider} live doctrine already contains Agent-Doctrine managed markers and no "
                "existing live_adoption snapshot is available; adopt unmanaged sections separately"
            )
        snapshot_data = snapshot.read_bytes()
        snapshot_text, snapshot_sha256 = decode_doctrine_bytes(provider, snapshot, snapshot_data)
        if manifest["managed_start"] in snapshot_text or manifest["managed_end"] in snapshot_text:
            raise DoctrineError(f"{provider} live_adoption snapshot contains Agent-Doctrine managed markers: {snapshot}")
        return snapshot_text, snapshot_data, snapshot_sha256
    return text, data, source_sha256


def reply_verbosity_digest(text: str) -> str | None:
    try:
        start = text.index(REPLY_VERBOSITY_START)
        end = text.index(REPLY_VERBOSITY_END, start) + len(REPLY_VERBOSITY_END)
    except ValueError:
        return None
    return sha256_text(text[start:end])


def build_adoption_manifest(
    provider: str,
    target: Path,
    text: str,
    source_sha256: str,
    snapshot_rel: str,
) -> str:
    spec = PROVIDER_SPECS[provider]
    public_source_path = f"<{provider} config>/{spec['filename']}"
    manifest = {
        "provider": provider,
        "filename": spec["filename"],
        "source_path": public_source_path,
        "adopted_snapshot": f"source/{provider}/{snapshot_rel}",
        "adopted_source_sha256": source_sha256,
        "adopted_install_sha256": sha256_text(text.strip()),
        "reply_verbosity_relay_adopted_install_sha256": reply_verbosity_digest(text),
        "provider_lane": provider,
        "adoption_scope": "explicit live user-level doctrine import",
        "runtime_loaded": False,
        "note": (
            "The exact adopted baseline remains recoverable from the snapshot path. "
            "This manifest is source-side audit metadata, not inline runtime doctrine."
        ),
    }
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def write_if_changed(path: Path, content: str | bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        if path.exists() and path.read_bytes() == content:
            return False
        path.write_bytes(content)
        return True
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def update_manifest(provider: str, snapshot_rel: str, source_sha256: str) -> bool:
    path = REPO_ROOT / "source" / provider / "manifest.json"
    manifest = load_manifest(provider)
    manifest["modules"] = [
        module
        for module in manifest.get("modules", [])
        if module != "modules/000-adopted-live-user-level.md"
    ]
    manifest["live_adoption"] = {
        "snapshot": snapshot_rel,
        "source_sha256": source_sha256,
        "manifest": ADOPTION_MANIFEST,
    }
    rendered = json.dumps(manifest, indent=2) + "\n"
    if path.read_text(encoding="utf-8") == rendered:
        return False
    path.write_text(rendered, encoding="utf-8")
    return True


def adopt_provider(provider: str, target_root: Path | None = None, target_file: Path | None = None) -> dict:
    target = live_target(provider, target_root, target_file)
    text, data, source_sha256 = read_live_file(provider, target)
    spec = PROVIDER_SPECS[provider]
    source_dir = REPO_ROOT / "source" / provider
    snapshot_rel = f"{ADOPTED_SNAPSHOT_DIR}/live-user-level-{spec['filename']}"
    snapshot_path = source_dir / snapshot_rel
    adoption_manifest_path = source_dir / ADOPTION_MANIFEST
    adoption_manifest_changed = write_if_changed(
        adoption_manifest_path,
        build_adoption_manifest(provider, target, text, source_sha256, snapshot_rel),
    )
    snapshot_changed = write_if_changed(snapshot_path, data)
    manifest_changed = update_manifest(provider, snapshot_rel, source_sha256)
    return {
        "provider": provider,
        "target": str(target),
        "source_sha256": source_sha256,
        "source_bytes": len(data),
        "source_lines": len(text.splitlines()),
        "adoption_manifest": str(adoption_manifest_path.relative_to(REPO_ROOT)),
        "snapshot": str(snapshot_path.relative_to(REPO_ROOT)),
        "changed": adoption_manifest_changed or snapshot_changed or manifest_changed,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Adopt existing live user-level provider doctrine into Agent-Doctrine source.")
    parser.add_argument(
        "--provider",
        choices=provider_names(),
        action="append",
        help="Provider to adopt. Repeat for both providers. Defaults to all providers.",
    )
    parser.add_argument("--target-root", type=Path, default=None)
    parser.add_argument("--target-file", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.target_root is not None and len(args.provider or provider_names()) != 1:
        raise SystemExit("--target-root can only be used with exactly one --provider")
    if args.target_file is not None and len(args.provider or provider_names()) != 1:
        raise SystemExit("--target-file can only be used with exactly one --provider")
    providers = tuple(args.provider) if args.provider else provider_names()
    try:
        results = [adopt_provider(provider, args.target_root, args.target_file) for provider in providers]
    except DoctrineError as exc:
        raise SystemExit(str(exc)) from exc
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for result in results:
            state = "updated" if result["changed"] else "unchanged"
            print(
                f"adopted {result['provider']} live doctrine: {state}; "
                f"sha256={result['source_sha256']} "
                f"manifest={result['adoption_manifest']} snapshot={result['snapshot']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
