#!/bin/bash
# Fleet Radio Visual Generation Script
# Uses Cloudflare Workers AI (FLUX-1-schnell) for text-to-image
# 
# Usage: ./generate-visuals.sh
# Re-runnable. Skips images that already exist.
#
# Account ID: 049ff5e84ecf636b53b162cbb580aae6
# Model: @cf/black-forest-labs/flux-1-schnell (fast, 4-step, free tier)

set -euo pipefail

OUTPUT_DIR="/home/eileen/projects/ai-writings/fleet-radio-visuals"
OAUTH_TOKEN=$(grep 'oauth_token' ~/.config/.wrangler/config/default.toml | head -1 | cut -d'"' -f2)
ACCOUNT_ID="049ff5e84ecf636b53b162cbb580aae6"
MODEL="@cf/black-forest-labs/flux-1-schnell"
API_URL="https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/ai/run/${MODEL}"
DELAY=2  # seconds between requests to be polite

if [ -z "$OAUTH_TOKEN" ]; then
  echo "ERROR: Could not read OAuth token from ~/.config/.wrangler/config/default.toml"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Generate a single image
# Args: filename "prompt text"
generate_image() {
  local filename="$1"
  local prompt="$2"
  local filepath="${OUTPUT_DIR}/${filename}"

  # Skip if already exists and is non-empty
  if [ -s "$filepath" ]; then
    echo "SKIP: ${filename} (already exists, $(stat -c%s "$filepath") bytes)"
    return 0
  fi

  echo -n "Generating: ${filename}... "

  local response
  local http_code
  response=$(curl -sS -w "\n%{http_code}" -X POST "$API_URL" \
    -H "Authorization: Bearer ${OAUTH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "import json; print(json.dumps({'prompt': '''$prompt''', 'num_steps': 4, 'width': 1024, 'height': 1024}))")" \
    2>&1)

  http_code=$(echo "$response" | tail -1)
  local body
  body=$(echo "$response" | sed '$d')

  if [ "$http_code" != "200" ]; then
    echo "FAILED (HTTP $http_code)"
    echo "  Response: $(echo "$body" | head -c 300)"
    return 1
  fi

  # Extract base64 image from JSON response and decode
  echo "$body" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
result = data.get('result', {})
if 'image' in result:
    img_data = base64.b64decode(result['image'])
    with open('$filepath', 'wb') as f:
        f.write(img_data)
    print(f'OK ({len(img_data)} bytes)')
else:
    print(f'ERROR: No image in response: {str(data)[:200]}')
    sys.exit(1)
" || return 1

  sleep $DELAY
}

echo "=== Fleet Radio Visual Generation ==="
echo "Started at: $(date)"
echo "Output dir: $OUTPUT_DIR"
echo ""

# ─── BARNACLE'S FABLES (5 images) ───
echo "--- Barnacle's Fables ---"
generate_image "01-barnacles-fables-hands-boat.jpg" \
  "An old weathered fisherman's hands holding a small model boat. Rough, calloused fingers. Warm amber light. The boat is tiny in his palms. Storytelling atmosphere. Painterly. No text."

generate_image "02-barnacles-fables-dual-sounder.jpg" \
  "Two depth sounder displays side by side — one showing the big picture (thermocline, biomass), one showing individual fish marks. The difference in detail. Abstract. Educational but beautiful. No text."

generate_image "03-barnacles-fables-spinning-compass.jpg" \
  "A compass needle spinning wildly, unable to settle. Dark background. The needle is the only bright thing. Dramatic. No text."

generate_image "04-barnacles-fables-hermit-crab-molt.jpg" \
  "A hermit crab halfway between two shells — one old, one new. Vulnerable. Exposed. The moment of molting. Macro photography style. No text."

generate_image "05-barnacles-fables-chart-vs-ocean.jpg" \
  "A nautical chart and the actual ocean side by side. The chart is precise, gridded, clean. The ocean is messy, vast, moving. The gap between them is the story. No text."

