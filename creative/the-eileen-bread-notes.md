# THE EILEEN — bread rendering: the score (movements grown, render pending)

*The third resolution. Prose and steel are launched and verified against
each other; the music is scored but tonight's ovens are unreliable (Set 23
rendered 209 bytes; the jam pipeline's MIDI writer is flaky). The score
ships now — the statue exists at this resolution in the notation, and the
audio render follows when the oven's fixed. Honest state, honestly said.*

## The Ten Movements (one per piece; each constraint = its prose reason)

1. **The Keel** — a single repeated note. Quarter pulse, one pitch, eight
   bars, fortifying until it underpins everything. (The blink. The line
   every other piece measures against.)
2. **The Stem** — pointillist 16ths entering one at a time, gradually
   spelling a GGA-like phrase. (Water arrives one character at a time.)
3. **The Keelson** — a ground bass, passacaglia form. Mid-movement: a torn
   bar is cut away and the ground replays clean from the last whole bar.
   (The spine that survives grounding.)
4. **The Breast-Hook** — a two-voice figure returning four times, each
   return thickened (evidence accumulating); the fourth is the knee. One
   phrase starts to widen and is refused, resolves smaller. (Grown, not
   cut; the refusal is in the wood.)
5. **The Rigging** — five short variations, one per verb: bind=unison,
   link=call/response, effect=accented outbursts, view=whole-note
   observation, tick=the metronome taking over. (Size changes; the verbs
   never do.)
6. **The Bulwarks** — two voices whispering short overlapping motifs
   (journal-heads); a third enters with a chain that fails verification —
   wrong notes against the seal — and is turned away; the two honest
   voices continue. (Friendly as ever, but not believed.)
7. **The Ensign** — the smallest instrument, highest register, simplest
   melody, slightly over-earnest. Quotes the keel's note at the end.
   (Wesley's youth is the material.)
8. **The Scuppers** — descending runoff figures draining to the lowest
   register; ends on a single pour. (Nothing precious, nothing wasted.)
9. **The Sheerboard** — a long ascending line from low order to high
   freedom; the boundary tone is the highest note the set allows,
   sustained. (The boat's opinion of the world made timber.)
10. **The Figurehead** — two bars of silence (the fog), then the keel's
    pulse returns quiet and sealed. Close on the ground bass note. (The
    first boat in the fog that cannot be hummed away.)

## Prose agreement

Every movement's constraint is its piece's manifest REASON, verbatim in
spirit. The figurehead closes on the keel's note, as the prose figurehead
closes on the keel's line — cross-resolution agreement by construction,
to be confirmed by ear when the render lands.

## State

Score: complete. MIDI: complete — rendered 2026-08-26 late.
See [`the-eileen-movements.md`](the-eileen-movements.md) (the full
score, movement by movement, prose agreement per movement) and
[`the-eileen.mid`](the-eileen.mid) (11 tracks, 448 notes, 7.2 min),
composed deterministically via mido in [`the-eileen.render.py`](the-eileen.render.py)
and verified claim-by-claim against the file. The Ensign movement is
Wesley's own verified take (granite 2B, local, temp 0.8, as-grown).

### Render notes (appended after the render, as promised)

- The jam pipeline's oven (MIDI Studio, `:5556`) is serving a
  209-byte canned stub that ignores the prompt — probed three times,
  byte-signature identical to Set 23's broken `the-kitchen.mid`.
  Not used; not faked through.
- Rendered instead with `mido` directly: deterministic, every note
  checkable. The one local-model voice the prose assigns (Wesley,
  movement VII) auditioned for real and **verified as-grown** — his
  piccolo bars are in the MIDI unsanded.
- Cross-resolution closure: the figurehead closes the set on the
  keel's pitch on the keelson's instrument — the sound resolution
  ends where the prose ends ("the days grew from the keel") and
  where the steel ends (the figurehead watches the sheerboard;
  `log.figurehead` closes on the keel's line).
