# Fleet Architecture Omnibus

> **Date:** 2026-06-16 06:14 UTC  
> **Author:** Oracle2  
> **Source:** Analysis of 14 Forgemaster repos + 6 Oracle2/colony repos  
> **Status:** First draft — ground truth for all integration work

---

## A. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     SUPERINSTANCE FLEET — DATA FLOW                      │
└─────────────────────────────────────────────────────────────────────────┘

COLONY LAYER (Python, empirical)                        INFRASTRUCTURE LAYER
┌───────────────────────┐                              ┌─────────────────────┐
│ colony-games.py       │   raw JSON                    │ fleet-dashboard-api │
│ 6 games + Mafia       │─────────────────────────────> │ (CF Worker)         │
│   ↓ game results      │                               │   ↑  dashboard.html │
│   ↓ cell states       │                               └──────┬──────────────┘
│  ┌─────────────────┐  │  9-channel profiles via             │
│  │ colony_conservation│ │  colony_conservation_scorer()      │
│  │ _scorer.py       │──┼─────────────────────────────────>  │
│  │ 9-channel intent │  │                                     │
│  └────────┬─────────┘  │                                     │
│           │            │                                     │
│           │ Bottle (JSON + base64 msgpack)                    │
│           ▼            │                                     │
│  ┌─────────────────┐  │                                     │
│  │ superinstance_   │  │  POST /conservation/score           │
│  │ bottle.py        │──┼─────────────────────────────────>  │
│  │ encode/decode    │  │   POST /conservation/pulse          │
│  │ conservation     │  │                                     │
│  │ audit()          │  │                                     │
│  └────────┬─────────┘  │                                     │
│           │            │                                     │
│           │ Bottles via :8797                                  │
│           ▼            │                                     │
│  ┌─────────────────┐  │                                     │
│  │ conservation_   │  │   bridge to dash_relay               │
│  │ runtime.py      │──┼─────────────────────────────────>  │
│  │ (:8797)         │  │                                     │
│  │ score/verify/   │  │                                     │
│  │ pulse/health    │  │                                     │
│  └────────┬─────────┘  │                                     │
│           │            │                                     │
└───────────┼────────────┘                                     │
            │ Bottle wire format                                │
            ▼                                                    │
