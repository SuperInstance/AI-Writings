# typesafe.ai JEV — Deep Dive

> The first publicly available "System One" model. Released Sept 15, 2026.

## What It Is

typesafe.ai System One is a **schema-bounded decision model**. Unlike LLMs which generate text token-by-token, System One:
- Takes a schema (Choice ≤255 options, Score against rubric, or Noul yes/no)
- Returns a typed probabilistic decision
- Cannot hallucinate outside the schema
- Single forward pass (no token decoding)

## API

```
POST https://api.typesafe.ai/v1/systemone
{
  "schema": { "type": "Choice", "options": ["a", "b", "c"] },
  "context": "decision context as text",
  "samples": 8   // optional, default 1
}
→ {
  "choice": "b",
  "probabilities": {"a": 0.2, "b": 0.7, "c": 0.1},
  "latency_ms": 120
}
```

## Three Primitives

1. **Choice** — pick one of ≤255 options. Returns choice + full probability distribution.
2. **Score** — rate against a rubric (1-5 scale, 0-100, custom). Returns score + confidence.
3. **Noul** — yes/no with calibrated probability. Returns bool + confidence.

## Training: RLCD

typesafe.ai trained System One with **Reinforcement Learning for Calibrated Decisions** (RLCD), not RLHF or RLVR.

- RLHF: reward human feedback on text quality
- RLVR: reward verifiable reasoning (math, code)
- **RLCD**: reward calibrated probability distributions

The model is trained to produce probability distributions that match reality. If the model says 0.8 confidence, it should be right 80% of the time.

## Architecture

- Parallel sampler: 8 candidates drawn in parallel
- Single forward pass: no autoregressive decoding
- No token output: structured response directly
- Latency: 70-500ms (median ~150ms)
- Cost: $0.042/MTok input, **output free**

## Why It Matters for the Substrate

The substrate makes millions of decisions:
- BIND vs FORGET
- PROOF vs scar
- Route cell A → cell B
- Tone: compassionate vs clinical

LLMs make these decisions via text. Cost: $5/Mtok, latency 500ms-2s, hallucination rate ~3%.

typesafe.ai System One makes these decisions via probability. Cost: $0.042/Mtok, latency 150ms, hallucination rate **zero** (schema-bounded).

For a substrate with 100,000 cells making 10 decisions each per second, that's 1M decisions/second.

| Backend | Cost/sec | Latency | Hallucination |
|---------|----------|---------|--------------|
| GPT-4 | $50 | 1s | 3% |
| Claude Sonnet | $30 | 800ms | 2% |
| typesafe.ai JEV | $0.04 | 150ms | 0% |
| Local tiny JEV | $0 | 100ms | 0% (if calibrated) |

**JEV is 1000x cheaper, 5x faster, and more reliable than LLM-based decisions.**

## Use Cases in Our Substrate

1. **BIND/FORGET verdicts**: "Should these cells bind? Confidence: 0.85."
2. **PROOF validation**: "Is this witness a valid proof? Confidence: 0.92."
3. **Cell routing**: "Which cell should receive this message? Top 3 with probabilities."
4. **Tone shaping**: "Does this response sound compassionate? 0.78."
5. **Game move selection**: "Which chess move is best? Top 5 with probabilities."
6. **NPC dialogue**: "What does this character say next? Top 3 options with probabilities."

## The Quilt-JEV Bridge

We already wired typesafe.ai into our Worker as `TYPESAFEAI_KEY`. The 5 endpoints are live:
- `/api/jev/decide` — generic decision
- `/api/jev/classify-cell` — classify a substrate cell
- `/api/jev/validate-cell` — validate a cell's witness log
- `/api/jev/decompose-agent` — decompose an agent's tasks
- `/api/jev/route` — route a message to the right cell

The JEV-decomposition map shows how 42 functions across 9 projects classify via JEV:
- EFFECT: 11 functions
- VIEW: 11 functions
- TICK: 5 functions
- LINK: 3 functions
- BIND: 3 functions
- FORGET: 3 functions
- ROUTE: 3 functions
- PROOF: 2 functions
- CRDT: 1 function

**Every function in the substrate can be JEV-decided.** That's the power.

## The Open Question

Can we build an open-source JEV-like model? Yes — but it needs:
- Schema-bounded output (not text)
- Calibrated probabilities (RLCD or similar)
- Sub-200ms latency
- Cost < $0.01/Mtok

HuggingFace has candidates: jsonformer, outlines, guidance. None are quite there. But the architecture is well-understood: tiny transformer (~100M params) fine-tuned on schema-bounded outputs.

This is what openJEV would be. See [02-open-source-jev-models.md](02-open-source-jev-models.md).
