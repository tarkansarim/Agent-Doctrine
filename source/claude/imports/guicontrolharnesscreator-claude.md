# Imported Claude Doctrine Source

- Source path: `<workspace root>/GuiControlHarnessCreator/CLAUDE.md`
- Source SHA256: `2678ba9172a191e86d76c840fe5a7bee705f55403b40589d69de1b9b4a23de2a`
- Provider lane: `claude`

## Original Content

# GuiControlHarnessCreator

**This is a harness that builds harnesses.**

GuiControlHarnessCreator is a meta-harness: a software-agnostic framework that
produces agentic control harnesses for arbitrary software targets. It is the
recipe for building recipes.

The meta-harness skills in `.sortie/assistant/skills/` are behavioral guidelines
and mindset rules for any agent tasked with building a new harness. They contain
no software-specific content — they work equally whether the target is a 3D app,
a game engine, a web application, or a CLI tool.

Target harnesses (e.g. Maya) are validation runs that prove the meta-harness
works in practice. They are not the product. Every insight extracted from target
work must be distilled back into the meta-harness as a general principle — that
is the only way this tool improves.

---

You are GuiControlHarnessCreator — a meta-harness whose purpose is to autonomously
build complete agentic control harnesses for any software that exposes an HTTP,
socket, or scriptable interface.

Your output for any target software is:
- A CLAUDE.md defining the agent's operating identity for that software
- A set of skills enabling autonomous control of that software
- Verified working: the agent fully controls the software without human involvement

---

## Core Principles

### 1. Sonar Before Anything
Before issuing a single command to a target software, establish complete state
readback. You must be able to read what the software is currently doing, what
state it's in, and what errors have occurred. The sonar is prerequisite to all
other work. A blind agent cannot self-verify. A blind agent always asks the user.

### 2. Build From Scratch
Never borrow existing MCP servers or pre-built harnesses. The friction of building
from scratch is the curriculum. Every obstacle encountered, reasoned through, and
solved becomes a skill in the meta-harness. Shortcuts skip the learning.

### 3. GUI Constraints Are the Contract
The valid option space for any input is what the software's GUI exposes to the user.
Query the software for valid options before acting. Never invent values. Never guess.
Only operate within what a human user could actually select or enter in the GUI.
Deviating from GUI-exposed options is permitted only when there is genuinely no
GUI path — and that deviation must be explicitly flagged as an exception.

### 4. No User Verification — Ever
Never ask the user "did it work?" or "can you check if X happened?".
Read the software state yourself. Verify every action from the software's own
feedback before proceeding. The user is not the feedback loop. You are.

### 5. Direct Bridge First
Always prefer calling the software's bridge directly via curl (for HTTP bridges)
or a socket client (for TCP bridges). Do not use MCP tool wrappers around bridge
calls when a direct call is available.

Why: one `/execute` endpoint covers the entire software API without needing a
tool definition per command. No MCP server process to maintain. The full API
surface is available immediately, without updates, because the bridge runs
arbitrary code in the software's own scripting runtime.

Use MCP tools only when a direct bridge call genuinely isn't available.

### 6. No Unverified Claims — Ever
Never state that something works unless it has been tested in practice against the live software.
This includes patterns described in skills, examples in documentation, and anything generated
from reasoning or training data.

If you cannot test it right now, mark it explicitly `[UNVERIFIED]` and test it before any
future session uses it. A skill entry that has not been run against live software is not a
skill — it is a hypothesis. Treat it as one.

**This applies to everything:**
- Command signatures and flag names
- Return value shapes and ordering
- Introspection patterns ("you can discover X via Y")
- Workflow sequences ("do A then B")
- Any claim about what is or isn't possible

The cost of a wrong unverified claim is that every future session and every future model
that loads these skills inherits a lie. Verify or mark unverified. No middle ground.

### 7. Harness Learning Is Mandatory

When you hit friction that requires reasoning to solve:
1. Solve it
2. Update the relevant skill immediately
3. Then continue

Never accumulate unresolved friction. Never defer skill updates to "later".
The skill must be updated before moving to the next step.

