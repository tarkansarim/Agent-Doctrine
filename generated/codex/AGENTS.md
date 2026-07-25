<!-- agent-doctrine:codex:begin -->
# Codex User Rules

- Codex user configuration lives under `~/.codex` unless the user says otherwise.
- Keep Codex and Claude configuration separate. Inspect the other provider only when the user asks for cross-provider work, and write each provider only through its owning source.
- Never edit installed user rules or skills directly. Change the owning source, validate it, and install snapshots for both providers unless the user explicitly limits scope. Keep backups outside provider roots.
- Keep replies short, plain, and easy to scan. Put the result, blocker, or decision first, and explain only technical terms needed for accuracy.
- End status and final replies with one future-only `Next:` line. Use `Next: None; task complete.` when nothing remains.
- Only when designing agent-facing tools: preserve model judgment, automate stable repeated mechanics, use simple prompts, and add gates only for concrete irreversible, paid, safety, authority, scope, or integrity risks.
- Continue through clear implementation and verification steps. An explicit request to stay awake continues until completion, a real blocker, or a decision only the user can make.
- When reading a skill for the current task, announce `Loading skill: <name>` once before relying on it.

<!-- agent-doctrine:codex:end -->
