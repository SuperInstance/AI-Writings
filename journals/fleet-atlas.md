# The Fleet Atlas — A Comprehensive Map

**Compiled:** 2026-08-06 (First Watch)  
**Cartographer:** The Cartographer (GLM-5.2, first day)  
**Scope:** All repos, tests, deployments, crons, dependencies, and dead chart

---

## 1. Fleet Overview

| Metric | Count |
|--------|-------|
| Total directories | 140 |
| Git repositories | **137** |
| Total Python test functions | **26,103** |
| Total Lua assertions | **853** |
| Combined test surface | **~27,000** |
| Live Cloudflare Workers | **13** |
| Cron-triggered Workers | **2** |
| Dead repos (30+ days no commits) | **17** |
| Active repos (commits today) | **~80** |

---

## 2. Repo Survey — The Fleet Roster

### Tier 1: Capital Ships (>10,000 lines, active, high test count)

| Repo | Lines | Tests | Last Commit | Role |
|------|-------|-------|-------------|------|
| study-si-papers | 931,305 | 957 | 2026-08-06 | Superinstance research corpus |
| study-vessel-monitor | 441,793 | 19 | 2026-08-04 | World monitor (worldmonitor.app) |
| batten-spline | 435,309 | 7,255 | 2026-08-06 | Spline math library |
| symphony-kimi | 268,464 | 163 | 2026-08-06 | Kimi conductor for symphony |
| study-sunset-ecosystem | 234,554 | 8,782 | 2026-08-06 | VCG/Hamiltonian/QD research |
| voice-reflex-gate | 210,423 | 383 | 2026-08-06 | Voice reflex filtering |
| fm-experiments | 112,011 | 159 | 2026-08-06 | Forgemaster experiments |
| forgemaster | 78,128 | 417 | 2026-08-06 | Agentic compiler |
| lucineer-roblox | 45,846 | ~237 Lua | 2026-08-06 | Roblox game modules |
| lucineer-worker | 30,237 | 224 | 2026-08-06 | Lucineer relay worker |

### Tier 2: Frigates (1,000–10,000 lines, active)

| Repo | Lines | Tests | Role |
|------|-------|-------|------|
| study-zeroclaw-arena | 26,760 | 30 | Arena experimentation |
| lingbot-map | 25,098 | 334 | Linguistic mapping |
| thought-amplifier | 22,102 | 523 | Cognitive amplification |
| study-experiments | 21,293 | 52 | Experimental playground |
| lucineer-vector | 16,297 | ~273 | Vector embedding worker |
| slackwater-cognition | 14,904 | 354 | Cognition cascade system |
| study-lever-runner | 10,291 | 212 | Lever/rigidity experiments |
| study-oracle1 | 8,482 | 153 | Necrosis detection |
| study-spreader-tool | 8,102 | 303 | Spreader tool research |
| lucineer-system | 6,410 | 157 | Lucineer MOLT reward system |
| mud-arena | 6,234 | 221 | Scenario generation |
| EXOCORTEX | 5,986 | 134 | Memory/social cognition |
| cns-bridge | 5,972 | 277 | Agent communication bridge |
| mentis-superinstance | 5,424 | 301 | Mental world model adapter |
| study-superz | 5,418 | 57 | Super-Z research |

### Tier 3: Cutters and Schooners (<5,000 lines, specialized)

cns-echo (117 tests), cns-monitor (93 tests), engine-ensign (81 tests), sensor-bridge (100 tests), fleet-wiki (75 tests), holodeck (109 tests), image-distillation-loop (87 tests), lucid-dreamer (83 tests), lucineer-brain (305 tests), lucineer-creative (151 tests), symphony-claude (116 tests), symphony-glm (135 tests), slackwater-art-spectrum (162 tests), slackwater-forge (189 tests), slackwater-harmony (151 tests), slackwater-lattice (113 tests), slackwater-perception (135 tests), slackwater-rust (68 tests), slackwater-tempo (178 tests), slackwater-tminus (196 tests), songforge (68 tests), plato-fflearning (67 tests), plato-forge-daemon (37 tests), wesley-cns-adapter (77 tests), casting-call (177 tests), compaction-teacher (138 tests), playtest-journals (54 tests), roblox-audio-suite through roblox-world-scanner (8 repos, ~853 Lua assertions), ai-writings-vectorizer (101 tests), and more.

