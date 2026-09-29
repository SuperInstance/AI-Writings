#!/usr/bin/env bash
# run_all.sh — one command to (re)build the inter-relational corpus from scratch.
# Backfill the ledger → fold in the live transcripts → verify every chain → write
# situations/corpus/ tables → print the base rate a learned cell must beat.
# Zero external deps (Python stdlib). MicroMoth-quilt is optional (only draw_local
# needs it); set MICROMOTH_QUILT to a clone to exercise the local dice.
set -euo pipefail
cd "$(dirname "$0")"

echo "== recorder self-test (chain + tamper-evidence) =="
python3 recorder.py >/dev/null && echo "  ok"

echo "== backfill corpus from the dispatch-ledger =="
python3 ledger_to_transcript.py

echo "== build model-ready tables (verifies every chain) =="
python3 corpus.py

echo "== base rate a learned cell must beat =="
python3 baseline_decompose.py

echo "== done: situations/corpus/{decompositions,routes,judgments}.jsonl =="
