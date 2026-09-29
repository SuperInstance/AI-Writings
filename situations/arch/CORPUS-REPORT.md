# Corpus report — the SuperInstance modeled as a thing (first real numbers)

*A measurement-mark (2026-09-29). Regenerate any time: `python3 labs/situation-recorder/corpus.py`
then `python3 labs/situation-recorder/baseline_decompose.py`. This is the descriptive first pass —
what the saved manager↔crew system actually looks like as data — not a trained model. Honest and
early on purpose.*

## What's in the corpus now

| source | situations | how captured |
|--------|-----------:|--------------|
| live transcripts | 3 | recorded end-to-end (capture-path + 2 real JEV folds) |
| ledger backfill | 123 | **reconstructed** from `dispatch-ledger.csv` (honest silver) |
| **total** | **126** | 504 relation-records, **all 126 chains verified** |

Relation mix: `TASK=126 ROUTE=124 MARK=125 OUTCOME=124 FOLD=3 DRAW=1 KEEP=1`. The backfill supplies
the `ROUTE→OUTCOME` spine at volume; the live transcripts supply the rare, expensive verbs (`FOLD`,
`DRAW`, `KEEP`) that only real capture produces. The gap between those two counts *is* the argument
for the capture discipline: we have thousands of routes on record and almost no folds — so folds are
the gold to capture going forward.

## The fleet as a routing process (ROUTE → OUTCOME, n=124)

| outcome | count | share |
|---------|------:|------:|
| DONE | 107 | 86% |
| OPEN | 9 | 7% |
| BLOCKED | 2 | 2% |
| PENDING | 2 | 2% |
| PARTIAL | 1 | 1% |
| ABANDONED | 1 | 1% |
| FOLDED | 1 | 1% |
| capture-path-validated | 1 | 1% |

86% of dispatches reached DONE. The honest scars (ABANDONED, FOLDED, PARTIAL) are booked, not hidden
— which is what makes this clean training data for a learned dispatch router: the negatives are real
negatives. This table is the first quantitative self-portrait of the fleet's operation.

## Decomposition (FOLD, n=3)

The gap — `folded_min − whole_verdict`, i.e. how much a single scalar verdict hid — ran
min −0.250, mean −0.127, max −0.060. Small for plain factual conjunctions (JEV already propagates a
false conjunct into the whole, so the fold's value there is *localization*, not detection — matches
`JEV-USAGE-LOG.md`); larger for the compound tool-claim, where the whole (0.35) smoothed over a leaf
at 0.10. Three folds is a scaffold, not a finding — but the *shape* is now measurable.

## The first ML step: base rate before any learned cell

Task: given only the leaf **texts** (not the oracle's verdicts), predict the weakest leaf. A
transparent lexical baseline (limitation/negation/absoluteness cues, word-boundary matched):

| metric | value |
|--------|------:|
| folds evaluated | 3 |
| baseline top-1 accuracy | 0.33 |
| random base rate | 0.29 |
| lift over base rate | **+0.04 (noise)** |
| factual-error folds | **0 / 2** |
| stated-limitation folds | 1 / 1 |

**Finding (Law 7, measured):** the lexicon localizes a *stated limitation* ("simulator has none")
but cannot reach a *factual error* ("the chemical symbol for gold is Ag") — there is no lexical tell
for factual falsehood. An earlier version even scored a *spurious* hit (substring "wall" ⊃ "all"),
the exact hazard of lexical hacking; word boundaries removed it. So a learned cell must **buy
independent reach** (JEV, or a symbolic checker for counting/spelling — JEV's own blind spot), not
enlarge the lexicon. This is why the fleet pays for a reader at all.

**Gate (`ML-IN-THE-LOOP.md`):** this is **not** a CI gate yet. N=3 is a scaffold, and a lexicon
provably can't reach factual folds. `labs/ci-brain` is earned only when live director folds give
volume **and** a model beats this base rate by a margin — then it's asserted from data, not hope.

## What this establishes

The saved system is now queryable and model-ready: `situations/corpus/{decompositions,routes,
judgments}.jsonl` are the three tables, regenerable from the transcripts, with every chain verified.
"Modeling the SuperInstance as a thing" has a concrete first form — a verified relational corpus with
an honest base rate — and a clear next move: capture folds live (the 05:18 director wave does this),
grow the decomposition table, and only then let a learned cell try to beat 0.29.
