# JEV × Sunset-Ecosystem · Spec · Sept 19, 2026

## Motivation

Sunset-ecosystem is the simulation substrate. Today, each ecosystem tick runs JEPA-predicted next state, then LLM narrates the tick. There's no principled check that the prediction matches reality.

JEV adds the validation step: did the predicted state agree with observed state? Disagreement = fork.

## Design

**Before**: tick = JEPA → LLM → next tick (no validation)

**After**: tick = JEPA → JEV validate → LLM narrate → next tick

### Validation step

```javascript
async function tickValidate(predicted, observed) {
  const r = await jev.decide(JSON.stringify({predicted, observed}), {
    agree: {
      type: "noul",
      instructions: "Decide whether the predicted state matches the observed state, accounting for acceptable drift.",
      question: "The predicted state agrees with the observed state."
    },
    drift: {
      type: "score",
      question: "How much drift is there between predicted and observed?",
      criteria: ["none", "minor", "moderate", "major", "impossible"],
      scale: ["none", "minor", "moderate", "major", "impossible"]
    },
    confidence: {
      type: "score",
      question: "How confident are you in the validation?",
      criteria: ["low", "medium", "high"],
      scale: ["low", "medium", "high"]
    }
  });
  
  return {
    agree: r.answers.agree.noul,
    drift: r.answers.drift.score,
    confidence: r.answers.confidence.score,
    fork: r.answers.agree.noul < 0.5 || r.answers.drift.score > 3
  };
}
```

## Endpoints

- `POST /api/sunset/tick-validate` — predicted + observed → {agree, drift, confidence}
- `POST /api/sunset/sim-batch` — N simulations → flags for divergence

## Use case: 1000 parallel simulations

Run 1000 simulations in parallel. Each simulation predicts a state. Compare to observed reality. JEV flags the 5 that have diverged.

```javascript
async function findDivergences(simulations, observed) {
  const scores = await Promise.all(simulations.map(sim => 
    jev.tickValidate(sim.predicted, observed)
  ));
  
  return simulations
    .map((sim, i) => ({sim, score: scores[i]}))
    .filter(r => r.score.fork)
    .sort((a, b) => b.score.drift - a.score.drift);
}
```

## What this enables

- **Early detection of "impossible" simulation paths**
- **Calibrated drift estimation** (not just "did we diverge" but "how much")
- **Audit trail** of every fork in the simulation log
- **Cross-simulation consensus** (multiple sims agreeing → high confidence)

## Workload

- 1M simulation ticks/month × 500 tokens state
- 500M tokens input = **$21/month** on JEV alone
- Compare: JEPA self-hosted ~$0.001/tick × 1M = **$1,000/month**
- Plus LLM narration: 1M × 1500 tokens = 1.5B tokens = **$63/month**

Total: **$84/month** for fully validated, narrated, audited simulation.

## Pattern: simulation as a service

```javascript
async function runSimulation(spec) {
  // JEPA pre-classifies
  const predicted = await jepa.predict(spec.state, spec.deltaT);
  
  // JEV validates against prior observations
  const validation = await jev.tickValidate(predicted, spec.observed);
  
  if (validation.fork) {
    // Disagreement fork → escalate to LLM
    const narrative = await llm.explainDivergence(predicted, spec.observed);
    spec.witnessLog.append({type: 'fork', validation, narrative});
    return { status: 'diverged', validation, narrative };
  }
  
  // LLM narrates the tick
  const narrative = await llm.narrate(predicted);
  spec.witnessLog.append({type: 'tick', predicted, validation, narrative});
  return { status: 'proceeded', predicted, validation, narrative };
}
```

## Limitations

- JEV's Noul question (yes/no) returns a single probability. For richer drift explanations, use Score.
- 1200 req/min limit. For high-throughput simulation, batch with application layer.
- Each tick now has 2 model calls (JEV validate + LLM narrate). Optimize by combining if possible.

## Cost / benefit

| Aspect | Before (JEPA + LLM) | After (JEPA + JEV + LLM) |
|--------|---------------------|--------------------------|
| Cost / 1M ticks | $1,063 | $84 + $0.50 (if fork) = ~$85 |
| Latency p50 | 2.5s | 2.7s |
| Divergence detection | None | Calibrated |
| Audit | None | Witness-log per tick |
