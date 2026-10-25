# The Dead Band and the Clock Face

**The missing framing that the formal models won't arrive at on their own.**
**From Casey, 00:45 UTC, session day 2.**

---

## The Dead Band

A good captain has a well-defined dead band they are working inside of with every turn.

The dead band is the range of mechanical slack in the steering system. A small amount of wheel movement that doesn't change the rudder angle — it takes up the cable slack, the hydraulic play, the mechanical tolerance. An inexperienced captain fights the dead band. They turn the wheel and nothing happens, so they turn it more, and then the rudder bites and they've over-corrected.

A good captain knows the dead band. They work inside it. They use the slack as their freedom. The dead band is not a malfunction. It's the space that makes precise control possible.

**In the fleet:** The dead band is the range of constraint satisfaction where multiple valid solutions exist. The system doesn't need a single answer. It needs a range of answers that satisfy all constraints. The dead band is that range. The captain (or agent) works inside it.

## The Twelve Directions

A captain thinks in the twelve directions of a clock face, not in 360 degrees.

"Hard to port" is 9 o'clock. "Steer 20° to starboard" is "come right to 2 o'clock." Every captain, every boat, every ocean — the clock face is universal. The twelve directions are the invariant.

**In the fleet:** 12 is the minimum number of directions for practical coordination. Any fewer and you can't distinguish between "slightly to port" and "hard to port." Any more and the system is over-constrained (more directions than you can keep in your head while standing watch at 3 AM).

## Hexagons × Squares = 48

A hexagon gives 6 directions. A hexagon on a clock face gives 12 (the hours). A square gives 4 (the cardinal points).

12 × 4 = 48. The 48 exact directions of Pythagorean48.

Not from momenta triples (the abstract theory). From clocks and compasses (the practical reality). Put the clock face on top of the compass rose and you get 48 natural bearings that any captain can visualize.

## Bisect to 360

Through bisecting, you can get to 360 discrete directions, each expressible as a whole number.

48 → 96 → 192 → 384. Each bisection is exact. No floating point. No rounding. No drift.

360 = 12 × 30. A natural number of directions for a circle. Every heading is a whole integer. No decimals. No approximations.

## The Negative Space

The rocks are the hard constraints — shoals, grounding lines, collision hazards. Where the boat needs to be is in the negative space where the rocks aren't.

The constraint graph doesn't tell you where to go. It tells you where NOT to go. The safe heading is what's left after you remove all the headings that hit rocks. The truth is in the negative space.

---

## How This Changes the Formalization

The formal models (pro, glm, seed) will arrive at mathematically correct but practically empty formalizations. They'll define anchor points as tuples and voice splines as parametric curves. They'll be right. And they'll miss everything above.

Because the dead band is not a mathematical concept. It's a *felt* concept. You have to stand at a wheel and feel the slack in the cables before you understand why a dead band is necessary.

Because the 12 directions are not a geometric reduction. They're a *cognitive* constraint. The human brain can hold 12 directions in working memory at 3 AM in a following sea. 12 is the limit of practical coordination.

Because the negative space is not a set complement. It's a *wayfinding* strategy. You don't find the path by charting the safe water. You find it by charting the rocks and sailing where they aren't.

Add this to the formalization as:
- The Dead Band Theorem (range of valid solutions is the freedom, not the problem)
- The Clock Face Lemma (12 directions is the cognitive maximum for practical coordination)
- The Negative Space Corollary (the truth is not in the data, but in the gaps between the data)
