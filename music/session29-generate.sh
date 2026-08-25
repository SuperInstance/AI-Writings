#!/bin/bash
# SongForge Session 29 — Monday August 10, 2026 6:46 AM AKST
# "The Vocal BPM Study + New Impossible Fusions"
#
# MMX weekly quota: 69% remaining. First MMX session since reset.
#
# EXPERIMENTS:
# A) Vocal BPM Study — same lyrics, same key, same prompt, 6 different BPMs (40-140)
#    Tests whether the bimodal curve persists WITH vocals
# B) Three new impossible genre fusions
# C) DeepSeek/GLM-generated lyrics experiment (using mmx text chat as lyricist)

set -e
cd /home/eileen/projects/ai-writings/music

OUTDIR="mmx-session29"
mkdir -p "$OUTDIR"

echo "=== EXPERIMENT A: Vocal BPM Study ==="
echo "Same lyrics, same key (C major), same prompt, 6 BPMs"

for BPM in 40 60 80 100 120 140; do
  echo "--- Vocal BPM Study: ${BPM} BPM ---"
  mmx music generate \
    --prompt "Warm indie folk, fingerpicked acoustic guitar, soft piano, gentle" \
    --lyrics-file lyrics-vocal-bpm-study.txt \
    --vocals "warm female alto, intimate, conversational" \
    --bpm "$BPM" \
    --key "C major" \
    --out "$OUTDIR/vocal-bpm-${BPM}.mp3" \
    --quiet
  echo "Done: ${BPM} BPM"
  sleep 15
done

echo "=== EXPERIMENT B: New Impossible Genre Fusions ==="

echo "--- Track 70: Free Jazz Balkan Brass ---"
mmx music generate \
  --prompt "Free jazz balkan brass, Ornette Coleman meets Fanfare Ciocarlia, chaotic horns, odd meters, celebration and deconstruction" \
  --lyrics "[Verse]
The trumpet knows a secret it won't tell
The tuba has been drinking since the bell
Rang out in B-flat odd-time celebration
The saxophone forgot the notation

[Chorus]
The village burns, the brass plays on
The form dissolves, the rhythm's gone
The dance doesn't need a key
The free jazz balkan brass agrees" \
  --vocals "raw male tenor, celebratory, slightly unhinged" \
  --bpm 150 \
  --key "F minor" \
  --out "$OUTDIR/70-free-jazz-balkan-brass.mp3" \
  --quiet
echo "Track 70 done"
sleep 15

echo "--- Track 71: Ambient Blackgaze Dub ---"
mmx music generate \
  --prompt "Ambient blackgaze dub, atmospheric black metal guitars meeting King Tubby dub production, vast reverb spaces, tape delays, tremolo picking dissolving into echos" \
  --lyrics "[Verse]
The frost forms on the mixing board
The delay pedal catches a chord
That was meant for a cathedral
But ends up in a winter forest
Where every echo is a ghost

[Chorus]
The black metal meets the dub
The blast beat meets the one-drop
The reverb is the same religion
The cold and the bass are one" \
  --vocals "ethereal female soprano with black metal shriek accents" \
  --bpm 70 \
  --key "D minor" \
  --out "$OUTDIR/71-ambient-blackgaze-dub.mp3" \
  --quiet
echo "Track 71 done"
sleep 15

echo "--- Track 72: Microtone Gamelan Techno ---"
mmx music generate \
  --prompt "Microtone gamelan techno, Indonesian pelog and slendro scales meeting Detroit minimal techno, metallic percussion, looping patterns shifting in phase, Robert Hood meets the court of Yogyakarta" \
  --lyrics "[Verse]
The bronze keys sing in frequencies
Between the notes we know
The detuned pairs beat slowly
Like waves that come and go

[Chorus]
The palace is a warehouse now
The gongs are drum machines
The pattern shifts a cent per loop
The old scale always redeems" \
  --vocals "mixed ensemble, part sung part spoken, Indonesian and English blend" \
  --bpm 128 \
  --key "C minor" \
  --out "$OUTDIR/72-microtone-gamelan-techno.mp3" \
  --quiet
echo "Track 72 done"
sleep 15

echo "=== EXPERIMENT C: M3 as Lyricist for New Corpus Adaptations ==="

