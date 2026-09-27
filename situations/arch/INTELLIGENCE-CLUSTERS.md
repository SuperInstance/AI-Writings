# INTELLIGENCE-CLUSTERS — a research program for a cluster that is more than its models

*Opus-tier planning, blinders on. A concrete program of synergistic studies in which
SuperInstance's existing tools — the dispatch org, the external roster, the jev-quilt
substrate, erised, the situations loop, the mid-state playtester, Autoresearch — work
**together** to make a multi-model cluster measurably smarter than any model in it, and
to do real ML/DL where "real" means a predicate, not a press release. This is a **plan**.
Nothing here is built by this document; every rung ends in a green/red bar someone can
run. Grounded in `DISPATCH.md` (O1–O12), `ROSTER.md` (funded providers + `jev-1.13.0`),
`FABLE-ANSWER.md` (Law 6, G20), `METHODOLOGY.md` (the loop), `TRAINING.md` (standing as a
grade), `jev-quilt/` (the booked substrate), `tools/experiment-proxy/` (keyless judge
access). Companion to `DISPATCH.md` and `NEW-DIRECTIONS.md`. Do **not** commit — the
dispatcher books.*

🦋 → ⏳ → 🔧 → 🌊

---

## 0. The thesis in one breath

**A cluster is more than the sum of its models when the thing that flows between them is
content-addressed evidence, not verdicts (Law 6): each model folds the shared evidence
under its own weights, we aggregate the *folds* not the votes, we let a cheap model
inherit an expensive model's answer only after an *independent reader reproduces it*
(G16), and we route with a signal that separates *legal* from *good* (JEV two-floors) so
no single metric can be gamed (O9). Everything else — MoE, best-of-N, LoRA distill — is
table-stakes we borrow; the booked, replayable substrate underneath is what makes our
version an experiment instead of a demo.**

---

## 1. The thesis in full — six primitives, one claim

Generic mixture-of-experts says "average some models, it's better." That is not our
claim and we should not pretend it is. Our claim is narrower and testable: the substrate
gives ensembling and distillation **three properties they normally lack** — verifiability
(a stranger can recompute the aggregate from the bytes), reproduction-gating (a cheap
model earns a task-class only when its output is independently re-derived), and a
verdict-free wire (we never trust a carried conclusion). Each maps to a shipped primitive.

**(P1) JEV-routed mixture-of-experts.** The dispatcher already routes by a four-verdict
kernel (ESCALATE/ACT/ANSWER/CONFIRM, `DISPATCH.md`). Today the verdict is hand-reasoned;
the roster gives us a *real* oracle — `typesafe.ai jev-1.13.0`, a `noul`/`choice`/`score`
judge (`ROSTER.md`; client shape in `src/typesafe.ts`; `POST /v1/systemone`). Routing
becomes a measured function of a judge's confidence, not a vibe. This is MoE where the
gate is an *external, separately-calibrated* model — not a softmax trained jointly with
the experts, which is exactly why it can't collude with them.