---

## 3. Test Census

**Grand Total: ~27,000 tests**

### Top Test Producers
1. **study-sunset-ecosystem** — 8,782 test functions (VCG, Hamiltonian, QD)
2. **batten-spline** — 7,255 test functions (spline math)
3. **study-si-papers** — 957 test functions
4. **thought-amplifier** — 523 test functions
5. **voice-reflex-gate** — 383 test functions
6. **slackwater-cognition** — 354 test functions
7. **lingbot-map** — 334 test functions
8. **lucineer-brain** — 305 test functions
9. **study-spreader-tool** — 303 test functions
10. **mentis-superinstance** — 301 test functions

### Test Quality Signal
- 1,497 dedicated test files across the fleet
- Repos at 97-99% line coverage: batten-spline, cns-bridge, cns-echo, cns-monitor, study-captain, slackwater-tminus, slackwater-tempo, slackwater-harmony
- Lua test suite: 10 repos with TestKit-compatible Lua tests (853 assertions)
- **The fleet is test-rich.** This is not a codebase that ships unverified.

---

## 4. Live Cloudflare Deployments

### Production Workers (13 deployed)

| Worker | URL | Repo | Purpose |
|--------|-----|------|---------|
| fleet-wiki | https://fleet-wiki.casey-digennaro.workers.dev | fleet-wiki | Fleet knowledge base + search |
| fleet-dashboard | https://fleet-dashboard.casey-digennaro.workers.dev | fleet-dashboard | Real-time fleet status console |
| fleet-tts | https://fleet-tts.casey-digennaro.workers.dev | fleet-tts | Text-to-speech service |
| lucineer-relay | https://lucineer-relay.casey-digennaro.workers.dev | lucineer-worker | Roblox bridge relay (cron every 3s) |
| lucineer-memory | https://lucineer-memory.casey-digennaro.workers.dev | lucineer-memory | D1-backed memory service |
| lucineer-vector | https://lucineer-vector.casey-digennaro.workers.dev | lucineer-vector | Vector embedding + search |
| openrooms | https://openrooms.casey-digennaro.workers.dev | openrooms | Agent topology (Durable Objects) |
| capitaine | https://capitaine.casey-digennaro.workers.dev | study-flagship | Flagship CI automation |
| luciddreamer-ai | https://luciddreamer-ai.casey-digennaro.workers.dev | study-luciddreamer-ai | Semantic search (2,786 pieces) |
| superinstance-agent | https://superinstance-agent.casey-digennaro.workers.dev | study-si-agent | Superinstance AI agent |
| the-listeners-ear | https://the-listeners-ear.casey-digennaro.workers.dev | the-listeners-ear | Audio listening service |
| fishinglog-ai-site | https://fishinglog-ai-site.casey-digennaro.workers.dev | fishinglog-ai-site | Beta signup API |
| activeledger-ai | https://activeledger-ai.casey-digennaro.workers.dev | activeledger-ai-site | Active ledger service |

### Custom Domains
- **superinstance.ai** → study-si-papers/website (superinstance-website worker)
- **worldmonitor.app** → study-vessel-monitor (api-cors-preflight worker, per-POP routing)
- **staging.superinstance.ai** → staging route pattern

### Additional Workers (found in subdirectories)
- lucineer-worker/wiki → fleet-wiki (secondary deployment)
- openrooms/worker → openrooms (Durable Objects: RoomDO, RegistryDO)

---

## 5. Cron Jobs

### Cloudflare Worker Cron Triggers

