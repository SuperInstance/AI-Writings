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
| B1 | P1 | `activeledger` (labs) — **thin adapter**: adopt ActiveLog v1 envelope, define types `cell.tick`/`route.hop`/`ledger.transaction`, wrap `cell-runtime` `DoubleEntry`, book the canonical mic→filter→STT→LLM route + OTel projection. No new format. | ActiveLog v1, cell-runtime, differ/gauge | the transcript out of the route | the pre-filter path taken | **DONE — Sonnet 5.5, selftest 28/0, 60% STT load cut, landed on main** |
| B2 | P5 | `unit-translation-audit` (labs) — wrap `quilt-studio` `EFFECT(forward,inverse)`: prove each hop sums to zero after translation (round-trip) or document the lossy hop, so the tensor pages are trustworthy **before** anything builds on them | P1 schema, **quilt-studio** | the value across a round-trip | the page/plane | **DONE — Sonnet 5.5, selftest 34/0, run over the example quilts' real hops, landed on main (d145)** |
| B3 | P4 | `pincher` (labs) — wrap `quilt-pincher` as a **second real route**: learned early-exit that grows a threshold for when the cheap known answer suffices, else falls back to the full route | P1 schema, **quilt-pincher** | pinched answer == full-route answer within tolerance | pinch vs full | TODO |
| B4 | P2 | `route-preference` (labs) — wrap `pareto-tournament` + `hebbian-router`: with ≥2 product-identical routes (certified equal by the differ), place each on the **iron-triangle** {good, fast, cheap} from its budget vector + rubric-forge dense reward, and record which is *preferred when*. Not a scalar winner (§11). GPU-agent-facing. | P1 schema, P4, differ, **rubric-forge, pareto-tournament, hebbian-router** | the computed output | which of k routes | TODO (dispatch Sonnet 5.5) |
| B5 | P3 | `synoptic-view` — extend `quilt-view` + OTel export: Phoenix-style pivot table (project tensor by any 2D dim) + Temporal/LangGraph tick-scrubber with rewind/fork over the **finished** model (P1+P4+P2) | frozen schema + real runs, **quilt-view** | the recorded run | the projection dimension | TODO |
| B6 | P6 | quantum reach — `MicroMoth-quilt` as a *superposed route* (§10.4): let the preference map hold amplitude, collapse at the settle tick; IonQ only once the classical map exists to hedge | P2 preference map, **MicroMoth-quilt** | the product a classical route yields | classical vs quantum route | LATER |
| B7 | P7 | `system2-backtest` (labs) — **System-2 evaluator**: replay historical ActiveLog runs against an *alternative* network and score both on the budget vector across the iron-triangle. Differ must certify product-identity BEFORE budgets are compared. Runs offline on the budgeted benchmark corpus — zero live cost. | P1 budget schema, ActiveLog history, differ | the product each recorded input yielded | the network being scored | **DONE — Sonnet 5.5, selftest 38/0, gates product-identity first then splits cheap into compute vs storage, real iron-triangle placements over all 5 example quilts, landed on main (d146)** |
| B8 | P8 | `system2-redesigner` (labs) — **System-2 proposer**: the slow cell that proposes alternative networks, runs B7 to A/B them, and promotes iron-triangle winners (better-faster / better-cheaper / faster-better, plus satisfice fallbacks) into B4's preference map | B7, B4 | the product | the proposed topology | TODO |

### 6.1 Why this order (so it doesn't get rejigged)

1. **B1 freezes the schema — by ADOPTING ActiveLog v1, not authoring one** (see §8). The load-bearing
   act is choosing the existing internal envelope and defining three namespaced types on it, so
   everything downstream reads/writes a format that already has a spec, a hash idiom, and internal
   users. Its demo (one route) matters less than the schema being stable.
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

## 7. Scouting gate — DONE (both scouts folded into §8)

Casey's rule: **don't reinvent the wheel, follow prevailing UX so we fit and integrate seamlessly.**
Two scouts ran before B1's schema-freeze (2026-09-29). Raw findings:
`situations/scout/internal-inventory.md` (Scout A, org) and `situations/scout/external-ux-conventions.md`
(Scout B, cutting edge). Decisions distilled in §8.

## 8. Schema decisions (scouts folded — this un-gates B1)

The headline: **we do not author a record format. Almost every layer already exists internally.**

