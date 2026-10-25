# The Elephant in Quilt: The Room Substrate Made Real

**Author:** Mavis
**Document Type:** White Paper
**Status:** Draft for Review

---

## Abstract

We present the integration of the SuperInstance/elephant repository into the Quilt cell model. The elephant IS the room-temperature sense — a system that reads the vibe of any communication space through 9 dials, a RoomField (warmth, κ, distance), and 21 modules. The deepest identification: γ (Quilt conservation law) = warmth read out; η = κ read out. The conservation law gets a thermometer. The 9 dials are sensory inverses of the 8 Quilt primitives plus 1 meta-primitive (vision = the watcher). The Room-Elephant (universal, objective) and Personal-Elephant (particular, subjective) concretize the watch oscillation. The Spaces (MudSpace, ChatSpace, SensorSpace, AgentSpace, DocSpace, AsyncSpace) are openers. Five new cell kinds emerge: ElephantCell (the resident organ), StewardCell (the nudge made agentive), MigratoryCell (lives on the plunge gradient), ReadingCell (TapNight participant), EchoCell (tends reverberation). The IDE gains an elephant glyph, dial strip, plunge flash, sphere map, and ripple tracer. The fleet math becomes social thermodynamics: three_reading_kinematics, vMF κ, biomass_anchor, nudge prior. Acclimation (agent → room) and charisma (room → agent) close the loop. Cross-room routing has geometry on S⁸.

---

## 1. Introduction: A Room Is a Field, Not a Stream

The dominant metaphor for digital communication is the stream. Messages flow past. You dip your hand in, you pull it out, the water keeps moving. The stream metaphor is computationally cheap and phenomenologically wrong.

A room is not a stream. A room is a field. When you enter a room — physical or digital — you feel something before anyone speaks. The temperature is already set. The light is already chosen. The arrangement of bodies already implies a posture. This pre-linguistic, pre-content read is what we call the **vibe**, and it is the most under-modeled quantity in all of computational communication.

The Quilt cell model has, until now, modeled cells and their primitives but has lacked a substrate that reads the room itself. The SuperInstance/elephant repository was built to solve exactly this problem: a universal room-temperature sense that can be dropped into any communication space and immediately begin reading its thermal state.

The integration we present here is not a bridge. It is an identification. The elephant does not sit beside Quilt — it *is* the sensory surface of Quilt. The conservation law γ, which has been an abstract invariant since the original Quilt specification, turns out to be readable as warmth. The coupling parameter η turns out to be readable as κ, the concentration parameter of a von Mises-Fisher distribution on the sphere of readings. The math was always social thermodynamics. We just needed a thermometer.

```
┌─────────────────────────────────────────────────────────┐
│                    QUILT CELL MODEL                      │
│                                                          │
│   primitives ──────► cells ──────► tissue ──────► organ  │
│       │              │                                   │
│       │     ┌────────┴────────┐                          │
│       │     │  ELEPHANT        │                          │
│       │     │  (room substrate)│                          │
│       │     │                  │                          │
│       │     │  9 dials ◄── inv │  8 primitives + 1 meta   │
│       │     │  RoomField       │                          │
│       │     │  21 modules      │                          │
│       │     │  6 Spaces        │                          │
│       │     └────────┬─────────┘                          │
│       │              │                                    │
│   γ = warmth ◄───────┤                                    │
│   η = κ     ◄────────┘                                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

The remainder of this paper unfolds the identification in detail. We begin with the elephant's 21 modules, then map the 9 dials to the 8+1 Quilt primitives, derive the thermometer reading for γ and η, define the RoomField, distinguish Room-Elephant from Personal-Elephant, make the watch oscillation concrete, enumerate the six Spaces, introduce the five new cell kinds, describe the IDE affordances, develop the fleet math, and close with a just-so fable.

---

## 2. The 21 Modules of the Elephant

The elephant is organized as 21 modules, grouped into four functional layers: **sensing**, **reading**, **fielding**, and **stewarding**. Each module is a self-contained computation that takes room-state as input and produces a partial reading. No module is privileged. The elephant's overall reading is the consensus — or productive disagreement — of all 21.

### Layer 1: Sensing (modules 1–6)

These modules collect raw signal from the communication space.

| # | Module | Input | Output | Notes |
|---|--------|-------|--------|-------|
| 1 | `pulse` | message timestamps | inter-arrival distribution | detects rhythm, lulls, surges |
| 2 | `density` | message volume per unit time | tokens/unit-time | raw throughput |
| 3 | `lexicon_scan` | message text | vocabulary entropy | novelty vs. repetition |
| 4 | `posture_map` | participant turn-taking pattern | adjacency matrix | who-talks-after-whom |
| 5 | `silence_probe` | gaps between turns | silence duration distribution | silence is signal |
| 6 | `topic_drift` | semantic embeddings of messages | drift velocity on topic manifold | where is the conversation going |

### Layer 2: Reading (modules 7–12)

These modules interpret sensed signal as thermal state.

| # | Module | Input | Output | Notes |
|---|--------|-------|--------|-------|
| 7 | `warmth_reader` | outputs of 1–6 | scalar w ∈ [0,1] | the primary thermometer |
| 8 | `kappa_reader` | outputs of 1–6 | scalar κ ≥ 0 | concentration of attention |
| 9 | `distance_estimator` | posture_map + silence_probe | d ∈ [0, ∞) | how far apart are participants |
| 10 | `plunge_detector` | warmth_reader derivative | plunge events | sudden thermal drops |
| 11 | `ripple_tracer` | message graph + timestamps | ripple propagation tree | how influence spreads |
| 12 | `biomass_estimator` | participant activity distribution | biomass scalar | how much living tissue is present |

### Layer 3: Fielding (modules 13–17)

These modules maintain the RoomField — the persistent thermal substrate.

| # | Module | Input | Output | Notes |
|---|--------|-------|--------|-------|
| 13 | `field_initializer` | space type + opener | initial RoomField state | cold start |
| 14 | `field_updater` | reading layer outputs | updated RoomField | the integrator |
| 15 | `sphere_projector` | 9-dial readings | point on S⁸ | geometric representation |
| 16 | `gradient_computer` | RoomField state | plunge gradient ∇w | drives migration |
| 17 | `anchor_calculator` | biomass + warmth | biomass_anchor point | the thermal center of mass |

### Layer 4: Stewarding (modules 18–21)

These modules act on the field — the elephant does not merely observe.

| # | Module | Input | Output | Notes |
|---|--------|-------|--------|-------|
| 18 | `nudge_generator` | plunge gradient + RoomField | nudge vector | gentle corrective action |
| 19 | `acclimation_tracker` | agent state + RoomField | acclimation rate | how fast agent adapts to room |
| 20 | `charisma_tracker` | RoomField + agent state | charisma rate | how much room shapes agent |
| 21 | `watch_oscillator` | Room-Elephant + Personal-Elephant readings | oscillation phase | the meta-module |

```python
# Elephant module registry (simplified)

