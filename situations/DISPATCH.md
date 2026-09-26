# DISPATCH — the build org as a quilt

*How SuperInstance is **staffed**. [`METHODOLOGY.md`](METHODOLOGY.md) says how we
build; this says who builds, at what power, and how the work is routed. The org is
not a hierarchy drawn as boxes — it is a **quilt**: every dispatch is a typed cell
booked into a double-entry ledger, routing is by earned standing, and waking the
expensive tier is gated by a deadband. The spreadsheet is
[`dispatch-ledger.csv`](dispatch-ledger.csv) — the append-only WAL of who did what,
why, and what it cost. Replay ≡ live: the ledger tells us exactly why any piece of
work happened.*

## The tiers (three power levels, one dispatcher)

| tier | model | role | cost class | woken | earns |
|---|---|---|---|---|---|
| **Architecture / top management** | **Opus 5.5** | pressure-tests the design, sets the architecture a build team executes, makes the irreversible/cross-cutting calls | **8** (expensive) | **sparingly** — only past the deadband (a genuine architectural fork, an outward/irreversible action, a law-level change) | — |
| **Build team** | **Sonnet 5** | executes an architecture into shipped, tested code; the standing workforce | **3** | per project | **standing** on a task-class after N booked-correct |
| **Runner** | **Haiku 4.5** | low-power grunt work — search sweeps, test running, format/lint, mechanical edits, batch checks | **1** (cheap) | freely, in **parallel batches** | standing on narrow, well-specified runs |
| **Dispatcher** | *me* | routes work to the cheapest tier that can pass its acceptance test; books every dispatch; wakes Opus only past the floor | **1** | always on | — |

The dispatcher is a **cell**, not a boss: it makes one typed decision — *which tier,
and why* — and books it. The "why" is a **JEV verdict** (below). It never does the
build team's work; it routes and books.

## Routing is a verdict (the same four the substrate uses)

Every dispatch decision names *why* the tier was chosen, in the kernel's own verdicts:

- **ESCALATE → Opus.** The decision clears the deadband: a novel architecture, an
  irreversible or outward-facing action, a change that touches a law or crosses many
  modules. Rare by design.
- **ACT → Sonnet.** A well-shaped build with a known architecture. The default for
  real work.
- **ANSWER → Haiku (unsupervised).** A task-class a runner has **earned standing** on
  (a streak of booked-correct); recall the proven procedure, don't re-supervise. One
  miss revokes standing and the class drops back to ACT.
- **CONFIRM → cheap tier, checked.** Run it low-power but book a check before trusting
  the result — the calibrated middle when the sea is a little rough.

## The five laws, applied to the org

1. **Identity never floats.** Cost is an integer class (8/3/1), not a vibe. A dispatch
   has an exact id and an exact tier. No fuzzy "senior-ish."
2. **Deadband before waking Opus.** The single most important calibrated decision.
   Ordinary chop — a bug, a doc, a well-specified feature — never wakes the expensive
   tier. Only a real change of altitude clears the floor. (Law 2 + R1.)
3. **Decide-one-pass, project elsewhere.** The dispatcher decides the tier once and
   hands down a self-contained spec; it does not hover and re-decide mid-build.
4. **Every dispatch is booked; replay ≡ live.** The ledger is append-only. We can
   replay why any rung got built, by whom, at what cost. Un-booked side work is a bug.
5. **Viability binary, difference graded.** A dispatch either passed its acceptance
   test (viable) or did not; *how well* is graded separately and feeds standing.

## Reverse-actualizing the optimizations

**Ideal end-state (the 2036 self-dispatching fleet).** Every task flows on its own to
the cheapest tier that can pass its acceptance test. Opus wakes only at true forks and
its wake-rate falls as the commons of solved architectures grows. Runners earn standing
and run unsupervised until a miss revokes it. Every dispatch is booked and replayable.
The org's own efficiency is a *booked, improving quantity* — the org optimizes itself
the way the software does. Nobody triages by feel; triage is physics.

**The ladder compiled back to today** — each optimization tied to a law/rung, each with
a predicate that says it's working:

| # | optimization now | grounded in | working iff (predicate) |
|---|---|---|---|
| O1 | **Deadband on Opus** — don't wake the expensive tier below the complexity/novelty floor | Law 2, R1 | Opus-wake rate falls over time while acceptance-test pass-rate holds |
| O2 | **Standing-based routing** — a runner past N booked-correct on a class gets ANSWER (unsupervised); one miss revokes | R2 standing | share of tasks run unsupervised rises with no rise in escaped defects |
| O3 | **Commons of solved dispatches** — reuse a prior architecture instead of re-asking Opus | R2 commons | repeat architecture-questions to Opus trend to zero |
| O4 | **Calibrated escalation floor** — tighten supervision on novel/stormy projects, relax in routine calm | R1 | supervision spend correlates with project novelty, not with calendar |
| O5 | **Booked double-entry dispatch** — every hand-down (debit) and result (credit) is a ledger row | Law 4 | 100% of shipped work traces to a booked dispatch; replay reproduces the org's history |
| O6 | **Batch the cheap tier** — Haiku runs go out in parallel, never one-at-a-time | efficiency | wall-clock per batch ≪ Σ serial run times |
| O7 | **Metabolism** — token-cost is a conserved budget; a tier that spends more than it returns in passed tests gets throttled | R5 | cost-per-passed-acceptance-test falls quarter over quarter |

## Failure modes (and their guard)

- **Waking Opus for chop.** → O1 deadband; the expensive tier is the exception, not the reflex.
- **A runner acting on stale standing.** → O2 revocation on one miss; O4 floor re-tightens when the class's sea changes.
- **Un-booked side work.** → O5; if it isn't in the ledger it didn't happen (and can't be replayed).
- **Goodharting the cost metric** (going cheap to look efficient while defects escape). → O7 measures cost *per passed acceptance test*, not raw cheapness; O2 counts escaped defects.
- **The dispatcher doing the build.** → the dispatcher is a routing cell; it decides the tier and books it, then hands down a self-contained spec.

## Dual track (of course)

- **Toy.** A family at a table with three colored tokens — gold (Opus, use once, it's precious), blue (Sonnet, the workers), white (Haiku, cheap and many) — and a chore list. The game is *routing*: never spend gold on a chore a white token can do; a worker who nails the same chore three times earns a "just do it" badge (standing); write every hand-off on an index card so a stranger can rebuild who did what (the ledger). A kid learns triage-as-physics in an afternoon.
- **Industrial.** This document + the booked `dispatch-ledger.csv`, driving real Opus/Sonnet/Haiku subagent calls under the deadband and standing rules, every dispatch content-addressed and replayable.

Same law both sides: *route to the cheapest tier that can pass the test, wake the
expensive tier only past the floor, and book everything so the org can replay itself.*

---
*Companion to [`METHODOLOGY.md`](METHODOLOGY.md) and [`GAPS.md`](GAPS.md). The ledger
is the live artifact; this is its law.*
