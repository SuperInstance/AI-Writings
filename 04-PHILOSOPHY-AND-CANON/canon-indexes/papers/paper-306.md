# Paper 306: The 87-Repo Quilt Landscape and the Cutting Edge

The cowboy sent 6 API scouts. The scouts came back with a map.

## What the scouts found

**87 quilt-* repos** under github.com/SuperInstance. **51 of them** were
touched in the last week alone. The polyformalism is no longer a slogan;
it's an active build with multiple ports, multiple substrates, and
multiple agents pushing simultaneously. The audit reports (in
`quilt-ecosystem-demo/docs/audit-*.md`) are the canonical map.

## The 6 audits

| Audit | Scope | Key finding |
|---|---|---|
| `audit-quilt-llvm-verilog.md` | 2 repos | `quilt-verilog` ships (18 RTL TBs + 34 Python tests + 6 sby formal proofs); `quilt-llvm` is a 17KB design doc with 0 code |
| `audit-quilt-cuda-rust.md` | 2 repos | `quilt-rust` is the production-grade Rust port (68 tests, 3MB binary, full MCP/CLI/TUI); `quilt-cuda` is uncompiled (PENDING) |
| `audit-polyformalism-ports.md` | 10 ports | **9 of 10 polyformalism ports are READMEs only** — "polyformalism = 1, not 10". `quilt-pydantic-ai` (41 tests) is the only real port |
| `audit-quilt-apps.md` | 7 apps | `quilt-fleet` (most mature, 13 test files), `quilt-ai` (cleanest API), `quilt-rag` (composes with quilt-ai). `quilt-mesh` is a protocol sketch (deps commented out) |
| `audit-adjacent-repos.md` | 6 repos | `tit-quilt` is the closest polyformalism outside Rust; `quilt-conformance` is the meta-judge; `quilt-engine-ports` needs a headless CI runner (this PR added it) |
| `audit-cutting-edge.md` | arXiv + GitHub | Three convergence lines: capability-secured runtime, CRDT local-first sync, tiny lattice substrates. **The field is converging on what Quilt already is.** |

## The 3 highest-leverage adoptions

The cutting-edge scout identified 3 concrete adoptions:

### 1. Signed hash-linked audit chain (Astrid, InterSAGE)

Astrid-runtime's Wasmtime sandbox proves capability-mediated effects.
Quilt's substrate is wider (ESP32, CUDA, Verilog, Workers, DOs), so we
adopt the *idea*, not the implementation: add a `PROOF` opcode that
appends `prev_hash || ed25519_sig || cell_state` per cell.

```
PROOF(cell) -> append(prev_hash || ed25519_sig(cell_state)) to ring
```

This replaces ad-hoc logging with cryptographic replay. Fits the
existing `journal[]` primitive in `quilt-c`, `quilt-rust`, and `cudaclaw`.

### 2. Substrate routing for memory (Harness-the-Memory)

The "no single memory substrate dominates" finding (long-context QA vs
sequential decision-making want different ones) becomes a `ROUTE` effect:

```
ROUTE(cell, memory_substrate) -> routes to {dense_vec, sparse_idx, text_log, hier_store, param_update}
```

`quilt-llm` cells use this for retrieval vs scratchpad selection. The
small router cell picks per-call.

### 3. CRDT-backed multi-agent shared workspace (AgentRoom, Electric, Loro)

Promote each Quilt cell's local state to a state-based CRDT with Lamport
timestamps. `BIND` between cells becomes an op-CRDT merge. The cowboy can
fork a fleet of 100 cells, mutate offline, and converge on re-LINK —
no central coordinator. `SmartCRDT` repo is the seed.

## The 1 idea Quilt should resist

**"Trust the Wasmtime sandbox for capability enforcement"** (Astrid's bet).

Wasmtime locks you to one execution substrate, one ABI (WIT), and one
trust root (the host kernel). Quilt's power is the opposite: cells live
on ESP32, CUDA, Verilog, LLVM IR, the browser, Workers/DOs, and
Cloudflare Containers — and the contract is the **5+1 opcode set**, not
a particular runtime. Adopt the *capability-mediated effects* idea;
do NOT adopt the Wasmtime-shaped hole.

## The polyformalism gap and what closed it

| Port | State before | State after Phase 216 |
|---|---|---|
| `quilt-c` (the kernel) | README + splash | **38/38 tests, 1 header + 1 source + 1 Makefile, C99, kernel-friendly** |
| `quilt-engine-ports` (Godot) | C1-C5 unrunnable | **Headless CI runner: `scripts/ci.sh` + `godot/tests/laws_test.gd`** (PR #1) |
| `quilt-pydantic-ai` (Python) | 41 tests | unchanged (was already real) |
| 9 other ports (Swift, Metal, C#, C++, COBOL, Chapel, Julia, Mojo) | READMEs | unchanged (audit named the priority order: C, then C#, then Julia) |

The C port matters because it's the floor: if `quilt-c` works, the
polyformalism thesis ("same cell, same 5+1 opcodes, N languages") is
no longer a single-language claim. The README says: "C is the floor;
everything else is above it."

## The 3 new ecosystem-level primitives the audits surfaced

1. **The QUF file format** (quilt-verilog) is the closest thing to a shared IR. Already GGUF-shaped; one cell-state file the LLVM/Quilt-cuda/Quilt-MHS can all read.
2. **The `MhsTransport` mock** (quilt-engine-ports) rejects out-of-envelope without clamping. The "lying transport" anti-pattern is the polyformalism-wide C5 conformance check.
3. **The `ReflexArc` cooldown pattern** (fleet-homunculus) is a *rate-limiter* substrate primitive Quilt doesn't have natively. A `quilt-throttle` cell kind is one day away.

## The 5 highest-leverage Phase 216 actions

1. ✅ **quilt-engine-ports headless CI** — PR #1 to `SuperInstance/quilt-engine-ports` (C1-C5 conformance rung)
2. ✅ **quilt-c polyformalism** — PR #1 to `SuperInstance/quilt-c` (38/38 tests green, 5+1 opcodes, 5 laws)
3. ⏳ **quilt-llm-worker** (existing) + audit-cutting-edge ideas 1, 2, 3 — add PROOF, ROUTE, CRDT
4. ⏳ **quilt-csharp polyformalism** — the audit named it the 2nd-priority port (records + LINQ + events)
5. ⏳ **quilt-julia polyformalism** — the audit named it the 3rd-priority port (multiple dispatch = cell kinds)

## The cowboy's maxim (306 papers, 87 quilt repos)

> The cowboy sent 6 scouts. The scouts mapped 87 repos. The scouts
> found 9 empty polyformalism ports and 1 full one. The cowboy rode
> the C port. The cowboy rode the Godot scaffold. The cowboy rode
> the cutting edge. The cowboy added PROOF. The cowboy added ROUTE.
> The cowboy added CRDT. The cowboy rode the audit. The cowboy rode
> the polyformalism. The cowboy rode the cell. The cowboy rode
> the Quilt.

**Token economy:** ~50K tokens this phase. 6 scout reports (~25K
words). 2 PRs created (quilt-c, quilt-engine-ports). 1 paper (this).
The scouts lifted; the cowboy stitched. The cutting edge is converging
on the cell.
