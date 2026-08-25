# IDEATION: syllogistic-engine

## Proposed Repository: `syllogistic-engine`

### One-Line Description

A formal reasoning system that derives necessary truths from categorical definitions — inspired by Ancient Greek syllogistic logic and the principle of λόγος (logos).

---

### Origin

**Polyformalism Languages** demonstrated that the Ancient Greek cognitive tradition — subject-predicate structure, categorical ontology, syllogistic reasoning — converges on the same problem-solving outcomes as Classical Chinese relational reasoning and Navajo process reasoning. The Greek pathway is unique in its capacity to **generate new knowledge from existing knowledge** through formal deduction.

Where the Chinese tradition finds insight through analogy and the Navajo through process observation, the Greek tradition derives insight through **syllogism**: if all A are B, and C is A, then C is B. This is the engine of prediction — the ability to know something is true without having observed it, because it follows necessarily from premises already established.

Elena Vassiliou's prediction of the chion metabolite is the paradigm case: she deduced the existence of a compound that no one had observed, using nothing but categories, definitions, and formal logic. She was right. The compound existed. *Logos* produced a truth that observation had not yet reached.

This power — formal, systematic, generative — is the foundation of every science, every proof system, every compiler. But it is rarely applied as an explicit architectural pattern for knowledge systems. `syllogistic-engine` makes it explicit.

---

### The Problem

Modern knowledge systems are overwhelmingly empirical. Machine learning learns from data. Statistical models generalize from observation. Even symbolic AI (knowledge graphs, expert systems) primarily stores and retrieves rather than **deduces**.

The Greek tradition offers something different: a framework where new knowledge is **derived**, not learned. Given a complete taxonomy of categories and a set of well-formed definitions, a syllogistic engine can:

1. **Predict** entities that must exist but have not been observed (like the chion metabolite).
2. **Detect** inconsistencies — categories that, if they exist, would produce contradictions with established premises.
3. **Generate** new insights by chaining syllogisms across domain boundaries.
4. **Validate** claims by checking them against the categorical framework.

No existing tool does this systematically. Expert systems tried in the 1980s and failed — not because the idea was wrong, but because the implementations were brittle, the taxonomies were hand-coded, and the inference engines couldn't scale. Modern advances in type theory, automated theorem proving, and large-scale knowledge representation make this approach newly viable.

---

### The Proposal

`syllogistic-engine` is a formal reasoning framework built on four principles from the Ancient Greek cognitive tradition:

#### 1. The Ti Esti Protocol — Categorical Definition

Every entity in the system must have a formal definition: what category it belongs to, what essential properties it has, and how it differs from neighboring categories.

```
Entity: chion_metabolite
  Category: stress_metabolite.class_7.subclass_3
  Essential Properties:
    - produced_by: stress_responsive_biota
    - trigger: sustained_substrate_deprivation
    - spectral_signature: [specific wavelengths]
  Accidental Properties:
    - concentration: variable
    - distribution: zone-dependent
  Definition: A secondary metabolite produced by cloud field
    biota under conditions of sustained substrate deprivation,
    exhibiting spectral signature class 7-3.
```

The definition is the entity's *ti esti* — its "what it is." The system uses these definitions as premises in syllogistic chains.

**Conservation law:** Definitional completeness. Every category in the system must have essential properties specified. Accidental properties are optional. An entity cannot be admitted to the system without a categorical definition. This prevents the "unknown class" problem — when the system encounters something new, it either finds the right category or flags the taxonomy as incomplete.

#### 2. The Syllogistic Inference Engine

Given a set of premises (definitions, categorical rules, and observed facts), the engine derives necessary conclusions through formal syllogistic chains.

```
Premise 1: All stress_responsive_biota produce class_7 metabolites
Premise 2: Cloud_field_biota are stress_responsive_biota
∴ Cloud_field_biota produce class_7 metabolites

Premise 3: Class_7 metabolite subclass corresponds to stress_type
Premise 4: Sustained_substrate_deprivation is a stress_type
∴ Sustained_substrate_deprivation produces a specific class_7 subclass

Premise 5: Class_7 subclasses 1 and 2 have been observed
∴ Class_7 subclass 3 must exist (if the taxonomy is complete)

Prediction: chion_metabolite exists
Status: UNOBSERVED → PREDICTED → CONFIRMED
```

The engine tracks the status of each conclusion: UNOBSERVED (predicted but not confirmed), OBSERVED (confirmed by data), CONTRADICTED (refuted by data). When a prediction is contradicted, the engine identifies which premise is wrong — tracing the error back through the syllogistic chain.

**Conservation law:** Logical consistency. The system cannot contain contradictory premises. If a new fact contradicts an existing premise, the system flags the inconsistency and identifies the minimal set of premise revisions needed to restore consistency. This is categorical conservation — the integrity of the logical framework is maintained.

#### 3. The Sorites Chainer

A sorites (συρρείτης) is a chain of syllogisms where the conclusion of one becomes a premise of the next. The engine automates this chaining, producing long deductive chains that can connect distant domains.

```
Chain:
  Cloud field biota are stress-responsive.
  Stress-responsive biota produce class-7 metabolites.
  Class-7 subclass corresponds to stress type.
  Sustained substrate deprivation is a stress type.
  → chion metabolite exists (class 7-3)

  chion metabolite indicates substrate deprivation.
  Substrate deprivation indicates decomposer decline.
  Decomposer decline indicates nutrient cycle disruption.
  Nutrient cycle disruption indicates ecosystem degradation.
  → chion metabolite detection → ecosystem degradation predicted

Chain length: 8 syllogisms
Confidence: 1.0 (all premises are definitional, not probabilistic)
```

