#!/bin/bash
# Session 30 - Generation Script
# Focus: Duration as the true variable, 80 BPM investigation, impossible genres
# Runs after quota resets (12:00 PM AKST / 20:00 UTC)

set -e
cd /home/eileen/projects/ai-writings/music/mmx-session30
OUTDIR="."

echo "=== Session 30 Generation ==="
echo "Start: $(date)"
echo ""

# ============================================================
# EXPERIMENT 1: BPM → Duration mapping (instrumental controls)
# Same prompt, same genre, same key, different BPMs.
# Question: does the model make shorter instrumental tracks at 80 BPM too?
# ============================================================

echo "--- Experiment 1: Instrumental BPM → Duration ---"

INST_PROMPT="Dark ambient, analog synth pads, sub-bass drone, cavernous reverb"
LYRICS="The keeper strikes the match
The lens begins to turn
Eight seconds per revolution
The beam sweeps the fog
Something rises from the water
Something approaches the shore
The hand hovers over the switch
The light says here I am
The light says here is land
The keeper says I know"

for bpm in 60 80 100 120; do
  echo "Generating instrumental at BPM ${bpm}..."
  mmx music generate \
    --prompt "${INST_PROMPT}" \
    --instrumental \
    --bpm $bpm \
    --key "D minor" \
    --out "${OUTDIR}/inst-bpm-${bpm}.mp3" \
    --quiet --yes 2>/dev/null && \
    echo "  ✓ inst-bpm-${bpm}.mp3 ($(stat -c%s ${OUTDIR}/inst-bpm-${bpm}.mp3) bytes)" || \
    echo "  ✗ inst-bpm-${bpm} FAILED"
done

# ============================================================
# EXPERIMENT 2: 80 BPM across genres
# Does the "short song" effect at 80 BPM persist across genres?
# ============================================================

echo ""
echo "--- Experiment 2: 80 BPM across genres ---"

LYRICS_FILE="${OUTDIR}/lighthouse-lyrics.txt"
cat > "${LYRICS_FILE}" << 'LYRICS'
[Verse 1]
Strike the match and the mechanism turns
Eight seconds per revolution the beam returns
The fog comes in and the light diffuses
Into grey particles the shore confuses

[Chorus]
The light says here I am
The light says here is land
The rocks say I will hurt you
The keeper does not understand

[Verse 2]
Something rises where the water breaks
Following the pulse the shoreline makes
Forty million years of coming near
The light is three hundred years of standing here

[Chorus]
The light says here I am
The light says here is land
The thing says I am coming
The keeper says I understand

[Bridge]
At eighty beats the heart is at rest
The hand hovers above the switch
The lens rotates the fog the shore
The duration is sufficient

[Outro]
The keeper strikes the match again
LYRICS

for genre in "Folk horror, fingerpicked acoustic guitar, eerie choir" \
             "Minimalist electronic, ticking hi-hat, sub-bass, cold synth pads" \
             "Doom metal, distorted guitar, thunderous drums, growled vocals" \
             "Bedroom pop, jangly guitar, warm tape saturation, soft drums"; do
  # Create safe filename from genre
  safename=$(echo "$genre" | cut -d',' -f1 | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | head -c 20)
  echo "Generating 80 BPM: ${genre}..."
  mmx music generate \
    --prompt "${genre}" \
    --lyrics-file "${LYRICS_FILE}" \
    --bpm 80 \
    --key "D minor" \
    --out "${OUTDIR}/bpm80-${safename}.mp3" \
    --quiet --yes 2>/dev/null && \
    echo "  ✓ bpm80-${safename}.mp3 ($(stat -c%s ${OUTDIR}/bpm80-${safename}.mp3) bytes)" || \
    echo "  ✗ bpm80-${safename} FAILED"
done

# ============================================================
# EXPERIMENT 3: Temperature comparison (lyrics from M3 at different temps)
# Since M3 text is rate-limited, use pre-written lyrics at 3 detail levels
# to test the duration effect with controlled lyrics
# ============================================================

echo ""
echo "--- Experiment 3: Same lyrics, different genre complexity ---"

