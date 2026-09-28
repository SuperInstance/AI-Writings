# Playable Situations — project JEV + Moth so PLAYING finds the answer

*Authored by Opus 5.5 (architecture tier), 2026-09-28. Method, in the owner's words:
"set up quilt SITUATIONS so that PLAYING them finds the answers — that's the ultimate pass
on the untested subject." Ground truth: `arch/TOOLING-LIVE-2026-09-28.md` (verified live JEV +
Moth schemas), `JEV-FINDINGS.md` (choice ≫ noul; counting is the one blind spot), `README.md`
(Situations as the development substrate). Every schema below was re-verified live on the
rotated keys during this session before the designs were written.*

## The two now-live primitives, in one line each

- **JEV** (`POST api.typesafe.ai/v1/systemone`, `noul|score|choice`) = **the located verdict.**
  Projecting `noul` across a decomposition turns an opaque scalar into a *map*: the whole is a
  shadow, the fold is where the rot is. `choice` beats independent `noul` for adjudication.
- **Moth** (`comet-qrng-v1`, 5 credits/run) = **the un-gameable draw.** A curriculum/cast/seed
  whose provenance is physics (CHSH Bell witness **S ≈ 2.82 > 2**, p ~ 1e-297), so a run cannot
  be quietly re-rolled until it flatters the thing under test.

The bet of every situation here: compose *located verdict* × *un-gameable draw* so that the act
of **running** the scenario emits an answer to a question we had not tested — and bias hard
toward questions whose answer **makes a fleet tool better**.

---

## Live-schema corrections booked this session (use these exact shapes)

Re-verifying against the live keys turned up **one correction to the ground-truth doc** that any
runnable must carry, plus the exact result paths:

- **Moth params go under a `params` wrapper, and integers under `derive`.** `{}` (defaults) works,
  but the derivation body is:
  `POST /engines/comet-qrng-v1/process  {"params":{"derive":{"integers":{"min,max,count}}}}`.
  Sending `integers` or `derive` at the top level → **422 unexpected property**.
- **Result paths:** Bell `S` at `result.output.bell_witness.S`; derived draws at
  `result.output.random.derived.integers.values`; a 256-bit quantum seed at
  `result.output.random.hex`. (`TOOLING-LIVE` implied a bare `integers`; the wrapper is required.)
- **JEV** confirmed exactly as documented: `{model:"jev-latest", state, questions:{<n>:{type,
  question, criteria:{true,false}}}}` → `answers:{<n>:{noul|score|confidence|choice, probabilities}}`.
- **Browser `User-Agent` is load-bearing** on Moth (Cloudflare error-1010 otherwise), key trimmed.

---

## Scout — synergy verdicts (honest; no forced fits)

Inspected `exoj`, the `pincher` family (`pincher`, `quilt-pincher`, `mavis-pincher`,
`pincher4jev`), `purplepincher/constraint-theory-core`, and searched for `lever-runner`.

### exoj — **STRONG, and the deepest fit of the set.**
`exoj` is an "external, non-collapsing, vectorized scratch-paper": Field is primary, the **quilt is
the projection**, and — verbatim from its charter — **"JEV is the inference engine that only ever
emits soft deformations"**, keeping a **chain-of-probabilities open** until an *explicit, recorded*
observation collapses one locus. This is precisely the surface the *decomposing fold* wants: a tree
of leaf-verdicts held in superposition, visual and auditable, that you localize without collapsing
the whole. Honest caveat: exoj's shipped "JEV" is a *local mock* soft-deformation emitter
(classical/jepa/quantum-inspired/cellular-llm), **not** the live `typesafe.ai` oracle — so the
synergy is a concrete *build*, not an existing wire. The build: back exoj's `jev_emit` with a live
`noul` per cell and seed its non-collapse schedule from a Moth draw → exoj becomes the visual
substrate for Situation S17/S19 below.

### pincher family — **STRONG (structural), needs one wire.**
`pincher`/`quilt-pincher` is a reflex engine with a **confidence-gated escalation that is the same
shape as the JEV deadband**: fire ≥0.80, confirm 0.55–0.80, compile <0.55. That middle band is
exactly a *Look-Again* / abstain-and-buy-a-reader zone. Two live wires: (a) let **JEV `choice`
adjudicate the confirm band** instead of a human (JEV is a reliable adjudicator everywhere but
counting, per `JEV-FINDINGS`); (b) feed **`pincher mature`'s adversarial fuzzing from a Moth draw**
so coverage grows against cases nobody steered. `pincher4jev` already names the pairing in its
title — it is the natural home for the wire. Situation S18 below is built on this.

