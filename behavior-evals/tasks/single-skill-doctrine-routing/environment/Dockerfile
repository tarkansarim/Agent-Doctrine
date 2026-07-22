FROM ubuntu:24.04

RUN apt-get update -qq \
    && apt-get install -y -qq ca-certificates curl git nodejs npm python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash agent \
    && mkdir -p /home/agent/.codex /testbed \
    && chown -R agent:agent /home/agent /testbed

WORKDIR /testbed