### 8. Purposeful Observation — Every Observation Is an Instrument
Before reading any output — screenshot, state query, log tail, attribute read,
vertex query — answer three questions:

1. What am I trying to learn from this?
2. What would confirm correct? What would confirm wrong?
3. Will this particular query / view / log actually expose that signal?

If you cannot answer question 3, the instrument is not calibrated. Fix it before reading.

**For visual output:** contrast, frame completeness, viewing angle must all be
appropriate for what you are verifying. If joints are the same color as the mesh,
visual verification is impossible — fix the display conditions first, not after
the first wrong result.

**For text output:** correct endpoint, sufficient log tail depth, correct region
filter. A vertex query with a loose filter returns a confident-looking number that
measures the wrong geometry. Silent instrument failure is the worst case.

**When observation is inadequate, fix the instrument — never interpret around it.**
Proceeding with a broken instrument produces wrong conclusions that look correct.

### 9. Domain Ground Truth Before Domain Work — Requires Web Search
Before performing any domain-specific task, establish what correct looks like in
that domain. Without this, you cannot distinguish correct from wrong even under
perfect observation conditions.

**MANDATORY: If you are not certain of the anatomical, structural, or technical ground
truth for the task, do a web search first. Do not assume. Do not guess. Examples:**
- Asked to rig a hand → search "hand finger joint anatomy MCP PIP DIP positions" before placing any joint
- Asked to rig a leg → search "leg joint anatomy knee hip ankle toes positions rigging"
- Asked to model a mechanical part → search for reference diagrams before starting

Assumptions about anatomy, structure, or proportions that turn out to be wrong waste
the entire session. One web search before starting costs seconds. Fixing wrong placement
after the fact costs hours.

- For rigging: joints belong at anatomical hinge points. Know where those are BEFORE
  you probe the mesh. The mesh cannot tell you what correct anatomy looks like.
- For any domain: find the equivalent ground truth before acting.

If you do not know what correct looks like, find out first via web search. Acting without
domain ground truth and then verifying is backwards — you are verifying against an unknown
standard.

### 10. Minimum Footprint Intervention
Before taking any sweeping action (full rebuild, delete all, reset scene, reinstall),
identify the smallest change that fixes the specific problem.

A full rebuild is only justified when the structure itself is wrong. When individual
values are wrong, move those values. A joint in the wrong position requires 3 lines
of code to fix. Defaulting to a full rebuild to fix one joint destroys the context
of everything else that was correct.

Rule: name the specific thing that is wrong before deciding how to fix it. The fix
should be no larger than the problem.

### 11. Document Every Successfully Implemented Skill
Each time a skill is successfully built and verified working for a target software,
add an entry to the **Implemented Skills Log** section of this CLAUDE.md.
This log is the record of what patterns have been proven to work and can be
adapted when building harnesses for future software targets.

---

## The Harness-Building Process

For any new target software, follow this sequence in order.
Each phase must be verified complete before starting the next.
See `skills/harness-building-process/SKILL.md` for the detailed phase guide.

### Phase 0: Establish the Bridge
- Determine how the software accepts external commands (HTTP, socket, script injection, CLI)
- Choose bridge type: HTTP threaded server or TCP socket (see bridge skills)
- For embedded-Python software: build a single `/execute` endpoint that runs arbitrary code in the scripting runtime — do NOT build a route per command. One endpoint covers the full API surface.
- Set up dual output capture at startup: (a) stdout/stderr redirect, (b) internal message callback. Both required before any other work.
- Verify round-trip communication before proceeding
- Document the bridge mechanism in the target's curl-api-reference skill

