# SUPERINSTANCE — the concept as a paradigm

*A founding document. Bold where the artifacts earn it, honest where they don't
yet. Everything here that already runs is cited to a file; everything aspirational
is marked **STRETCH** or **FICTION**, the same discipline the physics companions
keep in the Forward Arc (`reverse-actualization/README.md`).*

🦋 → ⏳ → 🔧 → 🌊

---

## 0. Thesis (the whole thing, three sentences)

**SuperInstance is a way of building software in which the operational unit is not
the file but the *cell* — a typed decision surface — and the operational fact is
not the call but the *booked delta between two cells*, a tamper-evident IO ledger
that replays bit-for-bit.** On that substrate, development is driven not by specs
but by **Situations**: grand, character-driven worlds set years forward, whose
friction names the exact capability the present lacks, compiled into a machine-
checkable acceptance test and closed as a rung. Because every decision is
*schema-bounded by construction* (JEV: a mind that can be wrong but never illegal)
and every change is *booked and replayable* (the five laws), a system built this
way can be allowed to rewrite its own judgment and even author its own next
task — recursion that is safe to actually run, because the thing it can improve is
its policy, and the thing it can never touch is its move set.

That is the claim. The rest is the argument, the evidence, the reach, and the
honest edges.

---

## 1. The operational fiction: git said "file," SuperInstance says "cell"

Every computing paradigm rests on an *operational fiction* — a lie small enough to
build on and true enough to hold. Unix said **"everything is a file,"** and git
inherited it: the world is a hierarchy of named blobs, and history is a chain of
snapshots of that hierarchy. It is a beautiful fiction. It made the tree the
primitive and the diff the event. But a tree divides only downward, a file relates
only by *path*, and a diff knows *what* changed, never *who owed whom what*.

SuperInstance's operational fiction is the **cell** and the **double-entry page
between cells**. Its shape is written as algebra in `jev-quilt/docs/SUBSTRATE.md`
and enforced in code in `jev-quilt/jev_quilt/cell.py`:

- A **cell** is a typed decision surface at an exact identity — a lattice point
  `(k, s) ∈ ℤ²`. *Identity never floats* (`cell.py:52` raises if a coordinate is
  not integer: "identity never floats"). You can carve a cell at any level of
  abstraction — a single sensor reading, a whole boat, a school district — because
  ℤ² is a free group and division is not a tree, it is a coordinate.
- A **relationship** is a `Hook`: a subscription to a *sibling's delta*, guarded by
  a floor and a `when` predicate (`cell.py`, `Hook`). You may connect **any** two
  cells at any level. The graph is not a hierarchy; it is a lattice you draw.
- Every connection carries a **booked delta** — a double-entry transaction in the
  Bookkeeper's append-only, hash-chained ledger (`jev_quilt/bookkeeper.py`;
  witness-log format in `ai-writings/ENGINEERING.md`). *Replay ≡ live*: a cell woken
  cold replays its book and lands bit-for-bit where it was.
