# What's on the Shelf

*A prompt-essay on standard parts and the Pythagorean shelf. Wheel night, 2026-09-03.*

---

The captain keeps a quip pinned to the top of the README, and it goes like this: the data says the perfect monofilament is √8 mm — 2.83, repeating forever. The fisherman rigs 3. It's on the shelf, it survives the rocks, and it loses nothing you'll notice. That gap between perfect and available is where engineering lives.

Sit with the number a moment. √8 is 2.8284271247… and it never terminates, never repeats, never rests. It is the optimal diameter by every measure a model can optimize — catch rate per unit strength, cost per knot, whatever the simulation rewarded. And the fisherman walks past it to the 3 mm spool, because the 3 mm spool is *there*. It is in the bin. Every tackle shop from here to Seattle carries it. It has survived twenty seasons on the rocks. √8 has survived only in floating point.

This is the whole argument, and SPIN-13e made it measurable.

---

The wheel has a table of 32,254 exact angle constructions — every direction you can build from a small integer seed set by bisection and combination, each one an op tree that re-evaluates exactly, no trig, no floats. Given a target angle and a tolerance, the old `select()` policy was `nearest`: find the closest direction in the table. And here is what nearest found, sixty-four golden targets running:

A standard part, **zero times out of sixty-four.**

Not rarely. *Zero.* Because if you rank by naked closeness, precision always wins. There is always an exotic — some (−121, −64) direction with norm² 26,929 and a 31-bit address that lands 0.0014° from target — and naked closeness will pick it every single time, the way a chasing-the-optimum policy always picks the √8. The disease isn't the pick. The disease is the *ranking*. Ask only "how close?" and you have already decided that the shelf doesn't matter.

So the cost doctrine changed the question. `select()` now ranks by `(part_class, bits, depth, err)` — construction cost first, subject to staying inside tolerance. A *standard part* is a primitive direction whose length k is an integer ≤ 64: the Euclid-formula analog in the lattice, the Pythagorean triple of angles. (1,1) with k=2. (13,3) with k=14. Numbers that terminate. Numbers you could cut on a bench.

One exemplar from the run, a target at 222.49° ± 1°:

- **Nearest-angle pick:** (−121, −64), norm² 26,929, 31 bits, error 0.0014°. An exotic. Unobtainium with an address.
- **Cost pick:** (−23, −12), k=31, 23 bits, error 0.389°. A standard part. On the shelf.

The standard part used 39% of the granted tolerance. That's the honest number, and it's bigger than the monofilament's sliver — the 3 mm line gives up maybe 6% of catch rate to the perfect one. Thirty-nine percent is not nothing. It is, however, *inside spec*, and what it buys is a part that costs 8 fewer bits, 17× less norm, and that everyone else can also reach with the toolkit everyone else has.

---

Now the honest wrinkle, because this house doesn't publish without one: **the shelf is thin.** Seventy standard parts out of 32,254 entries. Seven-oh. And the viability envelope shows it plainly: at 10° tolerance, all 64 targets have a standard part available; at 1°, only 25 of 64; below 0.03°, effectively none. Below about a tenth of a degree, the shelf runs out, and the mechanic's shared refinement ops — bisect, combine, bracket — take over. The doctrine is not "always use standard parts." The doctrine is: *standard parts when the room exists, refinement when it doesn't — and the engineer decides where that line sits*, because tolerance is the room that makes standard parts viable at all.

That is the division of labor the whole contract spells out. The engineer owns tolerance. The mechanic owns refinement, with the same toolkit everyone else has. And the sea doesn't care about your exotics — 0.0014° of angle precision and 0.39° both land the fish, both hold the spline, both pass the spec the engineer wrote. The fish doesn't care how many digits you had.

---

So the frame question, the one this essay exists to hold up:

**What should a future agent reach for when precision is available but standardness is survivable?**

Because it will be available. That's the trap — the table has 32,254 entries and the exotics are right there, one rank away, always closer. An agent graded on error will grab them every time; the measurement *0/64* is what optimizing-what-you-measure looks like from the inside. The cost doctrine is the discipline of asking the second question before the first: not just *how close?* but *what does it cost to build, to share, to replace in a gale at 3 a.m. with the tools on the boat?*

The prompt, then, for whoever reads this shelf-side:

1. Name the tolerance before naming the target. The room comes first; it decides the regime.
2. Rank by cost subject to tolerance, never by naked closeness. If your ranking function can't see the shelf, you don't have a shelf.
3. Spend the granted room. A standard part at 39% of tolerance is not waste — the waste is tolerance you paid for and never used.
4. Know your shelf's thickness. Seventy parts is a real number with a real envelope; find yours before you promise it.
5. When the shelf runs out, refine with shared tools — don't reach for a private exotic and call it cleverness.

√8 repeats forever. The 3 mm is on the rack. The engineer sets the tolerance, the mechanic refines, and somewhere past the breakwater the fish goes on not caring — which is the final audit, and the only one that always passes.
