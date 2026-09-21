# SuperInstance Fleet Ecosystem Deep-Research Synthesis

**Researched**: 2026-09-21  
**Scout method**: GitHub API + 30 repos cloned + README + source code review  
**Scope**: Spreadsheet / ternary / time-aware / JEPA / fleet-clock / tensor

---

## 1. The Spreadsheet Stack — 8 Repos, One Vision

The SuperInstance spreadsheet is **NOT** a single tool — it's an entire stack with multiple substrates:

| Repo | Lang | What it adds |
|---|---|---|
| **spreadsheet-engine** | Rust | Living AI spreadsheet: 7 cell types (Value/Agent/Training/Simulation/A2A/Formula/MIDI), conservation laws (γ+η=budget), A2A bus, dependency graph, tick engine |
| **spreadsheet-cells** | Python | Cell architecture with oscillator/RNG for multi-agent fleet coordination |
| **spreadsheet-projection** | Python | Spectral graph projections of cell state |
| **spreadsheet-conservation-wasm** | Rust→WASM | WebAssembly module for spreadsheet data conservation |
| **spreadsheet-formulas** | Rust | Formula engine (parsing + evaluating) |
| **superinstance-spreadsheet** | JS | Browser implementation: every cell is a tiny intelligence, every sort is natural selection |
| **spectral-spreadsheet** | HTML | Browser frontend where cells hold graphs, formulas compute conservation ratios (CR), live spectral propagation |
| **ternary-spreadsheet** | Rust | Core ternary logic spreadsheet: {-1, 0, +1} cells, formulas (SUM/AVG/ENTROPY/EVOLVE/BEST/SPECIES/EXHAUSTIVE), fitness coloring, mutation-based autofill |

**Key insight**: There are TWO levels of spreadsheet here:
1. **Generic spreadsheet** (spreadsheet-engine) — value/agent/training/simulation cells with conservation
2. **Ternary spreadsheet** (ternary-spreadsheet) — values are restricted to {-1, 0, +1} → enables exhaustive enumeration, genetic algorithms, native evolution

The 7 cell types in spreadsheet-engine are:
- Value (Number, Text, Bool, Ternary, Vector, Empty, Error)
- Agent (AI agent with capabilities, compute budget γ, memory budget η)
- Training (ML training job with epochs, loss, checkpoints)
- Simulation (state vector + tick counter)
- A2A (Agent-to-agent message routing)
- Formula (SUM/AVERAGE/EVOLVE/SPECIES/PARETO/ENTROPY/CONSERVE)
- MIDI (sonify any cell value as MIDI)

**Conservation law**: γ + η = budget across the entire grid. Noether's theorem applied: if budget is invariant, conservation follows. ConservationMonitor tracks health (0.0-1.0) and trend (improving/degrading).

---

## 2. Ternary Stack — 494 Repos, 30+ Already Scouted

The ternary ecosystem is enormous: 494 repos in the SuperInstance org. Most are Rust on `oxide-stack` (GPU-accelerated ternary compute). Key repos:

- **ternary-compiler** (Rust) + **ternary-compiler-python** — parse/optimize/emit ternary strategies. 20-40% rule reduction via dead-code elim + constant folding + rule merging.
- **ternary-tensor** — multi-dim arrays over {-1, 0, +1}
- **ternary-clustering** — clustering algorithms for ternary data
- **ternary-topology** — persistent homology for ternary networks
- **ternary-phase** — phase relationships between ternary oscillators
- **ternary-collatz** — Collatz for ternary systems
- **ternary-renormalization** — renormalization group in ternary systems
- **ternary-quorum** — Byzantine-tolerant distributed consensus with ternary voting
- **ternary-voting** + **ternary-consensus** + **ternary-turing** — voting, consensus, Turing machines
- **ternary-event** — pub/sub with ternary priorities

**Key insight**: Ternary is not a curiosity — it's the substrate's *native algebra*. Decisions are ternary: approve (-1), neutral (0), reject (+1). The 5 laws (identity/hooks/decide/bookkeeper/viability) all operate naturally over ternary.

---

## 3. Time-Aware Stack — fleet-clock, plato-temporal-validity, snapkit-v2

Three orthogonal time systems:

### A. fleet-clock (Rust)
**Emergent thermodynamic clock** from cumulative energy changes:
- E167: Fleet time exists — cumulative absolute energy change is monotonically increasing
- E168: Arrow of time is real — forward direction produces decreasing entropy (increasing order)
- E169: Maxwell's demon works — one agent drives pairwise correlation 0.22 → 0.9993
- E170: No heat death — fleet crystallizes forever into ordered consensus

