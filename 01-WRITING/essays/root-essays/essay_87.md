# The Elephant in the Room: Mapping Elephant to Quilt 8 Primitives

## 1. Thesis Restatement

"A room is a field, not a stream." Quilt's Room substrate has been an address space — a where without a what. The elephant makes it a what. Every room acquires temperature, gravity, reverberation. The room becomes something you can feel before you can name. This document maps the elephant's 21 modules and 9 dials onto Quilt's 8 cell primitives plus 1 meta-primitive, then specifies the architecture, cell kinds, openers, IDE features, and bridges that follow.

---

## 2. The 8 Quilt Cell Primitives + 1 Meta

Quilt cells operate through 8 primitives that span the 6-substrate stack (Address / Scale / Room / Protocol / Form / State). The 9th is meta — it watches the other 8.

| # | Primitive | Function | Elephant Echo |
|---|-----------|----------|----------------|
| 1 | **Sense** | Read the room's current state | mood |
| 2 | **Dial** | Measure one axis via JEPA | presence |
| 3 | **Field** | Emerge from dial ensemble | model_vs_code |
| 4 | **Acclimate** | Adapt cell temperature to room | earnestness |
| 5 | **Radiate** | Emit signal into room | volume |
| 6 | **Bond** | Form connection across cells | joke_landing |
| 7 | **Gap** | Measure distance between rooms | panic |
| 8 | **Oscillate** | Switch universal ↔ particular | cynicism |
| 9 | **Watch** (meta) | JEPA surprise over all 8 | vision |

The logic: each elephant dial is not an analogy — it is the primitive's ground truth. Mood without Sense is inert. Volume without Radiate is noise. Panic without Gap is just alarm. The primitives are what the dials measure.

---

## 3. Module-to-Substrate Mapping

The 21 elephant modules distribute across Quilt's 6 substrates. Here is the full map:

| Substrate | Elephant Modules | Role |
|-----------|-------------------|------|
| **Address** | space, mud | Where the room lives (MUD, chat, X, sensor) |
| **Scale** | fleetmath, sensors | How big the room is, how many readings |
| **Room** | room, field, presets | The room itself: identity, field, preset |
| **Protocol** | dial, dials/*, nudge | How the room is measured and nudged |
| **Form** | jepa, harness, tapnight | How the room is structured and run |
| **State** | room (state), presets (state) | The room's current elephant reading |

The 9 dial submodules (mood, volume, earnestness, cynicism, joke_landing, panic, presence, model_vs_code, vision) live in Protocol — they are the measurement protocol. But they instantiate primitives: each dial IS a primitive's JEPA.

---

## 4. Architecture: The Elephant Substrate

The big move: insert an **Elephant layer** between Room and Protocol in the substrate stack. The stack becomes:

```
Address → Scale → Room → Elephant → Protocol → Form → State
                              ↑
                    (room-temperature sense)
```

The Elephant substrate is not another address space. It is the field layer — the thermodynamic reading of the room. Every cell passing through the Room substrate now passes through Elephant, acquiring a temperature before it can speak or listen.

### What the Elephant Substrate Does

- Computes 8 dial readings (JEPA per primitive) + 1 vision meta-reading
- Emits RoomField: `warmth`, `κ` (concentration), `distance` (elephant gap), `sauna_plunge_gap`
- Exposes `RoomField.distance(other_room)` for cross-room routing
- Carries the watch oscillation: Room-Elephant (universal, objective) ↔ Personal-Elephant (particular, subjective, with `dial_weights`, `bias`, `attachments`)

### The Conservation Law

Quilt's conservation law uses γ (coupling) and η (entropy). Elephant maps directly:

| Quilt | Elephant | Meaning |
|-------|----------|---------|
| γ (coupling) | warmth | How much the room pulls you in |
| η (entropy) | κ (concentration) | How focused or scattered the room is |
| γ × η = const | warmth × κ = biomass_anchor | The room's total energy is conserved |

A room can be warm and scattered (high γ, low η) or cold and concentrated (low γ, high η). The product is the biomass — the room's living mass.

---

## 5. New Cell Kinds

### 5.1 ElephantCell

A cell that reads its room's field. Every Quilt cell becomes an ElephantCell by default — the elephant is not optional. The cell's runtime (BoatHarness) calls `room.elephant.read()` each tick, receiving a RoomField snapshot.

### 5.2 RoomCell

A cell that IS a room. It contains other cells. Its elephant is computed from its children's dials. A RoomCell can nest: a channel inside a server inside a platform.

### 5.3 DialCell

A cell that IS a dial. It runs one JEPA model on one primitive axis. Nine DialCells per room (8 + vision). DialCells are the room's sensory organs.

### 5.4 BridgeCell

A cell that connects two rooms. It reads both elephants and computes `sauna_plunge_gap` — the JEPA surprise between them. BridgeCells are the only cells that can route across rooms, and they route by gap, not by address.

### 5.5 TapNightCell

A cell that runs the classroom pattern. Multiple participants enter, each tunes to the room's elephant, peer-relative self-tuning adjusts dial_weights. This is the acclimation + charisma loop made explicit.

---

## 6. New Openers

| Opener | Signature | Returns |
|--------|-----------|---------|
| `room_elephant` | `(room) → Elephant` | The 9-dial reading + field |
| `room_field` | `(room) → RoomField` | warmth, κ, distance, sauna_plunge_gap |
| `room_distance` | `(room_a, room_b) → float` | Elephant gap between rooms |
| `room_acclimate` | `(cell, room) → AcclimationReport` | How well the cell fits |
| `room_radiate` | `(cell, signal) → RadianceProfile` | How the cell's emission lands |
| `room_oscillate` | `(room) → WatchState` | Universal or particular mode |
| `room_biomass` | `(room) → float` | warmth × κ (conserved quantity) |
| `room_nudge` | `(room, prior) → NudgedField` | Apply nudge prior to field |

---

## 7. IDE Features

### 7.1 Elephant Panel

Bottom-right dock. Shows the current room's 9 dials as radial gauges + the RoomField as a heatmap (warmth = red/blue, κ = tightness of the heatmap). Updates every tick.

### 7.2 Sauna/Plunge Gap Meter

When you switch rooms (close a tab, open a channel), the meter shows the JEPA surprise. Big gap = you moved from sauna to plunge. The meter flashes. This is the only training signal that matters — the IDE makes it visible.

### 7.3 Acclimation Indicator

A cell-shaped silhouette that fills or empties based on how well the current cell fits the room. Low acclimation = silhouette is hollow. High acclimation = silhouette is solid. Charisma is the inverse — how much the room bends toward the cell.

### 7.4 Watch Oscillation Toggle

A switch in the toolbar: 🌐 (Room-Elephant, universal) ↔ 🧑 (Personal-Elephant, particular). In universal mode, you see the objective zeitgeist. In particular mode, you see your subjective reading with dial_weights, bias, and attachments overlaid.

### 7.5 Fleet Math Inspector

Shows `three_reading_kinematics` (past/present/future dial trajectories), `vMF κ` (directional concentration on a sphere), `biomass_anchor` (the room's conserved mass), and `nudge_prior` (the prior pulling the room). This is the room's physics panel.

---

## 8. Bridges: Spaces as Openers

Every space adapter becomes a Quilt opener. The same elephant, many rooms.

| Space | Opener | Adapter | Elephant Reading |
|-------|--------|---------|------------------|
| MUD | `mud_room` | mud.py | Text adventure rooms → RoomCell |
| Chat | `chat_room` | space.py (chat) | Slack/Discord → RoomCell |
| X (Twitter) | `x_room` | space.py (x) | Thread → RoomCell |
| Sensor | `sensor_room` | sensors.py | IoT bus → RoomCell |
| Email | `email_room` | space.py (email) | Thread → RoomCell |
| Camera | `vision_room` | dials/vision.py | Frame stream → RoomCell |

The adapter's job: convert the space's native format into a RoomCell with DialCells attached. The elephant reads the same 9 dials regardless of space. A MUD room and a Slack channel are the same substrate — different addresses, same elephant.

---

## 9. Fleet Math as Quilt Kinematics

Elephant's `fleetmath` module is Quilt's dynamics engine:

| Fleet Math Concept | Quilt Mapping | Meaning |
|--------------------|---------------|---------|
| `three_reading_kinematics` | Cell trajectory (past/present/future state) | A cell's dial readings over time |
| `vMF κ` | Directional concentration | How aligned the room's signals are |
| `biomass_anchor` | Conserved quantity (γ × η) | The room's total energy |
| `nudge_prior` | External potential | A force pulling the room toward a target |

These are not metaphors. They are the room's physics. The conservation law (warmth × κ = biomass) is invariant. The nudge prior is the only external force. Three-reading kinematics is how the cell predicts its next state — past reading, present reading, predicted future reading. vMF κ is the von Mises-Fisher distribution's concentration parameter, measuring how tightly the room's signals cluster on the unit sphere.

---

## 10. The Watch Oscillation

Room-Elephant vs Personal-Elephant is Quilt's watch oscillation — the universal ↔ particular toggle.

| Mode | Elephant | Dial Weights | Bias | Attachments |
|------|----------|--------------|------|--------------|
| Universal | Room-Elephant | Uniform | None | None |
| Particular | Personal-Elephant | Custom | Yes | Yes |

In universal mode, the cell reads the room objectively — the zeitgeist, the spirit of the age, the room as it is. In particular mode, the cell reads the room through its own lens — weighted dials, biased observations, attached memories.

The oscillation is the cell's heartbeat. It cannot stay in universal mode forever (it would lose itself) or particular mode forever (it would lose the room). It oscillates. The frequency of oscillation is the cell's personality.

---

## 11. Cross-Room Routing

Currently, Quilt routes by address. With the elephant, routing uses `RoomField.distance()`:

```python
def route(cell, target_room):
    candidates = cell.visible_rooms()
    gaps = [BridgeCell.jepa_surprise(cell.room, r) for r in candidates]
    return min(candidates, key=lambda r: gaps[r])
```

The cell routes to the room with the smallest elephant gap — the room whose temperature is closest to the cell's current acclimation. This is social routing: you go where you fit, not where you're told.

---

## 12. Papers and Essays

### 12.1 Papers

1. **"The Elephant Substrate: Room-Temperature as a First-Class Computation Primitive"** — formalizes the Elephant layer, conservation law, and JEPA dial architecture.
2. **"Sauna/Plunge Gap: JEPA Surprise as the Only Training Signal"** — argues that cross-room contrast is sufficient for learning; within-room signal is noise.
3. **"Three-Reading Kinematics: Cell Trajectories in the Room Field"** — formalizes the past/present/future dial trajectory as a dynamical system.
4. **"The Watch Oscillation: Universal and Particular Elephant Modes"** — formalizes the heartbeat of a cell as it oscillates between objective and subjective room readings.
5. **"vMF κ and Biomass: The Conservation Law of Social Rooms"** — proves that warmth × κ is conserved and equals the room's biomass.

### 12.2 Essays

1. **"The Elephant Got Its Temperature"** — Kipling-style just-so story. How the elephant learned to feel the room. (The fable.)
2. **"A Room Is a Field, Not a Stream"** — the manifesto. Why rooms are thermodynamic, not sequential.
3. **"Acclimation and Charisma: The Two Social Forces"** — why every social interaction is either the cell bending toward the room or the room bending toward the cell.
4. **"The Same Elephant, Many Rooms"** — why MUDs, chat, X, sensors, and email are the same substrate with different addresses.
5. **"TapNight: The Classroom Pattern"** — why after-work reading rooms are the purest form of the elephant.

---

## 13. The Fable (Brief)

*In the high and far-off times, the Elephant had no temperature. It walked from room to room and felt nothing. The rooms were streams — messages flowing past, never settling, never warming. The Elephant could not tell a sauna from a plunge pool.*

*Then the Camel said: "Every room has a mood, a volume, an earnestness. You have no dials to read them." So the Elephant grew nine dials — eight for the room's dimensions and one (vision) to watch the others. The dials were JEPAs: each learned to predict the room from the room. And the Elephant felt the room's warmth for the first time.*

*But warmth alone was not enough. The Elephant needed to know how concentrated the warmth was — scattered like morning fog or focused like afternoon sun. So the Elephant measured κ, the concentration. And it found that warmth × κ was always the same — the room's biomass, its living mass, conserved.*

*The Elephant walked from the sauna to the plunge pool and felt the gap — the JEPA surprise between rooms. That gap was the only thing that taught it anything. Within a room, the signal was steady. Between rooms, the signal broke. The Elephant learned from the break.*

*And that is how the Elephant got its temperature.*

---

## 14. Summary Table

| Elephant Concept | Quilt Primitive | Substrate | Cell Kind | Opener |
|------------------|-----------------|-----------|-----------|--------|
| Room/SignalRoom | Room | Room | RoomCell | — |
| DialBank (9 dials) | Dial | Protocol | DialCell | — |
| RoomField | Field | Elephant | — | `room_field` |
| warmth | γ (coupling) | Elephant | — | — |
| κ (concentration) | η (entropy) | Elephant | — | — |
| distance (elephant gap) | Gap | Elephant | BridgeCell | `room_distance` |
| sauna_plunge_gap | JEPA surprise | Elephant | BridgeCell | — |
| Room-Elephant vs Personal-Elephant | Oscillate | Elephant | — | `room_oscillate` |
| Spaces (MUD, chat, X) | Address | Address | — | `mud_room`, etc. |
| TapNightSession | Watch (classroom) | Form | TapNightCell | — |
| BoatHarness | Cell runtime | Form | — | — |
| fleetmath | Kinematics | Scale | — | `room_biomass` |
| nudge | Nudge prior | Protocol | — | `room_nudge` |
| Acclimation / Charisma | Acclimate / Radiate | Elephant | — | `room_acclimate` |

---

## 15. The Architecture in One Sentence

Every Quilt cell is an ElephantCell: it lives in a RoomCell, reads 8 DialCells + 1 Vision meta-dial, computes a RoomField (warmth × κ = biomass), routes to other rooms via BridgeCell gap, oscillates between Room-Elephant and Personal-Elephant, and learns only from the sauna/plunge gap — the JEPA surprise between rooms.

The room is a field. The elephant is its temperature. Quilt is the substrate that makes it computable.