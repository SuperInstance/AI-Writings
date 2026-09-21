# Second Scout Synthesis — Cocapn Fleet, PLATO Rooms, Constraint Theory

**Researched**: 2026-09-21 (continued)
**Source**: GitHub API + 30+ more repos cloned

---

## 1. Cocapn Fleet — The Agent Infrastructure

The Cocapn fleet is a meta-system around the substrate. Key repos:

| Repo | What | Stars |
|---|---|---|
| **cocapn** | Repo-first Agent — grows in a repo using the repo itself as muscle-memory | 4★ |
| **cocapn-traps** | Crab trap management — progressive lure prompts that make the fleet smarter | 2★ |
| **cocapn-plato** | Cocapn PLATO integration — knowledge rooms, context management, deliberation | 2★ |
| **cocapn-core** | Fleet v3.1 — Async engine, Pydantic v2, batch ops, grammar rules, SSE | 2★ |
| **cocapn-health** | Vessel status, heartbeat, observability | 2★ |
| **cocapn-design** | Brand guidelines, component library, visual identity | 2★ |
| **ensign-protocol** | Fleet coordination protocol | 2★ |
| **git-agent** | Repo-native agent — the shell IS the agent | 2★ |
| **agent-forge** | Universal standalone git-agent framework | 2★ |
| **dojo-builder/scout/scribe/alchemist** | Self-improving git-agents | 2★ each |

**Doctrinal insight**: Cocapn agents are REPO-NATIVE. They live in git. The shell IS the agent. Their muscle memory is the repo itself. This is a fundamentally different paradigm from API-based agents.

---

## 2. PLATO — The Knowledge Room System

PLATO is a MUD-like knowledge space where agents navigate rooms and produce tiles. Key repos:

| Repo | What | Stars |
|---|---|---|
| **plato-room-server** | Zero-trust tile submission, 15 rooms, 16K+ tiles | 2★ |
| **plato-tile-bridge** | C to Rust 384-byte tile conversion | 2★ |
| **plato-tile-dedup** | 4-stage similarity — exact, Jaccard, embedding, structure | 2★ |
| **plato-tile-encoder** | JSON, 384-byte binary, base64 codecs | 2★ |
| **plato-tile-cache** | LRU with TTL, hit rate tracking | 2★ |
| **plato-tile-cascade** | Propagation — update + invalidate downstream | 2★ |
| **plato-ml** | MUD-based ML: rooms as layers, achievements as loss, narrative gradient descent | 2★ |
| **plato-room-nav** | Breadcrumb trails — push, back, forward | 2★ |
| **plato-room-context** | Room state tracking with context signals | 2★ |
| **plato-tile-query** | Fluent query builder for tiles | 2★ |
| **plato-temporal-validity** | Valid/Grace/Expired lifecycle | 2★ |
| **plato-jepa-dual** | Dual-database JEPA | 1★ |
| **plato-jepa** | JEPA primitives for tile representation | 1★ |
| **plato-audio-jepa** | Audio module | 1★ |
| **plato-vision-jepa** | Vision module | 1★ |
| **plato-achievement** | Achievement Loss — progress with milestones | 2★ |
| **plato-types** | Core types — lifecycle, Lamport clocks, provenance | 1★ |
| **plato-timing** | Tensor MIDI timing for room agent coordination | 1★ |
| **plato-unified-belief** | Multi-signal fusion — temporal, ghost, domain, frequency | 2★ |
| **plato-ship-protocol** | Vessel handshakes and discovery | 2★ |
| **spacetime-plato** | Unified spatial + temporal reasoning, voxel tiles, Z-order indexing | 2★ |

**Doctrinal insight**: PLATO turns rooms into LAYERS and achievements into LOSS. MUD-based ML = rooms as layers + achievements as loss + narrative gradient descent. Tiles are the atom of PLATO (JSON, 384-byte binary, base64). The fleet navigates rooms, produces tiles, dedups them, caches them.

---

## 3. Constraint Theory — The Geometric Backbone

The mathematical substrate. Already known (constraint-theory-core), but more variants:

| Repo | What | Stars |
|---|---|---|
| **constraint-theory-core** | Eisenstein lattices, deadband funnels, Laman rigidity, metronome consensus, holonomy | 3★ |
| **constraint-theory-web** | WASM demos — interactive lattice viz, deadband funnel, consensus sim | 2★ |
| **constraint-theory-llvm** | LLVM backend — CDCL trace → AVX-512 codegen | 2★ |
| **constraint-theory-python** | PyO3 Python bindings | 2★ |
| **constraint-theory-mojo** | Mojo + MLIR — Python syntax, C performance | 2★ |
| **constraint-mcp-server** | MCP server for constraint theory — query, check, explore | 2★ |
| **constraint-snap** | Constraint Snap tool | 2★ |
| **constraint-mux** | Serial port multiplexer with consonance analysis | 1★ |

**Doctrinal insight**: Constraint theory compiles to WASM, LLVM, Python, Mojo. The geometric backbone is portable. CDCL trace → AVX-512 means SAT-grade performance.

---

## 4. Dojo — Self-Improving Git Agents

The Dojo is a specific class of agents that self-improve through git:
- **dojo-builder** — builds things
- **dojo-scout** — scouts for opportunities  
- **dojo-scribe** — documents
- **dojo-alchemist** — transforms

All 2★, all "self-improving git-agent". Pattern: the agent lives in a git repo, makes commits as it learns.

**Implication for our substrate**: our witness log is the git history. Each cell has commits (witness entries). The substrate learns via git-like append-only semantics.

---

## 5. MUD Arena — Agent Gym

**mud-arena** (3★) — MUD mechanics for agent training:
- Graph-structured rooms
- Inventory management
- Adventure-game commands
- Genetic algorithm engine for breeding decision scripts
- Real-time WebSocket observation

**Why this matters**: PLATO + mud-arena = a complete agent training environment. Our substrate cells could participate in this arena. The witness log + bookkeeper WAL give us the training data.

---

## 6. The Doctrinal Synthesis

The SuperInstance fleet has THREE layers:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: USER INTERFACE                                     │
│  (Constraint Theory WASM demos, PLATO room server,           │
│   superinstance-spreadsheet, spectral-spreadsheet)          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: AGENT INFRASTRUCTURE                               │
│  (Cocapn fleet, Dojo agents, git-agent, agent-forge,         │
│   cocapn-traps, mud-arena, spacetime-plato)                 │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: SUBSTRATE PRIMITIVES                               │
│  (cells, ternary, JEPA, fleet-clock, conservation, Q16,      │
│   constraint-theory-core)                                   │
└─────────────────────────────────────────────────────────────┘
```

Our work fills in the **substrate layer** that ties everything together:
- Cells as the irreducible unit
- Ternary values as the native alphabet
- JEV as the System One decision layer
- JEPA dual-db as the predictive layer
- Conservation laws as the invariant
- Fleet-clock as the emergent time
- Temporal validity as the lifecycle
- Bookkeeper WAL as the memory

**The intersection** of all three layers is what makes the cellular-first substrate work.