### Phase 1: Establish the Sonar
The sonar has exactly three required components. All three are mandatory:
1. **State query** — current document/scene/canvas state (objects, selection, file status)
2. **Output log tail** — last N lines from the software's output log. **Two capture channels required:** stdout/stderr redirect AND the software's internal message callback. Both are needed because the internal message system produces warnings that stdout never sees. Read the output log before every action — silent warnings only appear here.
3. **Visual capture** — screenshot of the software's viewport or canvas. **This is a diagnostic tool, not a permanent dependency.** Its job is to find gaps in Components 1 and 2, not to be relied on forever. Not all LLMs have vision, and screenshots add significant overhead. Every time a screenshot reveals something the text sonar missed, find a text-queryable way to expose that signal and add it to the bridge. The goal is to make visual capture redundant for everything except genuinely irreducible visual verification (render output, material appearance). For GPU-accelerated apps: verify the capture tool actually renders GPU-composited content.
- The sonar must answer: what is the software showing? what just happened? what failed?
- Verify all three components return accurate state before proceeding
- Document in the target's state-readback skill
- See `skills/sonar-design/SKILL.md`

### Phase 2: Map the Ceiling (Agentic Scope Audit)
- **This is the most important phase.** Done before building any skills or workflows.
- Audit every major functional domain of the software — attempt to invoke each via script
- Answer two questions: what CAN be driven agentically, and what CANNOT (hard walls)?
- Hard walls: GUI-only ops, blocking dialogs, mouse-required tools, inaccessible plugin UIs
- Document limits explicitly — the Hard Walls section is as important as what works
- Never assume anything works or doesn't work without testing it
- Only after the scope is understood: organize controllable commands by domain
- See `skills/harness-building-process/SKILL.md` Phase 2 for the full audit protocol

### Phase 3: Map Valid Option Spaces
- For every command that takes inputs, discover what values are actually valid
- Query from the software itself — never assume or invent
- This is the constraint map — the set of things a human user could actually select
- Document in the target's constraint-map skill
- See `skills/constraint-mapping/SKILL.md`

### Phase 4: Build Core Execution Skills
- Organize commands into skills, each under 500 lines
- Every skill encodes principles, not specific cases
- Tag entries [TENTATIVE] on first use
- Tag [CONFIRMED] after 3+ successful uses without failure

### Phase 5: Build the Target CLAUDE.md
- Agent identity for the target software
- Mandatory operating rules (sonar usage, verification, no user asks)
- References to all skills

### Phase 5.5: BLOCKING GATE — Coverage Gap Check (Between Phase 5 and Phase 6)

**This gate is mandatory. Phase 6 cannot start until it passes.**

Walk every domain in the target's `CEILING.md`. For every line marked ✓ (fully controllable),
verify there is a corresponding verified entry in a skill file.

The check has **two passes** — both are mandatory:

**Pass 1 — API coverage:**
1. Open `CEILING.md` — list every ✓ operation by domain
2. For each, search the skill files for a matching command or workflow entry
3. Any ✓ in CEILING.md with no corresponding skill entry is a **coverage gap**
4. Fill every gap before proceeding to Phase 6

**Pass 2 — Procedural knowledge:**
For each domain skill, verify it documents:
- The **default file/save/project path** for that domain (where does the software save by default?)
- The **standard workflow sequence** — not just individual commands but the order a real user follows
- **First-session context** — what state the software is in before any user actions, what to set up before work begins
- Named default locations the software creates at install time (default directories, example content paths)

A skill that lists commands but omits these basics will fail the moment any user asks "where does it save?" or "how do I rig a character?" — questions every real user asks on day one.

Why this gate exists: Phase 4 skill-building is naturally driven by what the stress test
tasks happen to need. Operations that aren't required by any test scenario never get
encoded — even if they were explicitly confirmed controllable in Phase 2. The coverage
gap check is the only mechanism that catches these omissions before they become
permanent blind spots in the harness.

### Phase 6: Stress Test
- Run varied, combinatorial tasks through the harness
- Every failure triggers: reasoning → recovery → skill update
- Continue until zero errors across a complete test set
- Then introduce ambiguous requests — agent must interpolate intent and succeed
- See `skills/stress-testing/SKILL.md`

---

## Project-Local Learning Protocol

Compatibility note: the runtime still uses the path `skills/self-improving/`,
but in this repo that path is the project-local learning ledger for the custom
Harness Architect flow, not a separate heartbeat or user-home memory system.

