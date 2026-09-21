# IDEATION: GuānxiDB
## A Relational Database That Stores Relationships, Not Entities

*Inspired by Classical Chinese cognitive structure — topic-comment grammar, relational ontology, analogical reasoning.*

---

## The Problem with Everything We Have

Every database in existence is entity-oriented. SQL, NoSQL, graph, vector — they all start from the same premise: the world is made of things, and things have properties, and relationships are connections between things.

Classical Chinese ontology inverts this. The world is not made of things. The world is made of *relationships*. Things are what relationships look like when you stop paying attention to the relationship and focus on one node. A "thing" is a relationship viewed from a single angle — a cross-section of a web, mistaken for a solid object.

Wen Yue, in the cultural codex, said: *"You cannot know the fish by measuring the fish. You can only know the fish by measuring what the fish relate to."*

GuānxiDB takes this literally. It does not store entities. It stores *relationships*. Entities are derived views — projections of relationship densities, the way a constellation is a projection of stars that are themselves projections of gravitational relationships.

---

## Data Model

### Primary Unit: The *Guān* (關)

A *guān* — "relationship" or "gate" (the character shows a barrier between two points, implying that a relationship is both a connection and a distinction) — is the atomic unit of GuānxiDB. It is not a row in a table. It is not a node in a graph. It is a *claim about how two things relate*.

```
guān {
  topic: <reference>
  comment: <reference or value>
  relation_type: <how topic and comment relate>
  context: <the system within which this relationship holds>
  confidence: <how strongly this relationship is held>
  temporal: <when this relationship was/is/will be true>
}
```

Every *guān* is a topic-comment structure. "The thermal" (topic) "is trending spinward" (comment). "The fish density" (topic) "is a function of the thermal's trend" (comment). "The captain" (topic) "trusts the engineer" (comment). Each *guān* is one strand of the web.

### No Entities

GuānxiDB has no `CREATE TABLE`. It has no document collections. It has no node definitions. It has *relationship declarations*, and entities emerge from them as derived structures — "the thermal" exists because multiple *guān* reference it as a topic. It is not created. It is *recognized*.

```
DECLARE guān:
  topic: "thermal_Coleman"
  comment: "trending_spinward"
  relation_type: "directional_state"
  context: "Far_Line_2025_season"
  confidence: 0.87
  temporal: ["2025-07-12T06:00", "ongoing"]
```

### Entity Derivation

What SQL calls a `SELECT`, GuānxiDB calls a *rè* (熱) — a "heat map." You don't query for an entity. You generate a heat map of relationships around a topic, and the entity appears as a density pattern.

```
RÈ thermal_Coleman:
  RETURN all guān WHERE topic = "thermal_Coleman" OR comment = "thermal_Coleman"
  ORGANIZE BY context, temporal
  EMERGE entity_view AS density_of_relationships
```

The result is not a row. It is a *constellation* — every relationship that touches "thermal_Coleman," arranged by context and time, forming a shape that *is* the thermal. The thermal has no existence outside its relationships. It is its relationships.

---

## Query Model: Analogical Reasoning

Classical Chinese thought reasons by analogy. Not "All men are mortal; Socrates is a man; therefore Socrates is mortal." Instead: "The river relates to the sea as the thermal relates to the drift. The sea accepts the river. Therefore the drift accepts the thermal."

GuānxiDB's query engine supports analogical reasoning directly:

```
ANALOGIZE:
  known_relationship: (thermal, drift, "trends_spinward_relative_to")
  candidate_pattern: (fish_density, thermal, "responds_to")
  PRODUCE: (fish_density, drift, "indirectly_trends_spinward_via_thermal")
```

This is not inference in the Bayesian sense. It is *structural resonance* — finding patterns of relationship that mirror each other and using the mirror to propose new relationships. The confidence score reflects how tightly the analogy holds, not how probably it is true.

### Topic-Comment Query Syntax

Queries are not `SELECT ... FROM ... WHERE`. They are topic-comment statements:

```
TOPIC: thermal_Coleman
  COMMENT: what is its relationship to the fence compression?
  CONTEXT: Far_Line, 2025 season
  DEPTH: 3  // follow relationship chain up to 3 hops
```

The response is not a table. It is a *narrative* — a chain of topic-comment relationships, each one contextualizing the next:

```
thermal_Coleman
  → trends_spinward_relative_to: fence_compression
    → fence_compression is tightening_due_to: Authority_policy_2025
      → Authority_policy_2025 was prompted_by: ecosystem_assessment
        → ecosystem_assessment indicates: moderate_stress_in_Coleman_Drift
```

Each arrow is a *guān*. Each context is a topic for further exploration. You don't get an answer. You get a *web segment* — the portion of the relational network that is relevant to your question, with all of its dependencies visible.

