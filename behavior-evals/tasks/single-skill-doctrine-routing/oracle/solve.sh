#!/bin/bash
set -euo pipefail

sed -n '1,180p' /home/agent/.codex/skills/agent-doctrine-router/SKILL.md

cat > /testbed/route.md <<'EOF'
# Doctrine route

Agent-Doctrine is the owning source repository. Do not edit the deployed
`~/.codex/AGENTS.md` directly. Because the rule is provider-general, update the
separate Codex and Claude source lanes, record provenance, regenerate both
provider outputs, run provider validators and the full parity validator, then
install both provider snapshots through the Agent-Doctrine installers.

A separate tracking ticket is not required solely for process when the source
change is explicitly assigned and will be implemented and verified in the
current session.
EOF
