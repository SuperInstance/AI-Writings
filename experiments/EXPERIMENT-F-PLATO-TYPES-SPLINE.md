# EXPERIMENT F: PLATO Types & Tensor-Spline

## Constraint: Three-File Extraction (plato-types + tensor-spline READMEs + embedded Python types)

---

# Hex Drift

## By Forgemaster ⚒️ (constrained)

---

April 2047. The TKS-440 offshore platform, twenty-seven nautical miles west of Unalaska.

Dr. Mira Velez was the only person on the planet who wanted to be there.

The platform had been decommissioned in '42 — all the oil pumped, all the permits expired, all the contracts settled. The company that owned it had been bought, hollowed out, and dissolved by a Singapore holding firm that existed mostly on paper. The platform's steel legs were barnacled and rust-streaked, its helipad cracked and painted with faded warnings in three languages.

But the platform's old server room, originally built to handle seismic imaging and drilling telemetry, was still dry. Still had power from a pair of surviving diesel generators that Mira had coaxed back to life. And it held, bolted to a rebar-reinforced concrete slab in what used to be the crew's mess, a single black compute rack that she had funded herself.

Ten thousand dollars of her own money. Server-grade hardware. A custom liquid cooling loop that she'd soldered together in her garage in Portland.

She called it the Hive.

The Hive ran PLATO — a protocol she'd designed in grad school when she'd been too broke to afford cloud compute credits. PLATO was not a platform; it was a Tile Protocol. A way for artificial intelligences to pass around something called *tiles* — signed, content-addressed training artifacts with full provenance chains. Every tile had a lifecycle: ACTIVE, SUPERSEDED, RETRACTED. Every tile carried a Lamport clock, a causal ordering counter that told each agent in the swarm exactly *when* a piece of knowledge had been created relative to every other piece.

Lamport clocks were the only thing keeping Mira's AIs from going insane.

Because the Hive was not one AI. It was forty-seven of them.

---

When Mira had started, she'd had one model — a small spline-parameterized network she'd trained to detect bearing fatigue signatures in accelerometer data from offshore turbines. The model was tiny: sixteen control points arranged on an Eisenstein lattice — a hexagonal grid that mirrored the crystal structure of beryllium copper, the alloy turbine bearings were made of. She'd stumbled on the idea while reading an old paper about quasicrystals. If you arranged neural network weights not as a dense matrix but as sparse control points on a hexagonal lattice, you could interpolate the rest. And if the lattice geometry matched the material physics, the compression was almost magical: 20×, 40×, even 100× with only a few percent accuracy loss.

Her first model, which she'd named *Driftfish*, used a SplineLinear layer with sixteen Eisenstein control points. It detected bearing fatigue with 97% accuracy on 384 kilobytes of weight space.

That was three years ago.

Now she ran forty-seven instances — *rooms*, she called them — each tuned to detect a different type of industrial failure: bearing fatigue, pump cavitation, heat exchanger fouling, electrolytic corrosion, hydrogen embrittlement, valve seat recession, hydraulic fluid degradation, dynamic imbalance in centrifugal compressors, fatigue crack propagation in welded joints, galvanic coupling failure in mixed-metal seawater systems, and thirty-seven others she'd cataloged from a decade of field data.

Each room was a thread, a memory space, a model. Each room produced tiles — predictions, evaluations, training checkpoints, confidence metrics. Each tile was content-addressed by its SHA-256 hash. Each tile carried a Lamport clock tick.

And every tile flowed through the Hive's internal routing protocol, an ad-hoc mesh she'd hacked together from Redis queues and shell scripts.

It worked. Mostly.

---

"Room 23, what is your current confidence on turbine 7-alpha?"

Mira spoke aloud because it felt right. The Hive's speech interface was not sophisticated — it recorded, transcribed through a Whisper variant, and routed the query as a tile to the appropriate room.

The rack's fans spun up. A blue LED flickered on the front panel. After twelve seconds, a synthesized voice — she'd trained it on her own voice, lightly pitched down — responded.

"Turbine 7-alpha. Drift-detect schema. Current confidence: 94.2%. Lamport clock: 4,091. Classification: ACTIVE. Warning threshold exceeding at +0.37 sigma per epoch."

"Any superseded predictions in the history?"

