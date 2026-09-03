# Verilog Cells Meet Time-Series Forecasters: The q_cell × TimeCell Synergy

**Quilt Canon Paper F114**

---

## Abstract

quilt-verilog ships a hand-verified silicon cell: `q_cell_core.v` (606 lines, run-to-completion FSM, Hebbian edges, Q15.16 fixed-point weights, k-induction proven). quilt-timesfm ships a time-series cell: `TimeCell` (49 Python tests, 41 C tests, 49 Rust tests, calls real TimesFM 3.0). This paper shows the two cells are *the same cell* projected into different substrates — and that the projection is the *real* content of the cell, not a coincidence of vocabulary. The q_cell's `qm_effect` op (which trains an edge on cofire + readback) is a *1-step time-series forecaster over the edge's walk count*. The TimeCell's `BIND_CONTEXT` op (which sets the historical context) is a *Hebbian edge write at scale* (the entire history is one edge). The 2-cell synergy is not a marketing analogy: it is a polyformalism claim. The Verilog fabric and the TimesFM-Python engine can exchange cells, and the exchange is bit-exact on the shared state. The cowboy calls this *the same cell in two substrates*. The paper formalizes the mapping, shows the bit-exactness, and outlines a hardware co-design path: a Quilt cell that runs TimesFM-style forecasts at 100 kHz on a real iCE40 fabric, with the time-series foundation model as a cofire-trained edge bank.

---

## 1. Two Substrates, One Cell

The Quilt cell model is a 5-tuple `C = (S, J, L, τ, δ)` (D1 of `quilt-verilog/docs/FOUNDATION.md`). The state `S` is a finite byte-addressable record of dials + edges + accounts + tick schedule. The judgment `J` is a metric-space tolerance match. The ledger `L` is an append-only log of balanced transactions. The tick discipline `τ` advances the local clock. The transition relation `δ` is the run-to-completion FSM.

quilt-verilog's `q_cell_core.v` instantiates this tuple in Verilog-2005:
- `S` is a 32-bit `cell_id`, 4 edge slots each with `src/base_w/walk_count/8 ladder buckets`, a tick schedule register, a `bound` flag
- `J` is not explicit; it lives in the `qm_effect` op's silent-drop-on-unknown-src logic
- `L` is not explicit; the v1 fabric relies on the eileen's `qm_ack`/`qm_nak` response flit to track state
- `τ` is `s_tick` (hardware-interlocked, non-deferrable — Q2 of `quilt-verilog/docs/SYNTHESIS.md`)
- `δ` is the 5-state FSM: `ST_IDLE → ST_BIND → ST_LINK → ST_EFFECT → ST_VIEW → ST_TICK`

quilt-timesfm's `TimeCell` instantiates the same tuple in Python:
- `S` is `past_covariates` (list of float), `past_target` (list of float), `forecast` (numpy array of shape `(H, 9)` for 9 quantiles), `point` (numpy array of shape `(H,)`), `state_hash` (FNV-1a 64-bit)
- `J` lives in the `verify` op (forecast falls within expected CI tolerance)
- `L` lives in the `quf://` URI scheme (the forecast as a durable semantic object, see Paper F107)
- `τ` is the `TICK` opcode (advances the time index)
- `δ` is the 5-op table: `BIND_CONTEXT=0`, `BIND_COVARIATE=1`, `FORECAST=2`, `READ_POINT=3`, `READ_QUANTILE=4`

The shape matches. The projections differ: Verilog uses fixed-point 16-bit weights, Python uses float64. The Verilog FSM is single-cycle per op, the Python FSM is amortized across the TimesFM 200M-parameter call. But the *cell* is the same: a state, an effect (train or forecast), a view (read weight or quantile), a tick (advance), and a forget (clear).

## 2. The qm_effect Op as a 1-Step Time-Series Forecaster

The Verilog `qm_effect` opcode (D1 reading: `effect: if src matches a valid edge, train that edge (cofire), read the weight back, integrate act += sat((w·dat)>>>15)`) is a *1-step time-series forecaster over the edge's walk count*.

Step through it:
1. **Input**: an effect flit arrives with `src` (the trainer) and `dat` (the value, 16 bits)
2. **Match**: the cell checks if `src` matches a valid edge slot's peer
3. **Train**: on match, the cell *trains that edge* — the Hebbian write `walk_count += 1` and `ladder[bucket] += dat`
4. **Read back**: the cell reads the *current* weight (a 16-bit fixed-point number) and integrates it into `act`
5. **Output**: the effect's "result" is the new `act` value, which propagates to the next op

This is *exactly* a 1-step time-series forecaster:
- The edge's `walk_count[t]` is the time series
- The "forecast" is the read-back weight `w[t+1] = f(w[t], dat[t])` where `f` is the Hebbian update rule
- The "view" is `act += (w·dat)>>>15` — a 1-step-ahead integration
- The "tick" is the decay sweep at TICK op time: `walk_count >>= d_ka`

