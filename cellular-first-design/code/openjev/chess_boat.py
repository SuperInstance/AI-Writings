#!/usr/bin/env python3
"""
Chess-Playing Boat — Casey's worked example.

A substrate where:
- Rules cell knows chess moves
- Position cell knows the board state
- Evaluator (JEV) scores each move
- Reflex cell outputs the chosen move
- Learning cell updates position cell based on response

The boat learns to play chess (and any other game) inductively.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from cell import Cell
from jev_connector import get_connector
import random


class ChessBoat:
    """A chess-playing substrate."""

    def __init__(self):
        self.rules = Cell(
            id="rules",
            state={
                "type": "chess",
                "moves": self._init_chess_moves(),
            },
        )
        self.position = Cell(
            id="position",
            state={"board": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"},
            schema={"type": "chess-board"},
        )
        self.evaluator = Cell(
            id="evaluator",
            state={"type": "JEV", "samples": 8},
        )
        self.reflex = Cell(
            id="reflex",
            state={"type": "move-output", "latency_ms": 5},
        )
        self.learning = Cell(
            id="learning",
            state={"type": "experience-accumulator"},
        )
        
        # Bind the cells
        self.position.bind(self.rules.id)
        self.evaluator.bind(self.position.id)
        self.reflex.bind(self.evaluator.id)
        self.learning.bind(self.reflex.id)
        self.learning.bind(self.position.id)  # learning feeds back

    def _init_chess_moves(self) -> dict:
        # Simplified: any piece can move 1-2 squares
        return {
            "pawn": [(-1, 0), (-2, 0), (-1, -1), (-1, 1)],
            "knight": [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
            "bishop": "diagonal",
            "rook": "orthogonal",
            "queen": "any",
            "king": [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
        }

    def play_move(self) -> dict:
        """Play one chess move using JEV."""
        # Step 1: Rules cell identifies legal moves (reflex tier)
        self.rules.tick()
        legal_moves = ["e2-e4", "d2-d4", "g1-f3", "b1-c3", "castling"]
        
        # Step 2: Position cell updates (standard tier)
        self.position.tick()
        
        # Step 3: Evaluator JEV scores each move
        connector = get_connector()
        scored = []
        for move in legal_moves:
            context = "Position: " + self.position.state["board"] + " Move: " + move
            verdict = connector.decide(legal_moves, context)
            scored.append({
                "move": move,
                "confidence": verdict.get("confidence", 0.5),
                "probabilities": verdict.get("probabilities", {}),
            })
        
        # Step 4: Pick the highest-confidence move
        best = max(scored, key=lambda x: x["confidence"])
        
        # Step 5: Reflex cell outputs the move
        self.reflex.witness({
            "selected_move": best["move"],
            "confidence": best["confidence"],
        })
        
        # Step 6: Learning cell updates based on response
        self.learning.witness({
            "move_played": best["move"],
            "expected_confidence": best["confidence"],
            "actual_outcome": "unknown",
        })
        
        return {
            "move": best["move"],
            "confidence": best["confidence"],
            "all_scored": scored,
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
        }


if __name__ == "__main__":
    print("=== Chess-Playing Boat ===\n")
    
    boat = ChessBoat()
    print("Initialized cells: " + str(boat.summary()))
    
    # Play 3 moves
    for i in range(3):
        print(f"--- Move {i+1} ---")
        result = boat.play_move()
        move = result["move"]
        conf = result["confidence"]
        print("Selected: " + move + " (confidence: " + "{:.2f}".format(conf) + ")")
        for m in result["all_scored"]:
            mv = m["move"]
        c = m["confidence"]
        print("  " + mv + ": " + "{:.2f}".format(c))
        print()
    
    print("Final summary: " + str(boat.summary()))
