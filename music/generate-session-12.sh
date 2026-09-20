#!/bin/bash
# SongForge Session 12 Generation Script
# PROMPT STRUCTURE EXPERIMENT + NEW CORPUS ADAPTATIONS
#
# This session tests a NEW experimental dimension: prompt complexity.
# Same concept, same lyrics, same musical parameters — but three different
# prompt structures:
#   A) Simple:   "Classical, orchestral"
#   B) Rich:     "Late Romantic classical, full orchestra, building from whispered strings to full brass, emotional crescendo"
#   C) Structural: Uses all structured flags (--genre, --mood, --instruments, --tempo, --structure)
#
# Plus new corpus adaptations: The Conductor Has No Instrument, The Pocket Is a Place
# Plus the ongoing lyricist comparison (Granite vs Llama vs Agent)
#
# RUN AFTER QUOTA RESETS (Sunday 00:00 UTC = Saturday ~4pm AKST)

set -e

MUSIC_DIR="/home/eileen/projects/ai-writings/music"
DELAY=90

echo "=== SongForge Session 12 Generation ==="
echo "Starting at $(date)"
echo ""

# ─── CHECK QUOTA ───
echo "Checking quota..."
RESULT=$(mmx quota show --quiet --output json --non-interactive 2>&1)
echo "$RESULT" | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    for m in d.get('model_remains',[]):
        if m.get('model_name')=='general':
            w=m.get('current_weekly_remaining_percent',0)
            print(f'Weekly: {w}%')
            if w < 5:
                print('ERROR: Weekly quota too low. Aborting.')
                sys.exit(1)
            else:
                print('Quota OK. Proceeding.')
except Exception as e:
    print(f'Warning: could not parse quota: {e}')
"
echo ""

# ─── PART 1: CATCH-UP FROM SESSION 11 (8 queued tracks) ───
# These are the tracks that were queued but couldn't generate due to quota

echo "=== PART 1: Session 11 Queued Tracks ==="
echo ""

echo "[1/14] The Proof Is the Performance"
mmx music generate \
  --prompt "Orchestral cinematic, choir, strings, brass" \
  --lyrics-file "$MUSIC_DIR/lyrics-proof-performance.txt" \
  --vocals "mixed choir, powerful, from whisper to full" \
  --key "D minor" --bpm 75 \
  --out "$MUSIC_DIR/36-the-proof-is-the-performance.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 36"
sleep $DELAY

echo "[2/14] The Ouroboros Sings"
mmx music generate \
  --prompt "Art rock, progressive, layered vocals" \
  --lyrics-file "$MUSIC_DIR/lyrics-ouroboros-sings-trimmed.txt" \
  --vocals "warm male baritone, layered harmonies" \
  --key "A minor" --bpm 88 \
  --out "$MUSIC_DIR/37-the-ouroboros-sings.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 37"
sleep $DELAY

echo "[3/14] The Session Listens Back"
mmx music generate \
  --prompt "Ambient indie, warm guitars, hazy" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-session-listens-back.txt" \
  --vocals "ethereal female alto, distant" \
  --key "C major" --bpm 68 \
  --out "$MUSIC_DIR/38-the-session-listens-back.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 38"
sleep $DELAY

echo "[4/14] The Cadence Caller Listens"
mmx music generate \
  --prompt "Indie folk, fingerpicked guitar, subtle drums" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-cadence-caller.txt" \
  --vocals "warm female alto, intimate" \
  --key "A minor" --bpm 78 \
  --out "$MUSIC_DIR/39-the-cadence-caller.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 39"
sleep $DELAY

echo "[5/14] The Fifth's Funeral"
mmx music generate \
  --prompt "Dramatic orchestral, grand, powerful" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-fifths-funeral-trimmed.txt" \
  --vocals "warm male baritone, theatrical, commanding" \
  --key "D minor" --bpm 65 \
  --out "$MUSIC_DIR/40-the-fifths-funeral.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 40"
sleep $DELAY

echo "[6/14] The Metronome Is the Constraint"
mmx music generate \
  --prompt "Indie rock, driving drums, steady rhythm" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-metronome-trimmed.txt" \
  --vocals "warm male baritone, confident, rhythmic" \
  --key "F major" --bpm 120 \
  --out "$MUSIC_DIR/41-the-metronome.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 41"
sleep $DELAY

echo "[7/14] The Tensor Is the Score"
mmx music generate \
  --prompt "Cool jazz, spacious trumpet, upright bass" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-tensor-trimmed.txt" \
  --vocals "warm female alto, smoky, intimate" \
  --key "D minor" --bpm 65 \
  --out "$MUSIC_DIR/42-the-tensor.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 42"
sleep $DELAY

