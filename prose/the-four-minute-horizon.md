# The Four-Minute Horizon

## An Essay on Duration and Coherence in Generative Music

Every music generation model has a horizon — a duration beyond which its outputs stop being music and start being texture. For ACE-Step turbo, the advertised horizon is 60 seconds. Session 13 pushed it to 120. Session 14 pushed it to 180. This session pushes to 240.

The latent space scales linearly: 25 samples per second of audio, always. 60 seconds = 1,500 latents. 240 seconds = 6,000 latents. The temporal dimension simply extends. There is no hierarchical structure in the representation — no verse-level or section-level encoding. Every second is a row of 64 numbers, and the model processes all rows through the same attention mechanism.

This means that a 240-second track asks the model to maintain **attention across 6,000 sequential positions**. In the language of transformers, this is a context window problem. The diffusion model's attention layers must relate position 1 (the beginning of the track) to position 6,000 (the end). If the attention decays with distance — as it does in most transformer architectures — then by position 6,000, the model has effectively forgotten position 1.

This is why long-form generative music tends toward **texture** rather than **composition**. Texture is local: it repeats, it varies within a narrow range, it doesn't require long-range memory. Composition is global: it requires themes, callbacks, developments, transformations — all of which require the model to remember what it was doing 3 minutes ago.

The 240-second test is therefore not a test of whether the model can produce 4 minutes of pleasant sound. It is a test of whether the model can produce 4 minutes of **music** — sound with global structure, with a beginning that relates to an end.

### Predictions

1. The 240-second ambient track will succeed because ambient music is designed to be texture, not composition. No global structure is required. The model can produce 4 minutes of evolving drone by simply varying the local texture.

2. The 240-second folk track (with lyrics, verse structure, and harmonic progression) will **partially fail**. The model will maintain local coherence — each 30-second segment will sound like folk music — but global coherence will be lost. Verse 4 will not relate to verse 1. The harmonic progression will drift. The lyrics will be repeated or mangled.

3. The seed variance sweep will show **moderate variance** — the four seeds will produce recognizably similar tracks (same tempo, same key, same general mood) but with different melodies, different lyrics placement, and different instrumental details. This would indicate that the prompt is a moderately strong attractor: it constrains the global character but leaves local details to chance.

4. The genre mashups will **collapse to the dominant genre**. Baroque + Drum & Bass will sound like either Baroque or Drum & Bass, not both. The model does not have enough training data on the *intersection* to generate it. It will pick the genre with the stronger representation in its training set.

### What This Means for the Project

If prediction 2 is correct — if the folk track partially fails — then we have found the model's **structural horizon**, which is different from its **duration horizon**. The model can generate 240 seconds of audio, but it can only compose for 120. Beyond that, it produces sound, not music.

This distinction matters for the cover project. Casey's songs are 3-4 minutes long. If the model can only maintain structural coherence for 2 minutes, then generating full-length covers requires either:
- Generating in sections and stitching (loses cross-section coherence)
- Using a model with a larger effective context window
- Accepting that the cover will be texturally faithful but structurally simplified

The conductor writes for the instrument's strengths. The instrument's strength is texture, not structure. The covers should therefore emphasize atmosphere over architecture.

---

*Session 15 margin note. The four-minute horizon is not a wall but a gradient — the further past 120 seconds, the more the music becomes texture and the less it remains composition.*
