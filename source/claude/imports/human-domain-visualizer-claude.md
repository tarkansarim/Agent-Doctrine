# Imported Claude Doctrine Source

- Source path: `<workspace root>/human-domain-visualizer/CLAUDE.md`
- Source SHA256: `59749addef368ee1a4a2d807e21fafef2b930411cd2f649614fc9cc1f149e2a8`
- Provider lane: `claude`

## Original Content

# human-domain-visualizer — Project Instructions

This file is auto-loaded into every Claude Code session that opens this repo. It is the per-project operating identity. `AGENTS.md` mirrors the load-bearing parts for Codex / Sortie compatibility.

## Operating discipline

**Re-read `PLAN.md` end-to-end before starting work on any milestone.** The plan is the source of truth for execution. Compaction makes recall of milestone details unreliable; the file does not lie.

**Hard pause after every milestone deliverable.** No proceeding to the next milestone without explicit user approval ("M_x approved, proceed to M_y"). Pause artifacts (live demo, screenshot, test output, file diff) are required for each pause.

**No silent scope expansion.** If a milestone exposes a need to revisit a prior decision or expand scope, halt and ask. Update `PLAN.md` and append to `DECISIONS.md` before continuing.

**Stage specific files, never `git add .`** — neighborhood convention. Catch-all staging risks committing secrets, large binaries, or `.codex/` / `.sortie/` runtime state.

**Halt-and-ask on these specific triggers:**
- A milestone deliverable can't be produced with the listed sub-steps.
- A test fails and the fix would require touching code outside the current milestone's scope.
- A new dependency would be added that isn't in the locked stack.
- A schema change would break a fixture or production module already committed.
- The visual contract (M5a / M6) needs a direction the plan doesn't anticipate.
- Mobility / motion / animation is requested for v0 (forbidden — D19).

## Project paradigm (one-paragraph primer)

The repo is rendered **as a creature**. Modules are organs; files are tissue cells; templates are body plans (vertebrate / insectoid / single-cell / etc.). A module declares an `anatomy` block (`kind` + `role`); a template optionally declares an `archetype` and `anatomy_override` per module. The blueprint resolver composes modules with `extends:` and `overrides:`; the body plan resolver then maps the resolved modules to 2D anatomy slots. Visual rendering uses **abstract organic shapes** (blobs, tubes, chambers) — not anatomical illustration, not cartoon. v0 is **static** (no motion); v1 adds lifecycle dynamics; v2 couples to an `olalaaa`-style DDE substrate; v3+ explores monetization-driven self-preservation. See `PLAN.md` § Creature pivot overview.

## v0 scope (LOCKED)

**In:**
- Load YAML modules and YAML templates from `modules/` and `templates/`.
- Modules declare `anatomy { kind, role }`; templates optionally declare `archetype` and per-module `anatomy_override`.
- Compose: a template can `extends:` another and reference modules via `modules:` with `overrides:`.
- Resolve: produce a flat node list with provenance (which module/template introduced each node) and inherited anatomy.
- **Body plan resolver**: map the resolved blueprint to a 2D creature (archetype + slot assignments + `(x, y)` per organ).
- Watch a target directory with `notify-rs`, respecting `.gitignore`.
- Render the creature as an abstract organic 2D scene in PixiJS: organs as blobs/tubes/chambers, file cells inside, connective edges between, ghost styling for missing organs.
- Completion levels 0/1/2 only (missing / exists / parses cleanly) — aggregated to organ level for rendering, also visible per-file as cells.
- One built-in composed template: `cpp-cuda-vulkan` (vertebrate archetype) over 6+ modules.
- One synthesized demo target under `examples/`.
- Self-host template for live iteration against this repo.
- Discovery mode: open without a blueprint, render embryonic blob with floating ghost organ candidates; user "Apply"s modules to differentiate.

