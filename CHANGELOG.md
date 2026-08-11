# Changelog

## Unreleased

- Require concise README front-page change notes plus detailed changelog entries
  before completed work is committed and pushed; checkpoint-only and diagnostic
  commits are excluded.
- Slimmed down the always-loaded Codex and Claude doctrine substantially to
  reduce heavy process thrashing observed with newer models such as GPT 5.6 Sol
  and Claude Opus 5.
- Converted `agent-doctrine-router` into a thin relay so detailed procedure is
  loaded only when doctrine work needs it.
- Preserved a small set of provider boundaries, reply clarity, autonomous
  progress, agentic judgment, skill-load visibility, and source-owned install
  rules.
- Added an exploratory patch-stacking workflow: anchor the first failed patch,
  use later stacked patches to discover the fix, then restore and replay only
  the proven fix cleanly.
