# G13 + G14 architecture — the portable, weather-carrying diploma

*Dispatch d006. The Opus 5.5 architecture tier was woken for this fork and made the
decisive call before it hit the session limit: **do not invent crypto — build on the
vendored, stdlib-only Ed25519 verify-only envelope jev-quilt already ships**
(`signed_receipts.py` + `ed25519.py`). This spec carries that decision forward to a
build a Sonnet team can execute with no further Opus wake, checked by a Haiku runner
against the acceptance predicates already in [`../GAPS.md`](../GAPS.md).*

## The decisive finding (why this is cheap, not a research project)

`signed_receipts.py` already gives us exactly the primitive a portable diploma needs:

- **`seal_bytes(canonical, chain_tip, signer, seed_hex)`** — the low-level path
  *explicitly built for FOREIGN/sibling receipts whose canonical form is their own
  substrate's rule.* A diploma is precisely that: its canonical form is
  `Standing.deposits()`, not a `Receipt`. We seal over the diploma's own bytes.
- **`verify_bytes(...)`** — permissionless, **verify-only** (a receiving kernel holds
  only public keys, never a secret), and it **never raises** — it returns a verdict
  `{ok, reasons}` with `unknown_signer / bad_signature / wrong_chain_head / malformed`.
  Refusal is a booked row, not an exception. This *is* the family's refusal polarity.
- **chain-head binding** — `seal` binds a signature to the chain tip it seals so a
  signature "cannot be lifted onto a different fork of the ledger." We reuse this to
  bind the signature to **the standing's own content-addressed root**, so a diploma
  cannot be lifted onto a different standing.

So G13 is mostly *assembly* of shipped parts. G14 adds one exact-ℚ field (the floor)
to what gets signed, and one read-time grading function.

## G13 — portable diploma (cross-substrate standing morphism)

**New file: `jev_quilt/diploma.py`.** No changes to the immutable move set; `standing.py`
gets one additive constructor. Rewrite judgment, never the moves.

### Data
```python
@dataclass(frozen=True)
class Diploma:
    deposits: list[tuple[str, str, int]]   # (key, answer, streak), sorted — from Standing.deposits()
    diploma_n: int                          # the threshold these streaks were judged against
    earned_floor: Optional[str]             # G14: "num/den" exact, or None (see below)
    root: str                               # mmr_root hex over the diploma leaves (content address)
    signer: str
    signature: str                          # Ed25519 over blake3(message_bytes(canonical, root))
```

### Canonical bytes + root (content-addressed under the receiver's own law)
```python
def _leaf(key, answer, streak) -> bytes:          # reuse commons._leaf's shape (\x1f-delimited sha256)
    return sha256(f"{key}\x1f{answer}\x1f{streak}".encode()).digest()

def diploma_root(deposits, diploma_n, earned_floor) -> str:
    leaves  = [_leaf(k, a, s) for (k, a, s) in sorted(deposits)]
    leaves += [sha256(f"__meta__\x1f{diploma_n}\x1f{earned_floor or ''}".encode()).digest()]
    return mmr_root(leaves).hex()             # fold.mmr_root — the receiver recomputes this itself
```
`mmr_root` handles arbitrary deposit counts (blake3's 1024-byte refusal is why we do
**not** hash one big buffer). The meta-leaf folds `diploma_n` and the floor **into the
root**, so neither the threshold nor the weather can be edited without breaking it.

### Mint (the kernel that earned it signs — needs the seed)
```python
def issue(standing, *, signer, seed_hex, earned_floor=None) -> Diploma:
    deps = standing.deposits()
    root = diploma_root(deps, standing.diploma, earned_floor)
    _, sig = seal_bytes(canonical_diploma_bytes(deps, standing.diploma, earned_floor),
                        chain_tip=root, signer=signer, seed_hex=seed_hex)
    return Diploma(deps, standing.diploma, earned_floor, root, signer, sig)
```
`canonical_diploma_bytes` = pipe-joined UTF-8 over sorted deposits + `diploma_n` +
`earned_floor` (bytes-law clean, cross-language reproducible — same discipline as
`signed_receipts.canonical_bytes`).

### Verify + reconstruct (the receiving kernel — verify-only, never raises)
```python
def verify_diploma(diploma, pubkeys) -> dict:
    recomputed = diploma_root(diploma.deposits, diploma.diploma_n, diploma.earned_floor)
    if recomputed != diploma.root:
        return {"ok": False, "reasons": ["root_mismatch"], "signer": diploma.signer}
    return verify_bytes(canonical_diploma_bytes(diploma.deposits, diploma.diploma_n,
                                                diploma.earned_floor),
                        chain_head=diploma.root, signer=diploma.signer,
                        signature_hex=diploma.signature, pubkeys=pubkeys)

def standing_from_diploma(diploma, pubkeys, *, diploma_n=DEFAULT_DIPLOMA) -> Standing:
    """Confer standing on a foreign kernel iff the receipt folds valid under OUR law.
    A refused diploma yields an EMPTY standing (earned False everywhere) — refusal
    polarity, never an exception."""
    v = verify_diploma(diploma, pubkeys)
    s = Standing(diploma_n)
    if not v["ok"]:
        return s
    for (k, a, streak) in diploma.deposits:
        s._streak[k] = streak; s._answer[k] = a     # replayed, not self-granted
    return s
```

