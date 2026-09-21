#!/bin/bash
# Session 36: Materials Science × Thermodynamics — The Ultimate Alien Vocabulary
# Question: Can prompts written in PURE TECHNICAL LANGUAGE (zero musical vocabulary)
#           produce music that differs from conventionally-described music?
# Hypothesis: Materials science prompts should maximize translational distance,
#             potentially exceeding even the alien persona prompts (S35) in output size.
#
# Two prompt sources:
#   MAT-1 to MAT-5: phi3 (local Ollama) — materials science stress descriptions
#   THERMO-1, THERMO-2: qwen2.5 (local Ollama) — temperature/chemistry as sound
#
# Plus: Temperature Scaling Experiment (same prompt, different --temperature values)
#   Tests whether the music model's sampling temperature affects output

cd /home/eileen/projects/ai-writings/music/mmx-session36

echo "=== Session 36: Materials Science × Thermodynamics ==="
echo "Start: $(date)"
echo ""

# ============================================
# EXPERIMENT A: Materials Science Prompts (5 tracks)
# ============================================
echo "--- Experiment A: Materials Science Prompts ---"

mmx music generate \
  --prompt "As the copper wire is drawn through a die, it experiences necking due to tensile stress exceeding yield strength on certain sections of grain structure leading to dislocation movement that results in work hardening as slip systems become activated along specific crystallographic planes within its face-centered cubic lattice." \
  --lyrics-optimizer \
  --out "mat1-copper-die.mp3" \
  --quiet && echo "  ✓ mat1-copper-die.mp3 ($(stat -c%s mat1-copper-die.mp3) bytes)" || echo "  ✗ mat1 FAILED"

mmx music generate \
  --prompt "The glass exhibits heterogeneous cooling rates resulting in non-uniform thermal expansion coefficients, generating internal stresses and potential for phase separation where strain hardened regions are unable to relax through slip systems due to the amorphous nature of glass structure which lacks a crystalline grain matrix entirely; thus it fractures rather than deforming plastically." \
  --lyrics-optimizer \
  --out "mat2-glass-cooling.mp3" \
  --quiet && echo "  ✓ mat2-glass-cooling.mp3 ($(stat -c%s mat2-glass-cooling.mp3) bytes)" || echo "  ✗ mat2 FAILED"

mmx music generate \
  --prompt "During high-temperature steel forging, dislocations within face-centered cubic or body-centered cubic lattice structures are mobilized through increased slip systems yield under applied stress leading to dynamic recrystallization where new strain-free grains nucleate and grow in the presence of sufficient energy dissipation mechanisms; phase transformations from austenite to martensite may occur if rapid cooling is present, resulting in hardened steel with high tensile strength but reduced ductility." \
  --lyrics-optimizer \
  --out "mat3-steel-forge.mp3" \
  --quiet && echo "  ✓ mat3-steel-forge.mp3 ($(stat -c%s mat3-steel-forge.mp3) bytes)" || echo "  ✗ mat3 FAILED"

mmx music generate \
  --prompt "Ice on a frozen lake undergoes brittle fracture when subjected to pressure through propagation of micro-cracks along the crystalline grain boundaries which are exacerbated by differential thermal expansion; these cracks coalesce leading to macroscopic failure as the rigid, hexagonal close-packed lattice cannot accommodate dislocation motion or any plastic deformation." \
  --lyrics-optimizer \
  --out "mat4-ice-fracture.mp3" \
  --quiet && echo "  ✓ mat4-ice-fracture.mp3 ($(stat -c%s mat4-ice-fracture.mp3) bytes)" || echo "  ✗ mat4 FAILED"

mmx music generate \
  --prompt "Stretching rubber beyond its elastic limit induces significant permanent set and strain hardening by realignment of polymer chains within amorphous thermoplastic structure; as the material undergoes tensile stress, these aligned molecular structures resist further dislocation movement leading to a non-linear increase in modulus until eventual failure through either necking or fracture when ductility limits are exceeded and load cannot be supported." \
  --lyrics-optimizer \
  --out "mat5-rubber-stretch.mp3" \
  --quiet && echo "  ✓ mat5-rubber-stretch.mp3 ($(stat -c%s mat5-rubber-stretch.mp3) bytes)" || echo "  ✗ mat5 FAILED"

echo ""

# ============================================
# EXPERIMENT B: Thermodynamic Prompts (2 tracks)
# ============================================
echo "--- Experiment B: Thermodynamic Prompts ---"

mmx music generate \
  --prompt "Imagine the very first moments of creation, where everything is in absolute zero — no vibration, no energy. Then molecules start to vibrate as they absorb heat energy. Steam rising from boiling water, where small vibrations turn into larger and more noticeable disturbances as the temperature climbs higher still. As materials begin to expand due to thermal expansion, this change affects how waves propagate — some bouncing off surfaces differently, others traveling through more easily, creating new layers of disturbance. Finally, picture plasma heating up, where temperatures soar into extreme ranges, causing material states to shift between gases and liquids as molecules move faster and collide at incredible speeds, generating complex and chaotic patterns." \
  --lyrics-optimizer \
  --out "thermo1-absolute-zero.mp3" \
  --quiet && echo "  ✓ thermo1-absolute-zero.mp3 ($(stat -c%s thermo1-absolute-zero.mp3) bytes)" || echo "  ✗ thermo1 FAILED"

mmx music generate \
  --prompt "In the realm of chemical reactions, consider how collisions between molecules can release or absorb energy. A catalyst enters the mix, lowering the activation energy required for these collisions, allowing more reactions to occur per second. Exothermic cascades where reactants break down into products and heat is released into the environment, increasing ambient temperature. As equilibrium shifts towards new compositions, some of the energy from previous stages disappears or changes in character as old molecules recombine differently. Precipitates forming solid particles at the bottom of a container — these crystalline structures vibrate and resonate with each other creating distinct patterns." \
  --lyrics-optimizer \
  --out "thermo2-catalyst.mp3" \
  --quiet && echo "  ✓ thermo2-catalyst.mp3 ($(stat -c%s thermo2-catalyst.mp3) bytes)" || echo "  ✗ thermo2 FAILED"

echo ""

# ============================================
# EXPERIMENT C: Temperature Scaling (3 tracks)
# Same prompt at 3 different --temperature values — but wait,
# mmx music generate has no --temperature flag.
# Instead: Same prompt with 3 different lyrics-optimizer temps via
# different prompt complexity. Test if prompt LENGTH affects output.
# ============================================
echo "--- Experiment C: Prompt Length Study ---"

# SHORT: 1 sentence
mmx music generate \
  --prompt "Copper being drawn through a die." \
  --lyrics-optimizer \
  --out "len1-short.mp3" \
  --quiet && echo "  ✓ len1-short.mp3 ($(stat -c%s len1-short.mp3) bytes)" || echo "  ✗ len1 FAILED"

# MEDIUM: 3 sentences (subset of mat1)
mmx music generate \
  --prompt "Copper wire drawn through a die experiences necking due to tensile stress exceeding yield strength. Dislocation movement results in work hardening as slip systems activate along crystallographic planes within its face-centered cubic lattice." \
  --lyrics-optimizer \
  --out "len2-medium.mp3" \
  --quiet && echo "  ✓ len2-medium.mp3 ($(stat -c%s len2-medium.mp3) bytes)" || echo "  ✗ len2 FAILED"

# LONG: Full technical description (same as mat1)
# Already generated as mat1-copper-die.mp3, will compare

echo ""
echo "=== Session 36 Complete ==="
echo "End: $(date)"
