# Imported Codex Doctrine Source

- Source path: `<workspace root>/DonorLibrarySystem/AGENTS.md`
- Source SHA256: `8676c4775cde34148f723b425f0c561c59c43c38220ef2240bffddce72fa0543`
- Provider lane: `codex`

## Original Content

# Agent Instructions

This folder is a standalone extraction candidate for CppStudio's donor-library packaging,
progressive-disclosure, provenance, and freshness mechanisms.

## Current Status

- Scaffold only. Do not install until the standalone package is implemented.
- CppStudio remains the source of the existing native GPU donor content.

## Pickup Rules

- Read `README.md` and `IMPLEMENTATION_BRIEF.md` before editing.
- Extract the generic donor-library mechanism. Do not move CppStudio's C++/CUDA/Vulkan donor content
  until a migration is explicitly planned.
- Keep donor content and donor management separate: this repo should provide the framework; domain
  repos can own their donor collections.
- Do not fetch or vendor large upstream source trees without an explicit license/storage plan.

## Expected First Commit

Implement the skill, donor profile schema, freshness/provenance validators, fixtures, and dry-run
install path.
