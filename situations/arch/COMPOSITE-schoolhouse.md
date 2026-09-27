# COMPOSITE — the Federated Schoolhouse (the spine, composed)

*Opus 5.5 architecture/synthesis pass. Woken past the deadband: this is the
**composition** of the whole shipped rung-spine into one end-to-end organism —
bootstrap-gate #1 ("the spine is composed, not just shipped"). Not a new rung on
the G-list; the **integration** that turns seven shipped rungs into a single
walkable path. Written against the frontier as of the state where R2, G11,
G13/G14, G16, G17, G12 and G18 are all on `main` (`standing.py`, `commons.py`,
`diploma.py`, `claim.py`, `attest.py`, `orgbook.py`). Companion to
[`NEW-DIRECTIONS.md`](NEW-DIRECTIONS.md), [`../DISPATCH.md`](../DISPATCH.md),
[`../FABLE-DOSSIER.md`](../FABLE-DOSSIER.md).*

The rule, unchanged: quilt idiom, exact/integer identity, offline-deterministic,
replay-verifiable, **additive-only** (the immutable move set is not touched — this
composes shipped functions, it re-implements none of them). Decisions over
surveys. Honest limits at the end.

---

## The spine as one sentence, then as one path

The shipped line walks faith out of the system rung by rung:

> **earned (R2)** — I earned the right to stop asking, from my own book
> (`standing.py`).
> **glued-by-trust (G11)** — we glue our proven routes across strangers, weighted
> by *earned* trust, so a stranger's lie at weight 1000 scales to 0
> (`commons.trust_weighted` / `provenance_merge`).
> **carried, signed + sea-graded (G13/G14)** — standing crosses a kernel boundary
> signed and content-addressed, and degrades honestly in rougher seas than it was
> earned in (`diploma.py`).
> **reproduced (G16)** — a *claim* earns standing only when N independent strangers
> reproduce it to one 32-byte root, a drifter excluded by a pre-registered floor,
> not by taste (`claim.py`).
> **recipient-re-verifies (G17)** — the credential itself becomes re-derivable: a
> stranger admits an attestation only by re-deriving the root, applying its **own**
> trust, quorum and floor, and recomputing consensus — the issuer's "it's earned"
> is never on the wire (`attest.py`).
> **forgetting (G12)** — a route that encoded someone's private ground can be
> **provably** forgotten: a witnessed tombstone folded into the root, gone from
> every read path (`commons.forget`).
> **org-on-quilt (G18)** — the org that builds the kernel is booked *on* the
> kernel; every dispatch is a receipt, routing is `standing.verdict`, replay ≡ live
> on the org itself (`orgbook.py`).

Each rung has shipped as its own module with its own 1:1 predicate. **What has
not shipped is the sentence read as a single breath** — one artifact, one witness
set, walking the *entire* path: reproduced → attested → admitted under a stranger's
own trust → conferred into that stranger's trust-weighted commons → provably
forgotten → all of it booked on the org, and the whole chain replay ≡ live. That
composition is the Federated Schoolhouse, and building it (as the smallest possible
glue over shipped parts) is what closes gate #1.

## What the schoolhouse *is* (the organism, not the metaphor)

A **schoolhouse** is a node that admits credentials from strangers on its own
authority and keeps a living, forgettable memory of what it has come to trust:

1. **N witnesses reproduce a claim (G16).** `Claim.from_books` folds N independent
   books to one reproduction root; a drifting instrument is excluded by the
   calibrated floor, an honest dissenter halts consensus. The claim earns standing
   iff the non-drifters are unanimous and number ≥ quorum.
2. **An issuer attests it (G17).** `attest(claim, ...)` seals every witness's
   reading (drifters included) + the issuer's advisory consensus/quorum/floor into
   a signed, content-addressed `Attestation`. It **refuses to issue** a certificate
   of an unreproduced claim.
