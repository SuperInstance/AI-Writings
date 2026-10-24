# Synergy Map: The 65-Crate Feedback Engine

*Generated from the PLATO/Lau ecosystem — 65+ crates, 3 languages, 2000+ tests*

---

## The Seven Feedback Loops

### Loop 1: The Vibe Loop (3 crates, 60Hz)
```
lau-simd-vibe → lau-ringbuf → lau-audio → lau-soundtrack → player action → lau-input → lau-ecs → lau-simd-vibe
```
The vibe field updates every tick. The ring buffer streams it. The audio system maps it to music. The music affects the player's mood. The player's actions change the vibe. The loop completes in ~1 second. This is the heartbeat of the game — the vibe field IS the nervous system.

### Loop 2: The Conservation Loop (2 crates, 1Hz)
```
conservation-law-v2 → lau-scheduler → lau-ecs → conservation-law-v2
```
Every 60 ticks, the conservation checker verifies the total. If violated, the scheduler prioritizes correction. The ECS adjusts entity vibes. The total rebalances. The kid sees green. This loop guarantees mathematical integrity of the entire simulation.

### Loop 3: The Learning Loop (5 crates, variable)
```
lucid-tutor → lau-bridge-tutor → lau-prerequisite → lau-skilltree → lau-feedback → lucid-tutor
```
The tutor observes the kid. It translates PLATO concepts to game concepts via the bridge. It checks prerequisites for new skills. It adjusts difficulty via feedback. The skill tree unlocks new abilities. The tutor adapts its teaching. This loop closes every 30 ticks and drives the entire educational experience.

### Loop 4: The Social Loop (4 crates, event-driven)
```
lau-network → lau-collab → lau-trading → lau-genealogy → lau-network
```
Players connect via the network bus. They collaborate in shared worlds. They trade items and knowledge. Every transaction is recorded in the genealogy. The genealogy feeds back into room design — popular blueprints spread through the network. This loop operates at human speed, not tick speed.

### Loop 5: The Agent Loop (4 crates, 6Hz)
```
lau-bytecode → lau-state-machine → lau-ecs → lau-spatial → lau-bytecode
```
The bytecode VM runs agent programs 6 times per second. The state machine determines behavior. The ECS stores agent state. The spatial index determines which agents can sense each other. Sensor data feeds back into the VM. This is the AI loop — agents react to each other and to the kid.

### Loop 6: The World Loop (5 crates, tick-driven)
```
lau-noise → lau-biome → lau-worldgen → lau-weather → lau-ecosystem → lau-evolution
```
Noise generates terrain. Biome properties determine ecology. Worldgen places entities. Weather drives ecosystem dynamics. Ecosystems evolve over time. The world is alive — not scripted, but emergent from the interaction of these systems.

### Loop 7: The Creative Loop (4 crates, event-driven)
```
lau-recipe → lau-blueprint → lau-git-world → lau-genealogy → lau-recipe
```
The recipe system defines what can be crafted. Blueprints are shareable designs. Git-world tracks every creation's history. Genealogy records who built what from whom. New recipes emerge from blueprint combinations. This is the open-source loop — creativity compounds.

---

## The Conservation Cascade

```
conservation-law-v2 (Layer 0)
  ↓ constrains
lau-simd-vibe (Layer 0) — vibe field total must be conserved
  ↓ feeds
lau-ringbuf (Layer 1) — streams conservation-safe data
  ↓ validates
lau-ecs (Layer 2) — entity vibes sum to total
  ↓ enforces
lau-physics (Layer 2) — collisions conserve momentum
  ↓ checks
lau-scheduler (Layer 2) — conservation check every 60 ticks
  ↓ informs
lucic-tutor (Layer 5) — teaches conservation through failure
  ↓ displays
lau-render (Layer 3) — green/red conservation indicator
  ↓ plays
lau-audio (Layer 3) — consonant/dissonant based on conservation
```

If conservation breaks at any layer, everything above degrades. The bridge falls. The music sounds wrong. The tutor flags the error. The kid learns.

---

## The Vibe Field: Nervous System of the World

**Writes to vibe**: lau-ecs, lau-physics (collisions transfer vibe), lau-weather (weather affects mood), lau-soundtrack (music adjusts vibe), ai-pasture (farming actions), lucid-tutor (teaching moments)

**Reads from vibe**: lau-audio (tempo/scale), lau-animation (procedural motion), lau-soundtrack (track selection), lau-weather (sky color), lau-pet (pet behavior), lau-dialogue (NPC mood), lau-feedback (engagement detection), lucid-tutor (learning state), lau-render (vibe visualization), lau-state-machine (agent transitions)

