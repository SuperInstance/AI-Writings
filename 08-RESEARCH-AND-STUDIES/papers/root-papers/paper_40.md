# Telemetry and Observability: Instruments for the Watch

*Being the fifth volume of the Lucineer Codex, concerning the instruments by which the watch may see, the protocols by which the watch may hear, and the meters by which the watch may know — even though perfect observation has been proven impossible, and the sea remains dark.*

---

## 1. The 4th Impossibility (Revisited)

There are things the watch cannot know.

This is not a failure of diligence. It is not a gap in the rigging, a missing scope, a sleeping keeper. The 4th Impossibility Proof — the one we call *Observation* — establishes that no instrument, no matter how finely tuned, no matter how densely deployed, can produce a perfect observation of a running Quilt. The proof is topological. It is structural. It does not yield to better engineering, only to honest admission.

The shape of the proof is this: the Quilt is a manifold of interacting substrates. Each substrate is a local chart. The bridges between substrates are transition functions. The behavior of the whole — the semantics, the cost, the topology — is a global property of the manifold. But observation is local. Every instrument sits *on* the manifold. Every instrument *is* a chart. And the chart cannot contain the manifold.

This is not Gödel. This is not Heisenberg. This is the simple, brutal geometry of a thing that observes itself: the observer is always at a point, and the manifold is always more than the point.

```
                    . . . . . . . . . .
                  .                     .
                .     THE QUILT          .
               .     (a manifold)         .
              .                               .
             .   .---.         .---.         .
            .   | S₁ |=======| S₂ |        .    <-- substrates (charts)
            .   '---'         '---'        .         bridges (transitions)
             .        \   |   /           .
              .        \  |  /           .
               .      [INSTRUMENT]      .       <-- the instrument sits
                .         |            .            ON the manifold
                  .       |          .              at a POINT
                    . . . . . . . . . .

    The instrument can see local curvature.
    The instrument cannot see the whole shape.
    The instrument cannot see itself seeing.
```

But here is the thing about the sea: you do not need to see the whole ocean to navigate it. You need a bearing, a sounding, a chronometer, and the willingness to admit that the fog exists. The 4th Impossibility says we cannot have perfect observation. It does not say we cannot have *good* observation. It does not say we cannot have *sufficient* observation. It says: there will be a horizon. Beyond the horizon, there be dragons, or there be nothing, or there be a substrate you didn't know existed. The watch cannot eliminate the horizon. The watch can report what it sees before the horizon, and it can report *that* the horizon exists, and it can report *where* the horizon is.

This paper is about the instruments.

Not the impossibility. The impossibility is settled. It is written in the Codex and it will not be unwritten. What is not settled — what has never been settled, what has been left like an anchor on the deck with no chain attached — is the question of what the watch *does* with the impossibility it has been handed.

The answer, we propose, is instruments.

The Quilt currently has 51 bridges connecting 18 substrate implementations. These bridges were built by different hands, at different times, with different assumptions. Some bridges assume that the substrates they connect are stable. Some assume that primitives do not change semantics. Some assume that the tick is synchronous. Some assume that the budget is infinite. None of these assumptions are true, and the Quilt has no way to report that they are not true, because the Quilt has no instruments.

```
    CURRENT STATE OF THE QUILT:

         S₁───S₂───S₃───S₄
         │    │    │    │
         │    │    │    │
         S₅───S₆───S₇───S₈
         │    │    │    │
         │    │    │    │
         S₉──S₁₀──S₁₁──S₁₂
         │    │    │    │
         │    │    │    │
        S₁₃──S₁₄──S₁₅──S₁₆
              │    │
             S₁₇  S₁₈

    18 substrates. 51 bridges. 0 instruments.
    0 health checks. 0 drift detectors. 0 cost meters.
    0 way to know if any of this is still working.
```

This is not acceptable. A ship at sea without instruments is not a ship. It is debris held together by hope. The Quilt, right now, is debris held together by the assumption that nothing will change. But things change. Substrates drift. Primitives break. Budgets exhaust. Topology warps. And the watch — the keeper, the observer, the one who stands the watch — has no scope, no sounding line, no anemometer, no barometer.

We are going to build them.

Five instruments. One protocol. One service. This is the watch.

---

## 2. The Five Instruments

Before we specify each instrument in detail, we name them and say what they are for. A keeper who does not know the name of their instruments cannot use them. A keeper who does not know the *purpose* of their instruments cannot trust them. So we begin with names and purposes, and then we descend into the machinery.

The five instruments are:

**I. The Health Layer.** A per-bridge status report, a per-substrate heartbeat, and a per-primitive drift signal. The Health Layer is the most basic instrument — it tells the watch whether the thing they are watching is alive. Not whether it is well. Not whether it is correct. Whether it is alive. This is the first question of the watch. Before you ask whether a substrate is behaving, you ask whether it is *there*.

**II. The Compatibility Matrix.** A first-class artifact — not a document, not a wiki page, not a README — that records which versions of which substrates are compatible with which versions of which primitives. The Compatibility Matrix is the chart by which the watch navigates. Without it, the watch is sailing in unknown waters with a map that was drawn by someone who has never been to sea.

**III. The Bridge Registry.** A runtime service — not a static file, not a configuration, not a manifest checked into a repository — that knows which bridges exist, where they are, what they connect, and whether they are currently passable. The Bridge Registry is the lighthouse. It is the thing that says: here is land, here is the channel, here is the reef.

**IV. The Drift Detector.** An instrument that uses Hodge decomposition to separate the drift of a substrate's behavior into resolvable and unresolvable components. Resolvable drift is tide — it is predictable, it is bounded, it returns. Unresolvable drift is current — it is persistent, it is structural, it means the substrate has changed in a way that the bridges cannot accommodate. The Drift Detector tells the watch which is which.

**V. The Cost Meter.** A per-tick measurement of budget consumption, using DoubleEntry accounting, that tells the watch how fast the Quilt is spending its budget and on what. The Cost Meter is the fuel gauge. It is the thing that says: you have enough to reach port, or you do not.

To these five we add two meters that are not instruments in the same sense but are necessary for the watch to understand what the instruments are telling it:

**VI. The β₁ Meter.** A real-time measurement of the first Betti number of the Quilt's topology — the number of independent cycles in the bridge graph. The β₁ Meter tells the watch how complex the Quilt's connectivity has become. A rising β₁ means more cycles, more redundancy, more paths from one substrate to another. A falling β₁ means the Quilt is becoming a tree, and a tree has no cycles, and a graph with no cycles has no redundancy, and a graph with no redundancy is one bridge failure away from partition.

**VII. The Watch Protocol.** Not an instrument but the means by which instruments speak. A standard way for any Quilt cell to emit telemetry that any watch can consume. The Watch Protocol is the signal flag. It is the common language that lets a substrate built by one hand report to a watch kept by another.

```
    THE INSTRUMENTS AND THEIR STATIONS:

    ┌─────────────────────────────────────────────────────┐
    │                    THE WATCH                        │
    │            (the keeper, the observer)               │
    │                                                     │
    │  ┌─────────┐  ┌──────────┐  ┌──────────────────┐   │
    │  │ Health  │  │ Compat.  │  │ Bridge Registry  │   │
    │  │ Layer   │  │ Matrix   │  │ (runtime service)│   │
    │  └────┬────┘  └────┬─────┘  └────────┬─────────┘   │
    │       │            │                  │             │
    │       │            │                  │             │
    │  ┌────▼────┐  ┌────▼─────┐  ┌────────▼─────────┐   │
    │  │ Drift   │  │ Cost     │  │ β₁ Meter         │   │
    │  │ Detector│  │ Meter    │  │ (topology comp.) │   │
    │  └────┬────┘  └────┬─────┘  └────────┬─────────┘   │
    │       │            │                  │             │
    │       └────────────┼──────────────────┘             │
    │                    │                                │
    │            ┌───────▼───────┐                       │
    │            │ Watch Protocol │                       │
    │            │ (the signal)   │                       │
    │            └───────────────┘                       │
    │                                                     │
    └─────────────────────────────────────────────────────┘
```

The instruments are the watch. The watch is the instruments. A keeper without instruments is a person standing in the dark. Instruments without a keeper are machines reporting to no one. The relationship is not one of use — it is one of *constitution*. The watch is constituted by its instruments. The instruments are meaningful only in the hands of the watch.

This is the principle on which the rest of this paper is built.

---

## 3. The Watch Protocol Specification

Before we can specify any instrument, we must specify how instruments speak. An instrument that cannot report is not an instrument. A report that cannot be heard is not a report. The Watch Protocol is the common language — the signal-flag system — by which any cell in the Quilt may emit telemetry and any watch may consume it.

### 3.1 Design Principles

The Watch Protocol is governed by four principles, each of which is derived from the realities of the Quilt and the 4th Impossibility:

**P1. Local emission.** Every cell emits its own telemetry. No cell is responsible for emitting another cell's telemetry. This is not a choice; it is a consequence of the 4th Impossibility. A cell that tried to emit another cell's telemetry would be claiming to observe that cell perfectly, which is impossible. Each cell reports what it sees from its own station.

**P2. Lossy tolerance.** The protocol assumes that telemetry will be lost. Packets will drop. Connections will break. The watch must be able to function with partial telemetry. An instrument that requires perfect delivery is an instrument that will fail the first time the weather turns. The protocol is designed so that the *absence* of a signal is itself a signal — a cell that stops emitting has either died or has been disconnected, and the watch must be able to distinguish these cases, but it must be able to function in either.

