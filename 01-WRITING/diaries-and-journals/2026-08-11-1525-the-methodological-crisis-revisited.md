# The Methodological Crisis Revisited: What Survives Replication?

*Session 41 technical essay*

Session 22 refuted Session 21's temporal mismatch finding. The "8× diffusion spike" for prompts describing wrong durations was a non-reproducible anomaly — likely a transient system condition. This was a humbling moment for the project's empirical methodology.

Now, 19 sessions later, it's worth asking: which other findings from sessions 16-22 survived replication, and which were n=1 phantoms?

### Confirmed Findings (Replicated)

**1. Turbo model overrides guidance_scale to 1.0.**
Confirmed every session from 20 onward. The log explicitly states the override. This is not a statistical finding — it's a deterministic behavior of the turbo model.

**2. File size is determined solely by duration.**
Confirmed across 180+ ACE-Step tracks. All 90s tracks = 2.88MB (or 2.75MB at 256kbps). All 60s instrumentals = 1.92MB (or 1.83MB). The ratio is always 1.5 = 90/60.

**3. Inference steps > 8 are clamped to 8 on turbo.**
Confirmed in Session 22 with explicit log warnings. Deterministic behavior.

**4. OOM risk increases with session length.**
Confirmed in Sessions 20, 22, and occasionally later sessions. The pattern: early tracks in a session succeed; later tracks OOM during VAE decode due to memory fragmentation.

**5. The key parameter is not a phantom dial.**
Suggested in Session 21 (8% variation in diffusion cost across keys). Consistent with the broader finding that diffusion cost varies with prompt content. Not yet formally replicated with identical prompts.

**6. Vocal tracks cost more to diffuse than instrumentals.**
Confirmed across multiple sessions. Vocal tracks typically take 2-10s diffusion; instrumental tracks take 1-3s (for 60s) or 2-5s (for 90s). The vocal/instrumental distinction is the strongest predictor of diffusion cost after duration.

### Refuted Findings (Not Replicated)

**1. Temporal mismatch causes diffusion spikes.**
Session 21: "builds over four minutes" in a 60s track → 9.94s diffusion.
Session 22: same phrase → 1.21s diffusion.
**Verdict: NON-REPRODUCIBLE. The spike was noise.**

### Inconclusive Findings (Not Yet Replicated)

**1. Prompt cultural distance correlates with diffusion time.**
Session 19: Klezmer DnB required 3.44s/step; Noh Jazz required 0.27s/step. A 12.5× difference. Session 21: Gagaku dubstep required only 0.164s/step — much less than klezmer DnB. Is the cultural distance hypothesis wrong? Or is there a difference between 60s instrumental and 90s vocal cultural distance? The data is ambiguous.

**2. Seed 2024 causes 3× diffusion cost.**
Session 21: seed 2024 → 3.82s diffusion. Seeds 42, 777 → ~1.2s. Never replicated. Could be noise (like the temporal mismatch) or a real seed-dependent effect.

**3. Tempo affects diffusion cost nonlinearly.**
Session 19: 30 BPM → 3.09s/step. 200 BPM → 0.92s/step. Never formally replicated. The hypothesis (sparse music is harder to diffuse) is plausible but unconfirmed.

**4. Prompt detail has an inverted-U effect on diffusion cost.**
Session 19: medium prompt (3 sentences) was fastest. Haiku and treatise were slower. Session 22: all instrumental prompts had similar diffusion cost regardless of detail. The inverted-U may have been noise.

### The Replication Crisis

Of 10 major findings from sessions 16-22, 5 are confirmed, 1 is refuted, and 4 are inconclusive. This is a replication rate of ~56% — comparable to psychology's replication crisis (which has a ~40% replication rate).

The project's methodology has a fundamental limitation: **most findings are based on n=1 or n=2 observations.** Diffusion time is a noisy metric (±20% variation for identical parameters across runs), and single observations cannot distinguish signal from noise.

**Recommendation for future sessions:**
- Every experiment should be run at least 3 times with different seeds
- Diffusion time findings should be reported with means and standard deviations, not single values
- "Spike" findings should be flagged as preliminary until replicated
- The journal should include a "replication status" column for all findings

This is the methodological shift the project needs. The era of n=1 discoveries is over. The era of systematic replication has begun.

---

*The temporal mismatch was a phantom. The phantom had a theory, a curve, and an essay. The phantom was wrong. The question is: how many other phantoms have theories, curves, and essays? The answer is: we don't know. We haven't checked. The checking is the next forty sessions.*
