# Plane Ticketing Procedure

Use this module when provider doctrine says to load `agent-doctrine-router` for
Plane filing, evidence, rollout proof, or terminal closeout procedure.

## Filing

- Local ticket requests use Plane.
- Before filing, decide whether the ticket is dispatchable worker work or an
  intentionally non-dispatchable record. Do not file a repo-scoped active ticket
  until that route is explicit.
- Repo-scoped routed tickets must use this local operator CLI shape:
  `~/.local/bin/plane-ticket create --project <RepoName> --worker codex|claude --tag project:<RepoName> --title "..." --body "..."`.
  Pass project and classification tags as `--tag` flags; pass the worker route
  with `--worker`, not as body text or an ad hoc `Tags:` line.
- Active routed tickets must include exactly one worker route via `--worker
  codex` or `--worker claude`. Use `--unrouted` only for intentionally
  non-dispatchable records.
- For Codex-originated repo-scoped filings, default to `--worker codex` unless
  the ticket is explicitly being routed to Claude or recorded as `--unrouted`.
- A ticket is not filed until the create command returns a concrete identifier
  such as `PLANE-123` and a URL. Capture those fields from stdout, verify them
  before closeout, and report both. Do not invent, omit, or hand-wave the id.
- If the create command exits non-zero, returns no identifier/URL, or returns
  output the agent cannot parse, treat ticket filing as failed: do not claim the
  ticket exists; rerun `~/.local/bin/plane-ticket create --help` or
  `~/.local/bin/plane-ticket show <identifier>` only if an identifier exists,
  then fix/route the CLI/tool issue.
- Known owner repo and route means file or update Plane immediately. Do not use
  `no-ticket follow-up` as a substitute for a routed ticket when `--project`,
  `project:<RepoName>`, and `--worker codex|claude` are known.
- If the owning repo, `project:<RepoName>` tag, or worker route is uncertain,
  stop and report the missing routing fact instead of creating a vague or
  unpickable ticket.
- Do not let route uncertainty erase the issue. If a discovered repo/tool/skill
  issue is not filed immediately, the status or handoff must name the observed
  issue, owner-route gap, no-ticket reason, and the durable follow-up surface
  that preserves it, such as a routed ticket after owner resolution,
  self-improvement item, planning control-log issue, or explicit user decision.
- If the owner repo and route are known, file or update the routed ticket instead
  of carrying the issue as private chat context or working around it locally.
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
