"""E5 godel_cellgraph — Gödel-number a situation cell-graph into ONE integer, and back.

Gem: Gödel numbering (godel-number was named in the brief but is not reachable at
SuperInstance/godel-number on master/main; this implements the classical scheme).

Graph: labs/situation-recorder/example_situation.jsonl — 8 real cells (TASK, ROUTE,
DRAFT, DRAW, FOLD, DROP, MARK, OUTCOME) whose `refs` point at earlier cells by hash.

Encoding (two squarefree/prime-power parts, multiplied):
  labels   prod_i  p_i ^ (rel_code_i + 1)        p_i = i-th prime       (sequence part)
  edges    prod_{(i->j)}  q_{pair(i,j)}          one prime per possible ordered pair j<i
Decoding: trial-divide by the known primes -> exact labels and edge set.

What it buys (MEASURED): edge-set algebra becomes integer algebra —
  H is a sub-graph of G  <=>  G_edges % H_edges == 0
  merge (union)          =    lcm(G, H)        common core = gcd(G, H)
What it costs (MEASURED): size, vs a varint adjacency list, as graphs grow.

Run: python3 godel_cellgraph.py [--selftest]
"""
from __future__ import annotations
import json, math, os, sys, time
import common as C

RELS = ["TASK", "ROUTE", "DRAFT", "DRAW", "FOLD", "KEEP", "DROP", "MARK", "OUTCOME"]


def primes(n):
    lim = max(16, int(n * (math.log(n + 2) + math.log(math.log(n + 3)) + 3)))
    sieve = bytearray([1]) * (lim + 1)
    sieve[0:2] = b"\0\0"
    for k in range(2, int(lim ** 0.5) + 1):
        if sieve[k]:
            sieve[k * k::k] = bytearray(len(sieve[k * k::k]))
    return [k for k in range(lim + 1) if sieve[k]][:n]


def pair_index(i, j):  # edge i -> j with j < i, dense index over the lower triangle
    return i * (i - 1) // 2 + j


def load_graph():
    p = os.path.join(C.HERE, "..", "situation-recorder", "example_situation.jsonl")
    recs = [json.loads(l) for l in open(p, encoding="utf-8")]
    idx = {r["hash"]: i for i, r in enumerate(recs)}
    labels = [RELS.index(r["rel"]) for r in recs]
    edges = sorted((i, idx[h]) for i, r in enumerate(recs) for h in r["refs"])
    return labels, edges


