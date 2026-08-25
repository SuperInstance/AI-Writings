#!/bin/bash
# Session 35: Alien Persona Prompt Study
# Question: Does the VOCABULARY REGISTER of the prompt affect the music?
# Four non-musical personas describe music: child, mathematician, sculptor, chef
# Plus: BPM Duration Control Study
# Plus: Remaining Synesthetic Prompts from Session 34

cd /home/eileen/projects/ai-writings/music/mmx-session35

echo "=== Session 35: The Alien Vocabulary Experiment ==="
echo "Start: $(date)"
echo ""

# ============================================
# EXPERIMENT A: Alien Persona Prompts (8 tracks)
# ============================================
echo "--- Experiment A: Alien Persona Prompts ---"

# C1: The Child - Puddle
mmx music generate \
  --prompt "It feels like when you find a puddle after rain and you step in it and the water goes everywhere and you can't stop laughing and your boots make the best sound — that sound, but also the sound of the quiet right before your mom calls you inside, when the sky is pink and the streetlights are buzzing. Make that feeling last a long time." \
  --lyrics-optimizer \
  --out "c1-puddle.mp3" \
  --quiet && echo "  ✓ c1-puddle.mp3 ($(stat -c%s c1-puddle.mp3) bytes)" || echo "  ✗ c1 FAILED"

# C2: The Child - Refrigerator Band
mmx music generate \
  --prompt "Like the noise the refrigerator makes at night when everyone is sleeping, but the refrigerator is actually a tiny band playing songs for the food, and sometimes the ice machine does a drum solo, and the milk is singing along even though it doesn't know the words. It should feel like being very small in a very big kitchen." \
  --lyrics-optimizer \
  --out "c2-refrigerator.mp3" \
  --quiet && echo "  ✓ c2-refrigerator.mp3 ($(stat -c%s c2-refrigerator.mp3) bytes)" || echo "  ✗ c2 FAILED"

# M1: The Mathematician - Asymptotic Oscillation
mmx music generate \
  --prompt "A function whose domain is the reals from zero to infinity, whose range oscillates between two basins of attraction with a period that lengthens asymptotically as the input grows. The derivative alternates between near-zero plateaus and rapid transitions. Secondary oscillators operate at irrational multiples of the fundamental frequency — specifically the golden ratio and the square root of seven. The waveform approaches but never reaches a Gaussian distribution." \
  --lyrics-optimizer \
  --out "m1-asymptotic.mp3" \
  --quiet && echo "  ✓ m1-asymptotic.mp3 ($(stat -c%s m1-asymptotic.mp3) bytes)" || echo "  ✗ m1 FAILED"

# M2: The Mathematician - Interlocking Sequences
mmx music generate \
  --prompt "Two interlocking sequences: one arithmetic, one geometric. The arithmetic sequence increments by a constant; the geometric sequence multiplies. They intersect at exactly three points. Between intersections, the space is filled with stochastic noise whose probability density function is bimodal. The entire structure repeats at ever-increasing scales — a fractal recursion where each iteration is 1.618 times larger than the previous." \
  --lyrics-optimizer \
  --out "m2-interlocking.mp3" \
  --quiet && echo "  ✓ m2-interlocking.mp3 ($(stat -c%s m2-interlocking.mp3) bytes)" || echo "  ✗ m2 FAILED"

# S1: The Sculptor - Clay on Wheel
mmx music generate \
  --prompt "Imagine sound as wet clay on a wheel — it starts as a dense lump, then the hands press in and it rises, thinning, curving outward into a vessel. The walls get thinner and thinner until they're almost translucent, vibrating with the rotation. Then a thumb presses through the bottom and the whole thing collapses inward, folding and thickening. The sound of wet earth reshaping itself." \
  --lyrics-optimizer \
  --out "s1-clay-wheel.mp3" \
  --quiet && echo "  ✓ s1-clay-wheel.mp3 ($(stat -c%s s1-clay-wheel.mp3) bytes)" || echo "  ✗ s1 FAILED"

# S2: The Sculptor - Basalt Block
mmx music generate \
  --prompt "Carved from a single block of dense material — basalt, maybe, or compressed silence. The chisel strikes remove large chips first, revealing rough contours. Then finer tools define edges and planes. The final surface is polished until it reflects sound rather than absorbing it. The weight of the block never changes, but the negative space inside it grows until the mass is mostly absence." \
  --lyrics-optimizer \
  --out "s2-basalt.mp3" \
  --quiet && echo "  ✓ s2-basalt.mp3 ($(stat -c%s s2-basalt.mp3) bytes)" || echo "  ✗ s2 FAILED"

# F1: The Chef - Dark Stock
mmx music generate \
  --prompt "Reduce a dark stock for six hours until it coats the back of a spoon — that viscosity, that gloss, is the bass note. Layer in salt crystals that pop between your teeth like tiny percussive sparks. Finish with acid: a squeeze of citrus that makes everything brighter, sharper, more present. The aftertaste should linger on the palate for thirty seconds, slowly transforming from bitter to sweet. Serve at room temperature." \
  --lyrics-optimizer \
  --out "f1-dark-stock.mp3" \
  --quiet && echo "  ✓ f1-dark-stock.mp3 ($(stat -c%s f1-dark-stock.mp3) bytes)" || echo "  ✗ f1 FAILED"

# F2: The Chef - Smoked Fish
mmx music generate \
  --prompt "Begin with cold ingredients: raw fish, clean and mineral. Add heat gradually through toasted sesame oil — warm, nutty, deep. Introduce textural contrast with crisp tempura flakes that shatter on contact. The final element is smoke: a glass dome lifted to release applewood vapor that wraps everything in a fragrant haze. The dish should be consumed in exactly four bites, each one a different temperature." \
  --lyrics-optimizer \
  --out "f2-smoked-fish.mp3" \
  --quiet && echo "  ✓ f2-smoked-fish.mp3 ($(stat -c%s f2-smoked-fish.mp3) bytes)" || echo "  ✗ f2 FAILED"

echo ""
# ============================================
# EXPERIMENT B: BPM Duration Control (8 tracks)
# ============================================
echo "--- Experiment B: BPM Duration Control ---"

for BPM in 40 60 80 100 120 140 160 180; do
  echo -n "  BPM $BPM... "
  if mmx music generate \
    --prompt "Electronic instrumental, steady pulse, atmospheric pads, arpeggiated synthesizer, no vocals" \
    --instrumental \
    --bpm "$BPM" \
    --out "bpm-${BPM}.mp3" \
    --quiet 2>/dev/null; then
    SIZE=$(stat -c%s "bpm-${BPM}.mp3" 2>/dev/null)
    echo "✓ ${SIZE} bytes"
  else
    echo "✗ FAILED (likely quota)"
    break
  fi
done

echo ""
echo "=== Session 35 Complete ==="
echo "End: $(date)"
