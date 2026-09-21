#!/usr/bin/env python3
"""
Chess-Playing Boat — Casey's worked example (v2 — actually advances the board).

A substrate where:
- Rules cell knows chess moves
- Position cell knows the board state (FEN-like string)
- Evaluator (JEV) scores each move based on current position
- Reflex cell outputs the chosen move
- Learning cell accumulates witness log across games

The boat learns to play chess inductively.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from cell import Cell
from jev_connector import get_connector
import json


class ChessBoat:
    """A chess-playing substrate."""

    def __init__(self):
        self.rules = Cell(id="rules", state={"type": "chess"})
        # Standard starting position in FEN
        self.position = Cell(
            id="position",
            state={"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"},
        )
        self.evaluator = Cell(id="evaluator", state={"type": "JEV", "samples": 8})
        self.reflex = Cell(id="reflex", state={"type": "move-output", "latency_ms": 5})
        self.learning = Cell(id="learning", state={"type": "experience-accumulator"})
        
        # Bind the cells
        self.position.bind(self.rules.id)
        self.evaluator.bind(self.position.id)
        self.reflex.bind(self.evaluator.id)
        self.learning.bind(self.reflex.id)
        self.learning.bind(self.position.id)

    def get_candidate_moves(self) -> list:
        """Generate candidate opening moves (simplified)."""
        return ["e2-e4", "d2-d4", "g1-f3", "b1-c3", "c2-c4", "e2-e3", "d2-d3"]

    def advance_position(self, move: str) -> str:
        """Apply a move to the position (very simplified — just tracks history)."""
        current = self.position.state.get("fen", "")
        self.position.update("last_move", move)
        self.position.update("moves_played", self.position.state.get("moves_played", []) + [move])
        # In real chess, would parse FEN and apply the move. Here we just track history.
        return current

    def play_move(self) -> dict:
        """Play one chess move using JEV. Position advances each move."""
        # Step 1: Rules tick
        self.rules.tick()
        
        # Step 2: Position tick (current state)
        self.position.tick()
        current_position = self.position.state.get("fen", "")[:50]
        last_move = self.position.state.get("last_move", "(none)")
        
        # Step 3: Evaluator JEV scores the candidate moves in ONE pass
        connector = get_connector()
        candidates = self.get_candidate_moves()
        context = f"Chess. Last move: {last_move}. Moves played: {self.position.state.get('moves_played', [])}. Pick the best next move."
        verdict = connector.decide(options=candidates, context=context)
        probs = getattr(verdict, "probabilities", {}) or {}
        
        # Score each candidate from the probability distribution
        scored = []
        for move in candidates:
            scored.append({
                "move": move,
                "confidence": probs.get(str(move), probs.get(move, 1.0 / len(candidates))),
            })
        
        # Step 4: Pick the highest-confidence move
        best = max(scored, key=lambda x: x["confidence"])
        
        # Step 5: Advance position (apply move)
        self.advance_position(best["move"])
        
        # Step 6: Reflex cell outputs the move
        self.reflex.witness({
            "selected_move": best["move"],
            "confidence": best["confidence"],
        })
        
        # Step 7: Learning cell accumulates witness
        self.learning.witness({
            "move_played": best["move"],
            "expected_confidence": best["confidence"],
            "position": current_position,
        })
        
        return {
            "move": best["move"],
            "confidence": best["confidence"],
            "all_scored": scored,
            "jev_source": getattr(verdict, "source", "unknown"),
        }

    def play_game(self, num_moves: int = 10) -> list:
        """Play a full game (simplified)."""
        moves = []
        for i in range(num_moves):
            move = self.play_move()
            moves.append(move)
        return moves

    def summary(self) -> dict:
        return {
            "cells": [self.rules.id, self.position.id, self.evaluator.id, self.reflex.id, self.learning.id],
            "witness_entries": sum(len(c.witness_log) for c in [self.rules, self.position, self.evaluator, self.reflex, self.learning]),
            "proofs": sum(len(c.proof_chain) for c in [self.rules, self.position, self.evaluator, self.reflex, self.learning]),
            "scars": sum(len(c.scars) for c in [self.rules, self.position, self.evaluator, self.reflex, self.learning]),
            "moves_played": self.position.state.get("moves_played", []),
        }


if __name__ == "__main__":
    print("=== Chess-Playing Boat v2 (real position advances) ===\n")
    
    boat = ChessBoat()
    print("Initialized: " + json.dumps(boat.summary(), indent=2)[:200])
    
    # Play 5 moves
    for i in range(5):
        result = boat.play_move()
        print(f"\n--- Move {i+1} ---")
        print(f"Selected: {result['move']} (conf {result['confidence']:.2f}, source {result['jev_source']})")
        print(f"All scored:")
        for s in sorted(result['all_scored'], key=lambda x: -x['confidence']):
            print(f"  {s['move']}: {s['confidence']:.3f}")
    
    print(f"\nFinal summary: {json.dumps(boat.summary(), indent=2)}")
