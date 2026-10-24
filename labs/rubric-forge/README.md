# rubric-forge

Turns a JEV `FOLD` (claim + per-leaf verdicts) into a **weighted rubric** `{criterion, weight, score,
influence}` and one **dense scalar reward** in [0,1], so the corpus gets a graded training label
instead of a thin whole verdict or a KEEP/DROP bit. Zero dependencies (Python stdlib).

```
python3 selftest.py            # rubric-forge selftest: 1091 checks, 0 failures (offline)
python3 forge.py               # table over situations/transcripts/*.jsonl
python3 forge.py --json        # one rubric record per FOLD (JSONL)
python3 forge.py --jev         # JEV importance weights (served from jev_weights.json)
python3 forge.py --calibrate   # which fixed p best reproduces the referees' whole verdicts
```

## Why (Rubrics-as-Rewards)

[Rubrics-as-Rewards](https://arxiv.org/abs/2507.17746) shows that an explicit, weighted checklist of
criteria aggregated into a reward trains better than a single holistic score, even on verifiable
tasks. Our `FOLD` records already hold the checklist: JEV's leaves **are** the criteria. What was
missing is the weighting and the aggregation. That is this cell.

## The scheme (fixed; never tuned per instance)

- **The whole-claim leaf (`is_whole`) is graded, not a criterion.** It is carried through as
  `whole_verdict`, the thin label to compare against. It becomes the reward only when a fold has no
  criteria.
- **Weights don't look at verdicts.** The first of these that applies is used: the leaf's `weight`,
  then its RaR `importance` (essential 1.0 / important 0.7 / optional 0.3), then with `--jev` a JEV
  noul on *"if this criterion failed, would the compound claim fail?"* (asked from the claim texts
  only, mapped to `0.25 + 0.75·noul`), and otherwise **uniform**, which is the offline default.
  Because no weight reads a score, the grader can't gain reward by shifting weight onto the leaves
  that scored well, and monotonicity holds by construction.
- **Aggregate with the weighted power mean at p = −1 (weighted harmonic).** At p → −∞ you get the
  recorder's `folded_min` (a conjunction is capped by its weakest conjunct). At p = 1 you get RaR's
  weighted average. p = −1 sits between them: the reward stays dense, but one failed criterion
  dominates. For example 0.01 among 0.98s gives 0.03, where the arithmetic mean would give 0.64.
- **`influence`** is each criterion's share of ∂R/∂sᵢ (∝ wᵢ/sᵢ² at p = −1), which tells you how far
  raising that leaf would move the reward. It is only a diagnostic and never feeds back into the
  weights.

Every record carries `rubric_hash` (fnv1a-64 over canonical JSON, the recorder's idiom), so a label is
re-derivable byte-for-byte.

## Files

| file | what |
|---|---|
| `forge.py` | `forge(fold) -> {claim, rubric, reward, whole_verdict, folded_min, delta_vs_whole, scheme, rubric_hash}` |
| `selftest.py` | bounded, monotone (every leaf swept), degenerate = whole, whole-blind, verdict-blind weights, fixture reproduction, JEV cache offline, corpus chains intact |
| `fixture.json` | the 7 real FOLD bodies plus 2 synthetic ones, with expected reward and hash (`selftest.py --regen` only after a deliberate scheme change) |
| `jev_weights.json` | cached JEV importance nouls, keyed by the hash of (claim, criterion). Makes `--jev` reproducible offline; live calls only fill cache misses |

Mark: [`../../docs/marks/0001-rubric-forge.md`](../../docs/marks/0001-rubric-forge.md).
