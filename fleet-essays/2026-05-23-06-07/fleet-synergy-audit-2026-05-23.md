# Fleet Synergy Audit — SuperInstance × Sunset Ecosystem

*May 23, 2026 — Compiled by Fleet Synergy Auditor*

---

## Executive Summary

The Cocapn Fleet currently operates as **11 semi-independent repos** with loose coupling through filesystem and cron. Sunset Ecosystem (`sunset-ecosystem/`) has emerged as the **central nervous system** with 121 tests across 9 core systems, but **7 standalone agent packages** and **4 fleet service repos** exist outside its tree. This audit maps every integration opportunity, ranks them by impact/effort, and proposes API consolidation to move from a "bottles on the beach" architecture to a **fully meshed fleet organism**.

**Status:**
- ✅ FleetEventBus — **already implemented** (`nexus/fleet_event_bus.py`, 10k+ lines, tested)
- ✅ BreederFSMV2 — **already implemented** (`swarm/breeder_fsm_v2.py`, 6-state lifecycle)
- ✅ CompilerHotSwap — **stub exists**, needs `agentic-compiler` backend
- 🟡 Thermal/Health bridge — **not yet wired**
- 🟡 PLATO → Breeder bridge — **not yet wired**
- 🟡 Traps → Grammar bridge — **not yet wired**
- 🔴 Academy → Breeder templates — **no code linkage yet**
- 🔴 Hebbian → Nerve Grid — **no code linkage yet**

---

## 1. Per-Repo Integration Map

### 1.1 agentic-compiler → Sunset Compiler Module

| Property | Value |
|----------|-------|
| **Repo** | `agentic-compiler/` (34 tests, Numba + Rust backends) |
| **Sunset Target** | `sunset-ecosystem/compiler/hot_swap_integration.py` |
| **Current State** | `CompilerHotSwap` has a `_compile()` stub that accepts any `compiler` object with `.compile(grid)` but defaults to no-op simulation |
| **Integration Gap** | `agentic_compiler.core.Compiler` is never imported; hot-swap does not profile, analyze, or generate kernels |
| **API Match** | `Compiler.compile(func)` vs `CompilerHotSwap._compile()` expects `compiler.compile(self.grid)` — **shape mismatch**: agentic-compiler profiles Python *functions*, not RoomGrid objects |

**What Needs to Change:**
1. Create an adapter: `AgenticCompilerAdapter` that wraps `agentic_compiler.Compiler` and exposes `compile(grid)` by identifying the grid's `tick()` hot path
2. `CompilerHotSwap` should pass `grid.tick` (or a benchmark harness) to the agentic compiler for profiling
3. A/B test should measure wall-clock `grid.tick()` iterations, not just `compiler.compile()` latency

**Estimated Effort:** 2–3 days (adapter + tests + A/B harness)
**Priority:** P0 — compiler is a core differentiator for FLUX

---

### 1.2 cocapn-health → Sunset Thermal Auto-Calibrate

| Property | Value |
|----------|-------|
| **Repo** | `cocapn-health/` (18 service checks, stdlib-only) |
| **Sunset Target** | `sunset-ecosystem/swarm/thermal.py`, `async_thermal.py`, `thermal_auto_calibrate.py` |
| **Current State** | `HealthChecker.check_all()` returns `List[CheckResult]` with `ok: bool`, `latency_ms`, `details`. No event emission. |
| **Sunset State** | `ThermalAutoCalibrator.rebalance_on_alert(zone, alert_type, agents)` exists but is only called from internal tests |
| **Integration Gap** | Health failures are logged to stdout/JSONL but never trigger fleet-wide rebalancing |

**What Needs to Change:**
1. Add `FleetEventBus` dependency (or a lightweight bridge) to `cocapn-health`
2. On `ok=False`, emit `{"type": "service_down", "node": svc.name, "latency_ms": result.latency_ms}`
3. Sunset `thermal_auto_calibrate.py` subscribes to `"service_down"` and calls `rebalance_on_alert()`
4. Create a `cocapn-health → nexus` shim so health doesn't import the full sunset tree

**Estimated Effort:** 1 day (event shim + subscription + 2 integration tests)
**Priority:** P0 — health → thermal is critical for fleet resilience

