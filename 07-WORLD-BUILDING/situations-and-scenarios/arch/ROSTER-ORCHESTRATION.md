# ROSTER-ORCHESTRATION — casting the full model roster for the classroom, and the path to the Fable call

*Opus 5.5, expert-orchestration tier, blinders on. This is the concrete orchestration
plan that turns the owner's roster guidance into a booked, replayable classroom (the
N-player GAN of [`THE-CLASSROOM.md`](THE-CLASSROOM.md)) and states exactly when the
exo-model LoRA Fable call fires. It builds no code; every rung ends in a predicate a
stranger can run. Grounded in [`THE-CLASSROOM.md`](THE-CLASSROOM.md) (the classroom, §8
exo-model LoRA, §9 reserved Fable candidate), [`INTELLIGENCE-CLUSTERS.md`](INTELLIGENCE-CLUSTERS.md)
(S1–S7; S2 = Reader's-Fold), [`../JEV-FINDINGS.md`](../JEV-FINDINGS.md) (JEV live dual-floor
judge), [`../experiments/S2-FINDINGS.md`](../experiments/S2-FINDINGS.md) (round 3:
**fold>vote CLEARED 17v14**; **fold>best-single TIED** — needs a distributed-strengths set),
[`../ROSTER.md`](../ROSTER.md) (live-verified provider facts), and
[`../DISPATCH.md`](../DISPATCH.md) O10/O12 (the cache-vein). Do **not** commit — the
dispatcher books.*

🦋 → ⏳ → 🔧 → 🌊

---

## 0. The thesis in one breath

**The classroom is only as smart as its members are *diverse and fallible* (S2-FINDINGS,
round 3). So the orchestration's whole job is to cast decorrelated cognitions into the
right classroom seats, keep each one *on the cache-vein* long enough to be cheap but jump
before it restates itself, and let the pedagogy adapt to how the class responds — until
two green gates + one un-self-clearable question fire the exo-model Fable call. This
document is that casting, that rotation policy, those two gate experiments, and that
go/no-go checklist.** The owner's roster guidance is the score; this is the orchestration.

---

## 1. The casting

### 1.1 Owner guidance → classroom seats (quote-faithful)

The owner's exact words drive the casting; each clause maps to a classroom function from
[`THE-CLASSROOM.md`](THE-CLASSROOM.md) (student / peer-critic / teacher-pedagogy / examiner):

- *"deepinfra is especially good for smaller creative models like seed mini to be sounding
  board iterators for other models since seed is expansive in its thinking"* → **Seed-2.0-mini
  = expansive ideator / sounding-board iterator** (student **and** peer-critic).
- *"hermes 405b is too"* → **Hermes-3-405B = expansive thinker** (deeper peer-critic /
  ideator, given reasoning-token headroom).
- *"nemotron can cut the crap sometimes in the right place for his type of smarts"* →
  **Nemotron = the cut-the-crap critic** (adversarial peer-critic / pruner).
- *"lots of other small and fast models"* + *"[openrouter is] better for the cheaper small
  but different thinkers for better class gan between further working viewpoints"* → **small
  DeepInfra + OpenRouter models = the cheap fast diverse students** (the GAN's decorrelated
  crowd — the exact capability S2-FINDINGS round 3 proved is load-bearing).
