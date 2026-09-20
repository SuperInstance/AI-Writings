# JEV × Pincher · Spec · Sept 19, 2026

## Motivation

Pincher is the vector-extraction primitive in the Quilt stack. It turns text into typed vectors. Today, developers hand-tune vector thresholds with regex + manual review. This is slow, brittle, and doesn't scale.

JEV replaces manual review with calibrated scoring. Each vector gets a rubric score in 150ms.

## Design

**Before**: developer writes a regex or a logistic-regression score. Iterates by reading 100 examples, adjusting weights, repeating.

**After**: developer defines a rubric. JEV scores each vector against the rubric. Developer iterates by adjusting the rubric, not the code.

### Rubric example

```javascript
const rubric = {
  intent: {
    type: "choice",
    question: "What's the user's primary intent?",
    criteria: {
      purchase: "User wants to buy something",
      support: "User needs help with an existing product",
      "compare": "User is comparing options",
      browse: "User is exploring without a specific goal"
    },
    options: ["purchase", "support", "compare", "browse"]
  }
};
```

### Scoring call

```javascript
const r = await jev.decide(vector.text, rubric);
const intent = r.answers.intent.choice; // "purchase"
const confidence = r.answers.intent.confidence; // 0.87
```

## Endpoints

- `POST /api/pincher/score` — vector + rubric → JEV score
- `POST /api/pincher/batch-score` — N vectors + rubric → N scores (parallel)

## Workload

- 1M vectors/month × 200 tokens each = 200M tokens input
- $0.042/MTok × 200M tokens = **$8.40/month** on JEV
- Compare: GPT-4 at $2.50/MTok in + $10/MTok out, average 600 in + 100 out = $0.0016/call
- 1M calls × $0.0016 = **$1,600/month** on GPT-4

**JEV is 190x cheaper** for this workload.

## Fast-iteration pattern

```javascript
async function iteratePincher(vectors, rubric) {
  // Parallelize 1000 vectors across 4 workers
  const chunks = chunk(vectors, 250);
  const results = await Promise.all(chunks.map(c => jev.batchScore(c, rubric)));
  
  // Find low-confidence vectors (the ones the rubric is wrong about)
  const lowConf = results.flat().filter(r => r.confidence < 0.7);
  
  console.log(`${lowConf.length} vectors need rubric review`);
  return lowConf;
}
```

Developer tunes the rubric by reading the low-confidence vectors. No code change required.

## Code patterns

### JavaScript

```javascript
import { JEV } from './jev-sdk';
const jev = new JEV(process.env.TYPESAFEAI_KEY);

async function scoreVector(text, rubric) {
  const r = await jev.decide(text, rubric);
  return r.answers;
}
```

### Python

```python
import os, requests

def score_vector(text, rubric):
    return requests.post(
        "https://api.typesafe.ai/v1/systemone",
        headers={"Authorization": f"Bearer {os.environ['TYPESAFEAI_KEY']}"},
        json={"model": "jev-latest", "state": text, "questions": rubric}
    ).json()["answers"]
```

## What this enables

- **10x faster iteration cycles** on vector scoring thresholds
- **Calibrated confidence** for every vector (know what you don't know)
- **Audit-grade scoring** for regulated industries
- **Self-tuning rubrics** via low-confidence sampling

## Cost / benefit

| Aspect | Before (manual) | After (JEV) |
|--------|----------------|-------------|
| Setup time | 2-4 weeks | 1 hour |
| Iteration time | 1-2 days | 1 hour |
| Cost / month | $200+ in dev time | $8.40 in API |
| Calibration | None | Yes (geometric mean) |
| Audit | None | Probabilities + log |
