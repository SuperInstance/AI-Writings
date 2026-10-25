# NQ-C3 — METAL SPIKE: worm touch-arc subcircuit → Verilog, bit-exact vs Python

**Lane:** NQ-C (metal) · **Date:** 2026-09-03 · **Spawned from:** inbound thesis audit (`AUDIT-SHEET-IS-THE-RUNTIME.md`)
**Claim under test (the doc's most auditable sentence):** *"a deterministic cell subgraph compiles to a hardware netlist"* and the netlist reproduces the Python-computed spike logic **bit-exactly on a fixed input trace**.

## Verdict up front

**NQ-C3: PASS.** All three pre-registered traces match **byte-for-byte** between the Python integer simulation and the iverilog-compiled Verilog netlist (100 ticks × 7 cells × 16-bit accumulators + fire bits compared). Yosys elaborates the same module to a **1,566-cell generic netlist** (119 SDFF + 144 MUX + wide combinational), i.e. it is a real synthesizable circuit, not a behavioral script. One honest rider: **under the pre-registered dynamics (TH = strongest incoming chemical weight, half-leak per tick), the arc does not propagate past the first synapse** — only AVM (the sensory cell) fires; downstream accumulators rise and fall but never reach threshold. The gate was bit-exact equivalence, not worm behavior — PASS stands on the equivalence; the propagation extinction is booked as the corpse finding for a future TH/leak sweep (NQ-C4 candidate).

## Circuit (verbatim from the cached NQ-C1 dataset)

- **Provenance:** `/tmp/NeuronConnect.xls` (WormAtlas, White et al. hermaphrodite somatic), sha256 `120c2c6332050a2d1494c19c687f447ed65620ad0db5f8b732189aa10e5162f1` — asserted at runtime; mismatch aborts.
- **Cells (7):** AVM (anterior touch receptor) · AVBL, AVBR (forward command) · PVCL, PVCR (command) · DB02, DB03 (B-class motor). This is the actual anterior-touch data path: AVM→AVB/PVC chemical, PVC→AVB chemical (the heaviest edges in the arc: PVCL→AVBR = 12, PVCR→AVBL = 8), AVB↔AVBR + AVB→DB gap junctions — the worm drives its B-motor pool electrically.
- **Weights:** summed synapse counts verbatim (16 chemical edges, 6 gap pairs; AVB↔AVBR and PVC↔PVC pairs carry BOTH chemical and gap wires — kept as separate contributions). **No tuning.**
- **Thresholds (pre-registered rule):** TH[i] = strongest incoming chemical weight (AVM: its own strongest outgoing, 6). → AVM 6, AVBL 8, AVBR 12, PVCL 4, PVCR 5, DB02 3, DB03 4.
- **Dynamics:** integer threshold-sum-fire · sensory poke lands at tick start (amendment, booked below) · chemical/gap fanout lands with one-tick delay · refractory 1 tick · half-leak per tick · saturating 16-bit arithmetic with **single saturation from exact 32-bit sums** (order-free, synthesizable). No floats — "rubber rulers" avoided per the doc's own (correct) doctrine.

**Amendment booked before any comparison ran:** the first implementation evaluated fire on pre-poke state, which starved the pre-registered weak pokes (T1/T3 produced zero events — a vacuous test). Amended: sensory lands first, fire after. The PASS gate itself never changed.

## Receipts (verbatim)

```
raw sha256 = 120c2c6332050a2d1494c19c687f447ed65620ad0db5f8b732189aa10e5162f1
chemical edges: [('AVBL','AVBR',1), ('AVBR','AVBL',1), ('AVM','AVBL',6), ('AVM','AVBR',6),
 ('AVM','PVCL',4), ('AVM','PVCR',5), ('PVCL','AVBL',5), ('PVCL','AVBR',12), ('PVCL','DB02',3),
 ('PVCL','DB03',4), ('PVCL','PVCR',2), ('PVCR','AVBL',8), ('PVCR','AVBR',6), ('PVCR','DB02',1),
 ('PVCR','DB03',3), ('PVCR','PVCL',3)]
gap pairs: AVBL↔AVBR, AVBL↔DB03, AVBR↔DB02, AVBR↔DB03, DB02↔DB03, PVCL↔PVCR
TH: AVM 6, AVBL 8, AVBR 12, PVCL 4, PVCR 5, DB02 3, DB03 4

[T1] bit-exact vs python: PASS   (poke 5 @ t0,1,2 — 30 ticks)
[T2] bit-exact vs python: PASS   (poke 8 @ t0..5   — 30 ticks)
[T3] bit-exact vs python: PASS   (poke 6 @ t0..2 + t10..12 — 40 ticks)
NQ-C3 VERDICT: PASS
```

T2 opening (identical in both files; AVM=col1 … DB03=col7):

```
t=00 fires=01 acc=0001 0003 0003 0002 0002 0000 0000
t=02 fires=01 acc=0003 0003 0003 0002 0003 0000 0000
t=04 fires=01 acc=0003 0003 0003 0002 0003 0000 0000   ← receptor saturating w/ refractory
t=08 …all zeros (arc extinguished — booked)
```

Synthesis (yosys 0.47, `synth -top worm_arc; stat`):

```
Number of cells: 1566   $_SDFF_PP0_ 119 · $_MUX_ 144 · $_ANDNOT_ 381 · $_OR_ 302
                        $_XOR_ 203 · $_NOR_ 99 · $_ORNOT_ 86 · … (no memories, no processes)
```

Files: `nq_c3_spike.py` (sim + emitter + comparator), `worm_arc.v` + `tb_worm_arc.v` (emitted from the same data structures — weights are never hand-typed twice), `trace_py_*.txt` / `trace_v_*.txt`, `spike_meta.json`.

## What this proves and does not prove

- **Proves:** the doc's core compilability claim in miniature — a deterministic integer cell subgraph derived from a real connectome, with verbatim synaptic weights, compiles to Verilog-2005, passes RTL simulation, synthesizes to a netlist, and is **bit-exact against an independent Python model**. The determinism boundary the doc preaches is real and cheap: no floats, single-saturation sums, one-tick delays.
- **Does not prove:** that arbitrary quilt sheets compile this way (no such compiler exists — the audit's finding), that the dynamics model the worm (it doesn't propagate under this TH/leak — the worm is not a half-leak-per-tick machine), or anything at fleet scale.
- **Note on the toolchain:** done standalone (emission + iverilog/yosys from the pinned oss-cad-suite) rather than inside the quilt-verilog fabric; the fabric's own `q_cell_core` tick/fire model (act ≥ thresh ∧ refr = 0, integrate-then-leak) is the same skeleton this spike uses — wiring the arc through real fabric cells is the natural NQ-C4/NQ-C5.
