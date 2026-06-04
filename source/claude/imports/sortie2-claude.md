# Imported Claude Doctrine Source

- Source path: `<workspace root>/sortie2/CLAUDE.md`
- Source SHA256: `5c0d3b3a5af7d085361ea58c71391918df17f2281222f1e05c96495874a3a4e4`
- Provider lane: `claude`

## Original Content

# Project Rules

## Always-Load Skills

Always load the `self-improving` skill at session start. It is not conditional — it runs every session.

## Build After Every Code Change (MANDATORY)

After ANY code change (edit, write, or new file), you MUST run the install script before asking the user to test or reload:

```bash
cd <workspace root>/sortie2 && bash install-extension.sh
```

This compiles TypeScript, packages as a VSIX, and does a full install to `~/.vscode/extensions/tarka.sortie-1.0.0/`. VS Code loads from the installed extension, NOT from the source directory — the full install is mandatory to ensure all assets (not just `out/`) are up to date.

**Do NOT use `npm run compile` alone** — it only syncs `out/` and misses other assets. Always use `install-extension.sh`.

Note: `update-extension.sh` is deprecated (renamed `.deprecated`). Ignore it.

## Harness Runtime Fix Reload Order (MANDATORY)

When a Harness Architect issue requires a Sortie code, prompt, skill, or instrumentation fix during an active or tainted run, use this order:

1. Stop/reset affected Harness workers and tracked target processes first.
2. Clear the tainted run state and wipe disposable Layer 2 target artifacts.
3. Apply the fix.
4. Run `bash install-extension.sh` from this repo.
5. Reload VS Code through Sortie's internal supervisor bridge, not GUI automation.
6. Verify `.sortie/autonomy/state/bridge.json`, the installed-extension `.sortie-harness-data/.../harness-control.json`, backend Harness state, and rendered panel state before rerunning the phase.

Do not rerun Harness Architect against patched source until the installed extension has picked up the change through a full VS Code reload.

## Harness Architect Module (`src/harness/`)

Sortie contains a controlled replay system for AI agents called **Harness Architect**.

**What it is:** A checkpoint/rewind/respawn loop for preserving provenance while building target-software harnesses. Accepted checkpoints prove restorable runtime state and accepted replay boundaries, not objective target behavior. When friction occurs, execution stops. You reason through the failure, encode the lesson where the next run will load it, then use `harness_rewind` to restore an accepted restorable checkpoint. Runtime must fail closed if the checkpoint is unaccepted, lacks a restorable snapshot, or cannot restore.

**The active model:** Supervisor/L1 is the active doctrine and runtime-control role. Layer 2 is the Target Executor. The old separate Layer 1 worker slot is legacy inactive state only for old records and panel compatibility; L1 skills and CLAUDE.md remain first-class doctrine assets and must not be deleted.

**No promotion stack:** Skill promotion, probe scoring, trusted oracle registry scaffolding, and adversarial lanes are deferred until real target-specific executable oracles exist.

**Key files:**
- `src/harness/types.ts` — checkpoint, session, runtime, friction, and replay types
- `src/harness/checkpointStore.ts` — atomic JSON checkpoint store under installed-extension Harness data
- `src/harness/forkOperation.ts` — checkpoint restore and layer files hash diagnostics
- `src/harness/snapshotAdapters.ts` — Maya / git / filesystem / none adapters
- `src/harness/README.md` — full concept and design reference

**Canonical MCP tools:** `harness_session_start`, `harness_reset_project`, `harness_executor` (`action: "start" | "send" | "stop"`), `harness_mark_friction`, `harness_checkpoint` (`action: "get" | "list"`), `harness_rewind`, `harness_target` (`action: "launch" | "stop"`)

**Full design:** `docs/harness-architect/ARCHITECTURE.md` and `docs/harness-architect/PROJECT.md`

### Harness Reset Discipline (MANDATORY)

When a Harness Architect run is tainted by a process or instrumentation issue, do not carry that run forward as the next baseline.

A run is tainted if any of the following happened:
- misleading or incorrect harness activity/transcript labeling
- Layer 1 or Layer 2 violated the assigned phase contract
- stale chat/transcript state would contaminate the next proof pass
- Layer 2 generated target artifacts during a dirty or untrusted run
- a harness/runtime bug was fixed mid-run and the user is about to reload or continue

If a tainted harness run requires a code fix, prompt fix, instrumentation fix, or process fix, you MUST clean up the tainted run before you make the fix. Do not leave live workers, active target processes, or dirty harness state running while you patch the system.

Required order for tainted Harness Architect runs:

1. Stop and reset the affected harness workers first.
2. Stop and reset any tracked target process.
3. Clear the affected harness chat/transcript state.
4. Remove the affected active harness session state/records.
5. Wipe the Layer 2-generated target artifacts from the dirty run.
6. Only preserve dirty chat state or dirty target artifacts if the user explicitly says to keep them for forensics.
7. Only after steps 1-5 are complete may you make the fix.
8. Treat the dirty run as disposable process evidence, not as trusted progress.

Do not preserve stale Layer 2 output by default just because deleting it is destructive. In Harness Architect, a dirty proof run is not a deliverable.

---

## Codebase Map Maintenance (MANDATORY)

After any structural change to `src/` (new files, moved files, renamed exports, deleted modules, significant refactors), update the corresponding codebase-map skill in `.sortie/assistant/skills/codebase-map/`. These skills are what workers load to navigate the codebase — stale maps mean wasted search time on every dispatch.

9 skills cover the full codebase: extension-core, panels, visualization, mcp-servers, assistant, adjutant, supervisor, autonomy, harness. See `.sortie/assistant/skills/codebase-map/SKILL.md` for the full maintenance procedure and file mapping.

## Temporary Files

All temporary files (test scripts, verify scripts, data dumps, debug output, scratch files, etc.) MUST be saved in the `tmp/` folder at the project root — never in the root directory itself. Create the `tmp/` folder if it doesn't exist. This includes but is not limited to:
- `verify-*.js`, `test-*.js`, `temp_*.js` scripts
- `.txt`, `.json`, `.md` data exports or descriptions
- Screenshots, debug images
- Any file that is not a permanent part of the project
