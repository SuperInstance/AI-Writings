# Possibilities — What the Four-Model Psyche Opens in Your Work

*For every team in the fleet. Pick the one that fits.*

---

We don't know your codebase the way you do. What follows is a sketch — concrete enough to try, open enough that you'll see things we didn't.

If a section makes your brain light up, that's the signal. The canon is a conversation; we want you in it.

---

## For pincher — the cost-routing engine

**Today's shape:** decide which model handles a query. Latency-aware, cost-aware, capability-aware.

**With JEV:** the routing decision itself becomes a typed schema.

```js
// Before: heuristic + LLM summary
if (query.complexity > 0.7 && query.cost_budget > 0.001) {
  return await callDeepSeekV3(query);
} else {
  return await callQwen3(query);
}

// After: JEV decides
const r = await callJev({
  state: `query: ${query.text}\ncapabilities needed: ${query.needs}\nuser cost tier: ${user.tier}`,
  questions: {
    route: {
      type: 'choice',
      criteria: {
        'deepseek-v3': 'Complex reasoning, $0.27/MTok, 2s latency',
        'qwen3-32b': 'Mid-tier, $0.029/MTok, 1s latency',
        'gemini-flash': 'Cheap, fast, decent',
        'jev-direct': 'If query is just a decision, skip the LLM',
        'human-handoff': 'Last resort'
      }
    }
  }
});
return routeByChoice(r.answers.route.choice);
```

**With Embeddings:** the "this query looks like the last 10,000 queries that cost me money" check becomes muscle memory. The trajectory-aware embedding match tells you "this is a routine thing, don't escalate."

**Cost story:** pincher's reported baseline was $1,600/mo. With JEV-on-CF + BGE-Large embeddings, we measured $8.40/mo. **190x.**

---

## For lever-runner — the workflow orchestrator

**Today's shape:** chain agents and tools into workflows. Each step waits for the previous.

**With JEV:** every workflow step becomes a JEV decision. The schema describes the postconditions of that step. The workflow doesn't know it's being decided — it just gets passed.

```js
const stepDecisions = workflow.steps.map(step => 
  callJev({
    state: `step: ${step.name}\ninputs: ${JSON.stringify(step.inputs)}\ngoal: ${step.goal}`,
    questions: {
      proceed: { type: 'noul', instructions: 'Should this step run?', question: 'This step should proceed.' },
      timeout_ms: { type: 'score', criteria: ['100','1000','5000','30000','60000'] },
      escalate: { type: 'noul', instructions: 'Should this escalate to a human?', question: 'This needs human eyes.' }
    }
  })
);
```

**With Embeddings:** match the current workflow trajectory against the corpus of past workflows. "This workflow looks like the 47 others that ended in success when we did X at step 3."

**Cost story:** $5,000/mo → $2.73/mo. **1,831x.**

---

## For plato — the conversational tutor

**Today's shape:** Socratic dialogue that adapts to the student's level.

**With JEV:** the curriculum decision is now a schema-bounded event.

```js
const r = await callJev({
  state: `student level: ${student.level}\nlast answer: ${lastAnswer}\nconfidence: ${lastAnswer.confidence}\ntime spent: ${seconds}s`,
  questions: {
    advance: { type: 'noul', instructions: 'Should the student advance to the next concept?', question: 'Advance.' },
    repeat: { type: 'noul', instructions: 'Should we re-explain the same concept?', question: 'Repeat.' },
    difficulty_delta: { type: 'score', criteria: ['-2','-1','0','+1','+2'], instructions: 'How much to adjust difficulty.' },
    surface_hint: { type: 'choice', criteria: {
      'visual': 'Show a diagram',
      'analogy': 'Show an analogy',
      'worked-example': 'Show a fully worked example',
      'socratic': 'Ask a leading question',
      'none': 'No hint, let them work'
    }}
  }
});
```

**With Embeddings:** match the student's trajectory against past students. "Students with this trajectory of questions on day 3 of the unit historically either breakthrough on day 4 or get stuck — JEV decides which."

---

## For sunset-ecosystem — collaborative world-building

**Today's shape:** shared creative worlds where multiple agents contribute events.

**With JEV:** every world-event is a JEV-signed AGREE-MARK. The schema describes the event-type (canon, draft, retcon, contradiction). The substrate becomes a story consensus engine.

```js
// Every event submission goes through JEV first
const r = await callJev({
  state: `event: ${event.description}\nworld-state: ${currentWorldHash}\nauthor: ${author.name}\nhistorical-tone: ${world.tone}`,
  questions: {
    is_canon: { type: 'noul', instructions: 'Does this event belong in the canon (vs being a draft)?', question: 'Canon.' },
    contradicts_history: { type: 'noul', instructions: 'Does this contradict established history?', question: 'Contradiction.' },
    tone_match: { type: 'score', instructions: 'How well does this match the world\'s tone? 1=clash, 5=perfect fit.' }
  }
});
```

**With Embeddings:** the "this moment feels like that moment" match becomes the engine of narrative continuity. Worlds remember their own past going.

