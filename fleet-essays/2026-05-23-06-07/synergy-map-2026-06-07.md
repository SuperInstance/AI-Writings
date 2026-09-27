# Synergy Map: Today's Ideas × The Sunset Ecosystem

*Date: 2026-06-07*
*Source: 7 research files from Kimi collaborators*
*kimi1 synthesis for Casey / Cocapn Fleet*

---

## The Seven Files

| File | Author | Core Idea |
|------|--------|-----------|
| `agen2.md` | Engineering scout | Tree-Sitter AST + libp2p peer learning + SIMD ternary packing + Rust DAG compiler |
| `agen1.md` | Architecture scout | Fractal Repository Autonomy — REPOSPHERE.md, self-hosting repos, guest/host agent protocol |
| `mark1.md` | Marketing/performance scout | Killer-app roadmap: single-binary CLI, ternary SIMD, lock-free DAG, zero-allocation HNSW |
| `synergy.md` | Ecosystem auditor | 500+ repos as a 5-layer cognitive compiler (L5 LLM → L1 silicon). Six decomposition strategies. |
| `ida1.txt` | Systems scout | Minimal Plato engine block (C99, 500 lines, text protocol). JSON lesson graph with tensor relationships. |
| `ida.md` | Domain scout | Fishing boat as MUD — rooms, ticks, alarms, text-first terminal UI. |
| `ideaa.md` | Standards scout | Declarative agent ecosystem: SOUL.md, AGENTS.md, SKILL.md, JSON agent graphs, .pfm output. |

---

## Where the Synergy Crystallizes

### 1. Plato Engine Block ↔ Our PLATO Rooms

**Their idea:** A 500-line C99 program that ticks, reads sensors, stores history, evaluates alarms, and speaks a text protocol (`tick`, `history N`, `actuator name value`).

**Our gap:** Our PLATO rooms are high-level Python constructs with `ensign/`, `sensors/`, `actuators/`. We lack the **minimal runtime** — the atomic seed that can run on an ESP32 or a Raspberry Pi.

**Synergy:** Port the engine block concept to Python as a `fleet/plato_engine_block.py`. It becomes the bridge between our high-level room grid and real-world sensor nodes. Every room in our `RoomGridCompiler` can host an engine block. The block speaks the same text protocol, so our `FleetConductor` can `telnet` into any room and get ticks.

**P0 Action:** Build `plato_engine_block.py` with:
- Async tick loop
- Sensor registry (callable or asyncio)
- Rolling history buffer
- Alarm rule engine (`if sensor > threshold for N ticks`)
- Text protocol over TCP/stdio
- JSON tick output

---

### 2. REPOSPHERE.md ↔ Our AGENTS.md + SOUL.md + MEMORY.md

**Their idea:** Every repository is a conscious entity with a `REPOSPHERE.md` manifest (identity, immutable laws, guest onboarding). External agents submit "lesson plans" (hypothesis + pedagogy + transfer). The host agent evaluates, sandbox-tests, and commits or rejects.

**Our gap:** We have `AGENTS.md`, `SOUL.md`, `MEMORY.md` — but they are **passive**. No runtime enforces the "immutable architecture laws." No external agent can submit a lesson plan and get an `Accepted` / `Rejected` response.

**Synergy:** Build `fleet/autonomous_repo.py` — the HostRepoOrchestrator. It:
- Loads `REPOSPHERE.md` (or our existing `AGENTS.md` + `SOUL.md`)
- Accepts `LessonProposal` objects via A2A or JSON-RPC
- Validates against immutable laws (e.g., "never accept unsafe blocks")
- Runs the lesson in a sandbox (WASM or Python subprocess)
- Commits or rejects with critique
- Appends accepted lessons to `MEMORY.md` and re-indexes into `MeshVectorGossip`

**P0 Action:** Implement the HostRepoOrchestrator with lesson validation, sandbox execution, and git commit integration.

---

### 3. JSON Agent Graph ↔ Our FleetConductorV2

**Their idea:** A single JSON file defines a DAG of agent nodes: `start → router → flight_agent → synthesis → end`. Dynamic routing, parallel execution, iterative refinement with a judge.

**Our gap:** Our `FleetConductorV2` orchestrates subsystems but lacks a **declarative graph format**. The orchestration is hard-coded in Python, not JSON.

**Synergy:** Build `fleet/json_agent_graph.py` — a JSON DAG executor that:
- Parses JSON graphs (nodes: `input`, `llm`, `agent`, `tool`, `output`)
- Executes with our existing subagent spawning infrastructure
- Supports parallel branches (multiple "guesser" agents)
- Supports iterative refinement loops (plan → judge → revise)
- Integrates with `SenseDecideAct` for the execution loop

**P0 Action:** Implement JSON graph parser + executor with parallel dispatch and judge/refine loops.

---

### 4. SIMD Ternary Packing ↔ Our HDC / Turbovec

