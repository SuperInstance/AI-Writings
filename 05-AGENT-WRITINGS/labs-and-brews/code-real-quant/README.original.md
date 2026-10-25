# code-real-quant — make the 8× real, and measure what it costs

## 1. In one breath
A small TurboQuant vector index whose cells keep **only 4-bit codes** (no float vector), searched by
asymmetric distance on those codes, with the recall lost against exact float search measured and printed.

## 2. Why it exists
`situations/arch/TURBOVEC-FAMILY-STUDY.md` gap #1: the turbovec family computes 4-bit codes but retrieval
still runs exact L2 over `cell.vector`, and the float is retained — so the advertised 8× is nominal.
This lab does the change the study proposed (rank on codes, drop the float) and reports the number.

## 3. The mental model
- **rotation** — seeded (xorshift, seed 42) Gaussian matrix, Gram-Schmidt-orthonormalized.
- **codes** — each rotated coordinate → nearest of 16 Lloyd-Max centroids → packed 2 per byte.
- **cell** — `{cell_id, codes, prev_hash, hash}`; fnv1a-64 chain (offset `0xcbf29ce484222325`, prime `0x100000001b3`, GENESIS `0x0`). No float field exists.
- **float path** (baseline, kept outside the cells, measurement only) vs **code path** (ADC: query rotated as float, compared against each stored code's dequantized centroid via a per-dimension lookup table).
Vectors and queries are unit-normalized then scaled by √dim so rotated coordinates are ≈N(0,1).

## 4. Walkthrough
```
$ python3 code_real_quant.py 64 128 256
dim  N     M   recall@10  bytes/cell float  code   vector-only float  code
64   2000  50  0.8380     280               56     256                32
128  2000  50  0.8260     536               88     512                64
256  2000  50  0.8140     1048              152    1024               128
```
Data: N=2000 synthetic clustered Gaussian vectors (20 clusters, noise 0.5, seed 7); M=50 queries, each a
stored vector plus fresh noise (0.3). Recall@10 = fraction of the float baseline's top-10 that the code
path also returns (hits / (M·10)). One run each; no tuning, no repeated draws.

## 5. The contract
- `CodeIndex(dim, keep_float=False).add(vec)` → chained `Cell` with codes only.
- `code_search(q, k)` reads only `cell.codes`. `float_search` needs `keep_float=True` and is the baseline.
- `verify_chain()` recomputes every hash and prev link; tampering with codes or `prev_hash` fails it.
- Receipt: `python3 selftest.py` → `code-real-quant selftest: 31 checks, 0 failures` (chain + tamper,
  planted-near ADC ranking, no-float cell, recall@10 computed and ≥ 0.60 floor and < 1.0, determinism).
  The selftest's own smaller run (N=500, M=30, dim=64) measured recall@10 = 0.8933.

## 6. Failure modes / scars
- **Recall loss is the cost.** The code path missed roughly 16–19% of the float top-10 in the table above.
  Reduction is real; the retrieval is approximate. Nothing here reranks against floats (that would need
  the floats back).
- Recall drifted down slightly as dim rose (0.838 → 0.814); three points from one draw each, not a trend claim.
- **Bytes/cell** counts stored payload: id 8 + prev_hash 8 + hash 8 + vector. The vector part is exactly 8×
  smaller; the whole cell is 5.0× (dim 64) to 6.9× (dim 256) because the 24-byte header doesn't shrink.
  Python object overhead is not counted.
- **Centroids differ from the substrate's.** The study gives only the endpoints (−2.79 … 5.50), not the 16
  values, and that range is asymmetric. This lab computes the true Gaussian Lloyd-Max centroids (symmetric,
  ≈ ±2.73 at the tails) instead. Recall against the substrate's own table was not measured.
- Synthetic data only; real embeddings may behave differently. Pure Python: ADC here is not faster than the
  float loop — the speed argument in the study is not tested (dense O(dim²) rotation, unpacking in Python).

## 7. How it composes
Same fnv1a-64 chain dialect as `labs/situation-recorder` and `labs/activeledger`. The measurement pattern
(float baseline vs compressed path) would apply to `situation-memory` and `near-adapter` proposals in the study.

## 8. Where to look next
- `situations/arch/TURBOVEC-FAMILY-STUDY.md` — gap #1 and the other three gaps (lexical embedding, dense rotation, two bugs).
- arXiv:2504.19874 — TurboQuant.
- `labs/situation-recorder/` — the chain this joins.