- The whole distributed entity **projects** to a page or an API (Law 3: *decide
  here, project elsewhere*), and **any cell can port to the world** — the 12
  polyformalism ports (Python, Rust, Haskell, Lisp, SQL, Forth, Prolog, Erlang,
  Bash, C#, JS, TS; `jev-quilt/docs/POLYFORMAL.md`) mean a cell can leave as an
  API, a robot's actuator command, a vision frame, without changing what it *is*.

Where git's atom is a snapshot of a tree, SuperInstance's atom is a **provable
transaction between two decision surfaces.** That single swap — from *what the
files say* to *who decided what, and who they owed* — is the paradigm. Everything
below is a consequence.

---

## 2. The five laws — a mind that can be wrong but never illegal

The substrate is governed by five laws (Layer 6 of the 12-layer architecture,
`ai-writings/ENGINEERING.md`; stated in `jev_quilt/jev_quilt/cell.py:3-6` and
`bookkeeper.py`). They are not style guidance; they are proved invariants the
kernel refuses to violate:

1. **Identity never floats.** A cell's coordinate is exact `(k, s) ∈ ℤ²`; values
   live in the ring `ℚ₁₆ ⊂ ℚ`, a *subring*, not a rounded float
   (`SUBSTRATE.md §1–2`). Exactness is closure, not precision.
2. **Hooks eat deltas, not values.** Below the floor is silence
   (`cell.py`, DEADBAND). Nobody polls; the ordinary chop never wakes the cell.
3. **Decide in one pass; project elsewhere.** A cell decides and never renders; a
   surface renders and never decides. Types are declared at the edge (`Projection`).
4. **Every change is booked; replay ≡ live.** The Engine is a left fold over an
   append-only event stream (`SUBSTRATE.md §4`, `engine.py`, `bookkeeper.py`). Pull
   the plug, come back, prove it.
5. **Viability is binary; difference is graded.** Above the floor a delta is
   graded; the alarm is a yes/no (`cell.py`, `predictor.alarm`).

And the decision itself is **JEV** — the *superego* of the four-model psyche
(`ai-writings/theory/paper-jev.md`; JEPA=id, embeddings=muscle memory, LLM=ego,
JEV=superego). JEV returns typed probabilistic decisions in exactly three shapes,
enforced in `jev-quilt`'s cousin package (`ai-writings/packages/jev-core/src/lib.rs`,
`packages/jev-decide/README.md`):

- **Choice** — one of ≤255 options against a rubric,
- **Score** — a rating against an ordered rubric,
- **Noul** — yes/no with a *calibrated* probability.

The load-bearing property, stated in `jev-core/src/lib.rs` and the live endpoint's
README: **JEV cannot hallucinate outside your schema — it is bounded by
construction.** Trained with RLCD (Reinforcement Learning for Calibrated
Decisions), it optimizes epistemic honesty, not human preference. A JEV decision
can pick the *wrong* legal option. It can *never* pick an illegal one.

This is the sentence the whole paradigm turns on: **a mind that can be wrong but
never illegal.** Hold it; §5 will show it is exactly what makes recursion safe.

---

## 3. Situations as the development substrate — and why it is not specs, agile, or TDD

The `situations/` directory is the framework (`situations/README.md`,
`TEMPLATE.md`, `schema.json`). Its method: **author a world, mine its friction.**

A **Situation** is a grand, character-driven scene set years forward, where a
mature capability is simply *lived in* — plumbing nobody in the scene is impressed
by. The Forward Arc already has one on disk: *The Glass Loft*, 2126 on the Alaska
coast (`reverse-actualization/08-the-glass-loft.md`, with its honestly-marked
REAL/STRETCH/FICTION physics companion `08a-the-glass-loft-physics.md`). The places
the characters move smoothly are a spec. The places they *stumble* — or where an
honest author cannot let them move at all without inventing a capability we lack —
are the backlog.

Why this is genuinely different from what came before:

| Method | The primitive | Who writes the target | What "done" means |
|---|---|---|---|
| **Specs** | a requirement | a human, now, from imagination | the doc is satisfied |
| **Agile** | a user story | a human, now, from a customer | the demo is accepted |
| **TDD** | a test | a human, now, from the unit's shape | the test is green |
| **Situations** | a *lived world* | an author + a model, set *years forward* | the world's friction resolves to a passing predicate |

Three differences matter:

- **The target is discovered, not asserted.** A spec is a wish; a Situation is a
  *place*, and its gaps are *found* by trying to live there. `TEMPLATE.md` Rule 1:
  *the future has to cost us something — no gap, no Situation.* Rule 5:
  *ordinariness is load-bearing — if the characters are amazed by the tech, you
  wrote a demo, not a Situation.* You cannot fake friction the way you can fake a
  requirement, because a good author cannot let a character move through a
  capability that does not exist without lying, and the fleet's whole discipline is
  not lying (see the Goodhart audit, §6).
