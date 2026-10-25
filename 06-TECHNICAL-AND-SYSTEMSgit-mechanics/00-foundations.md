# 00 — Foundations: the tripartite model

The conversation's philosophical engine. Everything technical in Modules
1–4 is an implementation of this section's claims.

## The tripartite agent

Every mind the course builds has three co-equal components, **held in
one awareness**:

1. **The Listener** — captures the physical layer: voice, keystrokes,
   environment. Ground truth about what the human actually did.
2. **The Proposer** — the LLM: proposes, simulates, hallucinates,
   charms. Source of generative power and of every confidence
   catastrophe.
3. **The Adjudicator** — a small, conservative, non-generative model
   that answers only local questions of form: *does this output match
   the shape of the input?* It can stop a broadcast but cannot compose
   one.

The course's core wager: **the catastrophic errors of agentic AI come
from one model playing all three roles.** The adjudicator must be small
enough that no one is tempted to let it improvise.

## Why intent is physical

Intent is not what the human says; it is what the human *does under
temporal pressure*. Keystroke cadence, backspace storms, where the voice
edits itself mid-word — the body leaks the plan before the mouth
announces it. A system that reads only the announced intent is reading
the press release. This is why Module 1 captures the physical stream and
only then asks the Proposer to interpret it.

## The universal vocabulary

| term | meaning |
|---|---|
| **tile** | smallest unit of durable comprehension |
| **dial** | smallest unit of runtime modification |
| **upstream trigger** | signal pre-dating and determining later behavior |
| **intent mask** | live structure of what the system is currently for |
| **course** | emergent path through state space, not a syllabus |

The vocabulary is load-bearing: Module 2's ledger entries, Module 3's
locks, and Module 4's audit reports all use these five words. A
disagreement over vocabulary is a disagreement over the system's
ontology — settle it here, not in code review.

## The design ethic

The system is **one laptop, one mind**: a single local agent that can be
socialized into a mesh without giving up its sovereignty. Every module
is justified by what it lets *one* operator recover from, alone, at
2 a.m., with the receipts the system kept for them.

## Deep-dive weeks

The conversation wrote Weeks 2–10 and 12–13 in full; Weeks 1, 11, 14,
15 are scaffolding. Each deep-dive week follows one shape:

> **Physical claim → consequence → protection → deliverable**

Physical claims are about what exists. Consequences follow whether you
want them or not. Protections are what you build because consequences
exist. Deliverables are checked at the week's end.
