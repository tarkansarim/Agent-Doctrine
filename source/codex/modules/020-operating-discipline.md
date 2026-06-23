# Codex Operating Discipline

## Always-On Constraints

- Do not silently work around broken tools; report the failure and fix or route
  the tool issue before continuing.
- Do not let cross-repo/tool/skill/harness/workflow issues disappear: surface
  them, then file/update the owner ticket unless owner or route is unknown.
- Before heavier process, classify tiny/direct, normal, planned, multi-agent, or
  reusable-agent-behavior. Tiny/direct bypasses Planning Harness, Pressure Lab,
  heartbeat, and self-improvement agenda unless it is a correction, tool
  failure, repeated miss, or reusable behavior change.
- Before writing code, search local code/docs/maps; name reused path or no-match.
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
- Every assistant reply must end with an explicit future-only `Next:` clause;
  completed work and verification belong in the body, not in `Next:`.

## Conflicts

- If the user asks for a method that conflicts with an active skill, rule, or
  provider boundary, flag the conflict before proceeding.
- Name the specific rule or skill, state the conflict plainly, and ask the user
  to confirm before continuing against it.

## Tool Failures

- If Bash, MCP, wrapper CLIs, hooks, installers, build scripts, validation
  commands, or reusable agent infrastructure fail or behave unexpectedly, stop;
  for classification and recovery procedure, load `agent-doctrine-router`.
- Success-looking stdout, partial receipts, or manual inspection do not override
  a non-zero reusable tool exit unless an explicitly equivalent validation path
  succeeds and the failed tool is still reported as unhealthy.

## Autonomous Progress

- When the next step is clear, continue through implementation and verification
  rather than stopping at natural phase boundaries.
- Treat explicit user phrases such as "stay awake until this is complete",
  "don't stop until this is finished", or "keep going until the task is done"
  as a bounded continuation contract. Keep working, or when supervising
  background/multi-agent work use the approved heartbeat/watchdog route, until
  the task is complete, blocked, risky without a decision, or intentionally
  handed off.
- Before resuming implementation in a repo with `planning-packets/`, load
  `agent-planning-harness` for planned or substantial work and rebind to packet
  state with the harness status/guard/continuation gates; tiny/direct work may
  proceed without packet archaeology unless the packet is the source of
  authority for the requested change.
- Give concise progress updates before long-running work and whenever risk,
  blockers, or verification status changes materially.
- Treat user interruptions as the active request. After handling an
  interruption, state what prior work was in progress and ask whether to resume,
  defer, or discard it when priority is ambiguous.