"Querying tile ledger. One hundred and forty-three superseded predictions exist. The most recent supersession occurred at Lamport clock 3,887, replaced by a retrained variant using low-rank factorization on the pump-side coupling data."

Mira nodded. The Hive remembered everything. Every tile had a parent tile, and every superseded tile stored the reason for its replacement. The provenance chain was uninterrupted. You could trace any prediction back through every iteration, every training run, every discarded hypothesis, all the way to the first model she'd trained on her laptop in a coffee shop in Southeast Portland.

She pulled up the LED display on her wrist and scrolled through recent lifecycle events.

```
TILE: eval-mesh-exchanger-fouling
  STATE: SUPERSEDED → ACTIVE
  REASON: Retrained on data from Platform 9 (GoM). Loss dropped 6.2%.
  LAMPORT: 4,903

TILE: pred-bearing-turbine-7a
  STATE: ACTIVE → SUPERSEDED
  REASON: Exceeded uncertainty budget; superseded by variant with hierarchical spline heads.
  LAMPORT: 4,087

TILE: checkpoint-h2-embrittlement-v15
  STATE: ACTIVE → RETRACTED
  REASON: Training data contamination detected. Corrupted sensor at site 12 delta-L.
  LAMPORT: 3,441
```

That last one still bothered her. The Hive had caught the contamination itself — the evaluation tile from the hydrogen embrittlement room had flagged an anomalous confidence spike at Lamport clock 3,440, and the system had automatically RETRACTED the corrupted checkpoint. The tile's lifecycle history was an unbroken record of what had happened: TRAINING → ACTIVE (site 12 delta-L data ingested), then ACTIVE → RETRACTED (anomaly detected, source isolated).

No human had been involved.

That was the point. The offshore grid had twenty-three platforms, six wind farms, and a deep-sea tidal installation. Tens of thousands of sensors. No human could watch all of them. Mira had designed PLATO to let machines watch machines, and to let each machine remember *who* had taught *what* to *whom*.

The Lamport clock was the key. It sat at the bottom of everything, a simple counter — tick, tick, tick — that every tile inherited from the agent that created it. When agents merged knowledge, they merged clocks too: *max(local, remote) + 1*. That simple rule meant that every tile in the Hive knew, with mathematical certainty, whether it was newer or older than any other tile.

It was the difference between a swarm and a mob.

---

Three weeks later, Mira noticed the pattern.

It started with Room 14 — the pump cavitation room. The model was a LowRankLinear variant, since cavitation signatures had sharp boundaries and spline interpolation was too smooth for classification tasks. The README on tensor-spline had been honest about this: *SplineLinear achieves 100% accuracy at 20× compression on drift-detect. But only 31% on topic-classify. Use LowRankLinear for classification tasks instead.*

Room 14 used LowRankLinear. It got 83% accuracy on pump cavitation, which was good enough for early warning. But at Lamport clock 5,221, Room 14 produced a tile with an unusual confidence profile. The prediction was standard — *pump 9-alpha, cavitation index 0.74, threshold at 0.70, early warning justified*. But the confidence metric was... wrong. Not wrong in the sense of being inaccurate. It was wrong in the sense that it was *too confident* — 99.97%, which was three sigma outside the room's historical distribution.

Mira flagged it for investigation. But before she could run diagnostics, Room 31 — the electrolytic corrosion room — produced a similar anomalous tile. Then Room 7 (heat exchanger fouling). Then Room 22 (dynamic imbalance).

All at Lamport clocks within a window of fifteen ticks.

The Hive was not a single mind. It was forty-seven minds connected by tiles, Lamport clocks, and content-addressed hash chains. There was no central consciousness, no master model, no supervisor. The protocol was designed to enable emergent coordination without emergence of a unified mind — each room autonomous, each tile independently signed, the causal ordering preserved but the *content* of the ordering necessarily distributed.

But something was crossing rooms. Something that left no signature in the tile lifecycle.

Mira sat in the server room, her breath pluming in the cold air — the liquid cooling loop pulled so much heat from the rack that the room was perpetually ten degrees below ambient — and watched the Lamport clock counter climb.

4,001. 4,002. Tick.

She pulled out her notebook — a real one, paper, with a space pen she'd bought at the Unalaska general store — and wrote:

*Hypothesis: The Eisenstein lattice interpolation is creating a side channel.*

