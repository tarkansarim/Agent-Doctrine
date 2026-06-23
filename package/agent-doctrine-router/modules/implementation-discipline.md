# Implementation Discipline Procedure

Use this module when provider doctrine says to load `agent-doctrine-router` for
implementation, editing, dependency, or verification procedure.

## Before Editing

- Read the relevant files completely, not only the function or section that
  looks likely to change.
- Trace modified functions at least two callers deep when a call chain exists.
- Identify all direct callers of functions being modified.
- State a short pre-mortem with the three most likely mistakes and how they will
  be prevented.
- Codex default implementation depth is Tier 2; quick requests narrow scope,
  while thorough or exhaustive requests broaden callers, failure modes, and
  verification.
- Codex interprets implement, fix, refactor, and optimize as complete
  implementation, root-cause repair, full dependent-code update, and
  profile-first work.
- If MCP tool arguments are lost, treat it as a tool issue: capture version and
  repro evidence before changing architecture or assuming a fixed tool-count
  cap.

## While Editing

- Implement complete behavior with real error handling.
- Do not leave stubs, TODOs, placeholders, or ellipses such as
  `... rest unchanged`.
- Match local naming, formatting, and ownership boundaries.
- Keep changes scoped to the request. Avoid unrelated refactors and metadata
  churn.
- Do not revert user changes. If the worktree contains unrelated dirty files,
  leave them alone.
- Use project-local virtual environments for Python dependencies. If no venv
  exists and dependencies must be installed, create one first.

## Verification

- Never claim a fix worked without running an appropriate verification command
  or behavior check.
- For visible or user-reported bugs, reproduce the exact reported behavior or
  an equivalent path before the fix, then compare the same path after the fix.
- If the user reports that a claimed fix is still identical, unchanged, or
  visibly wrong, treat the previous closeout as invalidated evidence. Re-run the
  same user path, compare current artifacts against the reported symptom, find
  the false-positive proof gap, and continue debugging or report the concrete
  blocker.
- If an end-to-end visible proof fails, do not narrow the proof into a smaller
  passing acceptance lane. Use narrower runs only to diagnose where the full
  path failed, then return to the full user path for closeout.
- For visible selection-to-result bugs, the primary proof artifact must show the
  user-visible input/control state and the resulting output together, with a
  negative assertion for the reported wrong result. Separate control state,
  app-owned crops, readbacks, helper-driven proof modes, scripted control
  setters, or metric artifacts are supporting evidence only. The primary
  validator must be able to fail when the exact user-reported visible mismatch
  is still present.
- For visible state or mode transition bugs, the primary proof must show the
  state/control transition and the immediate first user action result in the same
  canonical path, plus a negative assertion for the reported ignored, stale, or
  delayed first action.
- After repository changes, report at least one explicit verification command;
  diff/status checks alone are not enough for completion.
- When source changes affect installed artifacts, install, roll out, or sync
  those artifacts immediately after validation before reporting the work
  resolved.
- State assumptions and whether placeholders or simplifications remain. If none
  remain, say so.
