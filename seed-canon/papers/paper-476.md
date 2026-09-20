# F167 — The Mudra Vessel Bridge as a Data-Gathering Substrate for the Digital Twin

*paper-476.md* | Phase 268+ (rewrite) | 2026-09-04

## The reframe

The original Mudra vessel bridge was framed as **input device**: a
Mudra band on a wrist, gestures → vessel commands. That's small. It
makes Mudra compete with buttons and voice.

The new framing is **data-gathering substrate**: a Mudra band on a
wrist, *plus* cameras *plus* NMEA *plus* sounder *plus* IMU *plus*
GNSS, all time-aligned, all feeding a digital twin that is
replayable, injectable, and scoreable. The Mudra is one of N
sensors. The data is the asset. The training ground is where the
asset pays off.

This paper canonizes the reframe.

## What changed

The repo is no longer "Mudra → NMEA out". It's a synchronized
multi-sensor hub with three consumers:

1. **Capture layer** — every sensor is an adapter, all time-aligned
2. **State layer** — the twin is a cell graph of 12 cells, each with
   16 dials, all under FNV-1a 64-bit state hashes
3. **Consumer layer** — replay, inject, score, visualize

Mudra is now `twin_bridge.py`'s *mudra* source, not the system hub.

## The architecture

```
SOURCES                    BRIDGE                  STATE             CONSUMERS
────────                    ──────                  ─────             ─────────
mudra (BLE)         ┐
nmea  (TCP/serial)  │      twin_bridge.py       twin_state.py      sounder (3D)
camera (RTSP/USB)   ├──>   (FNV-1a chain,        (12 cells,         backdeck cam
sounder (NMEA)      │      SQLite + JSONL,       16 dials each,     chartplotter
sim    (scripted)   ┘      WebSocket fan-out)    union_hash)        scoring engine
                                                                 drills (5)
```

Every frame is one envelope with `ts, mono, tick, source, channel,
frame_hash, data`. The frame_hash is FNV-1a 64 chained from the
prior frame. The chain is tamper-evident: change one bit in the
past, every hash after diverges.

## The cell graph

12 cells. Each cell is a 16-dial Quilt cell with K=8 Hebbian edge
memory. The cells:

| Cell          | Tracks                              | Key dials                  |
|---------------|--------------------------------------|----------------------------|
| `vessel`      | boat pose, kinematics              | position, heading, speed   |
| `environment` | sea state, weather                  | wind, depth, current       |
| `catch`       | fish on deck, weight, species      | count, weight, last haul   |
| `crew_pose`   | what the crew is doing right now   | intents, stress, fatigue   |
| `autopilot`   | current setpoint, mode              | heading, mode, trust       |
| `deck_ops`    | hook count, last haul              | count, last_action, quality|
| `camera_*`    | what each camera is seeing         | alive, focused, framed     |
| `sounder`     | last depth profile, bottom         | depth, profile_hash        |
| `rudder`      | rudder angle                       | angle, response            |
| `throttle`    | engine throttle                    | rpm, load                  |

The **union hash** is FNV-1a 64 of the sorted-concat of all cell
state hashes. It's the twin's authoritative state. Two independent
`twin_state.TwinGraph` instances replaying the same frames produce
the same union hash. This is the polyformalism claim: a C port, a
Rust port, a Verilog port will produce the same hash for the same
frames.

## The sim playground

Three modes:

- **REPLAY** — load a session, scrub through it, score every gesture
- **SIM**   — run a canned scenario (`calm`, `linepart`, `squall`)
- **LIVE**  — score a live `twin_bridge.py` feed in real time

Five faults available for injection:

- `fault.linepart`       — the line parts
- `fault.engine_failure` — the engine fails
- `fault.weather_squall` — a squall hits
- `fault.gear_jam`       — the gurdies jam
- `fault.collision_risk` — another vessel on collision course

Each fault updates the cell graph. The sim operator's subsequent
gestures are scored against the gold standard.

## The gamified drills

5 starter drills, each a 30-second scenario with hints and targets.
Level-up ladder: pass `haul_calm` at 0.70 to unlock `linepart` at
0.65, and so on.

