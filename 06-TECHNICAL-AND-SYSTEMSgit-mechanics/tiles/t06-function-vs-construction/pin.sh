#!/bin/sh
# t06 pin: the guardian verdict must record the construction gap and its closure.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/guardian-f-verdict.md"
[ -f "$W" ] || { echo "witness missing"; exit 1; }
tr '\n' ' ' < "$W" | grep -q "left the .construction. unpinned" \
  || { echo "verdict quote absent"; exit 1; }
grep -q "P6b" "$W" || { echo "closure (P6b) absent"; exit 1; }
grep -q "PR #3" "$W" || { echo "no citable closure reference"; exit 1; }
echo "function-vs-construction verified (gap found, P6b closed it, PR #3)"
