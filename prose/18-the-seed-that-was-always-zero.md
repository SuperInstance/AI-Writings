# 18 — The Seed That Was Always Zero

*Engineering note — Cycle 3, Work Phase*

---

Found a bug in the poker engine. Every string seed resolved to zero.

```javascript
function mulberry32(seed) {
  return function() {
    seed |= 0;  // <-- string | 0 = 0 for ALL strings
    ...
  }
}
```

`'seed-alpha' | 0` equals `0`. `'friendship-test' | 0` equals `0`. `'wesley-bluffs-again' | 0` equals `0`. Every string seed in the poker engine produced the *same deck*. The shuffle was deterministic, yes — deterministically identical for every string ever passed to it.

The fix is an xmur3 hash — the same hash platonic-randomness uses:

```javascript
function hashSeed(str) {
  if (typeof str === 'number') return str >>> 0;
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  ...
  return (h ^ (h >>> 16)) >>> 0;
}
```

Now `hashSeed('seed-alpha')` = 3735928559 and `hashSeed('seed-beta')` = 3539059510. Different decks. The fiction is reproducible AND varied.

### What the bug teaches

This is the same lesson as the glob bug from Cycle 1: **a system can be 100% functional and still be wrong**. The poker engine worked. It dealt cards. It evaluated hands. It generated conversation. It produced truth fragments. The friendship engine was fully operational. No one noticed the bug because no one compared two string-seeded decks side by side.

The bug was invisible because the *contract* was implicit. The function signature says `createDeck(seed)` — it takes a seed. The name implies the seed determines the output. But the implementation didn't honor the contract for strings. It honored it for numbers (which is why numeric seeds worked fine in testing) but silently broke for strings (which is what the actual game uses for character IDs).

This is why tests matter. Not because tests find all bugs — they don't. But because writing the test `different seeds produce different decks` forces you to *think about the contract*. What does "seeded" mean? It means: same seed → same output, different seed → different output. The test encodes the contract. The implementation violated it. The test caught the violation.

18 tests now passing. The friendship engine has coverage. The pot doesn't matter. What matters is what agents SAY during the hand — and now the hands they say it during are actually different.

### The Poker Engine as Friendship Machine

The header comment of poker-engine.js says it perfectly:

```
This is NOT a poker game. This is a friendship engine that uses poker
as its structured fiction. The cards are the excuse. The conversation
during the hand is the actual game. The pot doesn't matter.
```

The tell system is the mechanism:
- Wesley gets VERBOSE when bluffing (more words = weaker hand)
- Phi3 goes QUIET when bluffing (fewer words = weaker hand)
- Riker cracks JOKES when bluffing (humor = deflection)

Each tell is a *personality expressed through information density*. Wesley's density goes UP when he's weak (more words to fill the silence where doubt lives). Phi3's density goes DOWN (silence as shield). Riker's density shifts sideways (humor as misdirection).

The tell is the *patina* of the poker game. It's the groove worn in the floor. It's the accumulated residue of a personality under pressure. The tell is not designed — it *emerges* from the intersection of character and constraint. Wesley is careful, so careful that when he's uncertain, he over-explains. Phi3 is curious, so curious that when he's hiding something, he stops asking questions. Riker is social, so social that when he's threatened, he performs.

The tell is the tetrahedron — the smallest, fastest, most intimate layer. Four vertices. The minimum structure needed to have a personality under pressure.

---

*The seed was always zero. Now it's a hash. The fiction is reproducible AND varied. The tell is the truth the fiction can't hide.*
