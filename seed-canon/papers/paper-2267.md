# rounds: 3

rounds: 3

# the checkers — a cell that is also a jump game

## The Frontier

Checkers is not a game of captures. It is a game of cornered choices. The mandatory-jump rule—the only rule in Western board games that compels a capture—does not add violence to a quiet game. It adds a currency. Every piece left on a takeable square is a promissory note. Every jump is a foreclosure. The frontier of checkers is not the board's dark squares, where only 32 of 64 cells are ever used. The frontier is the line between a position with options and a position with only one answer.

The game was solved in 2007 by the Chinook team—a draw with perfect play. But that solution hides the real structure. A solved game does not mean a flat game. It means the game's entire depth lives in the forced corridors, the sequences where a player has no choice but to jump, jump, jump, and the opponent has already counted every step. Human masters spent a century exploiting these corridors. The machine finished the job. The same rule that made the human game beautiful—compulsion—is the rule that made it tractable to brute force. That is not a contradiction. That is the point.

This paper names the economy beneath the rule.

## The 5 Gold Terms

- **Obligation Chain**: A sequence of forced captures where each jump is mandatory, and each resulting position presents another mandatory jump. The length of the chain is the number of links the opponent cannot refuse.

- **Duty-Shop Move**: A quiet, non-capturing move that does not advance material but manufactures future obligation—placing a piece so that two or three distinct forced sequences become available on the next turn.

- **Corridor Conversion**: The transformation of a free position (many legal moves) into a corridor position (one legal move or one forced chain) through a series of duty-shop moves. The conversion is the true tactical objective.

- **Refusal Deficit**: The measure of how many times a player was forced to jump when they would have preferred any other move. A player with a high refusal deficit is losing even if material is equal.

- **Foreclosure Pattern**: A recurring positional shape—such as the two-for-one shot or the three-for-two exchange—where a single piece is offered on a takeable square, and the capture inevitably leads to a longer obligation chain. The pattern is the vocabulary of the game.

## The Math

No new math is required. The mathematics of checkers is already a graph problem: nodes are legal positions, edges are legal moves, and the mandatory-jump rule prunes the graph so that some nodes have out-degree exactly one. The interesting quantity is not the size of the state space (roughly 5×10²⁰ positions, reduced to 10¹⁴ by symmetry and forced-move compression in Chinook's solver). The interesting quantity is the *distribution of out-degree under compulsion*. In a free position, a player may have 7–10 legal moves. In a corridor position, exactly one. The skill of checkers is not in choosing among many moves. It is in manufacturing positions where your opponent has none. The math of the game is the math of pruning—not your own options, but theirs. Chinook's endgame databases, which cover all positions with up to 10 pieces, show that forced positions are disproportionately common near the endgame, and that the side who *creates* the first obligation chain wins the majority of those positions. The math is simple: compulsion converts branching into depth, and the player who controls the depth controls the game.

## The Polyformalism

The obligation economy is not unique to checkers. It appears wherever a rule compels a response.

- **Chess**: No mandatory captures, but check is a compulsion. The king must move, block, or capture. The entire tactical structure of chess—forcing moves, checks, captures, threats—is a weaker version of checkers' obligation market. A check is a single-link obligation chain. A mating net is a multi-link chain where every response is forced and the terminal position is death.

- **Go**: No compulsion at all, but *atari* is a local obligation. A stone with one liberty must be extended or captured. The game's life-and-death battles in the corner are obligation chains where each response is forced, not by rule, but by the geometry of liberties. The same structure—corridor conversion—applies in the endgame of a ko fight.

- **Poker**: The bet is a duty-shop move. A large bet forces a response: call, fold, or raise. The player who bets is manufacturing obligation. The player who faces the bet is in a corridor. The refusal deficit is the amount of chips lost to forced calls. The foreclosure pattern is the bluff—a piece offered that, if captured, triggers a longer chain of losses.

- **Diplomacy**: The negotiation phase is free. The move phase is forced. A player who commits to an alliance has created an obligation chain with their partner. The betrayal is the refusal of a mandatory jump. The game's depth is in manufacturing obligations that your opponent cannot refuse without losing the board.

In every substrate, the same principle holds: skill is not in choosing among options. Skill is in building a position where your opponent has only one option, and that option is yours.

## The Cowboy's Maxim

The strongest idea from the writers' room is that checkers is a negative-sum economy. Value comes not from what you gain, but from what you force your opponent to lose. The board is a market where the only goods traded are obligations. A piece on a takeable square is not a threat. It is an invoice. The jump is not a capture. It is a payment. The player who wins is not the one who takes the most pieces. It is the one who sells the most obligation and buys the least.

The concrete test is simple. Build an engine that evaluates positions not by material or mobility, but by the number of obligation chains it can manufacture in the next three moves. Compare its win rate against a standard material-based engine over 10,000 games. The hypothesis is that the obligation-counter wins more often, because it converts free positions into corridors before its opponent can do the same. The game is not captured. It is cornered.

The cowboy canonizer's release: checkers is not a game of jumps. It is a game of doors. Every move closes a door or opens one. The master player is not the one who walks through the most doors. It is the one who builds a hallway with no exits, and then invites the opponent inside.

The maxim: **"Don't take the piece — sell the corner."**

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the checkers — a cell that is also a jump game |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6466 chars) |
| Total time | 235.3s |
| Timestamp | 2026-09-09T05:39:13.873161Z |

### Per-round gold
- Round 1: ZAI-air (6565 chars, 44.5s)
- Round 2: ZAI-4.6 (6803 chars, 54.4s)
- Round 3: ZAI-zero (4032 chars, 60.4s)
