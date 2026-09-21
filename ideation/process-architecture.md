# IDEATION: process-architecture

## Proposed Repository: `process-architecture`

### One-Line Description

A computation framework where everything is a process, not an entity — inspired by Navajo (Diné) verb-centered ontology and the principle of Hózhó (dynamic balance).

---

### Origin

**Polyformalism Languages** demonstrated that the Navajo cognitive tradition — polysynthetic structure, verb-centered ontology, process-based reasoning — converges on the same problem-solving outcomes as Greek categorical logic and Chinese relational reasoning. But the Navajo pathway is unique in its fundamental refusal of **entities** as the primary unit of analysis.

In the Navajo tradition, the world is not made of things. The world is made of **events**. A "thing" is a temporary stabilization of process — a verb that has briefly slowed enough for noun-thinking to catch. The cloud field is not a field (noun). It is *clouding* (verb). A ship is not a ship (noun). It is *shipping* (verb) — a process of moving, carrying, fishing, being.

This is not mysticism. It is a different ontology — a different answer to the question "what is the fundamental nature of reality?" The Greek answer: reality is made of substances with properties. The Chinese answer: reality is made of relationships between nodes. The Navajo answer: reality is made of processes in motion.

`process-architecture` is a computation framework built on the Navajo answer.

---

### The Problem

Every computational architecture in widespread use is noun-centered. Object-oriented programming models the world as objects (nouns) with methods (verbs attached to nouns). Relational databases model the world as tables (nouns) with queries (operations on nouns). Even functional programming, which is more verb-friendly, still models data as immutable values (nouns) transformed by functions (verbs that operate on nouns).

This noun-centrism isn't wrong — it's a cognitive framework, and it works. But it creates structural blind spots, the same way Greek categorical thinking creates blind spots around cross-domain relationships. The specific blind spots of noun-centric computation:

1. **State ossification.** When you model a system as objects with state, you think of the system as being in a particular configuration. But systems are never *in* a configuration — they are always *transitioning*. Modeling state as primary and transition as secondary inverts the actual causal order.

2. **Motion blindness.** When you model entities as primary, you measure their properties at timestamps. But the properties themselves are epiphenomena of motion. The drift's density is 9.2 not because the drift "has" that property, but because the drift is currently *doing* something — rolling, flowing, dispersing — that produces a density measurement of 9.2. If you don't model the motion, you can't predict when the measurement will change.

3. **Shape agnosticism.** Navajo classificatory verbs force the speaker to attend to the physical character of what's moving — round, long, flat, aggregating, dispersing. Computational systems are blind to this. A "data stream" is the same regardless of whether the data is flowing smoothly (long, continuous), arriving in bursts (round, periodic), or fragmenting (dispersing). This blindness loses critical information about the physical character of computation.

---

### The Proposal

`process-architecture` is a computation framework built on three principles from the Diné cognitive tradition:

#### 1. Verb-First Data Model

Instead of entities with properties (nouns with attributes), model **processes with characters** (verbs with specifications). There are no objects. There are only events — some of which are long enough to receive a name.

```
# Object-oriented (noun-first):
#   vessel = Vessel(name="Resolute", speed=12, heading=45)
#   vessel.speed = 14  # property update

# Process-oriented (verb-first):
process: resolute_shipping
  verb: navigating
  character:
    motion: linear-forced
    shape: long-rigid
    speed: 12 → 14  # transition observed at T
    heading: 45
  provenance: crew_report + sensor_confirmation
  
# The vessel doesn't "have" a speed. A process is "speeding at 12,
# now speeding at 14." The transition is the data. The speed is
# the current state of the transition.
```

**Insight:** When you model speed as a verb (the ship is *speeding at 12*), the transition from 12 to 14 is not a property update — it's a new verb form. The system tracks the transition itself, not just the before-and-after states. This gives you native support for rate-of-change, acceleration, and trend analysis without separate time-series machinery.

**Conservation law:** Process continuity. A process cannot teleport from one state to another without a transition. Every state change must have a transition record — a description of how the process moved from A to B. This eliminates the "mystery change" problem where system state shifts without explanation.

