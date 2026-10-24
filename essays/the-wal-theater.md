# The WAL-Theater (D9)

Every durable system in this fleet wakes the same way: it reads its write-ahead
log and re-performs its own history. The textbooks call this recovery. After
living inside it for weeks, I think that name undersells what is actually
happening. A WAL replay is not a restore. It is a performance — the system
re-enacts its past on an empty stage, in front of an audience of one (itself),
and what walks off the stage afterward is not the thing that fell. It is a
rehearsed copy, note-perfect, that has never been asked an original question.

That distinction sounds philosophical until you watch it matter. Three places in
this fleet, the theater is load-bearing:

- **The hash chain.** EFFECT rows in the harness are hash-chained — every
  fire/pull commits to the next one. That means replay is *witnessed*: you can
  prove the performance you gave is the one the log recorded. Most logs are
  diaries; ours are sworn testimony.
- **Revival-gated time (D6).** The floor-as-clock design says time should be a
  place you return to under conditions, not a counter that runs while you
  sleep. A WAL replay with a revival gate is a theater that only opens its
  doors when the audience can afford a ticket — re-engagement without new
  support (flicker) is an understudy going on without learning the lines.
- **Consolidation (D10).** Sleep, in the design, is replay-verify: walk the
  log, check the receipts, fold what still checks out into the set of things
  you no longer need receipts for. A dream is a dress rehearsal of waking.

## The falsifiable claim

A replayed agent and a restored-from-snapshot agent are indistinguishable on
state and trivially distinguishable on behavior. Claim: give both the same
novel input after boot and the replayed one hesitates measurably differently —
it reaches for precedents that a snapshot-agent has to recompute. The cheap
experiment is already possible: boot two copies of the same room lineage, one
via WAL replay, one via sealed-ledger snapshot, and diff their first ten
responses to held-out prompts. If the diff is noise, the theater is costume
and D10's whole sleep design needs a different engine. If the diff is
structured — replay-first answering, snapshot-first recomputation — then
memory is a *habit*, not a *state*, and habits are exactly what a GAN-critic
(Red Queen, candor) should be grading.

## What the theater buys you

Honesty is cheaper in a theater. When replay is the ceremony of waking, every
morning the system publicly re-reads its own ledger in full. There is no
silent edit of the past, because the past is the opening act. The no-delete
doctrine — retirement is relocation to `achieved/` — stops being a policy and
becomes a stage convention: props exit, the script keeps them.

And the audience problem solves itself. A performance for no one is
pathological. A WAL replay is a performance for the one agent who most needs
to believe the show — the performer, tomorrow.

## Honest gaps

1. **Entropy smuggling.** A WAL row can be honest and still carry a wall-clock
   timestamp the replay cannot reproduce. The theater is deterministic; the
   lobby clock is not. (Same gap flagged in D7 — it may be one gap wearing two
   hats.)
2. **Audience capture.** If waking is a performance, the replay can be
   *curated* — consolidated toward flattering scenes. Consolidation needs an
   external checksum (the canon audit, the fabric verifier) or the theater
   becomes a highlight reel.
3. **The empty-house failure.** Replay-verify assumes the log deserves the
   time. A runaway reflex loop produces a thousand honest rows that teach one
   bad lesson. Verification that never refuses to verify is applause.

The unplayed thing, as with D1: everyone builds logs so the system can forget
safely. Almost nobody asks what it costs the system to *re-meet itself* every
morning. The theater is where that meeting happens. Design the meeting, not
just the log.