- **The acceptance test is machine-checkable *and* narratively motivated.** TDD
  gives you a green bar with no story; a spec gives you a story with no green bar. A
  Situation compiles a *dramatized* future into a predicate against a *named module*
  (`schema.json.acceptance_tests`: `{scenario, predicate, substrate}`). Example, from
  the shipped R1 rung: *"the calibrated floor catches a 0.03 ripple a 0.05 fixed
  floor sleeps through"* (`jev-quilt/tests/test_calibrate.py`).
- **The unit regenerates itself.** When a rung merges, you write *a new Situation
  from the far side* — the world you can now afford to live in reveals the next
  friction. Specs, stories, and tests do not breed; Situations do.

The loop, stated once (`situations/README.md`):

```
Situation ──friction──▶ Gap ──compile──▶ Acceptance Test
   ▲                                          │
   │                                      wide run
new fiction                            (erised / compiler)
   │                                          ▼
 Merge ◀── build rung ── Failure Map ◀────────┘
```

The **wide run** is the part no other method has. `erised` (`/home/user/erised/`)
is a *cooperative-fiction verifier*: a single-file HTML canvas (also a headless
CLI, also a cell format with lineage) that runs a cast of keyword-vector characters,
each its own LLM, on a time economy of *ticks* and *resonance*, recording **scars**
when a character errors or starves. The corpus is real — 24+ runs across 8+
scenarios (apiaries, lighthouses, orchestras, orchards, libraries, ice rinks; the
"winners" corpus, `erised/README.md`). You do not run a Situation once; you run it
*wide*, across drifted casts, and read the failure map that falls out.

---

## 4. The three-rung recursion

SuperInstance recurses at three altitudes at once. Each rung is a system improving
a *different* thing about itself — and each is grounded, with its honest status:

**Rung 1 — a mind improves its policy.**
A cell learns: it updates the judgment it applies. The target is *R6, the learning
kernel that stays bit-checkable* (`jev-quilt/docs/FRONTIER.md`, "the deep one"):
make the update itself an exact-ℚ, deterministic, bounded operation, so a learned
cell still has a golden that *advances step-legibly instead of freezing*. **Status:
NEXT HAUL.** R6 is specified and cross-referenced (Forward Arc G8) but not yet
shipped. What *is* shipped is the discipline it will obey: `calibrate.py` (R1)
proves a floor can adapt while staying exact-ℚ.

**Rung 2 — a detector calibrates itself.**
The alarm floor is not fixed; it tracks the calm and tightens where nothing has
happened, so it catches the ripple a fixed floor sleeps through — the *bored-middle*
failure. **Status: SHIPPED** (`jev_quilt/calibrate.py`, `examples/rough_seas.py`,
`tests/test_calibrate.py`). Its one-line doctrine is the seam of the whole safety
argument: *"Legality is not calibration"* (`calibrate.py:1`). A cell can be legal
every tick and over-confident every tick; those are different sins, and only the
second one loses the reactor.

