"""A build step: two ways to bundle files into one artifact, receipted and priced.

Both strategies must emit the same bytes (products are compared by hash); they differ in
intermediate storage. Real wall time is measured here, so only the *relationship* is asserted.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from quilt_kernel import Cell, Ledger, price, which

FILES = {"a.js": "let a = 1;\n", "b.js": "let b = 2;\n", "c.js": "let c = a + b;\n" * 200}

def bundle_concat(files):          # one pass, builds the artifact directly
    return {"bundle": "".join(files[k] for k in sorted(files))}

def bundle_staged(files):          # stages a copy per file first: same bytes, more scratch storage
    staged = [files[k] for k in sorted(files)]
    return {"bundle": "".join(staged)}

def cost_concat(out, files): return {"train": 0, "prod": len(out["bundle"])}
def cost_staged(out, files): return {"train": sum(len(v) for v in files.values()), "prod": len(out["bundle"])}

def main():
    led = Ledger(dev="build")
    a = Cell(bundle_concat, "bundle.concat", led, cost=cost_concat)
    b = Cell(bundle_staged, "bundle.staged", led, cost=cost_staged)
    a(FILES); b(FILES)
    res = price({"concat": a.last, "staged": b.last})
    print("build:", res["status"], "| cheapest (storage):", which(res, "cheap"))
    return res

if __name__ == "__main__":
    main()
