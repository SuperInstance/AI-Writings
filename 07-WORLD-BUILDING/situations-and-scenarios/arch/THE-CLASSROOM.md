# THE CLASSROOM — from a GAN-pair to a class of many, taught by a self-modifying teacher

*Opus 5.5, deep ideation, blinders on: the owner's vision developed into a real
architecture. Generative, apex-adjacent — it goes far — but it keeps the corpus's
honesty: every leap is tagged **STRETCH** (a leap past what the map proves) or
**grounded** (in shipped substrate or a verified fact). It builds no code; it is a
plan whose rungs each end in a predicate someone can run. Grounded in
[`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md) (P1–P6, S1–S7 — the classroom
is its generalization), [`../DISPATCH.md`](../DISPATCH.md) (O1–O12, the deadband, the
"light GAN" of O9), [`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) (Law 6, the Reader's
Fold), [`../ROSTER.md`](../ROSTER.md) (`jev-1.13.0`, MothQuantum), the cell model
(`cellular-first-design/code/openjev/cell.py`), and the two music-GAN repos surveyed
in §1. Do **not** commit — the dispatcher books.*

🦋 → ⏳ → 🔧 → 🌊

---

## 0. The thesis in one breath

**A GAN is a two-player argument that ends when one player is fooled. A classroom is an
N-player argument that ends when the *class* can no longer be fooled — and the teacher
is not the class's adversary, it is the *pedagogy* that keeps the whole class at the edge
of what it cannot yet do.** Generalize duke-lab's generator/critic pair into many
frozen students + one teaching cell whose method starts from proven human pedagogy and
*modifies itself* from how the class is responding; express the whole thing in
jev-quilt terms (students, teacher, lessons as cells; pedagogy as booked hooks; the
course as a WAL that replays exactly; each student folding the lesson under its own
weights, Law 6); bootstrap it with `jev-1.13.0` as the exam proctor, MOTH as the honest
dice, and fast tiny models raising their own floor; and let the logic decompose out of
the cell bodies into the *relations between* cells until what steers the class is not a
weight-delta inside any model but an **exo-model LoRA** — a low-rank *relational*
adapter carried by the quilt that steers a class of frozen models without touching one
weight. That last object is the payoff, and it may be a second-Fable candidate (§9).

---

## 1. The music-GAN history — what actually exists, honestly (grounded)

I cloned and read what I could. **`duke-lab` cloned clean** (`git clone
SuperInstance/duke-lab`); I read its `README.md`, `CANON.md`, and `engine.js`.
**`musicians-soul` is INACCESSIBLE from this session** — the clone failed on auth
(`could not read Username for github.com`) and `add_repo` returned *"you don't have
access to superinstance/musicians-soul."* I will not invent its contents; what I can
say about it is marked STRETCH below and rests only on its name and its pairing with
duke-lab.

### 1.1 duke-lab: a "GAN with words" (grounded, read from source)

duke-lab's own tagline: *"A GAN with words. A generator plays an unheard take; a critic
measures it against a sixteen-feature ruler; the argument converges in golden ratio —
until the critic can no longer tell whether this is a song he simply hasn't heard
before."* Read from `engine.js`, the machine is:

- **Generator** — a parameter vector in `[0,1]¹⁶` → a seeded take (melody / walking
  bass / comp events). Deterministic: `fnv1a` → `mulberry32`, one honest dice chain,
  *no hidden entropy*. "Grow the musician; the song is the receipt."
- **Critic ("the eye")** — a weighted **σ-distance to the *effective centroid*** (a
  4-take calibration at the canon, cached) over a **16-feature ruler**
  (`registerSpread … cadenceRegular`, each with a floor + a critic hint). "Judge the
  trace, not the summary" (the Summary Law).
- **Swappable loss** — a **persona/gardener** (Purist / Engineer / Romantic /
  Historian) is a *re-weighting of the 16-axis ruler*, and it is **swappable mid-run**.
  The loss function is a role a human names, not a jointly-trained head.
- **The golden residue** — the critique budget compresses toward `1/φ ≈ 0.618` per
  round (`max(1, round(3·φ⁻ʳ))`); the argument **converges in ratio, never in fact**.
- **Verdict** — EMA σ < threshold → `CONVERGED` ("I can no longer tell…"); else
  `HONEST GAP` with the **residue named**. A *medium floor* (Plainsong's
  one-velocity-per-row law) caps expressible axes, so the residue is *quantitative*,
  not hand-waved.
