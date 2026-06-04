# Imported Claude Doctrine Source

- Source path: `<workspace root>/wetbrush_lin/CLAUDE.md`
- Source SHA256: `ad1d800ec05224372ad42b6de92f72f20a5be3bfa653faa93577124ddf3ada1c`
- Provider lane: `claude`

## Original Content

<claude-mem-context>

## Linux Scenario Execution

- Automated scenario playback on Linux must use playback mode, not record mode.
- Canonical Linux playback entrypoint: `scripts/gui/run_scenario_linux.sh`
- Canonical Linux recording entrypoint: `scripts/gui/record_scenario_linux.sh`
- Automated Linux scenario playback defaults to a visible non-blocking background window via `--background-window`.
- Exact replay / screenshot-oracle scenario validations must explicitly use `--hidden-window`.
- True offscreen EGL playback is explicit-only and not the default fidelity path for scenario correctness.
- Automated Linux scenario playback must select an idle GPU with `utilization.gpu < 5` from `nvidia-smi` before startup.
- Linux `--background-window` and `--hidden-window` playback must require an idle display-active GPU after subtracting only `Xorg` / `Xwayland` display-server SM load from the raw utilization sample; do not subtract other app load.
- Explicit offscreen EGL playback may use any idle GPU with a matching EGL device.
- Automated playback reports must preserve both the selected idle GPU and the actual CUDA/GL interop GPU used by the run; if they differ, report the mismatch instead of silently hiding it.
- If no eligible GPU is idle for automated playback, wait `30` seconds and retry until one is available.
- Only one Linux scenario playback or recording job may run at a time. The binary must serialize Linux scenario execution before any GLFW/EGL/GL context is created.
- Visible foreground scenario playback is debug-only and must be explicitly requested.
- `--record-scenario` remains visible and interactive by design.

</claude-mem-context>
