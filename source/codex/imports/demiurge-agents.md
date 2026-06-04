# Imported Codex Doctrine Source

- Source path: `<workspace root>/Demiurge/AGENTS.md`
- Source SHA256: `6031bdb104ac373c3b95d962d64d5228152519c9a35e55c7bebb410caf45bd3b`
- Provider lane: `codex`

## Original Content

# Repository Guidelines

## Project Structure & Module Organization

Demiurge now has docs plus a first WebGUI scaffold. `HANDOFF_CONTEXT.md`: state, references, constraints. `plans/generalized-node-system.md`: architecture. `src/`: Vite/React runtime workbench.

Current layout: `src/runtime/` canonical graph/runtime/types, `src/components/` React Flow workbench UI, `infra/n8n/` local n8n spike/reference, `plans/` architecture/specs. Put retired renderer experiments under `archive/` so active surfaces stay uncluttered. Keep reference projects external unless explicitly porting.

## Build, Test, and Development Commands

Canonical commands:

- `npm run dev`: start Vite WebGUI on localhost.
- `npm run build`: type-check and build production assets.
- `npm test`: run Vitest tests.
- `npm run n8n:config`: validate local n8n Compose config.
- `npm run n8n:up` / `npm run n8n:down`: start/stop local n8n evaluation stack.
- `npm run n8n:test-adapter`: call the active n8n adapter webhook and validate result shape.
- `npm run n8n:read-execution`: read n8n execution detail via API key or local Docker Postgres fallback.
- `npm run n8n:harness:auth` / `npm run n8n:harness:smoke`: save n8n browser auth state and probe UI control.
- `npm run n8n:harness:scenario`: run the default declarative n8n UI-control scenario.
- `npm run path:list`: validate and list specialization path definitions.
- `npm run graph:from-path -- harness_creation.v1`: derive canonical graph JSON from a specialization path.
- `npm run graph:execute-proof -- harness_creation.v1`: run one canonical graph proof slice and write ignored `.demiurge/state/` records.
- `rg "Node Contract|First Prototype" plans/generalized-node-system.md`: jump to key architecture sections.
- `wc -c AGENTS.md`: verify Codex instruction size.
- `git status` / `git log`: inspect working state, commits, and rollback anchors.

## Coding Style & Naming Conventions

Write `AGENTS.md` rules in telegraphic imperative style: short commands, minimal prose, rationale only for behavior changes.

Keep code-facing names technical. Prefer: `checkpoint`, `proof`, `node_contract`, `artifact_schema`, `verification_runner`, `runtime_adapter`.

Use TypeScript strict mode. Keep React components small. Treat runtime data as source of truth; UI state maps runtime events to visuals.

Keep canonical path data node-system agnostic. Do not store renderer layout, theme, viewport, n8n workflow IDs, React Flow-only fields, or any canvas-engine-only fields in `src/runtime/pathTypes.ts` path definitions. Put graph-engine specifics in adapters.

## Agent Operating Rules

