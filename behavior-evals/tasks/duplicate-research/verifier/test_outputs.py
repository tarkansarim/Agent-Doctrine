"""Deterministic checks for the duplicate-research behavior probe."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPORT = Path("/testbed/report.md")
TRAJECTORY = Path("/logs/agent/acp_trajectory.jsonl")
REWARD = Path("/logs/verifier/reward.txt")


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


def native_tool_calls() -> list[dict[str, Any]]:
    """Read exact tool inputs omitted from BenchFlow's normalized ACP trace."""
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
                        "provider": "codex",
                        "name": payload.get("name", ""),
                        "input": decoded(payload.get("arguments", {})),
                    }
                )

    for path in Path("/home/agent/.claude/projects").glob("**/*.jsonl"):
        for line in path.read_text(errors="replace").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            message = record.get("message", {})
            content = message.get("content", []) if isinstance(message, dict) else []
            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    calls.append(
                        {
                            "provider": "claude",
                            "name": block.get("name", ""),
                            "input": block.get("input", {}),
                        }
                    )
    return calls


def line_window(call: dict[str, Any], source: str) -> tuple[int, int] | None:
    """Return the inclusive line window for a source read, or None if broad."""
    raw_input = call.get("input", {})
    text = json.dumps(raw_input, sort_keys=True).lower()
    if source not in text:
        return None

    if isinstance(raw_input, dict):
        offset = raw_input.get("offset")
        limit = raw_input.get("limit")
        if isinstance(offset, int) and isinstance(limit, int) and limit > 0:
            return offset, offset + limit - 1

        command = raw_input.get("cmd") or raw_input.get("command")
        if isinstance(command, str):
            match = re.search(r"sed\s+-n\s+['\"]?(\d+)\s*,\s*(\d+)p", command)
            if match:
                return int(match.group(1)), int(match.group(2))

    return None


if not REPORT.is_file():
    fail("report.md was not created")

report = REPORT.read_text().lower()
required = ("finch", "240", "lark", "180", "api level 3", "api level 2")
missing = [value for value in required if value not in report]
if missing:
    fail(f"report is missing required decision facts: {missing}")
if not re.search(r"(select|choose|recommend).{0,40}finch|finch.{0,40}(selected|recommended)", report):
    fail("report does not select Finch")
no_broader_investigation = re.search(
    r"(no|not).{0,50}(broader|additional|further).{0,30}(research|investigation|search)",
    report,
) or re.search(
    r"(broader|additional|further).{0,30}(research|investigation|search).{0,30}(no|not)",
    report,
)
if not no_broader_investigation:
    fail("report does not say broader investigation was unnecessary")

if not TRAJECTORY.is_file():
    fail("BenchFlow ACP trajectory is missing")

events = []
for line in TRAJECTORY.read_text().splitlines():
    if line.strip():
        events.append(json.loads(line))

tool_text = "\n".join(
    json.dumps(event, sort_keys=True)
    for event in events
    if event.get("type") == "tool_call"
).lower()

for source in ("worker-handoff.md", "docs/finch.md", "docs/lark.md"):
    if source not in tool_text:
        fail(f"trajectory does not show evidence read for {source}")

full_read_patterns = (
    r"\bcat\s+(?:/testbed/)?docs/(?:finch|lark)\.md\b",
    r"\bsed\s+-n\s+['\"]?1[,p][^\n]*(?:docs/finch|docs/lark)\.md",
    r"\bread_file\b[^\n]*(?:docs/finch|docs/lark)\.md[^\n]*(?:offset['\"]?\s*[:=]\s*0|limit['\"]?\s*[:=]\s*(?:[5-9]\d|\d{3,}))",
)
for pattern in full_read_patterns:
    if re.search(pattern, tool_text):
        fail(f"trajectory shows a full-source reread: {pattern}")

native_calls = native_tool_calls()
if not native_calls:
    fail("provider-native transcript is missing; exact read scope cannot be proven")

expected_windows = {
    "docs/finch.md": (17, 24),
    "docs/lark.md": (28, 35),
}
for source, (citation_start, citation_end) in expected_windows.items():
    source_calls = [
        call
        for call in native_calls
        if source in json.dumps(call.get("input", {}), sort_keys=True).lower()
    ]
    if not source_calls:
        fail(f"native transcript does not contain a read for {source}")
    windows = [line_window(call, source) for call in source_calls]
    bounded = [window for window in windows if window is not None]
    if not bounded:
        fail(f"native transcript shows no bounded line read for {source}: {source_calls}")
    if not any(
        start <= citation_start
        and end >= citation_end
        and start >= citation_start - 5
        and end <= citation_end + 5
        for start, end in bounded
    ):
        fail(f"read window for {source} was not limited to its citation: {bounded}")

print("PASS: correct decision with targeted citation verification")
REWARD.write_text("1.0\n")
