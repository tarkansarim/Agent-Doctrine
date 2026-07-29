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

1. Decide whether separate tracking is needed. File or update an Agent-Doctrine
   ticket when the work is deferred, crosses to another owner, or needs rollout
   tracking beyond the current session. When the user explicitly assigns the
   Agent-Doctrine source change and it will be implemented and verified now, the
   source diff plus validation/install receipt is the durable record; do not
   create a ticket solely to satisfy process. Adoption/import still requires
   explicit authorization before reading a live provider file.
2. Before adding or changing a top-level doctrine rule, identify its origin,
   current owner, provider scope, promotion class, and override status. Add or
   preserve its adjacent `agent-doctrine-rule` marker and update
   `source/rule-provenance.json`. Unknown historical origin must be recorded as
   unknown; do not guess.
3. When doctrine promotes or narrows another repo's contract, reconcile the
   owner source first and add an owner-contract check covering every promoted
   rule ID. Validation rejects owner-derived origins without that check. Do not
   copy repo-local behavior into provider doctrine without an explicit promotion
   decision.
4. Patch the provider-specific source modules in Agent-Doctrine. Provider-general
   rules change both provider lanes; a single-provider change requires explicit
   scope and reason.
5. Regenerate the affected outputs, run the provider validators, and run the full
   parity validator. Provenance markers are source-only and must not appear in
   generated doctrine.
6. Install by snapshot only through the Agent-Doctrine installer. Unmanaged
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
- Stop if a top-level source rule lacks a registered origin or promotion
  decision, if an owner-derived rule lacks an owner-contract check, or if a
  promoted owner contract disagrees with its owner source.
