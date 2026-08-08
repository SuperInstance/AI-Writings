#!/bin/bash
# Cloudflare Workers AI image generation via FLUX-1-schnell
# Fast, free tier, good quality for atmospheric/artistic images

ACCOUNT_ID="049ff5e84ecf636b53b162cbb580aae6"
TOKEN=$(grep oauth_token ~/.config/.wrangler/config/default.toml | cut -d'"' -f2)

generate_image() {
  local prompt="$1"
  local outfile="$2"
  local steps="${3:-4}"
  
  echo -n "  Generating $(basename "$outfile")... "
  
  local tmpfile=$(mktemp)
  
  curl -s -X POST \
    "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$prompt" --argjson s "$steps" '{prompt:$p, steps:$s}')" \
    -o "$tmpfile"
  
  local success=$(jq -r '.success // "unknown"' "$tmpfile" 2>/dev/null)
  
  if [ "$success" = "true" ]; then
    jq -r '.result.image' "$tmpfile" | base64 -d > "$outfile"
    local size=$(du -h "$outfile" | cut -f1)
    echo "✓ ${size}"
    rm -f "$tmpfile"
    return 0
  else
    echo "✗ FAILED"
    jq '.errors // .' "$tmpfile" 2>/dev/null | head -3
    rm -f "$tmpfile"
    return 1
  fi
}