3. **A stranger kernel admits under its OWN trust (G11) / quorum / floor (G14).**
   `admit(att, pubkeys, trust=..., quorum=..., floor=...)` verifies the signature,
   re-derives the root (`root_mismatch` on any edit), drops witnesses the recipient
   assigns trust 0, re-judges drift under the recipient's own floor, and **recomputes
   consensus itself**. A laundered credential — real signature, real root, a chorus
   padded by a ring the issuer trusts — loses here the moment the recipient sets the
   ring's trust to 0. Sea-grading degrades `ANSWER→CONFIRM` when the recipient's sea
   is rougher than the floor the reproduction was graded under.
4. **The conferred standing (R2) enters a trust-weighted commons.** A conferred
   `Admission` is deposited into the schoolhouse's `Commons` — the one genuinely new
   line of logic in this module (§ The one bridge, below). Now the schoolhouse can
   `recall` a route it admitted, pool evidence across many admissions of the same
   route, and read the commons **through a second layer of trust** — over the
   *issuers*, not just the witnesses — via `commons.trust_weighted`.
5. **A route can be provably forgotten (G12).** `commons.forget(key, answer)` books
   a witnessed tombstone; the pair vanishes from `recall`, `weight`, `earned`,
   `sources`, `trust_weighted`, and `provenance_merge`, while the tombstone stays
   folded into `root()` — the erasure is itself a provable state change.
6. **All of it is booked on the org (G18).** Every step above is one dispatch
   `record_dispatch`'d onto an `OrgBook`: reproduce, attest, admit/refuse, deposit,
   forget. O5 becomes literal — every schoolhouse action traces to a booked
   dispatch, and `org.replay()` reconstructs the routing bit-for-bit.

The composite capability no single rung has: **a stranger's credential becomes a
first-class, forgettable, replay-verifiable entry in your own memory, admitted on
your authority alone, and every admission and forgetting is itself booked as
org history.** That is a school that issues and honors diplomas without a central
registrar — the fisherman-and-dad vow turned onto an institution.

---

## Module shape — new file `jev_quilt/schoolhouse.py`

**Decision (module vs. integration-test-only): ship a thin `schoolhouse.py`
composition module *and* a 1:1 `tests/test_schoolhouse.py`.** Rationale: the chain
has exactly **one** piece of genuinely new logic — bridging a conferred
`Admission` into a `Commons.deposit` (weight + provenance semantics) — and one new
concern — *booking each spine step on the org* as a coherent dispatch sequence.
Both deserve a named, importable, testable surface, exactly as `diploma.py` /
`claim.py` / `attest.py` / `orgbook.py` each earned a module by wiring shipped
parts onto a new cell rather than living only in a test. Everything else is
delegation to shipped functions; the module re-implements none of them.

Additive only. No import from this module reaches into another module's internals;
it calls their public API exactly as the tests do.

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional

from .claim import Claim
from .attest import Attestation, Admission, attest, admit
from .commons import Commons
from .orgbook import OrgBook
from .calibrate import CalibratedFloor
from .q16 import Q16
# NOTE: no re-implementation of reproduction, signing, admission, deposit,
# forgetting, or routing. This file is the *sentence*, not a new word.


@dataclass(frozen=True)
class Enrollment:
    """One credential's walk of the whole spine, as the schoolhouse booked it.

    `admission` is the recipient's OWN verdict (attest.admit) — never the
    issuer's. `deposited`/`weight` record what entered the commons (R2). Nothing
    here is a second decision procedure: every field is a value some shipped
    function returned, plus the org rows this enrollment wrote."""
    key: str
    admission: Admission
    deposited: bool
    weight: int                      # pooled evidence deposited = len(admission.trusted); 0 if refused
    source: Optional[str]            # the issuer id the deposit is tagged with (provenance for L2 trust)
    dispatch_ids: tuple              # tuple[str, ...] — the org receipts this enrollment booked


