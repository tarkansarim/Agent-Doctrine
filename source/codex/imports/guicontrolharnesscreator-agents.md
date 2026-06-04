# Imported Codex Doctrine Source

- Source path: `<workspace root>/GuiControlHarnessCreator/AGENTS.md`
- Source SHA256: `c63ca8a9e4c918404e2271ca6011fa45e88bfe5822c88738efb12dae0dd22b5d`
- Provider lane: `codex`

## Original Content

# AGENTS Instructions

Apply the root `CLAUDE.md` in full. This `AGENTS.md` adds repo-level operating rules that must not be skipped during Harness Architect work.

## Repo Driving Skill

Before doing live Harness Architect operations in this repo, read `skills/repo-driving-and-mcp-ops/SKILL.md`.

Use it for:
- startup/restart trust checks
- MCP-first harness control and cleanup
- safe reload or full-restart decisions
- backend/rendered/artifact truth verification before continuing a run

## Instruction Precedence For This Repo

The root `CLAUDE.md` contains general meta-harness doctrine. This repo has one important repo-specific override:

1. `Direct Bridge First` in root `CLAUDE.md` does **not** authorize bypassing Harness Architect runtime control.
   - Direct bridge calls remain valid for target-software probing **inside** a proven target harness.
   - They do **not** replace the harness MCP/tool surface for session control, cleanup, nudges, target launch/stop, or reload/restart flow.
2. For this repo, Harness runtime control is MCP-first.
   - If there is any conflict between root `CLAUDE.md` and the rules below for live harness control, cleanup, or reload safety, follow this `AGENTS.md`.

## Harness Fix Hygiene

When you detect a Harness Architect issue and are starting a fix cycle, do this in order before asking the user to reload VS Code for the fix to take effect:

1. Stop the active Harness workers first.
   - If the current run is already known-bad, contaminated, or headed for a restart-from-scratch, stop live `L1` and `L2` immediately so they stop spending tokens while you debug or prepare cleanup.
   - Use the MCP/tool surface for this stop path.
   - If stopping `L2` auto-resumes `L1` for wrap-up, stop that resumed `L1` too.
   - If stopping `L1` while it is inside `harness_prepare_layer2`, immediately re-check all layers before clearing transcripts; a late `L2` handoff can land after the `L1` stop returns.
   - If a restored `L1` stops with a structural escalation and asks Layer 0 for the missing failure signal, answer that same restored `L1` while it is still active. Do not wait for it to exit and then auto-spawn a generic bootstrap `L1`; that can drop checkpoint-specific phase contracts such as readiness recovery lanes.
   - Before using `harness_send_layer_message` as a correction to a restored `L1`, verify backend truth still shows that exact restored `L1` worker active. Send the correction with `expected_worker_id` set to that worker id and `allow_auto_spawn:false`. If it is no longer active, do not send the correction; restore the intended checkpoint again instead.
   - If the correction is already known before restoring a checkpoint, inject it atomically during `harness_fork` with `supervisor_directive` instead of restoring first and sending a separate `harness_send_layer_message`. A post-restore send can queue behind the current Layer 1 turn and arrive after `harness_prepare_layer2`, which makes the reprobe untrustworthy.
   - Treat `harness_fork supervisor_directive` as the complete current Layer 0 authority for the restored reprobe, not as a delta patch. Include any still-required phase-scope clauses, bounded startup/readiness recovery lane, stop conditions, and artifact proof obligations in that directive. If the directive only contains the new correction, the restored `L1` may drop older but still-required contracts or be rejected for inventing recovery authority.
   - When `harness_fork` restores an execution/L2 checkpoint and reroutes through the paired `L1` checkpoint, the backend `layers[1].task` may show only a generic reprobe summary. Do not treat that summary alone as proof the full `supervisor_directive` was dropped. Check the L1 layer log/rendered L0 event for the inbound routed directive before deciding whether to contain or trust the retry.
   - If a restored `L1` must be nudged after a `harness_prepare_layer2` validator rejection, that nudge is also replacement authority for the next brief. Include the full current directive again, not just the validator correction, or the retried `L2` brief can lose phase contracts such as one-shot readiness recovery and evidence pre-create gates.
   - If runtime state is ambiguous, verify which specific workers are active before stopping anything.
   - If you need evidence from the failed run, capture the minimum required evidence first, then stop the workers immediately.
