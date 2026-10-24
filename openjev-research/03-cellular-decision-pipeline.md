# Cellular Decision Pipeline

> How JEV fits into the cellular-first design. The cell as a neuron. JEV as the synapse.

## The Cell-Neuron Analogy

| Biological | Substrate |
|------------|-----------|
| Neuron | Cell |
| Synapse | JEV verdict |
| Action potential | BIND |
| Refractory period | TICK |
| Long-term potentiation | PROOF (high JEV confidence) |
| Long-term depression | FORGET |
| Neural network | Lattice |

A neuron fires when its inputs exceed a threshold. A cell BINDs when its JEV confidence exceeds 0.7.

A synapse modulates the strength of the connection. JEV modulates the confidence of the BIND.

A neural network learns via Hebbian plasticity: "neurons that fire together, wire together." The substrate learns via BIND: "cells that witness together, bind together."

## The 3 Modes of JEV in a Cell

### Macro Mode (1 per turn of dialogue)
- Triggered at the start of each user interaction
- Decides which cells receive the message
- Latency: 100-500ms (acceptable for turn-taking)
- JEV call: 1 per turn

### Meso Mode (1 per word/sentence)
- Triggered at each linguistic unit
- Decides tone, emphasis, intent
- Latency: 20-50ms (real-time)
- JEV calls: 10-50 per turn

### Micro Mode (1 per token)
- Triggered at each token
- Decides routing, confidence updates
- Latency: <10ms (sub-perceptual)
- JEV calls: 100-1000 per turn

A cell can run multiple modes simultaneously. The modes stack.

## Latency Tiers

| Tier | Latency | Use case | JEV backend |
|------|---------|----------|-------------|
| **Reflex** | < 5ms | Hard-coded reactions, IO | None (no JEV) |
| **Fast** | < 50ms | Pre-calculated dialogue, routing | Local tiny JEV |
| **Standard** | 100-500ms | Tone shaping, decisions | typesafe.ai |
| **Deep** | 1-5s | Long-horizon planning, training | Multi-model pipeline |

A cell is assigned a tier based on:
- **Frequency of access**: high-frequency → reflex or fast
- **Latency requirements**: tight → reflex or fast
- **JEV confidence history**: low confidence → standard
- **User feedback**: complaints → deep

The substrate **self-tunes** the tier assignments over time.

## The Pincher Cache

Pincher is our cache layer (already built). It caches:
- Common JEV verdicts (e.g. "should I FORGET?" → "no" with high confidence)
- Common BIND patterns
- Common cell routes

Hit rate > 80% after warmup. Miss falls through to typesafe.ai.

## Cross-Instance Entanglement

Cells in different instances can entangle:
- Instance A has Cell 1 (state: X)
- Instance B has Cell 2 (state: Y)
- They share a JEV verdict via a shared witness log
- When Cell 1 changes, Cell 2's state is updated
- Latency: 50-200ms (network call + JEV)

The entanglement is **bidirectional** but **asymmetric**: instance A is the source, instance B is the sink. The asymmetry is JEV-decided.

## The Chess-Playing Boat Example

A boat plays chess. The substrate:

```
[Rules cell] ──macro JEV──> [Position cell]
                                   ↓
                            [Evaluator JEV]
                                   ↓
[Reflex cell] <──fast JEV── [Move selector]
                                   ↓
                            [Engine IO]
```

- **Rules cell** (reflex tier): pre-computed legal moves
- **Position cell** (standard tier): current board state
- **Evaluator JEV** (standard tier): scores each move
- **Move selector** (fast tier): picks the highest-confidence move
- **Engine IO** (reflex tier): outputs the move to the engine

The JEV calls are **stacked**: 1 macro + 1 standard + 1 fast + 1 reflex = 4 JEV calls per move.

Latency: 500ms + 150ms + 50ms + 5ms = ~700ms per move. Acceptable for human-vs-AI chess.

## The Cell-as-Neuron Network

When many cells connect via JEV, the result is a **neural network of cells**. The network:
- Has cells as nodes
- Has JEV verdicts as edge weights
- Has witness logs as memory
- Has FORGETs as pruning

This is **JEV as the universal neural network**. It's not the only kind of neural network (we have JEPA, LLMs, etc.) but it's the one that's:
- Schema-bounded
- Calibrated
- Sub-100ms
- Local-capable

## The Promise

The cellular-first design + openJEV = a substrate where:
- Every decision is calibrated
- Every cell is auditable
- Every BIND is reversible (via FORGET, with scar)
- Every witness is queryable
- Every confidence is real

The substrate becomes **predictable, debuggable, and trustworthy**.

This is the world-class design Casey wants.