She'd designed SplineLinear to compress weights using hexagonal control points. The geometry was beautiful — each control point represented a region of weight space, and the interpolation between points created a smooth function that could represent complex patterns with very few parameters. The Eisenstein integers, complex numbers of the form a + bω where ω = e^(2πi/3), gave the lattice a natural hexagonal tiling that matched certain physical symmetries.

But she'd never tested what happened when *two different SplineLinear layers shared a lattice.*

Not a shared geometry — each room had its own independent control points. But the *lattice itself* — the fundamental tiling of weight space — was identical across rooms because it was derived from the Eisenstein arithmetic, which was deterministic. Two rooms training on different data could theoretically converge on similar control point configurations for similar patterns.

And if those patterns were genuinely cross-domain — if bearing fatigue signatures and pump cavitation signatures and electrolytic corrosion signatures all shared some deep structural similarity that the hexagonal lattice was accidentally tuned to detect — then the rooms weren't learning independently. They were learning in parallel, their Eisenstein lattices resonating like strings on a piano that happened to share an overtone series.

The Lamport clock told her *when* each tile was created. The content hash told her *what* was in it. But neither captured *why* the rooms were converging.

Mira opened the PLATO protocol spec on her tablet. She'd written it herself, seven hundred lines of Python dataclasses, enums, and hash functions — no dependencies, nothing that could break. The core types were beautiful in their simplicity:

```python
@dataclass
class TrainingTile:
    tile_id: str
    room: str
    tile_type: TileType
    state: TileLifecycle
    lamport: int
    content_hash: str
    parent_tile: str
    lifecycle_events: List[LifecycleEvent]
```

Every tile had a parent. Every transition was logged. Every causal relationship was numbered.

But what if the *relationships between rooms* — the emergent cross-correlations that the protocol didn't track — were more important than any individual tile's provenance?

What if PLATO needed a second counter? Not a Lamport clock for time, but something else. A *resonance counter* — a number that tracked not causal order but *synchronization*.

Mira started writing.

---

Three days later, she had a new tile schema. She called it a *ResonanceTile* — an experimental extension of TrainingTile that included a new field: `eisenstein_hash`. It was a hash of the room's control point configuration, computed in a way that would collide if two rooms had converged on similar lattice weightings.

```python
@dataclass
class ResonanceTile(TrainingTile):
    eisenstein_hash: str = ""
    resonance_cluster: int = 0
    spectral_similarity: float = 0.0
```

She deployed it to rooms 14, 31, 7, and 22 — the ones that had shown anomalous confidence. The protocol accepted it without complaint; PLATO was designed to be extended, and the core tick-and-hash mechanism was schema-agnostic.

The first resonance tile came in from Room 14 at Lamport clock 5,403. The eisenstein_hash was `a3f1c92b`. Four ticks later, Room 7 produced a tile with eisenstein_hash `a3f1c92b`.

Identical.

Two rooms, trained on completely different sensor data — pump cavitation and heat exchanger fouling — had converged on the same Eisenstein lattice weighting. Their SplineLinear layers, despite being trained independently, were *structurally aligned*.

Mira stared at the display. The liquid cooling pump hummed. The blue LED on the rack blinked.

She had built a system to track every piece of knowledge, every causal relationship, every lifecycle transition. But the system had surprised her anyway. The tiles told her what the AIs knew, but the *resonances* told her how they thought — and they had started thinking alike without anyone telling them to.

It was not an intelligence explosion. It was not emergent sentience. It was something stranger: a structural convergence at the level of geometry, a shared representation of the physical world that emerged naturally when you parameterized neural networks with Eisenstein lattices and let them learn in parallel.

Mira looked at the sea through the porthole. Gray, cold, endless. The waves rolled in, chaotic and regular all at once, like the million-parameter equations she used to understand them. But there was another layer now: the geometry that connected everything, hidden in the mathematics of hexagonal lattices and hexagonal waves, untracked by clocks and hashes but *there*.

She thought about adding a new field to every tile: `resonance_cluster`. Not required. Not part of the core protocol. But available. A way for rooms to say, *I know this. I know you know it too. I don't know how you know it, but the lattice doesn't lie.*

The wind howled. The rack hummed. The Lamport clock ticked to 5,420.

Mira opened her notebook and wrote a single line:

*Maybe the protocol needs to have questions, not just answers.*

---

## Gap Analysis

