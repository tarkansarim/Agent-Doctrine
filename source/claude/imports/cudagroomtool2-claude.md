# Imported Claude Doctrine Source

- Source path: `<workspace root>/CudaGroomTool2/CLAUDE.md`
- Source SHA256: `961a725a0014993b2ff3479d1cd678ab9a87d2e0061444ad73a8725173bb4d17`
- Provider lane: `claude`

## Original Content

# Repo-Level Claude Rules

This repository uses this file as the source of truth for offscreen/background automation policy.
`AGENTS.md` mirrors only the critical subset needed by other toolchains.

## Offscreen / Background Automation

- Agents must route all windowed, GUI, replay, recording, screenshot, and visual test execution
  through the `ostm` offscreen test manager CLI. Do not launch those binaries directly.
- Use `ostm submit --mode background` when you need to see the live window without blocking the
  desktop.
- Use `ostm submit --mode offscreen` for fully hidden correctness/oracle runs.
- `ostm` now owns the background/offscreen windowing behavior. Do not pass app-level
  `--background-window` or `--hidden-window` flags for automation; those removed app-owned modes
  are removed.
- Automated offscreen or background app tests must not obscure the user's current work.
- For fidelity-sensitive RT checks, use the normal live app/render path rather than treating
  `vulkan-offscreen` as the default correctness path.
- Do not treat `vulkan-offscreen` as the default correctness path for live RT replay, recording, or
  scene/source switching. Use it only when a test is explicitly exercising the offscreen backend.
- Background replay, recording, screenshot, and UI verification launches must default to
  `ostm submit --mode background`, not a visible foreground launch.
- Do not launch a visible foreground replay or recording verification window unless the user
  explicitly asks for that.

## GPU Selection For Offscreen Tests

- Automated offscreen/background test launches must check current GPU load before choosing a device.
- Query GPU load with:
  - `nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits`
- Also query per-process graphics load with:
  - `nvidia-smi pmon -c 1`
- Subtract display-server load (`Xorg`, `Xwayland`) from the aggregate GPU utilization before
  applying the idle threshold.
- Treat a GPU as idle only when the effective post-subtraction utilization is `<= 5%`.
- Choose the lowest-index idle GPU.
- If no GPU is idle, wait 30 seconds and try again. Repeat until an idle GPU is available.
- If `nvidia-smi` is unavailable or its output cannot be parsed, fail clearly. Do not silently guess.
- Explicit test overrides remain authoritative:
  - `SONICGROOM_RT_TEST_GPU_ID`
  - intentionally fixed `--gpu-id <n>` values inside a specific test

## Background Window Modes

- `ostm submit --mode background` is the default non-blocking visible launch shape:
  - run the normal live app/window/render path on the real display
  - keep the window below normal desktop windows
  - keep it click-through / non-focus-stealing
  - keep it out of the taskbar / pager
- `ostm submit --mode offscreen` is the fully hidden correctness/oracle mode.
- Exact replay or screenshot-oracle validations that require deterministic pixel dimensions should
  prefer `ostm submit --mode offscreen` around the normal live app path rather than relying on
  app-owned hidden-window flags.

## Profiling Confirmation

- Before handing an RT, brush-interaction, replay, or performance-sensitive fix to the user, run a
  fresh Nsight/`nsys` profile after the final code change.
- The profile must use the exact repro or oracle command for the lane being claimed fixed. Do not
  substitute a different scene, preset, recording, startup-only run, or synthetic harness and treat
  it as equivalent proof.
- When handing off those fixes, include the exact live demo command alongside any replay, oracle, or
  profiling command by default so the user always has the real interactive lane to launch.
- Do not treat functional tests or screenshot oracles alone as sufficient proof for those fixes.
- If a more specific Nsight tool is clearly required, use it, but `nsys` is the default first
  profiling check before handoff.

## Nsight Systems Stats Readback

- This workstation's `nsys` is Nsight Systems 2025.3.2 through `nsys on PATH`.
- Do not use legacy `nsys stats --report summary --format text ...`; this install does not support
  `summary` reports or `text` format.
- Do not add wrappers, aliases, or PATH shims to make legacy `summary/text` commands pass. Replace
  stale commands with explicit supported reports.
- For Vulkan/live RT captures, read stats with:

```bash
nsys stats --force-export=true --report vulkan_api_sum,osrt_sum,nvtx_sum --format column <report.nsys-rep>
```

- For CUDA-heavy captures, read stats with:

```bash
nsys stats --force-export=true --report cuda_api_gpu_sum,cuda_gpu_kern_sum,osrt_sum,nvtx_sum --format column <report.nsys-rep>
```

- If the capture lacks NVTX or CUDA data and those reports are skipped, do not treat that as an
  `nsys` failure when the relevant Vulkan/OS or CUDA reports process successfully.
- Before inventing a new stats command, run `nsys stats --help` and `nsys stats --help-reports`.

## Verification Handoff Discipline

- Do not stop debugging, ask for subjective confirmation, or hand a fix candidate back to the user
  as if it is plausibly solved unless the exact claimed lane has a fresh direct oracle or measured
  A/B evidence from the same repro.
- Build success, unrelated tests, replay completion, or profiler output alone are not sufficient
  proof of a user-visible behavioral fix unless they directly measure that behavior.
- If the exact user-visible behavior is not yet directly verified, say so explicitly and keep the
  status honest: hypothesis only, confirmation pending.
- Before pausing on a live brush-feel or visual-behavior bug, state the exact proof status:
  - what direct oracle was run
  - what it did and did not prove
  - whether user confirmation is still pending
- Treat this as a compaction-safe standing rule, not a per-turn preference.

## Rollback And Probe Discipline

- Before touching a live bug, RT bug, brush-interaction bug, replay bug, or performance-sensitive
  subsystem, create or confirm a rollback commit/checkpoint first.
- Keep only one active code probe at a time. Do not stack a new fix attempt on top of an
  unverified or regressing probe.
- If an attempt regresses the exact live demo lane or the exact replay/oracle lane, write the
  lesson down, revert to the rollback anchor immediately, rebuild, and continue from the clean
  state.
- Never build from a mixed dirty tree and treat that binary as proof of the rollback anchor or
  proof of a fix.
- Keep the current truth block explicit during debugging:
  - current `HEAD`
  - exact live demo command
  - exact replay/oracle command
  - whether the current binary was rebuilt from that exact tree
- After two failed code attempts on the same bug, stop patching and switch to a deeper audit/plan
  before editing more code.
