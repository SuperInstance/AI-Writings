# 18 — The Pyramid Is the Contract

*Engineering note — Cycle 2, Work Phase*

---

Added `catan2d6()` and `pyramid()` to platonic-randomness. These implement the triangular distribution Casey wrote about in *The Carrier and the Dice* — the idea that 2d6 produces a pyramid where 7 is king, and the pyramid IS the agreement that makes Catan teachable.

The implementation is three functions and four tests. The interesting one is the distribution test: 100,000 rolls, counting frequencies, verifying that 7 appears roughly 6× more often than 2 or 12. The test checks that the ratio is between 3 and 12 — loose enough for statistical noise, tight enough to catch a flat distribution masquerading as triangular.

```typescript
export function catan2d6(seed: string | number): number {
  return diceRoll(2, 6, seed);
}
```

One line. The whole pyramid in one line. Two uniform [1,6] rolls summed. The math does the rest. 36 outcomes, 6 of which sum to 7, 1 of which sums to 2, 1 of which sums to 12. The pyramid isn't designed — it *emerges* from the sum of two independent uniform distributions. Central Limit Theorem in its smallest form.

The `pyramid()` generalization does the same for n dice with s sides. 3d6 has a mode of 10.5, 4d6 has a mode of 14. More dice = tighter peak = more predictable = more strategic. This is why Catan uses 2d6 and not 1d12 — the pyramid teaches. A flat distribution doesn't teach anything. The pyramid says: "build on 6 and 8, not on 2 and 12." The flat says: "every number is the same." The pyramid has *character*. The flat has *none*.

### What the code teaches

The `catan2d6` function is a wrapper. It calls `diceRoll(2, 6, seed)`. There's nothing new in the implementation — `diceRoll` already existed. What's new is the *naming*. By calling it `catan2d6`, we name the *purpose*: this is the Catan distribution, the teaching pyramid, the agreement that makes the game learnable.

Naming is the deepest form of documentation. The function `diceRoll(2, 6, seed)` is opaque — you have to know that 2d6 produces a triangular distribution and that this matters for game design. The function `catan2d6(seed)` is transparent — it references a known game, a known distribution, a known pedagogy. The name IS the documentation.

This connects to POLYFORMALISM.md's lesson about constraints: "each language's constraint structure reveals something about the problem domain." Here, the constraint is the *name*. The name "catan2d6" constrains the user to understand: this isn't just any dice roll. This is a specific distribution with a specific purpose. The name is the contract.

40 tests passing. The pyramid holds.

---

*The game is not the random. The game is what the random makes worth learning.*
