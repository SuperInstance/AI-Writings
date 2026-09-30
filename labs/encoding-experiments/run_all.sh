#!/usr/bin/env bash
# Run every encoding experiment's selftest (offline, fast), then — with --measure — every
# measurement. Measurements are offline too except E6, which replays cached DeepInfra
# answers from data/cache_chat.jsonl and only calls the API on a cache miss.
set -euo pipefail
cd "$(dirname "$0")"
EXPS="vec_index hdc_theorems delta_budget ecc_chain entropy_corpus godel_cellgraph quipu_projection holos_flock encoding_routes adinkra_code"
fail=0
for e in $EXPS; do python3 "$e.py" --selftest || fail=1; done
if [[ "${1:-}" == "--measure" ]]; then
  for e in $EXPS; do echo; python3 "$e.py"; done
fi
exit $fail