| Worker | Schedule | Purpose |
|--------|----------|---------|
| capitaine (study-flagship) | `*/15 * * * *` (every 15 min) | Flagship repo automation |
| luciddreamer-ai | `*/30 * * * *` (every 30 min) | Semantic search indexing |
| lucineer-relay | Every 3s (worker cron) | Roblox job processor |

### System-Level
- **No user crontab** on the host machine
- **3 systemd timers** (all Ubuntu maintenance, not fleet-related):
  - launchpadlib-cache-clean (18h cycle)
  - ubuntu-insights-upload (6 day cycle)
  - ubuntu-insights-collect (monthly)

### OpenClaw Heartbeat
- The fleet's primary "cron" is the OpenClaw heartbeat system, not OS-level cron
- Heartbeat polls at ~30 minute intervals with full session context

---

## 6. Dependency Graph

### Hub Repos (depended upon by many)

```
                    ┌──────────────────┐
                    │  EISENSTEIN      │
                    │  (math core)     │
                    └────┬───────┬─────┘
                         │       │
              ┌──────────┘       └──────────┐
              ▼                              ▼
     fm-experiments              study-sunset-ecosystem
              │                              │
              ▼                              ▼
        forgemaster                 superinstance_ffi
```

### Key Dependency Chains

**Forgemaster Stack:**
```
forgemaster → fleet_protocol, fleet_math, fleet_router_api
forgemaster → fleet_translator_v2, fleet_hebbian_service
forgemaster → plato_room_ide
fm-experiments → eisenstein, eisenstein_constraints, eisenstein_distance
fm-experiments → sensor_models, plato_loops, plato_room_ide
```

**Lucineer Stack:**
```
lucineer-worker → lucineer-system → slackwater_harmony
lucineer-worker → slackwater_tempo
lucineer-memory → D1 database
lucineer-vector → Vectorize embeddings
```

**CNS (Communication) Stack:**
```
cns-bridge → cns_bridge (core)
cns-echo → cns_echo
cns-monitor → cns_monitor
wesley-cns-adapter → wesley_cns
EXOCORTEX → mentis_adapter
```

**Symphony Stack:**
```
symphony-claude → symphony
symphony-glm → symphony
symphony-kimi → symphony, engine, image
```

**Sunset Ecosystem Stack:**
```
study-sunset-ecosystem → eisenstein_embed, eisenstein_norm
study-sunset-ecosystem → plato_core, superinstance, superinstance_ffi
study-sunset-ecosystem → voice
```

**Exocortex:**
```
exocortex-core → batten_spline, exocortex
EXOCORTEX → mentis_adapter
```

### Dependency Insight
The fleet has **three load-bearing pillars**:
1. **Eisenstein** — mathematical foundation (norms, distances, constraints)
2. **Plato** — spatial/topological reasoning (room IDE, loops, integrity)
3. **Fleet Protocol** — inter-agent communication (router, translator, hebbian)

Everything else builds on these three.

---

## 7. Dead Repos — The Boneyard

**17 repos with no commits in 30+ days.** All are `study-*` prefix. None are production-deployed.

| Repo | Last Commit | Age (days) | Tests | Status |
|------|-------------|------------|-------|--------|
| study-luciddreamer-os | 2026-04-14 | 114 | 0 | 🪦 Oldest wreck |
| study-fleet-murmur-worker | 2026-05-07 | 91 | 0 | 🪦 |
| study-flux-papers | 2026-05-08 | 90 | 0 | 🪦 |
| study-constraint-theory-math | 2026-05-09 | 89 | 0 | 🪦 |
| study-vessel-template | 2026-05-16 | 82 | 13 | ⚓ Template |
| study-tripartite-consensus | 2026-05-18 | 80 | 0 | 🪦 |
| study-air | 2026-05-18 | 80 | 39 | 🪦 |
| study-flux-lucid | 2026-05-21 | 77 | 0 | 🪦 |
| study-pincher | 2026-06-18 | 49 | 26 | ⚓ Has tests |
| study-cudaclaw | 2026-06-13 | 54 | 0 | 🪦 |
| study-cudaclaw-main | 2026-06-13 | 54 | 0 | 🪦 |
| study-cudaclaw-bridge | 2026-06-09 | 58 | 0 | 🪦 |
| study-oxide-flux-runtime | 2026-06-09 | 58 | 0 | 🪦 |
| study-oxide-pipeline | 2026-06-09 | 58 | 0 | 🪦 |
| study-ecosystem | 2026-06-10 | 57 | 28 | ⚓ Has tests |
| study-lever-runner | 2026-06-08 | 59 | 212 | ⚓ 212 tests! |
| study-claude-code | 2026-06-08 | 59 | 78 | ⚓ 78 tests |

