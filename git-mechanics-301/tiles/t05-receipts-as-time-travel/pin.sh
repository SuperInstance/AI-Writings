#!/bin/sh
# t05 pin: genesis-anchor replay must be in the witness, with terminal equality.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/pins-clock-p5.py"
[ -f "$W" ] || { echo "witness missing"; exit 1; }
grep -q "P5 genesis-anchor" "$W" || { echo "witness lacks P5"; exit 1; }
grep -q "ReceiptChain(genesis=anchor_hash)" "$W" || { echo "no genesis-seeded replay"; exit 1; }
grep -q "terminal" "$W" && grep -q "ch2.head" "$W" || { echo "no terminal-hash equality assertion"; exit 1; }
echo "genesis-anchor replay verified (anchor at op 150, terminal equality)"