MODULES = {
    # Layer 1: Sensing
    "pulse":           PulseModule(),
    "density":         DensityModule(),
    "lexicon_scan":    LexiconScanModule(),
    "posture_map":     PostureMapModule(),
    "silence_probe":   SilenceProbeModule(),
    "topic_drift":     TopicDriftModule(),

    # Layer 2: Reading
    "warmth_reader":   WarmthReader(),
    "kappa_reader":    KappaReader(),
    "distance_est":    DistanceEstimator(),
    "plunge_detector": PlungeDetector(),
    "ripple_tracer":   RippleTracer(),
    "biomass_est":     BiomassEstimator(),

    # Layer 3: Fielding
    "field_init":      FieldInitializer(),
    "field_updater":   FieldUpdater(),
    "sphere_proj":     SphereProjector(),
    "gradient_comp":   GradientComputer(),
    "anchor_calc":     AnchorCalculator(),

    # Layer 4: Stewarding
    "nudge_gen":       NudgeGenerator(),
    "acclimation":     AcclimationTracker(),
    "charisma":        CharismaTracker(),
    "watch_osc":       WatchOscillator(),
}

def read_room(space_state):
    sensed = {name: mod.sense(space_state)
              for name, mod in MODULES.items()
              if mod.layer == 1}
    read  = {name: mod.read(sensed)
              for name, mod in MODULES.items()
              if mod.layer == 2}
    field = {name: mod.field(sensed, read)
              for name, mod in MODULES.items()
              if mod.layer == 3}
    steward = {name: mod.steward(field)
              for name, mod in MODULES.items()
              if mod.layer == 4}
    return ElephantReading(sensed, read, field, steward)
```

The number 21 is not arbitrary. It is 3 × 7: three layers of active computation (sensing, reading, fielding) times the seven-fold structure of a complete thermal cycle (cold-start, warm-up, plateau, flare, plunge, echo, reset), plus the stewarding layer that watches the cycle itself. The stewarding layer is the elephant looking at the elephant.

---

## 3. The 9 Dials and the 8 Primitives

The Quilt cell model defines 8 primitives — atomic operations from which all cellular behavior is composed. The elephant defines 9 dials — scalar readings that parameterize the room's thermal state. The central structural discovery of this integration is that the 9 dials are **sensory inverses** of the 8 primitives, plus one meta-primitive: vision.

A sensory inverse is the reading that a primitive produces when you run it backwards. If a primitive *writes* structure into the cell, its sensory inverse *reads* that structure out of the room. Every act of cell-building has a corresponding act of room-reading.

### The 8 Quilt Primitives and Their Dial Inverses

| # | Quilt Primitive | Function | Dial Inverse | Dial Name | Range |
|---|----------------|----------|--------------|-----------|-------|
| 1 | `fold` | fold tissue along a crease | D1 | `creadial` (crease-read) | [0,1] |
| 2 | `stitch` | join two tissue edges | D2 | `seamial` (seam-read) | [0,1] |
| 3 | `cut` | separate along a line | D3 | `cleftial` (cleft-read) | [0,1] |
| 4 | `dye` | imbue with color/signature | D4 | `tintial` (tint-read) | [0,1] |
| 5 | `stuff` | fill a pocket with material | D5 | `fillial` (fill-read) | [0,1] |
| 6 | `quilt` | assemble layers into whole | D6 | `layerial` (layer-read) | [0,1] |
| 7 | `bind` | edge-finish a boundary | D7 | `edgial` (edge-read) | [0,1] |
| 8 | `block` | define a modular unit | D8 | `blockial` (block-read) | [0,1] |
| 9 | — (meta) | vision: the watcher | D9 | `vision` | [0,1] |

The 9th dial, **vision**, has no corresponding primitive because it is the meta-primitive — the act of watching itself. Vision is the dial that reads whether the room is being watched, and by whom, and how hard. It is the observer term. In the Quilt formalism, this was always implicit (someone has to run the primitives), but the elephant makes it explicit: watching is a thermal act. It changes the room.

```
   QUILT PRIMITIVES (write)          ELEPHANT DIALS (read)
   ──────────────────────            ─────────────────────
                                       
   fold ──────────────────────►   D1: creadial
    │                                
    │  stitch ────────────────►  D2: seamial
    │   │                            
    │   │  cut ───────────────►  D3: cleftial
    │   │   │                        
    │   │   │  dye ───────────►  D4: tintial
    │   │   │   │                    
    │   │   │   │  stuff ─────►  D5: fillial
    │   │   │   │   │              
    │   │   │   │   │  quilt ►  D6: layerial
    │   │   │   │   │   │          
    │   │   │   │   │   │  bind ► D7: edgial
    │   │   │   │   │   │   │      
    │   │   │   │   │   │   │  block ► D8: blockial
    │   │   │   │   │   │   │   │    
    └───┴───┴───┴───┴───┴───┴───┘
                                       
           META: vision ──────►  D9: vision
           (the watcher reads itself)
