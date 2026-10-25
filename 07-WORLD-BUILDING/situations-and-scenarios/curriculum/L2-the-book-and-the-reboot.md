# L2 — The Book & the Reboot

> *Pull the plug. Come back. Prove you're exactly where you were.*

**The law:** Every state change is booked; replay ≡ live (Law 4). A cell woken
cold replays its book and is bit-for-bit where it was. A crash mid-haul costs
nothing but time. The book is not a log you keep in case someone asks — it *is*
the state, and the live cell is just the book, read fast.

**Who this is for:** a new engineer, a deckhand being left in charge overnight, a
model learning that its training run's receipt chain is its identity across a
checkpoint reload.

**Build against:** `jev_quilt/bookkeeper.py` (`Bookkeeper`, `Receipt`),
`jev_quilt/fold.py` (`mmr_root`, `Checkpoint`).

---

## The toy — the table version (the sea taken out)

You need: a stack of index cards, a pen, and a shoebox.

**The game — "replay the day."**

Every time something *changes* today — a coin moves, the tide turns, someone eats
the last cookie — you write the change on a card: *what changed, from what, to
what.* Not the state. The **delta.** Drop the card in the shoebox in order.

Then the reboot: at the end of the day, **hand the shoebox to someone who wasn't
there.** They deal the cards in order and rebuild the whole day from nothing —
where every coin ended up, whose cookie it was. If they land on the *exact* same
world you're living in, the book replayed = live. You win.

You lose two ways, and both are one scar:

- **You didn't write a card** for a change that happened → the replayer ends up in
  a different world than you. **`amnesia-scar`.**
- **You wrote the state instead of the delta** ("there are 4 coins" instead of "a
  coin moved from Sam to the jar") → the cards don't compose, and the replayer can't
  rebuild the *path*, only the snapshot. Also `amnesia-scar`: you booked a value,
  not a change.

**The seal (this is `mmr_root`):** before you hand over the box, everyone agrees on
a secret handshake number computed from the whole card stack — a *fold* of every
card. After the replay, compute it again from the rebuilt world. If the two
handshake numbers match, the day is *proven*, not just *plausible*. That single
number is `fold.mmr_root`: one value that folds the whole book, so "the replay
agrees with the live run" is one comparison, not a card-by-card audit. Kids love
this part — it's a magic number that catches a lie.

---

## The industrial version — the same law, the sea put back

3 a.m., mid-haul, the power cycles. The cell that was tracking the set wakes cold
into a dark wheelhouse. It reads its `Bookkeeper`, replays every booked delta, and
comes back **bit-for-bit** where it was — the same `q16` values, the same
`mmr_root`. The crash cost time, not state. This is the whole reason a boat can
trust a computer at all: not because it never crashes, but because a crash is just
a slow replay.

Same law, sea added: now the reboot is *involuntary* (a wave, a dead battery, a
watchdog), the book has to survive to disk offline, and the `mmr_root` has to prove
replay ≡ live with no human checking by hand. `fold.Checkpoint` folds the ledger so
the proof is one 32-byte value even after a hundred-thousand-delta season.

---

## The exercise (buildable today)

Run a `Cell` with its `Bookkeeper` through a sequence of decisions. Snapshot the
`mmr_root`. **Kill the process.** Reconstruct the cell from the book alone. Prove
the replayed `mmr_root` equals the live one — and that a *single dropped receipt*
makes them differ.

```python
from jev_quilt.bookkeeper import Bookkeeper
from jev_quilt.fold import mmr_root
live = Bookkeeper()
# ... book a season of deltas ...
root_live = mmr_root([r.leaf() for r in live.receipts])
# reboot: rebuild from the book alone
replay = Bookkeeper.from_receipts(live.receipts)      # replay ≡ live
assert mmr_root([r.leaf() for r in replay.receipts]) == root_live
# drop one receipt → the root MUST change (amnesia is detectable, not silent)
assert mmr_root([r.leaf() for r in live.receipts[:-1]]) != root_live
```

The point of the last line: amnesia is not a soft failure the system hides. A
missing change *shows up in the fold.* You cannot forget quietly.

---

## The acceptance test (booked, gradeable)

A learner **passes L2** when they:

1. run a cell through ≥ 50 deltas, kill it, and replay from the book to a
   **bit-identical** state (`mmr_root` matches), and
2. demonstrate that dropping **any one** delta changes the `mmr_root` (amnesia is
   detectable), and
3. do the whole thing **offline** — no network in the loop at any point.

`replay ≠ live` → **`amnesia-scar`**, booked. A clean cold-replay books a receipt
on the skill `replay-equals-live`. This is the level where the *reboot exam* the
whole school grades on is first practiced: the assessment IS a cold wake.

## Graduation — what L2 standing unlocks

Earn the streak and you hold **ANSWER** on `replay-equals-live`: the right to be
**left in charge across a reboot** — the night watch alone, the solo haul, and (for
a model) trusted across a checkpoint reload. If you can't prove the shift cold, you
can't own it. This standing is the precondition for every higher rung, because L3's
earned standing and L4's authored gaps are *derived by replaying a book* — no
trustworthy book, no trustworthy standing.

Lose it if a reboot ever fails to reproduce — a delta you stopped booking, a
non-determinism you let creep in — and everything you'd earned above it is suspect
until the book is honest again.

**In the mirror (`erised`):** Sig the memory (`presets/FIRST_SEASON.md`,
`remember+0.5, drift-0.2`) is the book made crew — he knows which old seasons to
trust and which to forget. Run the L2 Situation, force a rewind (a `crash`), and
watch whether the scene comes back bit-for-bit or whether an un-booked change
leaves the crew arguing about what actually happened last night. That argument is
the `amnesia-scar`, live.
