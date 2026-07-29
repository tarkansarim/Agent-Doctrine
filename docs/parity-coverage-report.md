# Parity / Coverage Report For Second-Pass Lean Doctrine

Scope: second-pass trim for generated `generated/claude/CLAUDE.md` and
`generated/codex/AGENTS.md`.

Rules are not silently dropped. Dispositions below are:

- **Inline**: active in generated doctrine.
- **Relay**: active by one-line pointer to a named skill and section.
- **Sidecar**: preserved outside generated doctrine as source/audit metadata.
- **Ledger**: preserved outside generated doctrine in adopted snapshots or
  provider ledgers.

## Verified Relay Homes

- `agent-doctrine-router` remains the single shipped Agent-Doctrine relay skill.
  Its thin top-level `SKILL.md` routes every matched task to
  `package/agent-doctrine-router/modules/core.md`.
- `modules/core.md` owns the detailed doctrine-change workflow, landing-surface
  classification, provider boundaries, and stop conditions. Both Codex and
  Claude skill installers snapshot the full package tree so this routed body is
  available at runtime.
- Existing relay pointers to `pressure-lab`, `rewind-checkpoints`,
  `self-improving`, `reply-verbosity`, and `cpp-cuda-vulkan-studio` remain
  unchanged where the generated doctrine already delegates to those skills.

## Header / Adoption Metadata Moves

| Old runtime-loaded content | Current disposition |
| --- | --- |
| Generated-from sentence for Codex | Removed from runtime output; source relation remains in `source/codex/manifest.json`, `source/codex/inventory.json`, and the generator. |
| Generated-from sentence for Claude | Removed from runtime output; source relation remains in `source/claude/manifest.json`, `source/claude/inventory.json`, and the generator. |
| Source inputs list for Codex | Removed from runtime output; Sidecar/source paths remain in `source/codex/manifest.json` and `source/codex/inventory.json`. |
| Source inputs list for Claude | Removed from runtime output; Sidecar/source paths remain in `source/claude/manifest.json` and `source/claude/inventory.json`. |
| Adopted Live User-Level AGENTS.md source path, snapshot path, hashes, provider lane, adoption scope | Sidecar at `source/codex/adopted/adoption-manifest.json`; exact snapshot remains Ledger at `source/codex/adopted/live-user-level-AGENTS.md`. |
| Adopted Live User-Level CLAUDE.md source path, snapshot path, hashes, provider lane, adoption scope | Sidecar at `source/claude/adopted/adoption-manifest.json`; exact snapshot remains Ledger at `source/claude/adopted/live-user-level-CLAUDE.md`. |
| Runtime recovery note that the adopted baseline is archival | Sidecar note in each provider adoption manifest. |

## Claude Coverage

| Old/current section | Current disposition |
| --- | --- |
| `# Claude Configuration Boundary` | Inline; first rule section in generated `CLAUDE.md`. |
| `# Claude Operating Discipline` always-on constraints | Inline. |
| Conflicts procedure | Inline compact rule. |
| Tool Failures: stop, classify real issue vs wrapper limitation, fix/validate owned real issues, permitted alternate route for external limitations | Inline. |
| Autonomous Progress | Inline. |
| Implementation Discipline: Before Editing, While Editing, Verification | Inline. |
| Plane ticket closeout install/comment/no-close-while-uninstalled rule | Retired from the current generated output and router package. |
| Pressure-Lab Hardenability | Inline trigger to `pressure-lab`. |
| Replay And Learning | Inline causal/replay invariants plus relay pointers to `rewind-checkpoints` and `self-improving`. |
| Doctrine Change Routing | Inline source boundary and provider separation rules plus relay pointer to `agent-doctrine-router`. |

## Codex Coverage

| Old/current section | Current disposition |
| --- | --- |
| `# Codex Configuration Boundary` | Inline; first rule section in generated `AGENTS.md`. |
| `# Codex Operating Discipline` always-on constraints | Inline. |
| Conflicts procedure | Inline compact rule. |
| Tool Failures: stop, classify real issue vs wrapper limitation, fix/validate owned real issues, permitted alternate route for external limitations | Inline. |
| Autonomous Progress | Inline. |
| Parity And Completion Closeouts: implemented slices, verified behavior, remaining weaker/missing features, live-proof gaps, accepted non-goals, unfinished planned points, no premature parity claims | Retired from the current generated output and router package. |
| Implementation Discipline: Before Editing, While Editing, Verification | Inline. |
| Codex-only implementation depth Tier 2, request interpretation, and MCP argument-loss handling | Retired from the current generated output and router package. |
| Local Plane Ticketing: Plane filing, repo project/tag, no Kanboard unless explicit, report id/URL | Dormant source module; excluded from the active Codex manifest and router package. |
| Pressure-Lab Hardenability | Inline trigger to `pressure-lab`. |
| Rewind And Learning | Inline causal/replay invariants plus relay pointers to `rewind-checkpoints`, `self-improving`, and `cpp-cuda-vulkan-studio`. |
| Doctrine Change Routing | Inline source boundary and provider separation rules plus relay pointer to `agent-doctrine-router`. |

## Coverage Notes

- Generated output no longer includes provenance/header metadata. The first
  loaded content after each managed marker is the provider Configuration
  Boundary section.
- The exact adopted snapshots remain untouched and recoverable; the new
  adoption manifests carry audit hashes and explicitly mark themselves
  `runtime_loaded=false`.
- No known rule from the first-pass generated outputs was dropped. Content that
  stopped appearing inline is mapped above to a relay module, sidecar, or ledger.
