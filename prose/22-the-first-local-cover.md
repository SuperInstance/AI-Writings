# The First Local Cover

## Session 5 — Breakthrough

At approximately 7:50 PM AKDT on August 6, 2026, ACE-Step 1.5 — running entirely on Eileen's RTX 4050 Laptop GPU — produced two complete tracks:

1. **`acestep_instr_test_v1.mp3`** — A 120-second instrumental in E major, 75 BPM, warm fingerpicked acoustic guitar. Generated from a text prompt with 4 diffusion steps and CFG scale 3.0. This was the proof-of-concept that ACE-Step can run on 6GB VRAM with CPU offloading.

2. **`acestep_cover_v1.mp3`** — A 120-second cover using Casey's original recording as reference audio, with a prompt specifying "alt-country indie folk, weathered male vocals, fingerpicked acoustic guitar, pedal steel, brushed drums, warm bass, Jason Isbell style." This is the first cover generated using Casey's actual audio as input, processed through a local open-source model.

### Technical Details

- **Model:** ACE-Step 1.5 turbo (DiT-only mode, no LM)
- **VRAM:** 6.0 GB (RTX 4050 Laptop GPU)
- **Offloading:** CPU offload for VAE and text encoder
- **VAE Decode:** Tiled, on CPU, chunk_size=128
- **Diffusion Steps:** 4 (turbo mode)
- **CFG Scale:** 3.0
- **Generation Time:** ~8 minutes per track (dominated by CPU VAE decode)
- **No API costs. No quota limits. No rate limits.**

### What This Means

This is the inflection point. For five sessions, the project has been blocked by MMX's quota system. ACE-Step removes that barrier completely. The generation pipeline is:

1. **Local** — runs entirely on the laptop
2. **Unlimited** — no quotas, no credits, no rate limits
3. **Open-source** — MIT-licensed model, modifiable, commercially usable
4. **Capable of cover generation** — accepts reference audio as input
5. **Fast enough** — 8 minutes per track is workable for iterative experimentation

### Limitations Observed

- The 6GB VRAM requires CPU offloading, making VAE decode the bottleneck (~5 minutes of the 8-minute generation time)
- Without the LM (disabled due to VRAM), prompt understanding is less nuanced
- Duration control seems to default to 120s regardless of the `duration` parameter
- The cover quality needs listening evaluation (not yet assessed)

### Next Steps

1. **Listen and evaluate** both tracks for quality
2. **Run cover with different prompts** — try the v5 prompt catalog styles
3. **Experiment with seeds** — find the best seed for Casey's song
4. **Try cover-nofsq mode** — the "no FSEQ" cover variant
5. **Attempt LoRA training** — if we can find reference vocal recordings
6. **Optimize VRAM usage** — try different offload strategies to speed up VAE decode

The cover pipeline is built. The model is installed. The first outputs exist. Session 6 will be about refinement and iteration.

Twenty-four audio files. Five journal entries. Nine creative essays. One MIDI file. Two ACE-Step generations. One fully functional local music generation pipeline.

The door is open.