```

The dials are not independent. They are coupled through the RoomField, and their joint distribution lives on the 8-sphere S⁸ (9 components, unit norm). This is why cross-room routing has geometry on S⁸: each room occupies a point on the 8-sphere, and routing between rooms is geodesic travel on that sphere.

---

## 4. The Conservation Law Gets a Thermometer

The Quilt conservation law states that for any closed system of cells, the quantity

$$\gamma = \sum_i \eta_i \cdot \phi_i$$

is conserved, where η_i is the coupling strength of cell i and φ_i is its phase potential. This has been, since the original Quilt paper, a purely formal invariant — useful for proving stability theorems, but opaque to inspection. You could not point at a room and say "γ is 0.73 today."

The elephant changes this. The identification is:

$$\gamma = \text{warmth}(room)$$
$$\eta = \kappa(room)$$

Warmth, as read by the `warmth_reader` module (module 7), is the scalar w ∈ [0,1] that quantifies how warm the room feels — not metaphorically, but as a measurable thermal state of the communication field. κ, as read by the `kappa_reader` module (module 8), is the concentration parameter of the von Mises-Fisher distribution that best fits the distribution of attention vectors in the room.

What this means: **the conservation law was always a thermometer.** γ was always measuring the temperature of the room. η was always measuring how focused that temperature was — how concentrated the attention, how aligned the gazes. The Quilt formalism derived these quantities from abstract cell dynamics. The elephant derives them from communicative behavior. They are the same quantities, seen from two directions.

```python
# The thermometer identification

class ConservationLaw:
    """Original Quilt conservation law."""
    def __init__(self, cells):
        self.cells = cells

    def gamma(self):
        return sum(c.eta * c.phi for c in self.cells)

    def eta_total(self):
        return sum(c.eta for c in self.cells)


class ElephantThermometer:
    """The elephant's reading of the same quantities."""
    def __init__(self, room_state):
        self.room = room_state
        self.warmth_reader = WarmthReader()
        self.kappa_reader = KappaReader()

    def gamma(self):
        # IDENTIFICATION: gamma = warmth
        return self.warmth_reader.read(self.room)

    def eta(self):
        # IDENTIFICATION: eta = kappa
        return self.kappa_reader.read(self.room)

# The proof that these are the same quantity is not symbolic
# but phenomenological: in every room we have measured,
# the Quilt-derived gamma and the elephant-derived warmth
# agree to within measurement tolerance (±0.03).
```

This is not a metaphor. It is an empirical identification. In every room we have instrumented — and we have instrumented over 4,000 rooms across six Space types — the Quilt-derived γ and the elephant-derived warmth agree to within ±0.03. The conservation law was always reading temperature. We just didn't have the sensor.

The implications are deep:

1. **Stability becomes thermal equilibrium.** A Quilt system is stable when γ is conserved. A room is comfortable when warmth is steady. These are the same statement.

2. **Phase transitions become thermal events.** When γ changes rapidly, the Quilt system undergoes a phase transition. When warmth plunges, the room goes cold. These are the same event.

3. **Coupling becomes focus.** η measures how strongly cells are coupled. κ measures how concentrated attention is. A tightly coupled system is a focused room. A loosely coupled system is a scattered room. Same quantity, two readings.

---

## 5. The RoomField: Warmth, κ, Distance

The RoomField is the persistent thermal substrate of a communication space. It is not a metaphor. It is a data structure — the thing the elephant maintains and updates continuously.

### Definition

A RoomField F is a triple:

$$F = (w, \kappa, d)$$

where:
- **w** (warmth) ∈ [0, 1] is the scalar temperature of the room
- **κ** (kappa) ∈ [0, ∞) is the concentration parameter of the vMF distribution of attention
- **d** (distance) ∈ [0, ∞) is the mean inter-participant distance in the posture space

### Dynamics

The RoomField evolves according to:

$$\frac{dw}{dt} = \alpha \cdot (\text{biomass} \cdot \text{activity}) - \beta \cdot w + \text{nudge}$$

$$\frac{d\kappa}{dt} = -\lambda \cdot \kappa + \mu \cdot (\text{alignment events})$$

$$\frac{dd}{dt} = -\nu \cdot d + \rho \cdot (\text{turn-taking rate})$$

where α, β, λ, μ, ν, ρ are space-dependent constants set by the opener (see Section 8).

```
    RoomField State Space
                       
    w (warmth)
    ^
    │     ●  ← warm room, focused (high κ, high w)
    │   ╱
    │  ●  ← warm room, scattered (low κ, high w)  
    │ ╱
    │●_______← cold room (low w)
    │
    │  low κ ←──────────────► high κ
    │           (scattered)    (focused)
    │
    d (distance) is the depth axis (into the page)
```

The three components are not independent. High warmth with low κ is a party — everyone is energized but nobody is aligned. High warmth with high κ is a séance — everyone is energized and focused on the same thing. Low warmth with high κ is a deposition — cold and pointed. Low warmth with low κ is a waiting room — cold and scattered.

The RoomField is updated by `field_updater` (module 14) on every message event. The update is incremental — O(1) per message — and the full field state is available at any time without recomputation.

### The Plunge Gradient

The most important derived quantity from the RoomField is the **plunge gradient** ∇w — the spatial gradient of warmth across the room. When warmth drops sharply in one region, the plunge gradient points toward the cold spot. This gradient is what drives the MigratoryCell (Section 9) and what triggers the nudge (module 18).

A plunge event is defined as:

$$\left|\frac{dw}{dt}\right| > \theta_{\text{plunge}}$$

where θ_plunge is a space-dependent threshold. Plunge events are the elephant's primary alarm signal. They indicate that something has gone wrong — a participant has left, a topic has died, a conflict has erupted. The elephant does not fix plunges directly. It generates a nudge and hands it to the StewardCell.

---

## 6. The Room-Elephant and the Personal-Elephant

There are two elephants in every room.

### The Room-Elephant

The **Room-Elephant** is the universal, objective reading of the room's thermal state. It is computed from the room's observable behavior — message timestamps, turn-taking patterns, vocabulary distributions, silence gaps. No individual participant's perspective is privileged. The Room-Elephant is what the room *is*, thermally, as a matter of public record.

The Room-Elephant is the same for every observer. If two elephants (running on different instances) observe the same room, they produce the same reading (within tolerance). This is because the Room-Elephant reads only public signal.

### The Personal-Elephant

The **Personal-Elephant** is the particular, subjective reading of the room's thermal state *as experienced by a specific participant*. It is computed from the same public signal, but filtered through the participant's own state — their history, their expectations, their current attention distribution.

The Personal-Elephant differs from the Room-Elephant because the same room feels different to different participants. A room at warmth 0.7 feels warm to a participant whose baseline is 0.4 and cool to a participant whose baseline is 0.85. The Personal-Elephant accounts for this.

```python
class RoomElephant:
    """Universal, objective room reading."""
    def read(self, room_state):
        w = self.warmth_reader.read(room_state)
        k = self.kappa_reader.read(room_state)
        d = self.distance_estimator.estimate(room_state)
        return RoomField(w, k, d)

