# Imported Claude Doctrine Source

- Source path: `<workspace root>/ComfyNative/CLAUDE.md`
- Source SHA256: `a43d0a3ad4b37adc0be5e00ec893cded75375bf66115c7a9a06e6dcb5b53055b`
- Provider lane: `claude`

## Original Content

# ComfyNative - Claude Code Reference

## Project Overview

ComfyNative is a standalone C++20/CUDA library and CLI that executes ComfyUI JSON workflows natively, eliminating Python dispatch overhead. The primary target workflow is a Qwen Image Edit pipeline (17 nodes) that runs ~60-120 seconds in Python ComfyUI; the goal is sub-5-second execution.

The project has two deployment surfaces:
- **comfynative** - static library (`libcomfynative.a` / `comfynative.lib`)
- **comfynative-cli** - single executable with five subcommands: `parse`, `compile`, `run`, `generate`, `info`

A sister project, **ComfyCompiled**, lives at `~/Documents/AI/ComfyUI_V81/ComfyUI/custom_nodes/ComfyCompiled` and wraps ComfyNative via pybind11 for use as a ComfyUI custom-node plugin. Changes to ComfyNative headers or the static library ABI affect that project.

Backend tensor library: **stable-diffusion.cpp** (GGML), pulled in as a CMake subdirectory from the sibling workspace `../comfy-native-workspace`.

---

## Hardware Target

- 2x NVIDIA RTX Pro 6000 Ada (sm_89, 96 GB VRAM each, 192 GB total)
- CUDA 12.x
- Ubuntu Linux (current dev environment)

---

## Execution Phases

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | Complete | Parser/executor infrastructure; all 15 node types as working stubs |
| Phase 2 | Active | Replace stubs with real implementations via stable-diffusion.cpp APIs |
| Phase 3 | Future | CUDA Graph AOT compilation, multi-GPU |

**Phase 2 constraint**: All work must remain compatible with sequential single-stream CUDA execution. Do not introduce CUDA Graph design decisions in Phase 2.

---

## Repository Layout

```
ComfyNative/
├── CMakeLists.txt              # Build root (C++20, CUDA, FetchContent)
├── include/comfynative/
│   ├── core/
│   │   ├── binary_format.h
│   │   ├── cfg_guider.h         # CFGGuider (ComfyUI parity)
│   │   ├── comfy_types.h
│   │   ├── conditioning_ops.h
│   │   ├── conditioning_pipeline.h
│   │   ├── conditioning_types.h  # CondTensor, CondEntry, CondObject, Device
│   │   ├── data_types.h          # ImageData, LatentData, VAEHandle, ModelHandle
│   │   ├── ggml_base_model.h
│   │   ├── image_io.h
│   │   ├── image_resize.h
│   │   ├── latent_noise.h        # RNGEngine, prepare_noise, fix_empty_latent_channels
│   │   ├── model_detection.h     # SafetensorsReader, GGUFReader, ModelDetector
│   │   ├── model_manager.h       # ModelManager singleton
│   │   ├── model_sampling.h      # ModelSampling (sigma tables)
│   │   ├── qwen_text_encoder.h
│   │   ├── samplers.h            # euler, euler_ancestral, heun
│   │   ├── scheduler.h           # 9 scheduler implementations
│   │   ├── tensor.h
│   │   └── torch_math.h
│   ├── graph/
│   │   ├── graph_executor.h      # GraphContext, GraphExecutor
│   │   ├── workflow_compiler.h   # WorkflowCompiler, CompiledWorkflow
│   │   └── workflow_parser.h     # WorkflowParser, Workflow, Node structs
│   └── nodes/
│       ├── all_nodes.h           # Declarations for all 15 node classes
│       ├── base_node.h           # Node base class, NodeRegistry, REGISTER_NODE macro
│       ├── init_nodes.h
│       └── node_registry.h
├── src/
│   ├── core/                     # Implementations of all core/ headers
│   ├── graph/                    # workflow_parser.cpp, graph_executor.cpp, workflow_compiler.cpp
│   ├── nodes/
│   │   ├── all_nodes.cpp         # All 15 node execute() bodies (~27k tokens - read in parts)
│   │   ├── base_node.cpp
│   │   ├── init_nodes.cpp        # Registers all 15 nodes at startup
│   │   └── node_registry.cpp
│   └── main.cpp                  # CLI: cmd_parse, cmd_compile, cmd_run, cmd_generate, cmd_info
├── thirdparty/
│   └── xsf/                      # SciPy xsf/cephes headers for beta.ppf parity
│       ├── cephes/               # C port of Cephes math library
│       ├── config.h
│       └── error.h
├── test_data/                    # Reference JSON workflows for testing
├── tests/                        # Test suite (BUILD_TESTS=ON, currently disabled)
├── examples/
│   └── parse_workflow.cpp
└── build/                        # CMake build output (not in VCS)
```

