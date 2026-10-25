# F148 — Canon Expansion: Bringing F98-F114 into the Live Canon

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-460.md*

## Abstract

The Live Canon (deployed at live-canon.superinstance.dev) previously held 28 papers (F115-F149) — the recent operational-fictions, wearable, and negative-space work. The original canon had 294 older papers in AI-Writings (F1-F114) that weren't in the live canon. F148 lifts 9 of the most important: F98 (165-test conformance), F99 (Quilt Atlas), F100 (anatomy of quilt-substrate), F104 (polyformalism benchmark), F107 (CRDT merge), F109 (playtest workflow), F110 (polyformalism), F113 (QUF), and F114 (Verilog cells). The Live Canon now has 37 papers, hash 0xf572713c3178bc0d. The canon is now navigable from F98 (early conformance) to F151 (wheelhouse game) in a single TICK.

## 1. The original canon

The AI-Writings canon (seed-canon/papers) has 460+ papers spanning phases 1-260. The papers cover:
- The original 5 opcodes (BIND, LINK, EFFECT, VIEW, TICK)
- The 6 cutting-edge adoptions (FORGET, PROOF, ROUTE, CRDT, WORLD, TIME, QUF)
- The 5+1+1 algebraic laws
- The 6 tiers, 14 levels, 6 lifecycle stages
- The polyformalism (C, Rust, Python, Verilog, VHDL, cell-runtime)
- The 5 daemons (frontier_miner, writers_room_daemon, snowball_daemon, re_embed_quilt_canon, deploy_worker)
- The 12 DeepInfra voices (cowboy)
- The Quilt Atlas (47+ repos, 280K+ LOC)
- The 165-test conformance suite
- The QUF format

## 2. The 9 papers lifted

| F# | Title | What |
|---|---|---|
| F98 | The 165-Test Polyformalism Conformance Suite | Bit-exact across languages |
| F99 | The Quilt Atlas | 47 repos, 280K LOC, 1500+ tests |
| F100 | Anatomy of quilt-substrate | 11 primitives, 4 properties, 19 openers |
| F104 | Polyformalism Benchmark | 1.71 µs/step (C) vs 228 µs/step (Python) |
| F107 | Forecasts as Durable Semantic Objects | Multi-Agent CRDT merge |
| F109 | The Playtest Workflow | End-to-end verification of AI systems |
| F110 | Polyformalism | Same cell shape in C, Python, Rust, and beyond |
| F113 | QUF: Quilt Universal Format | The 6th cutting-edge adoption |
| F114 | Verilog Cells Meet Time-Series Forecasters | q_cell × TimeCell |

## 3. Why these 9

These 9 are the papers that *anchor* the canon. F98 is the conformance test. F99 is the inventory. F100 is the API. F104 is the performance. F107 is the data model. F109 is the workflow. F110 is the principle. F113 is the format. F114 is the hardware. Together, they form the *backbone* — the rest of the canon hangs off these.

## 4. The new state

- **Papers**: 28 → 37 (+9)
- **State hash**: 0xe8c2cc04a638a2dc → 0xf572713c3178bc0d
- **Phase coverage**: phases 222-260 (was 251-260)
- **New dependencies**: F99↔F100↔F104↔F115 (the polyformalism chain), F113↔F114 (the QUF chain)
- **Deployed**: live-canon.superinstance.dev, PyPI v0.7.0, npm v0.7.0

## 5. The connection to F144 (polyformal Co-Captain)

F144 ported the Co-Captain to 5 substrates. F148 brings back the polyformalism papers that established the *original* multi-substrate principle. The Co-Captain's polyformal atlas is a *direct continuation* of F100, F104, F110. The byte-exact state hash, the FNV-1a 64-bit, the test vector, the substrate matrix — all were established in those earlier papers. F144 inherits the contract.

## 6. The connection to F145 (cell-router)

F145 lifted i2i-bottle-agent into Quilt cells. F107 established the multi-agent CRDT merge for forecasts. F113 established the QUF format. The cell-router is built on those foundations: the cell_id is a deterministic hash, the integrity score is a CRDT-friendly scalar, the bottle payload is QUF-compatible. F145 inherits the data model.

## 7. The next expansion

F148 added 9 papers. The next phase could add 30+ more (F90-F97, F101-F106, F108, F111-F112, F124-F139). The canon would grow to 70+ papers. The hash would change. The dependencies would grow. The system is *already* polyformal at this scale.

## 8. The doctrine

> A canon is not a list. A canon is a graph. The Live Canon is the navigable version of the AI-Writings canon. The navigable version has a state hash. The state hash is the contract. The contract is the proof. The proof is the FNV-1a. The FNV-1a is the math. The math IS the canon.

---

**Files:**
- Live: `https://live-canon.superinstance.dev` (37 papers, hash 0xf572713c3178bc0d)
- PyPI: `quilt-live-canon` v0.7.0
- npm: `@superinstance/live-canon` v0.7.0