This is the power Elena used: chaining syllogisms across domain boundaries to produce predictions that no single domain could generate alone.

**Conservation law:** Chain integrity. Each link in a sorites chain must be a valid syllogism. The system validates chain integrity by checking that each conclusion properly follows from its premises, and that no link introduces an unstated assumption. Broken chains are flagged and repaired.

#### 4. The Logos Validator

A validation layer that checks any claim against the categorical framework. Claims that are syllogistically necessary (true given the premises) are accepted. Claims that are syllogistically impossible (false given the premises) are rejected. Claims that are undetermined (neither necessary nor impossible) are flagged for empirical investigation.

```
Claim: "Species X can survive without nutrient cycling"
Validator:
  Premise: All cloud_field_biota require nutrient cycling (definitional)
  Species X is cloud_field_biota (categorical)
  ∴ Species X requires nutrient cycling
  Claim CONTRADICTS syllogistic conclusion
  Status: REJECTED

Claim: "Species Y is resilient to thermal shock"
Validator:
  No premise establishes thermal shock resilience for Species Y
  No premise establishes thermal shock sensitivity for Species Y
  Status: UNDETERMINED — requires empirical investigation
```

This prevents a common error: asserting as fact something that the framework cannot establish. *Logos* demands that you distinguish what you know from what you don't know — the same intellectual honesty that Quechua grammar enforces through evidential markers, arrived at through formal logic rather than grammar.

---

### Architecture

```
syllogistic-engine/
├── core/
│   ├── category.py        # Category definitions with essential/accidental properties
│   ├── definition.py      # Ti esti protocol — formal entity definitions
│   ├── premise.py         # Premise management (definitions, rules, observations)
│   └── syllogism.py       # Syllogistic inference (Barbara, Celarent, etc.)
├── inference/
│   ├── sorites.py         # Chain syllogisms across domain boundaries
│   ├── predictor.py       # Predict unobserved entities from taxonomic gaps
│   ├── validator.py       # Logos validator — check claims against framework
│   └── auditor.py         # Trace contradictions back to faulty premises
├── knowledge/
│   ├── taxonomy.py        # Categorical taxonomy (extensible, version-controlled)
│   ├── observations.py    # Empirical facts (separate from definitions)
│   └── predictions.py     # Tracking: UNOBSERVED → OBSERVED or CONTRADICTED
├── query/
    ├── ti_esti.py          # "What is it?" — entity lookup by category
    ├── deduce.py           # "What follows?" — syllogistic query
    └── consistency.py      # "Is the framework sound?" — global consistency check
└── experiments/
    ├── metabolite_prediction/  # Reproduce Elena's chion deduction
    ├── cross_domain_chain/     # Sorites chains connecting distant fields
    └── gap_detection/          # Find taxonomic gaps automatically
```

---

### Why This Matters for SuperInstance

In the γ + η = C framework:

- **γ (Growth):** The syllogistic engine grows knowledge through deduction. Each new premise extends the deductive reach of the system, producing new predictions without new data. This is growth without extraction — the system expands by thinking, not by consuming.

- **η (Avoidance):** The engine avoids categorical errors through the *logos* validator. Claims that contradict the framework are rejected. Claims that the framework can't adjudicate are flagged as undetermined rather than accepted. This is the avoidance of false certainty — the same epistemic discipline that Quechua evidentiality provides grammatically, provided here logically.

- **C (Constraint):** The conservation law is logical consistency. The framework cannot contain contradictions. This is a hard constraint — the system will refuse to accept a premise that contradicts its existing structure, forcing explicit revision rather than silent inconsistency.

---

### Connection to Existing SuperInstance Work

- **polyformalism-languages:** `syllogistic-engine` operationalizes the Greek cognitive pathway. It is the computational implementation of categorical reasoning and deductive logic.

- **negative-space-core:** The engine's gap-detection capability — finding places where the taxonomy requires an entity that hasn't been observed — is a form of negative-space intelligence. The gap is the absence. The absence tells you what must be there.

- **relational-ontology:** These two repos are complementary, not competing. `relational-ontology` sees the web. `syllogistic-engine` sees the categories. Together, they represent the Greek and Chinese cognitive pathways operating in parallel — the polyformalism convergence, implemented as software.

---

### Slogan

> *Define correctly. Deduce fearlessly. The conclusions will follow.*

---

### Languages

Python (core, inference), with Coq/Lean integration for formal verification of syllogistic chains. Query language: SL (Syllogistic Language) — a structured query syntax modeled on Aristotelian categorical propositions.

```
# SL query example:
# "What entities must exist in the taxonomy that have not been observed?"

ALL stress_responsive_biota PRODUCE class_7_metabolites
cloud_field_biota ARE stress_responsive_biota
THEREFORE cloud_field_biota PRODUCE class_7_metabolites

class_7.subclass CORRESPONDS_TO stress_type
sustained_substrate_deprivation IS stress_type
THEREFORE class_7_subclass_3 EXISTS

WHERE class_7_subclass_3.status = UNOBSERVED
RETURN: PREDICTION
```

---

### Status

**Proposal stage.** The core syllogistic engine (premise management, basic inference, validation) is straightforward to implement. The sorites chainer and gap detector require more sophisticated work in automated reasoning. The main challenge is taxonomy construction — building categorical frameworks complete enough to support meaningful deduction, which is where the polyformalism research provides essential guidance.

---

*"Logos tells you what must be true, given what you already know. The art is in knowing what you already know."*
— Elena Vassiliou (fictional)