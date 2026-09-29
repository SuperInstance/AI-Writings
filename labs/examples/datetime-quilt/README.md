# datetime-quilt (EX3) — mark

*Third worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`):
skip the whole timezone/DST stack when every input is UTC.*

- **WHAT** — A datetime calculator (add duration / diff) with **two product-identical routes**: a
  **utc** route (pure integer epoch-seconds arithmetic via days-from-civil; no `datetime`, no
  `zoneinfo`, no tz database) and a **full** route (`datetime` + `zoneinfo`, DST-aware). The quilt
  **chooses utc iff every input is UTC**, else full. Both reach the identical instant on the shared
  all-UTC cases. Every step is booked to an ActiveLog v1 run through the shared `labs/activeledger`
  emitter (imported, not re-emitted): `cell.tick` + balanced `route.hop` + `ledger.transaction`,
  each with a budget vector incl. `storage_bytes {train,prod}`.
- **STATE** — **HEWN.** `selftest.py`: **14 checks, 0 failures**, offline and deterministic (fixed
  inputs, no `now()`). utc vs full per run: wall_ms **5 vs 19**, prod storage **176 B vs 7168 B**,
  train storage **512 B vs 28672 B**. Also proves: chooser correctness (mixed UTC/non-UTC → full),
  utc route refuses non-UTC, full route handles NY spring-forward/fall-back, budget vectors well-formed,
  route total == sum of records, hops balance, chain tamper-evident, byte-identical re-runs.
- **RUNS** — `python3 datetime_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **SHORTCUT** — (1) Budgets are a deterministic cost model, not measured. (2) Durations are exact
  seconds; calendar-aware "+1 day/month" (where DST changes the answer) is out of scope. (3) Ambiguous
  wall times (fall-back overlap) take zoneinfo's default `fold=0`. (4) utc route assumes valid ISO
  `YYYY-MM-DDTHH:MM:SS`; no validation/offsets/fractions.
- **ASSUMES** — Python 3.9+ stdlib (`zoneinfo` needs a system tz db for the full route only).
- **BETTER-WHEN** — costs come from a real meter; System-2 (B7) backtests this against an
  alternative chooser; the interop harness runs it beside EX1/EX2.
- **SEED** — §13: chase unique *uses* — the clever skip is "don't load the tz db".
- **NEXT** — EX2/EX4/EX5 siblings; calendar-aware durations as a third route.
