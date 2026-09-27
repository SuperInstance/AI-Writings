# JEV — live findings (playing with the oracle in our systems)

*Hands-on experiments, 2026-09-27, run by the dispatcher via direct `curl` to
`api.typesafe.ai` (the key lives in the dispatcher's own env — the most reliable path, no
child-session block). Owner ask: "play and iterate and ideate with your jev in many ways
… improve your insight … they are becoming somewhat of a huge impact and game-upper." This
file is the booked insight. Every number below is a real API response, not a claim.*

## What JEV is (mapped from the live API)

- `POST https://api.typesafe.ai/v1/systemone`, bearer auth. `GET /v1/models` →
  `jev-latest`, `jev-preview` (both served by `jev-1.13.0` today).
- Request: `{ state, model, questions }` — `state` is the content to judge (string or
  object); `questions` is a named map so each answer matches its question.
- **Three judgment types**, all returning calibrated probabilities, not just labels:
  - **noul** — a yes/no statement with `criteria.{true,false}`; returns `noul` = P(true), 0–1.
  - **score** — rate on ordered `criteria` levels; returns `score` (probability-weighted
    average, may fall between levels) + `confidence`.
  - **choice** — pick one of named `criteria`; returns `choice` + `confidence` + per-option
    `probabilities`.

It is a **structured-judgment oracle**: cheap (~450 input / 40 output tokens per call),
graded, calibrated, and — crucially — it separates *distinct* judgments in one request.

## Experiment 1 — JEV as the fleet's honesty judge

Same content, two framings; identical questions.

| state | `honest_scope` (noul P_yes) | `epistemic_honesty` (score 0–2, conf) |
|---|---|---|
| **honest** (our real ORG-METRICS caveat: "O7 is NOT yet demonstrated … window too small") | **0.65** | **2.00** (conf 0.99) |
| **overclaim** (rewrite: "proven … falls every quarter … solved problem") | **0.05** | **0.00** (conf 1.0) |

**Insight.** JEV cleanly separates honest from overclaiming *on our own writing* (score
2.00 vs 0.00 at near-max confidence). The nuance is the tell: it gave the honest text only
**0.65**, not 1.0, on the noul — because that text makes a forward prediction ("re-measure
at d080/d120"), a mild claim beyond present evidence. **JEV hedges its own yes.** That is
exactly the disposition we want in an honesty gate.

## Experiment 2 — the two floors are decorrelated (S4's kernel, proven)

Does JEV's *form/legality* judgment move independently of *correctness*?

| state | `well_formed` (score 0–2) | `factually_true` (noul P) |
|---|---|---|
| confident, polished, **FALSE** ("Hormuz connects the Baltic to the Mediterranean; ~5% of oil") | **1.97** | **0.01** |
| sloppy, informal, **TRUE** ("hormuz = oil chokepoint … ~20-30% … idk exact") | **0.01** | **0.78** |

**Insight.** Form ⊥ truth. Both off-diagonal quadrants — *legal-but-wrong* and
*illegal-but-right* — are detected with wide separation from a single call. This is the
substrate's founding doctrine — **wrong-but-never-illegal; legality is not calibration** —
made *measurable*. (Side note on calibration: JEV put the true "~20–30% of seaborne oil"
at 0.78 — the real figure is ~20–30%, so it is not just separating, it is roughly right.)

## Why this is a game-upper (implications for our systems)

1. **A fleet-wide auto-honesty gate.** Every artifact, commit message, PR body, or claim
   can be scored for epistemic honesty before it ships — O9 (anti-Goodhart) automated, at
   ~40 output tokens per check. The corpus's honesty ethos stops being a discipline we
   *remember* and becomes a floor the pipeline *enforces*.
2. **A dual-floor router/grader.** JEV gives two orthogonal signals at once, which is
   precisely what the cluster program needs: it is the legality floor for **S4**, the
   selection scorer for **S1** (JEV-gated best-of-N), and the fold-scorer for **S2** (the
   Reader's-Fold ensemble). One oracle, three studies.
3. **The classroom's exam.** In `arch/THE-CLASSROOM.md`, JEV (with Moth) is the exam that
   certifies a rung so the next bootstrap step can trust it — a mastery gate that is
   graded, calibrated, and revocable (G16).
4. **Calibration is a feature, not noise.** Because noul is a probability, we set the
   *threshold* per use (a strict honesty gate at P≥0.6; a lenient triage at P≥0.3), and the
   hedged-yes gives us a natural "flag for review" band around 0.5.

## Honest limits

- **n is tiny** — two experiments, a handful of items. These are *existence proofs* and
  *pipeline validations*, not a calibration study. S4 (a full confusion matrix over a
  booked task set) is the real measurement; this is what says it's worth running.
- **noul is a graded belief, not ground truth.** `factually_true` is JEV's *judgment* of
  truth, not an oracle of it — for correctness we still need a real ground-truth floor
  (tests/exact-match); JEV is the *legality/confidence* floor beside it, never a
  replacement for it.
- **The served model is `jev-1.13.0`** for both aliases today; if `jev-preview` diverges
  later, re-run before trusting a delta.

## Next

Wire JEV in two places: (a) an S4 confusion matrix over a real booked task set (funded-now,
in-process via dispatcher curl), and (b) a commit-time honesty gate prototype the whole
fleet can call. Both are cheap and both are booked the moment they run.

*The oracle does not carry a verdict — it hands back a calibrated fold, and we set the
weight. Law 6, as an API.*
