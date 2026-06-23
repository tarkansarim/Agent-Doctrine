# Agent-Doctrine Agent Notes

This repo is the source-owned home for provider-specific agent doctrine:
Codex `AGENTS.md` and Claude `CLAUDE.md`.

## Provider Separation

- Keep Codex and Claude source trees, generated outputs, installers, validators,
  and tests separate.
- Do not create one shared deployed doctrine file or one shared installed
  runtime folder for both providers.
- Shared reasoning notes may live in neutral docs only when they are not an
  installed runtime surface.
- Codex output targets `AGENTS.md`; Claude output targets `CLAUDE.md`.

## Source Boundary

- Repo-level `AGENTS.md` and `CLAUDE.md` files under `<workspace root>`
  are source examples to inventory and distill.
- Do not use deployed user-level files as normal source material. The only
  exception is an explicit Agent-Doctrine adoption/import task for existing live
  user-level doctrine, where the live file is read-only source input so the
  deployed behavior becomes recoverable from this repo.
- Do not directly patch `~/.codex/AGENTS.md` or `~/.claude/CLAUDE.md`.
  Installers must build from this repo. Unmanaged non-empty deployed doctrine
  outside managed markers is drift, not a normal success state; the installer
  must report it and require a user decision to adopt/import it into source,
  discard it, or keep it only as a temporary unmanaged exception.
- Codex work must not read from or patch `~/.claude` for ordinary Codex
  behavior. An explicit Agent-Doctrine adoption/import task may read
  `~/.claude/CLAUDE.md` as read-only source input. Claude install support should
  still be implemented as source-owned scripts and docs, not by ad hoc edits.

## Required First Pass

1. Inventory repo-level `AGENTS.md` and `CLAUDE.md` examples from workspace.
2. Separate provider-specific rules from general concepts.
3. Design provider-specific source modules and build/install/validate scripts.
4. Preserve provider-specific semantics instead of normalizing them into one
   generic document.
5. Add a small discoverable skill/router for doctrine updates. Its job is to
   tell future agents that durable changes to `AGENTS.md` or `CLAUDE.md` must be
   requested by ticket to this repo instead of patched directly in deployed
   provider files.
6. Prove the generated outputs, skill trigger path, and validators work before
   claiming completion.

## Packaging Discipline

- Snapshot installs only; no symlinks into user-level provider roots.
- No backup artifacts under scanned provider roots.
- Keep installation explicit and reversible.
- Add tests for marker preservation, source/output parity, and provider
  separation.

<!-- agent-self-improvement-doctrine:begin -->
## Accepted Self-Improvement Doctrine

- 2026-06-01T02:06:40Z [global] Final and status closeouts for parity, migration, replacement, feature-completion, or integration work must explicitly separate implemented slices, verified behavior, remaining unimplemented or weaker-than-source features, live-proof gaps, accepted non-goals, and unfinished planned points before sounding complete. (source: self-improvement:user_correction:698158d73d07ee98)
- 2026-06-20T07:12:55Z [global] For user-reported bugs, repeated failures, visible regressions, or performance complaints, fix the root cause and prove the exact user-visible path before claiming success; symptom treatment, nearby tuning, internal counters, backend readbacks, widget state, smoke-test completion, or preview-only behavior are not fixed-proof unless the user explicitly accepts reduced scope. (source: self-improvement:user_correction:664ae6a6080c073f)
- 2026-06-20T15:01:03Z [global] For visual, interactive, realtime, or performance fixes, require exact user-visible invariant proof and reject proxy, preview-only, deferred, release-only, final-only, state-only, counter-only, generic-FPS, or provenance-only proof unless that behavior is the explicit product requirement. (source: self-improvement:user_correction:a1cc1db8c769f752)
- 2026-06-21T16:51:15Z [global] Visual selection-to-result bugs must not be closed by narrowing a failed end-to-end visible proof into a smaller passing lane; supporting state, crops, readbacks, and metrics are diagnostics unless the primary artifact proves the visible input/control and resulting output together with a negative assertion for the reported wrong result. (source: self-improvement:user_correction:fedb10a056b11cf7)
- 2026-06-23T16:20:17Z [global] When a correction, repeated miss, workflow failure, or reusable repo-specific lesson should change future behavior, classify the landing surface before closeout as no-action with reason, runtime record only, repo-local durable doctrine, promotion-candidate, provider-general doctrine, or tooling/ticket; implement or route the selected durable surface and name verification. (source: self-improvement:user_correction:8114bb2db1d663f5)
- 2026-06-23T23:02:13Z [global] Agents must not let discovered cross-repo/tool/skill/harness/workflow issues disappear because the current task can continue; they must surface the issue and either file/update the owner ticket or name the no-ticket follow-up surface. (source: self-improvement:user_correction:c949a377e05f2b07)
<!-- agent-self-improvement-doctrine:end -->
