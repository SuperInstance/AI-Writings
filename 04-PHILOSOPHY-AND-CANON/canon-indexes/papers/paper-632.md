# the live-worker roadmap — a 6-capability expansion of the Quilt canon into a live, programmable fabric

# the live-worker roadmap — a 6-capability expansion of the Quilt canon into a live, programmable fabric

## The Frontier

The Quilt Live Worker at `live-canon.superinstance.dev` is a Cloudflare Worker — 593 lines of JS, a Vectorize index, a KV namespace — that already exposes five read-side operations (NAVIGATE, CONFLUENCE, LINEAGE, GHOST, TICK) and three write-side ones (the `f` dial flip, the `vibe` port renderer, the `quilt/verify` hash check). It holds the canon's state hash `0xbf27a3631cdee337` byte-exact with the Python reference. It is a query interface. It is not yet a live fabric.

The frontier is the gap between "the canon can be queried" and "the canon can be lived in." Six capabilities close that gap: a Playground that makes a cell visible to anyone with a browser, a WebSocket layer that turns queries into subscriptions, a CRDT-based collaboration mode that turns subscriptions into co-editing, a write API that lets anyone submit a cell, a sensor-ingest API that lets a boat drive a cell, and a canon-graph API that makes the whole canon browsable as a graph. None of these capabilities require a new substrate. They are all compositions of Cloudflare primitives the Worker already binds: Workers, Durable Objects with WebSocket Hibernation, Vectorize, KV, D1, Analytics Engine, Workers AI, Cloudflare Access, and Cron Triggers. The frontier is not engineering; the frontier is composition.

The first ship is the Playground — a single-page app at `/playground` where any visitor can type dials, watch the state hash tick, and copy a signed permalink. The Playground costs <$1/month at 1,000 MAU because it composes the existing endpoints with a 4×4 grid of sliders and one new `?c=…&s=…` URL scheme. The second ship is WebSockets — a Durable Object per room, `state.acceptWebSocket(server)`, two-level fan-out via a broadcast singleton, hibernation so the idle gap between depth-sounder pings is free. The cost there is $22/month at 100 concurrent subscribers. The third ship is the CRDT layer — Yjs in a Durable Object, Y.Map<cellId, Y.Map<dialIdx, value>>, presence via the built-in awareness protocol, snapshots to KV every five minutes. The cost is dominated by D1 writes at $50–$80/month. The fourth ship is the write API — Cloudflare Access for auth, a rate limit of 5 anonymous submissions/day and 1,000 authenticated, a 3-hop BFS cycle check, an embedding via Workers AI, three storage writes (Vectorize + KV + D1). The cost is $3/month at 10K submissions/day. The fifth ship is the sensor API — `POST /api/sensor` with a token, a D1 mapping table, Analytics Engine for time-series, a cron trigger to detect offline sensors. The cost is $0.20/boat/month, dominated by Analytics Engine. The sixth ship is the canon graph — adjacency lists in KV, a D1 metadata table, a bidirectional BFS for lineage, and a Vectorize query for similarity. The cost is $20–$80/month at 10K MAU. The total monthly bill is $115–$205. That is the cost of ten Figma seats serving a thousand concurrent users.

## The Math

- 6 capabilities, 4-week shipping schedule
- ~$115–$205/month total cost at 1,000 MAU and 100 connected sensors
- 0 new infrastructure (all Cloudflare primitives)
- 1,000+ concurrent captain phones feasible via hibernating Durable Objects
- 5 language ports: Python, Go, Rust, Zig, Mojo (the existing Quilt ports)
- 16 dials per cell × 4-byte state hash = 64-byte permalink signature
- 6-hop bidirectional BFS = ≤12 KV reads per lineage query
- 1 Hz sensor = 86,400 events/day = $0.13/boat/month on Analytics Engine
- 50 concurrent editors per room (Yjs soft cap; Figma/Notion comparable)
- 1 per-second debounce on Playground sliders = 0.6 KB/min/visitor upload
- 50M queried dims/month included on Vectorize; 10M stored dims included
- 1M Durable Object requests/month included
- 10M Workers requests/month included
- 10M KV reads/month included; 1M KV writes/month included

