# Local Plane Ticketing

- Local ticket requests use Plane via `~/.local/bin/plane-ticket`; repo-scoped
  tickets must include `--project <RepoName>`, tag `project:<RepoName>`, and
  tag `worker:codex` or `worker:claude` unless explicitly `--unrouted`.
- Do not use Kanboard for new tickets unless explicitly requested; for Plane
  filing and closeout procedure, load `agent-doctrine-router`.
