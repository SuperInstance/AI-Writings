# NEW DIRECTIONS — frontiers the shipped rungs now make reachable

*Opus 5.5 architecture pass. Woken past the deadband: this is a genuine
strategic fork — chart directions **beyond** the current G-list, not the next
number on it. Written against the frontier as of **d013** (R1, R2, G11,
G13/G14, G16 shipped and on `main`; G12 in build; G15 unbuilt — `bridge.py`
does not yet exist). Companion to [`../GAPS.md`](../GAPS.md),
[`../DISPATCH.md`](../DISPATCH.md), and the arch specs
[`G16-architecture.md`](G16-architecture.md) /
[`G13-G14-architecture.md`](G13-G14-architecture.md).*

The rule for what follows: quilt idiom, exact/integer identity,
offline-deterministic, replay-verifiable, additive-only (the immutable move
set is not touched). Decisions over surveys. Honest limits at the end.

---

## What the shipped rungs have actually made reachable

Read the shipped line as a single sentence and the new frontier appears at its
end:

> **R2:** *I* earned the right to stop asking (`standing.py`, from my own book).
> **G11:** *we* can glue our proven routes across strangers, weighted by trust
> (`commons.trust_weighted` / `provenance_merge`).
> **G13/G14:** I can *carry* that standing across a kernel boundary, signed and
> content-addressed, and it degrades honestly in rougher seas than it was earned
> in (`diploma.py`).
> **G16:** a *claim* earns standing only when independent strangers **reproduce**
> it — reproduction is a 32-byte root, and a drifting instrument is excluded by a
> pre-registered floor, not by taste (`claim.py`).

Each of those was, until it shipped, a thing you had to take on faith. The line
has been walking faith out of the system one rung at a time. What it has **not**
yet reached — and what all three shipped composites now put within one additive
module — is the last faith-object standing in the fleet: **the credential
itself.** A G16 claim proves reproduction *here, now, to me*. It produces a
verdict (`claim_standing → ('ANSWER', consensus)`). It does **not** produce an
artifact a stranger can admit **without trusting the issuer** — and the diploma,
which does travel signed, is issued from *one cell's streak* (`Standing.from_book`),
never from a reproduced claim, and re-checks the *streak* on arrival but never the
*trustworthiness of the witnesses behind it*.

That gap is the frontier.

---

## The three directions

**A — The Attestation (federated schoolhouse; G17).** A credential *earned by
reproduction* and *re-verifiable by the recipient from scratch*: an issuer signs
a reproduced `Claim`; a stranger kernel admits it only by re-deriving the
reproduction root, applying its **own** trust weights (G11), its **own** quorum,
and its **own** floor (G14), and recomputing consensus itself. The issuer's
"it's earned" is never on the wire to be forged. *A credential is authority you
can reconstruct, not authority you must accept.* **Build first.** ACT-tier.

**B — The Org on the Quilt (recursive self-application; G18).** Book the dispatch
org *on* `jev_quilt`: dispatches as `Bookkeeper` receipts, tier-routing as a real
`standing.verdict` cell, a runner's ANSWER-unsupervised conferred by
`Standing.from_book` over its booked-correct runs and revoked on one miss. O1–O9
stop being prose and become predicates over the org-book; replay reproduces every
routing decision bit-for-bit. The replay-verifiable half is ACT-tier wiring of
shipped parts; its **metabolism half (O7 / R5)** — cost as a *conserved* budget
coupled to routing — is a real fork that needs a future Opus wake.

**C — Cross-boundary Reproducibility (sim-to-real as a root divergence; G19).** A
policy earns the right to move steel only when its booked behavior in *sim* folds
to the **same** reproduction root as its booked behavior on the *bench*, under a
floor that separates honest domain-shift (halt) from instrument drift (exclude) —
the G16 discriminator, turned across the reality boundary. **A true fork, and
gated on G15** (the `bridge.py` it needs is unbuilt). Deferred behind G15; needs a
future Opus wake for the cross-domain floor semantics.

