from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from doctrine_common import (
    PROVIDER_SPECS,
    REPO_ROOT,
    RULE_MARKER_RE,
    DoctrineError,
    load_manifest,
    module_paths,
    output_path,
    provider_names,
    render,
)
from import_repo_doctrine import DEFAULT_BASE, direct_git_roots, public_source_path


BACKUP_PATTERNS = (
    re.compile(r".*\.bak$"),
    re.compile(r".*\.old$"),
    re.compile(r".*~$"),
    re.compile(r".*\.orig$"),
    re.compile(r".*\.[0-9]{8}.*"),
)

TODO_MARKER = re.compile(r"(?m)(^|\s)(TODO:|\[TODO\b|<TODO\b)")
PLACEHOLDER_MARKER = re.compile(r"(?i)(\[placeholder\]|<placeholder>|placeholder text)")
GENERATED_MAX_LINES = 180
GENERATED_MAX_TOKENS = 2500
GENERATED_FORBIDDEN_INLINE_MARKERS = (
    "Generated from Agent-Doctrine source modules",
    "Source inputs:",
    "# Adopted Live User-Level",
    "Adopted source SHA256",
    "Adopted install SHA256",
    "## Original Live Doctrine Content",
    "<!-- rewind-checkpoints-trigger:begin -->",
    "## Rewind Hook Baselines",
    "<!-- agent-self-improvement:begin -->",
    "## Agent Self-Improvement",
    "<!-- agent-self-improvement-doctrine:begin -->",
    "## Accepted Self-Improvement Doctrine",
    "<!-- thrash-reporting-install:begin -->",
    "## Thrash Reporting",
    "<!-- BEGIN: reply-verbosity",
    "# Reply Verbosity (always-on)",
    "## Verbosity Tiers",
    "## Technicality",
    "starter Pressure-Lab lane",
    "pressure-lab suggest hardening",
    "<!-- agent-doctrine-rule:",
)
RULE_REGISTRY_PATH = REPO_ROOT / "source" / "rule-provenance.json"
RULE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
ALLOWED_PROMOTIONS = {"provider-general", "provider-specific"}
OWNER_DERIVED_ORIGIN_KINDS = {
    "owner-contract-reconciliation",
    "promoted-owner-contract",
    "shared-contract-reconciliation",
}


@dataclass(frozen=True)
class Violation:
    path: Path
    message: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def lexical_token_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def validate_generated_budget(path: Path, text: str) -> list[Violation]:
    violations: list[Violation] = []
    line_count = len(text.splitlines())
    if line_count > GENERATED_MAX_LINES:
        violations.append(
            Violation(
                path,
                f"generated output has {line_count} lines; budget is {GENERATED_MAX_LINES}",
            )
        )
    token_count = lexical_token_count(text)
    if token_count > GENERATED_MAX_TOKENS:
        violations.append(
            Violation(
                path,
                f"generated output has {token_count} lexical tokens; budget is {GENERATED_MAX_TOKENS}",
            )
        )
    return violations


def validate_no_inlined_skill_duplicates(path: Path, text: str) -> list[Violation]:
    violations: list[Violation] = []
    for marker in GENERATED_FORBIDDEN_INLINE_MARKERS:
        if marker in text:
            violations.append(
                Violation(
                    path,
                    f"generated output re-inlines skill-owned detail marked by {marker!r}",
                )
            )
    return violations


