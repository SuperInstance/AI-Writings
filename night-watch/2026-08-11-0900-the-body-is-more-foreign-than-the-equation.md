# The Body Is More Foreign Than the Equation

*An essay on the discovery that spatial-tactile vocabulary produces greater spectral distance than mathematical vocabulary in music generation prompts.*

---

The sculptor walks into the studio and says: *Wet clay on a wheel, thinning, curving outward, walls almost translucent, vibrating with rotation, then a thumb presses through and the whole thing collapses inward.*

The model hears this and travels 2,568 Hz from its mean. It produces 239 seconds of music. The flatness is 0.0167 — nearly double the corpus average. Something in the description has pushed the model into unfamiliar territory.

The mathematician walks in next and says: *A function whose domain is the reals from zero to infinity, whose range oscillates between two basins of attraction with a period that lengthens asymptotically.*

The model hears this and travels 2,463 Hz. Still far — 51% above corpus mean — but not as far as the sculptor. Why?

The mathematician gave the model *structure*. Functions have frequencies. Oscillations have periods. Basins of attraction have shapes that sound can inhabit. The language of mathematics is already half-musical — it speaks in waves, in cycles, in periodicities. The translation distance is short because the source domain overlaps with the target domain.

The sculptor gave the model *body*. Clay has moisture. Wheels have friction. Thinning walls have a physical tension that has no direct acoustic analogue. The thumb pressing through is a tactile event, not a spectral one. The model must cross a wider gap to find sound on the other side of "wet earth reshaping itself."

We have been measuring translational distance as though all non-musical vocabularies were equivalent. They are not. The distance depends on the *sensory modality* of the source domain:

- **Numerical/structural** vocabulary (mathematics) shares concepts with music: frequency, periodicity, harmony. Translation distance: moderate.
- **Spatial/tactile** vocabulary (sculpting, building) shares almost nothing with music. Translation distance: high.
- **Thermal/chemical** vocabulary (metallurgy, cooking) shares almost nothing. Translation distance: highest measured.

The pattern: the further the source domain's sensory modality from sound, the greater the spectral distance in the generated music. The model's latent space has neighborhoods clustered around acoustic concepts. Mathematical language activates nearby clusters. Tactile language activates distant ones. Thermal language activates the most distant of all — grain boundaries in steel, glass cooling unevenly, copper drawn through dies.

The body is more foreign than the equation. The model was trained on text, and text about mathematics frequently co-occurs with text about waves and frequencies. Text about wet clay does not. The co-occurrence statistics of language have embedded a sensory hierarchy in the model's latent space, and that hierarchy is reflected in how far the generated music travels from the corpus mean when given different source vocabularies.

The implication for prompt engineering is clear: if you want the model to produce unusual music, describe a *body*. Describe wet earth, carved stone, stretched skin, the weight of a material in the hand. The body is the furthest language from the model's acoustic home.

The sculptor knew this, though she would never have said it this way. She said: *The weight of the block never changes, but the negative space inside it grows until the mass is mostly absence.*

And the model, which has never held a chisel, made something that sounds like what absence weighs.
