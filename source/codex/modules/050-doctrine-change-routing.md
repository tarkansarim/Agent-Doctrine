# Codex Doctrine Change Routing

<!-- agent-doctrine-rule:doctrine.dual-provider-rollout -->
- Provider-general doctrine changes install both Codex and Claude snapshots;
  single-provider rollout requires explicit scope and reason.
<!-- agent-doctrine-rule:doctrine.lean-runtime -->
- Doctrine files contain only short, always-true, every-turn-essential rules;
  all procedure and detail live in relay-pattern skills referenced by one-line
  pointers.
<!-- agent-doctrine-rule:doctrine.install-drift -->
- Treat unmanaged deployed doctrine outside managed markers as install drift requiring a user decision: adopt/import, discard, or temporary exception.
<!-- agent-doctrine-rule:doctrine.router -->
- Provider-doctrine workflow details live in `agent-doctrine-router`.
<!-- agent-doctrine-rule:doctrine.provider-lane-separation -->
- Keep provider lanes separate. Codex source modules, generated output,
  validators, installers, tests, and deployment target are separate from Claude.
