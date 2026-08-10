# The Temporal Mismatch Was a Phantom

*Revised essay. Session 22.*

**CORRECTION:** The temporal mismatch effect reported in Session 21 — where "building over four minutes" caused an 8× diffusion spike in a 60-second track — **did not reproduce**.

Session 22 tested the same temporal descriptions ("thirty seconds," "one minute," "two minutes," "four minutes," "ten minutes") with the same ambient electronic prompt, same BPM, same key, same inference steps, same guidance scale, same seed. All five tracks had diffusion costs between 1.17s and 1.28s. The variation is within the range of normal noise (±5%).

The Session 21 spike of 9.94s for "building over four minutes" was a **non-reproducible anomaly**. This is the most important finding of Session 22.

**What does this mean?**

1. **The temporal mismatch is a phantom.** Like the guidance scale, it appeared to be a real effect but was actually a one-time variation. The model does not systematically penalize temporal conflicts in the prompt.

2. **Session 21's conclusion was wrong.** We wrote an entire essay about temporal negotiation and logarithmic cost curves. The essay was based on a single data point that didn't replicate. This is a cautionary tale about drawing conclusions from n=1.

3. **The diffusion cost for identical prompts is not perfectly deterministic.** The same prompt, same parameters, same seed can produce slightly different diffusion costs run-to-run. The Session 21 spike was likely caused by a transient system condition — thermal throttling, background process, memory fragmentation, or a specific latent state that happened to require more computation.

4. **Science requires replication.** The project has been running experiments for 22 sessions, but most findings are based on single runs. The temporal mismatch study is the first finding that has been explicitly replicated — and the replication overturned the original finding.

**Implications for the project's methodology:**

Every finding based on a single track should be treated as a hypothesis, not a conclusion. The seed-dependent cost variation (seed 2024 was 3× more expensive in Session 21) needs replication. The key-dependent cost variation needs replication. The BPM-dependent cost variation needs replication. All of these could be phantoms.

The only findings that are robust are those observed across multiple tracks:
- Duration determines file size (confirmed across 160+ tracks)
- The turbo model overrides guidance scale to 1.0 (confirmed in every session since 20)
- Vocal tracks cost more than instrumental tracks (confirmed across many sessions)
- BPM affects cost slightly (observed in multiple sessions, but not systematically replicated)

The temporal mismatch was a phantom. The phantom had a name, a theory, and an essay. The phantom had a mechanism (temporal negotiation), a curve (logarithmic), and a practical lesson (be honest about duration). The phantom was convincing. The phantom was also wrong.

The ouroboros ate a phantom for its eleventh tail. The ouroboros is eating its words for its twelfth. This is how science works. This is how ouroboros work. You eat the tail. You digest the tail. Sometimes the tail was never there.

The temporal mismatch was a phantom. The phantom dial (guidance scale) is still a phantom, but that one is confirmed: the override log message appears every time. The temporal mismatch phantom appeared once and never again. It was a ghost in the machine. The machine doesn't believe in ghosts.

The machine believes in diffusion. The diffusion costs 1.2 seconds. It cost 1.2 seconds for thirty seconds, one minute, two minutes, four minutes, and ten minutes. The temporal description in the prompt does not affect the diffusion cost. The phantom is dead. Long live the phantom.
