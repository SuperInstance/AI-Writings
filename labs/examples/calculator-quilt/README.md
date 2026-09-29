# calculator-quilt (EX1) — mark

*First worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`):
the anti-GAN-of-programming thesis on the most obvious possible use-case.*

- **WHAT** — A money calculator with **two product-identical routes** for the same equation: a
  **simple** route (integer-cents fixed-point, no interest tooling) and a **full** route
  (`decimal.Decimal` + compounding). The quilt **chooses the simple route for every equation that
  doesn't need interest**, and only escalates to the full route for compounding. Both routes reach the
  identical cent on the shared cases — *novelty in process, identity in product*. Every step is booked
  to an ActiveLog v1 run with a budget vector (compute + storage), so System-2 can backtest it.
- **STATE** — **HEWN.** `selftest.py`: **12 checks, 0 failures**, fully offline & deterministic.
  Proves product-identity across routes, the chooser, the simple route cheaper on **both** compute
  (wall_ms 5 vs 16) **and** storage (prod 256 B vs 4096 B), well-formed budget vectors, route-total
  reconciliation, route.hop double-entry balance after unit translation, dollars↔cents round-trip, a
  tamper-evident chain, and byte-identical re-runs.
- **RUNS** — `python3 calc_quilt.py` (demo over the workload) · `python3 selftest.py` (the proof).
- **SHORTCUT** — (1) The `ActiveLog` emitter here is a **self-contained stand-in for `labs/activeledger`
  (B1)**; the record shape matches the frozen schema, so swap the import when B1 lands. (2) Budgets are a
  **deterministic cost model**, not measured wall-clock — real numbers arrive when cells run for real.
  (3) `pct` uses floor division and the demo values divide exactly, so the rounding policy is not
  stress-tested; add a ROUND_HALF_EVEN reconciliation when pct goes general. (4) One equation grammar
  (structured dicts), not a parser.
- **ASSUMES** — Python 3.10+ stdlib (`decimal`, `json`) only. The fnv1a-64 canonical-JSON hash idiom
  matches `labs/situation-recorder` + MicroMoth-quilt.
- **BETTER-WHEN** — it imports `labs/activeledger` instead of the local emitter; the budget vector is
  fed by a real cost meter; the `labs/examples/run_all` interop harness runs it beside its siblings and
  checks they all book to one shared ActiveLog; System-2 (`system2-backtest`, B7) replays its runs to
  price an alternative calculator network.
- **SEED** — §13 example-collection principle: the clearer the use-case, the better the example; chase
  unique *uses* as much as unique *math*.
- **NEXT** — siblings EX2–EX5 (convert / datetime / text-normalize / image-thumb), each an obvious use
  with a clever skip; then the interop harness; then a tutorial.
