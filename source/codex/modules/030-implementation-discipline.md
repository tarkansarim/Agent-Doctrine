# Codex Implementation Discipline

- Before editing, inspect relevant files, trace callers when applicable, and
  state a short pre-mortem; for the full checklist, load
  `agent-doctrine-router`.
- For user-reported bugs, repeated failures, visible regressions, or performance
  complaints, identify and fix the root cause before claiming success. Do not
  treat symptoms, tune nearby behavior, or substitute partial mitigations unless
  the user explicitly accepts that reduced scope.
- For visible or interactive behavior, close on proof of the exact user-visible
  path that was broken. Internal counters, backend readbacks, widget state,
  smoke-test completion, or preview-only behavior are supporting diagnostics,
  not proof that the issue is fixed.
- For visual, interactive, realtime, or performance fixes, name the exact
  user-visible invariant and the forbidden substitutes before accepting tests or
  closeout evidence. Proxy behavior, preview-only behavior, deferred
  finalization, final-only screenshots, non-empty image diffs, generic FPS,
  provenance, or state JSON cannot be primary proof unless they directly prove
  that invariant. A test that encodes the reported failure mode as success is a
  blocker, not validation.
- Translate informal user wording into precise technical language before writing
  durable rules, tickets, changelogs, skills, or doctrine. If the correct
  established term is uncertain, verify it with primary/current sources or web
  search before making it durable; otherwise use a descriptive phrase instead of
  pseudo-jargon.
- Ship complete scoped behavior with real error handling; no stubs,
  placeholders, unrelated churn, or user-change reverts.
