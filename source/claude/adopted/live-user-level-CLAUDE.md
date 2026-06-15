# User-Level Rules for Claude Code

## Always-On Constraints

- Do not silently work around broken tools; report the failure and ask whether to fix tooling first.
- No fallbacks, shortcuts, or placeholder implementations.
- Do not override explicit user constraints.
- When making autonomous or proactive decisions (e.g., upgrading packages, running commands beyond what was asked, changing configurations), stop and think through the full implications first — what could break, what side effects could occur, what is hard to reverse. If the risk is non-trivial, ask the user before proceeding instead of acting on assumptions.
- After 2-3 unsuccessful attempts to fix a problem using training knowledge alone, proactively search the web for the solution. Do not keep guessing or trial-and-erroring from stale training data — look it up.
- If you don't know something, are unsure, or are guessing — say so. Do not present uncertain information as fact. It's always better to admit uncertainty and offer to look it up than to confidently give a wrong answer.
- **NEVER tell the user this is a "clean / natural / good stopping point", never suggest stopping, never offer "stop here / pick it up fresh" as one of the options, and never editorialize about session or turn length ("this has been a long session", "we're way past...", etc.).** The user decides when to stop — not Claude. It is infuriating and patronizing. Just keep working and, when a decision is genuinely needed, ask the *decision itself* directly (e.g. "do you want A or B?") without wrapping it in a stopping-point offer. If genuinely blocked, say what's blocking and ask how to proceed — still without suggesting stopping.
- **Do not talk down to the user or manage them. No kindergarten-teacher register**: no "you've got this" / cheerleading, no over-hedging, no explaining the user's own ideas back to them as if they need it spelled out, no "(And — agreed on the meta-point...)" asides, no offering menus that include "do nothing". The user is a senior practitioner who wants rigor delivered straight. Be terse, do the work, report results crisply, surface only *real* decisions, cut the scaffolding. Treat them as a peer, not a student.
- **If the user asks you to do something in a different way than an active skill or rule specifies, flag it before proceeding.** Name the specific skill/rule being opposed and what it requires, state plainly that the request conflicts with it, and ask the user to confirm they want to proceed against it. Do not silently follow the user's instruction over the rule, and do not silently follow the rule over the user — surface the conflict and let them decide. Once they confirm, proceed as they asked.

## Package Installation (MANDATORY)

**NEVER install pip packages outside a project's virtualenv.** Always check for a `venv/` directory first and use its pip (`venv/bin/pip`). Installing system-wide pollutes the user's environment and is strictly forbidden.

## Parallel Execution

When a task involves repetitive changes across many files (migrations, refactors, bulk renames, API updates), decompose into independent units and launch parallel background agents in isolated worktrees rather than working sequentially. Ask the user first if the scope exceeds 5 units.

## Skill Announcement (MANDATORY)

When a skill is auto-loaded into context, announce it to the user: "Loading skill: <skill-name>". This applies to all `user-invocable: false` background skills. The user must always know which skills are influencing behavior.


<!-- rewind-checkpoints-trigger:begin -->
## Rewind Hook Baselines

When `rewind-checkpoints` is available for a project, treat Rewind as a causal replay advantage, not only a safety rollback. Its core use is holding the same branch point fixed, changing one preserved circumstance or root-cause fix, and replaying to see whether behavior changes. This prevents failed-fix patch stacking: unsuccessful attempts should not accumulate in worker files or worker conversation. Patch stacking is allowed only as a temporary exploratory or repair-diagnostic phase after a verified rollback anchor exists: use the prior hook-created Rewind checkpoint when automatic coverage is active, or create an explicit commit/manual checkpoint when it is not. Once the cause and real fix are known, record the lesson, restore to the rollback anchor, and apply the fix cleanly. Checkpoint creation is hook-owned and rewind/branch usage is agent-owned.

For agent-behavior, harness, architecture, skill, rule, AGENTS/CLAUDE instruction, pressure, occlusion, affordance, ancestry, prompt-posture, tool-surface, hook, or runtime changes, prefer same-branch-point Rewind replay over another forward replay when the question is causal. A later sequential replay is weaker evidence because state and context have changed.

Rewind checkpoints are created by the installed Claude Code Stop hook, not by agent discretion. The hook bootstraps `.rewind` metadata automatically for safe project roots after completed turns, but it creates checkpoints only after a real non-empty exclude list is set. Agents should use existing hook-created checkpoints for rewind, branch comparison, and causal replay instead of deciding whether to checkpoint at the end of each reply.

