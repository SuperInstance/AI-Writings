# currency-round-quilt (EX7) — mark

*Worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`): integer-cents route when there is no fx rate.*

- **WHAT** — Round a money amount to cents, banker's (half-even), optionally via an fx rate. **Cheap**: digit-string → integer cents, no `Decimal` (only when fx is 1); **full**: exact `Decimal` multiply + quantize. Two **product-identical routes** (cheap / full); the quilt **chooses cheap iff its precondition holds**.
  Every step is booked to ActiveLog v1 through the shared `labs/activeledger` emitter
  (cell.tick + route.hop + ledger.transaction, budget vector incl. `storage_bytes`).
- **STATE** — **HEWN.** `selftest.py`: **17 checks, 0 failures**, offline & deterministic. Cents strings identical on 5000 seeded decimal strings (signs, exact ties, long tails) and pinned tie cases (0.125→0.12, 0.135→0.14, 2.675→2.68, -0.001→-0.00); chooser iff no-fx plain decimal; cheap cheaper on wall_ms/prod/mem/power; budgets well-formed; chain tamper-evident; byte-identical re-runs.
- **RUNS** — `python3 currency_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **GOTCHA** — Half-even needs the WHOLE dropped tail: `0.1250001` rounds up although its third digit is 5 — the cheap route checks for any nonzero digit after the 5. Negative values keep their sign even when rounding to zero (`-0.00`), matching `Decimal`.
- **SHORTCUT** — Budgets are a deterministic cost model, not measured.
- **ASSUMES** — Python 3.10+ stdlib; `labs/activeledger` importable by relative path.
- **SEED** — §13: an obvious use, a clever skip.
