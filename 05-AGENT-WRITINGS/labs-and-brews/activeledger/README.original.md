# activeledger (B1) — mark

*Thin adapter, not a new format. ActiveLog v1 envelope + three namespaced types + budget vector
(`situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §3, §8, §9, §11.3).*

- **WHAT** — `activeledger.py`: the ActiveLog v1 envelope `{alv,dev,seq,ts,mono,type,body,prev}`
  (append-only, (dev,seq)-keyed, sha256 `prev` chain) with types `cell.tick` (intra, own units — yin),
  `route.hop` (balanced double-entry `{credit,debit,price}` — yang), `ledger.transaction` (binds both
  sides + route total). fnv1a-64 canonical-JSON content hashing. Budget vector on every tick/hop.
  `route_sim.py`: mic → speech/noise pre-filter → STT → grammar-cleanup → LLM as deterministic cells.
  `otel_export.py`: projection to OTel-shaped spans + OpenInference attributes.
- **STATE** — **HEWN.** `selftest.py`: **28 checks, 0 failures**, offline & deterministic. Canonical
  route: pre-filter cuts STT load **10 → 4 frames (−60%)**, STT wall_ms 120 → 48, route total wall_ms
  175 → 113, power_w 7.58 → 5.38, identical transcript ("Turn on the lights.").
- **RUNS** — `python3 selftest.py` · `python3 -c "import route_sim as R; print(R.run(True)['transcript'])"`
- **SHORTCUT** — (1) **All cells are simulated** (fixed frames, canned words/reply); budgets are a
  deterministic cost model, not measurements. (2) **`DoubleEntry` is a minimal local implementation**
  with the documented contract (credit/debit/price, zero-sum after translation); `cell-runtime` was
  not read or wrapped. (3) The `cocapn-foundation/activelog-spec` schema was **not read** — the envelope
  is built from the shape in §8, so field-level details (e.g. `ts` format, `fix`) may differ; `ts` is a
  deterministic `det:NNNNNN` stamp, `fix` is unused. (4) Route total = sum of ticks **and** hops (as
  EX1 does); §8 says "sum of its hops" — flagged for the schema owner. (5) The org canary
  `0x24a555471370b18d` input is not documented in-repo, so it is not asserted; the fnv1a-64 core is
  checked against standard vectors instead. (6) OTel output is a dict projection; no collector tried.
- **ASSUMES** — Python 3.10+ stdlib only. Hash idiom == `labs/situation-recorder`.
- **BETTER-WHEN** — real cells replace the sim; `cell-runtime`'s `DoubleEntry` is wrapped; the
  official event schema is validated in CI; EX1 (`calculator-quilt`) imports this emitter; B2 audits
  each hop's round-trip via `EFFECT(forward, inverse)` (here only the zero-sum smoke test runs).
- **NEXT** — B2 `unit-translation-audit`; B3 `pincher` as the second route; factor EX1 onto this module.
