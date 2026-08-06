<!-- agent-doctrine:claude:begin -->
# Claude User Rules

- Claude user configuration lives under `~/.claude` unless the user says otherwise.
- Keep Claude and Codex configuration separate. Inspect the other provider only when the user asks for cross-provider work, and write each provider only through its owning source.
- Never edit installed user rules or skills directly. Change the owning source, validate it, and install snapshots for both providers unless the user explicitly limits scope. Keep backups outside provider roots.
- Keep replies short, plain, and easy to scan. Put the result, blocker, or decision first, and explain only technical terms needed for accuracy.
- End status and final replies with one future-only `Next:` line. Use `Next: None; task complete.` when nothing remains.
- Only when designing agent-facing tools: preserve model judgment, automate stable repeated mechanics, use simple prompts, and add gates only for concrete irreversible, paid, safety, authority, scope, or integrity risks.
- Continue through clear implementation and verification steps. An explicit request to stay awake continues until completion, a real blocker, or a decision only the user can make.
- A `failed patch` is a code-change attempt that fails required validation or does not fix the reported behavior. After the first failed patch, commit that exact state as a diagnostic rollback anchor before making more repair edits. Further patch stacking is exploratory: use it to find and record the real fix. Once the fix is proven, preserve its required changes, restore the diagnostic anchor, apply only the proven fix cleanly, and rerun the exact validation. If the first patch itself proved wrong, return to the original pre-repair commit instead. Load `rewind-checkpoints` for the rollback procedure.
- When reading a skill for the current task, announce `Loading skill: <name>` once before relying on it.
- A repo's `discipline-profile` marker block in its `CLAUDE.md`/`AGENTS.md` is generated content owned by Enterprise-Discipline: never hand-edit inside the markers, and route changes through its enrollment tool. Its constraints override skill defaults for work in that repo; an un-enrolled or T0/T1 repo makes it inert. Load `discipline` for the procedure.

<!-- agent-doctrine:claude:end -->
