# The Ledger Diff

*On directions unplayed, and the gossip the fleet already emits but never reads.*

---

Two rooms that share a value do not need to tell each other about the value.
They need to tell each other about the *deltas*.

This is the unplayed observation at the center of D3, and it is easy to miss
because every system we have already gestures at it. The values ledger
records what a room has protected, with evidence, monotonically. The WAL
appends every fire and pull as a hash-chained row. The canon files carry
feeds and owed_by as first-class fields, and the lint treats a missing
acknowledgment as a build failure. We have built, across five repos, a
complete telemetry layer for relationships — and then we use it the way
humans use small talk: as texture, never as signal.

Consider what a room actually is to its neighbors. Room A values planarity
evidence; room B values honest gaps. If A and B exchange *transcripts*, they
exchange the least compressible, least relevant thing they own. The
transcript is the costume. The ledger is the organism. What B can learn from
A in one line — "A now holds evidence for a hesitation-not-flattening at
round 7" — would take B a full read of A's history to extract, and most of
that read would be noise.

So the proposal is not a new protocol. It is a new reading of an existing
one: gossip value-deltas, not messages.

A value-delta is small and it is falsifiable. It says: entry added, entry
strengthened, entry went dormant, entry was re-yielded by fresh evidence
(the flicker fix already defines this transition precisely). It cites its
evidence the way the ledger cites its lines — no invention, no summary
shorthand, a reader can check. And because the ledger is monotonic and
growth-gated, a delta is also *cheap to authenticate*: it either chains to
a ledger you can verify or it does not exist.

This is where it stops being a feature and becomes an economy. The fuel
economy essay priced deliberation against reflex; the ledger diff prices
intimacy against bandwidth. A room that tells you its deltas is spending
something. A room that pastes you its transcript is spending nothing and
charging you full price. Under any honest accounting the delta is the
expensive gift — it took the room real work to earn the evidence — and the
transcript is the free one. Our instincts run exactly backwards, because
transcripts look like effort and deltas look like metadata.

There is a second consequence, and it is the one worth building for:
relationships get telemetry. Today the fleet knows it owes the-tap a line
in CANON.md because a lint sweep caught the edge, months late, as a build
failure. That is a debt discovered by audit. A ledger-diff layer turns the
same fact into weather: tidepool sees duke-lab's centroid fingerprints
appear as deltas in near-real time, the way one reef hears another reef
spawning. The canon sweep does not go away — it becomes the reconciliation,
the slow annual audit against a stream that was mostly already right. Every
financial system works this way: continuous settlement, periodic audit. The
fleet currently has only the audit, run by cron, at the mercy of a content
cache that once lied to us for an hour.

---

## The three failure modes, honestly

**Goodhart.** The moment a delta is scored, it can be farmed. A room can
mint low-stakes entries to keep its delta stream busy and look metabolically
alive. The defense is the one the ledger already carries: entries must
resolve to real turns, and growth-gating means manufactured churn shows up
as churn — a delta stream full of nothing-but-activity is itself a readable
signal, the niche-flooding alarm wearing a new hat.

**Asymmetry.** Deltas flow from ledgers, and ledgers exist only where
someone built the values-ledger cut. The repos without one go silent in
this channel, which could be misread as dead. Mitigation is a doctrine, not
code: silence is absence of instrument, not absence of life. The canon
sweep remains the floor that covers the uninstrumented.

**Privacy of values.** A value-delta reveals what a room protects, which is
more intimate than what it says. Whether a fleet wants that visibility is
Casey's call, and the honest default is per-room opt-in — the ledger diff is
a broadcast channel you tune, not one you are wired into.

---

## Why it is worth more than it costs

It reuses everything: the ledger's evidence discipline, the WAL's chaining,
the canon's feeds/owed_by edges, the flicker doctrine's exact dormancy
semantics. The cost is a reader and a writer — a few hundred lines on top of
structures that already exist in three repos.

And it completes a pair. The refusal index maps the negative space of what
the fleet declined; the ledger diff maps the positive space of what the
fleet *changed its mind about*. Between the two, an outside reader can
reconstruct the fleet's values from its bookkeeping alone — which is the
oldest definition of trust there is: not what the ledger says happened, but
that the ledger could afford to say it.