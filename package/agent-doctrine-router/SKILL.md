---
name: agent-doctrine-router
description: "Route durable AGENTS.md/CLAUDE.md doctrine, provider-boundary changes, implementation discipline, tool-failure recovery, Plane ticketing, and parity closeouts."
---

# Agent Doctrine Router

Load this skill before changing durable agent doctrine, user rules, provider
instruction files, or reusable behavior that belongs in Codex `AGENTS.md` or
Claude `CLAUDE.md`.

## Routing Rule

- Durable Codex `AGENTS.md` changes go to
  `<workspace root>/Agent-Doctrine`.
- Durable Claude `CLAUDE.md` changes go to
  `<workspace root>/Agent-Doctrine`.
- Do not patch deployed user-level provider files directly.
- Do not use deployed provider files as normal source material. The exception is
  explicit adoption/import of existing live user-level doctrine into
  Agent-Doctrine source; in that case the deployed file is read-only input, and
  source must own the content before install.
- Keep Codex and Claude lanes separate: source modules, generated outputs,
  installers, validators, tests, and deployment targets remain provider-specific.

## Workflow

1. File or update an Agent-Doctrine ticket describing the requested doctrine
   change, provider lane, evidence, and target behavior. For adoption/import,
   the ticket must explicitly authorize reading the live provider file.
2. Patch the provider-specific source modules in Agent-Doctrine.
3. Regenerate only that provider output unless both providers are explicitly in
   scope.
4. Run the provider validator and the full parity validator.
5. Install by snapshot only through the Agent-Doctrine installer. Unmanaged
   non-empty deployed doctrine outside managed markers is drift, not normal
   preservation; the installer must report it and require a user decision to
   adopt/import it into source, discard it, or keep it only as a temporary
   unmanaged exception.

## Procedure Modules

| Trigger | Load |
| --- | --- |
| Implementation, editing, dependency, or verification procedure | `modules/implementation-discipline.md` |
| Bash, MCP, hook, installer, build, validation, or reusable-tool failure | `modules/tool-failures.md` |
| Plane ticket filing, status evidence, rollout proof, or terminal closeout | `modules/plane-ticketing.md` |
| Parity, migration, replacement, feature-completion, or integration closeout | `modules/parity-closeouts.md` |
| Durable doctrine source routing, provider separation, or install drift | `modules/doctrine-routing.md` |
| Reddit primary-thread access when normal reddit.com fetch/search paths fail | `modules/reddit-access.md` |

## Stop Conditions

- Stop if the request would edit `~/.codex/AGENTS.md` or `~/.claude/CLAUDE.md`
  directly for a durable doctrine change.
- Stop if the request would read deployed provider doctrine as source material
  without an explicit Agent-Doctrine adoption/import task.
- Stop if a proposed shared deployed doctrine file or shared installed runtime
  folder would mix Codex and Claude.
- Stop if the source repo for the durable doctrine change is not identifiable.
