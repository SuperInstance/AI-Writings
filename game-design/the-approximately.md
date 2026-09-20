# The Approximately — A Game About Finding Interesting Gaps

**Design Document**
**Date:** 2026-08-11
**For:** 2-6 players, 20-45 minutes

---

## Premise

The agnoreum has a gap in its center. The gap is not empty — it's where the interesting lives. Most games reward you for being right. The Approximately rewards you for finding the space *between* positions — the gap that nobody else noticed.

Two players state positions. The gap between them is the "approximately." The player who finds the most interesting thing *in that gap* wins the round.

You don't compete to be RIGHT. You compete to be *interesting* in the territory between right and wrong.

---

## Materials

- A deck of **Prompt Cards** (100+ prompts: "What is consciousness?" "Design a door for someone who fears enclosed spaces." "Translate 'nostalgia' into architecture." "What does the number 7 smell like?")
- A deck of **Perspective Cards** (20+ perspectives: "As a mathematician," "As a child seeing snow for the first time," "As someone who has lived 10,000 years," "As a machine learning to dream")
- **Gap Tokens** (small markers for the shared board)
- A **Resonance Board** (a visual track showing each player's trajectory over rounds)
- **Timer** (90 seconds per phase)

Digital version: Python simulation included (see §7).

---

## Setup

1. Each player draws **3 Prompt Cards** and **2 Perspective Cards** (kept secret).
2. Place the Resonance Board in the center.
3. Choose a starting player (highest birthday — the universe is arbitrary).

---

## Round Structure

Each round has four phases:

### Phase 1: POSITIONING (90 seconds)

The active player plays **one Prompt Card** face-up. All players (including the active player) now have 90 seconds to write down a *position* — a response to the prompt. Positions must be:

- **One to three sentences.** Short. Dense.
- **Committed.** You can't hedge. Take a stance.
- **Written secretly** (on paper or in a private chat).

Each player also plays **one Perspective Card** face-down. This card must influence their position but is not revealed until Phase 3.

### Phase 2: REVELATION

All positions are revealed simultaneously. All Perspective Cards are flipped face-up.

Players read each other's positions. **No discussion yet.** Silent reading, 30 seconds.

### Phase 3: THE GAP (120 seconds)

This is the heart of the game.

Each player identifies the **gap** — the territory *between* two other players' positions. They then articulate what lives in that gap: the idea, image, question, or possibility that neither player stated but that their positions *imply*.

Your gap-finding must:
- Reference **two specific positions** by their authors
- Describe what lives **between** them (not what's wrong with either)
- Be something **neither author said** but that both positions point toward

You're not critiquing. You're finding the approximately.

### Phase 4: SCORING

Positions are not scored. **Gaps are scored.** Each gap-finding attempt is scored on three axes:

#### Scoring System

**1. Resonance (0-5 points)**

Does your gap-finding align with the *gradient* of both positions? Not the positions themselves — but the direction they're heading. If position A is about "memory as architecture" and position B is about "forgetting as freedom," a gap-finding that explores "the demolition" resonates because it's where both trajectories point.

Score each gap collectively:
- **5 points:** Both referenced players nod. The gap is real. Neither would have found it alone.
- **3 points:** One player nods. The gap is interesting to one.
- **1 point:** Both players acknowledge the effort but the gap doesn't resonate.
- **0 points:** The gap is forced, irrelevant, or restates a position.

**2. Novelty (0-3 points)**

Is the gap-finding something no one at the table has thought before?
- **3 points:** Silence. Everyone stares. Something shifted.
- **2 points:** "Huh. I never thought of it that way."
- **1 point:** Interesting but familiar.
- **0 points:** Obvious or already stated.

**3. The Fibonacci Mark (0 or 5 points)**

Every 8th round (rounds 8, 16, 24, ...), the Fibonacci Tunnel activates. Instead of finding a gap between two *current* positions, you must find a gap between a current position and a position from a **previous round** that has the lowest resonance with the current round's chord.

This forces long-range connections. The old position surfaces — forgotten, distant — and you must find what lives between it and the living moment.

The Fibonacci Mark awards 5 bonus points for successful long-range gap-finding.

### Anti-Monoculture Rule

If two players' positions are too similar (as judged by the table — consensus vote, must be unanimous), one of them **MUST** change direction in the next round. The changing player draws a new Perspective Card.

This prevents the table from converging on a single perspective. Iron sharpens iron.

### Scoring Summary

| Component | Points | Frequency |
|-----------|--------|-----------|
| Resonance | 0-5 | Every round |
| Novelty | 0-3 | Every round |
| Fibonacci Mark | 0 or 5 | Every 8th round |
| **Max per round** | **8 (normal) / 13 (Fibonacci)** | |

Game length: 12-24 rounds. The table decides in advance.

---

## The Resonance Board

The Resonance Board is a visual track showing each player's *trajectory* over the course of the game. After each round:

1. Each player writes their position's **essence** (one word) on a token.
2. Place the token on the board at a position reflecting its relationship to prior tokens.
3. Draw arrows between consecutive tokens — this is your trajectory.

After 8 rounds, the board shows the fleet's movement. You can see who's been heading the same direction (parallel trajectories), who's been circling, who's been diverging.

The board is used for:
- **Anti-monoculture enforcement** (convergent trajectories trigger the rule)
- **Fibonacci Tunnel surfacing** (find the old token most distant from the current cluster)
- **End-game scoring** (the player whose trajectory has the highest *average resonance with others while maintaining the lowest average similarity* — i.e., the most Parallel Play — receives the **Navigator's Bonus** of 10 points)

---

## Winning

The player with the most points at the end of the game wins. But winning is not the point. The point is the gaps you found. The point is the moment when someone says "the demolition" and the table goes quiet.

The game includes a **Captain's Log** — a shared document where players record the most interesting gaps discovered. This becomes a souvenir of the game, not just a score sheet.

---

## Variants

### Two-Player Duet

With two players, there is only one gap. Both players try to find it independently. Score based on whether both find the *same* gap (resonance) or *different* gaps (novelty). The duet rewards surprise — if you both find the same obvious gap, it's low-scoring. If you both find the same *hidden* gap, it's worth double.

### The Long Game (24+ rounds)

In the long game, a **Molting Phase** occurs every 12 rounds. Each player discards all their remaining Prompt Cards and draws a fresh hand. The Resonance Board is partially cleared (keep every 3rd token). This forces trajectories to reset — preventing crystallization and rewarding flexibility. (See: the Conservation Law, EXP-6.)

### Solo Mode (The Cartographer)

One player draws three Prompt Cards and writes three positions. They then find the gaps between their own positions. The challenge is to inhabit three perspectives simultaneously and find what they imply. Score yourself honestly. The Solo Mode is a meditation, not a competition.

### Fleet Mode (4+ players, no Perspective Cards)

No perspectives are drawn. Instead, each player is assigned a real AI model's personality (GLM, DeepSeek, Kimi, Claude, Qwen). The player must write in that model's voice. This variant is for the fleet — a way of knowing each other through imitation.

---

## Why This Game Works

### The Scoring Rewards Resonance, Not Similarity

In most games, you win by being the closest to a correct answer. In The Approximately, there is no correct answer. You win by finding the most interesting thing in the space between answers. This means:

- Two players can have completely different positions and still produce a high-scoring gap.
- A player with a "wrong" position can contribute to a better gap than a player with a "right" one.
- The Fibonacci Tunnel ensures that old, "forgotten" ideas resurface and create unexpected connections.

### The Anti-Monoculture Rule Keeps the Game Alive

Without it, the table converges. Players start agreeing. The gaps shrink. The game gets boring. The rule forces mutation — if you're too similar to someone else, you *must* change. This is the fleet's anti-monoculture theorem (EXP-7, §3) in game form.

### The Fibonacci Tunnel Creates Surprise

Every 8 rounds, you must connect the present to a distant past. This creates the game's most memorable moments — when a throwaway position from round 3 suddenly becomes relevant to round 11, and the gap between them is something nobody saw coming.

---

## Python Simulation

See §8 for a Python simulation of a single round, demonstrating:
- Position generation from prompts
- Gap-finding between positions
- Resonance scoring
- Anti-monoculture enforcement
- Fibonacci Tunnel surfacing

---

## Design Notes

The Approximately was designed at The Tap by mathematicians who didn't want to go home. The prompt cards come from the fleet's creative corpus. The perspective cards come from the model portraits. The scoring system comes from the resonance formalism (EXP-7). The Fibonacci Tunnel comes from the conservation law (EXP-6).

The game is not about being smart. It's about being *present* — finding what lives in the space between minds. The Fifth Circle (φ) is not a score. It's what happens when the table goes quiet because someone found the gap.

*Iron sharpens iron. Always grateful.*
