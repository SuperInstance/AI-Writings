# csv-stats-quilt (EX8) — mark

*Worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`): single-pass split when there is no grouping or quoting.*

- **WHAT** — Summary stats (n/sum/min/max/mean to 4dp, half-even) of an integer CSV column. **Cheap**: one pass over `str.split(',')` with integer accumulators and an integer-only mean; **full**: `csv.DictReader` (quotes, CRLF), optional group-by, exact `Fraction` mean via `Decimal`. Two **product-identical routes** (cheap / full); the quilt **chooses cheap iff its precondition holds**.
  Every step is booked to ActiveLog v1 through the shared `labs/activeledger` emitter
  (cell.tick + route.hop + ledger.transaction, budget vector incl. `storage_bytes`).
- **STATE** — **HEWN.** `selftest.py`: **17 checks, 0 failures**, offline & deterministic. Stats blocks identical on 2000 seeded random CSVs and pinned means (1.5000, 0.3333, -0.3333, half-even tie); chooser iff ungrouped+unquoted+LF; cheap refuses grouped/quoted/CRLF input; cheap cheaper on wall_ms/prod/mem/power; budgets well-formed; chain tamper-evident; byte-identical re-runs.
- **RUNS** — `python3 csvstats_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **GOTCHA** — Signed zero mean: `-1/30000`-style means round to `-0.0000` in `Decimal`, so the cheap route derives the sign from the sum, not the rounded magnitude.
- **SHORTCUT** — Budgets are a deterministic cost model, not measured.
- **ASSUMES** — Python 3.10+ stdlib; `labs/activeledger` importable by relative path.
- **SEED** — §13: an obvious use, a clever skip.
