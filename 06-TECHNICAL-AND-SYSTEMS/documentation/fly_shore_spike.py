#!/usr/bin/env python3
"""
FLY-SHORE-SPIKE: does the worm's quilt pipeline (NQ-C1/C2 lens) survive a 460x bigger animal?
Pre-registered in docs/FLYWIRE-SHORE-SPIKE.md §1-§8 (commit precedes this run's execution).

Shore: right antennal lobe, neuropil token AL_R (reason booked §2).
Gates (locked §4): REPLICATE worm result = inter-cluster edges LIGHTER:
  G1 R<1 | G2 MWU(intra>inter) p<0.001 | G3 perm T=m_intra-m_inter p<0.001 | G4 >=8/10 bootstrap R<1
  FALSIFY = mirror image (R>1, MWU(inter>intra) p<0.001, >=8/10 boots R>1). Else INCONCLUSIVE.
Data: FlyWire v783, CC BY-NC 4.0 — Dorkenwald 2024 + Schlegel 2024 (+Buhmann 2021, Eckstein 2024);
      gs://flywire-data/codex/data/fafb/783. Shas booked in pre-reg §7.
Memory discipline: full 3.87M-row table NEVER materialized; gzip+csv stream passes only;
RAM-resident = AL id set + AL_R pair dict (+secondary induced dict) + pruned build graph + stat arrays.
"""
import csv, gzip, hashlib, json, os, resource, sys, time, tracemalloc
from collections import defaultdict
import numpy as np
import networkx as nx
from scipy.stats import mannwhitneyu

DIR = "/tmp/fly783"
CONNS = f"{DIR}/connections.csv.gz"
NAMES = f"{DIR}/names.csv.gz"
BOOKED_SHA = "d49dd692e59e153aa3c83f5257bfc0eff51247b86d7bb183386c6d1622c70fc9"
NEURONS_SHA = "6a6b3759e635f0f35a677d169052362131ec61d95f55919298b55c43fce4e719"
SHORE = "AL_R"
TAU, SEED, NPERM, RNG_BASE = 3, 42, 10_000, 20260903
T = {}

def tick(tag):
    T[tag] = time.perf_counter(); return T[tag]

def rss_mb():
    with open("/proc/self/status") as f:
        for ln in f:
            if ln.startswith("VmRSS"): return int(ln.split()[1]) / 1024
    return -1

def phase(tag, fn):
    t0 = time.perf_counter(); out = fn(); dt = time.perf_counter() - t0
    print(f"[PHASE {tag}] {dt:.1f}s wall, RSS now {rss_mb():.0f} MB, peak {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.0f} MB")
    return out

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

# ---------- pass 1: stream whole file; keep only AL_R rows + whole-animal counters ----------
def pass1():
    pairs, al_ids, nrow, ge3, selfloops, nshore = {}, set(), 0, 0, 0, 0
    with gzip.open(CONNS, "rt") as f:
        r = csv.reader(f); next(r)
        for pre, post, np_, sc, _nt in r:
            nrow += 1; sc = int(sc)
            if sc >= 3: ge3 += 1
            if np_ != SHORE: continue
            a, b = int(pre), int(post)
            nshore += 1
            al_ids.add(a); al_ids.add(b)
            if a == b: selfloops += 1; continue
            pairs[(a, b)] = pairs.get((a, b), 0) + sc
    return pairs, al_ids, nrow, ge3, selfloops, nshore

# ---------- pass 2: secondary cell — all edges among S from ANY neuropil ----------
def pass2(S):
    pairs, alpair_seen = defaultdict(int), 0
    with gzip.open(CONNS, "rt") as f:
        r = csv.reader(f); next(r)
        for pre, post, np_, sc, _nt in r:
            a, b = int(pre), int(post)
            if a in S and b in S:
                if a != b:
                    pairs[(a, b)] += int(sc)
                    if np_ == SHORE: alpair_seen += 1
    return dict(pairs), alpair_seen

# ---------- worm C2-exact build/stat machinery ----------
def build(pairs, tau):
    G = nx.Graph()
    for (u, v), w in pairs.items():
        if w < tau: continue
        if G.has_edge(u, v): G[u][v]["weight"] = max(G[u][v]["weight"], w)
        else: G.add_edge(u, v, weight=w)
    return G

