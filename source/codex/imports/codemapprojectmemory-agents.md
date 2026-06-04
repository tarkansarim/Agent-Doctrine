# Imported Codex Doctrine Source

- Source path: `<workspace root>/CodeMapProjectMemory/AGENTS.md`
- Source SHA256: `cd756d8b9a2675f54b24b29bf9dba627005e0e482994427975331e5f719c4e4d`
- Provider lane: `codex`

## Original Content

# Agent Instructions

This folder is a standalone extraction candidate for CppStudio's maintained code-map and project
memory system.

## Current Status

- Scaffold only. Do not install until the skill, scripts, validators, and trigger probes are
  implemented.
- CppStudio remains the production source for code-map behavior until this standalone repo is proven.

## Pickup Rules

- Read `README.md` and `IMPLEMENTATION_BRIEF.md` before editing.
- Build the generic code-map system first. CppStudio should later consume it instead of owning the
  generic behavior.
- Preserve the useful CppStudio constraints: route before editing, drift checks before closeout,
  existing-project audit before map creation, and fresh-agent routing smokes.
- Do not make this C++ specific.
- Do not delete CppStudio code-map scripts until migration is explicitly planned and validated.

## Expected First Commit

Implement a minimal valid skill package, bootstrap/validate/drift scripts, fixtures, and dry-run
install verification.
