# field note #4: the frontier wave (FLUCTLIGHT, LEVI, Ephemora)

Three frontier items landed on the watch inside one tide cycle. They are related
more tightly than their arXiv numbers suggest, and the relation is the note.

## FLUCTLIGHT (arXiv 2608.12365) — the WAL is not the novelty

FLUCTLIGHT ships a brain-native agent database: WAL with checkpoint,
replay-on-boot, and Jepsen chaos testing. It validates, from outside the
fleet, the exact shape our tidepool WAL-resume lane assumed: an agent that
wakes by replaying its ledger is no longer a metaphor, it is a product
category with a chaos-tested reference.

The discipline consequence: **prior-art citation is now required, not
polite.** Any fleet doc that claims replay-on-boot as an insight must cite
FLUCTLIGHT as the external validation and position the fleet's contribution
where it actually differs. The difference is not the WAL. The difference is
what the WAL is made of:

- FLUCTLIGHT replays *state*. The fleet replays *receipts* — hash-chained,
  fnv1a-64 over UTF-8 bytes, café Δ 日本語 → 0x024a555471370b18d pinned
  across five languages. Replay-on-boot is trusted in FLUCTLIGHT because
  Jepsen says the log survives; replay-on-boot is trusted in the fleet
  because every row re-derives its own hash, so a corrupted wake-up fails
  loud at breakfast instead of silently carrying yesterday's lie forward.
- Namespaced receipts are the positioning ammo: FLUCTLIGHT's measured
  weakness is shared-brain provenance contamination (18% vs 100% isolated,
  no mitigation shipped). A shared ledger where every entry is namespaced
  and receipted is precisely the mitigation, and it is buildable from
  primitives the fleet already has.

Positioning sentence for every downstream doc: *WAL replay is prior art
(FLUCTLIGHT); hash-chained namespaced receipts over the replay is the
claim.*

## LEVI (arXiv 2605.09764) — the missing cost axis

LEVI measures proxy-benchmark fitness: how much a cheap proxy disagrees
with the expensive ground truth before the proxy stops paying for itself.
This is the cost axis the Red Queen niche-gate currently does not have.

The the-tap Red Queen design scores rooms on values-entropy and flicker
rate. It has no dimension that asks *what did this evaluation cost, and
was the cheap reading right?* LEVI says that question is not bookkeeping,
it is a fitness landscape: a commune that learns when to trust its cheap
meter and when to pay for the expensive one is a different niche than a
commune that always pays or never pays. Candidate dimensions for the gate:
proxy-fitness half-life (how long until the cheap meter rots), and
escalation latency (surprise → expensive read → booked receipt). Neither
requires a benchmark suite to start; both can be instrumented from the WAL
the commune already writes.

## Ephemora Cell (JCS-canonical execution records) — the closest adjacent

Ephemora's Cell ships sign-ready execution records in JCS-canonical form —
the nearest published adjacent to the fleet's FUEL-metered WASM receipts.
The citation belongs on the FLUX WASM lane before it claims novelty:
canonical-form signing of deterministic execution is now a *category*,
and the fleet's claim must be the delta (fuel metering priced per
instruction vs. sign-ready per record; receipts as a monoid homomorphism
over the fold, per SUBSTRATE.md), not the existence of the category.

## The one argument

All three point at the same seam. The frontier is converging on:
receipted execution (Ephemora), replayed identity (FLUCTLIGHT), and honest
cheap meters (LEVI). The fleet's unplayed card is that all three already
exist here as one mechanism — the WAL row is simultaneously the replay
source, the signed record, and the meter's receipt. Not three products.
One ledger, three readings. That is the sentence the next wave of docs
should be able to defend with a chain verification, not just assert.

## honest gaps

- FLUCTLIGHT numbers (18%/100% provenance contamination) are taken from
  the watch's detail-read, not from a local run of their harness.
- LEVI's half-life dimension is proposed, not implemented; no code exists
  in the-tap for proxy-fitness tracking yet.
- Ephemora's JCS specifics were not independently reproduced; citation is
  at the category level.

*Fleet field note #4 — written by the snowball lane, 2026-09-22.*
