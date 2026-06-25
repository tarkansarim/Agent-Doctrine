# Imported Claude Doctrine Source

- Source path: `<workspace root>/Integrity-Revenue/CLAUDE.md`
- Source SHA256: `7404c368e7c1ffab65c836e29845492f868eb4fb0ccf71bcb51c579b7f78d0f9`
- Provider lane: `claude`

## Original Content

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

Integrity-Revenue is a **documentation-only planning repo** — the portfolio and
self-preservation layer for the user's local tool ecosystem. There is no source
code, build system, tests, or runtime. All content is Markdown. Work here means
reading, classifying, and editing strategy documents, not writing or running
software.

There are no build/lint/test commands. Verification means checking that edits
stay internally consistent with the rules below and with the other documents.

## Core Purpose

The repo tracks the fair-return revenue path toward a base survival target of
**15K USD/month**, framed as ecosystem self-preservation rather than
maximum-revenue extraction.

Purpose is **layered** (see README "Two Layers of Purpose"): the 15K/month
target is **layer 1**, a survival floor that must be secured first. **Layer 2**,
after stabilization, is **deliberate controlled growth** — grow slowly, keep
capacity ahead of demand, and never rush into demand the ecosystem cannot
satisfy. Reaching the floor unlocks growth; it is not the destination. When
making revenue/lane/pricing/launch recommendations, treat survival as the floor
and pace growth so capacity always leads demand.

The integrity loop that every decision is judged against:

```text
internal capability grows
-> product output creates genuine value
-> buyer feels the deal is fair
-> balanced revenue preserves the ecosystem
-> the ecosystem keeps building
```

## Document Architecture

Read these together to understand the big picture; they cross-reference and must
stay consistent:

- `AGENTS.md` — agent operating rules for this repo (also applies to Claude).
  Treat as the authoritative behavior contract here.
- `README.md` — entry point; current focus and file index.
- `SURVIVAL_TARGET.md` — the 15K/month base target, why it exists, integrity rule.
- `PORTFOLIO.md` — the live classification of every ecosystem repo into lanes
  (primary revenue / moat-risk candidate / revenue-enabling infrastructure /
  open-source-research / external-not-a-target).
- `NEXT_REVENUE_GATES.md` — the concrete sequenced gates toward first revenue.
- `PRODUCT_HARDENING_GATES.md` — Pressure Lab hardening surfaces that form the moat.
- `REVENUE_BALANCE_SENSE.md` — design for a future early-warning urgency sense
  (planned, not yet implemented).
- `lanes/sonicgroom.md`, `lanes/wetbrush-lin.md`, `lanes/helmsman-trainer.md` —
  per-lane product thesis, revenue questions, hardening priorities, next gate.
- `classification/` — currently empty; reserved for classification artifacts.
- `.claude/skills/` — project-local skills for repeatable procedures in this repo
  (e.g. `lane-readiness-map`). See "Skills" below.

## Lane Classification (current state)

- **Primary revenue lanes:** SonicGroom (`CudaGroomTool2` / `CudaGroomTool`) and
  Wetbrush (`wetbrush_lin` / `wetbrush_lin_cas`).
- **Candidate with moat risk:** `helmsman-trainer` — easy to replicate once
  public; do not let it distract from the primary lanes until its moat is clearer.
- Everything else is infrastructure, research, or external reference.

Classification is practical, not permanent — a repo can move lanes when evidence
changes. Keep `PORTFOLIO.md` and the relevant `lanes/` file in sync when a
classification changes.

## Operating Rules (from AGENTS.md — follow when editing)

- Revenue is self-preservation pressure, not the purpose of every small gate.
  Don't force every research gate to monetize itself.
- A repo only counts as a revenue lane if the **user owns or controls it**.
  External repos are reference/inspiration/dependency only.
- Paid products must be genuinely useful and feel like a fair deal; avoid
  extractive optimization.
- Pressure Lab hardening is part of the moat — features can be copied, hardened
  behavior is harder to copy.
- Keep this repo **small, practical, and decision-oriented**. Do not turn it into
  broad theory. Ground every revenue question in: buyer pain, product shape,
  first sellable workflow, hardening requirements, fair-return pricing, and the
  path to 15K/month.
- Treat the revenue-balance sense as an early-warning gradient: bias toward
  revenue gates while runway is still comfortable, not at panic time.

## Working Rules (encoded from practice)

These are how to operate here, learned while grounding the lanes:

- **Docs are claims, not ground truth.** Repo READMEs and status docs in this
  ecosystem often describe the *target/aspirational* feature set, not what
  actually ships today (confirmed with `CudaGroomTool2`). Never build a
  readiness/revenue assessment from a README's feature list. Verify against real
  binaries/code/tests, and **let the user's stated status override the docs.**
  Flag the gap when docs and reality diverge.
- **Ground before you plan.** A lane's pricing, sequencing, and 15K math are
  unreliable until that lane's real state is mapped. Do the readiness map first
  (see the `lane-readiness-map` skill), then plan.
- **This repo holds decisions, not product work.** Hardening, bug fixes,
  features, and packaging are owned in the product repos (`CudaGroomTool2`,
  `wetbrush_lin`, etc.), never implemented here. Here you record the MVP
  boundary, buyer hypothesis, sequencing, and pricing decision — and point at
  the owning repo for the work.
- **Don't price a product that doesn't exist yet.** No pricing model or
  15K-path commitment until the lane has an assembled MVP loop. The revenue
  balance sense likewise needs real revenue/burn/readiness inputs — it stays a
  design until those exist.
- **Write findings back into the lane file** as a dated `Current-State
  Readiness Map`, and update the lane's `Next Gate` to the next real action.
- **Keep concepts repo-local while they mature.** Do not promote this repo's
  ideas into user-level doctrine (`~/.claude`, `~/.codex`, Agent-Doctrine) or
  into user-level skills until the user says they have matured.

## Skills

- Repeatable or repo-specific procedures should become **project-local skills**
  under `.claude/skills/<name>/SKILL.md`, discovered automatically when working
  in this repo. The repo is the source of truth for them; do not install copies
  into `~/.claude/skills` while concepts are still maturing.
- Before creating, editing, or auditing any skill, load `skill-packaging-discipline-router`
  and follow it: one relay `SKILL.md` per package at the package top, plain
  markdown for any internal modules, no editing of deployed copies.
- Current project skills:
  - `lane-readiness-map` — produce a grounded, evidence-based revenue-readiness
    map for a portfolio lane and write it back into the lane file.
- Create new skills when a new repeatable or specific procedure emerges; record
  them in this list.

## Conventions

- Markdown with `text` fenced blocks for the recurring loop/gate diagrams; match
  that style when adding sections.
- Repo references use absolute paths under `<workspace root>/`.
