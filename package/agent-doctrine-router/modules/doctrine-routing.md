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
