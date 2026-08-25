# IDEATION: relational-ontology

## Proposed Repository: `relational-ontology`

### One-Line Description

A knowledge representation framework where entities are defined by their relationships, not their properties — inspired by Classical Chinese topic-comment grammar and the concept of 理 (lǐ).

---

### Origin

**Polyformalism Languages** demonstrated that Classical Chinese cognitive patterns — topic-comment structure, relational ontology, analogical reasoning — converge on the same problem-solving outcomes as Greek categorical logic and Navajo process reasoning. But the convergence is not identity: each tradition sees different things on the way to the same destination.

The Chinese tradition sees **threads**. Where the Greek tradition asks "what IS this?" (categorization) and the Navajo tradition asks "how is this MOVING?" (process), the Chinese tradition asks "what does this CONNECT to?" (relationship). This suggests a fundamentally different approach to knowledge representation.

---

### The Problem

Current knowledge systems — databases, ontologies, type systems, graph stores — are overwhelmingly Greek in their cognitive architecture. They organize entities by type, assign properties to instances, and reason through categorical inference. This is powerful. It is also structurally blind to cross-domain relationships, emergent network effects, and the kind of "thinning threads" dynamics that Táng Wěi's story describes.

Graph databases (Neo4j, etc.) partially address this, but they still operate within a Greek ontology: nodes have types, edges have labels, and the graph is queried through pattern-matching against a schema. The schema is categorical. The relationships are first-class, but the thinking about relationships is still subordinated to the category of the nodes.

What if we built a knowledge system where **relationships are primary and entities are derivative**?

---

### The Proposal

`relational-ontology` is a framework for knowledge representation built on three principles borrowed from Classical Chinese cognitive patterns:

#### 1. Topic-Comment Data Model

Instead of the subject-predicate model (Entity HAS Property), use a topic-comment model (Regarding Topic, here is Observation).

```
// Subject-predicate (Greek):
//   Ship { class: "fishing", speed: 12, status: "active" }

// Topic-comment (Chinese):
//   Topic: ship:Resolute
//   Comment: observed-speed → 12 (witness: sensor-array, confidence: 0.97)
//   Comment: functional-class → fishing (source: registry, confidence: 1.0)
//   Comment: current-status → active (witness: crew-report, confidence: 0.9)
```

The topic doesn't "have" properties. Observations are made about the topic. Each observation carries provenance — how do we know? This mirrors Quechua evidentiality (independently arrived at from a different cognitive tradition) but the key structural difference is that the topic is a reference point, not a subject with essential attributes. Observations can change without changing the topic's identity.

**Conservation law:** Topic identity is invariant under observation change. The Resolute is still the Resolute whether its speed is 12 or 0. This prevents the identity-entanglement problem where changing properties threaten entity identity.

#### 2. Lǐ-Based Relational Indexing

Instead of indexing entities by type (as in SQL tables) or by label (as in graph databases), index by **relationship density** — the 理度 (*lǐ dù*, pattern-density) of each region of the knowledge graph.

```
// A region with high lǐ dù has many converging relationships
// and is structurally critical to the graph's coherence.
// A region with low lǐ dù has sparse relationships and is
// structurally peripheral.

// Query: "What are the most structurally critical entities
// in this knowledge space?"
// Answer: The ones with the highest lǐ dù — the densest
// relationship convergence.
```

This mirrors the concept of 理 (lǐ) — the underlying pattern that determines system health. When a structurally critical relationship thins, the system degrades — not because any entity has failed, but because the *pattern* has weakened.

**Conservation law:** *Lǐ dù* conservation. The total relational density of the system should be maintained. Extraction (removing relationships) must be balanced with regeneration (growing new relationships). This is a relational analog to the first law of thermodynamics.

#### 3. Analogical Inference Engine

Instead of deductive inference (syllogism) or inductive inference (statistical learning), implement **analogical inference** — finding structural correspondences between different domains and using them to transfer insights.

