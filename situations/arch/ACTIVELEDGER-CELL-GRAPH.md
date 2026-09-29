# ActiveLedger & the Relational Cell Graph — vision + sequenced build plan

**Status:** living charter. Written 2026-09-29 by the dispatch fleet (opus-4.8) from Casey's
vision dump. This is the anchor doc: it holds the vision AND the ordered build backlog so any
session can drop context and resume from here. Update the backlog table (§6) as items ship.

---

## 0. One-line

The SuperInstance is **one quilt of many embedding quilts**. Its first-class citizens are not data
but **cells** and the **relational logic between them**. Routing between cells is **double-entry
bookkeeping**: value leaves one cell's ledger in its own units and arrives in another's units, and
the **ActiveLedger is the tensor that holds the translation** between those units. We do not seek
the *best* route. We seek **what is preferred when** — because many routes to the same answer make
the system durable.

## 1. The thesis — anti-GAN, novelty-in-process, identity-in-product

A GAN converges two nets toward one equilibrium. We do the opposite. We are **thirsty for novelty
in *process*** while holding the **product invariant**. Given the same product (a value, a rendered
frame, a verdict), we want *many genuinely different processes* that reach it. Then:

- **Durability** = redundancy of route. If one route degrades (a model drifts, a device throttles,
  a key expires), another already produces the identical product.
- **"Preferred when," not "best."** Each route has a regime where it is preferred (cheapest,
  lowest-latency, most-robust, most-explainable). The system's job is to learn the *preference map*,
  not to crown a winner. A winner is brittle; a preference map is a hedge.
- This is why the fleet's verifier cells matter: to say "same product" you need an **un-gameable
  oracle** (see `kernel-oracle-mutant-gauge`, `wasm-native-drift-differ`, shipped 2026-09-29). The
  oracle certifies product-identity; the ActiveLedger then ranges freely over process-novelty.

Existing labs that already serve this thesis: `dominated-novelty-search`, `qd-arena` (quality-
diversity: keep the diverse-and-good, not the single-best), `jev-fold`/`weakest-claim` (decompose a
verdict), `situation-recorder` (hash-chained receipts of *how* a judgment was made).

## 2. Cells as first-class citizens

A **cell** is any bounded transformer of value with its own internal bookkeeping: a code function,
a file, a shell command, an SLM/LLM call, a RAG agent, a game-engine step, a **physical box** (real
hardware in the loop), or a **simulation of any of these**. A cell exposes:

- an **intra view** (ActiveLog): what it is doing *inside*, projected to whatever is valuable to the
  observer. An STT cell's intra view shows *words*, not matmuls — you only zoom to matmuls for
  maintenance. An LLM cell shows chain-of-thought. A filter cell shows a confidence indicator.
- an **inter face** (ActiveLedger): what it debits/credits on its routes, in its own units.

The relational graph of cells — who can route to whom, and in what units — is the first-class
object. The data flowing through is a *state of routing*, not the substance.

## 3. The ActiveLedger — double-entry routing as a tensor

Every route hop is a double-entry transaction: cell A **credits** an output in A's units; cell B
**debits** an input in B's units. The **routing book** holds the **translation** A-units → B-units.
That translation spreadsheet *is* the routing code.

The ActiveLedger is a **tensor**, not a flat book:

- It has **separate pages** whose **planes intersect but need not be orthogonal**, and need not
  share the same curvature. A quantity can appear on one page and not another because each
  bookkeeper measures in the context of *what its application perceives for*.
- Example: a **vibration** shows up as **heat** on the thermal page but is **not heard** on the
  listener page, because the listener cell's units are *perceived sounds within its application
  context*. Same physical event, different ledger pages, no contradiction — the tensor just doesn't
  require the planes to be at right angles.

### 3.1 Worked example (the canonical route)

`microphone → [speech/noise pre-filter] → STT → [grammar cleanup] → [RAG context] → [pincher] →
[game-engine action] → LLM`

