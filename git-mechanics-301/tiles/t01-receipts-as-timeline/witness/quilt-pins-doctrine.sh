#!/usr/bin/env bash
# tests/pins_quiltgit.sh — FAIL-first pin harness for the quilt-in-git PoC.
#
# Plain bash + git + awk. No bats, no network. Every pin runs in its own
# scratch repo under /tmp (one mktemp -d root, one subdir per pin), so pins
# cannot leak state into each other.
#
#   P1  dial commit  -> .quilt/receipts/<short>.json exists (holds commit
#                       hash + alias) and .quilt/watch.log grows by EXACTLY
#                       one line.
#   P2  freeze       -> dial 15 = 0.8 commits; the NEXT commit touching that
#                       cell is rejected (exit 1, "frozen" in the error,
#                       file/HEAD unchanged).
#   P3  cascade      -> a.dials/1 = 0.9 and b's links say "a 0.5"; ticking a
#                       gives b.dials/14 == 0.45 and a "quilt: cascade after"
#                       commit.
#   P4  rewind       -> change a dial, commit, checkout the previous commit
#                       for cells/<alias>/ -> dial file back to old value.
#   P5  clone        -> in a fresh clone hooks do NOT fire (no receipt, no
#                       watch line); after quilt-init they do.
#   P6  non-cell     -> a README-only commit creates NO receipt and NO
#                       watch.log line.
#   P7  notes        -> a tick also leaves a receipt NOTE on the commit
#                       (git notes --ref=quilt/receipts): JSON with the full
#                       commit hash, the alias, a 16-hex sig, byte-identical
#                       to .quilt/receipts/<short>.json.
#   P8  audit+ride   -> quilt-audit lists every noted cell commit's receipt;
#                       file receipts do NOT cross a clone, noted ones DO
#                       (quilt-init wires the fetch refspec) and the sig
#                       still verifies in the clone.
