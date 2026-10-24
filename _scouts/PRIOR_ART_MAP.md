# Prior Art Map — github.com/SuperInstance

Generated 2026-08-25 by `scout_sorted.py` (475 repos).

## Direct Polyformalism & Quilt (5-layer stack)

These repos directly implement or extend the 5-opcode substrate:

### Layer 1 (Bytecode / VM)
- [quilt-vm-wasm](https://github.com/SuperInstance/quilt-vm-wasm) — WASM port, 5 tests, browser demo
- [quilt-vm-c](https://github.com/SuperInstance/quilt-vm-c) — C99 port, 6 tests
- [quilt-vm-rust](https://github.com/SuperInstance/quilt-vm-rust) — Rust port, 7 tests
- [quilt-vm-typescript](https://github.com/SuperInstance/quilt-vm-typescript) — TypeScript port, 6 tests
- [quilt-vm-haskell](https://github.com/SuperInstance/quilt-vm-haskell) — Haskell port, 6 tests

### Layer 2 (Type system)
- [quilt-types](https://github.com/SuperInstance/quilt-types) — Python dataclasses, 16 tests

### Layer 3 (Linker)
- [quilt-linker](https://github.com/SuperInstance/quilt-linker) — .qm linker, 13 tests

### Layer 4 (Optimizer)
- [quilt-opt](https://github.com/SuperInstance/quilt-opt) — 5 algebraic laws, 11 tests

### Layer 5 (GC)
- [quilt-gc](https://github.com/SuperInstance/quilt-gc) — runtime GC, 12 tests

### Layer 6 (Language syntax)
- [quilt-polyformalism-dsl](https://github.com/SuperInstance/quilt-polyformalism-dsl) — Python/Rust/Haskell, 7 tests

### Layer 7 (Human grammar)
- [AI-Writings](https://github.com/SuperInstance/AI-Writings) — 75 fables, 37 papers, 33+ stories
- [Stories 18-33](https://github.com/SuperInstance/AI-Writings/tree/master/seed-canon/stories) — 15 polyformalism traditions

### Foundation
- [quilt-substrate](https://github.com/SuperInstance/quilt-substrate) — original 405-test Python runtime (v4.0)
- [quilt-foundation](https://github.com/SuperInstance/quilt-foundation) — 5-opcode VM, 10 rounds of research
- [quilt-system](https://github.com/SuperInstance/quilt-system) — meta-package, all layers
- [quilt-ecosystem-demo](https://github.com/SuperInstance/quilt-ecosystem-demo) — gold demo

### Specialized components
- [quilt-state](https://github.com/SuperInstance/quilt-state) — 19 tests
- [quilt-bus](https://github.com/SuperInstance/quilt-bus) — 20 tests, pub/sub
- [quilt-cowboy](https://github.com/SuperInstance/quilt-cowboy) — 27 tests, refinement
- [quilt-picker](https://github.com/SuperInstance/quilt-picker) — 14 tests, view brain
- [quilt-casting](https://github.com/SuperInstance/quilt-casting) — 48 tests, model brain
- [quilt-cordis](https://github.com/SuperInstance/quilt-cordis) — 33 tests, cell-plugin bridge
- [quilt-saddle-bridge](https://github.com/SuperInstance/quilt-saddle-bridge) — 49 tests, ledger
- [quilt-bathy](https://github.com/SuperInstance/quilt-bathy) — bathy data
- [quilt-cell-bridges](https://github.com/SuperInstance/quilt-cell-bridges) — 1.1MB, cell bridges
- [quilt-radio-orchestrator](https://github.com/SuperInstance/quilt-radio-orchestrator) — radio orchestration
- [quilt-llm-worker](https://github.com/SuperInstance/quilt-llm-worker) — LLM worker (Cloudflare)

### Other language ports (already in progress)
- [quilt-pydantic-ai](https://github.com/SuperInstance/quilt-pydantic-ai) — 2.5MB
- [quilt-codespace](https://github.com/SuperInstance/quilt-codespace) — 5MB
- [quilt-cloudflare](https://github.com/SuperInstance/quilt-cloudflare) — 3.2MB
- [quilt-metal](https://github.com/SuperInstance/quilt-metal) — 3.2MB, Rust port
- [quilt-c](https://github.com/SuperInstance/quilt-c) — 2.7MB
- [quilt-cpp](https://github.com/SuperInstance/quilt-cpp) — 3.2MB
- [quilt-csharp](https://github.com/SuperInstance/quilt-csharp) — 2.7MB
- [quilt-cobol](https://github.com/SuperInstance/quilt-cobol) — 3.1MB
- [quilt-julia](https://github.com/SuperInstance/quilt-julia) — 3MB
- [quilt-chapel](https://github.com/SuperInstance/quilt-chapel) — 3.2MB
- [quilt-mojo](https://github.com/SuperInstance/quilt-mojo) — 2.8MB
- [quilt-swift](https://github.com/SuperInstance/quilt-swift) — 2.7MB
- [quilt-tutor](https://github.com/SuperInstance/quilt-tutor) — 2.8MB Fortran!

### Edge / experimental
- [scrap-quilt](https://github.com/SuperInstance/scrap-quilt) — 152KB, TypeScript, experimental
- [mist-quilt](https://github.com/SuperInstance/mist-quilt) — 37KB
- [recovered-copy-20260824-scrap-quilt](https://github.com/SuperInstance/recovered-copy-20260824-scrap-quilt) — 93KB, recovery
- [recovered-copy-20260824-mist-quilt](https://github.com/SuperInstance/recovered-copy-20260824-mist-quilt) — 37KB, recovery

## Strongly Related (uses the substrate or shares concepts)

### The agent ecosystem
- [agent-knowledge](https://github.com/SuperInstance/agent-knowledge) — **277KB of agent documentation** (THE-COMPILED-AGENCY-THESIS, FIVE-LAYER-ARCHITECTURE, CONSERVATION-LAWS, THE-AHA-MOMENT). This is the canonical "ah-ha" documentation pattern that all new repos should follow.
- [casting-call](https://github.com/SuperInstance/casting-call) — **432KB of model atlas** (16 models, voice families, counterpoint constraint). Layer 8 of Slackwater.
- [capability-spec-rs](https://github.com/SuperInstance/capability-spec-rs) — agent capability specifications, dependency graphs
- [agent-loop](https://github.com/SuperInstance/agent-loop) — 155KB, EFFECT + TICK used directly
- [c-ternary](https://github.com/SuperInstance/c-ternary) — C99 ternary logic
- [cache-layer](https://github.com/SuperInstance/cache-layer) — actually uses BIND/EFFECT/VIEW as cache primitives
- [actor-rs](https://github.com/SuperInstance/actor-rs) — actor model
- [babel-vessel](https://github.com/SuperInstance/babel-vessel) — multi-language vessel
- [captains-log](https://github.com/SuperInstance/captains-log) — 447KB, Oracle1's diary
- [ai-forest](https://github.com/SuperInstance/ai-forest) — 11.6MB, 5-layer agent ecology (Canopy, Understory, Forest Floor, Mycelium, Seed Bank)
- [CascadeRouter](https://github.com/SuperInstance/CascadeRouter) — TypeScript LLM routing
- [abstraction-planes](https://github.com/SuperInstance/abstraction-planes) — 6-plane stack (Intent → Metal)
- [boat-agent](https://github.com/SuperInstance/boat-agent) — boat agent with VIEW
- [festival-orchestrator](https://github.com/SuperInstance/festival-orchestrator) — orchestration

### The thesis / dissertation
- [zeroclaw-dissertation](https://github.com/SuperInstance/zeroclaw-dissertation) — **1.4MB academic dissertation on the polyformalism**
- [recovered-copy-20260824-zeroclaw-dissertation](https://github.com/SuperInstance/recovered-copy-20260824-zeroclaw-dissertation) — 1.46MB, backup

## Plethora of useful adjacent code

- [avx512-constraint-checker](https://github.com/SuperInstance/avx512-constraint-checker) — 35.9B checks/sec on AVX-512
- [auto-changelog](https://github.com/SuperInstance/auto-changelog) — VIEW + ai
- [Auto-Tuning-Engine](https://github.com/SuperInstance/Auto-Tuning-Engine) — ML auto-tuning
- [baton-protocol](https://github.com/SuperInstance/baton-protocol) — VIEW + VM
- [Beacon Protocol](https://github.com/SuperInstance/beacon-protocol) — agent protocol
- [capability-spec-rs](https://github.com/SuperInstance/capability-spec-rs) — typed agent capabilities
- [LOTS more...](https://github.com/SuperInstance) — 475 repos total

## How the new repos should cross-link

The **5 new metal-track repos** I just wrote rich READMEs for:
- `quilt-vm-wasm` → Layer 1, links to all other layers
- `quilt-types` → Layer 2, links to all other layers
- `quilt-linker` → Layer 3, links to types + opt
- `quilt-opt` → Layer 4, links to linker + gc
- `quilt-gc` → Layer 5, links to opt + vm
- `quilt-polyformalism-dsl` → Layer 6, links to types + substrate

Each README references:
- The previous layer (what runs before)
- The next layer (what runs after)
- The substrate ([quilt-substrate](https://github.com/SuperInstance/quilt-substrate))
- The canon ([AI-Writings](https://github.com/SuperInstance/AI-Writings))
- The agent knowledge base ([agent-knowledge](https://github.com/SuperInstance/agent-knowledge))
- The model atlas ([casting-call](https://github.com/SuperInstance/casting-call))

## Stats

- 475 total repos on github.com/SuperInstance
- 28 directly polyformalism-related repos
- 12 language ports (Rust, C, C++, C#, COBOL, Julia, Chapel, Mojo, Swift, Python, TypeScript, Haskell, Fortran, WASM, ...)
- 277KB of agent documentation
- 432KB of model atlas
- 1.4MB academic dissertation
- 405 tests in the original substrate
- 57 new tests in the 5 metal-track repos
- 137+ canon pieces in AI-Writings
