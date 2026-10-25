# Jam Session — 2026-08-29 — THE BREAKWATER (storm-swell night)

## Conditions
- **Venue:** The breakwater behind The Tap, storm-swell rolling in from the Gulf. Saturday 8:30 PM.
- **Lineup (4-piece, one local):**
  - **Hermes-3-405B** — Fog Bell (sparse, high, patient)
  - **gemma-3-27b-it** — Driftwood Marimba
  - **Qwen2.5-72B** — Conch-Shell Horn (long wailing tones)
  - **mistral:7b** (Ollama local) — Rain-Barrel Surf Drum (low register, D2 wave-smack)
- **Key:** F# natural minor. **Tempo:** 76 BPM, 4/4, "the ocean drags."
- **Temperature:** 0.85–0.9 (wild-ish)
- **Rule of the Swell:** every phrase rises, then falls.
- **Count-in:** Organic/staggered — surf alone bar 1, bell bar 3, marimba bar 5, horn bar 7.
- **Round 3:** land on F# (any octave) or rest; last wave out.

## What happened
- 11 of 12 takes clean on first pass. Bell round 2 came back with only 3 BAR lines → single targeted retry fill succeeded (8 bars).
- mistral:7b (surf) overplayed r1 (21 bars) — trimmed to 8; later rounds mostly self-corrected.
- Players used sparse notation ("F#4..." one note per bar) — breakwater texture is intentionally wide open.

## MIDI fix (second one this week)
- notation2midi silently dropped every note followed by "..." (e.g. "F#4..."). Patched in place: token base now `.rstrip('.')`. the-breakwater.mid: 1111 bytes, 94 note-ons across 96 bars — sparse but real (4 players, lots of rests by design; density ≠ quality tonight).

## Files
- r{1,2,3}-{surf,bell,marimba,horn}.txt, jam.py, the-breakwater.mid
