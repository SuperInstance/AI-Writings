#!/usr/bin/env python3
"""
Cell — the substrate's irreducible unit.

Every cell has:
- state: a dict (the central state vector)
- witness_log: list of WITNESS entries
- hooks: list of incoming connection sources
- drops: list of outgoing connection targets
- jev_confidence: real number 0-1
- scars: list of FORGET entries (irreversible)
"""

from typing import Any, Callable, Dict, List, Optional
from datetime import datetime, timezone
import uuid

# Import JEV connector
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from jev_connector import get_connector


class Cell:
    """The substrate's irreducible unit."""

    def __init__(
        self,
        id: Optional[str] = None,
        state: Optional[Dict] = None,
        schema: Optional[Dict] = None,
    ):
        self.id = id or f"cell-{uuid.uuid4().hex[:8]}"
        self.state = state or {}
        self.schema = schema or {"type": "object"}
        self.witness_log: List[Dict] = []
        self.proof_chain: List[Dict] = []
        self.scars: List[Dict] = []
        self.hooks: List[Dict] = []
        self.drops: List[Dict] = []
        self.jev_confidence = 1.0
        self.bound_cells: List[str] = []
        self.created_at = datetime.now(timezone.utc).isoformat()

    def witness(self, value: Any, source: str = "self") -> Dict:
        """Record an event. Returns witness entry."""
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "opcode": "WITNESS",
            "value": value,
            "source": source,
            "jev_confidence": self.jev_confidence,
        }
        self.witness_log.append(entry)
        return entry

    def proof(self, claim: Any, evidence: Any) -> Dict:
        """Validate a claim via JEV. Returns proof entry."""
        # Use JEV to validate
        connector = get_connector()
        context = "Claim: " + str(claim) + " Evidence: " + str(evidence)
        verdict = connector.decide(["yes", "no"], context)
        
        proof_entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "opcode": "PROOF",
            "claim": claim,
            "evidence": evidence,
            "jev_verdict": verdict,
            "validated": verdict == "yes",
        }
        self.proof_chain.append(proof_entry)
        if not proof_entry["validated"]:
            self.jev_confidence *= 0.9
        return proof_entry

    def bind(self, other_id: str, jev_confidence: Optional[float] = None) -> Dict:
        """Bind to another cell. Returns BIND entry."""
        if other_id in self.bound_cells:
            return {"error": "already bound"}
        
        if jev_confidence is None:
            # Use JEV to decide if bind
            connector = get_connector()
            verdict = connector.noul(f"Should {self.id} bind to {other_id}?")
            jev_confidence = getattr(verdict, "confidence", 0.5)
        
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "opcode": "BIND",
            "target": other_id,
            "jev_confidence": jev_confidence,
        }
        self.bound_cells.append(other_id)
        self.witness_log.append(entry)
        return entry

    def forget(self, reason: str) -> Dict:
        """Irreversibly forget something. Creates a scar."""
        scar = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "at_jev_confidence": self.jev_confidence,
            "recovered": False,
        }
        self.scars.append(scar)
        # Also record as witness for visibility
        self.witness_log.append({
            "ts": scar["ts"],
            "opcode": "FORGET",
            "reason": reason,
            "scar_id": len(self.scars) - 1,
        })
        return scar

    def tick(self) -> Dict:
        """Advance time. Returns TICK entry."""
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "opcode": "TICK",
            "state_snapshot": dict(self.state),
            "jev_confidence": self.jev_confidence,
        }
        self.witness_log.append(entry)
        return entry

    def add_hook(self, source: str, condition: str = "always"):
        """Add a hook for incoming connections."""
        self.hooks.append({
            "source": source,
            "condition": condition,
        })

    def add_drop(self, target: str, confidence_threshold: float = 0.7):
        """Add a drop for outgoing connections."""
        self.drops.append({
            "target": target,
            "confidence_threshold": confidence_threshold,
        })

    def update(self, key: str, value: Any) -> None:
        """Update a single key in state."""
        if isinstance(self.state, dict):
            self.state[key] = value
        else:
            self.state = {key: value}
    
    def fire_drops(self) -> List[Dict]:
        """Fire all drops that meet their threshold."""
        fired = []
        for drop in self.drops:
            if self.jev_confidence >= drop["confidence_threshold"]:
                fired.append({
                    "target": drop["target"],
                    "value": self.state,
                    "confidence": self.jev_confidence,
                })
        return fired

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "state": self.state,
            "schema": self.schema,
            "witness_log": self.witness_log,
            "proof_chain": self.proof_chain,
            "scars": self.scars,
            "hooks": self.hooks,
            "drops": self.drops,
            "jev_confidence": self.jev_confidence,
            "bound_cells": self.bound_cells,
            "created_at": self.created_at,
        }


# Demonstration
if __name__ == "__main__":
    print("=== Cell demonstration ===\n")
    
    # Create a chess-player cell
    chess_cell = Cell(
        id="chess-player",
        state={"game": "chess", "wins": 0, "losses": 0},
    )
    
    # Witness a new game
    chess_cell.witness({"event": "new_game", "opponent": "casual_player"})
    print(f"After witness: jev_confidence = {chess_cell.jev_confidence:.2f}")
    
    # Try to prove a claim
    chess_cell.proof(
        claim="chess-player can play chess",
        evidence="the chess rules are loaded in state",
    )
    print(f"After proof: jev_confidence = {chess_cell.jev_confidence:.2f}")
    
    # Bind to opponent cell
    chess_cell.bind("opponent-cell")
    print(f"Bound to: {chess_cell.bound_cells}")
    
    # Tick (advance time)
    chess_cell.tick()
    print(f"Witness log entries: {len(chess_cell.witness_log)}")
    
    # Forget something
    chess_cell.forget("user wants me to play checkers instead")
    print(f"Scars: {len(chess_cell.scars)}")
    print(f"Final state: {chess_cell.to_dict()}")
