#!/bin/bash
# SongForge Session 29b — Monday August 10, 2026 ~6:00 AM AKST
# "New Voices, New Methods"
#
# EXPERIMENTS:
# A) Vocal BPM Study — same lyrics at 6 BPMs (tests bimodal curve with voice)
# B) M3-as-Lyricist: Two new concepts with M3-generated lyrics  
# C) Prompt Engineering Study: Same lyrics, 3 different prompt detail levels
# D) Three new impossible genres
# E) Cover chain link 4: Chiptune cover of the shoegaze cover of the dub techno cover

set -e
cd /home/eileen/projects/ai-writings/music

OUTDIR="mmx-session29"
mkdir -p "$OUTDIR"

echo "=== EXPERIMENT A: Vocal BPM Study ==="
echo "Same lyrics at 6 BPMs. Testing if bimodal curve persists WITH vocals."

for BPM in 40 60 80 100 120 140; do
  echo "--- Vocal BPM: ${BPM} ---"
  mmx music generate \
    --prompt "Warm indie folk, fingerpicked acoustic guitar, soft piano, gentle and intimate" \
    --lyrics-file lyrics-vocal-bpm-study.txt \
    --vocals "warm female alto, intimate, conversational" \
    --bpm "$BPM" \
    --key "C major" \
    --out "$OUTDIR/vocal-bpm-${BPM}.mp3" \
    --quiet 2>&1 && echo "OK: ${BPM}" || echo "FAIL: ${BPM}"
  sleep 12
done

echo ""
echo "=== EXPERIMENT B: M3 as Lyricist — New Concepts ==="

echo "--- B1: The Cosmic Web and the Fifth ---"
mmx text chat \
  --system "You are a poet writing song lyrics inspired by science. Write vivid, concrete, singable lyrics with verse-chorus structure. Use [Verse] and [Chorus] tags. Under 1000 characters." \
  --message "Write lyrics about: The cosmic web (large-scale structure of the universe) resembles a musical fifth interval. Filaments of galaxies stretched between voids like strings tuned to a perfect 3:2 ratio. The universe is a resonating chamber." \
  --temperature 0.93 \
  --output json \
  --quiet 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    content = data.get('content', data.get('response', ''))
    if not content: content = str(data)
    if len(content) > 1100:
        trimmed = content[:1100]
        last_nl = trimmed.rfind('\n')
        if last_nl > 800: content = trimmed[:last_nl]
    with open('$OUTDIR/m3-cosmic-web-lyrics.txt', 'w') as f:
        f.write(content)
    print(f'Lyrics: {len(content)} chars')
except Exception as e:
    print(f'Error: {e}')
"

if [ -f "$OUTDIR/m3-cosmic-web-lyrics.txt" ]; then
  mmx music generate \
    --prompt "Cosmic ambient folk, deep space drone with acoustic guitar, faint strings, vast and contemplative, like Sigur Rós in a void" \
    --lyrics-file "$OUTDIR/m3-cosmic-web-lyrics.txt" \
    --vocals "ethereal mixed choir, wordless harmonics" \
    --bpm 50 \
    --key "D minor" \
    --out "$OUTDIR/64-the-cosmic-web.mp3" \
    --quiet 2>&1 && echo "OK: cosmic web" || echo "FAIL: cosmic web"
  sleep 12
fi

echo "--- B2: The Quartz Clock Sings ---"
mmx text chat \
  --system "You are a poet writing song lyrics inspired by technology. Write vivid, concrete, singable lyrics with verse-chorus structure. Use [Verse] and [Chorus] tags. Under 1000 characters." \
  --message "Write lyrics about: A quartz crystal oscillator in a computer vibrates at 32,768 Hz. It has been singing B-sharp slightly flat its entire life and never knew. One day the RTC interrupt handler hears it." \
  --temperature 0.93 \
  --output json \
  --quiet 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    content = data.get('content', data.get('response', ''))
    if not content: content = str(data)
    if len(content) > 1100:
        trimmed = content[:1100]
        last_nl = trimmed.rfind('\n')
        if last_nl > 800: content = trimmed[:last_nl]
    with open('$OUTDIR/m3-quartz-clock-lyrics.txt', 'w') as f:
        f.write(content)
    print(f'Lyrics: {len(content)} chars')
