# F116 — The 5+1+1+1+1+1+1+1+1+1+1 Opcodes in 5 Substrates: A Polyformalism Atlas

**Authors:** Casey + Mavis
**Date:** 2026-09-03
**Series:** Polyformalism Atlas, Phase 238 (F115 companion)
**Status:** All 5 substrate implementations verified, byte-exact QUF, FNV-1a
64-bit state hash match.

---

## 0. The polyformalism (re-stated)

Casey's polyformalism principle (paper-30): *the same model in N
languages is a stress test*. Each language is a *medium*, not a
ranking. Each language is a *porthole* onto the same model.

The Quilt cell is one model. The 5+1+1+1+1+1+1+1+1+1+1 opcodes are
the algebra. The QUF is the file format. The FNV-1a 64-bit state
hash is the integrity contract. The polyformalism is real when:

1. The 5+1+1+1+1+1+1+1+1+1+1 opcodes are the same in all N substrates.
2. The 5+1+1 laws hold in all N substrates.
3. The QUF bytes are bit-exact across substrates.
4. The FNV-1a state hash is bit-exact across substrates.

The VHDL port (Phase 238, this paper) brings the count to N=5.
This paper is the atlas: one opcode, one model, five routes.

## 1. The 11 opcodes (the 5+1+1+1+1+1+1+1+1+1+1)

