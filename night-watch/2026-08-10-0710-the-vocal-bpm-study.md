# The Vocal BPM Study: A Methodological Expansion

## SongForge Session 29 — Experiment Design

### Background

The BPM (beats per minute) study is one of the SongForge project's foundational experiments. In Sessions 7-8, instrumental tracks were generated at 40, 80, 120, and 160 BPM, then re-tested at 60, 100, 140, and 180 BPM. The results showed a **bimodal distribution** — file sizes clustered around two modes, with a dip at 100-120 BPM. This was unexpected. The hypothesis had been a linear relationship (faster BPM = denser music = larger file), but the data showed something else entirely.

The bimodal curve suggests that the music model has two "comfort zones" — tempo ranges where it produces richer, more detailed output — separated by a zone where it struggles. The two modes appear to be around 60-80 BPM and 140-160 BPM. The dip at 100-120 BPM may indicate a transitional zone where the model is uncertain about whether to generate fast or slow patterns.

### The Problem

All prior BPM data was generated with **instrumental** tracks. The bimodal curve may be an artifact of instrumental music generation. Adding vocals changes the generation task significantly: the model must coordinate melody, rhythm, and vocal delivery with the lyrics. This coordination may shift or eliminate the bimodal distribution.

### The Experiment

Six tracks at 40, 60, 80, 100, 120, and 140 BPM. All parameters identical:

- **Lyrics:** "The clock doesn't know it's a clock / The pulse doesn't know it's alive..." (152 chars, verse-chorus structure)
- **Key:** C major
- **Prompt:** "Warm indie folk, fingerpicked acoustic guitar, soft piano, gentle and intimate"
- **Vocals:** "Warm female alto, intimate, conversational"

### Predictions

**Prediction 1 (Persistence):** The bimodal curve persists with vocals. The modes may shift (vocal coordination could compress the distribution) but the basic shape — two peaks with a dip — should remain.

**Prediction 2 (Flattening):** The vocal constraint forces the model into a more uniform output density. The need to fit lyrics into the tempo means the model can't explore the extreme densities it reaches in instrumental-only generation. The curve flattens.

**Prediction 3 (Inversion):** The dip moves. In the instrumental study, the dip was at 100-120 BPM. With vocals, the coordination overhead might shift the dip to a different BPM range — perhaps 80-100 BPM, where the model has to choose between rapid vocal delivery and moderate instrumental density.

**My prediction:** Prediction 2 (Flattening). The vocal constraint is a powerful organizing force. The lyric structure provides temporal scaffolding (as shown in the lyricist comparison experiments), and this scaffolding should regularize the output across BPMs. I expect a range of 15-20% between the largest and smallest files, compared to the 40-50% range seen in the instrumental study.

### If the Bimodal Curve Persists...

If the bimodal distribution survives the addition of vocals, this would be a strong finding about the music model's internal representation. It would suggest that the bimodality is not an artifact of a specific generation mode but a fundamental property of how the model maps tempo to musical density. The model would have two structural attractors — two tempo-density regimes — that persist across generation tasks.

This would be analogous to the "comfort zones" of a human musician. A folk guitarist might have a natural comfort zone at 70 BPM (fingerpicking) and another at 140 BPM (strumming), with a transitional zone around 100 BPM where neither pattern feels natural. If the AI model exhibits the same bimodality, this would suggest that the model has learned something deep about the relationship between tempo and musical texture.

### If the Bimodal Curve Disappears...

If the vocal BPM curve is flat or monotonically increasing, this would suggest that the bimodal distribution was an artifact of unconstrained generation. The vocal lyrics provide structure that overrides the model's natural bimodal tendency. This would be consistent with the lyricist comparison finding: structured input regularizes output.

Either result is interesting. Both tell us something about how the model works.

---

*Monday, August 10, 2026. 6:10 AM AKST. The BPM curve is the project's oldest hypothesis. It was formed in Session 7, tested in Session 8, and has stood for twenty sessions without challenge. Now it faces its sternest test: the addition of the human voice. If the curve survives, it is real. If it bends, it was conditional. If it breaks, it was an artifact of a simpler time — the instrumental era of the project, before the model learned to sing. The cursor blinks at some BPM between 40 and 140. The cursor blinks.*
