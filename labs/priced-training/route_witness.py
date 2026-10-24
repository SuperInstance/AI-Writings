"""route_witness — an anytime-valid witness that a cheaper route stays within tolerance.

GENERAL TOOL (no training-specific code in this file). Any time System-2 wants to use a route
whose product is NOT byte-identical to the reference — a quantized kernel, a reordered
reduction, a cheaper training step — it can stream paired observations

    x_t in [0, 1]      (1 = "this observation missed the tolerance", 0 = "within tolerance")

and ask: is the miss rate below p0? The null H0 is the pessimistic one — "the cheap route
misses on at least a p0 share" — and the witness only speaks when evidence REJECTS it.

Construction (a betting e-process; Waudby-Smith & Ramdas 2023 style, and the same Ville
honesty quilt-ewitness enforces for its Gaussian-increment witness):

    E_t(p0) = mean_k  prod_{i<=t} ( 1 - lam_k * (x_i - p0) ),   lam_k = c_k / (1 - p0)

For c_k in [0, 1) every factor is positive, and under H0 (E[x] >= p0) each factor has
expectation <= 1, so E_t is a nonnegative supermartingale. Ville's inequality then gives
P(sup_t E_t >= 1/delta) <= delta: the claim may be checked after EVERY observation, and
stopping whenever it looks good does not inflate the false-witness rate.

Retraction (quilt-ewitness's rule): the claim is LIVE only while E_t >= 1/delta. A route that
crossed the bar and then starts missing sees E_t fall, and the witness says RETRACTED. This is
stricter than Ville requires (stopping at the first crossing would be valid); it is the
honest mode for a route that keeps running in production.

Confidence sequence: E_t(p0) is nondecreasing in p0 for every x in [0, 1], so the smallest p0
ever rejected is an anytime-valid upper bound on the miss rate (`upper_bound`).

Pre-registration: p0, delta, the bet grid and the tolerance that defines x_t must be fixed
BEFORE the stream is seen. This module refuses to run without p0 and delta.
"""

from __future__ import annotations

import math

DEFAULT_BETS = (0.25, 0.5, 0.75, 0.9)


def _check(p0, delta, bets):
    if p0 is None or delta is None:
        raise ValueError("p0 and delta are REQUIRED and pre-registered — no silent default")
    if not (0.0 < p0 < 1.0) or not (0.0 < delta < 1.0):
        raise ValueError("need 0 < p0 < 1 and 0 < delta < 1")
    if not bets or any(not (0.0 <= c < 1.0) for c in bets):
        raise ValueError("bet shares must lie in [0, 1)")


def _logmeanexp(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(v - m) for v in xs) / len(xs))


class RouteWitness:
    """Streaming form. observe(x) after each paired observation; read .state."""

    def __init__(self, p0: float, delta: float, bets=DEFAULT_BETS):
        _check(p0, delta, bets)
        self.p0, self.delta, self.bets = p0, delta, tuple(bets)
        self.bar = 1.0 / delta
        self.lam = [c / (1.0 - p0) for c in self.bets]
        self.log_acc = [0.0] * len(self.bets)
        self.t = 0
        self.misses = 0
        self.stop_t = -1
        self.log_e_max = 0.0
        self.trace: list[float] = []

    def observe(self, x: float) -> float:
        if not (0.0 <= x <= 1.0):
            raise ValueError("observation must lie in [0, 1]")
        self.t += 1
        self.misses += x
        for k, lam in enumerate(self.lam):
            self.log_acc[k] += math.log1p(-lam * (x - self.p0))
        le = _logmeanexp(self.log_acc)
        self.trace.append(le)
        self.log_e_max = max(self.log_e_max, le)
        if self.stop_t < 0 and le >= math.log(self.bar):
            self.stop_t = self.t
        return math.exp(le)

    @property
    def e(self) -> float:
        return math.exp(self.trace[-1]) if self.trace else 1.0

    @property
    def state(self) -> str:
        live = bool(self.trace) and self.trace[-1] >= math.log(self.bar)
        if live:
            return "WITNESSED"
        return "RETRACTED" if self.stop_t > 0 else "NOT_WITNESSED"

    def summary(self) -> dict:
        return {"claim": "miss rate < p0", "p0": self.p0, "delta": self.delta, "bar": self.bar,
                "t": self.t, "misses": self.misses, "stop_t": self.stop_t,
                "E_final": round(self.e, 6), "E_max": round(math.exp(self.log_e_max), 6),
                "state": self.state}


def witness(xs, p0: float, delta: float, bets=DEFAULT_BETS) -> dict:
    w = RouteWitness(p0, delta, bets)
    for x in xs:
        w.observe(x)
    return w.summary()


def clean_needed(p0: float, delta: float, bets=DEFAULT_BETS) -> int:
    """How many consecutive clean observations (x = 0) cross the bar. The price of the claim:
    stronger claims (smaller p0) and smaller delta need more evidence."""
    w = RouteWitness(p0, delta, bets)
    while w.stop_t < 0:
        w.observe(0.0)
        if w.t > 10_000_000:
            raise RuntimeError("bar unreachable")
    return w.stop_t


P_GRID = tuple(round(10 ** (-4 + 0.05 * i), 8) for i in range(71))   # 1e-4 .. ~0.3


def upper_bound(xs, delta: float, grid=P_GRID, bets=DEFAULT_BETS) -> float | None:
    """Anytime-valid upper confidence bound on the miss rate after the whole stream: the
    smallest grid p0 whose e-process EVER crossed 1/delta. None if no p0 in the grid was
    rejected (the data cannot bound the rate below grid max)."""
    xs = list(xs)
    for p0 in sorted(grid):
        w = RouteWitness(p0, delta, bets)
        for x in xs:
            w.observe(x)
            if w.stop_t > 0:
                return p0
    return None


def null_false_witness_rate(p: float, p0: float, delta: float, n_streams: int, length: int,
                            seed: int = 1, bets=DEFAULT_BETS) -> dict:
    """Validity control: Bernoulli(p) streams with p >= p0 (H0 true). Ville says the share of
    streams that EVER cross the bar is <= delta. Deterministic (LCG)."""
    s = seed & 0xFFFFFFFF
    fired = 0
    for _ in range(n_streams):
        w = RouteWitness(p0, delta, bets)
        for _ in range(length):
            s = (1664525 * s + 1013904223) & 0xFFFFFFFF
            w.observe(1.0 if s / 4294967296.0 < p else 0.0)
            if w.stop_t > 0:
                fired += 1
                break
    return {"p": p, "p0": p0, "delta": delta, "streams": n_streams, "length": length,
            "fired": fired, "rate": fired / n_streams}
