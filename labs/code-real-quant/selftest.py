"""selftest for code_real_quant. Prints '<name> selftest: N checks, 0 failures'."""
import array
import sys
import code_real_quant as q

checks, fails = 0, []


def check(name, cond):
    global checks
    checks += 1
    if not cond:
        fails.append(name)
        print("FAIL:", name)


# --- constants / primitives
check("fnv1a64 empty == offset basis", q.fnv1a64(b"") == 0xcbf29ce484222325)
check("fnv1a64 known vector 'a'", q.fnv1a64(b"a") == 0xaf63dc4c8601ec8c)
check("16 sorted centroids", len(q.CENTROIDS) == 16 and q.CENTROIDS == sorted(q.CENTROIDS))
check("centroids symmetric", all(abs(a + b) < 1e-6 for a, b in zip(q.CENTROIDS, q.CENTROIDS[::-1])))
check("pack/unpack round trip", q.unpack_codes(q.pack_codes([1, 15, 0, 7, 9]), 5) == [1, 15, 0, 7, 9])

# --- rotation orthonormal + deterministic
R = q.make_rotation(16)
dots_ok = all(abs(sum(a * b for a, b in zip(R[i], R[j])) - (1.0 if i == j else 0.0)) < 1e-9
              for i in range(16) for j in range(16))
check("rotation orthonormal", dots_ok)
check("rotation deterministic", R == q.make_rotation(16))

# --- chain verify + tamper (both index kinds)
data = q.synthetic(30, 32, 5)
for cls in (q.FloatIndex, q.CodeIndex):
    ix = cls(32)
    for i, v in enumerate(data):
        ix.add("c%d" % i, v)
    check(cls.__name__ + " chain verifies", ix.verify_chain())
    check(cls.__name__ + " first prev_hash is GENESIS", ix.cells[0].prev_hash == q.GENESIS)
    check(cls.__name__ + " links prev_hash", ix.cells[5].prev_hash == ix.cells[4].hash)
    p = bytearray(ix.cells[10].payload)
    p[0] ^= 1
    ix.cells[10].payload = bytes(p)
    check(cls.__name__ + " payload tamper detected", not ix.verify_chain())
    ix2 = cls(32)
    for i, v in enumerate(data):
        ix2.add("c%d" % i, v)
    ix2.cells[7].prev_hash ^= 1
    check(cls.__name__ + " prev_hash tamper detected", not ix2.verify_chain())

# --- ADC ranking on a planted-near case
dim = 64
bg = q.synthetic(300, dim, 11)
query = q.synthetic(1, dim, 99)[0]
noise = q.synthetic(1, dim, 100)[0]
planted = [a + 0.1 * b for a, b in zip(query, noise)]
ci = q.CodeIndex(dim)
for i, v in enumerate(bg):
    ci.add("bg%d" % i, v)
ci.add("planted", planted)
res = ci.search(query, 5)
check("ADC ranks planted-near vector first", res[0][1] == "planted")
check("ADC scores ascending", [s for s, _ in res] == sorted(s for s, _ in res))
check("planted score well below runner-up", res[0][0] < 0.5 * res[1][0])

# --- code cell holds no float vector
cell = ci.cells[0]
check("code cell payload is bytes", isinstance(cell.payload, bytes))
check("code payload is dim/2 bytes", len(cell.payload) == dim // 2)
check("code cell has no vector attribute", not hasattr(cell, "vector") and not hasattr(cell, "__dict__"))
check("no cell field is float/list/array",
      all(not isinstance(getattr(cell, s), (float, list, tuple, array.array)) for s in cell.__slots__))
check("code index keeps no float store", not any(isinstance(v, (list, array.array)) and v and isinstance(v[0], float)
      for k, v in vars(ci).items() if k not in ("rot",)))

# --- measured recall and bytes
r = q.measure()
r2 = q.measure()
print("measured: recall@10=%.4f  vec bytes float=%d code=%d  cell bytes float=%d code=%d" % (
    r["recall_at_k"], r["float_vec_bytes"], r["code_vec_bytes"], r["float_cell_bytes"], r["code_cell_bytes"]))
check("recall@10 within stated bound [0.75, 1.0)", 0.75 <= r["recall_at_k"] < 1.0)
check("recall is a real loss (<1.0), not hidden", r["recall_at_k"] < 1.0)
check("vector bytes reduction is exactly 8x vs float32", r["float_vec_bytes"] / r["code_vec_bytes"] == 8.0)
check("total cell bytes reduction 5.67x (hash overhead counted)",
      abs(r["float_cell_bytes"] / r["code_cell_bytes"] - 272 / 48) < 1e-9)

# --- determinism
check("measure() deterministic", r == r2)
a, b = q.CodeIndex(32), q.CodeIndex(32)
for i, v in enumerate(data):
    a.add("c%d" % i, v)
    b.add("c%d" % i, v)
check("same input -> same head hash", a.cells[-1].hash == b.cells[-1].hash)

print("code_real_quant selftest: %d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
