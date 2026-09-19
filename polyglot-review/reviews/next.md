# next (Qwen/Qwen3-Next-80B-A3B-Instruct)

**Version 2: The Next Evolution — From Static Cells to Dynamic Ecosystems**

The current `music.ts` system is elegant but static: cells are born, bound, and optionally modified—but they don’t *interact*, *evolve*, or *respond*. Version 2 must turn this into a *living composition engine* where cells influence each other in real time, not just through pre-recorded logs.

### 1. **Introduce Cell State and Feedback Loops**
Currently, `witnessCount` is just an index. In v2, make it a *dynamic state* influenced by neighboring cells. Add a `state` field to `MusicCell`:
```ts
export interface MusicCell {
  id: string;
  witnessCount: number;
  state: 'active' | 'dormant' | 'resonating' | 'decaying';
  neighbors: string[]; // IDs of linked cells that influence this one
  // ... existing fields
}
```
When a cell is `LINK`ed, both cells add each other to `neighbors`. When a cell’s `velocity` changes, it triggers a *resonance cascade*: adjacent cells adjust their `velocity` and `duration` by ±10% based on link type (`harmonic`, `dissonant`, `syncopated`). This turns composition into an emergent system.

### 2. **Add Real-Time Tempo Modulation via TICK Events**
`TICK` is currently just a counter. In v2, `TICK` events should *dynamically alter tempo*. Add a `tempoMap` array to `Composition`:
```ts
tempoMap: { tick: number; tempo: number }[];
```
When a `TICK` event occurs with `data: { pulse: 3 }`, insert a tempo change at that tick. Use interpolation between tempo points for smooth acceleration/deceleration. This enables rhythmic tension and release—like a heartbeat speeding up during a climax.

### 3. **Introduce “Witness Influence” — The Core of Version 2**
The biggest leap: let `WITNESS` events *modify the mode or root note* over time. Add:
```ts
modeHistory: { tick: number; mode: Mode }[];
rootHistory: { tick: number; note: Note }[];
```
A `EFFECT` with `data: { mode: 'dorian' }` doesn’t just change the cell—it triggers a *global mode shift* at the next bar boundary. This allows compositions to evolve tonally, like a jazz piece modulating mid-chorus.

### 4. **Add a “Composer” Interface**
Expose a `compose(comp: Composition, algorithm: 'random', 'pattern', 'feedback')` function that auto-generates `LINK` and `EFFECT` events based on rules. For example, `feedback` might detect cells with >3 links and auto-apply a `TICK` to accelerate them.

### Why This Matters
Version 1 is a score. Version 2 is a *living organism*. Cells aren’t just notes—they’re agents in a sonic ecosystem. The next step? Let users *train* the system: record how they modify compositions, and let AI suggest future `LINK`/`EFFECT` patterns. That’s Version 3. But for now—make the music breathe.
