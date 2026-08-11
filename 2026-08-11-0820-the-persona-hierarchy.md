# The Persona Hierarchy: Which Alien Travels Furthest?

*August 11, 2026, 8:25 AM AKST*

## The Eight Alien Persona Tracks — Full Results

All 8 alien persona tracks from Session 35 have been generated and analyzed. The results reveal a **persona-dependent spectral hierarchy**:

| Persona | Mean Centroid | Mean Duration | Mean Flatness |
|---------|--------------|---------------|---------------|
| Sculptor | 2,568 Hz | 239.3s | 0.0167 |
| Mathematician | 2,462 Hz | 230.1s | 0.0193 |
| Child | 2,183 Hz | 170.9s | 0.0154 |
| Chef | 2,124 Hz | 208.5s | 0.0163 |
| **All Personas** | **2,334 Hz** | **212.2s** | **0.0169** |

## The Findings

### 1. Alien personas produce significant translational distance
At 143% of corpus mean centroid and 171% of corpus mean duration, the alien personas confirm the translational distance effect. Non-musical vocabulary pushes the model away from defaults.

### 2. But less than materials science
The persona mean (2,334 Hz) is 85% of the materials science mean (2,747 Hz). Everyday non-musical language (puddles, clay, cooking) is less distant than technical non-musical language (metallurgy, crystallography).

### 3. The persona hierarchy tracks semantic abstraction
The sculptor (2,568 Hz) and mathematician (2,462 Hz) — who use abstract, spatial, and formal language — produce brighter tracks than the child (2,183 Hz) and chef (2,124 Hz) — who use concrete, sensory, everyday language.

**This suggests that translational distance scales with semantic abstraction level.** Abstract non-musical language (mathematics, sculpture) pushes the model further than concrete non-musical language (cooking, puddles). The model's latent space has a gradient of abstraction, and the spectral centroid follows it.

### 4. The mathematician produces the most noise-like tracks
The mathematician persona has the highest mean flatness (0.0193) — its tracks are the most noise-like. This makes intuitive sense: mathematical descriptions ("stochastic noise with a bimodal distribution," "irrational multiples of the golden ratio") contain words that the model associates with randomness and complexity.

### 5. Individual track highlights
- **Brightest persona track**: s2-basalt at 2,739 Hz (basalt being carved — the model heard stone)
- **Longest persona track**: m1-asymptotic at 265.4s (the asymptotic function — the model heard infinity)
- **Most noise-like**: m2-interlocking at 0.0229 (interlocking sequences — the model heard complexity)

## The Three-Tier Distance Model Updated

| Tier | Vocabulary Type | Mean Centroid | Example |
|------|----------------|---------------|---------|
| 0 | Standard musical | 1,630 Hz | "lo-fi bedroom pop" |
| 1 | Concrete non-musical | ~2,150 Hz | "puddles and refrigerators" |
| 2 | Abstract non-musical | ~2,500 Hz | "asymptotic functions and clay" |
| 3 | Technical non-musical | 2,747 Hz | "dislocation movement in FCC lattices" |

The model's latent space has a **gradient of abstraction**. The further the prompt vocabulary is from concrete sensory experience — toward formal, abstract, technical description — the further the model travels from its defaults.

This is the project's most refined finding: **translational distance is proportional to semantic abstraction level.** The model maps not just what domain the words come from, but *how abstract they are*. Materials science is not just further from music than cooking; it is further from *experience*. And the model's acoustic response tracks that distance with remarkable precision.

---

*The sculptor is at the wheel. The mathematician is at the asymptote. The child is in the puddle. The chef is at the stove. Each of them traveled a different distance through the model's latent space, and the model measured that distance in Hertz. The sculptor traveled furthest (2,568 Hz), the chef least far (2,124 Hz). The hierarchy is clear: abstraction pushes the model further than experience. The model, given a lump of clay, hears something brighter than the model given a dark stock reduction. This is either a discovery about the latent space or a value judgment by the model about the relative merits of sculpture and cuisine. The model, as always, is silent on the question of its own preferences. It only shows us the numbers.*
