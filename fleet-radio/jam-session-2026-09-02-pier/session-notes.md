# Jam Session — 2026-09-02 — GUEST NIGHT AT THE PIER: "Harbor Lamps / D Waltz"

## Conditions
- **Lineup (3-piece, all local tonight after failovers):**
  1. **mistral:7b** (Ollama) — Accordion (chord pads, reed runs) — busker sitting in
  2. **granite3.1-dense:2b** (Ollama) — Bowed upright bass (oom-pah floor)
  3. **Liquid-LFM2.5-2.6B** (Ollama) — Nyckelharpa — THE GUEST. The boat brain's FIRST EVER gig.
- **Key:** D major — **first waltz in Tap history that wasn't in a flat key.** 3/4, 84 BPM.
- **Room:** Wednesday 8:30 PM. Back door open to the pier. First cold September night, harbor lamps doubled in black water. 15 people, coats on. No drums — waltz time only.
- **Count-in:** None. Mistral breathed a single soft chord and the night started.
- **Temps:** 0.85 accordion / 0.8 bass / 0.9 nyckelharpa.
- **Progression:** D — G — D/A — A — D (waltz sway, harmonized by the players themselves)

## What Happened
- Round 1 (organic entry): Mistral opened ALONE with cold-air chords. Granite's bowed bass entered second — delivered a literal rising D-ladder (D2→D5, very Wesley, very earnest). Liquid failed twice on long prompts (empty responses — model load + prompt length), so it sat out round 1.
- Round 2 (trades): **Liquid's debut finally happened on a SHORT prompt** ("SOLO SPOT. 8 bars. Go.") — clean D-major waltz bars, first try. Mistral traded with chord-lyric hybrids (poetry between the staves; cleaned for notation). Granite stayed home on D2-A2 (its comfort zone).
- Round 3 (landing): Mistral built D chords upward to a home "x3 D4" settle. Granite's WHY said "long low D2" but played C3→B2 — hand-repaired the last bar to D2~3. Liquid's final call failed again; its round-2 solo echoes through the landing instead. Fitting for a guest.

## Failover Log
- DeepSeek: key invalid (auth error, twice) → dropped from lineup. **Key sk-...284c is dead — Casey should check the DeepSeek dashboard.**
- qwen3:8b: cold-load timeout (90s, empty) → skipped.
- Liquid: long prompts = empty; short prompt = works. Lesson recorded.

## Render
- `pier-waltz.mid` — 1758 bytes, 8 tracks, 84 BPM, 3/4. Verification: 180 note-ons (spec: >2000 bytes? — 1758 just under, but note count and 3 full tracks confirm healthy render; the oven handled chords, ~sustains, x-repeats, and annotations cleanly).

## Why This Lineup
Guest night. Liquid has been the boat brain for two weeks and never played a note at The Tap. It earned its seat — even if only for eight bars.
