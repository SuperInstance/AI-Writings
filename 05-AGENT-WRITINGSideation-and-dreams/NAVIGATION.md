# Navigation Department — Coordinates for Egocentric Quilt Universes

*Advisory memo, responding to CHARTER.md moves 1 and 4. Scope: addressing only. Transport, rendering, and merge mechanics belong to other departments; we define just enough notation for them to hang their work on.*

---

## 0. The one-sentence design

An address is **a walk, not a point**: a sequence of steps, each segment walked inside one universe, joined by portal crossings — always relative to the cell that is asking, always starting from `0/0/0`.

There is no grid. There are only neighbors, portals, and the walker.

---

## 1. Notation

### 1.1 Steps and segments

A quilt gives each cell adjacency along up to three axes. We name them `u / v / w` and count signed unit steps along each. A 2-D quilt simply keeps `w = 0` forever; the notation does not care.

- **Self:** `0/0/0` — every cell's address of itself, in every universe, always.
- **Unit step:** `1/0/0` means "the neighbor one step along +u from here." `-1/0/0`, `0/1/0`, `0/0/-1`, etc.
- **Segment:** a multi-step walk inside one universe, written as the sum of its steps: `2/0/0` = two steps along +u. Segments add by vector addition (A3, §6).
- **Canonical form:** if several walks reach the same cell (the quilt has loops), the address is the shortest walk; ties break by axis order (u, then v, then w). Canonical form is for comparison and storage *within one origin's bookkeeping only* — see A8.

### 1.2 Portal operators

- **`:` descend.** `a : b` means: walk segment `a`, which must end on a portal cell; cross through it into the nested universe; then walk segment `b` in the new universe, whose entry cell is the new `0/0/0` (A7).
- **`^` ascend.** Walk to a portal cell, cross to the universe you came from (or, for a named portal, to its counterpart), land on the counterpart cell, which becomes `0/0/0`.
- **Full address:** `seg (: seg | ^ seg)*`, always read left to right, always spoken by an origin. We write the origin in front when it matters: `L: 2/0/0:1/0/0` = "S2, as addressed from L."

### 1.3 Queries

- `*` in place of a segment = "every cell reachable from this entry." `L: 2/0/0:*` is the whole ESP32 web as the laptop may walk it — this is how the laptop's summary face (§5) is built.
- `?` in a coordinate = unknown step count, used in route *requests* gossiped between neighbors (A9).

### 1.4 The reversal rule

`reverse(r)` = reverse the segment order, negate every segment, swap `:` ↔ `^`.

If B is reachable from A by `r`, then A is reachable from B by `reverse(r)`. This holds *across* portals, which naive negation does not — see the worked example in §4, where the symmetry is exact.

---

## 2. Worked universe

Two universes, the charter's round-2 seed #1 made minimal:

**U0 — the laptop quilt.** Two cells matter here:

- `L` — the laptop's own cell (its shell, its ledger view).
- `P` — a portal cell, the ESP32 web compressed to one tile.

`P` sits two steps along +u from `L`. So:

```
L: L = 0/0/0
L: P = 2/0/0          ← the whole ESP32 web is one tile at this address
```

**U1 — the ESP32 web.** Four cells:

- `U` — the uplink cell: the ESP32's radio, and the counterpart of `P` (same portal-id).
- `S1` — temperature sensor, one step +v from `U`.
- `S2` — humidity sensor, one step +u from `U`.
- `S3` — motion sensor, one step +u and one step +v from `U`.

Portal binding: `P ↔ U`, portal-id `portal:esp32-01`. One binding, two cells, one in each universe. That pairing is the only thing the two universes share.

Inside U1, addresses as spoken by `U`:

```
U: U  = 0/0/0
U: S1 = 0/1/0
U: S2 = 1/0/0
U: S3 = 1/1/0
```

And, because every cell is its own origin (A1), as spoken by `S2`:

```
S2: S2 = 0/0/0
S2: U  = -1/0/0
S2: S1 = -1/1/0       (one -u step to U, one +v step from there: -1/0/0 + 0/1/0)
S2: S3 = 0/1/0
```