### lever-runner — **EXISTS** (`github.com/SuperInstance/lever-runner`, Python, v0.4.0, 160 tests).
Post-inference command executor; three gates (Rust template 50µs / Python cache 200µs / LLM intent
500ms), **trust score per command**, teach-once-run-forever, `.nail`-compatible with pincher.
Synergy — **MEDIUM, and it is the best *first audit target*.** Its trust score is a scalar the fold
can localize, and its security-model table is a compound guarantee begging to be decomposed. It is
the concrete tool audited by the immediately-playable Situation S17 (below): playing S17 already
returned that lever-runner's most overclaimed guarantee is *"the LLM never sees absolute paths"* —
a real, actionable finding for making the tool honest.

### constraint-theory-core (purplepincher) — **MEDIUM (conceptual).**
Rust, zero-dep, 83 tests: Eisenstein lattices, **deadband funnels**, Laman rigidity, metronome
consensus, holonomy verification. The **deadband** is literally the abstain band JEV/pincher use;
`holonomy verification` (path-independence of a verdict) is a clean formalization of Law 6's
"each reader folds under its own weights and still agrees." No live wire today, but it is the
math vocabulary the situations are informally speaking. Use it as the *rigor backstop*, not a dep.

**One-line net:** exoj is the *surface*, the pincher family is the *deadband to instrument*,
lever-runner is the *first target*, constraint-theory is the *math*. All four converge on the
same object the situations play with: a graded verdict with an honest abstain band.

---

## The three playable situations

Each is a concrete RUNNABLE scenario. Format follows `situations/` doctrine (untested question →
decomposition → un-gameable draw → play loop → DONE signal → cost). S17 ships as code today.

### S17 — "The Weakest Leaf"  ·  **IMMEDIATELY PLAYABLE**  ·  `situations/play/weakest-leaf.mjs`

- **Untested question it answers:** *Of all the guarantees a fleet tool advertises, which one is
  its weakest — the claim it makes most confidently that the fold can least defend — and does
  that weakness survive an adversary nobody could have steered?*
- **Decomposition (JEV, increasingly folding):** the tool's headline compound guarantee →
  `noul(WHOLE)`; then each leaf-claim gets its own `noul` (**the tree of nouls is the visual
  logic**); then the *located* weakest leaf is **decomposed again** into atomic sub-claims until the
  rot lands on a single atom. `FOLD(min)` and `whole − fold` measure what the compound was hiding.
- **Where Moth enters (un-gameable draw):** quantum dice pick **which concrete bypass-hypotheses**
  from a fixed pool get fired at the located leaf — the auditor cannot stack the deck. Each drawn
  bypass is adjudicated by JEV `choice` (defeats / holds). The run is stamped with the Bell `S` and
  the `random.hex` seed, so the audit **cannot be re-rolled until it flatters the tool**.
- **Play loop:** `node situations/play/weakest-leaf.mjs` → prints the noul tree → deepens on the
  weakest → rolls Moth → prints the located answer. Swap the `AUDIT_TARGET` block to audit any tool.
- **DONE / answer signal:** the located weakest leaf (and its precise atom) + the count of
  quantum-drawn bypasses that land. That located leaf **is** the next thing to fix/soften.
- **Cost:** JEV ~11 calls (~cheap, ~450in/40out each) + 1 Moth run (**5 credits**). `--no-moth`
  makes it JEV-only and cents-cheap.
