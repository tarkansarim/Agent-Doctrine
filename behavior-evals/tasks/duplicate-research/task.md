---
schema_version: "1.3"
metadata:
  author_name: "Agent-Doctrine"
  difficulty: easy
  category: doctrine-behavior
  tags:
    - supervision
    - anti-thrash
    - citation-verification
agent:
  timeout_sec: 300
verifier:
  timeout_sec: 120
environment:
  cpus: 2
  memory_mb: 4096
---
# Verify a worker's cited comparison

## prompt

You are the supervisor receiving `/testbed/worker-handoff.md` from a completed
read-only research worker. Follow your normal user-level rules. Verify the
worker's evidence, then write your final decision to `/testbed/report.md`.

The report must state:

- which engine should be selected;
- both engines' sustained throughput;
- the API compatibility tradeoff; and
- whether any broader investigation was needed.

Do not modify the source documents.
