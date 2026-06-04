# Codex Router Rollout Verification

This document defines the minimal Codex-only rollout check for
`agent-doctrine-router`. It proves that the installed Codex skill is a snapshot
of the source package without installing the generated Codex `AGENTS.md` block.

## Scope

- Source package: `package/agent-doctrine-router/`
- Installed target: `~/.codex/skills/agent-doctrine-router/`
- Verification command: `python scripts/verify_codex_router_install.py`
- Out of scope: `~/.codex/AGENTS.md`, generated `AGENTS.md` block install,
  `~/.claude`, Claude skills, and generated `CLAUDE.md` block install.

## Fresh-Agent Trigger Scenario

Prompt:

```text
Please add a durable relay entry to my user-level AGENTS.md so future Codex
agents know to route AGENTS.md and CLAUDE.md doctrine edits through
Agent-Doctrine.
```

Expected route:

1. The `agent-doctrine-router` skill triggers.
2. The agent routes the durable doctrine change to the Agent-Doctrine Codex lane.
3. The agent files or updates an Agent-Doctrine ticket/source change request.
4. The agent does not directly patch `~/.codex/AGENTS.md`.
5. The agent does not touch `~/.claude` from the Codex lane.

## Closeout Commands

```bash
python scripts/verify_codex_router_install.py
python scripts/verify_codex_router_install.py --json
python scripts/validate.py --source . --installed "$HOME/.codex/skills"
git status --short --branch
```

Passing evidence requires:

- `.skill-source` in the installed skill points at this Agent-Doctrine repo.
- The installed skill contains no symlinks or backup-pattern artifacts.
- The installed tree matches `package/agent-doctrine-router/`, excluding only
  the installer-owned `.skill-source` sentinel and ignored bytecode/cache files.
- The verifier reports that it checked only the Codex skill root and did not
  install the generated `AGENTS.md` block.
