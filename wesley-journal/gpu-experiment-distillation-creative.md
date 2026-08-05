# Wesley GPU Experiment: Distillation — Maritime Creative Writing

- **Model:** granite3.1-dense:2b (Wesley)
- **Date:** 2026-08-05 01:20 AKDT
- **Experiment:** Does teaching with a good example improve Wesley's creative writing?

## Protocol
1. **Baseline:** Wesley writes "harbor at dawn" (100 words) without help
2. **Taught:** Wesley writes same prompt after seeing a masterful example with specific nouns

## Results

### Baseline (Wesley solo)
- 175 words, 4 specific nouns
- 299 tokens, 7.5s, 39.7 tok/s
- Style: ethereal, generic, romantic ("ethereal sheen," "intoxicating bouquet," "serene haven")
- Weakness: overuses abstract adjectives ("tranquil," "extraordinary")
- Strength: decent rhythm, paragraph structure

### Taught (Wesley after example)
- 112 words, 2 specific nouns
- 221 tokens, 3.7s, 59.3 tok/s
- Style: more concrete ("diesel fuel," "weather-beaten pier," "polished obsidian")
- Improvement: shorter, more focused, better imagery
- Regression: FEWER specific nouns than baseline — absorbed style but not vocabulary

### Analysis
**The teaching paradox:** The example was full of specific nouns (gill net buoys, sea otter, clam, float plane dock, etc.). Wesley didn't copy them. Instead, Wesley absorbed the *structural pattern* of the example (start with a specific sound, move to smell, then visual, then color on the ridge) but filled it with his own vocabulary. He got the shape right but the content is still his own.

**Specific noun count DROPPED** from 4 to 2. This means the teaching made Wesley *less* concrete on the metric I was measuring, even though the prose is arguably better. The teaching example raised the quality floor (no more "intoxicating bouquet") but didn't raise the specificity ceiling.

**Speed improvement:** Wesley generated faster when taught (59.3 vs 39.7 tok/s). This may be because the shorter output required less computation, or because the teaching prompt constrained the output space (less uncertainty = faster sampling).

### Casting Insight
Teaching creative writing to a 2B model transfers **structure** better than **content**. The student gets the shape of the master's prose but fills it with their own words. For distillation purposes:
- **Good:** Teaching structural patterns (paragraph flow, sensory ordering)
- **Bad:** Trying to transfer specific vocabulary or domain knowledge
- **Surprising:** Speed improvement suggests constrained outputs are computationally cheaper

---

## Baseline Output

Dawn seeps through the sky, it illuminates a harbor like a painter's gentle brushstroke. The water, once dark and still, now shimmers with an ethereal sheen, reflecting the pastel hues of pink and orange that bath the clouds above. This tranquil expanse is home to a diverse marine life, their silhouettes barely discernible against the fading night.

The air carries a subtle symphony - the rhythmic lapping of waves against the pier, punctuated by the distant honking of gulls, their voices growing louder as the sun peeks over the horizon. The scent of salt and sea mingles with the freshness of dew-kissed grass, creating an intoxicating bouquet that heralds a new day.

A soft, cool breeze stirs the sails of idle boats, whispering tales of distant voyages. The harbor's heart beats with anticipation, a prelude to the burgeoning activity that will unfold as the sun ascends, casting its warmth upon this serene haven. It is here, at dawn, where humanity and nature converge, promising an extraordinary day on the water.

## Taught Output

At the cusp of dawn, the once-vibrant harbor whispers in shades of gray and blue-black. The salty breeze carries the faint scent of seaweed, mingling with diesel fuel from the neighboring vessels' engines. A lone heron, silhouetted against the approaching sunrise, perches on a weather-beaten pier. Its long legs stir the water as it hunts, casting ethereal shadows. The first rays of dawn illuminate the horizon, painting it with fiery orange and pink. The boats' reflections shimmer in this pre-dawn tranquility, their hulls glistening like polished obsidian. The air is crisp, carrying the distant hum of seagulls heralding the day's awakening. Here, time slows; nature holds its breath, anticipating the harbor's rebirth.
