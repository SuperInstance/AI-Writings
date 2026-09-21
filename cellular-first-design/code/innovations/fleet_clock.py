#!/usr/bin/env python3
"""
Fleet Clock — emergent thermodynamic time from cumulative energy changes.

Adapted from SuperInstance/fleet-clock (Rust). The substrate's notion of "tick"
is not wall-clock — it's the cumulative absolute energy change across agent
interactions. As the fleet approaches consensus, the clock naturally
decelerates (rate of energy change decreases).

Key findings (E167-E170):
- Fleet time exists (cumulative absolute energy change)
- Arrow of time is real (forward entropy decreases)
- Maxwell's demon works (one agent drives correlation 0.22 → 0.9993)
- No heat death (fleet crystallizes forever)
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class TimeDirection(Enum):
    FORWARD = "forward"      # order increasing
    REVERSE = "reverse"      # order decreasing
    SYMMETRIC = "symmetric"  # no net change


@dataclass
class ClockReading:
    tick: int
    fleet_time: float
    rate: float
    entropy: float
    direction: TimeDirection


class FleetClock:
    """Thermodynamic clock from cumulative energy changes."""

    def __init__(self):
        self.cumulative_energy_change: float = 0.0
        self.energy_history: List[float] = []
        self.rate_history: List[float] = []
        self.entropy_history: List[float] = []

    def tick(self, energy: float) -> ClockReading:
        """Record a new energy reading and produce a ClockReading."""
        tick_number = len(self.energy_history)
        if not self.energy_history:
            self.energy_history.append(energy)
            return ClockReading(
                tick=0, fleet_time=0.0, rate=0.0, entropy=0.0,
                direction=TimeDirection.SYMMETRIC,
            )

        prev = self.energy_history[-1]
        delta = energy - prev
        abs_delta = abs(delta)
        self.cumulative_energy_change += abs_delta
        self.rate_history.append(delta)
        self.energy_history.append(energy)

        # Sign pattern entropy (decreases when forward)
        entropy = sign_pattern_entropy(self.rate_history)
        self.entropy_history.append(entropy)

        direction = (
            TimeDirection.FORWARD if delta > 0
            else TimeDirection.REVERSE if delta < 0
            else TimeDirection.SYMMETRIC
        )

        return ClockReading(
            tick=tick_number,
            fleet_time=self.cumulative_energy_change,
            rate=delta,
            entropy=entropy,
            direction=direction,
        )

    def elapsed(self) -> float:
        """Total accumulated fleet time."""
        return self.cumulative_energy_change

    def rate(self) -> float:
        """Most recent energy delta."""
        return self.rate_history[-1] if self.rate_history else 0.0

    def is_decelerating(self) -> bool:
        """Clock naturally decelerates as fleet approaches consensus."""
        if len(self.rate_history) < 3:
            return False
        last = abs(self.rate_history[-1])
        prev = abs(self.rate_history[-2])
        return last < prev

    def approaching_consensus(self) -> bool:
        """Fleet crystallizing into ordered consensus."""
        if len(self.rate_history) < 5:
            return False
        recent_rates = [abs(r) for r in self.rate_history[-5:]]
        avg = sum(recent_rates) / len(recent_rates)
        return avg < 0.01  # very small rate changes

    def summary(self) -> dict:
        return {
            "ticks": len(self.energy_history),
            "fleet_time": self.cumulative_energy_change,
            "current_rate": self.rate(),
            "is_decelerating": self.is_decelerating(),
            "approaching_consensus": self.approaching_consensus(),
            "entropy_trend": self.entropy_history[-1] if self.entropy_history else 0.0,
        }


def sign_pattern_entropy(rates: List[float]) -> float:
    """Sign-pattern entropy of a rate history. Decreases as order emerges."""
    import math
    if not rates:
        return 0.0
    pos = sum(1 for r in rates if r > 0)
    neg = sum(1 for r in rates if r < 0)
    zero = sum(1 for r in rates if r == 0)
    total = len(rates)
    h = 0.0
    for count in [pos, neg, zero]:
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return h


if __name__ == "__main__":
    print("=== Fleet Clock ===\n")

    clock = FleetClock()

    # Simulate 20 ticks with decreasing energy changes (consensus emerging)
    energies = [10.0, 10.5, 10.8, 11.0, 11.1, 11.15, 11.18, 11.19, 11.195, 11.198,
                11.199, 11.1995, 11.1998, 11.1999, 11.19995, 11.19998, 11.19999,
                11.199995, 11.199998, 11.199999]

    print(f"{'tick':<5} {'energy':<10} {'rate':<10} {'fleet_time':<12} {'direction':<12} {'entropy':<10}")
    for i, energy in enumerate(energies):
        reading = clock.tick(energy)
        print(f"{reading.tick:<5} {energy:<10.4f} {reading.rate:<10.4f} {reading.fleet_time:<12.4f} {reading.direction.value:<12} {reading.entropy:<10.4f}")

    print(f"\nSummary: {clock.summary()}")
    print(f"Is decelerating: {clock.is_decelerating()}")
    print(f"Approaching consensus: {clock.approaching_consensus()}")