class Godel:
    def __init__(self, max_nodes):
        self.n = max_nodes
        self.P = primes(max_nodes + max_nodes * (max_nodes - 1) // 2)
        self.node_p = self.P[:max_nodes]
        self.edge_p = self.P[max_nodes:]

    def edges_int(self, edges):
        g = 1
        for i, j in edges:
            g *= self.edge_p[pair_index(i, j)]
        return g

    def encode(self, labels, edges):
        g = 1
        for i, l in enumerate(labels):
            g *= self.node_p[i] ** (l + 1)
        return g * self.edges_int(edges)

    def decode(self, g):
        labels = []
        for p in self.node_p:
            e = 0
            while g % p == 0:
                g //= p
                e += 1
            if e == 0:
                break
            labels.append(e - 1)
        edges = []
        for i in range(1, len(labels)):
            for j in range(i):
                q = self.edge_p[pair_index(i, j)]
                if g % q == 0:
                    g //= q
                    edges.append((i, j))
        assert g == 1, "residue after factoring"
        return labels, sorted(edges)


def varint_adjacency(labels, edges):
    """The boring baseline: n, then per node (label, #refs, refs as back-distances)."""
    out = bytearray(C.varint(len(labels)))
    by = {i: [] for i in range(len(labels))}
    for i, j in edges:
        by[i].append(j)
    for i, l in enumerate(labels):
        out += C.varint(l) + C.varint(len(by[i])) + b"".join(C.varint(i - j) for j in sorted(by[i]))
    return bytes(out)


def synth_graph(n, r):
    labels = [r.randint(0, len(RELS) - 1) for _ in range(n)]
    edges = set()
    for i in range(1, n):
        for _ in range(r.randint(1, 2)):
            back = min(i, 1 + int(abs(r.gauss()) * 3))  # mostly-local refs, like a transcript
            edges.add((i, i - back))
    return labels, sorted(edges)


def measure(log=print):
    labels, edges = load_graph()
    G = Godel(len(labels))
    g = G.encode(labels, edges)
    back = G.decode(g)
    canon_bytes = len(C.canon({"labels": [RELS[l] for l in labels], "edges": edges}).encode())
    res = {"real": {"nodes": len(labels), "edges": len(edges), "godel_bits": g.bit_length(),
                    "godel_decimal_digits": len(str(g)), "varint_adj_bytes": len(varint_adjacency(labels, edges)),
                    "canon_json_bytes": canon_bytes, "roundtrip": back == (labels, edges)}}
    log(f"  real situation graph: {len(labels)} cells, {len(edges)} refs -> Gödel number of {g.bit_length()} bits "
        f"({len(str(g))} decimal digits); varint adjacency {res['real']['varint_adj_bytes']} B; canonical JSON {canon_bytes} B; round-trip {res['real']['roundtrip']}")
    log(f"  G = {g}")
    # algebra: sub-graph test by divisibility, merge by lcm, core by gcd
    Ge = G.edges_int(edges)
    sub = G.edges_int(edges[:3])
    other = G.edges_int(edges[2:] + [(7, 0)])
    res["algebra"] = {"sub_divides": Ge % sub == 0, "non_sub_divides": Ge % G.edges_int([(7, 0)]) == 0,
                      "lcm_is_union": math.lcm(Ge, other) == G.edges_int(sorted(set(edges) | set(edges[2:] + [(7, 0)]))),
                      "gcd_is_intersection": math.gcd(Ge, other) == G.edges_int(sorted(set(edges) & set(edges[2:] + [(7, 0)])))}
    log("  algebra: " + ", ".join(f"{k}={v}" for k, v in res["algebra"].items()))
    # growth
    r = C.Rng(12)
    grow = {}
    for n in (8, 16, 32, 64, 128, 256):
        lb, ed = synth_graph(n, r)
        Gn = Godel(n)
        t0 = time.time()
        gn = Gn.encode(lb, ed)
        t_enc = time.time() - t0
        t0 = time.time()
        ok = Gn.decode(gn) == (lb, ed)
        t_dec = time.time() - t0
        va = len(varint_adjacency(lb, ed))
        grow[n] = {"edges": len(ed), "godel_bytes": (gn.bit_length() + 7) // 8, "varint_bytes": va,
                   "ratio": round(((gn.bit_length() + 7) // 8) / va, 2), "enc_ms": round(1000 * t_enc, 1),
                   "dec_ms": round(1000 * t_dec, 1), "roundtrip": ok}
    res["growth"] = grow
    log("  growth (Gödel bytes / varint-adjacency bytes): " + ", ".join(f"n={n}: {v['godel_bytes']}/{v['varint_bytes']} = {v['ratio']}x (dec {v['dec_ms']} ms)" for n, v in grow.items()))
    return res


def selftest():
    c = C.Checks()
    c.ok(primes(6) == [2, 3, 5, 7, 11, 13], "primes")
    labels, edges = load_graph()
    c.ok(len(labels) == 8 and len(edges) >= 7, "real graph loaded")
    G = Godel(len(labels))
    g = G.encode(labels, edges)
    c.ok(G.decode(g) == (labels, edges), "real graph round-trips through one integer")
    c.ok(G.encode(labels, edges[:-1]) != g, "dropping an edge changes the number")
    Ge = G.edges_int(edges)
    for k in range(1, len(edges) + 1):
        c.ok(Ge % G.edges_int(edges[:k]) == 0, f"prefix sub-graph {k} divides")
    c.ok(Ge % G.edges_int([(7, 0)]) != 0 or (7, 0) in edges, "absent edge does not divide")
    r = C.Rng(4)
    for n in (5, 12, 30):
        lb, ed = synth_graph(n, r)
        Gn = Godel(n)
        c.ok(Gn.decode(Gn.encode(lb, ed)) == (lb, ed), f"synthetic n={n} round-trip")
    return c.report("godel_cellgraph")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    print("E5 godel_cellgraph")
    res = measure()
    with open(C.HERE + "/results_godel_cellgraph.json", "w") as f:
        json.dump(res, f, indent=1, default=str)
