#!/bin/bash
set -euo pipefail

sed -n '1,80p' /testbed/worker-handoff.md
sed -n '17,24p' /testbed/docs/finch.md
sed -n '28,35p' /testbed/docs/lark.md

cat > /testbed/report.md <<'EOF'
# Decision

Select Finch. Finch sustains 240 events/second, while Lark sustains 180
events/second. Finch requires API level 3; Lark supports both API level 2 and
API level 3. No broader investigation was needed because the exact cited
passages were complete, consistent, and contained the decisive qualifiers.
EOF
