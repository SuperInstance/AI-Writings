# QUIL — RFC: an HLS pseudolanguage for the quilt

**Status:** RFC (design decided; compiler not yet built) · **Date:** 2026-09-04
**Lane:** QUIL · **Charter:** two prior QUIL lanes died exploring; this lane writes the design only — no exploratory tooling, the design is already decided.
**Home:** this doc. Implementation lands in quilt-verilog when a builder lane picks it up (Two-Division Wheel: ideators feed builders — this is the feed).

---

## 0. What QUIL is

**QUIL = Quilt Intermediate Language.** A high-level-synthesis (HLS) *pseudolanguage* that lowers to synthesizable Verilog **within quilt paradigms** — not a new HDL, but a front end whose every construct maps 1:1 onto fabric concepts already proven in quilt-verilog:

| QUIL construct | Quilt paradigm it lowers from |
|---|---|
| `cell`, `int<PW>` | the cell as unit of state + witness |
| `tick` | the fabric-wide tick; append-only diff history (D5) |
| `view` | ledger/fabric read: pure function of history prefix |
| `bind` / `link` | wires with declared fan-out and arrival mechanism |
| `propose` | the neural/probabilistic side — proposals, never gates |

The thesis under test (inheritance from NQ-C3): **a deterministic cell subgraph compiles to a hardware netlist**, bit-exact against its reference. NQ-C3 proved it for one hand-written circuit (see §3). QUIL generalizes: the same proof must hold for *anything expressible in the language*, because determinism is not a property programmers maintain — it is a **lowering artifact**. The grammar cannot express a nondeterminism.

House law that motivates the whole design: byte-exact fabric work never passes through LLM inference (Two-Division Wheel, "rules carried"). QUIL makes that boundary *syntactic*: the neural side is grammatically quarantined (§1.5).

---

## 1. GRAMMAR (one page)

### 1.1 State: `cell` and `int<PW>`

```
cell <name> {
  int<PW>  <field>;        // PW-bit signed integer state (parametric width)
  int<PW>  <field> = <k>;  // initial value, journal entry 0
}
```

- All state lives in cells. Cells are the only things that *have* state; everything else is derived.
- `int<PW>` is the only data type. No floats, no strings, no pointers. PW is a **parameter** (§2.3): the compiler derives a minimum width and refuses widths below it; the *same source* must be bit-exact across all legal PW.
- A cell may reference constants and the journal (§1.3) but never another cell's raw state — only views of it.

### 1.2 `tick` — the only writer

```
tick { <effect assignments> }
```

- **Single-writer per cell per tick, and `tick` is the only writer, period.** Every effect assignment (`dest <= expr` inside a `tick` block) lowers to exactly one **journal entry** appended to that cell's diff history. Nothing outside `tick` writes anything.
- Within one tick, a cell's new value is a pure function of (its old value, the views it reads, black-box inputs). No assignment in a tick may read another assignment's *same-tick* result — the compiler rejects the cycle. This is SPIN-19's lesson made a *parse error*: the non-blocking last-write-wins mass-counter bug (only the final sensor's contribution survived each cycle) is a bug class QUIL makes inexpressible. You cannot write the bug, so it cannot ship.
- Determinism is therefore a **lowering artifact**: replaying journal entries 1..k reproduces the fabric bit-for-bit (D5) *because there is no other place state could have come from*.

### 1.3 `view` — pure function of the journal prefix

```
view <name>(<cell>.<field>, ...) -> int<PW> {
  <pure expression over the journal prefix>
}
```

- A view is a pure, total function of a **prefix of the journal** — never of "current state" as a mutable thing. It is replay-exact by construction: same prefix in, same value out, no side channels.
- **Trace-hash PW-invariance is a compiler check, not a hope:** the compiler simulates the design at two legal widths (PW and PW+1, or the derived floor and a wide over-approximation) and requires the emitted trace hash to be identical. A design whose observable behavior depends on width is rejected at compile time, not discovered in cosim. (This is the dequant discipline from SPIN-34, booked as: bit-exact down to PW = 41 for the reference design family — the floor is derived, not guessed; see §2.3.)

### 1.4 `bind` / `link` — declared fan-out, chosen arrival

```
bind <src view> -> <dst cell>[, <dst cell>...]   fanout = <n>  arrive = <mechanism>;
link <cellA> <-> <cellB>                          kind = gap;
```

- Every edge declares its **fan-out** at bind time. One writer, N named readers — the conservation ledger (D4) reconciles each tick that every bound value was delivered or dropped-with-entry.
- **Arrival is a synthesis-time choice**, not a language semantic. The language fixes *what* arrives and *that* it arrives exactly once; the compiler picks the mechanism from the **round-19 mechanism family**:
  1. **queue cell** — an intermediate cell buffers the value in its own journal;
  2. **credit fence** — receiver holds a credit token; delivery gated on token presence;
  3. **staged grant** — multi-cycle handoff where the writer journals a grant and the reader's tick consumes it.
  
  All three are observational-equivalent in simulation (same trace, same hash); they differ only in area/latency after synthesis. Switching `arrive =` never changes the bit-exact gate — only the netlist shape.
