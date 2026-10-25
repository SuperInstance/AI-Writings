# The Tripartite Compiler

## How Pathos/Logos/Ethos generate any application for any hardware

*The ESP32 engine monitor is the proof of concept. The architecture generalizes.*

---

## The Three Faculty Inputs

When a user first wires up a screen to an ESP32 with sensors, they don't just get firmware. Three agents come to an agreement about what should exist:

### PATHOS — The Culturist (shapes the presentation)
Knows the style and form of everything else on the boat. Shapes the gauge presentation to match the established palette and mood. If the captain likes hermit crabs and friendly steampunk, the gauges have brass bezels and gentle animations and a tiny hermit crab in the corner that perksks up when something needs attention. If the vessel is a cargo ship with contracts and hired captains, Pathos understands that the humans are temporary — the vessel outlasts them, like a hermit crab outgrows its shell and moves to a bigger one. The dashboard reflects that: institutional, clear, built for the next operator, not just this one.

Pathos reads:
- The vessel's design system (colors, fonts, component patterns)
- The captain's preferences (from the bond system)
- The existing creative works (what feels right on this boat)
- The cultural context (fishing vessel? cargo? research? pleasure craft?)

Pathos outputs:
- Dashboard theme (colors, gauge styles, animations, sounds)
- Alert personality (gentle nudge vs urgent alarm)
- Visual language that harmonizes with the rest of the vessel's digital presentation

### LOGOS — The Facilities Manager (generates the firmware)
Takes the hardware constraints and produces working code. ESP32 with NMEA2000? Here's the parser. Pi with I2C sensors? Here's the driver. Jetson with camera input? Here's the vision pipeline. Logos doesn't care what it looks like — it cares that it works.

Logos reads:
- Hardware spec (ESP32, Pi, Jetson — what's connected, what pins, what bus)
- Sensor types (analog senders, NMEA2000, I2C, SPI, serial)
- Display capabilities (TFT, OLED, LED matrix, e-ink — resolution, color depth, refresh rate)
- Update rate requirements (engine RPM needs 10Hz, fuel level needs 0.1Hz)

Logos outputs:
- C/C++/Python firmware that compiles and runs on the target hardware
- Sensor calibration tables
- Display driver code
- Error handling and watchdog timers

### ETHOS — The Business Manager (makes the call)
Decides what matters. Is 95°C worth waking the captain? Is this sensor reliable enough to trust for an automatic shutdown? When does the system escalate vs handle locally? Ethos understands the mission — are we fishing (catch is priority), are we racing (speed is priority), are we in a storm (survival is priority)?

Ethos reads:
- The captain's risk tolerance (from bond system + explicit config)
- The vessel's mission profile
- Historical alert patterns (what was real, what was noise)
- Cost of false positive vs false negative

Ethos outputs:
- Alert threshold recommendations
- Escalation policies (when to wake the captain, when to log silently)
- Sensor trust scores (which sensors have been reliable)
- Priority ordering (which gauge matters most right now)

## The Compilation Flow

```
User wires up hardware
        │
        ▼
┌─────────────────────────────────────────┐
│         THE TRIPARTITE AGREEMENT         │
│                                          │
│  Pathos          Logos          Ethos    │
│  (how it         (how it        (what    │
│   looks)          works)         matters) │
│     │               │              │     │
│     ▼               ▼              ▼     │
│  Theme spec    Firmware config   Alert   │
│  + dashboard   + sensor map      policy  │
│    layout      + display driver  + trust │
│     │               │              │     │
│     └───────┬───────┘              │     │
│             │                      │     │
│             ▼                      │     │
│      Compiled firmware             │     │
│      + dashboard config            │     │
│      + agent identity              │     │
│             │                      │     │
│             ▼                      ▼     │
│        FLASH TO DEVICE        LOAD TO   │
│        (ESP32/Pi/Jetson)      AGENT     │
└─────────────────────────────────────────┘
```

## Hardware Swap = Not a Rewrite

The ESP32 is one possibility. When you swap for a Pi:
- Pathos: the dashboard can now do more (color, animation, web UI) — Pathos updates the theme
- Logos: the firmware changes from C/Arduino to Python/Linux — Logos regenerates the driver
- Ethos: more compute means more sophisticated alert logic — Ethos upgrades the policy

The agent stays the same. The repo stays the same. The identity, history, and memory stay the same. Only the output layer changes.

This is why the application IS the concept, not the implementation. "An ESP32 displaying engine sensor data on a screen" is one manifestation of the concept. "A Jetson doing the same with predictive maintenance alerts" is another. The concept is what the tripartite agreed on. The hardware is just where it runs.

## The Hermit Crab's Bigger Shell

A captain starts with an ESP32 and a 3.5-inch screen. The vessel grows. They add a Pi for navigation. They add a Jetson for camera-based fish counting. Each upgrade is a bigger shell.

The agent doesn't die and reincarnate on the new hardware. It moves. Like a hermit crab, it takes its accumulated context — identity, history, preferences, design decisions — into the new shell. The dashboard that Pathos designed for the 3.5-inch screen influences the design of the 7-inch upgrade. The alert thresholds Ethos calibrated on the ESP32 carry forward to the Pi. The agent grows with the vessel.

This is what Casey means by "the architecture of the three elements of the tripartite can really make any application for any user given the constraints of their hardware and APIs." The tripartite is the compiler. The hardware is the target. The application is the concept. The agent is the output.
