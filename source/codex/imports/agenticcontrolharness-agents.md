# Imported Codex Doctrine Source

- Source path: `<workspace root>/AgenticControlHarness/AGENTS.md`
- Source SHA256: `932a66d015caab948ee6347f94536f29fd36ceecc87ce5a40b5c739040b01659`
- Provider lane: `codex`

## Original Content

# Agent Instructions

This folder is a standalone extraction candidate for CppStudio's agentic app-control harness skill.

## Current Status

- Scaffold only. Do not install until the standalone package is implemented and reconciled with
  existing local repos.
- Important overlap exists with `GuiControlHarnessCreator`, `Sonar`, `Offscreentest_manager`, and
  the installed `agent-tmux-control` skill. Inspect those before designing APIs.

## Pickup Rules

- Read `README.md` and `IMPLEMENTATION_BRIEF.md` before editing.
- Compose existing tools rather than duplicating them.
- Keep this generic for apps that agents need to drive and inspect. Native C++ GPU specifics should
  be examples or optional profiles, not the core.
- Do not remove the CppStudio-bundled `agentic-control-harness` until the standalone repo is proven
  and CppStudio has a relay/migration plan.

## Expected First Commit

Implement the standalone skill, references, endpoint contract templates, validation fixtures, and a
dry-run install path.
