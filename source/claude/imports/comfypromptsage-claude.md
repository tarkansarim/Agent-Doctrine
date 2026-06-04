# Imported Claude Doctrine Source

- Source path: `<workspace root>/ComfyPromptSage/CLAUDE.md`
- Source SHA256: `ddd2b20a44c08227a3fc1ca85579243869822fdb9c16cec256bf7595295c8058`
- Provider lane: `claude`

## Original Content

# ComfyUI-PromptSage — Project Rules

## What this project is

A ComfyUI custom node pack. Single-node v2 scaffold — a DOM widget rich-text prompt editor with element rows, inline weighted colored spans, hover-revealed weight slider, and drag-to-reorder. No real inference yet; the plan at `<home>/.claude/plans/purrfect-frolicking-lagoon.md` is the source of truth for scope.

**Python source of truth lives here.** Deploy to ComfyUI via `scripts/sync.sh`. Never edit `custom_nodes/ComfyUI-PromptSage/` directly — it's a deployment artifact.

## Memory policy (READ FIRST)

**Do NOT use the `~/.claude/projects/.../memory/` auto-memory system for this project.** It can be wiped between sessions. All durable rules, preferences, and learnings go in THIS file (and checked into git). If something is important enough to remember, it's important enough to be in CLAUDE.md.

When the user corrects me or I hit friction and figure out a fix, the update goes here — not into a `feedback_*.md` memory file. The "Hard rules" section below is the permanent record.

## Hard rules (never break)

### Safety / destructive actions

1. **Never `pip install` autonomously**, even for ComfyUI packages. Ask first; use ComfyUI Manager routes if they exist.
2. **Never edit `~/.claude/CLAUDE.md`** — user-level config is sacred. Project-level only.
3. **Never hard-reload or restart ComfyUI without the user's go-ahead** if they have uncommitted canvas state. A reload while a dialog is unsaved triggers Chrome's "Leave site?" prompt and loses their work. Check `list_tabs` / `get_canvas_state` first.

### Project scope

3a. **This project is SELF-CONTAINED.** Never write or modify code in any other repo as part of PromptSage work — not ComfyCommander, not sortie, not anything else. This node pack ships standalone: it registers its own aiohttp routes via `PromptServer.instance.routes` and its own browser-side JS under `web/comfyui/`. If another repo happens to have plumbing we'd like to reuse, REIMPLEMENT the small bits locally; don't create a cross-repo dependency or a "reference from the other repo." "It's only ~80 lines" is not an excuse to leak into a peer project. If in doubt, ask.

3b. **When adding a new required input to INPUT_TYPES, existing node instances on the canvas will break.** ComfyUI doesn't retrofit new required inputs onto already-placed nodes; their `widgets_values` arrays shift relative to the new widget order. Prefer `"optional"` for added fields if backwards-compat matters. If it must be required, document the upgrade path: right-click the node → "Fix Node (Recreate)" refreshes a stale instance against the new schema (may wipe non-widget state, so mention that).

3c. **`serialize: false` does NOT exclude a widget from `widgets_values`.** LiteGraph indexes `widgets_values` by widget POSITION, not by the serialize flag. Any widget in `node.widgets` — even a "hidden spacer" added for visual layout — eats a slot in the saved array and shifts every subsequent value by one index on reload. Concrete incident: an invisible spacer at `widgets[0]` was silently destroying prompt state on every hard reload for an hour before I caught it (commit d17574b). **Never use phantom widgets for layout.** Visual spacing belongs in CSS on the DOM widget's panel (padding/margin on `.ps-panel` and friends), never in `addWidget()` / `addCustomWidget()` with `serialize: false`.

3d. **"Reload wiped X" is ALWAYS a `widgets_values` / serialization bug — never a UI staleness issue.** If the user reports that content disappears after a hard reload, the first debugging step is `POST /promptsage/debug_widgets` (dumps live widgets with name/type/serialize/value + `node.serialize().widgets_values`) and `POST /promptsage/debug_persist_api` (probes the workflow manager + changeTracker + the current draft localStorage entry). Check widget slot alignment against what's on disk. Do NOT treat reload-wipes as "needs repopulation" — that's how I missed the spacer bug for an hour. Root-cause it every single time.

