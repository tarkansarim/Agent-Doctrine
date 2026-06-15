# Imported Codex Doctrine Source

- Source path: `<workspace root>/Self-Improvement/AGENTS.md`
- Source SHA256: `6f733ffe0712b006c49cb181f6e124696982ab616492d7c2f149c73682c83507`
- Provider lane: `codex`

## Original Content

# Self-Improvement Project Rules

## Legacy Replacement Rule

When replacing a user-level self-improvement mechanism, do not leave the old mechanism available in parallel. Remove legacy active installs, legacy runtime roots, and old self-improving backup copies unless the user explicitly asks to retain an archive.

For this repo, the current mechanism is:

- `bin/agent-self-improve`
- `skills/self-improving/SKILL.md`
- user-level installs at `~/.codex/skills/self-improving/SKILL.md` and `~/.claude/skills/self-improving/SKILL.md`
- provider runtime roots at `~/self-improving-codex` and `~/self-improving-claude`

Do not reintroduce the previous multi-file passive memory skill as an active user-level install.

## Doctrine Patch Rule

When a self-improvement lesson should change future agent behavior, do not leave it only in runtime records. Use `agent-self-improve record --doctrine-target repo_agents --doctrine-target repo_skill --repo <repo path> ...` only for repo-owned doctrine. Provider-level Codex `AGENTS.md`, Claude `CLAUDE.md`, autonomous steering, and installed self-improving skill snapshots are Agent-Doctrine owned; record evidence locally, patch `<workspace root>/Agent-Doctrine` source modules, regenerate, validate, snapshot-install, then close with `--updated-artifact`. Failed, non-final, dry-run, or provider-target records must not mutate deployed provider doctrine directly.

Manual doctrine-patch closure through `--updated-artifact` must reference an existing doctrine artifact that contains the exact item id or exact lesson text. If record commit fails after doctrine is written, the mechanism must roll back both doctrine and runtime commit artifacts instead of leaving false records.

Review packets must use `agent-self-improve review-add --fresh-context-review`; forked, reused, or inherited implementation-context reviewers are invalid review sources.

Before marking a ticket or reply as Done for reusable agent-behavior work that changes installed CLIs, installed skills, hooks, provider doctrine, or user-level behavior, run `agent-self-improve closeout-gate --provider <provider> --ticket <id> --agent-behavior-change --source-validation "<command/evidence>" --installed-verification "<command/evidence>"`. If rollout is not complete, use `--intended-state pending --remaining "<missing rollout item>"` and do not mark the ticket Done.

When a closeout or status says self-improvement happened, name and verify the landing surface: runtime record id, repo doctrine target, provider-doctrine route, or code-only verifier/tool hardening. Do not call code hardening a self-improvement record unless `agent-self-improve` actually recorded it.

<!-- agent-self-improvement-doctrine:begin -->
## Accepted Self-Improvement Doctrine

- 2026-05-09T03:27:49Z [global] Self-improvement lessons that should steer future behavior must patch durable doctrine with agent-self-improve record --doctrine-target, not only write runtime queue records. (source: self-improvement:user_correction:9d1c0c4c1a6d4c23)
- 2026-05-09T03:32:11Z [global] Accepted self-improvement lessons that should steer future behavior must patch durable doctrine with agent-self-improve record --doctrine-target, including installed and source skill files when the lesson changes the mechanism. (source: self-improvement:user_correction:bcf7ef0a92c0330f)
- 2026-05-09T03:42:51Z [global] When extracting or replacing an agent self-improvement mechanism, verify and preserve the source mechanism's active write surfaces such as AGENTS.md, CLAUDE.md, and skill updates; do not claim parity from a passive queue or audit log alone. (source: self-improvement:user_correction:581fccffb9622a59)
- 2026-05-09T04:00:46Z [global] For this user-level self-improvement mechanism, runtime records are only queue/audit evidence; successful self-improvement means updating durable behavior files such as AGENTS.md, CLAUDE.md, or self-improving skills when a lesson should change future agent behavior. (source: self-improvement:user_correction:bc4c1c8ab5832a3e)
- 2026-05-09T04:31:14Z [global] Doctrine mutation commands must validate the exact open item id, resolution, evidence refs, target files, and dry-run mode before writing AGENTS.md, CLAUDE.md, or self-improving skill files; failed or dry-run records must not mutate durable doctrine. (source: self-improvement:user_correction:b9232aaf6789f211)
- 2026-05-09T05:17:42Z [global] When running code-review or adversarial-review subagents for this user, use a fresh-context reviewer: spawn a new agent without fork_context and do not reuse a previous reviewer thread or a reviewer that inherited the implementation conversation. (source: self-improvement:user_correction:713201d3297f5870)
- 2026-05-09T05:53:42Z [global] Review packets must use agent-self-improve review-add --fresh-context-review; forked, reused, or inherited implementation-context reviewers are invalid review sources. (source: self-improvement:user_correction:02f1c2ae9de7057a)
- 2026-05-09T07:07:38Z [global] Public self-improvement discovery, docs, rule headings, CLI help, and generated item IDs must use application-neutral terminology rather than source-project layer labels. (source: self-improvement:user_correction:01e7b60200d25332)
- 2026-05-09T18:58:31Z [global] When closing self-improvement review findings, verify installed provider-label conversion, exact per-target doctrine dedupe, and normalized migration/error output; do not treat clean success paths as sufficient. (source: self-improvement:audit_gap:dd602cc58d09d4dc)
- 2026-05-09T19:09:12Z [global] Self-improvement verification for public migration paths must cover exact manual doctrine artifact matching, argparse parse-error output, and read-only agenda/status behavior, not only successful command output. (source: self-improvement:audit_gap:57496bde6bcb79bf)
- 2026-05-28T10:20:52Z [global] Self-improvement skill and installed steering must explicitly trigger for non-trivial work, corrections, repeated misses, verification gaps, tool failures, and reusable behavior friction. (source: self-improvement:user_correction:716a2d72e86f2ea6)
- 2026-06-01T00:00:00Z [global] Provider-level self-improvement doctrine changes must route through Agent-Doctrine source generation, validation, and snapshot install; agent-self-improve must not directly patch deployed Codex AGENTS.md, Claude CLAUDE.md, autonomous steering, or installed skill snapshots. (source: PLANE-157)
- 2026-06-01T00:51:32Z [global] Ticket closeout for reusable agent behavior must verify installed/rolled-out artifacts, not only source tests, before marking Done; if rollout is pending, the reply and ticket state must say exactly what remains. (source: self-improvement:user_correction:a77a868d116f7cb3)
- 2026-06-12T08:24:52Z [global] Self-improvement closeouts must name and verify the landing surface before claiming self-improvement happened: runtime record id, repo doctrine target, provider-doctrine route, or code-only verifier/tool hardening; code hardening is not an agent-self-improve record unless the runtime mechanism recorded it. (source: self-improvement:user_correction:f37bdbd8f49ad358)
<!-- agent-self-improvement-doctrine:end -->