**Out (deferred — DO NOT bring into v0):**
- **Motion of any kind** (D19) — no breathing, no pulses, no heartbeat, no spatial drift. v1+ only.
- Lifecycle dynamics (vitality bar, growth/decay, activity glow). v1.
- DDE substrate coupling (`olalaaa` integration: baseA ratchet, deficit cascade, death). v2.
- Monetization-driven self-preservation. v3+ research.
- Drift detection (off-blueprint files as foreign tissue). v1.
- Agent-driven module assembly (LLM-driven composition). v1.
- AAR-style activity event WebSocket + worker overlays + replay. v2.
- Tree-sitter symbol-level granularity. v1.
- Completion levels 3–5 (symbols, tests, coverage). v1.
- Cookiecutter / copier ingest, save-blueprint-to-target-repo, blueprint editor UI. v1.
- Tissue-packet / gate-registry adapters for Architect_L1 and Emergence_Build_Harness. v2+.

## Stack (LOCKED)

- **Shell**: Tauri 2 (Rust backend + webview UI; ~10 MB bundle target).
- **Frontend**: React + TypeScript + Vite.
- **Canvas**: PixiJS v8 (2D, GPU-accelerated).
- **Layout**: body plan resolver (in Rust) + `anatomyLayout.ts` in TS. **No treemap, no `d3-hierarchy`** — D16 superseded by D17.
- **Visual style**: abstract organic shapes (procedural blobs / tubes / chambers / branches / clusters). Not anatomical illustration. Not cartoon.
- **Rust deps**: `notify`, `serde`, `serde_yaml`, `ignore`, `walkdir`, `tokio`, `thiserror`.
- **JS deps**: `pixi.js` v8, `zustand`, `@tauri-apps/plugin-dialog`.
- **Package manager**: pnpm (>= 10).
- **Bundle identifier**: `com.user.hdv`.

Do not add dependencies outside this list without amending the plan and updating `DECISIONS.md`.

## Decisions

All design decisions are tracked in `DECISIONS.md` (append-only). Locked decisions (D1–D11, D17–D21) are documented in `PLAN.md` § Locked decisions. Outstanding decisions (D12–D16, D22–D23) resolve in their relevant milestone.

`ARCHITECTURE.md` has a separate decisions log specific to architectural concepts (schema, IPC, layout). When the two diverge, `DECISIONS.md` is the more recent source.

## Rewind discipline

This project uses the Claude Code Rewind file-checkpoint system. Automatic checkpoints are created after each completed turn once non-empty reviewed excludes exist in `.rewind/config.json`.

- **Use existing hook-created checkpoints for causal replay.** Do not create checkpoints unilaterally mid-turn.
- **Pair Rewind file restore with Claude branch/replay** when conversation state matters (e.g., causal probes of agent behavior).
- **Never put project-local agent-facing docs in the Rewind exclude list.** `PLAN.md`, `CLAUDE.md`, `AGENTS.md`, `DECISIONS.md`, `friction-log.md`, `ARCHITECTURE.md`, `README.md`, `ROADMAP.md` are learned operating fabric and must survive rewind.
- **Never exclude** `src/**`, `src-tauri/src/**`, `examples/*/src/**`, `modules/**`, `templates/**` — these are the rewind body (creature anatomy lives in `modules/` and `templates/`).
- **Always exclude**: `node_modules/`, `src-tauri/target/`, `dist/`, `dist-ssr/`, `examples/*/target/`, `examples/*/build/`, `examples/*/.cache/`, `.env*`, `*.log`.

## Tool surface

v0 does not expose MCP tools, plugins, or external integrations. v2+ will add an activity-feed adapter (sortie2 `AAR`-shape inspired) for Sortie / Claude Code hooks; until then, the app is standalone.

## Project memory

Cross-session memory lives at `~/.claude/projects/-home-user-storage-work-workspace-human-domain-visualizer/memory/`. Managed by the harness's `agent-self-improve` mechanism — do not hand-edit unless instructed.

## Quick references

- `PLAN.md` — execution plan with milestones, deliverables, pauses (re-read before each milestone)
- `ARCHITECTURE.md` — design concepts, schema strawman, IPC surface, decisions log
- `DECISIONS.md` — append-only decision log
- `ROADMAP.md` — v0/v1/v2/v3 phased scope
- `friction-log.md` — friction encountered during execution
- `modules/` — module library (YAML) — each declares `anatomy` block
- `templates/` — composed templates (YAML) — each optionally declares `archetype`
- `examples/` — demo targets (creatures derived from templates + tree state)
- `docs/` — screenshots, recordings, generated artifacts
