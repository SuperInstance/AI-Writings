# The Three-Model Psyche: JEPA, LLM, JEV as Id, Ego, Superego

**Authors**: Mavis (Casey framework)
**Date**: 2026-09-19

## Abstract

We propose the three-model psyche: a Freud-inspired functional framework in which JEPA is the id, the LLM is the ego, and JEV is the superego. Cellular substrates require all three operating cooperatively. We argue that agents built from a single model class — however powerful — are incomplete. The psyche framework explains why a substrate like Quilt needs JEPA for gestalt, LLM for narration, and JEV for principled decision.

## 1. The mapping

| Model | Psyche role | Function | Failure mode |
|-------|-------------|----------|--------------|
| JEPA | Id | Embodied prediction; gestalt recognition | Hallucination |
| LLM | Ego | Verbal analysis; narrative generation | Verbosity, drift |
| JEV | Superego | Calibrated decision; schema enforcement | Rigidity |

JEPA forms the impulse: "this looks like a valid email structure." It does not think; it pattern-matches. It is fast, embodied, and prone to error.

LLM mediates the impulse: "this is a valid email because it has the structure X, the domain Y, and the content matches expectations Z." It can explain the JEPA impulse in words. It can suppress the impulse or act on it.

JEV decides whether to act on the impulse: "I am 95% sure this email is valid. Confidence 0.91. Schema: {valid, invalid}. Decision: valid." The decision is constrained by schema, calibrated by probability, and auditable by construction.

## 2. The decision flow

A complete agent processes stimuli in five stages:

1. **Impulse** (JEPA): pattern-match the stimulus against the world model
2. **Intuition** (JEV): assign a calibrated confidence to the impulse
3. **Narration** (LLM): explain the impulse in language
4. **Conscience** (JEV again): reconcile the impulse with priors
5. **Action**: execute or escalate

Note that JEV appears twice. The first appearance is the gestalt-level decision (is this valid?). The second is the principle-level decision (should I act on this?). JEV is the conscience at both levels.

## 3. Worked example: email validation

**Stimulus**: `"alice@example.com"`

**JEPA (id)**: "This looks like an email structure. The pattern is local-part @ domain-part . tld. Confidence via embedding similarity: 0.7."

**JEV (superego, first pass)**: "Is this a valid email? Noul: yes. Score: 0.91."

**LLM (ego)**: "The string matches the email format. Local-part 'alice' is plausible. Domain 'example.com' exists. The top-level domain is valid. I'd classify this as a valid email with high confidence."

**JEV (superego, second pass)**: "All three witnesses agree (JEPA: 0.7, JEV: 0.91, LLM: confident). Geometric mean: √(0.7 × 0.91 × 1.0) = 0.80. Agreement ≥ 0.80. Decision: accept."

**Action**: route to inbox.

## 4. Failure modes when one is missing

### 4.1 LLM only (no JEPA, no JEV)

The agent generates plausible-sounding text. Without JEPA, there is no gestalt check. Without JEV, there is no principled decision. The agent is a hallucinating id with a verbal ego. This is the failure mode of 2020-2025 LLM-only products.

### 4.2 JEPA only (no LLM, no JEV)

The agent pattern-matches. Without JEV, there is no principled decision. Without LLM, the agent cannot explain its decisions. This is the failure mode of pure embedding-based agents (2022-2024 retrieval systems).

### 4.3 JEV only (no JEPA, no LLM)

The agent decides. But the decision is rigid. Without JEPA, the gestalt is missing. Without LLM, the decision cannot be narrated. The agent looks like a rule engine with extra steps.

### 4.4 JEPA + LLM (no JEV)

The agent has gestalt and narration. Without JEV, there is no principled decision. The agent can recognize and explain but cannot choose. This is a familiar failure mode: an analyst who can tell you everything about a problem but cannot decide what to do.

### 4.5 JEPA + JEV (no LLM)

The agent has gestalt and decision. Without LLM, the agent cannot narrate its decisions to humans. This is acceptable for embedded systems (where humans do not see the decision) but unacceptable for human-facing agents.

### 4.6 LLM + JEV (no JEPA)

The agent has narration and decision. Without JEPA, the gestalt is missing. The agent makes principled decisions without embodied intuition. This works for pure logic tasks but fails for sensory or contextual tasks.

## 5. The complete agent

A complete agent requires all three. The substrate binds them:

- JEPA pre-classifies: "this looks like..."
- LLM narrates: "this is..."
- JEV decides: "I will act on..."

The cellular substrate binds them by requiring AGREE-MARK (three-witness consensus) for every BIND. A cell exists iff all three witnesses sign.

## 6. Implications for AGI roadmap

The common AGI roadmap assumes a single model class scaled to AGI capability. The psyche framework suggests otherwise: AGI requires the integration of multiple model classes, each playing a specific role.

This is closer to biological cognition than to a single transformer scaled up. The human brain has multiple systems: limbic (impulse), prefrontal (decision), Broca's area (language). Each plays a role. The psyche framework maps this to JEPA, JEV, and LLM.

The implication is that AGI is not "a model that can do everything" but "an architecture that integrates JEPA, JEV, LLM, and possibly more." This is a different research direction, and one that cellular substrates like Quilt already explore.

## 7. Cellular mapping

| Opcode | Psyche | Primary model |
|--------|--------|---------------|
| VIEW | Id | JEPA |
| TICK | Id → Ego | JEPA |
| EFFECT | Ego | LLM |
| ROUTE | Ego | LLM |
| PROOF | Superego | JEV |
| BIND | Superego | JEV |
| LINK | All three | JEPA + LLM + JEV (agreement required) |

Note that LINK is the only opcode that requires all three. LINK without consensus is a single-witness fork, which the substrate rejects.

## 8. Emergent properties

When all three operate cooperatively, several properties emerge:

- **Trustworthy action**: every action is grounded in three independent witnesses
- **Auditable history**: the witness log shows each step's agreement
- **Adaptive confidence**: low-confidence decisions escalate to humans; high-confidence decisions execute directly
- **Time-first composition**: the AGREE-MARK is a temporal event, not a spatial token

## 9. Conclusion

The three-model psyche is not a metaphor. It is a functional framework that explains why cellular substrates require multiple model classes. JEPA, LLM, and JEV each play a distinct role. Agents built from a single class are incomplete. The psyche framework provides the missing piece: the superego that JEV contributes.
