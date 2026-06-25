# Claude Configuration Boundary

- Claude Code user rules, agents, skills, hooks, and persistent Claude
  behavior live under `~/.claude` unless the user explicitly says otherwise.
- Treat `~/.codex` as a separate Codex configuration namespace.
- Do not normalize Codex and Claude doctrine into one deployed file or one
  shared runtime folder.
- Do not directly patch deployed user-level `~/.claude/CLAUDE.md`. Durable
  doctrine changes are source-owned by the Agent-Doctrine repo and must flow
  through its ticketed pipeline.
- Do not create, keep, or install backup artifacts inside user-level provider
  roots such as `~/.claude` or `~/.codex`; move `.bak`, `.old`, timestamped, or
  rollback copies to a cache/backup path outside those roots.
