#!/usr/bin/env python3
"""
Cross-Instance Fabric — cells in different instances entangle.

An Instance is a container of cells.
A Fabric routes events between instances.
An Entanglement is a long-lived connection between 2 cells in different instances.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

sys.path.insert(0, str(Path(__file__).parent))

from cell import Cell
from bookkeeper import Bookkeeper, WakeReason


class Instance:
    """A container of cells (like a Quilt instance)."""
    
    def __init__(self, name: str):
        self.name = name
        self.cells: Dict[str, Cell] = {}
        self.bookkeepers: Dict[str, Bookkeeper] = {}
    
    def add(self, cell: Cell, with_bookkeeper: bool = True) -> None:
        self.cells[cell.id] = cell
        if with_bookkeeper:
            self.bookkeepers[cell.id] = Bookkeeper(cell)
    
    def remove(self, cell_id: str) -> None:
        self.cells.pop(cell_id, None)
        self.bookkeepers.pop(cell_id, None)
    
    def get(self, cell_id: str) -> Optional[Cell]:
        return self.cells.get(cell_id)
    
    def tick_all(self) -> List[Dict]:
        """Tick all cells. Each cell's bookkeeper processes the tick."""
        actions = []
        for bk in self.bookkeepers.values():
            action = bk.tick()
            if action:
                actions.append(action)
        return actions
    
    def summary(self) -> Dict:
        return {
            "name": self.name,
            "cells": list(self.cells.keys()),
            "cell_count": len(self.cells),
        }


@dataclass
class Entanglement:
    """A long-lived connection between 2 cells in different instances."""
    id: str
    source_cell_id: str
    source_instance: str
    target_cell_id: str
    target_instance: str
    jev_confidence: float = 0.5
    created_at: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = f"ent-{uuid.uuid4().hex[:8]}"
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


class Fabric:
    """Routes events between instances. Manages entanglements."""
    
    def __init__(self, instances: List[Instance] = None):
        self.instances: Dict[str, Instance] = {}
        self.entanglements: Dict[str, Entanglement] = {}
        if instances:
            for inst in instances:
                self.add_instance(inst)
    
    def add_instance(self, instance: Instance) -> None:
        self.instances[instance.name] = instance
    
    def connect(self, cell_a_id: str, instance_a: str, cell_b_id: str, instance_b: str, jev_confidence: float = 0.5) -> Entanglement:
        """Connect 2 cells in different instances."""
        if instance_a == instance_b:
            raise ValueError("Use direct cell.bind() for same-instance connections")
        
        ent = Entanglement(
            id="",
            source_cell_id=cell_a_id,
            source_instance=instance_a,
            target_cell_id=cell_b_id,
            target_instance=instance_b,
            jev_confidence=jev_confidence,
        )
        self.entanglements[ent.id] = ent
        return ent
    
    def broadcast(self, source_cell_id: str, from_instance: str, state: Any = None) -> List[Dict]:
        """Broadcast a state change to all entangled cells in other instances."""
        results = []
        for ent in self.entanglements.values():
            if ent.source_cell_id == source_cell_id and ent.source_instance == from_instance:
                # Send to target
                target_inst = self.instances.get(ent.target_instance)
                if target_inst:
                    target_cell = target_inst.get(ent.target_cell_id)
                    if target_cell:
                        target_cell.witness({
                            "from": from_instance,
                            "from_cell": source_cell_id,
                            "state": state,
                            "entanglement": ent.id,
                            "confidence": ent.jev_confidence,
                        })
                        results.append({
                            "target": ent.target_cell_id,
                            "instance": ent.target_instance,
                            "delivered": True,
                        })
        return results
    
    def entanglements_for(self, cell_id: str) -> List[Entanglement]:
        return [e for e in self.entanglements.values() if e.source_cell_id == cell_id or e.target_cell_id == cell_id]
    
    def tick_all(self) -> Dict:
        """Tick all instances."""
        all_actions = {}
        for name, inst in self.instances.items():
            all_actions[name] = inst.tick_all()
        return all_actions
    
    def summary(self) -> Dict:
        return {
            "instances": list(self.instances.keys()),
            "entanglements": len(self.entanglements),
            "instance_details": {name: inst.summary() for name, inst in self.instances.items()},
        }


if __name__ == "__main__":
    print("=== Cross-Instance Fabric Demo ===\n")
    
    # Create 2 instances
    instance_a = Instance("frontend")
    instance_b = Instance("backend")
    instance_c = Instance("analytics")
    
    # Add cells to each
    user_cell = Cell(id="user-state", state={"user_id": "u1", "name": "Casey"})
    instance_a.add(user_cell)
    
    session_cell = Cell(id="session", state={"active": True})
    instance_a.add(session_cell)
    
    db_cell = Cell(id="db-row", state={"row_count": 1000})
    instance_b.add(db_cell)
    
    log_cell = Cell(id="log-buffer", state={"lines": 0})
    instance_b.add(log_cell)
    
    analytics_cell = Cell(id="agg-counter", state={"count": 0})
    instance_c.add(analytics_cell)
    
    # Create fabric
    fabric = Fabric([instance_a, instance_b, instance_c])
    
    # Connect cells across instances
    ent1 = fabric.connect("user-state", "frontend", "db-row", "backend")
    ent2 = fabric.connect("session", "frontend", "log-buffer", "backend")
    ent3 = fabric.connect("db-row", "backend", "agg-counter", "analytics")
    
    print(f"Fabric: {fabric.summary()}")
    print(f"Entanglements: {len(fabric.entanglements)}")
    
    # Broadcast from user-state
    print("\nBroadcasting from user-state...")
    user_cell.state["action"] = "view-dashboard"
    results = fabric.broadcast("user-state", "frontend", {"action": "view-dashboard"})
    print(f"  Results: {results}")
    
    # Check that backend received it
    print(f"\ndb-row witness log: {len(db_cell.witness_log)} entries")
    if db_cell.witness_log:
        print(f"  Latest: {db_cell.witness_log[-1]}")
    
    # Tick all instances
    print("\nTicking all instances...")
    tick_actions = fabric.tick_all()
    for inst_name, actions in tick_actions.items():
        print(f"  {inst_name}: {len(actions)} actions")
    
    print(f"\nFinal fabric summary:")
    print(fabric.summary())
