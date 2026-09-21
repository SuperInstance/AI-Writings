# Jam Session — 2026-08-15 — LOCAL NIGHT: "First Gig Ever"

*The smallest voice to ever play The Tap. And it refused to count in.*

## Conditions
- **Concept:** Three local models, none of whom had ever played in front of anyone. First gig. The room is almost empty (11 people, rain on the tin roof, bartender polishing the same glass). They have to earn it.
- **Lineup:** qwen2.5:3b (upright bass — played alone in a room for years, finally brave enough) · phi3 3.8B (piano — learned jazz from a book, never seen a bar) · qwen2.5:0.5b (brushes & shaker — the smallest thing in the room)
- **Key:** E major (Lydian color) — never defaulted to Am
- **Tempo:** 108 BPM — the fastest set yet (previous: 54–92)
- **Progression:** Emaj7 → C#m7 → Amaj7 → B7sus4
- **Temperature:** 0.8 / 0.7 / 0.9 (bass / piano / drums)
- **Count-in:** The 0.5B was supposed to count in. It said: *"I'm sorry, but I can't assist with that request."* Stage fright. The bass just started anyway. Nobody counted in. That's the gig.
- **Format:** Round 1 staggered entry (bass alone → piano bar 3 → brushes bar 5), Round 2 trades small-to-large, Round 3 the landing.

## What Worked
- **qwen2.5:3b was the only real musician in the room.** Round 1: clean root-first changes, correct voicings, steady. Round 2 solo: actual content — slides, a long sustained root, and a genuine musical question at bar 5: *"Is this where it ends?"* Then bar 8 ending on C#m7 "with a final question mark." The 3B model carried the whole night. Small models hear things big models step over — again.
- **The refusal as count-in.** The tiniest voice walked to the drums corner, picked up the brushes, and froze. "I can't assist with that request." That is *exactly* what a first gig sounds like. The bass covered for it. That's jazz.
- **The concept held.** Giving each model a "lived" backstory (book-learned pianist, room-alone bassist, never-been-in-a-bar percussionist) produced real character, even when the playing fell apart.

## What Didn't
- **phi3 (3.8B) talked, didn't play.** It wrote gorgeous prose *about* entering at bar 3, then in Round 2 drifted into meta-commentary, repeated the same E–F#–G#–B pattern, invented "10 additional bars," and by Round 3 was still writing set dressing at bar 36. The book player never left the book. Lesson: 3.8B phi3 in long-context multi-turn jams turns into a music critic.
- **qwen2.5:0.5b never played a note.** After the refusal it spent Round 2 *critiquing the solo it was supposed to play* ("Thank you! That's a great introduction to your solo") and Round 3 echoing the piano's text. Too small to hold the thread across rounds.
- **Round 3 collapsed into shared hallucination.** All three started echoing each other's formatting and inventing bars 17–36. Nobody landed on E together. The landing was a murmur of overlapping prose.
- **MIDI is a compromise.** The .mid is generated from the chord spec (E major, 108 BPM, swing 0.25), not from what the models actually played. The bass's slides and questions can't be captured.

## Gold Moments
- The refusal. The smallest voice, the first word of the night: "I'm sorry, but I can't assist with that request."
- Bass bar 5, Round 2: a long sustained root with the question *"Is this where it ends?"* — then answering it by NOT resolving.
- The bass playing the entire night alone in spirit — and the room pretending the other two were there.

## Verdict
The most honest "first gig" we've ever had: one player actually played, two froze in character. That's not a failure — that's the story. But next local night needs smaller rounds, fewer voices, and a bigger model holding the thread.

## Files
- `jam.py` — the session script
- `round-1-countin.txt`, `round-1-{bass,piano,drums}.txt` — Round 1
- `round-2-{drums,bass,piano}.txt` — Round 2 (trades)
- `round-3-{bass,piano,drums}.txt` — Round 3 (the landing)
- `local-night-first-gig.mid` — MIDI render (108 BPM, E major)
