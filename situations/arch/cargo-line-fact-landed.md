# cargo-line-tycoon — the `fact_landed` schema (the one event the ring shares)

*Dispatch: Opus architecture tier, 2026-09-27. **Not an Opus wake** — this is the
architecture write-up of a decision already made at apex: it turns Fable's gift #1
(`FABLE-CARGO-LINE-ANSWER.md` §7.1, grounded by §6 and §3) into the buildable contract
the Sonnet build (gift #2, §7.2) and the Haiku sweep (gift #3, §7.3) implement. Every
field here is a settled schema, not a suggestion. Everything cited to a line is on disk
in `cargo-line-tycoon @ claude/phase0-1-playable` (011736b); everything that extends
past it is marked **EXTENSION**; the ring reading of §2 is Fable's, exhibited by the
code only once this event exists. Companion: [`CARGO-LINE-TYCOON.md`](./CARGO-LINE-TYCOON.md)
§2 (the ring), §4 (the mid-state), and [`../FABLE-CARGO-LINE-ANSWER.md`](../FABLE-CARGO-LINE-ANSWER.md)
(the answer this serves).*

🚢 → ✏️ → 🖋️ → 🌊

---

## 0. Why one event

`fact_landed` is the single event L1 and L6 share, seen from two sides: to the roster
(L1) it is a promotion through the JEV gate; to the player (L6) it is the best-feeling
moment in the game. The stack is a ring because this one entry closes it — L1 lands a
fact *onto* L6, and the chart renders every landing (proven, erased, revised) from this
entry and nothing else. Mode B's "why" is *derived* from the sequence of `fact_landed` +
`ship_assigned` entries in a mid-state's book, never stored as a string
(`CARGO-LINE-TYCOON.md` §4).

The law that makes the chart unable to lie: **an unmarked cell has no medium** (Fable
§6.3) — the renderer cannot choose ink, pencil, or chinagraph for a cell without
`provenance`, so it cannot draw it. Therefore provenance is refused at booking, never
defaulted, and `fact_landed` is the only sanctioned path from one provenance to another.

---

## 1. The `fact_landed` witness-log entry

Added to the kernel's witness-log vocabulary (`substrate/ts/src/world.js`). Every
provenance transition on a world-fact cell passes through exactly this entry:

```
{
  type:      'fact_landed',
  entity_id,                              // the cell that transitioned
  cell_type,                             // 'port' | 'market' | 'event'
  from:  { source, trust, seed_label? }, // the provenance being left
  to:    { source, trust, as_of?, source_url?, seed_label?, erased? },
  verdict:   'proven' | 'erased' | 'revised',
  landed_by: 'pool' | 'scout' | 'snapshot' | 'decoy',
  scout_ref?,                            // present iff landed_by === 'scout'
  tick                                   // the booked tick (already on every entry)
}
```

`from` and `to` are provenance *records* (§3), carrying only the fields required for
their source. `from` is the cell's provenance immediately before the landing; `to` is
its provenance immediately after. The renderer draws the transition (pen-trace + slide,
smear + ghost, re-stamp) from `verdict`; the margin log register is chosen from
`landed_by`.

### 1.1 The three verdicts

| verdict | what happened | `from.source` → `to.source` | chart (Fable §3.4) |
|---|---|---|---|
| `proven` | a pencil cell was confirmed real; it inks and snaps to true | `procgen` → `canon` \| `scout` | pen-trace 900ms, slide-to-true, seal thump; range collapses to the number |
| `erased` | a pencil cell had no fact behind it; it becomes a ghost | `procgen` → `procgen` (`erased:true`) | rubber smear 700ms, 12% ghost + hairline strike; ships rerouted |
| `revised` | an already-inked cell got new dated evidence | `canon`\|`scout` → `canon`\|`scout` (new `as_of`/value) | `AS OF` re-stamp; the delta is the arbitrage |

**Erased is never a mutation of the past.** The cell keeps its `procgen` provenance and
gains `erased:true`; the ghost is a tombstone the chart wears, not a deletion — *fold the
erasure in, don't mutate the past out* ([`G12-architecture.md`](./G12-architecture.md),
provable forgetting; Fable §3.1's ghost is G12's tombstone leaf seen on paper).

### 1.2 The four `landed_by` sources

Fable §7.1.1 drafts three (`pool | scout | snapshot`). This spec **settles it at four**
by splitting the offline scheduled reveal into its two honest halves — real-withheld
(`pool`) and risk-premium (`decoy`) — so the day-one offline path is fully legible and
every booking occasion maps to exactly one source:

