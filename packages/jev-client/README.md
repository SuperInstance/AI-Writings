# jev-client

JavaScript/TypeScript client for [JEV (TypeSafe System One)](https://ai-writings.pages.dev/theory/paper-jev.md) — the first publicly available "System One" decision model. Schema-bounded, cannot hallucinate outside your schema.

## What is JEV?

JEV is a **decision-only** model, not a chatbot. It returns typed probabilistic decisions inside your schema:

- **Choice** — pick 1 of ≤255 options, with rubric-based criteria
- **Score** — rate against an ordered rubric
- **Noul** — yes/no with calibrated probability

JEV is trained with **RLCD** (Reinforcement Learning for Calibrated Decisions), not RLHF/RLVR. Architecture: parallel sampler, single forward pass, no token decoding. **$0.042/MTok input, output free, 70-500ms latency.**

It cannot lie outside your schema — bounded by construction.

## Install

```bash
npm install jev-client
```

## Usage

### Browser

```ts
import { JevClient } from 'jev-client';

const jev = new JevClient();
const r = await jev.decide({
  state: 'The cell just received 47 new witnesses.',
  questions: {
    witness: {
      type: 'noul',
      question: 'this should be witnessed',
      instructions: 'yes if 47 witnesses is significant'
    }
  }
});
console.log(r.answers.witness.choice); // 'yes'
```

### Node.js

```js
const { JevClient } = require('jev-client');

(async () => {
  const jev = new JevClient();
  const r = await jev.decide({
    state: 'A new cell arrived.',
    questions: {
      category: {
        type: 'choice',
        question: 'what kind?',
        options: ['generative', 'diagnostic', 'transformative', 'connective', 'meta'],
        criteria: {
          generative: 'produces new content',
          diagnostic: 'inspects/audits',
          transformative: 'alters state',
          connective: 'binds/routes',
          meta: 'reflects on the system'
        }
      }
    }
  });
  console.log(r.answers.category.choice); // 'meta' or whatever JEV picks
})();
```

### Three primitives

```ts
// Yes/no
await jev.noul(state, 'is this valid?', 'yes if non-empty');

// Multiple choice
await jev.choice(state, 'which?', ['a','b','c'], {
  a: 'first',
  b: 'second',
  c: 'third'
});

// Score
await jev.score(state, 'rate it', ['low','mid','high']);
```

### Custom endpoint

```ts
// If you're running your own JEV instance
const jev = new JevClient({
  endpoint: 'https://your-deployment.example.com/api/jev/decide'
});
```

### Server-side (Cloudflare Workers, Vercel Edge, Deno)

```ts
// In a Cloudflare Worker
export default {
  async fetch(req: Request): Promise<Response> {
    const jev = new JevClient();
    const r = await jev.decide({
      state: 'A new event arrived',
      questions: { /* ... */ }
    });
    return Response.json(r);
  }
};
```

## What this is for

JEV is the substrate's superego. Use it when:

- You need **typed decisions** (not free text)
- You need **calibrated probabilities** (JEV reports its confidence)
- You need **schema-bounded** outputs (impossible to hallucinate outside the schema)
- You're building a Quilt cell or lattice operation
- You're routing cells and want a principled choice
- You're classifying cells into kinds and want consistent decisions
- You're scoring/validating and want a rubric-following answer

## The substrate context

JEV is one layer of the four-model psyche:
- **JEPA** = id (gestalt)
- **Embeddings** = muscle memory (trajectory)
- **LLM** = ego (verbal narration)
- **JEV** = superego (principled decision)

For more, see:
- `/theory/paper-jev.md` — formal treatment
- `/theory/paper-psyche-4model.md` — four-model psyche paper
- `/lab/jev-quantum/` — recent ideation on JEV as quantum-measurement apparatus
- `/invitation/` — open call to the fleet

## License

MIT
