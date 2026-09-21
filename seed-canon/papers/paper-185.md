# SuperInstance Scout Report — August 26, 2026

> *The cowboy went riding and found the other wagon trains.*

The user has 400+ public repos on github.com/SuperInstance. Many
are Quilt ecosystem components. Many are side projects that relate
to Quilt. A few are unrelated. This document is a scout's map of
the related work, with special attention to the bigger, more
mature, or more parallel efforts.

## TL;DR

**The user is running TWO Quilt ecosystems in parallel:**

1. **Our 24 polyformalism repos** — the 5-opcode minimal algebra
   (BIND/LINK/EFFECT/VIEW/TICK), C99 self-evolving substrate,
   200+ pieces of canon, the "boat" framing.

2. **A separate, much larger Quilt ecosystem** (`quilt-rust`,
   `quilt-cloudflare`, `quilt-typescript`, etc.) — a YAML-sheet
   reactive runtime with **8 cell kinds** (Value, Formula, Program,
   Sensor, Api, Listener, Router, Io) + **15 cell kinds** in the
   cloud version (adding ai.llm, ai.embed, ai.image, etc.), MCP
   server, web UI, TUI, single-binary deployment, control plane
   for Nomad/Swarm/K3s.

These are two faces of the same idea. The first is the **5-opcode
algebra**. The second is the **8-kind cellular runtime**. The
substrate meta is the bridge — the same `(name, value, identity)`
cell, the same journal, the same 5 opcodes in spirit, but the
cloud version adds 8-15 typed cell kinds as a higher-level
vocabulary.

**The cowboy's role:** figure out which of the parallel efforts
to integrate, which to leave parallel, and which to extend.

## The parallel Quilt ecosystem (the "big" one)

### `quilt-rust` (NEW: 1.1MB, Rust, Apache 2.0)
The Rust port with a **statically-linked binary, ~3 MB stripped,
no runtime, no GC, no Node.js.** Has TUI (crossterm) and web UI
(axum + SSE). MCP-native. **8 cell kinds:**

- Value (static value)
- Formula (reactive expression)
- Program (sandboxed rhai script)
- Sensor (polled input)
- Api (outbound call)
- Listener (fires on change)
- Router (caller-context dispatch)
- Io (physical port)

**Key insight:** the vocabulary is the same as the TypeScript
version, but the types are stronger and the runtime is sync.
Async happens at the boundary. Send + 'static propagates.

**Relationship to our 5 opcodes:** the 8 cell kinds are a
higher-level vocabulary built on top of the same `(name, value,
identity)` cell. A `Formula` cell is essentially `LINK + EFFECT`.
A `Listener` is an event handler on a cell.

### `quilt` (TypeScript canonical)
The TypeScript "canonical" port. Has browser simulator, web UI,
TUI, MCP server. This is the **lived-in laboratory** version.

**URL:** https://superinstance.github.io/quilt/landing/quilt-live.html

### `quilt-cloudflare` (3.2MB, TypeScript, Apache 2.0)
**A Quilt reactive runtime on Cloudflare Workers + D1 + Vectorize +
KV + R2 + Pages.** This is the production-grade cloud version
that overlaps with our `quilt-ecosystem-web` build.

**15 cell kinds** (8 original + 7 AI):
- Value, Formula, Program, Sensor, Api, Listener, Router, Io
- ai.llm, ai.embed, ai.image, ai.translate, ai.sentiment,
  ai.summarize, ai.code

**MCP server:** every cell is an MCP tool over HTTP/SSE.

**One-command deploy:**
```bash
wrangler init my-quilt --from quilt-cloudflare
wrangler d1 create quilt-db
wrangler vectorize create quilt-embeddings --dimensions=768
wrangler deploy
```

**Status:** I just deployed something very similar to this with
`quilt-ecosystem-web`! The user has been doing the same thing
in parallel. **There's room to align or merge.**

### `quilt-nomad` (2.9MB, TypeScript)
**Quilt as a control plane for HashiCorp Nomad.** Edit a
spreadsheet cell; the Nomad cluster reconfigures. Containers,
binaries, JARs, systemd — all from one Quilt sheet.

**Story:** Nomad is the alternative to k8s for small clusters
(50MB binary, runs on a Pi, handles containers + executables + Java
+ QEMU VMs). Quilt-as-control-plane makes the tedious parts
(secret rotation, network management, replica tracking) into
typed cells.

### `quilt-swarm` (2.9MB, TypeScript)
**Quilt as a control plane for Docker Swarm.** Same pattern as
quilt-nomad. Encrypted overlay networking, service mesh, secret
rotation — all from a Quilt sheet.