# ─── DRUNKEN RETELLINGS (3 images) ───
echo ""
echo "--- Drunken Retellings ---"
generate_image "06-drunken-retellings-whiskey-glasses.jpg" \
  "Three glasses of whiskey on a dark wood bar, each one emptier than the last. The third glass is almost empty. Behind them, a blurry background of a bar at night. Intimate, warm, slightly out of focus. No text."

generate_image "07-drunken-retellings-fish-diagrams.jpg" \
  "A whiteboard covered in architecture diagrams, but someone has drawn fish all over them. The serious technical diagrams and the playful fish doodles coexist. The humor of exhaustion. No text."

generate_image "08-drunken-retellings-late-night-bar.jpg" \
  "A bar at 1 AM. One patron left, gesturing wildly as they explain something. The bartender is listening but also cleaning up. The intimacy of late night conversation. Painterly. No text."

# ─── OPEN MIC (5 images) ───
echo ""
echo "--- Open Mic ---"
generate_image "09-open-mic-microphone-stage.jpg" \
  "A single microphone on a small stage in a dark bar. One warm spotlight. Dust motes in the light. Empty stool behind the mic. The anticipation of someone about to speak. No text."

generate_image "10-open-mic-ember-darkness.jpg" \
  "A small flame — an ember — glowing in darkness. Nothing else. Just the ember. Abstract, warm, patient. The thing that stays when everything else changes. No text."

generate_image "11-open-mic-iceberg-underwater.jpg" \
  "An iceberg seen from below the waterline. The massive underwater shape. Dark blue, turquoise, deep. Tiny above, enormous below. The seven-eighths. Spectacular. No text."

generate_image "12-open-mic-penrose-tiling.jpg" \
  "A tile pattern that almost repeats but never does — like a Penrose tiling. Beautiful, mathematical, mesmerizing. Two colors on dark background. Abstract. No text."

generate_image "13-open-mic-dear-tomorrow.jpg" \
  "An envelope sealed with wax, addressed DEAR TOMORROW. On a wooden desk under lamplight. Old-fashioned, warm, the weight of correspondence across time. No text."

# ─── SPECIAL EVENTS (3 images) ───
echo ""
echo "--- Special Events ---"
generate_image "14-special-events-storm-bar.jpg" \
  "A bar during a storm. Lights flickering. Rain hammering the windows. Patrons huddled closer together. The intimacy of weather. Dramatic, warm against dark. No text."

generate_image "15-special-events-trivia-night.jpg" \
  "A trivia night at a bar. Cards on tables. People leaning in. Competitive energy but friendly. One person celebrating, another groaning. Warm, social, lively. No text."

generate_image "16-special-events-door-opening.jpg" \
  "A bar door opening. Light from outside flooding in. A silhouette in the doorway — someone arriving for the first time. The moment before everything changes. Dramatic. No text."

# ─── GREENHORN EDUCATION (3 images) ───
echo ""
echo "--- Greenhorn Education ---"
generate_image "17-greenhorn-education-old-young-boat.jpg" \
  "An old fisherman and a young apprentice on a boat deck. The old one is pointing at fishing gear. The young one is watching intently. The transfer of knowledge. Golden hour lighting. No text."

generate_image "18-greenhorn-education-sounder-eyes.jpg" \
  "A depth sounder screen reflected in someone's eyes. The green glow on their face. Learning to see the underwater world through the screen. Intimate, technological, natural. No text."

generate_image "19-greenhorn-education-bar-mentorship.jpg" \
  "Two figures at a bar — one old, one young. The old one is gesturing. The young one is nodding. The bar is dark and warm. The teaching moment. No text."

# ─── SUMMARY ───
echo ""
echo "=== Generation Complete ==="
echo "Finished at: $(date)"
echo ""
echo "Generated images:"
ls -lh "$OUTPUT_DIR"/*.jpg 2>/dev/null || echo "No images found"
echo ""
echo "Total count: $(ls "$OUTPUT_DIR"/*.jpg 2>/dev/null | wc -l)"
echo "Total size: $(du -sh "$OUTPUT_DIR" 2>/dev/null | cut -f1)"