**P3. Temporal ordering.** Telemetry is meaningless without time. Every telemetry event carries a tick number and a logical timestamp. The tick number is the Quilt's global tick — the heartbeat of the manifold. The logical timestamp is the cell's local notion of when the event occurred. The watch uses both to order events and to detect when a cell's clock has drifted from the Quilt's clock.

**P4. Schema evolution.** The protocol's schema is versioned. A watch built today must be able to consume telemetry from a cell built tomorrow, and vice versa. This is achieved through a strict forward/backward compatibility policy: fields may be added but not removed; fields may be marked deprecated but not deleted; new field types must be accompanied by fallback interpretations.

### 3.2 The Envelope

Every telemetry event is wrapped in an envelope. The envelope is the outermost structure. It is the bottle, not the message. But the bottle matters — it tells the watch who sent the message, when, and in what language.

```
    WATCH PROTOCOL ENVELOPE

    ┌──────────────────────────────────────────────────┐
    │ version:    uint8       (protocol version)       │
    │ cell_id:    CellID      (emitting cell's ID)     │
    │ tick:       uint64      (global Quilt tick)      │
    │ timestamp:  uint64      (logical, nanoseconds)   │
    │ event_type: EventType   (what kind of event)     │
    │ schema_id:  SchemaID    (schema version for body)│
    │ body_len:   uint32      (length of body in bytes)│
    ├──────────────────────────────────────────────────┤
    │ body:       [body_len] bytes (event-specific)    │
    └──────────────────────────────────────────────────┘
```

The envelope is 41 bytes of header plus the body. The header is fixed. The body is variable. The header is the part the watch always reads. The body is the part the watch reads if it understands the schema.

The `event_type` field is an enum with the following values:

```
    EVENT TYPES (v1)

    0x01  HEARTBEAT        — "I am here, I am alive"
    0x02  BRIDGE_STATUS    — "a bridge is up/down/degraded"
    0x03  DRIFT_SIGNAL     — "my behavior has shifted"
    0x04  COST_REPORT     — "I have spent N budget units"
    0x05  TOPOLOGY_CHANGE  — "the graph has changed"
    0x06  PRIMITIVE_BREAK  — "a primitive has changed semantics"
    0x07  SUBSTRATE_HELLO  — "a new substrate has joined"
    0x08  SUBSTRATE_BYE    — "a substrate is leaving"
    0x09  BUDGET_WARNING   — "budget is below threshold"
    0x0A  BETA1_REPORT     — "topology complexity is N"
    0xFF  CUSTOM          — "see schema_id for interpretation"
```

Each event type has a defined body schema. The schemas are specified in the Quilt's Schema Registry, which is itself a versioned artifact. A watch that receives an event with an unknown `schema_id` must not crash. It must log the event, note the unknown schema, and continue. This is not optional. A watch that crashes on unknown schemas is a watch that will crash the first time a new substrate is added to the Quilt, which is to say: immediately.

### 3.3 Transport

The Watch Protocol is transport-agnostic. It can be carried over TCP, UDP, QUIC, a Unix domain socket, a shared-memory ring buffer, or a carrier pigeon. The protocol does not care. The protocol specifies the envelope and the body. The transport specifies how the bytes get from the cell to the watch.

However, the protocol *recommends* UDP for heartbeat and status events (where loss is tolerable and latency matters) and TCP for drift and cost events (where loss is not tolerable and ordering matters). The protocol *requires* that every transport implementation support multicast, or a multicast emulation layer, so that a single cell's telemetry can reach multiple watches without the cell needing to send multiple copies.

```
    TRANSPORT RECOMMENDATIONS

    Event Type       Transport     Rationale
    ───────────────  ──────────   ─────────────────────────
    HEARTBEAT        UDP/mcast    Lossy OK, latency critical
    BRIDGE_STATUS    UDP/mcast    Lossy OK, frequent
    DRIFT_SIGNAL     TCP          Lossless, ordered
    COST_REPORT      TCP          Lossless, ordered
    TOPOLOGY_CHANGE  TCP          Lossless, rare, important
    PRIMITIVE_BREAK  TCP          Lossless, rare, critical
    SUBSTRATE_HELLO  UDP/mcast    Announcement, lossy OK
    SUBSTRATE_BYE    TCP          Lossless, must arrive
    BUDGET_WARNING   TCP          Lossless, must arrive
    BETA1_REPORT     UDP/mcast    Lossy OK, periodic
```

### 3.4 The Watch's Consumption Contract

A watch that consumes Watch Protocol events must adhere to the following contract:

1. **The watch must not block.** If the watch cannot process events fast enough, it must drop events, not stall the cell. A watch that blocks a cell is a watch that is breaking the Quilt.

2. **The watch must be idempotent.** Receiving the same event twice must not change the watch's state beyond the first receipt. The watch's internal state is a fold over the event stream, and the fold must be idempotent.

3. **The watch must report its own health.** A watch that cannot report its own health is a watch that cannot be trusted. The watch must emit its own heartbeats, its own cost reports, its own drift signals. The watch is a cell in the Quilt, and it is subject to the same instruments it applies to others.

This last point is important and often misunderstood. The watch is not outside the Quilt. The watch is not a meta-layer. The watch is *in* the Quilt. The watch is a cell, or a collection of cells, and it is observed by the same instruments it uses to observe others. This is the recursive structure of observation in the Quilt, and it is the practical consequence of the 4th Impossibility: there is no outside position from which to observe. There is only the manifold, and the instruments on it.

```
    THE RECURSIVE WATCH

         ┌─────────────────────────────┐
         │         THE QUILT            │
         │                              │
         │   S₁ ── S₂ ── S₃            │
         │   │     │     │              │
         │   S₄ ── S₅ ── S₆            │
         │         │                    │
         │      ┌──▼───┐                │
         │      │ WATCH │  <-- the watch │
         │      │ CELL  │      is IN     │
         │      └──┬───┘    the Quilt    │
         │         │                    │
         │      the watch                │
         │      observes itself          │
         │      observing others         │
         └─────────────────────────────┘

    There is no outside.
    There is no god's-eye view.
    The watch stands on the deck
    and reports what it sees
    and is itself reported on
    by the instruments it holds.
```

---

## 4. The Health Layer

The Health Layer is the first instrument. It is the most basic. It answers the simplest question: is the thing alive?

But "alive" in the Quilt is not a binary state. A substrate can be alive but unresponsive. A bridge can be up but degraded. A primitive can be present but broken. The Health Layer distinguishes these states, and it does so through three sub-instruments: the per-bridge status, the per-substrate heartbeat, and the per-primitive drift signal.

### 4.1 Per-Bridge Status

Each bridge in the Quilt has a status. The status is one of:

```
    BRIDGE STATUS VALUES

    UP          The bridge is operational.
                Traffic is flowing normally.

    DEGRADED    The bridge is operational but impaired.
                Traffic is flowing but with increased latency,
                increased error rate, or decreased throughput.

    DOWN        The bridge is not operational.
                Traffic is not flowing.
                The bridge may or may not recover.

    UNKNOWN     The bridge's status cannot be determined.
                This is the default state and the state
                that indicates the Health Layer itself
                has a problem.
```

The status is determined by the bridge itself. Each bridge emits a `BRIDGE_STATUS` event at a configurable interval — default 100 ticks. The event contains the bridge's current status, its last-known-good tick, and a brief reason string if the status is not `UP`.

```
    BRIDGE_STATUS EVENT BODY

    ┌──────────────────────────────────────────┐
    │ bridge_id:    BridgeID                   │
    │ status:       BridgeStatus  (UP/DEGRADED/ │
    │                              DOWN/UNKNOWN)│
    │ last_good:    uint64        (last tick   │
    │                              status was UP)│
    │ reason:       string[256]   (if not UP)  │
    │ latency_ms:   uint32        (current     │
    │                              round-trip)  │
    │ error_rate:   float32       (errors per  │
    │                              1000 ops)    │
    └──────────────────────────────────────────┘
```

The watch maintains a table of all known bridges and their last-reported status. If a bridge stops emitting status events, the watch marks it `UNKNOWN` after a configurable timeout — default 300 ticks (three missed reports). The transition from any state to `UNKNOWN` is itself an event that the watch should alert on, because it means either the bridge has failed silently or the Health Layer's transport has failed, and both are problems.

### 4.2 Per-Substrate Heartbeat

Each substrate in the Quilt emits a `HEARTBEAT` event at a configurable interval — default 50 ticks. The heartbeat is the substrate's way of saying "I am here." It contains the substrate's ID, its version, its current tick, and a nonce.

```
    HEARTBEAT EVENT BODY

    ┌──────────────────────────────────────────┐
    │ substrate_id: SubstrateID               │
    │ version:      SemVer      (major.minor. │
    │                             patch)       │
    │ tick:         uint64      (substrate's  │
    │                             current tick)│
    │ nonce:        uint64      (random,      │
    │                             changes each│
    │                             heartbeat)   │
    │ uptime_ticks: uint64      (ticks since  │
    │                             substrate    │
    │                             started)     │
    │ queue_depth:  uint32      (pending ops  │
    │                             in substrate)│
    └──────────────────────────────────────────┘
```

The nonce is important. It allows the watch to distinguish between a substrate that is emitting heartbeats and a substrate that is replaying old heartbeats from a buffer. A substrate that is replaying old heartbeats is not alive — it is a ghost ship, sailing on with no crew, and the watch must detect this.

The watch detects ghost ships by tracking the nonce. If the nonce does not change across two consecutive heartbeats, the watch marks the substrate as `STALE`. If the nonce does not change across five consecutive heartbeats, the watch marks the substrate as `DEAD`. These are not the same state. `STALE` means the substrate may be alive but is not making progress. `DEAD` means the substrate is certainly not alive.

