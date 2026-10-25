# mark 0001 — rubric-forge

*First mark in `ai-writings/docs/marks/`. The directory didn't exist yet, so this is 0001. The format
follows the Syzygy mark vocabulary (`SuperInstance/Syzygy` `docs/marks/MARKS.md`), and the STATE
word comes from there too.*

**WHAT** — `labs/rubric-forge/`, item #4 of `situations/arch/RD-MODULAR-TOOLS.md`. It takes a JEV
`FOLD` record and produces a weighted rubric `{criterion, weight, score, influence}` plus one dense
scalar reward in [0,1]. The result is a graded training label to use in place of the thin whole
verdict / KEEP-DROP bit. It is grounded in Rubrics-as-Rewards (arXiv 2507.17746). The `is_whole`
leaf is what gets graded, not a criterion.

**STATE** — HEWN (functions + test). `python3 labs/rubric-forge/selftest.py` gives
`rubric-forge selftest: 1091 checks, 0 failures`, offline with no key.
`bash labs/situation-recorder/run_all.sh` still passes, with every chain verifying.

I mutation-checked the selftest. With a verdict-dependent weighting (`w = 1.05 − s`) it gives 364
failures, because monotonicity and verdict-blindness both break. Changing the exponent to p = 1 gives
21 failures (fixture rewards and hashes). So the checks can fail.

**RUNS** — over the 7 real FOLDs in `situations/transcripts/*.jsonl` (sorted by reward):

| transcript (sid) | n | whole | min | arith. mean | **reward** (uniform, offline) | reward (JEV-weighted, cached) |
|---|---:|---:|---:|---:|---:|---:|
| jev-fold-claimA (Great Wall in Japan) | 3 | 0.08 | 0.01 | 0.643 | **0.029** | 0.034 |
| jev-fold-claimB (gold is Ag) | 3 | 0.08 | 0.02 | 0.630 | **0.058** | 0.073 |
| sit-…-capture-path | 5 | 0.35 | 0.10 | 0.782 | **0.352** | 0.354 |
| sit-…-syzygy-p1-harvest | 5 | 0.55 | 0.30 | 0.822 | **0.663** | 0.615 |
| sit-…-hermit-harvest (0.45 weakest) | 5 | 0.70 | 0.45 | 0.816 | **0.751** | 0.732 |
| sit-…-tool-pin-harvest (0.55 weakest) | 4 | 0.70 | 0.55 | 0.865 | **0.814** | 0.823 |
| sit-…-syzygy-verifier-harvest | 5 | 0.72 | 0.55 | 0.886 | **0.841** | 0.827 |

What this shows:

- The rewards come out in a sensible order. The two false-fact folds sit near 0: a single failed
  conjunct dominates, where the arithmetic mean would have scored them about 0.64. The
  stated-limitation fold comes next, and then the harvest folds, ordered by their weakest leaf.
- Hermit's fold (0.45 weakest) scores 0.751. That is below tool-pin (0.814) and verifier (0.841),
  even though hermit and tool-pin have the **same** whole verdict (0.70). The whole verdict put them
  level. The rubric separates them, and this is exactly the grading signal the thin label threw away.
- `--calibrate` finds that the best-fit fixed p against the referees' whole verdicts is −1.5
  (SSE 0.038), against the shipped −1 (SSE 0.046). The referees read conjunctively, and p = −1 is in
  their neighborhood.

**SHORTCUT** — stated plainly:

1. **The weighting is one choice among several.** The offline default is **uniform**, which is RaR's
   equal-weight baseline. None of the existing folds carries a `weight` or `importance`, so the
   offline label is really "harmonic mean of the leaves", and the weighting only matters when a fold
   supplies weights or `--jev` is used.
2. **p = −1 is a stated fixed choice, not fitted.** The calibration's −1.5 comes from N = 7 folds.
   That is too few to adopt, so p is reported and not tuned.
3. **The JEV importance weights are noisy.** Two live passes differed by up to about 0.05 per leaf,
   and some are counter-intuitive. For example, "projection.ts re-exports …", which is the root-cause
   fix, scored only 0.21 essential. The cache (`jev_weights.json`) pins one pass so the labels
   reproduce, but pinning makes them reproducible, not correct.
4. The whole verdict is ignored when criteria exist. When the referee's holistic read disagrees
   with the leaves, the reward sides with the leaves and records the gap as `delta_vs_whole`, without
   reconciling it.
5. The fold's leaves are treated as flat, independent criteria. Nested folds (sub-leaves of a leaf)
   are not aggregated hierarchically.

**ASSUMES** — leaf verdicts are calibrated probabilities in [0,1] from one referee on one scale. The
leaves roughly cover the whole claim, so a missing criterion is not scored. Criteria are
conjunctive: the claim needs all of them. A disjunctive fold ("A or B suffices") would be
under-scored by p < 0.

**BETTER-WHEN** —
- folds carry RaR `importance` tags at creation, written by the referee who decomposed the claim;
  the cell already honors them;
- there is enough volume of live director folds with delayed `OUTCOME` labels to fit p (and
  per-category weights) against **outcomes**, not against whole verdicts. A cell fitted to whole
  verdicts only learns to imitate the thin label;
- JEV importance is averaged over k draws, or replaced by a pairwise "which criterion matters more"
  comparison, which is more stable than an absolute noul.

**NEXT** — have `corpus.py` emit `reward` (and `rubric_hash`) alongside each row in
`decompositions.jsonl` so the ML-IN-THE-LOOP router trains on the graded label. Add an `importance`
field to `Situation.fold()` leaves. Then try the pair with `skill-forge` (#5): a low reward whose
influence sits on one leaf is exactly the failure a reasoning card should distill.
