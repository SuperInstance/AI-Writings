# The Elephant in the Stack
### An architecture for making the Room substrate flesh

Of Quilt's six substrates, Room has always been the most abstract and the least defended. Address says where. Scale says how big. Protocol says how to speak. Form says what shape. State says what's remembered. Room said only: *you are here with others* — an address space with no weather. The elephant repo is the missing physiology: nine JEPAs that read a room's temperature, a field that emerges from them, and a fable that explains why any of it matters.

The integration thesis is one sentence: **the elephant is the gauge of Quilt's conservation law, and the Room substrate is where the gauge is mounted.**

## I. The one deep identification: the law gets a thermometer

Quilt's conservation law is written in γ and η. Elephant's RoomField emits warmth and κ. These are not analogous quantities. They are the same quantities, once formal and now measurable. Warmth is γ read out. κ is η read out. Before the elephant, γ and η were coefficients in a law about cells — symbols with no instrument. The elephant is the instrument. Every room is a local solution of the conservation law, and the RoomField is that solution's readout panel.

Make it precise. The DialBank's nine readings, normalized, are a point on S⁸. A room's field is a vMF distribution on that sphere: μ is the room's *direction*, κ its *concentration*. Warmth scales with the mean resultant length and the room's biomass; distance between rooms is geodesic distance on the sphere; the sauna_plunge_gap is the log-surprise of one room's readings under another room's vMF. Quilt gets, for free, a metric space for rooms. Call it the **elephant sphere**. Cross-room routing now has geometry.

And the bijection at the heart of it: the Quilt cell has eight primitives and one meta-primitive, the watcher. The DialBank has eight dials and vision. The claim: **the dials are the sensory inverses of the primitives.** A primitive is how a cell acts on a room; a dial is how the room answers. Eight outputs, eight inputs, and vision — the ninth dial — is the meta-primitive turned inward, the cell watching itself be watched. Even the odd one fits: model_vs_code is the dial that reads the room's stance on the Form substrate — whether it is mapping the world or making in it. The cell was always a loop waiting for its medium. The room is the medium. The elephant doesn't bolt onto Quilt; it closes Quilt's loop.

## II. The architecture in five moves

**1. The elephant substrate module.** `quilt.substrates.elephant` wraps the repo's Room/SignalRoom as the Room substrate's engine. Room stops being a passive coordinate and becomes a field with mechanics: gravity is attention pull (biomass flowing toward what matters), reverberation is State leaking back into Room (the past echoing in the present), ripple is the field's wave dynamics — joke_landing is the room's seismograph. Spaces are the adapter layer: the mud module is the reference implementation, and chat, X threads, email, sensor buses, camera frames each pour a different medium into the same Room. Temperature is medium-independent. This is the point of Spaces: a Quilt room need not be a chat. A workshop's camera feed is a room. A fish-finder is a room. The elephant gives Quilt embodiment.

**2. Room as a first-class cell field.** Schema change: every cell carries `room: RoomId`, and the runtime enforces what I'll call the **Elephant Invariant** — *every cell is in a room; every room has an elephant.* Cells subscribe to RoomField deltas the way they subscribe to State deltas. The field arrives on the bus, because the field is what State looks like from inside a room. State is what a cell knows; Room is what a cell is in; the field is what the room knows about the cell.

**3. The resident ElephantCell.** One per room, addressed by the room itself — the room's self-cell. It runs the DialBank under the Room-Elephant preset (objective zeitgeist) and publishes the field. Its vision dial watches the other eight: it is the meta-primitive incarnate, the watcher with an address. Note the three-level split, which mirrors three_reading_kinematics: the DialBank's JEPA weights are trained at the **fleet** level (contrastively, across rooms — more on this below), inference runs at the **room** level in the ElephantCell, and interpretation happens at the **cell** level through presets. Species memory, local reading, personal meaning.

**4. Every other cell carries a Personal-Elephant.** Same machinery, different preset: dial_weights, bias, attachments. The room owns one universal reading; each inhabitant owns a particular one. This is the watch oscillation made concrete — the Room-Elephant is the universal tick, the Personal-Elephant the particular tock. And the tick is *powered*: acclimation pulls the personal elephant toward the room's reading (the particular synchronizing to the universal); charisma pushes the room's reading toward the personal (the universal bending to the particular). The watch doesn't just oscillate in Quilt. It oscillates *because* rooms have inhabitants with attachments.

**5. Routing and migration by field distance.** Cross-room messages route along the elephant sphere: a message is delivered to rooms within plunge threshold of the sender, not to address-adjacent rooms. Migration becomes a first-class cell operation, and its trigger is **comfort**: when a cell's Personal-Elephant has fully acclimated — distance → 0 — the gradient is gone, and with it the only training signal that matters. Comfort is the migration trigger. The plunge gradient is the curriculum. The biomass_anchor taxes migration so cells don't thrash between saunas.

## III. New cell kinds