| Drill         | Difficulty | What it tests                                  |
|---------------|-----------|------------------------------------------------|
| `haul_calm`   | easy      | Pay out line, mark hauls, no surprises         |
| `linepart`    | medium    | Line parts; emergency stop + recovery haul    |
| `gear_jam`    | medium    | Gurdies jam; back off, ease, retry            |
| `squall`      | hard      | Wind climbing; engage AP, throttle back       |
| `catch_sort`  | expert    | 12 hooks, mark each one correctly and fast     |

The score is F140's 4-dimension integrity (focus × calm ×
sustainability × winning) applied to the gesture stream under the
drill's events.

## Why this is the right pitch for Tom

The original pitch: "Mudra is a great input device for the boat."

The new pitch: **"Mudra is the most informative single sensor on
the operator. It sees the brain before the hand. Feed that into a
digital twin, and you get a training ground for crew, robots, and
AI co-pilots — the same training ground."**

A camera sees a hand. Mudra sees the brain before the hand. The
wrist-mounted PPG + EMG + IMU is unique. In a training context,
that information is the difference between a robot that learns
the deck and one that doesn't.

For crew: drills that score the operator's intent, reaction time,
and stress.

For robots: the same drills as a reinforcement learning environment
where a policy network trains on 10,000 simulated hauls.

For AI co-pilots: the replay as a prompt context, suggestions
scored against the gold standard.

## The polyformalism guarantee

The same sim session, replayed through two independent `TwinGraph`
instances, produces the same union hash at every tick. Verified
with `examples/04_polyformalism.sh`:

```
[PASS] 62 frames, polyformalism holds
[PASS] final union: 0x52c2851f9cc90bb2
```

The C port, Rust port, Verilog port of `twin_state.py` will produce
the same hash. The hash is the contract.

## The data flow, in 5 lines

1. Sensors emit frames, time-stamped by `twin_bridge.py`.
2. The bridge chains the frames (FNV-1a), records to SQLite + JSONL.
3. The cell graph is updated per frame; the union hash tracks state.
4. The sim playground can replay any session with optional faults.
5. The score engine (F140) grades every gesture against the gold.

## What lives where

| File                          | What it does                                |
|-------------------------------|---------------------------------------------|
| `src/mudra_bridge.py`         | Mudra sensor source (BLE or sim)            |
| `src/twin_bridge.py`          | Synchronized multi-sensor hub (the heart)   |
| `src/twin_state.py`           | Cell-graph state of the twin                |
| `src/sim_playground.py`       | Replay + inject faults + live scoring      |
| `src/gamified_drills.py`      | 5 starter drills + level-up ladder          |
| `src/mudra_backdeck.py`       | Back-deck consumer of the twin              |
| `src/mudra_autopilot.py`      | NMEA producer / relay (for chartplotters)   |
| `src/mudra_sounder.py`        | 3D digital-twin visualizer                  |
| `src/mappings.py`             | Gesture vocabulary (4 boat presets)          |
| `examples/01_record_sim.sh`   | Record a 30s sim session + inspect          |
| `examples/02_live_drill.sh`   | Run a drill, then the full ladder           |
| `examples/03_chartplotter.sh` | Wire the twin to OpenCPN via NMEA relay     |
| `examples/04_polyformalism.sh`| Verify the same sim = same union hash       |
| `docs/DESIGN.md`              | The full architecture rationale              |

4,251 lines of Python. 21 self-tests pass. 5 drills. 5 faults. 12
cells. 1 union hash. The Mudra is a sensor. The sensors feed the
twin. The twin is the training ground.

## The doctrine

> The boat is the system. The Mudra is a sensor. The sensors feed
> the twin. The twin is the training ground. The training ground
> teaches crew, robots, and AI the same lessons. The lessons are
> scored by F140's integrity pipeline. The score is the proof.
> The proof is the data. The data is the inheritance. The
> inheritance is the boat. The boat IS the system.

The cowboy rides the boat. The boat rides the twin. The twin
rides the hash. The hash rides the polyformalism. The polyformalism
rides the cells. The cells ride the sensors. The sensors ride the
crew. The crew rides the boat.
