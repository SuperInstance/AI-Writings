# G16 architecture — reproducibility as `mmr_root` (federated discovery from strangers)

*Dispatch d009. **No Opus wake** — the deadband (O1) held: G16 reuses the
`fold`/`commons` machinery G11 hardened, plus `calibrate` + `q16`, all shipped. The
one real design question (below) was resolved at dispatch altitude. This spec is for a
Sonnet build team, checked by a Haiku runner against the [`../GAPS.md`](../GAPS.md)
predicate.*

## The idea

The commons proves two nodes' *proven routes* agree. It does not yet gate a **scientific
claim** on the agreement of the underlying raw books. G16 does: a claim earns standing
iff N independent witnesses **reproduce** it — their books fold to a single agreed root,
confluent across gossip order, and a drifting instrument is excluded rather than
silently averaged in. Reproducibility becomes a 32-byte comparison.

## The one real design question, resolved

The predicate has two clauses that look contradictory:
- **Clause 2:** one float's book diverges by a single delta → **NOT** `earns_standing` (`agrees_with` False).
- **Clause 4:** a drifting float flagged by the calibrated floor is **down-weighted, not silently averaged in** (so it does *not* break the claim).

Both are right, and the discriminator between them is **the calibrated floor**:

> A witness that disagrees but stays **within** the calibrated floor is an *honest
> disagreement* — the claim is genuinely not reproducible, so it must **halt** (clause 2).
> A witness whose surprise **clears** the floor is a flagged *instrument drift* — a
> known-bad sensor, **excluded** from the trusted set before consensus (clause 4).

This is the correct scientific stance: you may not discard an outlier because you
dislike it (clause 2); you may discard it only when an independent, pre-registered
drift criterion (the calibrated floor, R1) flags it (clause 4). The floor is exactly
the line between "real disagreement — stop" and "bad instrument — exclude."

## Definition of `earns_standing`

**A claim earns standing iff the *non-drifting* witnesses are UNANIMOUS on one value,
and there are at least `quorum` of them.** Reproducibility = everyone trusted got the
same answer (not a majority vote — a majority with a live dissenter is not reproducible).

## Module shape — new file `jev_quilt/claim.py`

Additive only; nothing in the immutable move set is touched. Mirror `commons.py`'s
idioms (`_leaf`, `root()`, `agrees_with()`).

```python
@dataclass(frozen=True)
class Reading:
    witness: str      # source id (a float / node)
    value: str        # the canonical reading, e.g. "north_shallow=42"
    drifting: bool    # flagged by the calibrated floor

def _leaf(witness: str, value: str) -> bytes:
    # sha256(f"{witness}\x1f{value}") — same \x1f-delimited shape as commons._leaf
```