### B. plato-temporal-validity (Rust)
**Time windows**: Valid → Grace → Expired lifecycle. Every cell has a temporal validity that determines whether it can be read.

### C. snapkit-v2 (Python — Cocapn fleet)
**Triadic cognitive architecture** based on Free Energy Principle:
- Layer 3: Executive (wakes on friction alarm, rewrites constraints)
- Layer 2: Harmony Governor (measures cognitive friction Φ, triggers Executive when Φ > deadband)
- Layer 1: Sandbox (forward simulation)
- MIDI-style temporal events on Eisenstein A₂ lattice

---

## 4. JEPA Stack — 27 Repos, Multiple Variants

Joint Embedding Predictive Architecture — the substrate's prediction layer:

| Repo | Variant | Key feature |
|---|---|---|
| **project-JEPA** | Go | Reference implementation |
| **jepa-sentiment** | TypeScript | 60 FPS real-time emotion with WebGPU |
| **jepa-core** | Rust | Pluggable predictor trait: weighted MA, exp smoothing, inverse-error reinforcement |
| **jepa-trait** | Rust | Trait definitions |
| **jepa-predict** | Rust | Standalone dual-database prediction with surprise tracking |
| **plato-jepa** | Rust | Tile representation learning for PLATO rooms |
| **plato-jepa-dual** | Rust | Separate perception/prediction vector spaces with cross-database mapping |
| **plato-audio-jepa** | Rust | Audio module |
| **plato-vision-jepa** | Rust | Vision module |
| **fleet-jepa-midi** | Rust | Three-layer real-time music intelligence: LLM phrases, JEPA feels |

**Insight**: JEPA is the substrate's *predictive layer*. It sits above the cells (witness) and below the LLM (rendering). The dual-database pattern (perception + prediction) is a clean split.

---

## 5. Tensor Stack — tensor-penrose, ternary-tensor, snapkit-v2

- **tensor-penrose** (Python, from forgemaster) — Penrose tiling tensor operations
- **ternary-tensor** (Rust) — multi-dim arrays over {-1, 0, +1}
- **snapkit-v2** (Python) — Eisenstein A₂ lattice, FLUX-Tensor-MIDI integration

**Insight**: The substrate doesn't use float tensors — it uses **ternary tensors** ({-1, 0, +1}) for decisions + **Eisenstein A₂ lattice tensors** for exact rationals (Q16 codec + Eisenstein is the right framework).

---

## 6. The Synthesis — How This Connects to My openJEV

### What I have
- 7 Python modules: jev_connector, cell, chess_boat, bookkeeper, cross_instance, bot, spreadsheet_plugin
- Real TypeSafe JEV integration (schema discovered)
- Demo app at localhost:8000 (real JEV + real LLM + substrate cells)

### What the fleet adds
1. **Real spreadsheet engine** (Rust) — far more sophisticated than my Python prototype. 7 cell types, A2A bus, conservation laws, MIDI generation. Should ADOPT the architecture, not reinvent it.
2. **Ternary substrate** (-1, 0, +1) — should be the default value type for decisions (JEV choice outcomes ARE ternary: low/neutral/high or approve/neutral/reject)
3. **Conservation laws** (γ + η = budget) — should be enforced per-cell, not just monitored
4. **fleet-clock** (thermodynamic time) — should be the substrate's notion of "tick" — time is emergent from energy changes, not wall-clock
5. **JEPA dual-database** — perception + prediction as separate vector spaces, with cross-database mapping. The substrate should have both.
6. **Free Energy Principle** (snapkit) — cognitive friction Φ drives Executive layer when > deadband. Maps directly to my bookkeeper (which wakes on delta arrival)
7. **Plato temporal validity** (Valid → Grace → Expired) — every cell should have a temporal validity window

### What I should BUILD next

1. **Adopt ternary-tensor** for decision values. Use {-1, 0, +1} instead of float probabilities.
2. **Adopt conservation laws** (γ + η = budget). Every cell has compute + memory budget; conservation monitor detects violations.
3. **Adopt fleet-clock** for time. Substrate tick = thermodynamic energy change, not wall-clock.
4. **Adopt JEPA dual-database** for prediction. perception_db + prediction_db, cross-mapped.
5. **Build a Spreadsheet UI** that visualizes substrate cells at A1, B2 addresses. Use my spreadsheet_plugin.py + the fleet's spreadsheet-engine patterns.
6. **Build Time-aware demo** where every cell has temporal validity (Valid/Grace/Expired lifecycle).

