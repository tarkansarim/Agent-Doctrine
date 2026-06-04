# Imported Codex Doctrine Source

- Source path: `<workspace root>/wetbrush_lin/AGENTS.md`
- Source SHA256: `ad242b96af9ca9fda9e30722a26f2695b7a7ae1dd78a157271c0e5e02409842e`
- Provider lane: `codex`

## Original Content

# Wetbrush Project AGENTS

These project instructions are in addition to the session-level rules.

## Codebase Map Maintenance Is Mandatory

The repo architecture map is a required maintained artifact, not optional documentation.

Whenever a change materially affects:

- subsystem ownership
- top-level frame sequencing
- timing model
- brush/liquid/render data flow
- scenario/replay integration
- persistence / active-window responsibilities
- paper-vs-live-runtime interpretation

you must update the codebase map before treating the work as complete.

The minimum map set is:

- `docs/CODEBASE_ARCHITECTURE_INDEX.md`
- `docs/ARCHITECTURE.md`
- `docs/PAPER_IMPLEMENTATION.md`

The supporting ownership/reference docs are:

- `docs/CODEBASE_SUBSYSTEM_MANIFEST.json`
- `docs/SIMULATION_SETTINGS_OWNERSHIP_MAP.md`
- `docs/WETBRUSH_PAPER_ARCHITECTURE_MAP.md`
- `docs/BRUSH_DYNAMICS_AUDIT.md`
- `docs/PAINT_PHYSICS_AUDIT.md`
- `docs/BRUSH_PAINT_DRAG_OWNERSHIP.md`
- `docs/ENGINEERING_MEMORY.md`
- `docs/FAILED_PROBES_LEDGER.md`

## Project-Local Wetbrush Skills Only

The canonical Wetbrush skill layer lives inside this repo under:

- `skills/wetbrush-*/SKILL.md`

Wetbrush skills must not live only in user scope under:

- `~/.codex/skills/`

If a Wetbrush skill changes, add/remove/update the repo-local copy in the same work stream.

When the skill tree changes, also update:

- `docs/CODEBASE_ARCHITECTURE_INDEX.md`
- `docs/CODEBASE_SUBSYSTEM_MANIFEST.json`
- any subsystem/router doc that points at the affected skill

## Required Sub-Agent Map Audit

When the codebase map needs updating, use sub-agents so the main agent can keep momentum on the implementation and integration work.

Default split:

1. app/timing/playback audit
2. brush/liquid mechanics audit
3. rendering/persistence/UI audit

Sub-agents should:

- read the current code directly
- identify outdated claims in the map docs
- summarize current ownership and flow
- return findings to the main agent

The main agent remains responsible for:

- integrating the findings
- editing the actual docs
- resolving contradictions
- verifying the updated map against the current tree

## No Major Drift Between Code And Map

If the code changes but the map is not updated, the task is not complete.

Do not defer map maintenance with:

- "update later"
- stale TODOs
- side notes in chat only

Durable repo docs must be updated in the same work stream.

## Behavior Investigation Memory

If a debugging or behavior investigation establishes a new live/runtime truth that changes how the codebase should be understood, update:

- the relevant map doc
- `docs/ENGINEERING_MEMORY.md`
- `docs/FAILED_PROBES_LEDGER.md` when a failed explanation or probe taught a real constraint

This applies even when no production code changed. New architectural, timing, ownership, or runtime-behavior insights are themselves map-changing facts and must be reflected in the codebase map in the same work stream.

## Status Updates Must Include Launch Command And Immediate Next Action

When reporting status on Wetbrush app work, always include:

- the exact app launch command:
  - `cd <workspace root>/wetbrush_lin`
  - `./build_linux/wetbrush_cpp`
- the immediate next action you are about to take

Do not make the user ask again how to launch the app or what you plan to do next.

## Verification

After map updates:

- `git diff --check` must pass
- any helper scripts added for map maintenance or audits must pass syntax checks
- if the map references a new workflow, that workflow should be smoke-tested when practical