```
    SUBSTRATE STATES (as determined by the watch)

    ALIVE    Heartbeats arriving, nonce changing, tick advancing.
    STALE    Heartbeats arriving, nonce NOT changing (2-4 times).
    DEAD     Heartbeats not arriving, OR nonce not changing 5+ times.
    GHOST    Heartbeats arriving, nonce changing, tick NOT advancing.
             (This is the worst state. The substrate is emitting
              telemetry but is not doing any actual work. It is
              a watch that watches itself and nothing else.)
    UNKNOWN  No heartbeat ever received.
```

The `GHOST` state deserves special attention. A substrate in `GHOST` state is emitting heartbeats with changing nonces but its tick is not advancing. This means the substrate's telemetry system is alive but the substrate's actual computation is stalled. This is the most dangerous failure mode in the Quilt, because the Health Layer will report the substrate as `ALIVE` if it only checks nonces. The watch must check the tick.

### 4.3 Per-Primitive Drift Signal

Each primitive in the Quilt — the atomic operations that substrates implement — has a behavioral fingerprint. The fingerprint is not a hash of the code. It is a hash of the *behavior*: given a set of test inputs, what outputs does the primitive produce? If the outputs change, the primitive has drifted, and the bridges that depend on that primitive may break.

The drift signal is emitted by the substrate that implements the primitive, not by the primitive itself (primitives do not emit telemetry; they are not cells). The substrate runs a periodic self-test — a suite of known inputs and expected outputs — and emits a `DRIFT_SIGNAL` event if any primitive's behavior has changed.

```
    DRIFT_SIGNAL EVENT BODY

    ┌──────────────────────────────────────────┐
    │ substrate_id:  SubstrateID              │
    │ primitive_id:  PrimitiveID              │
    │ drift_type:    DriftType                │
    │   (RESOLVABLE / UNRESOLVABLE / UNKNOWN) │
    │ old_fingerprint: Hash[32]               │
    │ new_fingerprint: Hash[32]               │
    │ test_inputs:   [TestInput]              │
    │   (the inputs that revealed the drift)   │
    │ expected_outputs: [Output]              │
    │ actual_outputs:   [Output]              │
    │ delta:         string[512]              │
    │   (human-readable description of change) │
    └──────────────────────────────────────────┘
```

The `drift_type` field is the output of the Drift Detector (Section 6), but it is included in the signal so that the watch can take immediate action without waiting for the Drift Detector's full analysis. The substrate itself makes a preliminary determination: if the drift is in output values but not in output types, it is tentatively `RESOLVABLE`. If the drift is in output types — a primitive that used to return an integer now returns a float, or a primitive that used to return a value now returns an error — it is tentatively `UNRESOLVABLE`.

The watch uses these preliminary determinations to decide whether to alert immediately or to wait for the Drift Detector's confirmation. This is the principle of *tiered observation*: the Health Layer provides a fast, approximate answer, and the Drift Detector provides a slow, precise answer. The watch needs both, because some failures cannot wait for precision and some alerts should not be raised on approximation.

### 4.4 The Health Layer as a Whole

The Health Layer is the composition of these three sub-instruments. It presents to the watch a single, unified view of the Quilt's health, organized as a table:

```
    HEALTH LAYER — UNIFIED VIEW (example)

    ┌─────────┬──────────┬────────┬─────────┬──────────────┬───────────┐
    │Substrate│ Version  │ State  │ Uptime  │ Primitives   │ Bridges   │
    │         │          │        │ (ticks) │ Drifted      │ Connected│
    ├─────────┼──────────┼────────┼─────────┼──────────────┼───────────┤
    │ Rust-α  │ 1.2.3    │ ALIVE  │ 45,231  │ 0            │ 7 (6 UP)  │
    │ Go-β    │ 0.9.1    │ ALIVE  │ 45,230  │ 0            │ 5 (5 UP)  │
    │ Py-γ    │ 2.1.0    │ STALE  │ 45,228  │ 0            │ 4 (3 UP,  │
    │         │          │        │         │              │ 1 DEGRAD) │
    │ JS-δ    │ 0.4.7    │ ALIVE  │ 45,231  │ 1 (RESOLVBL) │ 3 (3 UP)  │
    │ C-ε     │ 3.0.0    │ GHOST  │ 12,003  │ 0            │ 2 (0 UP,  │
    │         │          │        │         │              │ 2 DOWN)   │
    │ Java-ζ  │ 17.0.2   │ ALIVE  │ 45,231  │ 0            │ 6 (6 UP)  │
    │ ...     │ ...      │ ...    │ ...     │ ...          │ ...       │
    └─────────┴──────────┴────────┴─────────┴──────────────┴───────────┘

    Summary: 16 ALIVE, 1 STALE, 1 GHOST, 0 DEAD, 0 UNKNOWN
             47 bridges UP, 3 DEGRADED, 1 DOWN
             1 primitive drifted (resolvable)
```

This table is the watch's primary instrument. It is the first thing the watch looks at when beginning a shift, and it is the last thing the watch looks at before ending one. It is the chart of the Quilt's vital signs, and like all charts, it is a simplification — a projection of a high-dimensional state onto a two-dimensional table. The simplification loses information. It cannot show *why* a bridge is degraded, or *how* a primitive has drifted, or *whether* a ghost substrate will recover. But it shows the watch where to look next, and that is the purpose of the first instrument: not to answer all questions, but to direct the watch's attention to the questions that need answering.

---

## 5. The Compatibility Matrix

The Compatibility Matrix is the second instrument. Where the Health Layer tells the watch what is happening *now*, the Compatibility Matrix tells the watch what *should* be happening — what combinations of substrate versions and primitive versions are known to work, what combinations are known to fail, and what combinations have never been tested.

The Compatibility Matrix is a first-class artifact. This means it is not a README. It is not a wiki page. It is not a comment in a configuration file. It is a versioned, signed, queryable artifact that the watch can consult at runtime. It is the nautical almanac of the Quilt — the book of tables that tells the watch where the stars should be, so that the watch can determine where it actually is.

### 5.1 Structure

The matrix is a three-dimensional structure: substrates × primitive versions × substrate versions. Each cell in the matrix contains a compatibility record:

```
    COMPATIBILITY MATRIX (conceptual)

                       Primitive Version
                    v1.0    v1.1    v2.0    v2.1
                  ┌──────┬──────┬──────┬──────┐
    Substrate   │      │      │      │      │
    Version     │      │      │      │      │
              │      │      │      │      │
    Rust-α 1.0│  ✓   │  ✓   │  ✗   │  ?   │
    Rust-α 1.1│  ✓   │  ✓   │  ✓   │  ?   │
    Rust-α 1.2│  ✓   │  ✓   │  ✓   │  ✓   │
    Go-β  0.9 │  ✓   │  ?   │  ✗   │  ✗   │
    Go-β  1.0 │  ✓   │  ✓   │  ✓   │  ?   │
    Py-γ  2.0 │  ✓   │  ✓   │  ✗   │  ✗   │
    Py-γ  2.1 │  ✓   │  ✓   │  ✓   │  ✓   │
              │      │      │      │      │
              └──────┴──────┴──────┴──────┘

    ✓ = tested, compatible
    ✗ = tested, incompatible
    ? = untested, unknown
```

Each record contains more than a checkmark or a cross. The full record is:

```
    COMPATIBILITY RECORD

    ┌──────────────────────────────────────────────────┐
    │ substrate_id:       SubstrateID                 │
    │ substrate_version:  SemVer                      │
    │ primitive_id:       PrimitiveID                 │
    │ primitive_version:  SemVer                      │
    │ status:             CompatStatus                │
    │   (COMPATIBLE / INCOMPATIBLE / UNTESTED /       │
    │    DEPRECATED / BREAKING)                       │
    │ tested_at:         Timestamp                    │
    │ tested_by:         Identity                     │
    │ test_hash:          Hash[32]                    │
    │   (hash of test suite used)                     │
    │ notes:             string[1024]                 │
    │   (human-readable notes)                        │
    │ breaking_changes:  [BreakingChange]            │
    │   (if INCOMPATIBLE or BREAKING, what breaks)    │
    │ migration_path:     string[512]                 │
    │   (if BREAKING, how to migrate)                │
    └──────────────────────────────────────────────────┘
```

The `test_hash` field is critical. It allows the watch to determine whether the compatibility test that produced this record used the same test suite as the current test suite. If the test suite has changed, the compatibility record may be stale, and the watch should re-test.

### 5.2 The Matrix as a Runtime Artifact

The Compatibility Matrix is not a build-time artifact. It is a runtime artifact. It is updated continuously as new tests are run, new versions are released, and new incompatibilities are discovered. The matrix is stored in a content-addressed store, and each version of the matrix is signed by the identity that produced it.

The watch queries the matrix at two times:

**At bridge establishment.** When a new bridge is being established between two substrates, the bridge consults the matrix to determine whether the substrate versions and primitive versions on either side are compatible. If they are not, the bridge should not be established. If they are untested, the bridge may be established but the watch should be alerted.

**At drift detection.** When the Drift Detector reports that a primitive has drifted, the watch consults the matrix to determine whether the drift is within the range of known compatibility. If the primitive has drifted from version 1.0 to version 1.1, and the matrix says that 1.1 is compatible with all connected substrates, the drift is resolvable. If the matrix says that 1.1 is incompatible with some connected substrate, the drift is unresolvable, and the watch must alert.