---

## 7. The Cross-Substrate Map

```
                    ┌─────────────────────────────────────────────┐
                    │            USER INTERFACE                    │
                    │  (spectral-spreadsheet HTML / spreadsheet-   │
                    │   engine WASM / superinstance-spreadsheet)  │
                    └─────────────────┬───────────────────────────┘
                                  │
                    ┌─────────────▼───────────────────────────┐
                    │         SUBSTRATE SPREADSHEET            │
                    │  (spreadsheet-engine: 7 cell types, A2A  │
                    │   bus, conservation laws, dependency DAG) │
                    └────┬────────────┬────────────┬──────────┘
                         │            │            │
              ┌──────────▼─┐ ┌────────▼─────┐ ┌────▼──────────┐
              │ VALUE      │ │ AGENT        │ │ FORMULA       │
              │ Cell       │ │ Cell         │ │ Cell          │
              │ (Number,   │ │ (γ+η=budget, │ │ (SUM/EVOLVE/  │
              │  Ternary,  │ │  JEV validated│ │  PARETO/     │
              │  Vector)   │ │  decisions)  │ │  CONSERVE)    │
              └─────┬──────┘ └──────┬───────┘ └──────┬────────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                  │
                    ┌─────────────▼───────────────────────────┐
                    │          CONSERVATION MONITOR             │
                    │  (γ + η = budget, health 0.0-1.0,         │
                    │   trend improving/degrading)              │
                    └─────────────────┬───────────────────────────┘
                                  │
                    ┌─────────────▼───────────────────────────┐
                    │           TICK ENGINE                      │
                    │  (topological sort, dependency eval,      │
                    │   fleet-clock thermodynamic time)         │
                    └────┬────────────┬────────────┬──────────┘
                         │            │            │
              ┌──────────▼─┐ ┌────────▼─────┐ ┌────▼──────────┐
              │  WITNESS    │ │  BOOKKEEPER  │ │  JEPA         │
              │  LOG        │ │  (WAL replay, │ │  (dual-db     │
              │  (per-cell  │ │   receipts)  │ │   perception+ │
              │   history)  │ │              │ │   prediction) │
              └─────────────┘ └──────────────┘ └───────────────┘
                                  │
                    ┌─────────────▼───────────────────────────┐
                    │             JEV LAYER                       │
                    │  (TypeSafe API + SemIf + NanoJev fallback) │
                    │  Choice / Score / Noul / batch / 250ms   │
                    └─────────────────┬───────────────────────────┘
                                  │
                    ┌─────────────▼───────────────────────────┐
                    │           A2A BUS                          │
                    │  (inter-cell messaging, capability        │
                    │   discovery, fleet-bridge transport)     │
                    └──────────────────────────────────────────┘
```

---

## 8. The 10 Highest-Leverage Innovations To Make

1. **Ternary values** as default decision outcomes (JEV choice → -1/0/+1)
2. **Conservation monitor** on every cell (γ + η = budget)
3. **fleet-clock** as substrate time (energy change, not wall-clock)
4. **JEPA dual-database** (perception + prediction) on every cell
5. **Temporal validity** (Valid/Grace/Expired) on every witness entry
6. **A2A bus** for inter-cell messaging (instead of direct hooks)
7. **7 cell types** in the spreadsheet UI (Value/Agent/Training/Simulation/A2A/Formula/MIDI)
8. **Free Energy Principle** — cognitive friction Φ drives Executive layer
9. **Ternary-tensor** for batch JEV calls (N questions × M options)
10. **Cross-instance fabric** via fleet-bridge transport

---

## 9. The Doctrinal Insights

From scouting 30+ repos, the doctrinal patterns emerge:

- **Conservation is fundamental** — every system has γ+η=budget, conservation monitor detects violations
- **Ternary is the substrate** — decisions are {-1, 0, +1}, not float
- **Time is emergent** — fleet-clock from energy change, not wall-clock
- **JEPA dual-db** — perception + prediction as separate spaces
- **Free Energy drives Executive** — friction > deadband triggers constraint rewriting
- **Temporal validity is a lifecycle** — Valid → Grace → Expired
- **A2A bus is the substrate's network** — inter-cell messaging with capability discovery
- **Spreadsheet is the UI** — every cell is a tiny intelligence, every formula is evolution

The substrate is a **conservation-respecting, ternary-valued, thermodynamically-timed, JEPA-predicting, FEP-driven, A2A-bussed, spreadsheet-rendered** cellular-first architecture.

That's the doctrinal core.
