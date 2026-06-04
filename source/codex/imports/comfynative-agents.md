# Imported Codex Doctrine Source

- Source path: `<workspace root>/ComfyNative/AGENTS.md`
- Source SHA256: `b2134658a2fc7448c96d837cab4affb9a9329a340ffb3f253e9482c2ed211d65`
- Provider lane: `codex`

## Original Content

# ComfyNative Agent Notes

Use the `comfy-native-repo-onboarding` skill when starting work in this repo.

Repo-local rules:

- Distinguish the two runtimes before changing code:
  - Standalone ComfyNative in this repo
  - ComfyUI plugin runtime in `<Documents root>/AI/ComfyUI_V81/ComfyUI/custom_nodes/ComfyCompiled`
- If you validate through ComfyUI, rebuild the ComfyCompiled pybind module and restart ComfyUI. Rebuilding only this repo is not sufficient.
- Use `CLAUDE.md` as the main repo map.
- Prefer current code and live logs over older milestone markdown files.