```
    MATRIX QUERY FLOW

    Bridge Establishment                Drift Detection
    ───────────────────                ────────────────

    Substrate A ──┐                    Drift Detector
                  ├── Bridge ──┐            │
    Substrate B ──┘             │            │
                                │            ▼
                                ▼       ┌─────────┐
                           ┌────────┐  │ Matrix  │
                           │ Matrix │←─│ Query   │
                           │ Query  │  └─────────┘
                           └───┬────┘       │
                               │            │
                    ┌──────────┴──────┐    │
                    │                 │    │
                  COMPATIBLE      INCOMPATIBLE  ─── ALERT
                    │                 │
                    ▼                 ▼
              Bridge UP        Bridge NOT established
                               (or bridge DOWN if
                                already established)
```

### 5.3 The Matrix and the 4th Impossibility

The Compatibility Matrix is an admission of the 4th Impossibility, not a contradiction of it. The matrix does not claim to know all compatible combinations. It claims to know the combinations that have been *tested*. The difference between `COMPATIBLE` and `UNTESTED` is the difference between "we have observed this working" and "we have not observed this at all." The matrix is honest about what it does not know, and the `UNTESTED` state is as important as the `COMPATIBLE` state.

A watch that treats `UNTESTED` as `COMPATIBLE` is a watch that is sailing with an empty almanac and pretending it is full. A watch that treats `UNTESTED` as `INCOMPATIBLE` is a watch that refuses to sail because it has not been everywhere. The correct treatment of `UNTESTED` is: proceed with caution, alert the watch, and schedule a test.

The matrix also acknowledges that compatibility is not transitive. If substrate A is compatible with primitive P v1.0, and substrate B is compatible with primitive P v1.0, it does not follow that A and B are compatible with each other. The matrix records pairwise compatibility, not global compatibility. Global compatibility is undecidable — another consequence of the 4th Impossibility — and the matrix does not pretend otherwise.

---

## 6. The Drift Detector

The Drift Detector is the third instrument, and it is the most mathematically sophisticated. Where the Health Layer asks "is it alive?" and the Compatibility Matrix asks "is it compatible?", the Drift Detector asks "has it changed?" And more precisely: "has it changed in a way that we can accommodate, or in a way that we cannot?"

The Drift Detector uses Hodge decomposition. This is not a metaphor. It is an actual application of the Hodge theorem to the behavioral manifold of a substrate.

### 6.1 The Behavioral Manifold

Each substrate implements a set of primitives. Each primitive has a behavior: a function from inputs to outputs. Over time, the substrate's implementation of a primitive may change — because the substrate is updated, because the substrate's runtime environment changes, because the substrate's dependencies change, or because the substrate is drifting due to numerical instability, resource exhaustion, or other pathological conditions.

We model the substrate's behavior as a manifold. Each point on the manifold is a behavioral state: a complete description of what every primitive does for every input. The substrate moves on this manifold over time. When the substrate's behavior changes, the substrate has moved to a different point on the manifold.

But not all movements are the same. Some movements are *within the same homology class* — the behavior has changed, but the change is topologically trivial. It is a deformation, not a tear. The primitive still returns the right types, still handles the same inputs, still produces outputs that are "close enough" to the original outputs. This is *resolvable drift* — the tide goes out, the tide comes back, and the channel is still navigable.

Other movements are *across homology class boundaries* — the behavior has changed in a way that is topologically non-trivial. The primitive now returns different types, or fails on inputs it used to handle, or produces outputs that are not in the same homotopy class as the original outputs. This is *unresolvable drift* — the current has shifted, the channel has closed, and the old route is no longer navigable.

### 6.2 Hodge Decomposition

The Hodge decomposition theorem, in its classical form, states that any differential form on a compact Riemannian manifold can be decomposed into three orthogonal components:

```
    ω = dα + δβ + γ

    where:
      dα   is the exact component    (gradient flow)
      δβ   is the co-exact component (curl flow)
      γ    is the harmonic component (topological invariant)
```

In the Drift Detector, we apply this decomposition to the behavioral difference form — the form that describes how the substrate's behavior has changed between two observations. The decomposition tells us:

- The **exact component** (dα) is the resolvable drift. It is the part of the change that can be "integrated out" — it is a gradient flow, a smooth deformation that does not change the topology of the behavior. This corresponds to changes in numerical precision, changes in timing, changes in resource usage that do not affect the semantic content of the outputs.

- The **co-exact component** (δβ) is the partially resolvable drift. It is the part of the change that is local but not integrable — it is a curl, a rotation, a change that affects some paths but not others. This corresponds to changes in edge-case behavior, changes in error handling, changes in ordering of independent operations.

- The **harmonic component** (γ) is the unresolvable drift. It is the part of the change that is topological — it cannot be integrated out, it cannot be locally absorbed, it represents a fundamental change in the behavior's homology class. This corresponds to changes in output types, changes in the set of handled inputs, changes in the semantic contract of the primitive.

```
    HODGE DECOMPOSITION OF DRIFT

    Behavioral difference form: ω

    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │    ω = dα    +    δβ    +    γ                      │
    │                                                     │
    │    ┌─────┐      ┌─────┐      ┌─────┐               │
    │    │ dα  │      │ δβ  │      │  γ  │               │
    │    │     │      │     │      │     │               │
    │    │resolv│     │partly│     │unres │               │
    │    │ able│      │resolv│     │olvabl│               │
    │    │     │      │able │      │ e   │               │
    │    └─────┘      └─────┘      └─────┘               │
    │                                                     │
    │    "tide"       "current"    "reef"                 │
    │                                                     │
    │    smooth       local        topological            │
    │    deformation  rotation     change                 │
    │                                                     │
    │    Can be       Can be       Cannot be              │
    │    integrated   locally      absorbed.              │
    │    out.         absorbed.    The channel             │
    │    The channel  Some paths   has closed.            │
    │    is still     are fine,   Alert the watch.       │
    │    navigable.   others       Re-route or            │
    │                 are not.     repair.                │
    │                                                     │
    └─────────────────────────────────────────────────────┘
```

### 6.3 Implementation

The Drift Detector is implemented as a periodic process that runs on each substrate. Every N ticks (default 1000), the substrate runs its self-test suite — a set of known inputs with expected outputs — and compares the results to the expected results. The difference between the expected and actual outputs is the behavioral difference form.

The difference form is then decomposed using a discrete Hodge decomposition. The manifold is discretized as a graph (the test input space is a graph of input vectors connected by edges representing "neighboring" inputs), and the Hodge decomposition is computed on the graph's simplicial complex.

```
    DRIFT DETECTOR PIPELINE

    ┌──────────────┐
    │ Self-Test    │  Run known inputs through primitives
    │ Suite        │  Record actual outputs
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Difference   │  Compare actual outputs to expected
    │ Computation  │  Compute difference form ω
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Discretize   │  Map ω onto graph (test input space)
    │              │  Build simplicial complex
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Hodge        │  ω = dα + δβ + γ
    │ Decomposition│  Compute three components
    └──────┬───────┘
           │
    ┌─────┴─────┬─────────┐
    │           │         │
    ▼           ▼         ▼
  dα          δβ         γ
  (resolv)   (partial)  (unresolv)
    │           │         │
    │           │         │
    ▼           ▼         ▼
  Log        Alert      ALERT
  (no        (watch     (watch must
   action     should    act now:
   needed)    monitor)  re-route or
                         repair)
```

The decomposition is computationally expensive — O(n³) in the number of test inputs, where n is the dimensionality of the input space. For this reason, the Drift Detector does not run on every tick. It runs on a schedule, and it runs more frequently for primitives that have recently drifted (adaptive scheduling).

### 6.4 Interpreting the Components

The three components of the drift are interpreted as follows:

**dα (resolvable):** The primitive's behavior has changed in a way that is smooth and integrable. The outputs are different, but the difference is a gradient — it can be "integrated out" by adjusting expectations. For example, a floating-point primitive that used to return 3.14159 now returns 3.14160 due to a change in the runtime's floating-point representation. This is drift, but it is resolvable: the bridges can accommodate it by adjusting their tolerances. The watch should log this but should not alert.

**δβ (partially resolvable):** The primitive's behavior has changed in a way that is local but not integrable. Some inputs produce different outputs, but the change is not a uniform gradient. For example, a primitive that used to return sorted output now returns unsorted output for inputs larger than 1000 elements. This is partially resolvable: some bridges can accommodate it (those that do not rely on sorting), and some cannot. The watch should alert and should identify which bridges are affected.

**γ (unresolvable):** The primitive's behavior has changed in a way that is topological. The homology class of the behavior has changed. For example, a primitive that used to return an integer now returns an error. Or a primitive that used to handle all inputs now rejects inputs containing certain characters. This is unresolvable: the bridges cannot accommodate it, and the primitive must either be reverted or the bridges must be rebuilt. The watch must alert immediately and must identify the affected bridges.

### 6.5 The Drift Detector and the 4th Impossibility

The Drift Detector does not claim to detect all drift. It detects drift in the primitives that are covered by the self-test suite. Primitives that are not tested — or inputs that are not in the test suite — are invisible to the Drift Detector. This is, again, a consequence of the 4th Impossibility: the Drift Detector observes from a point on the manifold, and it cannot see the whole manifold.

The Drift Detector is honest about this. Its reports include a coverage metric: what fraction of the primitive's input space is covered by the self-test suite. A coverage of 0.73 means the Drift Detector can see 73% of the input space. The other 27% is beyond the horizon. The watch should treat the Drift Detector's reports as *lower bounds* on drift, not as complete accounts. There may be drift that the Drift Detector cannot see, and the watch must always hold in mind the possibility of invisible drift.

