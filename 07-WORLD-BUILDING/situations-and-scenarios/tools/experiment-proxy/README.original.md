# experiment-proxy

A gated Cloudflare Worker that lets the dispatcher experiment with the
**typesafe.ai** and **mothquantum.com** APIs **without ever holding the keys**.

## The security model (why this shape)

The upstream credentials — `MOTHQUANTUM_BASE`, `MOTHQUANTUM_KEY`, `TYPESAFEAI_KEY`
— live in the Cloudflare account **Secrets Store** and are **write-only**: no API,
tool, or account owner can read their plaintext back (by design). This Worker
binds them **by reference** (`secrets_store_secrets` in `wrangler.jsonc`), so:

- the plaintext exists only inside the Worker's runtime, never in this repo, never
  in the deploy environment, never in the dispatcher's session;
- the caller (the dispatcher) authenticates with a **separate** `PROXY_TOKEN` and
  only ever sees the upstreams' *responses*;
- the key is injected onto the outbound request and never echoed back.

It's a generic pass-through because neither API's authenticated surface is
publicly discoverable — so we forward whatever path we're given and map the API
at runtime.

## Routes

- `GET /health` — open; reports liveness and whether your bearer is valid.
- `ANY /moth/<path>` — → `${MOTHQUANTUM_BASE}/<path>` with `MOTHQUANTUM_KEY`.
- `ANY /ts/<path>`  — → `${TYPESAFE_BASE|https://api.typesafe.ai}/<path>` with `TYPESAFEAI_KEY`.

Query strings pass through. Auth style per upstream is a var (`MOTH_AUTH_STYLE` /
`TS_AUTH_STYLE`): `bearer` (default), `x-api-key`, or `query`.

## Deploy (needs Cloudflare write credentials — the only remaining blocker)

Add these to the **environment settings** (title-bar env menu → Edit; a new
session picks them up). Do **not** paste tokens into chat.

- `CLOUDFLARE_API_TOKEN` — permissions: **Workers Scripts: Edit** + **Secrets Store: Read**
- `CLOUDFLARE_ACCOUNT_ID`

Then:

```bash
bash situations/tools/experiment-proxy/deploy.sh
```

`deploy.sh` resolves the Secrets Store id, sets a random `PROXY_TOKEN` gate,
wires the bindings by reference, and deploys. It prints the `PROXY_TOKEN` once so
you (or the dispatcher, in-session) can call the proxy; it is never committed.

## Use (after deploy)

```bash
curl -s -H "Authorization: Bearer $PROXY_TOKEN" \
  https://experiment-proxy.<subdomain>.workers.dev/health | jq .

# discover the mothquantum surface at runtime (key stays in the Worker)
curl -s -H "Authorization: Bearer $PROXY_TOKEN" \
  https://experiment-proxy.<subdomain>.workers.dev/moth/healthz

# same for typesafe
curl -s -H "Authorization: Bearer $PROXY_TOKEN" \
  https://experiment-proxy.<subdomain>.workers.dev/ts/
```

## Alternative: reuse an existing Worker

If a Worker already binds these keys and exposes a route, point the dispatcher at
its URL + gate token instead — no deploy needed. (`ta-bridge` is *not* it: it's a
game-lessons pipeline using its own `TA_URL`/`TA_TOKEN`, unrelated to these keys.)