2. Clear the Harness chats.
   - Do not clear chats until backend and rendered truth both show no active `L1` or `L2` worker.
   - Clear `L0`, `L1`, and `L2` transcript history for the affected project before the next retest.
   - After clearing/stopping a layer, do not use `harness_resume_layer` unless backend truth still shows that layer's `task` or `bootstrapTask` is exactly the intended brief. If the task was cleared or is ambiguous, restore from the intended checkpoint with `harness_fork` instead.
3. Delete artifacts created by the contaminated run.
   - Remove target files and runtime artifacts created by `L1` or `L2` for the active run before the next bootstrap.
   - This includes target files under `targets/<software>/`, installed startup bridge files, and project-scoped Harness runtime artifacts for that run when they would contaminate the next verification pass.
4. Only after steps 1-3 are complete may you patch code, reinstall the extension, and ask the user to reload.

If you need evidence from the failed run, inspect or capture that evidence first, then perform the cleanup immediately before proceeding.

## Harness Operations Surface

Do not use low-level Harness control paths for normal project operations.

1. Use the MCP/tool surface first for routine Harness actions.
   - This includes reset, session start, nudges / layer messages, target launch, target stop, and similar day-to-day control actions.
   - Treat the MCP/tool path as the operational surface that must itself stay honest and exercised.
2. Do not default to direct control-client or backend-helper routes for convenience.
   - Do not use lower-level helpers such as direct control-command clients, ad hoc backend scripts, or other bypass paths just because they are faster to script.
   - "Same backend handler" is not enough reason to bypass the MCP/tool surface.
3. Only use a lower-level route when the MCP/tool path itself is the bug under investigation.
   - State that explicitly before using the lower-level route.
   - If the MCP/tool path is not the thing being debugged, stay on the MCP/tool surface.
4. If a bypass was used during an invalid run, do not continue building on top of it.
   - Clean up and restart from the proper MCP/tool path before treating the run as trustworthy.
5. A bridge sidecar is not target ownership.
   - Do not treat a live bridge process as proof that the target app PID is live or harness-owned.
   - If `harness_launch_target` reports a pre-existing external target app process, do not kill it manually from shell. Use tracked MCP cleanup for tracked state, or ask the user to close the external app before retrying.
6. Do not let a wedged control call burn tokens indefinitely.
   - If the control runtime is already suspected wedged, call the MCP/control path with a hard caller timeout.
   - If that bounded call hangs or times out, state that the MCP/control path is the bug and contain only exact tracked Harness-owned PIDs.

## Exact MCP Surface For This Repo

For routine live Harness Architect work, default to these tools first:

- `harness_session_start`
- `harness_send_layer_message`
- `harness_stop_layer`
- `harness_chat_clear`
- `harness_reset_project`
- `harness_launch_target`
- `harness_stop_target`
- `harness_worker_runtime_get`
- `harness_worker_runtime_set`

For safe non-GUI reloads, prefer:

- `supervisor_reload_window`

In the current local Sortie install, `supervisor_reload_window` is the safe internal bridge/API reload route, not a workflow-MCP tool exposed by `run-workflow-server --tools-filter`. Use the installed bridge client or another proven internal bridge command for this route; do not treat a missing workflow-MCP reload tool as permission to use GUI automation.

Do not substitute ad hoc backend helpers, direct control clients, shell cleanup, or manual file deletion just because they seem faster.

## Harness Worker Runtime Switching

Use the Harness MCP runtime tools to switch worker providers. Do not hand-edit `.sortie/harness/worker-runtime.json` during normal operation.

1. Before switching providers, verify backend and rendered truth show no active `L1` or `L2` worker.
   - If a worker is active and must not continue, stop it through `harness_stop_layer` first.
