# The Cloudflare backend pattern — live JEV/Moth wow, on a few-cents-per-visitor budget

*Owner directive, 2026-09-28: "on the backend, cloudflare apps can be using JEV and moth from
the secrets store. so web apps can be using them in the backend where they greatly enhance the
presentation and wow factor. remember, we want [each] user to get a few cents worth — enough to
try tools and get an ah-ha moment but not enough to abuse the connection." This is the pattern for
every SuperInstance web app (cargo-line first). It supersedes "static bundle only" for the
wow-tier features while keeping the offline-first core intact.*

## The shape

```
 Browser (static, offline-first)          Cloudflare edge                 Upstream
 ────────────────────────────────         ─────────────────────          ────────────
 cargo-line dist/  ──same-origin──▶  Pages Function /api/*  ──secret──▶  typesafe.ai (JEV)
 (no keys, ever)     fetch()          - reads key from            └────▶  mothquantum (Moth:
                                        Secrets Store binding               QRNG + media)
                                      - per-visitor budget bucket (KV/D1)
                                      - validate + rate-limit + book cost
                                      - degrade gracefully when spent
```

- **Keys never reach the client.** JEV/Moth keys live in the **Cloudflare Secrets Store**, bound
  to the Pages Function / Worker (server-side only). The browser only ever calls **same-origin**
  `/api/jev`, `/api/moth/*` — it never sees a token. (This is exactly what `tools/experiment-proxy`
  already does as a gated pass-through; this doc adds the per-visitor budget + graceful degrade to
  make it public-facing.)
- **Offline-first stays true.** The game is fully playable with the backend OFF or a visitor's
  budget spent — the live calls are *enhancements* (wow), never load-bearing for play.

## What the backend buys (the wow features)

- **Live JEV** — a real judgment on the player's own work: "rate my chart / my route" (honesty +
  quality score), or scoring a shared mid-state's fun-floor, rendered as a crisp verdict the
  static bundle can't produce. JEV is fully mapped + reliable (see `JEV-FINDINGS.md`), competent
  on everything except character-counting.
- **Moth QRNG** — provably-fair, quantum-random procgen seeds: "your chart's randomness is
  quantum-verifiable" is a genuine, honest wow no other tycoon game has. (Moth = QRNG + media,
  NOT a text grader — `ROSTER-ORCHESTRATION.md`.)
- **Moth media** — on-demand generated art/textures for a shareable moment (a rendered "your
  voyage" card), where dynamic beats static.
- *(Asset generation — FLUX — stays a BUILD-time pipeline, not a per-visitor cost: bake the art
  into the bundle. Only truly per-user media should be a live backend call.)*

## The budget cap (the anti-abuse — the load-bearing constraint)

Each visitor gets **~a few cents** of live API — enough for the aha moment, not enough to drain.

- **Token bucket per visitor** in Cloudflare **KV** (or D1), keyed by a first-party session
  cookie **+** a hashed IP (defeats cookie-clearing), refilled slowly. Example budget:
  ~20–40 JEV calls **or** a handful of Moth media gens per rolling window → target **$0.02–$0.05
  per visitor**. (JEV is cheap; Moth media is the pricier line — cap it hardest.)
- **Two ceilings:** the per-visitor bucket **and** a global per-day spend ceiling as a backstop
  (so a botnet can't run the bill up past a fixed daily cap; over it, everyone degrades to static).
- **Graceful degrade, never a hard wall:** when a visitor's budget is spent, the app keeps
  playing on its offline logic and shows a gentle "you've used today's live credits — the game
  plays on; come back tomorrow for more live scoring" — the aha already happened.
- **Server-side enforcement only** (never trust a client counter): the Function checks + decrements
  the bucket *before* calling upstream, books the actual cost after, caps request size and rate,
  and is same-origin CORS only. No key is ever echoed; every call is booked to KV for replay.

## Cost accounting (book it, like everything)

Each `/api/*` call books `{visitor_hash, tool, upstream_cost, ts}` to KV/D1 so spend is a
*measured, replayable* quantity (the org's own metabolism discipline, applied to user-facing
API spend). Tune the caps from the real numbers, not a guess.

## Dependencies / status

- **JEV backend: ready** — API fully mapped (`POST api.typesafe.ai/v1/systemone`), key in Secrets
  Store; the Function wraps it.
- **Moth backend: BLOCKED on Moth's API spec** — the server is reachable but every guessed route
  404s (`ROSTER.md` liveness). Need the real endpoint + request schema for QRNG and media before
  wiring Moth. (Owner to provide, or point at a Moth client.)
- **Cloudflare deploy of a Pages Function** needs the Secrets Store bindings configured on the
  `cargo-line-tycoon` Pages project + `CF_API_TOKEN` (have it). The experiment-proxy `wrangler.jsonc`
  is the binding template.

## Where this lands in the plan

This is a **P1/P2 wow layer** on top of the fun (P0) + graphics (P1) work in
`CARGO-LINE-FUN-AND-GRAPHICS.md`: ship the fun, bake the art, *then* add the live-JEV "rate my
chart" and Moth "quantum seed" as the budgeted backend wow. Fun and offline-play never depend on it.
