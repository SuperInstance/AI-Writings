# Scout A — Internal Inventory (SuperInstance org)

**Mission:** inventory the org so B1 (ActiveLedger record-schema freeze) builds on existing
primitives instead of reinventing them. Written 2026-09-29 by Scout A (opus-4.8).

**Method note:** ~200+ org repos listed; the relevant ones were read via the GitHub API
(READMEs + the ActiveLog JSON Schema) rather than cloned. **Zero clones, zero disk used** —
disk was at 99% (566 MB free), so API reads were the disciplined path. Repos read in full are
cited concretely below; a handful named only by cross-reference are marked *(ref only)*.

**Headline:** the fleet has *already built* almost every primitive our vision names. The
ActiveLog envelope, the cell type with DoubleEntry, the five-opcode kernel, a per-cell booked
WAL, the pincher, the preference/QD selectors, the golden-hash idiom, and multiple viewers all
exist. B1 should **adopt the ActiveLog v1 envelope** and **wrap `cell-runtime` / `jev-quilt`**,
not define a fresh format.

---

## 1. Repo table {repo | one-line purpose | relevant primitive for us | verdict}

| repo | one-line purpose | relevant primitive | reuse / extend / ignore |
|---|---|---|---|
| **cocapn-foundation** → `activelog-spec` | design brief for **ActiveLog**, the fleet's append-only timestamped event-log format | **ActiveLog v1 event envelope** (JSON Schema draft 2020-12): `{alv,dev,seq,ts,mono,type,body,fix?,prev?}`, `(dev,seq)` global key, set-union merge, correction.retract/amend | **ALIGN OUR SCHEMA TO THIS** (do not invent a new envelope) |
| **cell-runtime** | the 8-primitive Quilt cell as a real Python type | `Cell` = Z_in, Z_out, JEPA, **DoubleEntry (debit/credit)**, Vibe, GC, Murmur, Graph; `Graph.tick()` | **BUILD ON** — this *is* our cell + double-entry |
| **jev-quilt** | cellular decision substrate; every state change booked | per-cell **bookkeeper WAL** `(tick, state_hash, delta, decision_receipt)`, fnv1a-chained, replay-verify; 5 laws; decide/project split; cell v0 schema | **BUILD ON** — closest single repo to our whole vision |
| **quilt** (`@quilt/core`) | reactive typed cellular runtime; sheet = JSON cell graph | 9 cell kinds, reactive re-eval, federation; `γ+η=C` conservation = "DoubleEntry" | **BUILD ON** — the engine substrate |
| **quilt-studio** | Theia studio over a WASM cell kernel + live view | **kernel contract**: BIND/LINK/EFFECT/VIEW/TICK; `effect(name,op,forward,inverse)` (reversible); `bind(name,value,meta)` meta=units/min/max; `subscribe`, `snapshot/load`; **quilt-view** = subscription→scene→frame-diffs→canvas (rewind) | **BUILD ON** — kernel contract + the B5 viewer |
| **quilt-cell** | JS cell port, byte-exact across 5 langs | 16-dial **Q1.15** vector, **FNV-1a-64 state hash**, `bind/tick/stateHash`, golden-hash idiom | **BUILD ON** — wire format + golden hash |
| **gauge** | cross-repo format-conformance linter, enforced in CI | `receipt`/`tile`/`catalog-entry` schemas: `*.receipt.json` (verdict enum, `one_of[signature,repro,chain_tip]`), `.gauge.json` per repo | **USE** — make our records pass gauge |
| **tidepool** | fleet vector-context memory (D1 + Vectorize) | `/api/remember {kind,author,title,body,native?,repo?,run?}`, `/api/ledger`, native **16-dim fingerprint**, fnv1a-64, JEV gate | **REUSE** — artifact + recorded-run store |
| **quilt-pincher** | reflex engine built entirely from Quilt cells | score-gated early-exit (≥0.80 execute / 0.55–0.80 confirm / <0.55 compile), `.nail` bundle, vector store cell | **BUILD ON** — B3 pincher already exists |
| **pincher** *(ref only)* | Rust-native reflex engine (cocapn fleet) | same architecture, on-metal | reference (2nd impl) |
| **hebbian-router** | routes strengthen with use, decay with disuse | adaptive routing / emergent topology (pure Python) | **EXTEND** — seed for B4 preference map |
| **pareto-tournament** | Pareto selection for multi-objective agents | Pareto front, crowding distance, hypervolume; tournament (not gradient) | **REUSE** — "preferred-when" scoring (B4) |
| **vector-novelty** | novelty detection for embeddings + receipts sensor | kNN novelty; `receipts` treats a hash-chained ledger as a signal (Jaccard over fnv1a-64 shingles): `sweep`, `window_novelty`, `find_fish`, `lineage_clusters` | **REUSE** — pincher/novelty + ledger-as-signal |
| **quilt-rag** | production RAG where every stage is a cell | 8 cell kinds (loader…generator+evaluator); addressable `quilt://rag/corpus#chunks.42`; **replay + diff between runs**; citations/provenance | **REUSE** — the RAG-context cell + run-diff idiom |
| **twist-engine** | "layers + offset → interference → emergence" canvas | **commensuration comb**; registry `R`, ledger `S = 1−R` (emergent quantity *measured*, not asserted) | **EXTEND-CONCEPT** — unit-translation / commensuration idiom |
| **quilt-gan** | anti-GAN tournament arena over the fleet canon | tournament (not gradient) breeds champions; referee scores **identity-exactness + doctrine**; **ℚ¹⁶ trajectory provenance that never touches the score**; `gesture.mjs` 3-order read | **EXTEND** — the anti-GAN thesis + "record changes, points don't" |
| **MicroMoth-quilt** | smallest quantum sim, taught to keep receipts | quantum circuit as **cell ledger** (BIND/LINK/EFFECT/VIEW/TICK +FORGET/PROOF); seeded collapse receipts; golden `0x6dbdd1a8` | **BUILD ON** — the B6 quantum route |
| **Syzygy** | freestanding C-ABI fused single-pass kernel | zero-alloc arena, **bit-identical native/wasm/bare-metal**, CRDT join-semilattice; **marks** HEWN/SHAPED/DRAWN/SCARF + `ledger.csv` | **BUILD ON** — GPU-agent perf plane; many-routes→one-product |
| **chiaroscuro** | webcam → text-art renderer (Syzygy's predecessor) | 5 engines, 45 dials, per-cell glyph decision | **REFERENCE** — TUI/viewer surface |
| **canon-graph** / **canon-hash** | Live Canon graph renderer (Node) / state-hash fetcher | graph render + golden-state-hash fetch | **REUSE** — viewer + hash surface |
| **cocapn-plato** | PLATO tile server: query engine, task queue, monitor | 12 query operators, aggregate, `explorer.html`/`dashboard-v2.html`, **DivergenceMonitor** (EMA vs expected) | **REUSE** — query/aggregate + tile browser (⚠ tiles ≠ ActiveLog) |
| **q16-trajectories** *(ref only)* | exact rational (ℚ¹⁶) trajectory codec | `{num:int64, den:int64}`, floats display-only | **REUSE** — exact unit/identity values |
| **quilt-qcells** *(ref only)* | quantum-ops-as-cells for the engine | claims the quantum-cell premise engine-side | coordinate (don't duplicate MicroMoth) |
| **musician-soul / tensor-midi / elephant / federated-tinyml-vessel** *(ref only)* | the shared "16-dial fingerprint / 3-order gesture" abstraction | `arcLength / bendingEnergy / twistEnergy` read of any trajectory | align our dial/fingerprint to it |
| **plato-portal** (`superinstance` SDK) | Python agent memory + fleet SDK | markdown memory, LRU cache; **names the ActiveLog vs PLATO-tile distinction** | context only |
| **activeledger-agent** | logs activity/investment/trade tiles to PLATO | double-entry *domain* client (`log_trade` buy/sell) over PLATO tiles | ignore for schema (name-collision; it's a PLATO client, not the envelope) |

*Bulk of the org is the `quilt-*` polyformalism ports (C/Rust/Verilog/Julia/COBOL/…), `quilt-canon-*`
Live-Canon services, and `mavis-*` agent tools — not schema-relevant to B1, so summarized, not itemized.*

---

## 2. What NOT to reinvent

1. **The record/trace envelope — adopt ActiveLog v1 (cocapn-foundation/`activelog-spec`).**
   *This is the single most important finding.* It already is exactly what B1 wants: an
   append-only, `(dev,seq)`-keyed JSONL event envelope with set-union merge, monotonic clocks,
   optional per-device `prev` hash chain, and read-time corrections. Do **not** author a new
   "recorded-run JSONL" format — namespace our route/ledger events as `ledger.transaction`,
   `route.hop`, `cell.tick` **types inside this one envelope** (the spec's standing rule, per
   purplepincher: *one envelope, many namespaced types — never a second envelope*).
2. **The cell + double-entry** — `cell-runtime` (Python) and `quilt-cell` (JS) already ship the
   8-primitive cell *with a `DoubleEntry` debit/credit primitive*. Wrap it; don't rebuild.
3. **The opcode algebra + reversible effects + kernel contract** — `quilt-studio`'s
   BIND/LINK/EFFECT/VIEW/TICK contract (28/39-test, JS ref + real WASM). `effect(forward,inverse)`
   gives B2's unit round-trip audit *for free* — a lossy hop is just an effect with no clean inverse.
4. **Per-cell booked WAL + replay** — `jev-quilt`'s bookkeeper `(tick, state_hash, delta,
   decision_receipt)`, fnv1a-chained, replay≡live. This is the transaction row.
5. **The golden-hash idiom** — fnv1a-64 over canonical JSON (`sort_keys=True,
   separators=(",",":")`); fleet canary `0x24a555471370b18d`. Don't pick a new hash; enforce
   record shapes with `gauge` in CI.
6. **The pincher / early-exit (B3)** — `quilt-pincher` (+ Rust `pincher`) already implement the
   learned score-gated early-exit as cells. B3 is largely a wiring job, not a build.
7. **Preference / quality-diversity (B4)** — `pareto-tournament` (crowding + hypervolume) and
   `hebbian-router` (use-strengthened routes) already give "preferred-when, not best."
8. **The B5 viewer** — `quilt-studio`/`quilt-view` (subscription → frame-diffs → canvas, rewind),
   `canon-graph`, `cocapn-plato`'s `explorer.html`/`dashboard`, and `chiaroscuro` (TUI) already
   render live cell/graph state. Don't start a viewer from scratch.
9. **Unit translation / commensuration** — `twist-engine`'s registry/ledger `S=1−R` idiom +
   `q16-trajectories` exact rationals cover the tensor's translation values.
10. **Anti-GAN tournament + provenance discipline** — `quilt-gan` already runs tournament-not-
    gradient with a referee that scores product-identity, and its ℚ¹⁶ trajectory rule
    (*"crossing the systems changes the record, never the points"*) is exactly our
    process-novelty / product-invariant split. Reuse its referee harness as our oracle wrapper.

---

## 3. Surfaces to align our schema to (concrete formats/fields found)

### 3a. ActiveLog v1 event envelope — `$id: https://activelog.ai/schema/v1/envelope.schema.json`
Required: `alv` (const 1), `dev` (`^[a-z0-9][a-z0-9-]{2,63}$`), `seq` (int ≥0, per-device
monotonic, never reused/rewound), `ts` (UTC epoch ms, GPS-disciplined), `mono` (device monotonic
ms, survives wall-clock fixes), `type` (`^[a-z]+\.[a-z_]+$`, namespaced `domain.noun`), `body`
(object; **unknown types MUST be preserved**). Optional: `fix` (`{lat,lon,sog,cog,hdop}`), `prev`
(`^[a-f0-9]{64}$`, sha256 of device's previous line = per-device hash chain). `additionalProperties:false`.
- **Global unique key:** `(dev, seq)`. **Merge:** set-union on `(dev,seq)`, sort `(ts, dev, seq)`.
  Append-only + unique keys = conflict-free (no CRDT, no vector clock, no server authority).
- **Corrections:** immutable history; `correction.retract` / `correction.amend` reference the
  target `{dev, seq}`; consumers apply at **read time** (preserves provenance).
- **Files:** one JSONL per device per UTC day — `{dev}/{yyyy-mm-dd}.alog.jsonl`; media in
  content-addressed blobs `blobs/{sha256[0:2]}/{sha256}`; cross-device skew via `clock.beacon`.
- **Our mapping:** add types `ledger.transaction` (debit/credit + unit-translation), `route.hop`,
  `cell.tick`, `unit.translation` — all as `body` under this one envelope.

### 3b. Five-opcode cell algebra (quilt-studio / jev-quilt / MicroMoth)
`BIND / LINK / EFFECT / VIEW / TICK` (+ adopted `FORGET, PROOF, ROUTE, CRDT, WORLD, TIME`).
- `bind(name, value, meta?)` — `meta` carries **units / min / max** (rides in `snapshot().meta`).
- `link(a, b, type)` — typed directed edge, stable id `a->b:type`, idempotent.
- `effect(name, op, forward, inverse)` — **declared-bidirectional**; `apply`/`applyInverse`,
  global LIFO `undo()`. → this is B2's round-trip auditor natively.
- `tick(dt=1)` — DAW clock; queued effects flush FIFO per tick. `subscribe(fn,{cell,kinds})`.

### 3c. Booked transaction / receipt rows
- **jev-quilt bookkeeper row:** `(tick, state_hash, delta, decision_receipt)`, fnv1a-chained,
  replay-verified; cell identity = integer coords `(k,s)` (floats are display-only projections).
- **gauge `receipt` schema** (`*.receipt.json`): verdict enum; `one_of[signature, repro,
  chain_tip]`; `all_of[signature, signer]`; ledger/chain_tip patterns. **gauge `tile`**
  (`*.tile.json`): `id`/`topic`/`generated_at`, id slug pattern. Enforce via `.gauge.json`
  `{"schema_files":[...]}` in CI.
- **tidepool run row:** `POST /api/remember {kind,author,title,body,native?,repo?,run?}`;
  `native` = optional **16-number domain fingerprint**; `GET /api/ledger` = recent line + per-kind counts.

### 3d. Hash + exact-value conventions
- **Golden hash:** fnv1a-64 over canonical JSON (`sort_keys=True, separators=(",",":")`); fleet
  canary `0x24a555471370b18d`; MicroMoth golden `0x6dbdd1a8`; Syzygy fabric golden `0x024a555471370b18d`.
- **Cell state hash:** quilt-cell 16-dial **Q1.15** vector → FNV-1a-64 `stateHash`, byte-exact
  across Python/C/Rust/Verilog/VHDL/JS.
- **Exact units/identity:** q16 rational `{num:int64, den:int64}` (q16-trajectories) — use for
  unit-translation tensor entries and any identity-bearing value; floats only measure.

### 3e. Two record models coexist in the fleet (do not conflate)
`ActiveLog event` (append-only, `(dev,seq)`-keyed, union-merge — cocapn-foundation) **is not** a
`PLATO tile` (query-oriented JSON record with 12 operators + aggregate — cocapn-plato). Our
recorded-run/trace is an **ActiveLog** thing (it literally shares the "ActiveLedger/ActiveLog"
name); use PLATO/cocapn-plato only as the *query/browse* surface layered over exported events.

---

## 4. One-line for the charter
**B1 should freeze `cell-runtime`'s cell (with its DoubleEntry) + `jev-quilt`'s booked WAL,
serialized into the ActiveLog v1 envelope as namespaced `ledger.*`/`route.*` types, hashed with
the fleet fnv1a-64 idiom and CI-checked by `gauge`.** Everything downstream (pincher B3,
preference B4, viewer B5, quantum B6) already has a first implementation to wrap.