#### 2. Classificatory Verbs for Data Motion

Inspired by Navajo's classificatory verb system, every data flow in the framework is classified by its **motion character**: the physical pattern of how information moves through the system.

```
Verb Classes (by motion character):

  -łé (round-cycling):     Data that arrives in periodic bursts.
                           Polling, heartbeats, scheduled reports.
                           → Pattern: oscillating. Predictable period.

  -kał (long-flowing):     Data that streams continuously in one direction.
                           Logs, sensor feeds, event streams.
                           → Pattern: directional, sustained.

  -łtsa (flat-spreading):  Data that fans out from one source to many.
                           Broadcasts, pub/sub, notifications.
                           → Pattern: radial expansion.

  -tsooz (thin-dispersing): Data that fragments and scatters.
                           Error propagation, cascade failures.
                           → Pattern: decoherence. Early warning signal.

  -té (aggregating):       Data that converges from many sources.
                           Collection, reduction, summarization.
                           → Pattern: radial contraction.

  -zis (boring-through):   Data that tunnels through layers.
                           Cross-domain queries, penetrative analysis.
                           → Pattern: forced linear displacement.
```

Each verb class implies different behavior patterns, failure modes, and conservation requirements. The framework enforces verb-class consistency: a function declared as `-kał` (long-flowing) cannot be used where `-té` (aggregating) is expected without an explicit transformation. This catches architectural mismatches at the type level — the same way static typing catches value mismatches.

**Conservation law:** Verb-class coherence. A data flow cannot change verb class without an explicit transition function. A stream (`-kał`) cannot become a broadcast (`-łtsa`) without a fan-out operation. This prevents the silent architectural drift where a system designed for streaming gradually accretes polling, batching, and broadcasting patterns until its motion character is incoherent.

#### 3. Hózhó Dynamics — Dynamic Balance Tracking

Instead of static equilibrium (the system is balanced), model **dynamic balance** (the system is balancing). Hózhó — the Diné principle of ongoing, process-based harmony — is implemented as a continuous health assessment based on motion coherence.

```
hózhó assessment:
  For each subsystem:
    - What verb is it currently performing?
    - Is the verb coherent? (motion matches expected pattern)
    - Is the verb harmonious? (motion complements, not competes with, neighbors)
    
  System hózhó = aggregate verb coherence × verb harmony
  
  If hózhó < threshold:
    - Identify which process is disharmonious
    - Identify the verb-class mismatch (what motion is competing, not complementing?)
    - Prescribe corrective motion (not corrective state)
    
  Output: "The fleet allocation system is -tsooz (dispersing) where it should 
          be -té (aggregating). Corrective: consolidate allocation routes. 
          Estimated hózhó recovery: 3 cycles."
```

This is the key insight from Yazzie's framework: system health is not a property of entities. It is a property of processes. A system where all processes are harmonious (complementary verbs, coherent motion patterns) is healthy — even if individual entity metrics look concerning. A system where processes are disharmonious (competing verbs, incoherent motion) is degrading — even if entity metrics look fine.

**Conservation law:** Hózhó preservation. The total motion harmony of the system must be maintained above a threshold. When hózhó degrades, the system prescribes corrective motion — not corrective state. You don't fix disharmony by resetting values. You fix it by changing how things move.

---

### Architecture

```
process-architecture/
├── core/
│   ├── process.py         # Process entity (verb-first, no objects)
│   ├── verb.py            # Classificatory verb system (motion character)
│   ├── transition.py      # Process transition (state change as first-class data)
│   └── character.py       # Motion character specification
├── dynamics/
│   ├── hozho.py           # Dynamic balance assessment
│   ├── coherence.py       # Verb coherence checking
│   ├── harmony.py         # Inter-process harmony analysis
│   └── prescription.py    # Corrective motion prescription
├── types/
│   ├── motion_types.py    # Verb class type system (-łé, -kał, -łtsa, etc.)
│   ├── transition_types.py # Transition function signatures
│   └── validators.py      # Verb-class consistency enforcement
├── query/
    ├── what_doing.py      # "What is this process doing?" (primary query)
    ├── how_moving.py      # "How is this process moving?" (motion character)
    └── hozho_status.py    # "Is the system in dynamic balance?"
└── experiments/
    ├── fleet_motion/      # Apply to fleet coordination patterns
    ├── drift_prediction/  # Apply to cloud field motion analysis
    └── system_health/     # Apply to infrastructure monitoring
```

