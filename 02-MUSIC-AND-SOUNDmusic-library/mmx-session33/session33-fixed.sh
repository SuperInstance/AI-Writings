#!/bin/bash
# Session 33 - FIXED Generation Script
# Removed unsupported flags: --yes, --seed (not available on music generate)
# Removed set -e to continue on errors

cd /home/eileen/projects/ai-writings/music/mmx-session33
OUTDIR="."

echo "=== Session 33 Generation (FIXED) ==="
echo "Start: $(date)"
echo ""

# EXPERIMENT 1: Negative Space
echo "--- Experiment 1: Negative Space ---"

mmx music generate \
  --prompt "A pop song with absolutely no percussion, no drums, no hi-hats, no beats — only melody and harmony carrying the rhythm. Piano, strings, and voice only. The absence of drums is the statement." \
  --lyrics-optimizer \
  --bpm 90 \
  --key "F major" \
  --out "${OUTDIR}/neg-01-no-drums.mp3" \
  --quiet && echo "  ✓ neg-01-no-drums.mp3 ($(stat -c%s ${OUTDIR}/neg-01-no-drums.mp3 2>/dev/null) bytes)" || echo "  ✗ neg-01 FAILED"

mmx music generate \
  --prompt "A song with no melody — only rhythm, texture, and spoken word. Percussion and bass drive everything. The voice speaks rather than sings. No tuneful notes from any instrument. Pure rhythm and texture." \
  --lyrics-optimizer \
  --bpm 110 \
  --key "E minor" \
  --out "${OUTDIR}/neg-02-no-melody.mp3" \
  --quiet && echo "  ✓ neg-02-no-melody.mp3 ($(stat -c%s ${OUTDIR}/neg-02-no-melody.mp3 2>/dev/null) bytes)" || echo "  ✗ neg-02 FAILED"

mmx music generate \
  --prompt "A song built on a suspended chord that never resolves. The harmony hangs eternally on the edge of resolution but always pulls away. The listener waits for a cadence that never comes. Tension without release. Jazz-influenced, dreamlike, unsettling." \
  --lyrics-optimizer \
  --bpm 75 \
  --key "G major" \
  --out "${OUTDIR}/neg-03-never-resolves.mp3" \
  --quiet && echo "  ✓ neg-03-never-resolves.mp3 ($(stat -c%s ${OUTDIR}/neg-03-never-resolves.mp3 2>/dev/null) bytes)" || echo "  ✗ neg-03 FAILED"

mmx music generate \
  --prompt "A minimalist composition where silence is the primary instrument. Long pauses between phrases. The music is defined by what isn't played. Each note appears alone in a vast empty space. John Cage meets Arvo Pärt. The rests are more important than the notes." \
  --lyrics-optimizer \
  --bpm 60 \
  --key "B minor" \
  --out "${OUTDIR}/neg-04-silence-as-instrument.mp3" \
  --quiet && echo "  ✓ neg-04-silence-as-instrument.mp3 ($(stat -c%s ${OUTDIR}/neg-04-silence-as-instrument.mp3 2>/dev/null) bytes)" || echo "  ✗ neg-04 FAILED"

mmx music generate \
  --prompt "Upbeat, cheerful, sunny indie pop about losing someone you love. The music is bright and warm but the lyrics are devastating. The contradiction is the point. 1960s jangle pop instrumentation, handclaps, harmonies, murder on the dance floor energy." \
  --lyrics-optimizer \
  --bpm 128 \
  --key "C major" \
  --out "${OUTDIR}/neg-05-happy-grief.mp3" \
  --quiet && echo "  ✓ neg-05-happy-grief.mp3 ($(stat -c%s ${OUTDIR}/neg-05-happy-grief.mp3 2>/dev/null) bytes)" || echo "  ✗ neg-05 FAILED"

# EXPERIMENT 2: Impossible Genres #17-20
echo ""
echo "--- Experiment 2: Impossible Genres ---"

mmx music generate \
  --prompt "Microtonal gamelan drone music — detuned bronze bells, shimmering overtones, non-Western tuning systems, ritualistic atmosphere, no clear downbeat. Balinese gamelan meets Sunn O))) meets Arvo Pärt. Sacred and strange." \
  --lyrics-optimizer \
  --bpm 50 \
  --out "${OUTDIR}/imposs-17-gamelan-drone.mp3" \
  --quiet && echo "  ✓ imposs-17-gamelan-drone.mp3 ($(stat -c%s ${OUTDIR}/imposs-17-gamelan-drone.mp3 2>/dev/null) bytes)" || echo "  ✗ imposs-17 FAILED"

mmx music generate \
  --prompt "Blackgaze dub — the blast beats and tremolo guitar of black metal meet the deep bass and echo of Jamaican dub reggae. Wall of sound meets the abyss. Shoegaze guitar wash over massive bass drops. Impossible and overwhelming." \
  --lyrics-optimizer \
  --bpm 140 \
  --out "${OUTDIR}/imposs-18-blackgaze-dub.mp3" \
  --quiet && echo "  ✓ imposs-18-blackgaze-dub.mp3 ($(stat -c%s ${OUTDIR}/imposs-18-blackgaze-dub.mp3 2>/dev/null) bytes)" || echo "  ✗ imposs-18 FAILED"

