#!/bin/bash
# Session 39: The Physical Phenomena Experiment
# Question: Can emotion be evoked in music generated from prompts that contain NO emotion words?
# Four LLMs were given the constraint: "Describe music through purely physical phenomena"
# Each interpreted the constraint differently:
#   - Llama: Dramatic physical events (waterfalls, breaking ice, sinking stones)
#   - Phi3: Acoustic physics textbook (standing waves, sympathetic vibrations)
#   - Qwen: Minimal, almost haiku-like physical observations
#   - Granite: Warm, embodied instrument descriptions (vibrating wood, stretched skin)
#
# PREDICTION: Based on Session 36 translational distance findings,
# Phi3 (most technical/acoustic) should produce highest centroid.
# Granite (most conventionally musical language) should be closest to corpus means.
# Llama (dramatic but non-technical) should be in between.
# Qwen (sparse/minimal) should be shortest with lowest centroid.

cd /home/eileen/projects/ai-writings/music/mmx-session39-physical-phenomena

echo "=== Session 39: The Physical Phenomena Experiment ==="
echo "Start: $(date)"
echo ""

# ============================================
# EXPERIMENT A: Llama 3.2 Physical Prompts (5 tracks)
# ============================================
echo "--- Experiment A: Llama Physical Prompts ---"

mmx music generate \
  --prompt "The low rumbles of a distant waterfall echo through the air, resonating with the vibrations of a metal pipe struck by a hammer. As the sound waves propagate, they create a sense of tension that builds to a crescendo, releasing in a burst of sonic energy. The resonance lingers, leaving behind a faint hum." \
  --lyrics-optimizer --out "llama1-waterfall.mp3" --quiet && echo "  ✓ llama1" || echo "  ✗ llama1 FAILED"

mmx music generate \
  --prompt "A solitary violin string vibrates at its breaking point, emitting a piercing shriek as it oscillates between two frequencies. Each note is a sharp release of pressure, followed by an eerie silence that underscores the next moment's tension. As the vibration slows, it leaves behind a haunting echo." \
  --lyrics-optimizer --out "llama2-violin.mp3" --quiet && echo "  ✓ llama2" || echo "  ✗ llama2 FAILED"

mmx music generate \
  --prompt "The soft whoosh of air escaping through a narrow pipe creates a soothing melody that ebbs and flows with each breath. With each exhalation, the sound waves build in intensity before releasing in a gentle sigh, as if the music itself were exhaling slowly into the void." \
  --lyrics-optimizer --out "llama3-pipe.mp3" --quiet && echo "  ✓ llama3" || echo "  ✗ llama3 FAILED"

mmx music generate \
  --prompt "A heavy stone dropped into a stagnant pool creates concentric ripples that spread outward in all directions, disturbing the mirrored surface of the water. Each ripple's edge is sharp and defined, with an underlying oscillation that seems to reverberate through every molecule of air within earshot." \
  --lyrics-optimizer --out "llama4-stone.mp3" --quiet && echo "  ✓ llama4" || echo "  ✗ llama4 FAILED"

mmx music generate \
  --prompt "The repetitive crunch of ice breaking away underfoot echoes through a cavernous space, each successive impact sending shockwaves down a frozen tunnel. As the last shard of ice shatters into silence, it leaves behind a sharp-edged stillness that lingers like an open wound." \
  --lyrics-optimizer --out "llama5-ice.mp3" --quiet && echo "  ✓ llama5" || echo "  ✗ llama5 FAILED"

# ============================================
# EXPERIMENT B: Phi3 Acoustic Physics Prompts (5 tracks)
# ============================================
echo ""
echo "--- Experiment B: Phi3 Acoustic Physics ---"

mmx music generate \
  --prompt "The sound waves originating from the instrument reverberate throughout the room, causing standing wave patterns in resonant frequencies that create harmonic overtones blending seamlessly with each other to form complex timbre of rich sonic textures and tones emanating directly into the surrounding air." \
  --lyrics-optimizer --out "phi1-standing-waves.mp3" --quiet && echo "  ✓ phi1" || echo "  ✗ phi1 FAILED"

mmx music generate \
  --prompt "The rapid vibrations of strings within an instrument produce sound waves at high frequency, propagating through a medium as compressions and rarefactions that interact in phase interference patterns resulting in bright, cutting sounds with intense attack points creating sharp transients when hitting surfaces or striking tuning forks nearby." \
  --lyrics-optimizer --out "phi2-interference.mp3" --quiet && echo "  ✓ phi2" || echo "  ✗ phi2 FAILED"

mmx music generate \
  --prompt "The percussive impact of drumheads against the resonant body generates sound waves carrying high amplitude energy pulses transmitted through a fluid medium such as air causing sympathetic vibrations in neighboring objects that respond by producing their own harmonic frequencies, amplifying and enriching the acoustic environment." \
  --lyrics-optimizer --out "phi3-percussive.mp3" --quiet && echo "  ✓ phi3" || echo "  ✗ phi3 FAILED"

