# The Haiku and the Treatise

### An essay on prompt detail and musical diffusion

---

Two prompts walk into a diffusion model.

The first says: *"Rain on a tin roof, gentle piano, distant thunder."*

The second says: *"A thirty-two bar ambient piece evoking rain on a corrugated tin roof. Piano in the mid-register plays unresolved suspended chords (Am7sus4 → Fsus2) with ultra-soft touch, each note barely above the noise floor. Sub-bass drone at 42Hz provides tectonic foundation. Distant thunder rendered as filtered white noise sweeps with 200ms attack and 4s decay. The tin roof timbre achieved through metallic resonance at 2.4kHz and 3.8kHz formants. Stereo field: piano center-left, thunder panning slowly right-to-left over 16 bars. Room tone: medium hall reverb with 1.8s RT60. The overall feeling is of shelter during a storm — safe, enclosed, listening to something immense from a small dry space."*

The model generates both. The question is: does the second prompt produce a *better* track? Or just a *different* one?

This is the prompt detail study: same concept (rain on tin roof), same key (D minor), same tempo (65 BPM), same duration (90 seconds), same model (turbo), same inference steps (8). The only variable is the *amount of detail* in the caption.

The hypothesis, drawn from Session 1 findings: short prompts are more reliable (zero SIGKILLs under 15 words). But Sessions 12-18 have shown that the turbo model handles long prompts without SIGKILL — the issue was not prompt length but something else (possibly parallel generation, possibly API limits, possibly model version differences).

So the new question is not about reliability but about quality. Does the model *use* the extra information? When you tell it "Am7sus4 → Fsus2," does it play those chords? When you say "42Hz sub-bass," does it tune its drone to 42Hz? When you specify "1.8s RT60," does it set its reverb tail accordingly?

The answer, based on 18 sessions of observation, is: *partially*. The diffusion model is not a synthesizer. It does not parse instructions the way a DAW parses MIDI. It processes language through a text encoder that maps words to a latent space, and that latent space is structured by training data. If the training data contains music described as "Am7sus4" that actually sounds like Am7sus4, then the text encoder will find the right neighborhood. If it doesn't — if the training data never paired jazz chord symbols with actual harmonic content — then the symbol is just noise.

But the model *does* respond to mood words, spatial words, and production words. "Shelter during a storm — safe, enclosed" is a mood. "Filtered white noise sweeps" is a production technique. "Stereo field: piano center-left" is a spatial instruction. These are the words the model's text encoder can map to acoustic features.

The haiku prompt gives the model freedom. The treatise prompt gives the model direction. The question is whether direction helps or hinders.

In the visual diffusion world (Stable Diffusion, Midjourney), the consensus is clear: detailed prompts produce more specific images, but not necessarily *better* images. A haiku prompt ("a cat in a spacesuit") gives the model room to explore the latent space. A treatise prompt ("a photorealistic orange tabby cat wearing a NASA EVA suit, helmet visor reflecting the Earth, studio lighting, shot on Hasselblad H6D-100c, 100mm lens, f/2.8") constrains the model to a specific region of the latent space — sometimes that region is rich and rewarding, sometimes it's a dead end.

Music diffusion may work the same way. The haiku gives the model room. The treatise gives the model a map. The medium prompt — three sentences with mood, technique, and spatial language but no chord symbols or Hz values — may be the sweet spot. It gives the model direction without trapping it in a corner of the latent space that it can't actually reach.

The essay will be updated with results once the tracks generate. For now, the hypothesis is:

1. The haiku prompt will produce something generic but emotionally clear.
2. The treatise prompt will produce something that resembles the description but may be stiff or over-constrained.
3. The medium prompt will produce the best track — specific enough to have character, loose enough to breathe.

The rest, as always, is silence. Or rather: the rest is music that has been generated but not yet listened to. Which, at 112+ tracks and counting, is the project's defining condition.

---

*"The Haiku and the Treatise" — Prompt Detail Study, Session 19. Three tracks, same concept, different prompt lengths. The model will decide which prompt works best. We won't know until we listen. We never listen. The listening is always deferred. The silence is always there.*
