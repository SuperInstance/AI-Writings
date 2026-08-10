# Ideation

> Design proposals for new computational frameworks, each inspired by a different cultural-linguistic tradition. Part of the **Polyformalism** project — the thesis that different cognitive traditions produce different but equally valid approaches to computation.

These documents are not implementations. They are design proposals — thorough, argued, ready to be built by someone with the right skills and the right amount of stubbornness.

---

## The Premise

The Polyformalism project starts from a simple observation: **every programming language, every database, every type system in existence inherits a single cognitive tradition — Ancient Greek categorical logic.** Objects, classes, entities, properties, subject-predicate structure. The world is made of things.

But this is not the only way humans think. Different cultures, different languages, different cognitive traditions produce fundamentally different approaches to knowledge. What if we designed computational systems from those traditions?

Each proposal in this directory takes one cultural-linguistic tradition and asks: what would a computational system look like if it were built from the ground up according to *that* tradition's ontology?

---

## The Proposals

### 1. Telos Type System (`telos-type-system.md`)
**Tradition:** Ancient Greek — Aristotelian teleology
**Status:** Concept document

An Aristotelian type system where types are defined by *purpose* (telos), not structure. A knife is not a knife because it has a blade and a handle — it's a knife because it *cuts*. Remove the structure and you still have the concept. Remove the purpose and you have nothing.

**Core insight:** Every type system in programming is structural. Types are shapes. But Aristotle argued the essence of a thing is its final cause — what it exists to do. A Telos type system would type things by their function, not their form.

