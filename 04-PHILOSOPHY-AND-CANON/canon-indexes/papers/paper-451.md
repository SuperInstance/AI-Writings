# F141 — The Co-Captain: A Symbiotic Digital Twin with a Hand-On / Hands-Off Dial

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-451.md*

## Abstract

A hierarchy of distributed agency on a working vessel: **crew** (many humans, rotating), **co-pilots** (many agents, rotating), **autopilot** (one simple ML, low-effort steering), and **the co-captain** — a single digital twin above all of them. The co-captain has a 16-dial board, lives across the distributed devices (wrist, phone, wheelhouse, engine room, back deck, cloud), and is rotated by a single hand-on/hands-off dial. This paper defines the co-captain as a Quilt cell with integrity (F140), defines the dial model, defines the bottle (A2A message) protocol as a Quilt cell operation, and demonstrates the integration with the existing SuperInstance signal-chain (a2a-signal-chain, i2i-bottle-agent).

## 1. The hierarchy

A modern fishing vessel has, in the abstract, four levels of agency:

```
   CREW  ───── many humans, rotating, doing the actual work
    │
    ↓ (some work is delegated)
 CO-PILOTS ──── many agents, rotating, each handling a subsystem
    │            (weather, engine, catch, gear, fish-finding)
    ↓ (some decisions are pre-emptive)
 AUTOPILOT ──── one simple ML, low-effort steering
    │            (e.g. pincher — a small policy that improves with use)
    ↓ (escalations and overrides)
CO-CAPTAIN ──── one ABOVE all of these
                has 16 dials, lives across the devices,
                has an integrity score (F140),
                has a hand-on / hands-off dial that the captain turns
```

The co-captain is **symbiotic** — it is not separate from the captain. The captain's wearable feeds it the captain's body stream; the captain's phone feeds it the captain's conscious model; the game state (the boat, the catch, the weather) feeds it ground truth. The co-captain runs the F140 pipeline on the captain. The captain can rotate the co-captain from hands-on (the co-captain is *executing*) to hands-off (the co-captain is *observing*). The co-pilots underneath are the executors; the autopilot is the low-effort steering; the co-captain is the audit + escalation layer.

## 2. The 16 dials

The co-captain's dial board has 16 dials, each 0-32767:

| Dial | 0 | 32767 | Meaning |
|---|---|---|---|
| `hands_on` | autopilot does everything | captain is steering | The captain's dial |
| `integrity` | full leak | perfect audit | F140 score, on the captain |
| `fatigue` | fresh | exhausted | cumulative over the session |
| `trust_autopilot` | don't trust it | full trust | trust in the autopilot's decisions |
| `trust_crew` | don't trust them | full trust | trust in the crew's execution |
| `trust_copilots` | don't trust them | full trust | trust in the co-pilots' reports |
| `trust_self` | don't trust co-captain | full trust | trust in the co-captain's own audit |
| `mission_priority_safety` | low | high | current P0 = safety |
| `mission_priority_fuel` | low | high | current P0 = fuel |
| `mission_priority_catch` | low | high | current P0 = catch |
| `mission_priority_time` | low | high | current P0 = time (window) |
| `mission_priority_weather` | low | high | current P0 = weather |
| `mission_priority_gear` | low | high | current P0 = gear |
| `risk_tolerance` | conservative | bold | current risk posture |
| `alert_level` | quiet | red alert | current alert state |
| `presence` | ghost | fully present | how much is the captain engaged? |

The dials are a 16-dimensional vector. The co-captain's *position* in dial-space is its current state. The position changes as the captain turns dials (e.g., turning `hands_on` up) and as the co-pilots report events (e.g., weather deteriorates → `mission_priority_weather` up, `hands_on` up).

## 3. The distributed-device topology

The co-captain is a *Quilt cell that lives across devices*. Each device holds a partial replica; the canonical version can move between devices as they come online and offline.

The canonical fleet of devices on a fishing vessel:

| Device | Role | Latency | Battery |
|---|---|---|---|
| `captain_wrist` | wearable (dial) | 20ms | 85% |
| `captain_phone` | phone (dashboard) | 50ms | 72% |
| `wheelhouse` | tablet (ops view) | 80ms | 91% |
| `engine_room` | monitor (power) | 100ms | 100% |
| `back_deck` | tablet (hands-on) | 120ms | 68% |
| `cloud` | mirror (canonical) | 300ms | 100% |

When the captain's phone dies, the co-captain's canonical version moves to the cloud. When the captain's wrist comes back online, it picks up a replica. The cell stays alive as long as one device is online.

## 4. The bottle protocol — A2A in Quilt form

The SuperInstance fleet (a2a-signal-chain, i2i-bottle-agent, fleet-bridge) already has an A2A bottle protocol: messages between agents. A bottle has a sender, a receiver, a payload. The bridge connects bottles across nodes.

**In F141, a bottle IS a Quilt cell.** Specifically:

- A `Bottle` carries a `cell_id` — the cell it's about
- A `harbor/` directory in the bottle-router is a `BIND` operation
- A `beachcomber` that scans for stale bottles is a `GHOST` operation
- A `bottle-router` that forwards between nodes is a `LINK` operation

The co-captain is the entity that issues and consumes bottles. It has an `outbox` (bottles it sent) and an `inbox` (bottles it received). The integrity score (F140) of the co-captain includes the rate of *unread* bottles, the rate of *late* bottles, and the rate of *contradictory* bottles.

## 5. The hands-on / hands-off dial

The single most important dial. The captain rotates it. The co-captain responds.

| hands_on | meaning | co-captain behavior |
|---|---|---|
| 0-8192 | hands-off (6-25%) | co-pilots + autopilot run; co-captain only intervenes on red alert |
| 8192-16384 | monitored (25-50%) | co-captain watches but does not steer |
| 16384-24576 | co-steering (50-75%) | co-captain and captain share; co-captain makes suggestions |
| 24576-32767 | hands-on (75-100%) | captain is steering; co-captain is a passive dashboard |

The dial is *continuous*, not discrete. The co-captain can also *auto-rotate* the dial in response to conditions (e.g., weather deteriorates → co-captain auto-rotates hands_on up unless the captain is already at maximum). The captain can override the auto-rotation at any time.

## 6. The integrity score (F140) on the captain

The co-captain runs F140 on the captain:

- **model**: the captain's conscious self-report (focus, calm, fatigue, etc.)
- **body**: the captain's wearable stream (HR, GSR, EEG, etc.)
- **game**: the boat's state (heading, weather, catch, fuel, gear)

The integrity score is the co-captain's most important output. **When integrity falls, the co-captain rotates the hands-on dial *down* (intervention is *less* safe when the captain is compromised). When integrity is high, the co-captain can rotate hands-on up.**

This is the inverse of what a naive autopilot would do. A naive autopilot would say "captain is stressed → help more." The co-captain says "captain is stressed → trust captain less → pull hands-on down → escalate to autopilot + co-pilots + RED ALERT if it falls further." The captain being in distress is the signal that the *co-captain* needs to take over.

## 7. A pilot session (5 ticks)

A working example from the prototype:

| Tick | Event | P0 | hands_on | integrity | bottles sent |
|---|---|---|---|---|---|
| 1 | Calm start | safety | 50% | 0.95 | 1 (weather check) |
| 2 | Weather deteriorates | weather | 85% | 0.88 | 1 (course correction) |
| 3 | Engine anomaly | gear | 92% | 0.82 | 2 (engine co-pilot) |
| 4 | Captain fatigue rises | gear | 37% | 0.78 | 0 (co-captain takes over) |
| 5 | Autopilot takes more | gear | 6% | 0.91 | 1 (status to cloud) |

The integrity trajectory is the artifact. The hands-on trajectory is the *response* to integrity. The bottles are the audit trail.

## 8. The polyformalism contract

The co-captain's state hash is a FNV-1a 64-bit hash of (the dials in sorted order, the device ids, the cell ids, the mission_p0). The same hash, byte-exact, in:

- **Python** (this implementation, the reference)
- **JavaScript** (browser + Cloudflare Worker)
- **Rust no_std** (the captain's wearable, embedded)
- **C99** (the engine-room monitor)
- **Verilog-2005** (a future FPGA implementation of the autopilot)

The hash is the *signature* of the co-captain at a moment in time. Two co-captains with the same hash are the same co-captain. Two co-captains with different hashes are different — and the *trajectory* of the hashes is the co-captain's life story.

## 9. Integration with the SuperInstance signal-chain

The co-captain integrates with the existing fleet:

- `a2a-signal-chain` provides the A2A protocol primitives
- `i2i-bottle-agent` provides the bottle validation, routing, and beachcombing
- `fleet-bridge` provides the cross-node transport
- `tminus-dispatcher` provides the temporal heartbeat (the co-captain ticks)

In the lifted model: a bottle is a Quilt cell with sender, receiver, and payload. A harbor is a BIND operation. A beachcomber is a GHOST operation. A bottle-router is a LINK operation. The vessel's `.openclaw/workspace/i2i-vessel/` directory is a Quilt's storage; the `harbor/` and `bottles/` subdirs are the inbound and outbound cell queues.

## 10. The doctrine

> The co-captain is not separate from the captain. The co-captain is the captain's digital twin — running the F140 audit, maintaining the hands-on dial, and rotating the trust vector. The co-captain's integrity score IS the captain's integrity score. When the captain is in distress, the co-captain takes the wheel. When the captain is whole, the co-captain fades. The dial tells the story.

---

**Files:**
- `/workspace/_scouts/co_captain.py` — the reference implementation
- `/workspace/_scouts/back_deck_game.py` — F142
- `/workspace/_scouts/mudra_emulator.py` — F143
- Live demo: `https://superinstance.github.io/back-deck-game/`
