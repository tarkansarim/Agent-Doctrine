# Doctrine Routing Procedure

Use this module for durable `AGENTS.md` or `CLAUDE.md` changes, source boundary
questions, provider separation, generation, validation, install, or drift.

- Durable Codex and Claude doctrine changes go to the Agent-Doctrine source
  repo, not deployed provider files.
- Do not use deployed provider files as normal source material. The exception is
  an explicit Agent-Doctrine adoption/import task, where the deployed file is
  read-only source input and source must own the content before install.
- Keep Codex and Claude lanes separate: source modules, generated outputs,
  installers, validators, tests, and deployment targets remain
  provider-specific.
- Patch provider-specific source modules, regenerate the affected provider
  output, run provider validation and full parity validation, then install by
  snapshot.
- Unmanaged non-empty deployed doctrine outside managed markers is drift. The
  installer must require a decision to adopt/import it into source, discard it,
  or keep it only as a temporary unmanaged exception.
- When a correction, repeated miss, tool or workflow failure, verification gap,
  or repo-specific invariant should steer future agents, make a landing-surface
  decision before closeout instead of leaving the lesson in chat:
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
- Closeout must name the selected surface and verification. If no durable rule
  lands, closeout must say why the lesson was intentionally not made durable.