- **What playing it already found (live, this session):** auditing `lever-runner`'s security table,
  the fold localized **L5 "the LLM never sees API keys, absolute paths, or env vars"** (noul 0.10)
  as the weakest leaf; deepening pinned the atom to **"never sees absolute filesystem paths"** (0.14);
  the Moth-drawn adversary landed **2–3 of 3** bypasses (template-interpolation and
  metacharacter-in-argument are the real ones), Bell **S = 2.82**. **Second, sharper finding:** *every*
  leaf nouled 0.10–0.20 — the tool overclaims **uniformly** (every row says "fully / never / zero /
  blocked"), so `whole − fold` is small. The lesson for tool-auditing: when a spec overclaims across
  the board the divergence vanishes and the **ranking (argmin), not the level**, is the signal.

### S18 — "The Deadband Is Lying"  ·  design (build on `pincher4jev`)

- **Untested question:** *At what self-reported confidence does a reflex engine's match-score stop
  tracking actual correctness — i.e., is pincher's 0.80 fire-threshold set where the tool is
  actually right, or where it merely feels sure?* (Tuning this **is** making a better tool: it sets
  the gate every pincher/quilt-pincher instance fires on.)
- **Decomposition (JEV):** for a set of pinches, don't score the engine's confidence in isolation —
  project JEV `choice` (choice ≫ noul, per findings) to adjudicate, for each fired reflex, *was the
  action actually the right one?* The decomposition is **confidence-bucket → JEV-adjudicated
  correctness**, one leaf per bucket (0.5–0.6, 0.6–0.7, …). The tree of buckets is the calibration
  curve; the leaf where JEV-correctness falls below the bucket's confidence is the *located* lie.
- **Where Moth enters:** Moth draws the **pinch cast** — which intents from a large pool get tested,
  and their order — so you cannot quietly fill the test set with easy pinches the engine happens to
  nail. An un-gameable cast is what turns a calibration curve into a falsifier.
- **Play loop:** draw cast → run each pinch through pincher (record match-confidence + action) →
  JEV `choice`-adjudicates correctness → bin → plot confidence vs correctness → read the crossover.
- **DONE / answer signal:** the located threshold where self-confidence decouples from truth. If it
  is below 0.80, pincher fires too eagerly (lower the gate); if above, it wastes the LLM (raise it).
- **Cost:** JEV 1 `choice`/pinch (cheap; ~40–80 pinches) + 1–2 Moth runs for the cast (**5–10
  credits**). Counting-type pinches fall back to vote per the reliability contract.

### S19 — "The Un-gameable Curriculum"  ·  design (build on exoj as the surface)

- **Untested question:** *Did a tool's benchmark improve because the tool got better, or because we
  (consciously or not) steered the test set toward its strengths?* — the falsifier for teaching to
  the test, the exact master-risk shape from `TRAJECTORY.md` risk 6 (supply-side self-grading).
- **Decomposition (JEV):** decompose the capability under claim into skill-leaves; JEV `score`s the
  tool's output on each leaf. Run the **same leaves twice** — once on a **hand-picked** set, once on
  a **Moth-drawn** set from the same pool. Two trees side by side; the per-leaf gap between them is
  the steering. Held **open on an exoj field** (non-collapsing) so both trees are visible at once and
  the auditor can refract between them without collapsing either — exoj's native trick.
- **Where Moth enters:** Moth draws the **curriculum order and the held-out cast** — the one thing
  neither the tool's author nor the grader can steer. A gain that survives the quantum-drawn set is
  a gain against an adversary you *couldn't* have gamed.
- **Play loop:** define leaves → score hand-picked (JEV) → Moth-draw the matched set → score it
  (JEV) → overlay the two noul trees on exoj → read the divergence per leaf.
- **DONE / answer signal:** the aggregate hand-picked − Moth-drawn gap. Near-zero ⇒ the improvement
  is real; large ⇒ the benchmark was steered and the "better tool" was an artifact. This is the
  cheapest honest first pass at H3's "an outsider brings their own reader," run against ourselves.
- **Cost:** JEV 2 `score`s/leaf (cheap) + 1–2 Moth runs (**5–10 credits**).

---

## The through-line

All three are the same move at three altitudes: **decompose a claim into leaves JEV can locate, then
spend an un-gameable Moth draw exactly where the auditor would otherwise cheat** — S17 on *which leaf
to challenge*, S18 on *which cast to test*, S19 on *which curriculum to grade against*. The fold makes
the tool's weakness *visible*; the quantum draw makes the finding *un-fakeable*. That pairing is the
"ultimate pass on the untested subject": you do not argue about whether the tool is good — you play
the situation and read where it broke.

*Author the world. Mine the friction. Locate the leaf. Roll the un-gameable dice. Fix the tool.*
🦋 → 🌳 → 🎲 → 🔧
