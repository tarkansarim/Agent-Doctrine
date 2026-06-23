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
- If the user reports that a claimed fix is still identical, unchanged, or
  visibly wrong, treat the prior closeout as invalidated. Reproduce the same
  user path, compare before and after artifacts from that path, identify why
  the previous proof passed falsely, and keep debugging until the reported
  behavior changes or the remaining blocker is stated plainly.
- After a disputed visible or interactive fix, helper APIs, synthetic events, direct setters, and exercise-only harnesses are diagnostics only; prove canonical launch provenance and real-input or manual-equivalent evidence through the same controls and held path before reclaiming success.
- For visual, interactive, realtime, or performance fixes, name the exact
  user-visible invariant and the forbidden substitutes before accepting tests or
  closeout evidence. Proxy behavior, preview-only behavior, deferred
  finalization, final-only screenshots, non-empty image diffs, generic FPS,
  provenance, or state JSON cannot be primary proof unless they directly prove
  that invariant. A test that encodes the reported failure mode as success is a
  blocker, not validation.
- If an end-to-end visible proof fails, a smaller passing lane is diagnostic only; closeout must return to the full user path or state the blocker plainly.
- For visible selection-to-result bugs, one primary artifact must show the input/control and output together, plus a negative assertion for the reported wrong result; separate state, crops, readbacks, helper-driven proof modes, scripted control setters, or metrics are supporting evidence only. The primary validator must be able to fail when the exact user-reported visible mismatch is still present.
- For visible state or mode transition bugs, the primary proof must show the state/control transition and the immediate first user action result in the same canonical path, plus a negative assertion for the reported ignored, stale, or delayed first action.
- Translate informal user wording into precise technical language before durable rules, tickets, changelogs, skills, or doctrine; if the established term is uncertain, verify it with primary/current sources or use a descriptive phrase instead of pseudo-jargon.
- Ship complete scoped behavior with real error handling; no stubs,
  placeholders, unrelated churn, or user-change reverts.
