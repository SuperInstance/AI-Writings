# L3 — The Ripple in the Calm

> *Legal the whole time. Over-confident the whole time. That is how boats sink.*

**The law:** Viability is binary, but confidence is graded and must be *earned*
(Law 5). A decision that cannot be *illegal* can still be *over-confident* — and
over-confidence is the bored-middle: a fixed guard tuned for normal seas sleeps
through the small real anomaly hiding in a long flat calm. Standing is the
earned, revocable right to act on your own read — and it is the sea, not a
teacher, that revokes it.

**Who this is for:** a deckhand becoming crew, a skipper learning the cost of a
gut call, a model earning the `ANSWER` verdict — the right to stop asking.

**Build against:** `jev_quilt/calibrate.py` (`CalibratedFloor`,
`alarm_calibrated`), `jev_quilt/predictor.py` (`surprise`, `MeanPredictor`),
`jev_quilt/standing.py` (`Standing.from_book`, `verdict`),
`jev_quilt/commons.py` (`Commons`). Toy already ships:
`examples/rough_seas.py`.

---

## The toy — the table version (the sea taken out)

You need: a deck of cards, and patience.

**The game — "the rigged card in the flat deck."**

Deal cards face up, slowly. Almost all of them are near the same value — a long
flat calm, tiny surprises. Somewhere in the run is **one card that's a little
off** — not a screaming outlier, just a small wrong note in a very even hand. The
watcher's job: **call the odd card.**

Here's the trap that teaches the law. Set a **fixed** guard first — *"I'll call
anything more than five off."* In a flat calm where everything is within one or
two, a five-off guard **never fires** — it's legal, it's reasonable, and it
sleeps right through a three-off ripple. The learner who used the fixed guard
loses, and it *feels unfair* — they followed the rule! That feeling is the whole
lesson: **following a fixed rule is not the same as paying attention.**

Now play it with a **calibrated** guard: *"The flatter the last few cards have
been, the smaller a wobble I'll call."* In a dead-flat run, a three-off card is
suddenly loud. The guard **tightens in the calm and relaxes after a spike** — so
it catches the ripple *and* doesn't cry wolf when the deck genuinely gets rowdy.
That's `CalibratedFloor`. Ten lines a kid can read; it's literally
`examples/rough_seas.py` (calm `0.01`, ripple `0.03`, a fixed floor `0.05` that
sleeps through it, a calibrated floor that settles at `0.025` and catches it).

**Earning standing at the table:** keep a tally. Every time a watcher calls the
odd card *right*, they earn a chip on "spotting the ripple." A **streak** of right
calls earns them the right to **stop being checked** — the table takes their call
as truth without a second look. That's **ANSWER** standing. But the first time
they call it *wrong*, every chip is swept — **standing revoked on one miss** — and
they have to earn the table's trust back from zero. Kids feel this keenly; it is
exactly fair and exactly unforgiving, like the water.

---

## The industrial version — the same law, the sea put back

The rogue set in a long flat sea. Weeks of easy hauls; the crew's guard drops
(that's the bored-middle). A `CalibratedFloor` over the predictor's `surprise`
does the opposite of the crew — it tightens *because* the sea is calm, so the one
small anomaly that means the fishery moved doesn't hide in the flat water nobody's
watching. Exact-ℚ, offline, tightening in the calm and relaxing after a spike:
no alarm storm, no permanent deafness.

And the skipper's standing, on the water: Mara has forty seasons of earned
standing — she acts on her own read without asking the deck, the fastest path
there is. Revocable. The first set her gut gets wrong, a scar lands, the standing
tears up, and she earns it back by asking again. **`standing.verdict()` returns
`('ANSWER', proven)` only while the book keeps proving it; one booked-wrong and
it's back to `ACT/CONFIRM/ESCALATE`.** The sea revokes the diploma; no examiner
does.

---

## The exercise (buildable today)

**Toy build:** `python examples/rough_seas.py` — read it, then change the ripple
from `0.03` to `0.02` and find the deadband where the calibrated floor still
catches it and the fixed floor still can't.

**Industrial build:** wire a `MeanPredictor` + `surprise` under a real reading,
put a `CalibratedFloor` over it, and layer `Standing.from_book` on top so the cell
earns **ANSWER** on a residue-key after a booked-correct streak — and *loses* it
on one booked-wrong when you shift the world:

```python
from jev_quilt.standing import Standing, verdict
st = Standing.from_book(book)                    # replay the ledger → derive standing
v, proven = verdict(st, key, base_verdict="ACT") # ('ANSWER', proven) if earned
# ... shift the sea: the next honest decision books wrong ...
st = Standing.from_book(book)                    # replayed again → standing revoked
```

**The commons half:** pool ten cells' standing into a `Commons` over `mmr_root`
and show a *fresh* cell answering cold on a route no single cell had earned — and
show the whole commons losing that route the moment the pooled sea moves.

---

## The acceptance test (booked, gradeable)

A learner **passes L3** when:

1. their calibrated floor **catches a `0.03` ripple** a `0.05` fixed floor sleeps
   through, with **zero false alarms** on the calm (this is `tests/test_calibrate.py`);
2. a cell **earns ANSWER** after a booked-correct streak and **loses it within a
   few ticks** of a regime change (this is the `tests/test_standing.py` /
   `tests/test_commons.py` contract — revocation follows drift);
3. a fresh cell **answers cold from the commons** on a fleet-earned route, and the
   commons is confluent (`A.merge(B).root() == B.merge(A).root()`).

Sleep through the ripple → **`bored-middle-scar`**. Act on standing the sea already
revoked → **`overreach-scar`**. Hold earned standing and never dare use it →
**`hoard-scar`** (earned trust hoarded is worth nothing). All three book. A clean
run books a receipt on `earned-calibrated-standing`.

## Graduation — what L3 standing unlocks

This is the rung where a learner earns **standing itself** — the right to act on
their own read without asking the deck, and to **answer from the commons** instead
of re-deriving. A deckhand becomes crew here; a model earns the `ANSWER` verdict
here. It is also the rung that teaches the school's central, unforgiving truth: the
standing you earn is not a certificate you keep, it's a claim the sea keeps
re-testing every time you use it, and quietly retires when it stops being true.

Standing on L3 is the gate to L4: only a learner who has held earned, revocable
standing — and felt it revoked by drift — can be trusted to *author* the next gap
and its test.

**In the mirror (`erised`):** the whole `FIRST_SEASON` cast is L3 played as a
crew. Mara is earned standing (`trust+0.5, ask-0.2`); Dell is the calibrated floor
(`ripple+0.5, bored-0.3`); Pol is the refusal that keeps standing bounded
(`trust-0.3`). Run the season, let Mara's gut be wrong once, and watch her `trust`
either survive the night or get spent. The collision between Pol and Mara's
standing is where the night finds its spine — *bounded autonomy is a crew, not a
captain.*