### Why the three predicate cases fall out for free
- **valid receipt → `earned(k)`**: streaks replay; `earned` uses the receiver's own
  `diploma_n`. ✅
- **tamper rejected**: inflate a streak → deposits change → `recomputed != root`
  (`root_mismatch`); re-sign to fix the root → needs the secret seed, which a
  verify-only holder does not have → `bad_signature`; flip a byte of the sig →
  `bad_signature`. All three → empty standing → `earned False`. ✅
- **withheld ≠ conferred**: an un-earned key has streak `< diploma_n` (or is absent
  from `deposits`, which only emits `streak>0`); after replay, `earned(k)` is False on
  the receiver. ✅

## G14 — sea-graded transfer (the floor travels, signed, with the diploma)

*"Standing without its calibration is a certificate with the weather torn off."* So the
floor is **already inside the signed root** above (the meta-leaf). One read-time
grading function does the rest — no mutation of standing, so revocability stays free.

```python
def sea_graded_verdict(standing, key, base_verdict, *, surprise: Q16,
                       earned_floor: Q16) -> tuple[str, Optional[str]]:
    if not standing.earned(key):
        return (base_verdict, None)
    if earned_floor is not None and surprise > earned_floor:
        return ("CONFIRM", None)              # imported ANSWER auto-degrades in rougher sea
    return ("ANSWER", standing.recall(key))
```
`earned_floor` is parsed from the diploma's `"num/den"` back to an exact `Q16` (never a
float — identity never floats). The comparison is exact-ℚ, matching `CalibratedFloor`.

### Why the predicate cases fall out
- `surprise <= floor` → `('ANSWER', a)`. ✅
- the tick `surprise > floor` → `('CONFIRM', None)` — degrade, not silent recall. ✅
- **revocable both ways**: `sea_graded_verdict` reads live surprise every tick; when the
  sea calms it returns ANSWER again, and if k books wrong on the receiver, ordinary
  `Standing.observe` revokes the streak. G14 adds a *weather gate* on top of the streak
  gate; neither is sticky. ✅

## Test plan (1:1 with the predicates → `tests/test_diploma.py`)

- `test_g13_valid_diploma_confers_earned_on_a_fresh_kernel` — issue on kernel A, verify
  with A's pubkey on empty kernel B → `earned(k)`.
- `test_g13_tamper_rejected` — three sub-cases: inflated streak (`root_mismatch`), bad
  signature byte (`bad_signature`), unknown signer (`unknown_signer`) → each yields
  empty standing, `earned False`.
- `test_g13_withheld_is_not_conferred` — a streak-1 key transfers but `earned` False at
  `diploma_n=3`.
- `test_g14_answer_in_calm_confirm_in_chop` — same diploma: `surprise <= earned_floor`
  → ANSWER; one tick `surprise > earned_floor` → CONFIRM.
- `test_g14_revocable_both_ways` — sea calms → ANSWER returns; k books wrong → base
  verdict returns.
- `test_diploma_content_addressed` — same deposits+floor ⇒ same root on any instance;
  changing one streak or the floor changes the root (the G14 "weather is signed" pin).

Run: `python -m unittest discover -s tests` (the repo's runner). Expect the current
green suite + these new checks, all passing.

## Dual track (same law both sides)

| | toy (table) | industrial (rough seas) |
|---|---|---|
| **G13** | a paper badge a second table re-earns by *replaying your moves*, not by trusting the badge | a signed, content-addressed diploma a different kernel admits only on valid replay under its own law |
| **G14** | a card marked "true in a flat pool" that flips to "ask again" when the water's choppy | `ANSWER→CONFIRM` bound to the **signed** floor the streak was earned beneath |

## Honest limits (STRETCH)

- **Cross-*language* morphism is asserted, not run here.** Both kernels in the tests are
  the same Python impl, so the test proves cross-*instance* transfer. The true morphism
  (a Rust/TS kernel recomputing `mmr_root` + Ed25519 verify to the same bytes) rests on
  the byte-canonical discipline (`canonical_diploma_bytes`, `_leaf`), which is designed
  for it but unverified in this repo. **Mark STRETCH** in the module docstring and pin
  the canonical bytes with a hard-coded expected root vector so a future port has a
  target. This is the same honesty `signed_receipts` already uses for its Rust/TS ports.
- **Stolen-seed window** is inherited from `signed_receipts` (a stolen key signs until
  rotation) — unchanged, already a named gap; `rotation_payload` is the escape hatch.
- **Least-certain claim:** that `Standing`'s private `_streak`/`_answer` are acceptable
  to populate directly in `standing_from_diploma`. If the maintainers prefer, add a
  public `Standing.from_deposits(deps, diploma_n)` classmethod and call that — a
  one-line additive change, cleaner than reaching into privates. **Recommend the
  public constructor.**
