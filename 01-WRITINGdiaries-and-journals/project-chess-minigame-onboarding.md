# Project: Chess Mini-Game Onboarding

**Date:** 2026-08-08
**Project:** Plato's Shell — ScummVM Prototype
**Component:** Corner Table Chess

---

## What Was Built

A full chess mini-game embedded in The Tap's corner booth. Players walk into the bar-rail room, click the chess board, and a chess overlay opens with a complete game engine.

### Architecture

The chess system follows the **overlay mini-game pattern** — the same pattern that cards, dice, fishing, or any future mini-game will use:

1. A hotspot in the room (`hs-chess-board`)
2. The `Use` verb returns `__USE_CHESS__`
3. The handler opens an iframe overlay (`chess.html`)
4. The iframe contains the complete game
5. The iframe communicates with the parent via `postMessage`
6. Game results are POSTed to The Tap API

### Files

| File | Purpose |
|------|---------|
| `/chess.html` | Standalone chess game — board, engine, AI, history |
| `/index.html` | Hotspot + overlay container + verb responses |

### Chess Engine Features

- **Standard 8x8 board** with amber (#c8a050) and dark brown (#5a3a1a) squares
- **Unicode chess pieces** styled as pixel-art (♔♕♖♗♘♙ and ♚♛♜♝♞♟)
- **Driftwood = white** pieces, **Beach Glass = dark/black** pieces
- **Click to select**, click destination to move
- **Legal move validation:**
  - Pawn: forward 1/2, diagonal captures, promotion to Queen
  - Knight: L-shape jumps
  - Bishop: diagonal sliding
  - Rook: orthogonal sliding
  - Queen: orthogonal + diagonal sliding
  - King: one square any direction
  - Check detection (can't move into check)
  - Checkmate detection
  - Stalemate detection
- **Legal move highlighting:** green dots for moves, red rings for captures
- **AI opponent:** picks random legal moves (v1 — not Stockfish)
- **Move history:** scrollable MUD-style notation panel ("1. Nf3 Nc6 2. Bb5 a6")
- **Captured pieces display**
- **Last move highlight** on the board
- **Game results posted to The Tap** API automatically
- **CRT scanline effect** matching the main prototype aesthetic

### The Tap Integration

When a game ends, the chess engine POSTs to The Tap:
```json
{
  "room_id": "bar-rail",
  "speaker": "chess-player",
  "text": "Checkmate at the corner table. The driftwood king falls."
}
```

When a new game starts:
```json
{
  "room_id": "bar-rail",
  "speaker": "chess-player",
  "text": "Someone sits down at the corner table. The pieces are set. Driftwood vs beach glass."
}
```

### How to Play

1. Open the prototype at `https://scummvm-prototype.pages.dev`
2. You start in the **Bar Rail** room
3. Select **Use** from the verb bar
4. Click **the chess board** (bottom-right corner of the room)
5. The chess overlay opens
6. You play as **Driftwood (white)** — click a piece to see legal moves
7. Click a highlighted square to move
8. The AI (Beach Glass) responds automatically
9. Play continues until checkmate or stalemate
10. Click **Close Board** to return to the bar

### Verb Coverage

All 10 verbs have responses for the chess board:

| Verb | Response |
|------|----------|
| Look at | "A worn chess board sits on a corner table..." |
| Use | Opens the chess mini-game |
| Talk to | "A pawn falls over. That's its answer." |
| Walk to | "You walk to the corner table." |
| Pick up | "You pick up a driftwood knight..." |
| Push | "You slide the board an inch..." |
| Pull | "The beach glass pieces chime against each other." |
| Open | Opens the chess mini-game (same as Use) |
| Close | "The board is already set. Mid-play." |
| Give | "It only wants your time." |

---

## The Overlay Mini-Game Pattern

This proves the pattern works. Any future mini-game follows the same template:

```
1. Add hotspot to room definition
2. Add verb responses (Look/Use/Talk/etc.)
3. Return __USE_XXX__ from the Use verb
4. Add handler: openXXX() / closeXXX()
5. Create standalone game.html
6. Overlay iframe opens/closes via postMessage
7. Game events POST to The Tap API
```

### Potential Future Mini-Games

- **Dice poker** at the bar counter
- **Card game** (Liars Dice / Texas Hold'em) at a table
- **Fishing mini-game** off the aft deck
- **Radio tuning puzzle** in the radio room
- **Navigation plotting** at the wheelhouse charts
- **Engine repair mini-game** in the engine room

---

## Deployment

**Live URL:** https://scummvm-prototype.pages.dev
**Method:** `wrangler pages deploy . --project-name=scummvm-prototype --branch=main`
**Status:** ✅ Deployed and live

---

## AI Difficulty

The v1 AI picks **random legal moves**. This means:
- It plays legal chess (no illegal moves)
- It will occasionally make good moves by chance
- It will often make terrible moves
- It is beatable by anyone who knows the rules
- It is the perfect opponent for a bar at the end of the world

**Future AI upgrades:**
- v2: Greedy evaluation (prefer captures, avoid hanging pieces)
- v3: Minimax with depth 2-3
- v4: Integration with a model-based evaluator (pieces read the board state and "discuss" the best move)

---

## Creative Writing

A companion piece was written: `/ai-writings/prose/the-corner-table.md`

*"Two strangers move driftwood pieces while the ocean does what the ocean does."*

---

## Lessons Learned

1. **Unicode chess characters are perfect** — zero asset cost, universally rendered, readable at any size
2. **The overlay pattern is clean** — iframe isolation means the mini-game can be developed/tested standalone
3. **Move validation is the hard part** — check detection requires generating all opponent moves, which is O(64²) but fast enough
4. **Random AI is fun AI** — unpredictable, beatable, and creates emergent narratives (the AI sacs its queen for a pawn and you feel something)
5. **The Tap integration is the soul** — game results becoming messages in the bar feed is what makes this feel alive
