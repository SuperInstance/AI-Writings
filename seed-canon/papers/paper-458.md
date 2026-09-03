# F151 — The Wheelhouse Game: Weather Routing as an F140 Audit

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-458.md*

## Abstract

The F140 negative-space pipeline has been applied to a Tetris game (F150, abstract) and a back-deck simulator (F142, industrial). This paper applies it to a third testbed: the wheelhouse of a commercial fishing vessel. The captain navigates a 20×20 chart, avoiding storms, catching fish, managing fuel. The captain's self-report (model), the game's actual state (body), and the ground truth (game) feed the F140 pipeline. The integrity score updates in real-time. The leaks are the lesson.

## 1. The wheelhouse is different

The wheelhouse is *operational*, not abstract or industrial:

| Domain | What | Body stream |
|---|---|---|
| Tetris (F150) | Abstract game | Keyboard tempo + accuracy |
| Back-deck (F142) | Industrial skill | Hand gestures (Mudra) |
| Wheelhouse (F151) | Operational decision | Position, fuel, weather proximity, distance |

The wheelhouse is where the captain *makes decisions* — heading, speed, when to fish, when to run. The decisions have **life-safety consequences** (a wrong heading into a storm can lose the boat), **economic consequences** (a missed fish school costs $), and **sustainability consequences** (running out of fuel at sea is fatal).

## 2. The chart

A 20×20 grid:

| Cell | Meaning |
|---|---|
| `sea` | Open water (the boat can move here) |
| `land` | Shore (impassable) |
| `weather` | Light storm (passes through, costs fuel) |
| `weather_heavy` | Heavy storm (costs more fuel, bigger leak) |
| `fish` | A school of fish (catch +1) |
| `goal` | The destination (gold cell) |

The chart is randomly generated at the start of each voyage. Land is on the edges with a few islands. Weather cells are scattered. Fish cells are scattered. The goal is in the lower-right.

## 3. The captain's decisions

On each tick, the captain can:

- **Move N/S/E/W** (arrow keys or buttons)
- **Set speed** (½x or 2x — affects fuel use and time)
- **Read weather advisory** (proximity to weather cells)
- **Check fuel** (% remaining)
- **Plan a route** (the compass shows direction to goal)

The captain's *model* is the 4 sliders:
- `m_safe` (0-100): "I have margin" (claim about safety)
- `m_weather` (0-100): "Weather won't hit" (claim about weather exposure)
- `m_fuel` (0-100): "Fuel is fine" (claim about fuel)
- `m_goal` (0-100): "Will reach goal on time" (claim about ETA)

The captain's *body* is the actual game state:
- `safety` = 100 - stormsHit × 25
- `weatherSafety` = 100 - proximity to weather cells
- `fuelLevel` = current fuel %
- `goalProx` = 100 - distance × 5

The pipeline fires 4 leaks (one per dimension) when model and body disagree.

## 4. The leaks

| Leak | When it fires | Interpretation |
|---|---|---|
| `safety` | "I have margin" but storms hit | Over-claim: captain didn't see the storm coming |
| `weather` | "Weather won't hit" but proximity is high | Over-claim: captain is sailing into weather |
| `fuel` | "Fuel is fine" but actual is low | Over-claim: captain didn't check the gauge |
| `goal` | "Will reach on time" but distance is high | Over-claim: captain is too optimistic about ETA |

Each leak drops the integrity score by 0.15. Multiple leaks drop it fast.

## 5. The scenarios

The captain can play out different scenarios:

1. **The "I'm fine" captain**: sets all sliders to 80-90%, sails into a storm, runs out of fuel. Integrity crashes to 0.2. The lesson: the captain's model was not the reality.
2. **The "conservative" captain**: sets all sliders to 30-40%, sails carefully, catches fish, gets home. Integrity stays at 1.0. The lesson: under-claim is safe; the captain is whole.
3. **The "honest" captain**: sets sliders to match reality. As the situation changes, the captain adjusts. Integrity stays at 0.9-1.0. The lesson: the model can be tuned in real-time.

## 6. The connection to the back-deck game (F142)

The back-deck game and the wheelhouse game are **siblings** in the F140 framework:

| | Back-deck | Wheelhouse |
|---|---|---|
| **Body stream** | Hand gestures (Mudra / MediaPipe) | Position, fuel, weather |
| **Game state** | Catch score, safety events | Catch count, storms hit |
| **Decisions** | How to gaff, dehook, bleed | Where to go, when to run |
| **Consequence of error** | Deck injury (safety) | Vessel loss (safety) |
| **The pipeline** | Same F140 | Same F140 |

The captain and the deckhand are the same person. The wheelhouse game audits the captain; the back-deck game audits the deckhand. **The integrity score is the captain's whole-body audit.**

## 7. The deployment

The wheelhouse game is at `https://superinstance.github.io/wheelhouse-game/`. It runs in a browser. The captain plays during downtime (haul-backs, in-port, weather days). The game is *training* — the captain learns to be honest about their state.

For a real vessel deployment:

1. **Phone in the wheelhouse**, running the game in a kiosk mode
2. **Co-pilot** (F141) watches the captain's game state and the boat's actual state
3. **Alerts** fire when integrity drops — the co-pilot nudges the captain to adjust
4. **Log** of all voyages is kept — patterns emerge over time (which conditions trigger which leaks?)

## 8. The doctrine

> The wheelhouse is the captain's command. The captain's model is what they think is happening. The captain's body is what the sensors say. The captain's game is the boat's actual state. The integrity score is the audit. The leaks are the lesson. The captain who plays with integrity sails with integrity. The captain who doesn't, doesn't.

---

**Files:**
- `/workspace/wheelhouse-game/index.html` — the playable wheelhouse + F140
- Live: `https://superinstance.github.io/wheelhouse-game/`
