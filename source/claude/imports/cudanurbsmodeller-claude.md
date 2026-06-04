# Imported Claude Doctrine Source

- Source path: `<workspace root>/CudaNurbsModeller/CLAUDE.md`
- Source SHA256: `38af042104bd5a1042ee5fc1697907a9facd727ecd1a556d0e4f17a1722b4730`
- Provider lane: `claude`

## Original Content

# CudaNurbsModeller — Project Rules

## MCP Tools Skill Maintenance

The `nurbs-mcp-tools` skill documents all MCP tool commands for agentic control of the app. **Every time a new feature is added to the app**, update:

1. `src/app.cpp` → `handleCommand()` — add the C++ command handler
2. `mcp_server/nurbs_mcp.py` — add the corresponding `@mcp.tool()` Python bridge function
3. `nurbs-mcp-tools` skill — add the new tool to the reference table

If the tool list grows beyond ~40 commands, split the skill into sub-category skills (e.g., `nurbs-mcp-creation`, `nurbs-mcp-editing`, `nurbs-mcp-display`).
