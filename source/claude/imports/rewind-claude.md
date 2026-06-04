# Imported Claude Doctrine Source

- Source path: `<workspace root>/Rewind/CLAUDE.md`
- Source SHA256: `5a75d0977c4a5eac16794e02dae58a344d32fdead898f33d0ae621bf7978060e`
- Provider lane: `claude`

## Original Content

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Rewind is local checkpoint/rewind tooling for agentic coding sessions (Codex CLI
and Claude Code). Its primary value is **causal replay**, not just rollback: hold
a branch point fixed, change exactly one preserved circumstance or root-cause
fix, and replay to measure the behavior delta. Failed fixes must not accumulate
as patch-on-patch in worker files or chat history.

The repo ships **skills plus their installers** — there is no application build.
The source lives here; the installers copy snapshots into `~/.codex` and
`~/.claude`. Never edit a deployed copy to make a durable change; edit source
here and re-run the installer.

## Commands

```bash
# Full unit verifier — run this after any change to a script or installer.
python tools/verify_rewind.py

# Install/update the Codex skill snapshot (also writes a managed AGENTS.md trigger block).
python tools/install_rewind_skill.py            # add --skip-user-rules to skip rules
python tools/install_rewind_skill.py --json     # machine-readable closeout

# Install/update the Claude Code skill snapshot (also writes a managed CLAUDE.md trigger block).
python tools/install_claude_rewind_skill.py

# Live runtime check of the installed Codex Stop hook (needs working Codex login + model).
# Not part of verify_rewind.py.
python tools/probe_codex_stop_hook.py --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

`verify_rewind.py` is a single `main()` of sequential `assert`s driven against
real subprocess invocations of the CLIs in a tmp project — there is no pytest and
no per-test selection. To run "one test", read the relevant assert block and run
the underlying `rewind.py`/installer command by hand with the same args. The
verifier exercises both the Codex (`skills/`) and Claude (`claude-skills/`) copies,
the installers, the MCP server, auto-checkpoint hooks, and the manual fallback.

All scripts are **dependency-free stdlib Python 3** (snapshots are `tar.gz`,
metadata is JSON). Do not add third-party imports — the skills must run inside
provider runtimes with no install step.

## Architecture

### Two parallel skill trees — keep them in lockstep
- `skills/rewind-checkpoints/` — **Codex** variant (includes `rewind_mcp.py`,
  `agents/openai.yaml`, and Codex `codex-checkpoint`/`codex-fork`/`codex-rewind`
  chat-pairing commands).
- `claude-skills/rewind-checkpoints/` — **Claude Code** variant (includes
  `claude_branch.py`; uses Claude-native `/branch`, `/rewind`, `--fork-session`
  instead of Codex chat forking).

The two `rewind.py` files are near-duplicates that intentionally **differ** (the
Claude copy has no Codex chat-fork commands; provider markers and probe output
differ). A change to shared CLI behavior usually has to be applied to **both**
copies, and `verify_rewind.py` asserts against both. Do not assume editing one
covers the other.

Each tree also has a `manual-checkpoint-and-rewind/` sibling: the explicit
`--project` fallback for repos outside the provider session root. Manual
destructive rewind refuses implicit refs (`latest`, `latest-paired`) and requires
a reviewed exclude profile + explicit checkpoint id/alias.

### `rewind.py` is the engine (~5.9k lines)
Single dependency-free CLI implementing init / set-excludes / checkpoint /
status / diff / restore / delete plus codex-checkpoint, codex-fork, codex-rewind,
sidecar-anchor, mark, ready, quick-status, disable-project, enable-project,
relocate, init-new-project, configure-archive, archive-status. `rewind_mcp.py`
re-exposes the same operations over stdio MCP (and rejects string booleans).

### Activation is fail-closed (the central invariant)
`init` writes `.rewind/config.json` with `"exclude": []`. Checkpoint, status,
diff, restore, and delete **refuse to run** until a non-empty, non-catch-all,
non-protected-only exclude list is set via `set-excludes --yes`. The exclude list
is an explicit decision about what to preserve *outside* rewind scope. `.git/**`
and `.rewind/**` are always protected and must not be added as project excludes.
Never hand-edit `.rewind/config.json` — the CLI rejects empty/catch-all/
protected-only boundaries that a manual edit would silently allow.

### Automatic checkpoints are hook-owned, not agent-owned
`auto_checkpoint.py` is the Stop-hook entrypoint (`--provider codex|claude`). It
bootstraps `.rewind` metadata for safe roots after completed turns and creates a
checkpoint only once a real exclude list exists. It has an internal **45s
deadline** (`AUTO_CHECKPOINT_DEADLINE_SECONDS` in verify_rewind.py, with a 15s
margin under the provider hook timeout); on timeout it records a skipped attempt
in `.rewind/hooks/auto-checkpoints.json` rather than blocking the turn. Checkpoints
fire per completed turn for the **session-root** cwd — not for arbitrary repos
passed later via `--project`.

### Restore is staged and fail-closed
Restore refuses if the current exclude policy differs from checkpoint-time policy,
writes an outside-project emergency copy ring (under `XDG_STATE_HOME`, refused if
that would land inside the project), creates a pre-restore safety checkpoint,
extracts to `.rewind<temp dir>/restore-*`, fingerprints the staged tree against
metadata, and only then restores per-path (replacing symlinks, never
`copytree`-ing into the project). Deleting post-checkpoint files needs
`--delete-added`; large deletes need `--allow-large-delete`.

### Installers copy snapshots + manage doctrine blocks
`install_rewind_skill.py` / `install_claude_rewind_skill.py` copy the skill trees
into `${CODEX_HOME}/skills` / `${CLAUDE_CONFIG_DIR}/skills` and inject an
idempotent managed trigger block (delimited by `rewind-checkpoints-trigger:begin/
end`) into `AGENTS.md` / `CLAUDE.md`. They **refuse to write through symlinked**
`AGENTS.md`/`CLAUDE.md`/`hooks.json`/`config.toml`/`settings.json` and guard
against symlink-swap and parent-directory-swap races (see the swap-rejection
helpers in `verify_rewind.py`). `--json` emits a `post_install_closeout` object;
treat any required item (pending Codex `/hooks` trust, stale running sessions) as
blocking before claiming automatic checkpoint coverage.

### `ready` vs file-rewind readiness
`rewind.py ready` distinguishes **automatic** coverage (initialized + reviewed
excludes + a hook-created Stop checkpoint + matching session root) from
**file-rewind** readiness (a manual checkpoint exists). A project can support file
rewind without being automatic-ready. For Codex, `ready` also checks the installed
Stop hook is trusted in Codex's `/hooks` review state.

## Working conventions

- After installing or updating a skill, an **already-running** Codex/Claude
  process still uses the old hook until restarted/resumed — a missing checkpoint
  after a turn is often a stale process, not a Rewind failure. Check session start
  time against `hooks.json` / `settings.json`.
- `.rewind/` in this repo is live checkpoint data for *this* repo's own sessions
  (snapshots, checkpoints, chat, codex-sessions). It is not test fixtures — do not
  treat it as scratch.
- `rules/claude-rewind-trigger.md` and `rules/codex-rewind-trigger.md` are the
  source of the managed trigger blocks the installers inject. Edit doctrine wording
  there, not in deployed `AGENTS.md`/`CLAUDE.md`.
- `docs/agent-context/SLICE_WATCHLIST.md` is an agent-maintained ledger of
  per-slice constraints/gates that must survive compaction; consult it before
  multi-step changes and update it as work lands.
- The README is the authoritative, exhaustive command reference — consult it for
  exact flags (sidecar anchors, probe workspaces, causal-probe wrappers,
  archive retention) before inventing argument combinations.
