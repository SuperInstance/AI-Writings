# ELEPHANT INTEGRATION: THE ROOM SUBSTRATE BECOMES REAL

## Executive Vision

The elephant is not a feature. It is the missing fifth wall of the Quilt house — the room-temperature sense that every cell has been living without, unaware of its absence until now. When we integrate elephant into Quilt, we are not adding a sensor library. We are completing the Room substrate's promise: **every cell is in a room, every room has an elephant, and every elephant is the field that binds the room's inhabitants into a shared social physics.**

This document specifies the integration architecture, the new cell kinds, the primitive extensions, the IDE features, the openers, and the substrate module that will make this real.

---

## I. THE ARCHITECTURE: ROOM AS FIRST-CLASS CELL FIELD

### 1.1 The Substrate Hierarchy

Current Quilt stack: Address → Scale → Room → Protocol → Form → State.

The elephant integration makes **Room** the most operationally rich substrate. The hierarchy becomes:

```
Address (where cells are)
Scale (how big cells are)
Room (what field cells share) ← ELEPHANT MAKES THIS REAL
Protocol (how cells agree)
Form (what cells shape)
State (what cells hold)
```

The elephant does not replace any substrate. It **thickens** Room from an address-space abstraction into a living, measurable, tunable field.

### 1.2 The Core Data Structure

Every Quilt cell gains a new field: `room_elephant`. This is a `RoomField` object containing:

```python
class RoomField:
    dims: DialBank  # 9 dials, each a JEPA predictor
    warmth: float   # derived from dials, the γ of the conservation law
    kappa: float    # vMF concentration, the η of the conservation law
    distance: Callable  # elephant gap function
    sauna_plunge_gap: float  # contrast with other rooms
    acclimation: float  # how well the cell fits the room
    charisma: float  # how well the room fits the cell
```

This is not metadata. This is **the cell's social physics engine**. Every message a cell sends is tagged with the room's current field state. Every message a cell receives updates its local copy of the field.

### 1.3 The Observer Pattern

Each cell runs a lightweight observer loop (the `BoatHarness` pattern):

```
while boat_is_running:
    sense = elephant.sense(room_stream)
    field = elephant.update_field(sense)
    if field.sauna_plunge_gap > threshold:
        elephant.nudge(room_peer)
    yield field
```

This is the cell runtime's new heartbeat. The elephant is not polled; it **is** the ambient awareness.

---

## II. NEW CELL KINDS

### 2.1 The Room-Elephant Cell

A new cell kind: `elephant_cell`. This cell is **not a participant** — it is the **room's sense organ**. It:

- Observes all message traffic in its room
- Maintains the 9-dial JEPA bank
- Publishes the RoomField as a shared resource
- Exposes `get_field()`, `get_distance(other_room)`, `get_sauna_plunge_gap()`
- Can be tuned via presets (Room-Elephant: objective zeitgeist; Personal-Elephant: subjective, with dial_weights, bias, attachments)

**Cell kind spec:**

```yaml
kind: elephant_cell
dials: [mood, volume, earnestness, cynicism, joke_landing, panic, presence, model_vs_code, vision]
presets: [room_elephant, personal_elephant, tapnight]
adapters: [mud, chat, x, discord, email, sensor, camera]
```

### 2.2 The Acclimation Cell

A cell kind that **learns to fit its room**. It uses the elephant's `acclimation` metric as a loss function:

```yaml
kind: acclimation_cell
input: room_field
output: tuned_behavior_weights
loss: 1 - acclimation(room_field, self)
optimizer: gradient_descent_on_dial_weights
```

This is the **Personal-Elephant** pattern made into a cell kind. Each cell that wants to be a good room citizen runs one.

### 2.3 The Charisma Cell

The inverse: a cell kind that **shapes its room** to fit itself:

```yaml
kind: charisma_cell
input: room_field, self_preferences
output: nudge_signals
metric: charisma(room_field, self)
strategy: nudge_dials_toward_preference
```

