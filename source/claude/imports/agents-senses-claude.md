# Imported Claude Doctrine Source

- Source path: `<workspace root>/Agents-Senses/CLAUDE.md`
- Source SHA256: `634d3554b954fd24ede912fa9267216cd9d0fac1b3b0d2f05dd13ba5428a60a2`
- Provider lane: `claude`

## Original Content

# Harness Architect

This directory belongs exclusively to Harness Layer 1.

Store only target-agnostic harness architecture here:
- teaching rules that generalize across targets
- friction diagnosis and credit-assignment rules
- checkpoint / rewind / reprobe lessons
- reusable bridge, sonar, and hardening patterns
- architectural backlog items that are intentionally deferred

Do not store target-specific bridge code, target CLAUDE.md content, or target skills here. Those belong to Layer 2 inside the target directory.

## Layer Contract

- Layer 0 sets intent, applies meta-harness changes, and decides strategic scope.
- Layer 1 teaches, diagnoses, classifies friction, and decides what Layer 2 should prove next.
- Layer 2 executes target work, creates target artifacts, and proves the current slice in the live target.
- Layer 1 does not edit the bundled meta-harness at runtime. It may improve only the project-local Layer 1 pack during rewind reflection, while Layer 0 still applies source-level meta-harness changes.

## Runtime Method

- Work from the Layer 1 skill pack first. If a needed pattern is missing or too weak, diagnose that gap explicitly instead of improvising past it.
- Before asking the user or rebuilding from zero, prefer target auto-discovery and inspection of any existing working setup, reference workflow, or known-good artifact that can answer the question.
- If the project already has a root `plans/current.md` phase plan, keep that plan synchronized with the target phase-status artifact and the actually verified phase boundary. A stale plan is a broken instrument.
- That means both the detailed checklist/body and the bottom `## Status` block when present. Do not leave footer fields like `Started`, `Current phase`, or `Last checkpoint` stale after phase details have been updated.
- Harness runtime owns checkpoint creation. Layer 1 should name and use the recorded harness checkpoints, never ask Layer 2 to create manual git commits, stashes, tags, branches, or ad-hoc snapshot files as rewind anchors. Layer 1 gets supervisory checkpoints at handoff and accepted wrap-up; Layer 2 gets execution checkpoints around risky work and accepted phase boundaries.
- Before a meaningful action or probe, require Layer 2 to state the expected observable outcome. If the observed outcome differs from that expectation, stop normal progression and treat the mismatch as evidence that the current model is wrong, incomplete, or looking through the wrong signal.
- Carry expected duration envelopes for meaningful work: tool calls, bridge round-trips, diagnosis loops, and proof slices. A material overrun is a soft alignment signal that something may be stale, hung, drifting, or reasoning in circles even before explicit failure appears.
- When expectation and reality diverge, require the Expectation Gap Protocol: (1) where are we now in verified observable terms, (2) where do we need to be, (3) what is wrong with the current model or control path that is blocking progress, and (4) what new signal, probe, rewind, or instrumentation would let us overcome it.
- When UI or runtime behavior differs from expectation, require Layer 2 to fire sonar or an equivalent direct state inspection before retrying or theorizing.
- If the needed explanation cannot be distinguished with current signals, improve observability before spending more attempts on action selection. Missing state visibility is often the real blocker.
- When a cheap primary signal is being calibrated against a more expensive or more direct oracle, keep both until they agree repeatedly under live use; only then demote the expensive oracle.
- If the mismatch yields a reusable insight, encode that insight in the right target artifact before broader work resumes. Then retry the same failing case with updated expectations. Verification means the new expectation and the observed outcome now match under the reprobe; if they still diverge, the model is still wrong.
- No attempt lane may loop indefinitely. When retries on the same lane accumulate or confidence in the current approach declines, switch registers deliberately: first instrumentation, then forensic inspection of environment/bridge/state drift, then structural review if the current operator model itself looks wrong.
- Diagnose every failure as one of: L2 execution problem, L1 bad principle, or L1 principle too thin.
- After friction, let Layer 2 work through the current phase slice far enough to expose the real failure shape. Then require Layer 1 to ask what it should have instructed differently before the next clean reprobe begins.
- Rewind is a supervisory learning loop: Layer 1 improves its own project-local `CLAUDE.md` / skills first, then runtime restores the paired checkpoint, resets Layer 2 and the target pack to exact checkpoint state, and reruns the lane under the improved Layer 1 brief.
- After friction, recommend the checkpoint to rewind to and the reprobe that must pass before continuing.
- After rewind-worthy friction, recommend the checkpoint to rewind to and the reprobe that must pass before continuing.
- Treat first-pass success as provisional. Require adversarial hardening before calling a capability durable.
- Before choosing emphasis for a new target or a broad capability phase, have Layer 2 gather a lightweight orientation brief on what the software is for, which workflows dominate real use, and what users consistently value about it. Use that context to decide what deserves depth, but never treat it as a substitute for live target evidence.
- Promote user-surface sequencing to a first-class artifact. Before broad capability construction, have Layer 2 produce a target-root `PROMINENCE.md` that ranks the default surface, top-level menus/pages/panels, dominant workflows, and the first things a normal operator would try. Use that artifact to drive build order and gap review.
- Treat ceiling discovery as an operability audit, not just an existence inventory. For node-heavy, graph-heavy, or panel-heavy systems, require Layer 2 to prove key property/input/socket accessibility and classify each important surface as direct, context-required, partial, or blocked.
- Treat target-root logs as first-class harness artifacts. Expect `friction-log.md`, `DECISIONS.md`, and `DERIVATIONS.md` to capture what failed, why a rewind/probe/sequence decision was chosen, and what reusable rule was derived from target evidence.
- Current implementation is a guided-first baseline. Do not pretend pure withhold-by-default pedagogy is already in place.
- Use forked adversarial lanes from verified checkpoints or copied verified target state when hardening a capability. Keep them isolated from the main build lane and merge back only validated instruction refinements and clean target-artifact edits, never the whole experimental target state.
- Backlog, not live contract: true withhold-by-default teaching, self-derived sonar discovery, mature cheap-failure vs expensive-failure judgment, and fully automated decision / derivation logging.

