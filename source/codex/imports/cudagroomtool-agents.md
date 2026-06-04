# Imported Codex Doctrine Source

- Source path: `<workspace root>/CudaGroomTool/AGENTS.md`
- Source SHA256: `3c19a2f7cbae02694ef4b4e0cec8e34e634970a80177f60b5758c9395399086d`
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
- Automated offscreen/background test launches must select an idle GPU first:
  - query `nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits`
  - query `nvidia-smi pmon -c 1`
  - subtract display-server load (`Xorg`, `Xwayland`) from the aggregate GPU utilization
  - treat a GPU as idle only when the effective post-subtraction utilization is `<= 5%`
  - choose the lowest-index idle GPU
  - if none are idle, wait 30 seconds and retry until one is available
  - explicit `CUDAGROOM_RT_TEST_GPU_ID` or intentionally fixed `--gpu-id <n>` values stay
    authoritative

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

## Close-Out Reporting

- When reporting a kept or verified runtime/performance win, the final sentence of the reply must
  contain the current authoritative win metrics from the exact lane that was used to justify the
  win.
- For app/runtime work, final replies must also include one ready-to-run live GUI command for
  convenience, even when the authoritative verification used `ostm` or another offscreen path.
- Do not print a live GUI command from memory. Before handing one to the user, verify the exact
  executable and flags from the current binary (`--help` or parser source) and run the same launch
  shape through `ostm` with `--startup-only` or `--smoke-test` when feasible.
- Prefer the repo-local launcher script `./launch_live_spheregroom.sh` for the default live demo
  lane instead of retyping long raw commands. If a raw command is unavoidable, keep it on one
  physical line and validate that no flag or path is split.
- If no authoritative win was proven, say that plainly instead of ending with speculative metrics.

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
