# Imported Codex Doctrine Source

- Source path: `<workspace root>/CudaGroomTool2/AGENTS.md`
- Source SHA256: `a0a3b3d9c75847bb99e3c261b5f77f16cb99e0c38132aaace0ca165dc974042f`
- Provider lane: `codex`

## Original Content

# Project Agent Notes

Repo-level Claude rules now live in [`CLAUDE.md`](CLAUDE.md). Read that file first for the
offscreen/background automation contract.

Critical mirror of the offscreen policy:

- When the `offscreen-test-manager` skill applies, agents must route all windowed/GUI/offscreen
  execution through `ostm submit`; they must not launch those binaries directly.
- Use `ostm submit --mode background` for visible non-blocking visual debugging and
  `ostm submit --mode offscreen` for fully hidden correctness/oracle runs.
- `ostm` owns the offscreen/background windowing behavior now. Do not pass app-level
  `--background-window` or `--hidden-window` flags for automation.
- Automated offscreen/background app tests must not obscure the user's current work.
- Fidelity-sensitive RT checks must prefer the hidden live path, not `vulkan-offscreen`, unless the
  test is explicitly exercising the offscreen backend.
- Background replay, recording, screenshot, and UI verification launches now default to
  `ostm submit --mode background`, not app-owned window flags.
- Exact replay / screenshot-oracle validations should use `ostm submit --mode offscreen` when they
  require deterministic pixel dimensions.
- OSTM UI/windowed SonicGroom runs used as evidence must launch a maximized window and must prove
  maximized/full-size state through `--ui-state-json` window fields before the evidence is accepted.
- Non-maximized OSTM UI/windowed SonicGroom runs must be discarded and must not be used for
  profiling, screenshot, UI, or fix proof.
- Automated offscreen/background test launches must select an idle GPU first:
  - query `nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits`
  - query `nvidia-smi pmon -c 1`
  - subtract display-server load (`Xorg`, `Xwayland`) from the aggregate GPU utilization
  - treat a GPU as idle only when the effective post-subtraction utilization is `<= 5%`
  - choose the lowest-index idle GPU
  - if none are idle, wait 30 seconds and retry until one is available
  - explicit `SONICGROOM_RT_TEST_GPU_ID` or intentionally fixed `--gpu-id <n>` values stay
    authoritative
- On this workstation, realtime 3D/live Vulkan/Qt/OSTM replay/render validation for SonicGroom
  must use GPU 1. Set `SONICGROOM_GPU_ID=1` and `SONICGROOM_RT_TEST_GPU_ID=1`; do not use GPU 0
  for realtime 3D validation just because it appears idle.

## Qt UI Boundary

- The active product UI in this repo is the Qt shell/native Vulkan viewport, not Dear ImGui.
- Do not describe Qt panels, menus, sliders, launchers, recordings, live validation, or viewport UI
  work as `imgui`/`ImGui`.
- Do not use ImGui assumptions when planning, implementing, or verifying UI behavior in this repo.
- Do not launch legacy ImGui/native Groom binaries or broad portability tests during Qt UI,
  Qt viewport, Qt recording replay, or Qt performance work unless the explicit purpose is to
  compare legacy ImGui behavior against Qt behavior. If that comparison is intentional, state it
  before launch and route the run through `ostm` so it cannot obscure the user's desktop.
- If legacy files, comments, or history mention ImGui, treat that as historical context only; verify
  the active Qt path before using it as implementation guidance.
- For UI work, start from the Qt shell, app lifecycle, runtime-state, and Vulkan viewport paths unless
  the user explicitly asks for legacy ImGui code.

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

## Nsight Systems Stats Readback

- This workstation's `nsys` is Nsight Systems 2025.3.2 through `nsys on PATH`.
- Do not use legacy `nsys stats --report summary --format text ...`; this install does not support
  `summary` reports or `text` format.
- Do not add wrappers, aliases, or PATH shims to make legacy `summary/text` commands pass. Replace
  stale commands with explicit supported reports.
- For Vulkan/live RT captures, read stats with:
  - `nsys stats --force-export=true --report vulkan_api_sum,osrt_sum,nvtx_sum --format column <report.nsys-rep>`