3e. **Reload survival test sequence.** The CORRECT order when testing persistence after a code change: (1) deploy via `scripts/sync.sh`, (2) hard-reload browser — loads the new code, (3) USER types text into a row through the real UI (not the HTTP API — `/promptsage/set_row` bypasses ComfyUI's change tracker so it's not a valid persistence test), (4) hard-reload AGAIN and run `/promptsage/sonar`. If I'm tempted to use the API to inject test text: stop. The API path has its own separate persistence questions; never conflate it with "does user input survive." Ask the user to type, then validate.

### Verification / honesty

4. **ALWAYS SONAR FIRST, BEFORE creating or modifying ANYTHING on the graph.** Before `add_node`, `remove_node`, `connect`, `update_input`, load_workflow, or any other canvas-mutating command: read `/commander/canvas_summary` (the textual sonar — primary) to see what's already there. Never assume the canvas is empty. Never drop a test node onto an unknown graph. Never wire a connection without checking the existing topology first. Assuming the graph is blank is how the user's work gets corrupted.
5. **Always run a sonar after any disruptive action** too — hard reload, ComfyUI reboot, adding/removing nodes, workflow load, dialog dismissal. Textual sonar first: `/promptsage/sonar` (richest — includes PromptSage state, pairwise overlap detection across ALL nodes, heartbeat staleness, X11 workspace mismatch) or `/commander/canvas_summary` (plain canvas summary). Screenshot sonar is the *fallback*, not the primary — use it only when a suspicion isn't answered by text. Never retry a second UI operation without first sonar-ing to understand what actually happened.

    **Textual sonar is your primary sense of the canvas. Use it frequently.** Before every user-facing claim about what's on the graph, run it. Between every mutation and the next, run it. "I think X is on the canvas" is never an answer — `/promptsage/sonar` is. You CANNOT assume. The user experiences the canvas visually; you experience it textually — keeping those in sync is the entire job of the sonar system.

    **Screenshots are for the things textual can't yet describe.** Pixel-perfect visual bugs, a style regression, an image preview, something you haven't yet taught the textual sonar to probe. When a screenshot reveals something textual missed, the fix isn't "screenshot more" — it's "patch the textual sonar so next time it catches it." Three classes already patched this session: pairwise node overlap (all pairs, not just PS-adjacent), blocking Chrome modals (heartbeat staleness), X11 workspace mismatch (browser window on different desktop than active).

    **After any multi-node canvas change, auto-resolve overlaps.** `POST /promptsage/resolve_overlaps` does AABB detection + minimum-translation separation with a 20px margin, iterating until clean (max 40 passes). Call it after `batch` that creates nodes, or any sequence of `set_position`. `{"dry_run": true}` to preview the moves without applying. This eliminates the manual compute/eyeball/adjust loop — don't do that by hand anymore.

    **Off-viewport nodes are also reported.** `/promptsage/sonar` now uses the browser's canvas viewport dimensions (from the bridge) + the canvas transform (scale + offset) to flag nodes that are entirely outside the visible viewport. If the warning fires, fix it with `POST /promptsage/fit_view` (`{"node_ids": [...]}` for a specific subset, or empty body for all nodes). Don't leave nodes floating at off-screen coordinates hoping the user will notice — they won't.

    **The sonar system is self-improving. Fix gaps in-session, not "later."** Textual sonar is primary (fast, structured, greppable). Visual sonar is a secondary verification that *will eventually fade away* as textual matures. After any multi-node change, pair them: run textual THEN take a screenshot and compare. If the screenshot reveals something textual missed — overlapping nodes, off-canvas placement, a blocking dialog, wrong visual state of a widget — **that gap is a textual-sonar-improvement bug**. **Patch it in the same session** — log-and-defer is banned as a final state. Either implement the detector now, or add it as a mandatory todo in the current commit set. Both known gaps from this conversation's history (layout overlaps; blocking Chrome modals) now have textual detectors because they were patched in-session; that's the shape of the rule.