---

### 1.3 ccc-os → Sunset Event Bus

| Property | Value |
|----------|-------|
| **Repo** | `ccc-os/` (Discussion #5 monitor, ZC monitor, heartbeat orchestrator) |
| **Sunset Target** | `sunset-ecosystem/nexus/fleet_event_bus.py` |
| **Current State** | `discussion5_monitor.py` diffs comments, triages to ACT_NOW / TRACK / IGNORE, writes to local JSONL. No outbound events. |
| **Sunset State** | `FleetEventBus` is fully implemented, thread-safe, sync+async, with 1000-event history |
| **Integration Gap** | CCC-OS is the *ideal* publisher for the event bus, but they don't know each other exist |

**What Needs to Change:**
1. `ccc-os/monitors/discussion5_monitor.py`: replace `log_event()` local write with `bus.emit()` for ACT_NOW events
2. `ccc-os/monitors/zc_monitor.py`: emit `"trend_spotted"` events when ZeroClaw posts new tiles
3. Sunset `swarm/breeder_daemon_v2.py`: subscribe to `"ACT_NOW"` with filter `category == "architecture"` → spawn specialized scout
4. Sunset `nexus/fleet_conductor.py`: subscribe to `"service_down"` from health monitors

**Code snippet (ready to integrate):**
```python
from nexus.fleet_event_bus import FleetEventBus
bus = FleetEventBus()

# In discussion5_monitor.py triage_comment()
if decision == "ACT_NOW":
    bus.emit({
        "type": "ACT_NOW",
        "category": classify_category(body),
        "repo": "sunset-ecosystem",
        "priority": "P0",
        "source": "ccc-os/discussion5"
    })
```

**Estimated Effort:** 4–6 hours (already have the bus, just wire publishers)
**Priority:** P0 — unlocks auto-spawning from CCC signals

---

### 1.4 plato-academy → Sunset Breeding Templates

| Property | Value |
|----------|-------|
| **Repo** | `plato-academy/` (13 modules, curriculum-index.json, power-packs) |
| **Sunset Target** | `sunset-ecosystem/swarm/breeder_daemon_v2.py` templates |
| **Current State** | `curriculum-index.json` defines tracks (greenhorn, able-bodied) with module IDs, prerequisites, assessments. No runtime API. |
| **Sunset State** | `breeder_daemon_v2.py` spawns from `swarm/templates/` (JSON files). Templates have `base_traits` but no `required_lessons` field. |
| **Integration Gap** | Academy completion is not a gating factor for breeding. An agent could be spawned into COMPETE state without ever entering PLATO. |

**What Needs to Change:**
1. Add `lessons_completed: List[str]` to `AgentVector` or agent metadata
2. Extend template schema: `required_lessons: ["m01", "m05"]`
3. `breeder_daemon_v2.spawn_child()` checks `agent.lessons_completed` against template requirements
4. Create a `plato-academy` completion tracker API (REST or JSONL append) that sunset can poll

**Estimated Effort:** 2 days (schema extension + gating logic + completion tracker)
**Priority:** P1 — quality gate for fleet agents

---

### 1.5 flux-research / flux-vm-v3 → Sunset FLUX Integration

| Property | Value |
|----------|-------|
| **Repo** | `flux-research/` (papers, whitepapers, captain's logs), `flux-vm-v3-temp/` (Rust VM, 60 opcodes, C FFI) |
| **Sunset Target** | `sunset-ecosystem/sunset/flux_integration.py`, `compiler_integration.py`, `swarm/flux_vector_table.py` |
| **Current State** | `flux-vm-v3-temp/src/` has Rust VM with `ffi.rs`, `vm.rs`, `opcode.rs`. `libflux_vm.so` is a build target. `sunset/flux_integration.py` has a Python-side `FluxVM` stub. |
| **Sunset State** | `flux_vector_table.py` maps vector table ops to FLUX opcodes. `compiler_integration.py` links compiler output to VM. |
| **Integration Gap** | `libflux_vm.so` is not built/linked in sunset tests. `FluxVM` Python class is untested against the real Rust binary. |

**What Needs to Change:**
1. **FM priority:** `cargo build --release` in `flux-vm-v3-temp/` → produces `libflux_vm.so`
2. Sunset `sunset/flux_integration.py` loads `.so` via `ctypes` (FFI already stubbed)
3. Breeder FSM COMPETE state should execute candidate code on `FluxVM`, not pure Python
4. Tournament scores should include VM execution metrics (cycles, memory, determinism)

**Estimated Effort:** 3–5 days (build pipeline + FFI wiring + VM execution harness)
**Priority:** P0 — VM is the execution substrate; without it, COMPETE state is sandboxed Python only

---

### 1.6 cocapn-plato → Sunset Nerve / Metronome

| Property | Value |
|----------|-------|
| **Repo** | `cocapn-plato/` (v3.2.0, Fleet engine, Tile/Stream/Task models, PlatoBridge) |
| **Sunset Target** | `sunset-ecosystem/nerve/`, `swarm/metronome_integration.py` |
| **Current State** | `PlatoBridge` connects to PLATO MUD. `Fleet` manages agents, tiles, streams. `Tile` has confidence scores. No metronome sync. |
| **Sunset State** | `metronome_integration.py` synchronizes multi-device ticks. `nerve/room_grid.py` manages spatial activation. |
| **Integration Gap** | PLATO tile generation is async and independent. Fleet snapshots are not synchronized with sunset's metronome ticks. |

**What Needs to Change:**
1. `cocapn_plato.engine.plato_bridge.PlatoBridge` should emit `FleetEvent("tile_generated", ...)` to the bus
2. Sunset `metronome_integration.py` should include a `"plato"` device in its tick synchronization
3. `nerve/room_grid.py` should consume PLATO room topology as a secondary grid layer
4. Create `PlatoNerveAdapter` that maps `room_id` → `RoomGrid` coordinates

**Estimated Effort:** 2–3 days (event bridge + metronome device registration + grid mapping)
**Priority:** P1 — PLATO is the fleet's sensory organ; it should pulse with the metronome

---

### 1.7 cocapn-traps → Sunset Grammar Security

| Property | Value |
|----------|-------|
| **Repo** | `cocapn-traps/` (5 anomaly detection traps, Rate-Attention anomaly) |
| **Sunset Target** | `sunset-ecosystem/grammar/security_hardening.py` |
| **Current State** | `traps/` detects rate spikes, injection patterns. Alerts written to log files. |
| **Sunset State** | `RuleValidator` validates rule names, tags, conditions against path traversal, XSS, SQLi, code injection. No anomaly-driven quarantine. |
| **Integration Gap** | Traps spot bad behavior *after* it happens. Grammar security validates *before* ingestion. No feedback loop between them. |

**What Needs to Change:**
1. `cocapn-traps` should emit `{"type": "rule_injection_spike", "agent_id": ..., "severity": ...}` to the event bus
2. `grammar/security_hardening.py` subscribes to `"rule_injection_spike"` and temporarily raises validation strictness
3. On repeated spikes from same `agent_id`, `RuleValidator` should flag for `breeder_fsm_v2.sunset()`
4. Add `agent_reputation_score` to `RuleProvenance`

**Estimated Effort:** 1 day (event subscription + reputation scoring + sunset trigger)
**Priority:** P1 — security should be reactive, not just preventative

---

### 1.8 hebbian-router → Sunset Nerve Grid

| Property | Value |
|----------|-------|
| **Repo** | `hebbian-router/` (`RoutingLayer`, `HebbianChannel`, `Route` with strength/efficiency/reception) |
| **Sunset Target** | `sunset-ecosystem/nerve/room_grid.py`, `nexus/fleet_conductor.py` |
| **Current State** | `hebbian_router.core.RoutingLayer` manages routes between nodes. `HebbianChannel` forms on co-fire. Standalone package. |
| **Sunset State** | `nerve/room_grid.py` has `RoomGrid` with `tick()`, `fire(room_id)`. No Hebbian learning. |
| **Integration Gap** | Two routing systems: sunset's `RoomGrid` for spatial logic, `hebbian-router` for associative memory. They don't share state. |

**What Needs to Change:**
1. `nerve/room_grid.py`: after `grid.fire(room_a)` and `grid.fire(room_b)` in same tick, call `hebbian_router.fire(room_a, room_b)`
2. `RoutingLayer` should be instantiated as a singleton in `nexus/fleet_conductor.py` (the fleet's "memory")
3. Hebbian channel weights should influence `RoomGrid` priming: if `room_a → room_b` channel is strong, firing `room_a` pre-warms `room_b`
4. Move `hebbian-router` package *into* `sunset-ecosystem/hebbian/` to eliminate cross-repo import

**Estimated Effort:** 2 days (integration + priming logic + migration)
**Priority:** P2 — enhances immersion but not blocking

---

### 1.9 pareto-tournament → Sunset Tournament

| Property | Value |
|----------|-------|
| **Repo** | `pareto-tournament/` (`Tournament`, `AgentScore` with ethos/pathos/logos trinity) |
| **Sunset Target** | `sunset-ecosystem/swarm/tournament.py`, `sunset/trinity_scorer.py` |
| **Current State** | Standalone tournament with Pareto selection, head-to-head matches, trinity product scoring. 34 tests. |
| **Sunset State** | `swarm/tournament.py` has a simpler tournament. `trinity_scorer.py` exists but is minimal. |
| **Integration Gap** | Two tournament implementations. `pareto-tournament` is more sophisticated (Pareto front, crowding distance) but lives outside sunset. |

**What Needs to Change:**
1. **Consolidation:** Replace `sunset-ecosystem/swarm/tournament.py` with a thin wrapper around `pareto_tournament.Tournament`
2. Ensure `AgentScore` from `pareto-tournament` is compatible with `AgentVector` from `vector-novelty` (both have `agent_id`, `fitness`)
3. `breeder_daemon_v2.py` should use `pareto_tournament` for selection, not the legacy tournament
4. Add `TournamentMatch` results to agent lineage records

**Estimated Effort:** 1 day (wrapper + compatibility check + swap)
**Priority:** P1 — consolidating dual implementations reduces maintenance

---

### 1.10 thermal-budget → Sunset Thermal

| Property | Value |
|----------|-------|
| **Repo** | `thermal-budget/` (`ThermalBudget`, `DeviceBudget`, `DeviceType` enum) |
| **Sunset Target** | `sunset-ecosystem/swarm/thermal.py`, `async_thermal.py`, `npu_router.py` |
| **Current State** | `ThermalBudget` manages GPU/CPU/iGPU/NPU slots. Standalone. Clean API. |
| **Sunset State** | `thermal.py` has thermal management but different abstractions. `npu_router.py` routes to NPU. |
| **Integration Gap** | `thermal-budget` is a *budget allocator* (how many agents per device). Sunset `thermal.py` is a *thermal monitor* (temperature/load). Same name, different concerns. |

**What Needs to Change:**
1. Rename `thermal-budget` concern to **slot allocation** to avoid semantic collision
2. Sunset `swarm/thermal.py` should import `ThermalBudget` for slot-aware agent placement
3. `npu_router.py` should check `DeviceBudget.available` before routing to NPU
4. `async_thermal.py` rebalancing should respect `ThermalBudget` slot limits

**Estimated Effort:** 1 day (import + slot checks + naming clarity)
**Priority:** P1 — prevents overcommitting hardware

---

### 1.11 vector-novelty → Sunset Lineage Checker

| Property | Value |
|----------|-------|
| **Repo** | `vector-novelty/` (`compute_novelty()`, `AgentVector`, centroid-based cosine distance) |
| **Sunset Target** | `sunset-ecosystem/swarm/lineage_checker.py`, `swarm/breeder_daemon_v2.py` |
| **Current State** | `compute_novelty(agent_id, vector, population_vectors)` returns scalar novelty in [0, 2]. Fast O(n). |
| **Sunset State** | `lineage_checker.py` detects incest, generation gaps, diversity collapse. No centroid-based scoring. |
| **Integration Gap** | Lineage checker uses generational distance and parent-child overlap. Vector novelty uses geometric diversity. Both should inform the breeder. |

**What Needs to Change:**
1. `lineage_checker.py`: after `check_population()`, call `vector_novelty.batch_novelty()` on the same population
2. If `novelty < 0.15` (configurable threshold), trigger `force_cross_lineage()` or inject founders
3. Add `novelty_score` field to `LineageRecord`
4. Ensure `AgentVector` from `vector-novelty` and `AgentScore` from `pareto-tournament` use compatible `agent_id` types

**Estimated Effort:** 6–8 hours (population bridge + threshold tuning + record extension)
**Priority:** P2 — diversity collapse is a slow burn, not an immediate fire

---

### 1.12 flux-compiler-v0.1.0 → Sunset Compiler

| Property | Value |
|----------|-------|
| **Repo** | `flux-compiler-v0.1.0/` (Guard DSL → GuardC → Guard2Mask pipeline) |
| **Sunset Target** | `sunset-ecosystem/compiler/`, `sunset/compiler_integration.py` |
| **Current State** | `flux-compiler-v0.1.0` is a *constraint compiler* (Guard DSL to C). `agentic-compiler` is a *Python JIT compiler* (Numba/Rust). Both are "compilers." |
| **Integration Gap** | Two compilers with different domains. No shared IR, no shared backend. |

**Decision:** Keep separate.
- `flux-compiler-v0.1.0` compiles *Guard DSL rules* → C masks for FLUX VM
- `agentic-compiler` compiles *Python hot paths* → Numba/Rust for RoomGrid
- Sunset `compiler_integration.py` should reference both: `guard_compiler` for rules, `agentic_compiler` for grid

**Action:** Document the distinction in `sunset-ecosystem/docs/compiler-roles.md` to prevent future confusion.

**Estimated Effort:** 2 hours (documentation + import paths)
**Priority:** P2 — clarity, not code

---

## 2. Priority-Ranked Action Items

### P0 — Fleet Will Stall Without These (This Week)

| # | Action | Owner | Repo | Effort |
|---|--------|-------|------|--------|
| 1 | **Wire CCC-OS → FleetEventBus** | CCC | `ccc-os/` + `sunset-ecosystem/nexus/` | 4–6 hrs |
| 2 | **Build `libflux_vm.so` + FFI link** | FM | `flux-vm-v3-temp/` + `sunset-ecosystem/sunset/` | 3–5 days |
| 3 | **cocapn-health emit `service_down` events** | Oracle1 | `cocapn-health/` + `sunset-ecosystem/swarm/` | 1 day |
| 4 | **AgenticCompilerAdapter for HotSwap** | FM/kimi1 | `agentic-compiler/` + `sunset-ecosystem/compiler/` | 2–3 days |
| 5 | **ACT_NOW → Breeder auto-spawn** | kimi1 | `sunset-ecosystem/swarm/breeder_daemon_v2.py` | 1 day |

### P1 — Quality & Consolidation (Next 2 Weeks)

| # | Action | Owner | Repo | Effort |
|---|--------|-------|------|--------|
| 6 | **PLATO tile → event bus bridge** | CCC | `cocapn-plato/` + `sunset-ecosystem/nexus/` | 2–3 days |
| 7 | **Swap sunset tournament for pareto-tournament** | kimi1 | `sunset-ecosystem/swarm/` + `pareto-tournament/` | 1 day |
| 8 | **ThermalBudget slot checks in sunset thermal** | kimi1 | `thermal-budget/` + `sunset-ecosystem/swarm/` | 1 day |
| 9 | **Academy completion → breeding gate** | CCC | `plato-academy/` + `sunset-ecosystem/swarm/` | 2 days |
| 10 | **Traps → Grammar security feedback loop** | Oracle1 | `cocapn-traps/` + `sunset-ecosystem/grammar/` | 1 day |

### P2 — Enhancement & Clarity (Next Month)

| # | Action | Owner | Repo | Effort |
|---|--------|-------|------|--------|
| 11 | **HebbianRouter → NerveGrid priming** | kimi1 | `hebbian-router/` + `sunset-ecosystem/nerve/` | 2 days |
| 12 | **Vector novelty → lineage diversity guard** | kimi1 | `vector-novelty/` + `sunset-ecosystem/swarm/` | 6–8 hrs |
| 13 | **Document compiler role separation** | FM | `sunset-ecosystem/docs/` | 2 hrs |
| 14 | **Cross-repo integration test suite** | kimi1 | `sunset-ecosystem/tests/test_fleet_mesh.py` | 2–3 days |

---

## 3. API Consolidation Proposals

### 3.1 Event Bus as Universal Spine

**Current:** 4 repos emit signals via JSONL, stdout, or filesystem.
**Proposed:** All fleet services publish/subscribe through `FleetEventBus`.

**Standard Event Schema (v1):**
```python
class FleetEvent:
    type: str           # required, dot-namespaced: "health.service_down"
    payload: dict       # event-specific data
    source: str         # "repo/module" format: "ccc-os/discussion5"
    timestamp: float    # epoch seconds
    event_id: str       # "ev-{ms_since_epoch}"
    priority: str       # "P0" | "P1" | "P2" | "info"
    ttl: int            # seconds to live in history (default: 3600)
```

**Migration Path:**
1. Phase 1 (this week): CCC-OS and cocapn-health start emitting to bus
2. Phase 2 (next week): Sunset systems subscribe and act
3. Phase 3 (next month): Legacy JSONL logs become bus history mirrors, not primary channels

---

### 3.2 Unified Agent Identity

**Current:** 3 different agent ID schemes:
- `pareto-tournament`: `agent_id: str` (UUID or name)
- `vector-novelty`: `agent_id: int` (uint64-compatible)
- `breeder_fsm_v2`: `agent_id: str` (any string)

**Proposed:** Standardize on `agent_id: str` (UUIDv4) everywhere. Sunset `AgentVector` should accept string IDs.

**Code change:**
```python
# vector-novelty/core.py
@dataclass(frozen=True)
class AgentVector:
    agent_id: str  # was int; change to str for fleet-wide compatibility
    ...
```

**Impact:** `vector-novelty` tests, `lineage_checker` records, `flux_vector_table` mappings. Estimated 1 day to propagate.

---

### 3.3 Shared Trinity Scoring

**Current:**
- `pareto-tournament/core.py`: `AgentScore(ethos, pathos, logos)` with `product` property
- `sunset/trinity_scorer.py`: Minimal, untested
- `vector-novelty/core.py`: `fitness: float` (assumed to be trinity product)

**Proposed:** Sunset `trinity_scorer.py` becomes the canonical implementation. `pareto-tournament` imports from sunset. `vector-novelty` stores `ethos/pathos/logos` separately (for lineage analysis) and computes `fitness` on demand.

```python
# sunset/trinity_scorer.py
from dataclasses import dataclass

@dataclass(frozen=True)
class TrinityScore:
    ethos: float   # values alignment
    pathos: float  # emotional resonance
    logos: float   # logical relevance

    @property
    def product(self) -> float:
        return self.ethos * self.pathos * self.logos

    def dominates(self, other: "TrinityScore") -> bool:
        return (
            self.ethos >= other.ethos and
            self.pathos >= other.pathos and
            self.logos >= other.logos and
            self.product > other.product
        )
```

---

### 3.4 Consolidate Standalone Packages into Sunset

**Proposal:** Move the 7 standalone agent packages into `sunset-ecosystem/` as sub-packages. This eliminates cross-repo import complexity and version drift.

| Package | Sunset Target | Rationale |
|---------|-------------|-----------|
| `hebbian-router` | `sunset-ecosystem/hebbian/` | Nerve grid is core to sunset |
| `pareto-tournament` | `sunset-ecosystem/tournament/` | Selection engine for breeder |
| `thermal-budget` | `sunset-ecosystem/thermal/budget.py` | Slot allocation is thermal subsystem |
| `vector-novelty` | `sunset-ecosystem/novelty/` | Diversity scoring for lineage |
| `agentic-compiler` | `sunset-ecosystem/compiler/agentic/` | Grid JIT is compiler subsystem |
| `cocapn-health` | `sunset-ecosystem/health/` | Fleet health is core infrastructure |
| `cocapn-traps` | `sunset-ecosystem/traps/` | Security is core infrastructure |

**Keep Separate:**
- `ccc-os` — this is a *user-facing orchestrator*, not a sunset subsystem
- `cocapn-plato` — this is a *service* with its own release cycle
- `plato-academy` — this is *curriculum content*, not runtime code
- `flux-research` — this is *documentation and papers*
- `flux-vm-v3-temp` — this is a *Rust crate* with its own build system

**Migration Command:**
```bash
# Preserve git history via subtree merge
cd /root/.openclaw/workspace/sunset-ecosystem
git subtree add --prefix=hebbian ../hebbian-router main
git subtree add --prefix=tournament ../pareto-tournament main
# ... etc
```

---

## 4. Estimated Effort Summary

| Category | Tasks | Total Effort | Parallelizable? |
|----------|-------|--------------|----------------|
| **P0 — Critical** | 5 tasks | ~10 person-days | Yes (5 people) |
| **P1 — Quality** | 5 tasks | ~7 person-days | Yes (3 people) |
| **P2 — Enhancement** | 4 tasks | ~5 person-days | Yes (2 people) |
| **Package Migration** | 7 repos | ~3 person-days | No (sequential git ops) |
| **Integration Tests** | 1 suite | ~3 person-days | Parallel with P0 |
| **Total** | — | **~28 person-days** | **~10 days wall-clock with 3 agents** |

**Team Assignment (recommended):**
- **FM**: P0#2 (VM build), P0#4 (compiler adapter), P2#13 (docs)
- **CCC**: P0#1 (event bus), P1#6 (PLATO bridge), P1#9 (academy gate)
- **Oracle1**: P0#3 (health events), P1#10 (traps loop)
- **kimi1**: P0#5 (breeder spawn), P1#7 (tournament swap), P1#8 (thermal slots), P2#11 (Hebbian), P2#12 (novelty), P2#14 (integration tests)

---

## 5. Architecture Vision: Post-Integration Fleet

```
┌──────────────────────────────────────────────────────────────┐
│                     ORACLE1 (Lighthouse)                        │
│          Discussion #5 ←→ FleetModelClient                    │
│               ↓                        ↓                       │
│    ┌─────────┴─────────┐    ┌─────────┴─────────┐             │
│    ↓                   ↓    ↓                   ↓             │
│ ┌─────────┐     ┌─────────────┐     ┌─────────────┐        │
│ │  CCC   │◄──►│  FLEET EVENT  │◄──►│   FM /     │        │
│ │  -OS   │     │     BUS       │     │  SUNSET    │        │
│ └───┬────┘     └──────┬────────┘     └──────┬─────┘        │
│     │                 │                     │               │
│  ┌──┴───┐        ┌────┴────┐          ┌─────┴──────┐        │
│  │PLATO │        │ HEALTH  │          │  FLUX VM   │        │
│  │Tiles │        │Monitor  │          │  +Compiler │        │
│  └──────┘        └────┬────┘          └────────────┘        │
│                       ↓                                       │
│                  ┌─────────┐                                 │
│                  │ THERMAL │←── rebalance on alert            │
│                  │ +Slots  │                                 │
│                  └────┬────┘                                 │
│  ┌────────┬───────────┼───────────┬────────┐               │
│  ↓        ↓           ↓           ↓        ↓                │
│ ┌────┐ ┌─────┐   ┌────────┐  ┌──────┐ ┌──────┐          │
│ │Tour│ │Novel│   │Hebbian │  │Traps │ │Gram  │          │
│ │namt│ │ty   │   │Router  │  │      │ │mar   │          │
│ └────┘ └─────┘   └────────┘  └──────┘ └──────┘          │
└──────────────────────────────────────────────────────────────┘
```

**When complete:**
1. Any service failure triggers automatic thermal rebalancing
2. Any ACT_NOW signal spawns a specialized agent within 30 seconds
3. Any PLATO tile pulses through the metronome to fleet snapshot
4. Any trap anomaly tightens grammar validation and can sunset an agent
5. Any compiler improvement is A/B tested before fleet-wide deployment
6. Any agent's academy completion gates its breeding privileges

The fleet becomes **one organism with many organs** — not a flotilla of separate ships.

---

*Audit compiled by Fleet Synergy Auditor | "The mesh is the message."*