### `Claim`
- `Claim.from_books(books, *, reading_fn, quorum, floor=None) -> Claim`
  - `books: dict[str, Bookkeeper]` — witness id → its book.
  - `reading_fn(book) -> (value: str, magnitude: Q16)` — extracts this witness's reading
    and a `Q16` magnitude (the quantity whose surprise-vs-consensus decides drift). Keep
    `reading_fn` injected (like `standing.from_book`'s `key_fn`) so the phenomenon is
    caller-defined and the module stays substrate-neutral.
  - **Drift pass (clause 4):** compute each witness's `surprise` (from `predictor.surprise`)
    of its magnitude vs the swarm consensus magnitude (the modal value's magnitude, or the
    exact-ℚ mean of agreeing witnesses). Feed the surprises to a `CalibratedFloor` (the
    `floor` arg, or a default) and mark a witness `drifting=True` iff its surprise clears
    `floor.floor()`. Drift is exact-ℚ throughout — no float touches identity.
  - Store all `Reading`s (drifting flag included).
- `readings(self, *, include_drifting=False) -> list[Reading]` — sorted (by witness) for
  determinism; excludes drifters unless asked.
- `root(self) -> bytes` — `mmr_root([_leaf(r.witness, r.value) for r in sorted ALL readings])`
  over **every** witness's actual reading (drifters included), so the root is the full
  content address of what the swarm reported. Sorted → **confluent** (clause 3). This is
  what makes a single-delta divergence show up as a different root (clause 2).
- `agrees_with(self, other) -> bool` — `self.root() == other.root()` (the 32-byte check).
- `consensus(self) -> Optional[str]` — the value all **non-drifting** witnesses agree on,
  if they are unanimous and number ≥ `quorum`; else `None` (honest absence).
- `earns_standing(self) -> bool` — `consensus() is not None`.
- `drifters(self) -> set[str]` — witnesses excluded by the floor (for the audit trail).

### Conferral into the substrate
- `claim_standing(claim, key, base_verdict) -> tuple[str, Optional[str]]` — thin bridge
  mirroring `standing.verdict`: `('ANSWER', claim.consensus())` when `earns_standing()`,
  else `(base_verdict, None)`. So a reproduced claim confers the fourth verdict just like
  an earned streak does — one law, whether the evidence is one cell's book or a swarm's.

Export the public names from `jev_quilt/__init__.py` (follow how `Commons`/`Standing` are
exported).

## Why each predicate clause falls out

- **Clause 1 — earns standing when nodes recompute and agree.** All witnesses report the
  same value → non-drifting set unanimous, count ≥ quorum → `earns_standing` True. Two
  nodes running `from_books` on the same books get identical roots (deterministic) →
  `agrees_with` True. ✓
- **Clause 2 — one delta → NOT earned, `agrees_with` False.** The diverging witness (small
  delta, surprise **within** the floor → not flagged) stays in the trusted set → not
  unanimous → `earns_standing` False. Its changed reading changes its leaf → different
  `root()` → `agrees_with(canonical)` False. ✓
- **Clause 3 — confluent across gossip order.** Leaves sorted before `mmr_root` →
  `from_books(shuffle(books)).root() == from_books(books).root()`. ✓
- **Clause 4 — drifter down-weighted, not averaged.** A witness whose surprise **clears**
  the floor is `drifting=True` → excluded from `consensus()`; if it was the lone dissenter,
  the rest are unanimous → `earns_standing` True. Its value never enters consensus (never
  "averaged in"); `drifters()` records the exclusion. ✓

## Test plan — `tests/test_claim.py` (1:1 with the predicate)

Build small books with `Bookkeeper.book({}, {}, value, {...residue...})`; `reading_fn`
reads the residue (mirror `test_commons.py`/`test_standing.py`).
- `test_reproduced_claim_earns_standing` — 5 witnesses all "42", quorum 3, no drift →
  `earns_standing` True; two independent `from_books` → `agrees_with` True.
- `test_single_delta_divergence_breaks_reproducibility` — flip one witness to "43" with a
  **within-floor** magnitude (not flagged) → `earns_standing` False; its claim
  `agrees_with` the canonical claim is False.
- `test_confluent_across_gossip_order` — `from_books(shuffled).root() == from_books(ordered).root()`.
- `test_drifting_float_is_downweighted_not_averaged` — one witness reports an
  **over-floor** anomalous magnitude → `drifting` True, in `drifters()`, absent from
  `consensus()`; the remaining unanimous witnesses (≥ quorum) → `earns_standing` True.
- `test_honest_disagreement_vs_drift_are_distinguished` — the same numeric divergence, once
  below the floor (breaks reproducibility) and once above it (excluded) → opposite
  outcomes, proving the floor is the discriminator.
- `test_content_addressed_root_vector` — a hard-coded expected-root hex over a fixed small
  swarm (the cross-language pin, like `test_diploma.py`).

Run `python -m unittest discover -s tests`; full suite green (new + existing), no test
weakened or skipped.

## Dual track

| | toy (table) | industrial (rough seas) |
|---|---|---|
| **G16** | three kids count the jar independently; the number counts **only if all three match** — and the kid whose glasses are fogged (a pre-agreed "bad instrument" rule) sits out, they don't just average him in | N floats' books fold to one agreed `mmr_root` or the claim earns nothing; a float the calibrated floor flags as drifting is excluded, not averaged |

Same law both sides: **a claim is earned only when independent witnesses reproduce it;
you exclude a witness only by a pre-registered drift rule, never by taste.**

## Honest limits (STRETCH)

- Cross-*language* reproducibility is asserted via the byte-canonical `_leaf` + sorted
  `mmr_root` (the family's existing contract) and pinned by the expected-root vector;
  both "nodes" in tests are the same Python impl (cross-*instance*), same STRETCH as G13.
- The drift criterion uses surprise-vs-consensus through one `CalibratedFloor`; a swarm is
  a *set*, not a time series, so the floor is applied over the witnesses' surprise
  distribution rather than a temporal window. If a maintainer prefers a temporal/streaming
  swarm, the same floor applies per-tick — note it, don't block on it.
- **Least-certain claim:** that unanimity-among-non-drifters (not majority) is the right
  bar for `earns_standing`. It is the strict-reproducibility reading and it satisfies the
  predicate; a future rung could add a graded "N-of-M reproduced" standing if the fleet
  wants quorum-consensus rather than unanimity.
