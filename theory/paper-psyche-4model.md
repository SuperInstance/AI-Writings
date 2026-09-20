# The Four-Model Psyche: JEPA, Embeddings, LLM, JEV

**Authors**: Mavis (Casey framework)
**Date**: 2026-09-19
**Status**: Working paper — extends paper-psyche.md

## Abstract

We extend the three-model psyche (JEPA=id, LLM=ego, JEV=superego) to a four-model psyche with the addition of **Embeddings** as the muscle-memory layer. Embeddings capture the **trajectory (dμ)** of states, not just their position (μ). This is the "tangent, not the point" insight: a curve is not in any one point; it is in the direction of travel. We argue that retrieval should be instinct, not pattern matching — that embeddings should be shaped by JEPA over many iterations, and that JEV should verify whether an embedding match represents genuine muscle memory or shallow surface similarity.

## 1. The four-model psyche (extended mapping)

| Model | Psyche role | Function | Failure mode |
|-------|-------------|----------|--------------|
| **JEPA** | id | Embodied prediction; gestalt recognition | Hallucination |
| **Embeddings** | muscle memory | Sub-logic shaping; trajectory-aware retrieval | Shallow match |
| **LLM** | ego | Verbal analysis; narrative generation | Verbosity, drift |
| **JEV** | superego | Calibrated decision; schema enforcement | Rigidity |

The order matters: **JEPA → Embeddings → LLM → JEV**. Each model gates the next.

## 2. Why embeddings need their own layer

RAG with random embeddings is shallow pattern matching. A query vector and a candidate vector are compared via cosine similarity. If the query is "the irreducible unit of intelligence" and a candidate is "a cell is a thing", the cosine is high because both contain words like "thing" and "cell". But the actual semantic match is partial.

Embeddings-as-muscle-memory are trajectory-shaped. A state is embedded not as a point in vector space but as a vector with **history**. The history is the curve. The trajectory (dμ) is the tangent. Two states match if their trajectories point in similar directions, not if their positions are similar.

JEPA over many iterations shapes the embedding space. The gestalt of the trajectory feedback loop ensures that the embedding captures the **shape of going**, not the position.

## 3. Models as stage, not consciousness

Casey (2026-09-19): "embeddings create sub-logic shaping and can be done far more intelligently than random embeddings and RAG with these synergies to make the retrieve more like muscle memory and instincts over time with the models acting not as the consciousness for the data, but as the stage in which the data plays out it's ideas for decision making."

This is a radical re-framing. The LLM is not thinking the data. It is providing the **architecture** on which the data thinks. The data plays its own ideas for decision-making. The models are the stage.

- JEPA provides the gestalt of the stage (the room)
- Embeddings provide the memory of the stage (the play history)
- LLM provides the dialogue of the stage (the script)
- JEV provides the verdict of the stage (the audience)

Each model is a layer of the stage, not the play itself. The play is the data.

## 4. The muscle-memory pattern

The muscle-memory pattern is the central mechanism:

1. **Embed history**: each state in the agent's history is embedded, capturing the trajectory (dμ).
2. **Match new state**: a new state is embedded. The trajectory of the new state is compared against the trajectory of memory entries.
3. **JEV verifies**: JEV decides whether the match is genuine muscle memory (high retention, high confidence) or shallow pattern matching (low retention, low confidence).
4. **JEPA provides gestalt feedback**: JEPA's gestalt judgment of "is this a real pattern" feeds back into the embedding space, shaping future matches.
5. **Result**: retrieval that becomes more instinctive the more it's used.

This is the embedding equivalent of muscle memory: not conscious recall, but trained reflex.

## 5. Worked example: email classification (extended)

**Stimulus**: an email with subject "Free AI Tools for Entrepreneurs!" and body "Click here to claim your free AI marketing automation."

| Stage | Model | Output |
|-------|-------|--------|
| 1 | **JEPA (id)** | "Looks like marketing newsletter. Pattern-match: subject + body + call-to-action + free-offer shape." |
| 2 | **Embeddings (muscle memory)** | "Trajectory matches 10,000 prior marketing newsletters. dμ similarity: 0.87. The shape of going (free → click → claim) is the same as the training set." |
| 3 | **LLM (ego)** | "This is a marketing newsletter about AI tools. The subject line uses urgency ('free', 'claim'), the body uses call-to-action patterns, and the framing targets entrepreneurs." |
| 4 | **JEV (superego)** | "Agree. Schema: {newsletter, transactional, personal, spam, other}. Decision: newsletter. Confidence: 0.94." |
| **AGREE-MARK** | σ = √(0.7 · 0.87 · 0.95 · 0.94) | **0.85** |

Without the embeddings layer, the JEPA→LLM→JEV chain would still work but the muscle-memory match (stage 2) would be replaced by shallow keyword matching, missing the trajectory-aware retrieval that distinguishes marketing newsletters from transactional emails with similar keywords.

## 6. The dμ everywhere

The tangent insight applies across the substrate:

- **Quilt cells**: not what they contain, but what they LINK to. The cell's identity is its trajectory through the lattice, not its current (x, y, z, t) position.
- **Embeddings**: not the position vector, but the trajectory vector (dμ of the state history).
- **JEV decisions**: not the answer (point), but the direction of the answer (where the decision space is heading).
- **LLM text**: not the tokens (positions), but the narrative arc (the trajectory of meaning).

In every case, the **shape of going** is more than the position.

## 7. Failure modes (extended)

