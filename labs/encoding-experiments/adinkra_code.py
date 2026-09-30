"""E10 adinkra_code — the supersymmetry Adinkra IS a code; decode errors by walking its edges.

Gem: adinkra-math-pypi (`supersymmetry.create_adinkra`, `verify_chromotopology`). Its
rank-N construction links boson B_i to fermion F_{(i xor 2^j) mod 2^(N-1)} with colour j.

Known mathematics, re-derived and MEASURED here (not a new result: Doran, Faux, Gates,
Hübsch, Iga, Landweber showed Adinkras are N-cubes quotiented by doubly-even binary codes):
  1. adinkra-math's rank-N Adinkra is isomorphic to the N-cube, bipartitioned by parity:
     boson/fermion statistics == even/odd parity, one supersymmetry generator == one bit flip.
  2. Quotient the 8-cube by the doubly-even extended Hamming code e8 = [8,4,4]: 16 nodes
     (8 bosons + 8 fermions), still a valid chromotopology. Each node is a SYNDROME class.
  3. Decoding by adjacency: a received word's node is either the origin (no error), one
     colour-j edge from the origin (single error at bit j: correct it), or further (detect).

Run: python3 adinkra_code.py [--selftest]
"""
from __future__ import annotations
import itertools, sys
import common as C


def create_adinkra(rank):  # verbatim construction from adinkra-math (labels as ints)
    half = 1 << (rank - 1)
    return [(("B", i), ("F", (i ^ (1 << j)) % half), j) for i in range(half) for j in range(rank)]


def adjacency(edges):
    adj = {}
    for a, b, g in edges:
        adj.setdefault(a, []).append((b, g))
        adj.setdefault(b, []).append((a, g))
    return adj


def chromotopology_ok(edges, rank):
    adj = adjacency(edges)
    for node, nb in adj.items():
        if sorted(g for _, g in nb) != list(range(rank)):
            return False
        if any(node[0] == m[0] for m, _ in nb):
            return False
    step = {(n, g): m for n, nb in adj.items() for m, g in nb}
    for n in adj:  # every 2-colour walk i,j,i,j closes after 4 steps
        for i, j in itertools.combinations(range(rank), 2):
            x = n
            for g in (i, j, i, j):
                x = step[(x, g)]
            if x != n:
                return False
    return True


def cube_iso(rank):
    """Explicit isomorphism adinkra-math rank-N -> N-cube: B_i -> (i, 0); F_k -> (k, 1) in
    the basis where colour j<N-1 flips bits j and N-1, colour N-1 flips bit N-1."""
    edges = create_adinkra(rank)
    top = 1 << (rank - 1)
    vid = lambda node: node[1] | (top if node[0] == "F" else 0)
    ok = True
    for a, b, g in edges:
        flip = top | (1 << g) if g < rank - 1 else top
        ok &= (vid(a) ^ vid(b)) == flip
    return ok and len({vid(n) for e in edges for n in e[:2]}) == 2 ** rank


# ---------------- e8 = extended Hamming [8,4,4] (doubly even) ------------------------------------
G8 = [0b11110000, 0b11001100, 0b10101010, 0b11111111]


def span(gens):
    out = {0}
    for g in gens:
        out |= {x ^ g for x in out}
    return sorted(out)


E8 = span(G8)


def coset_rep(x):
    return min(x ^ c for c in E8)


def quotient_adinkra(n=8):
    reps = sorted({coset_rep(x) for x in range(1 << n)})
    edges = set()
    for r in reps:
        if bin(r).count("1") % 2 == 0:  # boson = even weight (e8 is even, so parity is well defined)
            for j in range(n):
                edges.add((("B", r), ("F", coset_rep(r ^ (1 << j))), j))
    return reps, sorted(edges)


def decode(received, adj):
    """Walk the quotient Adinkra: origin -> clean; origin one colour-j edge away -> flip bit j."""
    node = ("B" if bin(received).count("1") % 2 == 0 else "F", coset_rep(received))
    origin = ("B", 0)
    if node == origin:
        return received, "clean"
    for m, g in adj[node]:
        if m == origin:
            return received ^ (1 << g), "corrected"
    return None, "detected"


def encode4(d):
    x = 0
    for k in range(4):
        if (d >> k) & 1:
            x ^= G8[k]
    return x


def measure(log=print):
    res = {"cube_iso": {N: cube_iso(N) for N in range(1, 9)},
           "chromotopology": {N: chromotopology_ok(create_adinkra(N), N) for N in range(1, 9)}}
    reps, edges = quotient_adinkra()
    adj = adjacency(edges)
    res["quotient"] = {"nodes": len(reps), "bosons": sum(1 for r in reps if bin(r).count("1") % 2 == 0),
                       "valid_chromotopology": chromotopology_ok(edges, 8), "e8_codewords": len(E8),
                       "e8_min_weight": min(bin(c).count("1") for c in E8 if c)}
    tallies = {1: {}, 2: {}, 3: {}}
    for d in range(16):
        cw = encode4(d)
        for w in (1, 2, 3):
            for bits in itertools.combinations(range(8), w):
                e = sum(1 << b for b in bits)
                out, status = decode(cw ^ e, adj)
                key = status if status != "corrected" or out == cw else "MIScorrected"
                tallies[w][key] = tallies[w].get(key, 0) + 1
    res["decode"] = tallies
    log(f"  adinkra-math rank N=1..8 isomorphic to the N-cube: {all(res['cube_iso'].values())}; chromotopology valid: {all(res['chromotopology'].values())}")
    log(f"  8-cube / e8 quotient: {res['quotient']}")
    log(f"  decode-by-walking-the-graph over all 16 codewords: 1-bit {tallies[1]}, 2-bit {tallies[2]}, 3-bit {tallies[3]}")
    return res


def selftest():
    c = C.Checks()
    for N in range(1, 7):
        c.ok(chromotopology_ok(create_adinkra(N), N), f"adinkra-math rank {N} valid")
        c.ok(cube_iso(N), f"rank {N} is the {N}-cube")
    c.ok(len(E8) == 16 and all(bin(x).count("1") % 4 == 0 for x in E8), "e8 is doubly even, 16 words")
    reps, edges = quotient_adinkra()
    c.ok(len(reps) == 16, "quotient has 16 nodes")
    c.ok(chromotopology_ok(edges, 8), "quotient chromotopology valid")
    m = measure(log=lambda *a: None)
    c.ok(m["decode"][1] == {"corrected": 128}, "every single error corrected")
    c.ok(m["decode"][2] == {"detected": 16 * 28}, "every double error detected")
    return c.report("adinkra_code")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E10 adinkra_code")
    res = measure()
    with open(C.HERE + "/results_adinkra_code.json", "w") as f:
        json.dump(res, f, indent=1, default=str)