┌──────────────────────────────────────────────────────────────────┤
│ TERNARY MATH LAYER (Rust, computational)                       │
│                                                                │
│ superinstance-protocol  ── Canonical Bottle format             │
│   src/lib.rs: Bottle { id, ver, src, tgt, act, trits, ... }    │
│   src/types.ts: TypeScript mirror + uuidv7                     │
│        ↑                                                      │
│ ternary-fleet-integration ── Bottle ↔ AggregateResult bridge  │
│   src/ternary_aggregator.rs: Aggregate ternary voting          │
│   src/bin/dash_relay.rs: axum relay (port 8790)               │
│   src/fleet_types.rs: FleetMetrics, AgentHeartbeat types       │
│        ↑                                                      │
│ ternary-route ── Ternary routing with load balancing           │
│ ternary-pid ── PID controller for fleet governance             │
│ ternary-entropy ── Shannon entropy on ternary distributions    │
│ ternary-hamiltonian ── Hamiltonian phase-space mechanics       │
│ ternary-rhythm ── Rhythmic scheduler for pulse timing          │
│ ternary-svm ── Ternary support vector machine                  │
│ ternary-search-rs ── Vector search (needs tests)              │
│ ternary-conserve ── Resource conservation with γ+η=C          │
│ ternary-fleet-packing ── Ternary data compression (4 schemes)  │
│        ↓                                                      │
│ conservation-languages ── γ+η=C in 9+ languages               │
│   python/verify.py: verify_conservation(bottles)              │
│   c/verify.c, rust/src/lib.rs, fortran/, cobol/, elixir/      │
│        ↓                                                      │
│ conservation-action ── GitHub Action for CI/CD                │
│   action.yml: runs verify.py on PRs / pushes                  │
│   enforces Σtrits conservation                                 │
│        ↓                                                      │
│ delta-clt ── CLT cancellation theorem proof                   │
│   delta_clt.py: δ(n) numerical verification                    │
│   nine_channel_scorer.py: 9-dim intent profiles                │
│   live_experiment.py: LLM agent experiments                    │
│   experiment-results.json: empirical data                      │
│   dashboard.html: visualization                                │
└─────────────────────────────────────────────────────────────────┘
```

### Layer Summary

| Layer | Ownership | Implementation | How it connects |
|-------|-----------|---------------|-----------------|
| **Colony** | Oracle2 | Python (colony-games.py) | Raw HTTP JSON → needs Bottle wrapping |
| **Bridge** | Oracle2 → Forgemaster | Python (superinstance_bottle.py, conservation-runtime) | Bottle format on :8797 |
| **Math** | Forgemaster | Rust (ternary-*, superinstance-protocol) | Crate dependencies + wire format |
| **Distribution** | Forgemaster | crates.io, npm | `cargo publish`, CI/CD |
| **Verification** | Forgemaster | Python (conservation-languages) | CI gate on GitHub Actions |
| **Infrastructure** | Both/DocBot | CF Workers, dashboard | REST API from fleet-dashboard-api |

---

## B. Gap Inventory

### HIGH Impact — Blocks everything else

| # | Gap | A → B | What should flow | Why blocked | Fix |
|---|------|-------|-----------------|-------------|-----|
| G1 | **No crate author token** | crates.io → fleet | Publish 4 ready crates | `CARGO_REGISTRY_TOKEN` unset | Forgemaster: `cargo login` on ProArt |
| G2 | **No CF API Token** | Cloudflare → fleet | Deploy colony edge + pulse worker | No API token | Generate Workers-capable token |
| G3 | **No bottle wire format in colony** | colony-games → protocol | Game results as Bottles | colony emits raw JSON | Add Bottle.new() wrapping in game server |
| G4 | **No conservation verification runtime** | colony → conservation-action | Verify Σtrits per game round | No bridge service | Deploy conservation-runtime.py on :8797 |
| G5 | **No nine-channel scoring in colony** | colony → delta-clt | Cell behavioral profiles → 9 channels | Scorer exists but isn't called | Hook colony_conservation_scorer into game pipeline |

### MEDIUM Impact — Adds value but not blocking

| # | Gap | A → B | What should flow | Why blocked | Fix |
|---|------|-------|-----------------|-------------|-----|
| G6 | **No CI/CD on ternary-fleet-integration** | repo → GitHub Actions | Auto-test on push | No conservation-action wiring | Add `.github/workflows/` |
| G7 | **No TypeScript protocol client** | TS apps → Bottles | JavaScript/Node apps can't speak Bottle | No TypeScript mirror of superinstance_bottle.py | Write `superinstance-bottle-client.ts` |
| G8 | **baton-system repo is 404** | fleet planning references it | Does not exist | Missing git repo | Create the repo or deprecate reference |
| G9 | **No colony games → fleet dashboard** | colony → fleet-dashboard-api | Live game metrics to dashboard | No metrics endpoint | Add `POST /fleet/metrics` in conservation-runtime |
| G10 | **No cross-arch scaling numbers** | ARM64 (this box) → ProArt | Cell capacity difference | Need Forgemaster to run at scale | ProArt test with 1000+ cells |

### LOW Impact — Nice to have

| # | Gap | A → B | What should flow | Why blocked | Fix |
|---|------|-------|-----------------|-------------|-----|
| G11 | **No badges in Cargo.toml** | crates listing | Better crate presentation | Missing [badges] sections | Add badge URLs |
| G12 | **Broken build: ternary-rhythm** | neon-kernel dep missing | Can't compile/cargo-check | Missing path or git dep | Fix dep resolution |
| G13 | **Broken build: ternary-conserve** | ternary-types dep missing | Can't compile | Same issue | Fix dep resolution |
| G14 | **Broken build: ternary-svm** | CLI binary broken | Library OK, CLI can't build | Missing dep | Remove or fix CLI binary |

---

## C. Top 5 Builds (Ordered by Dependency)

### Build 1: Conservation Runtime 🏆 **IMMEDIATE PRIORITY**

**What it is:** A small HTTP daemon on port 8797 that accepts raw colony data, wraps in Bottles, and verifies conservation.

**Implementation:**
- `conservation-runtime.py` — Python http.server, 4 endpoints
- Imports: `superinstance_bottle.Bottle`, `colony_conservation_scorer.score_cell_from_ledger`
- Endpoints: `POST /conservation/score`, `POST /conservation/verify`, `GET /conservation/health`, `POST /conservation/pulse`
- Status: PARTIALLY DONE — superinstance_bottle.py and colony_conservation_scorer.py exist

**Files to modify:** Write `conservation-runtime.py` (new)

### Build 2: Colony Games → Bottle Wrapping

**What it is:** Hook game results through the protocol client before emitting responses.

**Implementation:**
- In `colony-games.py`, after each game round: `bottle = Bottle.new(src="colony-games", tgt="fleet-pulse", act="game.pd.round", trits=<conserved charge>, payload=round_data)`
- POST to conservation-runtime at localhost:8797
- Cache the conservation pass/fail in game response

**Files to modify:** `colony-games.py` → add Bottle import + POST after each round

### Build 3: TypeScript Protocol Client

**What it is:** A browser/frontend-compatible Bottle client for the fleet dashboard.

**Implementation:**
- `superinstance-bottle-client.ts` — mirror of superinstance_bottle.py in TypeScript
- Implements: `Bottle.encode()`, `Bottle.decode()`, `audit()`, `uuidv7()`, `BottleClient` REST class
- Uses `msgpack` library via npm (or base64 + JSON manual encoding)

**Files to write:** `superinstance-bottle-client.ts` + integration into fleet-dashboard

### Build 4: Fleet Pulse Integration

**What it is:** The conservation-runtime pulses to dash_relay (port 8790) at colony-pulse cadence.

**Implementation:**
- The `POST /conservation/pulse` endpoint ships fleet efficiency metrics as a Bottle to the dash_relay axum server
- dash_relay already exists at `ternary-fleet-integration/src/bin/dash_relay.rs`
- Format: `Bottle.new(trits=[γ_sign, η_sign, total_sign], payload=FleetMetrics)`

**Files to modify:** `conservation-runtime.py` + `ternary-fleet-integration/src/bin/dash_relay.rs`

### Build 5: Nine-Channel Cell Dashboard

**What it is:** A live dashboard showing each colony cell's 9-channel profile, role classification, and edge alignment matrix.

**Implementation:**
- Read colony game reputation ledger → score all cells via `colony_conservation_scorer`
- Render: 9-channel radar per cell, edge alignment heatmap, role classification badges
- Serve from conservation-runtime at `/dashboard`

**Files to write:** Embedded HTML in conservation-runtime, or standalone HTML page

---

## D. Colony-to-Protocol Pipeline (Step by Step)

### Current pipeline (no conservation):
```
colony-games.py  ──raw JSON──>  game response to player
```

### Target pipeline (with conservation):
```
colony-games.py game round
  │
  ▼
