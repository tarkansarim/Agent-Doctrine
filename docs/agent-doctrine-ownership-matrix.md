# Agent-Doctrine Ownership Matrix

Agent-Doctrine owns provider doctrine generation and installation. It should not
own every operational procedure that user-level doctrine mentions.

| Current surface | Target owner | Agent-Doctrine role |
| --- | --- | --- |
| Provider boundary, managed markers, adoption/import, drift, generation, validation, install | Agent-Doctrine | Own source, generated output, installer, validators, and the narrow doctrine router skill. |
| Durable `AGENTS.md` / `CLAUDE.md` changes | Agent-Doctrine | Route changes through source modules and snapshot install. |
| Reddit primary-thread access for community/adoption research | CeilingResearch / `ceiling-research` | Keep only a one-line trigger to load `ceiling-research`; detailed RSS/WebSearch route lives in `references/reddit-access.md`. |
| Plane ticket command syntax, state moves, rollout closeout | Plane-Tickets / Agent-Ticket-Orchestration | Keep only bootstrap trigger if needed; exact CLI/API contract belongs to Plane owner. |
| Tool failure recovery | Agent operations/tooling owner, to be split | Keep hard gate to stop and route; detailed taxonomy belongs outside Agent-Doctrine. |
| Implementation and visible-proof procedure | Verification/implementation discipline owner, to be split | Keep minimal proof gate; detailed procedure belongs outside Agent-Doctrine. |
| Parity/migration closeouts | Integration/release closeout owner, to be split | Keep completion honesty gate; detailed checklist belongs outside Agent-Doctrine. |
| Rewind procedure and patch-stacking workflow | Rewind | Keep rollback-anchor invariant and trigger; procedure belongs to Rewind. |
| CppStudio native GPU/CUDA/Vulkan procedure | CppStudio skills | Keep one-line trigger only. |

## Extraction Rule

When a module describes commands, endpoints, examples, local service behavior,
or domain-specific validation, it belongs to the specialist owner. Agent-Doctrine
keeps only the provider bootstrap rule and a trigger to the owning skill.

## Current Slice

Reddit access was extracted from `agent-doctrine-router` to
`ceiling-research/references/reddit-access.md`. The generated provider doctrine
now points to `ceiling-research` for that route.