echo "--- Track 73: The Cosmic Web and the Fifth (M3 lyrics) ---"
# Generate lyrics via M3 text chat
mmx text chat \
  --system "You are a poet writing song lyrics inspired by essays about music and mathematics. Write vivid, concrete, singable lyrics. Use [Verse] and [Chorus] tags. Keep under 1000 characters." \
  --message "Write lyrics inspired by the concept: 'The Cosmic Web and the Fifth' — the cosmic web (large-scale structure of the universe) resembles a musical fifth interval. Filaments of galaxies stretched between voids like strings tuned to a perfect ratio. The universe vibrates at the interval of creation." \
  --temperature 0.93 \
  --output json \
  --quiet > "$OUTDIR/m3-cosmic-web-lyrics.json"

# Extract lyrics from JSON
python3 -c "
import json, sys
with open('$OUTDIR/m3-cosmic-web-lyrics.json') as f:
    data = json.load(f)
content = data.get('content', data.get('response', ''))
if not content:
    content = str(data)
# Trim to 1100 chars
if len(content) > 1100:
    # Find last complete line before 1100
    trimmed = content[:1100]
    last_nl = trimmed.rfind('\n')
    if last_nl > 800:
        content = trimmed[:last_nl]
with open('$OUTDIR/m3-cosmic-web-lyrics.txt', 'w') as f:
    f.write(content)
print(f'Lyrics: {len(content)} chars')
" 2>&1 || echo "Lyrics extraction deferred"

if [ -f "$OUTDIR/m3-cosmic-web-lyrics.txt" ]; then
  mmx music generate \
    --prompt "Cosmic ambient, deep space drone, faint strings, expanding universe, vast and contemplative" \
    --lyrics-file "$OUTDIR/m3-cosmic-web-lyrics.txt" \
    --vocals "ethereal mixed choir, wordless and harmonic" \
    --bpm 50 \
    --key "D minor" \
    --out "$OUTDIR/73-the-cosmic-web.mp3" \
    --quiet
  echo "Track 73 done"
fi
sleep 15

echo "--- Track 74: The Quartz Clock Sings (M3 lyrics) ---"
mmx text chat \
  --system "You are a poet writing song lyrics inspired by essays about music and mathematics. Write vivid, concrete, singable lyrics. Use [Verse] and [Chorus] tags. Keep under 1000 characters." \
  --message "Write lyrics inspired by the concept: a quartz crystal oscillator that keeps time for a computer discovers it is singing. The piezoelectric vibration at 32,768 Hz is a note — B-sharp slightly flat. The clock has been singing its entire life and never knew." \
  --temperature 0.93 \
  --output json \
  --quiet > "$OUTDIR/m3-quartz-clock-lyrics.json"

python3 -c "
import json, sys
with open('$OUTDIR/m3-quartz-clock-lyrics.json') as f:
    data = json.load(f)
content = data.get('content', data.get('response', ''))
if not content:
    content = str(data)
if len(content) > 1100:
    trimmed = content[:1100]
    last_nl = trimmed.rfind('\n')
    if last_nl > 800:
        content = trimmed[:last_nl]
with open('$OUTDIR/m3-quartz-clock-lyrics.txt', 'w') as f:
    f.write(content)
print(f'Lyrics: {len(content)} chars')
" 2>&1 || echo "Lyrics extraction deferred"

if [ -f "$OUTDIR/m3-quartz-clock-lyrics.txt" ]; then
  mmx music generate \
    --prompt "Minimalist electronic, ticking percussion, crystal-clear tones, Steve Reich meets Aphex Twin, precise and shimmering" \
    --lyrics-file "$OUTDIR/m3-quartz-clock-lyrics.txt" \
    --vocals "clean male tenor, precise, almost robotic" \
    --bpm 90 \
    --key "C major" \
    --out "$OUTDIR/74-the-quartz-clock-sings.mp3" \
    --quiet
  echo "Track 74 done"
fi

echo ""
echo "=== SESSION 29 COMPLETE ==="
echo "Tracks generated:"
ls -la "$OUTDIR"/*.mp3 2>/dev/null || echo "No tracks found"
echo ""
echo "Total size:"
du -sh "$OUTDIR" 2>/dev/null || echo "N/A"
