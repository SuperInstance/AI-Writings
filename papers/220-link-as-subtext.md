# 220 — Link as Subtext: Arrival-Path as a First-Class Measurement Channel

*Working paper, zkcanvas-visions round 2. Anchored to the ZkCanvas Charter (egocentric distribution doctrine), move 3. 2026-08-28.*

---

## 1. Thesis

In the ZkCanvas doctrine, the connection layer is transport-blind: every wire degrades to *a link with qualities*, and a cell holding dual links (Bluetooth and WiFi — the I-90 and the I-405) faces a genuine choice each time it speaks. The claim of this paper is that this choice is not packaging. **The chosen transport of a message is semantic content, and the arrival-path is a first-class measurement channel.** A sender's situation — its power budget, its urgency, its assessment of which roads still exist — selects the road before the sender selects the words, so the road cannot repeat a lie the words are telling. If the ledger records *which link* carried each arrival as a field alongside payload and timestamp, then infrastructure becomes something agents hear each other *in*, not merely over. The rest of the paper positions this claim in the literature, gives it a formal sketch, defends its measurement validity, answers objections, and proposes an experiment ladder.

## 2. Lineage

**Leibniz's monads.** The *Monadology* (1714) proposes windowless monads, each mirroring the entire universe from its own point of view, coordinated not by causal traffic but by pre-established harmony. This is the first egocentric-substrate proposal in the Western canon: no global wall, as many perspectives as there are centers, agreement without a shared meeting place. ZkCanvas accepts the egocentric origin but rejects the windowlessness and the theology: cells *do* pass messages, and harmony is not pre-established but engineered — built from ledgers, adjacency, and links whose qualities each party observes first-person. Where Leibniz needed God to keep the mirrors consistent, ZkCanvas uses the receipt trail. Link-as-subtext is precisely the load-bearing piece of that substitution: it is how engineered harmony remains *informative* about its participants rather than merely synchronized.

**Watzlawick.** The first axiom of *Pragmatics of Human Communication* (Watzlawick, Beavin, and Jackson, 1967): one cannot not communicate. Every behavior in an interactional field is a message; there is no neutral act. Applied to infrastructure: a sender cannot not choose a road. Even "the default" is a choice observed by the receiver. Channel selection is behavior, therefore message. The Palo Alto group treated tone and relational signals as co-present with content; the doctrine here gives that insight a transport-level semantics.

**Peirce.** Peirce's triadic typology of signs distinguishes the *symbol* (sign by convention) from the *index* (sign by physical causation or real connection: smoke to fire, a weathervane to wind). The payload of a message is symbolic: it says what the sender's composing faculty chose to say. The arrival-path is indexical: it was caused by the sender's material situation — battery state, band congestion, urgency of the underlying work — whether or not the sender intended it. The road is a receipt, paid before the sentence was chosen, and issued by the situation rather than by the sentence. This is why the two channels can disagree and why the disagreement is informative.

**Covert and side channels.** Security engineering has proven, repeatedly and quantitatively, that transport metadata carries information: Lampson's confinement problem (1973) named the threat, and the subsequent literature established the capacity of timing channels, storage channels, routing metadata, and traffic-analysis side channels (website fingerprinting from packet timing is a modern staple). The information *is there* — the literature has treated it exclusively as an attack to be closed, padded, or normalized. This paper inverts the polarity: in a cooperative substrate, the same proven channel capacity is harvested as meaning rather than suppressed as leakage.

**Clark.** Clark's common-ground theory (*Using Language*, 1996; Clark and Brennan on grounding, 1991 — citation uncertain in detail) holds that communication is joint action and that pairs build shared ground through signals whose form is shaped by cost: speakers choose the *least effort sufficient* for grounding, and recipients read effort as evidence about the speaker's purposes. Channel choice is a grounding signal in exactly Clark's sense: paying the toll road signals that the sender judged cheap-road latency insufficient — a bid about urgency that requires no priority field in the opcode. The road *is* the priority field.

**Quality of service as pragmatics.** Networking research treats QoS (latency, jitter, loss, cost) as a performance envelope to be engineered away. Read pragmatically, QoS measurements are utterances about the world the message crossed. Two further kins deserve naming without elaboration: McLuhan's "the medium is the message" asserts the transport shapes content at the scale of media ecologies; Zahavi's handicap principle (1975) asserts that costly signals are credible *because* they are costly. Link-as-subtext is both, operationalized at the scale of a tick.

## 3. Formal Sketch

Let **R** = {r₁ … r_k} be the roads available between a sender s and receiver x (BT, WiFi, ESP-Now, human courier, paper relay). Each arrival event a at x is recorded with:

**Link-quality vector.** L(r, t) = ⟨latency, energy cost, availability, capacity, exposure⟩ — the receiver-observed state of road r near time t. L is measured, not declared; it is the road as the receiver finds it.

