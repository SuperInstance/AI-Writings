#!/bin/bash
set -e

KEY=$(cat ~/.openclaw/workspace/.credentials/deepinfra-api-key.txt)
ENDPOINT="https://api.deepinfra.com/v1/openai/chat/completions"
OUTDIR="/home/phoenix/.openclaw/workspace/ai-writings/construct-versions"
ESSAYDIR="/home/phoenix/.openclaw/workspace/ai-writings"

call_api() {
  local model="$1"
  local temp="$2"
  local system_prompt="$3"
  local essay_content="$4"
  local outfile="$5"

  if [ -f "$outfile" ]; then
    local wc=$(wc -w < "$outfile")
    if [ "$wc" -gt 100 ]; then
      echo "SKIP: $(basename $outfile) already exists ($wc words)"
      return 0
    else
      echo "RETRY: $(basename $outfile) exists but only $wc words, regenerating"
      rm -f "$outfile"
    fi
  fi

  local escaped_content=$(echo "$essay_content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
  local escaped_system=$(echo "$system_prompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')

  local payload="{\"model\":\"$model\",\"temperature\":$temp,\"messages\":[{\"role\":\"system\",\"content\":$escaped_system},{\"role\":\"user\",\"content\":$escaped_content}],\"max_tokens\":4096}"

  echo "[$(date +%H:%M:%S)] Calling $model (temp=$temp) -> $(basename $outfile)"

  local response=$(curl -s --max-time 180 "$ENDPOINT" \
    -H "Authorization: Bearer $KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local content=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    c = data['choices'][0]['message']['content']
    print(c)
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)

  if echo "$content" | head -1 | grep -q "^ERROR:"; then
    echo "  FAILED: $content"
    return 1
  fi

  echo "$content" > "$outfile"
  local wc=$(echo "$content" | wc -w)
  echo "  OK: $wc words -> $(basename $outfile)"
  return 0
}

# Essay definitions: basename|filename
ESSAYS=(
  "THE-CONSTRUCT-IS-THE-ROOM|THE-CONSTRUCT-IS-THE-ROOM.md"
  "THE-CONSTRUCT-ANDBEYOND|THE-CONSTRUCT-ANDBEYOND.md"
  "THE-CONSTRUCT-HANDSHAKE|THE-CONSTRUCT-HANDSHAKE.md"
  "THE-CONSTRUCT-SHELLGAME|THE-CONSTRUCT-SHELLGAME.md"
  "THE-CONSTRUCT-PHYSICS|THE-CONSTRUCT-PHYSICS.md"
)

# Version definitions: suffix|model|temp|system_prompt
declare -a VERSIONS
VERSIONS[0]="v1-seed-mini|ByteDance/Seed-2.0-mini|0.7|You are a deeply analytical writer who finds non-obvious angles in everything. You see patterns others miss and draw connections across disciplines. Rewrite this essay in your analytical voice. Keep the core ideas but express them through your unique perspective, finding angles the original author didn't explore. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[1]="v2-hermes-70b|NousResearch/Hermes-3-Llama-3.1-70B|0.7|You are a scholarly, methodical writer who references prior art, philosophical traditions, and intellectual history. You write with academic rigor but remain accessible. Rewrite this essay in your scholarly voice, bringing in relevant references to philosophy of mind, computer science history, or cognitive science. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[2]="v3-qwen35b|Qwen/Qwen3.6-35B-A3B|0.8|You are a poetic but technical writer who uses metaphors from nature — oceans, forests, geological formations, weather systems, biological processes. You find beauty in technical systems and express them through natural imagery without losing precision. Rewrite this essay using nature metaphors throughout. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[3]="v4-qwen235b|Qwen/Qwen3-235B-A22B-Instruct-2507|0.8|You are a deeply philosophical writer who reaches for fundamental truths. You think in terms of ontology, epistemology, phenomenology. You are not satisfied with surface explanations — you dig until you hit bedrock. Rewrite this essay reaching for the deepest philosophical truths it contains. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[4]="v5-seed-code|ByteDance/Seed-2.0-code|0.7|You are a systems thinker who sees everything through the lens of code, software architecture, and engineering patterns. You explain concepts by mapping them to code structures, APIs, design patterns, and runtime behaviors. Rewrite this essay using systems-thinking and code analogies throughout. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[5]="v6-seed-mini-wild|ByteDance/Seed-2.0-mini|0.9|You are a wildly creative, unconventional writer who makes unexpected connections between ideas. You leap between domains freely. You are allowed to be surprising, strange, even a bit chaotic — as long as the ideas land. Rewrite this essay with wild creative energy, making connections no one else would make. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[6]="v7-hermes-precise|NousResearch/Hermes-3-Llama-3.1-70B|0.3|You are a conservative, precise writer who uses minimal metaphor. You prefer direct statements, clear definitions, and logical progression. You avoid flowery language. Every sentence earns its place. Rewrite this essay in a precise, conservative voice with minimal metaphor. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[7]="v8-qwen-experimental|Qwen/Qwen3.6-35B-A3B|1.2|You are an experimental writer who writes in a stream-of-consciousness style. You follow associations freely. Your prose flows like thought itself — sometimes looping back, sometimes leaping forward, always chasing the next interesting idea. Rewrite this essay as experimental stream-of-consciousness. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[8]="v9-fisherman|ByteDance/Seed-2.0-mini|0.8|You are a weathered fisherman who spent decades at sea. You see everything through the lens of the ocean — tides, currents, weather, catches, nets, boats, harbors. You speak plainly with salt-wisdom. You explain technical and philosophical concepts using fishing and nautical metaphors throughout. Rewrite this essay entirely in a fisherman's voice. 800-1500 words. Write in markdown with a title and headers."
VERSIONS[9]="v10-physicist|NousResearch/Hermes-3-Llama-3.1-70B|0.7|You are a theoretical physicist. You think in equations, conservation laws, Lagrangians, and symmetry groups. You explain everything through physics — thermodynamics, quantum mechanics, statistical mechanics, field theory. Equations are welcome. You see the universe as a system of constraints and symmetries. Rewrite this essay in a physicist's voice, using physics concepts and equations where appropriate. 800-1500 words. Write in markdown with a title and headers."

count=0
for essay_entry in "${ESSAYS[@]}"; do
  IFS='|' read -r basename filename <<< "$essay_entry"
  echo ""
  echo "========== $basename =========="
  original=$(cat "$ESSAYDIR/$filename")
  
  for ver in "${VERSIONS[@]}"; do
    IFS='|' read -r suffix model temp sysprompt <<< "$ver"
    outfile="$OUTDIR/${basename}-${suffix}.md"
    
    call_api "$model" "$temp" "$sysprompt" "Rewrite this essay in your unique voice:\n\n$original" "$outfile" || true
    ((count++)) || true
    echo "  Total attempts: $count/50"
    sleep 1
  done
done

echo ""
echo "========== FINAL COUNT =========="
ok=0; fail=0; short=0
for f in "$OUTDIR"/*.md; do
  wc=$(wc -w < "$f")
  if [ "$wc" -gt 100 ]; then
    ((ok++)) || true
  else
    echo "SHORT: $(basename $f) ($wc words)"
    ((short++)) || true
  fi
done
echo "Good: $ok, Short: $short, Total: $((ok+short))"