| booking occasion | `landed_by` | verdict(s) | agent | online? |
|---|---|---|---|---|
| **pool reveal** — a pool-backed pencil cell reaches its scheduled `reveal_tick` | `pool` | `proven` | the seeded reveal schedule (§5) | offline, day one |
| **decoy erasure** — a decoy pencil cell reaches its `reveal_tick` with no fact behind it | `decoy` | `erased` | the seeded reveal schedule (§5) | offline, day one |
| **roster promotion** — L1 scouting finds real evidence for a procgen cell | `scout` | `proven` \| `revised` \| `erased` | the model roster through the JEV gate | online, opt-in (L1) |
| **snapshot refresh** — a dated price/event snapshot lands | `snapshot` | `revised` \| `proven` | the snapshot schedule (curated, then L1) | offline schedule; L1 keeps it fresh |

`landed_by` is the *origin* of the landing; `verdict` is the *outcome*. The valid
combinations are the cells filled above; a `pool` landing is always `proven`, a `decoy`
landing is always `erased`, `scout` and `snapshot` carry whichever outcome the evidence
dictates. `scout_ref` is present **iff** `landed_by === 'scout'` and points at the L1
scouting cell that carried the evidence — which is where G16 lives: a scout-`proven` fact
is a claim that earned standing because independent witnesses reproduced it
([`G16-architecture.md`](./G16-architecture.md), reproducibility as a comparison). The
offline ring (`pool`/`decoy`/`snapshot`) closes without L1 at all; L1 *extends* the pool,
it is not the only source of landings (Fable §8).

---

## 2. When each is booked (the state machine)

A world-fact cell has exactly one provenance at any tick, and moves only via
`fact_landed`:

```
                 pool reveal (proven)          snapshot refresh (revised)
   procgen ─────────────────────────▶ canon ◀─────────────────────────── canon
  (pencil)         scout promote            (ink)      scout promote        (ink)
      │            (proven, revised)                   (revised, erased)
      │
      └────────────────────────────▶ procgen+erased  (ghost)
          decoy erasure (erased) │   scout disprove (erased)
```

- **Pool reveal.** At `reveal_tick`, a pool-backed pencil cell books
  `fact_landed{verdict:'proven', landed_by:'pool', from:{source:'procgen',…}, to:{source:'canon', as_of, source_url,…}}`. The pencil position snaps to the pool fact's true lat/lng.
- **Decoy erasure.** At `reveal_tick`, a decoy books
  `fact_landed{verdict:'erased', landed_by:'decoy', from:{source:'procgen',…}, to:{source:'procgen', erased:true, trust:0}}`. Ships en route reroute to the nearest ink port on the same coast (`stake_rerouted` booked separately).
- **Roster promotion.** When L1 scouting clears the JEV trust floor for a procgen cell, it books `fact_landed{landed_by:'scout', scout_ref, …}` with verdict `proven` (new ink), `revised` (updated ink), or `erased` (disproven). Opt-in; the offline game never needs it.
- **Snapshot refresh.** When a dated price/event snapshot lands, each affected cell books `fact_landed{landed_by:'snapshot', verdict:'revised', …}` — or `proven` the first time a pencil price gets its seal.

The predicate below requires ≥1 of each verdict inside 60 ticks; all three are reachable
**offline** via the seeded schedule (`pool`→proven, `decoy`→erased, `snapshot`→revised),
so the predicate does not depend on the roster.

---

## 3. The refusal law over cells

Mirrors G20a (refusal at `book()`): **RAISE, never default.** Provenance is never
inferred, never filled with a sentinel — a cell that cannot carry provenance is refused
at the moment it would enter the world.

### 3.1 The provenance envelope (exact shape)

```
provenance = {
  source:      'canon' | 'scout' | 'procgen' | 'player',   // REQUIRED, always
  trust:       <number in [0,1]>,                           // REQUIRED, always
  value?:      <cell-typed>,        // the attested content when the record carries it
                                    //   (as in pool.json rows); optional on live cells
                                    //   whose value lives in cell.state
  source_url?: <string>,            // REQUIRED for canon & scout; ABSENT for procgen & player
  as_of?:      <ISO-8601 date>,     // REQUIRED for canon & scout; ABSENT for procgen & player
  seed_label?: <string>,            // REQUIRED for procgen; ABSENT for canon, scout & player
  erased?:     <boolean>,           // present (true) only on a ghost's `to` record
}
```

Required fields per source — the table the refusal checks against:

