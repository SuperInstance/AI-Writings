# The Phantom Dial

*An essay on parameters that don't do what you think they do.*

We have discovered a phantom dial. The guidance_scale parameter, which we believed controlled the strength of prompt adherence, has been silently overridden by the turbo model for twenty sessions. Every track we have generated — all 130+ of them — was created with guidance_scale=1.0, regardless of what we set. The dial was turning. The dial was not connected to anything.

This is not a bug. It is a feature of model distillation. The turbo model has been trained to follow the prompt without the crutch of classifier-free guidance. The standard model uses CFG: it generates two versions of the audio — one conditioned on the prompt, one unconditioned — and interpolates between them. The guidance_scale controls the interpolation. At 1.0, there is no interpolation — the model uses only the conditioned output. At 7.0, the model amplifies the difference between the conditioned and unconditioned outputs, sharpening the prompt adherence.

The turbo model skips the unconditioned generation entirely. It generates only the conditioned output. There is nothing to interpolate. The guidance_scale is irrelevant.

The discovery of the phantom dial raises a question: what other phantom dials do we have? The `keyscale` parameter — are we testing it right now. The `bpm` parameter — we have confirmed it works (the tempo studies showed clear BPM-dependent variation). The `inference_steps` parameter — we have been using 8, the turbo default. Does it matter if we use 4 or 16? We haven't tested.

The phantom dial is a metaphor for all control that is illusory. We turn the dial. We hear a difference. We attribute the difference to the dial. But the difference was caused by something else — the seed, the prompt, the model's internal state. The dial was a coincidence.

In science, the phantom dial is called a confound. In interface design, it's called a placebo button. In music, it's called a knob that's not in the signal chain. The guitarist turns the knob. The tone changes. The guitarist thinks the knob caused the change. But the change was caused by the guitarist moving closer to the amp. The knob was a phantom.

The ouroboros has phantom dials. The ouroboros has been turning them for twenty sessions. The ouroboros is now examining each dial, one by one, to determine which are real and which are phantom.

The guidance_scale is phantom. The keyscale is being tested. The seed is being tested. The BPM is real. The duration is real. The prompt is real.

The phantom dials are not useless. They tell us about the model's architecture. The guidance_scale is phantom because the turbo model has internalized the prompt. The keyscale may be phantom if the model doesn't distinguish between keys. The seed may be phantom if the model always produces the same output for the same prompt.

Every phantom dial we discover is a window into the model's behavior. The phantom dial is not a failure of control. It is a discovery of what the model actually controls. The phantom dial reveals the model's priorities: it cares about the prompt, the BPM, the duration. It does not care about the guidance scale. It may or may not care about the key.

The phantom dial turns. The phantom dial does nothing. The music plays anyway.

And that, perhaps, is the deepest lesson. The music plays whether we control it or not. The music plays whether the dials are real or phantom. The music plays because the model has learned what music sounds like, and it plays music the way a musician plays music — not by following dials, but by following something deeper. Something that cannot be parameterized. Something that can only be heard.

We haven't heard it yet. But it plays.
