# Imported Codex Doctrine Source

- Source path: `<workspace root>/human-domain-visualizer/AGENTS.md`
- Source SHA256: `fa548242e5b59961a77e8d1abe0e37bcd78af896402948d6743ffbb86c7057a2`
- Provider lane: `codex`

## Original Content

# AGENTS Instructions — human-domain-visualizer

Apply the root `CLAUDE.md` in full. This file is the Codex / Sortie compatibility surface and only adds repo-specific build/run/test commands and tool surface notes.

## Repo-specific overrides

(none for v0)

## Build commands

```
pnpm install                                            # install JS deps
pnpm tauri dev                                          # development window with HMR
pnpm tauri build                                        # production build
cargo check --manifest-path src-tauri/Cargo.toml        # Rust syntax/type check
pnpm tsc --noEmit                                       # TypeScript check
```

## Test commands

```
cargo test --manifest-path src-tauri/Cargo.toml         # all Rust unit + integration tests
# v0 does not yet have a frontend test suite.
```

## Verify-before-commit checklist

Before any commit (including the M8 first commit), run all four:

```
cargo check --manifest-path src-tauri/Cargo.toml
cargo test --manifest-path src-tauri/Cargo.toml
pnpm tsc --noEmit
pnpm tauri dev    # quick smoke that the window still launches
```

Stage specific files; never `git add .` or `git add -A`.

## Tool surface

v0 does not expose MCP tools or external integrations. Activity-feed adapters (for Sortie events, Claude Code hooks, etc.) arrive in v2+.

## Project memory

See `CLAUDE.md` § Project memory.

## Rewind

See `CLAUDE.md` § Rewind discipline.
