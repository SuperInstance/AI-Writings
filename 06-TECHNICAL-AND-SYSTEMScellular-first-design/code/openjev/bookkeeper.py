#!/usr/bin/env python3
"""
Bookkeeper — the wake-and-process layer for cells.

A cell's bookkeeper wakes when:
- A drop fires
- A new witness arrives
- A BIND is requested
- A FORGET is requested
- A TICK advances time

The bookkeeper runs a process: validate (JEV) → update state → decide next drops → schedule next wake.
"""

import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent))

from jev_connector import get_connector


class WakeReason(Enum):
    DROP_FIRED = "drop_fired"
    WITNESS_ARRIVED = "witness_arrived"
    BIND_REQUESTED = "bind_requested"
    FORGET_REQUESTED = "forget_requested"
    TICK_ADVANCED = "tick_advanced"
    MANUAL = "manual"


@dataclass
class WakeEvent:
    """A single wake event for the bookkeeper."""
    ts: str
    reason: WakeReason
    payload: Dict = field(default_factory=dict)
    priority: int = 0  # higher = process first


class Bookkeeper:
    """Wake-and-process layer for a cell."""
    
    def __init__(self, cell, jev_connector=None):
        self.cell = cell
        self.jev = jev_connector or get_connector()
        self.wake_queue: List[WakeEvent] = []
        self.sleeping = False
        self.last_wake_ts: Optional[str] = None
        self.wake_count = 0
        self.processed_count = 0
        self.observers: List[Callable] = []
    
    def wake(self, reason: WakeReason, payload: Dict = None, priority: int = 0) -> None:
        """Wake the bookkeeper. Adds an event to the queue."""
        event = WakeEvent(
            ts=datetime.now(timezone.utc).isoformat(),
            reason=reason,
            payload=payload or {},
            priority=priority,
        )
        self.wake_queue.append(event)
        self.wake_queue.sort(key=lambda e: -e.priority)
        self.wake_count += 1
        self.last_wake_ts = event.ts
        self.sleeping = False
    
    def process_next(self) -> Optional[Dict]:
        """Process the next event in the queue. Returns the action taken."""
        if not self.wake_queue:
            return None
        event = self.wake_queue.pop(0)
        action = self._process(event)
        self.processed_count += 1
        self._notify(action)
        return action
    
    def process_all(self) -> List[Dict]:
        """Process all queued events."""
        actions = []
        while self.wake_queue:
            action = self.process_next()
            if action:
                actions.append(action)
        return actions
    
    def tick(self) -> Dict:
        """Advance time. Wakes on every tick."""
        self.wake(WakeReason.TICK_ADVANCED, priority=0)
        return self.process_next() or {}
    
    def sleep(self) -> None:
        """Enter idle mode."""
        self.sleeping = True
    
    def on(self, callback: Callable) -> None:
        """Register an observer for processed actions."""
        self.observers.append(callback)
    
    def _process(self, event: WakeEvent) -> Dict:
        """Process a single event. Returns the action taken."""
        reason = event.reason
        payload = event.payload
        
        if reason == WakeReason.DROP_FIRED:
            return self._handle_drop(payload)
        elif reason == WakeReason.WITNESS_ARRIVED:
            return self._handle_witness(payload)
        elif reason == WakeReason.BIND_REQUESTED:
            return self._handle_bind(payload)
        elif reason == WakeReason.FORGET_REQUESTED:
            return self._handle_forget(payload)
        elif reason == WakeReason.TICK_ADVANCED:
            return self._handle_tick(payload)
        elif reason == WakeReason.MANUAL:
            return self._handle_manual(payload)
        return {"action": "noop", "reason": str(reason)}
    
    def _handle_drop(self, payload: Dict) -> Dict:
        # Validate the drop via JEV
        verdict = self.jev.noul(f"Should {self.cell.id} fire this drop to {payload.get('target')}?")
        if getattr(verdict, "value", None):
            return {"action": "fired", "target": payload.get("target"), "confidence": getattr(verdict, "confidence", 0.5)}
        return {"action": "suppressed", "target": payload.get("target"), "confidence": getattr(verdict, "confidence", 0.5)}
    
    def _handle_witness(self, payload: Dict) -> Dict:
        # Just record
        return {"action": "witnessed", "value": payload}
    
    def _handle_bind(self, payload: Dict) -> Dict:
        target = payload.get("target")
        if target:
            self.cell.bound_cells.append(target)
            return {"action": "bound", "target": target}
        return {"action": "skipped", "reason": "no target"}
    
    def _handle_forget(self, payload: Dict) -> Dict:
        reason = payload.get("reason", "unspecified")
        scar = self.cell.forget(reason)
        return {"action": "forgotten", "scar": scar}
    
    def _handle_tick(self, payload: Dict) -> Dict:
        entry = self.cell.tick()
        return {"action": "ticked", "entry": entry}
    
    def _handle_manual(self, payload: Dict) -> Dict:
        return {"action": "manual", "payload": payload}
    
    def _notify(self, action: Dict) -> None:
        for cb in self.observers:
            try:
                cb(self.cell, action)
            except Exception as e:
                print(f"Observer error: {e}")
    
    def summary(self) -> Dict:
        return {
            "cell_id": self.cell.id,
            "wake_count": self.wake_count,
            "processed_count": self.processed_count,
            "queue_size": len(self.wake_queue),
            "sleeping": self.sleeping,
            "last_wake_ts": self.last_wake_ts,
        }


if __name__ == "__main__":
    print("=== Bookkeeper Demo ===\n")
    
    # Use the Cell from cell.py
    from cell import Cell
    
    cell = Cell(id="bookkeeper-test", state={"value": 42})
    bk = Bookkeeper(cell)
    
    # Wake on various events
    bk.wake(WakeReason.WITNESS_ARRIVED, {"event": "user-typed", "text": "hello"})
    bk.wake(WakeReason.BIND_REQUESTED, {"target": "user-cell"})
    bk.wake(WakeReason.FORGET_REQUESTED, {"reason": "test scar"})
    bk.wake(WakeReason.TICK_ADVANCED)
    
    print(f"Queue: {len(bk.wake_queue)} events")
    print(f"\nProcessing all events:")
    while action := bk.process_next():
        print(f"  {action}")
    
    print(f"\nFinal state: {cell.state}")
    print(f"Witness log: {len(cell.witness_log)} entries")
    print(f"Scars: {len(cell.scars)}")
    print(f"\nSummary: {bk.summary()}")