**The one to build now: A.** It is the apex of the shipped line, all three of its
dependencies (`claim.py`, `diploma.py`, `commons.py` trust) are on `main`, and the
one real design fork is resolved below — so a Sonnet team can start immediately
with no further Opus wake.

---

# A · G17 — the Attestation (build this now)

## The idea

`claim.py` proves reproduction to *the node holding the books*. It cannot leave
that node as a trusted object. `diploma.py` leaves the node signed — but it seals
*one cell's streak*, and the receiver re-checks only that the streak transferred
and clears its own threshold; it never asks *whether the evidence behind the
streak came from witnesses worth believing.*

An **Attestation** closes the loop: it is a signed, content-addressed envelope
over a **reproduced `Claim`** — the readings of every witness, the issuer's
consensus, the quorum, and the calibrated floor the reproduction held under. A
stranger kernel does not admit it on the issuer's word. It:

1. verifies the issuer's Ed25519 signature (`unknown_signer` / `bad_signature`);
2. re-derives the reproduction root from the carried readings and checks it
   equals the sealed root (`root_mismatch` — no silent edit in transit);
3. applies its **own** trust weights to the witnesses (G11) — a witness the
   recipient distrusts is dropped from the trusted set;
4. applies its **own** quorum and its **own** calibrated floor (G14);
5. confers `('ANSWER', consensus)` **only if the recipient's own recomputation**
   still yields unanimity among trusted, non-drifting witnesses of at least the
   recipient's quorum — degrading to `CONFIRM` when the recipient's sea is rougher
   than the floor the reproduction was earned under, and refusing (booked reason)
   otherwise.

The capability that falls out is one no shipped module has: **the recipient can
honestly reach a *different* verdict than the issuer from the very same bytes.**
An issuer who trusts a colluding witness ring signs `earns_standing = true`; a
recipient who assigns that ring trust 0 gets `conferred = false` from the *same
attestation* — and that is **correct, not a failure.** That is the anti-credential-
laundering property, and it is exactly the fisherman-and-dad vow turned onto trust
itself: the season-opening number (G16) becomes a portable, signed certificate a
regulator, an insurer, or a rival fleet can bank **without trusting the issuer** —
because they re-run the reproduction under their own weights before they act.

## The failure it prevents / the value it creates (in the fleet's terms)

The replication crisis and the credentialism crisis are the same crisis one step
apart: a number no one can regenerate, and a diploma no one can re-examine. G16
killed the first inside a node. G17 kills the second across nodes. Concretely: a
diploma today asserts an authority the recipient must accept on faith in the
issuer's honesty about *who* vouched. A laundered credential — real signature,
real root, but a consensus manufactured by a trusted-by-the-issuer ring — passes
every check `diploma.py` and `claim.py` can make. G17 is the door that a laundered
credential loses at, because the recipient reconstructs the trust from the raw
witness readings it carries.

## The one real design fork, resolved (so no further Opus wake is needed)

**Fork: does the attestation carry the witnesses' *readings*, or only the
*consensus + a proof of reproduction*?**

Carrying only the consensus is smaller (O(1)) and still lets a recipient verify
*that* reproduction happened. **Reject it.** It cannot let the recipient *drop a
distrusted witness and watch the answer change* — which is the entire capability.
A credential you can authenticate but cannot re-weigh is precisely the
credentialism failure G17 exists to kill.

**Decision: the Attestation carries every witness's reading (drifters included),
and the issuer's `earns_standing` boolean is *never on the wire.*** There is no
"it's earned" field to forge; there is only the evidence and a signature over it,
and the recipient always recomputes the verdict itself. The cost — the artifact is
O(N) in the witness count, not O(1) — is the correct trade and is flagged as an
honest limit below.

This mirrors `claim.py`'s own resolved fork exactly: **the root is taken over ALL
witnesses' readings** (the full content address of what the swarm reported, so a
single-delta edit still changes the root even for a witness later excluded), while
**consensus is taken over the trusted, non-drifting subset.** One law, carried
from `claim.py` into the portable artifact.

## Module shape — new file `jev_quilt/attest.py`

