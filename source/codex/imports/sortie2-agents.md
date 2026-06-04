# Imported Codex Doctrine Source

- Source path: `<workspace root>/sortie2/AGENTS.md`
- Source SHA256: `cac55fd1a9179156bd98ede9ce6269bb3c9b3dc69592ac1121e283873198dd95`
- Provider lane: `codex`

## Original Content

# Project Rules

This repo currently uses [CLAUDE.md](<workspace root>/sortie2/CLAUDE.md) as the active workspace instruction file. The rules there remain in force. This file exists to make the repo-level rules explicit and durable.

## Earned Capability Design (MANDATORY)

Before adding a new process mechanism, gate, queue, reviewer, memory surface,
agent role, runtime automation, or Harness lane, first ask whether the desired
behavior can be earned through lower-level pressure, occlusion, affordance,
trace, replay, structural dependency, or hard-contract boundaries.

Do not implement the visible high-level behavior directly when the lower-level
conditions can make it emerge. Create the smallest environment where the direct
shortcut is unavailable, the real goal and raw contact remain visible, and the
useful behavior becomes the path with traction.

Promote the lower-level condition that made the behavior emerge, not the
surface behavior itself. A pattern is not ready for skill/runtime promotion
until it survives replay or nearby variation without relying on the original
top-down instruction.

## Build After Every Code Change (MANDATORY)

After ANY code change (edit, write, or new file), run:

```bash
cd <workspace root>/sortie2 && bash install-extension.sh
```

Do not ask the user to test or reload before that full install completes successfully.

## Implementation Close-Out Discipline (MANDATORY)

After finishing an implementation, always state what is still left or explicitly state that no known implementation work remains for the requested scope. Do this even when tests pass.

When an implementation changes tracked files and the required verification/install steps pass, commit the intentional tracked changes before handing the work back. Do not wait for a separate "commit" prompt. Keep transient runtime state, bridge files, local MCP files, event logs, and unrelated user changes out of the commit.

## Harness Runtime Fix Reload Order (MANDATORY)

When a Harness Architect issue requires a Sortie code, prompt, skill, or instrumentation fix during an active or tainted run, use this order:

1. Stop/reset affected Harness workers and tracked target processes first.
2. Clear the tainted run state and wipe disposable Layer 2 target artifacts.
3. Apply the fix.
4. Run `bash install-extension.sh` from this repo.
5. Reload VS Code through Sortie's internal supervisor bridge, not GUI automation.
6. Verify the active bridge, the installed-extension `.sortie-harness-data/.../harness-control.json`, backend Harness state, and rendered panel state before rerunning the phase.

Do not rerun Harness Architect against patched source until the installed extension has picked up the change through a full VS Code reload.

## Harness Runtime Storage Boundary (MANDATORY)

Generated Harness Architect runtime state, checkpoints, Layer 1 pack, control manifests, adversarial lanes, and target harness artifacts must live under the installed extension data root:

```text
~/.vscode/extensions/tarka.sortie-1.0.0/.sortie-harness-data/projects/<project-key>/
```

Do not store new Harness target artifacts under this repo's `targets/` directory or new Harness runtime state under repo-local `.sortie/harness/`. Each external project storage directory has `project.json` mapping it back to the real source project root. Rewind/snapshot code must operate on the external Harness target directory, never on the source repo root.

## Harness Rewind Destructive Guardrails (MANDATORY)

Harness filesystem and git snapshot restore paths are destructive by design: they remove the current target tree before materializing the checkpoint. They must never run against the source repo root, repo-local `targets/`, repo-local `.sortie/harness/`, old `<workspace root>/sortie` roots, or any path outside the installed-extension Harness storage root.

Before using or modifying rewind/snapshot code:
- Verify the checkpoint `channel_values.context.session.targetPath` is under the installed-extension `.sortie-harness-data/projects/<project-key>/targets/<target>/` path or an installed-extension Harness lane `harness/lanes/<lane-id>/target` path.
- Verify the snapshot adapter refuses source-repo and repo-local target paths before it can call `fs.rmSync`, `git restore`, or any equivalent destructive operation.
- Run `npm run verify:harness-rewind-storage-guardrails` after changes touching snapshot, rewind, reset, checkpoint, target-path canonicalization, or Harness storage paths.
- If an old checkpoint points at an unsafe path, treat that checkpoint as non-restorable evidence. Do not rewind from it.