class Schoolhouse:
    """A node that admits strangers' credentials on its own authority and keeps
    a living, forgettable, replay-verifiable memory of what it came to trust.

    Holds exactly two pieces of durable state, both already replay-verifiable
    on their own: an `OrgBook` (the WAL of every schoolhouse action, G18) and a
    `Commons` (the trust-weighted, forgettable memory of admitted routes, R2/G11/
    G12). It adds no third store and no float."""

    def __init__(self, name: str = "schoolhouse", *, quorum: int, diploma: int):
        self.org = OrgBook(name, diploma=diploma)
        self.commons = Commons(quorum=quorum)
        self._n = 0                  # monotonic dispatch counter, for stable ids

    def _next_id(self, phase: str) -> str:
        self._n += 1
        return f"{phase}-{self._n:04d}"

    # ── G16: reproduce, booked ──────────────────────────────────────────
    def reproduce(self, books: dict, *, reading_fn: Callable, quorum: int,
                  floor: Optional[CalibratedFloor] = None,
                  runner: str = "swarm", base_verdict: str = "ACT") -> Claim:
        claim = Claim.from_books(books, reading_fn=reading_fn, quorum=quorum, floor=floor)
        did = self._next_id("reproduce")
        self.org.record_dispatch(did, tier="claim", task_class="reproduce",
                                 runner=runner, verdict=base_verdict,
                                 outcome=("viable" if claim.earns_standing() else "halt"),
                                 base_verdict=base_verdict, answer=base_verdict)
        return claim

    # ── G17: issue, booked ──────────────────────────────────────────────
    def issue(self, claim: Claim, *, signer: str, seed_hex: str,
              floor: Optional[Q16] = None) -> Attestation:
        att = attest(claim, signer=signer, seed_hex=seed_hex, floor=floor)  # refuses if unreproduced
        did = self._next_id("attest")
        self.org.record_dispatch(did, tier="attest", task_class="attest",
                                 runner=signer, verdict="ACT", outcome="viable",
                                 base_verdict="ACT", answer="ACT")
        return att

    # ── G11 + G14 + R2 + G18: admit under OWN trust, deposit if conferred, book ──
    def enroll(self, att: Attestation, pubkeys: dict, *, key: str,
               trust: dict, quorum: int,
               floor: Optional[CalibratedFloor] = None,
               reading_magnitude: Optional[Callable] = None,
               base_verdict: str = "CONFIRM") -> Enrollment:
        """Admit `att` on the SCHOOLHOUSE's own authority, and — iff conferred —
        deposit the conferred standing into the commons, tagged by the issuer.
        The org books the admission dispatch, routed by the ISSUER's standing at
        this door: correct = conferred, so an issuer whose credentials keep being
        refused (padded with untrusted rings) never earns a fast path here."""
        a = admit(att, pubkeys, trust=trust, quorum=quorum, floor=floor,
                  reading_magnitude=reading_magnitude, base_verdict=base_verdict)
        dids = []

        # THE ONE BRIDGE (see § below): a conferred admission becomes R2 memory.
        deposited, weight, source = False, 0, None
        if a.conferred:
            weight = len(a.trusted)                        # integer, exact: how many trusted witnesses reproduced
            source = att.signer                             # provenance → second-layer G11 over issuers
            self.commons.deposit(key, a.value, weight, source=source)
            deposited = True

        # G18: book the admission, routed by the issuer's own booked history here.
        did = self._next_id("admit")
        route_v, _ = self.org.route(task_class="admit", runner=att.signer,
                                    base_verdict=base_verdict)
        self.org.record_dispatch(
            did, tier="admit", task_class="admit", runner=att.signer,
            verdict=a.verdict, outcome=("conferred" if a.conferred else "refused"),
            base_verdict=route_v, correct=a.conferred, answer=a.verdict,
            reason=a.reason)                                 # refusal reason is a booked field, never silent
        dids.append(did)
        return Enrollment(key=key, admission=a, deposited=deposited,
                          weight=weight, source=source, dispatch_ids=tuple(dids))

    # ── G12: forget, booked, through every read path ───────────────────
    def forget(self, key: str, answer: Optional[str] = None, *,
               runner: str = "custodian") -> str:
        self.commons.forget(key, answer)                    # tombstone folded into commons.root()
        did = self._next_id("forget")
        self.org.record_dispatch(did, tier="custodian", task_class="forget",
                                 runner=runner, verdict="ACT", outcome="viable",
                                 base_verdict="ACT", answer="ACT")
        return did

    # ── reading the memory, optionally through a SECOND layer of trust ──
    def recall(self, key: str, *, issuer_trust: Optional[dict] = None) -> Optional[str]:
        """The schoolhouse's best admitted answer for `key`. With `issuer_trust`,
        the commons is first re-scaled by each ISSUER's earned trust (a stranger
        issuer defaults to 0) — G11 applied a second time, at the credential layer
        rather than the witness layer. Without it, a plain pooled-weight recall."""
        c = self.commons.trust_weighted(issuer_trust) if issuer_trust is not None else self.commons
        return c.recall(key)

    # ── the three pins (content-addressed agreement over the whole chain) ──
    def pins(self) -> tuple:
        """(org WAL chain, org decisions digest, commons root) — the three
        32-byte-ish content addresses that make the WHOLE schoolhouse
        replay-verifiable. Two schoolhouses fed the same script agree on all
        three; a forgotten route changes the commons root and nothing silently."""
        return (self.org.chain(), self.org.decisions_digest(), self.commons.root().hex())
