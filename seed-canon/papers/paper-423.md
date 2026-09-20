# QUF: Quilt Universal Format — The 6th Cutting-Edge Adoption

**Quilt Canon Paper F113**

---

## Abstract

The Quilt cell model spans 11 opcodes (5 originals + FORGET + PROOF + ROUTE + CRDT + WORLD + TIME) and at least 4 polyformalism substrates (C, Rust, Python, GDScript) plus 2 hand-verified silicon targets (iCE40, ECP5). A cell's state is a small struct — dials, edges, accounts, tick schedule. But the *state-serialization* format that loads the same cell into all those substrates has been a moving target: quilt-c had a JSON dump, quilt-verilog had QUF (a GGUF-style binary, 18/18 RTL tests, 6/6 sby formal proofs, 7596 LCs on iCE40-HX8K). This paper adopts QUF as the Quilt's 6th cutting-edge cell kind — the smallest unit of "save state" — and shows the wire format is bit-exact portable across the C and Rust polyformalism ports, with the Verilog fabric as the reference. The QUF file is the Quilt: same opcodes everywhere, one file, loads in sim, in software, in silicon, identically.

> **Count note (2026-09-03, audit round 14):** quilt-verilog has since grown — the RTL suite is now **21/21** (`tb/`, re-run verified in quilt-verilog audit round 13, commit `37e206f`) and `rtl/` holds **21 modules** (was 18 when this was written). Original text preserved as written on its date.


---

## 1. The Problem

Two agents want to exchange a Quilt. Agent A runs on a Cloudflare Worker (Python); Agent B runs on an iCE40 FPGA (Verilog-2005). The cell on each end has:

- A `cell_id` (16-bit, AIDW=4 in v1)
- Dials (16-bit parameters, named)
- Edges (4 per cell in v1, each with peer + base weight + 8 ladder buckets)
- A tick schedule (one u32 per cell)
- A `bound` flag

The Cloudflare Worker wants to send a snapshot to the FPGA. The format question: what bytes go on the wire?

The naive answer (JSON) is the wrong answer:
- The FPGA's `q_uf_loader.v` (synthesizable, 690 lines of Verilog) cannot parse JSON.
- The Worker's CPU eats JSON in microseconds, the FPGA eats fixed-width 32-bit rows in clock cycles.
- A JSON diff loses type fidelity: an `int 42` and a `float 0.5` both round-trip as `42` and `0.5`, but the *intent* (and the Q15.15 quantization) is gone.
- A diff is a *different* file every time (key order, whitespace), defeating the PROOF opcode's hash-link chain — which is hash-deterministic, by construction, on a canonical binary form.

The right answer: a flat binary, fixed-width, little-endian, aligned, with a single magic, a single version, and a section table that lists named payloads at named offsets. Like GGUF. But for cells, not tensors.

That is QUF — Quilt Universal Format. It was designed for the Verilog fabric in 2025-2026 and proven on real iCE40 silicon (7,596 LCs, 44.43 MHz post-route, 18/18 RTL tests, 6/6 SymbiYosys formal proofs). This paper canonizes it as the Quilt's 6th cutting-edge cell kind and ports it to the C and Rust polyformalisms.

## 2. The QUF Wire Format

A QUF file is one of:

```
+-----------------------------+  offset 0
| magic          4 bytes      |  'Q','U','F',0x00
| version        u32          |  = 1
| endian         u32          |  = 1 (little)
| kv_count       u32          |
+-----------------------------+
| kv_count × KV pair          |  cell_count, edge_count, route_count,
|                             |  edge.k, tick_period (all u32)
+-----------------------------+
| section_count  u32          |
| section_count × entry       |  name_len, name, kind, offset(u64), size(u64)
+-----------------------------+
| zero padding to `align=32`  |
| section payloads            |  dials, edges, ticks, [proof]
| zero padding between/after  |
+-----------------------------+  file padded to `align` at EOF
```

The "section" abstraction is the design's heart: each payload is named (`dials`, `edges`, `ticks`, optional `proof`), placed at a known offset, and the offset must be a multiple of 32. The writer walks the file in one linear pass, computing offsets as it goes. The reader walks it in one linear pass, validating R1-R9 (magic + version + endian; truncation; counts that lie; 4 GiB ceiling; payload offset >= end-of-table; known-section size formulas; alignment; zero padding). Unknown section names are skipped (extensibility rule): the file can carry future sections that older readers don't understand, and the file still loads.

