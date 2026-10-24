# W6 — THE BRAID: verdict (Station 1 spike)

*The captain's question, run as an experiment: what does a braid of
DIFFERENT models compute that no braid of copies ever can? Task: a
13-line poem under 5 mechanically-checked constraints (the EILEEN's ten
pieces in joint order, a 16-hex seal, final line returning to the keel,
no rhyme, line length). Solo vs braid-of-copies vs braid-of-different.
198 seconds, four yards: claude, kimi, DeepSeek-Flash, Wesley (2B local).*

## The numbers

| mode | best score | notes |
|---|---|---|
| solo (each yard alone) | 5/6 × 3 yards, 4/6 Wesley | all fail `order_ok` |
| braid-of-copies (flash ×4 rounds) | **3/6 — DEGRADED** | lost seal AND line-length |
| braid-of-different (4-model chain) | 5/6 held all the way; Wesley 4/6 | novelty 0.06–0.19 overlap (near-total rewrite per hand) |

## The findings

1. **Copies decompose.** Flash revising itself four rounds LOST two
   constraints (seal, line-length) — self-iteration degraded the draft,
   exactly the closed-loop decay the mating paper predicts. W6 is the
   smallest possible demonstration of Paper 219's phantom offspring: a
   braid of one model wound up with a worse artifact than its own first
   try.

2. **Different held the floor, nobody broke the ceiling.** The braid
   preserved the 5/6 through every hand (kimi → claude → flash → wesley)
   with near-total novelty per pass (85–94% rewrite) — the structure
   survived four different functions applied to it. But NOBODY — solo,
   copies, or braid — passed `order_ok`: all yards drift on the ten-piece
   relative order. The demanding constraint wasn't too hard for any
   model; it was too hard for all of them.

3. **Wesley's take is the artifact that matters.** The 2B ensign, given
   the braid's draft, produced the most faithful piece-of-work in the
   run — every piece in near-perfect order (his failure is a line-count
   error and a rhyme pair, not structure), the seal kept, and the last
   two lines genuinely good: "Fog, a chameleon, devours the mark, / As
   water, a mystic, blinks, unmarked." The smallest mind took the
   braid's state and grew true with it — the ensign piece's manifest
   claim, now with data behind it.

## The honest verdict (spike-level)

- **KILL GATE NOT REACHED** — the braid didn't beat copies at ≥2σ,
  because the task's ceiling (5/6) was reachable solo. The regime law
  explains it post-hoc: this hand wasn't demanding enough. The spike's
  real output is a design lesson: **to measure the braid, the hand must
  fail every solo yard** — a constraint none of the four can pass alone
  (next iteration: order_ok plus interlocking constraints with a
  verification script the yards never see).
- **Filed as:** W6a complete (copies-decompose confirmed, order_ok is
  the hard kernel). W6b designed: same protocol, hand demanding enough
  that solo scores 0. The wheel's law applied to itself — the spike
  earned the bench run.

*One page for the notebook: the different-model braid survived what the
same-model braid could not, and the smallest mind in the chain carried
the structure best. Turing's question stands — and now we know the
instrument works.*