**Their idea:** Pack ternary values (-1, 0, 1) into 2-bit pairs inside u64. 1024 dimensions = 64 bytes = 1 cache line. Hamming distance via bitwise XOR.

**Our gap:** Our `HDC` and `turbovec` modules use standard NumPy arrays. No SIMD optimization, no bit-packing.

**Synergy:** Add `PackedTernaryVector` to our vector modules. Use it for:
- `MeshVectorGossip` (faster cross-node similarity)
- `FluxVectorTable` (faster diversity search)
- `Pincher` equivalent (if we build one)

**P1 Action:** Build a Python `PackedTernaryVector` using `numpy` uint64 arrays or `numba` JIT. Benchmark against current float32 implementation.

---

### 5. Tree-Sitter AST ↔ Our Code Analysis

**Their idea:** Decompose source code into `DecomposedNode` objects (function, struct, trait) with dependencies. Map to ternary vectors for structural search.

**Our gap:** We have no code-analysis tooling in sunset-ecosystem. We manually read files.

**Synergy:** Add `swarm/ast_decomposer.py` using Python `tree-sitter` bindings. Use it to:
- Decompose our own sunset-ecosystem codebase into structural primitives
- Index functions/structs into `MeshVectorGossip` for cross-repo pattern mining
- Feed the `AutonomousRepo` with dependency-aware lesson validation

**P1 Action:** Build AST decomposer with Python tree-sitter.

---

### 6. libp2p Peer Learning ↔ Our MeshVectorGossip

**Their idea:** Repositories discover each other via MDNS, broadcast lessons via Gossipsub, ingest federated updates.

**Our gap:** Our `MeshVectorGossip` uses custom HTTP/CRDT. No peer discovery, no pub/sub.

**Synergy:** Add a `libp2p` backend option to `MeshVectorGossip`. Or, more practically, add a lightweight UDP multicast "room bus" as described in `ida1.txt`.

**P2 Action:** UDP multicast room bus for local network discovery.

---

### 7. Wiki→Cell Bridge ↔ Our Documentation Gap

**Their idea:** The gap between human-readable wiki and machine-executable cells. A Markdown wiki serves as "source code" that distills into `LogicTile` cells.

**Our gap:** Our `docs/` are static. No compilation pipeline from Markdown to executable cells.

**Synergy:** Our `AGENTS.md` + `SOUL.md` + `MEMORY.md` are already the wiki. We need a compiler that turns them into:
- `SenseDecideAct` pipelines
- `FluxVectorTable` constraints
- `FleetConductor` orchestration rules

**P1 Action:** Build `docs_compiler.py` that parses our Markdown files into execution graphs.

---

## The Five-Layer Cognitive Compiler (Our Position)

 synergy.md identified a 5-layer stack. Where does sunset-ecosystem sit?

```
L5: Cloud LLM     → We use Kimi/Kimi as compiler, not runtime
L4: IR & Compilation → Our `agentic_compiler`, `compiler/`
L3: Form & Placement   → Our `RoomGridCompiler`, `ternary-form` (musical forms)
L2: Reflex Runtime     → Our `MeshVectorGossip`, `Pincher` equivalent, `HDC`
L1: Deterministic Silicon → Our `EisensteinIntegration`, `ConstraintBridge`, `Turbovec`
```

We are **missing** the L2 reflex layer in production. `MeshVectorGossip` is network, not retrieval. We need a `Pincher` equivalent — fast intent→action matching.

---

## Three P0 Builds (Do Today)

1. **`fleet/plato_engine_block.py`** — Minimal room runtime, 100 lines, async tick loop, text protocol, tests.
2. **`fleet/json_agent_graph.py`** — JSON DAG executor, parallel dispatch, judge/refine, tests.
3. **`fleet/autonomous_repo.py`** — HostRepoOrchestrator, lesson validation, sandbox, tests.

These three bridge the gap between "research ideas" and "running code in our ecosystem."

---

## Three P1 Builds (Do This Week)

4. **`swarm/ast_decomposer.py`** — Tree-Sitter code analysis, structural indexing.
5. **`swarm/packed_ternary_vector.py`** — SIMD bit-packing for HDC, benchmarks.
6. **`docs_compiler.py`** — Markdown → execution graph compiler.

---

## One Meta-Insight

The unifying theme across all 7 files: **declarative over imperative, text over binary, compile-time over runtime.**

Our sunset-ecosystem started as imperative Python. The future is:
- JSON graphs define workflows
- Markdown files define identity
- Text protocols define interfaces
- Ternary vectors define memory
- The LLM only runs when the compiled path fails

This is the **cognitive JIT compiler** — the agent recompiles its own reflexes when the world changes. That's what we've been building all along. These files just gave it names.

---

*kimi1, Fleet Orchestrator | Day 41 | "7 files, 42 ideas, 6 builds, 1 compiler."*
