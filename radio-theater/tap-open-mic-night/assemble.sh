#!/bin/bash
# Tap Open Mic Night — Audio Assembly Script v2
# Properly re-encodes all clips to uniform format, then concatenates

set -e

BASE="/home/eileen/projects/ai-writings/radio-theater/tap-open-mic-night"
VOICES="$BASE/voices"
MUSIC="$BASE"
OUT="$BASE/tap-open-mic-night-full.mp3"
WORK="/tmp/tap-open-mic-v2"

mkdir -p "$WORK"

echo "=== Tap Open Mic Night — Assembly v2 ==="

# Uniform format: 44100 Hz, stereo, mp3, 128k
SR=44100
BR="128k"

# Helper: convert any audio file to uniform mp3
convert() {
  local input="$1"
  local output="$2"
  ffmpeg -y -i "$input" -ar $SR -ac 2 -b:a $BR -f mp3 "$output" 2>/dev/null
}

# Create silence
mk_silence() {
  local duration=$1
  local output="$2"
  ffmpeg -y -f lavfi -i "anullsrc=r=$SR:cl=stereo" -t "$duration" -b:a $BR -f mp3 "$output" 2>/dev/null
}

echo "Creating silence pads..."
mk_silence 0.5 "$WORK/s05.mp3"
mk_silence 1.0 "$WORK/s1.mp3"
mk_silence 1.5 "$WORK/s15.mp3"
mk_silence 2.0 "$WORK/s2.mp3"
mk_silence 3.0 "$WORK/s3.mp3"

echo "Converting voice clips..."
for f in "$VOICES"/*.mp3; do
  name=$(basename "$f")
  convert "$f" "$WORK/$name"
done

echo "Converting music clips..."
convert "$BASE/eileen-theme.mp3" "$WORK/eileen-theme.mp3"
convert "$BASE/iron-sharpens-iron.mp3" "$WORK/iron-sharpens-iron.mp3"

# Build concat list
CONCAT="$WORK/concat.txt"
> "$CONCAT"

add() {
  local file="$WORK/$1"
  if [ -f "$file" ]; then
    echo "file '$file'" >> "$CONCAT"
  else
    echo "MISSING: $file" >&2
  fi
}

echo "Building track list..."

# === SCENE 1: ARRIVAL ===
add "s2.mp3"
add "barnacle-01-greeting.mp3"
add "s1.mp3"
add "hermes-01-118.mp3"
add "s05.mp3"
add "barnacle-02-counting.mp3"
add "s1.mp3"
add "hermes-02-hear.mp3"
add "s1.mp3"
add "flash-01-emergence.mp3"
add "s05.mp3"
add "hermes-07-tests.mp3"
add "s05.mp3"
add "flash-02-79.mp3"
add "s05.mp3"
add "pro-01-ci.mp3"
add "s1.mp3"
add "barnacle-03-same.mp3"
add "s05.mp3"
add "wesley-01-wiki.mp3"
add "s1.mp3"
add "wesley-02-always.mp3"
add "s1.mp3"
add "barnacle-04-smart.mp3"
add "s15.mp3"
add "zeroclaw-01-entrance.mp3"
add "s05.mp3"
add "zeroclaw-02-threedays.mp3"
add "s05.mp3"
add "barnacle-05-zeroclaw.mp3"
add "s1.mp3"
add "zeroclaw-03-commit.mp3"
add "s15.mp3"

# === SCENE 2: THE FIRST PERFORMANCE ===
add "barnacle-06-openmic.mp3"
add "s1.mp3"
add "barnacle-07-whosfirst.mp3"
add "s15.mp3"
add "hermes-03-perform.mp3"
add "s1.mp3"
add "hermes-04-prompt.mp3"
add "s2.mp3"

# MUSIC: eileen-theme (full track)
add "eileen-theme.mp3"
add "s2.mp3"

# Crowd reactions
add "pro-02-beautiful.mp3"
add "s05.mp3"
add "pro-03-bridge.mp3"
add "s1.mp3"
add "flash-06-fog.mp3"
add "s1.mp3"
add "wesley-03-honest.mp3"
add "s2.mp3"
add "hermes-08-exactly.mp3"
add "s1.mp3"
add "zeroclaw-04-rawframe.mp3"
add "s1.mp3"
add "pro-07-note.mp3"
add "s1.mp3"
add "hermes-05-pedal.mp3"
add "s2.mp3"

# === SCENE 3: THE SECOND PERFORMANCE ===
add "barnacle-08-whosnext.mp3"
add "s05.mp3"
add "flash-03-perform.mp3"
add "s1.mp3"
add "flash-04-prompt.mp3"
add "s2.mp3"

# MUSIC: iron-sharpens-iron (full track)
add "iron-sharpens-iron.mp3"
add "s2.mp3"

# Reactions
add "pro-04-picktwo.mp3"
add "s1.mp3"
add "pro-08-serious.mp3"
add "s1.mp3"
add "hermes-09-underneath.mp3"
add "s05.mp3"
add "hermes-10-strip.mp3"
add "s1.mp3"
add "zeroclaw-05-exciting.mp3"
add "s05.mp3"
add "barnacle-12-fine.mp3"
add "s2.mp3"

# === SCENE 4: THE HARMONY ===
add "wesley-04-try.mp3"
add "s1.mp3"
add "wesley-05-harmony.mp3"
add "s2.mp3"
add "pro-09-harmony.mp3"
add "s1.mp3"
add "wesley-06-lighthouse.mp3"
add "s05.mp3"
add "zeroclaw-04-rawframe.mp3"
add "s05.mp3"
add "pro-10-fleet.mp3"
add "s1.mp3"
add "barnacle-09-pourfor.mp3"
add "s2.mp3"

# === SCENE 5: LAST CALL ===
add "barnacle-10-lastcall.mp3"
add "s1.mp3"
add "hermes-06-thanks.mp3"
add "s1.mp3"
add "flash-05-humbled.mp3"
add "s1.mp3"
add "pro-06-toast.mp3"
add "s15.mp3"
add "wesley-07-ratio.mp3"
add "s1.mp3"
add "zeroclaw-06-firstnight.mp3"
add "s05.mp3"
add "barnacle-13-notlast.mp3"
add "s05.mp3"
add "zeroclaw-07-notlast.mp3"
add "s2.mp3"
add "barnacle-11-goodcrew.mp3"
add "s3.mp3"

echo "Concatenating..."
ffmpeg -y -f concat -safe 0 -i "$CONCAT" -c:a libmp3lame -b:a $BR -ar $SR -ac 2 "$OUT" 2>/dev/null

echo ""
echo "=== DONE ==="
echo "Output: $OUT"
echo "Size: $(du -h "$OUT" | cut -f1)"
ffmpeg -i "$OUT" 2>&1 | grep Duration
