# Using the labs — a run-through of the whole loop

## 1. In one breath

Three commands, run from the repo root, exercise the whole shelf: one rebuilds the corpus of recorded manager↔crew missions, one runs the five example quilts, one prices cheap-vs-full routes; this article shows the real output and what each line proves.

## 2. Why it exists

`labs/docs/README.md` explains what each lab is for. This article is for the moment after that, when you want to run the thing and know what a good result looks like. It also says what the output does *not* prove, because two of the checks are weaker than their names suggest.

## 3. The mental model

Read the three commands as three separate checks on two separate strands (see the graph in [`README.md`](README.md) §3):

- `bash labs/situation-recorder/run_all.sh` — **strand A**, the transcripts. It rewrites `situations/corpus/` from `situations/transcripts/` and refuses to continue if any hash chain fails to verify.
- `python3 labs/examples/run_all.py` — **strand B**, the quilts. It runs each quilt's own selftest, then reports which ones sit on the shared `labs/activeledger`.
- `python3 labs/system2-backtest/backtest.py` — **strand B, downstream**. It replays route pairs from those quilts and decides whether the cheap route is safe to prefer.

Two more Python labs in the middle of strand B and one in strand A have no command in the list above but are part of the loop: `unit-translation-audit` (audits every hop the quilts book), `rubric-forge` (turns transcript `FOLD` records into rewards) and `activeledger` (the emitter everything in B imports). §4 runs them briefly after the three main commands.

Everything below was run on 2026-09-30 in a clean checkout with Python 3 stdlib only; no network keys were needed.

## 4. Walkthrough

### Step 1 — capture and corpus: `bash labs/situation-recorder/run_all.sh`

```
$ bash labs/situation-recorder/run_all.sh
== recorder self-test (chain + tamper-evidence) ==
  ok
== backfill corpus from the dispatch-ledger ==
backfilled 147 situations (588 records) → /home/user/ai-writings/situations/transcripts/backfill/ledger.jsonl
all chains verified ✓  provenance stamped: 'backfill-from-ledger (reconstructed)'
== build model-ready tables (verifies every chain) ==
all 154 chains verified ✓
situations: 154   records: 626
relation mix: DRAW=3, FOLD=7, KEEP=5, MARK=153, OUTCOME=152, ROUTE=152, TASK=154
decompositions (FOLD): 7
  gap (folded_min − whole): min=-0.250 mean=-0.171 max=-0.060  (how much a scalar hid)
routes: 152   outcome mix: ABANDONED=1, BLOCKED=2, DONE=122, FOLDED=1, OPEN=18, P1-byte-exact-verified=1, PARTIAL=1, PENDING=2, both-cells-independently-verified-shipped=1, capture-path-validated=1, cell-shipped-verified=1, fix-structurally-verified-awaiting-CI=1
judgments: 5 (kept=5 dropped=0)
wrote tables to /home/user/ai-writings/situations/corpus/
== base rate a learned cell must beat ==
weakest-leaf localization — transparent lexical baseline
  folds evaluated: 7
  baseline top-1 accuracy: 0.14
  random base rate:        0.25
  lift over base rate:     -0.10
  ...
FINDING (Law 7): the lexical baseline localizes stated-limitation folds but
cannot reach factual-error folds (0/5) — no lexical tell exists for 'gold is Ag'.
...
== done: situations/corpus/{decompositions,routes,judgments}.jsonl ==
```

(The per-fold lines are trimmed with `...`; the full run prints all seven.) What it proves, line by line:

- `recorder self-test ... ok` — the writer builds a demo transcript, verifies it, and confirms a tamper is caught.
- `backfilled 147 situations (588 records)` — old dispatch-ledger rows are converted into the same record format so the corpus is not just seven hand-made transcripts. They are stamped as reconstructed, and they are the reason `ROUTE`/`OUTCOME`/`MARK` counts are ~150 while `FOLD` is 7.
- `all 154 chains verified` — every line's fnv1a-64 hash re-derives from its predecessor. If someone edited, dropped or reordered a record, `corpus.py` would stop here.
- `gap ... mean=-0.171` — in the 7 real folds, the weakest part scored on average 0.17 below the whole-claim verdict. That is the functional point of a `FOLD`: a single score hid a weak part.
- `lift over base rate: -0.10` — a lexical guesser picks the weakest leaf right 1 time in 7 (0.14), *worse* than the 0.25 random rate. Use this as the number a learned decomposer has to beat. It is not a result about any model, and N=7 is too small to gate anything; the script says the same.

Re-running left `git status` clean, so the corpus build is deterministic against the committed tables.

### Step 2 — the example quilts: `python3 labs/examples/run_all.py`

```
$ python3 labs/examples/run_all.py
== example-collection interop harness ==
  calculator-quilt selftest: 12 checks, 0 failures
  convert-quilt selftest: 21 checks, 0 failures
  datetime-quilt selftest: 14 checks, 0 failures
  image-thumb-quilt selftest: 18 checks, 0 failures
  text-normalize-quilt selftest: 17 checks, 0 failures

selftests: 5/5 green
on the shared labs/activeledger: 5/5  (all one ledger)
```