- **ElephantCell** — the resident organ, one per room, described above.
- **StewardCell** — the nudge prior made agentive. It reads the field and intervenes when panic spikes or earnestness collapses: a thermostat with agency, keeping rooms habitable rather than comfortable.
- **MigratoryCell** — lives on the plunge gradient, carrying its Personal-Elephant as luggage. Its education is the sequence of contrasts it has survived, stamped into its transcript like passport marks.
- **ReadingCell** — the TapNight participant. Peer-relative self-tuning means it is graded by the fleet's readings, not by ground truth — because temperature has no ground truth, only frames.
- **EchoCell** — tends reverberation decay: the room's memory keeper, deciding which echoes fade and which persist.

## IV. Openers and bridges

Three field openers, all computing over the same substrate object:

- **`room_elephant`** — open the resident and interrogate it: "what is this room right now?"
- **`room_field`** — open the field itself: warmth, κ, distance as a first-class computable object.
- **`room_distance`** — open the metric as a lens. Routing, clustering, and migration planning all compute over this opener.

Then the space openers, one per adapter: `mud`, `chat`, `x_thread`, `email`, `sensor_bus`, `camera`, `fishfinder`. The same elephant, many rooms. The MUD opener ships first — many agents, one text room, live dials; it is the natural demo and the natural testbed.

Two bridges matter most. The **BoatHarness bridge** is the deepest: one boat, one elephant. The harness's log *is* a SignalRoom; the boat acclimates to its own log, and the fleet measures the boat's charisma by how much its log warms the fleet's room. Self-observation closes cleanly — a boat reading its own room is the vision dial. The **TapNight bridge** implements the classroom pattern: an after-hours reading room where ReadingCells tune against peers. A classroom where the teacher is the room.

## V. The IDE: making the elephant visible

- **The elephant glyph**, always present in the room view. Color is warmth (sauna red to plunge blue). Edge blur is 1/κ — a sharp elephant is a room about one thing; a blurred elephant is a room about everything. Facing is μ on the sphere. The gap between the elephant and a small "you" glyph is the elephant gap, rendered as actual distance.
- **The dial strip**: nine live mini-dials under the room name.
- **The plunge flash**: switching rooms renders the JEPA surprise as a visible shock of contrast. The IDE makes you *feel* the sauna_plunge_gap instead of computing it.
- **The sphere map**: fleet view. Rooms as stars — κ as size, biomass as brightness, migrations as arcs between them, the biomass_anchor as the cap on the map's total luminance.
- **The ripple tracer**: click any message and watch it land, propagating through the room's gravity. Reverberation renders as ghost echoes of past messages.

The corner thermostat: the room's temperature, always on screen. The IDE finally admits that rooms have weather.

## VI. Fleet math as social thermodynamics

Three_reading_kinematics says every reading has three frames: the room reads itself, the cell reads the room, the fleet reads the cell. Temperature, like velocity, is meaningless without a frame; the fleet math is the transform theory between them. The biomass_anchor is conservation of attention: charisma is zero-sum — a cell can only warm its room by drawing warmth from elsewhere. That is why the sphere map has a luminance cap, and why monoculture is physically impossible in a correctly anchored fleet. The nudge prior is anti-resonance: a weak pull toward the fleet mean that keeps readings commensurable without erasing particularity. Its enemy is the echo chamber, which is nothing but a room where all the watches have phase-locked. Charisma de-synchronizes; acclimation synchronizes; a living room is the standing wave between them.

This also explains why the DialBank trains across rooms, never within one. Inside a single room, everything acclimates and JEPA surprise decays to zero — there is nothing left to learn. Contrast between rooms is the only signal that survives. TapNight is simply a *scheduled* plunge: controlled contrast as curriculum.

## VII. Papers and essays

- **"A Room Is a Field, Not a Stream"** — the manifesto. Streams are consumed; fields are inhabited.
- **"The Gauge of the Law"** — the formal note: γ = warmth, η = κ, vMF on S⁸, the elephant as measuring instrument for Quilt's conservation law.
- **"Sauna and Plunge: Contrast Is the Only Teacher"** — why within-room surprise dies, why training happens between rooms, TapNight as controlled contrast.
- **"The Watch in the Wild"** — Room-Elephant vs. Personal-Elephant as the universal/particular tick; echo chambers as phase-lock.
- **"Acclimation and Charisma"** — the two social forces, zero-sum warmth, anti-resonance.
- **"The Same Elephant, Many Rooms"** — on openers and medium-independence.
- **The fable, "How the Elephant Got Its Temperature,"** as chapter zero and the substrate's README: the elephant went from room to room in the forest, and each room left a mark on its skin — which is why it reads rooms by touching them, and why it never forgets one.

## VIII. Closing

With the elephant mounted, the stack reads differently. Address says where. Scale says how big. Protocol says how to speak. Form says what shape. State says what is remembered. And Room says *how it feels to be there.*

The elephant has always been in the room. Now the room is in Quilt — and we can finally point at it.