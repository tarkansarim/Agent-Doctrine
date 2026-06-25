---
name: agent-doctrine-router
description: "Route durable AGENTS.md/CLAUDE.md doctrine, provider-boundary changes, source generation, validation, install, adoption/import, and drift handling."
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

## Landing Surface Classification

When a correction, repeated miss, tool or workflow failure, verification gap,
or repo-specific invariant should steer future agents, choose the landing
surface before closeout instead of leaving the lesson in chat:

- `no-action with reason`: one-off preference or current-turn fact; state why
  it should not become durable.
- `runtime record only`: audit trail is enough and no future behavior changes.
- `repo-local durable doctrine`: stable rule belongs to the owning repo's
  `AGENTS.md`, `CLAUDE.md`, repo skill, or source-owned equivalent.
- `promotion-candidate`: likely cross-repo, but evidence is not yet broad or
  stable enough for provider doctrine; keep it local and open a candidate with
  owner, evidence needed, exclusions, and review date.
- `provider-general doctrine`: stable provider-wide behavior; route through
  Agent-Doctrine source, generation, validation, and snapshot install.
- `tooling/ticket`: prose is not enough or enforcement should be mechanical;
  implement the tool/hook/harness fix or file the owning repo ticket.

Closeout must name the selected surface and verification. If no durable rule
lands, closeout must say why the lesson was intentionally not made durable.

## Stop Conditions

- Stop if the request would edit `~/.codex/AGENTS.md` or `~/.claude/CLAUDE.md`
  directly for a durable doctrine change.
- Stop if the request would read deployed provider doctrine as source material
  without an explicit Agent-Doctrine adoption/import task.
- Stop if a proposed shared deployed doctrine file or shared installed runtime
  folder would mix Codex and Claude.
- Stop if the source repo for the durable doctrine change is not identifiable.