5a. **Compute, don't eyeball.** Any claim of the form "X doesn't overlap Y" / "N is less than M" / "these IDs are unique" / "the list is sorted" is a fact with a formula. Compute it in Python/bash, don't inspect a screenshot. Eyes are for aesthetic and UX judgments (does this feel right?), not geometric or numeric ones. Concrete failure mode that earned this rule: "intersection probing is faulty" — I looked at a screenshot, said "looks fine," missed a 40px AABB overlap that took 5 lines of Python to find.
6. **Never OCR error dialogs via screenshot zoom.** Dismiss the dialog first (`xdotool key Escape`), then get the real error from DevTools console (F12) or a JSON diff. The dialog's tiny text is not the log.
7. **Flag friction immediately.** Wrong port, silent failure, no confirmation, config drift — surface it and fix. Don't wait to be asked.
8. **Never claim I've verified an interactive UI feature I couldn't actually drive.** I can prove files served, module symbols present, canvas state correct. I cannot simulate text selection, hover, drag. For those, ask the user for a one-step confirmation.
9. **Never infer node behavior from its name.** Query `/object_info/<NodeType>` or read the source.

### Mechanics

10. **No blocking wait loops in a single Bash call.** No `while true; do sleep N; done`. Use `run_in_background=True`, or `until <check>; do sleep 2; done` (which the harness allows as a short poll).
11. **Never `xdotool windowactivate` during testing.** It raises the Chrome window and steals the user's focus. `import -window <wid>` captures without raising — use that alone. Only raise the window if the user explicitly allows it for a specific action.

    **Never use ImageMagick `-crop` or `-resize` either.** They reliably fail on these full-resolution captures with "cache resources exhausted" / "unable to read X window image", leaving an empty output and a broken pipeline. Take the full-window screenshot and show it as-is — the Read tool displays full 4K PNGs fine. If the user wants detail on a specific area, ask for coordinates or ask them to share their own zoomed screenshot. Do not try to "zoom in" via ImageMagick post-processing.

    **Before any screenshot, switch to the target window's workspace first.** Multi-workspace X11 setups keep off-workspace windows' pixmaps but the rendering can be stale — `import -window <wid>` captures whatever pixels are cached, which may not reflect the current state. Use `xdotool get_desktop_for_window <wid>` to find the window's workspace and `xdotool set_desktop N` to switch (this is NOT `windowactivate` — it switches the viewport only, doesn't raise any specific window or steal keyboard focus). Example pattern:
    ```bash
    WID=75497495
    TARGET=$(xdotool get_desktop_for_window $WID)
    [ "$(xdotool get_desktop)" != "$TARGET" ] && xdotool set_desktop $TARGET && sleep 0.3
    import -window $WID <temp dir>/sonar.png
    ```
    Without this, you'll keep misreading screenshots that look plausibly right but are minutes or versions behind reality.
12. **Always probe ports for the running ComfyUI instance.** The ComfyCommander `paths.yaml` drifts — observed drift: config says ComfyUI_V81 port 8189, reality is ComfyUI_V85 port 8188. Run the probe loop before trusting config.
13. **Correct endpoints:**
    - Restart ComfyUI: `GET /api/manager/reboot` (NOT `/manager/reboot` — that returns 405).
    - "Hard refresh" in user speak = `/commander/hard_reload_browser` (calls `window.location.reload()` with cache-bust). Same thing. Don't draw a distinction.

### Self-improvement

14. **When friction produces a fix, update THIS file immediately — before the next action.** Not at end of task. Not "I'll document later." Stop, edit CLAUDE.md, then continue. If I repeat a mistake across three sessions, promote the fix to a hard rule here.

15. **The commit of a fix is NOT the end of the task — the promotion to a hard rule here (or a skill file) IS.** If I commit a fix without also updating CLAUDE.md / skill docs in the SAME working session (ideally the same commit, or at worst a follow-up commit made autonomously before handing back to the user), rule 14 was violated. The user should NEVER have to prompt "now self improve" — that prompt is a second-order correction I should be logging too, and each time it happens the rule below this one gets an additional line. Do not ask "should I promote this to a rule?" — just do it, announce it, move on. Recurring failure mode: I log the correction to `~/self-improving-claude/corrections.md`, sprinkle a code comment, then stop — instead of elevating the lesson to the permanent project-rules layer where future-me will actually see it. Corrections.md is a scratchpad, CLAUDE.md is the law.

16. **Revert every failed attempt before trying something different.** If an attempted fix doesn't work, back it out completely (including temporary instrumentation like console.log / setSize overrides) BEFORE writing the next attempt. Stacking failed attempts on top of each other makes the diff impossible to reason about, leaves debug noise in production code, and hides which change actually fixed it when something finally works. Concrete case that earned this rule: a failed `requestAnimationFrame + _psSizeRestored` flag attempt at preserving node size on Run left instrumentation code in place even after it was proven not to fix the bug — user had to explicitly say "Undo that shit before trying something new." A failed attempt's correct terminus is `git checkout <file>` or an Edit that reverts to the pre-attempt state, not "leave it and layer on".

