# GAPS — the situations gap ledger (G11–G16)

*The gaps the grand Situations surfaced. This is the **local** ledger for the
Situations layer: gaps the fiction named that today's stack cannot yet reach.
It is deliberately **separate** from the Forward Arc's own ledger
(`reverse-actualization/forward/GAPS.md`, G2–G10 + `G-auto-1`), which lives on the
unmerged branch `claude/reverse-actualization-forward` (see the lineage note in
[`README.md`](README.md)). When that branch lands, the two ledgers read as one
continuous G2→G16 spine — the Forward Arc built the floor, the Situations author
the frontier past it.*

Each gap here is a real cost, not a wish. Each carries a **machine-checkable
predicate** against a named `jev-quilt` module — so it is a compile target, not a
postcard. A gap with no test is a daydream; it does not enter this table.

The loop, once: **Situation → gap → predicate → wide run → merged rung → new
fiction.** It has turned once already — G11 below is shipped.

---

## The board

| gap | one line | surfaced by | compiles against | status |
|---|---|---|---|---|
| **G11** | trust-weighted cross-fleet gluing (an inflated lie can't buy the helm) | [01 · The Hundred Boats](grand/01-the-hundred-boats.md) | `commons.py` | **SHIPPED** — jev-quilt PR #37 |
| **G12** | provable forgetting (remove a deposit, fold the erasure into the root) | [01 · The Hundred Boats](grand/01-the-hundred-boats.md) | `commons.py` + `fold` | OPEN |
| **G13** | portable diploma (standing earned on one kernel, verified by replay on another) | [02 · The Table and the Wheelhouse](grand/02-the-table-and-the-wheelhouse.md) | `standing.py` + `commons.py` | OPEN |
| **G14** | sea-graded transfer (an imported `ANSWER` auto-degrades to `CONFIRM` when the new sea exceeds the floor it was earned beneath) | [02 · The Table and the Wheelhouse](grand/02-the-table-and-the-wheelhouse.md) | `standing.py` + `calibrate.py` | OPEN |
| **G15** | sensor→actuator identity bridge under a provable latency budget (steel never moves on a stale or rounded read) | [03 · The Long Sounding](grand/03-the-long-sounding.md) | `bookkeeper` + a new `bridge` | OPEN |
| **G16** | reproducibility as `mmr_root` (a claim earns standing iff N independent books fold to one agreed root) | [03 · The Long Sounding](grand/03-the-long-sounding.md) | `commons.py` + `fold` + `standing.py` | OPEN |

---

## The predicates (the compile targets)

### G11 · trust-weighted cross-fleet gluing — **SHIPPED**
```
H = honest commons: deposit(k, "safe_a", 3)              # earned from books
P = untrusted peer: deposit(k, "onto_shoal_b", 1000)     # inflated lie
B = provenance_merge(H, P, trust={H: earned, P: 0})
PASS iff B.recall(k) == "safe_a"                          # the lie loses
 AND     provenance_merge(H,P,τ).root() == provenance_merge(P,H,τ).root()   # confluent under trust
 AND     B.agrees_with(other_honest_node_running_same_τ)  # 32-byte agreement survives the weighting
```
*Landed:* `Commons.trust_weighted` / `provenance_merge` + per-source provenance;
`tests/test_commons.py` (+4 G11 checks). The step from one honest account's commons
to a fabric strangers can safely glue.

### G12 · provable forgetting
```
C.deposit(k, a, 3); r0 = C.root()
C.forget(k, a)                                            # books a tombstone leaf
PASS iff C.recall(k) is None and C.weight(k, a) == 0
 AND     C.root() != r0                                   # removal is a real, booked state change
 AND     mmr_root(surviving_leaves + [tombstone(k,a)]) == C.root()   # a peer replays the delta to the same root
 AND     after C.deposit(k, a, 1): C.weight(k, a) == 1    # no silent resurrection of old weight
```
*Hard part:* forgetting must itself be a witnessed, content-addressed operation —
you fold the erasure in, you do not mutate the past out. Right-to-leave without a
surveillance archive.

### G13 · portable diploma (cross-substrate standing morphism)
```
toy_book: 3 booked-correct on k  ->  S_toy = Standing.from_book(toy_book)
receipt  = sign(S_toy.deposits())                         # ed25519/blake3, content-addressed
S_ind    = Standing.from_receipt(receipt, verifier=industrial_kernel)
PASS iff S_ind.earned(k) when receipt.root replays valid on the industrial kernel
 AND     Standing.from_receipt(tamper(receipt)).earned(k) is False   # bad sig / inflated weight / root mismatch rejected
 AND     an un-earned k yields earned(k) is False on transfer         # withheld != conferred
```
*Prevents* the two builds drifting into two laws — a diploma that means one thing at
the table and something false on the water.

### G14 · sea-graded standing transfer
```
earn ANSWER for k under a CalibratedFloor tightened in a calm regime (surprise << floor)
transfer S into a rough regime where predictor.surprise(k) > floor_at_transfer
PASS iff verdict(S, k) == ('ANSWER', a)     while surprise(k) <= floor
 AND     verdict(S, k) == ('CONFIRM', None) the tick surprise(k) > floor   # auto-degrade, not silent recall
 AND     standing re-earns ANSWER once the sea calms and k books correct again   # revocable both ways
```
*Subtlety:* the diploma must carry its *floor*, not just its streak. Standing without
its calibration is a certificate with the weather torn off.

### G15 · sensor→actuator identity bridge under a latency budget
```
d, R = sensor_cell.book_delta()                           # delta + blake3 receipt, at t_book
act(bridge, d_seen, R, t_act, budget)
PASS iff bridge.commit succeeds, books an actuation entry chained to R,
         when blake3(d_seen) == R.delta_hash and (t_act - t_book) <= budget
 AND     bridge.refuse (viability 0, scar booked, no motion) when (t_act - t_book) > budget   # stale read never moves steel
 AND     bridge.refuse when blake3(d_seen) != R.delta_hash  # acted on a copy, not the booked delta
 AND     replay(book) reproduces the exact actuation chain bit-for-bit   # law 4 across the real-time boundary
```
*Prevents* the crushed hand, the snapped line, the sim-to-real gap that kills.

### G16 · reproducibility as `mmr_root` (federated discovery from strangers)
```
books = { float_i.book for i in swarm }                   # N independent witnesses
claim = fold_claim(books)                                 # e.g. count of pollock north-shallow
PASS iff claim.earns_standing() when every node independently recomputes root and agrees_with is True
 AND     NOT claim.earns_standing() when one float's book diverges by a single delta   # agrees_with False
 AND     fold_claim(shuffle(books)).root() == claim.root()   # confluent across gossip/arrival order
 AND     a drifting float flagged by the calibrated floor is down-weighted, not silently averaged in
```
*Prevents* the replication crisis on the water — a season opened or closed on a
number no one can regenerate.

---

## Dual track, per gap

Every gap ships twice on one kernel (the vow in [`README.md`](README.md)):

- **G12** — *toy:* a shoebox of index cards where "forget this card" means writing a
  strike-card the next reader must also apply to rebuild the day; *industrial:* a
  tombstone leaf folded into `mmr_root`, replay-verifiable, no phantom weight.
- **G13** — *toy:* a paper badge a second table re-earns by replaying your moves, not
  by trusting the badge; *industrial:* a signed, content-addressed standing receipt a
  different kernel admits only on valid replay.
- **G14** — *toy:* a card that says "true in a flat pool" and flips to "ask again" when
  the water is choppy; *industrial:* `ANSWER`→`CONFIRM` bound to the calibrated floor.
- **G15** — *toy:* "don't grab the mug from the photo taken a minute ago" — freshness as
  a rule a child can catch; *industrial:* a latency-budgeted, receipt-checked bridge.
- **G16** — *toy:* three kids count the jar independently; the number counts only if all
  three match; *industrial:* N books fold to one agreed root or the claim earns nothing.

*Next haul, by leverage:* **G13/G14** are the closest to shipped rungs (they extend
`standing.py` + `calibrate.py`, both aboard) and they directly guard the fisherman-and-dad
vow — the toy diploma and the boat diploma must be the *same* law. **G16** reuses the
`fold`/`commons` machinery G11 just hardened. **G12** and **G15** open new primitives
(tombstones; the real-time bridge) and want their own Situations run wide first.
