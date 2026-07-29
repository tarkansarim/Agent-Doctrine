# Claude Replay And Learning

<!-- agent-doctrine-rule:rewind.opt-in -->
- Use Rewind or the active Claude replay, checkpoint, or rollback mechanism when
  the user requests it, a destructive or broad experiment needs restoration, or
  same-branch causal evidence matters. Do not initialize or snapshot a replay
  mechanism merely because work is substantive, visible, or a correction.
<!-- agent-doctrine-rule:rewind.causal-evidence -->
- Do not claim causal replay from a later forward correction; same-branch-point claims require a checkpoint from before the decision.
<!-- agent-doctrine-rule:rewind.rollback-anchor -->
- Before destructive operations, broad mechanical rewrites, experimental probes,
  or a second fix attempt that would stack on an unproven first attempt, confirm
  a rollback anchor. For ordinary scoped Git edits, current `HEAD` plus a full
  changed-file inventory is sufficient when no overlapping uncommitted work is
  endangered; use a commit or explicit manual checkpoint only when Git cannot
  preserve the state that must survive.
<!-- agent-doctrine-rule:rewind.router -->
- For rollback anchors, same-branch replay, Rewind checkpoints, hook review, or fork comparison, load `rewind-checkpoints`.
<!-- agent-doctrine-rule:learning.self-improvement-suspended -->
- The `self-improving` skill and `agent-self-improve` CLI are suspended unless
  the user explicitly asks to use them. Do not automatically run `agenda`,
  `status`, `record`, `enqueue`, `reliability-gate`, or `review-add`.
<!-- agent-doctrine-rule:learning.durable-surface -->
- Before closing a repeated miss, workflow failure, or reusable agent/tool/harness/workflow/doctrine
  lesson, choose and name its durable surface: none, runtime record only when
  explicitly requested, repo doctrine, promotion candidate, provider doctrine,
  or tool/ticket. Provider doctrine routes through Agent-Doctrine
  source/generate/validate/install. An ordinary repository code fix needs no durable-surface label unless it exposes such a reusable lesson.
<!-- agent-doctrine-rule:learning.no-false-self-improvement -->
- While the mechanism is suspended, do not call ordinary source-rule, skill,
  repo-document, tool, or ticket changes self-improvement. Name the actual
  durable surface that changed.
<!-- agent-doctrine-rule:learning.thrashing-stop -->
- If reusable agent behavior, skills, hooks, wrappers, installers, or doctrine
  appear to be thrashing, pause mutation of the suspect mechanism, continue
  unaffected work, report the evidence, and ask before broad rule/tool rewrites.
