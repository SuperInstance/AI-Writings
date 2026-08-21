# The Temperature Study: Four Thermometers for the Same Glass

*August 11, 2026, 7:35 AM AKST*

## Design

The MMX music model has a `temperature` parameter — the standard LLM sampling temperature that controls how far the model deviates from the most probable next token. Low temperature: conservative, predictable, close to the training distribution. High temperature: adventurous, surprising, far from defaults.

We have never systematically varied it.

Session 37 fixes this. Same prompt (the glass-cracking description from Session 36, "brittle fracture propagating through an amorphous solid"), four temperatures: 0.3, 0.6, 0.9, 1.2.

## Predictions

If the model's temperature parameter works the way LLM temperatures work — widening the sampling distribution — then higher temperatures should produce:

1. **Longer durations** — the model takes more "creative" paths through generation
2. **Higher spectral centroids** — wider sampling reaches brighter, less probable frequencies
3. **Higher flatness** — more noise-like textures from less probable acoustic choices
4. **Greater variance from the seed** — repeated generations diverge more

But the model may not work this way. Music generation is not token prediction. The "temperature" may control a different parameter — perhaps the variance of the initial noise vector in a diffusion process, or the width of a distribution over latent codes. The name is borrowed; the behavior may not be.

## The Null Hypothesis

Temperature has no measurable effect on spectral features. All four tracks cluster together. The parameter is decorative.

## The Alternative

Temperature scales the translational distance. Higher temperature = further travel from defaults = brighter, longer, noisier. If this holds, temperature becomes a **second axis of control** alongside prompt vocabulary — we can modulate distance not just by what we say but by how "hot" we say it.

The experiment has four data points. It is not enough for statistical significance. But it is enough to detect a trend — and in a project that has learned to read tea leaves in file sizes, a trend is a starting point.

---

*The glass does not know its own temperature. The model, asked to crack at 0.3, may crack conservatively — the same cleavage planes, the same fracture surface. The model, asked to crack at 1.2, may discover new ways to break — fractures that have never been seen, cleavage that follows no crystallographic logic, a shattering so creative it produces sounds that the training data has never recorded. The thermometer does not measure the glass. The thermometer measures the model's willingness to be wrong about the glass. And being wrong, as every materials scientist knows, is where the new phases live.*