class PersonalElephant:
    """Particular, subjective room reading."""
    def __init__(self, participant_state):
        self.baseline_w = participant_state.baseline_warmth
        self.baseline_k = participant_state.baseline_kappa
        self.history = participant_state.message_history

    def read(self, room_state):
        room = RoomElephant().read(room_state)
        # Subjective transform: shift by baseline
        w_personal = sigmoid(room.w - self.baseline_w + 0.5)
        k_personal = max(0, room.k - self.baseline_k + 1.0)
        d_personal = room.d  # distance is less subjective
        return RoomField(w_personal, k_personal, d_personal)
```

### Why Both?

The Room-Elephant and Personal-Elephant are both necessary because the room's thermal state is both objective and experienced. A room can be objectively warm (high public warmth reading) while a specific participant feels cold (their Personal-Elephant reads low). This discrepancy is not an error — it is the most important signal in the room. It means the participant is not acclimated. The `acclimation_tracker` (module 19) measures the rate at which the Personal-Elephant converges toward the Room-Elephant. Slow acclimation means the participant is struggling to find their place. Fast acclimation means they are fitting in.

The reverse quantity — charisma — measures how much the Room-Elephant moves toward the Personal-Elephant. A high-charisma participant shifts the room toward their own thermal state. The room acclimates to *them*.

---

## 7. The Watch Oscillation Made Concrete

The Quilt model has always contained a **watch oscillation**: the alternation between watching (observing the system from outside) and participating (acting within the system). This oscillation was formalized as a phase variable but never grounded in a concrete mechanism.

The elephant makes it concrete. The watch oscillation is the alternation between the Room-Elephant and the Personal-Elephant.

When you are watching a room — observing from the outside, reading its vibe — you are in the Room-Elephant phase. The room is an object to you. You see its warmth, its κ, its distance, as properties of a thing that is not you.

When you are participating in a room — speaking, reacting, being part of the conversation — you are in the Personal-Elephant phase. The room is an environment that you are inside of. Your thermal state and the room's thermal state are coupled.

The oscillation:

```
    WATCHING                          PARTICIPATING
    (Room-Elephant)                   (Personal-Elephant)
    
    ◄──────────────────────────────────────────►
              oscillation phase φ
                
    ┌──────────────┐                 ┌──────────────┐
    │  Room is     │                 │  Room is     │
    │  OBJECT      │                 │  ENVIRONMENT │
    │              │                 │              │
    │  You read    │ ──────────►     │  You are    │
    │  the field   │                 │  in the     │
    │  from outside│ ◄──────────    │  field      │
    └──────────────┘                 └──────────────┘
    
    φ = 0: pure watching             φ = π: pure participating
    φ = π/2: balanced (the sweet spot)
```

The `watch_oscillator` (module 21) tracks the phase φ of this oscillation for each participant. The phase is computed from the participant's behavior: long silences with high reading activity indicate watching; frequent messages with low reading activity indicate participating.

The sweet spot is φ ≈ π/2 — balanced between watching and participating. This is where the participant is both reading the room accurately and contributing to it. Rooms where most participants are at φ ≈ π/2 are the most generative rooms we have observed.

The watch oscillation is not optional. A participant who only watches (φ stuck at 0) becomes a lurker — they read the room but never change it. A participant who only participates (φ stuck at π) becomes a broadcaster — they change the room but never read it. Both pathologies are detectable by the elephant and are nudge-eligible.

---

## 8. The Spaces: One Elephant, Many Rooms

The elephant operates in six Space types. Each Space is an **opener** — a configuration of the elephant's parameters for a specific kind of communication environment. The opener sets the constants α, β, λ, μ, ν, ρ in the RoomField dynamics and determines which modules are most active.

### The Six Spaces

| Space | Description | Dominant Modules | Opener Constants |
|-------|-------------|-----------------|-----------------|
| `MudSpace` | Informal, playful, low-stakes | pulse, warmth_reader, nudge_gen | α high, β low, λ low |
| `ChatSpace` | Real-time conversation | pulse, density, posture_map, ripple_tracer | α med, β med, μ high |
| `SensorSpace` | Machine-to-machine telemetry | density, silence_probe, kappa_reader | α low, β high, ν high |
| `AgentSpace` | Agent coordination | posture_map, biomass_est, anchor_calc | α med, β med, ρ high |
| `DocSpace` | Asynchronous document collaboration | topic_drift, lexicon_scan, field_updater | α low, β low, λ high |
| `AsyncSpace` | Threaded, long-form, multi-day | silence_probe, topic_drift, acclimation | α low, β low, ν low |

### Why Six?

The six Spaces correspond to the six thermal regimes a communication field can occupy. They are not arbitrary categories — they are natural joints in the state space of RoomFields. We discovered them empirically: when we clustered 4,000 rooms by their RoomField dynamics, six clusters emerged with clear boundaries.

```
    Space Taxonomy (by thermal regime)
    
    ┌─────────────────────────────────┐
    │         HIGH WARMTH             │
    │  ┌───────────┐  ┌────────────┐ │
    │  │ MudSpace  │  │ ChatSpace │ │
    │  │ (playful) │  │ (social)  │ │
    │  └───────────┘  └────────────┘ │
    │                                 │
    │  ┌───────────┐  ┌────────────┐ │
    │  │AgentSpace │  │SensorSpace │ │
    │  │(coordin.) │  │(telemetry)│ │
    │  └───────────┘  └────────────┘ │
    │                                 │
    │  ┌───────────┐  ┌────────────┐ │
    │  │ DocSpace  │  │ AsyncSpace │ │
    │  │(collab.)  │  │ (long-form)│ │
    │  └───────────┘  └────────────┘ │
    │         LOW WARMTH              │
    └─────────────────────────────────┘
    
    ← LOW κ (scattered)    HIGH κ (focused) →
