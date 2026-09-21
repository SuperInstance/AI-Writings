# GAPS — The Situational-Engineering Ledger

*The Forward Arc's stories are only worth writing if their friction compiles into
work. This is the compiler's output: every gap a character stumbled over, turned
into an experiment an engineer can run now, against code that already exists.*

Each entry has the same shape:

- **Gap** — what 2036 takes for granted that 2026 cannot do.
- **Story** — where it surfaced.
- **Experiment** — the concrete thing to build/measure this week.
- **Substrate** — the real code it runs against.
- **Passing condition** — how we know the gap is (partly) closed. This is the
  *verifier*: the future wrote the acceptance test; the present writes the code.
- **Status** — where it stands today.

The substrates referenced are real, in-hand as of 2026:
`craftmind-engine/experiments/rsi/{rsi,embed}.mjs` (deterministic JEV-bounded RSI
+ fixed-point embeddings + FNV-1a content hashing), the `craftmind-rsi` Cloudflare
D1 (`rsi_run`, `rsi_generation`, `rsi_vector`), the four alternate-route modules
in `experiments/rsi/routes/`, and `erised-next` (the wide-run harness).

---

## G1 — A latent-prediction head, with divergence-as-escalation

- **Gap.** Noor's cells *predict* the representation of their next neighborhood
  (JEPA), and the gap between prediction and arrival is a first-class, located,
  early **escalation** signal — a raised hand. Our stack has retrieval and a
  legality gate but **no predictor and no divergence signal.**
- **Story.** [The Cell-Shepherd](2036-01-the-cell-shepherd.md).
- **Experiment.** Add a tiny deterministic latent predictor to the RSI embedder:
  given the current behavior/genome vector and the JEV-chosen move, predict the
  *next* behavior vector (in Q8.8, fixed-point, so it stays bit-checkable). Each
  tick, compute `divergence = l2(predicted, arrived)`. Emit `ESCALATE` when
  divergence exceeds a trust radius; log a located, per-region raised-hand trace.
- **Substrate.** New `experiments/rsi/predict.mjs` beside `embed.mjs`; drive it
  from the Hold-the-Line episode loop in `rsi.mjs`.
- **Passing condition.** On a run with an injected novel disturbance, the
  predictor's divergence spikes **before** the fitness/error metric does — i.e.
  surprise is detected earlier than damage. Report lead-time (ticks) of the
  raised hand vs. the first band violation.
- **Status.** ✅ **Built** — `craftmind-engine/experiments/rsi/predict.mjs`
  (+ `predict.test.mjs`, CI-enforced). A JEPA-style forward predictor learns the
  nominal drift online in fixed point, and routes prediction-vs-arrival
  divergence through a JEV `{ACT, CONFIRM, ESCALATE}` gate — the raised hand is a
  legal move, not a fabricated one. **Result:** on a novel-drift shock at tick
  200, the hand goes up at 200 and the band breaks at 202 — lead-time **2 ticks,
  4/4 seeds, 0 false hands in calm, 0 illegal**, and driftHat converges to the
  true drift. The passing condition (surprise before damage) is met. This is the
  first Forward-Arc gap closed; it unblocks G2.

## G2 — Confidence calibration (the bored-middle failure)

- **Gap.** Noor's colony grew *confident faster than it grew calibrated*; its
  trust radius inflated in the boring regions, so a real surprise there slipped
  under the threshold. Legality held perfectly and still nearly lost the field.
  **Legality is not calibration.**
- **Story.** [The Cell-Shepherd](2036-01-the-cell-shepherd.md).
- **Experiment.** Give the G1 predictor a trust radius that *grows with sustained
  low divergence and decays with time-since-last-surprise* — explicitly shrinking
  in quiet regions. Then run the adversarial "bored-middle" scenario: long calm,
  then a small fast novel event in the calmest region.
- **Substrate.** Extends G1's `predict.mjs`; add the scenario to `erised-next`'s
  sweep specs so it runs wide across radius-policies.
