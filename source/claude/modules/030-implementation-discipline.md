# Claude Implementation Discipline

- Before editing, read relevant files, trace callers when a call chain exists,
  and state a short pre-mortem; for the full checklist, load
  `agent-doctrine-router`.
- During implementation, ship complete scoped behavior with real error handling
  and without stubs, placeholders, unrelated churn, or user-change reverts; for
  edit procedure, load `agent-doctrine-router`.
- Verify behavior before claiming success, and do not close a local Plane ticket
  with changed installed artifacts still uninstalled; for verification and
  ticket closeout procedure, load `agent-doctrine-router`.