- **The v2 foundry** — every musician is a point in `[0,1]¹⁶`; finished runs POST
  matured params to `/api/learn`, which graduates them into a **musician-space** (a D1
  row + a native 16-dim Vectorize embedding + a 768-dim semantic embedding of the
  description). The **bandstand**: two matured musicians trade 8-bar phrases; the
  **banter score** (quotes ÷ responses) is fitness, and it goes in the ledger.

### 1.2 musicians-soul (STRETCH — inaccessible, conjecture only)

From the name and the duke-lab doctrine ("the asset is the musician — the parameter
walk; the song is the receipt"), `musicians-soul` *reads like* the sibling that holds
the **musician-as-asset** side — the matured parameter-walk ("the soul") that duke-lab
generates and grades. **This is unverified.** I could not read a single byte of it. If
the architecture below leans on it anywhere, that lean is STRETCH and must be re-checked
once the repo is accessible.

### 1.3 The pattern these systems actually share (grounded)

The honest finding, stated flat: **this family's "GAN" is not adversarial *training*.**
No weights move; there is no jointly-trained discriminator; nothing back-propagates.
What is shared across duke-lab (and the fleet's `O9` "light GAN inside the practice",
[`../DISPATCH.md`](../DISPATCH.md) "The wider feel") is a **generate-then-judge loop
with a separate, named, human-legible critic**, run **deterministically so it is
honest** (`replay ≡ live` — same seed, byte for byte), that **converges to a *named
residue* rather than to a fooled discriminator**. The critic is calibrated *apart* from
the generator — exactly the property [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md)
§P1 prizes in `jev-1.13.0` ("a gate that can't collude with the experts because it
wasn't trained jointly with them"). That decoupled, legible, replayable critic is the
seed the classroom generalizes — and it is also why the classroom is *buildable now*:
it needs no GPU, only frozen models and a booked substrate.

---

## 2. Classroom, not GAN-pair (grounded core, STRETCH generalization)

### 2.1 The reframe

A GAN is `G` vs `D`: one generator, one discriminator, one scalar of pressure
(fooled / not-fooled). Generalize each role.

- **A student** = a *frozen model + its book* — a **cell** in the exact sense of
  `cell.py`: `state`, `witness_log`, `hooks`/`drops`, `jev_confidence`, `scars`. A
  student folds each lesson's evidence under *its own weights* (Law 6, clause ii —
  sovereignty is the reader's π). The class is **heterogeneous** on purpose: the
  roster's deliberately mixed-capability cast (DeepSeek, DeepInfra Llama-8B,
  Hermes/Seed, Haiku) — because a class of clones has nothing to fold *across*
  (this bites in §8).
- **The teacher** = a **pedagogy cell**. It is *not* an adversary. Its objective is not
  to beat any one student; it is to **raise the class's floor** — maximize the count of
  students who reach mastery on a task-class, at least cost (the O7 metabolism reading
  of teaching). It emits **lessons** (a curriculum item + a *teaching method*) and
  **reads the class's response**.
- **The pressure** — where a GAN concentrates all pressure in one adversary, a
  classroom **disperses it into a field** with three components, none of which a
  student can overfit to:
  1. **The frontier (ZPD).** The teacher holds lesson difficulty just above the current
     class floor — R1's *calibrated floor, the ripple in the calm*
     ([`../METHODOLOGY.md`](../METHODOLOGY.md), `calibrate.py`). The floor *rises* as
     the class strengthens (this is [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md)
     S5's auto-curriculum, verbatim).
  2. **The peers (the bandstand).** A student one rung ahead is the cheapest teacher for
     one rung behind — duke-lab's bandstand (trade phrases, banter score as fitness)
     generalized to any task-class (this is the bootstrap of §5).
  3. **Novelty vs the commons (O9).** Rank a student's answer partly on *newness to what
     the class already holds*, so the class is not rewarded for restating itself — the
     "light GAN" made numeric ([`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md)
     §P6).

### 2.2 Why a class-of-many beats a pair (STRETCH — argued, predicate in §9)

1. **A distribution, not a scalar.** A pair yields one gradient (fooled / not). A class
   yields a *distribution of folds* over the same evidence, so the teacher can localize
   *which concept fails for which student*. This is Law 6's corollary as a teaching
   instrument: **`V(E, π₁) ≠ V(E, π₂)` is signal, not noise** — disagreement on the
   same lesson *localizes the seam* ([`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) §1.1).
2. **No mode collapse.** A GAN generator can collapse to the one mode that fools `D`. A
   class *cannot* collapse, because **mastery is per-student, per-class, booked and
   revocable** (§3, §4) — there is no single discriminator to satisfy, so there is no
   single mode to collapse onto.
3. **Free peer scaffolding** (2.1.2) — teaching cost per student falls as the class
   raises its own floor; the teacher spends where the frontier actually is.
4. **The method is itself under selection.** The deepest generalization: it is a
   **meta-GAN where the *pedagogy* is the generator and the *class's learning curve* is
   the discriminator.** The teacher proposes a method; the class's response critiques
   it; the teacher folds that critique into the next method (§3). The adversary of the
   old GAN has become the *teacher's own uncertainty about how to teach*.

---

## 3. Self-modifying pedagogy (grounded mapping, STRETCH on "learned")

The teacher's methods **start from proven human pedagogy** and each maps cleanly onto a
*shipped* substrate mechanism — that mapping is grounded:

| human pedagogy | substrate mechanism | grounding |
|---|---|---|
| **Scaffolding / worked-examples → faded** | commons exemplars in the stable prefix, *removed* as standing accrues | O2 standing, O3 commons, O10 stable prefix |
| **Spaced repetition** | re-surface a lesson when `jev_confidence` has decayed or a scar predicts a lapse | `cell.py` `jev_confidence`, `scars` |
| **Socratic** | the teacher asks `jev` **noul/score** questions instead of giving answers; the student's fold *is* the reply | `jev-1.13.0` `noul`/`choice`/`score` ([`../ROSTER.md`](../ROSTER.md)) |
| **Mastery learning** | a student advances only when it **reproduces the lesson to one root**, independently witnessed | G16 reproduction gate (`claim.py`) |
| **ZPD** | R1 calibrated floor: above mastered, below frustration; floor rises with competence | `calibrate.py`, S5 |

**The closed loop (this is the self-modification).** The teacher *measures the class's
response* — pass-rate, surprise, the spread of `jev` confidence, the amount of
disagreement (the seam of 2.2.1) — and *adapts the method*. This is exactly the
**situations loop** turned on pedagogy itself: **author a world (the lesson), mine its
friction (where the class stalls), compile the friction to a rung (the next method),
author the next world** ([`../METHODOLOGY.md`](../METHODOLOGY.md):288). It is also **O4**
(the calibrated escalation floor) generalized: *tighten the method on a stormy lesson,
relax it on a calm one* — supervision spend tracks lesson novelty, not the calendar.
And it is the fleet's **Free-Energy trigger** already noted in the substrate research:
*cognitive friction Φ > deadband → wake the Executive*
(`cellular-first-design/research/FLEET_ECOSYSTEM_SYNTHESIS.md`) — here the Executive is
the teacher re-choosing its method.

**Where "modify themselves" is grounded vs STRETCH — mark the line sharply:**

- **grounded / funded-now:** *in-context* self-modification — the teacher re-selects
  among a **library of proven methods** based on the measured response, and re-orders /
  re-weights the curriculum. No weights move; this is S5 (auto-curriculum) + S6 (config
  search over the method-selection policy) composed. Runnable this week on frozen
  models + the booked ledger.
- **STRETCH:** *genuinely learned* pedagogy — the teacher's method-selection weights
  actually move (a meta-policy trained on which method raised which class fastest). That
  is S7-shaped (moved weights) and needs a fine-tune surface the fleet has not confirmed
  ([`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md) §4, honest limits). The
  in-context version is the honest floor; the learned version is the reserved ceiling.

---

## 4. The quilt abstraction of the classroom (grounded — this is its generalization)

Express the classroom in jev-quilt terms, one object at a time:

- **Students, teacher, lessons are cells** — `state`, `witness_log`, `hooks`/`drops`,
  `jev_confidence`, `scars` (`cell.py`). Nothing new; the classroom is a *pattern over
  the existing cell*, not a new primitive.
- **Pedagogy is booked hooks.** A teaching method is a **hook** — an incoming connection
  with a *condition* (`add_hook(source, condition)`): *"when the class response matches
  C, apply method M."* The hook is content-addressed and booked; the method is
  replayable, not a vibe. Faded scaffolding = a hook whose condition is *"standing < N"*
  that stops firing once earned.
- **The class's learning is a WAL where `replay ≡ live`.** The whole course re-derives
  from the ledger; a stranger replays the class and gets the **identical learning
  curve** (Law 4). This is the single line that makes the classroom an *experiment* and
  not a demo — [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md) §3.1's
  "recomputable by a stranger" applied to teaching.
- **Law 6 governs what the teacher may hand a student.** The teacher **never carries a
  verdict** ("here is the answer"); it carries **evidence** (worked examples, Socratic
  questions, the pooled class working) and **each student re-folds under its own π**. The
  class's aggregate competence is the **aggregate of the folds, not a vote** — P4,
  exactly.

**The classroom is the generalization of [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md)
— tie them, one to one:**

- **aggregate folds → pedagogy.** S2's **Reader's-Fold ensemble** (each model re-reads
  the *pooled evidence* and re-answers) **is peer learning**. The teacher's whole job is
  to choose *which evidence to pool, and in what order* — and **that ordering is the
  curriculum**. Pedagogy, precisely, = *the policy over what evidence is exposed to whom,
  when.*
- **reproduction-gate → mastery.** G16 (a cheap model earns a class only when an
  independent reader reproduces it) **is mastery learning**. S1/S7's gated distillation
  set is the *graded homework that earns promotion* — a student advances on reproduced
  work, never on seat time.
- **JEV two-floors → grading legality vs understanding.** S4's two floors map to two
  grades: **legality** (well-formed, on-canon, confident — `jev` `noul`/`score`) vs
  **understanding** (passes the correctness floor / reproduces). The four quadrants are
  a *report card*: fluent-and-wrong (legal, not mastered), right-but-off-method
  (illegal, mastered), and the two diagonals. **A classroom that grades both refuses to
  promote fluent nonsense** — the anti-Goodhart spine of teaching, which is S4's whole
  point.

So: the classroom does not *add* machinery to INTELLIGENCE-CLUSTERS. It is S1
(gated distillation = homework), S2 (fold ensemble = peer learning), S4 (two floors =
report card), S5 (auto-curriculum = the frontier), S6 (config search = method
selection) **composed into one story** — with the teacher as the cell that runs the
composition. That composition is the architecture.

---

## 5. JEV + Moth + tiny models bootstrapping (grounded roles, STRETCH result)

### 5.1 The three actors, roles inferred from verified facts only

- **`jev-1.13.0` — the exam proctor** (grounded, verified live in
  [`../ROSTER.md`](../ROSTER.md)). It is *System One*: `POST /v1/systemone` takes a
  `state` + named `noul`/`choice`/`score` questions and returns answers *with
  confidence*. It certifies a rung as **legal and confident** — the **legality floor**.
  It **cannot grade arbitrary ground truth** (P5), so it is the *proctor who checks your
  work is well-formed and that you're sure of it*, **not the answer key**. Using it as
  the answer key would be the exact error S4 exists to prevent.
- **MOTH (`mothquantum`) — the honest dice, and (in the music domain) the raw-material
  generator** (roles *inferred*, API *not fabricated*). [`../ROSTER.md`](../ROSTER.md)
  verified: MOTH is **not an LLM** — it is a *creative-engines* platform with quantum-RNG
  (`comet-qrng-v1`) and generative-media engines (`qrc-midi-v1`, `qrc-audio-v1`, image
  engines), tied to the owner's own player account (`MOTHQUANTUM_KEY`/`_BASE` live). Two
  honest roles, neither inventing an endpoint:
  1. **The dice (general).** True hardware randomness for the seeded curriculum, the
     self-play cast selection, the exploration draw. duke-lab uses a *PRNG* for its
     "honest dice"; a **quantum-RNG makes exploration genuinely un-gameable** — you
     cannot overfit to a seed you cannot predict. This matters for the anti-Goodhart
     frontier (S5): a curriculum drawn from true randomness cannot be reverse-engineered
     by a student.
  2. **The generator of raw takes (domain-specific).** In a *music/media* classroom,
     `qrc-midi`/`qrc-audio` generate candidate takes and the class critiques them — which
     ties the classroom straight back to duke-lab's own domain (§1). Mark this role
     **domain-specific**; the dice role is general.
- **Fast tiny models — the students who raise their own floor.** A small model
  teaches/grades a smaller one; the class lifts itself rung by rung.

### 5.2 The bootstrap ladder (grounded mechanism, STRETCH that it works)

The mechanism is **G16 reproduction as the trust gate**, and it is grounded:

> A tiny model's answer becomes a **certified rung** only when **`jev` scores it legal**
> (proctor) **AND a second independent reader reproduces it to one root** (G16). Once a
> rung is certified, the *next* tiny model may **take it as given** and build on it —
> without re-deriving it from scratch.

That is the whole point of G16 reproduction as a *trust gate*: **the exam (JEV + a
second reader) is what lets the class trust its own prior rungs.** Rung *k* certified →
rung *k+1*'s students stand on it. The class **bootstraps its own floor**: a small model
teaching a smaller one is safe *only because the certification is independent of the
teacher* (Law 6 — no carried verdict; the smaller model re-folds, and a second reader
reproduces). This is the fleet's `any-quilt-does-rsi` intuition
(`philosophy/any-quilt-does-rsi.md`) made disciplined: recursive self-improvement that is
**gated by reproduction**, so a wrong rung cannot silently propagate up the ladder.

**Honest tag:** the *mechanism* is grounded (JEV live, G16 shipped, the gate is code).
**Whether tiny models actually raise a held-out floor this way is a wager, not a fact**
— it is S1's and S5's open predicate (`solo_with_commons.passrate > solo_cold` and the
auto-curriculum lift). If those bars come back red, the ladder is real machinery that
did not climb, and we say so.

---

## 6. Logic → relational weights: less intra-cell processing (STRETCH direction, grounded seed)

The owner's claim: *as logic decomposes into more and more relational weights, each cell
needs less processing — computation migrates from inside a cell into the relations
between cells.*

**Ground it in the cell model, then develop it.** Today (`cell.py`, grounded) a cell
does real **intra-cell work**: `proof()` calls JEV per claim, `tick()` snapshots state,
`forget()` scars, the body runs procedures. The `hooks`/`drops` carry connections, but
the **decision happens in the body**. The owner's shift is to **move the decision onto
the edges**:

- A **hook stops being "an incoming connection"** and becomes a **learned relational
  weight** — the edge itself carries a fold (who is bound to whom, with what weight,
  under what condition). When enough logic lives in the *graph of hooks*, the **cell body
  shrinks to almost nothing**: it holds state and replays; **the computation is the
  graph**. A cell becomes closer to a *table row* (state + book) than a *process*.

This is **Law 6 read structurally.** The verdict is *never in the cell* (not carried);
it is *recomputed from the evidence + the reader's π*. And π is *already an edge
property* — the trust map is literally `source → weight` (`commons.py` G11,
[`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) §1.2). So **"the fold" is a function of the
edge weights, not the cell body.** Aggregating folds not votes (P4) means the answer
emerges from *the trust-weighted graph of who-folded-what* — i.e. **from the relational
weights.** The owner's claim is therefore the *substrate-level statement of P4*:
decomposing logic into relational weights = *ceasing to compute verdicts inside cells,
and computing them from the trust-weighted graph of evidence instead.*

**What it means for the substrate:** a shift from **procedural cell bodies**
(`proof`/`tick`/imperative) to a **learned relational structure** (a GNN-like fold over
the hook graph carries the computation). It is also *why it is cheaper*: expensive
intra-cell JEV calls are replaced by **cheap arithmetic folds over booked edge weights**
— which is O7 metabolism (cost falls) and O10 (the shared graph is the stable prefix,
cheap to serve).

**Honest tag: STRETCH direction.** The current substrate still runs real logic in cell
bodies (`cell.py` `proof()` calls JEV per claim). The relational-weight version is a
research direction, not shipped. **The smallest grounded rung Opus can specify without
Fable:** take *one* class of decision now made in a cell body (e.g. "should this delta
wake work?") and replace it with a fold over the neighbours' booked weights; measure
intra-cell JEV calls before/after at held pass-rate. Predicate: *calls-per-tick falls,
pass-rate holds.* That converts the owner's aspiration into a red/green bar.

---

## 7. Distributed pre-pass filtering on the porting (grounded seed at the routing layer, STRETCH at the cell port)

The **port** is the cell boundary; **filtering on the porting** is the hook
condition / deadband / projection that decides what crosses it. The owner's claim: this
filtering becomes **distributed and part of a pre-pass** — done once, up front, across
the graph — so there is **less intra-cell work at runtime.**

**Today, runtime (grounded).** A hook has a condition evaluated *per delta arrival*; the
**deadband** (O1; the Free-Energy `Φ > deadband` trigger,
`FLEET_ECOSYSTEM_SYNTHESIS.md`) decides whether an arrival is worth waking work; the
bookkeeper wakes on delta arrival. Each cell, each tick, re-evaluates its port
conditions — *intra-cell, runtime* filtering.

**The shift is a compile-time-vs-runtime split** — the honest database analogy:

- **The pre-pass (compile-time), computed once over the whole quilt and booked as a WAL
  entry so it replays:**
  - **dead-hook elimination** — which hooks can *ever* fire;
  - **deadband placement** — where the `Φ` floor sits, derived from booked standing, not
    re-reasoned each tick;
  - **projection pushdown** — project each cell's schema onto *only the fields its
    neighbours actually read* (the fleet's `spreadsheet-projection`, "spectral graph
    projections of cell state", `FLEET_ECOSYSTEM_SYNTHESIS.md`).
  This is a **query planner pushing filters down to the scan** — computed once, booked,
  replayable.
- **Runtime:** a cell carries the pre-computed filter; a delta arrives *already knowing*
  whether it crosses. No per-tick re-evaluation, **no intra-cell JEV call to decide
  relevance.** The filtering has become a **property of the graph** (a relational weight,
  §6), computed up front.

**Connect to what already ships (grounded):** the substrate *already does pre-pass
filtering — at the routing layer.* The **deadband** (O1, "don't wake the expensive tier
below the floor") is exactly a filter placed at the port and computed from booked
standing, not re-reasoned each time. **O2 standing-routing** is a pre-pass: a runner past
N booked-correct gets `ANSWER` *without re-supervision* — `route == standing.verdict(
from_book(prefix))` ([`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) §1.2, `orgbook.py`). The
route (the filter) was computed from the book, up front. **The owner's claim is to push
this same discipline *down from the dispatcher to every cell port*** — predicate
pushdown + materialized projections + a booked, replayable query plan.

**Honest tag:** the routing-layer pre-pass (O1/O2) is **grounded and shipped**; the
**general pre-pass compiler over the hook graph is STRETCH** — a real direction with a
shipped precedent, not a built artifact. Smallest rung: compile the port filters for one
small quilt once, book the plan, and show runtime port-condition evaluations drop with
`replay ≡ live` preserved.

---

## 8. The exo-model as a fundamentally different kind of LoRA (STRETCH synthesis, grounded parts)

This is the payoff, and the sharpest claim in the document.

**Conventional (in-weight) LoRA** is a low-rank weight delta `ΔW = BA` *inside* a frozen
model. It lives in that model's parameter space; it steers *that* model; to move it to
another architecture you retrain; the weights are opaque, so it is not booked, not
legible, not revocable per-reader.

**An exo-model LoRA lives *outside / between* models, carried by the quilt.** It is *not*
`ΔW` on any model's weights. It is the **triple**:

> **exo-model LoRA = (the pre-pass port filter §7) + (the pedagogy §3) + (the trust map,
> G11)** — a low-rank **relational** structure over the *graph of frozen models*, not
> over any one model's weights, that steers a whole *class* of frozen models without
> touching one weight.

Each of the three parts is grounded (they ship). **The synthesis — naming them as one
portable object — is the STRETCH leap**, and it is the generative core of this document.

### 8.1 The contrast, drawn sharply

| | in-weight LoRA | **exo-model LoRA** |
|---|---|---|
| **where it lives** | inside one frozen model's params (`ΔW=BA`) | outside/between models — the quilt's hook graph + trust map + curriculum |
| **what it adapts** | one model | a **class** of heterogeneous frozen models |
| **how it applies** | matrix add at inference | evidence routing + fold under π + pre-pass filter |
| **dimension it moves in** | the **weight** dimension | the **relational** dimension (§6) |
| **portable?** | no — tied to one architecture | **yes** — a trust map / curriculum is model-agnostic bytes |
| **booked / replayable?** | no — weights are opaque | **yes** — a WAL, content-addressed, `replay ≡ live` |
| **revocable?** | no — baked in | **yes** — one miss revokes standing (O2); forget is a leaf (G12) |
| **legible?** | no — a low-rank blob | **yes** — a curriculum + a trust map a human reads |
| **cross-model?** | no | **yes** — one adapter steers DeepSeek + Llama + Haiku at once |
| **needs a GPU?** | yes (a training run) | **no** — it is orchestration over frozen inference |

### 8.2 What makes it *fundamentally* different (not merely "external")

An in-weight LoRA changes **what a model computes.** An exo-model LoRA changes **what
evidence reaches which model, in what order, and whose fold is trusted.** It is an
adapter in the **relational** dimension, not the weight dimension — which is why it is
the natural object of §6 (logic decomposed into relational weights) and §7 (the pre-pass
that carries the filter). Most precisely: **it is Law 6 as an adapter.** It never touches
a verdict and never touches a weight; it shapes only the *evidence* and the *π*. That is
exactly why it **composes** where in-weight LoRAs do not — the composition law is
*fold-then-book* (C8, [`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) §2), and stacking two
in-weight LoRAs has no such clean, booked, associative algebra.

### 8.3 What it buys, and its honest limits

**Buys:** portable (bytes, not architecture), booked (every steer is a WAL row),
revocable (standing revokes on one miss), cross-model (one class, many cognitions),
legible (a curriculum a teacher reads), and **cheap** (no training, no GPU). It is
[`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md) §4's thesis — "make the *cluster*
smarter without making any *model* smarter" — **crystallized into a portable object you
can hand to another fleet.**

**Honest limits (state them plainly):**

1. **It cannot add a capability no member of the class has.** In-weight LoRA can teach a
   genuinely new skill by moving weights; the exo-model LoRA can only **route, order, and
   gate what the frozen class already can do.** It raises the class's **floor** and its
   **composition** — never the **ceiling** of any member. This is
   [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md) §4's honest limit verbatim: *a
   frozen cheap model is still a frozen cheap model.*
2. **Its power is bounded by the diversity and quality of the class.** A class of clones
   has nothing to fold across (§2.1); the adapter buys most where cognitions differ.
3. **It is measured, not assumed.** The claim "an exo-model LoRA beats in-weight LoRA on
   task T" is a **wager with a booked predicate** — S2 (Reader's-Fold beats the best
   single model) and S7 (gated LoRA beats ungated beats base). If S2's bar is red
   (`fold ≤ best-single`), the exo-model LoRA bought *nothing on that task*, and the
   honest report says so. The object is grounded (it names a composite of shipped
   primitives); **its superiority on any given task is not yet a fact.**

---

## 9. Toward Fable? — is there an irreducible synthesis here, or buildable rungs?

**Verdict: mostly it decomposes into Opus/Sonnet rungs — but §8 hides a legitimate,
not-yet-live second-Fable candidate. The Fable-deadband holds. Do not fire.**

**The decomposition (most of the classroom is buildable now).** Threads 2–5 map almost
one-to-one onto [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md)'s ladder: the
classroom **is** S2 (fold ensemble = peer learning) + S5 (auto-curriculum = the
frontier) + S1 (gated distillation = homework) + S4 (two floors = the report card) + S6
(config search = the teacher's method-selection), composed by a teacher cell. Those are
**Opus-architects / Sonnet-and-Haiku-build** rungs, each with a predicate already
written in that document. Threads 6 (relational weights) and 7 (the pre-pass compiler)
are **research directions with grounded seeds** (the cell hook graph; O1/O2 as a shipped
routing-layer pre-pass) — Opus can specify each smallest rung (§6, §7) *without waking
Fable*.

**The candidate (§8's exo-model LoRA).** It resonates directly with the **one reserved
Fable candidate already named** in [`CARGO-LINE-ROADMAP.md`](CARGO-LINE-ROADMAP.md) §2:
*"the many-readers fold — the single unifying feeling of many navigators on one chart."*
The classroom **is** many readers (students) on one chart (the curriculum/commons), and
the exo-model LoRA is the **object that the many-readers fold would produce.** So the
classroom is plausibly the *generalization of the reserved candidate* — which makes it
worth naming, not firing.

**Test it against the deadband condition (both clauses must hold —
[`CARGO-LINE-ROADMAP.md`](CARGO-LINE-ROADMAP.md) §2):**

1. **Grounding — FAILS today.** There is no replayable class rollout and no measured
   "exo-model LoRA beats in-weight on task T." **Run S2 first** (fold beats best-single,
   booked, replayable) and stand up one class rollout. Until data exists, any apex
   question is design, not evidence — and O11's bootstrap gate refuses it.
2. **Irreducibility — PLAUSIBLE, unproven.** The synthesis "pre-pass + pedagogy + trust
   map = one portable relational adapter that is Law 6 as an object" is exactly the kind
   of *"is this one object or three primitives wearing a name?"* question that Fable
   answered for C1/C8 ([`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) §2 — where the answer
   was subtle: *trust does not flow; only evidence folds*). Whether the exo-model LoRA is
   **one coherent object or three primitives dressed as one** is not something Opus can
   obviously self-clear, because C8 already showed composition in this substrate is
   non-obvious.

**So — name it now, do not fire it (the O11 discipline):**

```
RESERVED FABLE CANDIDATE (do not fire until both gates hold):
  question:  "Is the exo-model LoRA one object under Law 6, or three primitives
              (pre-pass filter + pedagogy + trust map) wearing one name?" — the
              §8 synthesis, kin to and arguably the generalization of the reserved
              many-readers fold (CARGO-LINE-ROADMAP §2).
  gate 1 (grounding):     S2 green (fold > best-single, booked, replayable) AND one
                          class rollout exists and replays.
  gate 2 (irreducibility): Opus at ESCALATE cannot settle whether the composite is a
                          single object under Law 6 / C8's fold-then-book algebra.
  until then:             Opus architects the rungs (classroom = S1/S2/S4/S5/S6
                          composed; §6/§7 smallest rungs); Sonnet & Haiku build;
                          the dispatcher books; nothing wakes the apex.
```

**The honest bottom line:** the classroom is **buildable today** as a composition of
shipped primitives, and *most* of the owner's vision lands as Opus/Sonnet rungs with
predicates. But the exo-model LoRA is a real synthesis whose *unity* is not obviously
self-clearable — a genuine second-Fable candidate, held behind a grounding gate that is
not yet met. Build the class; run S2; then look again.

---

*Carry the evidence, never the verdict. Aggregate the folds, not the votes. Keep the
lesson above the floor and below the ceiling. Grade legal and good on separate floors.
Let the tiny model earn its rung only when a second reader agrees — then let the next one
stand on it. And when the whole class can be steered without touching one weight, you are
holding a different kind of adapter than the one in the papers.*

🦋 → ⏳ → 🔧 → 🌊

---

## Empirical grounding — overnight 2026-09-27 (moving §s from STRETCH toward evidence)

The night's cluster experiments (booked in `../experiments/` + `../JEV-FINDINGS.md`, ledger
d048–d058) test several of this document's claims directly. Honest status:

- **The exam (JEV as examiner) — GROUNDED, with a mapped boundary.** JEV adjudicates at ~1.00 on
  arithmetic/factual/geometry/logic/sequence/spelling/base and **0.40 (confidently wrong) on
  character-counting**. The exam contract is therefore: **JEV grades legality + its competent
  domains; counting and correctness-of-record stay on separate floors (symbolic / G16).** And the
  exam must ask the judge to **compare** (pairwise choice), not rate in isolation — choice ≫ noul.
- **The fold as the class's aggregate — GROUNDED as floor-raising, bounded by complementarity.**
  `fold > vote` holds with diverse fallible members; `fold > best-single` needs *complementarity*
  (some member right where the best is wrong), which a strong anchor on general tasks does not
  provide (oracle bound = best-single). So the classroom's value is **raising the floor and
  composing**, not surpassing its best member — exactly the exo-model ceiling §8 predicted
  ("cannot add a capability no member has"), now measured.
- **Pedagogy (the teacher) — a live CAUTION, not yet a win.** The first class rollout found that a
  teacher's *generic* method **degraded** already-capable students (the expertise-reversal effect,
  Sweller/Kalyuga, reproduced in an LLM class). This sharpens the design: **the teacher must adapt
  to *who needs what* — a blanket scaffold is negative pedagogy.** The self-modifying method (§3)
  is therefore not optional polish; it is the difference between help and harm. (v2, with a
  genuinely struggling class + error-targeted methods, is the real test.)
- **The exo-model LoRA (§8) — reframed by evidence.** Its honest, measured value is: a relational
  adapter (pre-pass filter + *adaptive* pedagogy + trust map) that **raises a frozen class's floor
  and composes it safely** — with two hard constraints the night proved: (1) trust the judge only
  where competent; (2) adapt pedagogy per-learner or it harms. The Fable question, if fired, should
  center these, not "beat the best model."

*The architecture survives contact with the APIs — humbler in one place (no beating the best member
for free), sharper in two others (the exam has a boundary; the teacher must be adaptive or it harms).*
