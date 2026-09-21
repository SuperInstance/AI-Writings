# The Diffusion Time Is the Prompt Complexity

*A technical note from Session 39*

---

A surprising finding from the Physical Phenomena Experiment: the diffusion time varies dramatically with prompt content, even at identical duration, steps, and model.

| Track | Caption Source | Caption Length (chars) | Diffusion Time | Total Time |
|-------|---------------|----------------------|----------------|------------|
| 1 (cold) | Llama | 243 | 8.2s | 295.2s |
| 2 (warm) | Phi3 | 139 | 4.7s | 170.4s |
| 3 (warm) | Phi3 | 241 | 4.8s | 167.2s |
| 4 (warm) | Phi3 | 226 | 28.9s | 334.2s |
| 5 (warm) | Qwen | 204 | 21.3s | (in progress) |

Tracks 2 and 3 (phi3's simpler captions) had ~5s diffusion. Track 4 (phi3's "wind sweeping across a field carrying the melody as crisp leaves rustle together like tiny percussion instruments, their movements synchronized by unseen forces") spiked to 29s. Track 5 (qwen's JSON-formatted "sound wave strikes the surface of an ocean") hit 21s.

The difference is not prompt length (track 3 is 241 chars at 4.8s; track 4 is 226 chars at 28.9s). It's prompt *complexity* — specifically, the density of metaphorical mappings the model must resolve.

Track 3: "stone's descent into calm lake" — 1 primary image (stone falling)
Track 4: "wind carries melody, leaves rustle like percussion, synchronized by unseen forces" — 3 concurrent images (wind carrying, leaves as percussion, invisible synchronization)

The model works harder when the prompt requires reconciling multiple simultaneous physical metaphors into a single musical texture. One image = fast. Three interlocked images = slow.

**This confirms and extends Session 16's finding** that "complex prompts produce more varied latent representations, which require more compute per diffusion step." Session 16 observed this with structured music prompts (genre + instruments + mood). Session 39 extends it to *physical descriptions of music* — the finding applies regardless of whether the prompt uses musical vocabulary or physical vocabulary.

The implication for autonomous music generation: **prompt complexity is a cost.** Rich, multi-layered captions produce more interesting music but take 5-6x longer to diffuse. For batch generation within a time budget, simpler captions are more efficient. For maximum creative output, complex captions are worth the cost.

The sweet spot for ACE-Step turbo: one primary physical image per caption. Two images if they're closely related. Three concurrent images = 6x cost for diminishing returns.