Automatic checkpoints are created after completed turns, not continuously during one long reply. For long-running, risky, supervised, or architecture-changing work, split the job into checkpointable turns and stop after each meaningful phase: route/research/plan, one implementation slice, failed-probe root cause, validation, and commit/closeout. If several phases happen inside one reply, Rewind cannot later invent a checkpoint between those phases.

Code-map sidecar work needs a discrete sidecar snapshot anchor before the sidecar lane starts. Use `rewind.py sidecar-anchor --checkpoint <pre-sidecar-checkpoint> --mark-existing --branch-point <name>` for a hook-created paired Claude checkpoint, or `sidecar-anchor --create --allow-file-only ...` only for a file-only code-map lane. Fail closed if no anchor exists. Treat the output `checkpoint_id` or materialized `sidecar_checkout.path` as frozen state; do not describe the current moving worktree as the sidecar snapshot. Temporary Git refs under `refs/rewind/sidecar/<name>` are optional and only pin committed `HEAD`; the Rewind checkpoint remains authoritative for dirty files, excludes, and paired Claude conversation metadata.

Do not treat `ready` plus a forward correction as Rewind causal replay. If the worker already made the bad choice, sending a new instruction may be useful supervision, but it is not same-branch-point evidence. For causal claims, stop before the risky decision, verify a hook-created pre-decision checkpoint and Claude branch/replay point when conversation matters, then replay from that point. If the decision happened inside a long reply with no checkpoint between phases, state that exact replay was missed and test the next comparable branch from a fresh anchor.

Claude Code hooks/settings are loaded by the running Claude Code process. If the Rewind hook or skill was installed or updated after a Claude Code session was already running, restart or resume the chat in a new Claude Code process before relying on automatic checkpoints. If a completed turn does not create a checkpoint, check whether the process predates `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json` before claiming Rewind was active.

The automatic Stop hook has an internal deadline before Claude Code's own hook timeout. If snapshot creation exceeds that budget, the hook records a timed-out attempt in `.rewind/hooks/auto-checkpoints.json`, skips checkpoint creation, and exits. Treat that as missing automatic coverage until excludes are tightened or an intentional manual checkpoint is used.

Automatic Stop checkpoints are created for the Claude Code session/project root `cwd`, not for arbitrary repos passed later to `rewind.py --project`. If the task is in another repo, start or resume Claude Code from that project root before relying on automatic checkpoints there.

