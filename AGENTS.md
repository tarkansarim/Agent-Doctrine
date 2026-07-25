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

## Bootstrap Checklist

Run this checklist only when creating, adopting, or restructuring the doctrine
pipeline. Ordinary rule edits use the existing source, generation, validation,
and install path without repeating the inventory or redesign.

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

## Rule Provenance

- Every active top-level source rule must have an adjacent stable
  `agent-doctrine-rule` marker and an entry in
  `source/rule-provenance.json`.
- Record the original evidence honestly. If the bootstrap history did not retain
  an exact per-rule origin, mark it unknown instead of inventing one.
- Provider-general promotions from another repo must name that owner and carry a
  validator-backed owner-contract check. Generated provider doctrine must not
  contain the source-only provenance markers.
