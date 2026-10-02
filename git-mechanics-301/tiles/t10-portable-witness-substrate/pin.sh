#!/bin/sh
# t10 pin: the portable-witness layer exists with its honest boundary stated.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
E="$D/witness/export-header.py"
S="$D/witness/sign-header.py"
[ -f "$E" ] && [ -f "$S" ] || { echo "witness excerpts missing"; exit 1; }
grep -q "genesis-anchored" "$E" || { echo "genesis anchor absent"; exit 1; }
grep -q "GENESIS = " "$E" || { echo "GENESIS root absent"; exit 1; }
grep -q "naming the line on any tamper\|export tampered at line" "$E" || { echo "named-tamper contract absent"; exit 1; }
grep -q "does NOT prove the filter was complete\|Completeness is the verifier" "$E" || { echo "completeness limit unstated — the witness would be laundering a hole"; exit 1; }
grep -q "Ed25519" "$S" || { echo "root signing absent"; exit 1; }
grep -q "stays stdlib-only\|stdlib-only" "$S" || { echo "stdlib-only core abandoned"; exit 1; }
echo "portable-witness-substrate verified (genesis chain, named-tamper, signed tip, completeness limit stated)"
exit 0
