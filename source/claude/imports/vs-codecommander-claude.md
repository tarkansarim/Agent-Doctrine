# Imported Claude Doctrine Source

- Source path: `<workspace root>/VS-CodeCommander/CLAUDE.md`
- Source SHA256: `38a10aa80688144849f637034bbacac0896a4a17157794949a55f721db01f471`
- Provider lane: `claude`

## Original Content

# VS-CodeCommander Claude Notes

Use [docs/agents/reload-safe-harness.md](docs/agents/reload-safe-harness.md) as the shared source of truth.

- Connect Claude Code to the sidecar endpoint, not the extension bridge.
- Use `reload_window_and_wait` for any agent-initiated reload.
- Treat Claude as an external terminal-side controller; VS-CodeCommander only waits for VS Code to come back.
