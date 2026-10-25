# Quilt As JEV Target

> Quilt's cells ARE the targets and outputs of JEV verdicts. Bidirectional.

## The Bidirectional Pattern

JEV operates on Quilt cells in both directions:

**JEV → Cell**: JEV sends a verdict to a cell.
- Cell receives: new state, new witness, new BIND, or new FORGET
- Cell updates: its state vector reflects the verdict
- Cell records: the verdict in its witness log

**Cell → JEV**: Cell sends state to JEV for validation.
- JEV receives: the cell's current state + witness log
- JEV returns: a verdict (BIND/PROOF/FORGET, with confidence)
- Cell records: the verdict as a new witness entry

The pattern is **bidirectional**: JEV and cells talk to each other in both directions.

## The Cell Schema

Each cell has a JEV-compatible schema:

```typescript
interface CellSchema {
  id: string;
  state_type: 'string' | 'int' | 'float' | 'vector' | 'json' | 'binary';
  output_type: 'string' | 'int' | 'float' | 'vector' | 'json' | 'binary';
  hooks: Hook[];
  drops: Drop[];
  jev_schema: ChoiceSchema | ScoreSchema | NoulSchema;
  witness_log: WitnessEntry[];
  proof_chain: ProofEntry[];
  scars: ScarEntry[];
}

interface Hook {
  source: string;  // cell id or external
  condition: string;  // JEV-validated condition
}

interface Drop {
  target: string;
  confidence_threshold: number;
  wake_condition: string;
}

interface WitnessEntry {
  ts: string;
  opcode: 'WITNESS' | 'PROOF' | 'BIND' | 'FORGET' | 'TICK';
  value: any;
  jev_confidence: number;
  source: string;
}

interface ProofEntry extends WitnessEntry {
  proof_chain_hash: string;
  validated_by: string;
}

interface ScarEntry {
  ts: string;
  reason: string;
  jev_confidence_at_time: number;
  recovered: boolean;
}
```

This is the schema. JEV operates against it.

## Example: Cell Routing

```python
# User sends message: "play chess"

cell_message = {
  "id": "msg-12345",
  "content": "play chess",
  "source": "user-input"
}

# JEV decides where to route
jev_verdict = jev.decide(
  schema={
    "type": "Choice",
    "options": [
      "chess-player-cell",
      "holdem-player-cell",
      "general-game-cell",
      "drop"
    ]
  },
  context=f"User said: {cell_message['content']}",
  state=current_cell_states
)

# Verdict: "chess-player-cell" at 0.92 confidence
# Cell receives the message
chess_cell.receive(cell_message, jev_verdict)

# Chess cell BINDs to the user's session
chess_cell.bind_to_session(user_session, jev_verdict.confidence)

# Witness log records the event
chess_cell.witness_log.append({
  "ts": now(),
  "opcode": "BIND",
  "value": {"session": user_session.id, "game": "chess"},
  "jev_confidence": jev_verdict.confidence,
  "source": "user-input"
})
```

## Example: Tone Shaping

```python
# NPC response candidate
response = "I will destroy you in this game."

# Tone vectors
desired_tone = {
  "compassion": 0.3,
  "authority": 0.8,
  "humor": 0.1,
  "formality": 0.6
}

# JEV evaluates tone
tone_verdicts = {}
for dim, target in desired_tone.items():
  tone_verdicts[dim] = jev.score(
    candidate=response,
    rubric=f"How {dim} is this response? Target: {target}. Score 0-1."
  )

# Average tone deviation
avg_deviation = sum(abs(v - target) for v, target in tone_verdicts.items()) / len(desired_tone)

# If deviation > threshold, regenerate or rewrite
if avg_deviation > 0.2:
  response = rewrite_response(response, tone_verdicts, desired_tone)

# Cell outputs the final response
npc_cell.output(response, jev_verdict=tone_verdicts)
```

## The Drop System (Deeper)

Drops are how cells propagate their state. A drop is:
- **Target cell**: where the output goes
- **Confidence threshold**: minimum JEV confidence required
- **Wake condition**: when this drop should fire
- **Type contract**: what kind of data flows through

Example:
```python
class Drop:
  def __init__(self, target, threshold=0.7):
    self.target = target
    self.threshold = threshold
    self.wake_condition = lambda state: state.confidence > threshold
    self.type_contract = "string"
  
  def fire(self, state):
    if self.wake_condition(state):
      return {
        "target": self.target,
        "value": state.value,
        "confidence": state.confidence,
        "type": self.type_contract
      }
    return None
```

A cell has many drops. Each drop has its own threshold + wake condition. The substrate **organically discovers** useful drops as cells find that talking to each other is beneficial.

## The Bookkeeper

Each cell has a **bookkeeper** that wakes up when:
- A drop fires
- A new witness arrives
- A BIND is requested
- A FORGET is requested
- A TICK advances time

The bookkeeper runs a process:
1. Validate the event (via JEV)
2. Update the cell's state
3. Decide which drops to fire next
4. Schedule the next wake

This is **the cell's local loop**. It's what makes cells "alive" — they have their own agenda, not just passive data structures.

## The Cross-Instance Fabric

When cells are in different instances, the fabric:
1. Routes the drop through JEV verdicts
2. Signs the value with the witness log
3. The receiving cell hooks the value
4. The receiving cell's bookkeeper wakes up
5. The bookkeeper runs its process

The fabric is **the substrate's nervous system**. It carries signals between cells, regardless of where they live.

## The Quilt-JEV Conclusion

Quilt cells are not data structures. They are **neurons with witness logs**. JEV is the synapse. The substrate IS a neural network — but a calibrated, schema-bounded, auditable one.

This is what makes the cellular-first design **world-class**: every component has a clear role, every decision is traceable, every cell is alive.

The substrate teaches itself. The cells are the students. JEV is the teacher. The witness log is the textbook.