mmx music generate \
  --prompt "The oscillation of reeds within woodwind instruments causes periodic changes to pressure resulting in sound waves with specific wavelengths travelling through a medium causing resonant vibrations at natural frequencies which then constructively interfere creating unique timbres characterized by overtones and undertones that create warm, mellow sounds blending together like honey flowing downhill." \
  --lyrics-optimizer --out "phi4-reeds.mp3" --quiet && echo "  ✓ phi4" || echo "  ✗ phi4 FAILED"

mmx music generate \
  --prompt "The mechanical movement of metal keys in pianos transfers energy to strings causing them to vibrate at specific frequencies with varying amplitude which then generate sound waves propagating through a medium interacting constructively and destructively creating rich textures where multiple pitches blend together into harmonic overtones, the resulting timbre evoking an earthy sonic quality reminiscent of distant thunder rumbling in storm clouds." \
  --lyrics-optimizer --out "phi5-piano-keys.mp3" --quiet && echo "  ✓ phi5" || echo "  ✗ phi5 FAILED"

# ============================================
# EXPERIMENT C: Qwen Minimal Physical Prompts (5 tracks)
# ============================================
echo ""
echo "--- Experiment C: Qwen Minimal Physical ---"

mmx music generate \
  --prompt "The air vibrates with the low, rhythmic pulsations of drums, creating an audible wave upon striking surfaces." \
  --lyrics-optimizer --out "qwen1-drums.mp3" --quiet && echo "  ✓ qwen1" || echo "  ✗ qwen1 FAILED"

mmx music generate \
  --prompt "A high note pierces through the ether, forming a shimmering trail that dances across smooth metal before dissipating into silence." \
  --lyrics-optimizer --out "qwen2-shimmer.mp3" --quiet && echo "  ✓ qwen2" || echo "  ✗ qwen2 FAILED"

mmx music generate \
  --prompt "Strings are plucked to produce notes that resonate within hollowed wooden vessels, causing them to emit faint hums like tiny bells." \
  --lyrics-optimizer --out "qwen3-strings.mp3" --quiet && echo "  ✓ qwen3" || echo "  ✗ qwen3 FAILED"

mmx music generate \
  --prompt "Blasts of air from brass instruments sculpt billowing clouds of condensation around their mouths, leaving behind trails that dissipate quickly in stillness." \
  --lyrics-optimizer --out "qwen4-brass.mp3" --quiet && echo "  ✓ qwen4" || echo "  ✗ qwen4 FAILED"

mmx music generate \
  --prompt "Percussion hits strike the ground with force, generating ripples spreading outward until they merge and dissipate into the ambient background noise." \
  --lyrics-optimizer --out "qwen5-percussion.mp3" --quiet && echo "  ✓ qwen5" || echo "  ✗ qwen5 FAILED"

# ============================================
# EXPERIMENT D: Granite Warm Instrument Prompts (5 tracks)
# ============================================
echo ""
echo "--- Experiment D: Granite Warm Instruments ---"

mmx music generate \
  --prompt "Imagine the first notes emerging from a flute, its wooden body vibrating gently against your ear, sending subtle pulsations that echo in the stillness of an autumn forest." \
  --lyrics-optimizer --out "granite1-flute.mp3" --quiet && echo "  ✓ granite1" || echo "  ✗ granite1 FAILED"

mmx music generate \
  --prompt "Visualize the drum's surface, a tightly stretched animal skin, quivering with each strike, causing ripples that travel through the air and seem to resonate within your chest, mimicking the rhythmic heartbeat of nature." \
  --lyrics-optimizer --out "granite2-drum.mp3" --quiet && echo "  ✓ granite2" || echo "  ✗ granite2 FAILED"

mmx music generate \
  --prompt "Envision a cello, its thick, dark wood body expanding and contracting as it plays, generating deep, resonant tones that ripple through the air, like a gentle wave in a tranquil lake." \
  --lyrics-optimizer --out "granite3-cello.mp3" --quiet && echo "  ✓ granite3" || echo "  ✗ granite3 FAILED"

mmx music generate \
  --prompt "Picture a piano's hammer striking the strings, causing them to vibrate rapidly against the metal frame, producing high-pitched shards of sound that crackle and scatter, much like the frost on winter morning grass breaking free from its icy bonds." \
  --lyrics-optimizer --out "granite4-piano.mp3" --quiet && echo "  ✓ granite4" || echo "  ✗ granite4 FAILED"

mmx music generate \
  --prompt "Visualize a violin's thin, curved wood body vibrating swiftly, generating delicate, trembling notes that dance in the air, resembling the graceful, swift movements of birds taking flight on a clear summer day." \
  --lyrics-optimizer --out "granite5-violin.mp3" --quiet && echo "  ✓ granite5" || echo "  ✗ granite5 FAILED"

echo ""
echo "=== Session 39 Complete ==="
echo "End: $(date)"
echo "Expected tracks: 20"
ls -la *.mp3 2>/dev/null | wc -l
