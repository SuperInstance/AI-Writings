#!/bin/sh
# t08 pin: RED BY DESIGN. The wave-4 query layer is not shipped yet;
# this pin asserts the shipped evidence exists, so it MUST fail until then.
# When the layer lands: point this pin at the shipped witness, watch it go green.
set -u
D=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SHIP="$D/witness/shipped-receipts"
if [ -f "$SHIP" ]; then
  grep -q "trusted-but-unaudited" "$SHIP" || { echo "shipped witness lacks the subcommand evidence"; exit 1; }
  grep -q "FAIL-first" "$SHIP" && grep -q "GREEN" "$SHIP" || { echo "shipped witness lacks red-then-green receipts"; exit 1; }
  echo "wave-4 query layer shipped and witnessed — tile ready to pin"
  exit 0
fi
echo "DRAFT: wave-4 query layer not shipped; design contract only (witness/design-contract.md)"
exit 1
