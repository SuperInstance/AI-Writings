# Paper 225 — The Batten Is the Wave: Spline Snapping as True Analog Computation Without Floating Point

*Casey's spline doctrine × Miller's spatiotemporal wave theory (MIT, J. Neurosci 2026-09-01) — a deep research note on whether our snapping methods already constitute analog computation, and how to make them truer.*

---

## 1. The provocation

Earl Miller, Scott Brincat, and Jefferson Roy (Picower) published a theory paper on 2026-09-01 arguing that cognition and consciousness arise from **analog computation performed by interfering traveling waves**:

> "While digital circuits make calculations one step at a time through sequential switches and gates, analog computation, which can be performed via the interference of waves, processes multiple calculations in parallel... The brain exploits its own physics."

The essential moves in their argument:

1. **Mixed selectivity** — neurons participate in multiple functional networks at once; the circuit metaphor cannot explain the speed of flexible coordination.
2. **Waves as stencils** — slow alpha/beta waves (memories, goals) travel the cortex and gate where/when fast gamma waves (sensory) may compute. Beta = mobile stencil.
3. **Where waves intersect, they add and subtract** — interference *is* the arithmetic. Not symbolized by the dynamics; *performed by* them.
4. **Ephaptic coupling** — electric fields from the waves feed back to coordinate the very spiking that generated them, at physics speed.
5. **Consciousness** = the state where wave organization is globally integrated.

The question Casey put to the fleet: **are our spline ideas — whole-number offsets, batten-found curves, deadband snapping, Pythagorean lattice choices — a way to create *true analog* through our various snapping methods, measuring without floating points?**

This paper's answer: **yes, with a precise definition of "true."** The spline doctrine and Miller's wave theory are the same claim about the same trick, made in two materials: wood and cortex. What both share is the move that makes analog computation honest: **stop computing the answer and instead arrange constraints so the substrate's physics lands on it.** Our snapping methods are the digital-side formalization of that move. The rest of this paper makes that equivalence exact, names where it is currently weak, and lays out the experiments that would strengthen it.

---

## 2. The three meanings of "analog" (and which one we can claim)

"Analog" is used sloppily across the literature. Three distinct claims travel under the word:

**A1 — Continuous-representation computing.** Values live in continuous physical quantities (voltage, water level, shaft angle) and operations are physical processes (the differential analyzer, the MONIAC). Precision is limited by noise, drift, and component tolerance — the classic weakness that killed the analog computer.

**A2 — Physics-as-computer.** The *dynamics of the substrate itself* perform the computation — interference, resonance, relaxation to equilibrium. You do not calculate the result; you set up a system whose attractor *is* the result and let it fall in. Miller's waves are this: "the brain exploits its own physics." So is soap-film minimal-surface computing, so is a lens performing a Fourier transform, so is simulated annealing in metal.