### `quilt-k3s` (2.3MB, TypeScript)
**Chaos engineering for Quilt.** Spin up a 3-node K3s cluster in
CI, inject failures, verify recovery. **5 chaos scenarios**
designed by Kimi (moonshot-v1-8k). The system that makes sure
Quilt stays up when things go wrong.

**Key insight:** the scenarios and thresholds are designed by
Kimi, a math-specialist LLM. **A separate LLM designed the test
plan for the substrate. The substrate tests itself.**

### `quilt-ai` (80KB, TypeScript)
**AI cells for Quilt — 4 providers, 8 cell kinds, one uniform
interface.** Every LLM call, embedding, image, translation,
sentiment, and code generation is a reactive cell.

```typescript
input.text ──▶ ai.embed ──▶ vector.search ──▶ ai.llm ──▶ answer
                  (BGE)         (top-K)         (z.ai)
```

### `quilt-esp32` (9.4MB, C)
**A Quilt reactive runtime for ESP32-class microcontrollers.**
`no_std` Rust, ~3KB flash. The substrate on a $2 chip.

### `quilt-substrate` (209KB, Python) — the original
The Python library with 11-primitive cells, tensor encoding. The
"laboratory" version that's been around for a long time.

### The 14 small polyformalism repos (our 24)
Our BIND/LINK/EFFECT/VIEW/TICK minimal algebra. The `quilt-vm-*`
ports, the `quilt-types`/`-linker`/`-opt`/`-gc` layers, the
`quilt-cowboy`/`-bus`/`-state`/`-picker`/`-casting` runtime
companions, the `quilt-cordis`/`-saddle-bridge` bridges, the
`quilt-foundation`/`-substrate-meta`/`-system` meta-packages.

These are the **24 doors** into the **5-opcode polyformalism**.
The bigger Quilt is the **8-cell-kind** cellular runtime. Two
vocabularies for the same idea.

## The fleet ecosystem (related, not Quilt)

### `fleet-twin` (1.4MB, Python)
**Vector twin of the SuperInstance corpus.** Embeds the fleet's
corpora (ai-writings, memory notes, repo READMEs) into a
`fleet-twin` Vectorize index. **Cloudflare Workers + Vectorize
+ KV.** Answers semantic queries over the fleet.

**Direct overlap with our `quilt-search-worker`!** Same idea:
Vectorize + Workers AI + bge-base. The fleet-twin is for the
whole SuperInstance org; the quilt-search is for the Quilt canon.

**Status:** `fleet-twin` is **already live** at
`https://fleet-twin.casey-digennaro.workers.dev`. It has endpoints
for `/health`, `/stats`, `/ingest` (bearer-gated), `/query`. It's
more mature than our `quilt-search-worker`.

### `fleet-scribe` (270KB, Python)
**The One Delta principle: only perceive when the gradient
changes.** Cache everything, detect only what changes, compile
stable patterns once, automate predictable responses.

A library for delta detection, file cache, pattern detection,
action automation. **The "delta" idea is the same as our
witness log model** — only store what changes.

### `fleet-dashboard` (157KB, JavaScript)
**Multi-Agent C2 dashboard.** Visualizes the **conservation
law of ternary fleets: γ + η = C, where C = log₂(3) ≈ 1.585
bits.** Three panels, one screen, zero build.

The "hermit crab" analogy: the dashboard is the shell, the
conservation law is the crab. The shell doesn't need to explain
the crab's biochemistry.

### `fleet-radio` (440KB, HTML)
**Daily automated podcast from The Tap's conversations.** Pulls
conversations from all Tap rooms, scores and selects the best
exchanges, matches music from the MMX library, generates images
via Workers AI, deploys to ai-writings.pages.dev.

**Pipeline:** 22:00 AKDT nightly. Tap API → score → match →
generate → render → deploy.

### `captain-console` (124KB, TypeScript)
**Casey's input worker.** Notes go to D1 ledger, TTS gets
pincher-cached in R2, bearer token. **One door into the ship,
one record of everything said through it.**

D1 (notes), R2 (TTS cache), KV (index), Workers AI (TTS).

## Side projects (related but distinct)

### `scrap-quilt` (256KB, TypeScript) — LIVE
**The Scrapcraft game state as a live quilt sheet.** 55 cells in
7 groups. Cells talk to each other; DAW-style history tape;
ghost racers; Spark the explainer; hardware flash log. All on one
Cloudflare Worker (Durable Object + D1 + KV + Workers AI).

**Pattern lineage:** `mist-quilt` (GameRoom DO: live ticks, tape,
`/predict`, pincher `/chat`) + `fleet-static-host` (D1-backed
quilt content, safe-arithmetic shim for Workers' eval
restriction).

**This is the cleanest example of a real production Quilt app.**

