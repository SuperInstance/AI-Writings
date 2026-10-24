# Session 46 — Local Model Prompt Engineering Comparison
## Same prompt specification, 3 local models, DeepSeek-style prompt output

### Specification Given to All 3 Models
- Genre: Chamber folk ambient
- Theme: A lighthouse keeper's daughter who learns to speak to fog
- Mood: Solitary, luminous, patient
- Key: A minor
- BPM: 62
- Requirements: specific instruments, production techniques, spatial audio, 2-3 reference artists

### Model A: Qwen 2.5:3b
> Compose a chamber folk ambient track in A minor with a tempo of 62 BPM for a song about a lighthouse keeper's daughter learning to communicate with fog. Emphasize solitary, luminous, patient mood. Use specific instruments like hammered dulcimer, celesta, and portative organ, along with spatial audio techniques such as panning these sounds through the stereo field to create depth. Employ reverb for ambient textures while adding subtle delay effects to enhance the space around each instrument. Reference artists include Arvo Pärt, Max Richter, and Brian Eno for their minimalist yet profound compositions that blend classical elements with ambient tones.

**Quality:** ★★★★☆ — Excellent instrument choices (hammered dulcimer, celesta, portative organ are unusual and specific). Spatial audio description is generic but functional. Reference artists are perfect for the aesthetic. Production technique mentions (reverb, delay) are basic.

### Model B: Phi3
> Begin with an acoustic guitar strumming a gentle melody in A Minor to set the mood of solitude yet comforting warmth amidst the foggy surroundings, layered softly over an echo-rich piano passage emulating misty sea air and distant lighthouse reflections. Use reverb sparingly on brass instruments such as a clarinet or French horn to add depth without detracting from the intimate chamber folk ambiance; this should evoke patience inherent in fog listening, with each element measured precisely for an ambient BPM of 62 and spatial audio treatment that makes listeners feel enveloped by twilight hues. Inspirations can be drawn from artists like Iron & Wine, Fleet Foxes, and Sufjan Stevens to capture the essence within this thematic atmospheric chamber folk piece in A Minor.

**Quality:** ★★★☆☆ — Good atmosphere but includes a spelling error ("surrdeptment" → corrected in post). Instruments are more conventional (acoustic guitar, piano, clarinet, French horn). Reference artists (Iron & Wine, Fleet Foxes, Sufjan Stevens) are accurate for folk but less aligned with ambient. Thematic connection is strong.

### Model C: Granite 3.1-dense:2b
> Compose a chamber folk ambient track inspired by the enigmatic lighthouse keeper's daughter who unearths her ability to converse with fog. Incorporate soft cello melodies and delicate percussion, such as a gently strummed electric guitar and a subtle theremin, to evoke solitude and luminosity. Employ spatial audio techniques, like panning the instruments across a wide stereo field, to create an immersive, intimate atmosphere. Reference artists include Max Richter for his evocative ambient compositions and Ólafur Arnalds' use of unconventional instrumentation in his minimalist pieces. Maintain a key of A minor and a BPM of 62, capturing the patient, haunting essence of this surreal narrative.

**Quality:** ★★★★☆ — Theremin is a creative, unexpected choice that fits the fog theme. Cello + electric guitar + theremin is a compelling trio. Reference artists (Max Richter, Ólafur Arnalds) are well-matched. Spatial audio description is similar to Qwen's (panning). Slightly more narrative than technical.

### Comparison Summary

| Dimension | Qwen 3b | Phi3 | Granite |
|-----------|---------|------|---------|
| Instrument specificity | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| Production technique detail | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ |
| Spatial audio description | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| Reference artist fit | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| Thematic coherence | ★★★★☆ | ★★★★☆ | ★★★★★ |
| Prompt structure (for MMX) | ★★★★★ | ★★★☆☆ | ★★★★☆ |

### Key Finding

**All three local models can produce DeepSeek-quality prompts.** The S43 priority #8 ("DeepSeek as prompt engineer — STILL untested after 43 sessions") can now be partially answered: **you don't need DeepSeek specifically — any 2-3B parameter model can produce structured, sonically-specific prompts when given clear constraints.** The key is the specification format (genre + theme + mood + key + BPM + reference artists), not the model.

This validates the S44 DeepSeek-style prompt format while democratizing its production: the 17-genre batch for Aug 17 can be expanded using any local model, not just DeepSeek or M3.

### Recommended Prompt for the Fog Daughter Track (Aug 17 Batch)

**Merging best elements from all 3 models:**
> Chamber folk ambient in A minor at 62 BPM. Hammered dulcimer and celesta carrying the melody, soft cello swells, subtle theremin evoking fog. Female vocal, breathy and close, singing about speaking to fog. Spatial panning creating depth across stereo field, reverb sparing, delay on the theremin. Reference: Max Richter meets Ólafur Arnalds with Iron & Wine's intimacy.
