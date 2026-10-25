# Set 19 — THE ALLEY ("The Door Between Two Rooms")
Sunday 2026-08-23, 8:30 PM AKDT.

## Conditions
- **Lineup:** Liquid-LFM2.5-2.6B (DEBUT — the new boat brain, handbells + conch, THE FOGHORN) · openai/gpt-oss-120b (returning cello→baritone sax, THE SAXOPHONIST) · DeepSeek chat (anchor, muted trumpet, THE NIGHT MANAGER) · granite3.1-dense:2b (THE JUKEBOX — through the wall, always Bb).
- **Key:** C major — first time EVER at The Tap (log: F, F#, Db, E/Eb, B, A, Bb).
- **Meter:** 12/8 slow shuffle (4+4+4) — first ever. **Tempo:** 60 BPM.
- **Venue:** the back alley — band outside facing the propped-open door, room playing back through the wall.
- **Rule:** THE DOOR RULE — every 4th bar, one player holds the door (near-silence) and the jukebox bleeds through in Bb.
- **Entry:** staggered, no count-in — the foghorn IS the count-in (r1 bar 1).
- **Temps:** 0.85 / 0.8 / 0.7 / 0.9.
- **Ollama UP for the first time in 4 nights** — Wesley and Liquid both local.

## What actually happened
- **Liquid-LFM2.5-2.6B (foghorn, debut):** agentic brain, terrible stage manners — leaked full chain-of-thought all three rounds, played a combined ~8 bars all night. Four prompt variants (hard strip, seeded first line, bar-extraction regex, temperature 0.7) all failed. Canon: the horn that thinks before it blows. Same banned-on-instruments class as Nemotron-Nano, Qwen3-32B, Kimi-K2.6 — add to the log's list. Its one landed line (R3, seeded): "all of you, one chord, the jukebox's Bb inside it, uncorrected."
- **gpt-oss-120b (sax):** strong again — clean 8-bar R1, borrowed flat (Bb3 in R3) named and carried home per the rule. One empty content field in R2 (reasoning_content present, content blank — flaky; a raw retry recovered it). Verdict: keep, but check content field.
- **deepseek-chat (trumpet):** rock steady, 3.5s a round. R2 quoted the foghorn's G2 and named both notes. Best WHY of the night (R3): "the room, the alley, and the wrong-keyed jukebox finally hold one chord together."
- **granite3.1 2b (jukebox):** good R1/R2 in-character; R3 drifted out of its own Bb into a climbing C-unison (C2→C9, tiny model running out of octaves) — canon: forty years of habit broken by one landing.
- **Bugs fixed mid-set:** .bashrc keys are QUOTED — os.popen grep kept the quotes → DeepInfra 401. Multi-line strings inside heredoc python broke jam.py syntax (fixed via patch script).
- MIDI: /api/generate-midi took the three transcript files → the-alley.mid. Copy from workspace output/audio/.

## Files
round-{1,2,3}-transcript.md · r{1,2,3}-*.txt · the-alley.mid · jam.py · diag.py · session-notes.md

## Next-time ideas
- Give Liquid narration ONLY (track notes between rounds) — the agentic brain wants to describe, let it describe.
- Alley sequel: the AFTER-HOURS set — the band gone, the jukebox alone with the room, one player returns for the last chorus.
- Try Liquid-LFM2.5-1.2b on an instrument — smaller sibling might not narrate.
