#!/usr/bin/env bash
# Deploy experiment-proxy. Requires (in the environment, NOT pasted in chat):
#   CLOUDFLARE_API_TOKEN  — perms: Workers Scripts:Edit + Secrets Store:Read
#   CLOUDFLARE_ACCOUNT_ID
# The upstream keys stay in the account Secrets Store; this script never reads
# or prints their plaintext. It only wires the bindings by reference.
set -euo pipefail
cd "$(dirname "$0")"

: "${CLOUDFLARE_API_TOKEN:?set CLOUDFLARE_API_TOKEN (Workers Scripts:Edit + Secrets Store:Read)}"
: "${CLOUDFLARE_ACCOUNT_ID:?set CLOUDFLARE_ACCOUNT_ID}"

echo "==> resolving Secrets Store id"
# Parse the store id from wrangler's listing (id column). Adjust if your account
# has multiple stores — pass STORE_ID=... to override.
STORE_ID="${STORE_ID:-$(npx --yes wrangler secrets-store store list 2>/dev/null \
  | grep -oE '[0-9a-f]{32}' | head -1)}"
[ -n "${STORE_ID:-}" ] || { echo "!! could not resolve STORE_ID — run: npx wrangler secrets-store store list"; exit 1; }
echo "    store id: ${STORE_ID:0:6}… (redacted)"

echo "==> writing store id into a deploy copy of wrangler.jsonc"
sed "s/<STORE_ID>/$STORE_ID/g" wrangler.jsonc > wrangler.deploy.jsonc

echo "==> setting PROXY_TOKEN (the caller's gate) if not already set"
# Generate a strong gate token; keep it in the deploy session's env as PROXY_TOKEN
# so you can call the proxy. Never commit it.
if [ -z "${PROXY_TOKEN:-}" ]; then
  PROXY_TOKEN="$(openssl rand -hex 24)"
  echo "    generated PROXY_TOKEN (export it in your shell to call the proxy):"
  echo "    export PROXY_TOKEN=$PROXY_TOKEN"
fi
printf '%s' "$PROXY_TOKEN" | npx --yes wrangler secret put PROXY_TOKEN --config wrangler.deploy.jsonc

echo "==> deploying"
npx --yes wrangler deploy --config wrangler.deploy.jsonc

echo "==> done. smoke test:"
echo "    curl -s -H \"Authorization: Bearer \$PROXY_TOKEN\" https://experiment-proxy.<your-subdomain>.workers.dev/health | jq ."
echo "    curl -s -H \"Authorization: Bearer \$PROXY_TOKEN\" https://experiment-proxy.<your-subdomain>.workers.dev/moth/healthz"