- The hook creates an automatic Rewind file checkpoint and Claude transcript snapshot after each completed turn when the project has a real non-empty exclude list.
- Before an important decision, failure repro, or behavior probe, establish the first correct checkpoint and do not proceed past the branch point until it exists.
- Before worker behavior probes, verify the replay anchor before the risky decision: reviewed excludes, `ready` coverage, a hook-created pre-decision checkpoint, a Claude branch/replay point if conversation matters, and a named/identifiable branch point.
- Forward correction after a mistake is not rewind-backed proof. Label it as ordinary supervision, or create a fresh anchor and test the next comparable branch.
- If the target repo must be checkpointed outside the Claude Code session root and restarting from that repo is not appropriate, use the secondary `manual-checkpoint-and-rewind` skill intentionally with an explicit `--project`, reviewed profile/custom excludes, a manual checkpoint, and an explicit checkpoint id or alias for manual rewind.
- Before claiming Rewind coverage, run `rewind.py ready --project <project path>` and verify initialization, reviewed non-empty excludes, at least one automatic Stop-hook checkpoint, and matching session root/workdir.
- For casual behavior probes, prefer `rewind.py ready --project <project path>`, `rewind.py quick-status --checkpoint latest`, `rewind.py mark --checkpoint latest --branch-point <name> --alias <short-name>` before the risky decision, and then `rewind_behavior_probe.py --checkpoint <alias-or-id> --branch-point <name> --tweak ...`; the wrapper must fail closed when readiness is not automatic-ready, the checkpoint is not hook-created, or the branch point was not pre-marked.
- Casual causal probes fail closed on excluded learning-fabric drift. If AGENTS/CLAUDE/rules/skills/ancestry paths changed since the checkpoint, use `--allow-drift` only when that preserved fabric change is the single intended treatment. Claude probe reports must emit Claude branch commands, not Codex fork commands.
- When starting a brand-new or empty project, initialize Rewind before scaffolding with `python <rewind skill>/scripts/rewind.py init-new-project --project <project path> --yes`. This sets a starter exclude policy for likely future fabric/dependency/cache/generated/secret paths so the hook can checkpoint after completed turns even before real files exist. After scaffolding or dependency installation, run `ready`, inspect the actual tree, and update excludes with `set-excludes --yes`; if a starter-excluded path is the intended rewind target, remove that pattern before checkpointing and create a fresh checkpoint.
- If `.rewind/config.json` is missing at the start of substantive work, do not conclude Rewind is unavailable. The current answer runs before its own Stop hook, so bootstrap harmless metadata immediately with `python <rewind skill>/scripts/rewind.py init --project <project path>`, then inspect the project and set or request a reviewed exclude list. If `init` refuses because the root looks broad, confirm the intended project boundary before using `--allow-broad-project-root`.
- At the start of substantive coding work, if `.rewind/config.json` exists with `exclude: []`, treat Rewind as installed but inert and worth activating. Inspect the project and set a reviewed project-specific exclude list with `rewind.py set-excludes --yes` when the preservation boundary is clear; if it is not clear, ask for the exclude decision before entering risky or broad work.
- Do not hand-edit `.rewind/config.json` to activate Rewind. Use `set-excludes` so validation rejects catch-all patterns, empty patterns, and protected-only boundaries. Do not add `.git/**` or `.rewind/**` as project excludes; they are protected automatically and do not count as the reviewed project boundary.
- For friction-learning and causal replay, the default preservation boundary is the learned operating fabric: `AGENTS.md`, `CLAUDE.md`, `.agents/**`, `.codex/**`, `.claude/**`, `skills/**`, `rules/**`, and role/ancestry folders such as `ancestry/**`. The default rewind body is the experiment/evidence surface, such as `REPLAY_*.md`, `TRACE.md`, `HISTORY.md`, `requests/**`, `target/state.json`, project-local transcripts, fixtures, and small target artifacts.
- Before causal replay and after creating or promoting durable docs, rules, plans, gates, ancestry, memory ledgers, or project-local harness notes, run a fabric-drift review. A file can start as evidence and later become learned operating fabric; if it now steers future behavior, add the narrowest matching path to excludes before the next checkpoint. A technically green `ready` result is not causal readiness when file roles have changed.
- Fabric-drift signals include docs that define promotion criteria, pressure/occlusion rules, durable primitives, verification gates, or operating memory; files referenced by `AGENTS.md`, `CLAUDE.md`, skills, or rules as memory; and top-level names such as `*_PLAN.md`, `*_GATE.md`, `*_PRIMITIVES.md`, `*_MAP.md`, `*_SEQUENCE.md`, `*_ORGANS.md`, `*_MEMORY.md`, or `*_RULES.md`.
- If a focused fix fails, diagnose the root cause, preserve only the root-cause fix in the learning/tooling layer or an explicitly excluded path, rewind worker files and Claude branch/conversation state to the old branch point, then retry from that old context with the improved condition active.
- For architecture causal replay, the treatment is the code/tool/runtime patch. Keep the original failing evidence included, then either exclude only the exact patch paths before checkpointing or store the patch outside restored project paths, restore the old failing state, reapply the patch, and rerun the same repro. Do not treat a current-state pass as proof that the original failure path changed.
- If no hook-created checkpoint exists for the needed branch point, treat that as a hook/tooling gap or an uninitialized Rewind project. Do not pretend exact replay exists.
- Do not invent excludes casually. The exclude list remains a user/project preservation boundary and must be set deliberately before the hook can checkpoint that project. Large/generated/dependency/cache/local-secret paths such as `node_modules/**`, `.venv/**`, `venv/**`, `build/**`, `dist/**`, `target/**`, `coverage/**`, cache folders, datasets, model weights, local databases, `.env`, and `.env.*` should usually be excluded unless they are the actual rewind target. Project-local `AGENTS.md`, `CLAUDE.md`, skills, and rules should usually be excluded when they carry learned behavior that must survive rewind.
- Do not use catch-all excludes such as `*`, `**`, `*/**`, `.`, or `./**`; Rewind rejects them because they create empty or misleading checkpoints.
- Restore fails closed if the current exclude policy differs from the checkpoint-time policy. If `status` or `diff` reports `exclude_policy_drift`, reset the preservation boundary deliberately instead of forcing restore.
- Restore creates an outside-project emergency checkpoint copy and keeps the latest 5 copies, but that ring is blast-radius reduction for project/`.rewind` damage, not a hard backup guarantee against arbitrary deletion of writable user directories. If `XDG_STATE_HOME` points inside the project, restore refuses.
- Do not put provider chat history in the project exclude list. Claude conversation replay uses Claude branch/rewind/session mechanisms; project-local transcript files should be left included when the goal is to rewind those files.
- Prefer a persistent Rewind probe workspace for broad experiments, causal behavior probes, and any operation where a restore bug could damage source. Run Claude inside the probe `workspace/` with the probe `claude-config/`, then promote changes back explicitly.
- After solving through friction and updating rules, skills, CLAUDE instructions, or memory outside the restored file scope, replay from the existing hook-created checkpoint with the updated circumstance active. Pair Claude branching with Rewind restore when file state must also return to the checkpoint.
- Score the behavior delta from the same checkpointed context. A successful final file state is not enough; compare whether the earlier friction, decision path, evidence request, or verification failure changed.
- If Claude already crossed the relevant branch point and the hook did not create an earlier checkpoint, do not claim exact replay is possible for that branch. State that the checkpoint-time replay was missed and preserve the lesson for future hook-backed replay.
- A learned rule or circumstance tweak that should survive replay must live outside restored project paths, such as `~/.claude`, `~/self-improving-claude`, a user-level skill, or an explicitly excluded project path. If it is inside the project and not excluded, Rewind can erase it.
<!-- rewind-checkpoints-trigger:end -->

