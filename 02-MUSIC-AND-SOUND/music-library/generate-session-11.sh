#!/bin/bash
# SongForge Session 11 Generation Script
# Run after weekly quota resets (Sunday 00:00 UTC = Saturday ~4pm AKST)
# This script generates all queued tracks sequentially with proper delays

set -e

MUSIC_DIR="/home/eileen/projects/ai-writings/music"
DELAY=90  # seconds between generations

echo "=== SongForge Session 11 Generation ==="
echo "Starting at $(date)"
echo ""

# Check quota first
echo "Checking quota..."
mmx quota show --quiet --output json --non-interactive 2>&1 | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    for m in d.get('model_remains',[]):
        if m.get('model_name')=='general':
            w=m.get('current_weekly_remaining_percent',0)
            di=m.get('current_interval_remaining_percent',0)
            print(f'Weekly: {w}%  Daily: {di}%')
            if w < 5:
                print('ERROR: Weekly quota too low. Aborting.')
                sys.exit(1)
except: pass
"
echo ""

# --- QUEUED TRACKS FROM PREVIOUS SESSIONS ---

echo "[1/8] Generating: The Proof Is the Performance"
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

echo "[2/8] Generating: The Ouroboros Sings"
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

echo "[3/8] Generating: The Session Listens Back"
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

echo "[4/8] Generating: The Cadence Caller Listens"
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

echo "[5/8] Generating: The Fifth's Funeral"
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

# --- NEW CORPUS ADAPTATIONS (Session 11) ---

echo "[6/8] Generating: The Metronome Is the Constraint"
mmx music generate \
  --prompt "Indie rock, driving drums, steady rhythm" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-metronome-trimmed.txt" \
  --vocals "warm male baritone, confident, rhythmic" \
  --key "F major" \
  --bpm 120 \
  --out "$MUSIC_DIR/41-the-metronome.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 41"
echo "Done: $(date)"
sleep $DELAY

echo "[7/8] Generating: The Tensor Is the Score"
mmx music generate \
  --prompt "Cool jazz, spacious trumpet, upright bass" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-tensor-trimmed.txt" \
  --vocals "warm female alto, smoky, intimate" \
  --key "D minor" \
  --bpm 65 \
  --out "$MUSIC_DIR/42-the-tensor.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 42"
echo "Done: $(date)"
sleep $DELAY

echo "[8/8] Generating: The Chip That Sang"
mmx music generate \
  --prompt "Electronic ambient, analog synths, cold and beautiful" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-chip-that-sang-trimmed.txt" \
  --vocals "ethereal male tenor, distant, processed" \
  --key "A minor" \
  --bpm 60 \
  --out "$MUSIC_DIR/43-the-chip-that-sang.mp3" \
  --quiet --non-interactive --yes 2>&1 || echo "FAILED: track 43"
echo "Done: $(date)"

# --- SUMMARY ---
echo ""
echo "=== Generation Complete ==="
echo "Finished at $(date)"
echo ""
echo "New track sizes:"
ls -lh "$MUSIC_DIR"/3[6-9]-*.mp3 "$MUSIC_DIR"/4[0-3]-*.mp3 2>/dev/null || echo "No new tracks found"
echo ""
echo "Total tracks:"
ls "$MUSIC_DIR"/*.mp3 2>/dev/null | wc -l
echo ""
echo "Total project size:"
du -sh "$MUSIC_DIR"/