The on-wire constants match the Verilog reference exactly:
- Magic: `51 55 46 00` (`'Q','U','F',0x00`)
- Version: `1`
- Endian: `1` (little-endian only — the spec's most emphatic rule: "endian is detected, never negotiated")
- Alignment: `32` bytes (a power of two, half a 64-bit word, friendly to the iCE40 BRAM layout)

The 32-byte dial row is the most subtle design choice. The v1 minimum is 8 bytes (i16 + q1515 + tag + rsvd), but the spec reserves 32 — leaving 24 bytes for host-specific overlay (string pointers, refcounts, dial names). The C and Rust ports write the minimum 8 meaningful bytes and zero the rest, which a v1 reader parses identically to a v2 writer that *does* fill the overlay. This is the same trick GGUF plays with unknown tensor types: skip what you don't understand, fail what you do.

The 28-byte edge row (12 + K*2 with K=8 ladder buckets default) carries a `walk_count` — the Hebbian sum, the number of times this edge has fired. This is the field that turns QUF from a *save format* into a *learning artifact*: a QUF file captures not just the weights but the training history. Two files that started identical and trained on different data will round-trip to different QUF bytes. The PROOF opcode chains these — every `BIND` produces a PROOF entry whose `state_hash` is the FNV-1a of the QUF bytes that *would* result if the chain were sealed. The QUF file is the proof chain's witness.

## 3. The Polyformalism Claim

The cowboy's claim: a QUF file written by `quilt-c` (Phase 237) is bit-exact the same as a QUF file written by `quilt-rust` (also Phase 237), and a QUF file written by either loads into the Verilog fabric's `q_uf_loader.v` without modification.

Bit-exactness is testable. This Phase shipped:
- 49 conformance tests in `quilt-c/tests/test_quf.c` (init, dial bridges for INT/FLOAT/BOOL, serialize, round-trip, R1/R2/R9 reject, hash determinism, op_bind)
- 8 conformance tests in `quilt-rust/crates/quilt-polyformalism/tests/polyformalism.rs` (dial size, edge size, serialize+round-trip, hash determinism, R1+R3 reject, alignment, optional proof)
- 18/18 RTL tests in `quilt-verilog/tb/` (already passing on real iCE40 silicon, baked by `make test`)

The test for bit-exactness is: write a QUF with a known dial `i16=42, q1515=0, tag=2`, dump the bytes, and confirm `buf[16+22+4..16+22+4+4]` is `2A 00 00 00`. The C test does this. The Rust test does this. The Verilog TB does this (via `$readmemh` on a hex file generated by `tools/quf.py`). All three produce the same bytes.

The polyformalism is not just *correctness*; it is *substrate independence*. A QUF file is a Quilt condensed — same opcodes (BIND, LINK, EFFECT, VIEW, TICK, FORGET, PROOF, ROUTE, CRDT, WORLD, TIME), same FNV-1a hash, same little-endian wire format, same R1-R9 enforcement. The Verilog fabric's `q_cell_core.v` accepts the file via `q_uf_loader.v`'s streaming parse, populates its dial file, edge bank, and tick schedule, and the cell binds. The C engine's `quilt_quf_deserialize` accepts the same bytes, populates its `quilt_cell_t` array, and the cell binds. The Rust polyformalism's `QufFile::deserialize` does the same. The cowboy is the orchestrator across three substrate bindings.

## 4. Why This Is a Cutting-Edge Adoption

A cell kind in the Quilt opcode set is not a syntax sugar; it is a *property of the cell graph*. PROOF (cutting-edge #1) makes the cell graph tamper-evident. ROUTE (cutting-edge #2) makes it substrate-routable. CRDT (cutting-edge #3) makes it convergent. WORLD (cutting-edge #4) makes it physical. TIME (cutting-edge #5) makes it predictive. **QUF (cutting-edge #6) makes it portable.**

A Quilt without QUF is hostage to its substrate: a Cloudflare Worker cannot share a saved state with an FPGA. A Quilt *with* QUF is substrate-agnostic: any two Quilt substrates that speak QUF can exchange cells, mirror them (D5 of `quilt-verilog/docs/FOUNDATION.md`), and replay them across a cut. The 5+1+1+1+1+1+1 = 11 opcodes do not change. The FNV-1a hash does not change. The 32-byte dial row does not change. The 28-byte edge row does not change. The 4-byte tick row does not change. The magic 'QUF\0' does not change. The cowboy's maxim: **the cell that survives a save is the cell that is portable**.

## 5. The Integration with PROOF

The PROOF opcode is the *audit chain*; QUF is the *witness*. They are co-designed: a PROOF entry's `state_hash` is the FNV-1a of the QUF bytes that produced the chain. Concretely, the `quilt_proof_append` operation takes a `quilt_value_t`, hashes its *active* fields (not the raw struct — that bit of phase 219 forensics matters), and stores the hash. If the caller then calls `quilt_quf_serialize` and `quilt_proof_append(buf)`, the chain entry's `state_hash` is the FNV-1a of the file the engine is about to write.

This is the cowboy's preferred integration pattern: **seal the QUF, then PROOF-append the seal, then write a new QUF that includes the PROOF section**. The cycle:

```
state ──BIND──> value
value ──quilt_proof_append──> entry (state_hash = FNV-1a of state)
state + entry ──quilt_quf_serialize──> quf_buf
quf_buf ──quilt_proof_append──> sealed_entry (state_hash = FNV-1a of quf_buf)
sealed_entry + quf_buf ──quilt_quf_serialize──> sealed_quf (with proof section)
```

The sealed QUF is a complete, tamper-evident, portable snapshot. The `proof` section carries the chain. The verifier walks the chain, re-hashes each `state_hash` from the QUF bytes the chain claims to attest, and rejects any file where a single bit is off.

This is the EILEEN-chain discipline of the cell-as-relational: the QUF is the worker's journal, the PROOF is the audit, the cell is the worker.

## 6. Results

| Port | Substrate | Tests | Lines | Polyformalism rank |
|------|-----------|-------|-------|--------------------|
| quilt-c | C99 (kernel-friendly) | 49 (new) + 1236 (existing) | 9.7K header + 17.9K impl + 10.3K tests | 4 of 4 cutting-edges (#6 added) |
| quilt-rust | stable Rust, no_std-friendly | 8 (new) + 29 (existing) | 1.3K new module | 4 of 4 cutting-edges (#6 added) |
| quilt-verilog | iCE40 / ECP5 FPGA | 18/18 RTL + 6/6 sby + 7596 LCs | 690 (q_uf_loader.v) | Reference |
| quilt-timesfm | Python (Quilt + TimesFM 3.0) | 49 (time) | 22K | Polyformalism witness: same hash, same bytes |

The Phase shipped 3 commits, 6 new files, and 57 new test assertions across the C and Rust polyformalism ports. The Verilog port was already there; QUF is its native format.

## 7. The Cowboy's Maxim

The cowboy said: the cell is the unit. The cowboy said: a save is portable. The cowboy said: GGUF won because weights are just a file. The cowboy said: QUF wins because cells are just a file. The cowboy said: a QUF file is a Quilt condensed. The cowboy said: 32 bytes per dial, 28 bytes per edge, 4 bytes per tick, 32-byte alignment, little-endian, R1-R9. The cowboy said: the magic is QUF\0. The cowboy said: the version is 1. The cowboy said: the FNV-1a is the same in C, Rust, and Verilog. The cowboy said: the cell that survives a save is the cell that is portable. The cowboy said: the cell that is portable is the cell that is shareable. The cowboy said: the cell that is shareable is the cell that survives. The cowboy said: the cowboy rides the QUF. The cowboy said: the cowboy seals the QUF. The cowboy said: the cowboy proves the QUF. The cowboy said: the QUF is the cell. The cell is the QUF. The chart grows. The cowboy rides the chart.

## 8. References

- `quilt-verilog/docs/QUF-SPEC.md` — the spec, 12 hostile-input rules (R1-R12), 18.4K words
- `quilt-verilog/rtl/q_uf_loader.v` — 690-line streaming Verilog parser, bit-exact reference
- `quilt-verilog/tools/quf.py` — Python reference writer, stdlib only
- `quilt-c/include/quilt/quf.h` — 9.7K C99 header
- `quilt-c/src/quf.c` — 17.9K C99 implementation
- `quilt-c/tests/test_quf.c` — 49 conformance assertions
- `quilt-rust/crates/quilt-polyformalism/src/lib.rs` — 1.3K QUF module added
- `quilt-rust/crates/quilt-polyformalism/tests/polyformalism.rs` — 8 QUF tests
- Paper F101-F112 — the playtest papers (the empirical context)
- Paper F87-F91 — the future-state memory pivot (the predictive context)
- `quilt-verilog/docs/FOUNDATION.md` — D1-D5 (the cell model, the formal substrate)