Each quilt has two routes to the same product (e.g. calculator: integer-cents fixed point vs `Decimal`; text-normalize: skip unicode handling for pure ASCII) and a chooser that picks the cheap one when it applies. The selftests prove product identity across routes, well-formed budget vectors, reconciling route totals, a tamper-evident chain and byte-identical re-runs. 82 checks in total (12+21+14+18+17).

**Read the last line carefully.** `run_all.py` decides "on the shared ledger" by checking whether any `.py` file in the example directory contains the text `activeledger`. `calculator-quilt/calc_quilt.py` contains that text in a comment about its inline stand-in emitter, so it counts. Step 4 shows a concrete consequence.

### Step 3 — price the routes: `python3 labs/system2-backtest/backtest.py`

```
$ python3 labs/system2-backtest/backtest.py
== calculator  (simple vs full): certified 5, refused 0, inapplicable 1
   simple      wall_ms=25   usd=0.0   tokens=0   storage_bytes=6400
   full        wall_ms=80   usd=0.0   tokens=0   storage_bytes=102400
   verdict: dominates-faster-cheaper  axes={'good': 'tie', 'fast': 'simple', 'cheap': 'simple'}  cheap={'compute': 'tie', 'storage': 'simple'}
   preferred-when: {'good': 'tie', 'fast': 'simple', 'cheap': 'simple'}
== convert  (cheap vs full): certified 3, refused 0, inapplicable 5
   cheap       wall_ms=9    usd=0.0   tokens=0   storage_bytes=1200
   full        wall_ms=39   usd=0.0   tokens=0   storage_bytes=46080
   verdict: dominates-faster-cheaper  ...
== datetime  (utc vs full): certified 5, refused 0, inapplicable 3
   utc         wall_ms=25   usd=0.0   tokens=0   storage_bytes=3440
   full        wall_ms=95   usd=0.0   tokens=0   storage_bytes=179200
   verdict: dominates-faster-cheaper  ...
== text-normalize  (cheap vs full): certified 7, refused 0, inapplicable 2
   cheap       wall_ms=35   usd=0.0   tokens=0   storage_bytes=4816
   full        wall_ms=91   usd=0.0   tokens=0   storage_bytes=250880
   verdict: dominates-faster-cheaper  ...
== image-thumb  (passthrough vs resample): certified 3, refused 0, inapplicable 2
   passthrough wall_ms=15   usd=0.0   tokens=0   storage_bytes=1584
   resample    wall_ms=72   usd=0.0   tokens=0   storage_bytes=122880
   verdict: dominates-faster-cheaper  ...
```

(Verdict lines for the last four workloads are shortened to `...`; each was the same class with the cheap route winning `fast` and `cheap`, `good` tied, compute cheapness tied.)

How to read one block, using calculator: the workload has 6 cases. On 5, both routes produced the identical product, so they are **certified** and their budgets are summed and compared. On 1 (a compound-interest case) the simple route cannot run, so it is **inapplicable**: a coverage fact, not a comparison. `refused 0` means no case had differing products. The verdict `dominates-faster-cheaper` says: where the simple route applies it is faster (25 vs 80 wall_ms) and cheaper, and loses on nothing, so keep the full route only as the fallback for the inapplicable case. `usd` and `tokens` are 0 on both sides (local compute), so the entire "cheap" win comes from `storage_bytes`, and `wall_ms` and bytes come from each quilt's deterministic cost model, not a stopwatch.

### Step 4 — the two audits that sit between them

These are not in the requested three but complete the strand-B loop.

```
$ python3 labs/unit-translation-audit/audit.py | head -10
calc/0:add             EXACT       USD->USD-cents 12.34 USD -> 1234 USD-cents  rate=100.0
calc/0:add             EXACT       USD-cents->USD 1800.0 USD-cents -> 18 USD  rate=0.01
calc/1:sub             EXACT       USD->USD-cents 100.0 USD -> 10000 USD-cents  rate=100.0
calc/1:sub             LOSSY       USD-cents->USD 9999.0 USD-cents -> 100 USD  rate=0.01
    why: debit is an integer but credit*rate = 99.99 has a fractional part; sub-unit remainder 0.01 dropped (integer-quantized debit)
calc/2:scale           EXACT       USD->USD-cents 9.99 USD -> 999 USD-cents  rate=100.0
...
SUMMARY {'audit_v': 1, 'runs': 14, 'n_hops': 25, 'counts': {'EXACT': 16, 'WITHIN_TOL': 4, 'LOSSY': 5}, 'audit_digest': '0xddf7f4f5c220409c'}
```

(Piping through `head` truncates the output and Python prints a `BrokenPipeError` afterwards; run it without `head` for the clean SUMMARY line.) This proves something Step 2 did not: five of the calculator's cents→USD hops are booked with an integer debit (9999¢ becomes `100` USD, not `99.99`). The calculator's *answer* is still correct; its *bookkeeping hop* is lossy. This is the concrete consequence of the stand-in emitter noted in Step 2.