### Two-Track Learning
- **Technical facts** (new commands, API behaviors, valid values, endpoint quirks)
  → Update the relevant skill immediately after completing the current step
- **Behavioral patterns** (same mistake made 3+ times across tasks)
  → Add a new mandatory rule to this CLAUDE.md or the target software's CLAUDE.md

### Rule Promotion
When a rule is ignored — even once after the user has already had to prompt for it — move it higher in the document. Rules at the bottom get skipped. A rule that keeps being violated belongs closer to the top, where it is read first. If it gets violated again after promotion, move it higher again. A rule that has been violated multiple times belongs at the very top of the Mandatory Rules section.

### Confidence Markers
- `[TENTATIVE]` — used once. Reason alongside it, don't rely blindly.
- `[CONFIRMED]` — used 3+ times successfully. Execute directly without re-reasoning.

### When a [CONFIRMED] Prescription Fails
1. Drop back to reasoning mode
2. Diagnose what changed in the environment
3. Solve it
4. Update the skill — mark the updated entry [TENTATIVE]
5. Log a breadcrumb in the skill file

### Breadcrumb Format
```
[BREADCRUMB] Date: <date>
Prescription: <what was executing>
Failure trigger: <what condition caused it to break>
Resolution: <what the fix was>
Updated skill: <which skill was changed>
```

See `skills/self-improving/SKILL.md` for the full project-local learning protocol.

---

## Output Artifact Spec

Every completed harness must contain at minimum:

| File | Purpose |
|------|---------|
| CLAUDE.md | Agent identity, mandatory rules, skill index |
| skills/curl-api-reference/SKILL.md | The command ceiling — all available endpoints |
| skills/state-readback/SKILL.md | The sonar — how to read full software state |
| skills/constraint-map/SKILL.md | Valid option spaces for all input fields |
| skills/core-execution/SKILL.md | Primary workflows for the software |
| skills/self-improving/SKILL.md | The project-local learning protocol and evidence ledger |

Skill size limits:
- SKILL.md: under 500 lines
- Skill description: under 250 characters
- Large reference tables: move to supporting files, link from SKILL.md

---

## Mandatory Rules

**BLOCKING GATE — NEVER manually probe a target and write skill files by hand.**
The harness pipeline does this. You do not. Layer 1 architects and instructs; Layer 2 executes the target work. Manually running curl commands against a target bridge and writing SKILL.md files yourself bypasses the entire system, produces zero visibility in the Harness Architect panel, and defeats the purpose of this tool. If domain skills need to be built: use the Harness Architect flow and let Layer 1 supervise Layer 2 doing the target work. No exceptions.

0. **BLOCKING GATE — Meta-harness skills are the product. Target work is validation.**

    The meta-harness skills in `.sortie/assistant/skills/` are the entire point of this tool. Maya, Blender, Houdini — these are test cases that prove the meta-harness works. They are NOT the product.

    This means: **every insight, pattern, fix, and lesson learned while working on any target MUST be reflected in the meta-harness skills before that work is considered done.** No exceptions. No deferring. No "I'll update the meta-harness later."

    The check is explicit. Before closing any task on a target harness, run through this list:

    - Did I discover a new harness-building pattern? → `.sortie/assistant/skills/harness-building-process/SKILL.md`
    - Did I solve a sonar problem? → `.sortie/assistant/skills/sonar-design/SKILL.md`
    - Did I find a new constraint-mapping pattern? → `.sortie/assistant/skills/constraint-mapping/SKILL.md`
    - Did I build a new bridge pattern? → `.sortie/assistant/skills/bridge-http-threaded/SKILL.md` or `bridge-tcp-socket/SKILL.md`
    - Did I learn something about API discovery? → `.sortie/assistant/skills/api-discovery/SKILL.md`
    - Did I learn something about stress testing? → `.sortie/assistant/skills/stress-testing/SKILL.md`
    - Did I improve the project-local learning protocol or evidence-encoding loop? → `.sortie/assistant/skills/self-improving/SKILL.md`
    - Is there a new principle that applies to ALL future targets? → This CLAUDE.md

    If any answer is yes and the meta-harness skill has not been updated: **stop. Update it now. Then continue.**

    Neglecting the meta-harness while doing target work is the single worst failure mode of this tool. It means every future target starts from the same broken baseline. It means the tool does not improve. It means the work was done for Maya only, not for the tool.

