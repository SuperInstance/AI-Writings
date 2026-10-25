#!/bin/sh
# Ask a cheap DeepInfra model for candidate fixtures. Output is UNTRUSTED; metabolizer.gate_crew() filters it.
# usage: crew.sh "<plain technical prompt>"  -> prints the model's text
curl -sS https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $DEEPINFRA_KEY" -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json,sys;print(json.dumps({"model":"deepseek-ai/DeepSeek-V4-Flash","temperature":0.7,"max_tokens":1500,"messages":[{"role":"user","content":sys.argv[1]}]}))' "$1")" \
 | python3 -c 'import json,sys;print(json.load(sys.stdin)["choices"][0]["message"]["content"])'
