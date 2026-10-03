# match-quilt (EX6) — mark

*Worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`): literal fast-path when the pattern has no regex metacharacters.*

- **WHAT** — A substring/regex matcher returning all non-overlapping match spans (`start-end,...`). **Cheap**: a `str.find` loop; **full**: compile + `re.finditer`. Two **product-identical routes** (cheap / full); the quilt **chooses cheap iff its precondition holds**.
  Every step is booked to ActiveLog v1 through the shared `labs/activeledger` emitter
  (cell.tick + route.hop + ledger.transaction, budget vector incl. `storage_bytes`).
- **STATE** — **HEWN.** `selftest.py`: **17 checks, 0 failures**, offline & deterministic. Span lists identical on 3000 seeded literal pattern/text pairs (overlaps, repeats, misses, unicode); chooser iff literal; cheap cheaper on wall_ms/prod/mem/power; budgets well-formed; ticks+hops == ledger.transaction; hops balance; chain tamper-evident; byte-identical re-runs.
- **RUNS** — `python3 match_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **GOTCHA** — Non-overlap: `re.finditer` resumes at the match END, so the cheap loop must advance by `len(pattern)`, not 1. The empty pattern is excluded (re matches at every position).
- **SHORTCUT** — Budgets are a deterministic cost model, not measured.
- **ASSUMES** — Python 3.10+ stdlib; `labs/activeledger` importable by relative path.
- **SEED** — §13: an obvious use, a clever skip.