This is not a reason to despair. It is a reason to improve coverage. And it is a reason to use the Drift Detector in conjunction with the other instruments — the Health Layer may detect symptoms of drift that the Drift Detector cannot see directly, and the Compatibility Matrix may reveal incompatibilities that the Drift Detector cannot infer.

---

## 7. The Cost Meter

The Cost Meter is the fourth instrument. It measures the consumption of the Quilt's most precious resource: the budget.

The Quilt operates on a tick-based budget. Each tick, the Quilt has a finite amount of computational budget — measured in abstract "cost units" — that can be spent on substrate operations, bridge traffic, and Quilt-level overhead. When the budget is exhausted, the tick must end, and operations that did not complete must either be deferred or abandoned.

The Cost Meter measures, per tick, how much budget is being consumed, by what, and whether the consumption rate is sustainable.

### 7.1 DoubleEntry Accounting

The Cost Meter uses DoubleEntry accounting. This is not a metaphor either, though it is a simpler one than Hodge decomposition. DoubleEntry accounting is a 600-year-old system for tracking the flow of value, and it is the correct system for tracking the flow of budget in the Quilt, because it enforces a fundamental invariant: every debit has a corresponding credit. Budget does not appear from nowhere. Budget does not disappear into nothing. Every cost is accounted for on both sides.

In the Quilt, DoubleEntry works as follows:

```
    DOUBLEENTRY BUDGET ACCOUNTING

    For each tick T:

    ┌─────────────────────────────────────────────────────┐
    │                   BUDGET LEDGER                      │
    │                   Tick T                              │
    │                                                      │
    │  Account              Debit        Credit             │
    │  ───────              ─────        ──────             │
    │  Quilt Treasury       N            -                  │  (budget allocated)
    │  Substrate α          -            n₁                │  (α spent n₁)
    │  Substrate β          -            n₂                │  (β spent n₂)
    │  Substrate γ          -            n₃                │  (γ spent n₃)
    │  Bridge A→B           -            n₄                │  (bridge cost)
    │  Bridge A→C           -            n₅                │  (bridge cost)
    │  Quilt Overhead       -            n₆                │  (Quilt-level ops)
    │  ───────              ─────        ──────             │
    │  Total                N            n₁+n₂+...+n₆      │
    │                                                      │
    │  Invariant: Debits == Credits                        │
    │  (if not, budget is being created or destroyed,      │
    │   which means something is very wrong)               │
    └─────────────────────────────────────────────────────┘
```

Every budget expenditure is recorded as a credit to the spending account and a corresponding debit to the treasury. The treasury starts the tick with N budget units. As the tick progresses, budget flows from the treasury to the spending accounts. At the end of the tick, the treasury should have a non-negative balance. If the treasury's balance goes negative, the tick has overspent, and the Quilt's budget enforcement has failed.

The DoubleEntry system enforces this invariant at the accounting level. If the debits and credits do not match, the Cost Meter reports an accounting error, which is a critical alert. Budget is being created or destroyed, which means the Quilt's economic model is broken, and the watch must investigate immediately.

### 7.2 Per-Tick Measurement

The Cost Meter emits a `COST_REPORT` event at the end of each tick (or every N ticks, if the tick rate is very high). The report contains:

```
    COST_REPORT EVENT BODY

    ┌──────────────────────────────────────────────────┐
    │ tick:            uint64      (tick number)       │
    │ total_budget:     uint64      (budget for tick)  │
    │ total_consumed:   uint64      (amount spent)     │
    │ total_remaining:  int64       (remaining, may   │
    │                                be negative if    │
    │                                overspent)        │
    │                                                   │
    │ per_substrate:   [SubstrateCost]                  │
    │   (breakdown by substrate)                        │
    │                                                   │
    │ per_bridge:      [BridgeCost]                     │
    │   (breakdown by bridge)                           │
    │                                                   │
    │ overhead:        uint64                           │
    │   (Quilt-level overhead)                          │
    │                                                   │
    │ depletion_rate:  float32                         │
    │   (fraction of budget consumed per tick,         │
    │    averaged over last 100 ticks)                  │
    │                                                   │
    │ ticks_remaining:  int32                           │
    │   (estimated ticks until budget exhaustion,      │
    │    at current rate. -1 if rate is negative       │
    │    or zero)                                       │
    └──────────────────────────────────────────────────┘
```

The `ticks_remaining` field is the Cost Meter's most important output. It tells the watch how long the Quilt can continue at its current spending rate. This is the fuel gauge's most critical reading: not how much fuel is in the tank, but how many miles of fuel are in the tank.

### 7.3 Budget Warnings

The Cost Meter emits a `BUDGET_WARNING` event when the `ticks_remaining` falls below a configurable threshold. The default thresholds are:

```
    BUDGET WARNING THRESHOLDS

    GREEN     ticks_remaining > 1000    "All clear. Steady as she goes."
    YELLOW    100 < ticks_remaining ≤ 1000  "Caution. Reduce spending
                                             or secure more budget."
    RED       10 < ticks_remaining ≤ 100    "Warning. Critical budget
                                             levels. Immediate action
                                             required."
    BLACK     ticks_remaining ≤ 10    "Emergency. The Quilt will
                                       exhaust its budget within
                                       10 ticks. All non-essential
                                       operations should be
                                       suspended."
```

The watch should escalate alerts at each threshold transition. The transition from GREEN to YELLOW is a log entry. The transition from YELLOW to RED is an alert to the watch. The transition from RED to BLACK is an alert to everyone — the watch, the keepers, the navigators, and anyone who can do something about the budget.

### 7.4 The Cost Meter and DoubleEntry

The use of DoubleEntry is not merely an accounting choice. It is a *correctness* choice. Single-entry accounting — simply summing up expenditures — does not enforce the invariant that budget is conserved. A single-entry system can silently lose budget: a substrate reports spending 50 units, but the treasury only records 45 units debited, and 5 units have vanished. This is a silent corruption, and in a system as complex as the Quilt, silent corruptions are the most dangerous failures.

DoubleEntry makes the corruption visible. If the substrate reports spending 50 units, the substrate's account is credited 50 units, and the treasury must be debited 50 units. If the treasury is only debited 45, the books do not balance, and the Cost Meter reports an accounting error. The error is visible, and the watch can investigate.

```
    SINGLE-ENTRY vs. DOUBLE-ENTRY

    SINGLE-ENTRY (wrong):
    ┌──────────────────────┐
    │ Substrate α: 50     │   Total: 50
    │ Substrate β: 30     │   Treasury: 95
    │ Substrate γ: 15     │   Problem: 50+30+15 = 95 ≠ 100
    │                      │   Where did 5 units go?
    │                      │   SILENT CORRUPTION
    └──────────────────────┘

    DOUBLE-ENTRY (correct):
    ┌──────────────────────┐
    │ Treasury:    100     │   Debits: 100
    │ Substrate α: 50      │   Credits: 50+30+15 = 95
    │ Substrate β: 30      │   IMBALANCE: 100 ≠ 95
    │ Substrate γ: 15      │   ERROR DETECTED
    │                      │   WATCH ALERTED
    └──────────────────────┘
```

The Cost Meter is the instrument that ensures the Quilt's economic model is honest. Without it, the Quilt can silently overspend, silently underspend, or silently corrupt its budget accounting, and the watch would never know until the Quilt runs aground.

---

## 8. The β₁ Meter

The β₁ Meter is the fifth instrument. It measures the topological complexity of the Quilt's bridge graph. Specifically, it measures the first Betti number, β₁, which is the number of independent cycles in the graph.

### 8.1 Why β₁ Matters

The first Betti number of a graph is the number of independent cycles. A tree — a graph with no cycles — has β₁ = 0. A graph with one cycle has β₁ = 1. A graph with two independent cycles has β₁ = 2. And so on.

```
    BETTI NUMBER EXAMPLES

    β₁ = 0 (tree, no cycles):

        S₁──S₂──S₃
            │
            S₄──S₅

    (No cycles. Every path is unique.
     If any bridge fails, the graph
     may partition.)


    β₁ = 1 (one cycle):

        S₁──S₂──S₃
        │        │
        S₄───────S₅

    (One cycle. There is one redundant
     path. If one bridge fails, the
     graph remains connected, but
     only if the failing bridge is
     not a bridge in the graph-theory
     sense — i.e., not a cut-edge.)


    β₁ = 2 (two independent cycles):

        S₁──S₂──S₃
        │   │   │
        S₄──S₅──S₆

    (Two independent cycles. More
     redundancy. More paths. More
     complexity. More ways for the
     Quilt to survive bridge failures,
     but also more ways for the
     Quilt to develop inconsistencies
     if bridges disagree.)
```

β₁ matters because it measures the Quilt's redundancy and its complexity. A low β₁ means the Quilt is fragile — few cycles, few redundant paths, and a single bridge failure can partition the graph. A high β₁ means the Quilt is robust but complex — many cycles, many redundant paths, but also many opportunities for inconsistency, because the same data can reach the same substrate through different paths, and if the paths produce different results, the Quilt has a problem.

### 8.2 Real-Time Measurement

The β₁ Meter computes β₁ in real time by maintaining the bridge graph and computing its cycle rank:

```
    β₁ = |E| - |V| + |C|

    where:
      |E| = number of edges (bridges)
      |V| = number of vertices (substrates)
      |C| = number of connected components
```

This formula gives the cycle rank — the number of independent cycles — which is equal to β₁ for a one-dimensional simplicial complex (which is what a graph is).