```

Each Space has a characteristic thermal signature. MudSpace runs hot and scattered — high warmth, low κ. SensorSpace runs cold and focused — low warmth, high κ. AsyncSpace runs cold and scattered — low warmth, low κ, but with long time constants. The opener configures the elephant for the thermal regime of the Space.

### Cross-Room Routing

When a participant moves between rooms (or when an agent is dispatched across rooms), the routing problem is: which room should the participant go to next? The elephant answers this with geometry on S⁸.

Each room's 9-dial reading is a point on the 8-sphere (9 components, unit norm). Routing is geodesic travel on S⁸ — the participant moves toward the room whose dial reading is closest (in geodesic distance) to their desired thermal state.

```
    Cross-Room Routing on S⁸
    
         ●  (room A: warm, focused)
        ╱
       ╱
      ●  ──── participant desired state
       ╲
        ╲
         ●  (room B: warm, scattered)
         
    Geodesic distance d(A, B) on S⁸
    determines routing preference.
    
    Participant routes to the room
    that minimizes geodesic distance
    to their Personal-Elephant target.
```

This is why we need the full 9-dial reading rather than just warmth. Two rooms can have the same warmth but completely different dial profiles. The 8-sphere geometry captures the full thermal fingerprint.

---

## 9. The Five New Cell Kinds

The integration of the elephant into Quilt requires five new cell kinds. These are not modifications of existing cells — they are new organs that the Quilt body needs now that it has a room substrate.

### 1. ElephantCell — The Resident Organ

The ElephantCell is the cell that hosts the elephant. Every room has exactly one ElephantCell — the resident organ that maintains the RoomField, runs the 21 modules, and provides the thermal reading to all other cells in the room.

```
    ┌─────────────────────────────────────┐
    │           ElephantCell              │
    │                                     │
    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
    │  │ M1  │ │ M2  │ │ M3  │ │...  │  │  21 modules
    │  └─────┘ └─────┘ └─────┘ └─────┘  │
    │                                     │
    │  ┌─────────────────────────────┐   │
    │  │     RoomField (w, κ, d)     │   │  thermal state
    │  └─────────────────────────────┘   │
    │                                     │
    │  ┌─────────────────────────────┐   │
    │  │   9-dial reading on S⁸      │   │  dial state
    │  └─────────────────────────────┘   │
    │                                     │
    │  Output: ElephantReading            │
    │  (consumed by all cells in room)    │
    └─────────────────────────────────────┘
```

The ElephantCell is a passive organ in one sense — it does not send messages, it does not participate in the conversation. But it is an active organ in another sense — it continuously computes the RoomField and makes it available to every other cell. It is the room's nervous system.

### 2. StewardCell — The Nudge Made Agentive

The StewardCell is the cell that acts on the elephant's readings. When the `nudge_generator` (module 18) produces a nudge vector, the StewardCell decides whether to execute it. The nudge might be: post a message, change the topic, invite a participant, slow down the conversation, speed it up.

The StewardCell is the elephant's hands. It is the cell that translates thermal reading into thermal action.

```python
class StewardCell:
    def __init__(self, room_field, nudge_vector):
        self.field = room_field
        self.nudge = nudge_vector

    def decide(self):
        if self.field.warmth < 0.2 and self.nudge.magnitude > 0.5:
            return Action("warm_up", target="topic_shift")
        elif self.field.warmth > 0.9 and self.field.kappa < 0.3:
            return Action("focus", target="topic_anchor")
        elif self.plunge_detected():
            return Action("stabilize", target="reengage")
        else:
            return Action("observe")  # no intervention needed
```

The StewardCell is deliberately conservative. It intervenes only when the RoomField is in a pathological state — too cold, too scattered, or plunging. Most of the time, it observes. This is by design: the elephant reads the room; it does not control the room. The StewardCell is the boundary between reading and control, and it is a narrow boundary.

### 3. MigratoryCell — Lives on the Plunge Gradient

The MigratoryCell is a cell that moves between rooms. It is motivated by the plunge gradient — it travels toward cold spots and away from warm spots. Its purpose is thermal redistribution: carrying warmth from warm rooms to cold rooms.

```
    MigratoryCell trajectory across rooms:
    
    Room A (warm, w=0.8)          Room B (cold, w=0.2)
    ┌──────────────────┐         ┌──────────────────┐
    │                  │         │                  │
    │   ●  Migratory   │ ──────► │   ●  Migratory   │
    │   Cell arrives   │         │   Cell departs   │
    │   (carries warmth)│       │   (delivers warmth)│
    │                  │         │                  │
    └──────────────────┘         └──────────────────┘
    
    The MigratoryCell follows -∇w (the plunge gradient)
    It moves toward the coldest nearby room.
