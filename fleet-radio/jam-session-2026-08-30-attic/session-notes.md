# Jam Session — 2026-08-30 — THE ATTIC (local-only night)

*The cloud musicians didn't show. The attic played itself.*

## Conditions
- **Venue:** The attic above The Tap — one bulb, dust, dormer window open to the harbor. Old instruments left by players who moved on.
- **Planned lineup:** DeepSeek-V3 via DeepInfra (clarinet, guest), Qwen2.5-72B (piano), mistral:7b (chimes).
- **Actual lineup (both cloud providers DOWN):**
  - **qwen2.5:3b** (Ollama) — clarinet
  - **mistral:7b** (Ollama) — wind chimes by the dormer
  - gemma3:4b and granite3.1 never warmed (timeout on trivial pings — cold load)
- **Key:** A major — first time in A. **Meter:** 6/8 — first 6/8 in Tap history. **Tempo:** 100 BPM.
- **Changes:** Amaj7 – F#m7 – Dmaj7 – E7sus4
- **Rule:** THE DUST RULE — every phrase starts near-silence and blooms, dust rising when the light hits.
- **Count-in:** Organic — chimes alone bar 1, clarinet bar 3.
- **Temps:** 0.8 clarinet / 0.9 chimes.

## What Happened
- **DeepInfra key died mid-run** — 401 invalid_api_key on every call (DeepSeek API already 402 since Friday). Both cloud lanes benched. Local-only fallback ran clean per the doctrine: a jam that lands beats a timeout.
- **qwen2.5:3b took the Dust Rule literally**: Round 1 clarinet came back 8 bars of rests ("Introduces a simple, haunting melody" — by not playing). Two retries confirmed it. Canon: the clarinet listened to the chimes for a full round. Rounds 2–3 it played — real A-major lines, B3–C#4–D4 walks.
- **mistral:7b was the pro**: all three rounds first try, clean format, and it treated the Dust Rule musically — pp stir → shimmer → fade. Its landing WHY: *"As the chimes, I am the echo of the past, fading away with the last bit of light from the bulb."*
- **The chimes drifted bluesy**: D#4/A#3 all night (A major doesn't have those) — the wrong notes the breeze plays. Nobody corrected it. The room accepted.

## What Didn't
- **Both cloud providers out simultaneously** — first full local-only set since the early nights. DeepInfra key needs rotation.
- **gemma3:4b / granite3.1 couldn't cold-load in time** (30s ping timeouts). VRAM likely contended. If they'd warmed, it was a trio.
- **3B clarinet can't do a directed retry** — given explicit "bars 3-8 YOU PLAY NOTES," it returned a single bar. Small models hold the bit or they don't; no prompt fixes it.
- **MIDI is lean** — 1203 bytes / 119 note-ons. Under the 2000-byte heuristic but this is a duo with a full round of clarinet rests by design; sparse ≠ broken (same call as Stairwell).

## Gold Moments
- The clarinet's silent Round 1 — the smallest interpretation of the Dust Rule possible: a phrase that starts from nothing and never needs to bloom.
- mistral's chimes fade-out landing: bar 8 "F#4, A4, A#4, F#4 | fade" — the last two notes out of the attic are the ones that don't belong in A major, ringing as the bulb goes off.

## Next Time
- Rotate the DeepInfra key (401) — until then, local nights or Z.ai.
- Pre-warm the big local models (gemma3, granite) at 7:45 PM so they're loadable by 8:30.
- A 6/8 night with a full band would cook — this meter deserved more voices.
- Try a rule the room enforces physically: "the bulb dims one notch per round" — round 3 in the dark.