2. Use `harness_worker_runtime_get` to inspect the current durable default and effective `L1`/`L2` selections.
3. Use `harness_worker_runtime_set` to switch future workers.
   - For Codex: set `provider:"codex"`, `model:"gpt-5.4"`, and `reasoning_effort:"medium"` unless the user explicitly asks otherwise.
   - For Claude: set `provider:"claude"` and the intended Claude model.
4. Runtime switches are durable project settings and do not expire automatically.
5. Runtime switches affect future worker spawns only. Existing workers keep the provider/model they were launched with until stopped and respawned.

## Startup And Restart Trust Checks

After the user says VS Code was reloaded, restarted, or reopened, do not assume the patched build is live.

1. Check `.sortie/autonomy/state/bridge.json`.
   - Record the current `extensionProcessPid` and `authorityEstablishedAt`.
2. If a restart was expected, verify that a **new** authority PID actually appeared.
   - If the PID did not change, treat the host as the old authority until proven otherwise.
3. Check host health before continuing a live run.
   - Sample CPU / RSS for the authority PID.
   - If the host is still pathological, do not continue bootstrap, cleanup-sensitive retests, or phase-boundary work.
4. Re-check both backend truth and rendered panel truth before trusting the window.
5. Read backend truth from the canonical runtime schema, not from ad hoc guesses.
   - `.sortie/harness/state.json` stores live layer bindings under `layers[0]`, `layers[1]`, and `layers[2]`.
   - Do not infer backend state from nonexistent top-level fields such as `layer1` or `layer2`.
   - When you need a quick check, use `skills/repo-driving-and-mcp-ops/scripts/check-harness-backend-truth.js`.

## Phase Artifact Truth

For accepted phase boundaries and phase transitions, backend truth plus rendered panel truth is necessary but not sufficient.

Also verify the on-disk phase artifacts:

- `plans/current.md`
- `targets/<software>/CLAUDE.md`

If those artifacts disagree with backend truth or rendered panel truth, treat the boundary as not trustworthy.

## Layer 1 Rewind Regression Stack

After any Layer 1 self-improvement / Layer 1 pack edit that leads to a rewind, do not validate only the newly fixed failure.

1. Before trusting the next Layer 2 brief or reprobe result, cross-check the brief against the stack of prior Layer 1 instruction failures recorded in `HARNESS_ISSUES.md` and the current Layer 1 pack.
2. The check must include scope preservation, full-current-directive preservation, readiness/recovery lane preservation, MCP lifecycle requirements, evidence pre-create/write/self-check gates, context-budget limits, and exact Layer 2 brief section format.
3. If the new Layer 1 instruction fixes the latest issue but drops or weakens an older required behavior, treat the reprobe as untrusted.
4. If target work has not started, stop before target launch/probing and fix the Layer 1 instruction path first. If target work already started under the regressed brief, contain through MCP and restart from a clean checkpoint after the instruction path is fixed.


## Cleanup Doctrine For This Repo

When the user wants a fresh start, cleanup, reset, or decontamination:

1. Prefer `harness_reset_project` as the authoritative cleanup tool.
2. If targeted cleanup is needed before reset:
   - stop active layers with `harness_stop_layer`
   - clear transcripts with `harness_chat_clear`
   - then use `harness_reset_project`
3. Do not manually delete target files, bridge residue, or runtime artifacts unless the MCP/tool cleanup path itself is the bug under investigation.
4. If the current host is still on an old build or untrusted after restart, do not wipe and rerun on that host.
   - load the correct host first
   - then clean via MCP
   - then rerun from a clean state
5. Treat stale `plans/current.md` future-phase details as cleanup contamination.
   - After a fresh reset, `plans/current.md` must return to a clean Bootstrap baseline.
   - It must not preserve prior-run bridge paths, PIDs, target versions, friction IDs, decisions, derivations, or completed-phase evidence as unchecked future work.
   - If those details survive reset, the MCP cleanup path itself is the bug under investigation.

## Where To Encode New Repo Rules

When you learn a durable repo-driving rule for this project:

1. Put the short hard rule in `AGENTS.md` if it changes default operating behavior.
2. Put the repeatable step-by-step procedure in `skills/repo-driving-and-mcp-ops/SKILL.md`.
3. Do not rely on chat memory or context summaries for repo-driving rituals.

## User "Do Not Stop" Directive

When the user says not to stop, keep polling, continue autonomously, or equivalent, treat that as a persistent repo-level directive until the user explicitly says to pause, stop, or change scope.

1. Do not pause at same-phase acceptance, clean slice completion, idle-worker gaps, or because a natural handoff point was reached.
2. Do not send wrap-up, handoff, or completion-style responses while that directive is active.
   - Use short progress updates in commentary only while work continues.
3. Continue with the next bounded action yourself.
   - If a live run finishes, immediately choose the next repo-grounded bounded slice instead of waiting for permission.
4. Only stop autonomously for one of these reasons:
   - the user explicitly tells you to stop or pause
   - the exact requested terminal milestone has been reached
   - a real blocker requires user action that cannot be performed from the repo or local machine
5. If a user action is required, state the blocker briefly, wait only for that action, and then resume automatically under the same persistent directive.

## VS Code Reload Safety

Do not drive VS Code reloads through GUI automation.

1. Never use `xdotool`, synthetic keystrokes, focus stealing, or command-palette typing to reload VS Code.
   - This includes window activation, `F1`, typing `Developer: Reload Window`, or any similar GUI-injection path.
2. Prefer the internal Sortie bridge/API reload path first.
   - If a programmatic internal reload path exists, use that instead of GUI interaction.
3. If the internal reload path is unavailable or untrusted, ask the user to reload manually.
   - Do not improvise with desktop automation.
4. Treat focus disruption, accidental desktop interaction, or session interference as a real bug.
   - Stop using the offending method immediately and switch to a safe reload path.

## Sortie Rollout Discipline

When this repo depends on a local `sortie` code change, do not treat a source-only compile as a real rollout.

0. Before editing or building `sortie`, verify the current Codex/session sandbox can actually write it:
   - `test -w <workspace root>/sortie`
   - `test -w <workspace root>/sortie/out`
   - If either check fails, this is a session writable-root problem, not Unix ownership or chmod. Do not suggest `chown`, `chmod`, moving `sortie` into this repo, or copying original Sortie source into `GuiControlHarnessCreator`.
   - The clean fix is to restart/launch Codex with `<workspace root>/sortie` as the workspace or as an added writable root. A temporary `<temp dir>/*.patch` handoff is acceptable only as a last-resort bridge when the user explicitly applies it from a normal terminal.
   - User's preferred longer-term consolidation direction is the opposite of copying `sortie` into this repo: move/integrate the `GuiControlHarnessCreator` project under `sortie` so the Harness Architect has one primary source/workspace root. Do this only as an intentional migration with path updates and verification, not as an ad hoc duplicate copy.
1. After any `sortie` code edit that is meant to affect the live VS Code extension used by this repo, install the extension with:
   - `cd <workspace root>/sortie && bash install-extension.sh`
2. Do not use `npm run compile` alone as the rollout step for live Harness work.
   - `npm run compile` only syncs `out/` and is not sufficient as the authoritative install path.
3. If TypeScript source files were deleted or restored from an older commit, verify generated-output residue before packaging.
   - `out/` and the installed extension must not contain stale `.js` files for deleted source modules.
   - If stale generated files survive, fix the build/installer cleanup first; do not reload VS Code or run Harness on a contaminated install.
4. Only after `install-extension.sh` succeeds may you ask for or perform a VS Code reload/restart to pick up the new host build.
5. After reload/restart, still perform the normal trust checks in this file.
   - A successful install does not prove the running window actually loaded the new authority host.

## Resume After Context Reset

Do not trust remembered intent after chat context reset/summary, restart, or resume.

1. Reread `AGENTS.md` before taking action after any context-reset/resume boundary.
   - Treat this as mandatory, even if the prior session seemed recent or obvious.
