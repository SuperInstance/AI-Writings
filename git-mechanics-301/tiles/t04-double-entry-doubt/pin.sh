#!/bin/sh
# t04 pin: the Entry grammar must enforce required fields.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/entry-grammar.py"
[ -f "$W" ] || { echo "witness missing"; exit 1; }
grep -q "stopped_checking" "$W" && grep -q "because" "$W" && \
  grep -q "covered_by" "$W" && grep -q "revisit_trigger" "$W" \
  || { echo "four required fields absent"; exit 1; }
grep -q "missing" "$W" && grep -q "ValueError" "$W" \
  || { echo "no named refusal for incomplete entries"; exit 1; }
grep -q "discharge_reason" "$W" || { echo "no discharge discipline"; exit 1; }
echo "double-entry doubt grammar verified (4 required fields, named refusal)"