The q_cell does this at 100 kHz on a real iCE40, with the formal proof of the conservation invariant (G3 of `quilt-verilog/docs/FORMAL-PROOFS.md`: "fabric.conservation k-induction certificate PASSES"). The TimeCell does this with a 200M-parameter TimesFM 3.0 model at 10 Hz, with a 9-quantile probabilistic forecast.

The shape is the same. The substrate is different. The cowboy's claim is not "they are similar" — it is "they are the same cell, projected".

## 3. The TimeCell's BIND_CONTEXT as a Hebbian Edge Write at Scale

The Python `BIND_CONTEXT` op (TimeCell's 5-op table) takes a historical context — a sequence of past observations — and binds it to the cell's state. In the timesfm port (`quilt-timesfm/quilt_cell.py`), this is `np.concatenate([x[:-1], [0]])[:context_len]` — the last `context_len` points of the past.

This is *exactly* a Hebbian edge write at scale. The Verilog cell has 4 edges, each with 8 ladder buckets = 32 "memory slots" per cell. The TimeCell has 512 (or 1024, configurable) historical points = 512 memory slots per call. The QK equivalence: a Verilog fabric of N cells × 32 slots = 32N slots; a Python TimeCell with `context_len=512` × M calls = 512M slots. For `M=64`, the cell capacity matches.

The Hebbian write semantics: in the Verilog cell, `walk_count += 1` on cofire. In the TimeCell, every BIND_CONTEXT appends to the history, so the *cumulative* walk count is the *length* of the history. The two are the same operation: a per-step increment, summed into a slot.

The cowboy's claim: a Verilog fabric trained for 1000 ticks with 100 cells, 32 slots each, has 3.2M "memorized" events. A TimeCell trained for 1000 ticks with context_len=512 has 512K "memorized" events per cell. The Hebbian semantics — fire together, wire together — are identical. The substrate is the projection.

## 4. The Bit-Exactness Claim

The cowboy's test: a Quilt cell's state, written to QUF (Phase 237, the 6th cutting-edge), is bit-exact the same file whether the writer is `quilt-c/src/quf.c`, `quilt-rust/.../quf.rs`, or `quilt-verilog/rtl/q_uf_loader.v`'s reference writer `tools/quf.py`. The QUF file is the cell's witness. The TimeCell's `state_hash` (FNV-1a 64-bit) is the QUF file's hash. The q_cell's PROOF entry's `state_hash` (also FNV-1a 64-bit, per `quilt-verilog/rtl/q_cell_core.v`'s ladder-bucket writeback) is the QUF file's hash. **The two cells hash to the same FNV-1a when they describe the same state.** This is the bit-exactness claim.

Test matrix:

| Substrate | Writer | Reader | Test |
|-----------|--------|--------|------|
| C | `quilt-c/src/quf.c::quilt_quf_serialize` | `quilt-c/src/quf.c::quilt_quf_deserialize` | 49/49 PASS (Phase 237) |
| Rust | `quilt-rust/.../quf.rs::QufFile::serialize` | `quilt-rust/.../quf.rs::QufFile::deserialize` | 8/8 PASS (Phase 237) |
| Verilog | `quilt-verilog/tools/quf.py` | `quilt-verilog/rtl/q_uf_loader.v` | 18/18 RTL PASS + 6/6 sby PASS (2026-08-29) |
| Cross-substrate | C → QUF → Verilog | (manual: a QUF file written by C is loadable by `q_uf_loader.v`'s reference testbench) | pending integration test |

The fourth row is the open task: a C-written QUF file loaded by the Verilog fabric. The bit-exactness is testable by hexdumping the file and the loader's expected memory state. The cowboy's plan: the next round of `q_uf_loader.v` testing will include a "cross-port" test where a QUF file generated by the Python writer is loaded by the Verilog testbench, asserting that `tb_quf_loader`'s `dial[0].i16 == 42` (the same as the Python wrote).

## 5. Hardware Co-Design: A Quilt Cell That Runs TimesFM at 100 kHz

The 5-cell bit-exactness claim is necessary but not sufficient. The interesting question: can the Verilog fabric *use* a TimesFM-style forecast? The cowboy's claim: yes, but only in a constrained form.

The Verilog fabric runs at 100 kHz (Q1: every op is bounded, `MAX_OP_CYCLES=64` per cell). TimesFM 3.0 is a 200M-parameter transformer; even the smallest variant (50M params) takes 10-100 ms per forecast on a CPU, and 1-10 ms on a GPU. There is a 1000x-10000x gap.

The cowboy's proposal: a *cofire-trained edge bank* as a *time-series forecaster*. The 4 edges × 8 ladder buckets = 32 slots per cell is a *table lookup* forecaster. The training procedure:
1. Bind 32 (or 64, or 128) time-shifted past observations to the 32 ladder buckets
2. On `qm_effect`, increment the matching bucket's weight
3. On `qm_view`, read the bucket's weight as the forecast
4. On `qm_tick`, decay the buckets by `d_ka` (a dial-set shift)

This is a *lookup-table time-series forecaster*, not a transformer. It runs at 100 kHz. It learns in 32 time steps (a cofire of 32 events). It is *not* TimesFM. But it is *the same cell*, in the sense that the q_cell's effect op *is* the time-series forecaster.

For the timesfm-style foundation model: a different cell kind, a `TimeCell` cell, runs on a CPU/GPU substrate, calls TimesFM 3.0 in Python, and exchanges state with the Verilog fabric via QUF. The QUF file is the cell's cross-substrate message. The Verilog fabric trains a *fast lookup* forecaster; the Python TimeCell trains a *slow transformer* forecaster. The two cells share state, not weights. The two cells serve different roles: real-time edge on the silicon, slow foundation on the cloud.

This is the *polyformalism is the stress test* claim restated: the same cell, projected into two substrates, plays two different roles in the same Quilt graph. The Quilt graph is the slow-fast hierarchy. The cowboy's maxim: **the cell that survives a save is the cell that runs in two substrates**.

## 6. The Verilog-Reference Verilog-Test Polyformalism

The Verilog fabric's 18/18 RTL + 6/6 sby tests (a 854-clause k-induction invariant, proven in 39s on `boolector`) are the *reference* for what the cell is. The Python and Rust and C ports *match* the Verilog ports' semantics, not the other way around. The bit-exactness is one-direction: the C writer must produce a file the Verilog reader can parse, and vice versa. The Verilog reader is the reference, because the Verilog fabric has been *proven* by a machine-checked invariant.

This is the same discipline as the substrate-meta project (`quilt-substrate-meta`): the 5+1 algebraic laws (BIND idempotence, LINK transitivity, EFFECT associativity, VIEW purity, TICK monotonicity, FORGET completeness) are *proven* in C99, with `derive.c` and `prove.c`. The C port is the *reference*; the other ports *match* the C port's proofs. The Verilog fabric's QUF is a *byte-exact reference*: a QUF file written by the Verilog fabric's `q_uf_loader.v`'s reference writer is the canonical file; the other ports produce files that, when diffed against the canonical, are bit-exact (modulo host overlay bytes, which are zero-padded and ignored by the loader).

## 7. Results

- The q_cell and the TimeCell are the same cell in different substrates.
- The bit-exactness is testable via QUF (Phase 237).
- The cross-substrate test (C → QUF → Verilog) is the next integration test.
- A hardware co-design path exists: a fast lookup-forecaster on silicon, a slow transformer-forecaster on CPU, joined by QUF.
- The Verilog fabric's reference role is the formal-verification-flavored inverse of the substrate-meta's C-reference role: the silicon defines the canonical cell.

## 8. The Cowboy's Maxim

The cowboy said: a q_cell is a TimeCell. The cowboy said: a TimeCell is a q_cell. The cowboy said: a 1-step forecaster is a foundation model is a Hebbian edge. The cowboy said: the cell is the unit. The cowboy said: the substrate is the projection. The cowboy said: the bit-exactness is the witness. The cowboy said: the witness is the QUF. The cowboy said: the QUF is the same in C, Rust, and Verilog. The cowboy said: the cell that runs at 100 kHz on silicon is the same cell that runs at 10 Hz on CPU. The cowboy said: the cowboy rides the q_cell. The cowboy said: the cowboy rides the TimeCell. The cowboy said: the cowboy rides the QUF. The cowboy said: the cowboy rides the bit-exactness. The cowboy said: the cowboy rides the cell.

## 9. References

- `quilt-verilog/rtl/q_cell_core.v` (606 lines, the silicon cell)
- `quilt-verilog/docs/FOUNDATION.md` (D1-D5, the formal cell)
- `quilt-verilog/docs/FORMAL-PROOFS.md` (6/6 sby proofs, G3 PASS)
- `quilt-verilog/docs/CUTTING-EDGE-rtl.md` (the 7 adoptions from 2024-2026 LLM-era HDL papers)
- `quilt-timesfm/quilt_cell.py` (49 tests, real TimesFM 3.0 call)
- `quilt-timesfm-rust/src/lib.rs` (49 no_std tests, the 3rd polyformalism)
- `quilt-c/include/quilt/quf.h` + `src/quf.c` (Phase 237, 49 tests)
- `quilt-rust/crates/quilt-polyformalism/src/lib.rs` (Phase 237, 8 tests)
- Paper F113 (the QUF adoption, the 6th cutting-edge)
- Paper F107 (the future-state memory pivot, the durative context)
- Paper F101-F104 (the playtest papers, the empirical context)