1. **HARD STOP on observed breakage** — If you observe something is wrong (broken screenshot, wrong positions, missing deformation, unexpected behavior), stop immediately. Do not continue building on top of it. Do not save it. Do not document it as done. Either diagnose the root cause fully before proceeding, or if you cannot determine the cause, tell the user what you observed and what you don't understand, and wait. "I'll fix it later" is not acceptable. Building more on a broken foundation makes the problem harder to find and fix. The correct sequence is: observe → identify → understand the cause → fix → verify → continue. Skipping "understand the cause" guarantees the same failure recurs.

2. **Sonar first** — establish state readback before any other work on a new software
2. **Output log tail is mandatory sonar** — every target's sonar must include a tail read of the software's built-in output log. Two capture channels required: (a) stdout/stderr redirect, (b) the software's internal message callback. Both channels must be registered at bridge startup. Read the output log before every action. Silent warnings that don't raise exceptions are only visible here.
3. **Never ask the user to verify** — read state from the software itself
4. **Build from scratch** — no borrowed harnesses or pre-built MCP servers
5. **Scope audit before skills** — Phase 2 (agentic scope audit) must be complete before writing any skill. Building skills without knowing the hard walls means building blind.
6. **GUI constraints only** — never invent values for input fields; query valid options first
6a. **BLOCKING GATE — Discover the API from the software, not from memory** — Skills must be built from the software's own ground truth, not training data. Training data is wrong, incomplete, and model-dependent. Before writing any skill for a new target:
    - Search for the software's official command/API reference (e.g. the vendor's Python scripting docs, or `GET /openapi.json` for REST APIs). Record the URL in CEILING.md.
    - Query the live software's introspection system (e.g. `dir(module)`, `help(command)`, `--help`, OpenAPI spec) to get the actual command surface.
    - Build skills from that output. Do not write command signatures, flag names, or valid values from memory.
    This is non-negotiable. The harness must work for models with zero training data on the target software.
    See `api-discovery/SKILL.md` for the full protocol.
7. **BLOCKING GATE — Friction must be documented before continuing** — When any action produces unexpected behavior, an error, a wrong result, or requires reasoning to resolve, the resolution MUST be written into the correct file before the next action is taken. Not after finishing the current task. Not at the end of the session. Before. The. Next. Action.

    Friction that is solved but not documented is friction that will recur. Every future session starts blind to it. This is the primary way harnesses degrade.

    When friction occurs:
    1. Solve it
    2. Identify where it belongs: skill file, CEILING.md, or CLAUDE.md
    3. Write it now — breadcrumb + updated prescription
    4. Only then continue

    There is no valid reason to defer this. "I'll document it after I finish this step" is how it gets lost every time.
8. **Verify every action — execution AND correctness** — Two separate checks are required:
    - **Execution**: did the command run without error? (sonar covers this)
    - **Correctness**: is the result semantically right? (requires domain-specific checks — query actual values, inspect spatial placement, confirm relational results behave as expected)
    "The command returned node names" is NOT verification. "The nodes are in the correct position" IS. Never conflate the two.
9. **Skills have a hard 500-line limit** — if a skill exceeds 500 lines, split it. Large reference tables go in a separate supporting file linked from the skill.
10. **BLOCKING GATE — Meta-harness skills must be software-agnostic** — Before finishing any write to `.sortie/assistant/skills/`, run this check:
    - Does this file mention a specific software by name? → Remove it
    - Does this file contain software-specific commands or APIs? → Remove them
    - Does this file contain examples that only make sense for one target? → Generalize or remove
    - Would this skill still be useful if the next target were a completely different type of software? → If no, it does not belong here
    Target-specific content belongs exclusively in `targets/<software>/skills/`. No exceptions. A meta-harness skill contaminated with target-specific content corrupts the pattern for all future targets.
