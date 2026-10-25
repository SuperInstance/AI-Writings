"""Data pipeline: two dedupe implementations, receipted and priced.

Budgets here come from a deterministic op-count cost model (so the output is reproducible);
drop the `cost=` argument and wall_ms is measured with the real clock instead.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from quilt_kernel import Cell, Ledger, price, which

def dedupe_sorted(xs):            # O(n log n), low memory
    out = []
    for x in sorted(xs):
        if not out or out[-1] != x:
            out.append(x)
    return out

def dedupe_hashed(xs):            # O(n), extra memory
    return sorted(set(xs))

def cost_sorted(out, xs):   n = len(xs); return {"wall_ms": n * max(n.bit_length(), 1) / 100, "mem_mb": 1}
def cost_hashed(out, xs):   n = len(xs); return {"wall_ms": n / 100, "mem_mb": 4}

def main():
    led = Ledger(dev="pipeline")
    a = Cell(dedupe_sorted, "dedupe.sorted", led, cost=cost_sorted)
    b = Cell(dedupe_hashed, "dedupe.hashed", led, cost=cost_hashed)
    data = [[5, 3, 3, 9, 1, 1], list(range(50)) * 3, [7] * 40]
    ra, rb = [], []
    for xs in data:
        a(xs); ra.append(a.last)
        b(xs); rb.append(b.last)
    res = price({"sorted": ra, "hashed": rb})
    print("ledger intact:", led.verify()["intact"], "| records:", len(led.records))
    print("status:", res["status"], "| class:", res["class"], "| faster:", which(res, "fast"))
    return res

if __name__ == "__main__":
    main()