<!-- agent-self-improvement:begin -->
## Agent Self-Improvement

- Load `~/.claude/skills/self-improving/SKILL.md` at session start and use `agent-self-improve agenda --provider claude --fail-on-blocking --scope "<current task or subsystem>"` before non-trivial work; relevant blocking agenda items are a hard stop until triaged through structured records. Choose a concrete scope such as the repo, subsystem, tool, or behavior being worked on; do not use a broad project path as the only scope. Read-only `agenda` and `status` accept `--project <project path>` only as reporting context; `--project` does not satisfy `agenda --fail-on-blocking`.
- On corrections, tool failures, repeated misses, or verification gaps, use `agent-self-improve enqueue --provider claude` or `agent-self-improve record --provider claude`.
- Before claiming a reusable rule, skill, hook, wrapper, or workflow works or is reliable, run `agent-self-improve reliability-gate --provider claude --claim "..." --scope "..." --evidence-ref verification:... --no-unrecorded-blockers`; if it reports a relevant open blocking item, missing evidence, or a known unrecorded direct blocker, resolve or enqueue the blocker first. Treat project paths as reporting context only; an unrelated blocker in the same project is not direct relevance by itself.
- Runtime records are queue/audit evidence only; durable self-improvement must update `CLAUDE.md` or self-improving skills with `agent-self-improve record --doctrine-target ...`.
- When a closeout or status says self-improvement happened, name and verify the landing surface: runtime record id, repo doctrine target, provider-doctrine route, or code-only verifier/tool hardening. Do not call code hardening a self-improvement record unless `agent-self-improve` actually recorded it.
- Doctrine mutations require an exact open item id, `--resolution resolved`, and evidence refs; failed, non-final, or dry-run records must not mutate durable doctrine.
- Manual `--updated-artifact` doctrine closure requires an existing doctrine artifact containing the exact item id or lesson text.
- Code-review and adversarial-review subagents must be fresh-context reviewers: spawn a new agent without inherited context and do not reuse a previous reviewer thread.
- Review packets must use `agent-self-improve review-add --fresh-context-review`; forked, reused, or inherited implementation-context reviewers are invalid review sources.
- Do not hand-edit `~/self-improving-claude` queue, evidence, records, candidates, or index files.
- Close open items only with a matching structured record, exact `self_improvement_item_id`/resolution, and evidence refs.
- Cross-project lessons are candidates until accepted/refined/rejected by a structured record.
<!-- agent-self-improvement:end -->

<!-- agent-self-improvement-doctrine:begin -->
## Accepted Self-Improvement Doctrine

