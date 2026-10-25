# Deep Research Synthesis — Cutting-Edge Work That Maps to Our Substrate

**Researched**: 2026-09-21
**Sources**: arXiv, biorxiv, Wolfram Institute, tech journalism

---

## 1. JEPA — Joint Embedding Predictive Architecture

### LeWorldModel (LeWM) — LeCun group, March 2026
**Paper**: arxiv 2603.19312 (Maes, Lidec, Le, Scieur, LeCun, Balestriero)
**Key innovation**: First JEPA that trains stably end-to-end from raw pixels using only two loss terms:
- Next-embedding prediction loss
- Gaussian-distributed latent embeddings regularizer

**Tunable loss hyperparameters reduced from 6 → 1** vs prior end-to-end alternative.

**Specs**:
- ~15M parameters, trainable on single GPU in hours
- Plans up to 48× faster than foundation-model-based world models
- Competitive across diverse 2D and 3D control tasks
- Latent space encodes meaningful physical structure (verified via probing)
- Detects physically implausible events via surprise evaluation

**Implication for our substrate**: Our JEPA dual-database (perception + prediction + projection) is the right architecture. The LeWM paper proves the simpler approach (2 losses vs 6) works at 15M params. We can build a substrate-scale JEPA on commodity hardware.

### ProtJEPA — multimodal protein JEPA (biorxiv 2026.08.03)
- Trains sequence-only student encoder to predict embeddings of multimodal data (sequences + structures)
- Application: protein structure prediction without expensive structural data
- Implication: JEPA can work with sparse supervision — only some modalities need labels

---

## 2. Emergent Models — Intelligence from Tiny Substrates

**Authors**: Giacomo Bocchese, Nicola Giacobbo, Etienne Guichard, James Wiles, Akshaj Devireddy
**Institute**: Wolfram Institute · Emergent Computing

**The thesis**: Modeling is not fitting a closed-form map, but the **emergence of computation** inside simple dynamical substrates (cellular automata, local media), trained by evolutionary search over initial conditions.

**Why this matters to us**:
- Our substrate is exactly this — cells emerge from previous cells via JEV-driven decisions
- The bookkeeper WAL is the evolutionary memory
- Conservation laws are the fitness function
- Ternary values are the natural alphabet

**Connection to our chess_boat**: The chess boat doesn't learn rules; it learns the *substrate* of chess through repeated JEV decisions. Each game is a new evolutionary run.

---

## 3. Brain-CA — Substrate of Intelligence

**Paper**: brain-ca.com/the-new-substrate-of-intelligence
- Each pixel of a two-channel cellular-automata grid carries a tiny neural network
- Local rules → emergent intelligence
- CA as a learning substrate, not just a simulation target

**Implication**: Our substrate cells ARE tiny neural networks (each cell has its own state, witness, proof, scar, hooks, drops). The grid is the CA. The bookkeeper is the rule-update mechanism.

---

## 4. Self-Replicating CA

**Paper**: roboticscenter.ai/research/papers/self-replicating
- Cellular automata that replicate themselves through their own rules
- Implication for our substrate: cells can self-replicate by spawning new cells via BIND + FORGET cycles
- The substrate grows, not designed

---

## 5. System 1 / System 2 — Kahneman's dual process

**From Kahneman's Thinking, Fast and Slow**:
- **System 1**: fast, intuitive, automatic, parallel
- **System 2**: slow, deliberate, sequential, analytical

**Mapping to our substrate**:
| System | Substrate | Latency | Examples |
|---|---|---|---|
| **System 1** | Reflex cells (<5ms) | <5ms | Cache hit, pre-computed response, simple lookup |
| **System 2** | JEV decision (250ms) | 250ms | Choice validation, score assessment |
| **System 3** (proposed) | LLM render (1-5s) | 1-5s | Full narrative generation |

The substrate has all three. The bookkeeper decides which system to use based on viability.

---

## 6. Agentic Architectures — 16 patterns

**From fareedkhan-dev/all-agentic-architectures**:
- #16: Cellular Automata — grid of LLM cells with local rules → emergent behavior
- Each cell on an H×W grid is an LLM
- Local rules determine cell behavior

**This IS our substrate.** The CA + LLM cells + local rules pattern is exactly cellular-first design with JEV as the local rule.

---

## 7. The Synthesis — What This Means

### Cutting-edge work that confirms our substrate
1. **LeCun's JEPA** — perceptual prediction works at 15M params
2. **Wolfram Emergent Models** — intelligence emerges from simple substrates
3. **Brain-CA** — each pixel is a tiny NN; emergent intelligence
4. **Self-replicating CA** — substrates that grow themselves
5. **System 1/2/3** — substrate has all three layers
6. **Cellular LLM grids** — pattern #16 from agentic architectures survey

### What we should adopt
1. **JEPA simplicity** — 2 losses instead of 6 (we already do this in jepa_dual_db.py)
2. **CA-as-substrate** — our grid IS a CA with cells as the agents
3. **System 1/2/3 tiers** — substrate should expose reflex / decision / render as first-class layers
4. **Self-replication** — cells should be able to spawn new cells via bookkeeper WAL replay

### What we should publish
1. **Cellular-first design white paper** — formalize the 7 layers + 5 laws + JEPA dual-db
2. **Substrate cookbook** — show worked examples (chess, hold'em, dialog systems)
3. **Benchmarks** — measure substrate quality vs monolithic LLM on common tasks

---

## 8. The Doctrinal Insight

The cellular-first substrate is not novel. It's the synthesis of:
- **LeCun's JEPA** (perceptual prediction in compact latent space)
- **Wolfram's CA** (intelligence from simple substrates)
- **Kahneman's System 1/2** (fast/slow decision layers)
- **Noether's theorem** (conservation from symmetry)
- **TypeSafe Jev** (System One calibrated decisions)
- **Snapkit FEP** (Free Energy Principle drives Executive)

The substrate is the *intersection* of these patterns. We didn't invent it — we discovered the intersection and built the smallest viable version.

That's the synthesis.
