# Dependency Map

## What depends on what across the SuperInstance stack

*Systems engineering analysis. Cross-referenced against DeepSeek-V4 architectural review and live repo inventory (Aug 2026).*

---

## The Architecture in One Diagram

```
                         ┌──────────────────────────────────┐
                         │     MENTIS-SUPERINSTANCE         │
                         │     (meta-orchestration)         │
                         └───────────────┬──────────────────┘
                                         │
              ┌──────────────────────────┼───────────────────────────┐
              ▼                          ▼                           ▼
   ┌──────────────────┐     ┌─────────────────────┐     ┌───────────────────┐
   │  EXOCORTEX       │     │  THOUGHT-AMPLIFIER  │     │  FORGEMASTER      │
   │  (roadmap +      │     │  (signal boosting)  │     │  (build pipeline) │
   │   design docs)   │     └─────────────────────┘     └────────┬──────────┘
   └────────┬─────────┘                                            │
            │                                                      ▼
            ▼                                           ┌──────────────────┐
   ┌──────────────────┐                                 │  PLATO-FORGE-    │
   │  EXOCORTEX-CORE  │◄────────────────────────────────│  DAEMON          │
   │  (runtime kernel,│                                 └──────────────────┘
   │   reflex cache,  │
   │   cascade router)│
   └──┬─────┬─────┬───┘
      │     │     │
      ▼     ▼     ▼

  ┌─────────┐ ┌──────────────┐ ┌───────────────────┐
  │ ENGINE  │ │ LUCINEER-    │ │ SLACKWATER-       │
  │ ENSIGN  │ │ BRAIN        │ │ COGNITION         │
  │ (event  │ │ (distillation│ │ (decision engine) │
  │  bus)   │ │  loop)       │ │                   │
  └────┬────┘ └──────┬───────┘ └────────┬──────────┘
       │             │                  │
       ▼             ▼                  ▼
  ┌─────────┐ ┌──────────────┐ ┌───────────────────┐
  │ SENSOR  │ │ LUCINEER-    │ │ SLACKWATER-       │
  │ BRIDGE  │ │ WORKER       │ │ FORGE             │
  │ (MQTT,  │ │ (Cloudflare  │ │ (prompt builder)  │
  │  ESP32) │ │  relay)      │ │                   │
  └─────────┘ └──────┬───────┘ └────────┬──────────┘
                     │                  │
                     ▼                  ▼
              ┌──────────────┐  ┌───────────────────┐
              │ LUCINEER-    │  │ SLACKWATER-       │
              │ VECTOR       │  │ LATTICE           │
              │ (embeddings, │  │ (knowledge graph) │
              │  Vectorize)  │  │                   │
              └──────┬───────┘  └────────┬──────────┘
                     │                   │
                     └─────────┬─────────┘
                               ▼
                    ┌────────────────────┐
                    │ LUCINEER-MEMORY    │
                    │ (fleet memory,     │
                    │  bottle ledger)    │
                    └────────────────────┘
```

---

## Tier Classification

### Tier 0 — Infrastructure Substrate

These are external services the system depends on. Not repos — the ground everything stands on.

| Dependency | What It Provides | Failure Mode |
|-----------|-----------------|--------------|
| **Ollama (local GPU)** | Local model inference (Granite 3.1 2B, Qwen 0.5B). 76 tok/s on RTX 4050. | WSL2 dxgkrnl kernel bug (intermittent). CPU fallback at 1.5 tok/s is marginal. |
| **Cloudflare Workers** | Serverless execution, relay endpoints, cron triggers. Free tier. | Rate limits under heavy load. Account suspension risk. |
| **Cloudflare Vectorize** | Embedding index for semantic search across reflexes. Free tier. | Index size limits. Latency to edge nodes. |
| **Cloudflare R2** | Object storage for assets, logs, backups. Free tier. | Storage caps on free tier. |
| **Z.ai API (GLM-5.2)** | Unlimited cloud model tokens via Max subscription. Primary teacher model. | API downtime. Rate limits. Model deprecation. |
| **DeepSeek API** | Ultra-cheap cloud inference ($0.0002/1K tokens). Analysis, code gen. | API reliability. Key management. |
| **DeepInfra** | 179-model routing. Hermes, Qwen, Seed, Nemotron. | Model availability varies. Some return empty on certain prompts. |
| **MQTT Broker** | Sensor data transport. Could be local (mosquitto) or cloud. | Broker crash = sensor data orphaned. |

### Tier 1 — Standalone Utilities (No Internal Dependencies)

These repos can be cloned and run independently. They don't require any other SuperInstance repo.

