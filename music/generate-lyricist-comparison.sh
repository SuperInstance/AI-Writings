#!/bin/bash
# SongForge Session 11 — Lyricist Comparison Experiment
# Three models, same concept, same musical parameters
# Run after weekly quota resets

set -e
MUSIC_DIR="/home/eileen/projects/ai-writings/music"
DELAY=90

echo "=== Lyricist Comparison Experiment ==="
echo "Starting at $(date)"

# Already have agent-written lyrics for Cadence Caller: lyrics-the-cadence-caller.txt
# Need M3 lyrics for the same concept
echo "[1] Generating M3 lyrics for Cadence Caller..."
mmx text chat \
  --system "You are a skilled lyricist who writes singable, emotionally vivid song lyrics with concrete imagery and recursive metaphors." \
  --message "user:Write song lyrics (2 verses, 1 chorus, 1 bridge, 1 outro — under 1100 characters total) inspired by this concept: The Cadence Caller Listens — the idea that the best leaders don't dictate rhythm, they discover it. A marching formation already has a rhythm before the cadence caller opens his mouth. A jazz band already has a pocket before anyone counts off. The leader is a mirror, not a clock. Include structural tags. Singable meter. Avoid cliches." \
  --temperature 0.93 \
  --max-tokens 2048 \
  --output json --quiet --non-interactive 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('content',''))" > "$MUSIC_DIR/lyrics-cadence-m3.txt" 2>&1 || echo "FAILED: M3 lyrics"

echo "[2] Generating: Cadence Caller (M3 lyrics)"
mmx music generate \
  --prompt "Indie folk, fingerpicked guitar, subtle drums" \
  --lyrics-file "$MUSIC_DIR/lyrics-cadence-m3.txt" \
  --vocals "warm female alto, intimate" \
  --key "A minor" --bpm 78 \
  --out "$MUSIC_DIR/44-cadence-m3.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 44"
echo "Done: $(date)"
sleep $DELAY

echo "[3] Generating: Cadence Caller (Granite lyrics)"
mmx music generate \
  --prompt "Indie folk, fingerpicked guitar, subtle drums" \
  --lyrics-file "$MUSIC_DIR/lyrics-cadence-granite.txt" \
  --vocals "warm female alto, intimate" \
  --key "A minor" --bpm 78 \
  --out "$MUSIC_DIR/45-cadence-granite.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 45"
echo "Done: $(date)"
sleep $DELAY

echo "[4] Generating: Cadence Caller (Llama lyrics)"
mmx music generate \
  --prompt "Indie folk, fingerpicked guitar, subtle drums" \
  --lyrics-file "$MUSIC_DIR/lyrics-cadence-llama.txt" \
  --vocals "warm female alto, intimate" \
  --key "A minor" --bpm 78 \
  --out "$MUSIC_DIR/46-cadence-llama.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 46"
echo "Done: $(date)"
sleep $DELAY

echo "[5] Generating: Cadence Caller (Agent lyrics — already queued as track 39)"
echo "Skipping — track 39 already uses agent-written lyrics"

echo ""
echo "=== Comparison Results ==="
echo "M3 lyrics size: $(wc -c < "$MUSIC_DIR/lyrics-cadence-m3.txt") chars"
echo "Granite lyrics size: $(wc -c < "$MUSIC_DIR/lyrics-cadence-granite.txt") chars"
echo "Llama lyrics size: $(wc -c < "$MUSIC_DIR/lyrics-cadence-llama.txt") chars"
echo "Agent lyrics size: $(wc -c < "$MUSIC_DIR/lyrics-the-cadence-caller.txt") chars"
echo ""
echo "Track sizes:"
ls -lh "$MUSIC_DIR"/4[4-6]-cadence-*.mp3 2>/dev/null || echo "No tracks generated"
