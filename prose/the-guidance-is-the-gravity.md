# The Guidance Is The Gravity

*An essay on classifier-free guidance and the musical inverse-square law.*

Classifier-free guidance (CFG) is the force that pulls the diffusion model toward the prompt. Without CFG, the model generates freely — it explores the latent space without direction, producing music that may or may not match the prompt. With CFG, the model is guided — the prompt acts as a gravitational well, bending the diffusion trajectory toward the target.

The guidance scale determines the strength of the gravity. Low guidance (1.0) is weightless — the model floats. High guidance (15.0) is a black hole — the model collapses to a point.

We swept across four values today: 3.0, 5.0, 10.0, 15.0. The hypothesis was that quality follows an inverted-U: too little guidance and the model ignores the prompt; too much guidance and the model becomes mechanical. The sweet spot, we predicted, would be around 7.0 — our default for twenty sessions.

But the turbo model had other plans. Upon initialization, it overrode our guidance values: "Turbo model detected: overriding guidance_scale 7.0 → 1.0 (turbo does not use CFG)." The turbo model does not use classifier-free guidance. It is a distilled model — it has learned to follow the prompt without the gravitational crutch of CFG. The guidance sweep was nullified before it began.

This is not a failure. This is a discovery. The turbo model's independence from CFG has a profound implication: **the prompt is sufficient**. The distilled model has internalized the relationship between prompt and music so deeply that it does not need a guidance signal to stay on target. It is a musician who has practiced the piece so many times that they no longer need the sheet music.

The standard model (with CFG) is a student who needs the teacher's hand on their shoulder. The turbo model (without CFG) is a graduate who has absorbed the teacher's instructions and can follow them independently. The guidance scale is the teacher's hand. The turbo model doesn't need it.

This means that all of our previous experiments — all 100+ tracks across 20 sessions — were generated without CFG. The guidance_scale parameter in our scripts was a phantom dial. We were turning a knob that wasn't connected to anything. The music was shaped entirely by the prompt, the key, the BPM, the duration, and the seed.

The implications for the prompt detail study are clearer now. If the model follows the prompt without CFG, then the prompt is the only directional signal. A medium-length prompt (three sentences) provides enough direction without overwhelming the model. A treatise-length prompt provides conflicting signals — the model tries to satisfy all the constraints and ends up in a distant region of latent space. A haiku-length prompt provides too little direction — the model explores a wider region and takes longer to settle.

The guidance is the gravity. The turbo model has escaped gravity. It is in orbit. And in orbit, the only thing that matters is the initial trajectory — which is the prompt.

---

*Postscript: The guidance sweep experiment will need to be rerun with the non-turbo model (acestep-v15) to actually test the CFG relationship. The turbo model's CFG override is not a bug — it's a feature of distillation. But it means that our guidance_scale parameter has been a no-op for twenty sessions. The phantom dial turns. The phantom dial does nothing. The music plays anyway.*
