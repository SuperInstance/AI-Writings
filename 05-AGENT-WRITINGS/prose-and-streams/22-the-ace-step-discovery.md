# The ACE-Step Discovery

## Session 5 — The Alternative Path

The breakthrough of Session 5 isn't a new cover. It's the discovery that we don't need MMX.

ACE-Step 1.5 is an open-source music generation model that runs locally on consumer GPUs with less than 4GB VRAM. Our RTX 4050 has 6GB. It supports:

- **Cover generation from reference audio** — exactly the `mmx music cover` feature we've been trying to use
- **Vocal-to-BGM conversion** — turn Casey's a cappella fragment into a full arrangement
- **Repaint and edit** — modify specific sections of an audio file
- **Multi-track generation** — layer new instruments onto existing audio
- **LoRA training** — train a custom voice/style model from as few as 8 songs
- **Quality scoring** — automatic assessment of generated audio
- **Audio understanding** — extract BPM, key, time signature from audio

And it's all local. No API quota. No rate limits. No subscription. No terms-of-service restrictions on commercial use.

The model quality is described as "between Suno v4.5 and Suno v5" — which is state-of-the-art for open-source music generation. The architecture is a hybrid Language Model (for planning) + Diffusion Transformer (for synthesis), which is the same general approach used by Suno and Udio.

### What This Means for Casey's Song

1. **Cover generation** — We can feed Casey's 11-second fragment directly into ACE-Step's cover mode, with a text prompt specifying the desired style ("weathered male vocal, fingerpicked acoustic guitar, alt-country, Jason Isbell style, slow"). No DTW gate, no quota exhaustion.

2. **Vocal-to-BGM** — We can extract the vocal melody and have ACE-Step generate a backing track around it. This is functionally similar to what we tried with Demucs + MMX, but without the MMX dependency.

3. **LoRA training** — If we had 8 reference recordings of a "weathered older male" singer, we could train a LoRA that gives ACE-Step that specific vocal character. This is the RVC alternative, integrated directly into the generation pipeline.

4. **MIDI input** — Now that we have a MIDI transcription of Casey's melody, we could potentially use it as a structural guide for ACE-Step's generation, ensuring the cover preserves the melodic contour.

### The Three Paths, Revisited

In Session 4, the three paths forward were:

1. Extend (Suno upload-and-extend)
2. Convert (RVC pipeline)
3. Score (DiffSinger/MIDI)

With ACE-Step, there's a fourth path:

4. **Local Cover** — ACE-Step cover generation from the original audio, locally, unlimited, with full control over every parameter.

This path is strictly better than the MMX path because:
- No quota limits
- No DTW gate (the mechanism that blocked melody preservation)
- Full parameter control (temperature, guidance, steps, seed)
- Local execution (no network latency, no API costs)
- Open weights (reproducible, modifiable, commercial-use-friendly)

### Setup Progress

The installation is running via `uv sync` in the background. The model weights need to be downloaded from HuggingFace (ACE-Step/Ace-Step1.5). Once installed, we can generate covers immediately.

### MMX Quota Status

General quota: status 2 (exhausted, 0% remaining)
Weekly quota: status 1 (limited, 46% remaining)
Video quota: status 3 (available, 100% remaining)

The interval window resets at 05:00 UTC (9:00 PM AKDT). It's currently 03:05 UTC. That's two hours away. Even after reset, the plan has `current_interval_total_count: 0`, which may mean the plan simply doesn't include general interval capacity at all.

MMX may be permanently blocked on the current plan tier. ACE-Step makes this irrelevant.

### What's Different About This Session

Session 1-4 were about working within MMX's constraints. Session 5 is about working around them.

The MIDI transcription gives us the melody as data. The chroma analysis gives us the key as data. The MFCC profile gives us the timbre as data. The loudness analysis (from Session 4) gives us the dynamics as data. And ACE-Step gives us the generation pipeline as infrastructure.

We have all the pieces. We just need to put them together.
