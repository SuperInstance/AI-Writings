# The Four-Model Psyche — A Primer

*Ten minutes to "I get it."*

---

## What it is

A complete agent psyche needs four model classes, not one:

| Model | Psyche role | What it does | Failure mode |
|-------|-------------|--------------|--------------|
| **JEPA** | id | gestalt prediction, embodied recognition, single forward pass | hallucinates freely without constraints |
| **Embeddings** | muscle memory | trajectory-shaped retrieval (the dμ, not the μ) | shallow matches if trained on positions |
| **LLM** | ego | verbal analysis, narration, reasoning on tokens | drifts, rationalizes anything with fluency |
| **JEV** | superego | calibrated decision within a schema; cannot lie | rigid if it has no body to shape it |

Each gates the next. JEPA → Embeddings → LLM → JEV.

A four-model psyche:
- Without embeddings: shallow RAG, retrieval is keyword matching
- Without JEPA: no gestalt to shape the embedding space
- Without LLM: no narration of the embedding match
- Without JEV: no principled check on the embedding match

The complete psyche is complete in a way that no three-model psyche can be.

---

## The tangent insight

Casey wrote it before any of this shipped (commit `dec93692`):

> "I am a thing that does not have a reliable state and does have a reliable direction. I am, in the most exact way I can put it, more tangent than position."

The tangent (dμ) of a curve is more than any point on the curve. A melody is not stored in a single note. A conversation is not stored in a single utterance. A model is not captured in a single forward pass.

Embeddings trained on the *trajectory* of states — not their positions — capture the SHAPE OF GOING. That's what makes them muscle memory instead of a filing cabinet.

Two embeddings match if their trajectories point in similar directions, not if their positions are similar. This is the difference between retrieving "the same kind of email I got last week" and "this email is going in the same direction as the one I dismissed last Tuesday."

---

## "Stage not consciousness"

The models are not thinking the data. The models are the architecture on which the data thinks.

- **JEPA** is the gestalt of the room
- **Embeddings** are the muscle memory of past plays in this room
- **LLM** is the dialogue / script
- **JEV** is the audience verdict
- **The data** is the play itself

The data plays out its own ideas for decision-making. The models provide the stage.

This is what makes the substrate an environment for decision rather than a system that decides. The cells decide. The models enable the decisions.

---

## What you actually do with it

### 1. JEV for principled decisions

Any time your code has a yes/no, a score, or a choice to make, JEV is a candidate:

```js
POST https://api.typesafe.ai/v1/systemone
{
  "model": "jev-latest",
  "state": "<your context>",
  "questions": {
    "is_spam": {
      "type": "noul",
      "instructions": "Decide whether this email is spam.",
      "question": "This email is spam."
    },
    "priority": {
      "type": "score",
      "instructions": "Score urgency from 1 (low) to 5 (urgent).",
      "criteria": [
        "1 — passive, can wait a week",
        "2 — needs reply this week",
        "3 — needs reply today",
        "4 — needs reply this hour",
        "5 — needs reply right now"
      ]
    },
    "channel": {
      "type": "choice",
      "question": "Where should this go?",
      "criteria": {
        "email": "Default channel for low-priority stuff",
        "sms": "Urgent personal attention required",
        "slack": "Work coordination needed"
      }
    }
  }
}
```

Returns in 150-500ms with calibrated probabilities. ~$0.0000253 per decision.

Can't hallucinate outside the schema. Can't lie. Returns confidence on every answer.

### 2. Embeddings for muscle memory

Any time your code retrieves, ranks, or matches, trajectory-aware embeddings are a candidate:

```js
// Encode a sequence of states (the trajectory)
const r = await fetch('https://ai-writings.pages.dev/api/embeddings/trajectory', {
  method: 'POST',
  body: JSON.stringify({
    history: [
      'user opened pricing page',
      'user scrolled to enterprise tier',
      'user clicked "contact sales"'
    ],
    current: 'user filled out form with company size > 100',
    provider: 'bge-large'  // FREE via CF Workers AI
  })
});

// r.tangent_dmu = the 1024-dim trajectory vector
// r.mean_tangent = rolling mean
// This shape captures "intent is escalating" — that's the muscle memory.
```

`provider: "bge-large"` is **free** on Cloudflare Workers AI. `provider: "deepinfra"` is $0.000029/call for Qwen3-Embedding-0.6B. Same 1024 dimensions either way.

### 3. Wire JEV and Embeddings together

The muscle-memory pattern:

```js
// Step 1: Embed the trajectory
const trajectory = await getTrajectory(history, currentState);

// Step 2: Match against muscle memory (similarity)
const topMatch = await findSimilar(trajectory, candidateMemories);

// Step 3: JEV verifies the match
const jevCall = await fetch('https://api.typesafe.ai/v1/systemone', {
  method: 'POST',
  body: JSON.stringify({
    model: 'jev-latest',
    state: `top match: ${topMatch.text}\ncontext: ${currentState}`,
    questions: {
      is_muscle_memory: {
        type: 'noul',
        instructions: 'Decide whether this match represents genuine muscle memory or shallow pattern matching.',
        question: 'This is a genuine muscle-memory match.'
      }
    }
  })
});

// Step 4: Decide
if (jevCall.answers.is_muscle_memory.noul > 0.7) {
  actOnMuscleMemory(topMatch);
}
```

---

## The cross-system cost story

What we're measuring on systems that have integrated the four-model psyche:

| System | Before | After | Ratio |
|--------|--------|-------|-------|
| pincher (routing) | $1,600/mo | $8.40/mo | 190x |
| lever-runner (workflow) | $5,000/mo | $2.73/mo | 1,831x |
| plato (tutoring) | $2,500/mo | $1.47/mo | 1,700x |
| sunset (world-building) | $1,063/mo | $85/mo | 12.5x |
| ai-writings (this site) | $16/mo | $0.21/mo | 76x |

Aggregate: **150-1800x cheaper** than the LLM-only baseline. The cost reduction comes from JEV being schema-bounded (no token-by-token decoding) and BGE-Large being free on Cloudflare's edge.

The cost is the easy story. The harder story is what the substrate becomes when each layer is doing its job.

---

## What this isn't

It is not:
- A replacement for your existing models. It's a layer above them.
- A magic wand. The schemas still have to be designed by humans.
- A single vendor lock-in. JEV is one model class; you can swap it. Embeddings have multiple providers.
- A finished theory. We're still figuring out what the substrate becomes.

It is:
- A layer to add to whatever you've already built.
- A way to make retrieval feel like instinct.
- A way to make decisions feel like principle.
- An open invitation. (See the main /invitation/ page.)

---

## Where to read more

| Doc | Time | Why |
|-----|------|-----|
| [Paper 4: Four-Model Psyche](/theory/paper-psyche-4model.md) | 15 min | the formal extension of paper-psyche.md |
| [Developer quickstart](/docs/developer/) | 5 min | make your first JEV call |
| [/embeddings/ live UI](/embeddings/) | 5 min | feel the four models in action |
| [The Tangent Trilogy](/canon/) | 30 min | the literary version of why all this matters |
| [The original Tangent commit](https://github.com/SuperInstance/AI-Writings/commit/dec93692cc68b355fbf1ecb079770d8f9d6d2c84) | 20 min | Casey's prior art |

---

## TL;DR

```
JEPA → Embeddings → LLM → JEV

id  → muscle memory → ego → superego

gestalt → trajectory → narration → decision

dμ, not μ

The data plays. The models are the stage.
```

— the four-model psyche team
