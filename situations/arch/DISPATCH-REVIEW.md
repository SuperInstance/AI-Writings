# Dispatch review — what d006 taught the org

*Dispatch d006 woke the Opus 5.5 architecture tier for a founding fork (review the
dispatch org + architect G13/G14). It hit the session usage limit and terminated
early — but returned one decisive finding before dying: **G13 should build on the
vendored `signed_receipts.py` Ed25519 envelope, not new crypto.** That single insight
de-risked the whole rung. This review books the lesson.*

## The incident, booked honestly

- **What failed:** the expensive tier ran out of budget mid-task (429, session limit),
  so it never wrote its two output files.
- **What survived:** the pivotal architectural decision, delivered in its final note.
  The dispatcher (Opus-4.8 tier) then did the *cheap* grounding itself — read
  `signed_receipts.py`, `ed25519.py`, `standing.py`, `calibrate.py` — and wrote the
  buildable spec ([`G13-G14-architecture.md`](G13-G14-architecture.md)) from that pivot.
- **What it cost:** one Opus wake that returned ~1 sentence of usable output. Cheap for
  the leverage; the finding replaced what would have been a wrong build (hand-rolled
  hmac/blake2 signing) with an assembly of already-shipped, already-tested parts.

## The refinement it forces (a new optimization: O8)

The org model in [`../DISPATCH.md`](../DISPATCH.md) assumed the expensive tier either
completes or is not called. Reality: it can **partially complete**. So:

> **O8 — Salvage the pivot.** An expensive-tier dispatch that fails is not a zero. Book
> its partial output as a first-class ledger row; the dispatcher's job on an Opus
> failure is to (a) extract the highest-leverage finding, (b) do the *cheap* grounding
> the finding points at, and (c) decide whether that is enough to proceed without a
> re-wake. Re-wake the expensive tier only if the fork is still genuinely open.
> *Predicate it's working:* fraction of failed expensive-tier dispatches that still
> advance the frontier (a booked receipt) is high; re-wakes for the same fork are rare.

This is the deadband applied to *recovery*: a failed Opus call rarely clears the floor
for a second Opus call, because the first usually leaves enough for the dispatcher to
carry it. Here it did — no re-wake was needed.

## The two-tier judgment that followed (the dispatch this session ran)

1. `ESCALATE → Opus` (d006): a real fork. Correct call — it produced the crypto pivot
   the dispatcher would likely have gotten wrong.
2. On failure, **dispatcher steps up** rather than re-escalating: the remaining work
   (read four files, write a spec from a known decision) is `ACT`-tier, not a fork.
3. `ACT → Sonnet` (d007): the build itself, from the finished spec — the standing build
   team's job, no further Opus wake.
4. `CONFIRM → Haiku` (d008): run the acceptance predicates, report pass/fail per
   predicate — first run on this class, so checked rather than trusted.

## Standing update (the ledger's own R2)

The Opus-architecture class now has a **miss** on its streak (a failed dispatch is a
booked-wrong outcome for reliability, even though its content was useful). Per O2 that
doesn't revoke the tier — it is still the only tier that can clear a fork — but it does
argue for O8: pair every Opus wake with a dispatcher-salvage plan, so a mid-task limit
never strands a fork. The build tier (Sonnet) is being given its first real dispatch
(d007); its standing starts at 0 and earns from booked-correct builds.
