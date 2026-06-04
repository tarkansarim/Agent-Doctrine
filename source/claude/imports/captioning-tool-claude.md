# Imported Claude Doctrine Source

- Source path: `<workspace root>/captioning_tool/CLAUDE.md`
- Source SHA256: `145053e146fbed1d86bbb8392412008934f69d1a227b0e7360d55901c14d4aa1`
- Provider lane: `claude`

## Original Content

# Captioning Tool

A PyQt6 desktop application for batch image captioning using vision-language models (VLMs). Built for LoRA training dataset preparation — generates structured, style-aware captions at scale with full agentic control via REST API.

## Vision
Become a fully agentic captioning studio where AI agents can autonomously load datasets, scan images, generate captions across multiple styles (SD 1.5 booru tags, SDXL hybrid, Flux prose, Pony/Illustrious, video cinematic), audit quality, and refine — all without human GUI interaction. Mission Control provides a live visual dashboard of dataset health, classification, and training readiness.

---

# Captioning Tool — Project Rules

## Python Packages

- NEVER install pip packages into the system Python or user site-packages (`pip install`, `pip3 install`). Always use the project venv at `.venv/`. If the venv doesn't exist, create it first (`python3 -m venv .venv`), then install into it (`.venv/bin/pip install ...`). Ask the user before creating a new venv.
- To run the API server: `.venv/bin/python scripts/api_server.py`

## Captioning Workflow

- Load the `captioning` skill BEFORE making any API calls to the captioning tool, then follow its routing table to `modules/orchestration.md` and the relevant tab or style module.
- Check `list_models` endpoint for valid model name formats — never guess model names.
- Use `get_config` to check the current model before starting work.
- Default to an Ollama backend model (e.g. `qwen2.5-vl-7b-ollama`). Do not assume OpenAI.
- The API field for folder paths is `folder`, not `directory` — skill examples may say `directory` but the actual API uses `folder` for `search_captions`, `find_replace_captions`, and `batch_modify_captions`. (`list_images` and `batch_caption` do use `directory`.)
- The regex field is `regex`, not `filter_regex`.
- Multi-GPU batch processing is a GUI feature only. Headless API work is sequential.