```
// Problem: "Why is the cloud field declining?"

// Step 1: Find structurally analogous systems.
//   The cloud field's relational structure matches
//   a river delta network (identified by topological
//   correspondence, not domain similarity).

// Step 2: Query the analog.
//   "What causes decline in river delta networks?"
//   Answer: substrate disruption at bottleneck nodes.

// Step 3: Map back to the original.
//   "Where are the bottleneck nodes in the cloud field?"
//   → Identified through relational topology mapping.
```

This is the cognitive operation Táng Wěi describes: understanding a system by finding its structural parallel. It's not metaphor — it's isomorphism detection at the level of relational structure.

**Conservation law:** Analogical scope. The inference engine can only draw analogies between systems with demonstrated structural correspondence (verified by topological isomorphism testing). This prevents false analogies — the kind of "this is like that" reasoning that sounds persuasive but has no structural basis.

---

### Architecture

```
relational-ontology/
├── core/
│   ├── topic.py          # Topic entity (reference point, not subject)
│   ├── comment.py         # Observation (with provenance and confidence)
│   ├── relation.py        # Relationship (primary; entities are derivative)
│   └── pattern.py         # Lǐ detection — find structural patterns in relation graph
├── inference/
│   ├── analogical.py      # Analogical reasoning engine
│   ├── topology.py        # Isomorphism detection for structural correspondence
│   └── prediction.py      # Predict cascade effects from relational disruption
├── query/
│   ├── shì_reader.py      # Read 勢 (shì) — the strategic disposition of the system
│   ├── lǐ_map.py          # Map the lǐ — the deep structural pattern
│   └── relational_health.py  # Assess relational integrity, not entity health
├── conservation/
│   ├── thread_monitor.py  # Monitor relationship thinning (early warning)
│   ├── bottleneck.py      # Identify structurally critical nodes
│   └── lǐ_dù.py           # Track pattern-density across the knowledge space
└── experiments/
    ├── belt_ecology/      # Apply to ecological systems
    ├── fleet_network/     # Apply to fleet coordination
    └── quota_system/      # Apply to resource allocation
```

---

### Why This Matters for SuperInstance

In the γ + η = C framework:

- **γ (Growth):** Relational ontology enables growth through relationship discovery. The system grows by finding new connections, not by creating new entities. This is a fundamentally different growth model than entity-accumulation.

- **η (Avoidance):** The framework avoids categorical bias — the structural blind spot that occurs when a system's ontology forces cross-domain relationships into within-domain categories. The *ti esti* question ("what IS it?") is replaced by the *guānxì* question ("what CONNECTS to it?"), avoiding the entire class of errors that come from misclassification.

- **C (Constraint):** The conservation law is *lǐ dù* preservation — the total relational density of the system must be maintained. This is a relational constraint, not an entity constraint, and it captures dynamics that entity-level conservation laws miss.

---

### Connection to Existing SuperInstance Work

- **polyformalism-languages:** `relational-ontology` operationalizes the Chinese cognitive pathway identified in the polyformalism research. It is the computational implementation of topic-comment reasoning.

- **negative-space-core:** The concept of *lǐ* — the pattern that exists in the spaces between entities — is a manifestation of negative-space intelligence. The pattern is not in the nodes. It is in the threads. The avoidance (η) of categorical thinking reveals the relational structure that categories obscure.

- **conservation-authority (theoretical):** A relational conservation law (*lǐ dù* preservation) is a different governance tool than species-level conservation. It protects the web, not the knots.

---

### Slogan

> *The web is older than the knots. Build for the web.*

---

### Languages

Python (core), with Rust bindings for large-scale relation graph traversal. Query language: RL (Relational Language) — a topic-comment query syntax inspired by Classical Chinese grammatical structure.

```
# RL query example:
# "Regarding the Coleman Drift, how are its relationships?"
# Resolves to: topic-comment query returning relational health assessment

topic: zone:coleman-drift
  ask: relational-health
  depth: 7
  include: cascade-predictions
```

---

### Status

**Proposal stage.** Exists as this ideation document. Implementation depends on validation of the analogical inference approach against existing graph database benchmarks, and on demonstrating that *lǐ dù* tracking provides materially better early-warning signals for system degradation than entity-level monitoring.

---

*"Build for the web, not the knots. The knots will follow the web."*
— Táng Wěi (fictional)