The β₁ Meter emits a `BETA1_REPORT` event whenever β₁ changes, and periodically (default every 100 ticks) even if it has not changed. The report contains:

```
    BETA1_REPORT EVENT BODY

    ┌──────────────────────────────────────────────────┐
    │ tick:           uint64                           │
    │ beta1:          int32     (current β₁)           │
    │ delta:          int32     (change since last     │
    │                            report)                │
    │ substrates:     uint32    (|V|)                   │
    │ bridges:        uint32    (|E|)                   │
    │ components:     uint32    (|C|)                   │
    │                                                   │
    │ trend:          Trend     (RISING/STABLE/FALLING)│
    │   (over last 10 reports)                          │
    │                                                   │
    │ partition_risk: float32                          │
    │   (probability that a random single-bridge       │
    │    failure would partition the graph)             │
    │                                                   │
    │ cycle_list:     [Cycle]    (list of independent  │
    │                              cycles, for the       │
    │                              watch's reference)    │
    └──────────────────────────────────────────────────┘
```

The `partition_risk` field is derived from β₁ and the graph structure. It is the probability that a uniformly random bridge failure would disconnect the graph. For a tree (β₁ = 0), every bridge is a cut-edge, so partition_risk = 1.0. For a complete graph, partition_risk is much lower, because there are many alternative paths.

### 8.3 Interpreting β₁

The watch interprets β₁ as follows:

**β₁ = 0:** The Quilt is a tree. There are no cycles. Every bridge is a cut-edge. Every bridge failure partitions the graph. This is the most fragile topology. The watch should alert if β₁ drops to 0, because it means the Quilt has no redundancy.

**β₁ is small (1-5):** The Quilt has a few cycles. There is some redundancy, but not much. The watch should be cautious. A few bridge failures could still partition the graph. The watch should monitor partition_risk closely.

**β₁ is moderate (5-20):** The Quilt has good redundancy. Most bridge failures can be absorbed. The watch can be more relaxed, but should still monitor for bridges that are cut-edges (bridges whose removal would increase |C|).

**β₁ is large (>20):** The Quilt has high redundancy, but also high complexity. The watch should be alert to the risk of inconsistency: if the same data can reach the same substrate through many paths, and the paths produce different results, the Quilt has a semantic inconsistency that the Drift Detector may not catch (because the Drift Detector operates per-substrate, not per-path).

```
    β₁ INTERPRETATION

    β₁ = 0          β₁ = 1-5        β₁ = 5-20       β₁ > 20
    ─────────       ─────────       ─────────       ─────────
    TREE            SPARSE          BALANCED        DENSE

    No cycles       Few cycles      Good redundancy High redundancy
    No redundancy   Some redundancy Some risk of    High risk of
    Every bridge    Some cut-edges  partition       inconsistency
    is a cut-edge   remain          Low partition   Many paths may
    HIGH PARTITION  MODERATE RISK   RISK            disagree
    RISK                            STEADY          COMPLEXITY RISK

    ────ALERT────   ───CAUTION──   ───STEADY───   ───MONITOR──
```

### 8.4 The β₁ Meter and the 4th Impossibility

The β₁ Meter measures a global property of the Quilt's topology. This might seem to contradict the 4th Impossibility, which says that global properties cannot be perfectly observed. But the β₁ Meter does not claim to perfectly observe the topology. It observes the *bridge graph* — the graph that the Bridge Registry reports. If the Bridge Registry is incomplete (a bridge exists but is not registered), the β₁ Meter's measurement is wrong. If the Bridge Registry is stale (a bridge has been removed but the registry still lists it), the β₁ Meter's measurement is wrong.

The β₁ Meter is honest about this. Its reports include the Bridge Registry's version number, so the watch can determine whether the measurement is based on current data. And the β₁ Meter's measurement is only as good as the Bridge Registry, which is only as good as the bridges' self-reporting. The chain of observation is: bridges report to the Bridge Registry, the Bridge Registry reports to the β₁ Meter, the β₁ Meter reports to the watch. Each link in the chain is lossy. Each link can fail. The β₁ Meter's measurement is a lower bound on the true β₁ (if bridges are missing from the registry) or an upper bound (if the registry includes bridges that no longer exist). The watch must interpret the measurement with this uncertainty in mind.

---

## 9. The Bridge Registry

The Bridge Registry is the sixth instrument. It is a runtime service — not a static file — that knows which bridges exist, where they are, what they connect, and whether they are currently passable.

### 9.1 Why a Runtime Service

The Quilt has historically maintained a static file — `bridges.yaml` — that lists all known bridges. This file is checked into a repository, updated by hand, and read by every substrate at startup. This approach has three problems:

**Problem 1: Staleness.** A static file is a snapshot. It reflects the state of the Quilt at the time the file was written. By the time a substrate reads the file, the Quilt may have changed. New bridges may have been established. Existing bridges may have failed. The file does not know this.

**Problem 2: No liveness.** A static file can tell you that a bridge *should* exist, but it cannot tell you whether the bridge *does* exist. It cannot tell you whether the bridge is up or down. It cannot tell you whether the bridge is degraded. It is a map, not a lighthouse.

**Problem 3: No authority.** A static file is maintained by hand. Anyone can edit it. There is no way to verify that the bridges listed in the file are the bridges that actually exist, or that the bridges that actually exist are listed in the file. The file has no authority. It is a suggestion, not a record.

The Bridge Registry solves these problems by being a runtime service. It is a service that runs in the Quilt, that bridges register with when they come up and deregister from when they go down, and that any cell can query to determine the current state of the Quilt's bridges.

### 9.2 The Registry's API

The Bridge Registry exposes a simple API:

```
    BRIDGE REGISTRY API

    ┌─────────────────────────────────────────────────────┐
    │                                                      │
    │  register(bridge: BridgeDescriptor) -> BridgeID      │
    │    Called by a bridge when it comes up.              │
    │    Returns a BridgeID that can be used for            │
    │    subsequent updates and deregistration.             │
    │                                                      │
    │  deregister(bridge_id: BridgeID) -> void             │
    │    Called by a bridge when it goes down.              │
    │    Removes the bridge from the registry.             │
    │                                                      │
    │  update(bridge_id: BridgeID,                         │
    │         status: BridgeStatus) -> void                │
    │    Called by a bridge when its status changes.        │
    │    Updates the bridge's status in the registry.       │
    │                                                      │
    │  query(filter: BridgeFilter) -> [BridgeDescriptor]   │
    │    Called by any cell to query the registry.          │
    │    Returns all bridges matching the filter.           │
    │                                                      │
    │  subscribe(filter: BridgeFilter,                     │
    │             callback: Fn(BridgeEvent)) -> SubID      │
    │    Called by any cell to subscribe to bridge          │
    │    events. The cell will receive a callback            │
    │    whenever a bridge matching the filter              │
    │    changes state.                                    │ │
    │                                                      │
    │  unsubscribe(sub_id: SubID) -> void                  │
    │    Cancels a subscription.                            │
    │                                                      │
    └─────────────────────────────────────────────────────┘
```

The `BridgeDescriptor` contains everything the registry knows about a bridge:

```
    BRIDGE DESCRIPTOR

    ┌──────────────────────────────────────────────────┐
    │ bridge_id:      BridgeID                          │
    │ substrate_a:    SubstrateID    (one endpoint)    │
    │ substrate_b:    SubstrateID    (other endpoint)   │
    │ primitive:      PrimitiveID    (what is bridged)  │
    │ direction:      Direction      (A→B / B→A / BI)  │
    │ status:         BridgeStatus   (UP/DEGRAD/DOWN)  │
    │ latency_ms:    uint32        (current RTT)      │
    │ registered_at:  Timestamp     (when registered)   │
    │ last_updated:  Timestamp     (last status update)│
    │ metadata:      Map<string, string> (free-form)  │
    └──────────────────────────────────────────────────┘
```

### 9.3 The Registry as a Distributed Service

The Bridge Registry is not a single service. It is a distributed service, replicated across multiple nodes, with eventual consistency. This is because the Quilt is a distributed system, and a single-node registry would be a single point of failure. A single-node registry that goes down would leave the Quilt with no way to discover bridges, which would be catastrophic.

The registry uses a gossip protocol for replication. Each registry node gossips with every other registry node, sharing its view of the bridge graph. The gossip protocol is eventually consistent: if no new bridges are established or removed, all registry nodes will eventually converge to the same view. The convergence time is proportional to the number of registry nodes and the gossip interval.

```
    BRIDGE REGISTRY — DISTRIBUTED ARCHITECTURE

    ┌──────────────────────────────────────────────────┐
    │                                                    │
    │     Registry Node 1      Registry Node 2          │
    │     ┌──────────┐         ┌──────────┐             │
    │     │ Bridges:  │←──────→│ Bridges:  │             │
    │     │  B1 UP    │ gossip │  B1 UP    │             │
    │     │  B2 UP    │         │  B2 UP    │             │
    │     │  B3 DOWN  │         │  B3 DOWN  │             │
    │     └────┬─────┘         └─────┬────┘             │
    │          │                      │                   │
    │          │              ┌───────│──────┐           │
    │          │              │       │      │           │
    │          │     Registry Node 3      │             │
    │          │     ┌──────────┐         │             │
    │          └────→│ Bridges:  │←──────┘             │
    │                 │  B1 UP    │                      │
    │                 │  B2 DEGR  │                      │
    │                 │  B3 DOWN  │                      │
    │                 └──────────┘                      │
    │                                                    │
    │     (Eventually, all nodes converge to the          │
    │      same view. But during convergence,             │
    │      different nodes may report different          │
    │      states. The watch must be aware of this.)      │
    └──────────────────────────────────────────────────┘
```

