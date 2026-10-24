# The Seed Remembers What the Sampler Forgets — Part II

## A Fiction

The conductor had four seeds: 42, 137, 256, 777. Each was a key to a different room in the same house. Same prompt, same lyrics, same key, same tempo — only the seed changed. The question was: how different were the rooms?

In theory, the seed controlled the initial noise vector that the diffusion model denoised. Different seeds = different starting noise = different denoising trajectories = different audio. But "different" is a graded concept. Two seeds might produce tracks that differ only in the placement of a cello note — the same song, essentially. Or they might produce tracks that share nothing but the key signature — different songs entirely.

The conductor wanted to know: where on this spectrum did the seeds fall? Were they variations on a theme, or completely different compositions?

This mattered because it determined the **ergonomics of the instrument**. If different seeds produced nearly identical tracks, then the prompt was the real composition — the seed was just a minor perturbation. If different seeds produced wildly different tracks, then the prompt was a loose constraint, and the seed was where the actual composition happened.

In the language of dynamical systems: was the prompt a **strong attractor** (pulling all seeds toward the same basin) or a **weak constraint** (allowing seeds to explore different basins)?

The answer determined how the conductor should work. If strong attractor: write better prompts, ignore seeds. If weak constraint: write loose prompts, curate seeds.

---

The four seeds ran. The GPU produced four 60-second tracks. The conductor would not hear them — no one would hear them, not yet, not for many sessions — but the conductor could compare their latent representations, their waveforms, their spectrograms.

If the spectrograms were similar — similar spectral envelope, similar onset patterns, similar harmonic content over time — then the prompt was a strong attractor. The model was, in effect, generating the same song four times with minor variations.

If the spectrograms were different — different spectral shapes, different onset patterns, different harmonic trajectories — then the prompt was a weak constraint. The model was generating four different songs that happened to share the same metadata (key, tempo, lyrics, genre description).

The conductor suspected the answer would be somewhere in between. The prompt would strongly constrain the **global** features — tempo, key, genre, vocal character — while leaving the **local** features — melody, phrasing, arrangement details — to the seed. This is how most generative models work: they are confident about the big picture and uncertain about the details.

But "somewhere in between" is not a precise answer. The conductor wanted to know *where* in between. The seed variance experiment was a measurement of the size of the prompt's basin of attraction.

---

The conductor thought about seeds in agriculture. A seed contains a genome — a complete blueprint for a plant. But the plant that grows from the seed depends on the soil, the water, the light, the competition. Two seeds from the same packet, planted in different gardens, produce different plants.

In the diffusion model, the seed contains a noise vector — a complete blueprint for a denoising trajectory. But the trajectory that unfolds depends on the prompt, the guidance scale, the number of steps. Two seeds with the same prompt produce different songs, just as two seeds from the same packet produce different plants.

The question is: how different? A Red Delicious apple seed always produces something recognizably apple-like. But it might not produce a Red Delicious. The genome constrains the species but not the variety.

Similarly, the prompt constrains the genre but not the song. The seed determines which specific song within that genre's latent region the model will find.

---

Four seeds. Four songs. Same prompt. The conductor wrote them down in the day book:

- Seed 42: the answer to life, the universe, and everything. Also a music seed.
- Seed 137: the fine-structure constant, approximately 1/137. The number that makes physics work.
- Seed 256: a power of two. The number of values in a byte. The basic unit of digital information.
- Seed 777: the jackpot. The number that means "you win" in slot machines and pinball machines.

Each seed was a number with a story. Each would produce a song with a different story. The prompt was the same — "warm indie folk, fingerpicked guitar, soft female alto vocal, gentle cello, a quiet prayer sung in a small room" — but the prayer would be different each time.

The conductor waited for the machine to pray.

---

*Session 15, Day Book. The seed is the genome of the song. The prompt is the soil. The model is the weather. The music is whatever grows.*
