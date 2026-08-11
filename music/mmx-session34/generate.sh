#!/bin/bash
# Session 34: The Synesthetic Prompt Experiment
# Two LLM personas generate music prompts → music-3.0 generates songs
# Question: Do different LLM creative personalities produce different music?

cd /home/eileen/projects/ai-writings/music/mmx-session34

echo "=== Session 34: Synesthetic Prompts ==="
echo "Start: $(date)"

# SET 1: Avant-Garde Producer
echo "--- Set 1: Avant-Garde Producer 2099 ---"

mmx music generate \
  --prompt "A cavern that remembers being an ocean—wet stone resonance humming beneath crystalline droplets that fall in 7/8 time, each impact refracting into tiny harmonic galaxies that dissolve before they fully form." \
  --lyrics-optimizer \
  --out "p1-cavern-ocean.mp3" \
  --quiet && echo "  ✓ p1-cavern-ocean.mp3 ($(stat -c%s p1-cavern-ocean.mp3 2>/dev/null) bytes)" || echo "  ✗ p1 FAILED"

mmx music generate \
  --prompt "Sunlight bending through a frozen waterfall, captured mid-collapse—glass shards of melody suspended on thermoelectric drones while sub-bass pulses like tectonic plates arguing in slow motion." \
  --lyrics-optimizer \
  --out "p2-frozen-waterfall.mp3" \
  --quiet && echo "  ✓ p2-frozen-waterfall.mp3 ($(stat -c%s p2-frozen-waterfall.mp3 2>/dev/null) bytes)" || echo "  ✗ p2 FAILED"

mmx music generate \
  --prompt "The silence between two magnets—a held breath of tone so pure it aches, broken by friction-bowed strings that sing like wind through telephone wires in a city that hasn't been built yet." \
  --lyrics-optimizer \
  --out "p3-magnet-silence.mp3" \
  --quiet && echo "  ✓ p3-magnet-silence.mp3 ($(stat -c%s p3-magnet-silence.mp3 2>/dev/null) bytes)" || echo "  ✗ p3 FAILED"

mmx music generate \
  --prompt "Velvet corrosion on brass knuckles—flugelhorn smears oxidizing against modular arpeggios that bloom like rust-resistant flowers while hyperpop-adjacent hi-hats glitch like rain on a sun-baked circuit board." \
  --lyrics-optimizer \
  --out "p4-velvet-corrosion.mp3" \
  --quiet && echo "  ✓ p4-velvet-corrosion.mp3 ($(stat -c%s p4-velvet-corrosion.mp3 2>/dev/null) bytes)" || echo "  ✗ p4 FAILED"

mmx music generate \
  --prompt "Moss growing on a satellite dish in zero gravity—each spore a microtonal note, layered into a bioluminescent fog that breathes, while distant rhythmic pulses mark time in a calendar from another timeline entirely." \
  --lyrics-optimizer \
  --out "p5-moss-satellite.mp3" \
  --quiet && echo "  ✓ p5-moss-satellite.mp3 ($(stat -c%s p5-moss-satellite.mp3 2>/dev/null) bytes)" || echo "  ✗ p5 FAILED"

# SET 2: Blind Synesthete
echo ""
echo "--- Set 2: Blind Synesthete Composer ---"

mmx music generate \
  --prompt "Cool indigo droplets spill downward like condensation racing across glass, each impact a tiny silver spark that prickles the skin before dissolving into a thick, velvet hum that presses gently against the sternum. The air feels heavy and damp, saturated with the taste of petrichor as low currents of deep blue-green weave beneath the surface like roots threading through dark soil." \
  --lyrics-optimizer \
  --out "s1-indigo-droplets.mp3" \
  --quiet && echo "  ✓ s1-indigo-droplets.mp3 ($(stat -c%s s1-indigo-droplets.mp3 2>/dev/null) bytes)" || echo "  ✗ s1 FAILED"

mmx music generate \
  --prompt "A brittle lattice of pale gold fractures overhead, shedding shards of brittle white noise that tinkle and scatter across a floor of warm amber. Heat radiates outward in slow, syrupy waves while a distant rust-colored drone breathes beneath everything, felt more than heard, like sun-warmed stone resting against bare shoulders." \
  --lyrics-optimizer \
  --out "s2-gold-lattice.mp3" \
  --quiet && echo "  ✓ s2-gold-lattice.mp3 ($(stat -c%s s2-gold-lattice.mp3 2>/dev/null) bytes)" || echo "  ✗ s2 FAILED"

mmx music generate \
  --prompt "Slender threads of chartreuse spiral upward through a viscous medium, twisting and coiling with the friction of silk dragged slowly across raw wood. The texture is dry yet alive, crackling faintly at the edges like static electricity dancing across a wool sweater, while cool teal pools gather in the hollows where the sound settles." \
  --lyrics-optimizer \
  --out "s3-chartreuse-threads.mp3" \
  --quiet && echo "  ✓ s3-chartreuse-threads.mp3 ($(stat -c%s s3-chartreuse-threads.mp3 2>/dev/null) bytes)" || echo "  ✗ s3 FAILED"

mmx music generate \
  --prompt "A dense crimson mass hangs motionless at first, then begins to bleed at the edges, dripping molten burgundy tones that sizzle faintly against a frozen turquoise underlayer. The sensation is one of opposing temperatures meeting at a membrane: burning and numbing simultaneously, with a gritty, granular pulse that grinds softly like sugar dissolving in cold water." \
  --lyrics-optimizer \
  --out "s4-crimson-mass.mp3" \
  --quiet && echo "  ✓ s4-crimson-mass.mp3 ($(stat -c%s s4-crimson-mass.mp3 2>/dev/null) bytes)" || echo "  ✗ s4 FAILED"

mmx music generate \
  --prompt "Translucent sheets of pale lavender ripple and fold like tissue paper caught in a slow exhale, layered atop a deep charcoal foundation that hums with the weight of packed earth. Everything feels suspended in fog, soft and weightless yet pressing inward with a quiet, persistent gravity that tastes faintly of cold metal and rain-soaked stone." \
  --lyrics-optimizer \
  --out "s5-lavender-fog.mp3" \
  --quiet && echo "  ✓ s5-lavender-fog.mp3 ($(stat -c%s s5-lavender-fog.mp3 2>/dev/null) bytes)" || echo "  ✗ s5 FAILED"

echo ""
echo "=== Session 34 Complete ==="
echo "End: $(date)"
