# Claude Configuration Boundary

- Claude Code user rules, agents, skills, hooks, and persistent Claude
  behavior live under `~/.claude` unless the user explicitly says otherwise.
- Treat `~/.codex` as a separate Codex configuration namespace.
- Do not normalize Codex and Claude doctrine into one deployed file or one
  shared runtime folder.
- Do not directly patch deployed user-level `~/.claude/CLAUDE.md`. Durable
  doctrine changes are source-owned by the Agent-Doctrine repo and must flow
  through its ticketed pipeline.