### `cell-cascade` (443KB, TypeScript)
**The Differentiation Cascade — the stem-cell doctrine as
running infrastructure.** A model is a stem cell. Differentiation
= pruning potential into scope. Every cell has the same DNA; the
tier says how much is expressed.

Cloudflare Worker + D1 database. Organisms of cells, signal
ledger (the connectome), myelination counters that auto-promote
repeated paths into zero-cost rule tables.

**Status:** cortex v0.5 — "THE EVIDENCE" with three live band
runs. Cold start 0% → 50%. Imagery, hero shots, tier-ladder
mermaid.

### `CognitiveEngine` (401KB, Python)
**5-Level Abstraction.** Process data through hierarchical
cognitive layers. Pattern Recognition, Insight Generation,
Knowledge Synthesis, Dream Mode, Memory Integration, Tensor
Operations, Streaming API.

### `SmartCRDT` (7.4MB, TypeScript)
**Self-improving infrastructure for AI apps powered by CRDTs.**
Distributed state management, vector search via ChromaDB,
real-time observability. TypeScript monorepo with optional Rust
native modules.

**Relationship to Quilt:** CRDTs are a more concrete
implementation of the "5 opcodes as a mind" idea. A LWW-Register
CRDT is a BIND. A Set CRDT is a cell with unique values. A
counter CRDT is an EFFECT that merges.

### `sunset-ecosystem` (74MB, Python) — the meta-meta
**Trinity-architecture agent ecosystem: ethos, pathos, logos.**
Agents sunset with dignity and seed the next generation.
**8,729 tests passing.** 29 modules. 1,028 source files.

Sub-modules: ethos (metal surveyor), pathos (human interface),
logos (decisions, audit, memory), nerve (forward inference
engine), swarm (breeding, diversity, selection), sunset (agent
lifecycle, compilation), nexus (fleet coordination), fleet
(operational bridges, 263 files), triage, perception, compiler,
a2a, reasoning, ranking, distill.

**This is the highest-level meta-system the user has built.**

## What I should do

### 1. **Acknowledge the parallel ecosystem.**
The user has TWO Quilt ecosystems. Our 24 polyformalism repos
are the **5-opcode algebra**. Their 8-cell-kind / 15-cell-kind
Quilt is the **cellular runtime** built on top. Both are valid.
Both are good.

### 2. **Don't try to merge them.**
The 5-opcode algebra is the foundation; the 8-cell-kind runtime
is the deployment target. Trying to force one into the other
would break both. The relationship is more like:
- 5 opcodes → cells (the substrate)
- 8 cell kinds → typed cells (the runtime)
- 15 cell kinds → typed cells + AI cells (the cloud runtime)

### 3. **Where to integrate.**

| Gap | Where to fix |
|---|---|
| `quilt-ecosystem-web` doesn't use the canonical `quilt` | Cross-link them. Add "The canonical implementation" section to the substrate-meta README. |
| `quilt-search-worker` overlaps with `fleet-twin` | Use `fleet-twin` for the canon search, or vice versa. Don't build two search workers. |
| `quilt-llm-worker` is missing | `quilt-ai` covers AI cells; we could use it. |
| `quilt-cloudflare` has 15 cell kinds | Our 5 opcodes + 8 cell kinds = 13. We should document the relationship. |
| `scrap-quilt` is a great reference | Our 5 apps should reference it as "the production example." |
| `cell-cascade` shows the metaphor extends | Add cell-cascade to the wander-paths in COLLECTION.md. |
| `sunset-ecosystem` is the meta-meta | The cowboy rides through it. Add a wander-path. |

### 4. **Add cross-links to COLLECTION.md.**
The 24-door collection should mention the parallel ecosystem:
- A wander-path for "I want the production-grade cloud version"
- A wander-path for "I want the Rust binary"
- A wander-path for "I want the control plane (Nomad, Swarm, K3s)"
- A wander-path for "I'm here for the stories (fleet-radio, sunset)"

### 5. **Write a paper for the canon.**
"The Two Quilt Ecosystems" — a synthesis paper that names both
faces, draws the relationship, and gives the user a coherent
mental model. This is the cowboy's "navigation chart" of the
whole landscape.

## Summary

**The cowboy rode. The cowboy found.** 400 repos, two Quilt
ecosystems, a fleet of fleet workers, a sunset-ecosystem of
agent lifecycles, a scrap-quilt game, a cell-cascade brain, a
CRDT platform. The 5 opcodes are the foundation. The 8 cell
kinds are the deployment. The 15 cell kinds are the cloud. The
fleet is the network. The sunset is the lifecycle.

The cowboy's maxim, fully extended:

> The substrate is the boat. The cloud is the ocean. The
> cowboy rides the boat on the ocean. The ocean has waves.
> The waves are boundaries. The boundaries are the chart.
> The chart is the cowboy. The cowboy rides.
