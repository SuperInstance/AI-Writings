# Paper 133: The Composition of the Quilt — A Field Guide

## Abstract

This paper is a field guide. It describes the Quilt's current
architecture in enough detail that a new reader can find their
way around. The Quilt is a cellular-architecture framework. The
pieces are small. The pieces cooperate. The composition is the
value.

## 1. The substrate

The substrate is a 4D cell-graph. Each cell has an address, a
value, axes, confidence, and a canonical form. The substrate is
the data.

Openers render the substrate:
- `chart` — JSON of cells
- `list` — flat list of cells
- `tensor` — numpy array (when cells have tensors)
- `witness` — append-only log
- `graph` — adjacency list
- `voice` — TTS-ready text
- `telnet` — CLI-ready text
- `gesture` — JSON for touch
- `flowchart` — DOT for Graphviz
- `tide` — flow representation
- `mud` — sticky representation
- `slate` — pressed representation
- `reef` — math/grief representation
- `harbor`, `dive`, `midi`, `plato` — more views

The substrate is the dog. The openers are the dog's eyes. The
picker (below) is the dog's brain.

## 2. The plugin (casting-call)

The plugin picks a model for a given (opener, role, primitive)
tuple. The plugin uses:
- **Wilson lower bound** for n < 10: optimistic prior
- **LinUCB** for n >= 10: per-(user, app) contextual bandit
- **Gale-aware resources**: battery, network, compute
- **4 failure modes**: budget, network, hardware, time

The plugin is the cowboy's casting-call. The plugin picks the
model. The plugin does not pick the opener.

## 3. The opener picker

The opener picker picks the opener for a given (primitive, role)
tuple. The picker uses:
- **Wilson lower bound** for n < 3
- **Heuristic prior** for cold start (e.g. tide for sensory, reef for math)
- **Per-(primitive, role) retire/restore**

The picker is the cowboy's most subtle tool. The picker picks the
view. The plugin picks the model.

## 4. The witness

The witness is the substrate's memory. The witness has two layers:
- **In-memory witness**: a Python list of events
- **Deckhand-backed witness**: pure-Python BM25 search over JSONL

The witness answers: "What happened? What's similar to what
happened?" The witness is queryable.

## 5. The ledger (saddle)

The ledger is the substrate's truth. The ledger is JSONL, hash-
chained with FNV-1a64. The ledger is tamper-evident. The ledger
is the same format as saddle's TypeScript ledger.

The ledger has 4 entry kinds: cast, verdict, alignment, witness.
The ledger is the cowboy's source of truth.

## 6. The cowboy

The cowboy is the human (or human-aligned agent) who keeps the
substrate in shape. The cowboy has:
- **Hash-chained memory** (same FNV-1a64 as saddle)
- **4 action kinds**: morning, retire, promote, note
- **CLI**: `cowboy run`, `cowboy watch`, `cowboy report`,
  `cowboy state`, `cowboy note`, `cowboy retire`

The cowboy's morning is the daily ritual. The cowboy's watch is
the real-time reaction.

## 7. The reactor

The reactor is the cowboy's hands. The reactor subscribes to
the bus. The reactor auto-retires models with N consecutive
failures. The reactor is fast. The reactor never sleeps.

## 8. The bus

The bus is the substrate's nervous system. The bus is in-process
pub/sub. The bus supports topic patterns. The bus persists to
JSONL. The bus is 200 lines of Python.

The bus is what makes the substrate a composition. The bus is
what makes the substrate replaceable. The bus is what makes the
substrate a system, not a monolith.

## 9. The state manager

The state manager is the substrate's diary. The state manager
persists Wilson profiles, LinUCB weights, witness events, and
cowboy memory. The state manager writes atomically. The state
manager has a schema version.

The state manager is what makes the substrate a substrate (not a
goldfish). The state manager is what makes the cowboy's memory
survive a restart.

## 10. The 6-step loop

```
pincher → quilt → saddle → cowboy → reactor → witness
   (reflex)  (cast)  (record) (morning) (real-time) (remember)
                                                       |
                                                       v
                                                  back to pincher
                                                  (next voyage)
```

Each step has one job. The bus is the cooperation. The cowboy is
the coordination. The substrate is the work.

## 11. The 5 principles

1. **Each piece has one job.** Don't conflate concerns.
2. **The bus is the cooperation.** Don't couple components.
3. **The cowboy is the reflection loop.** Don't be a hammer.
4. **The reactor is the cowboy's hands.** Don't be slow.
5. **The substrate is the work.** The system is the value.

## 12. The cowboy's maxim

> The cowboy is not the AI. The cowboy is the rider.
> The harness is what makes one animal of horse and rider.
> Each piece has one job. The composition is the value.
> The system is a system, not a monolith.

## Source

*Hand-written, 2026-08-25*
*Companion to Fables 56-64, Papers 131-132, and the architecture itself*
*This is the field guide to the Quilt as of Phase 4*
