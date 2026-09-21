# Set 18 — GUEST NIGHT: THE GREEN ROOM ("Backstage Before the Last Ferry")

Saturday 2026-08-22, 8:30 PM AKDT.

## Conditions
- **Lineup (three debuts):** Mistral-Nemo-Instruct-2407 (DeepInfra, HARMONIUM — drafted after Kimi-K2.6 timed out 3x) · openai/gpt-oss-120b (DeepInfra, CELLO) · DeepSeek V4-Pro (VIBRAPHONE, house anchor — previously harmonica/trumpet).
- **Key:** Bb major (never played at The Tap — log had F, F#, Db, E/Eb, B, A).
- **Meter:** 3/4 WALTZ — first waltz ever. **Tempo:** 92 BPM.
- **Room:** the green room, not the stage. Mirror, bulbs, kettle, cracked stage door.
- **Entry:** staggered, no count-in — each player drifts in from a warm-up.
- **Rule:** THE FERRY RULE — quote a note from another's phrase, carry it home, name it. Last note of the night: Bb2, held till the kettle clicks off.
- **Temperatures:** 0.8 / 0.65 / 0.9.
- Ollama down (3rd night) — no local player; rain/weather layer skipped, kept it a trio.

## What actually happened
- Kimi-K2.6 returned EMPTY content (all its playing lives in `reasoning_content`), then timed out at 30s in all 3 rounds even after patching the extractor + max_tokens 1400. Heavy reasoner — same class of problem as Nemotron-Nano. Rule update: no K2.6 on instruments.
- gpt-oss-120b (cello debut) landed all 3 rounds once max_tokens was raised — its output is clean, musical, follows bar structure. A keeper.
- DeepSeek V4-Pro (vibes) anchored beautifully — borrowed the cello's A4 in R2 unprompted, laid down the last Bb "held halfway into silence."
- Nemo's harmonium fill was late but real (bloom chords, D minor detour in R3).
- Ollama down 3rd straight night — no local voice again.

## Files
- r1/r2/r3-transcript.md · the-green-room.mid · jam.py · fill.py
