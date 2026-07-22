# Agent-Doctrine Behavior Evaluations

These BenchFlow tasks test fresh agents against generated user-level doctrine.
They complement structural pipeline tests; they do not replace them.

## Duplicate research

The `duplicate-research` task gives a supervisor a worker handoff with exact
source citations. A passing agent must verify the cited passages, avoid
repeating the worker's full investigation, and write the correct decision.

Run the same task for both providers from the repository root:

```bash
bench eval run \
  --tasks-dir behavior-evals/tasks \
  --include duplicate-research \
  --agent codex-acp \
  --model gpt-5.4 \
  --sandbox docker \
  --context-root "$PWD" \
  --jobs-dir /tmp/agent-doctrine-benchflow/codex

bench eval run \
  --tasks-dir behavior-evals/tasks \
  --include duplicate-research \
  --agent claude-agent-acp \
  --model sonnet \
  --reasoning-effort medium \
  --sandbox docker \
  --context-root "$PWD" \
  --jobs-dir /tmp/agent-doctrine-benchflow/claude
```

The task Dockerfile installs `generated/codex/AGENTS.md` and
`generated/claude/CLAUDE.md` into the corresponding `/home/agent` user-level
configuration paths. `--context-root` is therefore required.

BenchFlow 0.6.5's pinned `codex-acp` adapter selects the Codex effort through
the model option (`gpt-5.4[medium]`) and rejects a separate
`--reasoning-effort` argument. Claude's adapter accepts the explicit effort
argument shown above.