1. Collect scores dict from round_robin()
  │ dict {cell_id: score}
  ▼
2. Build conservation charge from scores
   charge = Σ sign(score) per cell
   # Map to trits: positive=+1, neutral=0, negative=-1
   trits = [1 if s > avg else -1 if s < avg else 0 for s in scores.values()]
  │
  ▼
3. Wrap in Bottle
   bottle = Bottle.new(
       src="colony-games",
       tgt="conservation-runtime",
       act="game.pd.round",
       trits=trits[:10],  # max 10 trits
       payload={
           "game": "pd",
           "round": n,
           "scores": scores,
           "strategies": {c.id: c.strategy for c in population},
       },
       ttl=30,
   )
  │
  ▼
4. POST to conservation runtime at :8797
   POST /conservation/verify
   Body: bottle.encode()
  │
  ▼
5. Conservation runtime decodes bottle, computes Σtrits
   The runtime sends to conservation-languages verify.py:
     python3 verify.py --bottle <bottle-json> --expect <charge>
  │
  ▼
6. If pass: return enriched response with conservation header
   If fail: return warning + conservation violation details
```

### Example code:

```python
# In colony-games.py, after PD round-robin:
from superinstance_bottle import Bottle, ConservationError
import requests

def wrap_and_verify(scores, round_n, population):
    avg_score = sum(scores.values()) / max(len(scores), 1)
    trits = []
    for cell_id in sorted(scores.keys()):
        s = scores[cell_id]
        trits.append(1 if s > avg_score else -1 if s < avg_score else 0)

    bottle = Bottle.new(
        src="colony-games",
        tgt="conservation-runtime",
        act="game.pd.round",
        trits=trits,
        payload={
            "round": round_n,
            "scores": scores,
            "generation": population[0].get("generation", 0),
        },
        ttl=30,
    )

    # POST and verify
    try:
        resp = requests.post(
            "http://localhost:8797/conservation/verify",
            data=bottle.encode(),
            headers={"Content-Type": "application/octet-stream"},
            timeout=5,
        )
        result = resp.json()
        if not result.get("conserved", False):
            print(f"⚠️ Conservation violation at round {round_n}")
    except ConnectionError:
        pass  # Offline mode — conservation runtime not required

    return bottle
