#!/bin/bash
# Session 35: BPM Duration Control Study
# Question: Is BPM the primary duration lever? Does specifying BPM override 
# the model's "natural" 3-minute length?
# 6 tracks at BPM 40, 60, 80, 100, 120, 140, 160, 180

set -u
cd /home/eileen/projects/ai-writings/music/mmx-session35

echo "=== BPM Duration Control Study ==="
echo "Start: $(date)"

for BPM in 40 60 80 100 120 140 160 180; do
  echo -n "  BPM $BPM... "
  if mmx music generate \
    --prompt "Electronic instrumental, steady pulse, atmospheric pads, arpeggiated synthesizer" \
    --instrumental \
    --bpm "$BPM" \
    --out "bpm-${BPM}.mp3" \
    --quiet 2>/dev/null; then
    SIZE=$(stat -c%s "bpm-${BPM}.mp3" 2>/dev/null)
    DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "bpm-${BPM}.mp3" 2>/dev/null || echo "unknown")
    echo "✓ ${SIZE} bytes, ${DURATION}s"
  else
    echo "✗ FAILED (likely quota)"
    break
  fi
done

echo "=== Complete: $(date) ==="