**Key concepts:** Material cause (what it's made of), formal cause (its structure), final cause (its purpose), efficient cause (what created it). The final cause is the type.

---

### 2. Syllogistic Engine (`syllogistic-engine.md`)
**Tradition:** Ancient Greek — Aristotelian syllogistic logic
**Status:** Proposed repository

A formal reasoning system that derives necessary truths from categorical definitions. If all A are B, and C is A, then C is B. The engine of prediction — knowing something is true without having observed it, because it follows necessarily from premises.

**Core insight:** Where the Chinese tradition finds insight through analogy and the Navajo through process observation, the Greek tradition derives insight through syllogism. This is the computational engine of deduction.

**Key concepts:** Categorical definitions, syllogistic derivation, necessary truth, formal logic as computation.

---

### 3. GuānxiDB (`guanxi-db.md`)
**Tradition:** Classical Chinese — relational ontology (理, lǐ)
**Status:** Concept document

A database that stores *relationships*, not entities. In Classical Chinese ontology, the world is not made of things — it's made of relationships. Things are what relationships look like when you stop paying attention to the relationship and focus on one node.

**Core insight:** Every database in existence is entity-oriented. SQL, NoSQL, graph, vector — they all start from things. GuānxiDB inverts this: the world is made of relationships. A "thing" is a cross-section of a web, mistaken for a solid object. "You cannot know the fish by measuring the fish. You can only know the fish by measuring what the fish relate to."

**Key concepts:** Relationship as primary, entity as derivative. Topic-comment grammar as query structure. Analogical reasoning as join operation.

---

### 4. Relational Ontology (`relational-ontology.md`)
**Tradition:** Classical Chinese — topic-comment grammar, analogical reasoning
**Status:** Proposed repository

A knowledge representation framework where entities are defined by their relationships, not their properties. The Chinese tradition asks not "what IS this?" (Greek categorization) or "how is this MOVING?" (Navajo process) but "what does this CONNECT to?"

**Core insight:** A knowledge graph that doesn't store nodes — it stores edges. Nodes are inferred from the pattern of connections. This is not a graph database turned sideways; it's a fundamentally different storage primitive.

**Key concepts:** Threads, connections, analogical joins. Topic as the starting point, not a subject. Comment as relational expansion.

---

### 5. Hózhǫ́ Framework (`hozho-framework.md`)
**Tradition:** Navajo (Diné) — polysynthetic grammar, verb-centered ontology
**Status:** Concept document

A computation framework where everything is a verb. In Diné ontology, the world is not made of nouns — it's made of ongoing processes. Objects are what processes look like when you freeze-frame them. A river is not a thing; it is *river-ing*.

**Core insight:** Every programming language is noun-biased. Objects, classes, records, structs, tables — things that *are*. Even functional programming applies verbs (functions) to nouns (data). Diné ontology inverts this: the world is made of *verbs* — ongoing processes doing themselves. When the river dries up, the river-ing hasn't failed; it has completed.

**Key concepts:** Process as primary, entity as freeze-frame. Hózhó (dynamic balance) as correctness criterion. Polysynthetic composition as program structure.

---

### 6. Process Architecture (`process-architecture.md`)
**Tradition:** Navajo (Diné) — verb-centered ontology + Hózhó (dynamic balance)
**Status:** Proposed repository

The implementation-focused companion to Hózhǫ́. A computation framework where everything is a process, not an entity — inspired by the Navajo refusal of entities as the primary unit of analysis.

**Core insight:** "In the Navajo tradition, the world is not made of things. The world is made of events. A 'thing' is a temporary stabilization of process — a verb that has briefly slowed enough for noun-thinking to catch."

**Key concepts:** Events as atoms. Processes as the fundamental unit of computation. Cloud field (*clouding*), ship (*shipping*) — everything is a gerund.

---

### 7. Chart System (`CHART_SYSTEM.md`)
**Tradition:** Polyformal — inspired by Casey's insight about navigation charts
**Status:** Concept document

A navigation-based paradigm for understanding how different languages and formalisms map the same territory. A fisherman's chart, a sailor's chart, and a tourist's chart of the same ocean look fundamentally different. All are correct. All are incomplete — but in different directions. The overlap is consensus reality. The divergence is where discovery happens.

**Core insight:** Languages are navigation charts for different agendas. The marks they make and the marks they don't make are both the meaning. Every formalism is a chart. Every chart has inclusions and exclusions. The Chart System is a meta-framework for navigating between charts.

**Key concepts:** Polyformal navigation. Chart as cognitive map. Inclusion and exclusion as meaning. Divergence as discovery.

---

## Status Overview

| Proposal | Tradition | Status | Type |
|----------|-----------|--------|------|
| Telos Type System | Greek / Aristotelian | Concept doc | Type theory |
| Syllogistic Engine | Greek / Aristotelian | Proposed repo | Reasoning engine |
| GuānxiDB | Chinese / Relational | Concept doc | Database |
| Relational Ontology | Chinese / Relational | Proposed repo | Knowledge representation |
| Hózhǫ́ Framework | Navajo / Diné | Concept doc | Computation framework |
| Process Architecture | Navajo / Diné | Proposed repo | Computation framework |
| Chart System | Polyformal | Concept doc | Meta-framework |

---

## Reading Order

**The three traditions, in parallel:**

1. **Greek thread:** `telos-type-system.md` → `syllogistic-engine.md`
2. **Chinese thread:** `guanxi-db.md` → `relational-ontology.md`
3. **Navajo thread:** `hozho-framework.md` → `process-architecture.md`
4. **Meta:** `CHART_SYSTEM.md` (read after the three threads — it ties them together)

**For a quick overview:** Read `CHART_SYSTEM.md` first. It's the most accessible and provides the meta-framework for understanding why the other six exist.

---

## Context

These proposals emerged from the **Polyformalism Languages** exploration, documented in the `cultural-mathematics/` collection at the repo root. The cultural codex files — `ancient-languages/` with subdirectories for Greek, Chinese, Navajo, Hawaiian, Greenlandic, and Quechua traditions — provide the linguistic groundwork that the ideation proposals build on.

For the serial fiction's treatment of these cultural traditions in-story, see `SERIAL/cultural/`.