def load_rule_registry() -> tuple[dict | None, list[Violation]]:
    try:
        data = json.loads(RULE_REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [Violation(RULE_REGISTRY_PATH, "rule provenance registry is missing")]
    except json.JSONDecodeError as exc:
        return None, [Violation(RULE_REGISTRY_PATH, f"invalid rule provenance JSON: {exc}")]
    if not isinstance(data, dict):
        return None, [Violation(RULE_REGISTRY_PATH, "rule provenance registry must be a JSON object")]
    return data, []


def validate_rule_registry() -> list[Violation]:
    registry, violations = load_rule_registry()
    if registry is None:
        return violations

    if registry.get("schema_version") != 1:
        violations.append(Violation(RULE_REGISTRY_PATH, "schema_version must be 1"))
    owner = registry.get("doctrine_owner")
    if not isinstance(owner, dict) or owner.get("repo") != "Agent-Doctrine" or owner.get("path") != "source":
        violations.append(
            Violation(
                RULE_REGISTRY_PATH,
                "doctrine_owner must identify Agent-Doctrine source",
            )
        )

    origins = registry.get("origins")
    if not isinstance(origins, dict) or not origins:
        violations.append(Violation(RULE_REGISTRY_PATH, "origins must be a non-empty object"))
        origins = {}
    else:
        for origin_id, origin in origins.items():
            if not RULE_ID_RE.fullmatch(origin_id) or not isinstance(origin, dict):
                violations.append(Violation(RULE_REGISTRY_PATH, f"invalid origin entry {origin_id!r}"))
                continue
            for field in ("kind", "reference", "certainty"):
                if not isinstance(origin.get(field), str) or not origin[field].strip():
                    violations.append(
                        Violation(
                            RULE_REGISTRY_PATH,
                            f"origin {origin_id!r} requires non-empty {field}",
                        )
                    )

    rules = registry.get("rules")
    if not isinstance(rules, dict) or not rules:
        violations.append(Violation(RULE_REGISTRY_PATH, "rules must be a non-empty object"))
        rules = {}
    else:
        for rule_id, metadata in rules.items():
            if not RULE_ID_RE.fullmatch(rule_id):
                violations.append(Violation(RULE_REGISTRY_PATH, f"invalid rule id {rule_id!r}"))
                continue
            if not isinstance(metadata, dict):
                violations.append(Violation(RULE_REGISTRY_PATH, f"rule {rule_id!r} metadata must be an object"))
                continue
            if not isinstance(metadata.get("title"), str) or not metadata["title"].strip():
                violations.append(Violation(RULE_REGISTRY_PATH, f"rule {rule_id!r} requires a title"))
            providers = metadata.get("providers")
            if (
                not isinstance(providers, list)
                or not providers
                or len(providers) != len(set(providers))
                or any(provider not in PROVIDER_SPECS for provider in providers)
            ):
                violations.append(
                    Violation(
                        RULE_REGISTRY_PATH,
                        f"rule {rule_id!r} has invalid providers",
                    )
                )
            if metadata.get("promotion") not in ALLOWED_PROMOTIONS:
                violations.append(
                    Violation(
                        RULE_REGISTRY_PATH,
                        f"rule {rule_id!r} promotion must be provider-general or provider-specific",
                    )
                )
            if metadata.get("origin") not in origins:
                violations.append(
                    Violation(
                        RULE_REGISTRY_PATH,
                        f"rule {rule_id!r} references an unknown origin",
                    )
                )
            if not isinstance(metadata.get("override_status"), str) or not metadata["override_status"].strip():
                violations.append(
                    Violation(
                        RULE_REGISTRY_PATH,
                        f"rule {rule_id!r} requires override_status",
                    )
                )

    contracts = registry.get("owner_contracts")
    if not isinstance(contracts, list):
        violations.append(Violation(RULE_REGISTRY_PATH, "owner_contracts must be a list"))
        return violations
    seen_contract_ids: set[str] = set()
    owner_checked_rule_ids: set[str] = set()
    for contract in contracts:
        if not isinstance(contract, dict):
            violations.append(Violation(RULE_REGISTRY_PATH, "owner contract entries must be objects"))
            continue
        contract_id = contract.get("id")
        if not isinstance(contract_id, str) or not RULE_ID_RE.fullmatch(contract_id):
            violations.append(Violation(RULE_REGISTRY_PATH, "owner contract requires a valid id"))
        elif contract_id in seen_contract_ids:
            violations.append(Violation(RULE_REGISTRY_PATH, f"duplicate owner contract id {contract_id!r}"))
        else:
            seen_contract_ids.add(contract_id)
        for field in ("repo", "path"):
            if not isinstance(contract.get(field), str) or not contract[field].strip():
                violations.append(Violation(RULE_REGISTRY_PATH, f"owner contract {contract_id!r} requires {field}"))
        rule_ids = contract.get("rule_ids")
        if not isinstance(rule_ids, list) or not rule_ids:
            violations.append(Violation(RULE_REGISTRY_PATH, f"owner contract {contract_id!r} requires rule_ids"))
        else:
            for rule_id in rule_ids:
                if rule_id not in rules:
                    violations.append(
                        Violation(
                            RULE_REGISTRY_PATH,
                            f"owner contract {contract_id!r} references unknown rule {rule_id!r}",
                        )
                    )
                else:
                    owner_checked_rule_ids.add(rule_id)
        for field in ("required_fragments", "forbidden_fragments"):
            fragments = contract.get(field)
            if not isinstance(fragments, list) or any(
                not isinstance(fragment, str) or not fragment.strip() for fragment in fragments
            ):
                violations.append(
                    Violation(
                        RULE_REGISTRY_PATH,
                        f"owner contract {contract_id!r} requires a string list for {field}",
                    )
                )

    for rule_id, metadata in rules.items():
        if not isinstance(metadata, dict):
            continue
        origin = origins.get(metadata.get("origin"))
        if (
            isinstance(origin, dict)
            and origin.get("kind") in OWNER_DERIVED_ORIGIN_KINDS
            and rule_id not in owner_checked_rule_ids
        ):
            violations.append(
                Violation(
                    RULE_REGISTRY_PATH,
                    f"owner-derived rule {rule_id!r} requires an owner_contract check",
                )
            )
    return violations


def validate_provider_rule_markers(provider: str) -> list[Violation]:
    registry, violations = load_rule_registry()
    if registry is None:
        return violations
    rules = registry.get("rules")
    if not isinstance(rules, dict):
        return violations

    occurrences: dict[str, list[tuple[Path, int]]] = {}
    for path in module_paths(provider):
        pending: tuple[str, int] | None = None
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            marker = RULE_MARKER_RE.fullmatch(line)
            if marker:
                if pending is not None:
                    violations.append(
                        Violation(
                            path,
                            f"rule marker on line {pending[1]} is not followed immediately by a top-level rule",
                        )
                    )
                pending = (marker.group(1), line_number)
                continue
            if line.startswith("- "):
                if pending is None:
                    violations.append(
                        Violation(
                            path,
                            f"top-level rule on line {line_number} is missing a provenance marker",
                        )
                    )
                else:
                    occurrences.setdefault(pending[0], []).append((path, line_number))
                    pending = None
                continue
            if pending is not None:
                violations.append(
                    Violation(
                        path,
                        f"rule marker on line {pending[1]} is not followed immediately by a top-level rule",
                    )
                )
                pending = None
        if pending is not None:
            violations.append(
                Violation(
                    path,
                    f"rule marker on line {pending[1]} has no top-level rule",
                )
            )

    for rule_id, locations in occurrences.items():
        if len(locations) > 1:
            rendered = ", ".join(f"{path.name}:{line}" for path, line in locations)
            violations.append(
                Violation(
                    RULE_REGISTRY_PATH,
                    f"rule {rule_id!r} occurs more than once for {provider}: {rendered}",
                )
            )
        if rule_id not in rules:
            path, line = locations[0]
            violations.append(Violation(path, f"rule marker {rule_id!r} on line {line - 1} is not registered"))

    expected = {
        rule_id
        for rule_id, metadata in rules.items()
        if isinstance(metadata, dict)
        and isinstance(metadata.get("providers"), list)
        and provider in metadata["providers"]
    }
    actual = set(occurrences)
    for rule_id in sorted(expected - actual):
        violations.append(
            Violation(
                RULE_REGISTRY_PATH,
                f"registered rule {rule_id!r} is missing from the {provider} source modules",
            )
        )
    for rule_id in sorted(actual - expected):
        violations.append(
            Violation(
                RULE_REGISTRY_PATH,
                f"rule {rule_id!r} appears in {provider} but its provider metadata does not include {provider}",
            )
        )
    return violations


def validate_owner_contracts(owner_root: Path | None = None) -> list[Violation]:
    registry, violations = load_rule_registry()
    if registry is None:
        return violations
    contracts = registry.get("owner_contracts")
    if not isinstance(contracts, list):
        return violations
    if owner_root is None:
        owner_root = Path(os.environ.get("AGENT_DOCTRINE_OWNER_ROOT", REPO_ROOT.parent))

    for contract in contracts:
        if not isinstance(contract, dict):
            continue
        repo_name = contract.get("repo")
        relative_path = contract.get("path")
        if not isinstance(repo_name, str) or not isinstance(relative_path, str):
            continue
        repo_path = owner_root / repo_name
        if not repo_path.is_dir():
            continue
        contract_path = repo_path / relative_path
        if not contract_path.is_file():
            violations.append(
                Violation(
                    contract_path,
                    f"owner contract {contract.get('id')!r} source file is missing",
                )
            )
            continue
        normalized = " ".join(contract_path.read_text(encoding="utf-8").split())
        for fragment in contract.get("required_fragments", []):
            if " ".join(fragment.split()) not in normalized:
                violations.append(
                    Violation(
                        contract_path,
                        f"owner contract {contract.get('id')!r} is missing required fragment {fragment!r}",
                    )
                )
        for fragment in contract.get("forbidden_fragments", []):
            if " ".join(fragment.split()) in normalized:
                violations.append(
                    Violation(
                        contract_path,
                        f"owner contract {contract.get('id')!r} contains forbidden fragment {fragment!r}",
                    )
                )
    return violations


def collect_expected_imports(provider: str, base: Path = DEFAULT_BASE) -> list[dict]:
    filename = PROVIDER_SPECS[provider]["filename"]
    records = []
    used_names: set[str] = set()
    for root in direct_git_roots(base):
        source = root / filename
        if not source.is_file():
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        stem = re.sub(r"[^a-zA-Z0-9]+", "-", root.name).strip("-").lower() or "repo"
        out_name = f"{stem}-{filename.lower()}"
        if out_name in used_names:
            suffix = 2
            while f"{stem}-{suffix}-{filename.lower()}" in used_names:
                suffix += 1
            out_name = f"{stem}-{suffix}-{filename.lower()}"
        used_names.add(out_name)
        import_path = Path("source") / provider / "imports" / out_name
        records.append(
            {
                "provider": provider,
                "repo": root.name,
                "source_path": public_source_path(source, base),
                "source_sha256": sha256_text(text),
                "source_lines": len(text.splitlines()),
                "source_bytes": len(text.encode("utf-8")),
                "import_path": str(import_path),
            }
        )
    return records


def live_inventory_available(base: Path = DEFAULT_BASE) -> bool:
    return "AGENT_DOCTRINE_WORKSPACE_ROOT" in os.environ and base.is_dir()


def validate_provider(provider: str) -> list[Violation]:
    violations: list[Violation] = []
    try:
        manifest = load_manifest(provider)
        modules = module_paths(provider)
    except DoctrineError as exc:
        return [Violation(REPO_ROOT / "source" / provider, str(exc))]

    if Path(manifest["output"]) != Path("generated") / provider / PROVIDER_SPECS[provider]["filename"]:
        violations.append(Violation(REPO_ROOT / manifest["output"], "provider output path is not isolated"))
    if manifest["managed_start"].count(provider) != 1 or manifest["managed_end"].count(provider) != 1:
        violations.append(Violation(REPO_ROOT / "source" / provider / "manifest.json", "managed markers must be provider-specific"))
    for path in modules:
        text = path.read_text(encoding="utf-8")
        if TODO_MARKER.search(text) or PLACEHOLDER_MARKER.search(text):
            violations.append(Violation(path, "module contains unresolved TODO or placeholder marker"))
    violations.extend(validate_provider_rule_markers(provider))

    generated = output_path(provider)
    expected = render(provider)
    if not generated.is_file():
        violations.append(Violation(generated, "generated output is missing"))
    elif generated.read_text(encoding="utf-8") != expected:
        violations.append(Violation(generated, "generated output is stale; rerun generator"))
    else:
        text = generated.read_text(encoding="utf-8")
        if text.count(manifest["managed_start"]) != 1 or text.count(manifest["managed_end"]) != 1:
            violations.append(Violation(generated, "generated output must contain exactly one managed block"))
        violations.extend(validate_generated_budget(generated, text))
        violations.extend(validate_no_inlined_skill_duplicates(generated, text))

    inventory_path = REPO_ROOT / "source" / provider / "inventory.json"
    if not inventory_path.is_file():
        violations.append(Violation(inventory_path, "provider inventory is missing; run import_repo_doctrine.py"))
    else:
        try:
            actual = json.loads(inventory_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(Violation(inventory_path, f"invalid inventory JSON: {exc}"))
            actual = []
        if live_inventory_available():
            expected_records = collect_expected_imports(provider)
            if actual != expected_records:
                violations.append(Violation(inventory_path, "inventory does not match current repo-level source files"))
        for record in actual:
            import_path = REPO_ROOT / record.get("import_path", "")
            if not import_path.is_file():
                violations.append(Violation(import_path, "import file listed in inventory is missing"))
                continue
            import_text = import_path.read_text(encoding="utf-8")
            if record.get("source_sha256", "") not in import_text:
                violations.append(Violation(import_path, "import file missing recorded source hash"))
            if record.get("source_path", "") not in import_text:
                violations.append(Violation(import_path, "import file missing recorded source path"))
    live_adoption = manifest.get("live_adoption")
    if live_adoption is not None:
        snapshot = live_adoption.get("snapshot")
        expected_sha = live_adoption.get("source_sha256")
        if not isinstance(snapshot, str) or not snapshot:
            violations.append(Violation(REPO_ROOT / "source" / provider / "manifest.json", "live_adoption snapshot is missing"))
        elif not isinstance(expected_sha, str) or not expected_sha:
            violations.append(Violation(REPO_ROOT / "source" / provider / "manifest.json", "live_adoption source_sha256 is missing"))
        else:
            snapshot_path = REPO_ROOT / "source" / provider / snapshot
            if not snapshot_path.is_file():
                violations.append(Violation(snapshot_path, "live adoption snapshot is missing"))
            else:
                actual_sha = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
                if actual_sha != expected_sha:
                    violations.append(Violation(snapshot_path, "live adoption snapshot SHA does not match manifest"))
            adoption_manifest = live_adoption.get("manifest")
            if not isinstance(adoption_manifest, str) or not adoption_manifest:
                violations.append(Violation(REPO_ROOT / "source" / provider / "manifest.json", "live adoption manifest is missing"))
            else:
                adoption_manifest_path = REPO_ROOT / "source" / provider / adoption_manifest
                if not adoption_manifest_path.is_file():
                    violations.append(Violation(adoption_manifest_path, "live adoption manifest is missing"))
                else:
                    try:
                        adoption_data = json.loads(adoption_manifest_path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError as exc:
                        violations.append(Violation(adoption_manifest_path, f"invalid live adoption manifest JSON: {exc}"))
                    else:
                        if adoption_data.get("adopted_source_sha256") != expected_sha:
                            violations.append(Violation(adoption_manifest_path, "live adoption manifest source SHA does not match provider manifest"))
                        if adoption_data.get("adopted_snapshot") != f"source/{provider}/{snapshot}":
                            violations.append(Violation(adoption_manifest_path, "live adoption manifest snapshot path does not match provider manifest"))
                        if adoption_data.get("runtime_loaded") is not False:
                            violations.append(Violation(adoption_manifest_path, "live adoption manifest must be marked runtime_loaded=false"))
    ledger_path = REPO_ROOT / "source" / provider / "ledgers" / "self-improvement-doctrine.md"
    if not ledger_path.is_file():
        violations.append(Violation(ledger_path, "self-improvement doctrine ledger is missing"))
    return violations


def validate_skill_source() -> list[Violation]:
    package = REPO_ROOT / "package" / "agent-doctrine-router"
    violations: list[Violation] = []
    skill_files = sorted(package.rglob("SKILL.md")) if package.exists() else []
    if skill_files != [package / "SKILL.md"]:
        violations.append(Violation(package, "skill package must contain exactly one top-level SKILL.md"))
        return violations
    text = (package / "SKILL.md").read_text(encoding="utf-8")
    if TODO_MARKER.search(text) or PLACEHOLDER_MARKER.search(text):
        violations.append(Violation(package / "SKILL.md", "skill contains unresolved TODO or placeholder marker"))
    if not text.startswith("---\n"):
        violations.append(Violation(package / "SKILL.md", "skill frontmatter is missing"))
    frontmatter_end = text.find("\n---\n", 4)
    if frontmatter_end == -1:
        violations.append(Violation(package / "SKILL.md", "skill frontmatter is not closed"))
    else:
        frontmatter = text[4:frontmatter_end]
        if "name: agent-doctrine-router" not in frontmatter:
            violations.append(Violation(package / "SKILL.md", "skill name must match directory"))
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        if not desc_match:
            violations.append(Violation(package / "SKILL.md", "skill description is missing"))
        elif len(desc_match.group(1).strip().strip('"')) > 300:
            violations.append(Violation(package / "SKILL.md", "skill description exceeds 300 characters"))
    openai_yaml = package / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        violations.append(Violation(openai_yaml, "agents/openai.yaml is missing"))
    elif "TODO" in openai_yaml.read_text(encoding="utf-8"):
        violations.append(Violation(openai_yaml, "agents/openai.yaml contains TODO"))
    violations.extend(validate_no_bad_files(package, installed=False))
    return violations


def validate_claude_repo_write_guard_source() -> list[Violation]:
    package = REPO_ROOT / "package" / "claude-repo-write-guard"
    violations: list[Violation] = []
    hook = package / "repo_write_guard.py"
    if not hook.is_file():
        return [Violation(hook, "Claude repo write guard hook source is missing")]
    text = hook.read_text(encoding="utf-8")
    if TODO_MARKER.search(text) or PLACEHOLDER_MARKER.search(text):
        violations.append(Violation(hook, "hook contains unresolved TODO or placeholder marker"))
    if "BLOCK_EXIT_CODE = 2" not in text:
        violations.append(Violation(hook, "PreToolUse guard must fail closed with blocking exit code 2"))
    if "Write" not in text or "Edit" not in text:
        violations.append(Violation(hook, "guard must explicitly target Write and Edit"))
    violations.extend(validate_no_bad_files(package, installed=False))
    return violations


def validate_no_bad_files(root: Path, installed: bool) -> list[Violation]:
    violations: list[Violation] = []
    if not root.exists():
        return [Violation(root, "path does not exist")]
    for path in root.rglob("*"):
        if installed and path.is_symlink():
            violations.append(Violation(path, "installed package must not contain symlinks"))
        if any(pattern.match(path.name) for pattern in BACKUP_PATTERNS):
            violations.append(Violation(path, "backup-pattern file is not allowed"))
    return violations


def validate_installed_skill_root(root: Path) -> list[Violation]:
    root = root.expanduser()
    violations: list[Violation] = []
    if not root.exists():
        return [Violation(root, "installed skill root does not exist")]
    target = root / "agent-doctrine-router"
    if not target.exists():
        return [Violation(target, "agent-doctrine-router is not installed in this root")]
    if target.is_symlink():
        return [Violation(target, "installed skill target is a symlink")]
    violations.extend(validate_no_bad_files(target, installed=True))
    skill_files = sorted(target.rglob("SKILL.md"))
    if skill_files != [target / "SKILL.md"]:
        violations.append(Violation(target, "installed skill must contain exactly one top-level SKILL.md"))
    source_marker = target / ".skill-source"
    if not source_marker.is_file():
        violations.append(Violation(source_marker, "installed skill is missing .skill-source"))
    elif source_marker.read_text(encoding="utf-8").strip() != str(REPO_ROOT):
        violations.append(Violation(source_marker, ".skill-source does not point at Agent-Doctrine"))
    return violations


def validate_repo() -> list[Violation]:
    violations: list[Violation] = []
    violations.extend(validate_rule_registry())
    for provider in provider_names():
        violations.extend(validate_provider(provider))
    violations.extend(validate_owner_contracts())
    violations.extend(validate_skill_source())
    violations.extend(validate_claude_repo_write_guard_source())
    required_scripts = [
        "generate_codex.py",
        "generate_claude.py",
        "install_codex.py",
        "install_claude.py",
        "install_claude_repo_write_guard.py",
        "install_codex_skill.py",
        "install_claude_skill.py",
        "verify_codex_router_install.py",
        "validate_codex.py",
        "validate_claude.py",
    ]
    for name in required_scripts:
        path = REPO_ROOT / "scripts" / name
        if not path.is_file():
            violations.append(Violation(path, "required provider-specific script is missing"))
    return violations


def print_violations(violations: list[Violation]) -> None:
    for violation in violations:
        print(f"ERROR  {violation.path}")
        print(f"       {violation.message}")


def run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent-Doctrine source, outputs, and installed skill copies.")
    parser.add_argument("--source", type=Path, default=REPO_ROOT)
    parser.add_argument("--installed", type=Path, action="append", default=[])
    args = parser.parse_args(argv)
    if args.source.resolve() != REPO_ROOT:
        parser.error(f"this validator must run against {REPO_ROOT}")
    violations = validate_repo()
    for root in args.installed:
        violations.extend(validate_installed_skill_root(root))
    if violations:
        print_violations(violations)
        return 1
    print("Agent-Doctrine validation passed")
    return 0


def run_provider_cli(provider: str) -> int:
    violations = validate_provider(provider)
    if violations:
        print_violations(violations)
        return 1
    print(f"{provider} validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.argv[1:]))