2. Re-anchor on written repo rules, not conversational memory.
   - If a workflow commitment matters, encode it here first instead of relying on "from now on" chat promises.
3. When resuming active Harness work, reread the current issue ledger too.
   - Check `HARNESS_ISSUES.md` before continuing so open bugs and prerequisites do not get forgotten across context resets.

## Failed Fix Rollback Discipline

If a proposed fix is deemed not working, do not leave that speculative edit stack in place while trying a different fix.

1. Revert the failed fix path first.
   - If the attempted fix did not solve the problem, roll it back before starting a materially different approach.
   - Do not accumulate dead speculative edits, partial workaround layers, or abandoned scaffolding.
2. Keep only changes that still have an independently verified purpose.
   - If a prior edit is retained, explicitly justify why it remains correct even though the larger attempt failed.
   - Otherwise remove it.
3. Treat "new diagnosis, new fix path" as a rollback boundary.
   - Once the root-cause theory changes, clean out the prior failed theory's code before proceeding.
4. Verify after cleanup and after the new fix.
   - Confirm the rollback itself did not leave residue.
   - Then verify the replacement fix from evidence, not belief.

## File Tool Overrun Handling

Treat Harness file-tool duration warnings as soft progress signals, not hard stop conditions.

1. Do not stop a worker only because `Edit` or `Write` exceeded the nominal duration window.
2. Before stopping a suspected wedged file edit/write, check all available progress evidence:
   - latest layer transcript entries
   - target artifact mtime/size
   - whether the tool returned and the worker resumed read-back/self-check work
3. Stop through MCP only when the evidence shows true no-progress behavior:
   - no tool result
   - no transcript progress beyond heartbeats
   - no relevant artifact mtime/size change after a stronger grace window
4. If mtime advances or the tool completes and the worker resumes verification, treat that as progress even if an alignment flag was raised.

## Layer 1 Prepare-Layer2 Overrun Handling

Treat `harness_prepare_layer2` heartbeats as ambiguous until you prove whether Layer 1 is still streaming the proposal input.

1. Do not stop Layer 1 only because `harness_prepare_layer2` exceeded its nominal duration window.
2. Before stopping a suspected wedged prepare call, check whether the worker stream is still emitting `input_json_delta` / tool-use argument chunks for the Layer 2 brief.
3. If the tool input is still streaming, treat that as progress and wait unless the content is visibly drifting from the active Layer 0 directive.
4. Stop through MCP only when evidence shows true no-progress behavior:
   - no new layer transcript entries beyond repeated heartbeats
   - no worker stream/tool-input deltas
   - no Layer 2 binding spawned
   - no MCP tool result after a stronger grace window
5. If a prepare call is stopped and the later evidence shows it was still streaming a valid brief, treat that as a false containment and restart from the accepted checkpoint rather than debugging the Layer 1 brief as failed.

## Harness Verification Standard

Do not claim a Harness Architect fix works from runtime state alone.

After any Harness fix or retest, verify both layers of truth before calling it fixed:

1. Backend truth.
   - Check the relevant Harness runtime state, transcript files, and exact worker/target PIDs.
   - Confirm the intended control/action actually happened and no forbidden side effect happened.
   - Read runtime bindings from `.sortie/harness/state.json -> layers[0|1|2]`, not from nonexistent top-level per-layer fields.
2. Rendered panel truth.
   - Check what the running Harness webview actually rendered, not just what the extension intended to send.
   - Use the live Harness render-capture path when available:
     - `node <workspace root>/sortie<temp dir>/capture-live-harness-render-state.js <workspace root>/GuiControlHarnessCreator`
   - Compare the returned rendered state against the expected panel result for the scenario.

Examples of required rendered-state checks:
- after `clear`, the visible `L0/L1/L2` entry counts must be `0`
- after a safe bootstrap, `L1` may be active but `L2` must still be idle and no target app PID may be present
- after the auto-handoff starts, `L2` may become active without any approval UI or approval-status text appearing in the panel
- after `stop`, the panel must no longer show the worker as active if its PID is gone

If backend truth and rendered panel truth disagree, treat the fix as not verified.
