from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PROVIDER_SPECS = {
    "codex": {
        "display": "Codex",
        "filename": "AGENTS.md",
        "default_root": Path.home() / ".codex",
    },
    "claude": {
        "display": "Claude",
        "filename": "CLAUDE.md",
        "default_root": Path.home() / ".claude",
    },
}


class DoctrineError(RuntimeError):
    pass


def provider_names() -> tuple[str, ...]:
    return tuple(PROVIDER_SPECS)


def provider_dir(provider: str) -> Path:
    _require_provider(provider)
    return REPO_ROOT / "source" / provider


def manifest_path(provider: str) -> Path:
    return provider_dir(provider) / "manifest.json"


def load_manifest(provider: str) -> dict:
    path = manifest_path(provider)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DoctrineError(f"missing manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DoctrineError(f"invalid JSON manifest {path}: {exc}") from exc
    if manifest.get("provider") != provider:
        raise DoctrineError(f"{path} provider must be {provider!r}")
    return manifest


def output_path(provider: str) -> Path:
    manifest = load_manifest(provider)
    return REPO_ROOT / manifest["output"]


def module_paths(provider: str) -> list[Path]:
    manifest = load_manifest(provider)
    base = provider_dir(provider)
    paths = []
    for rel in manifest.get("modules", []):
        path = base / rel
        if not path.is_file():
            raise DoctrineError(f"missing module for {provider}: {path}")
        paths.append(path)
    if not paths:
        raise DoctrineError(f"{provider} manifest has no modules")
    return paths


def render(provider: str) -> str:
    _require_provider(provider)
    manifest = load_manifest(provider)
    start = manifest["managed_start"]
    end = manifest["managed_end"]
    parts = [start]
    for path in module_paths(provider):
        parts.append(path.read_text(encoding="utf-8").rstrip())
        parts.append("")
    parts.append(end)
    return "\n".join(parts).rstrip() + "\n"


def write_generated(provider: str) -> Path:
    path = output_path(provider)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = render(provider)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return path
    path.write_text(content, encoding="utf-8")
    return path


def _require_provider(provider: str) -> None:
    if provider not in PROVIDER_SPECS:
        allowed = ", ".join(provider_names())
        raise DoctrineError(f"unknown provider {provider!r}; expected one of: {allowed}")
