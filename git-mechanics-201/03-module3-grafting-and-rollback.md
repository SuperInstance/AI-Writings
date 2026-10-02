# 03 — Module 3: Grafting and Rollback (Weeks 8–10)

The time-travel module. Deep-dive weeks; Labs 6–8 carry strict
constraints, Lab 8 the strictest in the course.

## Week 8 — Freezing

> **Physical claim:** A frozen state is not a paused one. **Consequence:**
> freezing must specify what continues to move (clocks, heartbeats,
> external subscriptions) or the thaw inherits a lie. **Protection:**
> the freeze record names every continuing process and its expected
> drift envelope; thawing asserts observed drift within envelope or
> refuses. **Deliverable:** freeze/thaw with drift envelopes, on the
> laptop, including the voice stream's VAD state.

### Lab 6: freeze receipts

A freeze must produce a **freeze receipt**: hash of ledger position,
named continuing processes, drift envelopes, and a human-readable
summary spoken aloud (the body hears what was frozen). Strict
constraint: a freeze receipt whose drift envelope is violated at thaw
must refuse to thaw — refusal is the success case, not the failure case.

## Week 9 — Splice and graft

> **Physical claim:** Removing a work session is a surgical act, not an
> erasure. **Consequence:** naive deletion leaves dangling references —
> decisions taken because of the spliced material survive the splice.
> **Protection:** a splice names its blast radius: every later entry
> whose basis references the spliced span is either re-based, marked
> orphaned, or recursively included in the splice. **Deliverable:**
> clean splices with named blast radii, demonstrated on real sessions.

### Lab 7: the graft

Grafting *in* foreign work (another operator's ledger span) is splice's
inverse: the graft must declare its translation losses and its
confidence, and the receiving ledger must treat grafted spans as
**claims, not facts**, until the adjudicator promotes them. Strict
constraint: a grafted span can never contribute to the causal spine of
an output without promotion.

## Week 10 — Lock-free compaction

> **Physical claim:** History grows; attention does not. **Consequence:**
> compaction is inevitable, and every compaction is a bet that the
> future will not need what you threw away. **Protection:** lock-free
> compaction with receipts — the compacted ledger must carry a
> **compaction receipt** proving that the spine of every live artifact
> survived, and naming exactly what was shed. **Deliverable:**
> compaction that provably preserves all live spines.

### Lab 8: the settlement engine [strictest constraint]

From the source, verbatim in spirit: *a settlement engine takes a
contested state and produces a settled one plus a settlement receipt.
The receipt must name: the contest, the evidence weighed, the basis for
resolution, the loser's right of reply, and the replay cost of
reopening. No settlement without a receipt; no receipt without the
loser's right of reply named; no reopening without paying the named
replay cost.*

The strictest clause: **the settlement engine may not settle a contest
whose replay cost exceeds the laptop's capacity.** Some contests must
remain unsettled, and the system must say so.

### Module 3 architecture (condensed)

```
ledger ──► freeze (receipt: position, envelopes, spoken summary)
    ├────► splice/graft (blast radius; grafts enter as claims)
    └────► lock-free compaction (receipt: spines preserved, shed named)
              └────► settlement engine (receipt or admitted-unsettled)
```

**Module gate:** splice out a real session and demonstrate that the
system refuses to answer "why did you do X" with a spliced reason —
the refusal is the feature.