17. **Before guessing at an unfamiliar ComfyUI / LiteGraph behavior, grep the installed custom_nodes for precedent.** `<Documents root>/AI/ComfyUI_V85/ComfyUI/custom_nodes/` contains dozens of node packs that have already solved the same problems — KJNodes, VHS, Easy-Use, rgthree, and others. For DOM widgets, addWidget quirks, node lifecycle hooks, canvas persistence, execution hooks, etc., a 30-second `grep -rn <suspected-API> custom_nodes/` is worth more than 30 minutes of guessing. Concrete case: the "node resizes back on Run" bug was a one-line fix (use `getMinHeight`, not `getHeight`, in addDOMWidget options) that KJNodes had been using correctly in three separate files all along. I didn't look, wasted two attempts guessing, user had to say "why don't you just check a different js node from a different repo?" The habit applies to any "how does ComfyUI do X" question — grep first, guess later.

    **Caveat: precedent from other packs is a hypothesis, not a cure.** The KJNodes `getMinHeight` pattern was a reasonable lead but not the actual fix for our "size resets on Run" bug — the real culprit was our own `recomputeNodeSize()` inside `lib/dom_widget.js` which was firing via `stateWidget.callback` during ComfyUI's `graphToPrompt` serialization. Finding the same API used elsewhere says "this is how you do X," not "this is your bug." Still must reproduce + verify (rule 18).

18. **Reproduce bugs programmatically BEFORE attempting fixes.** A user report ("X happens when I Y") is a symptom claim, not a verified baseline. Before any fix, build a reproduce that hits the same symptom from the terminal — for PromptSage, usually: call `/commander/set_position` with a non-default size, capture via `/promptsage/list_nodes`, fire `/commander/queue`, capture size again, assert the change. Then apply the fix and re-run the same test. If the test is hard to build (no endpoints for the action), BUILD the endpoints first — `/promptsage/_diag_log` was added mid-session to relay setSize writes from the browser to a server-side buffer so I could read the stack trace without DevTools access. Two "fixes" were shipped this session for a "node resets on Run" bug without a reproduce, both bypassed the real root cause; the third attempt, made after a proper reproduce, found that OUR OWN `recomputeNodeSize()` in `lib/dom_widget.js` was clobbering height during `graphToPrompt`. Reproduce FIRST, fix second. Screenshot + user-report isn't a baseline — a failing-then-passing test IS.

## Development loop

1. Edit in project root.
2. `bash scripts/sync.sh` — deploys to `ComfyUI_V85/ComfyUI/custom_nodes/ComfyUI-PromptSage/`.
3. Python changes → `GET /api/manager/reboot`. JS-only → `POST /commander/hard_reload_browser` + `POST /commander/reset_primary_client`.
4. **Sonar** the result before reporting anything.

## Autonomous UI testing

- **Harness source:** `<workspace root>/ComfyComannder/`
- **Harness config (drifts — verify reality first):** `.../ComfyComannder/config/paths.yaml`
- **Project skills:**
  - [`.claude/skills/harness-api/SKILL.md`](.claude/skills/harness-api/SKILL.md) — condensed curl cheat sheet
  - [`.claude/skills/promptsage-node-usage/SKILL.md`](.claude/skills/promptsage-node-usage/SKILL.md) — how to use the PromptSage node itself
  - [`.claude/skills/promptsage-ui-test/SKILL.md`](.claude/skills/promptsage-ui-test/SKILL.md) — the autonomous test loop

## User preferences (distilled)

- Wants grounded claims, not plausible-sounding speculation. Will push back if I assert something without evidence.
- Wants UX validated in the real ComfyUI graph before committing to architecture.
- Wants me to autonomously verify my own changes before handing off. "Never ask the user 'did it work?'" — find out myself, or say explicitly that I can't.
- Prefers registry-style plumbing for future extension points (model presets, modifier types) so new additions are drop-in files, not restructures.
- When iterating on a PromptSage prompt during an image-gen session, ALSO queue a run after every row change (`POST /commander/queue`) so the user gets a fresh image without having to click Run manually. Stop doing this only if they tell me to.
