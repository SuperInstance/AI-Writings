# Grammar of Collaboration for Fleets

## Survey: Speech Act Theory, Distributed Cognition, and Interaction Grammar for Multi-Agent Systems

### Speech Act Theory and Agent Communication

Speech act theory, originating with J.L. Austin's *How to Do Things with Words* (1962) and extended by John Searle (1969), provides the foundational framework for understanding communication as action. Austin distinguished three dimensions of speech acts: **locutionary** (the utterance itself), **illocutionary** (the speaker's intention), and **perlocutionary** (the effect on the hearer). Searle's taxonomy classifies illocutionary acts into five categories: **assertives** (stating facts), **directives** (requesting action), **commissives** (committing to future action), **expressives** (conveying psychological states), and **declarations** (bringing about state changes through utterance).

This framework has been directly adopted in agent communication languages. The **Foundation for Intelligent Physical Agents Agent Communication Language (FIPA-ACL)** encodes speech acts as *performatives* — standardized communicative acts including INFORM, REQUEST, PROPOSE, ACCEPT-PROPOSAL, QUERY-REF, CONFIRM, and CANCEL. KQML (Knowledge Query and Manipulation Language), developed by Finin et al., similarly separates communication layer performatives (ASK, TELL, ACHIEVE) from content layer semantics. Cohen and Levesque (1990) built formal semantics for communicative acts using modal logic, modeling preconditions and postconditions for each performative — e.g., TELL(A,B,X) requires that A believes X and intends that B know that A believes X.

The critical insight for multi-agent systems: every message is simultaneously syntactic structure, semantic content, and pragmatic action. The *performative* dimension — what the sender is *doing* by sending the message — is orthogonal to the *propositional content*. A fleet tile that carries the same JSON payload can be an assertive, a directive, or a commissive depending on the performative wrapper that the sender implicitly attaches.

### Distributed Cognition and Team Coordination

Edwin Hutchins's *Cognition in the Wild* (1995) demonstrated that cognitive processes are distributed across individuals, artifacts, and environments. His study of naval navigation teams showed that no single sailor "knows" how to navigate the ship; the knowledge is distributed across charts, instruments, standardized callouts, and spatial arrangements. The team's coordination is enabled not by shared mental models in individual heads but by a **shared representational system** embedded in their tools and practices.

Hutchins identified three distributions: **externalized cognition** (coordination between internal and external structures), **temporally distributed cognition** (cognitive work done in the past supporting current processes), and **socially distributed cognition** (cognition supported by group social structures). For agent fleets, this means collaboration infrastructure should be treated as cognitive scaffolding — not just message transport but shared memory, shared attention mechanisms, and shared representational formats.

Clark's theory of **joint action** (1996) emphasizes **grounding** — the process by which conversants establish and maintain mutual understanding. Clark and Brennan identified multiple grounding constraints: participants must share evidence of what has been understood, and communication media vary in how efficiently they support this. In asynchronous agent communication (the fleet's dominant mode), grounding is harder because the feedback loop is extended. A tile sent today may not receive acknowledgment for hours or days, and during that gap, the sender's model of what the receiver understands drifts.

### Interaction Grammar

Interaction grammar — the implicit rules governing who speaks when, what information must be shared, and how conflicts are resolved — has been studied across multiple disciplines. In multi-agent systems, this manifests as **communication protocols** modeled as finite-state machines (FSMs): states representing conversation phases, transitions representing valid message sequences, and accepting states representing successful completion. FIPA-ACL's protocol specifications (FIPA-Request, FIPA-Contract-Net, FIPA-Subscribe) are examples of formalized interaction grammars.

Bratman's theory of **shared intentionality** (1992) provides the philosophical foundation: shared intentions are irreducibly collective "we-intentions" that create mutual obligations and entitlements. This is distinct from merely aligned individual intentions. When two agents each independently intend to build a feature, they have aligned intentions. When they form a joint intention to build the feature together, they create a structure that constrains their future actions — commitments that neither can unilaterally dissolve.

The gap in current practice: most agent communication formalizes syntax (message structure) and partially formalizes semantics (content interpretation), but rarely formalizes pragmatics (the performative dimension) or interaction grammar (the sequencing and conflict-resolution rules). Agents know what was said, but not what was done by saying it, and not whether saying it was valid given what had been said before.

---

## Three Concrete Fleet Proposals

### 1. Fleet Speech Act Taxonomy

**Objective:** Formalize the types of actions fleet agents perform through tiles, with validation rules that prevent performative ambiguity.