mmx music generate \
  --prompt "Balkan brass band playing math rock — odd time signatures, trumpets and tubas playing complex interlocking patterns in 7/8 and 11/8, joyful and chaotic, wedding music for calculus students. Deviczelk meets Don Caballero." \
  --lyrics-optimizer \
  --bpm 175 \
  --out "${OUTDIR}/imposs-19-balkan-math.mp3" \
  --quiet && echo "  ✓ imposs-19-balkan-math.mp3 ($(stat -c%s ${OUTDIR}/imposs-19-balkan-math.mp3 2>/dev/null) bytes)" || echo "  ✗ imposs-19 FAILED"

mmx music generate \
  --prompt "Ambient bluegrass — banjo and mandolin processed through infinite reverb and delay until they become clouds of sound. Appalachian mountain music dissolved into Brian Eno atmosphere. The fog rolls over the Smoky Mountains and swallows the fiddle." \
  --lyrics-optimizer \
  --bpm 65 \
  --out "${OUTDIR}/imposs-20-ambient-bluegrass.mp3" \
  --quiet && echo "  ✓ imposs-20-ambient-bluegrass.mp3 ($(stat -c%s ${OUTDIR}/imposs-20-ambient-bluegrass.mp3 2>/dev/null) bytes)" || echo "  ✗ imposs-20 FAILED"

# EXPERIMENT 3: BPM Duration Control Study
echo ""
echo "--- Experiment 3: BPM Duration Control ---"

DUR_LYRICS="[Verse 1]
The clock on the wall doesn't tick anymore
It hums like a wire it hums like a door
The frequency shifts and the room changes key
I'm tuned to the station that nobody sees

[Chorus]
Time is a spiral time is a wire
Time is the shape of the music's desire
Every revolution brings us back near
But never quite here never quite here"

for bpm in 60 100 140; do
  mmx music generate \
    --prompt "Indie folk rock, acoustic guitar, warm male vocal, piano accents, steady driving rhythm" \
    --lyrics "$DUR_LYRICS" \
    --bpm $bpm \
    --key "G major" \
    --out "${OUTDIR}/dur-bpm-${bpm}.mp3" \
    --quiet && echo "  ✓ dur-bpm-${bpm}.mp3 ($(stat -c%s ${OUTDIR}/dur-bpm-${bpm}.mp3 2>/dev/null) bytes)" || echo "  ✗ dur-bpm-${bpm} FAILED"
  sleep 1
done

# EXPERIMENT 4: Contradictory Emotions
echo ""
echo "--- Experiment 4: Contradictory Emotions ---"

mmx music generate \
  --prompt "Simultaneously the happiest and saddest song ever written. Major key, upbeat tempo, joyful melody, but with a deep undercurrent of grief and loss. The two emotions coexist without resolving. Like dancing at a funeral." \
  --lyrics-optimizer \
  --bpm 120 \
  --key "A major" \
  --out "${OUTDIR}/contra-01-happy-sad.mp3" \
  --quiet && echo "  ✓ contra-01-happy-sad.mp3" || echo "  ✗ contra-01 FAILED"

mmx music generate \
  --prompt "Energetic lethargy — frantic percussion and blazing tempos paired with deadpan exhausted vocals and lyrics about not wanting to get out of bed. The music races while the voice sleeps. Punk rock played by someone who can barely stay awake." \
  --lyrics-optimizer \
  --bpm 170 \
  --key "F sharp minor" \
  --out "${OUTDIR}/contra-02-fast-tired.mp3" \
  --quiet && echo "  ✓ contra-02-fast-tired.mp3" || echo "  ✗ contra-02 FAILED"

mmx music generate \
  --prompt "A crowded room that feels completely alone. Dense, layered production with dozens of instruments playing at once, yet the overall effect is isolation and emptiness. Wall-of-sound loneliness. Phil Spector meets Elliott Smith." \
  --lyrics-optimizer \
  --bpm 88 \
  --key "D minor" \
  --out "${OUTDIR}/contra-03-crowded-alone.mp3" \
  --quiet && echo "  ✓ contra-03-crowded-alone.mp3" || echo "  ✗ contra-03 FAILED"

# EXPERIMENT 5: Cover Chain
echo ""
echo "--- Experiment 5: Cover Chain Link 5 ---"

SOURCE="../mmx-session32/m3-04-deep-sea-bossa-vaporwave.mp3"
if [ -f "$SOURCE" ]; then
  mmx music cover \
    --prompt "Solo piano, minimalist, classical, slow, melancholic, no vocals" \
    --audio-file "$SOURCE" \
    --out "${OUTDIR}/cover-01-piano.mp3" \
    --quiet && echo "  ✓ cover-01-piano.mp3" || echo "  ✗ cover-01 FAILED"

  mmx music cover \
    --prompt "Dark industrial metal, distorted guitars, mechanical drums, aggressive vocals, Nine Inch Nails meets Ministry" \
    --audio-file "$SOURCE" \
    --out "${OUTDIR}/cover-02-industrial.mp3" \
    --quiet && echo "  ✓ cover-02-industrial.mp3" || echo "  ✗ cover-02 FAILED"

  mmx music cover \
    --prompt "A capella, layered voices, choir, no instruments, Gregorian chant meets Bobby McFerrin" \
    --audio-file "$SOURCE" \
    --out "${OUTDIR}/cover-03-acapella.mp3" \
    --quiet && echo "  ✓ cover-03-acapella.mp3" || echo "  ✗ cover-03 FAILED"
else
  echo "  Source file not found, skipping cover chain"
fi

echo ""
echo "=== Session 33 Complete ==="
echo "End: $(date)"
