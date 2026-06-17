# Codex Implementation Discipline

- Before editing, inspect relevant files, trace callers when applicable, and
  state a short pre-mortem; for the full checklist, load
  `agent-doctrine-router`.
- Ship complete scoped behavior with real error handling; no stubs,
  placeholders, unrelated churn, or user-change reverts.
