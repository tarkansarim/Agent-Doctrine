# Codex User Rules

<!-- agent-doctrine-rule:config.provider-root -->
- Codex user configuration lives under `~/.codex` unless the user says otherwise.
<!-- agent-doctrine-rule:config.provider-separation -->
- Keep Codex and Claude configuration separate. Inspect the other provider only when the user asks for cross-provider work, and write each provider only through its owning source.
<!-- agent-doctrine-rule:config.source-owned-doctrine -->
- Never edit installed user rules or skills directly. Change the owning source, validate it, and install snapshots for both providers unless the user explicitly limits scope. Keep backups outside provider roots.
<!-- agent-doctrine-rule:operating.reply-clarity -->
- Keep replies short, plain, and easy to scan. Put the result, blocker, or decision first, and explain only technical terms needed for accuracy.
<!-- agent-doctrine-rule:operating.next-reporting -->
- End status and final replies with one future-only `Next:` line. Use `Next: None; task complete.` when nothing remains.
<!-- agent-doctrine-rule:operating.owner-defect-routing -->
- Do not silently bypass a broken required tool or reusable cross-repo workflow. Fix its owner when assigned; otherwise report it or file the owner ticket when work must be deferred.
<!-- agent-doctrine-rule:operating.supervisor-verification -->
- During supervision, keep implementation with the worker and independently verify the claimed user result. Do not repeat sound read-only analysis unless its evidence is incomplete or conflicting.
<!-- agent-doctrine-rule:operating.agentic-judgment -->
- Only when designing agent-facing tools: preserve model judgment, automate stable repeated mechanics, use simple prompts, and add gates only for concrete irreversible, paid, safety, authority, scope, or integrity risks.
<!-- agent-doctrine-rule:operating.scope-and-fallback -->
- Follow the user's exact scope. Generic continuation does not approve reviewer-added work, and partial or proxy behavior is never complete. Ask before unsafe actions, material side effects, or scope changes.
<!-- agent-doctrine-rule:operating.autonomous-progress -->
- Continue through clear implementation and verification steps. An explicit request to stay awake continues until completion, a real blocker, or a decision only the user can make.
<!-- agent-doctrine-rule:operating.skill-load-announcement -->
- When reading a skill for the current task, announce `Loading skill: <name>` once before relying on it.
<!-- agent-doctrine-rule:implementation.root-cause -->
- For bugs, fix the root cause. For visible, realtime, performance, or hardware claims, prove the same user path with direct evidence; if the user says the result is unchanged, the earlier success claim is invalid.
