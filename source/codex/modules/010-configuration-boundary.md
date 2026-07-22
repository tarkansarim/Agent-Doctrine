# Codex Configuration Boundary

<!-- agent-doctrine-rule:config.provider-root -->
- Codex user rules, protocols, skills, hooks, and memory live under `~/.codex`
  unless the user explicitly says otherwise.
<!-- agent-doctrine-rule:config.provider-separation -->
- Keep provider ownership separate. For Codex-only work, do not inspect or patch
  `~/.claude`. When the user explicitly asks for cross-provider diagnosis,
  parity, migration, or adoption, inspect both provider surfaces read-only as
  needed; write each provider only through its owning source/install pipeline.
<!-- agent-doctrine-rule:config.source-owned-doctrine -->
- Do not directly patch deployed user-level `~/.codex/AGENTS.md`. Durable
  doctrine changes are source-owned by the Agent-Doctrine repo and must flow
  through its source generation and install pipeline.
<!-- agent-doctrine-rule:config.no-provider-root-backups -->
- Do not create, keep, or install backup artifacts inside user-level provider
  roots such as `~/.codex` or `~/.claude`; move `.bak`, `.old`, timestamped, or
  rollback copies to a cache/backup path outside those roots.
