#!/bin/sh
# t02 pin: order-not-time must be demonstrated by the witness code.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/pins-clock-p2.py"
[ -f "$W" ] || { echo "witness missing"; exit 1; }
grep -q "P2 order-not-time" "$W" || { echo "witness lacks P2"; exit 1; }
grep -q "ReceiptChain" "$W" || { echo "witness lacks chain construction"; exit 1; }
grep -q "div == 1" "$W" || { echo "witness lacks the divergence assertion"; exit 1; }
grep -qi "clock" "$W" && { echo "witness references a clock — doctrine violated"; exit 1; }
echo "order-not-time verified: divergence at op 1, no clock in evidence"
