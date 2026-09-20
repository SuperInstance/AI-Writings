# JEV × Lever-Runner · Spec · Sept 19, 2026

## Motivation

Lever-runner is the agent-orchestration primitive. Today, each agent decision is an LLM-prompt that returns free text. The runner parses the text into actions. This is brittle.

JEV turns each decision into a typed probability. The runner scores candidate actions with confidence, escalates low-confidence to LLM, and executes high-confidence directly.

## Design

**Before**: agent emits 10 candidate actions as free text. Runner parses, ranks, picks top-1.

**After**: agent emits 10 candidate actions. JEV scores each with a rubric. Runner picks top-3, asks LLM to narrate, executes top-1.

### Decision flow

```
1. Agent proposes 10 candidate actions
2. JEV scores each (parallel, 150ms total)
3. Top-3 by confidence go to LLM for narrative
4. LLM picks the best 1 with explanation
5. Top-1 executes with witness-log entry
```

## Endpoints

- `POST /api/lever/agent-decide` — agent_id + state + questions → typed decision
- `POST /api/lever/score-actions` — actions[] + rubric → scored_actions[]
- `POST /api/lever/explain` — top-3 actions → narrative explanation

## Workload

- 100k agent decisions/month × 500 tokens state + 200 tokens output
- 50M tokens input + 20M tokens output = $2.10 + free output = **$2.10/month** on JEV alone
- LLM escalation for top-3 (10k times/month) × 1500 tokens = 15M tokens in + 5M out = $0.63 + free = **$0.63/month**
- Total: **$2.73/month** vs **$5,000/month** for full LLM-everywhere

## Reduction in hallucination-induced actions

Estimate: 80% reduction. Reasoning: today, ~30% of agent actions contain hallucinated commands (parsing the LLM output wrong, or LLM hallucinating). With JEV scoring:
- 50% of actions are JEV-scored at confidence > 0.95 → execute directly
- 30% of actions are JEV-scored at confidence 0.7-0.95 → LLM narrates, picks best
- 20% of actions are JEV-scored at confidence < 0.7 → human review

In the LLM-narrated tier, hallucination is reduced because the LLM is choosing between 3 known-good actions, not generating from scratch.

In the JEV-execute tier, hallucination is impossible (schema-bounded).

In the human-review tier, humans catch the rest.

## What this enables

- **4-agent psyche**: JEPA pre-classifies → LLM narrates → JEV certifies → runner executes
- **Continuous agent audit** via witness-log
- **Reduced hallucination** in production agent loops
- **Cheaper agent decisions** at scale

## Pattern

```javascript
async function agentDecide(state, candidates) {
  // Step 1: JEV scores each candidate
  const scores = await jev.scoreActions(candidates, {
    primary_op: {
      type: "choice",
      question: "Which is the dominant Quilt opcode?",
      criteria: { BIND: "creates cell", LINK: "connects", EFFECT: "mutates", VIEW: "reads", TICK: "advances time", FORGET: "removes", PROOF: "verifies", ROUTE: "sends", CRDT: "merges", WORLD: "places", TIME: "schedules" },
      options: ["BIND","LINK","EFFECT","VIEW","TICK","FORGET","PROOF","ROUTE","CRDT","WORLD","TIME"]
    }
  });
  
  // Step 2: Top-3 go to LLM
  const top3 = scores.sort((a,b) => b.confidence - a.confidence).slice(0, 3);
  
  // Step 3: LLM narrates
  const narrative = await llm.narrate(state, top3);
  
  // Step 4: Execute top-1
  return execute(narrative.recommended);
}
```

## What this enables for the substrate

- Agents with auditable decision trails
- Cross-agent composition via shared witness-log
- Reduced LLM cost at high-volume agent decisions
- Schema-bounded agent actions

## Limitations

- JEV's Choice primitive caps at 255 options. For agents with > 255 candidate actions, multi-stage decision.
- JEV is text-only. For agent actions on images/audio, use VLM or audio-specific models.
- JEV has 1200 req/min limit. For high-throughput agents, batch with the application layer.