- Before architecture changes, read `HANDOFF_CONTEXT.md`.
- Treat `<workspace root>/GuiControlHarnessCreator` as live Harness content reference; do not edit unless explicitly asked.
- Use `fixtures/harness-architect/GuiControlHarnessCreator/` as Demiurge's local Harness snapshot for graph proofs and n8n runs. Refresh by copying from the live reference only when asked or when a new accepted boundary must be imported.
- Treat `<workspace root>/sortie` as runtime/source reference. Do not edit unless the runtime itself is the task.
- Use this `AGENTS.md` for Demiurge-specific overrides.
- Work autonomously through agreed graph/proof milestones. Pause only for real blockers, explicit gates, direction-changing tradeoffs, or actions needing user authority.
- If the user delegates an autonomous finish, do not stop for optional confirmations or visible check-ins that tooling can cover. Continue until the active slice is implemented, verified, and committed.
- Use official tools, adapters, cleanup paths first. Bypass only when that surface is the bug; state why, contain, rerun properly before trusting results.
- After reload, restart, install, or environment change, verify the intended runtime is active.
- At phase boundaries, verify artifacts, runtime state, rendered/UI state, logs, and generated files agree where relevant.
- For graph milestones, involve the user visibly. Run code tests/build/generation first, then stop at the live graph UI before milestone execution/inspection. Tell the user the exact URL/workflow/graph name and what should be visible. Use offscreen OSTM for graph UI only when the user explicitly permits it or for non-milestone regression checks.
- After compaction/resume, reread `AGENTS.md`, `HANDOFF_CONTEXT.md`, and active plans before acting.
- If a fix path fails, remove speculative edits before a materially different approach. Keep only independently verified changes.
- If struggling, create a rollback-anchor git commit before deeper investigation. Probe freely, record evidence. Once root cause is known, roll back to the anchor and apply the fix cleanly.
- Work in explicit milestones. After each graph/workflow milestone, stop and verify it in the active n8n graph or graph UI before adding the next slice. Do not stack nodes or refs without rendered graph evidence.
- Promote phases to executable proof only when source artifacts show accepted/pass/complete evidence. Pending plans, precreated files, or "not started" status stay metadata-only.
- Encode durable lessons in durable files: short default behavior in `AGENTS.md`; procedures in skills or docs. Do not rely on chat memory.
- End final replies with `What's next:` and the next concrete project step.

## Imported L1 Doctrine

Use transferable rules from Harness Architect L1 sources:

- `<workspace root>/GuiControlHarnessCreator/AGENTS.md`
- `.sortie/assistant/skills/sonar-design/SKILL.md`
- `.sortie/assistant/skills/verify-before-wiring/SKILL.md`
- `.sortie/assistant/skills/harness-building-process/SKILL.md`
- `.sortie/assistant/skills/target-bootstrap/SKILL.md`
- `.sortie/assistant/skills/stress-testing/SKILL.md`

Apply these rules in Demiurge form:

- Sonar before trust. Before reading output, define the expected signal, wrong signal, and whether the instrument can expose it.
- Verify with text/state first: generated JSON, tests, DB payloads, logs, DOM text, runtime state. Use screenshots as calibration or genuinely visual proof, then prefer text-queryable signals.
- Never ask the user to verify what tooling can read. Ask only when authority, taste, or unavailable external context is required.
- Verify before wiring. Trace dependencies end to end, reuse existing paths, confirm handlers/resources are initialized at call time.
- No invented valid values. Query current options, official docs, or runtime state. If the option set is unavailable, stop and expose the blocker.
- Expectation gap protocol: stop normal progress, state expected observable outcome, state actual observed outcome, identify the missing/wrong model or signal, then retry the same case after updating the model.
- Smallest proof slice first. Each slice declares evidence, executes, verifies, then records durable lessons before broader work resumes.
- Stress testing is a completion gate. Cover every built domain/phase, include cross-domain and ambiguous cases, require zero unexpected errors, and update durable artifacts after each fixed failure.
- Do not copy Harness-specific MCP/runtime cleanup rules into Demiurge unless Demiurge owns the same runtime surface. Import the principle, adapt the tool path.

## Testing Guidelines

Use Vitest. Add tests beside proven modules or under `tests/`. Name behavior: `node_contract_rejects_missing_proof`.

## Commit & Pull Request Guidelines

Use short imperative subjects matching current history: `Add n8n execution reader`, `Normalize n8n adapter boundary`.

PRs: include summary, touched paths, verification, reference-project assumptions. Link issues/plans when relevant. Add screenshots only for UI-facing graph or panel changes.

## Instruction Size

Keep this `AGENTS.md` under Codex's default `project_doc_max_bytes` limit: 32 KiB. After edits, run `wc -c AGENTS.md`. If over 32768 bytes, compact prose; keep constraints, commands, paths, meaning.