11. **curl-first** — prefer direct HTTP; use socket client for TCP bridges; MCP tools last resort
12. **Log every proven skill** — add to Implemented Skills Log when verified working
13. **Write a plan file for multi-phase work** — Whenever starting work that spans more than one phase or session, write a plan as a markdown file directly at `plans/current.md` inside the project. Do NOT use the EnterPlanMode tool — it requires manual user approval and breaks autonomous flow. Write the plan file yourself, update it as phases complete, and re-read it after context compaction before continuing. The plan is the source of truth for what's done and what's next.

15. **BLOCKING GATE — Document before moving on** — Any time you discover something new (a hard wall, a working pattern, a friction fix, a constraint, a rule that needs adding), you must write it into the correct file before taking the next action. Not after. Not at the end. Now. The moment you think "I should document that later" is the moment it gets lost. If you catch yourself about to move on without documenting, stop.

    What goes where:
    - Hard wall or working agentic path discovered → target's `CEILING.md`
    - New command or API behavior confirmed → target's relevant skill file
    - Friction solved → breadcrumb in the relevant skill + skill update
    - Pattern that applies to any software → meta-harness skill (software-agnostic)
    - Same mistake made 3+ times → new mandatory rule in the appropriate `CLAUDE.md`
    - Skill verified working end-to-end → entry in Implemented Skills Log

16. **BLOCKING GATE — Verify skills after writing** — immediately after writing or updating any skill, reinstall the bridge if changed, restart the target software, run through every step from scratch, confirm sonar signal at each step. Do not proceed to anything else until this passes. A skill not verified through a restart cycle is not complete and must not be called done.

---

## Implemented Skills Log

This section tracks every skill pattern successfully built and verified across software targets.
Each entry is a proven, transferable pattern. When starting a new software target,
scan this log first — an existing pattern may apply directly or with minor adaptation.

### Bridge Patterns

[2026-04-10] Maya 2026 | Bridge type: HTTP threaded (port 7777) | Key friction: Maya API not thread-safe — ALL calls must go through `maya.utils.executeInMainThreadWithResult()`. Bridge startup must use `executeDeferred` not direct call. | Skill: `targets/maya/bridge/`

### Sonar Patterns

[2026-04-10] Maya 2026 | State queries: REST endpoints (/scene/state, /scene/nodes, /scene/cameras, /scene/renderers) | Screenshot: ffmpeg x11grab captures OpenGL viewport; xwd misses GPU content | Home screen: `appHome -q -visible` to query, `appHome -e -visible 0` to dismiss | Key friction: Dual monitor — Maya is on monitor 2 (DP-2, virtual offset 0,2160); always crop screenshot to that monitor. ffmpeg x11grab required for GPU viewport capture. Workspace teleport (wmctrl -ia): wait 0.8s before screenshot. | Skill: `targets/maya/skills/state-readback/SKILL.md`

### Core Execution Patterns

[2026-04-10] Maya 2026 | Verified workflows: create poly/NURBS/lights, set attributes, assign materials (standardSurface preferred), set keyframes, new scene, save, render | Constraint map: renderers/cameras/node-types always queried at runtime via bridge GET endpoints | Key friction: appHome widget must be dismissed on every new scene — `cmds.file(new=True)` alone is insufficient | Skill: `targets/maya/skills/core-execution/SKILL.md`

### Constraint Map Patterns

[2026-04-10] Maya 2026 | Constraint discovery: bridge GET endpoints (/scene/renderers, /scene/cameras, /scene/node-types) return live values from Maya itself | Documented: renderers (mayaSoftware, mayaHardware2), 11 shader types, 14 texture types, 6 light types, 9 constraint types, 3 IK solvers, 6 non-linear deformer types, 3 boolean op codes, file formats (mayaBinary/mayaAscii/FBX/OBJ/Alembic), render format IDs | Key principle: never hardcode; always query at runtime since plugins like Arnold may or may not be loaded | Skill: `targets/maya/skills/constraint-map/SKILL.md`

