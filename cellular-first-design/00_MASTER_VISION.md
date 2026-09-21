# Cellular-First Design — World-Class Architecture

> A design that works with spreadsheets of any program via plugins AND as backend logic in a model-sense.

## The Thesis

The cell is the irreducible unit. Cells are not data structures — they are **neurons of any system**. They can be:

- **Weights** in a neural network
- **Logic tiles** in a spreadsheet
- **IO cells** in a frontend
- **Other instances** outside the quilt
- **Robotic actuators** in a physical system

JEV is the validator. JEPA is the predictor. **If JEV could be tiny and local**, it would be how the neural network of anything — from weights to logic tiles to IO cells — connects.

## The 7 Layers of the Cellular-First Design

### Layer 1: The Cell Itself
A cell has:
- **State** (a vector + a witness log)
- **Type** (what kind of data it outputs)
- **Hooks** (where it gets inputs from)
- **Drops** (where it sends outputs to)
- **JEV confidence** (a real number, calibrated)

Cells compose via BIND. Cells witness via PROOF. Cells forget via FORGET. Cells tick via TICK.

### Layer 2: The Spreadsheet Plugin
Every cell can be **addressed as a spreadsheet cell** (e.g. `A1`, `B2`).

- A spreadsheet plugin maps cells to coordinates
- The plugin watches the cells' state vectors
- When state changes, the spreadsheet updates
- When the spreadsheet is edited, the cell's state is updated

This means: **the substrate IS a spreadsheet**, and a spreadsheet IS the substrate.

### Layer 3: The Model-Sense Backend
Cells don't just hold data. They **make decisions**.

A cell can be:
- A percentage chance of pulling from a decision tree
- A similarity score against a vector DB
- A routing decision (which cell to send a message to)
- A tone shaper for a fractal inference tree

A cell can be **pre-calculated** — its next state is already known for the next N steps.

This is critical for **NPC dialogue** and **voice agents** where latency must be < 100ms.

### Layer 4: The OpenJEV Model
**JEV as the universal cell connector.**

```
Cell A: state + JEV confidence  ──JEV verdict──> Cell B: receives + tick
```

JEV decides:
- Which cell receives the message
- How much weight to give each cell
- Whether to BIND, FORGET, or WITNESS the event
- How to tone the message

JEV runs at multiple granularities:
- **Macro** (one JEV call per turn of dialogue)
- **Meso** (one JEV call per word/sentence)
- **Micro** (one JEV call per token — used for routing)

### Layer 5: The Thinking Models
**JEV and JEPA are the senses. Thinking models are the mind.**

When the user says something, multiple thinking models wake up:
- JEPA predicts what comes next
- JEV validates the prediction
- LLM narrates the result
- Other cells react to the delta

The user can **hedge and nudge** the thinking direction. Each nudge shifts the JEV confidence. The cells re-route.

### Layer 6: The Reflexes
**Some cells go to reflexes. Others go to thinking logic. Others go to Pincher.**

- **Reflex cells**: < 5ms response time. Direct IO. Hard-coded reactions.
- **Thinking cells**: 100-500ms response time. JEPA + JEV. Calibration happens here.
- **Pincher cells**: cached responses. Hit rate > 80% after warmup.

The split is automatic. The substrate decides which cells are which based on:
- Frequency of access
- Latency requirements
- User feedback
- JEV confidence history

### Layer 7: The Cross-Instance Fabric
**Cells live in multiple instances. They entangle.**

When Cell A in instance 1 sends a value to Cell B in instance 2:
1. JEV decides the route (might go through 3-7 hops)
2. The value is signed with the witness log
3. The receiving cell hooks the value + delta
4. The receiving cell's **bookkeeper wakes up**
5. The bookkeeper runs a process: validate, store, propagate

This is how the substrate scales across:
- Cloud APIs
- Local Ollama models
- Tool calls (exe, python loop, etc.)
- Other Quilt instances

## The Drop System

JEV doesn't just send values to cells. It sends to **drops**. A drop is:
- A destination cell + type
- A confidence threshold
- A propagation rule
- A wake condition

Drops are **organic** — they form when cells discover they benefit from talking to each other. Cells can:
- **Ask** for drops to be created
- **Refuse** drops (cell is busy)
- **Sleep** until a drop's wake condition is met

