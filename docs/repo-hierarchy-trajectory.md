# Repo-Hierarchy Growth — A Possible Trajectory (not a spec)

How the multi-repo agent-tooling ecosystem *may* grow coordination structure over
time. This is a **compass, not rails**: a directional sketch held loosely, where
the actual shape is decided by real pressure when it arrives — not pre-committed
here.

Owned by Agent-Doctrine because this is governance (how the ecosystem is
organized), which is the standards/ancestral layer's concern. It does not build
anything; it records the trajectory and the triggers to watch for.

---

## Core principle

**Structure follows observable pressure.** You don't build coordination because
it's a nice-to-have; you build it when a specific, pointable signal makes it
necessary. Pre-defining the gates means that *when* pressure hits you escalate
**principled and fast**, instead of either improvising from zero or bolting on
machinery before it's earned. This is the Pressure-Lab philosophy applied to the
org itself — see `Pressure-Lab/docs/SCOUT_VERIFY_FIX_LOOP.md`.

---

## Two kinds of "parent" (resolving the ancestral-vs-emergent confusion)

The word *parent* does two unrelated jobs; keep them separate:

- **Ancestral / standards parent** — *precedes* its children and *defines* them;
  children derive direction from it. (Agent-Doctrine is this kind.) Does **not**
  emerge from children — design it up front. Test: *does it source the children?*
- **Coordinator / container parent** — groups children that already stand on
  their own and checks they *interoperate*; owns no craft authority. This kind is
  downstream and **can** emerge from felt need. Test: *does it just watch them?*

A folder/repo should be one or the other, never both.

---

## The VFX-studio model (the target shape, if it grows)

Two **orthogonal, parallel** chains — deliberately different roles:

- **Craft / authority chain** (Supervisor → dept supervisor → lead → senior →
  … → junior): the *ancestral/standards* axis. Sets direction + standards,
  reviews, approves. Higher = broader, more abstract, *fewer* decisions — **not
  more work.**
- **Production / coordination chain** (production manager → dept manager →
  coordinators): the *coordinator* axis. No craft authority; tracks dependencies,
  integration, and handoffs between disciplines.

Invariants from the model (these do **not** bend even as the trajectory does):

- **Higher layer = fewer/higher-level decisions, never more code.** A parent that
  accumulates work is mis-cast.
- **Layers emerge by span of control** — a new layer appears only when one
  overseer can no longer span the children, not on spec.
- **Children own their own work.** Authority flows down as direction + approval.
- **Dependency is one-way: parent knows children; children never depend "up."**
  Shared contracts live in a leaf both depend *down* on, not in the coordinator.
- **Folders aren't people with judgment** — a parent's authority must be encoded
  as *runnable gates that fail on drift*, not docs. A coordinator that doesn't run
  a check that can go red is decorative.
- **Lockstep components stay in ONE repo.** If two things must change together,
  git can't do atomic cross-repo changes — a coordinator just papers over the
  pain. Separate repos are for independent lifecycles + stable contracts.

---

## The escalation ladder (triggers firm, responses loose)

Each gate splits in two. **Commit only to the trigger.** The response is a
current best guess; when the trigger fires, **re-derive the response from the
actual pressure** (it may want a different shape, or to skip a step) and follow
that — then update this trajectory.

| Gate | TRIGGER (durable — watch for this) | RESPONSE (loose hypothesis — re-derive on trip) |
|------|-----------------------------------|--------------------------------------------------|
| **G0 — now** | — | Flat: independent repos, no parent. Only a manual *routing log* (note each cross-repo concern + why). |
| **G1 — first coordinator** | the same cross-repo check/fix is duplicated in ≥2 repos, **or** a cross-repo break ships undetected once | one integration/contract gate spanning those repos (executable, fails on drift) |
| **G2 — department split** | one coordinator can't span all children, **or** two disciplines need genuinely different standards | per-discipline coordinators |
| **G3 — top supervisor** | coordinators' gates start conflicting / a change must satisfy several at once | a cross-discipline standards layer (Agent-Doctrine-level authority) |
| **Automation (orthogonal)** | a coordinator's manual check recurs reliably K times | automate **that one check** only |

**A gate is "open" only when its specific signal has fired** — never "it feels
big." If you can't point at the signal, the gate is shut.

---

## Held loosely — this is a trajectory, not a plan of record

- The **trigger** is the part worth committing to ("pay attention here").
- The **response** is a hypothesis. Real pressure carries information this
  document can't have; when a gate trips (or pressure arrives in a shape not
  predicted here), follow the pressure and **edit this trajectory** to match.
- Treat divergence as expected and healthy, especially as complexity cascades.
  The map updating is the system working, not the plan failing.

---

## Current state

**G0.** Many independent repos under `<workspace root>`; no coordinator repo
exists and none should be built yet. The only coordination is manual. The next
move is *not* to build G1 — it's to notice (and log) whether a G1 trigger ever
actually fires.

## Through-line

Same lesson as the scout/verify/fix loop and the line-of-fixes that preceded it:
**coordination and structure count only when enforced by something that can fail —
never when merely declared, and never built ahead of the pressure that earns it.**