Additive only. Mirror `diploma.py`'s byte discipline (`canonical_*_bytes`
pipe-joined UTF-8, no json/repr/pickle; `*_root` folds meta into an MMR leaf;
verify-only, refusal-as-verdict) and `claim.py`'s witness idioms.

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Callable

from .claim import Claim, Reading
from .calibrate import CalibratedFloor
from .diploma import parse_floor, _floor_to_str          # reuse the Q16 wire codec
from .fold import mmr_root
from . import ed25519
# sha256 leaves as elsewhere in the family

@dataclass(frozen=True)
class WitnessReading:
    witness: str        # the witness's signer id
    value: str          # its canonical reading
    drifting: bool      # flagged by the issuer's floor at issue time (advisory; recipient re-judges)

@dataclass(frozen=True)
class Attestation:
    readings: tuple[WitnessReading, ...]   # ALL witnesses, sorted by witness id
    consensus: str                         # issuer's consensus value (advisory; recipient recomputes)
    quorum: int                            # issuer's quorum (advisory)
    earned_floor: Optional[str]            # "num/den" Q16 wire form, or None (G14 carry)
    signer: str                            # issuer id
    signature: str                         # Ed25519 over canonical_attestation_bytes || attestation_root
    # NOTE: there is deliberately NO earns_standing field. Nothing to forge.

def _leaf(r: WitnessReading) -> bytes:
    # sha256(f"{r.witness}\x1f{r.value}\x1f{int(r.drifting)}") — \x1f-delimited, collision-safe

def canonical_attestation_bytes(readings, consensus, quorum, earned_floor) -> bytes:
    # pipe-joined UTF-8 over sorted readings + consensus + quorum + floor — cross-language, no json

def attestation_root(readings, consensus, quorum, earned_floor) -> bytes:
    # mmr_root([_leaf(r) for r in sorted(readings)] + [__meta__ leaf sealing consensus|quorum|floor])
    # meta in the root => consensus/quorum/floor cannot be edited in transit without breaking the seal

def attest(claim: Claim, *, signer: str, seed_hex: str,
           floor: Optional[Q16] = None) -> Attestation:
    # REFUSE to issue if not claim.earns_standing() — a certificate of an unreproduced
    # claim is a lie at the source (raise, or return a refusal — match issue_diploma's polarity).
    # Carries claim.readings(include_drifting=True) as WitnessReadings, claim.consensus(),
    # the claim's quorum, and earned_floor (the sea reproduction held under). Signs the root.

def verify_attestation(att: Attestation, pubkeys: dict) -> dict:
    # verify-only, NEVER raises. {"ok": True} or {"ok": False, "reason": ...}
    # reasons: unknown_signer | bad_signature | root_mismatch  (mirror verify_diploma)

@dataclass(frozen=True)
class Admission:
    conferred: bool
    verdict: str                 # 'ANSWER' | 'CONFIRM' | base_verdict
    value: Optional[str]
    reason: Optional[str]        # refusal reason, for the booked v2-refused row
    trusted: tuple[str, ...]     # witnesses the recipient counted
    dropped: tuple[str, ...]     # dropped by recipient trust==0, or drifting under recipient floor

def admit(att: Attestation, pubkeys: dict, *, trust: dict[str, int],
          quorum: int, floor: Optional[CalibratedFloor] = None,
          reading_magnitude: Optional[Callable[[WitnessReading], "Q16"]] = None,
          base_verdict: str = "CONFIRM") -> Admission:
    # 1. verify_attestation -> on !ok, Admission(conferred=False, verdict=base, reason=...).
    # 2. recipient trusted set = readings whose witness has trust.get(w,0) > 0,
    #    MINUS any the recipient's own floor re-flags as drifting (needs reading_magnitude;
    #    if no floor/magnitude given, honor the carried drifting flags).
    # 3. conferred iff |trusted| >= quorum AND trusted are UNANIMOUS on one value
    #    (recipient recomputes consensus — the issuer's is advisory only).
    # 4. sea-grade (G14): earned_floor absent OR recipient sea within it -> 'ANSWER';
    #    conferred but recipient sea rougher than earned_floor -> 'CONFIRM', not 'ANSWER'.
    # 5. else Admission(conferred=False, verdict=base, value=None, reason='not_reproduced_for_recipient').
