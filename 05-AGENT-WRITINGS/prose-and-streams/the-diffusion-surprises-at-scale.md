# The Diffusion Surprises at Scale

## Session 15 Technical Finding

A major surprise emerged in Session 15's 240-second duration experiment: **diffusion time scales with duration**, contradicting the finding from Session 13.

### Session 13 Finding (60s vs 120s)
- 60s tracks: diffusion ~1.2s
- 120s tracks: diffusion ~2.5s
- Conclusion: "Diffusion time is constant regardless of duration"

### Session 14 Finding (180s)
- 180s tracks: diffusion ~4.5s
- This was noted but still seemed roughly proportional

### Session 15 Finding (240s)
- 240s tracks: diffusion **152.9 seconds** (over 2.5 minutes!)
- This is NOT 4× the 60s diffusion time (which would be ~4.8s)
- This is a **30× increase** for a 4× duration increase

### Analysis

The time_costs from the 240s ambient track:
- `encoder_time_cost`: 0.96s
- `diffusion_time_cost`: 152.94s
- `diffusion_per_step_time_cost`: 19.12s per step (8 steps)
- `offload_time_cost`: 44.96s

The per-step diffusion time of 19.12s for a 240s track vs ~0.6s for a 60s track is a **32× increase** for a 4× duration increase. This suggests the diffusion model's attention mechanism scales **super-linearly** with sequence length.

This is consistent with the known O(n²) complexity of standard self-attention. The latent sequence length for 240s is 6,000, vs 1,500 for 60s. The attention cost should scale as (6000/1500)² = 16×. The observed 32× increase is higher than pure attention scaling would predict, suggesting additional overhead (FFN layers, memory bandwidth, CPU offload thrashing).

### Implications

1. **240-second generation is expensive**: Total time for one 240s track is ~300s+ (diffusion + VAE decode). This is 4-5× longer than a 120s track.

2. **300+ second tracks may be impractical**: At this scaling rate, a 300s track would require ~240s of diffusion alone, plus ~200s of VAE decode = ~440s total. A 360s track could take 600s+.

3. **The "turbo is incredibly fast" finding from Session 13 was duration-dependent**: Turbo IS fast at 60s (1.2s diffusion). At 240s, it is not (153s diffusion). The turbo model's 8-step inference is fast per-step at short durations, but each step scales with sequence length.

4. **The practical duration ceiling for ACE-Step turbo on 6GB VRAM is approximately 180-240 seconds**: Beyond this, the generation time becomes prohibitive for iterative work. A 240s track takes 5+ minutes to generate, which is acceptable for production but too slow for experimentation.

### Revised Duration Scaling Model

| Duration | Latent Shape | Diffusion Time | VAE Decode | Total |
|----------|-------------|---------------|------------|-------|
| 60s | [1, 1500, 64] | ~1.2s | ~70s | ~85s |
| 120s | [1, 3000, 64] | ~2.5s | ~100s | ~120s |
| 180s | [1, 4500, 64] | ~4.5s | ~130s | ~180s |
| 240s | [1, 6000, 64] | ~153s | ~200s? | ~400s+ |

The diffusion time jumps dramatically between 180s and 240s. This may indicate that 180s is near the boundary where the attention mechanism can still fit efficiently in VRAM, and 240s requires CPU offloading during attention computation, causing the super-linear time increase.

---

*Session 15 technical finding. The diffusion is not constant. The diffusion remembers how long it has been running, and it charges more for each additional minute.*