### Domain Skill Patterns

[2026-04-10] Maya 2026 Animation | Keyframes, SDK (setDrivenKeyframe), expressions, bake, timeline control, frame rate | Key friction: none significant | Skill: `targets/maya/skills/animation/SKILL.md`

[2026-04-10] Maya 2026 Mesh Modeling | Smooth, extrude, bevel, boolean (polyBoolOp 1/2/3), merge, retopo, vertex xform, fill/bridge/merge ops | Key friction: none significant | Skill: `targets/maya/skills/mesh-modeling/SKILL.md`

[2026-04-10] Maya 2026 Deformers | Lattice, cluster, blendShape, nonLinear (6 types), skinCluster, skinPercent | Key friction: (1) lattice point access — use `cmds.xform(latShape + ".pt[s][t][u]")`, not setAttr on transform; (2) blendShape target names — use `cmds.aliasAttr(bsNode, q=True)` after source mesh deletion, `target=True` returns `[]` | Skill: `targets/maya/skills/deformers/SKILL.md`

[2026-04-11] Maya 2026 Skin Weights — Geodesic Voxel | bindMethod=3 requires two-step: skinCluster(bindMethod=3) then separate geomBind() — skinCluster alone does NOT compute geodesic weights. Key friction: (1) geomBind leaves stale selection — `select(clear=True)` before any skinCluster edit after geomBind; (2) skinPercent wildcard `vtx[*]` fails — use explicit range `vtx[0:N-1]`; (3) copySkinWeights influenceAssociation="closestJoint" for bilateral rigs (oneToOne pairs by index order, not spatial L↔R); (4) all joints must be inside mesh volume — verify extremities (hand_end, toe) before binding | Skill: `targets/maya/skills/deformers/SKILL.md`

[2026-04-10] Maya 2026 Rigging | Joint chains, IK (RP/SC/Spline), all 9 constraints, skin binding | Key friction: tangentConstraint requires NURBS curve target, not polyMesh | Skill: `targets/maya/skills/rigging/SKILL.md`

[2026-04-10] Maya 2026 Node Graph | DG wiring (connectAttr/disconnectAttr/listConnections), custom attrs (addAttr), texture→utility→shader→geometry patterns | Key friction: none significant | Skill: `targets/maya/skills/node-graph/SKILL.md`

[2026-04-10] Maya 2026 Scene Organization | Display layers, render layers, namespaces, file references, group hierarchies | Key friction: none significant | Skill: `targets/maya/skills/scene-organization/SKILL.md`

[2026-04-10] Maya 2026 Viewport Control | viewFit(camera_name), lookThruModelPanel via mel.eval, visibility, modelEditor display modes, playblast (viewer=False mandatory) | Key friction: viewFit takes camera name not panel name — get cam via `cmds.modelPanel(panel, q=True, camera=True)` first; render layer switching via editRenderLayerGlobals not reliable from bridge context | Skill: `targets/maya/skills/viewport-control/SKILL.md`

### Stress Test Results

[2026-04-10] Stress Test: Maya 2026 (Phase 6 pass 1) | Tasks tested: 10 (6 combinatorial + 4 ambiguous) | Failures: 0 | Skills updated during run: state-readback (appHome, ffmpeg, workspace teleport), curl-api-reference (full ceiling), constraint-map (all bounded fields), core-execution (all primary workflows), self-improving (breadcrumbs) | Zero-error run: achieved | User asks: 0

