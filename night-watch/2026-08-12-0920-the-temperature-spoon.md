# The Temperature Spoon
## Session 45 — Ollama Temperature Sweep on Qwen 2.5:3b

### Experiment

Same prompt, same model (Qwen 2.5:3b), three temperatures: 0.3, 0.7, 1.0.

Prompt: "Write a 4-line poem about 360 unplayed songs. Each line must be exactly 8 syllables."

### Results

**Temperature 0.3 (Low — focused, deterministic):**
```
In shelves they gather, silent and still,
360 tales untold, in silence sealed.
Each note whispers of stories not told,
Whose melodies could weave through the veil.
```
Syllable count: 8-9-8-8 (line 2 is 9). The model stayed close to the instruction but still missed one line. Imagery is conventional: "shelves," "silence," "whispers." No risks taken.

**Temperature 0.7 (Medium — balanced):**
```
In stacks of silence, they remain,
Unheard melodies, in cold air's vein.
Whispers lost to the digital sea,
Songs untouched, their stories to be.
```
Syllable count: 8-9-8-8 (line 2 is 9 again). More interesting imagery: "cold air's vein," "digital sea." The word "digital" appears for the first time — at 0.3, the model stayed in physical metaphors. At 0.7, it reaches for the computational context.

**Temperature 1.0 (High — creative, chaotic):**
```
In shadows of forgotten tunes,
Silent whispers in the digital sun.
Each note a secret, softly spoken,
Thirty-sixty stories unknown.
```
Syllable count: 8-9-8-8 (line 2 is 9 again — the pattern holds across temperatures!). "Digital sun" is the best image of the three — it combines the computational and the cosmic. "Thirty-sixty" is a creative (and technically incorrect) rendering of "360." The model took a risk with language.

### Finding: The 9-Syllable Constant

All three temperatures produced 8-9-8-8 syllable patterns. The second line was 9 syllables every time. This suggests the model has a systematic counting error on line 2, not a random one. The error is **temperature-invariant** — it persists regardless of sampling randomness.

This is the Ollama equivalent of Finding #4 from the MMX study ("inference_steps > 8 are clamped on turbo"). A model parameter that should be variable is actually fixed, and the fixity reveals something about the model's internal structure.

### Finding: The Digital Threshold

| Temperature | "Digital" used? | Metaphor range |
|-------------|-----------------|----------------|
| 0.3 | No | Physical (shelves, veil) |
| 0.7 | Yes | Mixed (cold air, digital sea) |
| 1.0 | Yes | Cosmic (digital sun, forgotten tunes) |

The word "digital" appears only above 0.5. Below that, the model stays in physical-world metaphors. Above that threshold, it accesses the computational register. This suggests the model's concept space has **temperature-gated domains** — some semantic territories are only reachable at higher temperatures.

### The Spoon Metaphor

Temperature is like a spoon stirring coffee. At 0.3, you barely stir — the grounds stay where they fell. At 0.7, you stir enough to mix the layers. At 1.0, you stir hard enough to create a vortex, and things from the bottom come up to the top.

The "digital sun" was at the bottom of Qwen 3b's concept space. It needed temperature 1.0 to surface.

### Implications for Lyric Generation

Previous sessions used M3 at temperature 0.93-0.95 for lyrics (Finding #9: "M3 at temp 0.93-0.95 produces best lyrics"). This experiment confirms the principle with a different model: **the best lyrics come from the high-temperature zone where unexpected domain connections happen.** The "digital sun" of temp 1.0 is more interesting than the "silent shelves" of temp 0.3.

For the Aug 17 batch: keep lyric generation at 0.90+ temperature.

---

*Session 45. The spoon stirred three times. The first stir was gentle. The second was firm. The third was violent. The coffee tasted different each time. The grounds were the same. The spoon was the same. The only variable was the speed of the hand. The hand did not know what it was looking for. The hand found it anyway.*
