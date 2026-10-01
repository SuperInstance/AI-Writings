import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import code_real_quant as q

checks = fails = 0
def check(name, ok):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
        print("FAIL:", name)

# --- rotation / centroids
R = q.rotation_matrix(16)
check("rotation deterministic", R == q.rotation_matrix(16))
check("rotation seed matters", R != q.rotation_matrix(16, seed=43))
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
check("rotation orthonormal", all(abs(dot(R[i], R[j]) - (i == j)) < 1e-9
                                  for i in range(16) for j in range(16)))
check("16 sorted centroids", len(q.CENTROIDS) == 16 and q.CENTROIDS == sorted(q.CENTROIDS))
check("centroids symmetric (Gaussian)", all(abs(a + b) < 1e-6 for a, b in
      zip(q.CENTROIDS, reversed(q.CENTROIDS))))
check("fnv1a64 empty == offset", q.fnv1a64(b"") == q.FNV_OFFSET)
check("fnv1a64 known vector 'a'", q.fnv1a64(b"a") == 0xaf63dc4c8601ec8c)

# --- chain verify + tamper
vecs = q.synth(60, 32, 3)
idx = q.CodeIndex(32)
for v in vecs:
    idx.add(v)
check("first prev_hash is GENESIS", idx.cells[0].prev_hash == q.GENESIS)
check("chain links", all(idx.cells[i].prev_hash == idx.cells[i - 1].hash for i in range(1, 60)))
check("chain verifies", idx.verify_chain())
c = idx.cells[30]
orig = c.codes
c.codes = bytes([orig[0] ^ 1]) + orig[1:]
check("tampered codes detected", not idx.verify_chain())
c.codes = orig
check("restore re-verifies", idx.verify_chain())
saved = idx.cells[10].prev_hash
idx.cells[10].prev_hash = 123
check("tampered prev_hash detected", not idx.verify_chain())
idx.cells[10].prev_hash = saved
check("restored prev_hash verifies", idx.verify_chain())

# --- no float on the cell
check("Cell has no vector attribute", all(not hasattr(cl, "vector") for cl in idx.cells))
check("Cell slots are ids/codes/hashes only",
      q.Cell.__slots__ == ("cell_id", "codes", "prev_hash", "hash"))
check("cell codes are bytes, dim/2 long", all(isinstance(cl.codes, bytes) and len(cl.codes) == 16
                                              for cl in idx.cells))
check("index without keep_float holds no floats", idx._float is None)
check("code_search works with no floats", len(idx.code_search(vecs[0], 5)) == 5)

# --- pack/unpack
codes = [i % 16 for i in range(33)]
check("pack/unpack roundtrip (odd dim)", q.unpack(q.pack(codes), 33) == codes)

# --- ADC ranking on a planted-near case
dim = 64
idx2 = q.CodeIndex(dim, keep_float=True)
base = q.synth(300, dim, 11)
target = base[137]
for v in base:
    idx2.add(v)
qry = [x + 0.05 * y for x, y in zip(target, q.synth(1, dim, 99, clusters=1, noise=1.0)[0])]
top = idx2.code_search(qry, 3)
check("planted near vector ranks #1 by codes", top[0] == 137)
check("float baseline agrees on planted case", idx2.float_search(qry, 1)[0] == 137)

# --- recall@k measured, within a stated bound (bound is a floor, not a target)
r = q.measure(n=500, m=30, dim=64, k=10)
print(f"  measured recall@10 (N=500, M=30, dim=64): {r['recall']:.4f}")
check("recall@10 computed in [0,1]", 0.0 <= r["recall"] <= 1.0)
check("recall@10 >= 0.60 (stated floor)", r["recall"] >= 0.60)
check("recall@10 < 1.0 (loss is real, not hidden)", r["recall"] < 1.0)
check("chain ok in measure()", r["chain_ok"])

# --- bytes per cell
check("code vector is 8x smaller than float32", r["vec_float"] == 8 * r["vec_code"])
check("whole cell smaller than float cell", r["code_bytes"] < r["float_bytes"])

# --- determinism
a = q.CodeIndex(32); b = q.CodeIndex(32)
for v in vecs:
    a.add(v); b.add(v)
check("same input -> same chain head", a.cells[-1].hash == b.cells[-1].hash)
check("same input -> same search", a.code_search(vecs[5], 10) == b.code_search(vecs[5], 10))
check("measure() deterministic", q.measure(n=200, m=10, dim=32)["recall"]
      == q.measure(n=200, m=10, dim=32)["recall"])

# --- playtest hardening (PLAYTEST-REPORT.md)
def raises(f):
    try:
        f()
    except ValueError:
        return True
    except Exception:
        return False
    return False
pi = q.CodeIndex(8, keep_float=True)
for v in q.synth(30, 8, 1):
    pi.add(v)
qq = q.synth(1, 8, 99)[0]
check("PT: negative k is refused (was: silently returned n-1 results)", raises(lambda: pi.code_search(qq, -1)) and raises(lambda: pi.float_search(qq, -1)))
check("PT: k=0 -> [] and k>n -> n results", pi.code_search(qq, 0) == [] and len(pi.code_search(qq, 1000)) == 30)
check("PT: NaN / inf vectors are refused (were: silently indexed as an all-zero code)",
      raises(lambda: q.CodeIndex(8).add([float("nan")] * 8)) and raises(lambda: q.CodeIndex(8).add([float("inf")] + [0.0] * 7))
      and raises(lambda: pi.code_search([float("nan")] * 8, 3)))
check("PT: wrong-dimension add/query is a ValueError (assert vanishes under -O; query used to truncate via zip)",
      raises(lambda: q.CodeIndex(8).add([1.0] * 7)) and raises(lambda: pi.code_search([1.0] * 7, 3)))
base = [1.0, -2.0, 3.0, 0.5, -0.25, 4.0, -1.5, 2.0]
check("PT: scale-invariance incl. 1e200 / 1e-200 (was: overflow/underflow -> constant all-7 code)",
      all(q.CodeIndex(8).add([x * sc for x in base]).codes == q.CodeIndex(8).add(base).codes for sc in (1e200, 1e-200, 1e-3, 1e3)))
check("PT: float_search without keep_float is a clear ValueError", raises(lambda: q.CodeIndex(8).float_search(qq, 3)))
check("PT: measure(n=0 / m=0) is a clear ValueError", raises(lambda: q.measure(n=0, m=2, dim=8)) and raises(lambda: q.measure(n=9, m=0, dim=8)))
check("PT: exact duplicates tie-break by id (deterministic)", (lambda ix: (ix.add([1.0] * 8), ix.add([1.0] * 8), ix.code_search([1.0] * 8, 2))[2])(q.CodeIndex(8)) == [0, 1])
tx = q.CodeIndex(8); tx.add([1.0] * 8); tx.add([2.0] + [1.0] * 7)
tx.cells[-1].codes = b"\x00" * 4; tx.cells[-1].hash = q.fnv1a64(q.struct.pack("<QQ", 1, tx.cells[-1].prev_hash) + tx.cells[-1].codes)
check("KNOWN LIMIT: tamper + re-hash of the LAST cell is undetectable without an external anchor (quilt-kernel has one; this lab does not)", tx.verify_chain())

print(f"code-real-quant selftest: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