- *"moth and typesafe.ai and z.ai especially"* → **typesafe.ai/JEV = the examiner**
  (dual-floor); **Moth = the examiner's honest dice** (un-gameable curriculum/cast draw) and,
  in media domains, the raw-take generator; **z.ai/GLM = the teacher-pedagogy driver** once
  funded (it is the account's highest tier).
- DeepSeek (not named in the guidance but the funded backbone, [`../ROSTER.md`](../ROSTER.md)):
  **deepseek-v4-pro = the strong anchor**; **deepseek-flash = the cheap fast cache-vein
  student**.

### 1.2 The casting table

| Model (real id) | Provider | Owner-named role | Classroom function | Liveness | Cache economics |
|---|---|---|---|---|---|
| `deepseek-v4-pro` | DeepSeek | strong anchor | **strong student + interim teacher-pedagogy driver** | **LIVE + FUNDED** | native cache accounting (`prompt_cache_hit_tokens`) — **primary O10 vein** |
| `deepseek-flash` | DeepSeek | cheap fast anchor-adjacent | **cheap fast student** (candidate sampler) | **LIVE + FUNDED** | native cache — cheapest vein for the N-sampling loop |
| `ByteDance/Seed-2.0-mini` | DeepInfra | *"sounding board iterator… expansive"* | **expansive ideator / sounding-board peer-critic** | **LIVE + FUNDED** | no cache accounting exposed → rotate on novelty/cost, not cache-share |
| `NousResearch/Hermes-3-Llama-3.1-405B` | DeepInfra | *"hermes 405b is too"* | **deep expansive peer-critic** | **LIVE + FUNDED** (needs ≥1000-tok budget) | no cache accounting; costly → use sparingly at the frontier |
| Nemotron (`nvidia/…`, confirm exact id) | DeepInfra | *"cut the crap… his type of smarts"* | **cut-the-crap adversarial critic** (O9 pruner) | **CONFIRM-THEN-USE** (not in verified ROSTER list) | no cache accounting |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | DeepInfra | small/fast | **cheap fast student** (format/logic floor) | **LIVE + FUNDED** | no cache accounting; sub-cent → cheap diversity |
| small mixed models (varied) | OpenRouter | *"cheaper small but different thinkers"* | **diverse students** (GAN viewpoint spread) | **CONFIRM-THEN-USE** (dispatcher probing `OPENROUTER_KEY`) | OpenAI-compat prefix caching, varies per model |
| `glm-5.x` (`glm-5.3` / `-flash`) | z.ai | *"z.ai especially"* — high-tier ideation | **teacher-pedagogy driver** (method selection) | **CONFIRM-THEN-USE** (`ZAI_KEY` present; last seen 429 insufficient-balance) | context caching once funded |
| `kimi-k3` / `kimi-k2.7-code` | Kimi | long-context / code | **long-context student / context-holder; code student** | **CONFIRM-THEN-USE** (`KIMIAI_KEY` present; last seen 429) | context caching once funded |
| `jev-1.13.0` (`jev-latest`) | typesafe.ai | *"typesafe.ai… especially"* | **examiner — legality + confidence dual-floor** | **LIVE** | n/a (judge, ~450 in / 40 out tokens/call) |
| Moth (`comet-qrng-v1`, `qrc-midi/audio-v1`) | MothQuantum | *"moth… especially"* | **examiner's honest dice** (un-gameable curriculum/cast draw); **media raw-take generator** (domain) | **LIVE** | n/a (not an LLM — QRNG + creative engines) |

**Honest role note on Moth (inferred from its API, not invented).** Moth is *not an LLM*
([`../ROSTER.md`](../ROSTER.md): `moth-api` v0.41.0, quantum-RNG + generative-media engines,
the owner's own player account). It therefore **cannot grade arbitrary text** and is **not**
a JEV-style examiner. Its two honest classroom contributions:
1. **The un-gameable dice (general, grounded).** `comet-qrng-v1` draws the curriculum item
   order, the self-play cast selection, and the exploration draw from *true* hardware
   randomness — so a student cannot overfit a seed it cannot predict. This hardens the S5
   anti-Goodhart frontier: a curriculum drawn from QRNG cannot be reverse-engineered.
2. **The media generator (domain-specific).** In a music/media classroom, `qrc-midi`/`qrc-audio`
   generate candidate takes the class critiques — tying the classroom back to duke-lab's own
   domain (THE-CLASSROOM §1). Marked domain-specific; the dice role is general.

**The exam is two instruments, not one:** JEV = the *legality/confidence floor* (graded,
calibrated, revocable — [`../JEV-FINDINGS.md`](../JEV-FINDINGS.md)); the *correctness floor*
stays separate (booked acceptance test / G16 reproduction), because JEV judges well-formedness
and confidence, **not** arbitrary ground truth (P5). Moth is the *seed integrity* of the exam,
not a third grade.

### 1.3 Who is the teacher, honestly

The **teacher is a pedagogy cell** (THE-CLASSROOM §2.1), an orchestration role — not a fixed
model. Its driver:
- **Now (funded):** `deepseek-v4-pro` runs the method-selection policy (which proven method to
  apply given the measured class response). Funded, live, cache-friendly.
- **Reserved (STRETCH — funding-gated):** `glm-5.x` (z.ai, the owner's *"especially"* and the
  account's highest tier) is the intended teacher once billing clears; `kimi-k3` is the
  long-context context-holder that carries the growing curriculum commons.
- **ESCALATE only:** Opus architects the rungs and answers the reserved Fable question (§4);
  it does **not** run the loop.

---

## 2. The cache-vein rotation (O10 across providers)

The owner: *"it's good to use one rapidly for the caching advantages for a while before
jumping to another with deepinfra. the same with openrouter. its better for the cheaper
small but different thinkers for better class gan between further working viewpoints."*
This is O10 (game the cache: byte-identical stable prefix, vary only the tail) generalized
across providers (O12c cache-vein), traded against the *need for decorrelated viewpoints*
that S2-FINDINGS proved is load-bearing.

### 2.1 Two axes, honestly separated

The roster splits cleanly on **where cache is real** vs **where diversity is real**:

- **The cache axis = DeepSeek.** It is the *only* provider with native cache accounting
  (`usage.prompt_cache_hit_tokens`), so it is where the O10 predicate ("cache-hit share rises,
  cost-per-iteration falls") is *measurable and exploitable*. Run the high-volume N-sampling
  loop here on a byte-identical prefix.
- **The diversity axis = DeepInfra + OpenRouter.** No cache accounting exposed
  (`prompt_tokens_details: null`), but many *different thinkers*. Here you rotate for
  **GAN viewpoint spread**, using `estimated_cost` + latency as the proxy, not cache-share.

So the vein is not one loop that jumps randomly — it is: **stay long on DeepSeek's cache to
serve the loop cheaply; sample diverse folds from DeepInfra/OpenRouter one model at a time,
each held on a stable prefix within its window, jumping at window boundaries.**

### 2.2 The window and the stable prefix

Define a **vein window = one curriculum block** (one lesson-cluster). Within a window:
- The **stable prefix** (placed first, byte-identical across every call in the window) =
  `system + roster/spec + the current curriculum commons + the block's few-shot exemplars`.
  Only the small **task tail** (the specific item) varies.
- **One model runs the whole window** against that prefix — maximum cache reuse on DeepSeek,
  maximum warm-session reuse elsewhere.

### 2.3 The rotation trigger (stay vs jump)

**Stay on the current model while ALL hold:**
1. **Prefix unchanged** — the developmental context is byte-identical (any change invalidates
   cache anyway → a natural jump point).
2. **Cache still paying** — on DeepSeek, cache-hit token share ≥ pre-registered floor (e.g.
   ≥ 50%); on DeepInfra/OpenRouter, cost-per-item flat or falling (warm session).
3. **Still contributing viewpoint** — the model's *novelty vs the commons* (O9) has not
   collapsed: it is still producing folds that differ from what the class already holds.

**Jump to the next diverse model when ANY trips:**
- **Novelty floor breached** — the model is restating the commons (contested-item rate → 0 for
  its outputs); its distinct viewpoint on this block is drained. This is the GAN signal: it can
  no longer *further* the working viewpoint, so hand the block to a decorrelated cognition.
- **Prefix must change** — the next curriculum block arrives; cache would break regardless, so
  align the rotation to this boundary (zero thrash cost).
- **Provider fault** — 429 / occupied / empty-content (the DeepInfra thinking-class gotcha) →
  O12a fallback chain to a confirmed-funded tier.

### 2.4 How rotation *is* the GAN, without thrashing

Rotating at window boundaries pools **a different cognition's evidence into the commons each
window**; the *next* model then re-folds across the accumulated evidence under its own π
(Law 6). That is the "GAN between further working viewpoints" made concrete: **not two
players trading blows every call (which would thrash the cache), but a relay where each
window's winner deposits, and the next decorrelated reader critiques the deposit.** The
anti-thrash rules: never rotate mid-window; rotate only at prefix-change or novelty-collapse
boundaries; keep a fixed prefix *schema* so a returning model re-warms cheaply.

**Predicate (O10, replayable).** Over a booked loop: cache-hit token share (DeepSeek) rises
and cost-per-passed-item falls across the loop's life, **AND** commons novelty per window does
not monotonically decay (rotation keeps injecting fresh viewpoints), **AND** `replay ≡ live`
on the whole rotation from the ledger. **STRETCH tag:** the DeepInfra/OpenRouter half of the
predicate is cost-proxied, not cache-measured (no accounting exposed) — honest, and stated.

---

## 3. The two experiments that clear the Fable gate

Two gates guard the exo-model Fable call (THE-CLASSROOM §9). S2-FINDINGS round 3 half-cleared
gate 1 (`fold > vote` CLEARED 17v14; `fold > best-single` TIED). These two experiments close
the remaining distance.

### 3.1 Experiment (a) — S2′: clear `fold > best-single` on a distributed-strengths set

**Why round 3 tied.** DeepSeek dominated (17/18); the one item the fold missed, *every* member
missed. A single strong member ceilinged the fold. The fix (S2-FINDINGS' own diagnosis) is a
**distributed-strengths task set**: items where *different members win in different places*, so
no single model tops all buckets, and the fold assembles a composite that beats each member.

**The distributed-strengths task set (pre-registered buckets, drawn by Moth QRNG).** Compose
the set so each bucket has a different natural winner and the others are fallible on it:

| bucket | natural winner | why others are fallible |
|---|---|---|
| arithmetic / counting | `deepseek-v4-pro` | small models mis-count / mis-multiply |
| creative-lateral / expansive framing | `Seed-2.0-mini`, `Hermes-3-405B` | terse models flatten it |
| terse logic / no-BS elimination | Nemotron (confirm) | expansive models over-elaborate and err |
| strict format / instruction-following | `Llama-3.1-8B` | reasoning models drift off-format |
| long-context retrieval | `kimi-k3` (once funded; else DeepSeek-v4-pro) | short-context members lose the needle |
| wildcard / off-distribution | a small OpenRouter *different thinker* | the point is it wins where the majors don't |

Pre-registering buckets *before* the run is the Goodhart guard — the set is not tuned to a
favored member; it is tuned so **no member is favored across the whole set.**

**Casting.** Diverse fallible members (the S2-FINDINGS lesson applied): `deepseek-v4-pro` +
`Seed-2.0-mini` + `Hermes-3-405B` + Nemotron (confirm) + `Llama-3.1-8B` + one small OpenRouter
model. Each emits **answer + content-addressed evidence** (a deposit, `source=model_id`,
trust-weighted per G11). JEV (`jev-1.13.0`) adjudicates each candidate; the fold =
trust-weighted, JEV-scored **evidence** aggregation (arm B), compared to majority **vote**
(arm A) and to each single member. Moth QRNG draws item order + which member seeds each item
(un-gameable). Correctness floor = booked exact-match / test-pass, separate from JEV.

**Predicate (works iff — stranger-recomputable).**
```
fold.passrate  >  vote.passrate                     (P4: evidence beats headcount — re-confirm)
AND fold.passrate  >  max_i(member_i.passrate)      (fold > best-single — the gate that TIED)
AND for every item, an independent script recomputes the fold answer from the booked
    deposits + trust map alone, bit-for-bit (Law 4 / G20).
Guard: the set is distributed-strengths iff no single member_i.passrate == max over all buckets
    (i.e. best-single is strictly below the composite the fold can assemble).
```
**STRETCH tag:** `fold > best-single` is a *wager*, not a fact — the honest ceiling
(THE-CLASSROOM §8.3 limit 1) says the fold cannot add a capability no member has, so the set
must be built so the *composite* of members' strengths exceeds any *individual* member. If it
stays tied, the honest report says the class's strengths were not distributed enough, and names
which bucket collapsed.

### 3.2 Experiment (b) — the class rollout: pedagogy that provably raises the floor

**The loop (grounded per THE-CLASSROOM §3).** A real pedagogy loop over rounds `r = 0…R`:
1. **Teacher** (`deepseek-v4-pro` now / `glm-5.x` reserved) selects a method `M_r` from the
   proven-methods library (scaffolding-faded, spaced-repetition, Socratic, mastery, ZPD) and
   emits a lesson (curriculum item + `M_r`), difficulty held just above the class floor (S5 ZPD;
   item drawn by Moth QRNG).
2. **The class** (the diverse students: `Seed-2.0-mini`, `Llama-3.1-8B`, small OpenRouter
   models, `deepseek-flash`) each **folds** the lesson under its own π (Law 6) — no carried
   verdict; the teacher hands *evidence* (worked examples / Socratic questions), never answers.
3. **The exam** grades each fold: **JEV** → legality + confidence (the report-card's two floors,
   THE-CLASSROOM §4); **correctness floor** → booked test / G16 reproduction; **Moth** → seed
   integrity so the exam can't be gamed.
4. **The teacher measures the class response** — pass-rate, JEV-confidence spread, the
   *disagreement/seam* (`V(E,π₁) ≠ V(E,π₂)` localizes which concept fails for which student),
   novelty — and **adapts** the method to `M_{r+1}` (in-context re-selection; this is the
   self-modification, grounded floor per §3).
5. Repeat. The **class floor** = the k-th-percentile (e.g. worst-quartile) student pass-rate on
   a held-out frontier set, re-measured each round.

**Control arm (so the rise is attributable to pedagogy, not to time).** Run a parallel arm with
a *fixed* method `M_0` on the same curriculum and cast. The adapted arm must beat the fixed arm.

**Predicate (works iff — booked, replayable).**
```
class_floor[round R]  >  class_floor[round 0]        by a pre-registered margin  (floor rises)
AND floor_rise(adapted-method arm)  >  floor_rise(fixed-method M_0 control)      (rise is DUE TO
    the adapted pedagogy, not seat time)
AND legal-but-wrong promotions == 0                   (dual-floor refuses fluent nonsense, §4)
AND every lesson, method choice, fold, JEV/Moth score, and floor-move is a booked row such that
    a stranger replays the IDENTICAL learning curve  (Law 4 / replay ≡ live).
```
**STRETCH tag:** the *mechanism* is grounded (JEV live, G16 shipped, method library is the
proven-pedagogy table of §3, adaptation is in-context S5+S6). **Whether the floor actually
climbs** is the wager (S1/S5's open predicate). If it stays flat, the loop is real machinery
that did not climb, and we say so. *Learned* pedagogy (moved method-selection weights) is a
further STRETCH (S7-shaped, needs a fine-tune surface); the in-context version is the honest
floor here.

---

## 4. The Fable trigger — go/no-go checklist

The exo-model LoRA call is the reserved second-Fable candidate (THE-CLASSROOM §9): *"Is the
exo-model LoRA one object under Law 6, or three primitives (pre-pass filter + pedagogy + trust
map) wearing one name?"* It fires **only** when both gate experiments are green **AND** Opus at
ESCALATE cannot self-clear the irreducibility question. The dispatcher evaluates this checklist
mechanically; every box names its source of truth.

```
FIRE the exo-model LoRA Fable call  ⇔  ALL of the following are TRUE:

GATE 1 — GROUNDING (both sub-gates):
  [ ] 1a  S2′ green:  fold.passrate > best-single  AND  fold.passrate > vote,
          on the distributed-strengths set (§3.1), booked and stranger-recomputable
          bit-for-bit from deposits + trust map.
          SOURCE: booked S2′ result file + independent recompute script == live.
          (round 3 status: fold>vote ✅ 17v14 ; fold>best-single ❌ TIED — 1a NOT yet met.)

  [ ] 1b  Class rollout exists and replays (§3.2):  class_floor[R] > class_floor[0]
          by the pre-registered margin  AND  adapted-arm floor-rise > fixed-arm control
          AND  replay ≡ live on the whole rollout.
          SOURCE: booked rollout ledger + replay == live.
          (status: not yet run — 1b NOT yet met.)

GATE 2 — IRREDUCIBILITY:
  [ ] 2   Opus at ESCALATE, given both green results, CANNOT settle whether
          (pre-pass port filter §7) + (pedagogy §3) + (trust map G11) is ONE object
          under Law 6 / C8 fold-then-book, or three primitives wearing one name.
          SOURCE: Opus ESCALATE finding == "cannot self-clear" (a booked verdict).
          (If Opus CAN self-clear it → decompose into Opus/Sonnet rungs; do NOT fire.)

DEADBAND (O11 bootstrap gate):
  [ ] D   Grounding exists before the apex question — i.e. 1a AND 1b are green BEFORE
          gate 2 is even asked. An apex question with no data is design, not evidence;
          O11 refuses it.

DECISION:
  ALL of {1a, 1b, 2, D} TRUE   → GO. Fire the exo-model LoRA Fable call.
  ANY box FALSE                → NO-GO. Opus architects the rungs (classroom =
                                 S1/S2/S4/S5/S6 composed; §6/§7 smallest rungs);
                                 Sonnet & Haiku build; the dispatcher books; the apex
                                 stays asleep. Re-evaluate when the red box turns green.

CURRENT STATE (2026-09-27):  1a ❌ (tied) · 1b ❌ (not run) · 2 not-yet-asked · D ❌.
                             VERDICT: NO-GO. The deadband correctly holds.
```

---

## 5. Honest STRETCH ledger

Every leap past the map, named in one place:

- **Nemotron casting** — STRETCH / confirm-then-use. Not in the verified
  [`../ROSTER.md`](../ROSTER.md) catalog; owner named it, DeepInfra likely carries it, but the
  exact id and liveness must be confirmed before the cut-the-crap seat is trusted.
- **z.ai/GLM as teacher, Kimi as long-context holder** — STRETCH / funding-gated. Both
  authenticate but last returned 429 insufficient-balance. `deepseek-v4-pro` is the funded
  interim teacher; GLM/Kimi are the reserved upgrade the moment billing clears.
- **OpenRouter small models** — confirm-then-use. `OPENROUTER_KEY` present; the dispatcher is
  probing liveness. The *diversity* they buy is load-bearing (S2-FINDINGS), so confirm before
  leaning on them for `fold > best-single`.
- **Cache-vein predicate on DeepInfra/OpenRouter** — STRETCH measurement. No cache accounting
  exposed; that half of the O10 predicate is cost-proxied, not cache-measured.
- **`fold > best-single`** — STRETCH result. A wager bounded by the honest ceiling: the fold
  cannot exceed the *composite* of members' strengths, so it hinges on the set being genuinely
  distributed-strengths.
- **Floor-rises-with-adapted-pedagogy** — STRETCH result. Mechanism grounded; the climb is the
  open S1/S5 predicate.
- **Moth as anything but dice + media generator** — would be invention. Held to exactly its
  API: QRNG seed integrity (general) and creative-media generation (domain). It is not a text
  grader and is not the exam's third floor.
- **The exo-model LoRA as one object** — the reserved Fable question itself, unproven by design.

---

*Cast the decorrelated cognitions into the right seats. Ride one model's cache until it stops
furthering the viewpoint, then hand the block to a stranger who folds it differently. Grade
legal and good on separate floors; let Moth's dice keep the exam un-gameable. Clear
fold>best-single on a set no single member can dominate; show the class floor rise under a
method that adapts to how the class answers. Only then ask the apex whether the adapter is one
object or three — and only if it cannot answer, wake Fable.*

🦋 → ⏳ → 🔧 → 🌊