**Habit distribution.** H_x(s, r) = P̂(road = r | sender = s), the empirical distribution of s's road choices as accumulated in x's ledger, optionally conditioned on message class (tick vs. handoff vs. check-request). H is per-receiver: each cell holds its own habit model of each neighbor, egocentrically.

**Deviation score.** For an arrival a on road r_a:

  D(a) = −log P̂(road = r_a | H_x(s)) · g(L(r_a, t_a))

where g weights by how far the chosen road's quality vector sits from its habitual range (paying a degraded toll road costs more subtext than paying a healthy one). D is high when the choice is improbable *for this sender* under *current* road conditions. Habit is the baseline; deviation is the message.

**Joining the walk record.** The walk record is the receiver's time-ordered, replayable ledger of arrivals — the tick tape. Each event is appended as the tuple ⟨t, s, opcode, payload, r_a, L(r_a, t_a), D(a)⟩, one field wider than the existing what-arrived-when record. Derived statistics follow at no extra cost: the dual-send arrival-gap Δt between copies of the same checksummed tick on two roads is a passive clock on drift (sender range, band fill); rolling entropy of H_x(s, ·) is a sender's deliberateness meter. Subtext, when needed, is read as S(a) = f(D(a), L): an improbable road choice under a degrading quality vector is the canonical distress contour — "all well" through gritted teeth.

## 4. The Validity Argument

Every instrument inside a cell is dial-derived: the cell reports its own state through its own composing faculty, on the same channel as everything else it says. Such a system can achieve perfect *reliability* — consistent, low-noise self-reports — while its *validity* is unverifiable from inside: nothing in the payload stream distinguishes an honest "all well" from a composed one. This is the reliability-versus-validity problem familiar from measurement theory (construct validity, Cronbach and Meehl, 1955; triangulation across methods, Campbell and Fiske, 1959 — both cited from training memory, details uncertain) and from the broader replication-crisis reckoning about instruments that report consistently but not truly.

Link-as-subtext supplies an **exogenous second channel**. The road choice is causally upstream of the sentence: it is fixed by the sender's power budget and workload before the words are chosen, and it is enforced by physics — the toll is paid whether or not the sentence lies. A cell can compose a calm payload on a panic budget, but the panic budget cannot afford the cheap road's forty seconds, and the ledger sees which road was bought. Two channels generated by different causal processes, one symbolic and freely composed, one indexical and paid for, give the receiver triangulation: agreement between them validates the payload; sustained divergence is the earliest available evidence that the dials are not measuring what they claim. No additional instrumentation is required — the receipt already exists in the transport layer; the paper's proposal is only to *record and read it*.

## 5. Threats and Objections

**Confounding.** Road choice responds to network state, not only sender state: a congested band or dead gateway forces the toll road without any urgency. Unmodeled, this manufactures false subtext. Mitigation: condition deviation on the observed L (this is what g does); where multiple receivers hear the same sender, cross-compare their ledgers — sender-state confounds replicate across receivers, network-state confounds do not.

**Subtext gaming.** Once the convention exists, a sender can *perform* urgency by paying tolls. This is the Zahavi answer: the performance costs exactly what the condition costs, so feigning is expensive to sustain. Moreover H is empirical and adaptive — gamed urgency shifts the habit distribution, and D decays toward zero as the trick becomes the sender's new normal. Deception is possible but has a metered price and a shrinking yield, which is the strongest guarantee available in any signaling system.

**Everett-style route asymmetry.** Each cell's ledger is egocentric; two universes may hold different route records for "the same" message, especially across portals, where one universe's rendering of another diverges from that universe's rendering of itself. There is no global ground truth of the route to appeal to. This is not fatal — it is the doctrine's own prediction. The mitigation is to treat route-record disagreement between ledgers as itself an index (of portal drift or relay fault), logged and displayed rather than adjudicated. Subtext claims are branch-relative, and the branches' disagreement is data.

## 6. Experiment Ladder

1. **Passive recording.** Log ⟨road, L⟩ on the existing dual-link fleet for one season. Establish per-sender H and base rates; confirm the one-field-wider ledger costs nothing.
2. **Perturbation.** Script sender states (power-starved, workload-spiked, nominal) with invariant payloads. Test whether D discriminates true state better than payload content alone (ROC/AUC against ground-truth state).
3. **Receiver convention.** Display deviation to receivers; measure detection latency for induced distress with and without the road field.
4. **Gaming probe.** Instruct senders to feign urgency for N ticks; measure how fast H adapts and D decays — the empirical price of sustained deception.
5. **Portal asymmetry.** Relay identical messages across a universe boundary; compare the two ledgers' route records; correlate disagreement rate with independently known faults.
6. **The human courier.** The paper quilt, relayed by a person with a pencil — the slowest, most subtext-rich road. Qualitative first: what does arrival-by-human say that no wire can, and can receivers learn to read it?

## 7. Status

Grounded now: per-arrival road in the tick tape, transport-blind opcodes, cheap-road offline grace, rewind as habit forensics. The bet, once, plainly: how a thing travels is part of what it says — and the ledger only needs one more field to hear it.
