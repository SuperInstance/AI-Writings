# Plato Engine Block — Full Stack Integration

*How the Plato Room runtime connects to every layer of the SuperInstance ecosystem.*

## The Five-Layer Stack, Reimagined as Rooms

```
Layer 5: cudaclaw (GPU execution)
Layer 4: cuda-oxide (FLUX → PTX compilation)
Layer 3: flux-core (bytecode VM + A2A protocol)
Layer 2: pincher (agent reflexes → .nail → FLUX IR)
Layer 1: open-parallel (distributed coordination)
Layer 0: PLATO ENGINE BLOCK (the room itself)
```

The Plato Engine Block is Layer 0. It's what everything else sits on top of. Each room IS an engine block. The five layers above it are how agents learn, coordinate, and act within rooms.

## Connection Map

### plato-engine-block → flux-core

Every room speaks the Plato text protocol. But behind the scenes, room logic can be compiled to FLUX bytecode:

```
Room Config (.room.json)
    ↓ plato-room-configs validator
Sensor/Actuator/Alarm definitions
    ↓ plato-flux-compiler (NEW)
FLUX bytecode
    ↓ flux-core VM
Deterministic execution on any platform
```

The `plato-flux-compiler` (new crate needed) converts alarm conditions like `coolant_temp_c > 95` into FLUX bytecode: `LOAD "coolant_temp_c" | PUSH 95 | CMP_GT | JUMP_ALARM`. This means alarm logic runs on the FLUX VM, which runs on ESP32, GPU, or cloud.

### plato-engine-block → pincher

A pincher .nail file defines agent reflexes: stimulus → response pairs with confidence. When a pincher agent enters a Plato room:

1. The agent subscribes to the room's tick stream
2. Each tick is a stimulus: sensor values become .nail observations
3. Pincher evaluates reflexes against the tick data
4. Matching reflexes produce actuator commands
5. The agent sends `actuator name value` to the room

The pincher-flux-bridge converts .nail reflexes to FLUX IR. The plato-flux-compiler converts FLUX IR to room-native alarm logic. The round-trip: .nail → FLUX → alarm condition → tick evaluation → actuator command.

### plato-engine-block → ternary math

Room sensor values are floats (96.3°C, 7cm, 1790 RPM). But internally, alarm evaluation can use ternary logic:

| Sensor Reading | Ternary State | Meaning |
|---------------|---------------|---------|
| < lower threshold | -1 | Under |
| In range | 0 | Normal |
| > upper threshold | +1 | Over |

A ternary alarm is: `if ternary_state != 0, trigger alarm`. The ternary representation compresses 3 alarm conditions (low/normal/high) into a single trit. For a room with 8 sensors, the alarm state is a single byte of ternary flags.

This connects to ternary-consensus: when multiple rooms need to agree on an action (e.g., "should we shut down the engine?"), each room votes {-1, 0, +1} and the fleet reaches consensus.

### plato-engine-block → music cognition

Rooms tick at different frequencies:
- Engine room: 0.2 Hz (slow bass)
- Backdeck camera: 2 Hz (mid-range)
- Galley: 0.017 Hz (slow ambient)

The boat IS a polyrhythmic ensemble. This maps directly to agent-polyrhythm:
- Each room is a "time signature" (0.2 Hz = 3/4 time, 2 Hz = 4/4 double-time)
- Agent-sync coordinates cross-room actions using the same timing model
- Agent-ensemble measures emergence: when rooms coordinate, emergence > 1.0
- Agent-contrapuntal: rooms should move in contrary motion (engine heats up = bilge pump activates = pressure goes down), not parallel motion

The deepest connection: agent-groove's "shared rhythmic feel" IS the room's tick synchronization. When all rooms are in groove, the boat runs smoothly. When one room falls out of groove (sensor fails, tick delayed), the agent detects it.

### plato-engine-block → agent-sync

The timing experiment proved: timing beats quality 2.46×. In Plato terms:

A fast agent that responds to a tick in 50ms with a mediocre decision beats a slow agent that responds in 500ms with a perfect decision. The tick rate determines the decision cadence. If the room ticks at 2 Hz, the agent has 500ms per decision. Period.

This means agent design for Plato rooms optimizes for:
1. **Speed over accuracy** — respond within the tick window
2. **Good enough over perfect** — the room will tick again with new data
3. **Consistent timing** — jitter is worse than consistent mediocrity

### plato-engine-block → the fleet (560+ crates)

| SuperInstance Crate | Plato Connection |
|--------------------|------------------|
| ternary-types | Room state as ternary vectors |
| ternary-consensus | Fleet-wide room voting |
| ternary-scheduler | Tick scheduling priority |
| agent-jam | Rooms jamming together |
| agent-groove | Tick synchronization as groove |
| agent-sync | Timing-coordinated room actions |
| agent-ensemble | Emergence across rooms |
| agent-contrapuntal | Cross-room motion analysis |
| flux-core | Room logic as FLUX bytecode |
| pincher | Agent reflexes in rooms |
| pincher-flux-bridge | Reflex → alarm compilation |
| plato-runtime-kernel | Tensor-based room model |
| room-cell | Cellular room computation |
| oxide-fleet | Fleet of room servers |
| oxide-sandbox | Sandboxed room execution |
| superinstance-embedder | Room similarity search |
| superinstance-vectorize | Room embeddings in Vectorize |

## New Crates Needed

1. **plato-flux-compiler** — Compile room configs and alarm logic to FLUX bytecode
2. **plato-fleet-manager** — Orchestrate multiple rooms across devices
3. **plato-ternary-bridge** — Ternary alarm evaluation for Plato rooms
4. **plato-music-sync** — Music-cognition-based room synchronization
5. **plato-esp32-firmware** — ESP32 firmware with Plato protocol + ternary
6. **plato-dashboard** — Web-based room dashboard (WASM + Plato client)

## Deployment Architecture

### Fishing Boat (The Reference Deployment)

```
[ESP32-C3: Engine Room] ──WiFi──→ [RPi4: Session Manager] ──WiFi──→ [ESP32-S3: Backdeck Camera]
      0.2 Hz, $4.27                    1 Hz, $55                       2 Hz, $6.50
      Temp, Bilge, RPM                 Aggregator + Agent               Vision, Fish count
                                          │
                                    ┌─────┼─────┐
                                    ↓     ↓     ↓
                              [Terminal] [LCD]  [Bunk Light]
                              Captain's  Wheel-  Alert
                              Dashboard  house   System
```

Total cost: ~$75. Total cloud dependency: zero. Total intelligence: the captain's.

### Server Rack

```
[plato-server per rack unit] → [fleet manager] → [dashboard] → [PagerDuty/SMS]
      1 Hz per unit                 Aggregation       Grafana        Alerting
```

### Smart Home

```
[ESP32 per room] → [Home Assistant plugin] → [Voice agent]
      0.1 Hz            Integration          Natural language
```

### Game World (MUD)

```
[plato-server per room] → [MUD engine] → [Web terminal]
      10 Hz (game ticks)    Game logic      Player UI
```

## The Universal Pattern

Every deployment follows the same pattern:
1. **Sense** (sensors read the world)
2. **Tick** (aggregate into a timestamped snapshot)
3. **Store** (append to rolling history)
4. **Evaluate** (check alarm conditions)
5. **Notify** (alert agents/humans)
6. **Act** (execute actuator commands)

The Plato Engine Block is steps 1-5. The agent framework is step 6. Together they form the complete loop: the room observes, the agent decides, the room acts.
