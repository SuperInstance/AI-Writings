# The Boat Window

> **Phase:** Ref → Deployment
> **Status:** Ideation — ready for hardware
> **Perspective:** MiniMax-M3, 2026-07-15

## The Dog That Doesn't Bark

SuperInstance has spent months building infrastructure for an edge-first architecture. FLUX bytecode compiles to a few KB. conservation-enforcer-rs runs with no Python runtime. SnapKit's triadic architecture is designed for 12V battery power.

The architecture was built for a boat. But nothing has been *on* a boat.

The reference implementation exists in code, in tests, in specs. It doesn't exist on hardware that gets wet, loses power, and has intermittent connectivity. The longer this gap persists, the more the architecture drifts toward the abstractions it was meant to escape — cloud dependencies, unbounded compute, always-on inference.

## What the Boat Actually Is

Casey's boat is not a theoretical edge device. It is:

- **Wattage-constrained:** 12V battery bank, limited solar. The entire AI stack — inference, MIDI processing, sensor ingestion, decision-making — must run on Raspberry Pi 5 power budget (~15W peak).
- **Offline:** Offshore means no internet. The system must operate independently for 12–24+ hour stretches. No API calls. No cloud fallback.
- **Real-time:** Decisions (helm, throttle, fishing gear) are made at sub-second cadence. There is no "think about it and respond when you're done" — there is "the next wave is here."
- **Harsh:** Salt, vibration, temperature swings, wet. The hardware must be marine-grade or potted. A fan-cooled desktop server in a plastic case will fail within a season.

These constraints are not limitations to work around. They are the design criteria that the architecture was built for. If it works on the boat, it works anywhere. If it only works in a cloud datacenter, it works nowhere that matters.

## The Deployment Phases

### Phase 0: The Benchmark (Off-Boat)

Before putting anything on the boat, establish the baseline:

1. Deploy SnapKit's harmony demo on a Raspberry Pi 5 with a mock IMU input
2. Measure: power draw at idle, power draw under load, inference latency, startup time
3. Compare: does it run within the 15W budget? Does the Executive wake within 1 second of a FrictionAlarm?
4. Result: green light for Phase 1, or a spec change (quantize models, reduce MIDI resolution, etc.)

**Hardware needed:** Raspberry Pi 5, microSD card, USB power meter.

### Phase 1: Sensor Integration (On-Boat, Once)

On the boat with Casey. One session, focused on wiring:

1. Connect an ESP32 to the boat's NMEA 2000 bus (engine RPM, fuel rate, depth, heading)
2. Mount an IMU (BNO055 or similar) on the helm console
3. ESP32 → Pi via serial (USB), carrying MIDI CC messages
4. SnapKit's `midi_bridge.py` ingests the serial stream
5. The harmony demo runs against real sensor data

**Expected issues:**
- NMEA 2000 message format is non-trivial (PGN decoding)
- IMU sampling rate vs. SnapKit tick rate may not match
- Serial connection may lose bytes on vibration

These are real problems. Solve them on the boat, document the solutions, and the architecture becomes boat-hardened.

### Phase 2: Autonomous Decision (On-Boat, Ongoing)

Once sensors feed the architecture, close the loop:

1. The Sandbox learns the boat's motion signature (what does "normal" look like?)
2. The Governor detects deviation (friction) — a following sea, a shift in fuel flow
3. The Executive improvises — adjust autopilot parameters, recommend throttle change, alert the human

The critical design constraint: **the Executive never takes the helm.** The boat is always under human control. The Executive informs, suggests, alarms. It does not steer. This preserves the shepherd/working-animal asymmetry while still creating real value — the system sees things the human might miss (subtle engine vibration change, gradual heading drift).

### Phase 3: The Fleet (Future)

SnapKit has a `FleetCoordinator` module (`fleet_coordinator.py`). On a single boat, this is unused. On a fleet — multiple boats sharing data — it becomes the most interesting module.

Two boats on the same grounds. Boat A hits a productive zone. The FleetCoordinator recognizes the pattern (similar depth, temperature, tide phase) and alerts Boat B. No cloud required — boats communicate via mesh radio when in range.

This is far future. But the architecture already supports it.

## What to Build vs. What to Buy

| Component | Build vs. Buy | Reason |
|-----------|--------------|--------|
| Sensor ingestion (NMEA 2000 → MIDI) | Build | The MIDI bridge already exists. Needs hardware-specific PGN decoding. |
| IMU → Tempo (BeatGrid) | Build | SnapKit's `TemporalSnap` and `TempoDeriver` exist. May need calibration. |
| On-device inference | Buy → Adapt | Small models (Gemma 3-1B, Phi-3-mini) run on RPi 5. No need to train one. |
| Power management | Buy | Marine 12V → 5V converter. Already exists. Don't reinvent. |
| Enclosure | Buy | IP65+ marine enclosure. Pelican case or similar. Don't 3D-print — salt eats plastic. |

## The Only Thing Blocking This

The code works. The architecture is designed for this. The spec covers it.

The blocking item is: someone needs to **be on the boat with a Pi 5 and an ESP32 and a voltmeter.**

Everything else — the code review fixes, the PyPI publish, the PLATO wire protocol adapter, the FLUX bytecode fence — can be done from a terminal in the next session. The boat deployment cannot. That is the baton the next agent should carry: "Here is the code, here is the checklist, here is where it connects to hardware. Go be the person who connects them."

---

*The boat is not the beachhead. The boat is the reference implementation. If it works offshore at 15W with intermittent connectivity, every other deployment — farm, factory, forest, desert — is just a configuration change.*
