# Imported Codex Doctrine Source

- Source path: `<workspace root>/CudaNurbsModeller/AGENTS.md`
- Source SHA256: `27cb88ca383640c158ed06d799a5d9ca9ca7fec37bafff78e14d760b32cc20c4`
- Provider lane: `codex`

## Original Content

# CudaNurbsModeller — Agentic Tool Reference

This project has full agentic access to all Sortie MCP tools. This file documents what's available and how to use each category. Keep this up to date as new tools are added.

## Build Tools (`mcp__sortie_build__*`)

| Tool | Purpose | Usage |
|------|---------|-------|
| `cmake_configure` | Run CMake configure step | Use when CMakeCache.txt is missing or CMakeLists.txt changed |
| `cmake_build` | Build the project | Standard build. Equivalent to `cmake --build build -j$(nproc)` |
| `cmake_run` | Build and run the executable | Builds then launches `./build/cudanurbsmodeller` |
| `cuda_run_pipeline` | Full CUDA build+run pipeline | Configure, build, run with CUDA env setup |
| `cuda_tool_pipeline` | Run CUDA tools (sanitizer, profiler) | For compute-sanitizer, Nsight debugging |
| `gui_run_scenario` | Launch app and capture frame | Visual verification — use `scenarioId: "default"` for this single-target GUI project |
| `compile_gate` | Check if project compiles cleanly | Quick compile check without running |
| `build_and_measure` | Build and collect metrics | Build + measure FPS, memory, etc. |
| `metric_collect` | Collect runtime metrics | FPS, frame time, GPU memory |
| `metric_compare` | Compare metrics across runs | Before/after comparison |
| `metric_get_history` | Get metric history | Trend analysis |
| `test_run` / `test_list` / `test_get_history` | Test management | Run `nurbs_math_validation_test` |

### Quick Reference
```bash
# Manual build
./run.sh build

# Build + run
./run.sh

# Clean rebuild
./run.sh clean

# CMake build dir: ./build
# Executable: ./build/cudanurbsmodeller
# Build type: Debug (default), set BUILD_TYPE=Release for release
```

## Graph Tools (`mcp__sortie_graph__*`)

The node graph tracks project structure and implementation progress.

| Tool | Purpose |
|------|---------|
| `graph_get_structure` | Compact graph summary (use `verbose:true` for full tree) |
| `graph_add_node` / `graph_delete_node` | Add/remove nodes |
| `graph_set_description` / `graph_get_description` | Node descriptions |
| `graph_set_plan` / `graph_get_plan` | Implementation plans per leaf |
| `graph_get_leaf_plan` | Get full leaf briefing for worker dispatch |
| `graph_prepare_research_brief` | Create research brief for a leaf |
| `graph_finalize_research_brief` | Finalize research after worker completes |
| `graph_finalize_worker_leaves` | Mark leaves complete after worker review |
| `graph_set_path` / `graph_bulk_set_path` | Set primary file path for nodes |
| `graph_set_stub` / `graph_bulk_set_stub` | Mark nodes as stub/implemented |

### Current Graph Structure (7 subsystems, 29 leaves, all complete)
- Scaffold & Infrastructure (CMake, Borrowed Utils, App Skeleton)
- NURBS Data Model (Types, CPU Math, Primitives, Validation Tests)
- GPU Tessellation (GPU Upload, Eval Kernel, CUDA-Vulkan Interop)
- Surface Rendering (Shaders, Wireframe, CV Points, Display Modes)
- CV Editing (Pick/Select, Drag/Transform, Undo, Insert Isoparms, CV Hardness)
- Primitive Creation UI (Scene Manager, Creation Panel)
- Selection & Manipulation (Object/Multi-Component Select, Gizmo, Translate/Rotate/Scale, Axis Constraints, Numeric Input)

## Worker Tools (`mcp__sortie__*`)

| Tool | Purpose |
|------|---------|
| `spawn_worker` | Dispatch a coding/research worker. Requires `nodeName` matching a graph node. |
| `spawn_research_worker` | Dispatch a research-only worker |
| `list_workers` | List all workers. Use `waitForCompletion: true, timeoutSeconds: 120` to poll. |
| `worker_status` | Get detailed status of one worker |
| `worker_get_activity` | Get worker activity log. Use `sinceTimestamp` for incremental. |
| `worker_send_message` | Send course-correction message to running worker |
| `worker_get_output` | Get worker output after completion |
| `worker_get_research_result` | Get research worker result |
| `terminate_worker` | Kill a running worker |

### Worker Dispatch Pattern
```
1. spawn_worker({ task: "...", nodeName: "Leaf Name", cudaMode: true })
2. list_workers({ waitForCompletion: true, timeoutSeconds: 120 })
3. worker_status({ workerId: "..." })
4. Review result, finalize if needed
```

## Knowledge Tools (`mcp__sortie_knowledge__*`)

| Tool | Purpose |
|------|---------|
| `architecture_recommend*` | Get architecture recommendations |
| `capability_card_*` | Track what the system can do |
| `context_packet_*` | Reusable context bundles |
| `learning_cycle_*` | Track learning progress |
| `playbook_*` | Reusable procedure playbooks |
| `scenario_*` | Testing/verification scenarios |
| `session_affinity_*` | Worker session continuity |
| `template_*` | Reusable templates |

## Observation Tools (`mcp__sortie_observe__*`)

| Tool | Purpose |
|------|---------|
| `visual_capture` / `visual_compare` | Screenshot capture and comparison |
| `aar_*` | After-action review recording |
| `pattern_*` | Pattern extraction and retrieval |
| `perf_budget_*` | Performance budget tracking |
| `recording_*` | Session recording |
| `verification_*` | Verification state tracking |

## Agent Tools (`mcp__sortie_agent__*`)

| Tool | Purpose |
|------|---------|
| `skill_list` / `skill_get_content` / `skill_create` / `skill_edit` | Skill management |
| `adjutant_*` | Adjutant intelligence (assess, blind spots, cross-project patterns) |
| `agent_*` | Agent loadout management |
| `hook_*` | Git/build hook management |
| `plugin_*` / `registry_*` | Plugin management |
| `scan_project` | Scan project structure |

## Workflow Tools (`mcp__sortie__workflow_*`)

Workflow pipeline is **disabled by default** for this project. Only use when the user explicitly asks for the workflow engine (Auditor -> Fix Planner -> Implementer pipeline).

## Relevant User-Level Skills

These skills are loaded automatically when their domain is triggered:

| Skill | When to load |
|-------|-------------|
| `graph-conventions` | Graph decomposition, node structure |
| `cpp-cuda-project-layout` | Project structure, file naming |
| `cpp-cuda-research-to-plan` | Pre-implementation research |
| `cuda-debug` / `cuda-profiling-and-debugging` | GPU debugging |
| `sortie-mcp-usage` | MCP call sequences |
| `manual-subagent-supervision` | Worker coordination |
| `parallel-lens-escalation` | Stuck problems needing multiple investigation angles |
| `systematic-debugging` | Bug investigation |

## Project-Specific Notes

- **CUDA mode**: Always pass `cudaMode: true` when spawning workers
- **Single GUI target**: Use `gui_run_scenario({ scenarioId: "default" })` for visual checks
- **Operator tier**: User typically operates in Operator tier (direct builds allowed)
- **Maya-style viewport**: Alt+LMB orbit, Alt+MMB pan, Alt+RMB zoom
- **Default mode**: Object mode (F5). F6 for Component, F8 cycles CV/Hull/Isoparm