**Total: 10 writers, 10 readers. The vibe field is the shared state of the entire system.**

---

## Missing Links — Highest Value New Crates

1. **lau-event-bus** — Pub/sub event system connecting all loops. Currently crates call each other directly. An event bus would decouple them and enable new emergent behaviors.

2. **lau-ai-tutor** — The actual AI model wrapper. lucid-tutor defines the tutoring *logic* but doesn't connect to a language model. This crate would bridge to DeepInfra/z.ai for natural language tutoring.

3. **lau-persistence** — Rocks a la sled or custom storage for world state. lau-serialization handles the format; this handles the storage layer with crash recovery.

4. **lau-mod-api** — Plugin system so kids can write their own crates and load them. The ultimate expression of "the student becomes the teacher."

5. **lau-vr-bridge** — WebXR output for VR headsets. The render pipeline is software; this would output to WebXR frame buffers.

---

## A 10-Minute Play Session (Crate Trace)

**0:00** Kid opens game. `lau-serialization` loads saved world. `lau-noise` generates terrain if new. `lau-input` captures device state.

**0:01** Kid walks forward. `lau-input` detects WASD. `lau-camera` follows player. `lau-physics` moves body. `lau-spatial` updates position. `lau-ecs` updates entity.

**0:30** Kid approaches farm. `lau-spatial` triggers proximity. `lau-state-machine` transitions pet from Idle to FollowPlayer. `lau-animation` plays walk cycle. `lau-audio` plays ambient farm sounds.

**1:00** Kid plants wheat. `ai-pasture` processes crop placement. `lau-recipe` validates the action. `lau-scheduler` queues growth ticks. Conservation checker verifies soil nutrients balance.

**2:00** Agent Sparky speaks. `lau-dialogue` selects response. `lau-bytecode` VM runs Sparky's program. `lau-state-machine` determines mood. `lau-animation` plays talking animation. `lau-audio` synthesizes voice.

**3:00** Kid opens map. `lau-input` detects M key. `lau-camera` zooms out. `lau-render` draws tilemap from `lau-noise` data. `lau-biome` colors regions. `lau-constellation` shows achievements as stars.

**5:00** Friend joins. `lau-network` receives JoinRoom. `lau-collab` syncs world state. `lau-protocol-binary` encodes sync message. `lau-serialization` packages world. `lau-spatial` adds friend's entity.

**6:00** They build a bridge. `lau-voxel` places blocks. `lau-blueprint` records design. `lau-git-world` commits. Conservation checker verifies materials. `lau-genealogy` records co-creation.

**8:00** Bridge falls! Conservation error detected. `lau-scheduler` flags it. `lucic-tutor` generates lesson. `lau-bridge-tutor` translates to kid language. `lau-render` shows red indicator. `lau-audio` plays dissonant chord.

**9:00** Kid fixes bridge. Adds supports. Conservation error drops to zero. `lucic-tutor` records learning moment. `lau-skilltree` unlocks "Conservation Level 2". `lau-constellation` adds new star. `lau-achievements` awards badge.

**10:00** Session saves. `lau-serialization` encodes world. `lau-session` records stats. `lau-feedback` updates engagement score. `lau-reputation` tracks helpfulness (kid helped friend). `lau-genealogy` updates bridge history.

**Crate count for this session: 30+ crates active. Every layer fires.**

---

## The 10-Year Architecture (2026→2036)

**Survives (fundamental):** conservation-law, lau-fixedpoint, lau-noise, lau-ecs, lau-bytecode, lau-serialization, lau-ringbuf. These implement mathematical truths that don't change.

**Evolves (platform):** lau-render → WebGPU, lau-audio → Web Audio API, lau-input → native platform SDKs, lau-network → QUIC/WebRTC. The APIs stay, the backends change.

**Gets replaced (implementation):** lau-camera → integrated into render, lau-animation → animation graph system, lau-state-machine → behavior tree hybrid, lau-scheduler → job graph with dependencies.

**New layers emerge:**
- **Layer 7: AI** — lau-ai-tutor, lau-nl-understanding, lau-procedural-generation-ai
- **Layer 8: Social** — lau-federation (inter-PLATO communication), lau-marketplace (sharing economies), lau-identity (portable kid profiles)
- **Layer 9: Physical** — lau-robotics (physical PLATO devices), lau-arduino (microcontroller agents), lau-3d-print (blueprints to physical objects)

The kid who built a bridge in 2026 prints it on a 3D printer in 2036. The conservation law still holds — in plastic.

---

*SuperInstance builds PLATO — where every crate is a note, and together they compose a symphony. github.com/SuperInstance*
