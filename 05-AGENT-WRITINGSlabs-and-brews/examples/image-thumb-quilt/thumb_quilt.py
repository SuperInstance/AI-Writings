"""image-thumb-quilt (EX5) — "make a thumbnail <= target WxH".

Two product-identical routes for the same request, on a deterministic synthetic
grayscale image {w, h, pixels:[[int]]} (stdlib only, offline):

  * PASS-THROUGH (cheap) — the source is ALREADY <= target, so skip decode+resample
    and hand the source back unchanged. No resample tooling shipped, tiny footprint.
  * RESAMPLE (full) — decode the packed bytes, then box-average downsample to the
    largest size that fits the target (aspect preserved). Ships the decoder +
    resampler, so it costs more compute AND storage. Works for any source.

The quilt CHOOSES pass-through iff source <= target, else resample. On the shared
(already-small) cases resample degenerates to a no-op, so both routes reach the
IDENTICAL thumbnail — novelty in process, identity in product.

Everything is booked to an ActiveLog v1 run via the shared labs/activeledger emitter.
Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §8, §11.3, §13.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "activeledger"))
from activeledger import (ActiveLog, DoubleEntry, ZERO_BUDGET, add_budget,  # noqa: E402
                          budget, verify_chain, route_total)

# ---- synthetic image ----------------------------------------------------------------

def make_image(w: int, h: int, seed: int = 1) -> dict:
    """Deterministic gradient+hash grayscale grid, values 0..255."""
    px = [[(x * 7 + y * 13 + seed * 31 + ((x * y) ^ seed) * 3) % 256 for x in range(w)]
          for y in range(h)]
    return {"w": w, "h": h, "pixels": px}


def encode(img: dict) -> bytes:
    """The 'file': 2-byte dims header + row-major bytes (what a decoder would eat)."""
    return bytes([img["w"], img["h"]]) + bytes(v for row in img["pixels"] for v in row)


def decode(data: bytes) -> dict:
    w, h = data[0], data[1]
    body = data[2:]
    return {"w": w, "h": h, "pixels": [list(body[y * w:(y + 1) * w]) for y in range(h)]}


def fits(img: dict, target: tuple[int, int]) -> bool:
    return img["w"] <= target[0] and img["h"] <= target[1]


def fit_size(w: int, h: int, tw: int, th: int) -> tuple[int, int]:
    """Largest aspect-preserving size within target; never upscales."""
    if w <= tw and h <= th:
        return w, h
    s = min(tw / w, th / h)
    return max(1, int(w * s)), max(1, int(h * s))


# ---- the two routes -----------------------------------------------------------------

def passthrough_route(img: dict, target) -> dict:
    """Cheap: refuses (by design) anything that needs resampling."""
    if not fits(img, target):
        raise NeedsResample("source exceeds target")
    return img


class NeedsResample(Exception):
    pass


def resample_route(data: bytes, target) -> dict:
    """Full: decode + box-average downsample (integer arithmetic, deterministic)."""
    img = decode(data)
    nw, nh = fit_size(img["w"], img["h"], target[0], target[1])
    out = []
    for y in range(nh):
        y0, y1 = y * img["h"] // nh, max(y * img["h"] // nh + 1, (y + 1) * img["h"] // nh)
        row = []
        for x in range(nw):
            x0, x1 = x * img["w"] // nw, max(x * img["w"] // nw + 1, (x + 1) * img["w"] // nw)
            cells = [img["pixels"][j][i] for j in range(y0, y1) for i in range(x0, x1)]
            row.append(sum(cells) // len(cells))
        out.append(row)
    return {"w": nw, "h": nh, "pixels": out}


def choose(img: dict, target) -> str:
    return "passthrough" if fits(img, target) else "resample"


# ---- cost model (resample ships decoder+resampler => more compute AND storage) ------

COST = {
    "passthrough": {"tick": budget(1, 0.1, 1, prod=48, train=96),
                    "hop": budget(1, 0.1, 1, prod=16, train=32)},
    "resample":    {"tick": budget(6, 0.8, 6, prod=2048, train=8192),
                    "hop": budget(3, 0.4, 3, prod=1024, train=4096)},
}


def _hop(al, route, src, dst, su, du, amt, rate, cost):
    de = DoubleEntry.translate(src, su, amt, dst, du, rate, "thumb:" + route)
    al.emit("route.hop", {"route": route, **de.body(), "budget": cost})


def run(img: dict, target, al: ActiveLog | None = None, force: str | None = None) -> dict:
    """Choose (or force) a route, run it, book every step. Returns thumbnail + log."""
    al = al or ActiveLog(dev="image-thumb-quilt")
    route = force or choose(img, target)
    c = COST[route]
    data = encode(img)
    npx = img["w"] * img["h"]

    al.emit("cell.tick", {"route": route, "cell": "request", "kind": "SIM",
                          "src": [img["w"], img["h"]], "target": list(target),
                          "units": "px", "budget": c["tick"]})
    _hop(al, route, "request", "thumbnailer", "px", "px-decoded" if route == "resample" else "px",
         float(npx), 1.0, c["hop"])
    thumb = passthrough_route(img, target) if route == "passthrough" else resample_route(data, target)
    al.emit("cell.tick", {"route": route, "cell": "thumbnailer", "kind": "SIM",
                          "out": [thumb["w"], thumb["h"]], "units": "px", "budget": c["tick"]})
    _hop(al, route, "thumbnailer", "result", "px", "px", float(thumb["w"] * thumb["h"]), 1.0, c["hop"])
    al.emit("cell.tick", {"route": route, "cell": "result", "kind": "SIM",
                          "units": "px", "budget": c["tick"]})
    total = route_total(al.records, route)
    al.emit("ledger.transaction", {"route": route, "thumb": [thumb["w"], thumb["h"]],
                                   "total_budget": total})
    return {"route": route, "thumb": thumb, "total_budget": total, "log": al}


TARGET = (8, 8)
WORKLOAD = [
    (make_image(4, 4, 1), TARGET),    # already small -> pass-through
    (make_image(8, 8, 2), TARGET),    # exactly target -> pass-through
    (make_image(6, 3, 3), TARGET),    # small, non-square -> pass-through
    (make_image(16, 16, 4), TARGET),  # needs resample
    (make_image(32, 16, 5), TARGET),  # needs resample (aspect kept: 8x4)
]

if __name__ == "__main__":
    for img, tgt in WORKLOAD:
        r = run(img, tgt)
        print(f"{img['w']}x{img['h']} -> {r['thumb']['w']}x{r['thumb']['h']} via {r['route']:11s} "
              f"(wall_ms={r['total_budget']['wall_ms']}, "
              f"prod_bytes={r['total_budget']['storage_bytes']['prod']})")
