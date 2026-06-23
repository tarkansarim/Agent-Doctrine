# Claude Replay And Learning

- Use Rewind or the active Claude replay, checkpoint, or rollback mechanism
  when a task depends on same-branch-point evidence, risky probes, or reusable
  behavior changes. Do not claim causal replay from a later forward correction.
- Patch stacking is allowed only as a temporary exploratory or repair-diagnostic
  phase after a verified rollback anchor exists. Use the prior hook-created
  Rewind checkpoint when automatic coverage is active; otherwise create an
  explicit commit/manual checkpoint. Once the real fix is known, record the
  lesson, restore to the anchor, and apply the fix cleanly.
- For detailed replay, checkpoint, Rewind, branch, and fabric-drift procedure,
  load `rewind-checkpoints`.
- For tool failures, repeated misses, verification gaps, durable lessons, and
  reliability claims, load `self-improving`.
- When a correction, repeated miss, workflow failure, or reusable repo-specific
  lesson should change future agent behavior, classify the landing surface before
  closeout: no-action with reason, runtime record only, repo-local durable
  doctrine, promotion-candidate, provider-general doctrine, or tooling/ticket.
  Provider-general lessons must route through Agent-Doctrine
  source/generate/validate/install; ambiguous cross-repo lessons stay local and
  open a promotion candidate.
- When a closeout or status says self-improvement happened, name and verify the
  landing surface: runtime record id, repo doctrine target, provider-doctrine
  route, or code-only verifier/tool hardening. Do not call code hardening a
  self-improvement record unless `agent-self-improve` actually recorded it.
- If reusable agent behavior, skills, hooks, wrappers, installers, or doctrine
  appear to be thrashing, stop further environment mutation, record a blocking
  self-improvement friction item, report evidence, and wait for approval.
