"""q16 exact-rational codec. Identity is (num:int64, den:int64); floats are
display projections only — the same codec as the fleet's lattice kernel.
"""

from __future__ import annotations
from dataclasses import dataclass
from math import gcd

SCALE = 10 ** 6  # ℚ×10⁶: denominators divide 10⁶ exactly (dyadic × 5-adic)


@dataclass(frozen=True)
class Q16:
    num: int
    den: int = 1

    def __post_init__(self):
        if self.den == 0:
            raise ZeroDivisionError("q16: zero denominator")
        g = gcd(self.num, self.den)
        object.__setattr__(self, "num", self.num // g)
        object.__setattr__(self, "den", self.den // g)
        if self.den < 0:
            object.__setattr__(self, "num", -self.num)
            object.__setattr__(self, "den", -self.den)

    @classmethod
    def from_float(cls, f: float) -> "Q16":
        """Projection INTO the lattice. Rejects values that are not
        representable (never silently rounds identity)."""
        num = round(f * SCALE)
        if abs(num / SCALE - f) > 1e-12:
            raise ValueError(f"q16: {f!r} is not a ℚ×10⁶ rational")
        return cls(num, SCALE)

    def to_float(self) -> float:
        return self.num / self.den

    def __add__(self, o: "Q16") -> "Q16":
        return Q16(self.num * o.den + o.num * self.den, self.den * o.den)

    def __sub__(self, o: "Q16") -> "Q16":
        return Q16(self.num * o.den - o.num * self.den, self.den * o.den)

    def __mul__(self, o: "Q16") -> "Q16":
        return Q16(self.num * o.num, self.den * o.den)

    def __truediv__(self, o: "Q16") -> "Q16":
        return Q16(self.num * o.den, self.den * o.num)

    def __eq__(self, o) -> bool:
        return isinstance(o, Q16) and self.num * o.den == o.num * self.den

    def __lt__(self, o: "Q16") -> bool:
        return self.num * o.den < o.num * self.den

    def __le__(self, o: "Q16") -> bool:
        return self.num * o.den <= o.num * self.den

    def __ge__(self, o: "Q16") -> bool:
        return self.num * o.den >= o.num * self.den

    def __gt__(self, o: "Q16") -> bool:
        return self.num * o.den > o.num * self.den

    def __hash__(self):
        return hash((self.num, self.den))

    def __repr__(self):
        return f"Q16({self.num}/{self.den})"


def commensurate(a: Q16, b: Q16) -> bool:
    """The comb predicate: a/b's reduced denominator divides 10⁶.
    TRUE means the pair lives on a common decimal lattice; FALSE is a
    ternary ghost (e.g. 1/3 against 1)."""
    if b.num == 0:
        return a.num == 0
    r = a / b
    return SCALE % r.den == 0
