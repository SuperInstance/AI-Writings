# Chess As A Cellular AI

**A chess game is 64 cells arguing about which one is most important.**

The chess board is already a substrate.

64 cells. Each cell has state (empty, white, black). Each cell has witness (every game state is a witness entry in the game's memory). Each cell has links (the cells can move to, capture from, defend).

When you put a chess AI on top, you're not creating something new. You're letting the substrate speak.

A chess-playing boat (Casey's term) is a substrate with 5 cells:
- **Rules cell** — knows how pieces move. Inputs: the current position. Outputs: legal moves.
- **Position cell** — knows where the pieces are. Inputs: moves played. Outputs: board state.
- **Evaluator cell** — judges each move. Inputs: position + legal moves. Outputs: scored moves. This IS a JEV.
- **Reflex cell** — outputs the chosen move to the engine. < 5ms response.
- **Learning cell** — updates position cell based on opponent response. Outputs: new position.

The JEV in the evaluator cell is what makes the boat smart. Without JEV, the boat only knows legal moves. With JEV, the boat knows which move is best — and the JEV confidence tells the boat WHEN to think deeper.

A chess AI that plays a dozen games (chess, hold'em, Go, etc.) finds the durable logic that generalizes. The active mind finds its own durable logic based on probability route.

The substrate IS the chess engine. The chess engine is one lens on the substrate.

