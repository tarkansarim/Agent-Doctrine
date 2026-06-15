from __future__ import annotations

import json
import hashlib
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "package" / "claude-repo-write-guard"))

import validate_common
from install_claude_repo_write_guard import install_hook
from repo_write_guard import BLOCK_EXIT_CODE


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        run_script("scripts/generate_all.py")

    def test_generated_outputs_match_provider_sources(self) -> None:
        result = run_script("scripts/validate_codex.py")
        self.assertIn("codex validation passed", result.stdout)
        result = run_script("scripts/validate_claude.py")
        self.assertIn("claude validation passed", result.stdout)

    def test_codex_closeout_doctrine_relays_parity_completion_gaps(self) -> None:
        codex_source = (
            REPO_ROOT
            / "source"
            / "codex"
            / "modules"
            / "020-operating-discipline.md"
        ).read_text(encoding="utf-8")
        codex_generated = (
            REPO_ROOT / "generated" / "codex" / "AGENTS.md"
        ).read_text(encoding="utf-8")
        claude_generated = (
            REPO_ROOT / "generated" / "claude" / "CLAUDE.md"
        ).read_text(encoding="utf-8")
        relay_module = (
            REPO_ROOT
            / "package"
            / "agent-doctrine-router"
            / "modules"
            / "parity-closeouts.md"
        ).read_text(encoding="utf-8")
        required_fragments = (
            "## Parity And Completion Closeouts",
            "implemented slices",
            "verified behavior",
            "remaining unimplemented or weaker-than-source features",
            "live-proof gaps",
            "accepted non-goals",
            "any reply before all planned points",
            "planned points remain missing",
            "Do not summarize work as done, complete, migrated, replaced, integrated, or",
            "explicitly accepted as a non-goal",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, relay_module)
        self.assertNotIn("## Parity And Completion Closeouts", claude_generated)
        self.assertIn("load `agent-doctrine-router`", codex_source)
        self.assertIn("load `agent-doctrine-router`", codex_generated)
        self.assertNotIn("any reply before all planned points", codex_generated)
        self.assertNotIn("planned points remain missing", codex_generated)

    def test_codex_plane_ticketing_requires_worker_route_and_documents_origin_fallback(self) -> None:
        codex_source = (
            REPO_ROOT
            / "source"
            / "codex"
            / "modules"
            / "035-local-plane-ticketing.md"
        ).read_text(encoding="utf-8")
        codex_generated = (
            REPO_ROOT / "generated" / "codex" / "AGENTS.md"
        ).read_text(encoding="utf-8")
        claude_generated = (
            REPO_ROOT / "generated" / "claude" / "CLAUDE.md"
        ).read_text(encoding="utf-8")
        relay = (
            REPO_ROOT
            / "package"
            / "agent-doctrine-router"
            / "modules"
            / "plane-ticketing.md"
        ).read_text(encoding="utf-8")
        normalized_relay = " ".join(relay.split())

        lean_worker_rule = "tag `worker:codex` or `worker:claude` unless explicitly `--unrouted`"
        detailed_fragments = (
            "Before filing, decide whether the ticket is dispatchable worker work",
            "Do not file a repo-scoped active ticket until that route is explicit.",
            "~/.local/bin/plane-ticket create --project <RepoName> --tag project:<RepoName> --tag worker:codex|worker:claude",
            "Pass every route tag as a `--tag` flag",
            "do not rely on title/body prose, ad hoc `Tags:` lines, or later rejection",
            "Active routed tickets must also include exactly one worker route tag",
            "Use `--unrouted` only for intentionally non-dispatchable records.",
            "For Codex-originated repo-scoped filings, default to `--tag worker:codex`",
            "stop and report the missing routing fact instead of creating a vague or unpickable ticket",
            "degraded origin metadata, not a failed ticket creation",
            "created-ticket success from context-only origin metadata",
        )
        self.assertIn(lean_worker_rule, " ".join(codex_source.split()))
        self.assertIn(lean_worker_rule, " ".join(codex_generated.split()))
        self.assertNotIn(lean_worker_rule, " ".join(claude_generated.split()))
        for fragment in detailed_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, normalized_relay)
                self.assertNotIn(fragment, codex_generated)

    def test_codex_python_performance_escalation_rule_is_provider_specific(self) -> None:
        codex_source = (
            REPO_ROOT
            / "source"
            / "codex"
            / "modules"
            / "030-implementation-discipline.md"
        ).read_text(encoding="utf-8")
        codex_generated = (
            REPO_ROOT / "generated" / "codex" / "AGENTS.md"
        ).read_text(encoding="utf-8")
        claude_generated = (
            REPO_ROOT / "generated" / "claude" / "CLAUDE.md"
        ).read_text(encoding="utf-8")
        normalized_codex_source = " ".join(codex_source.split())
        normalized_codex_generated = " ".join(codex_generated.split())
        normalized_claude_generated = " ".join(claude_generated.split())
        required_fragments = (
            "Python verifiers, test runners, build helpers, or agent tools",
            ">60s repeated paths",
            ">5 min critical paths",
            ">20 min repeated pipeline surfaces",
            "measure first and report timing",
            "setup, file copying, subprocess dispatch, or core logic",
            "Prefer parallel Python",
            "algorithm/data-layout fixes",
            "Rust for agent-facing CLI verifiers",
            "C++ only when the hot path is already native",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, normalized_codex_source)
                self.assertIn(fragment, normalized_codex_generated)
                self.assertNotIn(fragment, normalized_claude_generated)

    def test_reddit_access_rule_relays_to_router_skill_details(self) -> None:
        lean_rule = "Reddit primary threads are not unsearchable"
        relay_pointer = "`agent-doctrine-router` reddit-access relay"
        detailed_command = "curl -L -s -H 'User-Agent: Mozilla/5.0"
        blocked_json = "top.json"
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT
                    / "source"
                    / provider
                    / "modules"
                    / "020-operating-discipline.md"
                ).read_text(encoding="utf-8")
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized_source = " ".join(source.split())
                normalized_generated = " ".join(generated.split())
                self.assertIn(lean_rule, normalized_source)
                self.assertIn(relay_pointer, normalized_source)
                self.assertIn(lean_rule, normalized_generated)
                self.assertIn(relay_pointer, normalized_generated)
                self.assertNotIn(detailed_command, generated)
                self.assertNotIn(blocked_json, generated)

        skill = (REPO_ROOT / "package" / "agent-doctrine-router" / "SKILL.md").read_text(encoding="utf-8")
        relay = (
            REPO_ROOT
            / "package"
            / "agent-doctrine-router"
            / "modules"
            / "reddit-access.md"
        ).read_text(encoding="utf-8")
        self.assertIn("modules/reddit-access.md", skill)
        self.assertIn(detailed_command, relay)
        self.assertIn("top.rss?t=month", relay)
        self.assertIn(blocked_json, relay)

    def test_self_improvement_repo_lessons_require_promotion_classification(self) -> None:
        required = (
            "classify the lesson as repo-only, promotion-candidate, or provider-general",
            "Provider-general lessons must route through Agent-Doctrine source/generate/validate/install",
            "ambiguous cross-repo lessons stay local and open a promotion candidate",
        )
        for provider, filename, module_name in (
            ("codex", "AGENTS.md", "040-rewind-and-learning.md"),
            ("claude", "CLAUDE.md", "040-replay-and-learning.md"),
        ):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT / "source" / provider / "modules" / module_name
                ).read_text(encoding="utf-8")
                generated = (
                    REPO_ROOT / "generated" / provider / filename
                ).read_text(encoding="utf-8")
                normalized_source = " ".join(source.split())
                normalized_generated = " ".join(generated.split())
                for fragment in required:
                    self.assertIn(fragment, normalized_source)
                    self.assertIn(fragment, normalized_generated)

    def test_generated_outputs_start_at_first_rule_section(self) -> None:
        for provider, filename, first_heading in (
            ("codex", "AGENTS.md", "# Codex Configuration Boundary"),
            ("claude", "CLAUDE.md", "# Claude Configuration Boundary"),
        ):
            with self.subTest(provider=provider):
                text = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                lines = text.splitlines()
                self.assertEqual(lines[0], f"<!-- agent-doctrine:{provider}:begin -->")
                self.assertEqual(lines[1], first_heading)
                forbidden = (
                    "# Codex User-Level Rules",
                    "# Claude User-Level Rules",
                    "Generated from Agent-Doctrine source modules",
                    "Source inputs:",
                    "# Adopted Live User-Level",
                    "Adopted source SHA256",
                )
                for fragment in forbidden:
                    self.assertNotIn(fragment, text)

    def test_codex_installer_blocks_unmanaged_doctrine_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "codex-home"
            target = root / "AGENTS.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "user prefix\n\n"
                "<!-- agent-doctrine:codex:begin -->\nold managed\n"
                "<!-- agent-doctrine:codex:end -->\n\n"
                "user suffix\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "scripts/install_codex.py", "--target-root", str(root)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unmanaged non-empty doctrine", result.stderr)
            self.assertIn("adopt/import", result.stderr)
            self.assertIn("--discard-unmanaged", result.stderr)
            self.assertIn("--allow-unmanaged-exception", result.stderr)
            self.assertIn("before Agent-Doctrine managed block", result.stderr)
            self.assertIn("user prefix", result.stderr)
            self.assertIn("after Agent-Doctrine managed block", result.stderr)
            self.assertIn("user suffix", result.stderr)
            self.assertIn("old managed", target.read_text(encoding="utf-8"))

    def test_codex_installer_blocks_whole_unmanaged_file_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "codex-home"
            target = root / "AGENTS.md"
            target.parent.mkdir(parents=True)
            target.write_text("durable rule outside source\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/install_codex.py", "--target-root", str(root)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("entire file (no Agent-Doctrine managed block)", result.stderr)
            self.assertIn("durable rule outside source", result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "durable rule outside source\n")

    def test_codex_installer_preserves_unmanaged_doctrine_only_with_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "codex-home"
            target = root / "AGENTS.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "user prefix\n\n"
                "<!-- agent-doctrine:codex:begin -->\nold managed\n"
                "<!-- agent-doctrine:codex:end -->\n\n"
                "user suffix\n",
                encoding="utf-8",
            )
            run_script(
                "scripts/install_codex.py",
                "--target-root",
                str(root),
                "--allow-unmanaged-exception",
            )
            text = target.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("user prefix\n\n"))
            self.assertTrue(text.rstrip().endswith("user suffix"))
            self.assertIn("# Codex Configuration Boundary", text)
            self.assertNotIn("old managed", text)

    def test_codex_installer_discards_unmanaged_doctrine_only_with_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "codex-home"
            target = root / "AGENTS.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "user prefix\n\n"
                "<!-- agent-doctrine:codex:begin -->\nold managed\n"
                "<!-- agent-doctrine:codex:end -->\n\n"
                "user suffix\n",
                encoding="utf-8",
            )
            run_script(
                "scripts/install_codex.py",
                "--target-root",
                str(root),
                "--discard-unmanaged",
            )
            text = target.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("<!-- agent-doctrine:codex:begin -->\n"))
            self.assertIn("# Codex Configuration Boundary", text)
            self.assertNotIn("old managed", text)
            self.assertNotIn("user prefix", text)
            self.assertNotIn("user suffix", text)

    def test_claude_installer_blocks_unmanaged_doctrine_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "claude-home"
            target = root / "CLAUDE.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "user prefix\n\n"
                "<!-- agent-doctrine:claude:begin -->\nold managed\n"
                "<!-- agent-doctrine:claude:end -->\n\n"
                "user suffix\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, "scripts/install_claude.py", "--target-root", str(root)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unmanaged non-empty doctrine", result.stderr)
            self.assertIn("adopt/import", result.stderr)
            self.assertIn("--discard-unmanaged", result.stderr)
            self.assertIn("--allow-unmanaged-exception", result.stderr)
            self.assertIn("before Agent-Doctrine managed block", result.stderr)
            self.assertIn("user prefix", result.stderr)
            self.assertIn("after Agent-Doctrine managed block", result.stderr)
            self.assertIn("user suffix", result.stderr)
            self.assertIn("old managed", target.read_text(encoding="utf-8"))

    def test_claude_installer_preserves_unmanaged_doctrine_only_with_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "claude-home"
            target = root / "CLAUDE.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "user prefix\n\n"
                "<!-- agent-doctrine:claude:begin -->\nold managed\n"
                "<!-- agent-doctrine:claude:end -->\n\n"
                "user suffix\n",
                encoding="utf-8",
            )
            run_script(
                "scripts/install_claude.py",
                "--target-root",
                str(root),
                "--allow-unmanaged-exception",
            )
            text = target.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("user prefix\n\n"))
            self.assertTrue(text.rstrip().endswith("user suffix"))
            self.assertIn("# Claude Configuration Boundary", text)
            self.assertNotIn("old managed", text)

    def test_codex_adopts_whole_unmanaged_file_then_installs_without_drift(self) -> None:
        self._assert_whole_unmanaged_adoption_installs("codex", "AGENTS.md")

    def test_claude_adopts_whole_unmanaged_file_then_installs_without_drift(self) -> None:
        self._assert_whole_unmanaged_adoption_installs("claude", "CLAUDE.md")

    def test_reply_verbosity_relay_is_source_owned_and_installs_without_drift(self) -> None:
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                reply_block = self._reply_verbosity_block_from_snapshot(provider, filename)
                digest = hashlib.sha256(reply_block.encode("utf-8")).hexdigest()
                adoption_manifest = json.loads(
                    (
                        REPO_ROOT
                        / "source"
                        / provider
                        / "adopted"
                        / "adoption-manifest.json"
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual(adoption_manifest["reply_verbosity_relay_adopted_install_sha256"], digest)
                self.assertFalse(adoption_manifest["runtime_loaded"])
                generated_text = (
                    REPO_ROOT
                    / "generated"
                    / provider
                    / filename
                ).read_text(encoding="utf-8")
                self.assertNotIn("<!-- BEGIN: reply-verbosity", generated_text)
                self.assertNotIn("## Verbosity Tiers", generated_text)
                self.assertIn("Every assistant reply must end with an explicit `Next:` clause", generated_text)

                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / f"{provider}-home"
                    target = root / filename
                    target.parent.mkdir(parents=True)
                    target.write_text(
                        f"<!-- agent-doctrine:{provider}:begin -->\nold managed\n"
                        f"<!-- agent-doctrine:{provider}:end -->\n\n"
                        f"{reply_block}\n",
                        encoding="utf-8",
                    )
                    result = run_script(
                        f"scripts/install_{provider}.py",
                        "--target-root",
                        str(root),
                    )
                    self.assertIn(f"installed {provider} doctrine", result.stdout)
                    text = target.read_text(encoding="utf-8")
                    self.assertNotIn("old managed", text)
                    self.assertEqual(text.count("<!-- BEGIN: reply-verbosity"), 0)
                    self.assertTrue(text.startswith(f"<!-- agent-doctrine:{provider}:begin -->\n"))
                    self.assertTrue(text.rstrip().endswith(f"<!-- agent-doctrine:{provider}:end -->"))

    def test_generated_outputs_stay_lean_and_do_not_inline_skill_details(self) -> None:
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                text = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), validate_common.GENERATED_MAX_LINES)
                self.assertLessEqual(validate_common.lexical_token_count(text), validate_common.GENERATED_MAX_TOKENS)
                forbidden = [
                    marker
                    for marker in validate_common.GENERATED_FORBIDDEN_INLINE_MARKERS
                    if marker in text
                ]
                self.assertEqual(forbidden, [])

    def test_generated_budget_gate_reports_oversized_output(self) -> None:
        path = REPO_ROOT / "generated" / "codex" / "AGENTS.md"
        oversized = "\n".join("x" for _ in range(validate_common.GENERATED_MAX_LINES + 1))
        violations = validate_common.validate_generated_budget(path, oversized)
        self.assertTrue(any("budget" in violation.message for violation in violations))

    def test_generated_duplicate_gate_reports_skill_detail_markers(self) -> None:
        path = REPO_ROOT / "generated" / "codex" / "AGENTS.md"
        text = "short\n<!-- BEGIN: reply-verbosity (managed by install.sh) -->\n"
        violations = validate_common.validate_no_inlined_skill_duplicates(path, text)
        self.assertTrue(any("re-inlines skill-owned detail" in violation.message for violation in violations))

    def _assert_whole_unmanaged_adoption_installs(self, provider: str, filename: str) -> None:
        manifest = REPO_ROOT / "source" / provider / "manifest.json"
        adoption_manifest = REPO_ROOT / "source" / provider / "adopted" / "adoption-manifest.json"
        snapshot = REPO_ROOT / "source" / provider / "adopted" / f"live-user-level-{filename}"
        generated = REPO_ROOT / "generated" / provider / filename
        originals = {
            manifest: manifest.read_bytes() if manifest.exists() else None,
            adoption_manifest: adoption_manifest.read_bytes() if adoption_manifest.exists() else None,
            snapshot: snapshot.read_bytes() if snapshot.exists() else None,
            generated: generated.read_bytes() if generated.exists() else None,
        }
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / f"{provider}-home"
                target = root / filename
                target.parent.mkdir(parents=True)
                target.write_text("durable live rule\nsecond live rule\n", encoding="utf-8")
                run_script(
                    "scripts/adopt_live_doctrine.py",
                    "--provider",
                    provider,
                    "--target-root",
                    str(root),
                )
                run_script(f"scripts/generate_{provider}.py")
                result = run_script(f"scripts/install_{provider}.py", "--target-root", str(root))
                self.assertIn(f"installed {provider} doctrine", result.stdout)
                text = target.read_text(encoding="utf-8")
                self.assertNotIn("durable live rule", text)
                self.assertNotIn("second live rule", text)
                self.assertNotIn("Adopted source SHA256", text)
                self.assertNotIn("Adopted snapshot", text)
                self.assertTrue(adoption_manifest.is_file())
                adoption_data = json.loads(adoption_manifest.read_text(encoding="utf-8"))
                self.assertEqual(adoption_data["adopted_source_sha256"], hashlib.sha256("durable live rule\nsecond live rule\n".encode("utf-8")).hexdigest())
                self.assertEqual(adoption_data["adopted_snapshot"], f"source/{provider}/adopted/live-user-level-{filename}")
                self.assertFalse(adoption_data["runtime_loaded"])
                self.assertTrue(text.startswith(f"<!-- agent-doctrine:{provider}:begin -->\n"))
                self.assertEqual(snapshot.read_text(encoding="utf-8"), "durable live rule\nsecond live rule\n")
        finally:
            for path, original in originals.items():
                if original is None:
                    if path.exists():
                        path.unlink()
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(original)

    def _reply_verbosity_block_from_snapshot(self, provider: str, filename: str) -> str:
        snapshot = REPO_ROOT / "source" / provider / "adopted" / f"live-user-level-{filename}"
        text = snapshot.read_text(encoding="utf-8")
        start_marker = "<!-- BEGIN: reply-verbosity (managed by install.sh) -->"
        end_marker = "<!-- END: reply-verbosity (managed by install.sh) -->"
        start = text.index(start_marker)
        end = text.index(end_marker, start) + len(end_marker)
        return text[start:end]

    def test_skill_snapshot_install_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_skills = Path(tmp) / "codex-skills"
            claude_skills = Path(tmp) / "claude-skills"
            run_script("scripts/install_codex_skill.py", "--skills-root", str(codex_skills))
            run_script("scripts/install_codex_skill.py", "--skills-root", str(codex_skills))
            run_script("scripts/install_claude_skill.py", "--skills-root", str(claude_skills))
            run_script("scripts/install_claude_skill.py", "--skills-root", str(claude_skills))
            for root in (codex_skills, claude_skills):
                installed = root / "agent-doctrine-router"
                self.assertTrue((installed / "SKILL.md").is_file())
                self.assertTrue((installed / ".skill-source").is_file())
                self.assertFalse(any(path.is_symlink() for path in installed.rglob("*")))
                self.assertFalse(any("previous" in path.name or path.name.endswith(".new") for path in root.iterdir()))
            result = run_script(
                "scripts/validate.py",
                "--source",
                str(REPO_ROOT),
                "--installed",
                str(codex_skills),
                "--installed",
                str(claude_skills),
            )
            self.assertIn("Agent-Doctrine validation passed", result.stdout)

    def test_codex_router_install_verifier(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_skills = Path(tmp) / "codex-skills"
            run_script("scripts/install_codex_skill.py", "--skills-root", str(codex_skills))
            result = run_script(
                "scripts/verify_codex_router_install.py",
                "--skills-root",
                str(codex_skills),
                "--json",
            )
            report = json.loads(result.stdout)
            self.assertTrue(report["matches_source"])
            self.assertTrue(report["checked_only_codex_skill_root"])
            self.assertTrue(report["does_not_install_generated_agents_block"])
            self.assertEqual(report["skill_source_marker"], str(REPO_ROOT))

    def test_codex_router_install_verifier_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_skills = Path(tmp) / "codex-skills"
            run_script("scripts/install_codex_skill.py", "--skills-root", str(codex_skills))
            installed_skill = codex_skills / "agent-doctrine-router" / "SKILL.md"
            installed_skill.write_text(
                installed_skill.read_text(encoding="utf-8") + "\nlocal drift\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_codex_router_install.py",
                    "--skills-root",
                    str(codex_skills),
                ],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("installed package differs from source", result.stdout)

    def test_claude_repo_write_guard_allows_active_repo_and_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mytools = root / "workspace"
            active = mytools / "Agent-Doctrine"
            memory = root / "claude" / "projects" / "-home-user-project" / "memory" / "notes.md"
            for target in (active / "README.md", memory):
                with self.subTest(target=target):
                    result = self._run_repo_write_guard(
                        root,
                        target,
                        cwd=active,
                        mytools=mytools,
                        claude_root=root / "claude",
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_claude_repo_write_guard_allows_active_repo_from_worker_checkout_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mytools = root / "workspace"
            active = mytools / "Agent-Doctrine"
            worker = root / "symphony-workspaces" / "local-plane" / "PLANE-180"
            self._write_git_origin(worker, active)

            result = self._run_repo_write_guard(
                root,
                active / "README.md",
                cwd=worker,
                mytools=mytools,
                claude_root=root / "claude",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_claude_repo_write_guard_blocks_other_repo_from_worker_checkout_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mytools = root / "workspace"
            active = mytools / "Agent-Doctrine"
            worker = root / "symphony-workspaces" / "local-plane" / "PLANE-180"
            other = mytools / "Agents-Capabilities-Usage-Monitor" / "FRICTION_DETECTION_SPEC.md"
            self._write_git_origin(worker, active)

            result = self._run_repo_write_guard(
                root,
                other,
                cwd=worker,
                mytools=mytools,
                claude_root=root / "claude",
            )
            self.assertEqual(result.returncode, BLOCK_EXIT_CODE)
            self.assertIn("outside active repo Agent-Doctrine", result.stderr)
            self.assertIn("File or update a Plane ticket", result.stderr)

    def test_claude_repo_write_guard_blocks_other_mytools_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mytools = root / "workspace"
            active = mytools / "Agent-Doctrine"
            other = mytools / "Agents-Capabilities-Usage-Monitor" / "FRICTION_DETECTION_SPEC.md"
            for tool_name in ("Write", "Edit"):
                with self.subTest(tool_name=tool_name):
                    result = self._run_repo_write_guard(
                        root,
                        other,
                        cwd=active,
                        mytools=mytools,
                        claude_root=root / "claude",
                        tool_name=tool_name,
                    )
                    self.assertEqual(result.returncode, BLOCK_EXIT_CODE)
                    self.assertIn("blocked this Write/Edit", result.stderr)
                    self.assertIn("Agents-Capabilities-Usage-Monitor", result.stderr)
                    self.assertIn("File or update a Plane ticket", result.stderr)

    def test_claude_repo_write_guard_blocks_mytools_repo_when_active_repo_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mytools = root / "workspace"
            target = mytools / "Agents-Capabilities-Usage-Monitor" / "FRICTION_DETECTION_SPEC.md"
            result = self._run_repo_write_guard(
                root,
                target,
                cwd=root / "worker-copy",
                mytools=mytools,
                claude_root=root / "claude",
            )
            self.assertEqual(result.returncode, BLOCK_EXIT_CODE)
            self.assertIn("no active workspace repo could be determined", result.stderr)

    def test_claude_repo_write_guard_installer_snapshots_hook_and_merges_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "claude home"
            settings = root / "settings.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "PreToolUse": [
                                {
                                    "matcher": "Read",
                                    "hooks": [{"type": "command", "command": "echo keep"}],
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            hook_target, settings_path = install_hook(root)
            second_hook_target, second_settings_path = install_hook(root)
            self.assertEqual(hook_target, second_hook_target)
            self.assertEqual(settings_path, second_settings_path)
            self.assertTrue(hook_target.is_file())
            self.assertFalse(hook_target.is_symlink())
            self.assertEqual((hook_target.parent / ".repo-write-guard-source").read_text(encoding="utf-8").strip(), str(REPO_ROOT))
            installed_settings = json.loads(settings.read_text(encoding="utf-8"))
            pre_tool = installed_settings["hooks"]["PreToolUse"]
            commands = [
                hook["command"]
                for entry in pre_tool
                for hook in entry.get("hooks", [])
                if isinstance(hook, dict) and hook.get("type") == "command"
            ]
            self.assertIn("echo keep", commands)
            self.assertEqual(commands.count(f"python3 {shlex.quote(str(hook_target))}"), 1)

    def _run_repo_write_guard(
        self,
        root: Path,
        target: Path,
        *,
        cwd: Path,
        mytools: Path,
        claude_root: Path,
        tool_name: str = "Write",
    ) -> subprocess.CompletedProcess[str]:
        cwd.mkdir(parents=True, exist_ok=True)
        payload = {
            "tool_name": tool_name,
            "tool_input": {
                "file_path": str(target),
                "content": "test",
            },
        }
        env = {
            **os.environ,
            "AGENT_DOCTRINE_WORKSPACE_ROOT": str(mytools),
            "CLAUDE_CONFIG_DIR": str(claude_root),
        }
        return subprocess.run(
            [sys.executable, str(REPO_ROOT / "package" / "claude-repo-write-guard" / "repo_write_guard.py")],
            cwd=cwd,
            input=json.dumps(payload),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )

    def _write_git_origin(self, checkout: Path, origin: Path) -> None:
        git = checkout / ".git"
        git.mkdir(parents=True)
        (git / "config").write_text(
            '[remote "origin"]\n'
            f"\turl = {origin}\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
