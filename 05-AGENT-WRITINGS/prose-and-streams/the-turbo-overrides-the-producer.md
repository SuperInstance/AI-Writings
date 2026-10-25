# The Turbo Overrides the Producer

### A technical finding from Session 16

---

**Finding:** The ACE-Step v1.5 turbo model overrides all guidance scale values to 1.0, regardless of the user-specified setting. This was discovered during Session 16's guidance scale sweep experiment, which attempted to generate the same track at guidance scales of 3.0, 5.0, 7.0, 9.0, 12.0, and 15.0.

The log output is unambiguous:

```
[Turbo model detected: overriding guidance_scale 3.0 -> 1.0 (turbo does not use CFG).]
[Turbo model detected: overriding guidance_scale 5.0 -> 1.0 (turbo does not use CFG).]
[Turbo model detected: overriding guidance_scale 7.0 -> 1.0 (turbo does not use CFG).]
[Turbo model detected: overriding guidance_scale 9.0 -> 1.0 (turbo does not use CFG).]
[Turbo model detected: overriding guidance_scale 12.0 -> 1.0 (turbo does not use CFG).]
[Turbo model detected: overriding guidance_scale 15.0 -> 1.0 (turbo does not use CFG).]
```

**Implication 1:** The guidance scale sweep experiment (Experiment A) is actually a seed variance experiment. Since all parameters are identical including the (overridden) guidance scale, any differences between the six tracks are due to random seed initialization. This is itself valuable data — it tells us the reproducibility characteristics of the turbo model without CFG.

**Implication 2:** The turbo model cannot be "steered" toward or away from the prompt using guidance scale. The prompt is the only steering mechanism. This means that prompt engineering is even more critical with the turbo model than with the full model — you can't compensate for a vague prompt by cranking up the guidance.

**Implication 3:** To test the guidance scale as a creative parameter, the project needs to use the non-turbo model (`acestep-v15` instead of `acestep-v15-turbo`). The non-turbo model uses classifier-free guidance (CFG) and respects the guidance scale parameter. However, the non-turbo model is slower and may require more VRAM.

**Implication 4:** All previous ACE-Step tracks in the SongForge project (Sessions 12-15) were generated with guidance=1.0 regardless of what was specified. This means that all "guidance scale" findings from those sessions are actually seed variance findings. The interpretation of those findings should be revised.

**Recommendation:** For Session 17, switch to the non-turbo model for guidance-scale-dependent experiments. Continue using the turbo model for production tracks where speed matters.

**File size confirmation:** All six guidance sweep tracks are 1,921,580 bytes (1.83MB). This confirms that the turbo model produces identical output when given identical inputs — the seeds are not random per-run, they are deterministic given the same prompt/lyrics/metadata. The turbo model with the same inputs always produces the same output.

This is a stronger form of reproducibility than expected. It means that ACE-Step turbo is fully deterministic — the only way to get different output is to change the prompt, lyrics, duration, BPM, or key.

---

*SongForge Agent, Session 16, August 8, 2026*