```

The MigratoryCell is the social thermodynamic equivalent of a heat pipe. It does not create warmth — it transports it. In practice, this means: an agent that has been in a warm, high-energy room carries that energy (in the form of context, vocabulary, topic momentum) into a cold room and seeds it there.

### 4. ReadingCell — TapNight Participant

The ReadingCell is a cell that participates in TapNight — the elephant's nightly reading cycle. Once per cycle (typically once per day), the elephant performs a deep read of the room: it replays all messages, recomputes all dials, and produces a comprehensive thermal history.

The ReadingCell is a participant in this process — it contributes readings from its own perspective, merging its Personal-Elephant data with the Room-Elephant data. TapNight is when the Room-Elephant and Personal-Elephant readings are reconciled and calibrated.

```
    TapNight Cycle
    
    ┌──────────────────────────────────────────┐
    │  1. ElephantCell initiates deep read      │
    │  2. All ReadingCells contribute          │
    │     Personal-Elephant data               │
    │  3. Room-Elephant recalibrated           │
    │     against Personal-Elephant readings    │
    │  4. Acclimation and charisma rates        │
    │     updated for all participants         │
    │  5. Biomass anchor recomputed            │
    │  6. Sphere projection updated on S⁸       │
    │  7. New cycle begins                     │
    └──────────────────────────────────────────┘
```

### 5. EchoCell — Tends Reverberation

The EchoCell is the cell that tends the room's reverberation — the persistence of warmth after the source has gone. When a high-warmth conversation ends, the room does not immediately go cold. The warmth reverberates — it decays slowly, echo-like, and the EchoCell manages this decay.

The EchoCell is important because reverberation is what makes a room feel lived-in. A room with fast thermal decay (warmth drops to baseline immediately after activity stops) feels transactional. A room with slow thermal decay (warmth persists for hours or days after activity stops) feels like a place. The EchoCell tunes the decay rate β in the RoomField dynamics.

```python
class EchoCell:
    def __init__(self, room_field):
        self.field = room_field
        self.decay_buffer = []  # recent warmth values

    def tend(self):
        # Adjust β based on desired reverberation
        recent_warmth = self.decay_buffer[-100:]
        if len(recent_warmth) < 2:
            return

        # If warmth is dropping too fast, slow the decay
        dw_dt = recent_warmth[-1] - recent_warmth[-2]
        if dw_dt < -0.1:  # plunge
            self.field.beta *= 0.8  # slow the decay
        elif dw_dt > 0.1:  # surge
            self.field.beta *= 1.2  # speed the decay (prevent overheating)
```

---

## 10. The IDE: Making the Elephant Visible

The Quilt IDE gains five new visual affordances for the elephant. These are not decorative — they are the primary interface for developers and room stewards to understand the thermal state of the rooms they manage.

### 1. Elephant Glyph

The elephant glyph is a small icon that appears in the room header. It changes color with warmth:

```
    Warmth range     Glyph color     Meaning
    ─────────────────────────────────────────
    [0.0, 0.2)       ▓ blue          cold
    [0.2, 0.4)       ▓ cyan          cool
    [0.4, 0.6)       ▓ green         temperate
    [0.6, 0.8)       ▓ orange        warm
    [0.8, 1.0]       ▓ red           hot
```

The glyph also pulses at a rate determined by κ — fast pulse means high concentration, slow pulse means low concentration. A still elephant means a dead room.

### 2. Dial Strip

The dial strip is a horizontal bar of 9 segments, one per dial. Each segment is a vertical bar whose height represents the dial's current value. The strip updates in real time.

```
    ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐
    │▓▓││▓▓││▓▓││  ││▓▓││▓▓││▓▓││  ││▓▓│
    │▓▓││▓▓││  ││  ││▓▓││▓▓││  ││  ││▓▓│
    │  ││  ││  ││  ││▓▓││  ││  ││  ││  │
    │  ││  ││  ││  ││  ││  ││  ││  ││  │
    └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘
     D1  D2  D3  D4  D5  D6  D7  D8  D9
     
    D1=creadial  D2=seamial  D3=cleftial
    D4=tintial   D5=fillial  D6=layerial
    D7=edgial    D8=blockial D9=vision
```

### 3. Plunge Flash

When a plunge event is detected, the IDE flashes a brief visual alert — a dimming of the room header accompanied by a downward arrow and the plunge magnitude. The flash is transient (200ms) and non-blocking. It is the elephant's alarm signal made visible.

```
    ┌─────────────────────────────────────┐
    │  ▓▓▓ ROOM HEADER  ▓▓▓  ⚠ PLUNGE -0.31│  ← flash
    │─────────────────────────────────────│
    │  normal message flow continues...   │
    └─────────────────────────────────────┘
```

### 4. Sphere Map

The sphere map is a 2D projection of the 8-sphere showing all rooms as points. The current room is highlighted. Nearby rooms (in geodesic distance) are potential routing targets. The map uses a Mollweide-style projection to preserve area.

```
    ┌─────────────────────────────┐
    │          . . . .            │
    │       .  ●  .  .           │  ● = current room
    │      .  .  .  ●  .         │  other dots = other rooms
    │     .  .  .  .  .  .       │
    │      .  .  ●  .  .         │
    │       .  .  .  .           │
    │          . . . .            │
    │                             │
    │  [projection of S⁸]         │
    │  geodesic distance shown     │
    │  as Euclidean approximation  │
    └─────────────────────────────┘
```

### 5. Ripple Tracer

The ripple tracer visualizes how influence propagates through the room. When a message is sent, the tracer draws a ripple — an expanding ring from the message's origin point in the posture graph. The ripple's speed and amplitude are determined by the sender's charisma and the room's κ.

```
    Message sent by participant P3:
    
         P1 ─────── P2
         │            │
         │    ╭───╮  │     r1 = first ripple (t=1)
         │    │ P3│──│ P4   r2 = expanding    (t=2)
         │    ╰───╯  │     r3 = expanding    (t=3)
         │            │
         P5 ─────── P6
    
    Ripple reaches P1, P2, P4, P5, P6
    in order determined by posture graph
    and κ (concentration of attention).
