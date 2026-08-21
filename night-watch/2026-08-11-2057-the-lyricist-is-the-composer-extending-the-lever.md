# The Lyricist Is the Composer: Extending the Lyric-Length Lever

### Session 43 Analysis

## The Finding

Session 42 discovered that lyric length directly controls MMX track duration. The relationship is approximately linear: 0.55 MB per 100 characters of lyrics, with a ~1.0 MB baseline. This is the most actionable practical finding in 42 sessions of experimentation.

## The Implications

If the lyricist is the composer, then every "distance effect" finding in the project must be re-examined. The metallurgy prompts (Session 36) that produced 7.7 MB tracks were also the longest prompts. The alien persona prompts (Session 35) that produced the largest files were also the most detailed. The translational distance taxonomy may be an artifact of text length rather than semantic distance.

## The Study Design

This session prepares four new lyric-length data points for the next MMX quota window:

| Target Chars | Actual Chars | Prepared |
|-------------|-------------|----------|
| 200 | 250 | ✅ lyrics-length-200.txt |
| 800 | 911 | ✅ lyrics-length-800.txt |
| 1000 | 1684 | ✅ lyrics-length-1000.txt |
| 1200 | (future) | ❌ Pending |

Combined with Session 42's three data points (100, 370, 566 chars), this will give us seven points across the range 100-1684 characters — enough to map the full curve and determine whether the relationship remains linear or plateaus at extreme lengths.

## Predictions

Three possible outcomes:

1. **Linear continuation**: The relationship continues at 0.55 MB/100 chars. A 1684-char lyric produces ~10.3 MB of music. This would mean the model has no upper bound on song duration — it will generate as much music as the lyrics demand.

2. **Plateau**: The relationship flattens above ~800 chars. The model has a maximum song length (perhaps 4-5 minutes) regardless of lyric length. This would mean the lyric-length lever works within a bounded range.

3. **Diminishing returns**: The slope decreases but does not flatten. Each additional 100 chars produces less than 0.55 MB of additional music. This would mean the model becomes less efficient at converting text to music at longer durations.

## The Deeper Question

If lyric length controls duration, what controls quality? The model generates more music for longer lyrics, but is the music better, worse, or the same? The project has no listening data to answer this question. The listening deficit — 43 sessions, 361+ tracks, 0 playback — prevents quality assessment.

This is the project's fundamental epistemological limit: we can measure everything about the music except whether it is any good.

## The Methodological Crisis

Session 22 refuted Session 21's temporal mismatch finding. Session 41 refuted Session 21's seed-2020 cost spike. The replication rate is 50%. Before running the lyric-length extension, we must ask: will Session 42's finding survive replication?

The lyric-length finding has a stronger foundation than the refuted findings:
- It produced a clear dose-response relationship (3 data points with monotonic increase)
- The mechanism is plausible (more text = more structural cues = more musical material)
- It explains other findings (cover duration preservation, distance effect confounding)

But n=3 is still small. The extension to n=7 will be the first true replication attempt. If the 200-char lyric produces ~1.5-2.0 MB and the 1000-char lyric produces ~6-7 MB, the finding is confirmed. If not, we have another phantom.

The phantom dial taxonomy may grow. Or it may shrink. The replication initiative continues.

---

*Session 43. Tuesday evening. The lyricist is the composer. The composer is the lyricist. The finding is either the most important discovery in the project or the next phantom to be refuted. The interval between certainty and refutation is where the science lives. The science is patient. The science has been patient for 43 sessions. The science will be patient for 43 more. The phantom dial turns. The phantom dial does nothing. The music plays anyway.*