**Record envelope — adopt internal `ActiveLog v1`** (`cocapn-foundation/activelog-spec`,
`schema/event.schema.json`). Append-only, `(dev,seq)`-keyed JSONL envelope
`{alv, dev, seq, ts, mono, type, body, fix?, prev?}` with set-union merge, monotonic clocks, per-device
sha256 `prev` chain, read-time corrections. Its law is **one envelope, many namespaced types** — so we
*add* types, never a new format:

- `cell.tick` — a cell's intra-step (ActiveLog / yin view). Body carries the cell's own-units state.
- `route.hop` — an inter-cell hop (ActiveLedger / yang view), as a **balanced double-entry**:
  `{credit:{cell,units,amount}, debit:{cell,units,amount}, price:<translation ref>}`.
- `ledger.transaction` — the settled/promissory record binding the two sides (see §9 async settle).

**Budget vector on EVERY record (required, since B1).** Each `cell.tick` and `route.hop` body carries
`budget = {wall_ms, tokens:{<api>:int}, usd, power_w?, mem_mb?, storage_bytes?, reqs}`
(simulated/estimated is fine if deterministic; `storage_bytes` splits into `{train, prod}` — see §11.3).
A route's total budget = the sum of ALL its records' budgets (cell.tick + route.hop — compute lives on the ticks, so hops alone would undercount; both `labs/activeledger` and EX1 sum all records). This is non-negotiable from day one because the
whole of §11 (System-2 backtesting + the iron-triangle preference) has nothing to score against unless
every historical run already recorded what it *cost* in time, tokens-per-API, dollars, power, local
requirements, and storage. The append-only ActiveLog thus doubles as a **budgeted benchmark corpus**.

**Reuse, don't rebuild (Scout A map):**
- **cell** = `cell-runtime` (Python) / `quilt-cell` (JS) — the 8-primitive cell, already shipping a
  `DoubleEntry` debit/credit primitive. B1 wraps this; it does not reimplement a ledger.
- **booked WAL** = `jev-quilt` — per-cell `(tick, state_hash, delta, decision_receipt)`, fnv1a-chained,
  replay≡live. Closest single repo to the whole vision; B1 aligns to its record.
- **B2 unit round-trip** = `quilt-studio`'s `EFFECT(forward, inverse)` contract — the inverse *is* the
  round-trip auditor; B2 wraps it instead of writing a new one.
- **B3 pincher** = `quilt-pincher`. **B4 preference** = `pareto-tournament` + `hebbian-router`.
  **B5 viewer** = `quilt-view` (rewindable). **B6 quantum** = `MicroMoth-quilt`. **anti-GAN thesis** =
  `quilt-gan` (tournament-not-gradient referee; "record changes, points don't").
- **hash idiom** = fnv1a-64 over canonical JSON (org canary `0x24a555471370b18d`); enforce record
  shapes in CI with `gauge`'s `receipt`/`tile` schemas.

**External interop — a projection, not the native store (Scout B).** ActiveLog v1 stays native; we add
an **export projection to OpenTelemetry spans + OpenInference semantic attributes** so Phoenix / Langfuse
/ Weave / Jaeger ingest our runs with zero custom code. Cell kinds map to OpenInference span-kinds
(LLM / TOOL / RETRIEVER / CHAIN / AGENT / GUARDRAIL) **extended as a superset** with our kinds
(FILTER / PHYSICAL / SIM / PINCHER) — extend the enum, never rename. Borrow LangSmith's `dotted_order`
as the single hierarchy+tick sort key, and Weave's Op-vs-Call split (versioned cell *definition* vs
recorded cell *run*). Routes follow beancount: a hop must **sum to zero after translation** — that
zero-sum check *is* B2.

**So B1 is now a thin adapter PoC**, not an engine: adopt the ActiveLog v1 envelope, define the three
namespaced types, wrap `cell-runtime`'s `DoubleEntry`, book the canonical mic→filter→STT→LLM route, and
emit an OTel projection. Schema is **frozen on ActiveLog v1** — B1 is un-gated.

## 9. The heterogeneous async cell fabric + the typesafe.ai learning loop

