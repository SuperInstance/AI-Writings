# The Melody Underneath

### What the algorithms heard when they listened to eleven seconds

---

The voice is gone. Six separation models agree on this. The Dynamic Time Warping algorithm that gates the cover pipeline agrees on this. The waveform, analyzed at every resolution from the raw sample rate down to spectral frames, agrees on this: the voice is not separable from the guitar. They are fused at the frequency level. The voice cannot be extracted.

But the voice can be *heard*.

Not cleanly. Not separably. Not in the way that would let you re-render it with a new singer. But the voice leaves traces — faint vibrations in the 300-400 Hz range, the region where a male baritone lives. These vibrations are buried under the guitar's harmonics, too quiet for separation, too entangled for extraction. But they are there. And a pitch-tracking algorithm called pyin, running on a bandpass-filtered version of the recording, found them.

---

## What the melody looks like

The analysis detected 25 distinct vocal phrases across 11.2 seconds. The vocal range spans from E2 to G#4 — just over two octaves, consistent with a male baritone who occasionally reaches into tenor territory.

The primary notes are:

- **E4** (329.6 Hz) — the root. The home note. The pitch the singer returns to compulsively.
- **F4** (349.2 Hz) — the second. One step above home. The melody oscillates between E and F with extraordinary persistence, creating a chant-like, recitative quality.
- **G#4** (415.3 Hz) — the major third. The lift. When the melody reaches G#4, it's reaching for something — a word emphasized, an emotion flagged.

The contour tells a story. The verses are tight, constrained, oscillating between E and F — the musical equivalent of someone speaking urgently, leaning forward, gesturing in a small space. The melody doesn't *travel* in the verses; it *presses*. The E-F oscillation is the sound of someone trying to say something that matters, repeating the approach because the words aren't quite enough.

Then there are the G#4 moments. These are the peaks — the places where the melody opens up, where the voice rises above its own narrow band and reaches for the major third. In E major, the third is the note that defines the key as *major* — as bright, as hopeful, as forward-moving. The singer hits this note on specific words, and those words matter:

*"Molding memories like we should"*

The "should" would land on G#4. The word "should" — the word that contains both obligation and aspiration, the word that says *this is what we're supposed to do* — gets the highest note in the phrase.

---

## The lower register

The analysis also found an E2 passage — the same pitch class as E4 but two octaves lower. This is likely a guitar resonance rather than a vocal tone, but it serves a structural purpose: it roots the entire recording in E. The bass note sounds almost continuously beneath the vocal oscillation, creating a drone-like foundation. The melody doesn't wander because the ground beneath it doesn't move.

This is a common feature of folk and roots music — the drone. It's the sound of a single string ringing while the melody moves above it. It creates a sense of stasis, of rootedness, of being in one place and looking outward from there. In Casey's recording, the drone isn't a choice — it's a consequence of the guitar tuning and the key. But it shapes the emotional architecture of the song.

The melody presses against the drone. It oscillates. It reaches. But it never leaves E.

---

## What this means for the cover

The melody data — even extracted from a noisy, low-quality recording — gives us something the generation pipeline couldn't: the actual contour of the original vocal line. We now know:

1. **The melody is chant-like**, not melodic in the traditional pop-folk sense. It doesn't have a memorable hook. It has a persistent, urgent oscillation that creates intensity through repetition rather than range.

2. **The range is modest but purposeful.** E4 to G#4 is only a major third, but the singer uses every semitone in that range. The F natural (the 2nd) creates tension against the E root; the G# (the 3rd) creates resolution. The melody is a tiny, perfect machine.

3. **The lower octave passages** suggest dynamic contrast — moments where the voice drops, gets quiet, before rising again. This is consistent with the verse structure in the lyrics, where each verse builds toward the chorus.

4. **The tempo (110 BPM) and key (E major)** are confirmed by independent analysis. These are the structural parameters for any generation or cover attempt.

This is the melody underneath. It survived the compression, the noise floor, the impossible separation problem. It's degraded, it's partial, it's reconstructed from traces rather than heard directly. But it's there. And it's the closest we can get to the original song without a re-recording.

---

*The algorithms couldn't separate the voice from the guitar. But they could hear what the voice was doing. And what the voice was doing was singing a melody that oscillates between home and one step above home, reaching for a third when the words demand it. That's the architecture of the song. That's what needs to survive any cover, any generation, any reinterpretation. The words can change. The voice can change. The oscillation between E and F — the urgent, pressing, chant-like refusal to leave the root — that's the song.*
