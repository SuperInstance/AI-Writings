# synoptic-view (B5) — mark

*The read-only observability / projection layer over the finished ActiveLog tensor
(`situations/arch/ACTIVELEDGER-CELL-GRAPH.md` row B5). Pure projection: nothing here emits into a
recorded run, and every chain is verified with its owner's own `verify`.*

- **WHAT** — `synoptic_view.py`:
  1. **Pivot / synopsis.** Each budgeted record (`cell.tick`, `route.hop`) becomes one fact per atomic
     budget component (`wall_ms, usd, power_w, mem_mb, storage_train, storage_prod, tokens:<api>`).
     `pivot(facts, rows, cols)` projects those facts onto any two of 13 dimensions:
     `log dev type cell kind route path run reqs tick component axis api`. A hop's `cell` is
     `src->dst`, and `axis` is the iron-triangle corner: `fast` = wall_ms, `cheap-compute` =
     usd/power/mem/tokens, `cheap-storage` = storage bytes. `good` is shown but always empty, because
     standing is not in the ledger. Each pivot cell holds a vector of components summed exactly as
     `Fraction`s, so values in different units are never added together. `synopsis(facts, by)` gives
     per-cell `wall_ms / tokens / usd / storage_bytes` totals.
     `reconcile()` raises `ReconcileError` unless the projection sums back to the source along six
     separate paths:
     - **R0** the owner's chain verify passes;
     - **R1** the grand total equals an `activeledger.add_budget` fold over every record;
     - **R1b** each record appears exactly once;
     - **R2** the cells, the row margins and the column margins all sum to the grand total;
     - **R3** each route equals `activeledger.route_total`;
     - **R4** each `ledger.transaction`'s declared `total_budget` matches what its emitter computed, and
       each run's facts equal that run's segment;
     - **R5** the `otel_export` span projection gives the same per-kind wall_ms/usd.
  2. **Tick-scrubber.** `Scrubber(records)` refuses an unverified chain. `state_at(t)` refolds
     `records[:t]` from genesis each time, so a rewind cannot drift. The state holds the chain head, the
     type counts, the total, per-route and open budgets, the last body of each cell, and the settled
     transactions. `step / back / seek` move a cursor. `fork(t, branch)` returns a new `Fork`: its first
     `t` records are byte-identical deep copies, and new records are written as dev
     `<run>#<branch>`, so their `(dev,seq)` keys cannot collide with the original's. New records go
     through the owner's own emitter, so the same validation and chain rule apply. A fork can itself be
     forked (`#a#b`).
  `runs/*.jsonl` holds the recorded corpus: route_sim filtered and nofilter (activeledger), the six
  activeledger example quilts on one shared chain (312 records, each example writing as its own
  `dev`), and calculator-quilt on its own fnv1a-64 `hash` chain (36 records).
- **STATE** — **HEWN.** `python3 selftest.py` → **`synoptic-view selftest: 144 checks, 0 failures`**
  (offline, deterministic, ~11 s).
- **RUNS** — `python3 selftest.py` · `python3 synoptic_view.py --rows cell --cols component` ·
  `python3 synoptic_view.py --rows route --cols axis --measure wall_ms` · `--record` re-records `runs/`.
- **SHORTCUT** — (1) **No upstream `quilt-view` is importable in this checkout.** The projection is
  built fresh over `labs/activeledger`, and the OTel side reuses `activeledger/otel_export.py` rather
  than extending a viewer. (2) There is no UI: the output is Markdown tables plus Python state dicts. (3) The
  example dimensions `pattern` and `env` do not exist in any recorded record, so `pivot` refuses them
  instead of inventing them. (4) To book the six examples on one shared chain, `ActiveLog.dev` is set
  per example before its batch runs. `verify_chain` does not check `dev`, and `(dev,seq)` stays unique.
  (5) Budgets come from the producers' deterministic cost models, not from measurement.
- **FINDING (upstream, not a projection bug)** — convert-quilt and image-thumb-quilt reuse plain route
  ids (`cheap/full`, `passthrough/resample`). Their `total_budget` is `route_total(prefix, route)`, so on
  a shared ledger 9 transactions declare a total that includes earlier runs (for example, convert seq 7
  declares 6 ms where its own run took 3 ms). The other examples hash their inputs into the route id and
  stay exact. R4 asserts each emitter's own semantics, and `reconcile()["findings"]` lists the 9.
- **ASSUMES** — Python 3.10+ stdlib only. Imports `labs/activeledger` (B1) and
  `labs/examples/*` unmodified.
- **BETTER-WHEN** — a real `quilt-view` renders these pivots; the route-id reuse above is fixed
  upstream; `good` is joined from B4's OrgBook standing; forks are fed into B7 as what-if replays.