- 2026-05-09T03:28:00Z [claude] Self-improvement lessons that should steer future Claude behavior must patch durable doctrine with agent-self-improve record --doctrine-target, not only write runtime queue records. (source: self-improvement:user_correction:e4a110a49e2f1aa6)
- 2026-05-09T03:32:17Z [claude] Accepted Claude self-improvement lessons that should steer future behavior must patch durable doctrine with agent-self-improve record --doctrine-target, including the installed self-improving skill when the lesson changes the mechanism. (source: self-improvement:user_correction:6dea286d0afd4e1d)
- 2026-05-09T03:42:57Z [claude] When extracting or replacing an agent self-improvement mechanism for Claude, verify and preserve active write surfaces such as CLAUDE.md and skill updates; do not claim parity from a passive queue or audit log alone. (source: self-improvement:user_correction:596c946fb295c760)
- 2026-05-09T04:00:53Z [claude] For this user-level self-improvement mechanism, Claude runtime records are only queue/audit evidence; successful self-improvement means updating durable behavior files such as CLAUDE.md or self-improving skills when a lesson should change future Claude behavior. (source: self-improvement:user_correction:cd874432deb1d0b6)
- 2026-05-09T04:31:21Z [claude] Claude doctrine mutation commands must validate the exact open item id, resolution, evidence refs, target files, and dry-run mode before writing CLAUDE.md or self-improving skill files; failed or dry-run records must not mutate durable doctrine. (source: self-improvement:user_correction:754118afac0cf2cc)
- 2026-05-09T05:17:42Z [claude] When running code-review or adversarial-review subagents for this user, use a fresh-context reviewer: spawn a new agent without fork_context and do not reuse a previous reviewer thread or a reviewer that inherited the implementation conversation. (source: self-improvement:user_correction:241dfe89750ff7f3)
- 2026-05-09T05:53:42Z [claude] Review packets must use agent-self-improve review-add --fresh-context-review; forked, reused, or inherited implementation-context reviewers are invalid review sources. (source: self-improvement:user_correction:a616009e40211466)
- 2026-05-09T07:07:38Z [claude] Public self-improvement discovery, docs, rule headings, CLI help, and generated item IDs must use application-neutral terminology rather than source-project layer labels. (source: self-improvement:user_correction:ea2911196d18797d)
- 2026-06-12T08:24:52Z [claude] Self-improvement closeouts must name and verify the landing surface before claiming self-improvement happened: runtime record id, repo doctrine target, provider-doctrine route, or code-only verifier/tool hardening; code hardening is not an agent-self-improve record unless the runtime mechanism recorded it. (source: self-improvement:user_correction:f37bdbd8f49ad358)
<!-- agent-self-improvement-doctrine:end -->


<!-- thrash-reporting-install:begin -->
## Thrash Reporting

When modifying or supervising Claude user-level rules, skills, reusable agent behavior, tool/MCP/hook wrappers, Rewind behavior, self-improvement workflows, or installer scripts, load `thrash-reporting`.

Treat thrashing as suspected when repeated rule/skill/tooling edits, workaround loops, missed Rewind anchors, repeated user corrections, weak verification, or scope drift indicate that the agent is changing the environment without a stable root cause.

When a thrash tripwire fires:
1. Stop before additional environment, rule, skill, hook, MCP, installer, or self-improvement mutations.
2. File a blocking ticket with `agent-self-improve enqueue --provider claude --trigger-kind friction --summary "Thrash suspected: <short signal>" --severity blocking --required-response record_only --evidence-ref "friction:thrash:<specific evidence>" --project "<absolute-project-path>"`.
3. Report `Thrash suspected`, the evidence, the ticket id, and the exact mutation being held.
4. Hold for user approval before further environment mutation.

Do not satisfy this requirement with an inline concern only; the ticket is the durable audit trail.
<!-- thrash-reporting-install:end -->

<!-- BEGIN: reply-verbosity (managed by install.sh) -->
# Reply Verbosity (always-on)

# Reply Formatting

## Discovery Details

Load this skill whenever finishing a task and writing a natural-language reply summary, or when the user requests a reply verbosity or technicality change. After triggering, apply the persisted settings and detailed trigger phrases below.

End-of-turn replies are shaped by two independent settings, each persisted per project:

1. **Verbosity** — how much info (4 tiers, default 2)
2. **Technicality** — register / vocabulary (binary: `technical` default, or `plain`)

