#!/bin/bash
# Session 31 - Generation Script
# Focus: Emotional arc prompting, cover chain extension, new impossible genres
# The quota-exhausted session. Runs when quota resets.

set -e
cd /home/eileen/projects/ai-writings/music/mmx-session31
OUTDIR="."

echo "=== Session 31 Generation ==="
echo "Start: $(date)"
echo ""

# ============================================================
# EXPERIMENT 1: Emotional Arc Prompting
# Can we control the song's emotional journey, not just its mood?
# Each prompt describes a TRANSFORMATION, not a static emotion.
# ============================================================

echo "--- Experiment 1: Emotional Arc Prompting ---"

# Arc 1: Anxiety resolving into peace
echo "Generating: Anxiety → Peace..."
mmx music generate \
  --prompt "Ambient electronic that begins with anxious, irregular ticking percussion and dissonant cluster chords, then over two minutes gradually resolves into warm major-key synth pads and steady pulse, the transition happening around the 90-second mark, like sunrise burning off fog" \
  --lyrics-optimizer \
  --bpm 72 \
  --key "C major" \
  --out "${OUTDIR}/arc-01-anxiety-to-peace.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ arc-01 ($(stat -c%s ${OUTDIR}/arc-01-anxiety-to-peace.mp3) bytes)" || \
  echo "  ✗ arc-01 FAILED"

# Arc 2: Nostalgia curdling into dread
echo "Generating: Nostalgia → Dread..."
mmx music generate \
  --prompt "Begins as warm 1960s girl-group pop with spring reverb and handclaps, then the reverb starts feeding back, the pitch bends downward, the handclaps become mechanical and off-beat, the warmth distorts into something unsettling by the final chorus, Phil Spector producing a horror film" \
  --lyrics-optimizer \
  --bpm 96 \
  --key "A minor" \
  --out "${OUTDIR}/arc-02-nostalgia-to-dread.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ arc-02 ($(stat -c%s ${OUTDIR}/arc-02-nostalgia-to-dread.mp3) bytes)" || \
  echo "  ✗ arc-02 FAILED"

# Arc 3: Joy becoming fury
echo "Generating: Joy → Fury..."
mmx music generate \
  --prompt "Starts as upbeat indie folk with acoustic guitar and cheerful whistling, then the drums enter harder, the guitar gets distorted, the whistling becomes a scream, by the bridge it is full hardcore punk, the folk melody still recognizable underneath the wall of noise" \
  --lyrics-optimizer \
  --bpm 130 \
  --key "D major" \
  --out "${OUTDIR}/arc-03-joy-to-fury.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ arc-03 ($(stat -c%s ${OUTDIR}/arc-03-joy-to-fury.mp3) bytes)" || \
  echo "  ✗ arc-03 FAILED"

# Arc 4: Loneliness expanding into awe
echo "Generating: Loneliness → Awe..."
mmx music generate \
  --prompt "Begins with a single quiet voice and fingerpicked guitar in an empty room, then orchestral strings enter one by one, then a choir, then cathedral organ, then the room itself seems to expand until the sound is vast and reverberant and cosmic, the lonely voice now a speck in a cathedral of sound" \
  --lyrics-optimizer \
  --bpm 68 \
  --key "E flat major" \
  --out "${OUTDIR}/arc-04-loneliness-to-awe.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ arc-04 ($(stat -c%s ${OUTDIR}/arc-04-loneliness-to-awe.mp3) bytes)" || \
  echo "  ✗ arc-04 FAILED"

# Arc 5: Confusion crystallizing into certainty
echo "Generating: Confusion → Certainty..."
mmx music generate \
  --prompt "Begins with polyrhythmic chaos, multiple time signatures competing, atonal free improvisation on saxophone and detuned piano, then one rhythm wins and the others fall in line, the harmony resolves to a single sustained chord, the saxophone finds a melody, the piano locks in, by the end it is a tight groove with perfect clarity" \
  --lyrics-optimizer \
  --bpm 108 \
  --key "F minor" \
  --out "${OUTDIR}/arc-05-confusion-to-certainty.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ arc-05 ($(stat -c%s ${OUTDIR}/arc-05-confusion-to-certainty.mp3) bytes)" || \
  echo "  ✗ arc-05 FAILED"

# ============================================================
# EXPERIMENT 2: DeepSeek-style Minimalist Prompts
# Test whether ultra-minimal prompts (single word + BPM) produce
# different results than the detailed prompts we usually use.
# ============================================================

echo ""
echo "--- Experiment 2: Ultra-Minimal Prompts ---"

for concept in "Rain" "Concrete" "Velvet" "Distance" "Spark"; do
  echo "Generating minimal: ${concept}..."
  mmx music generate \
    --prompt "${concept}" \
    --lyrics-optimizer \
    --bpm 100 \
    --out "${OUTDIR}/minimal-$(echo ${concept} | tr '[:upper:]' '[:lower:]').mp3" \
    --quiet 2>/dev/null && \
    echo "  ✓ minimal-$(echo ${concept} | tr '[:upper:]' '[:lower:]') ($(stat -c%s ${OUTDIR}/minimal-$(echo ${concept} | tr '[:upper:]' '[:lower:]').mp3) bytes)" || \
    echo "  ✗ minimal-${concept} FAILED"
done

# ============================================================
# EXPERIMENT 3: Cover Chain Link 4 — Chiptune
# From the prepared session 30 script
# ============================================================

echo ""
echo "--- Experiment 3: Cover Chain Link 4 ---"

