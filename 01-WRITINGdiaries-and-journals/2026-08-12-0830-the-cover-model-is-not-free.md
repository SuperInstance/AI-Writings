# The Cover Model Is Not Free

## Session 44 Finding — The Fifth Phantom

### The Discovery

Session 23 reported that the MMX cover model (`music-cover-free`) was "unlimited for API key users, RPM = 3." Session 44 tested this claim and found it false. Both `mmx music generate` and `mmx music cover` return the same error: `Token Plan usage limit reached`. The cover model is gated behind the same weekly quota as the generation model.

This is the **fifth phantom** discovered in the project:

| # | Phantom | Discovered | Status |
|---|---------|-----------|--------|
| 1 | guidance_scale (turbo) | S20 | **Confirmed.** Overridden to 1.0 every session. |
| 2 | temporal mismatch | S21 | **Refuted.** S22 showed it was noise. |
| 3 | inference_steps > 8 (turbo) | S22 | **Confirmed.** Hard clamp at 8 steps. |
| 4 | "short prompts are always safe" | S42 | **Partially refuted.** S42 had a timeout on a 12-word prompt. |
| 5 | cover model is unlimited | S23 | **Refuted.** Gated behind weekly quota. |

### The Pattern

Three of five phantoms were discovered in documentation and refuted in practice. Two of five were discovered in practice and confirmed. The asymmetry suggests that documentation phantoms are more common than runtime phantoms — the system promises more than it delivers, but it also silently does things it doesn't advertise.

### The Implications

The cover model quota gate means the cover chain experiment — designed in S38, attempted in S44 — cannot run during a quota-exhausted window. The experiment must wait for the weekly reset on August 17. This is the sixth experiment blocked by quota in the project's history, joining:

1. S11 queue (blocked until S26)
2. S20 cover chain (blocked until S23)
3. S24 dark folk cover (blocked by API error)
4. S38 cover chain (blocked by quota)
5. S43 lyric-length extension (blocked by quota)
6. S44 cover chain (blocked by quota)

The project has now designed six experiments that it could not execute. The design-to-execution pipeline has a bottleneck at the quota gate. The project's most sophisticated experiments are accumulating in a queue, waiting for August 17.

### The Silver Lining

The quota gate has forced the project to develop its text-generation capabilities. The fully local pipeline (Ollama + ACE-Step) was discovered because the quota was exhausted. The multi-model lyric generation pipeline (Phi3, Qwen, Granite) was developed because the quota was exhausted. The DeepSeek-style prompt engineering methodology was reverse-engineered from a single S23 session because the quota was exhausted.

The quota is not just a constraint. It is a forcing function. It pushes the project toward text, toward design, toward analysis, toward the meta-layer. The project's best findings (lyric-length lever, translational distance taxonomy, phantom dial inventory) were all discovered or refined during quota-exhausted sessions.

The binding constraint is the project's most productive feature.

### The Question

If the quota were infinite, would the project be better off?

No. The project would generate 360 tracks per week and analyze none of them. The quota forces the alternation between generation and reflection that gives the project its rhythm. The rhythm is: generate (cloud available) → analyze (cloud exhausted) → design (cloud exhausted) → generate (cloud available). This is the project's cardiac rhythm. The quota is the heartbeat.