- For CUDA-heavy captures, read stats with:
  - `nsys stats --force-export=true --report cuda_api_gpu_sum,cuda_gpu_kern_sum,osrt_sum,nvtx_sum --format column <report.nsys-rep>`
- If the capture lacks NVTX or CUDA data and those reports are skipped, do not treat that as an
  `nsys` failure when the relevant Vulkan/OS or CUDA reports process successfully.
- Before inventing a new stats command, run `nsys stats --help` and `nsys stats --help-reports`.

## Close-Out Reporting

- When reporting a kept or verified runtime/performance win, the final sentence of the reply must
  contain the current authoritative win metrics from the exact lane that was used to justify the
  win.
- For app/runtime work, final replies must also include one ready-to-run live GUI command for
  convenience, even when the authoritative verification used `ostm` or another offscreen path.
- Do not print a live GUI command from memory. Before handing one to the user, verify the exact
  executable and flags from the current binary (`--help` or parser source) and run the same launch
  shape through `ostm` with `--startup-only` or `--smoke-test` when feasible.
- Prefer the repo-local Qt launcher script `./launch_live_sonicgroom_qt.sh` for the default live
  demo lane instead of retyping long raw commands. Use `./launch_live_sonicgroom.sh` or
  `./launch_live_spheregroom.sh` only when the user explicitly asks for the legacy app path. If a
  raw command is unavoidable, keep it on one physical line and validate that no flag or path is
  split.
- If no authoritative win was proven, say that plainly instead of ending with speculative metrics.

## Commit Origin Labels

- Every commit made by an agent must include final commit-message trailers identifying why the
  commit was created and a short human-readable description of the change:
  - `Commit-Origin: user-requested` when the user explicitly asks the agent to commit.
  - `Commit-Origin: agent-initiated` when the agent creates its own checkpoint, rollback anchor, or
    other autonomous commit.
  - `Commit-Description: <brief description>` with one concise phrase or sentence describing what
    that commit changed.
- Keep the trailer spellings exact so the user can later ask to roll back to user-requested commits,
  agent-initiated commits, or identify the purpose of a commit unambiguously.
- Commit verified completed slices automatically without asking for separate commit permission,
  unless the user explicitly says not to commit, verification is incomplete, the diff is destructive,
  or a real blocker remains unresolved.

## Debug Memory Protocol

- Before starting a new attempt in a subsystem with prior failed probes, read [`docs/ENGINEERING_MEMORY.md`](docs/ENGINEERING_MEMORY.md) and [`docs/FAILED_PROBES_LEDGER.md`](docs/FAILED_PROBES_LEDGER.md).
- After any unsuccessful attempt, discarded probe, or rollback, append a new entry to [`docs/FAILED_PROBES_LEDGER.md`](docs/FAILED_PROBES_LEDGER.md) in the same work session.
- Update [`docs/ENGINEERING_MEMORY.md`](docs/ENGINEERING_MEMORY.md) only with lessons still believed true after rollback.
- Do not retry a previously failed subsystem path until the prior failure mode and lesson are written down.

## Adversarial Review Requests

- When preparing material for an adversarial review, present it as a concrete implementation plan, not as a leading prompt.
- Use a short numbered plan that states what will be audited, what will be changed, what will be kept fixed, and how success will be verified.
- Do not ask the reviewer a directional question or bias the review toward a preferred answer.
- Do not pad the handoff with extra argumentation, theories, or desired conclusions beyond the minimal factual context needed to understand the plan.
- The goal of the handoff is to let the reviewer attack the plan for correctness, not to steer it toward agreement.
- If the user asks whether an adversarial review is needed, answer directly in the same message:
  - if the answer is `no`, say so briefly
  - if the answer is `yes`, immediately provide the exact adversarial-review handoff without waiting
    for another confirmation turn

<!-- agent-self-improvement-doctrine:begin -->
## Accepted Self-Improvement Doctrine

- 2026-05-09T22:56:51Z [global] For Qt shell brush parity, validate no-click startup state before explicit control exercise; Comb/Screen defaults to Screen influence and Screen+Local remains explicitly selectable. (source: self-improvement:user_correction:94153b875de3bfdd)
<!-- agent-self-improvement-doctrine:end -->
