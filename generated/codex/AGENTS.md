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

# Codex Implementation Discipline

- Before editing, read relevant files, trace callers when a call chain exists,
  and state a short pre-mortem; for the full checklist, load
  `agent-doctrine-router`.
- During implementation, ship complete scoped behavior with real error handling
  and without stubs, placeholders, unrelated churn, or user-change reverts; for
  edit procedure, load `agent-doctrine-router`.
- Verify behavior before claiming success, and install or sync changed deployed
  artifacts before reporting resolution; for verification procedure, load
  `agent-doctrine-router`.
- When Python verifiers, test runners, build helpers, or agent tools repeatedly
  bottleneck, measure first and report timing: >60s repeated paths need an
  optimization note, >5 min critical paths need an active migration or
  parallelization recommendation, and >20 min repeated pipeline surfaces are
  performance debt to route or ticket unless already planned.
- Diagnose whether setup, file copying, subprocess dispatch, or core logic
  dominates before rewriting. Prefer parallel Python for independent dispatch
  bottlenecks, algorithm/data-layout fixes for avoidable repeated parsing or
  broad scans, Rust for agent-facing CLI verifiers, artifact validators, and
  JSON/text/file-heavy deterministic tooling, and C++ only when the hot path is
  already native, GPU/realtime, ABI-bound, or existing C++ domain code.

# Local Plane Ticketing

- Local ticket requests use Plane via `~/.local/bin/plane-ticket`; repo-scoped
  tickets must include `--project <RepoName>`, tag `project:<RepoName>`, and
  tag `worker:codex` or `worker:claude` unless explicitly `--unrouted`.
- Do not use Kanboard for new tickets unless explicitly requested; for Plane
  filing and closeout procedure, load `agent-doctrine-router`.

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

<!-- agent-doctrine:codex:end -->
