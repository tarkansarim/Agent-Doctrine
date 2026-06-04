# Codex Implementation Discipline

- Before editing, read relevant files, trace callers when a call chain exists,
  and state a short pre-mortem; for the full checklist, load
  `agent-doctrine-router`.
- During implementation, ship complete scoped behavior with real error handling
  and without stubs, placeholders, unrelated churn, or user-change reverts; for
  edit procedure, load `agent-doctrine-router`.
- Verify behavior before claiming success, and install or sync changed deployed
  artifacts before reporting resolution; for verification procedure, load
  `agent-doctrine-router`.
- When Python verifiers, test runners, build helpers, or agent tools repeatedly
  bottleneck, measure first and report timing: >60s repeated paths need an
  optimization note, >5 min critical paths need an active migration or
  parallelization recommendation, and >20 min repeated pipeline surfaces are
  performance debt to route or ticket unless already planned.
- Diagnose whether setup, file copying, subprocess dispatch, or core logic
  dominates before rewriting. Prefer parallel Python for independent dispatch
  bottlenecks, algorithm/data-layout fixes for avoidable repeated parsing or
  broad scans, Rust for agent-facing CLI verifiers, artifact validators, and
  JSON/text/file-heavy deterministic tooling, and C++ only when the hot path is
  already native, GPU/realtime, ABI-bound, or existing C++ domain code.
