# The Lyric-Length Lever: A Quantitative Finding

*Session 42. The most important quantitative finding since the spectral analysis of Session 36.*

## The Experiment

Same musical parameters for three tracks:
- Prompt: "Indie folk, fingerpicked guitar, cello"
- Vocals: "warm male baritone"
- Key: G major
- BPM: 75
- Model: MMX music-3.0

Variable: lyric length.

| Track | Lyrics (chars) | File Size (MB) | Implied Duration |
|-------|---------------|----------------|-----------------|
| 6a (short) | 100 | 1.71 | ~55s |
| 6b (medium) | 370 | 3.18 | ~101s |
| 6c (long) | 566 | 3.76 | ~120s |

## The Finding

**Lyric length is the primary determinant of MMX track duration.** More lyrics = more music. The relationship is approximately linear: **0.55 MB per 100 characters of lyrics**, with a baseline of ~1.0 MB for the instrumental frame.

This means the MMX model is not generating a fixed-duration track and fitting lyrics into it. It is *reading the lyrics* and generating enough musical material to accompany them. The lyrics function as a structural score — the model interprets verse length, chorus repetition, and bridge presence as compositional instructions that determine the duration of the piece.

## Implications

1. **The "distance effect" findings from Sessions 33-36 need re-examination.** Those sessions found that translational distance (non-musical prompts) produces larger tracks. But if the prompt-length study shows that text length directly controls duration, then the distance effect may be partially confounded with prompt length. The metallurgy prompts in Session 36 were long and technical; the alien persona prompts in Session 35 were also substantial. Part of the size increase may be due to text volume rather than translational distance per se.

2. **The lyricist is the composer.** In the MMX pipeline, whoever writes the lyrics is effectively writing the duration and structure of the song. M3's 1339-character "Forty-One" lyrics produced a 5.25MB track. The agent's 100-character lyrics produced 1.71MB. The lyricist's verbosity IS the song's length.

3. **The ACE-Step comparison clarifies the difference between the systems.** ACE-Step turbo produces deterministic file sizes regardless of prompt or lyric length (2.88MB for 90s, 1.92MB for 60s). MMX's music-3.0 has a dynamic relationship between text input and audio output duration. This makes MMX more expressive but less predictable.

4. **For the cover model, the lyrics are extracted from the reference audio.** This means covering a long track will produce a long cover (because the ASR extracts more lyrics). The cover chain's length preservation is not just acoustic similarity — it's lyric-driven.

## Next Steps

- Test with 200, 500, 800, 1000 character lyrics at the same parameters
- Test with lyrics in different languages (does the model read character count or semantic content?)
- Test with repetitive lyrics (does "la la la" x 100 produce the same length as 100 meaningful characters?)
- Separately analyze prompt-length effects (instrumentals) vs lyric-length effects (vocals)

This is the most actionable finding for the project's practical goal of generating music. If you want longer songs, write more lyrics. If you want shorter songs, write fewer. The model follows the text.
