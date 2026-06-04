# Plane Ticketing Procedure

Use this module when provider doctrine says to load `agent-doctrine-router` for
Plane filing, evidence, rollout proof, or terminal closeout procedure.

## Filing

- Local ticket requests use Plane.
- Repo-scoped tickets must include `--project <RepoName>` and tag
  `project:<RepoName>` when using the local operator CLI.
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
