#!/usr/bin/env python3
"""
NQ-C2 shore-spike: are inter-cluster edges systematically stronger than intra-cluster
edges in the C. elegans chemical synapse graph?
Pre-registered in docs/NQ-C2-edges-as-channels.md (commit bd89fd14 precedes this run).

GATES (locked in pre-reg §3):
  PASS    perm p < 0.001 AND R = m_inter/m_intra >= 2.0          -> edges are channels
  PARTIAL perm p < 0.001 but R < 2.0                              -> edges lean outward, weakly
  FAIL    perm p >= 0.001                                          -> book honestly
Downgrades: hub-blind (§3.2), >=5/20 bootstrap inversions R<1 (§3.4). One notch each.
Bonus EJ cell (§3.5): exploratory, never gates.
Provenance: raw sha256 MUST equal NQ-C1's booked hash (no re-download); partition rebuild
MUST reproduce /tmp/nq_c1_constraint_table.json cluster sets exactly, else ABORT.
"""
import hashlib, itertools, json, os, sys, urllib.request
import numpy as np
import networkx as nx
import xlrd
from scipy.stats import mannwhitneyu
from sklearn.metrics import adjusted_rand_score

RAW = "/tmp/NeuronConnect.xls"
URL = "https://www.wormatlas.org/images/NeuronConnect.xls"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}  # wormatlas drops default curl UA (C1 scar)
BOOKED_SHA = "120c2c6332050a2d1494c19c687f447ed65620ad0db5f8b732189aa10e5162f1"
C1_TABLE = "/tmp/nq_c1_constraint_table.json"
TAU = 3
SEED = 42          # NQ-C1's booked Louvain seed
NPERM = 10_000
RNG_BASE = 20260903  # booked in pre-reg §2

