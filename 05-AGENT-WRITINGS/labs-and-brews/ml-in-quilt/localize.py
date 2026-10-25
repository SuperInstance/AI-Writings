"""Perturbation-localization control — recover the cell dependency graph from digests alone.

Sibling receipt: the cellgraph repo perturbs one weight and watches which cells' digests move
first (Wq->14 cells, Wv->12, Wlog->2). Our architecture doc *asserted* that faults localize;
this module is the control. It uses ONLY the per-cell activation digests a Stream already
logs (the `out` field of each cell.tick, plus the per-layer KV chain heads). It never looks at
which weight it touched when deciding what moved.

Method: run the prompt once (baseline), copy the model, add EPS to one element of one weight
tensor, run again, and compare digests cell by cell in execution order.
  first  = the earliest cell (execution order) whose output digest moved
  moved  = every cell whose output digest moved
Expected values come from a DECLARED graph (CONSUMER + execution order), written down from the
architecture, not derived from the digests. The check is that the two agree.

Honest shape of the toy: the residual stream makes the forward pass one chain, so the moved
set is always a suffix of the execution order; what localization pins down is *where the
suffix starts* (the direct consumer) and, through the KV chains, which layers' caches changed.
"""

from __future__ import annotations

import copy

import cellml as C  # noqa: E402  (sets sys.path for activeledger)
import activeledger as al  # noqa: E402

EPS = 1e-9
PROMPT = "the cat sat on the "


def cell_order(layers: int) -> list[str]:
    out = ["embed"]
    for l in range(layers):
        out += ["L%d.norm1" % l, "L%d.attn" % l, "L%d.norm2" % l, "L%d.mlp" % l]
    return out + ["final.norm", "head"]


def consumer(wname: str) -> str:
    """Declared direct consumer cell of a weight tensor."""
    if wname in ("embed", "head"):
        return wname
    l, w = wname.split(".")
    return "%s.%s" % (l, "attn" if w in ("wqkv", "wo") else "mlp")


def expected_kv_layers(wname: str, layers: int) -> list[int]:
    """Layers whose KV chain head must move. wqkv is perturbed in a K row, so its own layer
    moves; every other weight only reaches later layers through the residual stream."""
    if wname == "head":
        return []
    if wname == "embed":
        return list(range(layers))
    l, w = int(wname[1:wname.index(".")]), wname.split(".")[1]
    return list(range(l if w == "wqkv" else l + 1, layers))


def digests(model, prompt: str = PROMPT):
    """({cell: out digest}, [kv chain head per layer]) for one feed of `prompt`."""
    lg = al.ActiveLog(dev="localize")
    st = C.Stream(model, {}, lg, "loc")
    st.feed(C.tokenize(prompt))
    outs = {r["body"]["cell"]: r["body"]["out"] for r in lg.records}
    return outs, [h[-1] for h in st.kvh]


def target_element(model, wname: str, prompt: str = PROMPT):
    """(row, col) to perturb: a token in the prompt for embed; a K row for wqkv."""
    if wname == "embed":
        return C.tokenize(prompt)[0], 0
    if wname.endswith(".wqkv"):
        return model.cfg["d"] + 1, 0
    return 0, 0


def localize(model, wname: str, eps: float = EPS, prompt: str = PROMPT) -> dict:
    layers = model.cfg["layers"]
    order = cell_order(layers)
    base, base_kv = digests(model, prompt)
    pert = copy.deepcopy(model)
    r, c = target_element(model, wname, prompt)
    pert.W[wname][r][c] += eps
    pert._k = {}
    new, new_kv = digests(pert, prompt)
    moved = [x for x in order if new[x] != base[x]]
    kv_moved = [l for l in range(layers) if new_kv[l] != base_kv[l]]
    exp_first = consumer(wname)
    exp_moved = order[order.index(exp_first):]
    return {"weight": wname, "elem": (r, c), "eps": eps,
            "first": moved[0] if moved else None, "expected_first": exp_first,
            "moved": moved, "n_moved": len(moved), "expected_n": len(exp_moved),
            "moved_matches": moved == exp_moved,
            "kv_moved": kv_moved, "kv_expected": expected_kv_layers(wname, layers),
            "n_cells": len(order)}


def control(model, eps: float = EPS) -> list[dict]:
    return [localize(model, w, eps) for w in sorted((k for k in model.W if k != "jepa"), key=_pos)]


def _pos(w: str):
    """Tensor order = execution order, so the table reads top to bottom like the forward pass."""
    if w == "embed":
        return (-1, 0, w)
    if w == "head":
        return (10 ** 6, 0, w)
    return (int(w[1:w.index(".")]), ["wqkv", "wo", "w1", "w2"].index(w.split(".")[1]), w)


def table(rows: list[dict]) -> str:
    n = rows[0]["n_cells"]
    L = ["%-9s %-13s %-11s %s" % ("perturbed", "first moved", "#cells", "KV-chain layers moved")]
    for r in rows:
        L.append("%-9s %-13s %2d / %-6d %s" % (r["weight"], r["first"], r["n_moved"], n,
                                               r["kv_moved"] or "-"))
    return "\n".join(L)


if __name__ == "__main__":
    m, _ = C.build_model()
    print(table(control(m)))