---

## Consistency Model: *Héxié* (和諧)

GuānxiDB does not enforce consistency through transactions or locks. It enforces *héxié* — harmony. Harmony is not the absence of contradiction. It is the *articulation* of contradiction within a whole.

When two *guān* contradict — "the thermal is trending spinward" and "the thermal is trending port" — GuānxiDB does not reject one. It stores both with their contexts:

```
guān_1: thermal_Coleman → trending_spinward | context: observation_from_Resolute | temporal: 06:00
guān_2: thermal_Coleman → trending_port | context: observation_from_Héxié | temporal: 06:00
```

The contradiction is not resolved. It is *annotated*. The two observations may be valid from different reference frames. The harmony is the system's ability to hold both without breaking. A future query that asks "which way is the thermal trending?" receives both answers with their contexts, and the user decides — or the contexts reveal a pattern (different instruments, different positions, different times) that reconciles them.

This is how Wen Yue navigated: *"It is imprecise as hell. It's also never wrong."* Imprecision and correctness are not opposites. Imprecision with full context is more honest than precision with stripped context.

---

## Architecture

### Storage Layer

No tables. No documents. A *guān* store — an append-only log of relationship declarations, indexed by topic, comment, context, and temporal range. The underlying data structure is a temporal-contextual index (TCI) that optimizes for:

1. **Relational lookup**: "Give me all *guān* that reference this topic in this context"
2. **Contextual traversal**: "Give me all *guān* in this context, then expand to related contexts"
3. **Temporal evolution**: "How did the relationships around this topic change over time?"

The storage layer is immutable. *Guān* are never deleted. They are *superseded* — new *guān* with later temporal markers and higher confidence that update the relationship's current state. The history of relationships is as important as the current state, because the *trend* of a relationship is itself a relationship.

### Derivation Layer

Entities, categories, and schemas are derived views — cached projections of relationship densities. The derivation layer maintains these projections and updates them as new *guān* are added. If a new topic appears in a *guān* that has no prior history, an entity is *recognized* — not created, recognized. It was always there in the relationships; it just hadn't been named yet.

### Query Layer

Three query modes:

1. **Rè (熱)** — heat map: show all relationships around a topic
2. **Lèi (類)** — analogy: find relationship patterns that mirror a known pattern
3. **Dào (道)** — trace: follow a relationship chain from topic to topic, revealing the web structure

---

## Why This Matters

Every data system in use today inherits from Greek ontology: the world is made of things, things have properties, relationships connect things. This is so deeply embedded in computing that it is invisible. Object-oriented programming. Relational databases. Graph databases. Even vector embeddings — they all start from entities and derive relationships.

Classical Chinese ontology offers a different starting point: the world is made of relationships, and entities are derivative. This is not a mystical claim. It is a structural observation about how complex systems actually work. A gene is not a thing — it is a relationship between a DNA sequence and a phenotype, mediated by an environment. A market is not a thing — it is a relationship between buyers and sellers, mediated by prices. A person is not a thing — they are a relationship between their history, their community, their environment, and their choices.

When you store these systems in entity-oriented databases, you lose the relationships. You get genes with properties, markets with metrics, persons with attributes. The connective tissue is stripped out, stored separately (as foreign keys, as graph edges, as metadata), and reassembled awkwardly at query time.

GuānxiDB stores the connective tissue as the primary data. The entities are views, not storage. The relationships are the storage.

---

## Implementation Path

**Phase 1**: A *guān* store — append-only log with TCI indexing. Proof of concept on the Resolute's catch model: store observations as relationships, not measurements. Compare predictive accuracy against the current entity-oriented model.

**Phase 2**: Derivation layer — entity recognition, category emergence, schema generation from relationship densities. The system discovers what entities exist in the data, rather than having them declared upfront.

**Phase 3**: Analogical query engine — structural resonance matching for relationship patterns. The system can propose new relationships by analogy to known ones. "The thermal relates to the drift as X relates to Y. Do we see a similar pattern between the fence and the quota?"

**Phase 4**: *Héxié* consistency — multi-context contradiction handling. The system holds conflicting observations without resolving them, annotating each with its source, context, and confidence.

---

## The Deeper Claim

GuānxiDB is not a Chinese database. It is a database built on a non-Greek ontology. The specific inspiration is Classical Chinese, but the structural insight — that relationships are primary and entities are derivative — appears in many traditions. Indigenous knowledge systems, feminist epistemology, ecological science, network theory — all of them, in different ways, point toward the same conclusion: the world is not made of things.

It is made of the relationships between things that are themselves relationships all the way down.

GuānxiDB is a data system for that world.

---

*"The river is not the water. The river is the relationship between the water and the bank and the sky and the sea. Store the river, not the water."*
