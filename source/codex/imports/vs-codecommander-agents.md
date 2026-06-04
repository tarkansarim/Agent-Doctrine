# Imported Codex Doctrine Source

- Source path: `<workspace root>/VS-CodeCommander/AGENTS.md`
- Source SHA256: `daeae32483bf202cce8bb76d987c693f9c4338735180c9e290d062ae2fe6a46c`
- Provider lane: `codex`

## Original Content

# VS-CodeCommander Agent Notes

Use [docs/agents/reload-safe-harness.md](docs/agents/reload-safe-harness.md) as the shared source of truth.

- Connect to the sidecar endpoint, not the extension bridge.
- Use `reload_window_and_wait` for any agent-initiated reload.
- Treat external Claude and Codex terminal agents as the continuity boundary; VS-CodeCommander only controls VS Code.