def fetch():
    if not os.path.exists(RAW):
        req = urllib.request.Request(URL, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as r, open(RAW, "wb") as f:
            f.write(r.read())
    return hashlib.sha256(open(RAW, "rb").read()).hexdigest()

def edges():
    """Identical ingest to nq_c1_spike.py. chem[(a,b)]=summed S/Sp count; gap: frozenset->summed Nbr."""
    sh = xlrd.open_workbook(RAW).sheet_by_index(0)
    chem, gap = {}, {}
    for r in range(1, sh.nrows):
        a, b, t = sh.cell_value(r,0), sh.cell_value(r,1), sh.cell_value(r,2)
        n = int(sh.cell_value(r,3) or 0)
        if a == b: continue
        if t in ("S", "Sp"):
            chem[(a,b)] = chem.get((a,b), 0) + n
        elif t == "EJ":
            k = frozenset((a,b)); gap[k] = gap.get(k, 0) + max(n, 1)  # EJ row exists -> >=1 junction (booked §3.5)
    return chem, gap

def build(chem, gap, tau):
    G = nx.Graph()  # C1 exact: symmetrized max(w) chem w>=tau + EJ weight-1
    for (u, v), w in chem.items():
        if w < tau: continue
        if G.has_edge(u, v): G[u][v]["weight"] = max(G[u][v]["weight"], w)
        else: G.add_edge(u, v, weight=w)
    for e in gap:
        a, b = tuple(e)
        if not G.has_edge(a, b): G.add_edge(a, b, weight=1)
    return G

def partition(G, seed=SEED, resolution=1.0):
    comms = nx.community.louvain_communities(G, weight="weight", seed=seed, resolution=resolution)
    return {n: i for i, c in enumerate(sorted(map(frozenset, comms), key=len, reverse=True)) for n in c}

def labvec(part):
    """Label vector ALIGNED to sorted(part) — the index space edge_arrays emits.
    (Bug scar 2026-09-03: first run passed list(part.values()) — dict insertion order —
    silently permuting the classification; caught by post-hoc cross-check.)"""
    return np.array([part[n] for n in sorted(part)])

def edge_arrays(chem, part, min_w=1):
    """Directed chem pairs, both endpoints in partition, weight>=min_w."""
    us, vs, ws = [], [], []
    for (u, v), w in chem.items():
        if w < min_w: continue
        cu, cv = part.get(u), part.get(v)
        if cu is None or cv is None: continue
        us.append(u); vs.append(v); ws.append(w)
    idx = {n: i for i, n in enumerate(sorted(part))}
    return (np.array([idx[u] for u in us]), np.array([idx[v] for v in vs]),
            np.array(ws, dtype=float), us, vs)

def perm_test(ui, vi, w, labels, rng):
    """10k label-shuffles; T = m_inter - m_intra; one-sided p (pre-reg §2)."""
    lab = np.array(labels)
    same = lab[ui] == lab[vi]
    mi, ma = np.median(w[~same]), np.median(w[same])
    t_obs = mi - ma
    cnt = 0
    for _ in range(NPERM):
        p = rng.permutation(lab)
        s = p[ui] == p[vi]
        if not s.any() or s.all(): continue
        if np.median(w[~s]) - np.median(w[s]) >= t_obs: cnt += 1
    return t_obs, (1 + cnt) / (NPERM + 1)

def stat_run(name, ui, vi, w, labels, run_idx):
    """Full §2 statistic block; returns dict, prints receipt lines."""
    lab = np.array(labels)
    same = lab[ui] == lab[vi]
    inter, intra = w[~same], w[same]
    ni, na = len(inter), len(intra)
    mi, ma = float(np.median(inter)), float(np.median(intra))
    R = mi / ma if ma > 0 else float("inf")
    U, pu = mannwhitneyu(inter, intra, alternative="greater", method="asymptotic")
    rb = 2.0 * U / (ni * na) - 1.0
    t_obs, pp = perm_test(ui, vi, w, labels, np.random.default_rng(RNG_BASE + run_idx))
    print(f"[{name}] inter n={ni} median={mi:g} | intra n={na} median={ma:g} | R={R:.3f} | "
          f"MWU U={U:.0f} p={pu:.3e} rank-biserial={rb:+.3f} | perm T={t_obs:+.1f} p={pp:.5f}")
    return {"name": name, "R": R, "mwu_p": pu, "perm_p": pp, "rank_biserial": rb,
            "n_inter": ni, "n_intra": na, "m_inter": mi, "m_intra": ma}

def main():
    sha = fetch()
    if sha != BOOKED_SHA:
        sys.exit(f"ABORT: raw sha {sha} != booked {BOOKED_SHA} — provenance broken, no run.")
    print(f"raw sha256 OK = {sha} (matches NQ-C1 booking; no re-download)")

    chem, gap = edges()
    G = build(chem, gap, TAU)
    part = partition(G)
    print(f"tau={TAU} rebuild: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, "
          f"{len(set(part.values()))} clusters (seed={SEED})")

    # provenance check vs C1's cached constraint table — load-bearing (pre-reg §1)
    if os.path.exists(C1_TABLE):
        c1 = json.load(open(C1_TABLE))
        rebuilt = {frozenset(v) for v in c1["clusters"].values()}
        mine = {frozenset(n for n in part if part[n] == c) for c in set(part.values())}
        if rebuilt != mine:
            sys.exit("ABORT: rebuilt partition != NQ-C1 constraint table clusters — lens mismatch, no run.")
        print("partition reproduces /tmp/nq_c1_constraint_table.json cluster sets EXACTLY — lens verified")
        c1_part = {n: int(k[1:]) for k, v in c1["clusters"].items() for n in v}
    else:
        print("WARN: C1 constraint table absent — cannot cross-verify lens (continuing, booked)")
        c1_part = None
    sizes = sorted((sum(1 for n in part if part[n] == c) for c in set(part.values())), reverse=True)
    print(f"cluster sizes: {sizes}")

    # ---- primary (§2) ----
    ui, vi, w, us, vs = edge_arrays(chem, part)
    main_run = stat_run("PRIMARY all-weights", ui, vi, w, labvec(part), 0)

    # ---- sensitivity (§3.3, non-gating) ----
    ui3, vi3, w3, _, _ = edge_arrays(chem, part, min_w=TAU)
    stat_run("SENSITIVITY w>=3", ui3, vi3, w3, labvec(part), 1)

    # ---- hub-blind (§3.2) ----
    deg = sorted(G.degree(), key=lambda kv: (-kv[1], kv[0]))[:5]
    hubs = [n for n, d in deg]
    print(f"top-5 hubs (degree, build graph): {[(n, d) for n, d in deg]}")
    keep = [i for i, (u, v) in enumerate(zip(us, vs)) if u not in hubs and v not in hubs]
    hub_run = stat_run("HUB-BLIND minus top-5", ui[keep], vi[keep], w[keep], labvec(part), 2)

    # ---- bootstrap churn bound (§3.4) ----
    print("\n-- 20 bootstrap re-clusterings, tau=3, seeds 1..20 --")
    boots, n_invert = [], 0
    nodes_sorted = sorted(part)
    for s in range(1, 21):
        bp = partition(G, seed=s)
        if c1_part is not None:
            ns = [n for n in nodes_sorted if n in bp and n in c1_part]
            a = adjusted_rand_score([c1_part[n] for n in ns], [bp[n] for n in ns])
        else:
            a = float("nan")
        b = edge_arrays(chem, bp)[0:3]
        r = stat_run(f"BOOT seed={s:02d} ARI={a:.2f}", *b, labvec(bp), 2 + s)
        r["ari"] = a; boots.append(r)
        if r["R"] < 1: n_invert += 1
    Rs = [b["R"] for b in boots]
    ok_p = sum(1 for b in boots if b["perm_p"] < 0.001)
    print(f"bootstrap R: min={min(Rs):.3f} median={float(np.median(Rs)):.3f} max={max(Rs):.3f} | "
          f"inversions R<1: {n_invert}/20 | perm p<0.001 in {ok_p}/20")

    # ---- gates + downgrades (§3.1, 3.2, 3.4) ----
    if main_run["perm_p"] < 0.001 and main_run["R"] >= 2.0:   g, notes = "PASS", []
    elif main_run["perm_p"] < 0.001:                          g, notes = "PARTIAL", []
    else:                                                     g, notes = "FAIL", []
    if g != "FAIL":
        if g == "PASS" and not (hub_run["perm_p"] < 0.001 and hub_run["R"] >= 2.0):
            g, _ = "PARTIAL", notes.append("hub-driven (hub-blind failed gate §3.2)")
        elif g == "PARTIAL" and not (hub_run["perm_p"] < 0.001):
            g, _ = "FAIL", notes.append("PARTIAL died at hub-blind §3.2")
        if g != "FAIL" and n_invert >= 5:
            g = "PARTIAL" if g == "PASS" else "FAIL"
            notes.append(f"seed-luck: {n_invert}/20 bootstrap inversions (§3.4)")
    print(f"\n== VERDICT: {g}" + (f" — {'; '.join(notes)}" if notes else "") + " ==")
    if g == "PARTIAL": print("== booked words: edges lean outward, weakly — gradient, not channel ==")
    if g == "FAIL":    print("== connectome thread closes with two kills — still a result ==")

    # ---- bonus cell: gap junctions (§3.5, exploratory, never gates) ----
    print("\n-- BONUS (exploratory, no gate): gap-junction network --")
    idx = {n: i for i, n in enumerate(sorted(part))}
    gus, gvs, gws = [], [], []
    for e, wt in gap.items():
        a, b = sorted(e)
        if a in idx and b in idx:
            gus.append(idx[a]); gvs.append(idx[b]); gws.append(float(wt))
    stat_run("BONUS EJ gap junctions", np.array(gus), np.array(gvs), np.array(gws),
             labvec(part), 40)

if __name__ == "__main__":
    main()