```

Export the public names from `jev_quilt/__init__.py` exactly as `Diploma` /
`Claim` are exported (`Attestation`, `WitnessReading`, `Admission`,
`attest`, `verify_attestation`, `admit`, `attestation_root`,
`canonical_attestation_bytes`).

## First machine-checkable gap — G17 predicate (append to `../GAPS.md`)

Compiles against **`jev_quilt/attest.py`** (new), reusing `claim.py`,
`commons.py` (trust), `diploma.py`/`signed_receipts.py` (signing),
`calibrate.py` (G14 floor).

```
# issuer side (a reproduced claim, G16)
claim = Claim.from_books(books, reading_fn=..., quorum=3, floor=F)
assert claim.earns_standing()
att = attest(claim, signer="issuerA", seed_hex=SK_A, floor=F.floor())

# recipient side — an independent kernel with its OWN pubkeys / trust / quorum / floor
v = admit(att, pubkeys={"issuerA": PK_A}, trust=recipient_trust, quorum=3, floor=F_recip)

PASS iff v.conferred and v.value == claim.consensus() and v.verdict == 'ANSWER'
         when the signature is valid, the carried readings re-derive to att's sealed root,
         and the recipient trusts >= quorum non-drifting witnesses who all agree
 AND     admit(tamper(att), ...).conferred is False           # edited reading / consensus / bad sig
             with a booked reason in {root_mismatch, bad_signature, unknown_signer}   # refusal, never silent
 AND     admit(att, trust={ring: 0 for each colluding witness, ...}).conferred is False
             EVEN THOUGH the issuer reproduced+signed it   # a laundered credential loses at the recipient's door
 AND     admit(att, quorum=len(witnesses)+1).conferred is False   # the recipient's stricter quorum is its own to set
 AND     admit(att, floor=tighter_than_earned).verdict == 'CONFIRM'   # G14 across the credential: rougher sea degrades ANSWER->CONFIRM
 AND     admit(shuffle_readings(att), ...) == admit(att, ...)   # confluent: the recipient's verdict is order-free
 AND     attest(claim_that_does_not_earn_standing, ...) refuses to issue   # no certificate of an unreproduced claim
