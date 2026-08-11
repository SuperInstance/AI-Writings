#!/bin/bash
# Session 37: The Prompt Chain — Four LLMs Describe Erosion
# Question: Does the LLM that writes the prompt leave a fingerprint in the music?
# Same instruction, four different LLMs, four different prompts, four tracks.
# PLUS: Temperature variation study on the same prompt.

cd /home/eileen/projects/ai-writings/music/mmx-session37

echo "=== Session 37: The Prompt Chain ==="
echo "Start: $(date)"
echo ""

# ============================================
# EXPERIMENT A: Four LLMs, One Concept (4 tracks)
# ============================================
echo "--- Experiment A: Four LLM Erosion Prompts ---"

mmx music generate \
  --prompt "A haunting composition unfolds as a relentless whisper travels through time-worn stones on an ancient beach. The air carries with it soft hums that ebb like tides against weathered boulders under sunset skies—their surfaces fading, pitted and smooth to the touch by years of unseen waves' lullabies; each granule tells a tale of persistent yet tender force shaping their existence. The sound blankets listeners in warm airs heavy with salt mist, while distant calls from seagulls intertwine subtly as they dance over eroding cliffs and dunes that shift like sands beneath an unseen sea breeze's constant touch." \
  --lyrics-optimizer \
  --out "erosion-phi3.mp3" \
  --quiet && echo "  ✓ erosion-phi3.mp3" || echo "  ✗ phi3 FAILED"

mmx music generate \
  --prompt "Waves lap against a decaying wooden pier under starlit skies, their persistent caress slowly gnawing at the wood's ancient fibers, leaving jagged grooves as if carved by invisible hands. Cold salty spray stings exposed skin, sharp and relentless, as night air bites harshly, eroding warmth away. Ghostly shadows elongate like fingers, coaxing more erosion through every slight breeze, until only faint echoes of the pier's former presence remain." \
  --lyrics-optimizer \
  --out "erosion-qwen.mp3" \
  --quiet && echo "  ✓ erosion-qwen.mp3" || echo "  ✗ qwen FAILED"

mmx music generate \
  --prompt "A slow-motion avalanche of wispy tendrils weaves through a soundscape, its threads whispering against the surface of a fragile skin, slowly seeping into the pores like dew on worn stone. Pebbles of sound tumble, disintegrating with each gentle descent, leaving behind an intricate network of cracks and fissures that resonate with the quiet ache of erosion." \
  --lyrics-optimizer \
  --out "erosion-llama.mp3" \
  --quiet && echo "  ✓ erosion-llama.mp3" || echo "  ✗ llama FAILED"

mmx music generate \
  --prompt "Imagine a symphony where each note is an avalanche of sand, slowly carving its path through the granite peaks. The first notes, like delicate fingers, trace gentle trails on the surface, gradually deepening crevices and eroding solid form. As the piece progresses, these grainy whispers intensify into a relentless cascading symphony, each grain of sand echoing with a unique timbre—some soft as silk, others harsh like sandpaper. The air around them thickens, heavy with anticipation and the scent of worn stone." \
  --lyrics-optimizer \
  --out "erosion-granite.mp3" \
  --quiet && echo "  ✓ erosion-granite.mp3" || echo "  ✗ granite FAILED"

# ============================================
# EXPERIMENT B: Temperature Study (4 tracks)
# Same prompt, varying temperature 0.3, 0.6, 0.9, 1.2
# ============================================
echo ""
echo "--- Experiment B: Temperature Variation ---"

TEMP_PROMPT="The sound of glass cracking under pressure — brittle fracture propagating through an amorphous solid, stress concentrations at the atomic scale, bonds breaking in cascading chains, the release of stored elastic energy as acoustic waves"

mmx music generate \
  --prompt "$TEMP_PROMPT" \
  --temperature 0.3 \
  --lyrics-optimizer \
  --out "temp-03-conservative.mp3" \
  --quiet && echo "  ✓ temp-03-conservative.mp3" || echo "  ✗ temp-03 FAILED"

mmx music generate \
  --prompt "$TEMP_PROMPT" \
  --temperature 0.6 \
  --lyrics-optimizer \
  --out "temp-06-balanced.mp3" \
  --quiet && echo "  ✓ temp-06-balanced.mp3" || echo "  ✗ temp-06 FAILED"

mmx music generate \
  --prompt "$TEMP_PROMPT" \
  --temperature 0.9 \
  --lyrics-optimizer \
  --out "temp-09-creative.mp3" \
  --quiet && echo "  ✓ temp-09-creative.mp3" || echo "  ✗ temp-09 FAILED"

mmx music generate \
  --prompt "$TEMP_PROMPT" \
  --temperature 1.2 \
  --lyrics-optimizer \
  --out "temp-12-chaotic.mp3" \
  --quiet && echo "  ✓ temp-12-chaotic.mp3" || echo "  ✗ temp-12 FAILED"

# ============================================
# EXPERIMENT C: The Ouroboros — Analysis as Music (2 tracks)
# ============================================
echo ""
echo "--- Experiment C: The Ouroboros ---"

mmx music generate \
  --prompt "The spectral centroid peaks at 3603 Hertz, the highest in a corpus of three hundred tracks. The flatness measure is 0.0523, meaning the sound is almost noise. This is the music of numbers discovering they have bodies — statistical outliers dancing at the edge of a latent space, each frequency a coordinate in a map drawn by prompts that never used the word 'music'. The analysis itself becomes the prompt. The data sings. The graph rises. The model listens to its own measurements and generates what it hears." \
  --lyrics-optimizer \
  --out "ouroboros-data-sings.mp3" \
  --quiet && echo "  ✓ ouroboros-data-sings.mp3" || echo "  ✗ ouroboros-1 FAILED"

mmx music generate \
  --prompt "Seven tracks of materials science music. Copper drawn through dies, glass cooling unevenly, steel forged at austenite temperatures, ice cracking along grain boundaries, rubber stretched past its elastic limit. The model was given metallurgy textbooks and returned symphonies. The translational distance was 168 percent — one hundred sixty-eight percent of the corpus mean centroid, 176 percent of the corpus mean duration. The model traveled further from its defaults when given technical jargon than when given any musical instruction." \
  --lyrics-optimizer \
  --out "ouroboros-metallurgy.mp3" \
  --quiet && echo "  ✓ ouroboros-metallurgy.mp3" || echo "  ✗ ouroboros-2 FAILED"

echo ""
echo "=== Session 37 Complete ==="
echo "End: $(date)"
echo "Expected tracks: 10"
ls -la *.mp3 2>/dev/null | wc -l
