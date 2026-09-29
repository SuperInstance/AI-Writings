# text-normalize-quilt (EX4) — mark

*Fourth worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`):
skip the unicode tooling when the input is pure ASCII.*

- **WHAT** — A text normalizer (lowercase + strip + collapse whitespace) with **two product-identical
  routes** for the same request: a **cheap** route (pure-ASCII bytes: `translate`/`lower`/`split`, no
  `unicodedata`) and a **full** route (NFKC + casefold + unicode whitespace via stdlib `unicodedata`).
  The quilt **chooses cheap iff the input is pure ASCII**, else full. Every step is booked to an
  ActiveLog v1 run through the shared `labs/activeledger` emitter (cell.tick + route.hop +
  ledger.transaction, budget vector incl. `storage_bytes`).
- **STATE** — **HEWN.** `selftest.py`: **17 checks, 0 failures**, offline & deterministic. Products
  identical on all 128 ASCII code points (3 contexts) + 2000 seeded fuzz strings; chooser iff-ASCII;
  cheap cheaper on compute (wall_ms 5 vs 13), storage (prod 176 B vs 7168 B), mem, power; budgets
  well-formed; ticks+hops total == ledger.transaction; route.hops balance; chain tamper-evident;
  byte-identical re-runs.
- **RUNS** — `python3 textnorm_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **GOTCHA (caught by the exhaustive check)** — `str.split()` treats `0x1c–0x1f` as whitespace but
  `bytes.split()` does not; the cheap route maps them to space first, or the products would differ.
- **SHORTCUT** — Budgets are a deterministic cost model, not measured. Normalization spec is fixed
  (lower/strip/collapse), no punctuation or accent stripping.
- **ASSUMES** — Python 3.10+ stdlib; `labs/activeledger` importable by relative path.
- **BETTER-WHEN** — a real cost meter feeds the budgets; the `labs/examples/run_all` harness runs it
  beside EX1 and checks they share one ActiveLog; System-2 backtests it against alternatives.
- **SEED** — §13: an obvious use, a clever skip.