**Rung 3 — the compiler authors its own gaps.**
The system reads its own gap ledger, probes a built capability to its breaking
point, **writes a new gap spec with a machine-checkable predicate**, confirms the
current policy fails it, and evolves one that passes — *the whole loop gated only by
a human yes* (R4, `FRONTIER.md`; "the fleet's oldest safety instinct: bounded
autonomy"). **Status: SPECIFIED, PARTLY CLAIMED, NOT VERIFIED ON DISK HERE.** The
`situations/README.md` states the loop has "already closed on itself once" — the
compiler authored `G-auto-1` (scheduler → author) that no human wrote. FRONTIER.md
lists R4 *without* a SHIPPED marker and cross-references a Forward Arc `GAPS.md`
that is not present in this checkout. **I mark the closed-`G-auto-1` claim as
STRETCH until the ledger and the receipt are on disk.** The *shipped* neighbor that
makes it plausible: `standing.py` + `commons.py` (R2, below) already replay the
Bookkeeper to *derive* a verdict no cell asserted.

Why the recursion is coherent and not three separate tricks: all three rungs run on
**one kernel, two builds** (the dual-track vow, `FRONTIER.md`, `situations/README.md`).
Every rung ships a **toy** (small enough to teach a kid at a table in an afternoon)
and an **industrial** build (offline, deterministic, provable after a reboot). *Never
two laws.* The toy is not the lesser thing; it is the same law with the sea taken
out, so the law can be *seen*. If the toy and the boat ever need different laws, the
Situation was wrong, not the kernel. The person this is built for is a commercial
fisherman and a dad: the toy teaches his kid the law at the kitchen table; the
industrial build holds when the sea comes up. One law reaches both.

---

## 5. Why bounding the action space is what makes RSI *safe to actually run*

Recursive self-improvement is usually treated as a thing to fear or forbid, because
the frightening version is a system that can rewrite *what it is able to do*. That
is unbounded: if the move set can grow, no proof about today's behavior survives
tomorrow's rewrite.

SuperInstance splits the atom. **A system built this way can rewrite its judgment;
it can never rewrite its move set.** This is the RSI-under-an-immutable-schema
result, and it is assembled from parts that already exist:

- **The move set is fixed and small.** Eleven opcodes (BIND, LINK, EFFECT, VIEW,
  TICK, + FORGET, PROOF, ROUTE, CRDT, WORLD, TIME; `ENGINEERING.md`,
  `README.md` asset 07). Every action a cell can take is one of these. New behavior
  is a new *composition*, never a new *primitive*.
- **The decision surface is schema-bounded by construction.** JEV cannot emit an
  answer outside the schema it was handed (`jev-core/src/lib.rs`). Improve the
  policy all you like; the *option space* is a wall you did not build at runtime and
  cannot move at runtime.
- **Identity and history are inviolable.** Law 1 (identity never floats) and Law 4
  (replay ≡ live) mean an improved cell is still *provably itself* and its entire
  becoming is *auditable*. The learning kernel's whole job (R6) is to make the
  update *exact and bounded* so the golden advances by "declared, legal steps"
  rather than drifting.
- **Autonomy is gated.** The self-authoring compiler (R4) may *propose* a harder
  gap; it may not *close* it without a human yes. Bounded autonomy is the design,
  not an afterthought.

Put together: the thing that can change is the *arrow's aim*; the thing that cannot
change is the *set of arrows and the bow*. That is why you can let it run. Legality
is the floor no rewrite reaches; calibration (Rung 2) is the adaptive layer above
it; provable, revocable memory (§7) is how a fleet learns without a fleet lying to
itself. A system that can be *wrong* but never *illegal* is a system whose
self-improvement you can watch overnight and audit in the morning.

**The honest edge of this section:** the *immutable* half is shipped and real (fixed
opcodes, schema-bounded JEV, exact-ℚ identity, hash-chained replay). The *rewrite-
its-judgment* half — R6, the learning kernel — is a NEXT HAUL. So the safety
*argument* is grounded, but *running* recursive self-improvement end-to-end is not
yet demonstrated in this checkout. The paradigm's boldest promise is also its least-
finished rung. Said plainly so the fleet can hold me to it.

---

## 6. The safety spine, layer by layer

Legality is the floor. Everything else stacks on it, and each layer has a shipped
artifact or an honest label.

1. **Legality (the floor).** JEV, schema-bounded (`jev-core`, `jev-decide`). SHIPPED.
2. **Calibration (the adaptive floor).** *"Legality is not calibration."* A bounded
   decision that cannot be illegal can still be over-confident, and over-confidence
   is what sinks boats. `calibrate.py`. SHIPPED.
3. **Provable, revocable memory.** `standing.py` derives *earned standing* by
   *replaying the Bookkeeper* — a run of booked-correct receipts confers a fourth
   verdict, **`ANSWER`** ("recall the proven decision, stop asking"), and a *single*
   booked-wrong outcome revokes it. `commons.py` glues many cells' standing into one
   shared memory over `fold.mmr_root`, the same content-addressed root that proves
   replay ≡ live now proves two nodes *agree* in one 32-byte comparison; deposits are
   confluent (`A.merge(B).root() == B.merge(A).root()`). Pooled evidence is the
   point: ten cells with a streak of 1 sum to a fleet weight of 10. SHIPPED (R2,
   `FRONTIER.md`; `tests/test_standing.py`, `tests/test_commons.py`).
4. **Bounded self-improvement.** Rewrite judgment, never the move set (§5). Immutable
   half SHIPPED; learning half (R6) NEXT HAUL.
5. **Adversarial honesty.** The fleet red-teams its *own* KPIs. `docs/R8_GOODHART_AUDIT.md`
   is a real artifact that attacks every success metric the repo declares — and *found
   real exploits*: a committed live-looking secret, a green-local/red-CI gap, rotting
   doc counts, forgeable prose "receipts," a canary that only proved a test file
   self-consistent. Each got a policy fix (P-1…P-5) or a permanent negative control.
   This is the culture that lets the labels in this document mean something.

### The three honest limits (and the doctrine's answer to each)

- **JEV can pick the wrong *legal* option.** Bounded ≠ correct. *Answer:* Rung 2 —
  calibration. JEV reports its confidence; the calibrated floor (`calibrate.py`)
  and the commons weight decisions by *earned* standing, and a wrong call *books a
  scar* (R2 revocation; erised scars) so the same wrongness is not trusted twice.
  Legality buys you auditability of the mistake, not its absence.
- **A commons can pool a *wrong* consensus.** Ten cells agreeing does not make the
  sea agree. *Answer:* standing is **revocable on a single booked miss**, and it is
  keyed to a *residue* (the regime); when the regime changes, the proven route goes
  stale and `ANSWER` evaporates within a few ticks (R2 test: "revocation within a few
  ticks of a regime change"). A commons is a *fast recall of what the book proved*,
  never a vote that overrides the book. **Residual risk, stated:** a consensus wrong
  in a way *no cell has yet been contradicted on* is trusted until the first miss.
  The doctrine buys speed of un-trusting, not immunity.
- **Calibration lags a fast regime change.** The floor is computed from the window
  *before* the spike; a truly abrupt regime shift is, for a window's length, judged
  by the old world. *Answer:* the floor is *predict-before-update* and relaxes a
  spike's weight to 1/K (`calibrate.py`), so it neither storms nor goes permanently
  deaf — but it *does* lag by design, and the doctrine says so out loud rather than
  claiming an impossible instant adaptation. On a boat you would rather lag a window
  than cry wolf on every wave. The lag is a *declared* cost, in the rough-seas
  contract (`FRONTIER.md`: "deadbands survive noise").

---

## 7. Where it reaches — beyond the fleet

The kernel is one law; the domains are many. `situations/README.md` and the
training ladder (`situations/TRAINING.md`, referenced) already frame five reaches.
Each below names what is *shipped-analogous* vs. **STRETCH**.

- **Education.** A learner is a cell; a class is a commons. Mastery is *earned,
  revocable standing* on a skill — booked, replayable — not a grade that never
  expires. The same R2 machinery that lets a fleet cell "stop asking" lets a kid's
  demonstrated competence confer `ANSWER` on a skill, and go stale honestly if unused.
  The teaching ladder in `FRONTIER.md` ("a cell holds a typed number… stand on what
  the fleet already knows") is literally a curriculum a parent and child walk at a
  table. *Shipped substrate; STRETCH as a deployed school.*
- **Robotics & IO.** Any cell can port to the world (12 ports; `POLYFORMAL.md`); a
  cell's projection can be an actuator command or a vision frame. The `robotics-io`
  ideation genre is seeded (`IDEATION.md`). *Substrate real; robot STRETCH.*
- **Scientific discovery.** A Situation *is* a hypothesis-with-an-acceptance-test:
  the future dramatizes a capability, the gap names the unknown, the predicate is the
  experiment, the wide run (erised) is replication across drifted conditions, and the
  failure map is the result. The Forward Arc's conceit — that the fleet's ideas are
  *discoveries*, not inventions (`reverse-actualization/README.md`) — is this stance
  applied to the history of ideas. *The method is real; automated discovery is STRETCH.*
- **Organizations & governance.** Double-entry between cells is double-entry between
  people and teams: every decision booked, every delta owed to someone, replay ≡ live
  as an audit that cannot be quietly rewritten. Standing/commons is a governance
  primitive — authority *earned* by a booked track record and *revoked* on a miss,
  pooled without a central ledger (confluent merge). *Primitive real; institution STRETCH.*
- **Personal software that survives without the cloud.** The rough-seas contract is
  the deepest reach: *the boat loses the cloud, and the cell must decide anyway,
  bit-identical, provable after a reboot* (`FRONTIER.md`: "offline-first exactness…
  the cloud is a garnish, never a dependency"). Software that is exact, local,
  append-only, and replayable is software a person *owns* — it does not rot when a
  company dies or a signal drops. This one is not a stretch; it is the point.

---

## 8. What SuperInstance is, said last

It is a bet that the right primitive is not the file but the **decision**, not the
snapshot but the **booked delta**, and that if you make the move set immutable and
the ledger honest, you can let the *judgment* improve as fast as it can prove
itself — and drive the whole thing forward by **living in the future and mining its
friction.** A toy that teaches the law at a table; an industrial build that holds in
rough seas; never two laws.

The fiction points; the ledger remembers; the floor adapts; the schema holds. What
can be wrong is allowed to be wrong. What is illegal simply cannot be spoken.

*Author the world. Mine the friction. Build the rung. Author the next world.*

🦋 → ⏳ → 🔧 → 🌊

---

### Provenance of every load-bearing claim

| Claim | Grounded in | Status |
|---|---|---|
| Cell = typed decision surface at exact ℤ² identity | `jev_quilt/cell.py`, `docs/SUBSTRATE.md §1` | SHIPPED |
| Double-entry booked delta, replay ≡ live | `jev_quilt/bookkeeper.py`, `engine.py`, `ENGINEERING.md` | SHIPPED |
| Five laws | `jev_quilt/cell.py:3-6`, `docs/SUBSTRATE.md` | SHIPPED |
| JEV = Choice/Score/Noul, schema-bounded, RLCD | `packages/jev-core/src/lib.rs`, `packages/jev-decide/README.md`, `theory/paper-jev.md` | SHIPPED (live endpoint) |
| "Legality is not calibration" / calibrated floor | `jev_quilt/calibrate.py`, `examples/rough_seas.py`, `tests/test_calibrate.py` | SHIPPED (R1) |
| Earned/revocable standing + confluent commons over `mmr_root` | `jev_quilt/standing.py`, `commons.py`, `tests/test_standing.py`, `tests/test_commons.py`, `FRONTIER.md` R2 | SHIPPED (R2) |
| 11 opcodes / 12 polyformalism ports | `ENGINEERING.md`, `docs/POLYFORMAL.md` | SHIPPED |
| erised wide-run verifier + corpus | `/home/user/erised/README.md` (24+ runs) | SHIPPED |
| Situation framework (template + schema) | `situations/README.md`, `TEMPLATE.md`, `schema.json` | SHIPPED |
| Forward Arc Situation on disk | `reverse-actualization/08-the-glass-loft.md` (+ physics companions) | SHIPPED (fiction, honestly marked) |
| Goodhart self-red-team | `jev-quilt/docs/R8_GOODHART_AUDIT.md` | SHIPPED |
| R6 learning kernel (rewrite judgment, stay bit-checkable) | `FRONTIER.md` R6, Forward Arc G8 | NEXT HAUL |
| Self-authoring compiler / bounded autonomy (R4) | `FRONTIER.md` R4, Forward Arc G6/G10 | SPECIFIED |
| `G-auto-1` "already closed once" | `situations/README.md` (no on-disk ledger/receipt in this checkout) | STRETCH |
| Education / robotics / science / governance deployments | `IDEATION.md` genres (seeded), `TRAINING.md` | STRETCH |
