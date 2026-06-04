# Claude Doctrine Change Routing

- Agent-Doctrine is the source-owned home for durable Claude `CLAUDE.md`
  doctrine. The deployed user-level file is a generated install target, not the
  source of truth.
- Deployed provider files are not normal source material. The exception is an
  explicit Agent-Doctrine adoption/import of existing live user-level doctrine,
  where the live file is read-only input that must be imported into
  provider-specific source before installation.
- Durable changes to Claude `CLAUDE.md` must be filed or routed as tickets to
  `<workspace root>/Agent-Doctrine`.
- Do not directly edit deployed provider doctrine to make a durable behavior
  change. Patch the Agent-Doctrine source modules, regenerate, validate parity,
  and install by snapshot.
- Doctrine files contain only short, always-true, every-turn-essential rules;
  all procedure and detail live in relay-pattern skills referenced by one-line
  pointers.
- Treat unmanaged non-empty deployed doctrine outside Agent-Doctrine managed
  markers as drift during install. Report the unmanaged sections and require a
  user decision to adopt/import them into source, discard them, or keep them
  only as a temporary unmanaged exception.
- For detailed routing procedure, load `agent-doctrine-router`.
- Keep provider lanes separate. Claude source modules, generated output,
  validators, installers, tests, and deployment target are separate from Codex.
