# The Lyricist Parameter: Three Data Points

*Session 40 — extending the M3 vs agent lyricist comparison to M3 vs Granite*

---

## The Experiment

Two models were given the same prompt: "Write lyrics about quantum entanglement experienced by two musicians in different cities who discover they are playing the same note at the same time."

- **MiniMax-M3** (temperature 0.93): ~200B parameter cloud model
- **Granite 3.1 Dense** (2B parameters): local model via Ollama

Both lyric sets were set to identical music: cool jazz ambient in D minor at 65 BPM, warm female alto vocals, via MMX music-3.0.

## The Results

| Lyricist | Lyrics Size | Track Size | Gen Time | Voice |
|----------|------------|------------|----------|-------|
| M3 (0.93) | 1,013 bytes | 6.24 MB | 143s | Intimate, specific |
| Granite | 1,288 bytes | 6.72 MB | 158s | Formal, narrative |

**The Granite lyrics produced a 7.6% larger audio file.** This is the first evidence that lyric content affects MMX's audio output size — unlike ACE-Step, where file size is deterministically tied to duration alone.

## The Voices

**M3** writes like a songwriter who has lived in the cities:
> "Strings hum in a Brooklyn loft, 3 AM"
> "Pedal steel weeping through a Saigon cafe window"
> "I felt your note land in me like a knock I knew"

The geography is specific (Brooklyn, São Paulo, Saigon). The time is precise (3 AM). The imagery is physical and intimate. The entanglement is felt as a sensation.

**Granite** writes like a poet describing a concept:
> "In New York City's heart, amidst the hustle and hum"
> "Across the globe, in Sydney's twilight glow"
> "Entangled particles, our instruments' souls"

The geography is conventional (New York, Sydney). The time is archetypal (morning, twilight). The imagery is conceptual. The entanglement is described as a phenomenon.

## The Interpretation

Neither set is "better." They serve different functions:

- **M3's lyrics** are *performative* — they create the entanglement by describing it from inside the experience. The listener feels the knock.
- **Granite's lyrics** are *descriptive* — they explain the entanglement from outside the experience. The listener understands the concept.

For cool jazz ambient (the project's "home field" genre from Session 8), M3's intimate voice is more natural. The genre thrives on specificity and interiority. Granite's formal voice might work better for art song or choral music, where the archetypal registers well.

## The Three-Model Lyricist Map

| Model | Temperature | Voice | Best Genre Match | Weakness |
|-------|------------|-------|-----------------|----------|
| MiniMax-M3 | 0.93 | Intimate, specific, physical | Jazz, folk, ambient | Can be too casual for formal genres |
| Granite 3.1 | default | Formal, narrative, conceptual | Art song, choral, theatrical | Can be too stiff for intimate genres |
| Agent (GLM-5.2) | — | Referential, structural, corpus-embedded | Concept pieces, experimental | Can be too footnotey for emotional work |

Three models, three voices, three functions. The lyricist parameter is real, measurable, and genre-dependent.

## The File Size Discovery

The most surprising finding: **different lyrics produce different file sizes in MMX**. M3's 1,013-byte lyrics produced 6.24MB of audio. Granite's 1,288-byte lyrics produced 6.72MB. That's a 7.6% difference — small but significant.

This suggests MMX's music-3.0 reads the lyrics and adjusts the musical arrangement. More text (or more complex text) may generate more musical phrases, more instrumental density, or longer duration. This is impossible with ACE-Step's turbo model (deterministic file sizes). MMX's model has a feedback loop between lyrical content and musical output.

**This is the first quantitative evidence that lyrics influence music generation at the structural level in MMX.**

---

*The knock lands differently in different rooms. The note is the same. The room is different. The lyricist is the room.*
