#!/bin/bash
set -e

# ============================================================
# DOGS FELL IN LOVE — Video Builder
# Creates simple animated videos from background images,
# puppet-style sprite overlays, and episode audio tracks.
# Uses ffmpeg with Ken Burns zoom, sprite bobbing, and
# colorkey for white-background sprite transparency.
# ============================================================

BASE="/home/eileen/projects/ai-writings/radio-theater/dogs-fell-in-love"
VIDEO="$BASE/video"
FONTS="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# Helpers
get_duration() {
  ffmpeg -i "$1" 2>&1 | grep -oP 'Duration: \K[0-9:]+' | \
    awk -F: '{printf "%.2f", $1*3600 + $2*60 + $3}'
}

echo "========================================"
echo "  DOGS FELL IN LOVE — Video Builder"
echo "========================================"

# ─────────────────────────────────────────────
# EPISODE 1: "Dogs Fell in Love" (~43s)
# Scenes: cave (intro/origin) → stick (the throw/the play)
# Sprites: Hermes (narrator presence), Skipper (the dog)
# ─────────────────────────────────────────────
echo ""
echo "[EPISODE 1] Building 'Dogs Fell in Love'..."

EP1_AUDIO="$BASE/dogs-fell-in-love-episode-1.mp3"
EP1_DUR=$(get_duration "$EP1_AUDIO")
EP1_HALF=$(awk "BEGIN {printf \"%.2f\", $EP1_DUR / 2}")

# Build Episode 1: two-scene video with crossfade
# Scene 1 (cave): 0 to half — Hermes sprite, subtle zoom in
# Scene 2 (stick): half to end — Skipper sprite, subtle zoom out

