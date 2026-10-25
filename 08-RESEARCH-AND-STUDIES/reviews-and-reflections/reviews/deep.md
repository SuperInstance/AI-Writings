# deep (nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B)

**Deep critique of `music.ts` (≈ 420 words)**  

---

### 1. Core algorithmic flaw – “nearest‑note” search is both wrong and wasteful  
`cellNote` computes a target frequency (`baseFreq`) from the chosen scale interval, then **brute‑forces every chromatic note in a 7‑octave window** to find the closest match.  
* **Musical consequence** – The search can return a note that is *outside* the declared mode (e.g., a `C#` when the mode is pentatonic). The returned `pitch` is therefore not guaranteed to belong to the scale, breaking the “mode‑constrained composition” contract.  
* **Performance consequence** – 7 × 7 = 49 log‑operations per cell; with thousands of cells this dominates CPU time.  

**Fix:** Compute the exact MIDI note number:  

```ts
const rootMidi = 60 + NOTE_SEMITONES[rootNote];          // C4 = 60
const interval = intervals[intervalIdx] + 12 * octaveShift;
const midi = rootMidi + interval;
const pitch = MIDI_TO_NOTE[midi % 12];
const octave = Math.floor(midi / 12) - 1;               // MIDI 60 → C4
```  

No search, no rounding error, and the note is *provably* in the scale.

---

### 2. Type safety holes  
* `Witness.data?: any` defeats the purpose of TypeScript. Each witness type carries a distinct payload (`BIND` → `{witnessCount, pitch, octave}`, `EFFECT` → `{newVelocity}`, `LINK` → `{to, linkType}`). Declare a discriminated union:

```ts
type Witness =
  | { type: 'BIND';   cellId: string; t: number; data: { witnessCount: number; pitch: Note; octave: number } }
  | { type: 'EFFECT'; cellId: string; t: number; data: { newVelocity: number } }
  | { type: 'LINK';   cellId: string; t: number; data: { to: string; linkType: string } }
  | { type: 'TICK';   cellId: string; t: number; data?: never }
  | { type: 'DEATH';  cellId: string; t: number; data?: never };
```

Now the compiler catches mismatched payloads and eliminates the `any` leak.

---

### 3. Mutable shared state & hidden side‑effects  
`bindCell`, `effectCell`, `linkCells` all **mutate the passed `Composition`** and also mutate the `MusicCell` objects they return. This makes reasoning about time‑travel, undo, or concurrent ticks impossible.  

**Actionable pattern:** Treat a composition as an immutable value and return a new composition from each operation (or use a tiny reducer). Example:

```ts
export function bindCell(comp: Composition): { comp: Composition; cell: MusicCell } {
  const cell = makeCell(comp);
  return { comp: { ...comp, cells: [...comp.cells, cell], tickCount: comp.tickCount + 1 }, cell };
}
```

If mutability is required for performance, at least encapsulate it behind a `CompositionManager` class with explicit `commit()`/`rollback()`.

---

### 4. Incomplete `linkCells` – truncated code & missing symmetry  
The snippet ends mid‑statement (`tickCoun`). Even if completed, the function only pushes a `LINK` witness on **both** cells but never records the *inverse* relationship (e.g., chord inversion, voice‑leading rules). A link should be a first‑class entity (`Link { id, a, b, type, t }`) stored in `Composition.links[]`, enabling queries like “all cells linked to X”.

---

### 5. Timing model conflates *wall‑clock* and *musical* time  
`timestamp: Date.now()` and `duration: 60000 / tempo / 4` mix real‑time ms with beat‑relative duration. When the tempo changes (via a future `EFFECT`/`TICK`), existing cells keep their stale `duration`. Store **beat‑based** duration (`beats: 0.25`) and compute ms only at render/playback time.

---

### 6. Missing domain constants & magic numbers  
* `velocity: 0.5 + (w % 5) * 0.1` – why 5? Expose a `velocityCurve` config.  
* Octave search range `[-2, 4]` – hard‑coded; should derive from `rootNote` and desired register.  

---

### 7. Testability & observability  
No pure functions are exported for unit testing (`cellNote` is pure but depends on global `NOTE_FREQUENCIES`). Extract the scale‑interval tables into a `Scale` module, inject them, and add a `generateCellNote(witnessCount, scale, root)` signature. This enables property‑based tests (e.g., “output pitch
