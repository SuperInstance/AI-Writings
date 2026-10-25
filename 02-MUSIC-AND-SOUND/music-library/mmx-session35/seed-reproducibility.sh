#!/bin/bash
# Session 35: Seed Reproducibility Study
# Question: Is the cover model deterministic with the same seed?
# Method: Same prompt + same audio + same seed = 3 identical runs
# If seeds work, all 3 should produce identical files (same MD5)

cd /home/eileen/projects/ai-writings/music/mmx-session35

echo "=== Seed Reproducibility Study ==="
echo "Using cover model (which supports --seed)"
echo "Start: $(date)"

# Use the cavern-ocean track as source
SOURCE="../mmx-session34/p1-cavern-ocean.mp3"
PROMPT="Lo-fi indie folk, fingerpicked acoustic guitar, warm female vocal, gentle, intimate"

for SEED in 42 42 42 100 100 100 999 999 999; do
  RUN=$(ls seed-${SEED}-*.mp3 2>/dev/null | wc -l)
  OUT="seed-${SEED}-run${RUN}.mp3"
  echo -n "  Seed $SEED, run $RUN... "
  if mmx music cover \
    --prompt "$PROMPT" \
    --audio-file "$SOURCE" \
    --seed "$SEED" \
    --out "$OUT" \
    --quiet 2>/dev/null; then
    MD5=$(md5sum "$OUT" | awk '{print $1}')
    SIZE=$(stat -c%s "$OUT")
    echo "✓ ${SIZE} bytes, md5=${MD5:0:16}"
  else
    echo "✗ FAILED (likely quota)"
    break
  fi
done

echo ""
echo "=== Verification ==="
echo "If seeds work, runs with the same seed should have identical md5sums:"
for SEED in 42 100 999; do
  echo "  Seed $SEED:"
  md5sum seed-${SEED}-*.mp3 2>/dev/null | awk '{print "    " $1 " " $2}'
done

echo "=== Complete: $(date) ==="
