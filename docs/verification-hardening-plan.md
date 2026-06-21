# Verification Hardening Plan

## Context

On 2026-06-20, Sigma Painter commit `4f9c6f8` was accepted after Planning
Harness completion, OSTM proof rows, targeted tests, and code-map checks. The
user then reported the same product failure remained: the app still drew a
proxy/draft stroke while dragging, then computed and dropped the real paint
stroke after release.

Fresh adversarial review found the proof lane validated the bug:

- `tests/qt_vulkan_canvas_contract_validation.cpp` required
  `live_preview_mode == "continuous_segment_envelope"` and
  `live_preview_convergence == "deferred_exact_on_release"`.
- `src/qt_shell/sigma_vulkan_canvas_window.cpp` recorded samples during
  `mouseMoveEvent` but called the real mutation path
  `commitToolStrokeSegment(activeStrokeSamples_)` on `mouseReleaseEvent`.
- Packet evidence accepted before/held/after image diffs and FPS/provenance as
  completion proof, but did not prove that the held/live pixels came from the
  same real brush output path as final release.

This is not Sigma-only. The user reports the same failure class in other repos:
agents accept proxy behavior, counters, state JSON, final-state artifacts, or
nearby harness success while the exact user-visible behavior remains wrong.

Open self-improvement blockers:

- `self-improvement:user_correction:a1cc1db8c769f752`
- `self-improvement:verification_gap:023ff284f2d58635`
- Review evidence: `review:behavior_semantic_review:5611ece902dface337`

## Stop Conditions

Do not resume ordinary Sigma Painter implementation until all of these are true:

1. Agent-Doctrine or the relevant installed rules contain an enforceable rule
   for exact user-visible invariant proof and forbidden substitutes.
2. Planning Harness has a concrete packet gate or validator/linter path that
   forces visual, interactive, and performance packets to name:
   - the user-visible invariant,
   - forbidden substitutes,
   - required before/during/after evidence,
   - and a negative assertion that fails on the known bad implementation.
3. CppStudio guidance rejects proxy/preview/deferred-finalization evidence as
   primary proof for realtime viewport, brush, tool, render, or performance
   fixes unless the proxy behavior is explicitly the intended product behavior.
4. A new Sigma work item exists whose first acceptance check fails against
   current `4f9c6f8`.

If any gate is unclear or tool support is missing, stop and file/route the
owning ticket instead of patching Sigma production code.

## Target Outcome

Future agents cannot close visual, interactive, or performance bugs from
supporting artifacts alone. Before implementation and before completion, they
must name the exact user-visible invariant and prove it through the exact user
path.

For Sigma live brush, the invariant is:

> While the pointer is held and moving, product-visible pixels must be updated by
> the same real dry brush engine/output path as the final released stroke, or by
> an explicitly approved live layer that is visually and semantically equivalent
> to committed paint. Release must not introduce a delayed drop-in or materially
> different stroke.

## Workstreams

### 1. Agent-Doctrine Durable Rule

Owner: Agent-Doctrine.

Purpose: make the cross-repo rule visible to both Codex and Claude provider
doctrine without directly editing deployed provider files.

Tasks:

1. Inspect current dirty Agent-Doctrine doctrine edits and preserve them.
2. Patch provider-specific source modules, not generated files first.
3. Add a concise always-on rule to operating or implementation discipline:
   - reported visual, interactive, or performance fixes must name the exact
     user-visible invariant before closeout;
   - forbidden substitutes include proxy behavior, preview-only behavior,
     deferred-finalization behavior, final-only screenshots, internal counters,
     backend readbacks, widget state, FPS alone, provenance alone, and non-empty
     image diffs unless those directly prove the invariant;
   - tests that encode the reported failure as success are blockers.
4. Regenerate Codex and Claude outputs.
5. Validate both provider lanes and full parity.
6. Install snapshots only after validation and existing dirty/doctrine drift is
   understood.

Acceptance:

- Generated `AGENTS.md` and `CLAUDE.md` include the rule.
- Validator proves source/output parity.
- Installed user-level files are verified if rollout is part of the task.
- Self-improvement blocker is not closed until source and installed surfaces are
  named.

### 2. Planning Harness Gate

Owner: Agent-Planning-Harness.

Purpose: prevent structurally valid packets from marking the wrong acceptance
invariant as satisfied.

Required packet fields for visual, interactive, or performance work:

- `user_visible_invariant`: exact behavior that must be true to the user.
- `known_bad_current_behavior`: what must fail on the current baseline.
- `forbidden_evidence`: evidence types that cannot close this lane.
- `required_evidence`: before/during/after artifacts or metrics tied to the
  invariant.
- `negative_assertion`: at least one test/proof selector that fails on the known
  bad implementation.
- `release_or_finalization_check`: required when the symptom includes delayed
  drop-in, release-only finalization, or post-action computation.

Tasks:

1. Locate Planning Harness source and current packet schema/validators.
2. Add schema support or a strict linter for these fields.
3. Make `completion-claim` fail when:
   - the packet is visual/interactive/performance work and lacks the fields;
   - acceptance evidence does not map to the invariant;
   - forbidden evidence is listed as primary completion evidence;
   - no negative assertion is recorded;
   - the known bad implementation would pass the acceptance check.
4. Add tests with a minimal packet that mimics Sigma's bad proof:
   - `deferred_exact_on_release` accepted as completion should fail;
   - before/held/after non-empty diffs without live-state equivalence should
     fail;
   - a packet with explicit invariant, forbidden evidence, and negative
     assertion should pass.
5. Install/roll out the updated harness if it is user-level tooling.

Acceptance:

- A fixture based on the Sigma proxy-stroke packet fails before correction and
  passes after proper invariant mapping.
- `completion-claim` produces actionable blocker messages naming the missing or
  forbidden fields.
- User-level installed Planning Harness behavior is verified if applicable.

### 3. CppStudio Verification Rule

Owner: CppStudio source/skill lane.

Purpose: harden native C++ GPU/realtime supervision, where proxy and supporting
artifact failures are common and costly.

Tasks:

1. Locate the CppStudio source skill/rule repo, not installed snapshots.
2. Add or update a viewport/brush/tool/performance closeout rule:
   - live/realtime claims need held-state proof of real product state;
   - proxy/preview/deferred finalization is a failed acceptance unless it is the
     approved product behavior;
   - if release lag or drop-in is reported, prove release-to-final-frame
     latency and absence of visible replacement jump;
   - panning/zooming/brush performance claims need action-specific FPS/latency,
     not generic frame rows.
3. Add examples for Sigma-like brush behavior and renderer/viewport analogs.
4. Run skill/package validation and install for both Codex and Claude if the
   source owns both surfaces.

Acceptance:

- Installed CppStudio skill text contains the rule after rollout.
- A fresh worker-path probe asked to close a proxy-preview bug refuses to close
  from supporting artifacts alone.

### 4. Packet Linter / Forbidden Evidence Detector

Owner: Planning Harness or Agent-Doctrine, depending on where validators live.

Purpose: catch semantic red flags mechanically.

Initial flagged terms:

- `proxy`
- `preview-only`
- `preview envelope`
- `continuous_segment_envelope`
- `deferred_exact_on_release`
- `final-only`
- `supporting evidence`
- `non-empty diff`
- `state JSON`
- `counter`
- `FPS` when no action-specific invariant is named

Tasks:

1. Decide whether this belongs in Planning Harness, Agent-Doctrine pressure
   tests, or both.
2. Implement as a warning or blocker based on packet type:
   - blocker for reported visual/interactive/performance bug packets;
   - warning for neutral planning docs unless a closeout claim is present.
3. Add allowlist only when the packet explicitly says the proxy/preview is the
   intended product behavior and names the user-approved reason.
4. Add tests using Sigma bad packet snippets.

Acceptance:

- The exact Sigma bad vocabulary is detected.
- Legitimate preview-tool work can pass only when it explicitly defines preview
  as the product behavior.

### 5. Sigma New Work Item

Owner: Sigma Painter worker, after Workstreams 1-4 are sufficiently in place.

Purpose: fix the actual product behavior under the new verification contract.

Required first step:

- Create a new Planning Harness work item or packet. Do not continue the
  completed `planning.sigma-real-brush-engine` packet.

Required failing baseline proof against `4f9c6f8`:

1. Test or proof selector shows that drag/held state uses proxy/deferred
   behavior.
2. It fails if `live_preview_convergence == "deferred_exact_on_release"`.
3. It fails if real document/tile/mask output does not update during move.
4. It fails if release creates a delayed jump or materially different stroke.

Possible implementation directions:

- Incrementally commit brush segments during move and make release only finalize
  undo grouping.
- Use a live layer/buffer only if it is generated by the same brush engine and
  visually/semantically equivalent to committed paint, with bounded release
  convergence.
- Avoid full-stroke recomputation on release for every event path.

Required acceptance:

- Exact user launcher is rebuilt and run.
- Before/during/after artifacts are captured from the exact user path.
- During artifacts prove real brush output, not proxy overlay.
- Release latency is measured and bounded.
- The old test expectations for `deferred_exact_on_release` are removed or
  inverted.
- A fresh adversarial review runs after implementation and before commit.

### 6. Self-Improvement Closure

Owner: current supervisor after hardening lands.

Tasks:

1. Keep the blocking items open until doctrine/harness/CppStudio work is
   verified.
2. Record fresh review evidence and final decisions with exact item IDs.
3. Close `self-improvement:user_correction:a1cc1db8c769f752` only after durable
   doctrine/source artifacts are patched and validated.
4. Close `self-improvement:verification_gap:023ff284f2d58635` only after the
   capture failure has a concrete verified response.
5. If some enforcement must be deferred, file Plane tickets with owning repo,
   exact missing enforcement, and stop condition.

Acceptance:

- Runtime records name source artifacts, installed artifacts when applicable,
  validation commands, and residual gaps.
- No self-improvement item is closed from chat-only acknowledgment.

## Sequencing

1. Freeze Sigma production implementation.
2. Resolve Agent-Doctrine source rule and regenerate/validate.
3. Patch Planning Harness gate or file the exact Plane ticket if that repo is
   not immediately editable.
4. Patch CppStudio source skill/rule or file the exact Plane ticket if that repo
   is not immediately editable.
5. Add linter/pressure tests for the forbidden-evidence pattern.
6. Create the new Sigma work item with a failing baseline proof.
7. Implement Sigma live brush behavior.
8. Run exact user-path visual/latency proof.
9. Run fresh adversarial review.
10. Commit only after all completion gates pass.

## Open Risks

- Existing Agent-Doctrine worktree is dirty; preserve unrelated doctrine edits.
- Planning Harness may need a schema migration or compatibility rule.
- CppStudio source and installed skill surfaces may differ; rollout must verify
  both Codex and Claude if both are supported.
- Some repos may need local domain-specific invariant definitions; the global
  rule should enforce the shape, not guess each product's invariant.
- Screenshot diffs alone are easy to game; proof needs semantic comparison or
  app-owned state tied directly to real product pixels.

## Immediate Next Check

Before implementation, run a fresh adversarial review on this plan and fix
actionable planning issues. Then route workstream tickets or workers by owning
repo.