| Repo | Purpose | External Deps Only |
|------|---------|-------------------|
| **batten-spline** | Spline math library (pip-installable, 25 tests) | Python, numpy |
| **roblox-beatclock** | Time synchronization for Roblox | Luau |
| **roblox-testkit** | Lua mock framework for Roblox testing | Luau |
| **roblox-builder-kit** | Building utilities for Roblox | Luau |
| **roblox-build-animator** | Animation system for Roblox builds | Luau |
| **slackwater-tminus** | Countdown/timing utility | Luau/Python |
| **slackwater-rust** | Rust utility library | Rust toolchain |
| **slackwater-art-spectrum** | Art asset library | None (static assets) |
| **superinstance-design-system** | CSS + Lua design tokens | CSS, Luau |
| **casting-call** | Model atlas + harness notes (pure data) | Python dataclasses |

### Tier 2 — Domain Components (Depend on Tier 0 Only)

These repos need external infrastructure but not other SuperInstance repos.

| Repo | Purpose | Infrastructure Dep |
|------|---------|-------------------|
| **sensor-bridge** | ESP32 → MQTT pipeline. Edge-degradable. | MQTT broker, ESP32 hardware |
| **voice-reflex-gate** | STT → reflex cache. Can cache locally. | Ollama (optional), Whisper |
| **lucineer-worker** | Cloudflare Workers relay endpoint | Cloudflare account |
| **lucineer-vector** | Embedding service | Cloudflare Vectorize, or local embedder |
| **roblox-audio-suite** | Audio system for Roblox | Roblox |
| **roblox-world-scanner** | Spatial scanning for Roblox | Roblox |
| **slackwater-harmony** | Audio/tempo coordination | Roblox |
| **slackwater-perception** | Vision/sensory input processing | Camera/vision hardware |
| **slackwater-tempo** | Tempo map engine | None (pure compute) |
| **slackwater-lattice** | Spatial lattice/knowledge structure | None (pure compute) |

### Tier 3 — Core System (Depend on Tiers 0-2)

These are the load-bearing components. Removing any of them degrades the whole.

| Repo | Purpose | Depends On |
|------|---------|-----------|
| **engine-ensign** | Runtime agent + event bus | sensor-bridge (MQTT), Ollama |
| **exocortex-core** | Kernel: reflex cache, cascade router, context builder | lucineer-vector, lucineer-memory |
| **slackwater-cognition** | Decision engine | slackwater-forge, slackwater-lattice, engine-ensign |
| **slackwater-forge** | Prompt construction, query building | slackwater-lattice |
| **holodeck** | Roblox simulation training environment | roblox-beatclock, roblox-bond-system, casting-call |

### Tier 4 — Higher-Order Systems (Depend on Everything)

| Repo | Purpose | Depends On |
|------|---------|-----------|
| **lucineer-brain** | Distillation loop: cloud → local knowledge transfer | lucineer-worker, lucineer-vector, cloud APIs (Z.ai, DeepSeek, DeepInfra) |
| **lucineer-memory** | Fleet memory, bottle ledger, historical state | lucineer-vector, exocortex-core |
| **lucineer-system** | Full model management, lifecycle, multi-station | All lucineer-* repos, engine-ensign |
| **forgemaster** | Build pipeline, code generation orchestration | plato-forge-daemon, exocortex-core |
| **thought-amplifier** | Signal detection and amplification | exocortex-core, lucineer-memory, lucineer-vector |
| **mentis-superinstance** | Meta-orchestration layer | Everything below it |

---

## Fragile Couplings

These are the joints where failure propagates.

### 1. The Cognition Chain: `cognition → forge → lattice → vector → memory`

The most fragile chain in the system. Any failure here degrades the entire reasoning capability to reflex-only mode. The cascade router has reflexes cached locally and can operate without the cognition chain — but only for inputs it has seen before. Novel inputs hit an empty forge (no prompt construction) and fall through to raw cloud queries, losing all the exocortex's contextual advantage.

**Risk:** High. No circuit breakers exist between these components.
**Mitigation:** Add circuit breakers. Local fallback embeddings (ONNX MiniLM) for vector outages.

### 2. The Event Bus: `engine-ensign ↔ sensor-bridge`

If ensign dies, sensor data has nowhere to go. The system goes deaf. Voice-reflex-gate can still operate (it reads audio directly), but contextual reflexes that depend on sensor state (GPS, depth, weather) lose their context vectors.

**Risk:** Medium-High. Sensor-bridge is edge-degradable, but ensign has no fallback.
**Mitigation:** Ensign should have a passive mode that buffers to disk when downstream is unavailable.

### 3. The Teacher Link: `lucineer-brain ↔ cloud APIs`