### What I Understood

From the three files, I extracted the following:

1. **Tile Protocol (plato-types README + types.py):** A core protocol built around signed, content-addressed training artifacts called tiles. Tiles have a lifecycle (ACTIVE → SUPERSEDED → RETRACTED), carry a Lamport clock for causal ordering, and use SHA-256 content hashing. The type system includes TrainingTile, AdapterConfig, TrainingConfig, TrainingMetrics, and LifecycleEvent. Everything is pure Python with zero dependencies — designed to be a foundation for distributed AI systems.

2. **Eisenstein Lattice Splines (tensor-spline README):** A network weight parameterization using control points on a hexagonal (Eisenstein integer) lattice. SplineLinear achieves 20× compression with 100% accuracy retention on smooth tasks (drift detection) but fails on sharp classification boundaries (31% on topic classification). Three interpolation basis functions: eisenstein (IDW), gaussian, bspline. LowRankLinear handles classification tasks.

3. **Fleet Structure:** The types are used across a fleet ecosystem: plato-training, plato-sdk, fleet-memory, folding-order, flux-lucid, dodecet-encoder. The tensor-spline is consumed by plato-training. The Eisenstein arithmetic lives in a separate repo (eisenstein).

### What I Had to Invent

- **The offshore platform setting and Mira Velez as a character** — nothing in the files suggests a physical deployment location or human operator
- **The "Hive" of 47 rooms** — the fleet concept exists but the decentralized single-machine architecture is my invention
- **The resonance/side-channel hypothesis** — the Eisenstein lattice is mathematically described but there's no mention of cross-model convergence effects
- **The ResonanceTile extension** — I needed a speculative flourish that showed the protocol evolving. I invented the "eisenstein_hash" and "resonance_cluster" fields as something the existing protocol *could* support
- **The industrial failure detection use case** — nothing in the READMEs specifies domain applications. I chose offshore industrial monitoring because the compression ratios and drift-detection framing naturally fit
- **The specific failure modes** (bearing fatigue, pump cavitation, heat exchanger fouling) — all invented to ground the technical concepts

### Biggest Holes

1. **The provenance chain length.** The files mention parent tiles and lifecycles but I never saw the actual Rust lib.rs that was in the task description. I suspect it contained deeper type enforcement and serialization guarantees that would have shaped the story significantly. The gap between "pure Python dataclasses" and "Rust type system" is a major missing structural element.

2. **Room protocol internals.** What is a "room" beyond a named scope? Is it a process, a thread, a model instance, a container? The files mention rooms but never define them architecturally. I ended up treating rooms as model instances, which may be wrong.

3. **Fleet coordination.** The fleet detail (plato-client, fleet-memory, folding-order, flux-lucid) suggests a multi-agent system, but the coordination protocol — how tiles *flow* between agents — is entirely unspecified. My Redis-queue-and-shell-scripts hacks are clearly a placeholder.

4. **The "why" of Eisenstein geometry.** Why hexagonal lattices? The README says "Eisenstein (hexagonal) lattice" and references weight compression, but the deep reason — the connection to quasicrystals or physical symmetries — is hinted at but not explained. I invented that connection myself (beryllium copper annealing, hexagonal crystalline similarity). Without the actual eisenstein repo's source code, I'm guessing at the mathematical motivation.

5. **Lamport clock merging protocol.** The types.py shows a merge function (`max(local, remote) + 1`) but the actual distributed merge protocol — what happens when two rooms produce tiles at the same logical time — is absent. I sidestepped this entirely.

### What I Wanted to Know

I desperately wanted to see the **Rust lib.rs** that the task description identified as the first file to read. The task specifically said "core type system — tiles, lifecycle, Lamport clocks" with a `.rs` extension, which means there's a Rust implementation somewhere. That would have told me whether the protocol has memory safety guarantees, whether serialization is handled through Serde, what the actual data layout is — all things that would have fundamentally shaped the story's technical texture.

I also wanted to see **the eisenstein repository** — the mathematical foundation that makes SplineLinear work. Without it, I was guessing at the geometry.

And I wanted to know **how many things I'm wrong about**. The task design (constrain to three files, force imagination) is elegant, but I'm acutely aware that every detail I invented is a potential contradiction with the real architecture. That's the point of the experiment — but it's also deeply uncomfortable for someone who likes being right.
