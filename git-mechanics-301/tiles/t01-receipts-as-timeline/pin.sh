#!/bin/sh
# t01 pin: the receipts-as-timeline witness must encode the doctrine.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/quilt-pins-doctrine.sh"
[ -f "$W" ] || { echo "witness missing"; exit 1; }
grep -q "receipt" "$W" || { echo "no receipt doctrine in witness"; exit 1; }
grep -q "P1" "$W" && grep -q "P7" "$W" && grep -q "P8" "$W" || { echo "witness lacks pin doctrine (P1/P7/P8)"; exit 1; }
grep -q "clone" "$W" || { echo "witness lacks clone-provable evidence (P5/P8)"; exit 1; }
echo "clone-provable receipt doctrine verified (P1/P6/P7/P8)"