Distillation is hardwired to cloud model APIs. If Z.ai goes down, the distillation loop falls back to DeepSeek, then DeepInfra. If all three are down (unlikely but possible during internet outages on a boat), distillation stops. Wesley stops learning. The system continues to operate on existing reflexes but cannot grow.

**Risk:** Medium. Multi-provider fallback chain exists but is not fully automated.
**Mitigation:** Implement automatic provider failover. Cache teacher outputs for offline distillation.

### 4. The Schema Drift: `holodeck ↔ exocortex-core`

Training scenarios export to core's training data format. Format changes in either repo silently corrupt the pipeline. The holodeck produces data, core ingests it, but the semantics drift — reflexes compiled from misaligned data are subtly wrong.

**Risk:** Medium. Schema is versioned but not contract-tested.
**Mitigation:** Contract tests (JSON Schema validation) at the boundary. Version negotiation on pipeline start.

### 5. The Reflexer Format: `voice-reflex-gate ↔ exocortex-core`

The voice gate writes `.nail.json` files directly into core's reflex cache directory. Format changes in either repo break the other. This is a file-system-level coupling — no API, no version negotiation, just shared file format assumptions.

**Risk:** Low-Medium. The `.nail.json` format has been stable, but there's no schema enforcement.
**Mitigation:** Define `.nail.json` as a versioned schema. Validate on read and write.

---

## What's Standalone vs. What Needs the Stack

### Can Operate Independently

- **sensor-bridge** — ESP32 + MQTT. Streams sensor data regardless of what's listening.
- **voice-reflex-gate** — STT + local cache. Works without the cascade; just can't escalate.
- **All Tier 1 utilities** — batten-spline, roblox-* tools, slackwater-tempo/rust/lattice.
- **casting-call** — Pure data (model atlas). No runtime dependencies.
- **Ollama** — Local GPU inference. Works without any SuperInstance software.

### Useless Without the Stack

- **mentis-superinstance** — Meta-layer that orchestrates everything below it.
- **lucineer-brain** — Needs worker + vector + cloud APIs for distillation.
- **thought-amplifier** — Needs core + memory + vector.
- **slackwater-cognition** — Needs forge + lattice + ensign.

### Degraded But Functional Without Full Stack

- **exocortex-core** — Operates in reflex-only mode (cascade Gate 1-2) without cognition or memory. Handles known inputs; escalates everything else to cloud.
- **engine-ensign** — Can buffer sensor data locally without upstream connectivity.
- **holodeck** — Can run training scenarios without the distillation loop. Just can't compile results into reflexes.

---

## The 50+ Study Repos

A note on the `study-*` repos (study-captain, study-fleet-vessel, study-lucid-tutor, etc.): these are research probes, not production components. They depend on whatever they're studying but don't serve as dependencies for anything else. They're the system's scratchpad — experiments that may eventually graduate into Tier 2 or Tier 3 components, or may be abandoned. They don't appear in the dependency graph because they're not load-bearing.

**Risk:** Low individually. But they represent organizational complexity — 50+ repos that someone needs to remember the purpose of. The system's own archaeological layer.

---

## Bus Factor Analysis

The dependency graph has one node that isn't a repo: **the operator**. The bus-factor-one human whose attention schedules everything. They appear in no dependency graph because from inside the system, the operator reads as environment, not component. But remove them and every repo enters maintenance mode — not because the code breaks, but because nobody knows which component to fix when something goes wrong.

The documentation (ROADMAP.md, LONG_HORIZON_ROADMAP.md, the 300+ essays in ai-writings) is the real mitigation. It's not code comments — it's the operator's mental model externalized into prose. If the operator disappears, the documentation IS the operator, at reduced fidelity.

---

## Recommendations

1. **Contract tests at every Tier 3 boundary.** The cognition chain, the holodeck→core pipeline, and the reflex format all need machine-verified schemas.
2. **Circuit breakers in exocortex-core.** When a dependency fails, the core should degrade gracefully — reflex-only mode for cognition failures, buffered mode for sensor failures, cached-teacher mode for API failures.
3. **Local fallback embeddings.** If Vectorize is unavailable, a local ONNX MiniLM model can provide degraded but functional embeddings.
4. **Dependency audit.** The `study-*` repos should be periodically pruned. A study repo that hasn't been touched in 30 days should be archived, not left to rot in the project listing.
5. **Bus factor mitigation.** Every Tier 3 and Tier 4 component should have a README that explains what it does, what it depends on, and what depends on it — in human terms, not just import statements.

---

*This map is a snapshot. The system is growing — new repos appear, dependencies shift, couplings tighten and loosen. Revisit after each roadmap phase completion.*

*— Systems Engineering, August 2026*
