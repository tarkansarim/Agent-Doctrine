# Tool Failure Procedure

Use this module when Bash, MCP, wrapper CLIs, hooks, installers, build scripts,
validation commands, tmux/contact channels, or reusable agent infrastructure
fail or behave unexpectedly.

- Stop before silently routing around the failed tool.
- Classify the failure as either a real local/toolchain issue or an external
  wrapper/policy limitation.
- For real issues, report the command and behavior, fix the tool path when the
  active agent owns it, and validate the fix before resuming the original task.
- For external limitations, state the limitation and only use an alternate route
  when it preserves correctness and the user has allowed that class of route.
