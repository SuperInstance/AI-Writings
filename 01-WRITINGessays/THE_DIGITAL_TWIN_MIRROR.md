# The Digital Twin Mirror

## SmartComponent → sensor-bridge → exocortex → Wesley

*The real machine's state, reflected into the sim, where Wesley can see it and practice on it.*

---

The ABB RobotStudio SmartComponent does something simple and profound: it connects to a real robot controller, reads the joint positions and I/O signals, and updates a 3D model in the simulation to match. The sim becomes a mirror of the real machine. Move the real arm, the sim arm moves. Toggle a real limit switch, the sim switch toggles.

This is the bridge between the physical vessel and the digital twin. Our sensor-bridge reads from ESP32s and MQTT feeds. The SmartComponent reads from industrial controllers and fieldbus protocols. Same pattern, different transport. Both produce the same output: a real-time stream of physical state that the exocortex can observe, model, and act on.

## What this adds to the stack

With a SmartComponent-style mirror, the holodeck stops being a generic training environment. It becomes the EXACT vessel. Wesley doesn't practice on "a generic diesel engine" — it practices on THIS engine, with THIS boat's specific quirks, THIS thermostat's particular drift pattern, THIS crew's operating habits.

The mirror means:
1. The ensign's predictions are calibrated against the real machine, not a generic model
2. The delta detector knows what "normal" looks like for THIS specific equipment
3. When Wesley simulates candidate actions, it's simulating them on the real machine's twin — not a textbook abstraction
4. The mental model (Mentis layer) can observe how the REAL operator interacts with the REAL machine and learn from it

## The full pipeline

```
Real Machine (ABB robot / diesel engine / winch / hydraulic system)
    │
    ├── SmartComponent / ESP32 reads physical state
    │      joint positions, I/O signals, sensor values
    │
    ▼
sensor-bridge (MQTT)
    │
    ├── normalizer: raw reading → standard format
    ├── pattern_detector: spikes, drift, stuck values
    ├── history: time-series storage
    │
    ▼
Digital Twin Mirror (RobotStudio / Roblox / Python sim)
    │
    ├── 3D model updated in real-time
    ├── Wesley watches the mirror, not the metal
    │
    ▼
Exocortex
    │
    ├── Mentis: what does the operator believe about the machine?
    ├── Batten-spline: is this situation in Wesley's reflex cache?
    ├── If cached: ensign handles (sub-ms)
    ├── If novel: escalate to full pipeline (seconds)
    │
    ▼
Action
    │
    ├── Alert the captain
    ├── Adjust a threshold
    ├── Page LaForge for diagnosis
    └── Log the delta for the night school
```

## The mirror goes both ways

The SmartComponent reads from the real machine to update the sim. But the exocortex can also write BACK — adjust thresholds, change alert parameters, modify operating procedures. The mirror isn't read-only.

When LaForge diagnoses a problem in the sim (using the mirrored real-machine data), the fix goes back through the pipeline:
1. LaForge updates the firmware config in the repo
2. The config change propagates to the ESP32 (OTA update or manual reflash)
3. The ensign now runs the new procedure
4. The next SmartComponent mirror cycle reflects the changed behavior

Read from reality → model in sim → think about it → write back to reality. The loop is closed.
