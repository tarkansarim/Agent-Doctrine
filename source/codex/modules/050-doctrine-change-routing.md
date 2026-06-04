# Codex Doctrine Change Routing

- Agent-Doctrine is the source-owned home for durable Codex `AGENTS.md`;
  deployed user-level files are generated install targets, not source.
- Deployed provider files are not normal source material; explicit
  adoption/import reads live files only as read-only input.
- Durable changes to Codex `AGENTS.md` must be made in
  `<workspace root>/Agent-Doctrine`.
- Do not edit deployed provider doctrine for durable behavior changes; patch
  source modules, regenerate, validate parity, and install by snapshot.
- Doctrine files contain only short, always-true, every-turn-essential rules;
  all procedure and detail live in relay-pattern skills referenced by one-line
  pointers.
- Treat unmanaged deployed doctrine outside managed markers as install drift
  requiring a user decision: adopt/import, discard, or temporary exception.
- For detailed routing procedure, load `agent-doctrine-router`.
- Keep provider lanes separate. Codex source modules, generated output,
  validators, installers, tests, and deployment target are separate from Claude.
