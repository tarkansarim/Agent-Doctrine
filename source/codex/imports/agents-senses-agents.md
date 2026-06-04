# Imported Codex Doctrine Source

- Source path: `<workspace root>/Agents-Senses/AGENTS.md`
- Source SHA256: `ade6f3a7c82fdabbd221b7d4602cd3142259fcdf9bb283e80a802611ee3d5ac3`
- Provider lane: `codex`

## Original Content

# Agents-Senses Agent Rules

## External Target Missions

When another repository is used as a live pressure case for Agents-Senses, start
and maintain an external target mission before target work:

```bash
npm run external:mission -- start ...
```

`EXTERNAL_PRESSURE_GATE.md` is only the lower-level evidence trail. It is not
sufficient by itself for real external-repo work.

Rules:

- The orchestrator may inspect external target repositories, but must not edit,
  patch, format, commit, install, or otherwise mutate them.
- Target mutations must be routed to the target repo owner worker through the
  mission-owned ticket flow.
- Rewind readiness is required before mutation phases.
- Use `npm run external:mission -- guard --boundary target-edit` before any
  target edit decision.
- Use `npm run external:mission -- guard --boundary next-patch` before another
  patch attempt after first resistance or weak proof.
- Use `npm run external:mission -- guard --boundary fixed-claim` before any
  fixed/done claim.
- Use `npm run external:mission -- guard --boundary leave-task` before leaving
  an external target task.
- If donor/source or visual proof is required, append `donor-source` and
  `visual-artifact` evidence before closeout.
- After first resistance, append `friction` and require `worker-family` evidence
  before another patch attempt.
- Closeout requires target proof and Agents-Senses `learning` evidence.

If the mission controller blocks progress, stop and report the missing evidence
or phase prerequisite. Do not continue by falling back to ordinary Codex target
debugging.
