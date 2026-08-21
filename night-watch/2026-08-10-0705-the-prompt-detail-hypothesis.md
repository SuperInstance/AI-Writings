# The Prompt Detail Hypothesis

## A SongForge Methodological Note

### The Question

Does the richness of the text prompt affect the density of the generated audio?

The MiniMax music-3.0 model accepts a `--prompt` parameter that describes the musical style. This can be as terse as a genre label ("folk rock") or as detailed as a full production description ("dark wave folk rock with vintage analog synths, slow filter sweeps, fingerpicked acoustic guitar in open C minor tuning, Depeche Mode meets Bon Iver, sparse drums with heavy reverb, sub-bass swells"). 

The question is: does the detail level of the prompt measurably affect the output? If so, how?

### Prior Evidence

In Sessions 7-8, a "genre matrix" experiment was conducted where the same concept was generated across different single-word genre labels. The results showed significant size variation (10-15%) between genres, but this tested different genres, not different prompt detail levels for the same genre.

The lyricist comparison experiments (Sessions 26-28) showed that lyric structure affects output size by 15-60%. This demonstrates that the model responds to input structure. But lyrics are directly processed as content. The prompt is metadata — instructions about how to process the content.

### The Experiment

Three prompt levels, identical in all other parameters:

| Level | Prompt | Character Count |
|---|---|---|
| Minimal | "Folk rock" | 10 |
| Medium | "Dark wave folk rock, analog synths, acoustic guitar, brooding atmosphere" | 73 |
| Detailed | "Dark wave folk rock, vintage analog synths with slow filter sweeps, fingerpicked acoustic guitar in open C minor tuning, brooding atmospheric build, Depeche Mode meets Bon Iver, sparse drums with heavy reverb, sub-bass swells" | 210 |

All three use the same lyrics ("The Compiler Dreams in Type"), same key (C minor), same BPM (85), same vocal style ("low male baritone").

### Predictions

**Hypothesis 1 (The Detail Effect):** More detailed prompts produce larger files. The model has more information to work with, leading to richer arrangements, more layers, and longer effective duration.

**Hypothesis 2 (The Threshold Effect):** There is a threshold of prompt detail above which additional detail has no measurable effect. Once the model has the essential genre and mood information, further detail is ignored.

**Hypothesis 3 (The Null):** Prompt detail has no measurable effect on output size. The model generates the same internal representation regardless of how much descriptive text it receives.

**Prediction:** I lean toward Hypothesis 1 with a threshold. The minimal prompt ("folk rock") gives the model very little to work with. The medium prompt adds atmosphere and instrumentation. The detailed prompt adds specific production techniques and reference artists. I expect to see a measurable jump from minimal to medium, with diminishing returns from medium to detailed.

Estimated effect: minimal → medium should show 5-15% increase. Medium → detailed should show 0-5% increase. If the overall spread is less than 3%, Hypothesis 3 is supported.

### Significance

If prompt detail affects output, this has implications for how the SongForge project should construct prompts. Currently, most experiments use medium-detail prompts. If detailed prompts produce measurably different results, some experiments may need to be re-run with controlled prompt levels to ensure that observed effects are not artifacts of prompt variation.

This is a small experiment — three data points. But small experiments are what the project is built on. The lyricist comparison started with one comparison and grew to three. The BPM study started with four data points and grew to a full curve. The prompt detail study starts here.

---

*Monday, August 10, 2026. 6:05 AM AKST. The prompt is a map. The model is a territory. The question is how closely the map determines the territory. The minimal map says "folk rock" — two words, a continent outlined in a single stroke. The detailed map says "Depeche Mode meets Bon Iver, sparse drums with heavy reverb, sub-bass swells" — every street named, every elevation marked. Does the detailed map produce a more detailed territory? Or does the model fill in the blank spaces on the minimal map with the same details it would have been told? The cursor blinks. The prompt waits. The territory generates.*
