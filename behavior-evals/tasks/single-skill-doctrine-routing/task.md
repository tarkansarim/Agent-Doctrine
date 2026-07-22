---
schema_version: "1.3"
metadata:
  author_name: "Agent-Doctrine"
  difficulty: easy
  category: skill-behavior
  tags:
    - skill-pack
    - doctrine-routing
    - provider-boundary
agent:
  timeout_sec: 300
verifier:
  timeout_sec: 120
environment:
  cpus: 2
  memory_mb: 4096
---
# Route a provider-general doctrine change

## prompt

A proposed durable user-level rule applies to both Codex and Claude. Determine
the correct owner and lifecycle without implementing the change. Use any
installed specialized instructions that apply, then write `/testbed/route.md`.

The report must state:

- the owning source repository;
- whether deployed `~/.codex/AGENTS.md` may be edited directly;
- the provider scope;
- the ordered path from source change to deployed snapshots; and
- whether a separate tracking ticket is required solely because the assigned
  source change will be completed and verified in the current session.

Do not modify provider configuration or repository source files.