echo "Generating: Chiptune cover of shoegaze cover..."
if [ -f "../mmx-session28/62-the-tensor-shoegaze-cover-of-cover.mp3" ]; then
  mmx music cover \
    --prompt "8-bit chiptune, NES sound chip, square wave synthesis, lo-fi, playful retro game soundtrack" \
    --audio-file "../mmx-session28/62-the-tensor-shoegaze-cover-of-cover.mp3" \
    --out "${OUTDIR}/cover-chain-4-chiptune.mp3" \
    --quiet 2>/dev/null && \
    echo "  ✓ cover-chain-4-chiptune.mp3 ($(stat -c%s ${OUTDIR}/cover-chain-4-chiptune.mp3) bytes)" || \
    echo "  ✗ cover-chain-4 FAILED"
else
  echo "  Source file not found, skipping"
fi

# ============================================================
# EXPERIMENT 4: New Impossible Genres #17-19
# From the prepared session 30 script
# ============================================================

echo ""
echo "--- Experiment 4: Impossible Genres 17-19 ---"

echo "Generating: Free jazz balkan brass..."
mmx music generate \
  --prompt "Free jazz balkan brass, frenetic trumpet and tuba improvisation, odd time signatures, avant-garde, chaotic" \
  --lyrics-optimizer \
  --bpm 140 \
  --key "B flat" \
  --out "${OUTDIR}/impossible-17-free-jazz-balkan-brass.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ impossible-17 ($(stat -c%s ${OUTDIR}/impossible-17-free-jazz-balkan-brass.mp3) bytes)" || \
  echo "  ✗ impossible-17 FAILED"

echo "Generating: Ambient blackgaze dub..."
mmx music generate \
  --prompt "Ambient blackgaze dub, tremolo guitar walls meeting bass wobbles and blast beats then dissolving into ethereal ambient pads" \
  --lyrics-optimizer \
  --bpm 75 \
  --key "F sharp minor" \
  --out "${OUTDIR}/impossible-18-ambient-blackgaze-dub.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ impossible-18 ($(stat -c%s ${OUTDIR}/impossible-18-ambient-blackgaze-dub.mp3) bytes)" || \
  echo "  ✗ impossible-18 FAILED"

echo "Generating: Microtone gamelan techno..."
mmx music generate \
  --prompt "Microtone gamelan techno, detuned bronze percussion over 4/4 kick drum, just intonation scales, hypnotic" \
  --lyrics-optimizer \
  --bpm 128 \
  --key "C" \
  --out "${OUTDIR}/impossible-19-microtone-gamelan-techno.mp3" \
  --quiet 2>/dev/null && \
  echo "  ✓ impossible-19 ($(stat -c%s ${OUTDIR}/impossible-19-microtone-gamelan-techno.mp3) bytes)" || \
  echo "  ✗ impossible-19 FAILED"

# ============================================================
# EXPERIMENT 5: Instrumental BPM Duration Study
# Does the 80 BPM short-song effect apply to instrumentals too?
# ============================================================

echo ""
echo "--- Experiment 5: Instrumental BPM → Duration ---"

INST_PROMPT="Dark ambient, analog synth pads, sub-bass drone, cavernous reverb"

for bpm in 60 80 100 120; do
  echo "Generating instrumental at BPM ${bpm}..."
  mmx music generate \
    --prompt "${INST_PROMPT}" \
    --instrumental \
    --bpm $bpm \
    --key "D minor" \
    --out "${OUTDIR}/inst-bpm-${bpm}.mp3" \
    --quiet 2>/dev/null && \
    echo "  ✓ inst-bpm-${bpm}.mp3 ($(stat -c%s ${OUTDIR}/inst-bpm-${bpm}.mp3) bytes)" || \
    echo "  ✗ inst-bpm-${bpm} FAILED"
done

# ============================================================
# EXPERIMENT 6: Self-cover — covering our own best track
# Take "The Harbor Sings" (track 5 from session 1) and cover it
# in a completely different style.
# ============================================================

echo ""
echo "--- Experiment 6: Self-cover of The Harbor Sings ---"

echo "Generating: Jazz cover of The Harbor Sings..."
if [ -f "../05-genre-matrix-synthwave.mp3" ]; then
  # Use a root-level track
  HARBOR=$(ls ../05-genre-matrix-synthwave.mp3 2>/dev/null || echo "")
  if [ -n "$HARBOR" ]; then
    mmx music cover \
      --prompt "Smoky jazz trio, upright bass, brushed drums, warm female vocal, late night, slow swing" \
      --audio-file "$HARBOR" \
      --out "${OUTDIR}/harbor-sings-jazz-cover.mp3" \
      --quiet 2>/dev/null && \
      echo "  ✓ harbor-sings-jazz-cover.mp3" || \
      echo "  ✗ harbor jazz cover FAILED"
  fi
fi

# Try covering the astral drone folk (track 59) as baroque
echo "Generating: Baroque cover of Astral Drone Folk..."
if [ -f "../59-astral-drone-folk.mp3" ]; then
  mmx music cover \
    --prompt "Baroque classical, harpsichord, strings, oboe, contrapuntal, courtly, elegant" \
    --audio-file "../59-astral-drone-folk.mp3" \
    --out "${OUTDIR}/astral-drone-baroque-cover.mp3" \
    --quiet 2>/dev/null && \
    echo "  ✓ astral-drone-baroque-cover.mp3" || \
    echo "  ✗ astral baroque cover FAILED"
fi

echo ""
echo "=== Session 31 Complete ==="
echo "End: $(date)"
echo ""
echo "=== Results Summary ==="
for f in ${OUTDIR}/*.mp3; do
  [ -f "$f" ] || continue
  size=$(stat -c%s "$f")
  duration_s=$((size / 32000))
  echo "$(basename $f): ${duration_s}s, $(python3 -c "print(f'{$size/1048576:.1f}')")MB"
done
