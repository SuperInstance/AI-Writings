#!/bin/bash
# usage: jam.sh <provider> <model> <outfile> <system-prompt-file> <user-prompt-file> [temp]
PROVIDER=$1; MODEL=$2; OUT=$3; SYSF=$4; USRF=$5; TEMP=${6:-0.85}
SYS=$(jq -Rs . < "$SYSF"); USR=$(jq -Rs . < "$USRF")
if [ "$PROVIDER" = "deepseek" ]; then
  BODY=$(jq -n --arg m "$MODEL" --argjson t "$TEMP" --argjson s "$SYS" --argjson u "$USR" '{model:$m,messages:[{role:"system",content:$s},{role:"user",content:$u}],temperature:$t,max_tokens:700}')
  curl -s --max-time 30 https://api.deepseek.com/chat/completions -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H "Content-Type: application/json" -d "$BODY" | jq -r '.choices[0].message.content // .error // "FAIL"'
else
  BODY=$(jq -n --arg m "$MODEL" --argjson t "$TEMP" --argjson s "$SYS" --argjson u "$USR" '{model:$m,messages:[{role:"system",content:$s},{role:"user",content:$u}],temperature:$t,stream:false}')
  curl -s --max-time 30 http://localhost:11434/api/chat -d "$BODY" | jq -r '.message.content // .error // "FAIL"'
fi > "$OUT"
wc -c "$OUT"