```

`record_dispatch` accepts `**extra`, so `reason=a.reason` is booked as an extra
residue field (the `v2-refused`-style row the family already keeps) without
touching `orgbook.py`. `route(task_class=..., runner=..., base_verdict=...)` is
the shipped signature (`orgbook.route(task_class, runner, base_verdict)`).

Export from `jev_quilt/__init__.py` exactly as the family does its public names:
`Schoolhouse`, `Enrollment`.

## The one bridge (the only genuinely new logic)

Every rung is shipped. The composite introduces exactly **one** decision the
shipped modules leave open: *when a stranger's attestation confers standing on this
node, what enters the commons, at what weight, tagged as whose?* `attest.admit`
returns an `Admission(conferred, verdict, value, trusted, dropped, ...)` and stops;
`commons.deposit(key, answer, weight, source)` takes exactly those raw materials.
Nothing wires the two, because the wire is a *policy*, not a mechanism. Resolved
here, at dispatch altitude, so no further wake is needed for the build:

- **Answer = `admission.value`.** The recipient's own recomputed consensus — never
  the issuer's advisory `att.consensus`.
- **Weight = `len(admission.trusted)`** — the count of trusted, non-drifting
  witnesses *this recipient* actually counted. Integer, exact, and it is the
  recipient's honest measure of the evidence, not the issuer's. Ten admissions of
  the same route from many issuers pool the way `commons` already pools cells —
  a route no single credential earned alone can become schoolhouse-earned.
- **Source = `att.signer`** (the issuer). This is the load-bearing choice: tagging
  the deposit by issuer is what lets the commons be read a **second time** through
  `trust_weighted` over *issuers* — so the schoolhouse gets G11 twice, once at the
  witness layer (inside `admit`) and once at the credential layer (over the commons).
  A laundered credential that somehow cleared `admit` at one recipient still scales
  to 0 in a *downstream* schoolhouse that distrusts its issuer. Faith is walked out
  of the credential layer the same way `commons` already walked it out of the cell
  layer.
- **Refused ⇒ deposit nothing.** `conferred is False` writes no commons row; the
  org still books the refusal (with its reason) — refusal is a first-class ledger
  row, never a silent gap.
- **Correct = `conferred`** for the admission dispatch's org receipt (Law 5:
  viability binary). This is doctrinally exact: the acceptance test of *"admit this
  credential"* is *"did it confer standing for me?"* An issuer whose padded
  credentials keep being refused never accrues booked-correct runs, so it never
  earns ANSWER-standing at this door — R2 applied to issuers, falling straight out
  of G18. (Standing here routes the *supervision level* of future credentials from
  that issuer; it never skips re-verification — `admit` always re-derives the root
  and recomputes consensus. Earned trust buys a lighter touch, never blind faith.)

That is the whole of the new code. Everything else in `schoolhouse.py` is a call
to a shipped function followed by a `record_dispatch`.

---

## Acceptance test plan — `tests/test_schoolhouse.py` (1:1 with the four predicates)

Build small witness books with `Bookkeeper.book(...)` and a `reading_fn` reading
the residue, exactly as `test_attest.py` / `test_claim.py` do; mint identities with
`signed_receipts.generate_identity(node, gen) → (signer, seed_hex, pk_hex)`.

### Predicate 1 — the full chain runs green
`test_full_chain_confers_deposits_earns_and_books`
- 5 unanimous witnesses reproduce `"42"` (quorum 3) → `claim.earns_standing()`.
- issuer attests; a stranger schoolhouse (`quorum=3`, full witness trust) `enroll`s.
- **Assert:** `enrollment.admission.conferred`, `verdict == "ANSWER"`,
  `value == "42"`; `enrollment.deposited is True`, `weight == 5`,
  `source == issuer`.
- **Assert R2 landed:** `school.recall("season-count") == "42"`, and
  `school.commons.earned("season-count") is True` (pooled weight 5 ≥ quorum 3).
- **Assert G18 booked it:** the org WAL holds a `reproduce`, an `attest`, and an
  `admit` receipt in order; `org.book.verify()` is True (ticks 1..N, no gaps);
  every shipped-step dispatch id is present in the enrollment / org.
- **First acceptance predicate, stated crisply:**
  `enroll(attest(reproduce(books))).admission.verdict == "ANSWER"` **and**
  `school.commons.recall(key) == claim.consensus()` **and** the org WAL replays
  clean — reproduced-attested-admitted-deposited-booked, one green breath.

### Predicate 2 — a laundered credential dies at the stranger's door
`test_laundered_credential_dies_and_deposits_nothing`
- Mirror `test_attest.py::TestRecipientReweightsLaunderedCredential`: `clean1/clean2`
  genuinely reproduce `"42"`; `ring1/ring2` collude to pad the chorus (also report
  `"42"`); `quorum=4`. Issuer trusts the ring → `claim.earns_standing()` → a validly
  signed attestation (`verify_attestation.ok` — nothing is forged).
- Stranger schoolhouse `enroll`s with `trust={clean1:1, clean2:1, ring1:0, ring2:0}`,
  `quorum=4`.
- **Assert:** `enrollment.admission.conferred is False`,
  `reason == "not_reproduced_for_recipient"`, `trusted == ("clean1","clean2")`,
  `dropped == {"ring1","ring2"}`.
- **Assert nothing entered memory:** `enrollment.deposited is False`,
  `school.commons.recall(key) is None`, `school.commons.weight(key) == 0`.
- **Assert the refusal is booked, not silent:** the `admit` org receipt exists with
  `outcome == "refused"`, its residue carries `reason == "not_reproduced_for_recipient"`,
  and its `correct` folds False (so the issuer earns no standing at this door).
- **Assert same bytes, different verdict:** a *mirroring* schoolhouse with
  `trust={all 4: 1}` confers and deposits weight 4 from the identical attestation —
  the difference is entirely the recipient's re-weighing, nothing the issuer hid.

### Predicate 3 — a forgotten route stays gone through every read path
`test_forgotten_route_stays_gone_every_read_path`
- Enroll a conferred route so `recall`/`weight`/`earned`/`sources`/`trust_weighted`
  all see it; assert they do.
- `school.forget(key, "42")`.
- **Assert gone through every read path** (the G12 predicate, on the schoolhouse):
  `commons.recall(key) is None`; `commons.weight(key) == 0`;
  `commons.earned(key) is False`; `issuer not in commons.sources()`;
  `school.recall(key, issuer_trust={issuer: 5}) is None` (trust-weighted read is
  purged too — the provenance-keyed G11 path cannot resurrect it);
  `commons.trust_weighted({issuer: 5}).recall(key) is None`.
- **Assert the erasure is witnessed, not silent:** `commons.root()` **changed** vs.
  before the forget (the tombstone is folded in); a second schoolhouse that replays
  *surviving deposits + this tombstone* lands on the **same** root
  (`school_a.commons.root() == school_b.commons.root()`).
- **Assert it survives gossip of an un-forgotten copy (honest limit made a test):**
  merge in a stranger `Commons` that still holds `(key,"42")` — after the merge the
  pair is still absent from every read path of the schoolhouse's own commons
  (the tombstone purges it on merge), while a stranger that never received the
  tombstone would still carry it. Forgetting is local-until-gossiped, by design.
- **Assert G18 booked the forget:** a `forget` org receipt exists;
  `org.book.verify()` holds.

### Predicate 4 — replay ≡ live across the whole chain
`test_replay_equals_live_over_the_whole_schoolhouse`
- Drive a fixed script — reproduce, attest, several enrolls (some conferred, one
  laundered-and-refused), one forget — on schoolhouse A.
- **Assert org replay ≡ live:** `[d.verdict for d in org.replay()]` equals the
  live verdict sequence recorded during the run (the `orgbook.py` guarantee, over
  the composite's dispatch stream).
- **Assert the whole chain is content-addressed:** build schoolhouse B from the
  **same script** (differently-named cells) → `A.pins() == B.pins()` (org chain,
  decisions digest, **and** commons root all agree). Build schoolhouse C with one
  step diverged (a laundered credential the recipient here *trusts*, so it confers)
  → `C.pins() != A.pins()` — the divergence shows up in the commons root and, once a
  later dispatch observes changed standing, in the decisions digest, exactly as
  `test_orgbook.py`'s pin test shows for the org alone.
- **Assert the rebuilt-object invariant:** feed B's org a fresh `OrgBook` the same
  WAL entries → `rebuilt.replay() == B.org.replay()` (replay ≡ live, not replay ≡
  this Python object — the `orgbook.py` invariant, carried up to the composite).

Run `python -m unittest discover -s tests`; full suite green (new + all existing),
**no test weakened or skipped**. Add a hard-coded `pins()` vector (like the
`attestation_root` / `diploma_root` cross-language pins) so a non-Python port can
reproduce the whole schoolhouse's three addresses from the same script.

---

## Tier / wake

**ACT-tier build, checked by a runner (CONFIRM).** It is additive; it reuses
`claim` / `attest` / `commons` / `orgbook` / `calibrate` unchanged; it has exactly
**one** design fork (the Admission→deposit bridge — weight, provenance, correctness
polarity), resolved above at this pass; and it has a clean 1:1 predicate. This is
the same shape as the hauls that landed clean before it (G16: arch → build →
confirm; G17: `attest.py` from a resolved fork). **No further Opus wake is needed
for the build.** The dispatcher can book `schoolhouse → Sonnet` immediately against
this spec, then `→ Haiku` to independently re-run the four predicates.

## The one real remaining fork (flagged, not built — a genuine future wake)

The bridge deposits by issuer so the commons can be read through a **second** layer
of G11 trust. That reveals — but does not resolve — a deeper question the composite
makes visible for the first time: **does trust compose across the layers as a single
algebra?** The schoolhouse now has trust at the *witness* layer (inside `admit`) and
trust at the *issuer* layer (over the commons). Today they are applied *serially and
independently* — witnesses filtered first, issuers scaled after — which is a
deliberate, sound, gated composition (each layer's zero kills the contribution).
Whether the correct end-state is instead a **multiplicative** trust that flows
witness→issuer→commons→org as one associative operation — a "trust functor" the
whole spine obeys — is a **law-level** question, not wiring. It is out of scope for
this build (the serial/gated form satisfies every predicate above) and is filed as
the composite's contribution to the Fable dossier (see C8). **Flag: trust-algebra
across layers needs a future top-tier wake; do not pre-build it.** This is the exact
shape of B's honest split in `NEW-DIRECTIONS.md` (build the replay-verifiable org
now; flag the metabolism/conservation half for a future wake).

## Dual track (same law, both sides)

| | toy (a table) | industrial (rough seas) |
|---|---|---|
| **the schoolhouse** | Three kids counted the jar and all said 42 (G16). A teacher writes a card *with the three names on it* and signs it (G17). A **second classroom** gets the card, crosses off a name it doesn't trust (his glasses fog), recounts from the names left, and — only if they still agree — **pins the answer to its own wall** (R2 into the commons), noting *which teacher* sent it (issuer provenance). Later, a kid asks to be forgotten: the class **crosses the answer off the wall and writes on the log that it did so** (G12 tombstone), so no one can pretend it was never there. Every card in and every cross-off is written on the class's own index-card ledger, so a stranger can replay the whole term (G18). | A `Schoolhouse` composing `Claim`→`attest`→`admit`(own trust/quorum/floor)→`commons.deposit`(by issuer)→`commons.forget`(tombstone), every step `record_dispatch`'d onto an `OrgBook`; the whole chain pinned by (org chain, decisions digest, commons root) and replay-verifiable end to end. A federation of schoolhouses honoring each other's diplomas with no central registrar and no forced global memory. |

Same law both sides: **a credential is authority you can reconstruct and memory you
can prove you forgot — never authority you must accept, nor a record you must trust
was never edited.**

---

## Honest limits

- **STRETCH (inherited, cross-*instance* not cross-*language*).** As with
  G13/G14/G16/G17, both "kernels" in the tests are this same Python implementation,
  so the schoolhouse proves cross-*instance* federation (independent verifications,
  independent commons) not literally cross-*language*. The true cross-language
  morphism rests entirely on the byte-canonical discipline the composed modules
  already carry (`canonical_attestation_bytes`, `attestation_root`, `commons.root`,
  `orgbook.chain`/`decisions_digest` touch nothing but UTF-8/sha256/MMR) and is
  pinned by the hard-coded `pins()` vector a non-Python port can reproduce.
- **STRETCH (forgetting is local-until-gossiped).** Inherited whole from
  `commons.merge`'s tombstone rule: the schoolhouse's `forget` suppresses a pair
  everywhere the tombstone has propagated, not instantaneously across every copy in
  the federation. A node that never receives the tombstone still carries the pair.
  That is deliberate — instantaneous global erasure would require a surveillance
  archive of all copies, which is exactly what the right to leave is against — and
  predicate 3 tests the honest semantics, not a fantasy of global reach.
- **The trust-algebra fork is unresolved (see above).** The two G11 layers are
  composed serially and gated, which is sound and predicate-satisfying, but whether
  they should be one associative trust operation is a real open law-level question,
  filed as C8, not answered here.
- **O(N) attestations, inherited from G17.** The schoolhouse admits attestations
  that carry every witness reading; its per-credential cost is linear in the swarm,
  not O(1). Re-weighability is the whole point, so this is a load-bearing cost, not
  a defect — a sampled-proof variant is a later rung with its own predicate, not a
  thing to hedge now.
- **The metabolism half of G18 is still absent.** The schoolhouse books *routing*
  (which tier/issuer, replay-verifiable) but not *cost-as-conserved-budget* (O7/R5).
  It inherits G18's honest split unchanged: the org runs on the quilt; the org's
  *metabolism* does not yet.

**Least-certain claim.** That **`len(admission.trusted)` is the right deposit
weight** — the recipient's own count of trusted, non-drifting witnesses. It is
exact, it is the recipient's honest measure, and it makes pooling across credentials
behave exactly like `commons`'s pooling across cells. But an alternative — deposit a
flat weight 1 per conferred credential (one credential, one vote, regardless of how
wide its swarm) — is also defensible and would make a schoolhouse's memory count
*credentials* rather than *witnesses*. I choose witness-count now because it carries
the evidence's true breadth into the pooled weight, and because it degrades
correctly under the second trust layer; the flat-per-credential variant is a
tunable a future fleet can pick with its own predicate, not a fork to hedge on here.

---
*Companion to [`NEW-DIRECTIONS.md`](NEW-DIRECTIONS.md) (the three directions; this
composes A+B and the shipped G11/G12/G14 into one path) and
[`../FABLE-DOSSIER.md`](../FABLE-DOSSIER.md) (closes bootstrap-gate #1; reveals
candidate C8). Additive only — the immutable move set is untouched; this is the
sentence the shipped words already spell.*
</content>
</invoke>
