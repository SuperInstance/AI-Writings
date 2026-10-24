#!/usr/bin/env python3
"""
Conservation Monitor — enforce γ + η = budget per cell + across the fleet.

Adapted from SuperInstance/spreadsheet-engine/src/conservation.rs.
The substrate's fundamental invariant: every cell has compute budget (γ) +
memory budget (η) = total budget. ConservationMonitor tracks this and
detects violations.

Health = 1.0 - |γ + η - budget| / budget (0.0-1.0)
Trend = improving / degrading / stable (last 5 ticks)
"""

import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

sys.path.insert(0, "/workspace/repos/ai-writings/cellular-first-design/code/openjev")

from cell import Cell


@dataclass
class AgentCellBudget:
    """Per-cell budget tracker."""
    gamma: float = 0.0  # compute spent
    eta: float = 0.0    # memory used
    budget: float = 100.0  # total budget for this cell
    tolerance: float = 0.05  # 5% tolerance

    @property
    def used(self) -> float:
        return self.gamma + self.eta

    @property
    def remaining(self) -> float:
        return max(0.0, self.budget - self.used)

    @property
    def is_healthy(self) -> bool:
        return abs(self.used - self.budget) / max(self.budget, 1e-12) <= self.tolerance

    @property
    def utilization(self) -> float:
        """Fraction of budget used (0.0-1.0+)."""
        return self.used / max(self.budget, 1e-12)

    def spend(self, compute: float = 0.0, memory: float = 0.0) -> None:
        self.gamma += compute
        self.eta += memory


class ConservationMonitor:
    """Fleet-wide conservation monitor. Tracks γ + η = budget across all cells."""

    def __init__(self, total_budget: float = 1000.0, tolerance: float = 0.05):
        self.total_budget = total_budget
        self.tolerance = tolerance
        self.cell_budgets: Dict[str, AgentCellBudget] = {}
        self.history: List[tuple] = []  # (tick, health)

    def register(self, cell_id: str, budget: float = 100.0, gamma: float = 0.0, eta: float = 0.0) -> None:
        """Register a cell with its budget."""
        self.cell_budgets[cell_id] = AgentCellBudget(gamma=gamma, eta=eta, budget=budget, tolerance=self.tolerance)

    def spend(self, cell_id: str, compute: float = 0.0, memory: float = 0.0) -> None:
        """Record spend for a cell."""
        if cell_id not in self.cell_budgets:
            self.register(cell_id)
        self.cell_budgets[cell_id].spend(compute, memory)

    def health(self) -> float:
        """Fleet-wide conservation health (0.0-1.0)."""
        if not self.cell_budgets:
            return 1.0
        total_gamma = sum(b.gamma for b in self.cell_budgets.values())
        total_eta = sum(b.eta for b in self.cell_budgets.values())
        total_used = total_gamma + total_eta
        if self.total_budget < 1e-12:
            return 1.0
        error = abs(total_used - self.total_budget)
        return max(0.0, 1.0 - (error / self.total_budget))

    def record(self, tick: int) -> float:
        """Record a health reading at this tick."""
        h = self.health()
        self.history.append((tick, h))
        return h

    def violations(self) -> List[str]:
        """Cell IDs violating their individual budgets."""
        return [cid for cid, b in self.cell_budgets.items() if not b.is_healthy]

    def trend(self) -> str:
        """Recent trend: improving / degrading / stable."""
        if len(self.history) < 2:
            return "stable"
        recent = self.history[-5:]
        if len(recent) < 2:
            return "stable"
        first = recent[0][1]
        last = recent[-1][1]
        diff = last - first
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "degrading"
        return "stable"

    def summary(self) -> Dict:
        return {
            "total_budget": self.total_budget,
            "cells": len(self.cell_budgets),
            "violations": len(self.violations()),
            "health": self.health(),
            "trend": self.trend(),
            "history_len": len(self.history),
        }


if __name__ == "__main__":
    print("=== Conservation Monitor ===\n")

    monitor = ConservationMonitor(total_budget=1000.0, tolerance=0.05)

    # Register 5 cells with budgets
    for i, cid in enumerate(["memory", "mood", "personality", "bookkeeper", "jev"]):
        monitor.register(cid, budget=200.0, gamma=50.0 + i * 10, eta=30.0 + i * 5)

    print(f"Initial: {monitor.summary()}")

    # Spend some compute
    monitor.spend("memory", compute=80.0, memory=40.0)
    monitor.spend("mood", compute=10.0, memory=5.0)
    monitor.record(tick=1)

    print(f"After spend: {monitor.summary()}")
    print(f"Violations: {monitor.violations()}")

    # Force a violation
    monitor.spend("personality", compute=200.0, memory=200.0)
    monitor.record(tick=2)

    print(f"\nAfter massive spend: {monitor.summary()}")
    print(f"Violations: {monitor.violations()}")
