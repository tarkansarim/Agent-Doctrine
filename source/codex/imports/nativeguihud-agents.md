# Imported Codex Doctrine Source

- Source path: `<workspace root>/NativeGuiHud/AGENTS.md`
- Source SHA256: `186e5992df173776e4b46a93dfca2175bea28ccd60122e888935f7f0d2d2f3c6`
- Provider lane: `codex`

## Original Content

# Agent Instructions

Runtime packets for this repo. Source prose is preserved in `references/source-prose.md`.

```rule-packet
rule repo_status_migration_v1:
  when NativeGuiHud
  and repo = standalone_extraction_candidate for CppStudio native GUI/HUD skill
  and scaffold_only
  ban install until standalone_skill+trigger_probes done + migration_plan
  need keep bundled native-cpp-gui-hud active until migration_plan
  why avoid premature replacement
```

```rule-packet
rule pickup_rules_v1:
  when editing NativeGuiHud
  need read README.md + IMPLEMENTATION_BRIEF.md before edits
  need focus = native GUI/HUD/editor choices + quality_gates
  need compose_with sonar-design + offscreen-test-manager + agentic-control-harness
  ban duplicate composed systems
  need current web/source checks for toolkit choices
  why GUI ecosystems move
```

```rule-packet
rule expected_first_commit_v1:
  when first_commit
  need skill+GUI_refs+checklist+probes+dry-run_install
  verify package
  why first_slice
```
