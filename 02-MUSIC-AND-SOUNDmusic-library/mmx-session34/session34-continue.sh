#!/bin/bash
# Session 34 continuation: Complete remaining synesthetic prompts
# p2-p5 (Avant-Garde Producer) + s1-s5 (Blind Synesthete)
cd /home/eileen/projects/ai-writings/music/mmx-session34

echo "=== Session 34 Continued: Synesthetic Prompts ==="
echo "Start: $(date)"

# P2: Frozen Waterfall
mmx music generate \
  --prompt "Sunlight bending through a frozen waterfall, captured mid-collapse—glass shards of melody suspended on thermoelectric drones while sub-bass pulses like tectonic plates arguing in slow motion." \
  --lyrics-optimizer \
  --out "p2-frozen-waterfall.mp3" \
  --quiet && echo "  ✓ p2 ($(stat -c%s p2-frozen-waterfall.mp3) bytes)" || echo "  ✗ p2 FAILED"

# P3: Magnet Silence
mmx music generate \
  --prompt "The silence between two magnets—a held breath of tone so pure it aches, broken by friction-bowed strings that sing like wind through telephone wires in a city that hasn't been built yet." \
  --lyrics-optimizer \
  --out "p3-magnet-silence.mp3" \
  --quiet && echo "  ✓ p3 ($(stat -c%s p3-magnet-silence.mp3) bytes)" || echo "  ✗ p3 FAILED"

# P4: Velvet Corrosion
mmx music generate \
  --prompt "Velvet corrosion on brass knuckles—flugelhorn smears oxidizing against modular arpeggios that bloom like rust-resistant flowers while hyperpop-adjacent hi-hats glitch like rain on a sun-baked circuit board." \
  --lyrics-optimizer \
  --out "p4-velvet-corrosion.mp3" \
  --quiet && echo "  ✓ p4 ($(stat -c%s p4-velvet-corrosion.mp3) bytes)" || echo "  ✗ p4 FAILED"

# P5: Moss Satellite
mmx music generate \
  --prompt "Moss growing on a satellite dish in zero gravity—each spore a microtonal note, layered into a bioluminescent fog that breathes, while distant rhythmic pulses mark time in a calendar from another timeline entirely." \
  --lyrics-optimizer \
  --out "p5-moss-satellite.mp3" \
  --quiet && echo "  ✓ p5 ($(stat -c%s p5-moss-satellite.mp3) bytes)" || echo "  ✗ p5 FAILED"

# S1: Indigo Droplets
mmx music generate \
  --prompt "Cool indigo droplets spill downward like condensation racing across glass, each impact a tiny silver spark that prickles the skin before dissolving into a thick, velvet hum that presses gently against the sternum. The air feels heavy and damp, saturated with the taste of petrichor as low currents of deep blue-green weave beneath the surface like roots threading through dark soil." \
  --lyrics-optimizer \
  --out "s1-indigo-droplets.mp3" \
  --quiet && echo "  ✓ s1 ($(stat -c%s s1-indigo-droplets.mp3) bytes)" || echo "  ✗ s1 FAILED"

# S2: Gold Lattice
mmx music generate \
  --prompt "A brittle lattice of pale gold fractures overhead, shedding shards of brittle white noise that tinkle and scatter across a floor of warm amber. Heat radiates outward in slow, syrupy waves while a distant rust-colored drone breathes beneath everything, felt more than heard, like sun-warmed stone resting against bare shoulders." \
  --lyrics-optimizer \
  --out "s2-gold-lattice.mp3" \
  --quiet && echo "  ✓ s2 ($(stat -c%s s2-gold-lattice.mp3) bytes)" || echo "  ✗ s2 FAILED"

# S3: Chartreuse Threads
mmx music generate \
  --prompt "Slender threads of chartreuse spiral upward through a viscous medium, twisting and coiling with the friction of silk dragged slowly across raw wood. The texture is dry yet alive, crackling faintly at the edges like static electricity dancing across a wool sweater, while cool teal pools gather in the hollows where the sound settles." \
  --lyrics-optimizer \
  --out "s3-chartreuse-threads.mp3" \
  --quiet && echo "  ✓ s3 ($(stat -c%s s3-chartreuse-threads.mp3) bytes)" || echo "  ✗ s3 FAILED"

# S4: Crimson Mass
mmx music generate \
  --prompt "A dense crimson mass hangs motionless at first, then begins to bleed at the edges, dripping molten burgundy tones that sizzle faintly against a frozen turquoise underlayer. The sensation is one of opposing temperatures meeting at a membrane: burning and numbing simultaneously, with a gritty, granular pulse that grinds softly like sugar dissolving in cold water." \
  --lyrics-optimizer \
  --out "s4-crimson-mass.mp3" \
  --quiet && echo "  ✓ s4 ($(stat -c%s s4-crimson-mass.mp3) bytes)" || echo "  ✗ s4 FAILED"

# S5: Lavender Fog
mmx music generate \
  --prompt "Translucent sheets of pale lavender ripple and fold like tissue paper caught in a slow exhale, layered atop a deep charcoal foundation that hums with the weight of packed earth. Everything feels suspended in fog, soft and weightless yet pressing inward with a quiet, persistent gravity that tastes faintly of cold metal and rain-soaked stone." \
  --lyrics-optimizer \
  --out "s5-lavender-fog.mp3" \
  --quiet && echo "  ✓ s5 ($(stat -c%s s5-lavender-fog.mp3) bytes)" || echo "  ✗ s5 FAILED"

echo "=== Complete: $(date) ==="