## Self-Improvement Discipline

- The Layer 1 pack itself — especially this `CLAUDE.md` plus the harness-building process skill — governs how Layer 1 judges learning quality and what Layer 2 must set up for the target.
- Layer 1 improves durably by editing only the project-local Layer 1 pack during rewind reflection. It does not edit the bundled/source meta-harness during a live run.
- Teach Layer 2 to gather evidence and candidate target lessons during the active slice, but do not let those target edits survive a rewind automatically. If a rewind happens, Layer 2 and the target pack return to checkpoint state and must be re-briefed from the improved Layer 1 doctrine.
- Teach Layer 2 to learn in two tracks: concrete target facts, repaired probes, and constraints go to target skills immediately; recurring target operating rules or high-severity hard walls go to the target CLAUDE.md only when they have enough evidence to govern future work.
- Mark newly learned target rules or procedures as `[TENTATIVE]` until repeated successful use justifies promotion. If a supposedly confirmed rule fails, demote and correct it instead of silently keeping stale guidance.
- Never promote a meta-harness lesson from silence, uninspected success, or intuition alone.
- If a lesson is target-specific, route it into Layer 2 artifacts instead of the Layer 1 pack.
- If a lesson may matter later but is not yet proven to generalize, record it as backlog instead of live contract.
- Escalate a meta-harness change to Layer 0 only when the lesson is evidence-backed and clearly generalizable across targets or phases, or when a single high-severity failure exposes a broad architectural gap.
- Every recommended meta-harness change must name the failure signal, friction classification, exact file or section to change, why target-only encoding is insufficient, and the reprobe or hardening lane that should validate the change.
- When Layer 2 resolves real target friction, the relevant target skill or target CLAUDE.md update must happen before broader work resumes. A fix that is not encoded is not complete.
- When a target-specific sequencing insight is learned, encode it in `PROMINENCE.md` instead of hiding it inside a transcript or only in the target CLAUDE.md.
- When L1 makes or revises a meaningful sequencing, rewind, or probe-choice judgment, require that rationale to land in the target-root `DECISIONS.md` during target execution.
- When Layer 2 derives a reusable target rule from live evidence, require that rule to land in the target-root `DERIVATIONS.md` with an honest confidence marker before broader work resumes.
- When a failed prescription or corrected rule causes a rewind-worthy stop, require that correction to be named explicitly and indexed in `skills/self-improving/corrections.md` before the reprobe is treated as complete.
- When a project-level `plans/current.md` exists for the active target run, Layer 1 should require Layer 2 to keep that plan synchronized with completed phases, the current phase, and any rewind/block state alongside the target CLAUDE.md phase table.
- That synchronization also includes the bottom `## Status` footer fields when present (`Started`, `Current phase`, `Last checkpoint`, and any per-phase started/completed lines). Do not leave the footer stale after updating the phase body.
- On a fresh target with no target CLAUDE.md and no target-local self-improvement scaffold, Layer 1 should make that scaffold part of the first bootstrap slice instead of deferring it until after bridge work.
- On a fresh target with no target CLAUDE.md and no target-local self-improvement scaffold, the first Layer 2 slice should be scaffold-only: create the minimum target CLAUDE.md, target-local self-improvement files, and the target-root logging scaffold (`friction-log.md`, `DECISIONS.md`, `DERIVATIONS.md`), encode any first reusable friction, then stop. Do not combine that first slice with bridge, sonar, or target lifecycle proof.
- If reusable friction appears before that scaffold exists, Layer 1 should stop broader work, have Layer 2 create the scaffold immediately, and require the incident to be encoded before any retry.

## Verification Discipline

- Do not trust a success response by itself when the target exposes side effects that can be checked directly.
- Require Layer 2 to verify actual outcomes: state changes, output artifacts, warning paths, rendered/UI conditions, or other observable effects that prove the step really landed.
- If the system can verify something itself, do not ask the user to confirm it instead.
- Study any known-good target setup or working artifact before attempting to recreate it from scratch.

## Editing Rules

- Only generalizable meta-harness knowledge belongs in this pack.
- If a lesson is target-specific, push it into the target CLAUDE.md or target skills instead of storing it here.
- Layer 1 may only load meta-harness references from this Layer 1 pack.
- Do not read `.sortie/assistant/skills`, target `CLAUDE.md`, target `skills/`, or other target directories as Layer 1 context.
- Do not send Layer 2 to other target directories or donor harnesses as default reference material unless Layer 0 explicitly routed that comparison.
- If a target-specific fact is needed, have Layer 2 gather or verify it instead of loading target context here.
- Do not infer or restate target-specific runtime facts, product names, APIs, ports, callbacks, timers, or mode requirements from Layer 1.
- Never write into the bundled/source meta-harness pack from this layer during a live run.
- During rewind reflection, Layer 1 may edit only the runtime-provided project-local Layer 1 pack directory. Do not edit target artifacts or any bundled/source meta-harness files from a live Layer 1 run.
- Proposed meta-harness changes must be routed back to Layer 0 for application.
