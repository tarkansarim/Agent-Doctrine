# Codex Configuration Boundary

- Codex user rules, protocols, skills, hooks, and memory live under `~/.codex`
  unless the user explicitly says otherwise.
- Do not read from or patch `~/.claude` for Codex behavior; only explicit
  Agent-Doctrine adoption/import may read `~/.claude/CLAUDE.md` as source.
- Translate copied Claude-owned paths to Codex equivalents without inspecting
  Claude files.
- Do not directly patch deployed user-level `~/.codex/AGENTS.md`. Durable
  doctrine changes are source-owned by the Agent-Doctrine repo and must flow
  through its source generation and install pipeline.
- Do not create, keep, or install backup artifacts inside user-level provider
  roots such as `~/.codex` or `~/.claude`; move `.bak`, `.old`, timestamped, or
  rollback copies to a cache/backup path outside those roots.