# Use the lighthouse lyrics for all
# Test whether genre affects duration when lyrics are controlled
for genre in "Minimal" "Medium" "Detailed"; do
  case $genre in
    Minimal)
      PROMPT="Folk"
      ;;
    Medium)
      PROMPT="Folk horror, acoustic guitar, eerie choir, sub-bass drone, reverb"
      ;;
    Detailed)
      PROMPT="Nordic folk horror, fingerpicked nylon acoustic guitar tuned to DADGAD, spectral choir samples processed through spring reverb, sub-bass drone at 55Hz, field recordings of coastal wind, tape delay on percussion, cinematic build, influences: Darkside, Hildur Gudnadottir, Wardruna"
      ;;
  esac
  echo "Generating genre detail: ${genre}..."
  mmx music generate \
    --prompt "${PROMPT}" \
    --lyrics-file "${LYRICS_FILE}" \
    --bpm 90 \
    --key "D minor" \
    --out "${OUTDIR}/lighthouse-${genre,,}.mp3" \
    --quiet --yes 2>/dev/null && \
    echo "  ✓ lighthouse-${genre,,}.mp3 ($(stat -c%s ${OUTDIR}/lighthouse-${genre,,}.mp3) bytes)" || \
    echo "  ✗ lighthouse-${genre,,} FAILED"
done

# ============================================================
# EXPERIMENT 4: New impossible genres
# ============================================================

echo ""
echo "--- Experiment 4: Impossible genres ---"

# Genre 17: Free jazz balkan brass
echo "Generating: Free jazz balkan brass..."
mmx music generate \
  --prompt "Free jazz balkan brass, frenetic trumpet and tuba improvisation, odd time signatures, avant-garde, chaotic" \
  --lyrics-optimizer \
  --bpm 140 \
  --key "B flat" \
  --out "${OUTDIR}/impossible-17-free-jazz-balkan-brass.mp3" \
  --quiet --yes 2>/dev/null && \
  echo "  ✓ impossible-17 ($(stat -c%s ${OUTDIR}/impossible-17-free-jazz-balkan-brass.mp3) bytes)" || \
  echo "  ✗ impossible-17 FAILED"

# Genre 18: Ambient blackgaze dub
echo "Generating: Ambient blackgaze dub..."
mmx music generate \
  --prompt "Ambient blackgaze dub, tremolo guitar walls meeting bass wobbles and blast beats then dissolving into ethereal ambient pads" \
  --lyrics-optimizer \
  --bpm 75 \
  --key "F sharp minor" \
  --out "${OUTDIR}/impossible-18-ambient-blackgaze-dub.mp3" \
  --quiet --yes 2>/dev/null && \
  echo "  ✓ impossible-18 ($(stat -c%s ${OUTDIR}/impossible-18-ambient-blackgaze-dub.mp3) bytes)" || \
  echo "  ✗ impossible-18 FAILED"

# Genre 19: Microtone gamelan techno
echo "Generating: Microtone gamelan techno..."
mmx music generate \
  --prompt "Microtone gamelan techno, detuned bronze percussion over 4/4 kick drum, just intonation scales, hypnotic" \
  --lyrics-optimizer \
  --bpm 128 \
  --key "C" \
  --out "${OUTDIR}/impossible-19-microtone-gamelan-techno.mp3" \
  --quiet --yes 2>/dev/null && \
  echo "  ✓ impossible-19 ($(stat -c%s ${OUTDIR}/impossible-19-microtone-gamelan-techno.mp3) bytes)" || \
  echo "  ✗ impossible-19 FAILED"

# ============================================================
# EXPERIMENT 5: Cover chain link 4
# Cover the previous cover to extend the chain
# ============================================================

echo ""
echo "--- Experiment 5: Cover chain link 4 ---"

# Link 3 was shoegaze cover of dub techno cover of cool jazz
# Link 4: Chiptune cover of the shoegaze version
echo "Generating: Chiptune cover of shoegaze cover..."
if [ -f "../mmx-session28/62-the-tensor-shoegaze-cover-of-cover.mp3" ]; then
  mmx music cover \
    --prompt "8-bit chiptune, NES sound chip, square wave synthesis, lo-fi, playful retro game soundtrack" \
    --audio-file "../mmx-session28/62-the-tensor-shoegaze-cover-of-cover.mp3" \
    --out "${OUTDIR}/cover-chain-4-chiptune.mp3" \
    --quiet --yes 2>/dev/null && \
    echo "  ✓ cover-chain-4-chiptune.mp3 ($(stat -c%s ${OUTDIR}/cover-chain-4-chiptune.mp3) bytes)" || \
    echo "  ✗ cover-chain-4 FAILED"
else
  echo "  Source file not found, skipping"
fi

echo ""
echo "=== Session 30 Complete ==="
echo "End: $(date)"
echo ""
echo "=== Results Summary ==="
for f in ${OUTDIR}/*.mp3; do
  [ -f "$f" ] || continue
  duration=$(ffmpeg -i "$f" 2>&1 | grep Duration | awk '{print $2}' | tr -d ',')
  size=$(stat -c%s "$f")
  echo "$(basename $f): ${duration}, $(python3 -c "print(f'{$size/1048576:.1f}')")MB"
done