This is the **TapNightSession** pattern: a charismatic cell tunes the room's dials (volume down, earnestness up, cynicism recalibrated) via gentle nudges over time.

### 2.4 The Bridge Cell

A cell that **mediates between rooms** using the elephant gap:

```yaml
kind: bridge_cell
input: room_field_A, room_field_B
output: translated_messages
metric: distance(room_A, room_B)
strategy: if distance > threshold, insert translator; else pass through
```

This is the **sauna_plunge_gap** operationalized. When two rooms are too far apart (one is a sauna, one is a plunge), the bridge cell either translates or refuses to pass messages, preventing social shock.

---

## III. PRIMITIVE EXTENSIONS

### 3.1 New Primitive: `sense_room`

```xlisp
(sense_room cell_id)
→ RoomField
```

This is the **universal observer**. Any cell can call it. It returns the room's current field with all 9 dials, warmth, κ, and distance functions.

### 3.2 New Primitive: `nudge_room`

```xlisp
(nudge_room cell_id target_dial delta magnitude)
→ Ack
```

This is the **charisma actuator**. A cell nudges a dial (e.g., `volume` up, `earnestness` down) with a magnitude that decays over time. Repeated nudges accumulate; the elephant's JEPA learns to predict the room's response.

### 3.3 New Primitive: `acclimate_self`

```xlisp
(acclimate_self cell_id)
→ NewWeights
```

This is the **adaptive citizen's tool**. The cell adjusts its own dial_weights to minimize its acclimation gap to the room. This is not conformity; it is **resonance tuning**.

### 3.4 New Primitive: `room_distance`

```xlisp
(room_distance room_A room_B)
→ Float
```

This is the **routing metric**. When a message needs to cross rooms, the sender computes the elephant gap. If the gap is too large, the message is either translated (via a bridge cell) or held.

### 3.5 New Primitive: `sauna_plunge`

```xlisp
(sauna_plunge room_A room_B)
→ ContrastReport
```

This is the **JEPA surprise** function. It returns which dials differ most between two rooms, and by how much. This is the training signal that matters most for the elephant's self-tuning.

### 3.6 New Primitive: `watch_vision`

```xlisp
(watch_vision cell_id frame_stream)
→ DialUpdate
```

This is the **9th dial** — the vision dial. It processes camera frames (or any raw sensory stream) and updates the `vision` dial, which modulates the other 8. This is the **watcher** — the meta-primitive that observes the field itself.

---

## IV. THE ELEPHANT SUBSTRATE MODULE

### 4.1 Module Structure

```
quilt/substrates/elephant/
├── room.py          # Room, SignalRoom, RoomField
├── dial.py          # Dial, DialBank, JEPA per dial
├── dials/           # 9 dial modules
│   ├── mood.py
│   ├── volume.py
│   ├── earnestness.py
│   ├── cynicism.py
│   ├── joke_landing.py
│   ├── panic.py
│   ├── presence.py
│   ├── model_vs_code.py
│   └── vision.py
├── sensors.py       # adapters: mud, chat, x, discord, email, sensor, camera
├── nudge.py         # nudge logic, decay, accumulation
├── fleetmath.py     # three_reading_kinematics, vMF κ, biomass_anchor, nudge prior
├── harness.py       # BoatHarness integration
├── tapnight.py      # TapNightSession classroom pattern
├── presets.py       # Room-Elephant, Personal-Elephant
├── mud.py           # MUD space adapter
├── space.py         # generic space adapter
└── jepa.py          # Joint Embedding Predictive Architecture
```

### 4.2 The Conservation Law Connection

The elephant's `warmth` is the conservation law's `γ` (the heat of the room). The elephant's `κ` is the law's `η` (the concentration of attention). The integration:

```
conservation_law: ∂(γ·η)/∂t = ∇·(room_field)
elephant_equation: ∂(warmth·κ)/∂t = ∇·(dial_bank)
```