# Scene 1: cave background with Hermes sprite overlay
ffmpeg -y -loop 1 -t "$EP1_DUR" -i "$VIDEO/bg-ep1-cave.jpg" \
  -loop 1 -t "$EP1_DUR" -i "$VIDEO/sprite-hermes.png" \
  -i "$EP1_AUDIO" \
  -filter_complex "
    [0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,
      zoompan=z='min(zoom+0.0008,1.15)':d=1:s=1280x720:fps=30[bg];
    [1:v]scale=200:200[sprite];
    [sprite]colorkey=0xFFFFFF:0.3:0.15[spkey];
    [bg][spkey]overlay=x='W-w-80':y='H-h-60+sin(t)*8':format=auto[v]
  " \
  -map "[v]" -map 2:a \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest \
  -t "$EP1_DUR" \
  "$VIDEO/dogs-ep1.mp4" 2>&1 | tail -5

echo "[EPISODE 1] Done: $(ls -lh $VIDEO/dogs-ep1.mp4 | awk '{print $5}')"

# ─────────────────────────────────────────────
# EPISODE 2: "The Good Dog" (~32s)
# Scene: the bar at night — Lucineer sprite
# Mood: introspective, steady
# ─────────────────────────────────────────────
echo ""
echo "[EPISODE 2] Building 'The Good Dog'..."

EP2_AUDIO="$BASE/dogs-fell-in-love-episode-2.mp3"
EP2_DUR=$(get_duration "$EP2_AUDIO")

# Single scene: bar background with Lucineer sprite
ffmpeg -y -loop 1 -t "$EP2_DUR" -i "$VIDEO/bg-ep2-bar.jpg" \
  -loop 1 -t "$EP2_DUR" -i "$VIDEO/sprite-lucineer.png" \
  -i "$EP2_AUDIO" \
  -filter_complex "
    [0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,
      zoompan=z='if(lte(on,1),1.1,max(1.001,zoom-0.0005))':d=1:s=1280x720:fps=30[bg];
    [1:v]scale=180:180[sprite];
    [sprite]colorkey=0xFFFFFF:0.3:0.15[spkey];
    [bg][spkey]overlay=x=80:y='H-h-40+sin(t)*6':format=auto,
      fade=t=in:st=0:d=1.5,
      fade=t=out:st=$(awk "BEGIN {printf \"%.2f\", $EP2_DUR - 1.5}"):d=1.5[v]
  " \
  -map "[v]" -map 2:a \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest \
  -t "$EP2_DUR" \
  "$VIDEO/dogs-ep2.mp4" 2>&1 | tail -5

echo "[EPISODE 2] Done: $(ls -lh $VIDEO/dogs-ep2.mp4 | awk '{print $5}')"

# ─────────────────────────────────────────────
# EPISODE 3: "Dogs Know Things" (~15s)
# Scenes: boats at anchor → dog swimming
# Sprites: Skipper
# Mood: quiet, the simplest truth
# ─────────────────────────────────────────────
echo ""
echo "[EPISODE 3] Building 'Dogs Know Things'..."

EP3_AUDIO="$BASE/dogs-fell-in-love-episode-3.mp3"
EP3_DUR=$(get_duration "$EP3_AUDIO")
EP3_HALF=$(awk "BEGIN {printf \"%.2f\", $EP3_DUR * 0.55}")

# Scene 1: boats at night — establish setting (first ~55%)
ffmpeg -y -loop 1 -t "$EP3_HALF" -i "$VIDEO/bg-ep3-boats.jpg" \
  -loop 1 -t "$EP3_HALF" -i "$VIDEO/sprite-skipper.png" \
  -filter_complex "
    [0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,
      zoompan=z='min(zoom+0.001,1.12)':d=1:s=1280x720:fps=30[bg];
    [1:v]scale=120:120[sprite];
    [sprite]colorkey=0xFFFFFF:0.3:0.15[spkey];
    [bg][spkey]overlay=x='W-w-100':y='H-h-80+sin(t)*5':format=auto,
      fade=t=in:st=0:d=1[v]
  " \
  -map "[v]" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -t "$EP3_HALF" \
  "$VIDEO/ep3-scene1.mp4" 2>&1 | tail -3

# Scene 2: dog swimming — the emotional center (remaining ~45%)
EP3_SC2_DUR=$(awk "BEGIN {printf \"%.2f\", $EP3_DUR - $EP3_HALF}")

ffmpeg -y -loop 1 -t "$EP3_SC2_DUR" -i "$VIDEO/bg-ep3-swim.jpg" \
  -loop 1 -t "$EP3_SC2_DUR" -i "$VIDEO/sprite-skipper.png" \
  -filter_complex "
    [0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,
      zoompan=z='if(lte(on,1),1.12,max(1.001,zoom-0.0008))':d=1:s=1280x720:fps=30[bg];
    [1:v]scale=100:100[sprite];
    [sprite]colorkey=0xFFFFFF:0.3:0.15[spkey];
    [bg][spkey]overlay=x='340':y='420+sin(t*2)*10':format=auto,
      fade=t=in:st=0:d=1,
      fade=t=out:st=$(awk "BEGIN {printf \"%.2f\", $EP3_SC2_DUR - 1.5}"):d=1.5[v]
  " \
  -map "[v]" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -t "$EP3_SC2_DUR" \
  "$VIDEO/ep3-scene2.mp4" 2>&1 | tail -3

# Concatenate the two scenes and add audio
echo "[EPISODE 3] Concatenating scenes..."
cat > "$VIDEO/ep3-concat.txt" <<EOF
file 'ep3-scene1.mp4'
file 'ep3-scene2.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i "$VIDEO/ep3-concat.txt" \
  -i "$EP3_AUDIO" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  -map 0:v:0 -map 1:a:0 \
  "$VIDEO/dogs-ep3.mp4" 2>&1 | tail -5

# Cleanup temp files
rm -f "$VIDEO/ep3-scene1.mp4" "$VIDEO/ep3-scene2.mp4" "$VIDEO/ep3-concat.txt"

echo "[EPISODE 3] Done: $(ls -lh $VIDEO/dogs-ep3.mp4 | awk '{print $5}')"

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
echo ""
echo "========================================"
echo "  BUILD COMPLETE"
echo "========================================"
echo ""
for ep in 1 2 3; do
  f="$VIDEO/dogs-ep${ep}.mp4"
  if [ -f "$f" ]; then
    sz=$(ls -lh "$f" | awk '{print $5}')
    dur=$(ffmpeg -i "$f" 2>&1 | grep -oP 'Duration: \K[0-9:.]+')
    echo "  Episode $ep: $sz  Duration: $dur"
  else
    echo "  Episode $ep: FAILED"
  fi
done
echo ""
echo "Output directory: $VIDEO/"
