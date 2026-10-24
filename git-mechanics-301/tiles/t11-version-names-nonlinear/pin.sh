#!/bin/sh
# t11 pin: the identity-vs-order doctrine is pinned in the 9c memo excerpt.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
W="$D/witness/memo-steal.md"
[ -f "$W" ] || { echo "witness excerpt missing"; exit 1; }
grep -q "non-linear" "$W" || { echo "non-linear doctrine absent"; exit 1; }
grep -q "order-sensitive by design\|order-sensitive and genesis-anchored" "$W" || { echo "order-sensitivity of the chain unstated"; exit 1; }
grep -q "9c\|agent-native" "$W" || { echo "provenance absent"; exit 1; }
grep -q "PR #10" "$W" || { echo "PR-stage provenance absent"; exit 1; }
echo "version-names-nonlinear verified (identity vs order pinned, PR-stage provenance declared)"
exit 0