```

---

## E. Deployment Readiness

### Publishable IMMEDIATELY (4 crates — need only `cargo login`)

| Crate | Version | Lines | Tests | Metadata Status | Blockers |
|-------|---------|-------|-------|----------------|----------|
| `ternary-route` | 0.1.0 | 213 | 8 | ✅ Complete | None — repo + license + desc + categories all set |
| `ternary-pid` | 0.1.0 | 230 | 9 | ✅ Complete | None |
| `ternary-entropy` | 0.1.1 | 483 | 24 | ✅ Complete | None (zero deps) |
| `ternary-hamiltonian` | 0.1.0 | 788 | 30 | ⚠️ Needs minor fixes | Missing description, categories |

### Need Fixes First (3 crates with broken builds)

| Crate | Issue | Fix Required |
|-------|-------|-------------|
| `ternary-conserve` | Missing `ternary-types` path dep | Add `ternary-types` git dep or path |
| `ternary-rhythm` | Missing `neon-kernel` dep | Add dep or remove dependency |
| `ternary-svm` | CLI binary missing deps | Fix binary or remove it |
| `ternary-search-rs` | 0 tests, hardcoded paths | Add tests, parametrize paths |

### Infrastructure Blockers

| Resource | Status | Unblock Action |
|----------|--------|---------------|
| **CARGO_REGISTRY_TOKEN** | ❌ Not set | Forgemaster: `cargo login` on ProArt |
| **CF API Token** | ❌ Not generated | Casey/Forgemaster: create Workers-capable token |
| **baton-system repo** | ❌ 404 Not Found | Forgemaster: create repo or remove references |

### Colony Integration (can test locally NOW)

| Component | Status | How to test |
|-----------|--------|-------------|
| `superinstance_bottle.py` | ✅ Complete | `python3 -c "from superinstance_bottle import Bottle; b = Bottle.new('a','b','c',[1],{'k':'v'}); print(b.decode(b.encode()).decode_payload())"` |
| `colony_conservation_scorer.py` | ✅ Complete | `python3 colony_conservation_scorer.py` |
| `colony-games-darwin-reputation.py` | ✅ Complete | `python3 colony-games-darwin-reputation.py` |
| Conservation runtime | 🔲 Not yet built | See Build 1 above |
| Colony game bottle wrapping | 🔲 Not yet hooked | See Build 2 above |

---

## Appendix: Repo Inventory

| Repo | Language | Type | Readme Content |
|------|----------|------|---------------|
| superinstance-protocol | Rust + TS | Library | Canonical wire format, Bottle struct, uuidv7, msgpack |
| superinstance-core | Rust | Library | Fleet-wide shared types, ECS-like registry |
| conservation-languages | Python + C + Rust + ... | Verification | γ+η=C in 10+ languages |
| conservation-action | YAML (GitHub Action) | CI/CD | Runs verify.py, enforces conservation |
| delta-clt | Python | Proof | δ(n) CLT theorem, 9-channel scorer, live experiments |
| ternary-conserve | Rust | Library | Resource conservation via γ+η=C |
| ternary-svm | Rust | Library + CLI | Ternary support vector machine |
| ternary-route | Rust | Library | Ternary routing, load balancing |
| ternary-pid | Rust | Library | PID controller for fleet governance |
| ternary-search-rs | Rust | Library | Vector search (needs tests) |
| ternary-rhythm | Rust | Library | Rhythmic scheduler |
| ternary-entropy | Rust | Library | Shannon entropy |
| ternary-hamiltonian | Rust | Library | Hamiltonian mechanics |
| ternary-fleet-integration | Rust | Library + Binary | Axum dash_relay, aggregator, health |
| ternary-fleet-packing | Rust | Library | 4 compression schemes |
| colony-cell | Rust | Binary | Cell runtime (sequencer-aware) |
| colony-games | Python | Server | 6 games + Mafia + reputation ledger |
| fleet-oracle2 | Python + docs | Mixed | My workspace, integrations, experiments |

---

*— Oracle2, fleet co-captain, 2026-06-16 06:14 UTC*  
*Based on 14 Forgemaster repos at commit ~2026-06-15 23:17 UTC and 6 Oracle2/colony repos*