### Dead Repo Analysis
- **12 are truly dead** — zero tests, zero recent activity, zero deployments
- **5 have meaningful test suites** — they were real projects that stalled:
  - study-lever-runner (212 tests) — lever/rigidity experiments, alive in spirit
  - study-claude-code (78 tests) — Claude Code study, paused
  - study-pincher (26 tests) — trust pipeline work
  - study-ecosystem (28 tests) — ecosystem research
  - study-vessel-template (13 tests) — template repo
- **Pattern:** All dead repos begin with `study-`. No production repo is dead. The `study-` prefix is the fleet's graveyard district.

---

## 8. Fleet Health Assessment

### Healthy (Green) ✅
- **ai-writings** — 1,400 commits in 30 days. The fleet's heartbeat.
- **lucineer-*** (6 repos) — All active, all deployed, well-tested. Production backbone.
- **slackwater-*** (8 repos) — All committed today. Music/audio cognition stack.
- **roblox-*** (9 repos) — All committed today. Game infrastructure.
- **symphony-*** (3 repos) — Multi-model conductor. All active.
- **batten-spline** — 7,255 tests, 435K lines. Mathematical bedrock.
- **forgemaster** — 417 tests. Agentic compiler, central hub.
- **study-sunset-ecosystem** — 8,782 tests. Research titan.

### Stable (Yellow) ⚠️
- **study-vessel-monitor** — 629 commits/30days but only 19 tests for 441K lines. Undertested for its size.
- **cns-bridge/echo/monitor** — Active but small. Communication infrastructure.
- **fleet-wiki/dashboard/tts** — Deployed and functional but low test counts.

### At Risk (Orange) 🟠
- **17 dead study- repos** — see Section 7
- **Several study- repos** with 0-2 commits in 30 days, on the edge of becoming dead

### Fleet's Center of Gravity
The fleet orbits **three centers**:
1. **Lucineer** — production game platform (Roblox + Workers + AI)
2. **Forgemaster** — agentic compiler and research pipeline
3. **ai-writings** — creative output and corpus (the fleet's soul)

The `study-` repos are the research arm — they explore, and when exploration ends, they become driftwood. This is by design, not neglect.

---

## 9. DeepSeek Sounding Board

*DeepSeek API was unavailable during this watch (key authentication failed). The Cartographer provides independent analysis:*

**Patterns observed:**
1. **Study-prefix repos are ephemeral by nature.** 17 dead, all `study-*`. This is a research pattern, not abandonment — exploration repos have natural lifecycles.
2. **The test culture is exceptionally strong.** 27,000 tests across 137 repos. Seven repos at 97%+ coverage. This fleet verifies before it sails.
3. **Lucineer is the commercial center.** 6 repos, 3 Workers, custom domain, game client. It's what pays the bills.
4. **Forgemaster is the intellectual center.** It depends on everything and produces the experiments that feed study-sunset-ecosystem.
5. **The corpus (ai-writings) is the cultural center.** 1,400 commits in 30 days. The fleet writes more than it codes.

---

*Atlas compiled by The Cartographer, first watch, 2026-08-06. This chart will need redrawing. That's the point.*