---

## Architecture Pipeline

```
ComfyUI JSON workflow
        |
  WorkflowParser          (graph/workflow_parser.cpp)
        |  topological sort, model path extraction
        v
  Workflow struct          (nodes, execution_order, model_paths)
        |
  WorkflowCompiler         (graph/workflow_compiler.cpp)  [cmd_compile / cmd_generate]
        |  optional AOT step: extracts flat params
        v
  CompiledWorkflow         (prompts, size, steps, cfg, seed, paths)
        |
  ModelManager::initialize  (core/model_manager.cpp)
        |  loads sd_ctx_t via stable-diffusion.cpp
        v
  GraphExecutor::execute    (graph/graph_executor.cpp)
        |  iterates execution_order, dispatches each node
        v
  Node::execute()           (nodes/all_nodes.cpp)
  [VAELoader, UNETLoader, CLIPLoader, LoadImage, VAEEncode,
   TextEncodeQwenImageEditPlus, FluxKontextMultiReferenceLatentMethod,
   ModelSamplingAuraFlow, CFGNorm, KSampler, VAEDecode, SaveImage,
   ImageScaleToTotalPixels, GetImageSize+, ImageResize+]
        |
  GraphContext              (stores node outputs keyed by node_id + slot)
        |
  PNG output
```

`cmd_run` uses `GraphExecutor::execute` directly (no `WorkflowCompiler` AOT step).
`cmd_generate` runs both the compiler and the executor.

---

## 15 Node Types

All declared in `include/comfynative/nodes/all_nodes.h`, implemented in `src/nodes/all_nodes.cpp`, registered in `src/nodes/init_nodes.cpp`.

| # | ComfyUI type string | C++ class | Category |
|---|---------------------|-----------|----------|
| 1 | `VAELoader` | `VAELoaderNode` | Model loader |
| 2 | `UNETLoader` | `UNETLoaderNode` | Model loader |
| 3 | `CLIPLoader` | `CLIPLoaderNode` | Model loader |
| 4 | `LoadImage` | `LoadImageNode` | Image I/O |
| 5 | `SaveImage` | `SaveImageNode` | Image I/O |
| 6 | `ImageScaleToTotalPixels` | `ImageScaleToTotalPixelsNode` | Image processing |
| 7 | `GetImageSize+` | `GetImageSizeNode` | Image processing |
| 8 | `ImageResize+` | `ImageResizeNode` | Image processing |
| 9 | `VAEEncode` | `VAEEncodeNode` | VAE |
| 10 | `VAEDecode` | `VAEDecodeNode` | VAE |
| 11 | `TextEncodeQwenImageEditPlus` | `TextEncodeQwenImageEditPlusNode` | Encoding |
| 12 | `FluxKontextMultiReferenceLatentMethod` | `FluxKontextMultiReferenceLatentMethodNode` | Reference |
| 13 | `ModelSamplingAuraFlow` | `ModelSamplingAuraFlowNode` | Model modifier |
| 14 | `CFGNorm` | `CFGNormNode` | Model modifier |
| 15 | `KSampler` | `KSamplerNode` | Sampling |

Nodes are registered via the `REGISTER_NODE(ClassName)` macro (static-initializer pattern) or explicitly in `initialize_nodes()`. `main.cpp` calls `nodes::initialize_nodes()` before dispatching subcommands.

---

## Key Data Structures

### graph namespace (workflow_parser.h)
- `Node` - single graph node: id, type, widget inputs (`InputValue` variant), connections (node_id → slot)
- `Workflow` - full parsed workflow: nodes map, execution_order, output_nodes, model_paths, ComfyUI metadata fields (prompt_json, extra_pnginfo, output_dir, input_dir)

### graph namespace (graph_executor.h)
- `GraphContext` - stores `std::any` outputs keyed by (node_id, slot); also holds path config (output_dir, input_dir, temp_dir) and execution metadata

### core namespace
- `CondTensor` - flat `std::vector<float>` tensor with shape and Device
- `CondEntry` / `CondObject` / `ConditioningData` - ComfyUI conditioning dict parity
- `SamplerLatentDict` - full ComfyUI latent dict (samples, noise_mask, batch_index, downscale_ratio_spacial, nested support)
- `LatentFormat` - latent space spec (channels, dimensions, spatial_downscale_ratio)
- `ModelConfig` / `UNetConfig` - detected model architecture and sampling settings

---

## CLI Subcommands (src/main.cpp)