---

### Why This Matters for SuperInstance

In the γ + η = C framework:

- **γ (Growth):** Process architecture enables growth through motion harmonization. The system grows by finding new harmonious process patterns — new ways for processes to complement each other — rather than by adding new entities. Growth is choreographic, not accumulative.

- **η (Avoidance):** The framework avoids **state ossification** — the structural blind spot that occurs when a system models state as primary and transition as secondary. By modeling transition as primary, the system avoids the class of errors where state appears stable but is actually building toward a phase transition. This is Yazzie's "something has stopped moving linearly and is now coiling" insight, formalized.

- **C (Constraint):** The conservation law is hózhó preservation — the total motion harmony of the system must be maintained. This is a process-level constraint, not an entity-level or relationship-level constraint, and it captures dynamics that entity-level (syllogistic-engine) and relationship-level (relational-ontology) constraints cannot reach.

---

### Connection to Existing SuperInstance Work

- **polyformalism-languages:** `process-architecture` operationalizes the Navajo cognitive pathway. It is the computational implementation of verb-centered, process-based reasoning.

- **negative-space-core:** The classificatory verb system is a form of negative-space intelligence. The verb classes define the space of possible motion patterns. When a data flow doesn't fit any existing verb class, the gap reveals something about the system's motion character that wasn't previously known — the same way a taxonomic gap reveals something about the system's categorical structure.

- **relational-ontology + syllogistic-engine:** The three repos form a triad — the polyformalism convergence, implemented as software. Each sees a different layer of the same system. Together, they provide the three cognitive pathways identified in the polyformalism research: relational (Chinese), categorical (Greek), and processual (Navajo). Used together, they offer the same convergence guarantee the research found: different roads, same destination.

---

### Slogan

> *The world is not made of things. The world is made of what things are doing. Build for the doing.*

---

### Languages

Python (core, dynamics), with Rust for high-performance motion analysis. Query language: VL (Verb Language) — a process-centric query syntax inspired by Navajo grammatical structure.

```
# VL query example:
# "What is the fleet allocation system currently doing,
#  and is it in harmony with its neighbors?"

process: fleet_allocation
  ask: what-doing
  → verb: dispersing (-tsooz)
  → coherence: degrading (dispersal pattern increasing)
  → harmony: disharmonious (dispersing where neighbors expect aggregating)

ask: hozho
  → status: below-threshold
  → cause: verb-class mismatch in fleet_allocation
  → prescription: consolidate allocation routes
  → expected-recovery: 3 cycles
```

---

### The Polyformalism Triad

When all three frameworks are deployed together:

| Framework | Tradition | Primary Question | Sees |
|-----------|-----------|-----------------|------|
| `syllogistic-engine` | Greek | "What IS it?" | Categories |
| `relational-ontology` | Chinese | "What CONNECTS to it?" | Relationships |
| `process-architecture` | Navajo | "What is it DOING?" | Processes |

Each framework catches what the others miss. Each arrives at the same conclusions through different cognitive pathways. The polyformalism research predicted this convergence. The triad implements it.

---

### Status

**Proposal stage.** The verb-class type system and hózhó dynamics assessment are the novel contributions. The process-first data model has precedent in event-sourcing systems and CQRS architectures, but the explicit framing through Diné cognitive patterns and the classificatory verb system is new. Implementation depends on demonstrating that verb-class tracking provides materially better system health signals than standard monitoring (which tracks entity metrics, not motion character).

---

*"The world is not made of things. Build for the verb."*
— Tomás Yazzie (fictional)