- The **pre-filter** is itself a cell (algorithmic, or a tiny model, or a shell to a physical
  filtering box, or a simulated dynamic filter). It drops "obviously not speech," so the STT cell's
  model requirement **shrinks** — it gets a first-pass-filtered input. The ledger records
  speech/noise/nothing with a **confidence** entry.
- On the way to the LLM, a chain of filter cells light up: grammar-cleanup SLM, a RAG agent adding
  context, a **pincher-agent** that grows to know when to *pinch off the route and return the known
  answer* (a learned early-exit), a game-engine that supplies physics/world-sim/system-prompt/
  character context.
- The LLM cell shows chain-of-thought in its intra view. The ActiveLedger view shows the whole
  filter pipeline as pre/post cells around the process.

## 4. The two synoptic views — yin & yang

Seen **from outside the matrix** by a **viewing cell** that has its own filter for making cell
activity as valuable as possible to a human:

- **ActiveLog view** — the cells' **intra-workings** across tables (the yin, projected *in*).
- **ActiveLedger view** — the **pipelines and routes** porting around the cells, the inter-workings
  (the yang, projected *out*).

Both rendered in the **same synoptic spreadsheet format**: a tensor array the operator can **query
by any 2D dimension**, sorting the data as a spreadsheet projection, then **tick-wait for insight,
rewind, and simulate**. Surfaces: file output, browser real-time render with rewind, a low-level
TUI, or a first-person **"plato-room"** for an agent-operator who sees who he's connected to.

**This makes grepping a broad simulation obsolete** — you don't search logs, you *project the
tensor* along the dimension you care about and watch it tick.

## 5. Dovetail with the GPU agent "on the metal"

Read of the GPU agent's work: bit-exact kernel work on real hardware — MicroMoth-quilt and Syzygy
(the `0x6dbdd1a8` golden, fused passes, native-vs-wasm), pushing Moth-quantum simulation to its
limits *before* reaching for the IonQ API. He produces **many kernel routes** (algorithms, tilings,
precisions) that must yield the **bit-identical product**.

Our job around him: build the **cell/route/preference scaffolding** so his many-routes-to-one-
product work becomes a durable, queryable, rewindable relational graph.

- His differ/gauge cells certify "same product."
- Our ActiveLedger records **which kernel route is preferred when** (by size, sparsity, device
  state) — the preference map, not a winner.
- We hand him **example workflows and PoCs** to try on metal.

## 6. Build backlog — dependency-ordered (temporal plan)

Each PoC states its **product-invariant** (what must stay identical) and its **novelty-in-process**
(what must differ). The order below is chosen so **each step consumes a frozen prior artifact and
adds exactly one new thing** — nothing downstream needs rejigging. Build in this order; push each on
its own branch; book a ledger row + situation receipt; then update the status.

Steps are numbered by **build order** (B1..). The `P#` id is a stable name; `depends on` is what must
be frozen first.

| build | id | cell / tool | depends on | product-invariant | novelty-in-process | status |
|---|---|---|---|---|---|---|
| B1 | P1 | `activeledger` (labs) — double-entry routing book + **frozen record schema** (transaction, unit-translation tensor, recorded-run JSONL) + canonical mic→filter→STT→LLM route simulated; confidence + STT-load-reduction recorded | shipped differ/gauge (oracle) | the transcript out of the route | the pre-filter path taken | **BUILDING (self)** |
| B2 | P5 | `unit-translation-audit` (labs) — receipt idiom over §3 translations: prove A→B units round-trip or document the lossy hop, so the tensor pages are trustworthy **before** anything builds on them | P1 schema | the value across a round-trip | the page/plane | TODO |
| B3 | P4 | `pincher` (labs) — a **second real route**: learned early-exit cell that grows a threshold for when the cheap known answer suffices, else falls back to the full route | P1 schema (posts transactions) | pinched answer == full-route answer within tolerance | pinch vs full | TODO |
| B4 | P2 | `route-preference` (labs) — with ≥2 product-identical routes (P1 + P4) certified equal by the differ, learn/record which is *preferred when* over a regime grid. GPU-agent-facing. Consumes rubric-forge's dense reward as the preference score. | P1 schema, P4 (2nd route), differ, **rubric-forge** | the computed output | which of k routes | TODO (dispatch 5.5) |
| B5 | P3 | `synoptic-view` (artifact) — browser spreadsheet projection of the ActiveLog + ActiveLedger tensor, query-by-any-2D-dim, tick, rewind. Renders the **finished** data model (P1+P4+P2). | frozen schema + real runs from P1/P4/P2 | the recorded run | the projection dimension | TODO |
| B6 | P6 | quantum reach — once MicroMoth-quilt is maxed, an IonQ-API cell as one more *route* to a product a classical route already yields (durability, not novelty for its own sake) | P2 preference map | the product a classical route yields | classical vs quantum route | LATER |