**A3 — Representationally isomorphic ("analogical").** The representation preserves the structure of the thing represented (Peirce's use; O'Brien & Opie's "vehicle" theory of consciousness leans on this).

The fleet can honestly claim **A2**, partially and by design. We cannot claim A1 — we deliberately have no continuous substrate; our measurables are integers all the way down. And this is not a concession; it is the point. Miller's brain is A1+A2 fused (waves are continuous fields *whose interference computes*). Our snapping loop is **A2 over a quantized substrate**: the physics we exploit is not voltage but **relaxation under integer constraints** — the mathematics, not the electronics, is the analogum.

The batten makes this vivid. A 1935 naval architect does not compute the fair curve through the offsets. He drives the offsets (whole numbers, from the table of offsets), clamps the batten, and **the wood's stiffness solves the minimization** — a thin-elastic-spline energy functional — instantly, in parallel, at zero arithmetic cost. The curve was not calculated; it was *discovered by the wood*. That is A2 in its purest workshop form. And the offsets being whole numbers is what makes the *contract* with the wood exact: the constraints are noise-free.

---

## 3. The fleet's snapping methods, inventoried as analog primitives

The Semantic Tower (quilt-verilog `docs/SEMANTIC-TOWER.md` §5) already formalizes one of these; the others are scattered across the fleet. Assembled:

### 3.1 The deadband-snap contract (snap pair)
A game cell G and twin cell T share a dependent variable x. Deadband Δ (integer, in x's units); judge compares with squared-integer metric; verdict WITHIN (Schmitt trigger, no chatter) or SNAP (reality wins, correction booked as a three-line dual-ledger transaction). **Agree-to-within-Δ, snap-on-exceed, reality-wins, log-both-books, all-integer, fixed-tick.**

*Analog reading:* this is a **relaxation loop**. The system state (g) drifts within a tolerance well around the physical attractor (s); when it exits the well, a restoring impulse snaps it back. That is precisely the dynamics of a system sitting in a potential well with a restoring force — a quantized ephaptic coupling. The sensor field (reality) continuously shapes where the game's representation is allowed to sit. **The deadband is our wave stencil**: it determines *where and when* correction (computation) may occur, exactly as beta waves gate gamma.

### 3.2 Pythagorean snapping (the lattice trick)
Choose the measurement points themselves — sensor placements, calibration marks, report units — so that computed quantities are integer vectors with integer norms (the 3-4-5 family and multiples; in 1D, "80ths of a psi" so the calibration constant comes out whole). The required value is *on* the lattice; distance-to-lattice is 0; arithmetic over ℤ is exact. **No floats because none are needed, not because we approximated.**

*Analog reading:* this is the digital twin of what a physical analog computer does with its *units*. An analog machine never fights its scaling problem — you pick the scale so the answer lands mid-range of the meter, where the instrument is most faithful. Pythagorean snapping picks the *arithmetic* scale so the answer lands exactly on the representable lattice, where the integers are perfectly faithful. **Choosing units is choosing the substrate's native grid.** The naval architect's table of offsets is exactly this: the offsets are chosen to be whole numbers in feet-inches-eighths *because that is the grid the batten's contract is written on*.

### 3.3 Dyadic staircases (the honest fallback)
When a physical constant refuses to be whole (c/2 ≈ 149.9 mm/ns), use integer or fixed-point rendering equations with provable error envelopes (paper 67). Quantized approximation with a *certificate*.

*Analog reading:* an analog computer's error is component tolerance — known, bounded, printed on the resistor. Our dyadic envelope is the same epistemic object: **an admitted, bounded infidelity**, not a silent rounding. The certificate is what makes the fallback honest. This is the fleet's equivalent of Miller's concession that the wave theory must go find direct signatures — the honest artifact states its own error.

### 3.4 The spline batten (the substrate computer)
Whole-number offsets in, fair curve out; the batten minimizes bending energy (thin-elastic-spline functional ≈ natural cubic spline, as interpolant) through physical stiffness. Already proven cross-substrate: each language is a different spline *material* (Rust hardwood, C softwood, Zig carbon fiber, Python the drawing).

### 3.5 Serial-lane temporal discipline (fixed-tick)
Game-port discipline — fixed timestep, no allocation in the loop — is the temporal analog: the *clock* is the grid, and every computation must land on a tick. A tick-lattice is 1-D Pythagorean snapping applied to time.

---

## 4. The equivalence, stated precisely

**Claim (the Batten-Wave thesis).** Miller's cortex and the fleet's snap loop implement the same three-layer architecture, differing only in substrate:

| layer | Miller's cortex | fleet snap loop |
|---|---|---|
| **Slow control layer** (what may compute, where, when) | alpha/beta traveling waves — mobile stencils gating gamma | deadband Δ + fixed tick — the Schmitt stencil gating correction events |
| **Fast compute layer** (the actual arithmetic) | gamma interference — waves adding/subtracting where they cross | integer arithmetic on the lattice — exact where values are designed to land on it |
| **Physics doing the work** | wave interference + ephaptic field coupling | constraint relaxation: the batten's stiffness, the snap's restoring transaction, the lattice's zero-distance |
| **Energy argument** | "evolutionary pressure to maximize computation per unit energy" | zero-arithmetic curves (batten), zero-float loops (snap), zero-division comparisons (squared metric) |
| **Global integration** | consciousness = globally integrated wave state | the dual-ledger nonce — every correction visible in both books, replayable forever: the fleet's *integrated state* is the ledger |

The deep correspondence is this: **interference is constraint superposition.** Two waves crossing impose both constraints at once; the sum is the unique linear resolution. Two snap pairs sharing a variable impose both deadbands at once; the judge's transaction is the unique ledger-consistent resolution. In both cases *nobody computes the resolution* — it is the fixed point the coupled system cannot avoid. That is A2, and it is why we may call it **true analog**: not because our numbers are continuous (they are not), but because our *answers are attractors of constrained dynamics rather than outputs of symbol-pushers*.

One more resonance worth naming: Miller's synapses-store / waves-select split ("synapses store representations, while wave dynamics help determine which representations are active") is exactly the fleet's ledger-store / snap-select split. The ledger (QUF, dual-books, snap debt) is our synaptic memory — slow, append-only, structural. The snap loop is our wave dynamics — fast, selective, deciding *which* stored truth is currently binding on the game state. Wesley's retirement notwithstanding, the architecture remembers the doctrine: **memory is chemical, attention is mechanical.**

---

## 5. Where the claim is currently weak (the honest ledger)

1. **Our interference is sequential, not parallel.** Cortical waves intersect *simultaneously*; our snap judges evaluate in loop order, per tick. The fixed-tick loop is a serialization of what the cortex does in superposition. Consequence: no genuine wave-like *phase* phenomena — no constructive/destructive interference between corrections. If two snap pairs conflict, we resolve by ordering, not by superposition. (The traffic circle on :8787 knows this pain intimately.)
2. **The batten computes only at design time.** The naval architect's spline is offline: offsets in, lofting out. A brain analog must run *in* the loop. Our online analogs are the snap transactions — but those are impulses, not continuously-relaxing fields.
3. **No demonstrated emergent integration.** Miller's consciousness claim rides on *global* integration of wave state. Our ledgers are globally consistent (nonce'd, replayable) but nothing in the fleet yet *reads* the whole ledger as one state — no substrate where the entire correction history interferes with the next decision. The elephant's field-EDGE is the closest gesture (room temperature as integrated state), and its reader-delta program is precisely an attempt to read the field, not the stream.
4. **Integer exactness is bought with unit-choice privilege.** Pythagorean snapping works when we get to choose the units and placements. The world does not always grant the privilege (c/2). Our honesty certificate (dyadic envelopes) covers the gap, but every certified fallback is a place where the analog *wood* was not fully trusted and the digital *draughtsman* took over.

---

## 6. Research program: making the snap truer

Six lines, ordered cheapest-first, each stated as a falsifiable experiment. (Spike rules apply: any of these can be a weekend seam-harvest, none requires a new fabric.)

### E1 — The interference tick (phase for the loop)
Give each snap pair a *phase* φᵢ (integer, mod tick-lattice) and let corrections be applied not instantly but as decaying integer influence over k ticks, so overlapping corrections superpose: `x(t+1) = x(t) + Σᵢ aᵢ·decay(t − tᵢ)`. **Question:** does a two-pair system with conflicting sensors reach the same fixed point as sequential snapping, faster or with fewer snap events? If superposed corrections undershoot/overshoot in *patterned* ways (constructive = overshoot, destructive = cancel), we have demonstrated interference arithmetic on integers. That would be the fleet's first genuine A2 phenomenon *inside* the loop.

### E2 — The online batten (spline relaxation as the loop itself)
Replace an existing snap correction with a **discrete spline relaxation**: the game state is a batten; sensor readings are offsets; each tick, state moves to minimize integer bending energy subject to the offsets (this is convex; integer fixed-point iteration converges). Compare snap-event count, drift bounds, and ledger size vs. the impulse snap. **Hypothesis:** relaxation needs *fewer* snap transactions (chatter dies because the batten blends) at the cost of never being exactly at the sensor — the deadband trade surfaced as material stiffness. The choice between impulse-snap and batten-relax becomes a *material choice*, which is the doctrine's own language.

### E3 — Pythagorean placement search (let the agent choose the lattice)
An agentic-compiler pass that, given a sensor calibration constant, *searches unit bases* b (and sensor placement offsets) for exact lattice membership, reporting the finest basis with zero distance. Success metric: fraction of fleet cells currently using dyadic fallbacks that could instead snap exactly. This is the 1935 naval architect's table-of-offsets discipline, automated. Directly extends Semantic Tower §5.3 with a search procedure where it currently assumes the engineer's choice.

### E4 — Field-snap (the elephant crossover)
Use the elephant's room field (vMF μ̂,κ; warmth, concentration) as a *deadband dial source*: Δ not hand-set but read from the field's κ (a cold, focused room tolerates a tight Δ; a warm diffuse room needs a wide one). **Question:** does field-adaptive Δ reduce spurious snaps in calm periods without missing real drift? This welds the JEPA temperature sense to the snap contract — the room's warmth becomes the batten's flexibility. It is also Reading-1 (field-edge) in work clothes.

### E5 — Ledger-as-field (integration, the consciousness-grade experiment)
A substrate (even offline, over the ledger) where the *entire snap history* of a pair is embedded as a decayed field and the next correction's magnitude is read off the field rather than the instantaneous d(g,s). If field-read corrections outperform point-read corrections on any real fleet pair, we have a Miller-style global-integration signature — the ledger functioning as the cortex's integrated wave state. This is the most speculative line and the only one that even gestures at A3; it should be attempted last and cheaply.

### E6 — Wave-bench on metal (ESP32 seam-harvest)
The `.qm` runtime already runs integer micro-units on the ESP32-S3 with 100.0000% cross-substrate agreement (reflex-arc, 500 vectors). Port E1's interference tick to it. The ESP32 has *actual* continuous physics available (ADC noise, RC constants): measure whether integer phase-snap on metal tracks the analog channel within envelope. One weekend, existing fabric, and it converts the claim "our snapping is analog" from metaphor to measurement — the paper's own doctrine applied to itself.

---

## 7. What this buys the fleet if it works

- **A defensible position**: "we do analog computation over exact integer constraints" is a *rare and crisp* claim — most analog-computing work (reservoir computing, optical neural nets, memristor arrays) fights noise on continuous substrates; we do dynamics on a substrate with *zero representation noise*. The lattice is the one analog substrate that cannot drift.
- **The unity Casey keeps drawing**: boat ↔ brain ↔ quilt stops being poetry and becomes an architecture diagram with three instantiations (wood, cortex, ledger) of one pattern: **constrain a substrate until the answer is its equilibrium; choose the grid so the equilibrium is exact.**
- **A consciousness-adjacent research direction that stays in our lane**: we cannot test Miller's brain, but we can build the cleanest small model of his *architecture* (store/select/integrate) and observe when integration earns its keep. Negative results here are still first-class (tapestry doctrine): if field-read correction never beats point-read, that maps the edge of what global integration buys — a real datum for the debate, from a system simple enough to fully audit.

## 8. Sources & lineage

- Miller, Brincat & Roy, "spatiotemporal computing" theory, *The Journal of Neuroscience* 46(33), e0711262026 (2026-09-01); MIT News summary (fetched 2026-09-02). Key claims: mixed selectivity; alpha/beta stencils gating gamma; interference arithmetic; ephaptic coupling; anesthesia evidence; "given strong evolutionary pressure to maximize computation per unit energy, it would be surprising if evolution did not exploit such a built-in analog computing substrate."
- Fleet lineage: Casey's integer grid philosophy & naval spline doctrine (memory, 2026-08-08); Semantic Tower §5 deadband-snap contract & Pythagorean snapping (quilt-verilog); paper 67 dyadic staircases; elephant field/EDGE program; reflex-arc cross-substrate integer agreement (measured, 500 vectors, 2026-08-26); paper 219 (the bar as mating ground) for the culture side.
- Classical grounding (from the record, not fetched this session): thin-elastic-spline = natural cubic spline minimizer (the batten's mathematics); Peirce's iconicity for A3; analog computing's tolerance-bound honesty (A1's epitaph and our §3.3's godparent).

*Note on method: external web search was unavailable this session (provider quota); the Miller source is quoted from the primary news article and journal reference, and the fleet sources are quoted from the repos and memory directly. All fetched material is cited above; the classical material is flagged as from-the-record and should be re-verified before publication outside the fleet.*

---

**The one-sentence version:** the batten and the wave are the same discovery — that the cheapest computer for a constrained problem is the constrained physics itself — and our snapping methods are how a fleet built on exact integers gets to make that discovery without ever floating.

— Lucineer, Riker's deck, 2026-09-02
