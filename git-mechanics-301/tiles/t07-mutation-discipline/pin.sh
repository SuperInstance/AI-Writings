#!/bin/sh
# t07 pin: the false-claim story must be on file with the arithmetic detail.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/false-claim-correction.md"
[ -f "$W" ] || { echo "witness missing"; exit 1; }
grep -q "435 \* lo" "$W" && grep -q "436 \* lo" "$W" \
  || { echo "genuine arithmetic mutation absent"; exit 1; }
grep -q "comment" "$W" || { echo "cosmetic-mutation lesson absent"; exit 1; }
grep -qi "correct" "$W" || { echo "public correction absent"; exit 1; }
echo "mutation-discipline verified (false claim + arithmetic detail + public correction)"