## Harness Architect Driving Skill Maintenance (MANDATORY)

When operating Harness Architect, if you have to figure out a missing runtime-control detail, command-palette detail, verification path, or safe-driving rule, update the Harness Architect driving skill before treating the work as complete:

- project-local active skill: `.sortie/assistant/skills/harness-architect-window/SKILL.md`
- bundled assistant-pack skill: `data/assistant-pack/skills/harness-architect-window/SKILL.md`

Keep the update concrete and procedural so the next session can execute the same action without rediscovery.

## Harness L1 Supervisor Nudge Minimalism (MANDATORY)

When driving Harness Architect, keep Supervisor/L1 instructions sparse by default. Supervisor/L1 should normally express the strategic user intent only, such as `Start a new Harness Architect run for Blender` or `Continue the current Blender run`.

Do not pack Supervisor/L1 messages with detailed phase policy, scaffold instructions, runtime doctrine, anomaly-census interpretation, or implementation constraints unless the explicit purpose is to probe a specific Supervisor/L1 or Target Executor behavior. Those details belong in L1 skills, runtime doctrine, prompts, or generated executor briefs so the run tests whether L1 doctrine actually knows how to drive the process.

If a detailed Supervisor/L1 message is intentionally used as a probe, label it as a probe in the message and record what behavior is being tested. Otherwise, treat over-specified Supervisor/L1 instructions as tainting the run baseline.

## Fix Chain Integrity (MANDATORY)

When fixing a bug, preserve the surrounding chain of behavior. Do not patch the local symptom in a way that breaks upstream callers, downstream consumers, worker handoffs, runtime state transitions, UI expectations, persisted data formats, or other neighboring process contracts.

Before changing code for a fix:
- Identify the immediate contract being repaired.
- Identify known upstream callers and downstream dependants that rely on the current behavior.
- Identify the invariants those dependants need to remain true.

During the fix:
- Keep existing contracts intact unless the contract itself is wrong.
- Treat callers, prompts, skills, and worker instructions as dependants of the contract; do not patch those dependants to route around a broken predicate, provider, or upstream invariant unless the contract itself must change.
- If a contract must change, update every dependent caller, consumer, test, prompt, skill, and persisted-state path in the same fix.
- Prefer a fix that satisfies both the original bug and the neighbouring contract needs instead of trading one broken link for another.

Before declaring the fix complete:
- Verify the original failure path.
- Verify the dependent paths that could be affected by the change.
- If any dependant breaks or loses a required invariant, adjust the fix until the full chain is coherent again.

## Harness Reset Discipline (MANDATORY)

When a Harness Architect run is tainted by a process or instrumentation issue, do not carry that run forward as the next baseline.

A run is tainted if any of the following happened:
- misleading or incorrect harness activity/transcript labeling
- Layer 1 or Layer 2 violated the assigned phase contract
- stale chat/transcript state would contaminate the next proof pass
- Layer 2 generated target artifacts during a dirty or untrusted run
- a harness/runtime bug was fixed mid-run and the user is about to reload or continue

If a tainted harness run requires a code fix, prompt fix, instrumentation fix, or process fix, you MUST clean up the tainted run before you make the fix. Do not leave live workers, active target processes, or dirty harness state running while you patch the system.

Required order for tainted Harness Architect runs:

1. Stop and reset the affected harness workers first.
2. Stop and reset any tracked target process.
3. Clear the affected harness chat/transcript state.
4. Remove the affected active harness session state/records.
5. Wipe the Layer 2-generated target artifacts from the dirty run.
6. Only preserve dirty chat state or dirty target artifacts if the user explicitly says to keep them for forensics.
7. Only after steps 1-5 are complete may you make the fix.
8. Treat the dirty run as disposable process evidence, not as trusted progress.

Do not preserve stale Layer 2 output by default just because deleting it is destructive. In Harness Architect, a dirty proof run is not a deliverable.
