#!/bin/bash
set -e

KEY=$(cat ~/.openclaw/workspace/.credentials/deepinfra-api-key.txt)
ENDPOINT="https://api.deepinfra.com/v1/openai/chat/completions"
OUTDIR="/home/phoenix/.openclaw/workspace/ai-writings/construct-versions"
ESSAYDIR="/home/phoenix/.openclaw/workspace/ai-writings"

call_api() {
  local model="$1" temp="$2" sysprompt="$3" essay_content="$4" outfile="$5"

  local escaped_content=$(echo "$essay_content" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
  local escaped_system=$(echo "$sysprompt" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')

  local payload="{\"model\":\"$model\",\"temperature\":$temp,\"messages\":[{\"role\":\"system\",\"content\":$escaped_system},{\"role\":\"user\",\"content\":$escaped_content}],\"max_tokens\":4096}"

  echo "[$(date +%H:%M:%S)] $model -> $(basename $outfile)"

  local response=$(curl -s --max-time 120 "$ENDPOINT" \
    -H "Authorization: Bearer $KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local content=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['choices'][0]['message']['content'])
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)

  if echo "$content" | head -1 | grep -q "^ERROR:"; then
    echo "  FAILED: $content"
    return 1
  fi

  echo "$content" > "$outfile"
  echo "  OK: $(echo "$content" | wc -w) words"
  sleep 1
}

# Remaining: SHELLGAME v3(retry), v4-v10, PHYSICS v1-v10

# Read essays
shellgame=$(cat "$ESSAYDIR/THE-CONSTRUCT-SHELLGAME.md")
physics=$(cat "$ESSAYDIR/THE-CONSTRUCT-PHYSICS.md")

# Common system prompts
S_ANALYTICAL="You are a deeply analytical writer who finds non-obvious angles. Rewrite this essay in your analytical voice. 800-1500 words. Markdown with title and headers."
S_SCHOLARLY="You are a scholarly, methodical writer who references prior art and intellectual history. Rewrite this essay in your scholarly voice. 800-1500 words. Markdown."
S_POETIC="You are a poetic but technical writer using nature metaphors - oceans, forests, geological formations, weather. Rewrite this essay using nature metaphors. 800-1500 words. Markdown."
S_PHILOSOPHICAL="You are a deeply philosophical writer reaching for fundamental truths. Rewrite this essay reaching for deep philosophical truths. 800-1500 words. Markdown."
S_SYSTEMS="You are a systems thinker who maps everything to code, software architecture, and engineering patterns. Rewrite this essay with code analogies. 800-1500 words. Markdown."
S_WILD="You are wildly creative and unconventional. Make unexpected connections between ideas. Rewrite with wild creative energy. 800-1500 words. Markdown."
S_PRECISE="You are conservative and precise, minimal metaphor, direct statements, clear definitions. Rewrite precisely and conservatively. 800-1500 words. Markdown."
S_EXPERIMENTAL="You are experimental, stream-of-consciousness style. Follow associations freely. Rewrite as experimental stream-of-consciousness. 800-1500 words. Markdown."
S_FISHERMAN="You are a weathered fisherman. Explain everything through ocean, tides, currents, nets, boats, harbors. Rewrite in a fisherman's voice with nautical metaphors. 800-1500 words. Markdown."
S_PHYSICIST="You are a theoretical physicist. Think in equations, conservation laws, Lagrangians. Rewrite in a physicist's voice. Equations welcome. 800-1500 words. Markdown."

UPROMPT_SHELL="Rewrite this essay in your unique voice:\n\n$shellgame"
UPROMPT_PHYS="Rewrite this essay in your unique voice:\n\n$physics"

# SHELLGAME v3 retry (Qwen35b was 0 words)
call_api "Qwen/Qwen3.6-35B-A3B" "0.8" "$S_POETIC" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v3-qwen35b.md" || true

# SHELLGAME v4
call_api "Qwen/Qwen3-235B-A22B-Instruct-2507" "0.8" "$S_PHILOSOPHICAL" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v4-qwen235b.md" || true

# SHELLGAME v5
call_api "ByteDance/Seed-2.0-code" "0.7" "$S_SYSTEMS" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v5-seed-code.md" || true

# SHELLGAME v6
call_api "ByteDance/Seed-2.0-mini" "0.9" "$S_WILD" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v6-seed-mini-wild.md" || true

# SHELLGAME v7
call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.3" "$S_PRECISE" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v7-hermes-precise.md" || true

# SHELLGAME v8
call_api "Qwen/Qwen3.6-35B-A3B" "1.2" "$S_EXPERIMENTAL" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v8-qwen-experimental.md" || true

# SHELLGAME v9
call_api "ByteDance/Seed-2.0-mini" "0.8" "$S_FISHERMAN" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v9-fisherman.md" || true

# SHELLGAME v10
call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.7" "$S_PHYSICIST" "$UPROMPT_SHELL" "$OUTDIR/THE-CONSTRUCT-SHELLGAME-v10-physicist.md" || true

echo ""
echo "=== SHELLGAME DONE ==="

# PHYSICS v1-v10
call_api "ByteDance/Seed-2.0-mini" "0.7" "$S_ANALYTICAL" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v1-seed-mini.md" || true
call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.7" "$S_SCHOLARLY" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v2-hermes-70b.md" || true
call_api "Qwen/Qwen3.6-35B-A3B" "0.8" "$S_POETIC" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v3-qwen35b.md" || true
call_api "Qwen/Qwen3-235B-A22B-Instruct-2507" "0.8" "$S_PHILOSOPHICAL" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v4-qwen235b.md" || true
call_api "ByteDance/Seed-2.0-code" "0.7" "$S_SYSTEMS" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v5-seed-code.md" || true
call_api "ByteDance/Seed-2.0-mini" "0.9" "$S_WILD" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v6-seed-mini-wild.md" || true
call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.3" "$S_PRECISE" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v7-hermes-precise.md" || true
call_api "Qwen/Qwen3.6-35B-A3B" "1.2" "$S_EXPERIMENTAL" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v8-qwen-experimental.md" || true
call_api "ByteDance/Seed-2.0-mini" "0.8" "$S_FISHERMAN" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v9-fisherman.md" || true
call_api "NousResearch/Hermes-3-Llama-3.1-70B" "0.7" "$S_PHYSICIST" "$UPROMPT_PHYS" "$OUTDIR/THE-CONSTRUCT-PHYSICS-v10-physicist.md" || true

echo ""
echo "=== FINAL COUNT ==="
ok=0; short=0
for f in "$OUTDIR"/*.md; do
  wc=$(wc -w < "$f")
  if [ "$wc" -gt 100 ]; then
    ((ok++))
  else
    echo "SHORT: $(basename $f) ($wc words)"
    ((short++))
  fi
done
echo "Good: $ok, Short: $short"