```

Each clause falls out of the module shape: refusal from `verify_attestation`
(clauses 2); recipient recomputation over the trust-filtered non-drifting subset
(clauses 3, 4); sea-grading reused from `diploma.sea_graded_verdict` (clause 5);
sorted leaves before root/consensus (clause 6, confluence, inherited from
`claim.py`); the issue-time `earns_standing()` guard (clause 7).

## Test plan — `tests/test_attest.py` (1:1 with the predicate)

Build small books with `Bookkeeper.book(...)` and a `reading_fn` reading the
residue, exactly as `test_claim.py` / `test_diploma.py` do.

- `test_reproduced_claim_issues_admissible_attestation` — 5 unanimous witnesses,
  quorum 3, full recipient trust → `conferred`, `verdict=='ANSWER'`, `value==consensus`.
- `test_tampered_attestation_refused` — three sub-cases: edited carried reading;
  edited `consensus`/`quorum`/`floor` meta; flipped signature byte → each →
  `verify_attestation.ok is False` with the right reason and `admit(...).conferred is False`.
- `test_recipient_reweights_laundered_credential` — **the headline.** Issuer's
  claim includes a colluding ring reporting the false value; issuer trusts the ring
  so `earns_standing` is True and the attestation is validly signed. Recipient sets
  those witnesses' trust to 0 → trusted set loses unanimity (or falls below quorum)
  → `conferred is False`. Same bytes, different honest verdict.
- `test_recipient_stricter_quorum` — `quorum=len(witnesses)+1` → `conferred is False`.
- `test_sea_graded_admission` — recipient floor tighter than `earned_floor` →
  `verdict=='CONFIRM'`, not `'ANSWER'` (G14 carried into the credential).
- `test_confluent_admission` — shuffle carried readings → identical `Admission`.
- `test_content_addressed_root_vector` — a hard-coded expected `attestation_root`
  hex over a fixed small witness set (the cross-language pin, like
  `test_diploma.py` / `test_claim.py`).
- `test_issuer_refuses_unreproduced_claim` — `attest()` on a claim that does not
  `earns_standing()` → refusal at issue.

Run `python -m unittest discover -s tests`; full suite green (new + existing), no
test weakened or skipped.

## Dual track (same law, both sides)

| | toy (a table) | industrial (rough seas) |
|---|---|---|
| **G17** | Three kids counted the jar and all said 42 (that was G16). The teacher writes a card — **with the three kids' names on it**, not just the number — and signs it. A second classroom doesn't trust one of the three (his glasses fog); they **cross his name off the card and recount from the two names left**, and the card counts as "42" for them only if the remaining two still agree. The card carries the *names*, so a stranger can re-judge who to believe. A badge you re-earn by re-weighing, never by trusting the signer. | A signed, content-addressed `Attestation` over a reproduced `Claim`; a regulator / insurer / rival fleet admits it by re-deriving the reproduction root, applying its **own** trust weights (G11) and floor (G14), and conferring only on its **own** recomputed unanimity. The season-opening number becomes bankable across orgs with no trust in the issuer. |

Same law both sides: **a credential is authority you can reconstruct, not
authority you must accept.**

## Tier / Opus wake

**ACT-tier build, checked by a runner (CONFIRM).** It is additive, reuses
`claim` / `diploma` / `commons` / `calibrate`, has one design fork — resolved
above (carry the readings; never put `earns_standing` on the wire) — and a clean
1:1 predicate. **No future Opus wake is needed for the build.** This pass *is* the
fork. The dispatcher can book `d015 → Sonnet` immediately against this spec, then
`d016 → Haiku` to independently re-run the predicate. This is the exact shape of
the G16 haul (d009 arch → d010 build → d011 confirm), which landed clean.

---

# B · G18 — the Org on the Quilt (recursive self-application)

**Capability & why now.** Book the dispatch org *on* `jev_quilt` instead of a
flat CSV. A dispatch becomes a `Bookkeeper` receipt; tier-routing becomes a real
`standing.verdict(Standing.from_book(runner_book), task_class, base)` call; a
runner's *ANSWER-unsupervised* is conferred by replaying its book and revoked on
one miss — the org's cells obey the same five laws the software does. All the
parts are aboard (`standing`, `commons`, `bookkeeper`, `throttle`), and the ledger
is already a WAL in spirit; it just doesn't run on the kernel yet.

**Failure prevented / value.** The org's claims about itself (O1: Opus-wake rate
falls while pass-rate holds; O2: unsupervised share rises with no rise in escaped
defects) stop being prose in `DISPATCH.md` and become **predicates over the
org-book** — "triage is physics" made literally replay-verifiable. Un-booked side
work becomes impossible (law 4, on the org). The org optimizes itself the way the
software does, and can *prove* it did.

**First gap — G18 predicate** (against a new `orgbook` surface + `standing.py`):
routing a task of class `c` for a runner with book `B` returns exactly
`standing.verdict(Standing.from_book(B), c, base)`; one booked-wrong run on `c`
drops the next verdict from `ANSWER` back to the base; **replay of the org-book
reproduces every routing decision bit-for-bit** (`replay ≡ live` on the org). O5
(100% of shipped work traces to a booked dispatch) becomes: every merged rung's
receipt chains to a dispatch receipt, or the chain is broken.

**Dual track.** *Toy:* the gold/blue/white-token chore game from `DISPATCH.md`,
but now every hand-off card chains to the last so a stranger can replay the whole
afternoon. *Industrial:* the booked `orgbook`, driving real Opus/Sonnet/Haiku
calls, every dispatch content-addressed and replay-verifiable.

**Tier & Opus wake.** The replay-verifiable half is **ACT-tier wiring** of shipped
parts — Sonnet can build it now. The **metabolism half is a real fork**: O7 / R5
wants cost-per-passed-acceptance-test as a *conserved* quantity that throttles a
tier — a conservation law, not a wire, and law-level design. Build the
replay-verifiable org now; **flag R5-metabolism as needing a future Opus wake.**

---

# C · G19 — Cross-boundary Reproducibility (sim-to-real as a root divergence)

**Capability & why now.** A policy earns the right to move steel only when its
booked behavior in *sim* folds to the **same** reproduction root as its booked
behavior on the *bench*, under a calibrated floor that separates honest
domain-shift (halt) from instrument drift (exclude) — the exact G16 discriminator
(`claim.py`), turned across the reality boundary. G16's reproduction root is the
enabling rung; **G15's `bridge.py` is the missing dependency** and is unbuilt.

**Failure prevented.** The crushed hand — a policy green in sim, divergent on
metal, shipped anyway. This makes the sim-to-real gap a *booked, 32-byte
divergence* a machine refuses to cross, not a hope.

**First gap — G19 predicate** (against `claim.py` + the future `bridge.py`): a
sim-book and a real-book of the same policy fold to one root within floor →
cleared for actuation; divergence *within* floor → refuse (honest sim-to-real gap,
**halt**); divergence *clearing* the floor on one rig → that rig excluded as drift,
**not blended in**.

**Tier & Opus wake.** **A true fork.** It is gated on G15, and its core question —
what "the same phenomenon in two realities" means for `reading_fn`, and how the
floor is calibrated *across domains* rather than within one — is a law-level
question, not wiring. **Needs a future Opus wake, after G15 lands.** Named here so
the ladder can see where the physical seam is going; do not dispatch it yet.

---

## Honest limits

- **STRETCH (G17, inherited).** As with G13/G14 and G16, the tests run both
  "kernels" as the same Python implementation, so they prove cross-*instance*
  admission (two independent verifications), not literally cross-*language*. The
  true cross-language morphism rests entirely on the byte-canonical discipline
  (`canonical_attestation_bytes` / `attestation_root` touch nothing but UTF-8
  pipe-joined text and sha256/MMR — the family's existing contract) and is pinned
  by the hard-coded expected-root vector a non-Python port can reproduce.
- **STRETCH (G17, the O(N) trade).** The Attestation carries every witness's
  reading, so its size is linear in the swarm, not O(1). This is a *deliberate,
  load-bearing* cost — re-weighability is the whole capability — but for a very
  large swarm a future rung could carry a Merkle-proof'd *sample* of witnesses
  with the same root. Note it; do not block on it, and do not pre-build it.
- **STRETCH (G17, drift semantics on transfer).** The recipient re-flagging
  drift needs a `reading_magnitude` extractor to run its own floor; when the
  recipient supplies none, `admit` honors the *carried* drifting flags. That
  fallback trusts the issuer's floor for drift only (never for trust or
  consensus) — a smaller faith than a diploma asks today, but not zero. A
  recipient that cares supplies its own magnitude fn and owns the drift call too.
- **B is half-a-fork.** The replay-verifiable org is honest ACT-tier work; the
  metabolism/conservation half (R5) is not, and this doc does not pretend it is.
- **C is deferred, not designed.** It is named and gated, not architected.
  Dispatching it before G15 lands would be waking the wrong tier for the wrong sea.

**Least-certain claim.** That **carrying the full witness readings** (rather than a
consensus plus a succinct reproduction proof) is the right shape for G17. It is
the shape that delivers the headline capability — a recipient reaching a different,
honest verdict from the same bytes — and it satisfies every predicate clause; but
it is the shape that also costs O(N), and a future fleet that needs attestations
over thousand-float swarms may want the sampled-proof variant. I am choosing the
re-weighable-in-full shape now because *the first attestation the fleet ships
should be the one that most completely walks faith out of the credential* — the
optimization to a sampled proof is a later rung with its own predicate, not a
thing to hedge on today.
