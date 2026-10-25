#!/usr/bin/env python3
"""
Ternary JEV Adapter — bridge between float probabilities and ternary decisions.

JEV returns calibrated probabilities as floats. The substrate's natural algebra
is ternary {-1, 0, +1}. This adapter maps:

- probabilities near 0.0 (low confidence) → -1 (reject / false)
- probabilities near 0.5 (uncertain)     → 0 (neutral / unknown)
- probabilities near 1.0 (high confidence) → +1 (approve / true)

The threshold and deadband are configurable. The comb predicate (from Q16):
two ternaries are "commensurate" if their product is exact in {-1, 0, +1}.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TernaryValue(Enum):
    NEGATIVE = -1   # reject, false, down
    NEUTRAL = 0     # uncertain, unknown, same
    POSITIVE = +1   # approve, true, up

    def __repr__(self):
        return f"T({self.value:+d})"

    def __int__(self):
        return self.value


@dataclass
class TernaryJEV:
    """Map float probabilities to ternary values with thresholds."""
    reject_threshold: float = 0.33  # below this → -1
    approve_threshold: float = 0.67  # above this → +1
    # between → 0

    def to_ternary(self, probability: float) -> TernaryValue:
        """Map a single probability to ternary."""
        if probability < self.reject_threshold:
            return TernaryValue.NEGATIVE
        elif probability > self.approve_threshold:
            return TernaryValue.POSITIVE
        else:
            return TernaryValue.NEUTRAL

    def from_ternary(self, ternary: TernaryValue) -> float:
        """Map ternary back to canonical probability (for JEV)."""
        if ternary == TernaryValue.NEGATIVE:
            return 0.0
        elif ternary == TernaryValue.POSITIVE:
            return 1.0
        else:
            return 0.5

    def batch_to_ternary(self, probabilities: dict) -> dict:
        """Map a probability distribution {key: prob} to ternary."""
        return {k: self.to_ternary(v) for k, v in probabilities.items()}

    def commensurable(self, a: TernaryValue, b: TernaryValue) -> bool:
        """Q16-style comb predicate: two ternaries are commensurable if their
        product is in {-1, 0, +1} (always true for ternary). Returns True
        for "exact identity"; the substrate treats neutral as a separator."""
        return a != TernaryValue.NEUTRAL or b != TernaryValue.NEUTRAL

    def entropy(self, distribution: dict) -> float:
        """Shannon entropy of a ternary distribution.
        Max entropy (uniform {-1, 0, +1}) = log2(3) ≈ 1.585 bits.
        """
        import math
        total = sum(distribution.values())
        if total == 0:
            return 0.0
        h = 0.0
        for v in distribution.values():
            p = v / total
            if p > 0:
                h -= p * math.log2(p)
        return h


# Convenience
def jev_to_ternary(probability: float, reject: float = 0.33, approve: float = 0.67) -> TernaryValue:
    """Quick: convert a JEV probability to ternary."""
    return TernaryJEV(reject, approve).to_ternary(probability)


if __name__ == "__main__":
    print("=== Ternary JEV Adapter ===\n")

    tj = TernaryJEV()
    print("Single mappings:")
    for p in [0.0, 0.1, 0.3, 0.33, 0.5, 0.67, 0.8, 0.95, 1.0]:
        print(f"  {p:.2f} → {tj.to_ternary(p)}")

    print("\nDistribution mapping:")
    probs = {"approve": 0.82, "neutral": 0.15, "reject": 0.03}
    tern = tj.batch_to_ternary(probs)
    for k, v in tern.items():
        print(f"  {k}: {probs[k]:.2f} → {v}")

    print(f"\nEntropy of uniform ternary: {tj.entropy({-1: 1, 0: 1, 1: 1}):.3f} bits")
    print(f"Entropy of all-positive: {tj.entropy({1: 10}):.3f} bits")
    print(f"Entropy of 50/50 split: {tj.entropy({-1: 5, 1: 5}):.3f} bits")
