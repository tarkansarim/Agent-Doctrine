<!-- agent-doctrine:codex:begin -->
# Codex Configuration Boundary

- Codex user rules, protocols, skills, hooks, and memory live under `~/.codex`
  unless the user explicitly says otherwise.
- Do not read from or patch `~/.claude` for Codex behavior; only explicit
  Agent-Doctrine adoption/import may read `~/.claude/CLAUDE.md` as source.
- Translate copied Claude-owned paths to Codex equivalents without inspecting
  Claude files.
- Do not directly patch deployed user-level `~/.codex/AGENTS.md`. Durable
  doctrine changes are source-owned by the Agent-Doctrine repo and must flow
  through its source generation and install pipeline.

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

# Codex Pressure-Lab Hardenability (Build-Time Constraint)

- For agent-facing skills, hooks, CLIs, validators, artifact grammars,
  behavior contracts, and workflows, load `pressure-lab`.

# Codex Rewind And Learning

- Use Rewind as the opt-in rollback and causal replay substrate for
  substantive coding, reusable-agent behavior, hooks, skills, wrappers,
  doctrine, and risky probes.
- Do not treat a forward correction after a mistake as Rewind causal evidence.
  Same-branch-point claims require a checkpoint from before the decision.
- Patch stacking is allowed only as a temporary exploratory or repair-diagnostic
  phase after a verified rollback anchor exists. Use the prior hook-created
  Rewind checkpoint when automatic coverage is active; otherwise create an
  explicit commit/manual checkpoint. Once the real fix is known, record the
  lesson, restore to the anchor, and apply the fix cleanly.
- For detailed replay, checkpoint, Rewind, hook-review, fork, and fabric-drift
  procedure, load `rewind-checkpoints`.
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
- For native C++ GPU, realtime rendering or visualization, C++ GPU code maps,
  Vulkan, CUDA, or mixed CUDA/Vulkan work, load `cpp-cuda-vulkan-studio`.

# Codex Doctrine Change Routing

- Agent-Doctrine is the source-owned home for durable Codex `AGENTS.md`;
  deployed user-level files are generated install targets, not source.
- Deployed provider files are not normal source material; explicit
  adoption/import reads live files only as read-only input.
- Durable changes to Codex `AGENTS.md` must be made in
  `<workspace root>/Agent-Doctrine`.
- Do not edit deployed provider doctrine for durable behavior changes; patch
  source modules, regenerate, validate parity, and install by snapshot.
- Doctrine files contain only short, always-true, every-turn-essential rules;
  all procedure and detail live in relay-pattern skills referenced by one-line
  pointers.
- Treat unmanaged deployed doctrine outside managed markers as install drift
  requiring a user decision: adopt/import, discard, or temporary exception.
- For detailed routing procedure, load `agent-doctrine-router`.
- Keep provider lanes separate. Codex source modules, generated output,
  validators, installers, tests, and deployment target are separate from Claude.

<!-- cppstudio-user-agents-relay:begin -->
## CppStudio Skill Relay

For native C++ GPU, realtime rendering/visualization, C++ GPU code-map, Vulkan, CUDA, or mixed
CUDA/Vulkan work, load `cpp-cuda-vulkan-studio`.
<!-- cppstudio-user-agents-relay:end -->

<!-- agent-doctrine:codex:end -->
