#!/bin/bash
# SongForge Session 27 — Generation Script
# Run after 2:00 AM AKST quota reset
# One at a time to avoid SIGKILLs

set -e
cd /home/eileen/projects/ai-writings/music

echo "=== Track 51: Seed Reproducibility Test B ==="
mmx music generate \
  --prompt "Minimalist electronic, Philip Glass arpeggios, cold crystalline synths" \
  --instrumental \
  --key "A minor" --bpm 80 \
  --seed 42 \
  --out "51-seed-test-b.mp3" \
  --quiet --non-interactive
echo "Track 51 done"

echo "=== Track 52: The Unused Variable (Structured Lyrics) ==="
mmx music generate \
  --prompt "Folk rock, acoustic guitar, warm male vocals, narrative, bittersweet" \
  --lyrics-file lyrics-the-unused-variable-m3.txt \
  --key "A minor" --bpm 72 \
  --out "52-the-unused-variable-structured.mp3" \
  --quiet --non-interactive
echo "Track 52 done"

echo "=== Track 53: The Unused Variable (Free Verse) ==="
mmx music generate \
  --prompt "Folk rock, acoustic guitar, warm male vocals, narrative, bittersweet" \
  --lyrics-file lyrics-the-unused-variable-freeverse.txt \
  --key "A minor" --bpm 72 \
  --out "53-the-unused-variable-freeverse.mp3" \
  --quiet --non-interactive
echo "Track 53 done"

echo "=== Comparing seed tracks ==="
SIZE_A=$(stat -c%s 50-seed-test-a.mp3)
SIZE_B=$(stat -c%s 51-seed-test-b.mp3)
echo "Track A: $SIZE_A bytes"
echo "Track B: $SIZE_B bytes"
if [ "$SIZE_A" -eq "$SIZE_B" ]; then
  echo "IDENTICAL SIZE — checking md5sum"
  MD5_A=$(md5sum 50-seed-test-a.mp3 | awk '{print $1}')
  MD5_B=$(md5sum 51-seed-test-b.mp3 | awk '{print $1}')
  echo "MD5 A: $MD5_A"
  echo "MD5 B: $MD5_B"
  if [ "$MD5_A" = "$MD5_B" ]; then
    echo "IDENTICAL CONTENT — seed is deterministic!"
  else
    echo "SAME SIZE, DIFFERENT CONTENT — seed constrains length but not content"
  fi
else
  DIFF=$((SIZE_A - SIZE_B))
  DIFF_PCT=$(echo "scale=1; $DIFF * 100 / $SIZE_A" | bc)
  echo "DIFFERENT SIZE — difference: $DIFF bytes ($DIFF_PCT%)"
  echo "Seed is NOT deterministic"
fi

echo "=== Comparing lyricist tracks ==="
SIZE_S=$(stat -c%s 52-the-unused-variable-structured.mp3)
SIZE_F=$(stat -c%s 53-the-unused-variable-freeverse.mp3)
echo "Structured: $SIZE_S bytes"
echo "Free verse: $SIZE_F bytes"
DIFF_PCT=$(echo "scale=1; ($SIZE_S - $SIZE_F) * 100 / $SIZE_F" | bc)
echo "Difference: $DIFF_PCT%"

echo "=== All done ==="
