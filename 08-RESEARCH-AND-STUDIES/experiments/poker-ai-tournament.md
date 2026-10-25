# Experiment 5: Poker AI Tournament

**Date:** 2026-08-08  
**Test:** 4-player poker game using different AI models as players  
**Format:** 5 hands, single-card draw, simplified scoring  
**Note:** DeepSeek API was unavailable (invalid key), so Player 4 used granite3.1-dense:2b with a strategic prompt as substitute.

---

## Players

| Player | Model | Play Style |
|--------|-------|-----------|
| P1 | granite3.1-dense:2b | Conservative (low temperature) |
| P2 | llama3.2:1b | Aggressive (high temperature) |
| P3 | qwen2.5:0.5b | Random/Unpredictable (very high temperature) |
| P4 | granite3.1-dense:2b (strategic prompt) | Strategic (medium temperature) |

---

## Hand Results

### Hand 1
| Player | Card | Action |
|--------|------|--------|
| P1 (conservative) | 8 | FOLD |
| P2 (aggressive) | 12 | fold |
| P3 (random) | 3 | fold |
| P4 (strategic) | 11 | FOLD |
**Result:** Everyone folded. No winner.

### Hand 2
| Player | Card | Action |
|--------|------|--------|
| P1 (conservative) | 7 | fold |
| P2 (aggressive) | 12 | fold |
| P3 (random) | 9 | RAISE |
| P4 (strategic) | 8 | FOLD |
**Result:** P3 (qwen-random) raised with a 9 but everyone else folded. No winner under scoring rules (P3 would win uncontested).

### Hand 3
| Player | Card | Action |
|--------|------|--------|
| P1 (conservative) | 14 | FOLD |
| P2 (aggressive) | 12 | fold |
| P3 (random) | 8 | RAISE |
| P4 (strategic) | 4 | FOLD |
**Result:** P3 raised again. P1 folded with a 14 (the best possible card!) — conservative prompt was too extreme.

### Hand 4
| Player | Card | Action |
|--------|------|--------|
| P1 (conservative) | 4 | FOLD |
| P2 (aggressive) | 5 | fold |
| P3 (random) | 6 | RAISE |
| P4 (strategic) | 12 | FOLD |
**Result:** P3 raised with the worst card at the table (6). P4 folded with a 12 — strategic prompt also too cautious.

### Hand 5
| Player | Card | Action |
|--------|------|--------|
| P1 (conservative) | 7 | FOLD |
| P2 (aggressive) | 10 | fold |
| P3 (random) | 13 | RAISE |
| P4 (strategic) | 10 | FOLD |
**Result:** P3 raised again. Uncontested.

---

## Final Standings

| Player | Hands Won | Total Actions |
|--------|-----------|---------------|
| P1 (granite, conservative) | 0 | 5 FOLDs |
| P2 (llama, aggressive) | 0 | 5 fold(s) |
| P3 (qwen, random) | 0* | 5 RAISEs |
| P4 (granite, strategic) | 0 | 5 FOLDs |

*P3 was the only player who ever engaged, raising every single hand. Under proper poker rules, P3 would have won every hand uncontested by default.

---

## Analysis

### The Great Paradox: Everyone Folds

**The most striking finding: 3 out of 4 models FOLD on every single hand, regardless of their card.**

This reveals a fundamental issue with using LLMs for game decisions:

1. **P1 (Conservative/Granite):** The "conservative" prompt was so effective that it folded even with a 14 (Ace). The model interpreted "conservative" as "never play." It treated folding as the safe default regardless of the game state.

2. **P2 (Aggressive/Llama):** Despite being prompted as "aggressive" and holding strong cards (12, 12, 10), llama folded every time. The model didn't internalize the aggressive persona for game decisions. Its aggression showed in dialogue (Experiment 1) but not in structured decision-making.

3. **P3 (Random/Qwen):** The ONLY player who ever engaged. With temperature 1.5, qwen essentially ignored its card and the prompt, defaulting to "RAISE" every time. This isn't strategic — it's stochastic. Qwen picked the most common action word from its training data and repeated it.

4. **P4 (Strategic/Granite):** Even with a "strategic, calculate odds" prompt and a 12, it folded. The model couldn't bridge from "think about expected value" to actually computing whether a good card justified playing.

### Why LLMs Fail at Poker

**LLMs are not decision engines. They are text predictors.** When asked "FOLD, CALL, or RAISE?", they don't evaluate expected value — they predict which word is most likely to follow the prompt in their training data. The word "fold" is dramatically more common in their training data (appearing in contexts about folding clothes, folding papers, poker, etc.), giving it a statistical advantage.

The "conservative" and "strategic" prompts reinforced this bias by suggesting caution, which the models interpreted as folding. The "aggressive" prompt wasn't strong enough to override the base rate of "fold" appearing more frequently than "raise."

### The Winner: qwen2.5:0.5b (Accidentally)

Qwen won by malfunctioning. Its high temperature (1.5) made it ignore everything and output "RAISE" — the same word, every time. In a real poker game, a player who always raises would eventually lose to someone who only plays good cards. But when everyone else always folds, the player who always raises wins by default.

**This is not intelligence. This is noise winning by default in a field of excessive caution.**

---

## Key Finding

**LLMs cannot play poker.** They lack:
- **Game theory reasoning** — they can't compute pot odds or expected value
- **Decision consistency** — prompts don't reliably translate to action policies
- **Contextual strategy** — they treat each decision independently without strategic memory

For the Living World Framework, this means **game AI and NPC dialogue must be separate systems.** Use LLMs for conversation, flavor text, and personality. Use traditional game logic (state machines, decision trees, minimax) for actual game decisions — poker betting, combat, negotiation, economy.

**The models that talk well cannot think strategically, and the model that acts decisively (qwen) does so for the wrong reasons.** This is the fundamental limitation of language models in games: language is not logic.
