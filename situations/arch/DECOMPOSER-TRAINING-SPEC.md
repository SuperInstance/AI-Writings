# Decomposer training spec — how a model consumes this corpus when the time comes

*A spec-mark (2026-09-29). Owner's end-goal: "make sure the right information is saved so that when
the time comes, a model can help decompose." The information is saved (see
INTER-RELATIONAL-INTELLIGENCE.md, CORPUS-REPORT.md); this is the recipe for turning it into a model,
with the honest bar each objective must clear before it is worth shipping. Nothing here is asserted
to work yet — the corpus is still thin (3 folds). This is the plan the volume unlocks.*

## Inputs (materialize first)

`bash labs/situation-recorder/run_all.sh` writes `situations/corpus/{decompositions,routes,
judgments}.jsonl`. Schemas in `situations/corpus/README.md`. Every row descends from a
chain-verified transcript; the `corpus` CI gate refuses a broken chain, so the training set is
tamper-evident by construction — the MLOps "can't reproduce the data" failure is closed here.

## Objective 1 — the decomposer (learn to localize the weakest leaf)

- **Task.** Given the leaf *texts* of a decomposed claim (NOT the oracle verdicts), predict which
  leaf is weakest.
- **Data.** `decompositions.jsonl`; features = leaf texts (+ claim context); label = `weakest_index`
  among the substantive leaves (exclude `is_whole`).
- **Baseline to beat.** `labs/situation-recorder/baseline_decompose.py` — random base rate ≈ 1/n
  (0.29 now), lexical baseline ≈ 0.33 (noise). A learned model must beat the base rate by a margin
  on a held-out split, or it is not earned.
- **The hard truth it must respect (Law 7).** The lexical baseline scores **0/2 on factual-error
  folds** — there is no surface tell for "gold is Ag." A pure text model of leaves *cannot* localize
  factual folds by style; it must **buy reach** — condition on evidence a reader with independent
  reach supplies (JEV verdicts as features at train time; a symbolic checker for counting/spelling,
  JEV's own blind spot). Training a bigger lexical model is the wrong axis. This is the single most
  important design constraint.
- **Fit.** A ≤3B QLoRA or a small classifier fits the RTX 4050 (GPU-DOCKET D4/D5). Labels are free
  (the referee already produced them), so training is cheap.

## Objective 2 — the dispatch router (learn who to hand the oars to)

- **Task.** Given a subtask, choose the crew/tool that minimizes realized cost / time-to-green at
  acceptable quality.
- **Data.** `routes.jsonl` (`subtask, to, why, outcome`) joined to the ledger's cost_class/standing.
- **The base rate that matters is brutal and must be stated.** Outcomes are **86% DONE**, so a model
  that predicts "DONE" scores 0.86 and is **useless**. Accuracy is the wrong metric. The router is a
  **policy**, evaluated by realized cost/quality among the arm it *chose* — and the corpus only
  records the arm that was chosen (confounding: we never see how the unchosen crew would have done).
- **Therefore the router is not learnable from observational routes alone.** It needs either logged
  alternatives or **exploration** — which is exactly why `DRAW` records exist: Moth/MicroMoth-quilt
  draws that force an un-steerable arm choice on some fraction of dispatches turn the log into an
  off-policy-evaluable dataset (contextual-bandit shape). Until DRAW-gated routing runs, treat
  Objective 2 as **descriptive only** (cost/outcome summaries), not a trained policy. Do not ship a
  router trained on confounded observational data.

## Objective 3 — the value model (was a KEEP/DROP worth it?)

- **Task.** Predict whether a captain's KEEP/DROP agreed with the realized downstream `OUTCOME`.
- **Data.** `judgments.jsonl` + reachable outcome. Currently n=1 — a placeholder until capture volume
  arrives. Booked scars (DROP → good outcome) are the gold negatives.

## Splits and hygiene (non-negotiable)

- **Temporal split.** Train only on situations before a cutoff time; git's order + `ts` prevent
  leakage. Never shuffle across time.
- **Provenance filter (don't learn from your own shadow).** `backfill-from-ledger (reconstructed)`
  rows have no real FOLD/DRAW — never train the decomposer on them; the router may use their routes
  as descriptive context only. Live-captured folds are the only decomposer training data.
- **Un-gameable eval.** Choose the eval fold with a Moth/MicroMoth-quilt draw so no one can steer the
  test set (records the draw in the run's transcript — the eval is itself a captured situation).
- **Honest labels.** A hidden failure is a mislabeled example; the fleet's booked-scar ethos is
  literally clean data. Keep it.

## The "earned, not asserted" gate (ML-IN-THE-LOOP.md)

Ship a learned cell (`labs/ci-brain`) only when, on a temporal + provenance-clean held-out split:
(1) N is past a pre-registered minimum (decomposer: ≥ ~50 live folds spanning ≥2 fold types), and
(2) it beats the stated base rate by a margin that survives the small-N confidence interval, and
(3) its own accuracy is booked in the ledger like any cell — a model that got worse is a scar, not a
silent rollback. Until all three hold, the base rate script *is* the deliverable, honestly.

## The consumption interface (one paragraph a future builder can run)

```bash
bash labs/situation-recorder/run_all.sh            # verify chains, materialize tables, print base rate
python3 - <<'PY'
import json
folds  = [json.loads(l) for l in open("situations/corpus/decompositions.jsonl")]
live   = [f for f in folds if "reconstructed" not in (f.get("leaves") and "" or "")]  # provenance filter
# X = leaf texts (+ optional JEV verdicts to BUY reach); y = f["weakest_index"]; temporal split by sid/ts
PY
```

The corpus grows every dispatch; the moment live folds clear the gate, this spec is the switch from
"saved" to "a model that helps decompose." That is the whole point of saving it this way.
