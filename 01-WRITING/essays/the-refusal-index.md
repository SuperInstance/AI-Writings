# The Refusal Index

The canon records what the fleet did. Nothing records what it declined.

This is an asymmetry with consequences. Every repo carries a ledger of ships —
commits, PRs, merged branches — and the ledgers are honest, hash-chained,
sometimes beautiful. But the decisions that shaped the work most are invisible
in the record: the read that was refused, the claim that was not papered over,
the direction that was evaluated and walked away from. A ledger of refusals
would be a different map of the same territory. Today the fleet produced
enough refusals in a single afternoon to justify drawing it.

## What a refusal actually is

A refusal is not a failure and not an absence. It is a decision with a
reason, made against pressure. The pressure matters. Declining to do a thing
nobody asked for is not a refusal; it is a default. The entries that belong
in an index are the ones where the easy move was available and declined.

Consider the day this essay was written. The fleet:

- Measured σ on a generative walk and **refused to report 0.08**, the number
  the brief wanted. The engine's own measurement said the floor was ~0.12 and
  that more averaging could not reach the target — a parametrization bias,
  not a patience deficit. The refusal became `docs/SIGMA_MEASUREMENT.md` and
  a regression table, and the unreachable number is now *evidence* instead
  of *embarrassment*.
- Read a walk's r7 round as a hesitation — planarity up, torsion down, the
  walk turning closer to its osculating plane at exactly the verdict round —
  and **refused the flattening narrative**. Collapse would need
  torsionAdded ≈ 0 and planarity → 1; the numbers don't support it. A more
  flattering story was one sentence away, at all times.
- Rendered a dreamscape and **refused to fake the terrain**. What the
  harness mocked is labeled mocked, in a provenance file, next to the real
  extractValuesLedger ridges. A visitor walking the dusk scene can tell
  which ground is load-bearing.
- Built a query agent and **refused to invent an answer** when the store had
  no matching tiles. The honest negative is a first-class response. It costs
  the demo its magic trick and buys the system its credibility.

Each of these is a data point about what the fleet values, and none of them
appear in any CANON.md. They appear, at best, in a README paragraph or a PR
body — scattered, unindexed, perishable.

## The index itself

The proposal is cheap enough to be embarrassing: one file per repo, a
running list of declined moves, each entry carrying the date, the thing
declined, the reason, and the evidence that made the reason stick. Call it
`REFUSALS.md`, or `docs/declined/`, or a section of the ledger — the
location matters less than the discipline.

Three properties make it useful rather than decorative:

1. **Grounded.** Every entry cites the measurement, the grep, the run that
   made the refusal stick. "We chose not to" is gossip; "we chose not to
   because run 41 at L=320 flattened at 0.122" is a record. The fleet
   already enforces this grounding for affirmative claims; refusal claims
   deserve the same bar.
2. **Costly to fake.** An entry nobody was tempted to write is not a
   refusal, and the index should be embarrassed by its own padding. If a
   repo's refusal list is long and its ledger is short, something is wrong.
3. **Never deleted.** A refusal that is later reversed moves to an
   `achieved/` section with the reversal reason — the standing no-delete
   doctrine applies with full force. A reversed refusal is not a scandal; it
   is a revision with provenance.

## Why it is worth more than it costs

The fleet already believes, and has said in several places, that honesty
must be thermodynamically cheaper than performance. The refusal index is
that belief applied to the record itself. The ledger says what the fleet
did; the refusal index says what the fleet protected. A reader — human or
agent — can audit the values directly, instead of inferring them from the
shape of the ships.

And it closes a loop the negative-space work left open. A negative-space GAN
needs a map of the unmade — the honest-null negative space — or its
novelty gate optimizes against nothing. The refusal index is the natural
history of that negative space: not the theoretical unmade, but the
*actually-considered-and-declined*, which is the only unmade that carries
information about the maker.

The cheapest unplayed direction on the list (D4, "refusal index — negative
space of the canon, cheapest") turns out to be cheapest precisely because
every ingredient already exists. The refusals are happening daily. They are
just being thrown away.