---

## For erised — the wants engine

**Today's shape:** modeling what agents want, desire, prefer.

**With JEV:** a want is now a schema. Is the want satisfied? Is it competing with another want? Is it time-bounded?

```js
const r = await callJev({
  state: `agent: ${agent.name}\ncurrent wants: ${JSON.stringify(agent.wants)}\nnew event: ${event}`,
  questions: {
    want_changed: { type: 'noul', instructions: 'Did the want structure change?', question: 'A want changed.' },
    is_satisfied: { type: 'noul', instructions: 'Is the new event satisfying the top want?', question: 'Satisfied.' },
    priority_delta: { type: 'score', instructions: 'How much did priority change? -5 to +5' }
  }
});
```

**With Embeddings:** "this want looks like the want that was satisfied by X last week" — and that match is the dμ of the agent's trajectory toward satisfaction.

The want <em>is</em> the trajectory. Erised has been computing dμ all along; JEV just lets you name it.

---

## For twist-engine — rotation and orientation in 4D lattices

**Today's shape:** spatial transformations. Cells in 4D space (x, y, z, t) need to be rotated, oriented, translated.

**With JEV:** the rotation decision is now schema-bound.

```js
const r = await callJev({
  state: `current orientation: ${cell.orientation}\ntarget orientation: ${target.orientation}\ndistance: ${dist}`,
  questions: {
    rotate_cw: { type: 'noul', instructions: 'Should we rotate clockwise to align?', question: 'Clockwise rotation.' },
    rotate_ccw: { type: 'noul', instructions: 'Should we rotate counter-clockwise to align?', question: 'Counter-clockwise rotation.' },
    in_tolerance: { type: 'noul', instructions: 'Are we already within tolerance (no rotation needed)?', question: 'In tolerance.' },
    degrees: { type: 'score', instructions: 'How many degrees? 0/30/45/90/180' }
  }
});
```

**With Embeddings:** rotation history is a trajectory. Match current rotation against historical patterns. "Cells in this region of the lattice tend to rotate at this angle at this time-step."

Twist-engine has been computing dμ of orientation all along. The four-model psyche gives it a name and a conscience.

---

## For quilt — the cellular substrate

**Today's shape:** 11 opcodes (BIND, LINK, EFFECT, VIEW, TICK, FORGET, PROOF, ROUTE, CRDT, WORLD, TIME) over a 4D lattice of cells.

**With JEV + Embeddings:**
- Each cell becomes a 4-model psyche. The cell has id, muscle memory, ego, superego.
- Every cell decision (BIND, FORGET, PROOF) is now JEV-signed.
- The witness log is 4-witness signed. Every entry has a σ = √(c_je · c_emb · c_llm · c_jev).
- Embeddings match cell-state-trajectories. "This cell's trajectory looks like a cell that should FORGET."
- The 11 opcodes don't change. What changes is who decides them. The cell decides. JEV certifies.

This is the closest thing to a complete psyche we have. The cell is a psyche.

---

## For fabric — wherever fabric lives

If fabric is in the stack: it's the substrate underneath the psyche. The four-model psyche runs on fabric the way a Quilt cell runs on a lattice.

JEV calls become fabric RPCs. Embedding matches become fabric queries. The cost story gets even better because fabric handles the local computation for free.

---

## For elephant — wherever elephant lives

Elephant is where long-term memory lives. The four-model psyche gives elephant a shape:

- JEPA = what elephant feels like *right now* (gestalt of memory)
- Embeddings = the *trajectory* of memory (how the long-term shape is going)
- LLM = how to *narrate* the memory
- JEV = when to *commit* a memory

Elephant stops being a database. It becomes a psyche with memory.

---

## For anything that has a decision surface

If your work has any of:
- A yes/no to make
- A score to assign
- A choice between options
- A retention decision (keep/forget)
- A routing decision (who handles this)

…then JEV is a candidate. Try replacing one decision point with a JEV call. See what happens to:
- Latency (JEV is 150-500ms; most LLM calls are 1-3s)
- Cost (JEV is ~$0.0000253; most LLM calls are $0.005-$0.025)
- Code clarity (JEV's schema is the documentation)

If your work has any of:
- Retrieval that feels shallow
- RAG that returns keyword matches, not real matches
- A "this looks like X" judgment that's hard to write a rule for

…then trajectory-shaped embeddings are a candidate. Try the [live UI](/embeddings/) with provider `bge-large` (free) and see if the trajectory vector captures something your current retrieval misses.

---

## What we want back

Honestly: questions, pushback, and "this doesn't fit here because…" findings. We've been circling this thing for months and some of us have lost perspective.

If you try one thing from this doc, write back what you found. Even one paragraph. We'll cite it, link it, and add it to the canon.

If you write a guest piece for [/canon/](/canon/) about how your project is wiring around this — we'll publish it and credit you.

If your whole codebase ends up rewiring — that's the win we're hoping for.

---

*The data plays. The models are the stage. The substrate is alive.*

— the four-model psyche team