### 6.1 Why this order (so it doesn't get rejigged)

1. **B1 freezes the schema.** The ActiveLedger transaction + unit-translation tensor + recorded-run
   format is the load-bearing artifact. Everything else reads/writes it, so it is built and frozen
   first. Its demo (one route) matters less than the schema being stable.
2. **B2 audits the foundation before the tower.** If translations are lossy or wrong, every page of
   the tensor is on sand. Validate round-trips *immediately after* B1, *before* piling routes and
   views on top — this is the single biggest rejig-avoider.
3. **B3 adds a second real route.** You cannot have a "preferred when" map with one route. The
   pincher is the cheapest way to get a genuinely different second route to the same product.
4. **B4 needs ≥2 routes + the oracle + a dense score.** Only now can "preferred when" be learned.
   rubric-forge (in flight) supplies the dense reward; it lands before/with B4 by design, not luck.
5. **B5 renders last.** A viewer built before the data model is finished gets rejigged on every
   schema growth. Build it once the tensor's shape is settled by B1–B4.
6. **B6 is gated on MicroMoth-quilt being maxed** — quantum is one more route for durability, not a
   detour; it only makes sense once the classical preference map exists to hedge against.

**Rule (Casey):** every experiment must do something *new* — do not re-run a prior design. Novelty
in process is the point; the product staying identical is the proof it worked.

## 8. Scouting gate (runs BEFORE B1 schema-freeze)

Casey's rule: **don't reinvent the wheel, and follow prevailing UX so we fit and integrate
seamlessly.** So B1's schema-freeze is *gated* on two scouts landing first — otherwise we'd freeze a
home-grown format and rejig it later to match what the world already does.

- **Scout A — internal (SuperInstance org).** Inventory every org repo for primitives we'd otherwise
  reinvent: existing ledger/routing/cell-graph/quilt/embedding/viewer code, the MicroMoth-quilt and
  Syzygy surfaces, any recorded-run or trace format already in use. Deliverable:
  `situations/scout/internal-inventory.md` — a table of {repo, relevant primitive, reuse-or-extend}.
- **Scout B — external (cutting edge / trending).** Survey the conventions our B1 record schema and
  B5 synoptic viewer should adopt: agent-trace / dataflow / pipeline observability UX (e.g. LangSmith,
  LangGraph Studio, Arize Phoenix, W&B Weave, Temporal UI, Dagster/Prefect, ComfyUI node graphs,
  OpenTelemetry span model), tensor/spreadsheet projection UIs, and double-entry ledger data models.
  Deliverable: `situations/scout/external-ux-conventions.md` — {convention, who uses it, how we adopt}.

**Gate:** fold both into a short "schema decisions" section, THEN freeze B1. Until then B1 stays at
skeleton (interfaces sketched, format not frozen).

## 7. Working discipline

- Doc-first, sequential. This file is the source of truth; free context to it.
- Push often. Many small, unique PoCs beat one big one.
- Every PoC: a `selftest` in the house idiom, a receipt (situation-recorder), a ledger row.
- The oracle (differ/gauge) certifies product-identity before any novelty claim is booked.