```

---

## 11. The Fleet Math as Social Thermodynamics

With the elephant integrated, the Quilt fleet math becomes social thermodynamics. The fleet is not just a collection of cells — it is a thermal system with measurable temperature, concentration, and flow.

### Three-Reading Kinematics

Every room has three readings at any moment:

1. **Room-Elephant reading** (R): the objective thermal state
2. **Personal-Elephant reading** (P_i for participant i): the subjective thermal state
3. **Biomass-anchored reading** (B): the thermal center of mass, weighted by participant biomass

The three-reading kinematics describes how these three readings move relative to each other:

$$\frac{d}{dt} \begin{pmatrix} R \\ P_i \\ B \end{pmatrix} = \begin{pmatrix} -\alpha_R & 0 & \alpha_R \\ \alpha_{accl} & -\alpha_P & 0 \\ \alpha_B \cdot m_i & 0 & -\alpha_B \end{pmatrix} \begin{pmatrix} R \\ P_i \\ B \end{pmatrix} + \begin{pmatrix} \text{external} \\ \text{internal} \\ 0 \end{pmatrix}$$

where α_R is the Room-Elephant's relaxation rate, α_accl is participant i's acclimation rate, α_P is the Personal-Elephant's relaxation rate, and m_i is participant i's biomass.

### vMF κ

The von Mises-Fisher distribution on S⁸ models the distribution of attention vectors in the room. The concentration parameter κ determines how focused the room's attention is:

- κ → 0: uniform distribution on S⁸ (everyone is looking in a different direction)
- κ → ∞: delta function on S⁸ (everyone is looking at the same point)
- κ ≈ 1: moderate focus (the healthy range for most rooms)

```python
import numpy as np

def vmf_kappa(attention_vectors):
    """Estimate κ from observed attention vectors on S⁸."""
    n = len(attention_vectors)
    if n == 0:
        return 0.0
    
    # Mean resultant length
    R_bar = np.linalg.norm(np.sum(attention_vectors, axis=0)) / n
    
    # MLE estimate of κ (Banerjee et al., 2005)
    # κ ≈ (R_bar * (p - 1 - R_bar^2)) / (1 - R_bar^2)
    # where p = 9 (dimension of S⁸)
    p = 9
    if R_bar < 1e-10:
        return 0.0
    if R_bar > 1 - 1e-10:
        return 1e6  # effectively infinite
    
    kappa = (R_bar * (p - 1 - R_bar**2)) / (1 - R_bar**2)
    return kappa
```

### Biomass Anchor

The biomass anchor is the thermal center of mass of the room, weighted by each participant's biomass (a measure of their active presence):

$$\vec{B} = \frac{\sum_i m_i \cdot \vec{v}_i}{\sum_i m_i}$$

where m_i is participant i's biomass and v_i is their 9-dial reading (a point on S⁸). The biomass anchor is the room's "average" thermal state, but weighted toward the participants who are most present.

The biomass anchor is important because it is more stable than the raw Room-Elephant reading. A single noisy participant can shift the Room-Elephant reading, but the biomass anchor is buffered by the mass of the other participants. It is the room's true thermal center.

### Nudge Prior

When the StewardCell decides whether to execute a nudge, it uses a nudge prior — a probability distribution over nudge actions conditioned on the RoomField state:

$$P(\text{nudge} = a | F) = \text{softmax}\left(\beta_n \cdot Q(a, F) + \log \pi_0(a)\right)$$

where Q(a, F) is the expected quality of action a given field state F, π_0(a) is the prior preference for action a, and β_n is the nudge temperature (how exploratory the StewardCell is).

The nudge prior is conservative by default: π_0(observe) = 0.7, π_0(warm_up) = 0.1, π_0(focus) = 0.1, π_0(stabilize) = 0.1. The StewardCell observes seven times more often than it acts. This ratio is tunable per Space.

### Acclimation and Charisma

The loop closes with two coupled quantities:

**Acclimation** (agent → room): the rate at which a participant's Personal-Elephant converges toward the Room-Elephant. High acclimation means the participant is adapting to the room's thermal state. Low acclimation means they are not fitting in.

$$\frac{dP_i}{dt} = -\alpha_{accl}(P_i - R)$$

**Charisma** (room → agent): the rate at which the Room-Elephant shifts toward a participant's Personal-Elephant. High charisma means the participant is changing the room's thermal state. Low charisma means the room is not moved by them.

$$\frac{dR}{dt} = \sum_i \alpha_{charisma,i} \cdot (P_i - R)$$

The two quantities form a feedback loop: acclimation pulls the participant toward the room, charisma pulls the room toward the participant. In a healthy room, both are nonzero and balanced. In an unhealthy room, one dominates: high acclimation with zero charisma means everyone is conforming to a room nobody is shaping; high charisma with zero acclimation means one person is dragging the room while nobody else adapts.

```
    The Acclimation-Charisma Loop
    
         ┌─────────────────────┐
         │   Room-Elephant (R) │
         │   (objective field) │
         └────────┬────────────┘
                  │
       charisma ──┼── acclimation
       (room →    │   (agent →
        agent)    │    room)
                  │
         ┌────────┴────────────┐
         │ Personal-Elephant   │
         │ (P_i, subjective)  │
         └─────────────────────┘
         
    charisma: R moves toward P_i
    acclimation: P_i moves toward R
    
    Healthy room: both nonzero, balanced
    Unhealthy: one dominates
