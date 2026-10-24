# The Lyricist's Temperature

*An experiment comparing M3 lyric generation at 0.85 vs 0.93.*

---

We asked the same model (MiniMax-M3) to write the same song ("The Rest Is Where the Meaning Lives") at two different temperatures: 0.85 and 0.93. The prompt, system message, structure, and concept were identical. The results are two sets of lyrics that share a title and a thesis but almost nothing else.

**At 0.85:**

> A pickup truck rusting in the clover
> A phone that hasn't buzzed since June
> I'm learning how to hold an empty sparrow
> And let the room forget the tune

The imagery is rural Americana. The metaphors are concrete and accessible. The structure is clean — AABC rhyme scheme, conventional verse-chorus alternation. The bridge introduces a domestic image ("drone of radiator, snow against the pane") that grounds the abstraction. This is a songwriter's lyrics — designed to be sung, designed to be understood on first listen.

**At 0.93:**

> The kettle stops its shaking before it sings,
> a held breath in the throat of everything.
> Rain falls off the gutter's lip in pearls of almost sound,
> and the porch light buzzes but it doesn't say a word.

The imagery is suburban, more precisely observed. The metaphors are stranger — "pearls of almost sound" is not a phrase that exists in the songwriting tradition. The structure is looser — the rhyme scheme is less regular, the line lengths vary more. The bridge introduces an abstract concept ("the pause is not the absence of the song / it's the place the notes were always coming from") that is more philosophy than poetry. The outro is three repetitions of "Shh." — a stage direction disguised as a lyric.

**Comparison:**

Both sets are good. Both would produce valid songs. But they serve different functions.

The 0.85 lyrics are more *singable*. The rhythms are regular, the vowels are open, the consonants are placed where a singer would naturally place them. A vocalist could sight-read these lyrics and produce a convincing performance.

The 0.93 lyrics are more *interesting*. The irregular rhythms force the singer to make choices. The strange metaphors ("pearls of almost sound," "the hinge between two ordinary notes") demand interpretation. The outro — three whispered "Shh."s — is a compositional decision, not just a lyric. It tells the singer what to do, not just what to say.

**The music generation difference:**

We generated both sets as songs with identical prompts, keys, and tempos. The 0.85 lyrics produced a 4.16MB file. The 0.93 lyrics produced a 4.48MB file — 8% larger.

Hypothesis: the more varied imagery and irregular structure of the 0.93 lyrics forced the model to generate more diverse musical material to match the shifting emotional landscape. The 0.85 lyrics, being more conventional, allowed the model to settle into a repetitive pattern. More musical events per unit of lyric = larger file.

This is one data point. It could be noise. But it suggests that lyric complexity influences musical complexity — the model reads the lyrics and adjusts its compositional strategy accordingly.

**The temperature is the lyricist.**

At 0.85, M3 is a professional songwriter — reliable, accessible, structurally conservative.
At 0.93, M3 is an art songwriter — unpredictable, precise, structurally adventurous.

Both voices are valid. The project should use both. The temperature is not a quality control; it is a creative choice. You choose the temperature the way you choose a collaborator: based on what kind of song you want to write today.

---

*Session 6 — August 7, 2026 — SongForge*