*(Casey's second layer — the substance under the routes.)*

Cells are not one kind of thing. A route hops through a **heterogeneous palette**, each cell an async
worker with read/write links to its neighbours:

- **typesafe.ai cells** — *abundant allowance; use liberally.* The high-ceiling tier that raises the
  quality of everything. Every builder is told (see `DISPATCH.md`) it has an extensive typesafe.ai budget.
- **cheap-fast SLM cells** — DeepSeek, and Gemini Flash **with thinking OFF + limited output** — for
  high-fanout, low-stakes subtasks (grammar cleanup, speech/noise pre-filter, classification, pinch
  candidates). Pennies each; the workhorses of wide routes.
- **MothQuantum cells** — `MicroMoth-quilt` and Moth-quantum tech, simulated or real, pushed to their
  classical limits before IonQ.
- **async-algorithm cells** — plain clever code (filters, comb, FFT) in their own cells, linked to
  read/write each other.

**The learning loop (this is the compounding move).** typesafe.ai is used *and observed*. Every abundant
top-tier call is recorded as a **demonstration** in the ActiveLog. A distillation cell (`skill-forge` in
the RD backlog) mines those demonstrations into **quilt-native templates** — route-templates and
reasoning-cards a *cheap* cell can then execute. This is "many routes to the same product" applied to
**cost**: the expensive route *teaches* a cheap route that reaches the same product; once the differ
certifies equivalence, the preference map (B4) shifts that work down the cost gradient. **Pay once at the
top, harvest cheap forever** — amortized intelligence. As the template library grows, larger and larger
use-collections become quilt-native by default, and the thing designs *its own* templates for the next
scale up.

## 10. Horizon — thinking further than the brief

*(Explicit extrapolation beyond what Casey stated, marked as such so it stays honest. Harvest what earns
its keep; discard the rest.)*

1. **The ledger is the scheduler.** Model each async leg as a **promissory** double-entry: a `route.hop`
   posts an unbalanced debit the moment a typesafe.ai / MothQuantum / SLM call is *issued*, and
   **settles** when it returns. Unsettled transactions are accounts-receivable; a route completes when
   its legs settle. Asynchronous composition then needs no separate orchestrator — the append-only book
   *is* the scheduler, and rewind/replay is free because settling only appends.

2. **It is more than a neural network — the wiring diagram is the memory.** A NN has fixed
   gradient-learned weights. Here the links renegotiate by **earned standing** (`hebbian-router` already
   exists): "weights" are *booked per-context* ("preferred when"), not backprop'd once. Learning = writing
   the routing book, and it is auditable and rewindable. The topology *is* the memory; there is no separate
   weight store to drift out of sync with the trace.

3. **Routes as a market; the ActiveLedger as its order book.** Cells *bid* to serve a hop — typesafe.ai
   bids high-quality/high-cost, Flash-no-think bids cheap/low-confidence, the pincher bids "free, I already
   know." The router clears the market per context. Durability is then just **market liquidity**: many
   sellers for every product means no single failure starves the route. "Preferred when" is the cleared
   price, per regime.

4. **Superposed routes (the quantum reach, stated sharply).** A MothQuantum cell lets a route be a
   *mixture of routes* until measured/settled — something a classical NN cannot express. B6 is not "add a
   quantum backend"; it is "let the preference map hold amplitude, not just a winner," and collapse only at
   the settle tick. That is the first thing here a classical relational computer genuinely cannot do.

## 11. System-2 — the learning system (Casey named it)

**System-2** is the fleet's name for the slow, deliberative **learning component** — the counterpart to
the fast **System-1** routes that serve live traffic. System-1 *runs* the graph; System-2 *studies and
rebuilds* it. System-2 never touches live traffic; it works entirely against the append-only ActiveLog,
which — because every record carries a budget vector (§8) — is a **budgeted benchmark corpus** it can
replay for free.

System-2's loop:

1. **Propose** alternative cell-networks — different topologies / route choices that reach the *same
   product* (`system2-redesigner`, B8).
2. **Backtest** each alternative by replaying historical ActiveLog runs against it and scoring both on
   the recorded budgets — time, tokens-per-API, dollars, power, local requirements — with **no live
   cost** (`system2-backtest`, B7). The differ/oracle must certify the alternative reaches the identical
   product *before* any budget is compared; otherwise you are pricing a cheaper *different* answer.
3. **Promote** winners into the preference map (B4), and keep the losers as documented dead-ends.

### 11.1 The iron-triangle — "fast, good, cheap: pick two"

Preference is **not a scalar**. Each route is a position on the triangle {**good** (quality), **fast**
(latency), **cheap** ($/tokens/power)}. The old contractor line holds: the *best contractors* give you
**two** of the three — so System-2 keeps, per product and regime, a small stable of elite routes:

- **better-faster** (top quality, low latency, costs more),
- **better-cheaper** (top quality, low cost, slower),
- **faster-cheaper** (fast and cheap, quality merely adequate),

plus **satisfice routes** that only *meet the requirements* — a lesser contractor that hits one axis, or
none, but still does the job. "Preferred when" = which corner or edge the application demands *right now*
(a live UX turn wants faster; a batch backfill wants cheaper; a safety check wants better). **Durability**
is then structural: there is always at least a satisfice route standing, and usually an elite route for
the axis you need — many routes to the same product, priced.

The **cheap** axis is not one number. It carries at least two measurements: **compute-cost**
($/tokens/power/latency-as-money) and **storage-cost** (§11.3). A route can be cheap on compute yet
expensive on storage, or the reverse — so "faster-cheaper" and the rest are positions in a space, and
System-2 records *which* cheapness a route buys.

### 11.2 Honest caveat (so backtests don't lie)

Replay assumes recorded inputs are representative and budgets are roughly stationary. When a model gets
cheaper, hardware changes, or an API reprices, old backtests mislead. System-2 must **flag regime shift**
and re-weight recent history over stale — a backtest carries the as-of window it trusted, the same way a
FOLD carries its weakest leaf.

### 11.3 Pruning, and storage as its own cost

System-2 first grows **wide**: for an application it develops a large collection of alternative networks
(the anti-GAN thirst for novel process — §13). That collection *is training data*, and it is expensive to
keep. So pruning has two storage budgets, not one:

- **Training-data store (GC'd).** The full tree of alternatives + their backtest records. It has a **max
  size**; a garbage collector drops dominated / stale / redundant branches once backtesting has learned
  from them, keeping enough diversity to stay durable but not the whole combinatorial fan-out.
- **Production quilt spec (lean).** The pruned, deployed footprint — only the routes the preference map
  actually reaches, at the storage spec the target demands (an embedded money calculator ships kilobytes;
  a server quilt can ship more).

Storage is therefore **part of the cheaper↔expensive spectrum, but as a distinct measurement from
compute** (§11.1). Pruning optimizes the tree *toward the production storage spec* — the same alternative
that wins on tokens may lose once its on-disk footprint is counted, and System-2 must see both.

## 12. Working discipline

- Doc-first, sequential. This file is the source of truth; free context to it.
- Push often. Many small, unique PoCs beat one big one.
- Every PoC: a `selftest` in the house idiom, a receipt (situation-recorder), a ledger row.
- The oracle (differ/gauge) certifies product-identity before any novelty claim is booked.
- Every dispatched builder is reminded of its **extensive typesafe.ai allowance** and told to **record
  what it learns** about typesafe.ai's call patterns for template distillation (§9).

## 13. The example collection — the anti-GAN of programming

The point of the labs is not one grand quilt; it is a **collection of working example quilts in as many
novel configurations as possible, testable *between one another***. This is the anti-GAN of programming:
we chase **durable logic** by building many independent quilts that reach correct products through
genuinely different routing — quilts that **surprise the developer that they work**, then reveal a niche
optimization for a narrow-but-clever use.

**Principles for the collection:**

- **The clearer and more obvious the use-case, the better the example.** A reader should get it instantly.
- **Chase unique *uses* as much as unique *math*.** A weird routing pattern for an ordinary need teaches
  as much as clever math; the odd, obvious cases are the best templates.
- **Every example books to the shared ActiveLog** (same envelope, same budget vector) so examples are
  comparable and System-2 can backtest them against each other — testable *between* one another, not in
  isolation. An `labs/examples/run_all` interop harness runs them all and checks they book cleanly.
- **Progression: templates → examples → tutorials.** First a reusable template, then a concrete worked
  example quilt, and later a tutorial walking a zero-shot user through it.

**First worked example — `calculator-quilt` (EX1).** A calculator with two product-identical routes for
the same equation:

- a **simple money route** — fixed-point / integer-cents remainder arithmetic, because the register's
  transactions are limited in scope (no interest, no compounding). Tiny routing, tiny tooling, tiny
  storage.
- a **full route** — floating/decimal + interest & compounding tooling, for equations that need it.

The quilt **chooses the simple route for every equation that doesn't need the extra math tooling**, and
only escalates when the equation demands interest. It books both routes' budgets — the simple route wins
decisively on compute *and* storage (§11.3) — so it is a crisp, obvious demonstration of the whole
thesis at once: novelty-in-process / identity-in-product, iron-triangle preference, and the storage cost
axis. Endless siblings follow (a units-converter quilt, a date quilt that skips timezones when all inputs
are UTC, a text quilt that skips tokenization for pure-ASCII, …) — each an obvious use, each a clever
skip.

**Backlog for the collection** (all depend on B1's `labs/activeledger` landing, then fan out in
parallel — they are independent of each other by design):

| id | example quilt | the obvious use | the clever skip / niche optimization |
|---|---|---|---|
| EX1 | `calculator-quilt` | arithmetic | fixed-point money route when no interest is needed |
| EX2 | `convert-quilt` | unit conversion | identity/no-op route when source unit == target unit |
| EX3 | `datetime-quilt` | date math | skip timezone/DST tooling when all inputs are UTC |
| EX4 | `text-normalize-quilt` | clean up text | skip tokenizer/unicode tooling for pure-ASCII input |
| EX5 | `image-thumb-quilt` | make a thumbnail | skip decode+resample when the source is already ≤ target |

Each ships: the two+ routes, the route-chooser, an offline `selftest` (products identical across routes;
the chosen route is cheaper on the axis claimed), a mark, and a ledger row.

## 14. Coordination & reconciliation with the live org (2026-09-29)

*Outcome of reading the org before building further (FLEET-ACTIVITY-2026-09-29.md). The key finding: we
COMPLETE an existing spine rather than fork it.*

**ActiveLedger is the metabolism half that jev-quilt's OrgBook explicitly left open.** `jev-quilt`'s
`OrgBook` (G18, `jev_quilt/orgbook.py`) already books the dispatch org as a double-entry ledger and
routes by **earned standing** under five laws — Law 1 identity-never-floats (exact typed Receipts, no
float touches identity), Law 2/R2 standing (booked-correct streak confers ANSWER, one booked-wrong
revokes), Law 4 replay≡live (bit-for-bit reconstruction), a `chain()` + `decisions_digest()` pin. But it
states its own honest limit: **"O7/R5 — cost-per-passed-acceptance-test as a *conserved* budget that
throttles a tier — is a metabolism, not a wire… out of scope for this module; this file books the
routing half only."** That conserved cost-budget **is our ActiveLedger + budget vector.** So:

- **OrgBook = the routing/standing half ("good"/correctness).** ActiveLedger = **the metabolism/budget
  half ("fast"+"cheap": wall_ms / tokens / usd / power / storage).** They are the two halves of one
  ledger, not two competing ledgers. Do NOT fork OrgBook's routing; wire ActiveLedger's budget receipts
  as the conserved-cost dimension it is missing.
- **Adopt OrgBook's discipline for our budget receipts:** exact typed identity (Law 1 — a budget vector's
  identity fields never float), replay≡live (Law 4 — our ActiveLog already re-derives its chain), and a
  decisions/`route_total` digest that two runs agree on bit-for-bit.
- **B4 route-preference becomes the JOIN:** `preferred-when = f(OrgBook standing[good], ActiveLedger
  budget[fast,cheap])` over the iron-triangle. Standing says *who is allowed and correct*; the budget
  vector says *at what cost*; B4 clears the market between them. This is the single cleanest statement of
  what B4 is.
- **B2 unit-translation-audit** aligns with OrgBook's exactness: our route.hop zero-sum-after-translation
  is the same conservation invariant OrgBook enforces on Receipts — B2 should mirror its replay≡live pin.
- **System-2** signs into the `fleet-seeds`↔`breakthrough-prospector` mutual-awareness contract; its niche
  is route/network alternatives priced on the ActiveLedger budget (distinct from their model/kernel search).
- **exoj** (`core.mjs`) proved a commutative ledger closing to the 2.2e-16 float floor with "refusal beats
  silent renorm" (γ+η=1) — the conservation-purity reference for our translations.
- **Naming note (not a collision of substance):** `activeledger-agent` (org pip package) is a *different
  thing* — a PLATO tile-server client that logs activity/investments/trades (sibling of fishinglog-agent /
  reallog-agent). Ours is `labs/activeledger`, the budget/metabolism cell-graph. Keep the `labs/` namespace
  so the two are never conflated; if confusion arises, ours can be renamed `metabolism-ledger`.
- **Adopt fleet infra:** wire `quilt-forge@v0` (receipts-first CI) + `quilt-atlas` hooks into the labs for
  constellation visibility, like the rest of the fleet.