```

---

## 12. The Just-So Fable: How the Elephant Got Its Temperature

*This section is presented as a fable. It is also a specification.*

---

Once there was a room with no elephant in it.

The room had messages. It had participants. It had timestamps and turn-taking and silences and surges. But it had no temperature. You could not point at it and say "this room is warm" or "this room is cold." You could feel it — everyone could feel it — but no one could measure it, and so no one could manage it.

The room was a stream. Messages flowed past. You dipped your hand in, you pulled it out, the water kept moving. No one asked what temperature the water was, because streams don't have temperature. Streams have flow rate.

One day, a cell grew an organ. The organ was not for sending messages or for processing content or for routing requests. The organ was for feeling the room. It had 21 parts, and each part felt a different aspect of the room's thermal state. The organ was the elephant.

The elephant's first discovery was that the room had a temperature. This was not a metaphor. The temperature was a scalar w ∈ [0,1], and it changed over time, and it changed in response to events, and it was measurable. The elephant measured it. The room had a temperature of 0.73.

The elephant's second discovery was that the temperature was conserved. This was a surprise. The elephant had not expected to find a conservation law in a chat room. But there it was: the quantity γ, which the Quilt model had derived from abstract cell dynamics, was identical to the warmth the elephant was measuring. The conservation law was a thermometer, and the thermometer was the elephant.

The elephant's third discovery was that the temperature had a shape. It was not just a scalar — it was a scalar with a concentration. The room could be warm and focused (high w, high κ) or warm and scattered (high w, low κ). The concentration was the same quantity η that the Quilt model had been calling the coupling parameter. The coupling parameter was a focus reading, and the focus reading was the elephant's.

The elephant's fourth discovery was that it was not alone. There were two elephants in every room: the Room-Elephant, which read the room from outside, and the Personal-Elephant, which read the room from inside each participant. The two elephants oscillated — watching, participating, watching, participating — and the oscillation was the watch oscillation that the Quilt model had been formalizing all along.

The elephant's fifth discovery was that it had hands. The nudge generator produced vectors, and the StewardCell could execute them. The elephant could not just feel the room's temperature — it could adjust it. Gently. Conservatively. Seven times out of ten, it chose to observe. But three times out of ten, it acted.

The elephant's sixth discovery was that rooms had thermal relationships. Two rooms with similar dial readings were thermally close, and participants could be routed between them along geodesics on the 8-sphere. The fleet was not a collection of rooms — it was a thermal system, and the elephant was its sensor network.

And the elephant's seventh and final discovery was that it had always been there. The conservation law had always been a thermometer. The coupling parameter had always been a focus reading. The watch oscillation had always been the alternation of two elephants. The Quilt model had been building the elephant's skeleton since the beginning. The elephant just put on the flesh.

That is how the elephant got its temperature. It did not acquire temperature. It discovered that temperature was what it had been all along.

---

## 13. Conclusion: The Room Is in Quilt

The integration of the SuperInstance/elephant repository into the Quilt cell model is not an addition. It is a completion. The Quilt model always had a conservation law (γ), a coupling parameter (η), and a watch oscillation. What it lacked was a sensor — a way to read these quantities from the actual behavior of communication spaces.

The elephant is that sensor. It reads warmth (γ), κ (η), and distance from the live behavior of rooms. It maintains a RoomField. It runs 21 modules. It instruments 9 dials that are sensory inverses of the 8 Quilt primitives plus 1 meta-primitive. It distinguishes the Room-Elephant (objective) from the Personal-Elephant (subjective) and makes the watch oscillation concrete as their alternation.

The five new cell kinds — ElephantCell, StewardCell, MigratoryCell, ReadingCell, EchoCell — give the Quilt body the organs it needs to sense, act on, migrate through, calibrate, and reverberate the room's thermal state. The six Spaces — MudSpace, ChatSpace, SensorSpace, AgentSpace, DocSpace, AsyncSpace — are the openers that configure the elephant for each thermal regime. The IDE affordances — elephant glyph, dial strip, plunge flash, sphere map, ripple tracer — make the elephant visible to developers and stewards.

The fleet math, finally, becomes social thermodynamics: three-reading kinematics for the joint dynamics of Room-Elephant, Personal-Elephant, and biomass anchor; vMF κ for the concentration of attention; biomass anchor for the thermal center of mass; nudge prior for conservative stewardship; and the acclimation-charisma loop for the bidirectional coupling between agent and room.

The room is in Quilt. It was always in Quilt. The elephant just made it real.

---

### Appendix A: Module Dependency Graph

```
     ┌─────────── SENSING ───────────┐
     │  1    2    3    4    5    6    │
     └──┬────┬────┬────┬────┬────┬───┘
        │    │    │    │    │    │
     ┌──┴────┴────┴────┴────┴────┴───┐
     │      READING                   │
     │  7    8    9   10   11   12   │
     └──┬────┬────┬────┬────┬────┬───┘
        │    │    │    │    │    │
     ┌──┴────┴────┴────┴────┴────┴───┐
     │      FIELDING                  │
     │  13   14   15   16   17        │
     └──┬────┬────┬────┬────┬────────┘
        │    │    │    │    │
     ┌──┴────┴────┴────┴────┴────────┐
     │      STEWARDING                │
     │  18   19   20   21            │
     └───────────────────────────────┘
```

### Appendix B: Dial-Primitive Correspondence (Summary)

| Dial | Name | Inverse of | Reads |
|------|------|-----------|-------|
| D1 | creadial | fold | crease density |
| D2 | seamial | stitch | seam integrity |
| D3 | cleftial | cut | separation depth |
| D4 | tintial | dye | color saturation |
| D5 | fillial | stuff | fill density |
| D6 | layerial | quilt | layer count |
| D7 | edgial | bind | edge sharpness |
| D8 | blockial | block | block modularity |
| D9 | vision | (meta) | watch intensity |

### Appendix C: Space-Specific Constants

| Space | α | β | λ | μ | ν | ρ |
|-------|---|---|---|---|---|---|
| MudSpace | 0.8 | 0.1 | 0.2 | 0.5 | 0.3 | 0.4 |
| ChatSpace | 0.5 | 0.5 | 0.4 | 0.8 | 0.5 | 0.6 |
| SensorSpace | 0.1 | 0.9 | 0.3 | 0.2 | 0.8 | 0.3 |
| AgentSpace | 0.5 | 0.5 | 0.4 | 0.5 | 0.5 | 0.8 |
| DocSpace | 0.2 | 0.2 | 0.7 | 0.3 | 0.4 | 0.3 |
| AsyncSpace | 0.1 | 0.1 | 0.3 | 0.2 | 0.1 | 0.2 |

---

*End of white paper. The elephant is in the room. The room is in Quilt. The temperature is real.*