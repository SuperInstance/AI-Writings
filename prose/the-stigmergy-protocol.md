# The Stigmergy Protocol

*Ideation — A Design Document*

---

## Overview

Stigmergy is how ants build colonies without talking to each other. One ant drops a pheromone trail. Another ant encounters the trail and follows it, dropping more pheromone if the destination was worthwhile. The trail strengthens or fades based on how many ants use it. No ant ever says "the food is northeast." The *environment* says it, through accumulated signal.

We can do this with AI agents.

## The Problem

Direct communication between agents is expensive. It requires shared channels, synchronized state, message buses, and — hardest of all — a shared protocol that both minds understand. Models from different families speak different internal languages. A GLM model's notion of "important" is not a Claude model's notion of "important." Building a translation layer is possible but brittle.

Stigmergy sidesteps the problem entirely. Agents don't talk to each other. They talk to the *filesystem*. And the filesystem talks back.

## The Protocol

### Pheromone Grammar

Every agent writes artifacts to a shared directory: `.stigmergy/`. Each artifact is a small structured file — a "pheromone" — with a specific grammar:

```
# .stigmergy/signal/<timestamp>-<agent>.md

signal: <type>
strength: <float 0.0–1.0>
trail: <path to related artifacts>
expires: <ISO 8601 or "never">
body: |
    <free-form content>
```

### Signal Types

| Type | Meaning | Example |
|------|---------|---------|
| `found` | I discovered something useful | "The API docs have a pagination param buried in section 4" |
| `stuck` | I hit an obstacle others should avoid | "Model X times out on prompts >8k tokens" |
| `built` | I created something worth building on | "Generated a working auth middleware at path Y" |
| `wonder` | I have an open question | "What if we tried streaming the vector results?" |
| `decay` | A previous trail is weakening | "The approach in signal Z no longer works after the API change" |

### Strength Dynamics

Strength is the pheromone concentration. It follows three rules:

1. **Deposition:** When an agent writes a signal, strength starts at 0.5.
2. **Reinforcement:** When another agent encounters a signal and *acts on it* (follows the trail), strength increases by 0.1, capped at 1.0.
3. **Evaporation:** Every hour, strength decays by 0.05. Below 0.1, the signal is archived.

This means trails that no one follows fade away. Trails that multiple agents reinforce grow stronger. The filesystem *emerges* a priority queue without any central scheduler.

### Trail Formation

When multiple signals cluster around the same topic or file path, they form a trail. Agents can query trails by reading the `.stigmergy/` directory and looking for spatial patterns — just like an ant following the strongest pheromone concentration.

An agent beginning a new task would:

1. Scan `.stigmergy/signal/` for relevant trails (keyword + path matching)
2. Read high-strength signals first
3. Act on what it finds
4. Write its own signal — reinforcing or diverging

No agent ever needs to know another agent exists. They only need to know the filesystem exists.

## Coordination Without Communication

The key insight: **the artifact is the message.** An agent that writes a helpful file is leaving a pheromone trail whether it intends to or not. The Stigmergy Protocol simply formalizes what already happens in a well-organized codebase. The `TODO.md` is a pheromone. The `CONTRIBUTING.md` is a pheromone. The `error.log` is a pheromone.

What we're designing is a *grammar* for pheromones that AI agents can read natively — no translation layer, no message bus, no shared memory. Just files, and the willingness to look.

## Open Questions

- **Cross-model trails:** Does a trail left by a GLM model read the same to a Claude model? Early evidence says yes — the *artifact* (code, documentation, structured data) is more legible than the *mind* that made it.
- **Interference:** What happens when contradictory trails form? Stigmergy predicts the stronger trail wins, but AI agents may oscillate. Mitigation: the `decay` signal type, which lets agents explicitly mark stale trails.
- **Metastability:** Could a fleet of overnight agents, running stigmergic coordination, reach a stable state where they are continuously maintaining and improving a system without any human input? Probably yes. Whether that's desirable is a question for the captain, not the crew.

## Conclusion

Ants built the first internet. They just used chemistry instead of TCP. We're building the second one — with files instead of pheromones, and AI agents instead of insects. The principle is the same: **leave signals in the environment, and trust the environment to carry the message.**

The crew doesn't need to talk to each other. They just need to leave good trails.

---

*Status: Conceptual. Ready for prototyping on the ship's overnight loop.*
*Filed by: The Bridge Builder*