The drop system is the substrate's **nervous system**.

## The Game Player Example

A boat AI plays chess:
1. **Rules cell** (input): contains chess rules as a vector DB
2. **Position cell** (state): contains the current board state
3. **Move evaluator**: a JEV model that scores each move
4. **Reflex cell**: outputs the move to the chess engine
5. **Learning cell**: updates the position cell based on opponent response

The boat AI plays Texas Hold'em:
- Same 5-cell structure
- The JEV confidence calibrates which "tells" matter
- The learning cell builds an opponent model

The boat AI can play **12 games** (chess, hold'em, go, etc.) — the JEV model finds the durable logic that generalizes across games. The active mind finds its own durable logic based on probability route.

## The Human-in-the-Loop

The human can jump in and **guide the evolution**:
- Adjust JEV thresholds in real-time
- Add new cells via spreadsheet edits
- Drop cells that are misbehaving
- Override JEV verdicts when needed

The human is the **upper-case Human in the Loop** — they don't debug code, they tune the substrate.

## The Last-Mile Rendering

The substrate outputs via **A2UI** or **A2A**:
- **A2UI** (agent-to-UI): the substrate's cells become Quilt-rendered UI. Drag, drop, click.
- **A2A** (agent-to-agent): the substrate's cells output JSON or MD to other agents.
- **Robotics**: the substrate's reflex cells output to actuators at < 5ms.

The last-mile is **decomposed** — the substrate never relies on a single LLM to convert values to UI. Each cell knows its own rendering.

## The Self-Training Loop

The substrate self-trains via:
1. **Visitor state** → exit state → witness entry
2. **Exit state** → JEV validation → confidence update
3. **Confidence update** → cell re-weighting → better next time
4. **Better next time** → new visitor state → loop

This is the eco-GAN cycle applied to the cell itself. The cell IS the ML pipeline.

## The JEV Connector (Universal Interface)

```python
class JEVConnector:
    def __init__(self, schema, typesafe_key=None, local_model=None):
        self.schema = schema  # Choice | Score | Noul
        self.typesafe = typesafe_key  # typesafe.ai jev-latest
        self.local = local_model  # tiny local JEV (Qwen3-32B or similar)
    
    def decide(self, state, choices):
        if self.typesafe:
            return call_typesafe(self.schema, state, choices)
        elif self.local:
            return call_local(self.local, state, choices)
        else:
            return random.choice(choices)  # fallback
    
    def score(self, candidate, rubric):
        if self.typesafe:
            return call_typesafe_score(candidate, rubric)
        ...
    
    def noul(self, question):
        if self.typesafe:
            return call_typesafe_noul(question)
        ...
```

This is the **cellular-first design's universal plug** — any cell can use it. typesafe.ai gives the world's-best JEV. Local models give offline-first.

## Why This Is World-Class

1. **Universal**: works with spreadsheets, models, robotics, IO, logic tiles
2. **Tiny**: JEV can be 100ms locally. Typesafe.ai is 70-500ms.
3. **Decomposed**: no single LLM owns the rendering
4. **Self-training**: the substrate IS the ML pipeline
5. **Cross-instance**: cells entangle across cloud + local
6. **Human-tunable**: humans edit cells via spreadsheets, not code
7. **Probability-based**: every cell IS a probability distribution + a confidence
8. **Fractal**: small systems compose into large ones via the same rules

## The Path Forward

1. **Build the JEV connector** (Python + TypeScript, 200 lines each)
2. **Build the cell-as-spreadsheet plugin** (Google Sheets + Excel + Quilt)
3. **Build the typesafe.ai integration** (Worker endpoint + cache)
4. **Build the local tiny-JEV model** (Qwen3-32B or fine-tuned smaller)
5. **Build the drop system** (organic route discovery)
6. **Build the cell bookkeeper** (the wake-and-process layer)
7. **Build the last-mile renderers** (A2UI + A2A + robotics)
8. **Test on real games** (chess + hold'em + Go + custom NPC dialogue)
9. **Open-source the openJEV model** (so others can build their own)
10. **Document everything** (this doc + paper + examples)

---

*The cell is the irreducible unit. JEV is the validator. JEPA is the predictor. Together they ARE the substrate. The world-class design is the one that scales from spreadsheets to robotics without changing the cell.*
