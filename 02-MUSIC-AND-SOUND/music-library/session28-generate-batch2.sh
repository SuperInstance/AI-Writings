#!/bin/bash
set -e
cd /home/eileen/projects/ai-writings/music

echo "=== Track 64: Gagaku Drum and Bass ==="
mmx music generate \
  --prompt "Impossible fusion: ancient Japanese gagaku court music with sho, hichiriki, and biwa, blended with liquid drum and bass at 170 BPM, atmospheric pads, rolling amens, deep sub-bass" \
  --lyrics "[Verse]
The court of the emperor is a rave at 170 BPM
The sho breathes and the amens break
The hichiriki sings the imperial song
The biwa plucks the history of the empire in 16 bars

[Chorus]
The dragon descends through the rolling snares
The cherry blossoms fall in half-time
The court bows, the bass bows lower
The emperor's heart is a kick drum in 4/4" \
  --vocals "ethereal female soprano with traditional Japanese phrasing" \
  --bpm 170 \
  --key "E minor" \
  --out mmx-session28/64-gagaku-drum-and-bass.mp3 \
  --quiet
echo "Track 64 done"

echo "=== Track 65: The Compiler Dreams in Type (temp 0.7 prompt variant) ==="
mmx music generate \
  --prompt "Minimalist dark wave, cold analog synths, drum machine, brooding atmospheric, like Depeche Mode meets Philip Glass" \
  --lyrics-file lyrics-the-compiler-dreams-in-type.txt \
  --vocals "low male baritone, detached, whispered intensity" \
  --bpm 85 \
  --key "C minor" \
  --out mmx-session28/65-the-compiler-darkwave.mp3 \
  --quiet
echo "Track 65 done"

echo "=== Track 66: Cover chain link 4 - chiptune cover of shoegaze cover ==="
mmx music cover \
  --prompt "8-bit chiptune, NES-era video game music, square wave synths, simple drum machine, cheerful bleeps and bloops" \
  --audio-file mmx-session28/62-the-tensor-shoegaze-cover-of-cover.mp3 \
  --out mmx-session28/66-the-tensor-chiptune-cover-of-cover-of-cover.mp3 \
  --quiet
echo "Track 66 done"

echo "=== Track 67: New Orleans brass meets Nordic black metal ==="
mmx music generate \
  --prompt "Impossible fusion: joyful New Orleans brass band with tuba, trumpet, and snare, colliding with Nordic black metal tremolo guitar, blast beats, and shrieked vocals" \
  --lyrics "[Verse]
The second line marches through the frost
The trumpet breathes fire, the tuba is lost
In a forest of blast beats, the sousaphone screams
The jazz funeral meets the Norwegian dreams

[Chorus]
When the brass hits the ice, when the tremolo burns
When the procession meets the church of no returns
The joy and the fury are the same song
The dirge and the dance have been married all along" \
  --vocals "split: warm gospel tenor alternating with black metal shriek" \
  --bpm 130 \
  --key "B minor" \
  --out mmx-session28/67-brass-meets-black-metal.mp3 \
  --quiet
echo "Track 67 done"

echo "=== All done ==="
ls -la mmx-session28/