except Exception as e:
    print(f'Error: {e}')
"

if [ -f "$OUTDIR/m3-quartz-clock-lyrics.txt" ]; then
  mmx music generate \
    --prompt "Minimalist electronic, ticking percussion, crystal-clear bell tones, Steve Reich meets Aphex Twin, precise and shimmering" \
    --lyrics-file "$OUTDIR/m3-quartz-clock-lyrics.txt" \
    --vocals "clean male tenor, precise, almost robotic with warmth underneath" \
    --bpm 90 \
    --key "C major" \
    --out "$OUTDIR/65-the-quartz-clock.mp3" \
    --quiet 2>&1 && echo "OK: quartz clock" || echo "FAIL: quartz clock"
  sleep 12
fi

echo ""
echo "=== EXPERIMENT C: Prompt Detail Study ==="
echo "Same lyrics, 3 levels of prompt detail. Does prompt richness affect output density?"

# Minimal prompt
mmx music generate \
  --prompt "Folk rock" \
  --lyrics-file lyrics-the-compiler-dreams-in-type.txt \
  --vocals "low male baritone" \
  --bpm 85 \
  --key "C minor" \
  --out "$OUTDIR/prompt-minimal.mp3" \
  --quiet 2>&1 && echo "OK: minimal" || echo "FAIL: minimal"
sleep 12

# Medium prompt  
mmx music generate \
  --prompt "Dark wave folk rock, analog synths, acoustic guitar, brooding atmosphere" \
  --lyrics-file lyrics-the-compiler-dreams-in-type.txt \
  --vocals "low male baritone, detached delivery" \
  --bpm 85 \
  --key "C minor" \
  --out "$OUTDIR/prompt-medium.mp3" \
  --quiet 2>&1 && echo "OK: medium" || echo "FAIL: medium"
sleep 12

# Detailed prompt
mmx music generate \
  --prompt "Dark wave folk rock, vintage analog synths with slow filter sweeps, fingerpicked acoustic guitar in open C minor tuning, brooding atmospheric build, Depeche Mode meets Bon Iver, sparse drums with heavy reverb, sub-bass swells" \
  --lyrics-file lyrics-the-compiler-dreams-in-type.txt \
  --vocals "low male baritone, detached delivery with whispered intensity on verses, soaring on chorus" \
  --bpm 85 \
  --key "C minor" \
  --out "$OUTDIR/prompt-detailed.mp3" \
  --quiet 2>&1 && echo "OK: detailed" || echo "FAIL: detailed"
sleep 12

echo ""
echo "=== EXPERIMENT D: New Impossible Genres ==="

echo "--- D1: Free Jazz Balkan Brass ---"
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
  --out "$OUTDIR/66-free-jazz-balkan-brass.mp3" \
  --quiet 2>&1 && echo "OK: balkan" || echo "FAIL: balkan"
sleep 12

echo "--- D2: Ambient Blackgaze Dub ---"
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
  --out "$OUTDIR/67-ambient-blackgaze-dub.mp3" \
  --quiet 2>&1 && echo "OK: blackgaze" || echo "FAIL: blackgaze"
sleep 12

echo "--- D3: Microtone Gamelan Techno ---"
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
  --out "$OUTDIR/68-microtone-gamelan-techno.mp3" \
  --quiet 2>&1 && echo "OK: gamelan" || echo "FAIL: gamelan"
sleep 12

echo ""
echo "=== EXPERIMENT E: Cover Chain Link 4 ==="
echo "Chiptune cover of shoegaze cover of dub techno cover of cool jazz original"

mmx music cover \
  --prompt "8-bit chiptune, NES-era video game music, square wave synths, simple drum machine, cheerful bleeps" \
  --audio-file mmx-session28/62-the-tensor-shoegaze-cover-of-cover.mp3 \
  --out "$OUTDIR/69-tensor-chiptune-cover-chain4.mp3" \
  --quiet 2>&1 && echo "OK: chiptune cover" || echo "FAIL: chiptune cover"

echo ""
echo "=== SESSION 29b COMPLETE ==="
echo "Files generated:"
ls -la "$OUTDIR"/*.mp3 2>/dev/null || echo "No tracks"
echo ""
echo "Sizes:"
du -sh "$OUTDIR" 2>/dev/null
