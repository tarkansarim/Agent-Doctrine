# Plane Ticketing Procedure

Use this module when provider doctrine says to load `agent-doctrine-router` for
Plane filing, evidence, rollout proof, or terminal closeout procedure.

## Filing

- Local ticket requests use Plane.
- Before filing, decide whether the ticket is dispatchable worker work or an
  intentionally non-dispatchable record. Do not file a repo-scoped active ticket
  until that route is explicit.
- Repo-scoped routed tickets must use this local operator CLI shape:
  `~/.local/bin/plane-ticket create --project <RepoName> --tag project:<RepoName> --tag worker:codex|worker:claude ...`.
  Pass every route tag as a `--tag` flag; do not rely on title/body prose,
  ad hoc `Tags:` lines, or later rejection to discover the required route.
- Active routed tickets must also include exactly one worker route tag:
  `worker:codex` or `worker:claude`. Use `--unrouted` only for intentionally
  non-dispatchable records.
- For Codex-originated repo-scoped filings, default to `--tag worker:codex`
  unless the ticket is explicitly being routed to Claude or recorded as
  `--unrouted`.
- If the owning repo, `project:<RepoName>` tag, or worker route is uncertain,
  stop and report the missing routing fact instead of creating a vague or
  unpickable ticket.
- If origin fork capture fails or times out, treat that as degraded origin
  metadata, not a failed ticket creation, when the CLI reports the ticket id or
  URL. Record the warning text in the ticket context/workpad so a later agent can
  distinguish created-ticket success from context-only origin metadata.
- Do not use Kanboard for new tickets unless explicitly requested.
- Report the created Plane ticket id and URL.

## Local Plane Closeout

- When resolving a local Plane ticket, install, roll out, or sync any changed
  installed artifacts immediately after validation and before closing the
  ticket.
- Comment or otherwise record the ticket with the install command and result,
  or explicitly state that no installed artifacts changed.
- Do not close or report the ticket resolved while source changes remain
  uninstalled.