```
comfynative-cli parse   <workflow.json>   # Parse + print node count, model paths
comfynative-cli compile <workflow.json>   # Compile to CompiledWorkflow, print plan
comfynative-cli run     <workflow.json>   # GraphExecutor::execute (no AOT step)
comfynative-cli generate <workflow.json>  # Compile + ModelManager init + GraphExecutor
comfynative-cli info                      # Version + build info
```

All five subcommands are implemented. `run` uses the same ~15-line argv pattern as `parse`; it does not go through `WorkflowCompiler`. The hand-rolled argv interface is confirmed for the active milestone; CLI11 migration requires user confirmation before any code changes.

---

## Build Instructions

### Prerequisites
- CMake 3.25+
- CUDA Toolkit 12.x
- C++20-capable compiler (GCC 11+ / Clang 13+ / MSVC 2022)
- stable-diffusion.cpp workspace at `../comfy-native-workspace` (relative to this repo)
- nlohmann/json and stb fetched automatically via FetchContent
- LibTorch (optional; required for bit-exact PyTorch RNG parity for N >= 16)

### Configure and build
```bash
cd ComfyNative
mkdir build && cd build

# Minimal build (no LibTorch)
cmake .. -DCMAKE_BUILD_TYPE=Release

# With LibTorch for exact RNG parity (Linux path example)
cmake .. -DCMAKE_BUILD_TYPE=Release \
  -DTORCH_PATH=<ComfyUI root>/venv/lib/python3.12/site-packages/torch

# Specific CUDA arch (avoids native detection issues on mismatched toolchains)
cmake .. -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA_ARCH_LIST="89-real"

cmake --build . --parallel
```

Outputs:
- `build/libcomfynative.a` (or `.lib` on Windows)
- `build/bin/comfynative-cli`

### CMake options

| Option | Default | Purpose |
|--------|---------|---------|
| `BUILD_EXAMPLES` | ON | Builds comfynative-cli and test binaries |
| `BUILD_TESTS` | ON | Enables test framework (currently disabled in CMakeLists) |
| `ENABLE_CUDA_GRAPHS` | ON | Sets `COMFYNATIVE_ENABLE_CUDA_GRAPHS` define (Phase 3) |
| `ENABLE_MULTI_GPU` | ON | Sets `COMFYNATIVE_ENABLE_MULTI_GPU` define (Phase 3) |
| `ENABLE_FLASH_ATTENTION` | ON | Flash Attention kernels |
| `ENABLE_LIBTORCH` | ON | Link LibTorch for bit-exact RNG parity |
| `TORCH_PATH` | Windows default | Path to PyTorch installation |
| `GGML_CUDA_ARCH_LIST` | (from CUDA) | Override CUDA arch list |

---

## Parity Requirements

These three areas require bit-exact numerical match with ComfyUI's Python implementation. They are tested by dedicated test binaries (`test-rng-parity`, `test-scheduler-parity`).

### 1. PyTorch RNG Parity (latent_noise.h / RNGEngine)

Source of truth: `ATen/core/MT19937RNGEngine.h`, `ATen/core/DistributionsHelper.h`, `ATen/native/cpu/DistributionTemplates.h`

- PyTorch uses **double-precision** uniforms (via `random64()`) for Box-Muller, not float
- Box-Muller formula: `r = sqrt(-2.0 * log1p(-u2))`, NOT `log(s)` Marsaglia form
- Vectorized path (N >= 16): fills uniforms first, transforms in 16-blocks, **regenerates** last 16 if `size % 16 != 0`
- `normal_fill_16`: `u1 = 1.0f - data[j]` (NOT `data[j]` directly)

When `COMFYNATIVE_HAVE_LIBTORCH` is defined: `randn_tensor()` delegates to `torch::randn()` with a `LibTorch Generator` seeded identically — this is the only way to get exact parity for `N >= 16`. Without LibTorch the scalar path is exact for `N == 1` but diverges from `torch.randn(N)` for `N >= 16` due to SIMD differences in PyTorch's CPU kernel.

The `RNGEngine` class is marked **DELICATE**. Do not modify without verifying against PyTorch reference output.

### 2. Scheduler Parity (scheduler.h / scheduler.cpp)

Source of truth: `comfy/samplers.py` lines 406-497, `comfy/k_diffusion/sampling.py`

Nine schedulers implemented:
- `simple`, `normal`, `sgm_uniform`, `karras`, `exponential`, `ddim_uniform`, `beta`, `linear_quadratic`, `kl_optimal`

Entry point: `calculate_sigmas(model_sampling, scheduler_name, steps)` — matches ComfyUI `calculate_sigmas()`.

Also includes `ksampler_calculate_sigmas()` (handles `DISCARD_PENULTIMATE_SIGMA_SAMPLERS` set), `ksampler_set_steps()` (denoise strength), and `apply_start_last_step()`.