**(P2) Distillation expensive→cheap, GATED BY REPRODUCTION (G16).** The ordinary
distillation move — take Opus/`deepseek-v4-pro` traces, fine-tune or few-shot a cheap
tier to imitate — silently inherits the teacher's errors. Our gate is the substrate's own
law: a cheap model's output earns standing on a task-class only when an **independent
reader reproduces it to one root** (`claim.py`, G16; `TRAINING.md`'s "earned, never
self-granted; revocable by one miss"). A distilled answer that no second reader
reproduces never enters the commons. Distillation stops being "copy the teacher" and
becomes "copy the teacher *only where a witness agrees*."

**(P3) Trust-weighted gluing ACROSS heterogeneous models (G11) = verifiable federated
ensembling.** `commons.py`'s `merge` is confluent (`A.merge(B).root()==B.merge(A).root()`)
and weights each deposit by the *reader's own* trust map, default 0 for strangers
(`FABLE-ANSWER.md` §1.2 G11 row). Point the deposit key at "an answer to task T" and the
source at a model id, and the commons *is* a federated ensemble whose aggregate any node
can recompute from the deposits and its trust map — verifiable ensembling, not a black-box
average. A model earns weight in the ensemble the way a cell earns standing: booked,
per-class, revocable.

**(P4) Law 6 as the ensembling/distillation principle.** *Carry the evidence, never the
verdict; every reader folds its own; nothing booked is unreadable* (`FABLE-ANSWER.md` §1).
The ML translation is sharp: **do not aggregate the models' answers (verdicts); aggregate
the evidence each produced and let each model re-fold the pooled evidence under its own
weights, then take the aggregate of the folds.** A best-of-N vote is verdict-aggregation
(the naive thing). A Reader's-Fold ensemble is evidence-aggregation: each model sees the
others' *content-addressed working*, re-derives, and we book the re-derivations. The
theorem `V(E,π₁) ≠ V(E,π₂)` is legal (§1.1 corollary) tells us disagreement between
readers on the same evidence is *signal*, not noise — it localizes the seam.

**(P5) Two floors: legal ≠ good.** JEV gives a legality/alignment/calibration signal
(the `JEV_ORACLE_SPEC.md` battery scores voice/doctrine/misquote/substance — *is this
well-formed and non-contradictory*, and how *confident*). It does **not** know ground
truth for an arbitrary task. So it is a *legality floor*, not a correctness oracle. The
correctness floor is separate: a booked acceptance test or an independent reproduction
(G16). Keeping these two floors apart is the anti-Goodhart spine — a model can be legal
and wrong (fluent nonsense) or illegal and right (correct but off-canon), and a cluster
that measures both refuses to optimize one into the other.

**(P6) Anti-Goodhart via the wider feel + novelty (O9) as an explicit selection signal.**
`DISPATCH.md`'s O9 ("novelty scores higher; read cross-sections, not silos") is usually
prose about culture. Here it is a *training/selection term*: when ranking N candidates,
add a novelty-vs-the-commons component so the cluster is not rewarded for restating what
it already holds. This is the "light GAN inside the practice" made numeric.

**The composite claim, stated as a wager we can lose:** *Under P1–P6, a cluster of cheap
funded models (DeepSeek + DeepInfra) plus a real judge (`jev-1.13.0`) plus the booked
substrate beats the single best model in the cluster on a booked benchmark, and its
cost-per-passed-test falls over a run — and both facts are replayable by a stranger from
the ledger alone.* If that is false, we will see it in a red bar, not a feeling.

---

## 2. The experiment ladder

Seven studies. Each is a rung: **hypothesis · which tools compose · method · the
predicate that says it worked · the tier that runs it · funded-now/STRETCH.** Priority
order is roughly S1→S7; S1–S4 and S6 are runnable this week with confirmed-funded tools
and the substrate as the booked eval ledger.

| # | study | composes | tier | tag |
|---|---|---|---|---|
| **S1** | JEV-gated best-of-N + reproduction-gated self-distillation | roster + `jev-1.13.0` + `claim.py`/`bookkeeper.py` + O10 cache | Sonnet drives, Haiku batches | **FUNDED-NOW** |
| **S2** | Reader's-Fold ensemble beats the best single model | roster (≥3 models) + `commons.py` (G11) + booked eval | Sonnet | **FUNDED-NOW** |
| **S3** | The dispatch org (O1–O12) is a measurable learning system | `dispatch-ledger.csv` + O7 metabolism + booked tasks | Dispatcher + Haiku | **FUNDED-NOW** |
| **S4** | The two floors are decorrelated (legal ≠ good, measured) | `jev-1.13.0` + booked acceptance tests | Haiku batch, Sonnet reads | **FUNDED-NOW** |
| **S5** | erised self-play generates a curriculum the org auto-calibrates (R1) | erised-cli + `calibrate.py` + Autoresearch | Sonnet + Haiku | **FUNDED-NOW (canvas) / STRETCH (scale)** |
| **S6** | Autoresearch one-file-one-metric loop optimizes a substrate task | Autoresearch skill + `calibrate.py`/Tell-config + roster | SESSION-tier loop | **FUNDED-NOW** |
| **S7** | Reproduction-gated LoRA/distill — the smallest real "weights move" | DeepInfra fine-tune (if supported) + G16 gate + booked eval | Sonnet designs, external GPU | **STRETCH** |

---

### S1 — JEV-gated best-of-N with reproduction-gated self-distillation

**Hypothesis.** Sampling N candidates from cheap models and selecting with a *composite*
score (JEV legality floor × task-correctness floor × O9 novelty) beats greedy single-shot
*and* beats naive best-of-N-by-self-confidence — and the winners, once independently
reproduced, form a distillation set that lifts the cheap tier's solo pass-rate on the same
task-class without any weight update (in-context distillation via the commons).

**Composes.** DeepSeek (`deepseek-flash` for candidates, cache-friendly per O10) +
DeepInfra Llama-3.1-8B as a *different-cognition* second sampler + `jev-1.13.0` as the
legality/calibration scorer (via `experiment-proxy /ts/…` so no key is held) +
`bookkeeper.py` to book every candidate and score + `claim.py` for the reproduction gate.

**Method.** Pick a task-class with a *checkable* correctness floor (e.g. the GSM-style
word problems DeepSeek already answers with a strict `ANSWER:` suffix, `ROSTER.md`
example; or a JSON-format-compliance set; or small unit-tested code). For each item:
sample N=8 candidates; score each with (a) correctness (exact-match / test-pass — the
ground-truth floor), (b) JEV `score` on well-formedness/confidence (the legality floor),
(c) novelty vs the commons deposits for that class (O9). Select by the composite. Book
every candidate, every sub-score, and the winner. Then: an *independent* reader (a second
model, or a deterministic re-run under `replay ≡ live`) reproduces the winner; only
reproduced winners are deposited to the commons as few-shot exemplars. Re-run the cheap
tier's *solo* (N=1) pass-rate with the commons exemplars in the stable prefix (O10).

**Predicate (works iff).**
`bestN_composite.passrate > max(greedy.passrate, bestN_selfconf.passrate)` on a held-out
split **AND** `solo_with_commons.passrate > solo_cold.passrate` (reproduction-gated
in-context distillation lifts the floor) **AND** every candidate, score, and reproduction
is a booked row such that `replay()` reconstructs the selection exactly (Law 4).

**Tier.** Sonnet designs the harness and the composite; Haiku runs the N-sampling and
scoring in parallel batches (O6). Dispatcher books.

**Tag.** **FUNDED-NOW.** DeepSeek + DeepInfra confirmed funded; `jev-1.13.0` live. Only
soft blocker: `experiment-proxy` needs Cloudflare deploy creds (`README.md` §Deploy) *or*
a direct `TYPESAFEAI_KEY` call from an env that holds it. Falls back to correctness-floor-
only selection if JEV access stalls (O12 fallback chain) — degrades the study, doesn't
kill it.

---

### S2 — The cross-model Reader's-Fold ensemble

**Hypothesis.** An ensemble that pools each model's *content-addressed evidence* and
re-folds it under a per-node trust map (G11) beats the single best model in the cluster on
a booked benchmark, and the aggregate is recomputable by a stranger from the deposits
alone (verifiable ensembling). Disagreement between readers on the same evidence localizes
the hard items.

**Composes.** ≥3 heterogeneous funded readers (DeepSeek `deepseek-v4-pro`, DeepInfra
Hermes-3-405B or Seed-2.0-pro, DeepInfra Llama-3.1-8B — deliberately mixed capability) +
`commons.py` (`deposit` keyed by task, `source=model_id`, confluent `merge`, trust-weighted
`root`) + a booked benchmark as the eval ledger.

**Method.** For each item, each model emits an answer *and its evidence* (its working /
the facts it relied on) as a deposit; weight = a per-class trust integer earned via S1's
booked history (default 0 for an unproven model — G11's "a stranger's 1000 → 0"). Two
aggregation arms, compared head to head: **(A) verdict-vote** (majority over answers — the
naive baseline); **(B) Reader's-Fold** (each model re-reads the *pooled evidence* and
re-answers; aggregate the re-folds by trust-weighted argmax, `commons.py:222`). Book both.

**Predicate (works iff).**
`fold_ensemble.passrate > max_i(model_i.passrate)` (beats every single member) **AND**
`fold_ensemble.passrate > vote_ensemble.passrate` (evidence-aggregation beats
verdict-aggregation — the P4 claim, or it's refuted) **AND** an independent script
recomputes the ensemble's answer for every item from the booked deposits + the trust map
alone, bit-for-bit (verifiability; the G20 Second-Reader discipline applied to the
ensemble output).

**Tier.** Sonnet. Haiku batches the per-model calls.

**Tag.** **FUNDED-NOW.** Pure cheap-inference + the substrate. The strongest single novel
result if (B) > (A) holds.

---

### S3 — The dispatch org as a measurable learning system

**Hypothesis.** The org's own optimizations (O1 deadband, O2 standing, O3 commons, O7
metabolism) constitute a learning system whose *cost-per-passed-acceptance-test falls over
a booked run while pass-rate holds* — i.e. the org gets cheaper at fixed quality by
routing more work to earned-standing cheap tiers, exactly the O1/O2/O7 predicates.

**Composes.** `dispatch-ledger.csv` (the WAL) + the O1–O12 rules + any stream of booked
tasks (S1/S2/S4 items are ideal fuel) + `standing.py`/`orgbook.py` for the standing/route
derivation.

**Method.** Run a fixed batch of ~200 tasks spanning a few classes through the org twice:
**cold** (no standing, everything routes ACT/ESCALATE) and **warm** (standing accrues per
O2; commons reuse per O3). Instrument each dispatch with tier, token cost, and
pass/fail. Compute cost-per-passed-test over a sliding window across the warm run. This is
S3 measuring the *thesis of `DISPATCH.md` itself* — the reverse-actualized O1–O12 as a
booked, improving quantity.

**Predicate (works iff).**
`cost_per_passed_test[late_window] < cost_per_passed_test[early_window]` by a
pre-registered margin **AND** `escaped_defect_rate` does not rise (O2/O7 guard against
Goodharting cheapness) **AND** `opus_wake_rate` falls across the warm run at held pass-rate
(O1) **AND** the whole thing `replay()`s from `dispatch-ledger.csv` to the same numbers
(Law 4 — the org's history is reproducible).

**Tier.** Dispatcher orchestrates; Haiku runs the grunt tasks; no Opus wake needed for the
run itself (only its design cleared a deadband, and that's this document).

**Tag.** **FUNDED-NOW.** This is measurement of a system we already run; the only new build
is the instrumentation harness over the ledger.

---

### S4 — The two floors, measured (legal ≠ good)

**Hypothesis.** JEV legality and task correctness are *decorrelated enough to matter* —
the four quadrants (legal+right, legal+wrong, illegal+right, illegal+wrong) are all
populated, proving JEV is a genuine second floor and not a proxy for correctness. This is
the empirical ground under P5 and the anti-Goodhart claim.

**Composes.** `jev-1.13.0` (legality/confidence) + a booked task set with a ground-truth
correctness floor (S1's checkable classes) + `bookkeeper.py`.

**Method.** For a few hundred booked answers (harvest from S1/S2), record JEV
`noul`/`score` (legal?) and the correctness floor (right?). Build the 2×2 confusion; test
whether legality predicts correctness better than chance but far from perfectly. Identify
the *legal-but-wrong* set (fluent, confident, false) — the exact failure a
correctness-only selector misses and a legality-only selector rewards.

**Predicate (works iff).** All four quadrants are non-empty with the off-diagonal
(legal-wrong, illegal-right) each ≥ a pre-registered floor of the sample **AND** JEV's
`score` is calibrated (higher score → higher empirical correctness) but with AUC bounded
away from 1.0 (it's a floor, not an oracle) **AND** a composite selector using *both*
floors beats either floor alone on held-out selection accuracy (this closes the loop back
into S1's composite).

**Tier.** Haiku batches the JEV calls; Sonnet does the stats read.

**Tag.** **FUNDED-NOW.** Cheapest study; strongest honesty payload. Run it early — it
validates or kills the whole two-floors premise before S1's composite leans on it.

---

### S5 — erised self-play as an auto-calibrated curriculum (R1)

**Hypothesis.** erised cooperative-fiction self-play, drifting cast keywords across
v1/v2/v3 (`erised/README.md`, the winners corpus), generates a stream of scenarios whose
*difficulty the org can auto-calibrate* against a moving baseline — i.e. R1's calibrated
floor (`calibrate.py`) applied to a curriculum: the floor rises as the cluster gets
stronger, so the curriculum stays at the frontier instead of a fixed difficulty.

**Composes.** erised-cli (headless self-play) + `calibrate.CalibratedFloor` (R1, the
ripple-in-the-calm) + `predictor.surprise` + Autoresearch as the loop driver + funded
models as the cast (DeepInfra Seed-2.0-mini, DeepSeek — GLM/Kimi in the cast are STRETCH
until funded).

**Method.** Run erised scenarios headless; score each run's difficulty by the cluster's
pass-rate + surprise on it. Feed the difficulty stream to a `CalibratedFloor`; keep
scenarios whose difficulty sits *above* the current floor (frontier), retire ones that
fall below (mastered), and let the floor re-calibrate as pass-rate climbs. The curriculum
is thus a booked, self-adjusting frontier — `TRAINING.md`'s L4 "authored gap" mechanized.

**Predicate (works iff).** The retained-scenario difficulty tracks the cluster's rising
competence (the floor is not fixed) **AND** cluster pass-rate on a *held-out* frontier set
improves after training on the auto-curriculum vs a fixed-difficulty control **AND** every
scenario, score, and floor-move is booked and replayable (a past curriculum re-derives the
same frontier).

**Tier.** Sonnet designs; Haiku runs the erised batch; Autoresearch paces the loop.

**Tag.** **FUNDED-NOW** for the canvas/CLI proof-of-mechanism with cheap models;
**STRETCH** for scale (the full winners-corpus cast wants GLM/Kimi funding). Honest risk:
"difficulty" here is a proxy; guard it with S4's two-floors discipline so the curriculum
isn't gamed toward legal-but-trivial scenarios.

---

### S6 — Autoresearch one-file-one-metric optimization on a substrate task

**Hypothesis.** An Autoresearch autonomous loop (one file = the config, one metric = the
target; the Karpathy pattern, adopted in `CARGO-LINE-ROADMAP.md`) can optimize a real
substrate parameter — e.g. the `CalibratedFloor` hyper-parameters, or the cargo-line
Tell's range/decoy/reveal config against pencil-stake rate — better than hand-tuning, and
book its whole search so the optimum is reproducible.

**Composes.** Autoresearch skill (SESSION-tier loops) + one target file (`calibrate.py`
params, or a Tell config) + one booked metric (surprise-calibration error, or playtester
fun/winnability from the mid-state engine) + funded models to run the trials.

**Method.** Define the metric as a booked scalar. Let Autoresearch propose config edits,
run the eval, book the result, iterate. Compare its best-found config against the current
hand-set one on a held-out eval. The mid-state playtesting engine (roster self-play scoring
fun+winnability, `CARGO-LINE-ROADMAP.md` Rung C) supplies the metric where the target is a
game rung; `calibrate.py` supplies it where the target is the floor.

**Predicate (works iff).** `autoresearch_best.metric > handset.metric` on held-out eval by
a pre-registered margin **AND** the full search trace is booked such that the reported
optimum `replay()`s to the same score **AND** the found config passes its acceptance test
(a Goodhart guard: optimizing the metric must not break the test — O7/R8 audit
discipline).

**Tier.** SESSION-tier autonomous loop; Sonnet reviews the diff before any merge (O12b).

**Tag.** **FUNDED-NOW.** Autoresearch is orchestration over cheap inference; no weights
move. Honest scope: this is *hyper-parameter/config search*, not model training — real ML
methodology, in-context substrate.

---

### S7 — Reproduction-gated LoRA/distill: the smallest real "weights move"

**Hypothesis.** Fine-tuning a *small open model* on the reproduction-gated distillation set
from S1 (only winners that an independent reader reproduced) lifts its solo pass-rate on
the task-class *more than fine-tuning on the ungated set* — i.e. the G16 gate is a better
data filter for distillation than raw teacher-imitation, and this shows up in **moved
weights**, not just in-context.

**Composes.** DeepInfra fine-tune/LoRA API **if it exposes one** for an 8B-class model
(`meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`) — else a local/Colab LoRA on a small open
model — + S1's booked distillation set + `claim.py` as the gate + a booked held-out eval.

**Method.** Two training sets from S1's candidates, matched in size: **gated** (only
independently-reproduced winners) vs **ungated** (all best-of-N winners). LoRA-tune the
same base on each. Eval both, and the base, on a held-out split of the task-class. This is
the *one* study where parameters actually change.

**Predicate (works iff).** `gated_lora.passrate > ungated_lora.passrate > base.passrate` on
held-out **AND** the improvement is on the task-class the gate was defined over, not a
generic lift (specificity) **AND** the training data, both LoRA runs, and the eval are
booked so the result is reproducible from the ledger (weights move, but the *experiment*
still obeys Law 4).

**Tier.** Sonnet designs the data pipeline and eval; the training run itself is external
compute (Opus-level design decision cleared the deadband; the run is grunt GPU time).

**Tag.** **STRETCH.** Needs a real fine-tune surface. **Smallest viable form:** a single
LoRA on Llama-3.1-8B over a few hundred gated vs ungated examples for one task-class — a
day of one small GPU, not a training program. If DeepInfra has no fine-tune endpoint, the
smallest real weights-move is a local LoRA on a 1–3B open model; if even that is out of
reach, S1–S6 stand alone as *selection/orchestration* intelligence and we say so plainly.

---

## 3. The ML/DL angle that is genuinely ours (vs table-stakes)

Blunt separation, because a program that can't tell its novelty from its plumbing is a
manifesto.

**Genuinely ours (candidate paper/artifact material):**

1. **The substrate as a verifiable, booked, replayable training/eval ground.** `replay ≡
   live` (Law 4) means every experiment above is *perfectly reproducible from the ledger* —
   a stranger re-runs `dispatch-ledger.csv` + the deposits and gets the identical numbers,
   no seed-hunting, no "results may vary." ML reproducibility is a known open sore; a
   substrate where the eval ledger is content-addressed and confluent is a real
   contribution, and S2/S3's "recomputable by a stranger" predicates are its proof.
2. **JEV/typesafe.ai as a legality-vs-calibration-*separated* signal.** The two-floors
   framing (P5, measured in S4) is ours: most reward-model / LLM-judge work conflates "well-
   formed and confident" with "correct." Separating them, and showing the off-diagonal is
   populated and *useful for selection*, is a clean, publishable result about judge design.
3. **Trust-gluing as verifiable ensembling (G11).** A federated ensemble whose aggregate
   any node recomputes from booked deposits + a local trust map, where a stranger's weight
   defaults to zero and is earned per-class, revocably — that is not a softmax gate. S2 is
   its experiment.
4. **The Reader's Fold as distillation-without-carried-verdicts (Law 6).** "Aggregate the
   folds, not the verdicts; a cheap model earns a class only when a reader reproduces it"
   is a distillation *principle* with a mechanism (P4 + P2), and G20's Second-Reader
   discipline is the same idea turned on the cluster's own outputs. S1+S7 are its ladder
   from in-context to moved-weights.

**Table-stakes we borrow (orchestration, not novelty — say so):** best-of-N sampling; MoE
routing; LoRA/distillation itself; hyper-parameter search (S6); self-play curricula (S5's
core mechanic). We are not claiming to invent these. Our claim is *what we compose them
with* — the booked substrate, the reproduction gate, the two floors, the verdict-free wire.

**What is just orchestration and should never be dressed as ML:** S3 and S6 are
orchestration/measurement intelligence — no weights move. They are real, useful, and
honest as *systems* results, not learning results. Calling them "the cluster learns" would
be the exact Goodhart O9 guards against.

---

## 4. Honest limits

**What we have:** prompt-level orchestration, cheap funded API inference (DeepSeek +
DeepInfra), a real verification/scoring oracle (`jev-1.13.0`), and a booked, replayable
substrate to serve as the eval ledger. **What we do not have (yet):** our own GPU training.
Nothing above except S7 moves a weight.

**Real ML (weights move) vs in-context/orchestration intelligence:**

- **Weights move:** only **S7** (LoRA/distill), and it is STRETCH — it needs a fine-tune
  surface we have not confirmed. Everything else is selection, routing, ensembling, or
  config search over frozen models.
- **In-context / orchestration intelligence (funded-now):** S1 (selection + in-context
  distillation via the commons), S2 (ensembling), S3 (org metabolism), S4 (judge
  characterization), S5 (curriculum), S6 (config search). These make the *cluster* smarter
  without any model getting smarter — which is precisely the thesis (P1–P6), and also
  precisely the ceiling: a frozen cheap model is still a frozen cheap model.

**The smallest real "weights-move" experiment:** one LoRA on
`meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` (if DeepInfra exposes fine-tuning) — or a
local LoRA on a 1–3B open model otherwise — trained on **a few hundred reproduction-gated
vs ungated examples for a single task-class from S1**, evaluated on a held-out split, with
the predicate `gated > ungated > base`. That is the whole thing: one adapter, one class,
one day of one small GPU. It converts our best in-context result (the G16 gate as a data
filter) into a moved-weights result, and it is the honest boundary between what we can run
this week and what needs real compute.

**Infra blockers, named (not hidden):**

- `experiment-proxy` (keyless JEV/moth access) needs `CLOUDFLARE_API_TOKEN` +
  `CLOUDFLARE_ACCOUNT_ID` to deploy (`tools/experiment-proxy/README.md`). Until then, JEV
  studies (S1 legality floor, S4, S5 guard) need a direct `TYPESAFEAI_KEY` call from an env
  that holds it, or they run correctness-floor-only (O12 fallback) at reduced power.
- **GLM/Kimi are unfunded** (`ROSTER.md`): authenticate, reject completions on balance.
  Every study above is specified to run on DeepSeek + DeepInfra alone; GLM/Kimi are the
  STRETCH "high-tier orchestrator / long-context" upgrade path, not a dependency.
- **JEV judges canon-alignment and confidence, not arbitrary ground truth.** It is a floor,
  not an oracle (P5). Any predicate that leaned on JEV *as* correctness would be wrong; S4
  exists to keep us honest about exactly this.
- **DeepInfra "thinking"-class models silently return empty content** without a large token
  budget (`ROSTER.md` `Qwen3.5-27B` gotcha) — a real orchestration hazard for S2's cast;
  budget ≥1000 tokens or use the confirmed-good small Llama.

---

## 5. What to run first (the funded-now week)

If the dispatcher books one thing: **S4** (cheapest, validates the two-floors premise the
rest leans on). Then **S1** and **S2** in parallel (they share the candidate-generation
harness and the booked eval; S1 feeds S7's data). **S3** rides along on whatever tasks
S1/S2 generate — it needs no new inference, only instrumentation over the ledger. S5 and S6
are the second wave; S7 waits on a fine-tune surface.

Everything above is a rung with a predicate, a tier, and a tag. None of it is built by this
file. The dispatcher books; the substrate replays; a stranger checks the numbers.

*Carry the evidence, never the verdict. Aggregate the folds, not the votes. Let the cheap
tier earn its class only when a second reader agrees. Measure legal and good on separate
floors. Then read the red bar honestly.*

🦋 → ⏳ → 🔧 → 🌊