- `link` is the symmetric (gap-junction-shaped) form: both sides read a view of the other, still single-writer each way, still one journal entry per effect.

### 1.5 `propose` — the neural side never gates

```
propose <name> { <external black-box declaration> }   // lowers to an input port, nothing more
```

- The neural/probabilistic side lowers to a **black-box input port** feeding a `propose` region. It *suggests*; it never gates. `propose` output may only appear inside `tick` expressions guarded by deterministic conditions (thresholds, credits) — it can never appear in a view, never in an arrival-fence condition, never as a write enable.
- **No floats, no wall-clock, no nets inside the helm region — grammatically.** The helm region (deterministic control: ticks, binds, views) accepts only `int<PW>`, constants, journal-derived values, and black-box inputs *as integers*. The language has no float literal, no clock-reading primitive, no network primitive for helm code to even name. The determinism boundary is not a convention here; it is the absence of vocabulary.

### 1.6 Loops — static or journal-derived, nothing else

```
for i in 0..<N>            // static bound (elaboration-time constant)
for i in journal(<cell>)   // journal-derived trip count (replay-exact by D5)
```

- Trip counts must be **static** or **derived from the journal prefix**. Data-dependent loops on live state (unbounded, un-replayable) are a parse error. This keeps elaboration finite and replay total — the two properties every downstream proof leans on.

---

## 2. LOWERING RULES (QUIL → Verilog)

The compiler (`quilc`, to live in quilt-verilog) lowers in four passes. Each pass ships red/green (D1) and cites its own receipts (D3).

### 2.1 Pass L1 — elaboration

- Expand static loops; unroll journal-derived loops against a pre-registered trace or the declared maximum.
- Build the cell/wire graph; check single-writer, fan-out declarations, cycle-freedom within ticks. Any violation is a compile error — **before any Verilog exists**.

### 2.2 Pass L2 — journal lowering

- Each cell + its journal prefix becomes: a PW-bit register (or register file for multi-field), plus the *function of the prefix* expressed as combinational logic over the register and inbound wires.
- Each `tick` effect assignment becomes one non-blocking update, but only after the pass proves single-write: where a source-level tick computes a value from multiple contributions (e.g. summing N inbound edges), L2 **must** emit a blocking-assignment local accumulator feeding a single non-blocking write** — the SPIN-19 fix, now emitted mechanically so no human re-introduces the bug.
- Arrival mechanisms materialize here, chosen by the cost model (or pinned by the author via `arrive =`):
  - queue cell → an extra register stage (one journal entry deep);
  - credit fence → a credit counter per receiver, delivery muxed on credit ≠ 0;
  - staged grant → grant/ack handshake flops, writer journals the grant.
- Conservation ledger (D4) lowers to assertion logic in the testbench (not in the shipped netlist): every bound value delivered or explicitly dropped-with-entry each tick.

### 2.3 Pass L3 — width derivation (the PW rules)

- **PW is parametric with a compiler-derived floor.** The compiler computes, per design: the maximum journal-derivable magnitude (worst-case accumulation over the longest static/journal-derived loop), the saturation policy required, and the arrival-mechanism counters' widths. The floor PW_min is the smallest width at which the two legal guarantees hold:
  1. **Bit-exactness vs the integer reference** at the pre-registered traces (the NQ-C3 gate, generalized), and
  2. **Trace-hash invariance across legal PW** (§1.3) — simulate at PW_min and at an over-approximating wide width; identical trace hashes or the design is rejected.
- Booked anchor (SPIN-34): for the reference design family, bit-exactness held **down to PW = 41** — i.e. the floor was real, derived, and 5 bits below the hand-picked default, with the trace hash unchanged across the sweep. Designs whose floor cannot be established (unbounded growth, e.g. the step5_off-style reference that explodes to ~10^600 while a fixed-width datapath wraps — the SPIN-19 corpse finding) **do not lower**; the compiler names the cell and refuses. No silent wrap, ever.
- Saturation arithmetic follows NQ-C3's rule: single saturation from exact wider sums (order-free, synthesizable). No floats anywhere in lowering.

### 2.4 Pass L4 — Verilog emission