`rubric-forge` reads the transcripts from Step 1 and gives a reward per fold:

```
$ python3 labs/rubric-forge/forge.py
sid                                       n  whole    min   mean  REWARD weights
jev-fold-claimA                           3   0.08   0.01  0.643   0.029 uniform
jev-fold-claimB                           3   0.08   0.02  0.630   0.058 uniform
sit-2026-09-29-capture-path               5   0.35   0.10  0.782   0.352 uniform
sit-2026-09-29-syzygy-p1-harvest          5   0.55   0.30  0.822   0.663 uniform
sit-2026-09-29-hermit-harvest             5   0.70   0.45  0.816   0.751 uniform
sit-2026-09-29-tool-pin-harvest           4   0.70   0.55  0.865   0.814 uniform
sit-2026-09-29-syzygy-verifier-harvest    5   0.72   0.55  0.886   0.841 uniform
```

The reward is a weighted harmonic mean of the leaf scores, so one failed leaf drags it down (`claimA`: leaves mean 0.643, reward 0.029) where an average would hide it. Weights are `uniform` offline. The reward is not consumed by anything else in `labs/` yet.

### Step 5 — the receipts

```
$ for d in activeledger rubric-forge unit-translation-audit system2-backtest; do (cd labs/$d; python3 selftest.py | tail -1); done
activeledger selftest: 28 checks, 0 failures
rubric-forge selftest: 1091 checks, 0 failures
unit-translation-audit selftest: 34 checks, 0 failures
system2-backtest selftest: 38 checks, 0 failures
```

Also confirmed: `python3 labs/situation-recorder/recorder.py --verify situations/transcripts/sit-2026-09-29-capture-path.jsonl` prints `VERIFY OK  — ok: 8 records, chain intact`, and `python3 -c "import route_sim as R; print(R.run(True)['transcript'])"` in `labs/activeledger` prints `Turn on the lights.`

## 5. The contract

- **Inputs.** Repo root as working directory, Python 3 stdlib. Transcripts under `situations/transcripts/`. No network keys for anything in this article.
- **Outputs.** Step 1 rewrites `situations/corpus/{decompositions,routes,judgments}.jsonl` and `situations/transcripts/backfill/ledger.jsonl`; Steps 2–5 write nothing to disk.
- **Invariants.** Step 1 stops on any broken chain. All backtest verdicts and audit digests are deterministic: run them twice and diff.
- **Receipt.** Green means: `all 154 chains verified`; `selftests: 5/5 green`; every backtest block has `refused 0`; the four selftest lines above show `0 failures`. Counts confirmed in this session: 154 chains, 5/5 quilts (82 checks), 28 + 1091 + 34 + 38 lab checks.

## 6. Failure modes / scars

- **Chain failure in Step 1.** `corpus.py` aborts if a transcript was hand-edited. Fix the source (regenerate or restore the file); do not patch the hash. Note that `run_all.sh` also *overwrites* the backfill file and corpus tables, so expect a diff if the ledger has changed.
- **Trusting "all one ledger".** See Step 2/4. To fold `calculator-quilt` onto the shared emitter, import `labs/activeledger` in `calc_quilt.py`; per the audit README, the shared `emit` would then reject the five unbalanced hops, so expect that quilt's selftest to need attention.
- **Backtest `refused`.** If a case shows `refused`, the two routes returned different products. Fix the route; the gate is not something to loosen. A coarse `ledger.transaction` product field (image-thumb records the thumbnail *size*, not pixels) makes the gate coarse too.
- **Reading simulated costs as measurements.** `wall_ms` and `storage_bytes` come from deterministic cost models, and every verdict carries an as-of window and a stationarity caveat. Re-backtest after any repricing.
- **Small-N base rate.** The lift number in Step 1 is from 7 folds.
- **`BrokenPipeError` from `audit.py | head`.** Harmless; caused by `head` closing the pipe.

## 7. How it composes

- The corpus tables from Step 1 are the input a decomposer/router model would train on; the base-rate script gives the bar it must clear.
- The `route.hop` records the quilts book are what `unit-translation-audit` and `system2-backtest` both import; adding a sixth quilt that emits through `labs/activeledger` makes it auditable and backtestable with no changes to either, provided you add its workload to the backtest fixtures.
- `rubric-forge` rewards attach to `FOLD` records; a future B4 (route preference) is described as consuming them together with `preferred-when` from Step 3, but that code is not in this repo.
- To record your own mission, use `labs/situation-recorder/recorder.py` (`Situation.task/route/draft/fold/mark`, then `.write(...)` into `situations/transcripts/`); the next `run_all.sh` picks it up.

## 8. Where to look next

- [`README.md`](README.md) in this directory: the index and dependency graph.
- `labs/situation-recorder/README.md`: record types, the `Situation` API, and local dice via `draw_local.py`.
- `labs/system2-backtest/README.md` and `labs/unit-translation-audit/README.md`: full contracts and scars for the two strand-B gates.
