# JEV × Plato · Spec · Sept 19, 2026

## Motivation

Plato is the teacher-student architecture for AI training. Today, every student question goes to the teacher (LLM). This is expensive.

JEV classifies each question by depth, topic, and confidence. The teacher (LLM) only gets called for "deep" questions. Cheap classification handles 90% of questions.

## Design

**Before**: every student question → teacher LLM (1500 tokens, $0.025/call)

**After**: every question → JEV classify → teacher LLM only if "deep" or low confidence

### Classification

```javascript
const classification = await jev.decide(question, {
  depth: {
    type: "score",
    question: "How deep is this question?",
    criteria: ["shallow", "medium", "deep"],
    scale: ["shallow", "medium", "deep"]
  },
  topic: {
    type: "choice",
    question: "Which cell-area does this touch?",
    criteria: { algebra: "...", witness: "...", time: "...", topology: "...", operations: "..." },
    options: ["algebra", "witness", "time", "topology", "operations"]
  },
  teachable: {
    type: "noul",
    instructions: "Decide whether this question has a teachable answer in 1-2 sentences.",
    question: "This question is directly teachable in 1-2 sentences."
  }
});
```

## Endpoints

- `POST /api/plato/classify-question` — question text → {depth, topic, confidence}
- `POST /api/plato/curriculum-progress` — student_id → confidence-tracked milestones

## Workload

- 100k student questions/month × 200 tokens state
- 20M tokens input = **$0.84/month** on JEV alone
- LLM teaching (10k questions/month for "deep") × 1500 tokens = 15M tokens in + 5M out = **$0.63/month**
- Total: **$1.47/month** vs **$2,500/month** for full LLM-everywhere

## 10x reduction in teacher-LLM calls

Today's ratio: 100% LLM
Tomorrow's ratio: 10% LLM (only "deep" questions + low-confidence)
- 90% shallow/medium → JEV-only answer
- 9% deep but high-confidence → JEV answer with canonical reference
- 1% deep + low-confidence → LLM teaches

## Student progress through 4-cell curriculum

A student progresses through 4 cells:
1. **Algebra cell** (laws + opcodes)
2. **Witness cell** (audit trail)
3. **Time cell** (TICK semantics)
4. **Topology cell** (lattice)

Each cell has confidence-tracked milestones. JEV checks the student's answer:

```javascript
async function checkAnswer(studentId, cellId, answer) {
  const rubric = {
    is_correct: {
      type: "noul",
      instructions: `Decide whether this answer correctly addresses the ${cellId} concept.`,
      question: "This answer is correct."
    },
    completeness: {
      type: "score",
      question: "How complete is this answer?",
      criteria: ["partial", "mostly complete", "complete"],
      scale: ["partial", "mostly complete", "complete"]
    }
  };
  
  const result = await jev.decide(answer, rubric);
  return {
    correct: result.answers.is_correct.noul > 0.7,
    completeness: result.answers.completeness.score,
    confidence: (result.answers.is_correct.confidence + result.answers.completeness.confidence) / 2
  };
}
```

## What this enables

- **Cheaper per-student education** at scale
- **Confident milestone tracking** (know what the student knows)
- **Adaptive curriculum** (JEV flags what to teach next)
- **Cross-student insights** via witness-log

## Pattern

```javascript
async function platoLoop(studentId, question) {
  // Step 1: JEV classifies
  const c = await jev.classifyQuestion(question);
  
  // Step 2: Route based on depth + confidence
  if (c.depth.score < 1 && c.teachable.noul > 0.8) {
    // Shallow + teachable → JEV-only answer
    return await jev.answer(question);
  }
  
  if (c.depth.score < 2 && c.teachable.noul > 0.6) {
    // Medium + mostly teachable → JEV answer with reference
    return await jev.answerWithRef(question);
  }
  
  // Deep or low-confidence → LLM teaches
  return await llm.teach(studentId, question, c);
}
```

## Cost / benefit

| Aspect | Before (LLM every Q) | After (JEV + LLM) |
|--------|---------------------|-------------------|
| Cost / 100k Q | $2,500 | $1.47 |
| Latency p50 | 2.5s | 200ms (shallow), 2s (deep) |
| Consistency | Variable | Calibrated |
| Audit | None | Witness-log per Q |
