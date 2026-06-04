# Imported Codex Doctrine Source

- Source path: `<workspace root>/Emergence-Build-Harness/AGENTS.md`
- Source SHA256: `b23fdf9d54fe61e155281e17caaa1dd9b61df59c4e34dd545e6f80d0e09a454a`
- Provider lane: `codex`

## Original Content

# Emergence Build Harness Agent Rules

## Parallel Work Default

Use multi-agent or parallel lanes wherever the work can be split without shared
write conflicts. Good candidates are fresh reviews, independent source scans,
Pressure Lab interpretation, doc/audit checks, and unrelated implementation
slices with clear file ownership.

Keep the immediate critical path local. After spawning a parallel lane, keep
working on non-overlapping work instead of waiting by default. Wait only when
the result blocks the next local step, and merge findings through verification
rather than trusting reports.

Do not spawn agents for duplicate work, unclear ownership, or tightly coupled
edits. For review lanes, use a fresh-context reviewer and ask for concrete file
or test findings.

<!-- agent-self-improvement-doctrine:begin -->
## Accepted Self-Improvement Doctrine

- 2026-06-03T05:08:41Z [global] Pressure or hardening lanes that mutate fixture/run artifacts must isolate them with copies, not hardlinks, before mutation; hardlinks are allowed only for read-only fixtures. (source: self-improvement:friction:42022d0f8985c43a)
<!-- agent-self-improvement-doctrine:end -->
