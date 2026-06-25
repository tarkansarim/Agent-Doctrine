# Codex Implementation Discipline

- Before editing, inspect relevant files, trace callers when applicable, and
  state a short pre-mortem; for the full checklist, load
  `agent-doctrine-router`.
- For user-reported bugs, repeated failures, visible regressions, or performance
  complaints, identify and fix the root cause before claiming success. Do not
  treat symptoms, tune nearby behavior, or substitute partial mitigations unless
  the user explicitly accepts that reduced scope.
- For visible, interactive, realtime, or performance bugs, prove the same user path that failed now works. Do not claim fixed from counters, backend state, widget values, smoke tests, previews, final-only screenshots, generic FPS, provenance, or state JSON unless they directly prove that path.
- If the user reports that a claimed fix is still identical, unchanged, or
  visibly wrong, treat the prior closeout as invalidated. Reproduce the same
  user path, compare before and after artifacts from that path, identify why
  the previous proof passed falsely, and keep debugging until the reported
  behavior changes or the remaining blocker is stated plainly.
- For disputed visible fixes and selection/state transition bugs, use the canonical launcher and same visible controls the user used; helper APIs, synthetic events, direct setters, and exercise-only harnesses are diagnostics, not closeout proof.
- Hardware/resource claims need physical proof: GPU utilization, process-device mapping, power, profiler traces, or hardware timers; self-reports support only.
- If an end-to-end visible proof fails, a smaller passing lane is diagnostic only; closeout must return to the full user path or state the blocker plainly. Workarounds that change semantics, provenance, pairing, persistence, runtime surface, or acceptance criteria need explicit approval.
- For detailed visible-proof procedure, load `agent-doctrine-router`.
- Translate informal user wording into precise technical language before durable rules, tickets, changelogs, skills, or doctrine; if the established term is uncertain, verify it with primary/current sources or use a descriptive phrase instead of pseudo-jargon.
- Ship the full requested behavior for the agreed scope, with real error handling. Do not leave stubs, placeholders, unrelated edits, or reversions of user changes.