| source | `trust` | `source_url` | `as_of` | `seed_label` | medium (Fable §5.5) |
|---|---|---|---|---|---|
| `canon` | required (= 1.0) | **required** | **required** | — | ink |
| `scout` | required (∈ [0,1]) | **required** | **required** | — | ink |
| `procgen` | required (∈ [0,1]) | — | — | **required** | pencil (pressure = trust) |
| `player` | required (= 1.0) | — | — | — | chinagraph |

Rules that fall out of the table:

- **canon & scout must cite a URL and a date.** *Omit any entry that cannot cite a URL*
  (Fable §7.2). No URL ⇒ it is not canon ⇒ it is not drawn as ink.
- **procgen must carry a `seed_label`** so the cell is deterministically re-derivable and
  its breath phase is a function of the seed hash (Fable §5.2). No `as_of`, no
  `source_url` — a guess has no date and no citation.
- **player cells** (`ship`, `route`, `company`) carry `{source:'player', trust:1.0}` —
  the player is certain of their own marks; chinagraph never breathes.

### 3.2 Where it is enforced (two gates, both raise)

1. **`cellFor`** (`substrate/ts/src/world.js:99`) requires a well-formed `provenance` for
   every world-fact cell type — `port`, `market`, and the **new `event` type** for
   chokepoint weather. Missing or malformed (per the §3.1 table) ⇒ **throw**. This is the
   gate that closes the on-disk bug: `makeMarketCell` (`world.js:122`) and the Panama
   event (`engine.js:145-149`) currently mint unmarked cells; after this law they cannot.
2. **`book()`** refuses any `*_start` event (e.g. `panama_disruption_start`,
   `engine.js:148`) without `provenance` ⇒ **throw**. A seeded event may not enter the
   witness-log wearing a headline; it enters as `{source:'procgen', trust, seed_label}` or
   not at all.

