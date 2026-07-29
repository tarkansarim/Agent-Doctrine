# Agent-Doctrine

Agent-Doctrine is a source-owned builder for provider-specific agent instruction
files. It keeps Codex `AGENTS.md` and Claude `CLAUDE.md` in separate source
lanes, generates provider-specific managed blocks, validates parity, and installs
snapshots into provider config roots.

The goal is to make durable agent doctrine reviewable and reproducible from a
repository instead of being hand-edited in live user-level files.

## Safety Model

- Codex and Claude stay separate: source modules, generated outputs, installers,
  validators, tests, and deployment targets are provider-specific.
- Deployed files are install targets, not normal source material.
- Live user-level doctrine can be adopted only through an explicit import step.
- Installers refuse unmanaged live content by default and require an explicit
  choice to adopt, discard, or temporarily preserve it.
- Installs are snapshots, not symlinks.

## Layout

- `source/codex/` - Codex-only source modules and imported repo-level
  `AGENTS.md` examples.
- `source/claude/` - Claude-only source modules and imported repo-level
  `CLAUDE.md` examples.
- `generated/codex/AGENTS.md` - generated Codex managed block.
- `generated/claude/CLAUDE.md` - generated Claude managed block.
- `package/agent-doctrine-router/` - one discoverable thin relay plus its
  detailed `modules/core.md` doctrine module.
- `package/claude-repo-write-guard/` - Claude PreToolUse Write/Edit guard
  source for blocking writes into non-active workspace repositories.
- `scripts/` - separate provider generators, installers, skill installers, and
  validators.

## Quick Start

Generate and validate the provider outputs:

```bash
python scripts/generate_codex.py
python scripts/generate_claude.py
python scripts/validate.py --source .
python -m unittest discover -s tests
```

Optionally import repo-level examples from a workspace of repositories:

```bash
AGENT_DOCTRINE_WORKSPACE_ROOT=/path/to/workspace python scripts/import_repo_doctrine.py
```

Optionally adopt existing live user-level doctrine as read-only input:

```bash
python scripts/adopt_live_doctrine.py --provider codex
python scripts/adopt_live_doctrine.py --provider claude
```

## Behavior Evaluations

Fresh-agent BenchFlow tasks for whole user-level doctrine and isolated skill
packs are owned by
`<workspace root>/Agent-Behavior-Evals`. This repository
supplies generated doctrine and router skill sources as inputs under test; it
does not own the evaluation harness or task definitions.

## Install

Installers write snapshot content into provider-specific targets. By default
they refuse unmanaged non-empty deployed doctrine outside Agent-Doctrine managed
markers because user-level `AGENTS.md` and `CLAUDE.md` must be recoverable from
Agent-Doctrine source. When drift is reported, choose one explicit resolution:
adopt/import the content into provider-specific source modules, discard it with
`--discard-unmanaged`, or keep it only as a temporary unmanaged exception with
`--allow-unmanaged-exception`:

```bash
python scripts/install_codex.py
python scripts/install_claude.py
python scripts/install_codex_skill.py
python scripts/install_claude_skill.py
python scripts/install_claude_repo_write_guard.py
```

The adoption script reads the live provider file as read-only input, writes an
exact source snapshot under `source/<provider>/adopted/`, writes an active source
module under `source/<provider>/modules/`, and updates the provider manifest.
After regeneration, the installer recognizes the adopted unmanaged live file by
hash and can replace it with the managed Agent-Doctrine block without
`--discard-unmanaged`.

Both skill installers snapshot the complete
`package/agent-doctrine-router/` tree, including `modules/core.md`, into their
provider-specific skill roots. The installed `.skill-source` file is
installer-owned metadata and is not part of the source package.

Codex and Claude remain separate throughout the pipeline. Do not edit deployed
user-level provider files directly; patch source modules here, regenerate,
validate, and then install.

## What This Does Not Do

- It does not merge Codex and Claude doctrine into one shared runtime file.
- It does not use symlinks for installed doctrine.
- It does not silently delete unmanaged deployed content.
- It does not require a specific local repository folder name.

## Rollout Boundary

Sandboxed Plane workers may validate Agent-Doctrine source changes but cannot
write user-level provider roots such as `~/.codex` or `~/.claude`. When no
host-side rollout bridge is available, the sanctioned operator command is:

```bash
python3 scripts/generate_codex.py
python3 scripts/generate_claude.py
python3 scripts/validate.py --source .
python3 scripts/install_codex.py
python3 scripts/install_claude.py
wc -l "$HOME/.claude/CLAUDE.md" "$HOME/.codex/AGENTS.md"
```

Do not move doctrine tickets to done until that command, or an equivalent
host-side install bridge, has installed both provider files and reported the
expected deployed line counts.

For minimal Codex router rollout verification without installing the generated
Codex `AGENTS.md` block, see `docs/codex-router-rollout.md`.