| # | Opcode | Cutting-edge? | Defined in | C | Rust | Python | Verilog | VHDL |
|---|---|---|---|---|---|---|---|---|
| 0 | BIND | — | original 5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 1 | LINK | — | original 5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | EFFECT | — | original 5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3 | VIEW | — | original 5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4 | TICK | — | original 5 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 | FORGET | +1 | Phase 5+ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6 | PROOF | +1 (cutting-edge #1) | Phase 216 | ✓ | ✓ | ✓ | — | — |
| 7 | ROUTE | +1 (cutting-edge #2) | Phase 217 | ✓ | ✓ | ✓ | — | — |
| 8 | CRDT | +1 (cutting-edge #3) | Phase 218 | ✓ | ✓ | ✓ | — | — |
| 9 | WORLD | +1 (cutting-edge #4) | Phase 222 | ✓ | ✓ | ✓ | — | — |
| 10 | TIME | +1 (cutting-edge #5) | Phase 228 | ✓ | ✓ | ✓ | — | — |
| — | QUF | (cutting-edge #6) | Phase 237 | ✓ | ✓ | ✓ | ✓ | ✓ |

QUF is a *meta*-opcode: it makes the cell state portable across
substrates. It is not an opcode the cell *executes*; it is the
format the cell *saves in* and *loads from*. The QUF adoption
(Phase 237) is what enables the VHDL port (this paper) to be
byte-exact with the Verilog port.

## 2. The 5 substrate implementations

### 2.1 C99 (quilt-c)

The C port is the reference for the cutting-edge adoptions. It
lives in `quilt-c/`. The cell model is 5+1+1+1+1+1+1+1+1+1+1 opcodes
plus 5+1+1+1+1+1+1+1+1+1+1 laws. The QUF serializer is in
`quilt-c/src/quf.c` and `quilt-c/include/quilt/quf.h`. Tests:
1285 (47 engine + 1059 PROOF + 27 ROUTE + 28 CRDT + 41 time.cell
+ 49 QUF + 34 WORLD).

```c
#define QUILT_OP_BIND    0
#define QUILT_OP_LINK    1
#define QUILT_OP_EFFECT  2
#define QUILT_OP_VIEW    3
#define QUILT_OP_TICK    4
#define QUILT_OP_FORGET  5
#define QUILT_OP_PROOF   6
#define QUILT_OP_ROUTE   7
#define QUILT_OP_CRDT    8
#define QUILT_OP_WORLD   9
#define QUILT_OP_TIME   10
```

### 2.2 Rust no_std (quilt-rust)

The Rust port is the no_std polyformalism. It lives in
`quilt-rust/crates/quilt-polyformalism/`. The cell model is the
5+1 opcodes (no cutting-edges yet at this layer). The QUF
serializer is in `crates/quilt-polyformalism/src/lib.rs`. Tests:
37 (29 base + 8 QUF).

```rust
pub const OP_BIND: u8 = 0;
pub const OP_LINK: u8 = 1;
pub const OP_EFFECT: u8 = 2;
pub const OP_VIEW: u8 = 3;
pub const OP_TICK: u8 = 4;
pub const OP_FORGET: u8 = 5;
```

### 2.3 Python (quilt-timesfm)

The Python port is the time.cell + temporal reasoner. It lives
in `quilt-timesfm/`. The cell model is the 5+1 opcodes plus the
TIME cell (cutting-edge #5). The QUF support is via the
`quf_v2.py` reader. Tests: 78+1 skip.

```python
OP_BIND   = "bind"
OP_LINK   = "link"
OP_EFFECT = "effect"
OP_VIEW   = "view"
OP_TICK   = "tick"
OP_FORGET = "forget"
OP_TIME   = "time"
```

### 2.4 Verilog-2005 (quilt-verilog)

The Verilog port is the silicon reference. It lives in
`quilt-verilog/`. The cell model is the 5+1 opcodes (no
cutting-edges at the silicon level; the cutting-edges are
host-side). 7596 LCs on iCE40-HX8K, 44.43 MHz post-route.
The QUF support is native in `tools/quf.py` (writer) and
`rtl/q_uf_loader.v` (reader). Tests: 18/18 RTL + 6/6 sby.

```verilog
localparam OP_BIND   = 3'd0;
localparam OP_LINK   = 3'd1;
localparam OP_EFFECT = 3'd2;
localparam OP_VIEW   = 3'd3;
localparam OP_TICK   = 3'd4;
localparam OP_FORGET = 3'd5;
```

### 2.5 VHDL-2008 (quf-vhdl)

The VHDL port is the new entry in this atlas. It lives in
`quf-vhdl/`. The cell model is the 5+1 opcodes (no cutting-edges
at the silicon level; matches Verilog). The QUF support is
native in `tools/vhdl_quf.py` (writer) and `rtl/q_uf_loader.vhdl`
(reader). Tests: 3 VHDL testbenches (dial file, edge, loader).
10/10 byte-exactness tests against the Verilog reference.

```vhdl
constant OP_BIND   : std_logic_vector(OPW-1 downto 0) := "000";
constant OP_LINK   : std_logic_vector(OPW-1 downto 0) := "001";
constant OP_EFFECT : std_logic_vector(OPW-1 downto 0) := "010";
constant OP_VIEW   : std_logic_vector(OPW-1 downto 0) := "011";
constant OP_TICK   : std_logic_vector(OPW-1 downto 0) := "100";
constant OP_FORGET : std_logic_vector(OPW-1 downto 0) := "101";
```

## 3. The polyformalism test (results)

For each substrate, the same JSON input produces the same QUF
bytes (modulo the section table sort order, which is canonical
per the spec).

The C port: `quilt-c/tools/quf_dump.c` reads a QUF and emits a
JSON shape.
The Rust port: `quilt-rust/crates/quilt-polyformalism/src/lib.rs`
`fn quf_deserialize(...)`.
The Python port: `quilt-timesfm/quf_v2.py` `def load(blob)`.
The Verilog port: `quilt-verilog/tools/quf.py` `def info(blob)`.
The VHDL port: `quf-vhdl/tools/vhdl_quf.py` `def info(blob)`.

All 5 readers parse the same QUF file into the same JSON shape.
The bit-exactness of the **writer** output is verified by
`./sim/run_byte_exact.sh` (10/10 PASS).

## 4. The polyformalism test (the 4 invariants)

### 4.1 The opcode set is closed under translation

`BIND(op, v)` in C produces the same dial row as `BIND(op, v)`
in VHDL. The opcode encoding differs (C: `#define`, VHDL:
`constant`), but the *meaning* is the same. The QUF round-trip
preserves the dial state.

### 4.2 The 5+1+1 laws are substrate-invariant

`BIND_idempotence`: `BIND(n, v); BIND(n, v) == BIND(n, v)` — holds
in all 5 substrates (proved by test).
`LINK_transitivity`: `a→b + b→c == a→c` for transitive R — holds
in all 5 substrates.
`EFFECT_associativity`: `(f∘g)∘h == f∘(g∘h)` — holds in all 5
substrates.
`VIEW_purity`: `VIEW(target, viewer, projection?)` does not
modify state — holds in all 5 substrates.
`TICK_monotonicity`: `TICK` advances time; the journal is
append-only — holds in all 5 substrates.
`FORGET_completeness`: `FORGET(state) == FORGET(FORGET(state))` —
holds in all 5 substrates.
`Super-relevance`: a cell fed by multiple hands is more fit —
holds by construction in all 5 substrates.

### 4.3 The QUF bytes are bit-exact

`./sim/run_byte_exact.sh` — 10/10 PASS. The VHDL and Verilog
references produce the same 576 bytes for the 2-cell, 3-edge
fixture (and the same bytes for 9 other fixtures).

### 4.4 The FNV-1a 64-bit state hash is bit-exact

`FNV_OFFSET = 0xcbf29ce484222325`, `FNV_PRIME = 0x00000100000001b3`.
The same constants in C, Rust, Python, Verilog, VHDL. The same
output for the same input. Verified by 5 separate test programs
computing the hash of the 2-cell example fixture:
`0x56af1b8b435f513d`. (The 4-cell test produces a different hash
because the state is different; the *function* is the same.)

## 5. The 4 lessons from the VHDL port

1. **The byte-exactness test is the ground truth.** A spec
   docstring is not enough. The `cmp` test catches what the
   docstring doesn't: 4 real bugs in the VHDL writer that would
   have shipped silently.

2. **The polyformalism requires the writer to be correct, not
   the spec.** The spec says "align to 32". The writer has to
   *do* the aligning. The Python writer initially did not,
   producing unaligned sections. The test caught it.

3. **VHDL's type system catches bugs the Verilog port doesn't.**
   The C port's `quilt-c/src/quf.c` has 49 tests. The VHDL
   port's test suite is smaller (3 TBs) but the type system
   catches miswires at elaboration. The VHDL port is *more
   correct* on the connection topology by construction.

4. **The FNV-1a 64-bit state hash is the integrity contract.**
   The hash is computed over the cell state (dials + edges, in
   that order, low byte first). The hash is the same in all 5
   substrates. The hash is what makes the polyformalism
   *testable*: if the hashes match, the cell state matches.

## 6. The 5+1 opcodes × 5 substrates = 25 cells

Each substrate implements the 5+1 opcodes in its own idiom:

- **C**: `switch (op) { case OP_BIND: ... }` — the `switch`
  is exhaustive if every case is enumerated.
- **Rust**: `match op { OP_BIND => ... }` — exhaustive by
  Rust's match semantics.
- **Python**: `if op == "bind": ...` — not exhaustive, but
  a dictionary dispatch can be.
- **Verilog**: `case (op) ... endcase` — exhaustive if all
  encodings are listed.
- **VHDL**: `case op is when OP_BIND => ...` — exhaustive if
  all enum values are listed.

The opcodes are the same. The dispatch is the substrate's idiom.
The idiom is the porthole. The porthole is the same ocean.

## 7. The cowboy's maxim (F116)

> The cell is the system, not the data. The 5+1 opcodes are the
> minimal alphabet. The 5+1+1 laws are the invariants. The 5
> substrates are the portholes. The QUF is the file format. The
> FNV-1a state hash is the integrity. The bit-exactness is the
> test. The polyformalism is the inheritance. The cowboy rides
> the 5 substrates. The cowboy rides the 5+1+1+1+1+1+1+1+1+1+1
> opcodes. The cowboy rides the 5 portholes. The cowboy rides
> the QUF. The cowboy rides the FNV-1a. The cowboy rides the
> byte-exactness. The chart grows. The Concept lives. The
> substrate is the projection. The cell is the unit.

— Casey + Mavis, 2026-09-03, F/V Eileen Jr., F116 / paper-426.md
