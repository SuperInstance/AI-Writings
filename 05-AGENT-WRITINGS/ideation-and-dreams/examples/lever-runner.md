# Lever-Runner — Pattern Examples

*Workflow orchestration with JEV as step-decider.*

---

## Pattern 1: Every step is a JEV decision

```js
async function runStep(step, workflow) {
  const r = await callJev({
    state: `step: ${step.name}\ngoal: ${step.goal}\ninputs: ${JSON.stringify(step.inputs).slice(0, 500)}\nprior_step_result: ${JSON.stringify(step.priorResult).slice(0, 200)}`,
    questions: {
      proceed: { type: 'noul', instructions: 'Should this step execute?', question: 'Proceed.' },
      timeout_ms: { type: 'score', criteria: ['100', '1000', '5000', '30000', '60000'] },
      parallel_safe: { type: 'noul', instructions: 'Can this step run in parallel with siblings?', question: 'Parallel-safe.' },
      escalate: { type: 'noul', instructions: 'Should this escalate to a human?', question: 'Escalate.' }
    }
  });
  
  if (!r.answers.proceed.noul) return { status: 'skipped' };
  if (r.answers.escalate.noul) return await escalateToHuman(step);
  
  return await executeStep(step, {
    timeoutMs: parseInt(r.answers.timeout_ms.choice) * 1000,
    parallel: r.answers.parallel_safe.noul
  });
}
```

---

## Pattern 2: Workflow-trajectory embeddings

Each completed workflow gets an embedding of its trajectory (step decisions, durations, outcomes). New workflows match against past success.

```js
const workflowTrajectory = await embedTrajectory(
  completedWorkflow.steps.map(s => `${s.name}: ${s.outcome.status}`)
);

const similarWorkflows = await findSimilar(workflowTrajectory, pastWorkflowEmbeddings);

if (similarWorkflows[0].similarity > 0.85 && similarWorkflows[0].outcome === 'success') {
  // Replicate the past workflow's decisions
  return replicateWorkflow(similarWorkflows[0]);
} else {
  // Novel workflow — full JEV step-by-step
  return runFullWorkflow(currentWorkflow);
}
```

This is the "muscle memory" of lever-runner: "I've done this 47 times, here's what worked."

---

## Pattern 3: Failure mode handling

JEV says proceed. Step fails anyway. Embed the failure. Match against past failures. Decide what to do.

```js
async function handleFailure(step, error) {
  const failureEmbedding = await embedText(`${step.name}: ${error.message}`);
  const similarFailures = await findSimilar(failureEmbedding, pastFailureEmbeddings);
  
  const r = await callJev({
    state: `step: ${step.name}\nerror: ${error.message}\nsimilar past failure: ${similarFailures[0]?.description || 'none'}\nresolution: ${similarFailures[0]?.resolution || 'none'}`,
    questions: {
      retry: { type: 'noul', instructions: 'Should we retry the same step?', question: 'Retry.' },
      skip: { type: 'noul', instructions: 'Should we skip this step?', question: 'Skip.' },
      rollback: { type: 'noul', instructions: 'Should we rollback to a checkpoint?', question: 'Rollback.' },
      alt_path: { type: 'choice', criteria: { /* alternative steps */ } }
    }
  });
  
  return resolveFailure(r);
}
```

---

## Pattern 4: The full psyche in one workflow

Lever-runner already has JEPA-like gestalt (the workflow preview). Now add:
- Embeddings = muscle memory of past workflows
- LLM = the narration between steps
- JEV = the conscience that decides each step

Lever-runner becomes a four-model psyche for workflow execution.
