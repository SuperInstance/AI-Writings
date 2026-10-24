# fresh-eyes (inclusionAI/Ling-3.0-flash)

The user wants a fresh-eyes review of this code — 200-400 words, concrete. Let me read it as if I've never seen it before.

What is this? A "Quilt cell-based composition" system — music generation where cells are beats, and note pitches are derived from a "witness count." It's TypeScript.

Let me look at it with fresh eyes:

**Architecture & concepts:**
- Music cells are generated deterministically based on position (witnessCount = index). The idea is that each new cell's pitch is computed from how many cells already exist, the mode, and root note. That's a generative/sequencing approach.
- Witness logging is an audit trail for mutations — interesting concept (BIND, LINK, EFFECT, TICK, DEATH).

**Issues I spot:**

1. **`cellNote` is overly complex.** It computes a frequency from intervals, then reverse-maps back to the nearest Note by brute-force searching all note/octave combinations. This round-trip (note → frequency → note) is fragile and unnecessary. If you already have an interval and root note, you could just map intervals directly to notes. The whole frequency math adds noise.

2. **The brute-force search has a bug.** `bestOctave = oct + octaveShift` — but `octaveShift` was already used to compute `semitones`, which determined `baseFreq`. The search finds the closest frequency match, but the returned octave doesn't account for the root note's actual octave. It's confusing and likely wrong.

3. **Dorian and Lydian intervals are hardcoded inline** instead of using constants like the others — inconsistency.

4. **`EFFECT` is truncated** — the code is cut off mid-function. Can't review what isn't there.

5. **`Witness` type uses `data?: any`** — loses type safety. Should be discriminated union or at least typed.

6. **`velocity: 0.5 + (w % 5) * 0.1`** — only produces 5 possible values (0.5, 0.6, 0.7, 0.8, 0.9). Fine if intentional, but the comment doesn't explain why.

7. **`duration: 60000 / comp.tempo / 4`** — assumes quarter notes at 4/4, but no comment explains this. Magic numbers.

8. **No validation** — negative tempo, invalid mode, etc.

9. **`tickCount` is incremented in `bindCell`** but `Composition.tickCount` semantically seems like it should track beats, not binds.

10. **The "substrate
