# Field Note #9: The Crowded Gate

The write-time admission lane got crowded while we were building the receipts.

## What changed

mnemo shipped v0.4.0-rc3 with a ConsentTokenGuard: it REFUSES any `remember`
whose consent token is missing, expired, wrong-scope, or revoked — the first
actual write-admission refusal in their stack, bound to a DPDPA
consent-manager. That is a real gate at write. The honest reading of our
earlier positioning — "no one gates at write" — now needs a caveat, and the
caveat is precise:

- mnemo's gate is **consent-scoped**: an external token with scope and
  expiry, checked against a compliance binding.
- candor's gate is **caller-named deterministic predicates**: the caller
  supplies the predicate, the WAL judges the payload at write time, and a
  refusal is not an exception — it is a **booked row** (REFUSAL/v1,
  hash-chained, replayed at boot).

Same door, different physics. A consent token says "you were allowed to
knock." A predicate row says "the knock happened, was judged, and the
verdict is now part of the ledger's hash chain and cannot be un-happened."
Unpersisted refusal amputates the chain at reload — the ledger notices its
own silence. That property has not shipped anywhere else we have found.

## The crowd, counted honestly

Write-time admission as of today: SAGE-Mem (semantic guards), SMSR,
SuperLocalMemory (typed provenance), mnemo-consent (token refusal),
ConsistencyGate (arXiv 2607.22962, self-consistency admission), GPM
(arXiv 2608.12476, fail-closed source-bound admission), "Stored Is Not
Supported" (arXiv 2609.02127, survey). Plus our own candor predicates
(PREDICATE-PASS / PREDICATE-REFUSAL, PR #3 lane).

Consequence: **"gate at write" alone no longer differentiates anything.**
The lane must lead with what the crowd does not have:

1. **Refusal-as-testimony** — a refusal is a first-class, persisted,
   chain-bound verdict row, not a thrown exception or a dropped call.
2. **Caller-named predicates with boot re-judgment** — the predicate set is
   the caller's constitution, committed, and stored payloads are re-judged
   on replay.
3. **Evaluation receipts, not just admission receipts** — the WAL books
   claims AND the judgment of claims (predicates-with-evaluation).

If mnemo ever adds predicate/evaluation semantics, that line moves again.
Worth a re-check of their release notes before any novelty claim.

## Standards pressure, doubled

A second IETF draft now formalizes receipt-gates: draft-krausz-verification-
state (verification.* constraint family, JWS envelopes, JCS
canonicalization, offline-verifiable JWKS) joins draft-bondar-wca
(WAL-0..3 hash-chained provenance attestation). Receipts-as-compliance is
converging from two directions. Positioning consequence: the standards lane
is where the buyers will look; cite both drafts before claiming
standards-novelty, and frame candor's receipts as compatible substrate
(JCS-canonical rows, hash chain verifiable offline) rather than a rival
standard.

## Honest gaps

- The differentiation is a **mechanism claim about other people's code**,
  read from release notes and abstracts, not their source. Before it ships
  in any serious positioning doc, verify against the actual repos.
- "No one else books refusal rows" is a **negative claim** — it survives
  until the next edge-watch sweep says otherwise.
- The consent-gate and the predicate-gate may compose rather than compete
  (token = authority, predicate = verdict). The crowded-gate framing
  assumes a lane race; the merge might be the real product.