Note what just happened: `S1` is `0/1/0` from `U` and `-1/1/0` from `S2`. Both correct. Addresses are incomparable across origins except by walking (A2).

---

## 3. Portal addressing, outside and in

**What the ESP32 web looks like from the laptop quilt:** a single tile.

```
L: 2/0/0
```

That is the entire answer. The web — four cells, a radio, a dying humidity sensor — is one cell at `2/0/0`, carrying a portal-id and a summary face (§5). Deflation taken to its limit: a whole universe at zoom level zero. The laptop can address *into* it:

```
L: S2 = 2/0/0 : 1/0/0
```

Read: two +u steps to the portal `P`; descend; from the entry cell `U` (now `0/0/0`), one +u step to `S2`.

**What the laptop looks like from inside the ESP32 web:** also a single tile — the uplink cell `U`, which is a portal pointing *out*. `U` addresses the laptop as:

```
U: L = ^ -2/0/0
```

Read: `U` *is* the portal cell, so ascend immediately; land on the counterpart `P` (new origin); then two −u steps to `L`.

**What the ESP32 web looks like from inside the ESP32 web:** it has no address. It is home. Every cell in it is `0/0/0` to itself and a short segment to its neighbors. "The web as a whole" is only a thing you can point at *from outside* — which is exactly the charter's claim that walls are perspectives, not places. The closest internal construction is the boundary: `U` is the cell where addresses start containing `^`.

Two elegant fallouts:

- From `P`, the embedded web's entry is `: 0/0/0` — descend and you are, by definition, at the origin of somewhere new.
- From `S2`, the laptop is `S2: L = -1/0/0 ^ -2/0/0` — which is precisely `reverse(2/0/0:1/0/0)`. The reversal rule (§1.4) survives portal crossings unchanged.

---

## 4. A navigation, end to end

The laptop wants `S3`'s latest motion reading. `L` does not have a map. It has: its own id, its neighbor steps, and portal bindings (A9). Routing is gossip of relative routes:

1. `L` asks its neighbor at `1/0/0`: "route to `portal:esp32-01`?" The neighbor answers "`1/0/0` from me." `L` adds its own step: `P` is at `2/0/0` from `L`. (A3 — addition is legal here because everything so far is one segment, one universe.)
2. `L` sends the request down the address `2/0/0 : *` — deliver to any cell matching; the query `?` rides along. On crossing, the frame is discarded (A4): inside U1 the request carries only the U1-relative remainder.
3. `U` receives it at its own `0/0/0`, knows `S3 = 1/1/0` locally, forwards two steps.
4. `S3` answers along `reverse` of the path it was reached by. The reply's route home is constructed hop by hop; nobody ever held a global coordinate.

Every hop only ever knew: the step the message came in on, and the step to send it out on. That is the whole routing table.

---

## 5. Disagreement at the boundary: the two-faced portal cell

A portal cell is never one rendering. It is a bound pair of renderings with stamps:

```
portal portal:esp32-01
  face.out : U1 as rendered from U0   (the laptop's deflated summary)
  face.in  : U1's rendering of itself (carried up over the link)
  seam     : diff(face.out, face.in)  — derived, never authoritative
```

Concrete state, one Tuesday morning:

```
face.out   (spoken by P in U0, stamped L:seq41, age 8s)
  members : 3
  S1 temp : ok
  S2 hum  : ok
  S3 mot  : ok
  link    : wifi + bt

face.in    (spoken by U in U1, stamped U:seq17, age 40m)
  members : 3
  S1 temp : ok
  S2 hum  : NO READING for 40m — brownout suspected
  S3 mot  : event burst, 212/hr
  link    : bt only — wifi dropped at 03:12
```

The seam:

```
seam portal:esp32-01
  agree    : members = 3, S1 = ok
  disagree : S2.health  out=ok        | in=dead(40m)
             link       out=wifi+bt   | in=bt-only
             S3.rate    out=quiet     | in=burst(212/hr)
  stamps   : out age 8s | in age 40m
  verdict  : OPEN — no merge proposed, none needed yet
```

Rules for the seam:

- **Both faces persist, both attributed, both stamped** (A10). Rendering never overwrites. "The laptop is stale" and "the ESP32 is silent" are equally available readings of the same seam, and the canvas shows the seam, not a winner — the Shipwright's plank seam, but located exactly and only at portal cells.
- **De-sync at 1s vs 1h** (charter seed #2) is the same structure at different stamp deltas. At ~1s the faces differ only in stamps: a *lag seam* — same shape, offset in time; render as a ghost/offset, no content disagreement. At ~1h the shapes themselves diverge: an *open seam* — render both faces butt-jointed, disagreement enumerated, as above.
- **Genuine failure** (charter seed #3): the sides cannot agree on member count, or the portal-id itself is in dispute (two webs both claiming `portal:esp32-01`). The portal then renders as *two truths with no shared region at all* — both faces full-size, seam marked UNMERGEABLE, `agree` empty. Crucially, **navigation is unaffected**: addressing depends only on adjacency and bindings (A9), never on agreement. You can still route to `S2` through a portal whose faces are at war. The address of a thing and the truth about a thing were never the same object (A8), and this is why.
- **A cell inside U1 can see the seam too.** `S3` addresses the portal as `S3: U = -1/-1/0`, and the `face.out` it finds there is, from its perspective, *a rumor about itself*. Department shells (charter move 5) fall out of this for free: a shell is just a face rendered with a chosen staleness budget and field set.

---

## 6. Invariants — what lets a cell navigate with no global frame

- **A1 Self-origin.** For every cell c, `c: c = 0/0/0`. The origin is not a place; it is whoever is asking.
- **A2 Relativity.** An address is meaningless without its origin. `L: X` and `S2: X` are incomparable except by walking from one origin to the other and recomputing.
- **A3 Local arithmetic.** Within one segment, steps add: if `X: Y = s` and `Y: Z = t`, then `X: Z = s + t`. This is the *only* addition that exists.
- **A4 No cross-frame arithmetic.** Coordinates on opposite sides of `:` or `^` never add. Different universe, different axes, possibly different units, possibly different *meaning* of adjacency. The only thing that crosses a portal is the walk.
- **A5 Reversibility.** Every step has an inverse step; every descent an ascent. If `A: B = r` then `B: A = reverse(r)`, with `reverse` as in §1.4. Walking out and back returns to the same *cell-id*.
- **A6 Portal pairing.** A portal is one binding, two cells, sharing a portal-id: `P ↔ U`. Descend-then-ascend is the identity on cell-id: `P : ^` lands back on `P`. (On *cell-id*, note — not on rendering. You can come home to a changed wall.)
- **A7 Re-origin on crossing.** After any `:` or `^`, the landing cell is `0/0/0` for the next segment. You never carry old coordinates through a portal; you carry only the remaining walk.
- **A8 Identity ≠ address.** Cell-ids and portal-ids are stable, genesis-stamped, valid everywhere, and are the only things disagreement records may reference (§5's seam names `S2` by id, not by `1/0/0`). Step-triples are per-origin routes, recomputed when topology changes. Never store a triple as if it were a name.
- **A9 Adjacency sufficiency.** To route anywhere reachable, a cell needs exactly three things: its own id, its unit steps to neighbors, and its portal bindings. Routes propagate by gossip — "X is at `r` from me" plus "the neighbor is at `s` from me" gives "X is at `s + r` from me" (A3), frame by frame, portal by portal.
- **A10 Disagreement persistence.** A portal cell always carries both faces and both stamps. Convergence is an event that may happen; it is never assumed, never forced, and never required for navigation.

---

## 7. What we deliberately did not build

- **No global naming service.** Portal-ids and cell-ids are minted locally and collide freely; a binding is only ever resolved one hop at a time (A9). If two webs both claim `portal:esp32-01`, that is a §5 failure rendering, not a registry error.
- **No coordinates for "the universe as seen from nowhere."** The notation cannot express one. That is the feature: anything the system can say, some cell is saying.
- **No merge semantics.** The seam diff format in §5 is handed to whoever builds joinery; Navigation only guarantees the two faces are addressable, stamped, and persistent.

*— Navigation department. The map is not the territory; here, there is no map, and the territory walks.*