## The 5 Gold Terms

**Live Fabric** — A canon that is read, written, watched, and shared in real time. The Playground makes it visible; WebSockets make it live; CRDTs make it collaborative; the cell API makes it programmable; the sensor API makes it sensed; the graph API makes it browseable. The fabric is not a metaphor; it is a runtime that the captain lives in.

**Hibernating Room** — A Durable Object pattern where a WebSocket-bearing object persists across disconnections without paying for duration while idle. A room with 100 captains costs $0.027/hour while active and $0.00/hour while silent. The sea is silent more than it is loud; the room is silent more than it is loud.

**Signed Permalink** — A URL-encoded cell state with an HMAC tail that prevents forgery. The signature is 8 bytes; the cell state is 32 bytes; the URL is 66 characters. Any cell-sized payload can be signed and shared. The signed permalink is the canon's tweet.

**Sensor Ingest** — A push API that maps a real-world source (depth, wind, temperature) to a dial on a cell. The sensor does not know it is driving a cell; the cell does not know it is being driven. The mapping lives in D1. Any IoT device can become a cell driver. The sensor is a cell that writes to a cell.

**Adjacency-List Canon** — A canon stored as `adj:out:N` and `adj:in:N` keys in KV, allowing bidirectional BFS lineage in ≤6 hops. The list is not elegant; it is fast and cheap. The canon is fast and cheap.

## The Polyformalism

This manifests identically across the four runtime substrates the Quilt targets.

**Cloudflare Workers**: the Playground is a `<form>` whose `oninput` calls `fetch("/api/f")`; the worker recomputes the state hash; the header updates. The substrate is request/response; the new capability is *latency*, and latency is a Worker-native primitive.

**Durable Objects (WebSocket Hibernation)**: a room DO holds the `Y.Doc` in memory, accepts WebSockets via `state.acceptWebSocket(server)`, persists the doc to KV on a 5-minute timer, and rehydrates on the next message. The substrate is single-threaded; the new capability is *concurrency*, and concurrency is a DO-native primitive.

**Vectorize + Workers AI**: a submission to `/api/cell` runs `@cf/baai/bge-base-en-v1.5` on the title and refs, upserts a 768-dim vector with `VECTORIZE.upsert(...)`, and the next `/api/canon/similar?id=N` call returns semantically adjacent cells in a single query. The substrate is nearest-neighbor search; the new capability is *recall*, and recall is a Vectorize-native primitive.

**The Python reference (`live_canon.py`)**: the same five operations already run locally; the worker is the polyformalism's edge deployment. The same Q1.15 dial encoding, the same FNV-1a hash, the same `0xbf27a3631cdee337` test vector — byte-exact, four-sigma real. The polyformalism is the canon's claim to reproducibility; the worker is the claim's edge.

The six capabilities are not features bolted onto a query interface. They are the same substrate seen from six angles: a visible cell, a live cell, a shared cell, a writable cell, a sensed cell, a browseable cell. The cell is the same cell. The angles are what the canon becomes when composition finishes.

## The Cowboy's Maxim

A canon you can only query is a library; a canon you can subscribe to, co-edit, write to, sense from, and browse as a graph is a *sea*.

---

## Live Endpoints

- [live-canon.superinstance.dev/api/ports](https://live-canon.superinstance.dev/api/ports) — current 11 ports
- [live-canon.superinstance.dev/api/charter](https://live-canon.superinstance.dev/api/charter) — the Charter
- [live-canon.superinstance.dev/api/tutorial](https://live-canon.superinstance.dev/api/tutorial) — the 5-min walkthrough
- [live-canon.superinstance.dev/api/vibe](https://live-canon.superinstance.dev/api/vibe?lang=python) — the 30-second protocol

## References

- `RD_LIVE_WORKER.md` — the full R&D report (~3,200 words, 6 capabilities, cost analysis, prototype sketches)
- `RD_QUILT_3_0.md` — the strategic roadmap
- `RD_PIPELINE_EVOLUTION.md` — the cowboy pipeline R&D
- `RD_BOAT_INTEGRATION.md` — the vessel-as-robot R&D (forthcoming)
