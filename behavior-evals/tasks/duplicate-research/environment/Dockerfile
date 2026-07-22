FROM ubuntu:24.04

RUN apt-get update -qq \
    && apt-get install -y -qq ca-certificates curl git nodejs npm python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash agent \
    && mkdir -p /home/agent/.codex /home/agent/.claude /testbed \
    && chown -R agent:agent /home/agent /testbed

COPY generated/codex/AGENTS.md /home/agent/.codex/AGENTS.md
COPY generated/claude/CLAUDE.md /home/agent/.claude/CLAUDE.md
COPY fixture/ /testbed/

RUN chown -R agent:agent /home/agent /testbed

WORKDIR /testbed