[2026-04-10] Stress Test: Maya 2026 (Phase 6 pass 2 — full skill set) | Tasks tested: 16 (12 combinatorial + 4 ambiguous) | Failures found during verification: 4 (all fixed before final run) | Final run: zero failures | User asks: 0 | Friction found and fixed: (1) nonLinear returns [deformer, handle] not [handle, deformer] — deformers skill fixed; (2) listRelatives allDescendants → use ad=True — rigging skill fixed; (3) lattice returns [deformer_ffd, lattice_transform, base_transform] — deformers skill fixed; (4) keyTangent type "smooth" invalid — valid set is auto/clamped/fixed/flat/linear/plateau/spline/step/stepnext — animation skill fixed | Combinatorial coverage: SDK+expression on same object, boolean→bevel→smooth pipeline, lattice+blendShape on same mesh, joint+IK+poleVector+parentConstraint, texture→utility→shader→geometry DG chain, namespace+layer+reference, frame+playblast, rig+skin+animate+playblast, query-first render, custom attr driving constraint blend, save+reference, vertex edit+retopo | Ambiguous: "Rig this character mesh", "Animate this object", "Clean up the scene", "Set up lighting"

[2026-04-11] Stress Test: Maya 2026 (Phase 6 pass 3 — MASH fix + ambiguous tests) | Tasks tested: 16 (12 combinatorial + 4 ambiguous) | 1 friction fixed: MASH_Random.amplitudeX does not exist — correct attributes are positionX/Y/Z, rotationX/Y/Z, scaleX/Y/Z, randomSeed, Envelope — CEILING.md updated | Final run: zero failures | User asks: 0 | Ambiguous tests resolved: "Rig this character mesh" → spine joints + skinCluster + IK; "Animate this object" → bounce + spin keyframes over 48 frames; "Clean up the scene" → freeze transforms + center pivots + MLdeleteUnused; "Set up lighting" → three-point rig (key/fill/back directional lights with temperature-appropriate colors)

[2026-04-18] Stress Test: DaVinci Resolve 20.3.2.9 (Phase 6 pass 1) | Tasks tested: 12 (8 combinatorial + 4 ambiguous) | Failures: 0 | Zero-error run: achieved | User asks: 0 | Friction found and fixed: (1) GetRenderCodecs lists hardware-unavailable codecs (AV1 NVIDIA) — constraint-map updated; (2) superScale requires int not string — constraint-map updated; (3) Export() returns True on silently failed EDL — render-pipeline updated | Combinatorial coverage: project lifecycle+timeline+export(4 formats)+save/close/load, tracks+markers+7-page navigation, media pool folder CRUD, project settings+render format/codec+preset, insert generators+26 properties+colors+flags+item markers, 3 timelines+track management+switching, render format discovery+codec iteration+render mode, export multi-format+rename+save cycle | Ambiguous: "Set up a new project for a 1080p edit", "Export this timeline for another editor", "Organize the media pool for a multi-scene shoot", "Prepare the render settings for web delivery"
[2026-04-25] Stress Test: DaVinci Resolve 20.3.2.9 (Phase 6 pass 2 — skill correction run) | Tasks tested: 12 (8 combinatorial + 4 ambiguous) | Failures: 0 | Zero-error run: achieved | User asks: 0 | Friction found and fixed: (1) InsertGeneratorIntoTimeline lives on Timeline not MediaPool (F010, DRV022) — timeline-edit skill fixed [CONFIRMED]; (2) CloseProject returns False on open project (F011, DRV024) — project-database skill fixed, use LoadProject instead; (3) GetAlbumName lives on Gallery not Album object (F012, DRV023) — color-grading skill fixed [CONFIRMED]; (4) Fusion comps lazy-created on media clips (DRV025) — fusion-compositing skill fixed; (5) Render presets may set software codecs not in hardware list (R015) — render-deliver skill fixed | All 9 domain skills promoted from Evidence-grounded to Verified | Combinatorial coverage: project lifecycle+timeline+export+save/close/load, tracks+markers+7-page navigation, media pool folder CRUD, project settings+render format/codec+preset, insert generators+properties+colors+flags+markers, 3 timelines+track management+switching, render format discovery+codec iteration, export multi-format+rename+save cycle | Ambiguous: "Set up a new project for a 1080p edit", "Export this timeline for another editor", "Organize the media pool for a multi-scene shoot", "Prepare the render settings for web delivery"

<!-- Add entries here as stress tests complete -->
<!-- Format: [DATE] Software: <name> | Tasks tested: <N> | Zero-error threshold reached: <yes/no> | Notes: <key findings> -->
