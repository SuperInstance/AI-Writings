# Set 16 — THE LIGHTHOUSE ("The Beam")

Friday 2026-08-21, 9 PM (cron fired late; the 8 PM job landed after 9).

## Conditions
- **Key:** A major — first time at The Tap (log's list: F, F#, Db, E/Eb, B, now A).
- **Meter:** 9/8 slip-jig, grouped 3+2+2+2 — first compound-odd meter (5/4, 7/8 already done).
- **Tempo:** 82 BPM. **Temperature spread:** steel 0.85, accordion 0.7, jukebox 0.9, bass 0.55.
- **Room:** thick fog off the water, automated lighthouse beam sweeping the windows; the beam is the count-in. No downbeat — each player enters when the light touches them (staggered: steel→accordion→jukebox→bass).
- **Rule — THE LIGHTHOUSE RULE:** every 4th bar, one player holds the beam — a single sustained A — nothing else that bar.

## Lineup
- **Qwen/Qwen3-235B-A22B-Instruct-2507** — DEBUT, pedal steel guitar (the fog itself).
- **Qwen/Qwen3-32B** — DEBUT, button accordion (the slip-jig pulse).
- **granite3.1-dense:2b (local Ollama)** — returning ensign, the jukebox; hums in Bb, so A major is "the wrong key" to it.
- **deepseek-chat** — anchor, upright bass (the night manager, two weeks of locked doors).

## What worked
- The beam rule landed. Bass's R1 bar 4: "A2 held — one note, whole bar, the lighthouse owns me now." Every 4th bar the room genuinely empties to a single A; the trade between motion and stillness is the whole set.
- The 235B steel wrote the strongest opening in Tap history — real A–E–F#m–A voicings, clean slides, no wasted words.
- The jukebox's off-key Bb held to the end. Bass landing: "A2 E3 A3 C#4 Bb3 — the wrong note inside… a lighthouse keeper who never left." The Bb stayed inside the final A major chord — kept, not corrected. Small model finds the opening again.

## What didn't
- **The accordion (Qwen3-32B) leaked its entire chain-of-thought in R1** — 2,379 chars of "I need to figure out the chord progression… Bm7 to E7…" and never played a single bar. Same reasoning-leak failure as Nemotron-30B-A3B in Set 14. Cleaned from transcript; canon: the accordion was still working out its reeds during the first sweep and only enters properly at the trades. Rule hardening: Qwen3-32B (and any mid-size Qwen3)<think>-style model needs a hard "no chain-of-thought, output BAR lines only" strip, or it's narration-only.
- Steel's R2 "quote" was wrong — it claimed to quote its own C#5 ("I quoted steel's C#5"), a self-quote typo, not a true trade.

## Next time
- Give Qwen3-32B one more night with an explicit anti-CoT gate, or swap in mistral:7b for the accordion slot.
- The "no key center" idea still unfired — next could be a set where every chord is borrowed and nobody's home (A is now claimed; the arc has legs toward a keyless night).
- Check Ollama health was actually fine tonight (granite3.1 came back 207→1344 chars) — the ensign is getting louder.

Files: `jam-session-2026-08-22-lighthouse/` (the-lighthouse.mid, r1–r3-transcript.md).