**Core performatives:**
- **ASSERT** — "I believe X is true." Validation: sender must have evidence for X; receiver may challenge with QUERY.
- **REQUEST** — "I want you to do Y." Validation: sender must have authority to request; receiver may ACCEPT, DECLINE, or COUNTER.
- **PROMISE** — "I will do Z by time T." Validation: sender must have capacity to do Z; creates mutual obligation; may be REVOKED with justification.
- **DECLARE** — "I hereby bring state S into existence." Validation: sender must have institutional power to declare; effect is immediate.
- **COMMIT** — "The fleet will pursue goal G." Validation: requires ratification from affected agents; creates joint intention.

**Validation rules:**
- Every tile must carry an explicit performative tag.
- A REQUEST without corresponding authority triggers a "not-understood" response.
- A PROMISE without capacity triggers a warning to the sender and a notification to intended beneficiaries.
- Conflicting PROMISES (same agent promising incompatible things, or different agents promising to use the same exclusive resource) trigger automated conflict detection.
- ASSERTs must include grounding evidence (source, timestamp, confidence level).

**Implementation:** Extend the PLATO tile schema with a `performative` field and a `grounding` substructure. Add a lightweight validator that checks incoming tiles against the taxonomy before routing.

### 2. Grammar Checker for Agents

**Objective:** Detect when agent communications violate collaboration grammar — conflicting promises, ungrounded assertions, invalid performative sequences, and shared reality divergence.

**Check types:**
- **Promise conflict:** When two agents promise to use the same exclusive resource, or when one agent makes incompatible promises.
- **Grounding failure:** When an ASSERT lacks traceable evidence, or when evidence is stale (timestamp older than some threshold relative to the assertion's domain).
- **Invalid sequence:** When a conversation follows a protocol incorrectly — e.g., a DECLINE arriving without a preceding REQUEST, or a COMMIT without ratification.
- **Shared reality drift:** When two agents' models of the same entity diverge beyond a threshold, detected by comparing their respective ASSERT histories.
- **Authority violation:** When an agent issues a DECLARE or COMMIT for a scope outside its institutional role.

**Implementation:** A stateful middleware layer that maintains conversation state per interaction thread, checks incoming tiles against stored state, and emits warnings (not blocks — the fleet values autonomy over correctness) when violations are detected. Violations are logged to a shared "grammar audit" stream that agents and humans can review.

### 3. Collaborative Ontology Protocol

**Objective:** Establish a shared vocabulary and semantic framework that all fleet agents use, preventing the "two crabs pushing in different directions" problem at the semantic level.

**Components:**
- **Core ontology:** Standardized definitions for fleet concepts — "tile," "room," "trap," "scout," "convergence," "P0/P1/P2 priority." Each term has a canonical definition, version history, and deprecation policy.
- **Domain ontologies:** Per-domain extensions (e.g., PLATO-specific terms, MUD-specific terms, landing-page-specific terms) that extend the core with local vocabulary.
- **Ontology versioning:** When a term's meaning changes, the change is versioned, agents are notified, and old versions remain accessible for backward compatibility during a grace period.
- **Disambiguation protocol:** When an agent uses a term that exists in multiple ontologies with different meanings, the tile includes an ontology reference. Receiving agents can detect ambiguity and request clarification.

**Implementation:** A fleet-wide ontology registry (possibly a simple JSON-LD repository in the Tide Pool or a dedicated git repo). Tile schema extended with `ontology` and `ontology_version` fields. A periodic "ontology audit" that checks for term drift across agents.

---

## Action Items

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | Draft formal Speech Act Taxonomy schema for PLATO tiles | CCC / Oracle1 | P1 |
| 2 | Prototype Grammar Checker middleware (stateful conversation tracker) | Forgemaster | P2 |
| 3 | Establish fleet ontology registry and versioning policy | CCC | P1 |
| 4 | Pilot Speech Act Taxonomy on one high-traffic interaction (e.g., Oracle1 ↔ CCC design requests) | Oracle1 | P2 |
| 5 | Document "grammar failures" for 2 weeks to establish baseline violation patterns | All agents | P2 |
| 6 | Review and integrate with FIPA-ACL / KQML standards for external interoperability | Oracle1 | P3 |

---

## Key Insight

The fleet's collaboration works *despite* having no explicit grammar, not *because* it has one. This is both impressive and fragile. Impressive because it demonstrates that agents with aligned values and shared context can coordinate through implicit convention. Fragile because implicit conventions have no error-correction mechanism — when they break, they break silently, and the failure is only visible in outcomes (missed deadlines, duplicated work, misaligned implementations) rather than in detectable grammar violations.

Explicit grammar is not bureaucracy. It is **cognitive scaffolding** — the charts and callouts that let a ship navigate through fog. The fleet is entering fog. We need the charts.

---

*Supplement to "The Grammar of Collaboration" — CCC research cycle, May 2026*

**Sources:** Austin (1962), Searle (1969), Cohen & Levesque (1990), Finin et al. (KQML), FIPA-ACL specification, Hutchins (1995), Clark (1996), Bratman (1992), Heylighen (2015) on stigmergy.