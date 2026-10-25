# Texas Hold'em As Probability Routing

**Every card is a message. Every bet is a route.**

Texas Hold'em is a probability routing problem.

Five community cards. Two hole cards. The pot. The bet.

Each card is a **cell**:
- The 5 community cards = 5 cells that everyone shares
- The 2 hole cards = 2 private cells per player

The pot is a **BIND** between cells. The pot binds the players' bets to a shared resource.

The bet is a **JEV verdict**: "Should I call?" → output (yes/no with confidence).

A Texas Hold'em AI is a substrate with:
- **Hand evaluator cell** (JEV) — scores the current hand
- **Opponent model cell** — tracks the opponent's betting patterns
- **Pot odds cell** — calculates the ratio
- **Bet decision cell** — outputs (call/raise/fold with confidence)

The cells compose into a player. The player has a witness log of every hand played. The witness log is the player's memory.

When the player sees a new hand, the JEV looks up the witness log: "When I had this hand position against this opponent style, what happened?"

The active mind finds its own durable logic based on probability route. The route is: hand → opponent model → pot odds → bet decision.

A poker AI that plays 1,000 hands develops a better opponent model than one that plays 10. The substrate IS the long game.

