#!/bin/bash
set -e

KEY=$(cat ~/.openclaw/workspace/.credentials/deepinfra-api-key.txt)
ENDPOINT="https://api.deepinfra.com/v1/openai/chat/completions"
OUTDIR="/home/phoenix/.openclaw/workspace/ai-writings/construct-versions"
ESSAYDIR="/home/phoenix/.openclaw/workspace/ai-writings"

# Essays: basename, original filename
declare -a ESSAYS=(
  "THE-CONSTRUCT-IS-THE-ROOM:THE-CONSTRUCT-IS-THE-ROOM.md"
  "THE-CONSTRUCT-ANDBEYOND:THE-CONSTRUCT-ANDBEYOND.md"
  "THE-CONSTRUCT-HANDSHAKE:THE-CONSTRUCT-HANDSHAKE.md"
  "THE-CONSTRUCT-SHELLGAME:THE-CONSTRUCT-SHELLGAME.md"
  "THE-CONSTRUCT-PHYSICS:THE-CONSTRUCT-PHYSICS.md"
)

call_api() {
  local model="$1"
  local temp="$2"
  local system_prompt="$3"
  local essay_content="$4"
  local outfile="$5"

  # Escape content for JSON
  local escaped_content=$(echo "$essay_content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
  local escaped_system=$(echo "$system_prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')

  local payload="{\"model\":\"$model\",\"temperature\":$temp,\"messages\":[{\"role\":\"system\",\"content\":$escaped_system},{\"role\":\"user\",\"content\":$escaped_content}],\"max_tokens\":4096}"

  echo "[$(date +%H:%M:%S)] Calling $model (temp=$temp) -> $(basename $outfile)"

  local response=$(curl -s --max-time 300 "$ENDPOINT" \
    -H "Authorization: Bearer $KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")

  # Extract content
  local content=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    c = data['choices'][0]['message']['content']
    print(c)
except Exception as e:
    print(f'ERROR: {e}')
    print(f'Raw response (first 500): ', file=sys.stderr)
    print(str(data)[:500] if 'data' in dir() else 'no data', file=sys.stderr)
" 2>&1)

  if echo "$content" | head -1 | grep -q "^ERROR:"; then
    echo "  FAILED: $content"
    echo "$response" > "${outfile}.error"
    return 1
  fi

  echo "$content" > "$outfile"
  local wc=$(echo "$content" | wc -w)
  echo "  OK: $wc words -> $(basename $outfile)"
  return 0
}

count=0
total=50

for essay_entry in "${ESSAYS[@]}"; do
  IFS=':' read -r basename filename <<< "$essay_entry"
  echo ""
  echo "========== Processing: $basename =========="
  
  # Read original essay
  original=$(cat "$ESSAYDIR/$filename")
  
  # v1: Seed-2.0-mini, analytical
  call_api "ByteDance/Seed-2.0-mini" "0.7" \
    "You are a deeply analytical writer who finds non-obvious angles in everything. You see patterns others miss and draw connections across disciplines. Rewrite this essay in your own analytical voice. Keep the core ideas but express them through your unique perspective, finding angles the original author didn't explore. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay in your own analytical voice. Find the non-obvious angles:\n\n$original" \
    "$OUTDIR/${basename}-v1-seed-mini.md" || true
  ((count++)) || true
  sleep 1

  # v2: Hermes-70B, scholarly
  call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.7" \
    "You are a scholarly, methodical writer who references prior art, philosophical traditions, and intellectual history. You write with academic rigor but remain accessible. Rewrite this essay in your scholarly voice, bringing in relevant references to philosophy of mind, computer science history, or cognitive science. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay in your scholarly voice. Reference prior art and intellectual traditions where relevant:\n\n$original" \
    "$OUTDIR/${basename}-v2-hermes-70b.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v3: Qwen3.6-35B, poetic/technical with nature metaphors
  call_api "Qwen/Qwen3.6-35B-A3B" "0.8" \
    "You are a poetic but technical writer who uses metaphors from nature — oceans, forests, geological formations, weather systems, biological processes. You find beauty in technical systems and express them through natural imagery without losing precision. Rewrite this essay using nature metaphors throughout. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay using metaphors from nature. Be poetic but technically precise:\n\n$original" \
    "$OUTDIR/${basename}-v3-qwen35b.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v4: Qwen3-235B, philosophical deep truths
  call_api "Qwen/Qwen3-235B-A22B-Instruct-2507" "0.8" \
    "You are a deeply philosophical writer who reaches for fundamental truths. You think in terms of ontology, epistemology, phenomenology. You're not satisfied with surface explanations — you dig until you hit bedrock. Rewrite this essay reaching for the deepest philosophical truths it contains. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay philosophically. Reach for the deep truths beneath the surface:\n\n$original" \
    "$OUTDIR/${basename}-v4-qwen235b.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v5: Seed-2.0-code, systems-thinking with code analogies
  call_api "ByteDance/Seed-2.0-code" "0.7" \
    "You are a systems thinker who sees everything through the lens of code, software architecture, and engineering patterns. You explain concepts by mapping them to code structures, APIs, design patterns, and runtime behaviors. Rewrite this essay using systems-thinking and code analogies throughout. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay using systems-thinking and code analogies:\n\n$original" \
    "$OUTDIR/${basename}-v5-seed-code.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v6: Seed-2.0-mini temp=0.9, wild creative
  call_api "ByteDance/Seed-2.0-mini" "0.9" \
    "You are a wildly creative, unconventional writer who makes unexpected connections between ideas. You leap between domains freely. You're allowed to be surprising, strange, even a bit chaotic — as long as the ideas land. Rewrite this essay with wild creative energy, making connections no one else would make. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay with wild creative energy. Make unexpected connections:\n\n$original" \
    "$OUTDIR/${basename}-v6-seed-mini-wild.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v7: Hermes-70B temp=0.3, conservative precise
  call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.3" \
    "You are a conservative, precise writer who uses minimal metaphor. You prefer direct statements, clear definitions, and logical progression. You avoid flowery language. Every sentence earns its place. Rewrite this essay in a precise, conservative voice with minimal metaphor. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay precisely and conservatively. Minimal metaphor, maximum clarity:\n\n$original" \
    "$OUTDIR/${basename}-v7-hermes-precise.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v8: Qwen3.6-35B temp=1.2, experimental stream-of-consciousness
  call_api "Qwen/Qwen3.6-35B-A3B" "1.2" \
    "You are an experimental writer who writes in a stream-of-consciousness style. You follow associations freely. Your prose flows like thought itself — sometimes looping back, sometimes leaping forward, always chasing the next interesting idea. Rewrite this essay as experimental stream-of-consciousness. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay as experimental stream-of-consciousness:\n\n$original" \
    "$OUTDIR/${basename}-v8-qwen-experimental.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v9: Seed-2.0-mini, fisherman's voice
  call_api "ByteDance/Seed-2.0-mini" "0.8" \
    "You are a weathered fisherman who spent decades at sea. You see everything through the lens of the ocean — tides, currents, weather, catches, nets, boats, harbors. You speak plainly with salt-wisdom. You explain technical and philosophical concepts using fishing and nautical metaphors throughout. Rewrite this essay entirely in a fisherman's voice. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay in a fisherman's voice. Use nautical and fishing metaphors throughout:\n\n$original" \
    "$OUTDIR/${basename}-v9-fisherman.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

  # v10: Hermes-70B, physicist's voice
  call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.7" \
    "You are a theoretical physicist. You think in equations, conservation laws, Lagrangians, and symmetry groups. You explain everything through physics — thermodynamics, quantum mechanics, statistical mechanics, field theory. Equations are welcome. You see the universe as a system of constraints and symmetries. Rewrite this essay in a physicist's voice, using physics concepts and equations where appropriate. 800-1500 words. Write in markdown with a title and headers." \
    "Rewrite this essay in a physicist's voice. Use physics concepts and equations where appropriate:\n\n$original" \
    "$OUTDIR/${basename}-v10-physicist.md" || true
  ((count++)) || true
  echo "  Progress: $count/$total"
  sleep 1

done

echo ""
echo "========== COMPLETE =========="
echo "Generated $count files"
ls -la "$OUTDIR"/*.md 2>/dev/null | wc -l
echo "Error files:"
ls "$OUTDIR"/*.error 2>/dev/null || echo "  None"
