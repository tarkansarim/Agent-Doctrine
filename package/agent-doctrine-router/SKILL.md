---
name: agent-doctrine-router
description: "Route durable AGENTS.md/CLAUDE.md doctrine, provider-boundary changes, source generation, validation, install, adoption/import, and drift handling."
---

<!-- thin-relay:v1 -->
# Agent Doctrine Router

Load this skill when its frontmatter description matches the task.

## Always

- Read `modules/core.md` before taking skill-specific action.
- Keep detailed procedure, examples, and edge cases in modules, not this relay.
- Load only the module needed for the current task.

## Route

| Task | Module |
| --- | --- |
| Any task matched by this skill description | `modules/core.md` |

## Hard Limits

- Do not act from this relay alone when the routed module is available.
- Do not create another discoverable `SKILL.md` inside this package.
