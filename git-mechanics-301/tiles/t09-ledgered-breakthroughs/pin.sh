#!/bin/sh
# t09 pin: the meta-tile verifies against the repo's own structures.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$D/../.." && pwd)
L="$ROOT/LEDGER.md"
M="$ROOT/program/manifest.json"
[ -f "$L" ] || { echo "LEDGER.md missing"; exit 1; }
grep -q "t08" "$L" && grep -q "t03" "$L" || { echo "ledger lacks tile births"; exit 1; }
python3 - "$M" <<'PY' || exit 1
import json,sys
m=json.load(open(sys.argv[1]))
t=m['tiles']
assert set(t)== {f't0{i}' for i in range(1,10)}, "graph must have exactly the founding nine"
for k,v in t.items():
    for p in v['prereqs']:
        assert p in t, f"{k} prereqs unknown tile {p}"
assert t['t08']['status']=='draft', "t08 must stay draft until the wave-4 witness ships"
assert len(m['divergence-watch'])>=3, "honest gaps must be named"
print("graph coherent: 9 tiles, prereq edges closed, t08 honestly draft")
PY
grep -q "demonstrated RED\|demonstrated-red" "$L" || { echo "ledger lost the RED doctrine"; exit 1; }
echo "ledgered-breakthroughs verified (journal + graph + self-audit intact)"