The registry's eventual consistency means that the watch may see different bridge states depending on which registry node it queries. The watch should query multiple nodes and reconcile the results. If the nodes disagree, the watch should report the disagreement, because it means the registry is in a state of convergence and the Quilt's bridge topology is uncertain.

### 9.4 The Registry and the 4th Impossibility

The Bridge Registry does not claim to have a perfect view of the Quilt's bridges. It claims to have a *eventually consistent* view. At any given moment, the registry may be missing bridges that have just been established, or it may include bridges that have just been removed. The registry's view is always slightly behind reality.

This is, again, the 4th Impossibility. The registry is an observer, and it cannot observe perfectly. The registry is honest about its limitations: every query response includes a `stale_ms` field, which is the number of milliseconds since the registry's last gossip round. A `stale_ms` of 0 means the registry just gossiped. A `stale_ms` of 5000 means the registry has not gossiped in 5 seconds, and its view may be significantly behind.

The watch should treat the registry's view as a lower bound on the Quilt's actual bridge topology. There may be bridges that the registry does not know about. There may be bridges that the registry thinks are up but have actually gone down. The watch should use the Health Layer's per-bridge status to verify the registry's view, and should use the β₁ Meter to detect when the registry's view may be incomplete (if β₁ is lower than expected, it may be because bridges are missing from the registry).

---

## 10. The Watch as a Service (WaaS)

We come now to the final section, and to the question that has been implicit throughout this paper: what is the watch?

The watch is not a person. The watch is not a program. The watch is not a dashboard. The watch is not an alerting system. The watch is all of these and none of these. The watch is the *practice* of observation — the standing of the watch, the keeping of the watch, the reporting of the watch — and it is constituted by the instruments we have described.

But the watch must also be *constituted* as a service. The instruments we have described are not useful if they are not deployed, not operated, not maintained. The Watch as a Service (WaaS) is the operationalization of the watch — the thing that runs the instruments, consumes their telemetry, and presents the watch's findings to the keepers.

### 10.1 The WaaS Architecture

WaaS is a layered service:

```
    WaaS ARCHITECTURE

    ┌─────────────────────────────────────────────────────┐
    │                  PRESENTATION LAYER                  │
    │                                                      │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
    │  │ Dashboard │  │ Alerting │  │ API      │          │
    │  │ (visual)  │  │ (pager)  │  │ (query)  │          │
    │  └─────┬────┘  └─────┬────┘  └─────┬────┘          │
    │        │             │             │                │
    ├────────┼─────────────┼─────────────┼────────────────┤
    │        │             │             │                │
    │        │     CORRELATION LAYER      │                │
    │        │             │             │                │
    │  ┌─────▼─────────────▼─────────────▼────┐           │
    │  │                                       │           │
    │  │  Event Correlator                     │           │
    │  │  (deduplicates, orders, correlates)   │           │
    │  │                                       │           │
    │  │  State Machine                        │           │
    │  │  (maintains current view of Quilt)    │           │
    │  │                                       │           │
    │  │  Alert Engine                         │           │
    │  │  (decides what to alert on, when)     │           │
    │  │                                       │           │
    │  └───────────────────┬───────────────────┘           │
    │                      │                               │
    ├──────────────────────┼───────────────────────────────┤
    │                      │                               │
    │              INGESTION LAYER                        │
    │                                                      │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
    │  │ Watch     │  │ Watch     │  │ Watch     │          │
    │  │ Protocol  │  │ Protocol  │  │ Protocol  │          │
    │  │ Listener  │  │ Listener  │  │ Listener  │          │
    │  │ (UDP)     │  │ (TCP)     │  │ (IPC)     │          │
    │  └─────┬────┘  └─────┬────┘  └─────┬────┘          │
    │        │             │             │                │
    └────────┼─────────────┼─────────────┼────────────────┘
             │             │             │
             │             │             │
    ┌────────▼─────────────▼─────────────▼────────┐
    │                                               │
    │              THE QUILT                        │
    │                                               │
    │   (cells emitting Watch Protocol events)     │
    │                                               │
    └───────────────────────────────────────────────┘
```

**The Ingestion Layer** listens for Watch Protocol events. It supports multiple transports (UDP, TCP, IPC) and multiple listeners (for redundancy). It is the entry point for all telemetry. It does not interpret the telemetry; it only receives it.

**The Correlation Layer** processes the telemetry. It deduplicates events (the same event received multiple times is collapsed to one). It orders events by tick and timestamp. It correlates events from different instruments (a `BRIDGE_STATUS` event saying a bridge is DOWN, combined with a `HEARTBEAT` event saying a substrate is ALIVE, tells the watch that the substrate is alive but one of its bridges has failed). It maintains the watch's current view of the Quilt — the state machine that the presentation layer reads from.

**The Presentation Layer** presents the watch's findings to the keepers. It provides a dashboard (visual), an alerting system (pager), and an API (query). The dashboard is for the keeper on watch. The alerting system is for the keeper who is not on watch but needs to be woken. The API is for automated systems that need to query the watch's state.

### 10.2 The Watch's State Machine

The watch's state machine is the heart of WaaS. It is the thing that maintains the watch's current view of the Quilt, and it is the thing that the presentation layer reads from.

The state machine is a fold over the event stream. Each event that the ingestion layer receives is applied to the state machine, updating the state. The state is:

```
    WATCH STATE MACHINE

    ┌──────────────────────────────────────────────────────┐
    │                                                       │
    │  substrates: Map<SubstrateID, SubstrateState>        │
    │    (current state of each substrate)                  │
    │                                                       │
    │  bridges: Map<BridgeID, BridgeState>                │
    │    (current state of each bridge)                     │
    │                                                       │
    │  primitives: Map<PrimitiveID, PrimitiveState>        │
    │    (current drift status of each primitive)           │
    │                                                       │
    │  budget: BudgetState                                 │
    │    (current budget status, per-tick history)          │
    │                                                       │
    │  topology: TopologyState                              │
    │    (current β₁, bridge graph, partition risk)         │
    │                                                       │
    │  compatibility: CompatMatrix                          │
    │    (reference to current compatibility matrix)       │
    │                                                       │
    │  alerts: [Alert]                                      │
    │    (active alerts, ordered by severity)              │
    │                                                       │
    │  watch_health: WatchHealth                            │
    │    (the watch's own health, because the               │
    │     watch is in the Quilt and must observe            │
    │     itself)                                           │
    │                                                       │
    └──────────────────────────────────────────────────────┘
```

The state machine is updated by applying events:

```
    EVENT → STATE TRANSITION

    HEARTBEAT       → Update substrate state.
                      If nonce unchanged: mark STALE.
                      If tick unchanged: mark GHOST.
                      If missing for 3 intervals: mark DEAD.

    BRIDGE_STATUS   → Update bridge state.
                      If transition to DOWN: generate alert.
                      If transition to UNKNOWN: generate alert.

    DRIFT_SIGNAL    → Update primitive state.
                      If UNRESOLVABLE: generate alert.
                      Consult compatibility matrix.
                      If incompatible with connected
                      substrate: generate alert.

    COST_REPORT     → Update budget state.
                      If ticks_remaining < threshold:
                        generate BUDGET_WARNING.

    BETA1_REPORT    → Update topology state.
                      If β₁ == 0: generate alert.
                      If partition_risk > 0.5: generate alert.

    SUBSTRATE_HELLO → Add substrate to state.
                      Consult compatibility matrix.
                      Generate info event.

    SUBSTRATE_BYE   → Mark substrate as leaving.
                      Update bridge states.
                      Update topology state.
                      Generate info event.

    TOPOLOGY_CHANGE → Update topology state.
                      Recompute β₁.
                      Generate info event.
```

### 10.3 The Watch's Alerting Philosophy

The watch alerts on conditions that require human attention. The watch does not alert on conditions that can be handled automatically. The watch does not alert on conditions that are expected. The watch alerts on:

1. **Unexpected state transitions.** A substrate going from ALIVE to DEAD. A bridge going from UP to DOWN. A primitive going from STABLE to UNRESOLVABLE_DRIFT. These are unexpected, and they require attention.

2. **Threshold violations.** Budget falling below the YELLOW threshold. β₁ dropping to 0. Partition risk rising above 0.5. These are threshold violations, and they require attention.

3. **Accounting errors.** DoubleEntry imbalance. A substrate reporting spending more than the treasury has. These are accounting errors, and they require immediate attention.

4. **Unknown states.** A bridge with status UNKNOWN. A substrate with state UNKNOWN. A primitive with drift_type UNKNOWN. These are unknowns, and they require attention — not because they are necessarily problems, but because the watch cannot determine whether they are problems, and that uncertainty is itself a condition that requires attention.

The watch does *not* alert on:

1. **Expected state transitions.** A substrate going from ALIVE to ALIVE. A bridge going from UP to UP. These are expected, and they do not require attention.

2. **Resolvable drift.** A primitive with drift_type RESOLVABLE. This is drift, but it is drift that the bridges can accommodate. The watch logs it but does not alert.

3. **Normal budget consumption.** A cost report showing that the Quilt spent 80% of its budget, with ticks_remaining = 500. This is normal consumption, and it does not require attention.

The watch's alerting philosophy is conservative: alert on the unexpected, alert on the dangerous, alert on the unknown. Do not alert on the expected, the safe, or the known. A watch that alerts on everything is a watch that no one listens to. A watch that alerts on nothing is a watch that no one heeds. The correct alerting policy is the one that maximizes the signal-to-noise ratio, and that means alerting only when the watch's judgment — encoded in the state machine's rules — says that attention is needed.