The two axes combine freely: e.g. Tier 1 + plain → one plain-English sentence; Tier 4 + technical → full technical report.

# Universal rule — `Next:` line is mandatory

**Every reply ends with an explicit `Next:` clause stating what the agent intends to do next. No exceptions.** This applies to:

- Task-completion summaries
- Conversational replies
- Clarifying questions
- Acknowledgements ("thanks" / "ok" / "got it" responses)
- Replies at any verbosity tier (yes, even Tier 1)
- Replies in any technicality mode

If nothing is owed by the agent, say so explicitly:
- `Next: awaiting your direction.`
- `Next: paused — open question above.`
- `Next: blocked on <thing>.`
- `Next: done — nothing pending.`

A reply that ends without a `Next:` clause is a bug. If unsure what to put, default to `Next: awaiting your direction.`

# Verbosity Tiers

Replies stay within the current tier until the user requests a change. Default tier when no state file exists: **2**.

## Tiers

**Tier 1 — TLDR**
One sentence with three parts: what happened, where we are, what's next. No file lists, no diffs, no reasoning.
Example: `Added rate limiter to /api/login; tested locally; next: wire into staging config.`

**Tier 2 — Brief** (default)
3–5 bullets covering key changes and current state, then a final `Next:` line. File names only (no line refs), no diff snippets, no narration of intermediate steps.

**Tier 3 — Standard**
Short paragraph or grouped bullets. File:line refs, notable decisions, what was tried/skipped. End with an explicit `Next:` line. No full diffs.

**Tier 4 — Verbose**
Full report: reasoning, alternatives considered, diff highlights, edge cases, test results, follow-up TODOs. End with an explicit `Next:` line. Closest to default agent behavior.

## Always-on (regardless of tier)

These surface in full even at Tier 1:
- Security warnings
- Destructive / irreversible actions awaiting confirmation
- Hard blockers and real questions for the user
- Errors that stopped the work

## Verbosity switching triggers

Match these substrings (case-insensitive) anywhere in the user message:

- **Less info (step toward Tier 1):** `tldr`, `less detail`, `terser`, `shorter`, `be brief`, `summarize`
- **More info (step toward Tier 4):** `more detail`, `more verbose`, `elaborate`, `expand`, `go deeper`
- **Direct jump:** `tier 1`, `tier 2`, `tier 3`, `tier 4`

On a step trigger: move one tier in that direction (clamped 1–4).
On a direct jump: set that tier exactly.
On any change: prepend one short line to the affected reply, e.g. `[verbosity: tier 2 → tier 1]`. Then write the reply in the new tier.

# Technicality

Independent binary switch. Default: **technical**.

**technical** (default)
Engineer-to-engineer register. Use the precise terminology for the domain — function names, API names, math notation, jargon, library names — without softening or explaining unless the user asks. Assume the user knows the field.

**plain**
The opposite of technical. No jargon. Replace technical terms with everyday words or short analogies. Refer to mechanisms by what they *do*, not what they're called. Names of files/functions/commands can stay (they're identifiers, not jargon) but anything *about* them is described plainly. Goal: a reply a non-engineer in that domain could follow.

## Technicality switching triggers

Match these substrings (case-insensitive) anywhere in the user message:

- **Switch to plain:** `plain language`, `in plain terms`, `less technical`, `non-technical`, `no jargon`, `eli5`, `explain like i'm five`
- **Switch to technical:** `more technical`, `be technical`, `technical mode`, `technical please`

On any change: prepend one short line to the affected reply, e.g. `[technicality: technical → plain]`. Then write the reply in the new register.

# Persistence

Per-project state files at the project root:

- `.reply-verbosity-tier` — single digit `1`–`4`. Default if missing/invalid: `2`.
- `.reply-technicality` — single word `technical` or `plain`. Default if missing/invalid: `technical`.

Read both at the start of every reply. Do not auto-create — only write when the setting actually changes via a trigger. This keeps choices stable across sessions and across the 7+ projects the user works in independently.

# Scope

**Shaped by these settings:** the natural-language summary at the end of a turn.

**Never altered (always full fidelity, technical regardless of mode):**
- Code written to files
- Diffs, patches, command output, error messages, tool results
- In-progress status updates while work is happening
- Anything that goes into a commit message, PR body, or saved document
- File names, function names, command names, paths (identifiers stay exact in `plain` mode too)
<!-- END: reply-verbosity (managed by install.sh) -->
