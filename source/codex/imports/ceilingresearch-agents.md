# Imported Codex Doctrine Source

- Source path: `<workspace root>/CeilingResearch/AGENTS.md`
- Source SHA256: `167afeaf8704c16b7576e7da4e2125ef8e2b7d38381c6ce01ce11fa7554ea486`
- Provider lane: `codex`

## Original Content

# Agent Instructions

This folder is a standalone extraction candidate for CppStudio's current-best-practice and
state-of-the-art ceiling research behavior.

## Current Status

- Scaffold only. Do not install until `skills/ceiling-research/SKILL.md` and validation are
  implemented.
- CppStudio remains the working source of the behavior until this repo has passing trigger tests and
  an install path.

## Pickup Rules

- Read `README.md` and `IMPLEMENTATION_BRIEF.md` before editing.
- Use CppStudio as reference, not as code to blindly copy. Extract the behavior into a generic skill
  that can serve any serious software project, not only native GPU work.
- Do not delete or weaken the embedded CppStudio planner rules until the standalone skill is proven
  and CppStudio has been updated to relay to it.
- Keep the skill concise. Put larger checklists, output schemas, and source-quality rules under
  `references/`.
- Before claiming reliability, run fresh-agent trigger tests that prove the skill fires on broad
  planning prompts and produces current-vs-legacy evidence.

## Expected First Commit

Implement a minimal valid skill package, references, validator or smoke script, and a dry-run install
check. Then commit with a clear `Commit-Origin` trailer.
