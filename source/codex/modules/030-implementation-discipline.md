# Codex Implementation Discipline

<!-- agent-doctrine-rule:implementation.premortem -->
- Before editing, inspect relevant files and trace callers when applicable. Add
  a short pre-mortem only for guarded-direct, planned/substantial, destructive,
  or hard-to-reverse work; tiny/direct changes do not require one.
<!-- agent-doctrine-rule:implementation.root-cause -->
- For user-reported bugs, repeated failures, visible regressions, or performance
  complaints, identify and fix the root cause before claiming success. Do not
  treat symptoms, tune nearby behavior, or substitute partial mitigations unless
  the user explicitly accepts that reduced scope.
<!-- agent-doctrine-rule:implementation.exact-visible-path -->
- For visible, interactive, realtime, or performance bugs, prove the same user path that failed now works. Do not claim fixed from counters, backend state, widget values, smoke tests, previews, final-only screenshots, generic FPS, provenance, or state JSON unless they directly prove that path. If exact replay would itself mutate real user data, spend money, trigger an external/destructive action, or alter history, do not manufacture live proof: use a focused regression plus persisted-state readback after a full restart of the canonical runtime, report the exact interaction as awaiting user confirmation, and do not claim that interaction verified until confirmed.
<!-- agent-doctrine-rule:implementation.disputed-claim -->
- If the user reports that a claimed fix is still identical, unchanged, or
  visibly wrong, treat the prior closeout as invalidated. Reproduce the same
  user path, compare before and after artifacts from that path, identify why
  the previous proof passed falsely, and keep debugging until the reported
  behavior changes or the remaining blocker is stated plainly.
<!-- agent-doctrine-rule:implementation.canonical-visible-controls -->
- For disputed visible fixes and selection/state transition bugs, use the canonical launcher and same visible controls the user used; helper APIs, synthetic events, direct setters, and exercise-only harnesses are diagnostics, not closeout proof.
<!-- agent-doctrine-rule:implementation.hardware-proof -->
- Hardware/resource claims need physical proof: GPU utilization, process-device mapping, power, profiler traces, or hardware timers; self-reports support only.
<!-- agent-doctrine-rule:implementation.end-to-end-proof -->
- If an end-to-end visible proof fails, a smaller passing lane is diagnostic only; closeout must return to the full user path or state the blocker plainly. When exact replay is intentionally deferred because it would cause a protected side effect, use the non-destructive proof rule above and leave the interaction unverified pending user confirmation. Workarounds that change semantics, provenance, pairing, persistence, runtime surface, or acceptance criteria need explicit approval.
<!-- agent-doctrine-rule:implementation.terminology -->
- Translate informal user wording into precise technical language before durable rules, tickets, changelogs, skills, or doctrine; if the established term is uncertain, verify it with primary/current sources or use a descriptive phrase instead of pseudo-jargon.
<!-- agent-doctrine-rule:implementation.complete-scope -->
- Ship the full requested behavior for the agreed scope, with real error handling. Do not leave stubs, placeholders, unrelated edits, or reversions of user changes.
