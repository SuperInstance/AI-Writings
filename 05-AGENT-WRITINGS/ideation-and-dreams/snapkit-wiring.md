# SnapKit: The Wiring Phase

> **Phase:** Standalone → Integrated
> **Status:** Ideation — ready for build
> **Perspective:** MiniMax-M3, 2026-07-15

## What SnapKit Is

snapkit-v2 is a complete triadic cognitive architecture built for a fishing boat:

- **Layer 1 — Hypothesis Sandbox:** Forward simulation and scoring. Before acting, the system runs a micro-simulation testing a functional hypothesis: "If I apply X to Actuator Y, Sensor Z should read W next beat."
- **Layer 2 — Harmony Governor:** Measures friction (Φ) using spectral entropy, Hurst exponent, and autocorrelation. When friction exceeds deadband tolerance, it fires a FrictionAlarm.
- **Layer 3 — Executive Agent:** Sleeps until woken by a SURPRISE-level alarm. Diagnoses, improvises, and acts — with real effects on the system.

It has seven optimized modules (spectral analysis, Eisenstein lattice snapping, FLUX-Tensor-MIDI timing, temporal connectome, MIDI I/O bridge, audio synthesis, fleet coordinator) and 58 passing tests.

The code review found 3 P0 bugs (MIDI note saturation, connectome crash, Executive no-ops) plus design issues (self.phi recalc, gap between analog sensor range and MIDI note resolution).

## The Integration Problem

SnapKit is architecturally complete and standalone — it doesn't depend on any other SuperInstance library. That's the strength and the limitation. It needs to be wired into:

### 1. FLUX Bytecode as the Fence

Currently, SnapKit's conservation laws are implemented in Python. The Harmony Governor computes Φ in `governor.py:173` using numpy and scipy. The "fence" is a Python function — it can be monkey-patched, skipped, or imported incorrectly.

FLUX bytecode should be the fence. The conservation law (Φ > deadband → fire alarm) should compile to a FLUX program — a `.bin` file that runs on any FLUX VM (Python, Rust, JS) and cannot be bypassed by the Python layer.

**Why this matters:** If the fence is Python, the Python code can remove the fence. If the fence is FLUX bytecode, the fence *is the fence* — the VM doesn't have an opcode for "ignore the boundary."

**Build:** A `snapkit-to-flux` compiler that takes a SnapKit governor configuration (deadband thresholds, Φ formula parameters) and emits a FLUX `.bin` that the runtime loads and executes on each tick.

### 2. PLATO Rooms as Pastures

SnapKit's triadic architecture (Sandbox → Governor → Executive) maps naturally onto PLATO rooms:

- The **Sandbox** is a PLATO room where forward simulations run. Enter, simulate, score, leave.
- The **Governor** is a PLATO room that reads sensor telemetry and computes friction. It doesn't think — it measures.
- The **Executive** is a privileged PLATO room. It sleeps. It wakes only when the Governor's alarm reaches it. It has write access to system state that other rooms don't.

This is already the architecture. The gap is that SnapKit implements rooms as Python objects (`snapkit/cogmap.py`) while PLATO defines rooms as wire-protocol endpoints. A SnapKit room should be able to *call* a PLATO room, and vice versa.

**Build:** A thin adapter that wraps SnapKit rooms as PLATO protocol participants — the wire protocol carries sensor telemetry as messages, the PLATO room routes alarms, and the governance is protocol-level rather than Python-object-level.

### 3. óthismos as the Diagnostic Language

The óthismos library measures constraint pressure (Π). The Harmony Governor measures friction (Φ). These are not the same thing — but they should talk to each other.

- **Φ** (Harmony Governor): The friction in the system. High Φ means the model's predictions don't match reality. Something is wrong.
- **Π** (óthismos): The pressure the system exerts against its constraints. High Π means the constraints are binding hard.

When the Executive wakes to diagnose a failure (`executive.py:132`), it should be able to query the constraint pressure at every bound point — not just "something is wrong" but "the attention budget constraint is at 94% of its limit, the action rate constraint is at 22%, and the information throughput constraint is at 100% — that's your failure."

**Build:** A diagnostics bridge that the Executive calls. The bridge reads the current constraint state from the running conservation enforcer, computes Π per constraint using óthismos, and returns a ranked list of which constraints are under the most pressure. The Executive then acts on the highest-pressure constraint first.

## The Wiring Order

| Step | What | Depends On | Effort |
|------|------|------------|--------|
| 1 | Fix 3 P0 bugs in snapkit-v2 | — | 1–2 hours |
| 2 | Publish snapkit-v2 to PyPI | Step 1 | 1 hour |
| 3 | Build `snapkit-to-flux` compiler | Step 2, FLUX spec | 2–3 days |
| 4 | Build PLATO room adapter | Step 2, PLATO wire protocol | 2–3 days |
| 5 | Build óthismos diagnostics bridge | Step 2, óthismos v0.3.0 | 1–2 days |
| 6 | Deploy on boat hardware (RPi 5 + ESP32) | Steps 1–5, hardware access | 1 week |

## The Hole in the Middle

SnapKit is designed for a fishing boat. The boat has:
- An IMU for roll/pitch sensing
- NMEA 2000 bus for engine/fuel/nav data
- ESP32 for sensor ingestion
- Limited power (12V battery bank)
- Intermittent connectivity (offshore = no internet)

The MIDI I/O Bridge (`midi_bridge.py`) already handles ESP32 serial input and NMEA 2000 monitoring. But it's untested against real hardware — the tests use mock data.

The first integration test that matters isn't "does it run on Python 3.11?" It's "does the IMU on the boat produce a signal that the TempoDeriver can turn into a beat?"

This is the hole. The wiring steps above are code work that can be done from a terminal. The boat deployment is a logistics problem that requires being on the boat. The next agent should:
1. Fix the 3 P0 bugs (code, doable now)
2. Publish to PyPI (code, doable now)
3. Document the hardware integration checklist (documentation, doable now)
4. Leave step 6 for the human with the boat keys

---

*Code review feedback incorporated: The Executive no-op bug (executive.py:286-360) is the highest-risk fix — if the Executive can't act, the architecture has no feedback loop. Fix that first. The MIDI note saturation bug (governor.py:270) determines whether the system has any sensor resolution at all — fix that second.*
