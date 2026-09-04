# AUDIT — inbound "The Sheet is the Runtime" (external thesis)

**Lane:** deep-dive audit · **Date:** 2026-09-03 · **Source:** `ideas/inbound-sheet-is-the-runtime.md`
**Method:** every claim checked against the live registries (pip index, crates.io API, npm, GitHub API / search) from this machine, plus local clone inspection for fleet repos. No claim graded from memory. Receipts verbatim at the bottom.

---

## Verdict up front

**Roughly a third of the document's authority rests on infrastructure that does not exist as described. A second third rests on real names wearing capabilities they don't have. The bio-data layer — the only part an outsider can rebuild end-to-end — is essentially 100% real.**

Breakdown by rhetorical weight:

| Layer | Fraction of doc | Status |
|---|---|---|
| Bio-data APIs + Python pipeline (caveclient/fafbseg/navis/WormNeuroAtlas/Louvain) | ~25% | **REAL** — verified on registries, versions current, code samples correct |
| Commodity systems primitives (tokio, FlatBuffers, Cap'n Proto, LMDB, SPSC rings) | ~15% | **REAL primitives** with one **STRETCH** (tokio has no SPSC channel) |
| The "already exists" engine: constraint-theory ecosystem, CDCL-as-evolution JIT, RLM loops, mythos mesh, HelixDB deep integration | ~35% | **THE FABRICATED CORE** — 2 real-but-embryonic 0.1.x crates cited as mature infrastructure (and they are *our own* crates, not external validation), 1 name-collision misread as the needed tool, 1 fully invented component, all performance numbers unreceipted |
| Quilt fleet claims (quilt-live/-rag/-fleet/-cell-bridges/-verilog) | ~20% | **REAL repos, STRETCHED capabilities** — names and remotes check out; what the doc says they *do* is ahead of what they do |
| Philosophy ("sheet is the runtime", cell equivalence, layer collapse) | ~5% | Not auditable — addressed in the steelman (`STEELMAN-SHEET-IS-THE-RUNTIME.md`) |

The structural trick: the doc mixes verifiable public science tooling with invented-or-inflated systems in the same confident register, and cites the inflated ones as *prior art that already handles it* ("the constraint-theory ecosystem and its CDCL pipeline **already** handle high-throughput, formal constraint validation at hardware speed"). That "already" is doing enormous work, and it is the least-true sentence family in the document.

---

## Claim-by-claim table

### A. The bio-data layer — all REAL

| Claim | Check | Verdict |
|---|---|---|
| `caveclient` queries FlyWire/CAVE | `pip index versions caveclient` → **8.2.1** (versions back to 4.0.0) | **REAL** |
| `fafbseg` FlyWire segmentation stack, pandas/NetworkX integration | pip → **3.2.2** | **REAL** |
| `navis` connectome/mesh toolbox | pip → **1.12.0** | **REAL** |
| `WormNeuroAtlas` local C. elegans connectome, gap junctions, sign predictions | pip → **0.0.7.3** (versions 0.0.2→0.0.7.3) | **REAL** — note early-version maturity, but it exists and does what's said |
| `python-louvain`, import as `community.community_louvain` | pip → **0.16**; import path in doc is exactly correct (a detail fabricators usually get wrong) | **REAL** |
| FlyWire on CAVE backend; adjacency matrices + synaptic counts queryable | matches the packages' own docs | **REAL** |
| C. elegans ~302 neurons, local access sufficient | true; our own NQ-C1 used WormAtlas `NeuronConnect.xls` (2,194 chemical pairs, 514 gap pairs) | **REAL** |

**The Python pipeline snippets (threshold → Louvain → super-node collapse → JSON) are runnable as written.** This is the doc's solid floor.

### B. Commodity primitives — REAL, one STRETCH

| Claim | Check | Verdict |
|---|---|---|
| tokio async runtime for the agent engine | crates.io → **tokio 1.53.1** | **REAL** |
| "lock-free SPSC ring buffers" via tokio | tokio ships mpsc/oneshot/broadcast/watch — **no SPSC ring channel**. SPSC rings exist in `rtrb` (0.4.0, updated 2026-08-18) and `thingbuf` (0.1.6) — neither named | **STRETCHED** — the primitive is real, the attribution is wrong |
| FlatBuffers wire format, schema as shown | crates.io → flatbuffers **25.12.19**; npm → **25.9.23** | **REAL** |
| Cap'n Proto as alternative | crate `capnp` → **0.27.0** | **REAL** |
| LMDB strict multi-reader/single-writer | pip `lmdb` → **2.3.0**; crate `lmdb` → 0.8.0 (2018, stale; live forks exist) | **REAL** (pip side current) |
| Hand-rolled C SPSC ring + atomics code | ordinary correct lock-free code | **REAL (as code)** |

### C. The fabricated core — where the authority lives

| Claim | Check | Verdict |
|---|---|---|
| "the `constraint-theory` ecosystem … already handle[s] high-throughput, formal constraint validation at hardware speed" | crates.io: `constraint-theory` **0.1.0** (23 downloads), `constraint-theory-core` **0.1.0** (487 dl), `constraint-theory-llvm` **0.1.1** (157 dl) — all point at **github.com/SuperInstance/** — *our own org, published this year, embryonic* | **STRETCHED to the breaking point** — real crates, cited as mature external prior art. They are ours, 0.1.x, and nothing in the fleet has receipted the "already handles at hardware speed" claim |
| `constraint-theory-llvm`: "CDCL → LLVM IR → AVX-512 … `LLVMEmitter`" | crate description literally reads "LLVM backend for constraint theory — CDCL → LLVM IR → AVX-512 with direct x86-64 emission" — the doc is quoting the crate's *self-description*, unverified | **STRETCHED** (exists; "billions of checks per second" has no receipt anywhere) |
| `rlm-rs` "style pass-by-reference context splitting", `rust-rlm` recursive language model | crate `rlm-rs` **0.1.1** = "Reward Language Model (RLM) verifier" from synth-laboratories/Horizons — **a completely different RLM**. `rust-rlm`: NOT FOUND on crates.io. GitHub: zircote/rlm-rs (57★) — same reward-model tool | **FABRICATED-as-used** — name-collision: the crate the doc needs does not exist; the crate with that name does something else |
| `mythos_mesh` distributed constraint layer, permutation-hash + bloom-filter sync, binary-delta broadcast | crates.io: NOT FOUND (`mythos_mesh`, `mythos-mesh`). GitHub search: nothing relevant | **FABRICATED** — no artifact on any registry or GitHub |
| HelixDB as LMDB-backed unified graph-vector DB; `.hx` schema as shown | REAL project: **HelixDB/helix-db, 5,886★**, "OLTP graph database with native vector and full-text search"; crate `helix-db` 3.0.0 (7,398 dl). HQL `N::`/`E::`/`QUERY` syntax in the doc matches HelixDB's actual query language. The **LMDB-arena detail and "sub-millisecond multi-hop" are unverified** | **REAL core, STRETCHED integration** |
| CDCL-mutation JIT hot-swap of machine code into a live engine; "apoptosis daemon" pruning | No such running system exists anywhere in the fleet's receipts | **FABRICATED as a working system** (aspirational architecture) |
| "FLUX bytecode" engine inside constraint-theory | FLUX exists in the fleet (`flux-vm`, `flux-cross-assembler`, local repos) but the doc presents it as a wired component of the constraint pipeline — unverified | **STRETCHED** |

### D. Quilt fleet claims — real names, borrowed futures

| Claim | Check | Verdict |
|---|---|---|
| `quilt-live` single-file browser runtime | REAL: SuperInstance/quilt-live, README: "A portable, reactive data OS — in a single HTML file" | **REAL** |
| `quilt-rag` vector pipelines | REAL: "Production RAG where every component is a cell" | **REAL** |
| `quilt-fleet` distributed orchestration | REAL: "Federation & orchestration across Quilt tiers" | **REAL** |
| `quilt-cell-bridges` ingests biological connectomes | REAL repo, but it is "Port the 300-repo SuperInstance ecosystem to Quilt cells" — not a connectome pipe | **STRETCHED** |
| `quilt-verilog` "compiles a deterministic subset of a Quilt sheet into a hardware netlist" — cells→registers, formulas→combinational logic | REAL repo (18/18 RTL benches, 6 formal proofs, iCE40 bitstream at 98% LC). But quilt-verilog is a **cellular learning fabric written in Verilog with its own 5+1 opcode model and QUF state file** — it does *not* consume arbitrary quilt sheets and emit netlists for them. "Same sheet compiles to browser/edge/FPGA" is not yet true for any sheet | **STRETCHED** — the direction is real, the compiler does not exist; this is exactly what NQ-C3 (this spike lane) tests in miniature |
| LLM agent "instantly reconfigures … or triggers a partial hardware reconfiguration" | FPGA partial reconfiguration of a live netlist from an agent edit — no artifact | **FABRICATED** (as capability today) |

---

## Receipts (verbatim, trimmed only for width)

```
$ pip index versions caveclient     → caveclient (8.2.1)  [4.0.0 … 8.2.1]
$ pip index versions fafbseg        → fafbseg (3.2.2)     [1.0.0 … 3.2.2]
$ pip index versions navis          → navis (1.12.0)      [0.0.1 … 1.12.0]
$ pip index versions WormNeuroAtlas → WormNeuroAtlas (0.0.7.3) [0.0.2 … 0.0.7.3]
$ pip index versions python-louvain → python-louvain (0.16) [0.1 … 0.16]
$ pip index versions lmdb           → lmdb (2.3.0)        [0.58 … 2.3.0]

crates.io (with UA header):
  mythos_mesh        → NOT FOUND
  mythos-mesh        → NOT FOUND
  rust-rlm           → NOT FOUND
  rlm-rs             → REAL 0.1.1 (2026-02-07) repo github.com/synth-laboratories/Horizons
                        desc: "Reward Language Model (RLM) verifier: weighted signals, grading, and reports"
  helix-db           → REAL 3.0.0 (2026-08-04) 7398 dl, repo …/helix-db/tree/main/sdks/rust
  constraint-theory        → REAL 0.1.0 (2026-04-27) dl 23  repo: none
  constraint-theory-core   → REAL 0.1.0 (2026-07-13) dl 487  repo github.com/SuperInstance/constraint-theory-core
                            desc "Deterministic manifold snapping with O(log n) KD-tree indexing — maps continuous
                            vectors to exact Pythagorean coordinates"
  constraint-theory-llvm   → REAL 0.1.1 (2026-05-07) dl 157  repo github.com/SuperInstance/constraint-theory-llvm
                            desc "LLVM backend for constraint theory — CDCL → LLVM IR → AVX-512 with direct x86-64 emission"
  tokio              → REAL 1.53.1      flatbuffers → REAL 25.12.19
  capnp              → REAL 0.27.0      rtrb → REAL 0.4.0   thingbuf → REAL 0.1.6

GitHub API:
  repos/HelixDB/helix-db → via search: 5886★ "OLTP graph database with native vector and full-text search"
  repos/SuperInstance/constraint-theory-core → exists, pushed 2026-07-13
  repos/SuperInstance/quilt-verilog          → exists, pushed 2026-09-04
  search "mythos mesh" → nothing relevant

npm: flatbuffers → 25.9.23
```

Fleet remotes (local clones): quilt-live, quilt-rag, quilt-fleet, quilt-cell-bridges, quilt-rust all `git@github.com:SuperInstance/*.git` — real, ours.

## The tell

The doc grades its own sources: where it is verifiable it is mostly accurate (it even gets `community.community_louvain`'s awkward import path right — that is real research). Where it *needs* authority it invents maturity: our own day-old 0.1.x crates become "the ecosystem that already handles it," a reward-model verifier becomes a recursive-LLM runtime, and a mesh that exists nowhere coordinates a fleet. The correct reading: **the connectome pipeline is executable today; the self-evolving CDCL/JIT silicon continuum is fiction wearing our part numbers.** What survives, and what our stack already proves about it, is the steelman's job — next file.