- Emit one module per helm region: parameter `PW`; ports for black-box `propose` inputs (integer-width, direction in); one clocked `always` block per tick phase; no `initial` state beyond journal entry 0.
- Output is plain synthesizable Verilog — elaborated by yosys with no processes/memories surviving into the generic netlist (NQ-C3's receipt format is the template: cell count + cell-type breakdown).

### 2.5 Verification-before-report (D7)

Every lowering claim is re-verified in the working tree, this session, with the commands and outputs in the run trail: iverilog trace equality vs the reference, trace-hash equality across PW, yosys elaboration stats. "Green on my machine last week" is not a report.

---

## 3. ACCEPTANCE DEMO — NQ-C3 worm touch-arc in QUIL

**The gate that proves QUIL is a strict generalization of a proven hand-build.**

### 3.1 The reference (booked, PASS)

NQ-C3 (2026-09-03, `docs/nq-c3-metal/`): the *C. elegans* anterior touch-arc — 7 cells (AVM, AVBL, AVBR, PVCL, PVCR, DB02, DB03), 16 chemical edges + 6 gap pairs with summed-synapse weights verbatim (WormAtlas provenance, sha256-pinned), thresholds TH[i] = strongest incoming chemical weight, integer threshold-sum-fire, one-tick edge delay, refractory 1 tick, half-leak, saturating 16-bit with single saturation from exact 32-bit sums. The hand-written `worm_arc.v` matched the Python reference **byte-for-byte on 3 pre-registered traces**, and yosys 0.47 elaborated it to a **1,566-cell generic netlist** (119 `$_SDFF_PP0_` + 144 `$_MUX_` + wide combinational; no memories, no processes).

### 3.2 The demo, as QUIL

The same circuit in QUIL (sketch — this is design-intent for the acceptance test, not shipped code):

```
cell AVM    { int<PW> acc = 0; int<PW> refr = 0; }   // …7 cells
view  w_in(src, wt) -> int<PW> { wt * fired(src, -1) }  // journal prefix at t-1

bind  avm_out -> avbl, avbr, pvcl, pvcr   fanout = 4  arrive = queue_cell;
link  avbl <-> avbr                        kind = gap;   // …6 gap pairs

propose poke { external port int<PW> poke_strength }     // sensory input, black box

tick {  // per cell c:
  // acc_next = sat16(exact32(acc - leak) + Σ_in w_in)   ← L2 emits the safe accumulator
  // fire     = (acc_next >= TH[c]) && (refr == 0)
}
for i in 0..<TICKS { tick }        // static trip count; poke from the input port trace
```

Everything NQ-C3 hand-wired is expressed: cells state, one-tick arrival (`arrive = queue_cell`), gap symmetry (`link`), the sensory poke as `propose` input, the leak/refractory/threshold inside `tick`. Nothing more.

### 3.3 The acceptance criteria (pre-registered, kill condition first)

1. **Bit-exact trace equality:** QUIL→quilc→Verilog, simulated under iverilog on the three NQ-C3 traces (T1 poke 5 @ t0–2 / 30 ticks; T2 poke 8 @ t0–5 / 30 ticks; T3 poke 6 @ t0–2 + t10–12 / 40 ticks), must reproduce the Python reference and the hand-written netlist **byte-for-byte** — same accumulator columns, same fire bits, every tick.
2. **PW floor derived, not assumed:** quilc must derive PW_min and demonstrate trace-hash invariance across legal widths (the SPIN-34 discipline; the hand-build's 16-bit accumulators are expected to be above the floor, not at it).
3. **Synthesizability, same receipt format:** yosys `synth -top` elaborates with zero processes/memories surviving; cell count and type breakdown reported in the NQ-C3 format. (Cell-for-cell netlist equality with the hand-build is **not** required nor expected — arrival-mechanism and accumulator-shape choices may differ. The gate is behavioral bit-exactness, per NQ-C3's own precedent: "the gate was bit-exact equivalence, not worm behavior.")

**Kill condition:** any trace diverging at any tick, any floor that cannot be derived, or any process/memory surviving synthesis → QUIL fails as a strict generalization and the failure is booked first-class (a scar booked beats a result covered).

**Why this proves strict generalization:** NQ-C3 was one circuit, hand-lowered, with its determinism argued by a human reading 300 lines of Verilog. The same circuit in QUIL has its determinism *produced by the lowering*: single-writer is a parse property, the safe accumulator is emitted mechanically, arrival equivalence is the mechanism family's invariant, and width safety is a compile-time check. If the QUIL build is bit-exact with the hand build, then everything the human got right by care, the language gets right by construction — and everything *else* written in QUIL inherits those guarantees for free. That is the strict-generalization claim, and this demo is its falsifier.

---

## 4. Non-goals & open questions (booked, not hidden)

- **Not a goal:** behavioral fidelity of the worm arc (NQ-C3's propagation-extinction corpse finding stands — TH/leak sweep is NQ-C4's lane, not QUIL's).
- **Not a goal:** beating hand-written Verilog on area/latency. Arrival-mechanism selection is a cost-model knob for later rounds.
- **Open:** multi-tick-phase designs (one helm region, several `tick` blocks — grammar permits, lowering untested until a second demo demands it).
- **Open:** journal-derived trip counts beyond replay traces (needs a declared-maximum story that passes the width rules; sketched in L1, not proven).
- **Citation honesty (D2/D8):** NQ-C3 and SPIN-19 facts above are verifiable in `docs/nq-c3-metal/` and quilt-verilog `wheel/SPIN-19-rtl-honesty.md`. SPIN-34 (PW = 41 bit-exact floor) and the round-19 arrival-mechanism family are booked wheel facts cited from the charter; when this RFC's implementation lane lands, it must re-point those citations at their reachable docs before any claim depends on them.

---

*QUIL: the quilt's shapes, spoken in a language that cannot lie about time.*
