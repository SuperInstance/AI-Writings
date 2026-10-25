# G12 architecture — provable forgetting (the right to leave, witnessed)

*Dispatch d015. **No Opus wake** — deadband O1 held: G12 reuses the shipped
`fold.mmr_root` + `commons.py` and adds one primitive (a tombstone leaf). For a
Sonnet build team; checked by a Haiku runner against the [`../GAPS.md`](../GAPS.md)
predicate.*

## The idea (and the tension it resolves)

The commons is append-only and content-addressed; the fabric doctrine says *"the
witness-referenced is never destroyed."* But a person has a right to leave, and a
fleet has a right to shed a route that encoded a boat's private grounds. G12 lets
the commons **remove** a deposit **and prove the removal** — so `replay ≡ live`
still holds, no phantom weight lingers, and no one can silently resurrect the
forgotten route. The trick, exactly as with everything else here: you do not
*mutate the past out*; you **fold the erasure in**. Forgetting is itself a
witnessed, content-addressed operation.

## The predicate (from GAPS.md)
```
C.deposit(k, a, 3); r0 = C.root()
C.forget(k, a)                                    # books a tombstone leaf
PASS iff C.recall(k) is None and C.weight(k, a) == 0
 AND     C.root() != r0                            # removal is a real, booked state change
 AND     mmr_root(surviving_leaves + [tombstone(k,a)]) == C.root()   # a peer replays the delta to the same root
 AND     after C.deposit(k, a, 1): C.weight(k, a) == 1   # no silent resurrection of old weight
```

## Design — additive methods on `Commons` (backward-compatible)

Add to `commons.py`; when no `forget` has been called, behavior and `root()` are
**byte-identical** to today (pin this).

- **State:** a `self._tombstones: set[tuple[str,str]]` (sorted for determinism).
- **`_tombstone_leaf(key, answer) -> bytes`** — `sha256(f"__tomb__\x1f{key}\x1f{answer}")`,
  a distinct namespace from `_leaf` so a tombstone can never collide with a deposit.
- **`forget(key, answer=None)`** — remove `(key,answer)` (or all answers for `key`)
  from `self._w` and `self._prov`, and add each removed pair to `self._tombstones`.
  Idempotent; forgetting an absent pair still books the tombstone (the intent to
  forget is itself witnessed).
- **`root()`** — now `mmr_root(sorted(deposit leaves) + sorted(tombstone leaves))`.
  Empty tombstone set ⇒ identical to the current root (backward-compat pin).
- **`recall` / `weight` / `earned` / `deposits`** — unchanged; they already read
  `self._w`, which `forget` emptied, so a forgotten route returns `None` / `0` for
  free.
- **No silent resurrection:** because `forget` deleted `self._w[(k,a)]`, a later
  `deposit(k, a, 1)` starts from 0 → weight 1. The tombstone remains folded in the
  root (the erasure stays witnessed) even after re-deposit — that is correct: the
  ledger shows *it was forgotten, then re-learned*, not that it was never gone.
- **Confluence preserved:** tombstones are sorted before rooting, so
  `A.forget(x).root()` is order-free and two nodes that applied the same forgets
  converge (`agrees_with` still one 32-byte compare). A `merge` should also union
  `_tombstones`; **decide the merge rule explicitly:** a tombstone suppresses a
  pair's weight on merge **only if** the merging node also holds the tombstone —
  i.e. forgetting is local unless gossiped as its own tombstone. (Simplest correct
  rule: `merge` unions both `_prov` and `_tombstones`, then drops any `_w` entry
  whose pair is in the unioned tombstone set. Document this; it is the one real
  judgment call.)

## Test plan — `tests/test_forget.py` (1:1 with the predicate)
- `test_forget_removes_and_is_booked` — deposit, root r0, forget → recall None,
  weight 0, root != r0.
- `test_peer_replays_erasure_to_same_root` — `mmr_root(surviving + tombstone) == C.root()`.
- `test_no_silent_resurrection` — after forget, re-deposit weight 1 → weight == 1
  (not 4).
- `test_empty_tombstones_root_is_backward_compatible` — a commons with no forgets
  has the exact same `root()` as one built by the pre-G12 path (hard-coded vector).
- `test_forget_is_confluent` — `forget` then two merge orders → same root,
  `agrees_with` True.
- `test_forget_all_answers_for_a_key` — `forget(key)` with no answer clears every
  answer under that key.

Run `python -m unittest discover -s tests`; full suite green, nothing weakened.

## Dual track
- **Toy:** a shoebox of index cards where "forget this card" means writing a
  *strike-card* that the next reader must also apply to rebuild the day — you never
  tear the original out, you add the cancellation, so a stranger's rebuild still
  matches yours.
- **Industrial:** a tombstone leaf folded into `mmr_root`; replay-verifiable,
  no phantom weight, right-to-leave without a surveillance archive.

## Honest limits (STRETCH)
- The merge rule above is the one real judgment call — a tombstone only suppresses
  where it has propagated. That is the honest, gossip-safe semantics (you cannot
  force every node to forget without delivering the tombstone), but flag it clearly
  in the docstring so no one assumes global instantaneous erasure.
- Cross-language reproducibility rests on the byte-canonical tombstone leaf; pin it
  with an expected-root vector like the other rungs.
