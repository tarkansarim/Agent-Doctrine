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
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "package" / "claude-repo-write-guard"))

import validate_common
from install_common import DoctrineError, install_provider
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

    def test_registered_cppstudio_relay_is_not_unmanaged_doctrine(self) -> None:
        generated = (REPO_ROOT / "generated" / "codex" / "AGENTS.md").read_text(encoding="utf-8")
        relay = "\n".join(
            (
                "<!-- cppstudio-user-agents-relay:begin -->",
                "## CppStudio Skill Relay",
                "",
                "For native C++ GPU work, load `cpp-cuda-vulkan-studio`.",
                "<!-- cppstudio-user-agents-relay:end -->",
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            target.write_text(generated + "\n" + relay + "\n", encoding="utf-8")
            install_provider("codex", target_file=target)
            installed = target.read_text(encoding="utf-8")
        self.assertIn(relay, installed)
        self.assertEqual(installed.count("<!-- agent-doctrine:codex:begin -->"), 1)

    def test_unknown_text_still_blocks_when_registered_relay_is_present(self) -> None:
        generated = (REPO_ROOT / "generated" / "codex" / "AGENTS.md").read_text(encoding="utf-8")
        relay = "<!-- cppstudio-user-agents-relay:begin -->\nrelay\n<!-- cppstudio-user-agents-relay:end -->"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            target.write_text(generated + "\n" + relay + "\nunknown user doctrine\n", encoding="utf-8")
            with self.assertRaisesRegex(DoctrineError, "unmanaged non-empty doctrine"):
                install_provider("codex", target_file=target)

    def test_discard_unmanaged_preserves_registered_cppstudio_relay(self) -> None:
        generated = (REPO_ROOT / "generated" / "codex" / "AGENTS.md").read_text(encoding="utf-8")
        relay = "<!-- cppstudio-user-agents-relay:begin -->\nrelay\n<!-- cppstudio-user-agents-relay:end -->"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            target.write_text(generated + "\n" + relay + "\nunknown user doctrine\n", encoding="utf-8")
            install_provider("codex", target_file=target, discard_unmanaged=True)
            installed = target.read_text(encoding="utf-8")
        self.assertIn(relay, installed)
        self.assertNotIn("unknown user doctrine", installed)

    def test_doctrine_router_thin_relay_routes_to_core_module(self) -> None:
        package = REPO_ROOT / "package" / "agent-doctrine-router"
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        core = (package / "modules" / "core.md").read_text(encoding="utf-8")
        normalized_core = " ".join(core.split())
        self.assertIn("<!-- thin-relay:v1 -->", skill)
        self.assertIn("modules/core.md", skill)
        self.assertNotIn("Landing Surface Classification", skill)
        self.assertIn("Landing Surface Classification", core)
        self.assertIn("source/rule-provenance.json", core)
        self.assertIn("Unknown historical origin must be recorded as unknown", normalized_core)
        self.assertIn("add an owner-contract check", normalized_core)

    def test_codex_parity_completion_closeout_rule_is_not_router_owned(self) -> None:
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
        forbidden_fragments = (
            "## Parity And Completion Closeouts",
            "implemented slices",
            "remaining unimplemented or weaker-than-source features",
            "live-proof gaps",
            "accepted non-goals",
            "any reply before all planned points",
            "planned points remain missing",
            "Do not summarize work as done, complete, migrated, replaced, integrated, or",
            "explicitly accepted as a non-goal",
        )
        for fragment in forbidden_fragments:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, claude_generated)
                self.assertNotIn(fragment, codex_source)
                self.assertNotIn(fragment, codex_generated)

    def test_codex_local_plane_ticketing_cluster_is_dormant_in_active_doctrine(self) -> None:
        codex_manifest = json.loads(
            (REPO_ROOT / "source" / "codex" / "manifest.json").read_text(
                encoding="utf-8"
            )
        )
        codex_generated = (
            REPO_ROOT / "generated" / "codex" / "AGENTS.md"
        ).read_text(encoding="utf-8")
        claude_generated = (
            REPO_ROOT / "generated" / "claude" / "CLAUDE.md"
        ).read_text(encoding="utf-8")
        module_path = "modules/035-local-plane-ticketing.md"
        detailed_fragments = (
            "Before filing, decide whether the ticket is dispatchable worker work",
            "Do not file a repo-scoped active ticket until that route is explicit.",
            "~/.local/bin/plane-ticket create --project <RepoName> --worker codex|claude --tag project:<RepoName>",
            "pass the worker route with `--worker`, not as body text",
            "Active routed tickets must include exactly one worker route via `--worker codex` or `--worker claude`",
            "Use `--unrouted` only for intentionally non-dispatchable records.",
            "For Codex-originated repo-scoped filings, default to `--worker codex`",
            "A ticket is not filed until the create command returns a concrete identifier",
            "Capture those fields from stdout, verify them before closeout, and report both.",
            "If the create command exits non-zero, returns no identifier/URL, or returns output the agent cannot parse",
            "do not claim the ticket exists",
            "Known owner repo and route means file or update Plane immediately.",
            "Do not use `no-ticket follow-up` as a substitute for a routed ticket",
            "stop and report the missing routing fact instead of creating a vague or unpickable ticket",
            "Do not let route uncertainty erase the issue.",
            "no-ticket reason, and the durable follow-up surface",
            "If the owner repo and route are known, file or update the routed ticket",
            "degraded origin metadata, not a failed ticket creation",
            "created-ticket success from context-only origin metadata",
        )
        self.assertNotIn(module_path, codex_manifest["modules"])
        self.assertNotIn("# Local Plane Ticketing", codex_generated)
        self.assertNotIn("tag `worker:codex` or `worker:claude`", " ".join(codex_generated.split()))
        self.assertNotIn("tag `worker:codex` or `worker:claude`", " ".join(claude_generated.split()))
        for fragment in detailed_fragments:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, codex_generated)

    def test_historical_implementation_protections_are_not_always_on(self) -> None:
        codex_source = (
            REPO_ROOT
            / "source"
            / "codex"
            / "modules"
            / "005-minimal-doctrine.md"
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
        retired_fragments = (
            "For bugs, fix the root cause.",
            "prove the same user path with direct evidence",
            "partial or proxy behavior is never complete",
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
        for fragment in retired_fragments:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, normalized_codex_source)
                self.assertNotIn(fragment, normalized_codex_generated)
                self.assertNotIn(fragment, normalized_claude_generated)

    def test_historical_tool_failure_protection_is_not_always_on(self) -> None:
        retired = (
            "Do not silently bypass a broken required tool or reusable cross-repo workflow.",
            "Fix its owner when assigned; otherwise report it or file the owner ticket when work must be deferred.",
        )
        codex_source = (
            REPO_ROOT
            / "source"
            / "codex"
            / "modules"
            / "005-minimal-doctrine.md"
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
        for fragment in retired:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, normalized_codex_source)
                self.assertNotIn(fragment, normalized_codex_generated)
                self.assertNotIn(fragment, normalized_claude_generated)

    def test_minimal_behavior_rules_are_active_for_both_providers(self) -> None:
        required = (
            "Only when designing agent-facing tools: preserve model judgment",
            "Continue through clear implementation and verification steps.",
            "If a skill or repo rule defect or friction belongs to a repository outside the current task repo",
        )
        retired = (
            "Do not silently bypass a broken required tool",
            "During supervision, keep implementation with the worker",
            "Follow the user's exact scope",
            "For bugs, fix the root cause",
            "`tiny/direct`",
            "`guarded-direct`",
            "Task classification is a process ceiling",
            "Planning Harness packet",
            "adversarial-review loop",
            "`non-blocking repair`",
            "`agent-work-leases`",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT
                    / "source"
                    / provider
                    / "modules"
                    / "005-minimal-doctrine.md"
                ).read_text(encoding="utf-8")
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized_source = " ".join(source.split())
                normalized_generated = " ".join(generated.split())
                for fragment in required:
                    self.assertIn(fragment, normalized_source)
                    self.assertIn(fragment, normalized_generated)
                for fragment in retired:
                    self.assertNotIn(fragment, normalized_generated)

    def test_owner_defect_routing_uses_external_repo_boundary_without_recursion(self) -> None:
        required = (
            "file or update a ticket for that owning repo; do not silently work around it",
            "For defects owned by the current task repo, the active implementation, validation evidence, and repository history are sufficient",
            "unless the user requests a ticket, the repair is deferred, or separate durable rollout or tracking is needed",
            "Do not create recursive tickets solely because this ticketing process causes friction",
        )
        retired = (
            "If a skill or repo rule blocks the task or causes friction, file or update a ticket",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT
                    / "source"
                    / provider
                    / "modules"
                    / "005-minimal-doctrine.md"
                ).read_text(encoding="utf-8")
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                for text in (source, generated):
                    normalized = " ".join(text.split())
                    for fragment in required:
                        self.assertIn(fragment, normalized)
                    for fragment in retired:
                        self.assertNotIn(fragment, normalized)

    def test_specialist_skill_routes_are_not_always_loaded_by_user_doctrine(self) -> None:
        retired = (
            "For tmux workers, repo-agent supervision, or worker contact, load `agent-tmux-control`.",
            "For non-blocking repair workstreams during active process testing, or multi-agent edits that may overlap files or need integration packets, load `agent-work-leases`.",
            "For repo maps, project memory, or local past lessons, load `code-map-project-memory` or `routed-recall`.",
            "For GUI, visual, offscreen, fullscreen, or screenshot proof, load `offscreen-test-manager` or `sonar-design`.",
            "For creating, editing, installing, or auditing skills, load `skill-packaging-discipline-router`.",
            "For app control surfaces, launch/control/readback APIs, or native app automation, load `agentic-control-harness`.",
            "For every status or final reply, load `reply-verbosity` and follow its saved tier and language setting.",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized_generated = " ".join(generated.split())
                for fragment in retired:
                    self.assertNotIn(fragment, normalized_generated)

    def test_global_batching_rule_is_not_always_on(self) -> None:
        forbidden = (
            "normally at least 10 minutes",
            "do not stop after a tiny edit",
        )
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
                for fragment in forbidden:
                    self.assertNotIn(fragment, source)
                    self.assertNotIn(fragment, generated)

    def test_reply_contract_is_narrowly_scoped(self) -> None:
        required = (
            "Keep replies short, plain, and easy to scan",
            "End status and final replies with one future-only `Next:` line",
            "Use `Next: None; task complete.` when nothing remains",
        )
        forbidden = (
            "The `Next:` line may include completed work or be omitted when the task is complete",
            "`agent-contact send",
            "interrupt-working",
            "raw PTY",
            "During supervision, keep implementation with the worker",
            "independently verify the claimed user result",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized = " ".join(generated.split())
                for fragment in required:
                    self.assertIn(fragment, normalized)
                for fragment in forbidden:
                    self.assertNotIn(fragment, normalized)

    def test_skill_loading_is_observable_for_both_providers(self) -> None:
        required = "When reading a skill for the current task, announce `Loading skill: <name>` once before relying on it."
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized = " ".join(generated.split())
                self.assertIn(required, normalized)

    def test_pressure_lab_and_self_improvement_are_not_always_on(self) -> None:
        retired = (
            "Load `pressure-lab` only for substantive agent-facing behavior",
            "Narrow wording, metadata, and trigger changes use source validation and focused tests without Pressure Lab",
            "The `self-improving` skill and `agent-self-improve` CLI are suspended unless the user explicitly asks to use them",
            "Do not automatically run `agenda`, `status`, `record`, `enqueue`, `reliability-gate`, or `review-add`",
            "While the mechanism is suspended, do not call ordinary source-rule, skill, repo-document, tool, or ticket changes self-improvement",
            "pause mutation of the suspect mechanism, continue unaffected work",
            "For agent-facing skills, hooks, CLIs, validators, artifact grammars",
            "Self-improvement is optional, not a per-task gate",
            "a repeated, evidence-backed failure should produce a durable rule or tool change",
            "stop further environment mutation",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized = " ".join(generated.split())
                for fragment in retired:
                    self.assertNotIn(fragment, normalized)

    def test_cross_provider_diagnosis_is_readable_without_cross_provider_writes(self) -> None:
        required = (
            "Inspect the other provider only when the user asks for cross-provider work",
            "write each provider only through its owning source",
            "install snapshots for both providers unless the user explicitly limits scope",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized = " ".join(generated.split())
                for fragment in required:
                    self.assertIn(fragment, normalized)

    def test_repo_first_pass_is_bootstrap_only(self) -> None:
        repo_rules = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        normalized = " ".join(repo_rules.split())
        self.assertIn("## Bootstrap Checklist", repo_rules)
        self.assertIn("only when creating, adopting, or restructuring the doctrine pipeline", normalized)
        self.assertIn("Ordinary rule edits", normalized)
        self.assertNotIn("## Required First Pass", repo_rules)
        self.assertNotIn("agent-self-improvement-doctrine", repo_rules)

    def test_historical_visible_proof_protection_is_not_always_on(self) -> None:
        retired = (
            "For bugs, fix the root cause.",
            "For visible, realtime, performance, or hardware claims, prove the same user path with direct evidence",
            "if the user says the result is unchanged, the earlier success claim is invalid",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT
                    / "source"
                    / provider
                    / "modules"
                    / "005-minimal-doctrine.md"
                ).read_text(encoding="utf-8")
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized_source = " ".join(source.split())
                normalized_generated = " ".join(generated.split())
                for fragment in retired:
                    normalized_fragment = " ".join(fragment.split())
                    self.assertNotIn(normalized_fragment, normalized_source)
                    self.assertNotIn(normalized_fragment, normalized_generated)

    def test_reddit_access_procedure_is_not_always_on(self) -> None:
        retired_rule = "For Reddit primary-thread access during current/community research"
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
                self.assertNotIn(retired_rule, normalized_source)
                self.assertNotIn(retired_rule, normalized_generated)
                self.assertNotIn(detailed_command, generated)
                self.assertNotIn(blocked_json, generated)

        package = REPO_ROOT / "package" / "agent-doctrine-router"
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        core = (package / "modules" / "core.md").read_text(encoding="utf-8")
        self.assertNotIn("modules/reddit-access.md", skill)
        self.assertNotIn("Reddit primary-thread access", core)
        self.assertEqual(
            [path.name for path in (package / "modules").glob("*.md")],
            ["core.md"],
        )

    def test_continuation_contract_is_provider_general(self) -> None:
        required = (
            "Continue through clear implementation and verification steps.",
            "An explicit request to stay awake continues until completion, a real blocker, or a decision only the user can make.",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT
                    / "source"
                    / provider
                    / "modules"
                    / "005-minimal-doctrine.md"
                ).read_text(encoding="utf-8")
                generated = (
                    REPO_ROOT / "generated" / provider / filename
                ).read_text(encoding="utf-8")
                normalized_source = " ".join(source.split())
                normalized_generated = " ".join(generated.split())
                for fragment in required:
                    self.assertIn(fragment, normalized_source)
                    self.assertIn(fragment, normalized_generated)

    def test_self_improvement_classification_is_not_always_on(self) -> None:
        retired = (
            "Before closing a repeated miss, workflow failure, or reusable agent/tool/harness/workflow/doctrine lesson, choose and name its durable surface",
            "runtime record",
            "repo doctrine",
            "promotion candidate",
            "provider doctrine",
            "tool/ticket",
            "Provider doctrine routes through Agent-Doctrine source/generate/validate/install",
            "An ordinary repository code fix needs no durable-surface label unless it exposes such a reusable lesson",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (
                    REPO_ROOT / "generated" / provider / filename
                ).read_text(encoding="utf-8")
                normalized_generated = " ".join(generated.split())
                for fragment in retired:
                    self.assertNotIn(fragment, normalized_generated)

    def test_doctrine_router_names_self_improvement_landing_surfaces(self) -> None:
        core = (
            REPO_ROOT
            / "package"
            / "agent-doctrine-router"
            / "modules"
            / "core.md"
        ).read_text(encoding="utf-8")
        normalized_core = " ".join(core.split())
        required = (
            "choose the landing surface before closeout",
            "`no-action with reason`",
            "`runtime record only`",
            "`repo-local durable doctrine`",
            "`promotion-candidate`",
            "`provider-general doctrine`",
            "`tooling/ticket`",
            "Closeout must name the selected surface and verification",
            "do not create a ticket solely to satisfy process",
        )
        for fragment in required:
            self.assertIn(fragment, normalized_core)

    def test_patch_stacking_guard_is_always_on_without_full_rewind_procedure(self) -> None:
        required = (
            "A `failed patch` is a code-change attempt that fails required validation or does not fix the reported behavior.",
            "After the first failed patch, commit that exact state as a diagnostic rollback anchor before making more repair edits.",
            "Further patch stacking is exploratory: use it to find and record the real fix.",
            "Once the fix is proven, preserve its required changes, restore the diagnostic anchor, apply only the proven fix cleanly, and rerun the exact validation.",
            "If the first patch itself proved wrong, return to the original pre-repair commit instead.",
            "Load `rewind-checkpoints` for the rollback procedure.",
        )
        routed_procedure = (
            "Do not initialize or snapshot",
            "merely because work is substantive, visible, or a correction",
            "Before destructive operations",
            "broad mechanical rewrites",
            "experimental probes",
            "a second fix attempt that would stack on an unproven first attempt",
            "current `HEAD` plus a full changed-file inventory is sufficient",
            "use a commit or explicit manual checkpoint only when Git cannot preserve",
        )
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                generated = (
                    REPO_ROOT / "generated" / provider / filename
                ).read_text(encoding="utf-8")
                normalized_generated = " ".join(generated.split())
                for fragment in required:
                    self.assertIn(fragment, normalized_generated)
                for fragment in routed_procedure:
                    self.assertNotIn(fragment, normalized_generated)

    def test_generated_outputs_start_at_first_rule_section(self) -> None:
        for provider, filename, first_heading in (
            ("codex", "AGENTS.md", "# Codex User Rules"),
            ("claude", "CLAUDE.md", "# Claude User Rules"),
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

    def test_active_rules_have_registered_source_only_provenance(self) -> None:
        self.assertEqual(validate_common.validate_rule_registry(), [])
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                self.assertEqual(validate_common.validate_provider_rule_markers(provider), [])
                generated = (
                    REPO_ROOT / "generated" / provider / filename
                ).read_text(encoding="utf-8")
                self.assertNotIn("<!-- agent-doctrine-rule:", generated)

    def test_inactive_owner_derived_rules_do_not_require_live_contracts(self) -> None:
        registry = json.loads(
            (REPO_ROOT / "source" / "rule-provenance.json").read_text(
                encoding="utf-8"
            )
        )
        registry["owner_contracts"] = [
            contract
            for contract in registry["owner_contracts"]
            if "rewind.opt-in" not in contract["rule_ids"]
        ]
        with mock.patch.object(
            validate_common,
            "load_rule_registry",
            return_value=(registry, []),
        ):
            violations = validate_common.validate_rule_registry()
        messages = [violation.message for violation in violations]
        self.assertNotIn(
            "owner-derived rule 'rewind.opt-in' requires an owner_contract check",
            messages,
        )

    def test_rule_marker_validation_rejects_untracked_source_rules(self) -> None:
        registry = {
            "rules": {
                "test.expected": {
                    "providers": ["codex"],
                }
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            module = Path(tmp) / "module.md"
            module.write_text("# Test\n\n- untracked rule\n", encoding="utf-8")
            with (
                mock.patch.object(validate_common, "module_paths", return_value=[module]),
                mock.patch.object(validate_common, "load_rule_registry", return_value=(registry, [])),
            ):
                violations = validate_common.validate_provider_rule_markers("codex")
        messages = [violation.message for violation in violations]
        self.assertTrue(any("missing a provenance marker" in message for message in messages))
        self.assertTrue(any("registered rule 'test.expected' is missing" in message for message in messages))

    def test_present_owner_repositories_match_promoted_contracts(self) -> None:
        self.assertEqual(validate_common.validate_owner_contracts(), [])

    def test_userlevel_backup_artifacts_are_forbidden_for_both_providers(self) -> None:
        required = "Keep backups outside provider roots."
        for provider, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(provider=provider):
                source = (
                    REPO_ROOT
                    / "source"
                    / provider
                    / "modules"
                    / "005-minimal-doctrine.md"
                ).read_text(encoding="utf-8")
                generated = (REPO_ROOT / "generated" / provider / filename).read_text(encoding="utf-8")
                normalized_source = " ".join(source.split())
                normalized_generated = " ".join(generated.split())
                self.assertIn(required, normalized_source)
                self.assertIn(required, normalized_generated)

    def test_installer_blocks_userlevel_backup_artifacts_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "codex-home"
            root.mkdir(parents=True)
            (root / "AGENTS.md.20260625.bak").write_text("old backup\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/install_codex.py", "--target-root", str(root)],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("backup artifacts inside user-level provider root", result.stderr)
            self.assertIn("AGENTS.md.20260625.bak", result.stderr)

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
            self.assertIn("# Codex User Rules", text)
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
            self.assertIn("# Codex User Rules", text)
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
            self.assertIn("# Claude User Rules", text)
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
                self.assertIn("Keep replies short, plain, and easy to scan", generated_text)
                self.assertIn("Put the result, blocker, or decision first", generated_text)
                self.assertIn("End status and final replies with one future-only `Next:` line", generated_text)
                self.assertNotIn("load `reply-verbosity`", generated_text)

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
            source_package = REPO_ROOT / "package" / "agent-doctrine-router"
            source_files = {
                path.relative_to(source_package): path.read_bytes()
                for path in source_package.rglob("*")
                if path.is_file()
            }
            for root in (codex_skills, claude_skills):
                installed = root / "agent-doctrine-router"
                self.assertTrue((installed / "SKILL.md").is_file())
                self.assertTrue((installed / "modules" / "core.md").is_file())
                self.assertTrue((installed / ".skill-source").is_file())
                self.assertFalse(any(path.is_symlink() for path in installed.rglob("*")))
                self.assertFalse(any("previous" in path.name or path.name.endswith(".new") for path in root.iterdir()))
                installed_files = {
                    path.relative_to(installed): path.read_bytes()
                    for path in installed.rglob("*")
                    if path.is_file() and path.name != ".skill-source"
                }
                self.assertEqual(installed_files, source_files)
            self.assertEqual(validate_common.validate_skill_source(), [])
            self.assertEqual(
                validate_common.validate_installed_skill_root(codex_skills), []
            )
            self.assertEqual(
                validate_common.validate_installed_skill_root(claude_skills), []
            )

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
            installed_module = (
                codex_skills
                / "agent-doctrine-router"
                / "modules"
                / "core.md"
            )
            installed_module.write_text(
                installed_module.read_text(encoding="utf-8") + "\nlocal drift\n",
                encoding="utf-8",
            )
            violations = validate_common.validate_installed_skill_root(codex_skills)
            self.assertTrue(
                any(
                    "differs from source file(s): modules/core.md" in violation.message
                    for violation in violations
                )
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
