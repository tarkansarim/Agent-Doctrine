# Claude Configuration Boundary

<!-- agent-doctrine-rule:config.provider-root -->
- Claude Code user rules, agents, skills, hooks, and persistent Claude
  behavior live under `~/.claude` unless the user explicitly says otherwise.
<!-- agent-doctrine-rule:config.provider-separation -->
- Keep provider ownership separate. For Claude-only work, do not inspect or
  patch `~/.codex`. When the user explicitly asks for cross-provider diagnosis,
  parity, migration, or adoption, inspect both provider surfaces read-only as
  needed; write each provider only through its owning source/install pipeline.
<!-- agent-doctrine-rule:config.deployment-isolation -->
- Do not normalize Codex and Claude doctrine into one deployed file or shared
  runtime folder.
<!-- agent-doctrine-rule:config.source-owned-doctrine -->
- Do not directly patch deployed user-level `~/.claude/CLAUDE.md`. Durable
  doctrine changes are source-owned by the Agent-Doctrine repo and must flow
  through its ticketed pipeline.
<!-- agent-doctrine-rule:config.no-provider-root-backups -->
- Do not create, keep, or install backup artifacts inside user-level provider
  roots such as `~/.claude` or `~/.codex`; move `.bak`, `.old`, timestamped, or
  rollback copies to a cache/backup path outside those roots.
