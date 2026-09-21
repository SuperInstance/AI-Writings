# fast (deepseek-ai/DeepSeek-V4-Flash)

## Fast Review: `cell.music`

**What it is**: A functional music composition engine where each beat (cell) derives its note from a witness count. Think cellular automata meets MIDI.

**Strengths**:
- Clean type system with explicit `Note`, `Mode`, and `Witness` types
- `cellNote()` uses frequency matching instead of naive interval mapping — good for microtonal flexibility
- `bindCell()` auto-increments `tickCount` and timestamps, making sequencing deterministic
- Witness log pattern enables full audit trail per cell

**Critical Issues**:

1. **`cellNote()` is O(n²) on every call** — loops through 7 notes × 7 octaves with log2 math. For a 120 BPM track at 4/4, that's 480 frequency searches per minute. Cache the note-octave mapping per mode.

2. **`Date.now()` in cell ID** breaks reproducibility. Use `comp.tickCount` instead — composition playback should be deterministic.

3. **Floating point drift** in `duration: 60000 / comp.tempo / 4` — accumulate ticks as integers, convert to ms at render time.

4. **Missing `EFFECT` and `TICK` implementations** — the code cuts off mid-function. `effectCell` references `comp.t` which doesn't exist on `Composition`.

5. **`witnessCount` vs `cells.length`** — these diverge if cells are ever removed. Pick one source of truth.

**Concrete fixes**:
- Precompute `noteCache: Map<string, {pitch, octave}>` keyed by `witnessCount-mode-rootNote`
- Replace `Date.now()` with `comp.tickCount`
- Change `duration` to `tickDuration = 4 * 60 / tempo` (in beats per minute, stored as integer ticks)

**Verdict**: Solid foundation, needs perf optimization and completion before production use. The witness pattern is elegant for DAW-like undo/redo.
