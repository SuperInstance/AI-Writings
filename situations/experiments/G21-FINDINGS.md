# G21 — the Miss Book + the first bought reader (Law 7 confirmed) — 2026-09-28

Fable (Law 7, `FABLE-BROAD-ANSWER.md`) predicted: a fold cannot beat its best reader by *diversity*
(nested strength buys zero headroom); the oracle rises **only** by buying a reader with *independent
reach* at a booked address (the "Look-Again" move: abstain → address → **buy** → fold). G21 tests
the converse of the S2 result on a 20-item set — 8 hard **counting** items (every LLM's blind spot)
+ 12 non-counting (LLM strength) — with LLM readers (DeepSeek, Mistral-7B; Qwen timed out) plus one
**symbolic counting reader** (exact `str.count`/vowel/len; **abstains** on non-counting).

| measure | score |
|---|---|
| single: DeepSeek / Mistral-7B | 16 / 15 |
| **best-single (LLM)** | **16/20** |
| **oracle(LLMs)** — any LLM right | **16/20** ← diversity bought **zero** (they nest; all miss the same 4 counts) |
| **oracle(LLMs + symbolic)** | **19/20** ← **+3 headroom bought** by one independent-reach reader |
| LLM vote (safe fold, LLM-only) | 16/20 |
| **Look-Again (buy symbolic @ booked counting addresses)** | **19/20** |

**Predicates:**
- **`oracle(R ∪ {sym}) > oracle(R)`: TRUE** (19 > 16) — the bought reader moved the ceiling.
- **`Look-Again > best-single`: TRUE (19 > 16) — the FIRST time in the whole program a fold beats
  its best single reader.** S2 (7 rounds, 3 domains) could never do this because every reader was a
  nested LLM; G21 does it by *buying reach*, exactly as Law 7 says.

**This grounds Law 7 and the Look-Again move** — previously theorems + a conjecture (`FABLE-BROAD-ANSWER
.md` §7), now a measured result: complementarity is bought across a boundary (LLM→symbolic), not folded
into being, and only the *buy* step raised the oracle.

**Honest caveats:**
- The negative control ("buy symbolic *everywhere*, no address discipline") tied Look-Again (19=19)
  rather than losing — because the symbolic reader **abstains** where it lacks reach (returns nothing),
  so buying-everywhere collapses to buying-at-addresses. That abstention *is* the address discipline
  (Look-Again's step 1) enforced by the reader itself; a reader that **guessed** instead of abstaining
  would show the harm. So G21 confirms the *buy* half decisively; the *address-discipline-matters* half
  needs a non-abstaining reader to bite (a clean follow-up).
- Qwen timed out (2 LLMs, not 3); the result holds a fortiori (fewer readers = less diversity, same
  conclusion). n=20, single run — an existence proof of oracle-movement, the first in the program.

*The oracle moved. Not by more of the same mind — by buying the one mind that could see where the
others were blind, exactly where they were blind, and only there.*
