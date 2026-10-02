#!/bin/sh
# t03 pin: both witnesses must show demonstrated RED states.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
L="$D/witness/audit-p6-red.log"
R="$D/witness/r73-mutation.md"
[ -f "$L" ] || { echo "audit-p6-red.log missing"; exit 1; }
grep -q "FAIL P6" "$L" || { echo "no demonstrated RED for P6"; exit 1; }
grep -q "PASS P1" "$L" || { echo "witness lacks control PASSes (P1)"; exit 1; }
grep -q "first-divergence-position=1" "$L" || { echo "not the authentic run (P2 marker absent)"; exit 1; }
[ -f "$R" ] || { echo "r73-mutation.md missing"; exit 1; }
grep -q "the franken file must never download" "$R" || { echo "R73 lacks the exact refusal assertion"; exit 1; }
grep -q "RED" "$R" || { echo "R73 lacks demonstrated RED"; exit 1; }
echo "two demonstrated REDs on file (P6 sig-canonical, R73 franken-guard)"