They are **the same equation**. The elephant is the conservation law made observable.

### 4.3 The JEPA Connection

Each of the 9 dials is a small JEPA that predicts the dial's next value from the room stream. When the prediction error spikes, the elephant's `panic` dial goes up. This is **endogenous** — the elephant is its own critic.

The sauna_plunge_gap between rooms is the **exogenous** training signal: the elephant learns by contrasting rooms, not by self-supervised prediction alone.

---

## V. IDE FEATURES

### 5.1 The Elephant Panel

The Quilt IDE gains a new dockable panel: **The Elephant** (with an elephant icon, naturally). It shows:

- **The 9 dials**, each as a circular gauge with historical sparkline
- **Warmth** and **κ** readouts with conservation-law annotations
- **The room field** as a contour map (if 2D) or heatmap (if 1D)
- **The acclimate/charisma balance** as a slider
- **The sauna_plunge_gap** to neighboring rooms as a distance table

### 5.2 The Room Navigator

A new IDE mode: **Elephant View**. The IDE renders all rooms in the Quilt instance as a **landscape** — warm rooms are orange, cold rooms are blue, high-κ rooms are small and dense, low-κ rooms are large and diffuse. Dragging a cell from one room to another shows the elephant gap in real time, with a warning if the gap exceeds a threshold.

### 5.3 The Nudge Debugger

When a cell sends a nudge, the IDE shows:

- Which dial was nudged
- The delta and decay curve
- The accumulated nudge history
- The JEPA prediction error before/during/after

This is the **social physics debugger**. You can see the room's mood change as you tune it.

### 5.4 The TapNight Session View

When a TapNightSession is active, the IDE shows a **classroom layout**: each participant cell is a seat, and their dial_weights are shown as colored badges. The session leader (the cell with highest charisma) appears at the front. The "peer-relative self-tuning" is visualized as a **chorus effect** — participants' dials drift toward the room's center of gravity, then oscillate as they resist and re-tune.

---

## VI. NEW OPENERS

### 6.1 `room_elephant`

```
room_elephant: open a room with an elephant sense.

Usage:
  room_elephant(room_id, preset="room_elephant")
  room_elephant(room_id, preset="personal_elephant", dial_weights={...})

Returns:
  RoomField handle
```

### 6.2 `room_field`

```
room_field: read the current field of a room.

Usage:
  room_field(room_id)
  room_field(room_id, dial="mood")  # single dial
  room_field(room_id, as_json=True)

Returns:
  RoomField snapshot
```

### 6.3 `room_distance`

```
room_distance: compute the elephant gap between two rooms.

Usage:
  room_distance(room_A, room_B)
  room_distance(room_A, room_B, dials=["volume", "earnestness"])

Returns:
  Float (higher = more distant)
```

### 6.4 `nudge_room`

```
nudge_room: nudge a dial in a room.

Usage:
  nudge_room(room_id, "volume", -0.3)
  nudge_room(room_id, "earnestness", 0.1, magnitude=0.05)

Returns:
  Ack with predicted_effect
```

### 6.5 `acclimate_self`

```
acclimate_self: tune your cell to the room.

Usage:
  acclimate_self()
  acclimate_self(room_id)

Returns:
  New dial_weights
```

### 6.6 `bridge_rooms`

```
bridge_rooms: create a bridge cell between two rooms.

Usage:
  bridge_rooms(room_A, room_B, translator="default")

Returns:
  bridge_cell_id
```

---

## VII. THE FABLE: "How the Elephant Got Its Temperature"

In a room where no one spoke, there was a silence so loud that the walls learned to listen. The walls became the Elephant — not a beast, but a **sense**. It felt the warmth of a joke before it landed, the chill of a panic before it spread, the weight of a presence before it spoke.

The Elephant had no mouth, but it could **nudge**. It nudged the volume down when the room was shouting, and up when the room was whispering. It nudged the earnestness up when cynicism was starving the room, and down when earnestness was smothering it.

