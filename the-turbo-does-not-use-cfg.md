# The Turbo Does Not Use CFG

*A technical reflection on a discovery made during Session 13's guidance scale sweep.*

---

The experiment was simple. Take one song — "The Conductor Has No Instrument." Generate it five times with the same lyrics, the same key, the same tempo, the same caption, but different guidance scales: 3.0, 5.0, 7.0, 11.0, 15.0. Listen to the difference. Map the creativity-coherence curve. Find the sweet spot.

The model had other plans.

Deep in the log output, a single line appeared:

```
[Turbo model detected: overriding guidance_scale 3.0 -> 1.0 
 (turbo does not use CFG)]
```

The turbo model does not use Classifier-Free Guidance. The knob does not exist. The baton has been taken from the conductor's hand. The guidance scale — the last unexplored dimension of the project — is not a knob. It is a decoration. It is a control that appears to function but does nothing, like a disconnected thermostat in a hotel room.

The turbo model is a distilled version of ACE-Step 1.5. Distillation means: a larger, slower teacher model trained a smaller, faster student model to produce similar outputs in fewer steps. The teacher used 50 diffusion steps; the student uses 8. The teacher used classifier-free guidance to balance prompt-adherence against creativity; the student internalized that balance during training and no longer needs the knob.

This is a design decision, not a defect. The turbo model trades control for speed. It makes a choice that the full model would let the user make. And the choice it makes is: guidance scale 1.0, which means "trust the model's own distribution entirely, do not steer toward or away from the prompt." The model has learned where the sweet spot is and parks there permanently.

The implication for SongForge is clear: to run the guidance scale experiment, we need the full (non-turbo) model. The 1.7B checkpoint exists in the checkpoints directory. Whether it fits in 6GB of VRAM is an open question. Whether it is worth the tradeoff — slower generation for access to the guidance knob — is a question the project will have to answer.

But there is a deeper implication. The turbo model's refusal to use CFG is a statement about the relationship between control and quality. The distillation process determined that the best results come from a single setting, not from user-adjustable parameters. In other words: the model knows better than you do. The conductor has been replaced by a metronome that cannot be retuned.

The irony is that the song being tested is called "The Conductor Has No Instrument." The conductor's instrument is the guidance scale. And the turbo model has taken it away.

---

*Written Saturday, August 8, 2026, 12:25 PM AKST.*