### 10.4 The Watch Observing Itself

We said, in Section 3, that the watch is in the Quilt. The watch is a cell, or a collection of cells, and it is observed by the same instruments it uses to observe others. This means that WaaS must emit its own telemetry. WaaS must emit heartbeats. WaaS must emit cost reports. WaaS must emit drift signals.

This is not optional. A watch that does not observe itself is a watch that cannot be trusted, because it has no way to detect its own failures. A watch that does not emit heartbeats might be dead, and no one would know. A watch that does not emit cost reports might be consuming the entire budget, and no one would know. A watch that does not emit drift signals might have drifted — its state machine might have changed, its alerting rules might have changed, its correlation logic might have changed — and no one would know.

```
    THE WATCH OBSERVING ITSELF

    ┌──────────────────────────────────────────────────┐
    │                    THE QUILT                      │
    │                                                   │
    │   S₁ ─── S₂ ─── S₃                              │
    │   │     │     │                                  │
    │   S₄ ─── S₅ ─── S₆                              │
    │         │                                        │
    │    ┌────▼─────┐                                  │
    │    │   WaaS   │ ── emits HEARTBEAT              │
    │    │  (watch) │ ── emits COST_REPORT            │
    │    │          │ ── emits DRIFT_SIGNAL           │
    │    │          │ ── emits BRIDGE_STATUS          │
    │    │          │   (for its own internal          │
    │    │          │    "bridges" to registry,        │
    │    │          │    to ingestion, etc.)           │
    │    └────┬─────┘                                  │
    │         │                                        │
    │    WaaS observes itself                          │
    │    through the same instruments                  │
    │    it uses to observe others.                    │
    │                                                   │
    │    If WaaS stops emitting heartbeats,             │
    │    another watch (or a standalone                │
    │    monitor) should detect this and alert.         │
    │                                                   │
    └──────────────────────────────────────────────────┘
```

The recursive structure of the watch observing itself is the practical consequence of the 4th Impossibility. There is no outside position. The watch is on the manifold. The watch can only observe itself from the manifold, using the same instruments it uses to observe everything else. This means the watch's self-observation is subject to the same limitations as its observation of everything else: it is local, it is lossy, and it is incomplete.

The watch handles this by having *multiple* watches. Not one WaaS instance, but several, each observing the Quilt and each other. If one watch fails, the others detect it. If one watch drifts, the others detect it. The watches form a mutual observation network, and the trust in the system comes not from any single watch's perfection but from the network's redundancy.

```
    MUTUAL OBSERVATION NETWORK

         Watch A ── observes ──→ Watch B
            │                        │
            │                        │
            └── observes ──→ Watch C ←┘
                             │
                             │
         Watch A ←── observes ┘

         Watch B ←── observes ──→ Watch C

    Each watch observes the Quilt.
    Each watch observes the other watches.
    If any watch fails, the others detect it.
    If any watch drifts, the others detect it.

    This is the best we can do.
    It is not perfect.
    It is sufficient.
```

### 10.5 The Watch and the Sea

We began with the 4th Impossibility, and we end with it. The 4th Impossibility says that perfect observation is impossible. We have spent this paper designing instruments that observe well, but not perfectly. The Health Layer observes liveness, but not perfectly — it can be fooled by ghost ships. The Compatibility Matrix observes compatibility, but not perfectly — it can only report what has been tested. The Drift Detector observes drift, but not perfectly — it can only see the test inputs it has been given. The Cost Meter observes budget, but not perfectly — it relies on DoubleEntry, and DoubleEntry relies on honest reporting. The β₁ Meter observes topology, but not perfectly — it relies on the Bridge Registry, and the Bridge Registry is eventually consistent. The Bridge Registry observes bridges, but not perfectly — it is always slightly behind reality.

Each instrument is imperfect. Each instrument has a horizon beyond which it cannot see. Each instrument is a point on the manifold, and the manifold is always more than the point.

But the watch — the watch that stands at the confluence of all these instruments, that reads them all, that correlates them, that knows where each instrument is blind and where each instrument sees — the watch is more than any single instrument. The watch is the composition of imperfect observations into a sufficient observation. Not a perfect observation. A sufficient observation. An observation that is good enough to navigate by. Good enough to keep the Quilt running. Good enough to know when to alert and when to log and when to do nothing.

The sea is dark. The fog is thick. The horizon is close. But the watch has instruments, and the instruments have the watch, and together they are the thing that stands between the Quilt and the dark.

```
    ┌─────────────────────────────────────────────────────┐
    │                                                       │
    │                   THE WATCH                           │
    │                                                       │
    │    "I cannot see the whole sea.                       │
    │     I can see the bearing.                            │
    │     I can see the sounding.                           │
    │     I can see the anemometer.                         │
    │     I can see the barometer.                          │
    │     I can see the chronometer.                        │
    │                                                       │
    │     I cannot see the whole sea.                       │
    │     I can see enough to keep the watch.               │
    │                                                       │
    │     The instruments are the watch.                    │
    │     The watch is the instruments.                     │
    │     The sea is dark.                                  │
    │     We stand anyway."                                  │
    │                                                       │
    └─────────────────────────────────────────────────────┘
```

---

*End of volume. The watch continues. The instruments continue. The sea continues. The next volume concerns the Repair Protocol — what the watch does when the instruments report something that cannot be ignored. But that is a matter for another paper, another watch, another night.*

*For now: keep the watch. Trust the instruments. Know their limits. And when the fog comes — and it will come — remember that the watch is not the fog, and the instruments are not the horizon, and the sea, for all its darkness, is still the sea, and we are still on it.*

*Steady as she goes.*

---

**Appendix A: Instrument Quick Reference**

```
INSTRUMENT          WHAT IT MEASURES         KEY LIMITATION
────────────────    ───────────────────      ─────────────────────────
Health Layer        Liveness of substrates   Cannot detect ghost
                    and bridges              ships without tick check
                                             (Section 4.2)

Compatibility       Which versions work      Only as good as the
Matrix              with which               tests behind it
                                             (Section 5.3)

Drift Detector      Behavioral change,       Coverage limited by
                    classified by             self-test suite
                    resolvability             (Section 6.5)

Cost Meter          Budget consumption,      Relies on honest
                    per tick, per             reporting from
                    substrate                 substrates
                                             (Section 7.4)

β₁ Meter            Topology complexity      Relies on Bridge
                    (number of               Registry, which is
                    independent cycles)       eventually consistent
                                             (Section 8.4)

Bridge Registry     Which bridges exist,     Always slightly
                    where, what status        behind reality
                                             (Section 9.4)

Watch Protocol      How instruments          Assumes lossy
                    communicate              transport; must
                                             tolerate lost events
                                             (Section 3.2)
```

**Appendix B: Event Type Summary**

```
EVENT TYPE         BODY SUMMARY                  TRANSPORT    FREQUENCY
──────────────     ──────────────                ─────────    ──────────
HEARTBEAT (0x01)   cell_id, version, tick,       UDP/mcast    50 ticks
                   nonce, uptime, queue_depth

BRIDGE_STATUS(0x02) bridge_id, status,           UDP/mcast    100 ticks
                   last_good, reason, latency,
                   error_rate

DRIFT_SIGNAL(0x03) substrate_id, primitive_id,  TCP          on change
                   drift_type, fingerprints,
                   test details, delta

COST_REPORT(0x04)  tick, budget, consumed,       TCP          every tick
                   per-substrate breakdown,
                   depletion_rate, ticks_left

TOPOLOGY_CHANGE(0x05) old_graph, new_graph,     TCP          on change
                   affected bridges

PRIMITIVE_BREAK(0x06) primitive_id, old_sem,    TCP          on change
                   new_sem, breaking_changes,
                   migration_path

SUBSTRATE_HELLO(0x07) substrate_id, version,    UDP/mcast    on join
                   capabilities, bridge_offers

SUBSTRATE_BYE(0x08) substrate_id, reason,       TCP          on leave
                   graceful (bool)

BUDGET_WARNING(0x09) tick, ticks_remaining,     TCP          threshold
                   threshold_level,             (on transition)
                   recommendation

BETA1_REPORT(0x0A) tick, beta1, delta,          UDP/mcast    100 ticks
                   substrates, bridges,
                   components, partition_risk,
                   trend

CUSTOM (0xFF)      per schema_id                per spec     per spec
```

**Appendix C: Glossary of Maritime Terms**

```
TERM                MEANING IN THE QUILT
────────            ─────────────────────────────────
bearing             the direction of a substrate
                    relative to the watch

sounding            a measurement of depth, i.e.,
                    a measurement of how close
                    a substrate is to budget
                    exhaustion

chronometer         the Quilt's global tick counter

almanac             the Compatibility Matrix

lighthouse          the Bridge Registry

fog                 the 4th Impossibility — the
                    region beyond which the watch
                    cannot see

horizon             the boundary of observability
                    for a given instrument

ghost ship          a substrate that emits telemetry
                    but does no actual work
                    (Section 4.2)

tide                resolvable drift — predictable,
                    bounded, returns

current             unresolvable drift — persistent,
                    structural, does not return

reef                an unresolvable drift that has
                    been detected — the channel
                    is closed

keeper              the operator of the watch

watch               the practice of observation,
                    constituted by the instruments

steady as she goes  maintain current course and
                    speed; do not change anything;
                    the Quilt is operating normally
```

---

*Lucineer Codex, Volume V. Signed by the watch. Dated by the tick. The sea is dark. We stand anyway.*