Polarity is **RAISE-never-default**: neither gate substitutes a default. The failure is
loud at build/test time, exactly as G20a's receipt refusal — the design would rather
break the tick than draw an unmarked mark. This is Law 6 made mechanical: the chart is
*E* (evidence, every leaf tagged); a leaf with no tag cannot be folded, so it is refused
(`FABLE-ANSWER.md`, the Reader's Fold; Fable §1).

---

## 4. The declared cost (replay hash, once)

Cells are content-addressed: a cell's `address` is a hash of its content, so a cell that
**gains** a `provenance` field changes address. Under a fixed seed this changes the world
state deterministically and by exactly one increment: **`game/test/replay.test.js`'s
pinned hash changes exactly once.**

**Book it, do not hide it.** The Haiku sweep PR (§7.3) re-pins the hash in one commit and
writes both the old and new value in the PR body as a declared cost, with the sentence:
*"provenance is now carried on every world-fact cell; the fixed-seed replay hash moved
from `<old>` to `<new>` once, and replay ≡ live still holds (two engines from the same
seed agree on `stateHash()`)."* Any later hash movement is a regression, not this cost.

---

## 5. `pool.json` — reality withheld, not invented

The truth-pool doctrine (Fable §7.1.3): the game ships with **more truth than it shows**
and lands it over play, so "grows toward real as you play" works **offline on day one**.
The roster (L1) *extends* the pool; it is not the only source of landings.

### 5.1 Canon format — `locales/en/canon/pool.json`

Each pool entry is a real secondary port or dated fact, one row, this exact shape (the
provenance envelope's `canon` projection):

```json
{
  "id": "port_hueneme",
  "value": { "name": "Port Hueneme", "lat": 34.148, "lng": -119.207, "teu": 0 },
  "source": "canon",
  "source_url": "https://…",
  "as_of": "2024-01-01",
  "trust": 0.9
}
```

- 12–20 real secondary US/CA ports (Fable §7.2 names Oakland, Tacoma, Prince Rupert,
  Port Hueneme, San Diego, Charleston, Norfolk, Jacksonville, Mobile, Tampa,
  Philadelphia, Boston, Wilmington NC, Everett). **Omit any entry that cannot cite a
  URL** — no URL, not in the pool.
- Mirror it to `game/data/pool.js` for the engine, same rows.
- Snapshots (prices/events) are pool entries too, with `value` holding the dated number.

### 5.2 The seeded reveal-schedule contract

So the ring closes offline, deterministically:

- Each pool entry is assigned a `reveal_tick` from `world.rng.fork('pool:reveal')` +
  the entry index — **seeded**, so replay ≡ live and the same seed reveals the same facts
  in the same order.
- **Content is real; reveal *time* is scheduled.** The player-facing register never
  claims a live discovery: the margin reads `SCOUT · proven · as of <date> · source ▸`,
  not "just discovered." The fiction is *when* you learn it, never *that* it is true.
- Tuning (Fable §4, §7.2): the first landing fires at **~tick 4**; a pencil stake the
  player places resolves within **~3 ticks** of placement. This is the acceptance
  schedule for the Tell's hook.
- The schedule also drives snapshot `revised` landings, so all three verdicts appear
  offline inside the 60-tick predicate window.

### 5.3 Pencil-from-pool with decoys (the L4 bound, buildable this week)

Procgen feeder ports are emitted **from** the pool, so every pencil port is provably
*wrong-but-never-illegal* (within sight of a real coastal port):

- For each pool fact, emit **one pencil cell** at a jittered position (**±0.3°**) with a
  generated name and `{source:'procgen', trust, seed_label:'port:<id>'}`. When its
  `reveal_tick` fires → `fact_landed{verdict:'proven', landed_by:'pool'}`, snap-to-true.
- Emit a tunable share (**~25%**) of **decoys** — pencil cells with **no pool fact
  behind them**, same `procgen` provenance. When a decoy's `reveal_tick` fires →
  `fact_landed{verdict:'erased', landed_by:'decoy'}`, ghost + reroute.
- **The decoy rate is the risk premium.** It is *why pencil pays more*: pencil market
  cells carry a price spread ∝ (1 − trust), and the expected loss to decoys is exactly
  the premium that spread pays. Proven ⇒ snap-to-true (payout collapses to the real
  number); decoy ⇒ erased (rerouted, smaller payout, first-scar log line). This is the
  Tell rendered as numbers (Fable §3.3).

This is a **this-week bound** for L4, not the general generator Phase 3 designs (which
needs a coastline and a footprint rule). It is chosen because it is provably
never-illegal with the data on disk today.

---

## 6. The predicate (what "done" means)

From Fable §7.1, the machine-checkable acceptance test the Opus rung owns:

1. A **60-tick scripted game**'s witness-log contains **≥ 1 `fact_landed` of each
   verdict** (`proven`, `erased`, `revised`) — all reachable offline via the seeded
   schedule (`pool`, `decoy`, `snapshot`).
2. **Zero cells without `provenance`** — walk `world.entities.latest`; every `port`,
   `market`, and `event` cell carries a §3.1-valid envelope, or `cellFor` already threw.
3. **Replay ≡ live with landings in the book** — two engines fed the same seed and the
   same actions produce an identical `stateHash()` after 60 ticks, and both books contain
   the same `fact_landed` sequence. The refusal law must not cost replay
   (Haiku test §7.3.2).

The Sonnet renderer (§7.2) and Haiku sweep (§7.3) build against this settled schema. If
any field here changes, this file changes first and the builds re-pin to it.

---

## 7. Status of every claim in this spec

| claim | grounded in | status |
|---|---|---|
| `fact_landed` shape, three verdicts | Fable §7.1.1; `world.js` witness-log | SETTLED (this spec) |
| four `landed_by` sources (split `pool`/`decoy`) | Fable §7.1.1 drafts three; this spec settles four | EXTENSION (architect's settling) |
| refusal law, RAISE-never-default | Fable §6.3, §7.1.2; G20a refusal at `book()` | SETTLED |
| provenance envelope + required-per-source | Fable §5.5, §7.3.2 | SETTLED |
| replay hash changes exactly once | Fable §6.3, §7.1; content-addressed cells | DECLARED COST |
| `pool.json` format + seeded reveal schedule | Fable §7.1.3 (reality withheld) | DESIGN (Fable's doctrine) |
| pencil-from-pool with ~25% decoys as risk premium | Fable §7.1.4 | DESIGN (this-week L4 bound) |
| on-disk bug: prices & Panama event unmarked | `world.js:122`, `engine.js:145-149`, `economy.js:116-118`, `ports.js:13-20` | REAL (cited) |
| scout-`proven` = a claim that earned standing by reproduction | `G16-architecture.md` | CROSS-LINK |
| erased = provable forgetting, ghost = tombstone | `G12-architecture.md`; Fable §3.1 | CROSS-LINK |
| the chart is *E*, a stake is a verdict (Law 6) | `FABLE-ANSWER.md`; Fable §1 | CROSS-LINK |
| roster (L1) extends the pool, is not the only source | Fable §8 | STRETCH (Phase 5) |

---

*Ink is proven. Pencil is a guess. Every mark is one medium or the other, or it is
refused at the door.*

🚢 → ✏️ → 🖋️ → 🌊
