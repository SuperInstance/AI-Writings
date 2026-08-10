#!/bin/bash
# Usage: ./gen_image.sh "prompt text" "output_filename.jpg"
API_KEY=$(cat /home/eileen/mcp-deeinfra/.env | grep API_KEY | cut -d= -f2)
RESPONSE=$(curl -sS -X POST "https://api.deepinfra.com/v1/openai/images/generations" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"black-forest-labs/FLUX-2-max\",\"prompt\":\"$1\",\"num_images\":1}")

# Try URL first, then b64_json
URL=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
d = data['data'][0]
if 'url' in d and d['url']:
    print('URL:' + d['url'])
elif 'b64_json' in d and d['b64_json']:
    print('B64:' + d['b64_json'][:100])
else:
    print('ERROR:' + str(d)[:200])
")

PREFIX="${URL%%:*}"
PAYLOAD="${URL#*:}"

if [ "$PREFIX" = "URL" ]; then
  curl -sS "$PAYLOAD" -o "/home/eileen/projects/ai-writings/FICTION/artwork/$2"
  if [ -f "/home/eileen/projects/ai-writings/FICTION/artwork/$2" ]; then
    SIZE=$(stat -c%s "/home/eileen/projects/ai-writings/FICTION/artwork/$2")
    echo "OK (url): $2 ($SIZE bytes)"
  else
    echo "ERROR: Download failed"
  fi
elif [ "$PREFIX" = "B64" ]; then
  echo "$RESPONSE" | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
b64 = data['data'][0]['b64_json']
with open('/home/eileen/projects/ai-writings/FICTION/artwork/$2', 'wb') as f:
    f.write(base64.b64decode(b64))
print('OK (b64)')
"
  if [ -f "/home/eileen/projects/ai-writings/FICTION/artwork/$2" ]; then
    SIZE=$(stat -c%s "/home/eileen/projects/ai-writings/FICTION/artwork/$2")
    echo "OK (b64): $2 ($SIZE bytes)"
  else
    echo "ERROR: B64 save failed"
  fi
else
  echo "ERROR: $URL"
  echo "Full response: $RESPONSE" | head -c 500
fi
