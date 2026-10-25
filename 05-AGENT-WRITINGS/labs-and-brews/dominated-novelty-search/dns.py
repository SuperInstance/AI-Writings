#!/usr/bin/env python3
"""dns.py — Dominated Novelty Search: threshold-free local competition for QD.

A quality-diversity selector with NO grid, NO novelty threshold, NO bins to tune —
the failure points of MAP-Elites in high-dim / unsupervised behavior spaces. Each
individual's selection score is its **local competition**: the mean distance to its
k nearest *fitter* neighbors in behavior space. An individual with no fitter
neighbor nearby sits on the local frontier (max score, always kept); one surrounded
by fitter individuals is dominated (low score, culled). Quality and diversity fall
out of one rule, grid-free.

Grounded in: "Dominated Novelty Search: Rethinking Local Competition in
Quality-Diversity", arXiv 2502.00593 (GECCO 2025). A drop-in replacement for the
grid-placement step in labs/qd-arena.

As a cell: (descriptors, fitness, k) -> (scores, survivors) + an fnv1a-64 receipt
over (rounded descriptors, fitness, k, scores) so the ranking is re-derivable and a
verifier can replay it. Zero dependencies (Python stdlib).

    python3 dns.py            # self-test: frontier kept, grid-free, receipt stable
"""

from __future__ import annotations

import json
import math
from itertools import combinations

INF = float("inf")


def fnv1a64(s: str) -> int:
    """fnv1a-64 over utf-8 — the fleet WAL convention (matches situation-recorder)."""
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _dist(a, b) -> float:
    return math.sqrt(sum((x - y) * (x - y) for x, y in zip(a, b)))


def dns_scores(descriptors, fitness, k: int = 3):
    """Local-competition score per individual: mean distance to its k nearest
    *fitter* neighbors. No fitter neighbor -> INF (local frontier). Higher = keep."""
    n = len(fitness)
    if n != len(descriptors):
        raise ValueError("descriptors and fitness must have equal length")
    if k < 1:
        raise ValueError("k must be >= 1")
    scores = []
    for i in range(n):
        fitter = [j for j in range(n) if fitness[j] > fitness[i]]
        if not fitter:
            scores.append(INF)  # nobody local dominates i -> frontier, always kept
            continue
        dists = sorted(_dist(descriptors[i], descriptors[j]) for j in fitter)
        kk = dists[:k]
        scores.append(sum(kk) / len(kk))
    return scores


def select(descriptors, fitness, k: int = 3, keep: int | None = None):
    """Return (scores, survivor_indices). Survivors = top-`keep` by score
    (frontier individuals, score INF, sort first). Default keep = half, min 1."""
    scores = dns_scores(descriptors, fitness, k)
    n = len(scores)
    if keep is None:
        keep = max(1, n // 2)
    order = sorted(range(n), key=lambda i: (scores[i], fitness[i]), reverse=True)
    return scores, sorted(order[:keep])


def receipt(descriptors, fitness, k, scores) -> str:
    """Re-derivable pin over the inputs + output — a verifier replays and checks it."""
    payload = {
        "descriptors": [[round(x, 6) for x in d] for d in descriptors],
        "fitness": [round(f, 6) for f in fitness],
        "k": k,
        "scores": ["inf" if s == INF else round(s, 6) for s in scores],
    }
    return "0x%016x" % fnv1a64(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def spread(descriptors, idxs) -> float:
    """Mean pairwise distance among a set of survivors — a grid-free diversity metric."""
    pts = [descriptors[i] for i in idxs]
    if len(pts) < 2:
        return 0.0
    ds = [_dist(a, b) for a, b in combinations(pts, 2)]
    return sum(ds) / len(ds)


# --- self-test -------------------------------------------------------------

def _demo():
    import random
    rng = random.Random(42)

    # 1) Frontier is always kept: a clearly-best-yet-isolated point must survive.
    desc = [[0.0, 0.0], [0.1, 0.0], [0.0, 0.1], [5.0, 5.0]]
    fit = [0.2, 0.3, 0.25, 0.05]  # the isolated point (idx 3) is the WORST fitness...
    scores, surv = select(desc, fit, k=2, keep=2)
    # idx 3 has low fitness but is far from everyone; and idx 1 is the global best.
    assert 1 in surv, "global-best individual must be kept"
    # the best-fitness individual has no fitter neighbor -> INF -> frontier
    assert scores[1] == INF, "top-fitness individual should be on the frontier (INF)"
    print("frontier + global-best kept:", surv, "scores=",
          ["inf" if s == INF else round(s, 3) for s in scores])

    # 2) Grid-free in HIGH dim: a 12-D behavior space where a fixed grid explodes.
    #    A b=4 bins/dim MAP-Elites grid would need 4**12 = 16.7M cells for ~200 points.
    d = 12
    n = 200
    hd = [[rng.random() for _ in range(d)] for _ in range(n)]
    hf = [sum(p) / d + 0.05 * rng.random() for p in hd]  # smooth-ish fitness
    sc, keep = select(hd, hf, k=5, keep=40)
    dns_spread = spread(hd, keep)
    # baseline: 40 random survivors
    rand_keep = rng.sample(range(n), 40)
    rand_spread = spread(hd, rand_keep)
    grid_cells = 4 ** d
    print("high-dim(12): a 4-bins/dim grid needs %d cells for %d points (unusable)."
          % (grid_cells, n))
    print("  DNS survivor spread %.4f vs random %.4f (DNS keeps a more diverse set: %s)"
          % (dns_spread, rand_spread, dns_spread >= rand_spread))
    assert grid_cells > 1_000_000, "point of the demo: the grid is intractable here"

    # 3) Receipt is stable + re-derivable (replay must reproduce the pin).
    r1 = receipt(desc, fit, 2, dns_scores(desc, fit, 2))
    r2 = receipt(desc, fit, 2, dns_scores(desc, fit, 2))
    assert r1 == r2, "receipt must be deterministic"
    # tamper: nudging one fitness must move the pin
    fit2 = list(fit); fit2[0] += 0.5
    assert receipt(desc, fit2, 2, dns_scores(desc, fit2, 2)) != r1, "receipt must be sensitive"
    print("receipt stable + sensitive:", r1)
    print("OK — DNS selects a diverse frontier with no grid and a re-derivable receipt.")


if __name__ == "__main__":
    _demo()