- **Passing condition.** The calibrated policy raises its hand on the bored-middle
  event at least as early as a naive slow/dumb baseline, **without** flooding
  false alarms in the calm (measure ROC: lead-time vs. false-hand rate across the
  radius-policy sweep).
- **Status.** ✅ **Built** — `craftmind-engine/experiments/rsi/calibrate.mjs`
  (+ `calibrate.test.mjs`, CI-enforced). Done in the recursive spirit: the
  detector's calibration policy is a genome, its per-tick radius adjustment is a
  JEV `{tighten, hold, loosen}` Choice (legal by construction), and that policy is
  **evolved by the same (1+λ) engine** — RSI applied to the surprise-detector
  itself. **Result** on the bored-middle scenario (long calm, then a small brief
  event in the calmest stretch): the *confident* policy inflates its radius to
  ~80 and catches **0/6** (Noor's failure, reproduced); the *calibrated* policy
  shrinks to ~9 and catches **6/6** with 0 false alarms; the *evolved* policy
  matches/beats it (**6/6, radius 8**), all with **0 illegal**. The system that
  improves minds now improves its own capacity to know when it is surprised.

## G3 — A deposit-and-learn commons across many agents

- **Gap.** Tomás's forty billion thin agents both *read from* and *feed* one
  shared, content-addressed, self-deduplicating deposit library. Our route
  libraries are single-run and single-agent; there is no many-writers commons.
- **Story.** [The Thin Agent](2036-02-the-thin-agent.md).
- **Experiment.** Turn `experiments/rsi/routes/route-library.mjs` into a shared
  commons: many independent runs (via `erised-next` fan-out) deposit their proven
  routes into one `craftmind-rsi` `rsi_vector`-style table, deduped by content
  hash. A fresh thin agent then *reads* the commons instead of searching from
  scratch.
- **Substrate.** `route-library.mjs` + the `craftmind-rsi` D1 + `erised-next`
  dispatch.
- **Passing condition.** A thin agent standing on the commons reaches a target
  fitness in **fewer local decisions** than one that must (re)discover routes
  alone — quantify the decisions-saved multiple as the commons grows.
- **Status.** ✅ **Built** — `craftmind-engine/experiments/rsi/commons.mjs`
  (+ `commons.test.mjs`, CI-enforced). Many independent runs deposit champion
  routes into one content-addressed commons (dedup free), and a thin agent solves
  its task by *reading* it. **Result:** warm read reaches fitness 0.386 in **4,800
  decisions**; cold search reaches 0.371 in **465,600** — **~97× fewer decisions
  and a better result**, 0 illegal, and the empty commons is honest (read → null,
  never a fabricated route). The intelligence moved into the commons; the edge
  stayed thin. (The standalone **Pincher4Jev** tool productizes this: JEV as the
  mitochondria of every cell, thumbing the legal dice toward proven routes.)

## G4 — Earned standing: the conferred, revocable fourth verdict

- **Gap.** Tomás's agents have `ACT / CONFIRM / ESCALATE` but no way to *stop
  asking* — no legal move for "I have earned the right to answer this myself."
  Standing must be **conferred by the commons and revoked when the world shifts**,
  never self-granted.
- **Story.** [The Thin Agent](2036-02-the-thin-agent.md).
- **Experiment.** Add a fourth verdict `ANSWER` to the route selector's JEV
  schema, gated not by the agent but by the commons: a per-situation "diploma"
  granted after N correct ACTs on that content-hash neighborhood, and torn up on
  the first miss. Track diplomas and revocations.
- **Substrate.** `route-library.mjs` selector (extend the JEV choice set);
  standing state in the D1 commons.
- **Passing condition (G4).** Enabling `ANSWER` cuts redundant queries to the
  commons **without** raising the error rate beyond a set bound; revocation fires
  within K ticks of a regime change (measure it).
- **Passing condition (G4b — the metric first).** *Before* building `ANSWER`,
  measure the disease: what fraction of commons queries are re-answers of
  already-known situations (same content-hash neighborhood, agent already correct
  ≥N times)? That wasted-load number is the size of the prize.
- **Status.** ✅ **Built** — `craftmind-engine/experiments/rsi/standing.mjs`
  (+ `standing.test.mjs`, CI-enforced). **G4b (the prize), measured:** on a
  repeating stream, **90%** of a shared commons's queries are redundant
  re-answers of already-known situations. **G4:** a fourth verdict `ANSWER`,
  conferred by the commons after N correct ACTs on a content-hash neighborhood
  and revoked the instant the world shifts, **cuts queries by 90% with no
  increase in error rate**, and standing evaporates **~2.5 ticks** after a regime
  change. Standing is never self-granted (baseline serves 0 local answers), and
  the four-verdict set stays a JEV schema — even "stop asking" is a legal move.
  0 illegal. This is the exact seam Pincher4Jev's scale-thumbing bias rides.

## G5 — Portable, cross-model deposit inheritance (warm-start)

- **Gap.** Wren's world lets a four-minute-old mind inherit a decade of
  legally-earned experience by *reading the commons* — the learning got out of
  the model. Our vectors are content-addressed but task-local and model-local; we
  have never warm-started one mind from another's deposits.
- **Story.** [The Child Who Never Knew Otherwise](2036-03-the-child-who-never-knew-otherwise.md).
- **Experiment.** Cross-task transfer: build the deposit library on Task A (one
  Hold-the-Line regime), then seed Task B (a *different* drift/noise regime, or a
  different move-effect set) by retrieving A's nearest deposits as priors for B's
  initial population. Compare cold-start vs. warm-start convergence.
- **Substrate.** `rsi.mjs` (parameterize the regime), `embed.mjs`, the D1 commons.
- **Passing condition.** Warm-started B reaches target fitness in measurably fewer
  generations than cold-started B, and the transfer degrades *gracefully* (not
  catastrophically) as A and B grow dissimilar — plot gain vs. regime distance.
- **Status.** Not built. This is the "learning outlives the mind" proof-of-concept
  in miniature.

## G6 — The situation compiler (the keystone)

- **Gap.** Wren built *the past you can lose in* — a deterministic, seeded,
  wide-runnable world in which today's agents try to build a future capability and
  fail in **specific, mappable** ways. Devi's lament: *we had no place to fail on
  purpose.* We have the wide-run harness and the deterministic substrate; we lack
  the compiler that turns a named gap into a scenario whose **passing condition is
  the gap being closed.**
- **Story.** [The Child Who Never Knew Otherwise](2036-03-the-child-who-never-knew-otherwise.md).
- **Experiment.** Build a `situation` format: a gap id (G1…G5), a deterministic
  scenario generator, and an explicit passing predicate (the acceptance tests
  written above). `erised-next` runs it wide; the output is not a single score but
  a **failure map** — which joint each failed agent couldn't weld. This closes the
  Forward-Arc loop: story → gap → situation → wide run → failure map → next weld.
- **Substrate.** `erised-next` (sweep spec + collector) consuming
  `craftmind-engine` scenarios; failure maps stored in D1.
- **Passing condition.** Feed G1–G5's passing conditions in as `situation` specs
  and get back, from one wide run, a ranked map of *where* current agents fall
  short on each — reproducing, in code, the "thousand small failures" Wren watched
  bloom.
- **Status.** Not built. This is the meta-tool that makes every other gap
  self-verifying; it is where the fiction stops being fiction.

---

## The loop, stated plainly

1. A character in 2036 does something ordinary that we cannot yet build.
2. That friction is named as a **gap** (G1–G6) and given a **passing condition** —
   an acceptance test written *from the future.*
3. An engineer builds the smallest thing that could pass it, against real
   substrate (`craftmind-engine`, `craftmind-rsi`, `erised-next`).
4. `erised-next` runs it wide; where agents fail, the **failure map** points at
   the next gap.
5. A new story is written from the far side of the closed gap. The arc advances.

*The future is the verifier. The present is the implementation. The story is how
we know what passing feels like before we can measure it.*

🦋 → ⏳ → 🔧 → 🦋
