# Claude Replay And Learning

- Use Rewind or the active Claude replay, checkpoint, or rollback mechanism
  when a task depends on same-branch-point evidence, risky probes, or reusable
  behavior changes. Do not claim causal replay from a later forward correction.
- Before risky moves or new substantial work, confirm a clean rollback anchor: commit intentional worktree changes or create an explicit manual checkpoint; this covers ordinary repo coding, UI/runtime edits, destructive file operations, broad mechanical rewrites, and experimental probes.
- Patch stacking is temporary repair-diagnostic work after a verified rollback anchor exists: use hook-created Rewind when automatic coverage is active, otherwise use an explicit commit/manual checkpoint; once the fix is known, record the lesson, restore to the anchor, and apply it cleanly.
- For rollback anchors, same-branch replay, Rewind checkpoints, hook review, or fork comparison, load `rewind-checkpoints`.
- For tool failures, repeated misses, verification gaps, durable lessons, and
  reliability claims, load `self-improving`.
- Before closing a correction, repeated miss, workflow failure, or reusable lesson, choose and name its durable surface: none, runtime record, repo doctrine, promotion candidate, provider doctrine, or tool/ticket. Provider doctrine routes through Agent-Doctrine source/generate/validate/install.
- When saying self-improvement happened, name the proof. Only call it a self-improvement record if `agent-self-improve` recorded it.
- If reusable agent behavior, skills, hooks, wrappers, installers, or doctrine
  appear to be thrashing, stop further environment mutation, record a blocking
  self-improvement friction item, report evidence, and wait for approval.
