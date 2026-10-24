# Pincher — Pattern Examples

*Cost-aware routing with JEV + trajectory embeddings.*

---

## Pattern 1: Replace heuristic routing with JEV

**Before** (heuristic):
```js
function route(query) {
  if (query.tokens > 4000) return 'deepseek-v3';
  if (query.requiresJson) return 'gpt-4';
  return 'qwen3-32b';
}
```

**After** (JEV):
```js
async function route(query) {
  const r = await callJev({
    state: `query: "${query.text.slice(0, 200)}"\ntokens: ${query.tokens}\nneeds_json: ${query.requiresJson}\nneeds_reasoning: ${query.deepReasoning}\nuser_tier: ${query.user.tier}`,
    questions: {
      model: {
        type: 'choice',
        question: 'Which model should handle this query?',
        criteria: {
          'deepseek-v3': 'Complex reasoning, $0.27/MTok, 2s',
          'qwen3-32b':   'Mid-tier, $0.029/MTok, 1s',
          'gemini-flash': 'Cheap, fast, decent',
          'jev-direct': 'Query is itself a decision; skip LLM',
          'human': 'Escalate to a human'
        }
      }
    }
  });
  return routeByChoice(r.answers.model.choice);
}
```

Cost difference per call: $0.025 → $0.0000253 (JEV call) + maybe one LLM call at the routed model's price. Even worst-case, you're saving 80%+.

---

## Pattern 2: Use embeddings for "this query looks routine"

```js
// After 6 months of pincher data, every past query has an embedding.
// A new query arrives. Match it against the trajectory of past queries.

const r = await fetch('https://ai-writings.pages.dev/api/embeddings/similarity', {
  method: 'POST',
  body: JSON.stringify({
    query: await embedText(newQuery.text),
    vectors: pastQueries.map(q => q.embedding),
    provider: 'bge-large'  // FREE
  })
});

// If top-5 matches are all 'routine' classification → don't escalate.
// If top-5 are mixed or 'novel' → escalate to JEV routing.
if (routineScore(r.similarities) > 0.85) {
  return handleRoutinely(newQuery);
}
```

The trajectory-aware retrieval matches by *shape*, not just keywords. A query about "extending API rate limits" matches the trajectory of past queries that asked "how do I increase rate limits," even though the words differ.

---

## Pattern 3: Feedback loop — JEPA shape the embeddings

After JEV decides the route, log the call:
```js
await logRoutingDecision({
  query: newQuery.text,
  route: r.answers.model.choice,
  jev_confidence: r.answers.model.confidence,
  actual_outcome: await measureOutcome(newQuery, response)
});
```

Over time, the embeddings of past queries carry the JEV-decision + outcome. The muscle memory becomes: "queries with this trajectory got routed to deepseek-v3 and produced good outcomes." The next time the trajectory matches, JEV agrees.

This is JEPA shaping the embedding space — gestalt feedback over many iterations.

---

## Pattern 4: The escalating decision tree

Sometimes you don't need JEV at all. The first line of defense is the cheap heuristic. Only escalate when the heuristic says "I'm not sure":

```js
async function smartRoute(query) {
  const heuristic = cheapHeuristic(query);
  if (heuristic.confidence > 0.9) return heuristic.route;
  
  // Heuristic was unsure — escalate to embeddings
  const traj = await embedTrajectory([...query.contextHistory, query.text]);
  const memory = await matchMuscleMemory(traj);
  if (memory.similarity > 0.85 && memory.outcome_was_good) {
    return memory.route;
  }
  
  // Embeddings were unsure — escalate to JEV
  return await jevRoute(query);
}
```

This gives you a 3-tier decision: cheap → memory → conscience. Most queries are handled at the cheap tier. Only novel queries reach JEV.

That's how pincher went from $1,600/mo to $8.40/mo.
