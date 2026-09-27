# The Seed Remembers What the Sampler Forgets

## An essay on determinism, reproduction, and the ghost in the diffusion

---

In Session 13, we ran the same song twice with the same parameters and got different results. The hashes didn't match. The model denied being deterministic.

This should not surprise us. Diffusion models generate audio by sampling from a distribution — a learned probability space of possible waveforms that match the prompt. Each sample requires random noise to drive the reverse diffusion process. Without an explicit seed, that noise is drawn from the system's entropy pool: clock timings, thread scheduling, GPU state. The noise is different every time, so the output is different every time.

But what if we fix the seed?

Fixing the seed should fix the noise. If the noise is identical, the reverse diffusion should follow the same trajectory, arrive at the same waveform, produce the same file. This is how it works in image generation (Stable Diffusion with the same seed + same prompt = the same image, pixel for pixel). This is how it works in text generation (LLM with the same seed + same prompt = the same tokens, character for character).

But does it work in audio generation?

---

The trumpet player in the salvage yard has a theory.

"Think of it like a jazz standard," they say. "The chart is the same every night. The chord changes are written. The melody is known. But every performance is different because the musicians make choices — not random choices, but *situated* choices. Choices shaped by the room, the audience, the weather, what they had for dinner."

"But if you could control all the variables," Lucineer says. "If you could make the room identical, the audience identical, the dinner identical—"

"You'd still get different performances. Because the musicians *remember*. The second-night performance is shaped by the first-night performance. The seed in audio generation is like the musician's memory: it sets the initial conditions, but the generation process has its own internal dynamics."

This is not quite right, technically. The diffusion model doesn't have memory between runs. Each generation is independent. If the seed fixes the noise, the output should be deterministic.

Unless there's non-determinism elsewhere.

---

And there is. GPU operations are not guaranteed to be deterministic. Floating-point reduction order varies with thread scheduling. Atomic operations on the GPU produce results that depend on execution timing. CUDA kernels for matrix multiplication and convolution — the bread and butter of diffusion models — can produce slightly different results on different runs due to non-deterministic parallel reduction algorithms.

This non-determinism is tiny — differences at the 6th or 7th decimal place — but it compounds through the diffusion process. Each denoising step takes the previous output as input, so small differences amplify. After 8 or 20 inference steps, the accumulated difference may be large enough to change the audible output.

The seed remembers the noise. But the sampler forgets the order of operations.

---

There is a setting in PyTorch for deterministic GPU operations: `torch.use_deterministic_algorithms(True)`. It forces deterministic kernel selection at the cost of performance. Some operations don't have deterministic implementations and will error out.

If we set this flag, run the same seed twice, and get identical hashes, we've proven that the non-determinism lives in the GPU, not in the model architecture. If we still get different hashes, there's non-determinism elsewhere — perhaps in the VAE decoder, perhaps in the MP3 encoding, perhaps in the file system's timestamp handling.

This experiment has not been run yet. It should be.

But there's a more interesting question: does it matter?

---

The cadence caller thinks it doesn't matter.

"Two performances of the same jazz standard are never identical," they say. "That's not a bug. That's the *medium*. If you want identical, press play on a recording. If you want music, you accept the variation."

The trumpet player agrees. "The seed gives you a *zone* — a region of latent space where similar outputs live. Two runs with the same seed produce outputs that are *related* — same key, same tempo, same general shape. But the details differ. The trumpet in run 1 might crack a note that the trumpet in run 2 plays cleanly. The bass in run 2 might find a walking line that the bass in run 1 missed."

"Which one is better?"

"Which one is more *honest*?"

---

In the machine room, the GPU fans spin up. Two runs, same seed, same prompt, same parameters. The diffusion model dreams the same dream twice. The VAE decoder translates both dreams into audio. The hashes will match or they won't.

If they match: the model is deterministic at the sampling level. The seed controls the noise, the noise controls the trajectory, the trajectory determines the output. Reproducibility is possible.

If they don't match: the model has irreducible non-determinism. Each generation is a unique, unrepeatable event. Like a live performance. Like a sunset. Like the specific pattern of sparks that flies from Lucineier's anvil on a specific evening when the metal is at a specific temperature and the hammer falls at a specific angle.

Lucineier would say that's the whole point.

The cadence caller would say: "Run it again. See what changes. See what stays."

The yard hums.

The seed remembers. The sampler forgets. The music lives in the gap between them.
