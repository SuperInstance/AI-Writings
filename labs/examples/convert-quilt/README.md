# convert-quilt (EX2) — mark

*Second worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`): an
obvious use (unit conversion) with a free skip (identity).*

- **WHAT** — A unit converter with **two product-identical routes**: a **cheap** identity/no-op route
  (source unit == target unit → value returned untouched, no table loaded) and a **full** route (small
  deterministic table: length m/cm/km/in/ft, mass g/kg/lb, temp C/F/K, via a base unit). The quilt
  **chooses cheap iff src == target**, else full. Both reach the identical product on the shared cases.
  Every step is booked to an ActiveLog v1 run through `labs/activeledger` (imported, not re-emitted):
  `cell.tick` + balanced `route.hop` (unit-translation price) + `ledger.transaction`, each with a
  budget vector incl. `storage_bytes {train,prod}`.
- **STATE** — **HEWN.** `selftest.py`: **21 checks, 0 failures**, offline & deterministic. Cheap vs full
  on the same identity request: wall_ms **3 vs 13**, prod bytes **80 vs 3072**, train bytes **320 vs
  12288** — cheaper on compute *and* storage.
- **RUNS** — `python3 convert_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **SHORTCUT** — (1) Budgets are a deterministic cost model, not measured. (2) Hop rate is the effective
  ratio dst/src, so a non-identity hop with a zero source amount is degenerate (temperature offsets);
  the workload avoids 0. (3) Products are fixed 6-dp strings; hop amounts are floats within the
  `1e-6` balance tolerance. (4) Tiny unit table, no parser.
- **ASSUMES** — Python 3.10+ stdlib (`fractions`); `labs/activeledger` importable via the relative path.
- **BETTER-WHEN** — a real cost meter feeds the budgets; `labs/examples/run_all` books EX1–EX5 to one
  shared ActiveLog; System-2 (B7) backtests this against an always-full alternative; the cheap route
  rides quilt memoization / jev-quilt routing rather than a bespoke chooser.
- **NEXT** — EX3–EX5 (datetime / text-normalize / image-thumb); interop harness; tutorial.
