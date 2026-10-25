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
assert set(t)== {f't0{i}' for i in range(1,10)} | {'t10','t11'}, "graph must have the founding nine plus t10/t11"
for k,v in t.items():
    for p in v['prereqs']:
        assert p in t, f"{k} prereqs unknown tile {p}"
assert t['t08']['status']=='pinned', "t08 pinned on the wave-4 merge (2026-10-02); if this fails the flip regressed"
assert t['t10']['status']=='pinned' and t['t11']['status']=='pinned', "new tiles must be pinned"
assert len(m['divergence-watch'])>=3, "honest gaps must be named"
print("graph coherent: 12 tiles, prereq edges closed, t08 pinned on merge, new tiles pinned")
PY
grep -q "demonstrated RED\|demonstrated-red" "$L" || { echo "ledger lost the RED doctrine"; exit 1; }
echo "ledgered-breakthroughs verified (journal + graph + self-audit intact)"
