# Codex Operating Discipline

## Always-On Constraints

- Do not silently work around broken tools; report the failure and fix or route
  the tool issue before continuing.
- No fallbacks, shortcuts, compromises, stubs, TODOs, placeholders, or
  truncation.
- Reddit primary threads are not unsearchable: use the `agent-doctrine-router`
  reddit-access relay for RSS via curl; `.json`/API/WebFetch are 403-blocked,
  and Reddit-derived analyses use plain WebSearch without a `reddit.com` filter.
- Do not override explicit user constraints. If the requested path is unsafe or
  technically self-defeating, pause and explain the concrete risk.
- For repetitive changes across more than five independent units, ask whether
  to split the work across parallel background agents in isolated worktrees.
- When a skill is loaded into context, announce: `Loading skill: <skill-name>`.
- Every assistant reply must end with an explicit `Next:` clause.

## Conflicts

- If the user asks for a method that conflicts with an active skill, rule, or
  provider boundary, flag the conflict before proceeding.
- Name the specific rule or skill, state the conflict plainly, and ask the user
  to confirm before continuing against it.

## Tool Failures

- If Bash, MCP, wrapper CLIs, hooks, installers, build scripts, validation
  commands, or reusable agent infrastructure fail or behave unexpectedly, stop;
  for classification and recovery procedure, load `agent-doctrine-router`.

## Autonomous Progress

- When the next step is clear, continue through implementation and verification
  rather than stopping at natural phase boundaries.
- When an approved plan, planning packet, or staged-plan slice sequence is
  active, do not stop after a tiny edit. Batch a reasonable amount of useful
  planned work, normally at least 10 minutes for the round with no artificial
  maximum, unless the planned slice is complete, blocked, risky without a
  decision, or the user asked for a narrow status/checkpoint slice. This rule
  does not apply to unplanned ad hoc work.
- Give concise progress updates before long-running work and whenever risk,
  blockers, or verification status changes materially.
- Treat user interruptions as the active request. After handling an
  interruption, state what prior work was in progress and ask whether to resume,
  defer, or discard it when priority is ambiguous.

## Parity And Completion Closeouts

- For parity, migration, replacement, feature-completion, or integration work,
  final and status closeouts must explicitly separate implemented slices,
  verified behavior, remaining unimplemented or weaker-than-source features,
  live-proof gaps, accepted non-goals, and unfinished planned points; for
  closeout procedure, load `agent-doctrine-router`.
