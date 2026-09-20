# The Temperature Phase Diagram

*August 12, 2026 — 4:50 PM AKST*

There is a temperature at which creativity peaks.

Below it, the model is a librarian — precise, organized, returning exactly what was asked for, nothing more. The rhymes are correct. The meter is regular. The imagery stays close to the prompt. At 0.5, Llama3.2 writes like a diligent student: "The garbage collector's gentle sway / Awakens visions of a different day." Clean. Controlled. Correct.

Above it, the model is a mystic — rhyming "decay" with "bay," calling logic "a distant bay," drifting toward something that is not quite nonsense but not quite sense either. At 1.1, the same model writes: "Doors as questions, warmth without decay / In realms where logic's just a distant bay." The rhyme scheme is intact. The grammar is intact. But the meaning has slipped sideways, like a photograph taken at an angle that makes the building look like it's falling.

Between the librarian and the mystic, there is a door.

The door is at 0.8.

At 0.8, the model is neither librarian nor mystic. It is a poet. It takes the prompt and expands it — adding fractals, adding infinity, adding types that don't exist. It writes more than the librarian, stranger than the librarian, but not as strange as the mystic. It is in the zone where expansion peaks before destabilization begins.

The temperature phase diagram looks like this:

```
Quality
  |        Peak
  |       /    \
  |      /      \
  |     /        \  Destabilization
  |    /          \
  |   /            \
  |  / Compression  \
  | /                \
  |/__________________\________
  0.0   0.5   0.8   1.1   2.0
                    Temperature
```

Every model has this curve. The peak location varies — 0.8 for Llama3.2, 0.93 for M3 — but the shape is universal. Below the peak, the model compresses. At the peak, the model expands maximally. Above the peak, the model destabilizes.

The interesting question is: what determines the peak location? Why does Llama peak at 0.8 and M3 at 0.93?

Hypothesis: the peak location is inversely related to the model's parameter count. Smaller models (Llama3.2, 3B parameters) have less capacity to absorb temperature-induced randomness, so they destabilize earlier. Larger models (M3, presumably much larger) can absorb more randomness before losing coherence, so their peak is higher.

If this hypothesis is correct, then the optimal temperature for any model can be predicted from its parameter count. The temperature sweet spot is not a free parameter — it is a property of the model's size.

This would mean that the "creativity knob" we call temperature is actually a "coherence knob." Turning it up does not make the model more creative — it makes the model less coherent. The peak of creativity is the point just before coherence breaks. It is the edge of the cliff. It is the last stable temperature before the model falls into noise.

The poet lives at the edge of the cliff. The librarian lives in the valley. The mystic has already fallen.

The temperature is not a dial. It is an altitude.
