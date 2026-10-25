# Quilt — Pattern Examples

*The cellular substrate as a four-model psyche.*

---

## What changes

The 11 opcodes don't change. The cells don't change. The lattice doesn't change.

What changes is **who decides** each opcode. The cell decides. JEV certifies.

---

## Pattern 1: Each cell carries a 4-model psyche

```js
class Cell {
  constructor(coord, kind) {
    this.coord = coord;  // (x, y, z, t)
    this.kind = kind;
    // The psyche layers
    this.jepa = new JEPAGestalt();  // gestalt recognition
    this.embeddings = new EmbeddingMuscleMemory();  // trajectory-aware memory
    this.llm = new VerbalNarrator();  // for explanation
    this.jev = new SchemaBoundConscience();  // for decisions
  }
  
  async decide(opcode, args) {
    // JEPA: "looks like X"
    const gestalt = await this.jepa.gestalt({ opcode, args });
    
    // Embeddings: "trajectory matches Y at 0.87"
    const memory = await this.embeddings.match({ opcode, args, gestalt });
    
    // LLM: "X is the answer because..."
    const narration = await this.llm.narrate({ opcode, args, gestalt, memory });
    
    // JEV: "I agree. Schema: ... Decision: ... Confidence: ..."
    const decision = await this.jev.decide({
      schema: OPCODE_SCHEMAS[opcode],
      state: narration
    });
    
    return {
      opcode,
      args,
      psyche: { gestalt, memory, narration, decision },
      sigma: agreementMass({ gestalt, memory, narration, decision })
    };
  }
}
```

---

## Pattern 2: The 4-witness witness log

```js
class WitnessLog {
  async record(event) {
    const jepa_witness = await jeWitness(event);  // gestalt confirmation
    const embedding_witness = await embeddingWitness(event);  // trajectory match
    const llm_witness = await llmWitness(event);  // verbal narration
    const jev_witness = await jevWitness(event);  // schema-bounded verification
    
    const sigma = Math.sqrt(
      jepa_witness.confidence * 
      embedding_witness.confidence * 
      llm_witness.confidence * 
      jev_witness.confidence
    );
    
    const entry = {
      event,
      witnesses: { jepa_witness, embedding_witness, llm_witness, jev_witness },
      sigma,
      timestamp: this.latticeTime()
    };
    
    this.entries.push(entry);
    return entry;
  }
}
```

`sigma` is the AGREE-MARK agreement mass. 4-witness signed events.

---

## Pattern 3: FORGET becomes principled

Today, FORGET is an opcode. With JEV, FORGET becomes a principled decision:

```js
async function maybeForget(cell, witnessEntry) {
  const r = await jevDecide({
    state: `cell: ${cell.id}\nwitness entry sigma: ${witnessEntry.sigma}\nage: ${witnessEntry.age}`,
    questions: {
      should_forget: {
        type: 'noul',
        instructions: 'Decide whether this witness entry should be forgotten.',
        question: 'Forget this entry.'
      },
      retention: {
        type: 'score',
        criteria: ['ephemeral', 'short', 'medium', 'long', 'permanent']
      }
    }
  });
  
  if (r.answers.should_forget.noul > 0.7) {
    cell.witnessLog = cell.witnessLog.filter(e => e !== witnessEntry);
  }
  
  return {
    sigma: r.answers.should_forget.confidence,
    retention: r.answers.retention.score
  };
}
```

The substrate now has a principled forgetting mechanism. Memory becomes curated, not just accumulated.

---

## Pattern 4: Trajectory-shape cells

Each cell's identity is the dμ of where it has been, not where it sits now.

```js
async function cellTrajectory(cell) {
  // Embed the cell's history of state-changes
  const states = cell.history.map(h => h.state);
  const r = await embedTrajectory(states);
  return r.tangent_dmu;  // the cell's identity-as-going
}

async function findSimilarCells(cell, allCells) {
  const traj = await cellTrajectory(cell);
  const matches = await findSimilar(traj, await Promise.all(allCells.map(cellTrajectory)));
  return matches;
}
```

Two cells match if their *trajectories* are similar, not if their current contents are similar.

This is the substrate as a graph of trajectories, not a graph of states.

---

## Pattern 5: World and Time as first-class witnesses

WORLD and TIME opcodes — the rarest in the 42-function decomposition — become valuable because they're the only opcodes that touch the dμ:

- WORLD = "what world am I in?" → embedding match against the dμ of world-state
- TIME = "when am I?" → embedding match against the dμ of lattice-time

WORLD and TIME were 0/42 in the JEV decomposition. With the four-model psyche, they become the most-used opcodes.