### 3. Beta Scheduler — Cephes beta.ppf (thirdparty/xsf/cephes/)

The `beta_scheduler` requires `scipy.stats.beta.ppf`, which internally uses the regularized incomplete beta function. The C port lives in `thirdparty/xsf/cephes/` (SciPy xsf headers). This is included directly as a header-only dependency via `target_include_directories`.

---

## Dependencies

| Dependency | Version | How obtained | Purpose |
|------------|---------|--------------|---------|
| stable-diffusion.cpp | custom fork | CMake subdirectory at `../comfy-native-workspace` | GGML tensors, model loading, VAE, sampling backend |
| nlohmann/json | v3.11.3 | FetchContent (GH) | JSON workflow parsing |
| stb | master | FetchContent (GH) | Image I/O (stb_image, stb_image_write) |
| CUDA Toolkit | 12.x | System | `CUDA::cudart`, `CUDA::cublas` |
| LibTorch | PyTorch install | Optional; `find_package(Torch)` | Bit-exact RNG parity for N >= 16 |
| xsf/cephes | SciPy port | `thirdparty/xsf/` (in-tree) | beta.ppf for beta_scheduler |

The `../comfy-native-workspace` path is hardcoded in CMakeLists.txt (`add_subdirectory`). If the workspace is at a different relative location, pass `-DSTABLE_DIFFUSION_CPP_DIR=<path>` or adjust the CMakeLists.

---

## Model Detection

`ModelDetector` (core/model_detection.h) reads safetensors/GGUF headers without loading weights to determine architecture:
- `QWEN_IMAGE`, `QWEN_IMAGE_2511` (index_timestep_zero), `QWEN_IMAGE_LAYERED` (additional_t_cond)
- `FLUX`, `FLUX2`
- `SD1`, `SD2`, `SDXL`, `SDXL_REFINER`
- `CASCADE`, `AURA_FLOW`, `HUN_YUAN_DIT`, `WAN`

SD2 V-prediction detection reads tensor data (std-dev heuristic on `output_blocks.11.1.transformer_blocks.0.norm1.bias`). This is the only case where tensor weights are loaded during detection.

`ModelManager` (singleton) wraps `sd_ctx_t*` from stable-diffusion.cpp. It exposes:
- `initialize(diffusion, vae, clip, weight_dtype)` — loads all three models once
- `vae_encode` / `vae_decode`
- `encode_text_with_images_shaped` — returns `EncodingResultShaped` with `[B, T, C]` shape
- `sample_latent_structured` — ComfyUI-parity path accepting `ConditioningData` (no prompt string fallback)
- `set_flow_shift` / `set_cfg_norm_strength`

---

## Deploy Target (ComfyCompiled)

Location: `~/Documents/AI/ComfyUI_V81/ComfyUI/custom_nodes/ComfyCompiled/`

This is a ComfyUI Python plugin that exposes ComfyNative via pybind11. Its `cpp/` subdirectory has its own `CMakeLists.txt` that links against the ComfyNative static library. The Python module (`comfycompiled_native.pyd` / `.so`) is loaded by `__init__.py` when ComfyUI starts.

After any ComfyNative C++ change that affects the static library or its public headers:
1. Rebuild ComfyNative: `cmake --build build/`
2. Rebuild ComfyCompiled bindings: `cmake --build cpp/build/`
3. Restart ComfyUI (the old `.pyd` stays loaded in memory until restart)

---

## Large Files (Read in Parts)

| File | Approx. size | Notes |
|------|-------------|-------|
| `src/nodes/all_nodes.cpp` | ~27k tokens | All 15 node execute() bodies; use offset+limit |
| `include/comfynative/core/latent_noise.h` | ~1100 lines | Full RNGEngine + noise prep pipeline |
| `include/comfynative/core/scheduler.h` | ~330 lines | All 9 scheduler declarations with Python reference comments |
| `include/comfynative/core/model_manager.h` | ~350 lines | Full ModelManager API |
| `include/comfynative/core/model_detection.h` | ~415 lines | SafetensorsReader, GGUFReader, ModelDetector |

---

## Active Milestone Gap (as of 2026-03-19)

The `run` subcommand function body (`cmd_run`) is present and complete in `src/main.cpp`. It calls `WorkflowParser::parse_file`, `WorkflowParser::validate`, and `GraphExecutor::execute` directly — no `WorkflowCompiler` AOT step, following the same ~15-line pattern as `cmd_parse`.

Phase 2 real node implementations are in progress. Node stubs print execution messages but return empty values; the goal is to wire each node to the corresponding `ModelManager` or core API call.