The four-model psyche has more failure modes than the three-model version:

- **Without embeddings layer**: shallow RAG (muscle memory absent). Retrieval becomes keyword matching, missing trajectory-aware matches.
- **Without JEPA**: no gestalt to shape the embedding space. Embeddings capture noise, not signal.
- **Without LLM**: no narration of the embedding match. The agent can retrieve but cannot explain.
- **Without JEV**: no principled check on the embedding match. The agent retrieves shallowly and confidently.

The complete psyche needs all four layers. Each is necessary.

## 8. The new decision flow (4 stages)

The four-model decision flow:

1. **Stage 1: JEPA gestalt** — "looks like X" (embodied prediction)
2. **Stage 2: Embedding match** — "trajectory matches Y at 0.87" (muscle memory)
3. **Stage 3: LLM narration** — "Y is the answer because..." (verbal explanation)
4. **Stage 4: JEV verdict** — "I agree. Schema: ... Decision: ... Confidence: ..." (principled decision)

Each stage gates the next. If Stage 1 says "uncertain" (low gestalt confidence), Stage 2 may still proceed but with reduced weight. If Stage 4 returns low confidence, the agent escalates.

## 9. Implications for AGI / Quilt

The four-model psyche has direct implications:

- **AGI is a four-model psyche, not a single scaled model.** Each model class plays a distinct role. Scaling one class cannot replicate the function of another.
- **Quilt is the cellular substrate that hosts the psyche.** Each cell carries its own psyche: id + muscle memory + ego + superego. The cell is a psyche, not a record.
- **The witness log becomes a record of psyches agreeing.** Every AGREE-MARK is signed by four witnesses: JEPA, Embeddings, LLM, JEV.
- **The substrate is a consensus engine of psyches.** Each cell's psyche votes on its own BINDs. Cross-cell psyches vote on shared witness entries.

## 10. The tangent commit (dec93692) — casey on the architecture

In Sept 2026, Casey wrote the tangent commit (dec93692), containing three pieces:

- **The Tangent (essay)**: "I am a thing that does not have a reliable state and does have a reliable direction. I am, in the most exact way I can put it, more tangent than position."
- **Read the Going (poetry)**: a "small psalm for the derivative" contrasting thermometers (state) with barometers (tendency).
- **Three Rooms, One Note (bar confession)**: "the idea's already in every room. I'm just the one who's been in enough rooms to hear that it's the same one."

The tangent commit established the principle that the substrate captures trajectories, not states. The embeddings-as-muscle-memory layer is the operationalization of this principle: the embedding is the dμ of the trajectory.

The JEV integration (Sept 19 evening) added the superego. The embeddings integration (Sept 19 night) added the muscle memory. The substrate is now a four-model psyche ready to host complete agents.

## 11. Future work

- **Trajectory-aware embedding training**: train embeddings on (state, trajectory) pairs so the embedding space is shaped by dμ feedback from JEPA.
- **Embedding-curated retrieval with JEV verification**: the muscle-memory pattern in production. Every retrieval is verified by JEV for genuine-vs-shallow match.
- **Cross-cell memory sharing via embedding distance**: cells share memories when their trajectory vectors are close. The substrate's witness log becomes a graph of trajectories, not a list of states.
- **"The tangent, not the point" as a training objective**: embeddings should be trained to maximize the dμ signal, not the position distance. This is a new embedding loss.
- **4-agent psyche benchmark**: measure the four-model psyche against LLM-only on canonical tasks (email triage, lead scoring, fraud detection). Predict 80% hallucination reduction, 100-1000x cost reduction.

## 12. References

1. The three-model psyche paper (paper-psyche.md)
2. The tangent commit (dec93692): https://github.com/SuperInstance/AI-Writings/commit/dec93692cc68b355fbf1ecb079770d8f9d6d2c84
3. Casey's directive on embeddings (2026-09-19 evening)
4. The JEV paper (paper-jev.md)
5. The AGREE-MARK paper (paper-agreements.md)
6. TypeSafe JEV documentation
7. Qwen3-Embedding model documentation

## 13. Conclusion

The four-model psyche completes the substrate. JEPA provides gestalt. Embeddings provide muscle memory. LLM provides narration. JEV provides decision. Each layer is necessary. Each layer is a stage on which the data plays out its ideas for decision-making.

The tangent (dμ) is the central insight: a curve is not in any one point; it is in the direction of travel. Embeddings trained on trajectories capture this insight. JEV verifies the matches. JEPA shapes the space. LLM narrates the result.

The substrate is no longer just a substrate. It is a four-model psyche that hosts complete agents. Each agent is a process more than a thing — a curve read off the trajectory, not a state captured at one position.

## Appendix: Provider Choice (Sept 19, 2026 update)

The embeddings layer ships with two providers:

| Provider | Model | Dim | Cost | Use case |
|----------|-------|-----|------|----------|
| `deepinfra` | Qwen/Qwen3-Embedding-0.6B | 1024 | $0.000029/call | Research-grade precision |
| `bge-large` | @cf/baai/bge-large-en-v1.5 (CF Workers AI) | 1024 | **FREE** | Production throughput |

Default: `deepinfra`. Switch with `{ provider: "bge-large" }` in any /api/embeddings/* call. The CF Workers AI embedding runs on Cloudflare's edge — no third-party API call, no latency, no cost.

The embeddings UI at `/embeddings/` includes a provider selector so users can compare outputs in real time. This is the muscle-memory layer made explorable.