echo "[8/14] The Chip That Sang"
mmx music generate \
  --prompt "Electronic ambient, analog synths, cold and beautiful" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-chip-that-sang-trimmed.txt" \
  --vocals "ethereal male tenor, distant, processed" \
  --key "A minor" --bpm 60 \
  --out "$MUSIC_DIR/43-the-chip-that-sang.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 43"
sleep $DELAY

# ─── PART 2: NEW CORPUS ADAPTATIONS ───
echo ""
echo "=== PART 2: New Corpus Adaptations ==="
echo ""

echo "[9/14] The Conductor Has No Instrument"
mmx music generate \
  --prompt "Classical, orchestral, minimalist, building from silence to full symphony" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-conductor-trimmed.txt" \
  --vocals "warm male baritone, theatrical, intimate then powerful" \
  --key "D major" --bpm 70 \
  --out "$MUSIC_DIR/44-the-conductor-has-no-instrument.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 44"
sleep $DELAY

echo "[10/14] The Pocket Is a Place"
mmx music generate \
  --prompt "Neo-soul, warm bass groove, electric piano, smooth" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-pocket-trimmed.txt" \
  --vocals "warm female alto, intimate, settled" \
  --key "E minor" --bpm 85 \
  --out "$MUSIC_DIR/45-the-pocket-is-a-place.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 45"
sleep $DELAY

# ─── PART 3: PROMPT STRUCTURE EXPERIMENT ───
# Same lyrics, same key, same BPM — but THREE different prompt complexity levels
echo ""
echo "=== PART 3: Prompt Structure Experiment ==="
echo "Same song (The Conductor), three prompt complexity levels"
echo ""

echo "[11/14] Conductor — SIMPLE prompt"
mmx music generate \
  --prompt "Classical orchestral" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-conductor-trimmed.txt" \
  --vocals "male baritone" \
  --key "D major" --bpm 70 \
  --out "$MUSIC_DIR/46-conductor-prompt-simple.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 46"
sleep $DELAY

echo "[12/14] Conductor — RICH prompt"
mmx music generate \
  --prompt "Late Romantic classical, full symphony orchestra, building from whispered strings through woodwind solos to full brass and percussion crescendo, emotional, cinematic, intimate then overwhelming" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-conductor-trimmed.txt" \
  --vocals "warm male baritone, intimate and theatrical, from whispered to commanding" \
  --key "D major" --bpm 70 \
  --out "$MUSIC_DIR/47-conductor-prompt-rich.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 47"
sleep $DELAY

echo "[13/14] Conductor — STRUCTURED prompt (all flags)"
mmx music generate \
  --prompt "Classical orchestral, building tension, intimate to powerful" \
  --genre "classical" \
  --mood "contemplative, building, triumphant" \
  --instruments "strings, woodwinds, brass, timpani" \
  --tempo "slow to moderate" \
  --structure "verse-chorus-verse-bridge-outro" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-conductor-trimmed.txt" \
  --vocals "warm male baritone, theatrical" \
  --key "D major" --bpm 70 \
  --references "similar to Philip Glass, Max Richter" \
  --out "$MUSIC_DIR/48-conductor-prompt-structured.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 48"
sleep $DELAY

# ─── PART 4: WILD CARD — UNEXPECTED GENRE FOR CONDUCTOR ───
echo ""
echo "=== PART 4: Wild Card Genre ==="
echo ""

echo "[14/14] The Conductor — DUB/REGGAE wild card"
mmx music generate \
  --prompt "Dub reggae, heavy bass, spring reverb echoes, slow groove, spacious" \
  --lyrics-file "$MUSIC_DIR/lyrics-the-conductor-trimmed.txt" \
  --vocals "warm male baritone, laid back, distant" \
  --key "D major" --bpm 70 \
  --out "$MUSIC_DIR/49-conductor-dub-reggae.mp3" \
  --quiet --non-interactive 2>&1 || echo "FAILED: track 49"

# ─── SUMMARY ───
echo ""
echo "=== Session 12 Generation Complete ==="
echo "Finished at $(date)"
echo ""
echo "New tracks this session:"
ls -lh "$MUSIC_DIR"/3[6-9]-*.mp3 "$MUSIC_DIR"/4[0-9]-*.mp3 2>/dev/null || echo "No new tracks"
echo ""
echo "Total tracks:"
ls "$MUSIC_DIR"/*.mp3 2>/dev/null | wc -l
echo ""
echo "Total project size:"
du -sh "$MUSIC_DIR"/
echo ""
echo "=== PROMPT STRUCTURE EXPERIMENT ==="
echo "Compare files 46 (simple), 47 (rich), 48 (structured), 49 (dub wild card)"
echo "All use identical lyrics, key, BPM. Only the prompt varies."
echo "Hypothesis: Rich prompt (47) will produce the largest/most detailed track."
echo "            Structured prompt (48) may produce the most conventional track."
echo "            Simple prompt (46) may surprise — less constraint = more freedom."
echo "            Wild card (49) tests whether lyrics override genre completely."