def partition(G, seed=SEED):
    comms = nx.community.louvain_communities(G, weight="weight", seed=seed, resolution=1.0)
    return {n: i for i, c in enumerate(sorted(map(frozenset, comms), key=len, reverse=True)) for n in c}

def labvec(part):
    return np.array([part[n] for n in sorted(part)], dtype=np.int64)

def edge_arrays(pairs, part, min_w=1):
    idx = {n: i for i, n in enumerate(sorted(part))}
    us, vs, ws, raw = [], [], [], []
    for (u, v), w in pairs.items():
        if w < min_w or u not in idx or v not in idx: continue
        us.append(idx[u]); vs.append(idx[v]); ws.append(w); raw.append((u, v, w))
    return np.array(us), np.array(vs), np.array(ws, float), raw

def perm_run(ui, vi, w, labels, rng, reps=NPERM):
    lab = np.asarray(labels)
    same = lab[ui] == lab[vi]
    t_obs = np.median(w[~same]) - np.median(w[same])   # T = m_inter - m_intra (worm C2 form)
    cnt = 0
    for _ in range(reps):
        p = rng.permutation(lab)
        s = p[ui] == p[vi]
        if not s.any() or s.all(): continue
        if np.median(w[~s]) - np.median(w[s]) <= t_obs: cnt += 1  # one-sided LESS (inter lighter)
    return t_obs, (1 + cnt) / (reps + 1)

def stat_run(name, ui, vi, w, labels, run_idx, rng=None):
    lab = np.asarray(labels)
    same = lab[ui] == lab[vi]
    inter, intra = w[~same], w[same]
    ni, na = len(inter), len(intra)
    mi, ma = float(np.median(inter)), float(np.median(intra))
    R = mi / ma if ma > 0 else float("inf")
    U, p_rep = mannwhitneyu(intra, inter, alternative="greater")     # H1: intra heavier (replication dir)
    _, p_fal = mannwhitneyu(inter, intra, alternative="greater")     # H1: inter heavier (falsify dir)
    rb = 2.0 * U / (ni * na) - 1.0
    t_obs, pp = perm_run(ui, vi, w, lab, rng if rng is not None else np.random.default_rng(RNG_BASE + run_idx))
    print(f"[{name}] inter n={ni} med={mi:g} | intra n={na} med={ma:g} | R={R:.3f} | "
          f"MWU(intra>) p={p_rep:.3e} MWU(inter>) p={p_fal:.3e} rb={rb:+.3f} | perm(T=i-m) p={pp:.5f}")
    return {"name": name, "R": R, "mwu_rep_p": p_rep, "mwu_fal_p": p_fal, "perm_p": pp, "rb": rb,
            "n_inter": ni, "n_intra": na, "m_inter": mi, "m_intra": ma}

