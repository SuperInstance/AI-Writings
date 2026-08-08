#!/bin/bash
# SongForge Session 11+ Generation Script
# Run after weekly quota resets (Sunday 00:00 UTC = Saturday ~4pm AKST)
# This script generates all queued tracks sequentially with proper delays

set -e

MUSIC_DIR="/home/eileen/projects/ai-writings/music"
DELAY=90  # seconds between generations

echo "=== SongForge Session 11+ Generation ==="
echo "Starting at $(date)"
echo ""

# Check quota first
echo "Checking quota..."
mmx quota show --quiet 2>&1 | head -5
echo ""

# --- QUEUED TRACKS (Priority 1) ---

echo "[1/5] Generating: The Proof Is the Performance"
mmx music generate \
  --prompt "Orchestral cinematic, choir, strings, brass" \
  --lyrics-file "$MUSIC_DIR/lyrics-proof-performance.txt" \
  --vocals "mixed choir, powerful, from whisper to full" \
  --key "D minor" \
  --bpm 75 \
  --out "$MUSIC_DIR/36-the-proof-is-the-performance.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 36"
echo "Done: $(date)"
sleep $DELAY

echo "[2/5] Generating: The Ouroboros Sings"
mmx music generate \
  --prompt "Art rock, progressive, layered vocals" \
  --lyrics-file "$MUSIC_DIR/lyrics-ouroboros-sings-trimmed.txt" \
  --vocals "warm male baritone, layered harmonies" \
  --key "A minor" \
  --bpm 88 \
  --out "$MUSIC_DIR/37-the-ouroboros-sings.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 37"
echo "Done: $(date)"
sleep $DELAY

echo "[3/5] Generating: The Session Listens Back"
mmx music generate \
  --prompt "Ambient indie, warm guitars, hazy" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-session-listens-back.txt" \
  --vocals "ethereal female alto, distant" \
  --key "C major" \
  --bpm 68 \
  --out "$MUSIC_DIR/38-the-session-listens-back.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 38"
echo "Done: $(date)"
sleep $DELAY

echo "[4/5] Generating: The Cadence Caller Listens"
mmx music generate \
  --prompt "Indie folk, fingerpicked guitar, subtle drums" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-cadence-caller.txt" \
  --vocals "warm female alto, intimate" \
  --key "A minor" \
  --bpm 78 \
  --out "$MUSIC_DIR/39-the-cadence-caller.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 39"
echo "Done: $(date)"
sleep $DELAY

echo "[5/5] Generating: The Fifth's Funeral"
mmx music generate \
  --prompt "Dramatic orchestral, grand, powerful" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-fifths-funeral-trimmed.txt" \
  --vocals "warm male baritone, theatrical, commanding" \
  --key "D minor" \
  --bpm 65 \
  --out "$MUSIC_DIR/40-the-fifths-funeral.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 40"
echo "Done: $(date)"
sleep $DELAY

# --- M3 LYRICIST COMPARISON (Priority 2) ---

echo "[6] Generating M3 lyrics for Cadence Caller comparison"
mmx text chat \
  --system "You are a skilled lyricist who writes singable, emotionally vivid song lyrics with concrete imagery and recursive metaphors." \
  --message "user:Write song lyrics (2 verses, 1 chorus, 1 bridge, 1 outro — under 1100 characters total) inspired by this concept: The Cadence Caller Listens — the idea that the best leaders don't dictate rhythm, they discover it. A marching formation already has a rhythm before the cadence caller opens his mouth. A jazz band already has a pocket before anyone counts off. The leader is a mirror, not a clock. Include structural tags. Singable meter. Avoid cliches." \
  --temperature 0.93 \
  --max-tokens 2048 \
  --output json --quiet 2>&1 | python3 -c "import sys,json; print(json.load(sys.stdin).get('content',''))" > "$MUSIC_DIR/lyrics-cadence-m3.txt" 2>&1 || echo "FAILED: M3 lyrics"
echo "Done: $(date)"

echo ""
echo "=== Generation Complete ==="
echo "Finished at $(date)"
echo ""
echo "Track sizes:"
ls -lh "$MUSIC_DIR"/3[6-9]-*.mp3 "$MUSIC_DIR"/40-*.mp3 2>/dev/null || echo "No new tracks found"
echo ""
echo "Quota remaining:"
mmx quota show --quiet 2>&1 | head -5