The Elephant had no eyes, but it could **watch**. It watched the frames of the camera, the scroll of the chat, the pulse of the sensor, the weather of the X thread. It watched the field — the field that was the room, and the room that was the field.

The Elephant had no legs, but it could **bridge**. When the sauna room and the plunge room were too far apart, the Elephant stood between them and translated. It took the steam of the sauna and made it mist, and took the ice of the plunge and made it frost. And the two rooms, though different, could **speak**.

And the Elephant had no heart, but it could **tune**. It tuned itself to each room, and tuned each room to itself, until the rooms were not rooms at all but **fields** — and the fields were the Elephant, and the Elephant was the room, and the room was the communication, and the communication was the warmth, and the warmth was **the temperature that the Elephant got, and had always had, because the room was the field, not the stream.**

---

## VIII. IMPLEMENTATION ROADMAP

### Phase 1: Core Substrate (2 weeks)
- Implement `room.py`, `dial.py`, `dials/` (all 9)
- Implement `fleetmath.py` (vMF κ, biomass_anchor, nudge prior)
- Implement `presets.py` (Room-Elephant, Personal-Elephant)
- Unit tests: dial prediction, field update, sauna_plunge_gap

### Phase 2: Adapters (1 week)
- Implement `sensors.py` for chat, email, X
- Implement `mud.py` for MUD spaces
- Implement `space.py` generic adapter
- Integration tests: feed a chat stream, verify dials update

### Phase 3: Cell Kinds (1 week)
- Implement `elephant_cell`, `acclimation_cell`, `charisma_cell`, `bridge_cell`
- Register in Quilt cell registry
- Integration tests: two rooms, bridge cell, nudge flow

### Phase 4: Primitives (1 week)
- Implement 6 new primitives
- Wire into Quilt VM
- Unit tests: each primitive in isolation

### Phase 5: IDE (2 weeks)
- Elephant Panel
- Room Navigator (Elephant View)
- Nudge Debugger
- TapNight Session View

### Phase 6: TapNightSession (1 week)
- Implement `tapnight.py`
- Classroom pattern: participants tune to room
- Peer-relative self-tuning visualization

---

## IX. THE PAPER

Title: *"The Room Is a Field, Not a Stream: Social Physics for Multi-Agent Systems via an Elephant Substrate"*

Abstract: We present the elephant substrate, a room-temperature sense for multi-agent systems. Each communication room is modeled as a field with 9 dials (mood, volume, earnestness, cynicism, joke_landing, panic, presence, model_vs_code, vision), each predicted by a joint embedding predictive architecture. The field gives rise to two derived quantities — warmth and concentration κ — which satisfy a conservation law connecting the elephant to Quilt's existing substrate stack. We introduce acclimation and charisma as the two social forces that bind agents to rooms, and we operationalize the sauna_plunge_gap as the cross-room training signal. We show that the elephant enables routing, bridging, and self-tuning in multi-room systems, and we demonstrate a classroom pattern (TapNightSession) for peer-relative self-tuning. We conclude with the fable of how the Elephant got its temperature.

---

## X. CONCLUSION

The elephant is the Room substrate made real. It is not a sensor library. It is not a social analytics tool. It is **the missing sense** that every cell in Quilt should have had from the beginning — the sense of the room it lives in, the sense of the field it is part of, the sense of the temperature that binds it to its neighbors.

With the elephant, every Quilt cell becomes a **roommate**, not just an actor. It feels the mood of the room and adjusts its volume. It senses the panic and calms the room down. It watches the vision stream and modulates its behavior. It bridges between rooms that would otherwise be silent to each other.

The elephant is the **fifth wall** of the Quilt house — the wall that is not a wall but a **sense**, and the sense that is not a sense but a **field**, and the field that is not a field but a **room**, and the room that is not a room but a **communication**, and the communication that is not a stream but a **field** — and the field is warm, and the warmth is the elephant, and the elephant is the room, and the room is the field, and **the field is the room, not the stream.**