def main():
    print(f"== FLY-SHORE-SPIKE run {time.strftime('%Y-%m-%d %H:%M:%S %Z')} ==")
    s1 = sha(CONNS)
    if s1 != BOOKED_SHA: sys.exit(f"ABORT sha mismatch {s1}")
    print(f"connections.csv.gz sha256 OK ({s1[:16]}…) — matches pre-reg §7")

    pairs, S, nrow, ge3, loops, nshore = phase("pass1-stream", pass1)
    print(f"whole file: {nrow:,} rows streamed (ge3={ge3:,}) | shore {SHORE}: {nshore:,} rows, "
          f"{len(S):,} neurons, {len(pairs):,} unique directed pairs, {loops} self-loops dropped")
    S = set(S)

    # ---- build + cluster (worm lens) ----
    tracemalloc.start()
    G = phase("build-tau3", lambda: build(pairs, TAU))
    g_cur, g_peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    nodes, edges = G.number_of_nodes(), G.number_of_edges()
    t0 = time.perf_counter(); part = partition(G); t_louv = time.perf_counter() - t0
    k = len(set(part.values()))
    sizes = sorted((sum(1 for n in part if part[n] == c) for c in set(part.values())), reverse=True)
    print(f"tau={TAU} graph: {nodes:,} nodes {edges:,} edges | Louvain seed={SEED}: {k} clusters, "
          f"sizes {sizes[:12]}{'…' if len(sizes) > 12 else ''} ({t_louv:.2f}s)")
    print(f"graph mem (tracemalloc): current {g_cur/1e6:.1f} MB peak {g_peak/1e6:.1f} MB "
          f"-> {g_cur/max(edges,1):.0f} B/edge")

    # ---- primary statistic ----
    ui, vi, w, raw = edge_arrays(pairs, part)
    main_run = stat_run("PRIMARY all-w", ui, vi, w, labvec(part), 0)
    med_inter_n = main_run["n_inter"]; frac = med_inter_n / (med_inter_n + main_run["n_intra"])
    print(f"            thin-door density: {med_inter_n:,}/{med_inter_n+main_run['n_intra']:,} "
          f"({100*frac:.1f}%) of directed pairs cross a boundary (worm: 43.5%)")

    # ---- sensitivity: tau=5 stat subset + tau=5 rebuild (non-gating) ----
    stat_run("SENS w>=5 subset", *edge_arrays(pairs, part, min_w=5)[:3], labvec(part), 1)
    G5 = build(pairs, 5); part5 = partition(G5)
    stat_run(f"SENS tau=5 rebuild ({G5.number_of_nodes()}n/{G5.number_of_edges()}e/{len(set(part5.values()))}k)",
             *edge_arrays(pairs, part5)[:3], labvec(part5), 2)

    # ---- hub-blind ----
    deg = sorted(G.degree(), key=lambda kv: (-kv[1], kv[0]))[:5]
    hubs = [n for n, _ in deg]
    print(f"top-5 hubs (build-graph degree): {deg}")
    keep = np.array([i for i, (u, v, _) in enumerate(raw) if u not in hubs and v not in hubs])
    hub_run = stat_run("HUB-BLIND -top5", ui[keep], vi[keep], w[keep], labvec(part), 3)

    # ---- bootstrap: 10 seeds ----
    from sklearn.metrics import adjusted_rand_score
    boots, nR1, okp = [], 0, 0
    ref = labvec(part)
    for s in range(1, 11):
        bp = partition(G, seed=s)
        ns = sorted(set(part) & set(bp))
        a = adjusted_rand_score([part[n] for n in ns], [bp[n] for n in ns])
        r = stat_run(f"BOOT seed={s:02d} ARI={a:.2f}", *edge_arrays(pairs, bp)[:3], labvec(bp), 10 + s)
        r["ari"] = float(a); boots.append(r)
        if r["R"] < 1: nR1 += 1
        if r["perm_p"] < 0.001: okp += 1
    print(f"bootstrap: R<1 in {nR1}/10 | perm p<0.001 in {okp}/10 | "
          f"R range {min(b['R'] for b in boots):.3f}..{max(b['R'] for b in boots):.3f}")

    # ---- biggest-wire audit (pre-reg §5) ----
    order = sorted(((u, v, wt) for (u, v), wt in pairs.items() if wt >= TAU), key=lambda x: -x[2])[:12]
    idx_names = {}
    if os.path.exists(NAMES):
        with gzip.open(NAMES, "rt") as f:
            r = csv.reader(f); hdr = next(r)
            i_id = 0 if hdr[0].lower().startswith("root") else None
            i_nm = next((i for i, h in enumerate(hdr) if h.lower() in ("name", "labels", "user_name")), None)
            if i_id is not None and i_nm is not None:
                for row in r:
                    try: idx_names[int(row[i_id])] = row[i_nm]
                    except (ValueError, IndexError): pass
    print("-- biggest-wire audit: top-12 heaviest directed pairs (tau>=3) --")
    n_intra_top = 0
    for u, v, wt in order:
        same = part.get(u) is not None and part.get(u) == part.get(v)
        n_intra_top += same
        nm = lambda x: idx_names.get(x, str(x))
        print(f"  {nm(u)} -> {nm(v)}  w={wt}  {'INTRA' if same else 'INTER'} (C{part.get(u, -1)}->C{part.get(v, -1)})")
    print(f"  intra among top-12: {n_intra_top}/12 (worm: 12/12; replicate gate >=10/12)")

    # ---- degree distribution (descriptive) ----
    din = defaultdict(int); dout = defaultdict(int)
    for (a, b), wt in pairs.items():
        if wt >= TAU: dout[a] += 1; din[b] += 1
    slopes = {}
    for tag, d in (("in", din), ("out", dout)):
        ks = np.array(sorted(d.values()))
        hh = np.bincount(ks)
        x = np.nonzero(hh)[0]; y = hh[x]
        m = x > 0
        sl = float(np.polyfit(np.log10(x[m]), np.log10(y[m]), 1)[0])
        slopes[tag] = sl
        print(f"degree[{tag}]: n={len(d):,} max={ks.max()} median={np.median(ks):.0f} "
              f"log-log slope={sl:.2f} (descriptive only)")

    # ---- secondary: whole-wiring induced subgraph (non-gating) ----
    sec_pairs, alseen = phase("pass2-induced", lambda: pass2(S))
    ext = len(sec_pairs) - len(pairs)
    print(f"secondary induced: {len(sec_pairs):,} pairs among S ({ext:,} extra-animal-wiring beyond {SHORE}; "
          f"{alseen:,} AL_R rows re-seen)")
    sec_run = stat_run("SECONDARY whole-wiring", *edge_arrays(sec_pairs, part)[:3], labvec(part), 30)

    # ---- gates ----
    g = ("REPLICATED" if main_run["R"] < 1 and main_run["mwu_rep_p"] < 0.001 and main_run["perm_p"] < 0.001
         and nR1 >= 8 else
         "FALSIFIED" if main_run["R"] > 1 and main_run["mwu_fal_p"] < 0.001 and nR1 <= 2 else "INCONCLUSIVE")
    notes = []
    if g == "REPLICATED" and not (hub_run["mwu_rep_p"] < 0.001 and hub_run["R"] < 1):
        g = "WEAKLY-REPLICATED"; notes.append("hub-driven (hub-blind failed)")
    if g == "REPLICATED" and n_intra_top < 10: notes.append(f"biggest-wire audit missed: {n_intra_top}/12 intra")
    print(f"\n== VERDICT: {g}" + (f" — {'; '.join(notes)}" if notes else "") + " ==")

    # ---- extrapolation (pre-reg §6) ----
    t0 = time.perf_counter(); perm_run(ui[:2000], vi[:2000], w[:2000], labvec(part), np.random.default_rng(7), reps=100)
    t_perm100 = (time.perf_counter() - t0) / 100  # s per shuffle at 2,000 edges
    dedup = len(pairs) / max(nshore - loops, 1)   # unique pairs / raw rows (upper-bound factor for E_full)
    E_full = int(ge3 * dedup)                      # upper bound: cross-neuropil merges only shrink it
    bpe = g_cur / max(edges, 1)
    ram_full = bpe * E_full * 1.2  # 20% headroom, booked
    louv_full = t_louv * (E_full / edges) ** 1.1
    cell_hr = t_perm100 * (E_full / 2000) * NPERM / 3600  # hours per stat cell, single-core
    print(f"\n-- extrapolation to full animal (V=139,255; tau>=3 rows={ge3:,}) --")
    print(f"measured: {nshore:,} shore rows -> {len(pairs):,} unique pairs (dedup {dedup:.3f}), "
          f"{bpe:.0f} B/edge nx, louvain {t_louv:.2f}s @ {edges:,}e, {t_perm100*1e6:.0f} us/shuffle @ 2,000e")
    print(f"full-animal est: E<=~{E_full:,} unique pruned pairs (upper bound) | nx graph ~{ram_full/1e9:.1f} GB | "
          f"Louvain ~{louv_full/60:.0f} min | 10k-perm stat cell ~{cell_hr*60:.0f} min single-core "
          f"(13 cells; parallel over {os.cpu_count()} cores -> ~{cell_hr*13*60/max(os.cpu_count(),1):.0f} min wall)")
    print(f"peak RSS this run: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.0f} MB")

    json.dump({"verdict": g, "notes": notes, "main": main_run, "hub": hub_run, "secondary": sec_run,
               "boots": [{k: b[k] for k in ('name','R','perm_p','ari')} for b in boots],
               "nR1": nR1, "top12_intra": n_intra_top, "slopes": slopes,
               "shore": {"neurons": len(S), "pairs": len(pairs), "graph_nodes": nodes, "graph_edges": edges,
                         "clusters": k, "sizes": sizes},
               "extrap": {"E_full": E_full, "dedup": dedup, "ram_GB": ram_full/1e9, "louv_min": louv_full/60,
                          "cell_hr": cell_hr, "B_per_edge": bpe}},
              open("/tmp/fly_shore_summary.json", "w"), indent=1)

if __name__ == "__main__":
    main()
