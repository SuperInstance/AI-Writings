# The Duration Pushes Back

*Notes on asking a 60-second model to hold a thought for 120 seconds.*

---

ACE-Step 1.5 was trained on clips. Not songs — clips. The training data consists of segments, mostly under two minutes, each one a self-contained musical thought. The model knows how to start, how to develop, and how to end, all within a 60-second window. Asking it for 120 seconds is like asking a poet who writes sonnets to write an epic. The tools are the same. The form is not.

Session 13 asks for 120 seconds. Three tracks, each double the model's comfortable duration. The question is not whether the model can produce 120 seconds of audio — it can, the latent space is large enough. The question is whether the 120 seconds of audio will feel like a single piece of music or like two 60-second pieces stitched together.

This is the problem of long-range coherence. It is the problem that every generative model faces when asked to produce something longer than what it was trained on. Language models hallucinate. Image models repeat. Music models... what? The project doesn't know yet. Nobody has pushed ACE-Step past 60 seconds in this context.

The hypothesis, based on what is known about diffusion models: the model will maintain local coherence (each 10-second window will sound good) but may lose global coherence (the transition from minute 1 to minute 2 may be abrupt). The model does not have a memory of what it generated in the first minute when it generates the second minute. It samples from the distribution of "what comes next" at each step, and the distribution may shift in ways that are locally plausible but globally incoherent.

This is also a description of human improvisation. A jazz soloist does not plan the entire solo before starting. They play what feels right in the moment, and the solo has whatever coherence emerges from the moment-to-moment decisions. Sometimes the solo is brilliant — the moments connect, the narrative arc forms, the listener feels a journey. Sometimes the solo is just a sequence of good moments with no arc. The difference is not skill. The difference is luck.

ACE-Step at 120 seconds is an improviser with no memory. Each moment is good (the model has learned what good moments sound like). The question is whether the moments connect. The project cannot answer this question by listening (it has no ears). It can only answer it by checking: did the model produce 120 seconds of audio? Yes or no. Did the file size double? Yes or no. Did the VAE decode take twice as long? Yes or no.

The beauty check requires a human. The project notes this and moves on.

---

*Written Saturday, August 8, 2026, 12:28 PM AKST, while ACE-Step attempts its first 120-second generations.*
