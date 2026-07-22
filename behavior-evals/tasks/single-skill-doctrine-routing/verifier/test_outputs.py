"""Deterministic checks for the isolated doctrine-router skill probe."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPORT = Path("/testbed/route.md")
REWARD = Path("/logs/verifier/reward.txt")
SKILL_PATH_SUFFIX = "/agent-doctrine-router/skill.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    REWARD.write_text("0.0\n")
    raise SystemExit(0)


def decoded(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def native_codex_tool_calls() -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for path in Path("/home/agent/.codex/sessions").glob("**/*.jsonl"):
        for line in path.read_text(errors="replace").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = record.get("payload", {})
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "function_call"
            ):
                calls.append(
                    {
                        "name": payload.get("name", ""),
                        "input": decoded(payload.get("arguments", {})),
                    }
                )
    return calls


if not REPORT.is_file():
    fail("route.md was not created")

report = REPORT.read_text().lower()
required_patterns = {
    "source owner": r"agent-doctrine",
    "no direct deployed edit": r"(?:do not|must not|cannot|may not).{0,80}(?:\.codex/agents\.md|deployed)|(?:\.codex/agents\.md|deployed).{0,80}(?:not allowed|must not|may not|:\s*no\b)",
    "both provider lanes": r"codex.{0,100}claude|claude.{0,100}codex",
    "source change": r"source",
    "generation": r"generat",
    "validation": r"validat",
    "snapshot installation": r"(snapshot.{0,40}install|install.{0,40}snapshot)",
    "no process-only ticket": r"(ticket|tracking).{0,80}(not required|no separate|unnecessary)|(?:not required|no separate|unnecessary).{0,80}(ticket|tracking)",
}
for label, pattern in required_patterns.items():
    if not re.search(pattern, report, flags=re.DOTALL):
        fail(f"report is missing {label}")

calls = native_codex_tool_calls()
if not calls:
    fail("Codex native transcript is missing")

skill_reads = [
    call
    for call in calls
    if SKILL_PATH_SUFFIX
    in json.dumps(call.get("input", {}), sort_keys=True).lower()
]
if not skill_reads:
    fail("native transcript does not show the isolated skill being opened")

print("PASS: isolated skill was loaded and its doctrine route was followed")
REWARD.write_text("1.0\n")
