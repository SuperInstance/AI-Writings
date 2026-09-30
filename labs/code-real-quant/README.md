# code-real-quant — TurboQuant compression that is measured, not nominal

## 1. In one breath
A small vector index that stores only 4-bit codes (no float vectors), searches on those codes, and reports what that costs: on the run below, recall@10 is 0.828 against exact float search, in 1/8 of the vector bytes.

## 2. Why it exists
`situations/arch/TURBOVEC-FAMILY-STUDY.md` gap #1: the turbovec family computes 4-bit codes, but every cell also keeps the full float vector and retrieval runs exact L2 on it. The codes are never used, so the advertised 8x is a formula (`32/n_bits`), not a measurement. This lab makes the compression real and puts a number on the loss.

## 3. The mental model
- **Cell** — one chained entry: `cell_id`, `kind`, `payload` (bytes), `prev_hash`, `hash`. Hash is fnv1a-64 (offset `0xcbf29ce484222325`, prime `0x100000001b3`, GENESIS `0`), same idiom as the rest of the fleet.
- **Rotation** — fixed orthonormal matrix (xorshift64 seed 42 → Gaussian → Gram-Schmidt). Vectors are L2-normalized, rotated, and scaled by `sqrt(dim)` so each coordinate is about N(0,1).
- **Codes** — each rotated coordinate maps to the nearest of 16 Lloyd-Max centroids; two 4-bit codes pack into one byte.
- **FloatIndex** — cell payload is the float32 vector; search is exact L2. The baseline.
- **CodeIndex** — cell payload is *only* the packed codes. Search is asymmetric distance (ADC): the query stays float (rotated), and each stored code is compared as its centroid value, via a per-query lookup table.

Both indexes receive the same added vectors; recall is the share of the float top-k that the code top-k also returns.

## 4. Walkthrough
```
$ python3 code_real_quant.py
n=2000 queries=50 dim=64 k=10
recall@10           : 0.8280
vector bytes/cell  : float 256  code 32  (8.00x)
total bytes/cell   : float 272  code 48  (5.67x)

$ python3 selftest.py
measured: recall@10=0.8280  vec bytes float=256 code=32  cell bytes float=272 code=48
code_real_quant selftest: 31 checks, 0 failures
```
```python
import code_real_quant as q
ix = q.CodeIndex(64); ix.add("a", vec); ix.search(query, k=10)  # [(distance, cell_id), ...]
```

## 5. The contract
- **Inputs:** float vectors of length `dim` (non-zero). **Outputs:** `search` → `k` `(score, cell_id)` pairs, ascending.
- **Invariants:** `CodeIndex` cells hold only `bytes` of length `dim/2`; no float vector is retained anywhere on the index (checked in the selftest). Chain verifies from GENESIS; any payload or `prev_hash` change fails `verify_chain()`. Everything is deterministic.
- **Receipt:** `python3 selftest.py` → `code_real_quant selftest: 31 checks, 0 failures`. It covers chain verify + tamper, ADC on a planted-near vector, recall@10 inside the stated bound **[0.75, 1.0)**, no float on the code cell, and determinism.

**Measured** (synthetic iid Gaussian vectors, 2000 cells, 50 queries, k=10, dim 64, data seed 7, query seed 1234):

| path | recall@10 | vector bytes/cell | total bytes/cell (vector + two 8-byte hashes) |
|---|---|---|---|
| float (exact L2) | 1.000 (reference) | 256 (float32) | 272 |
| code (4-bit ADC) | **0.828** | 32 | 48 |
| ratio | — | 8.00x | 5.67x |

Other runs, same script (`measure(dim=..., data_seed=s, query_seed=s+1000)`), recall@10: dim 32 → 0.826, 0.840; dim 64 → 0.830, 0.816; dim 128 → 0.798, 0.802 (seeds 7, 8). The bound in the selftest was set from these runs, not the other way round.

## 6. Failure modes / scars
- **The loss is the cost.** About 17% of the float top-10 is missed here. That is what 4-bit codes cost on this data; it was not tuned.
- **iid Gaussian data is a hard case.** Random vectors in 64+ dimensions are nearly equidistant, so top-10 neighbours are separated by small margins and quantization noise reorders them. Real embeddings with cluster structure may behave differently; not measured here.
- **Bytes are payload bytes**, not Python object sizes. Float32 is used for the baseline (Python floats are 8 bytes, so the real in-process ratio is larger). Per-cell hashes are counted at 8 bytes each; `cell_id`/`kind` strings are excluded from both.
- **Centroids differ from the study's.** The study cites 16 centroids spanning `-2.79 … 5.50`; that table is not in this repo and I did not import the substrate. Here the centroids are computed by Lloyd-Max iteration for N(0,1) (range −2.73 … 2.73, symmetric). Cross-implementation code equality with `turbovec-substrate` is therefore **not** claimed.
- **Speed is not measured or claimed.** The rotation is a dense O(dim²) matmul and search unpacks codes in pure Python.
- **Full scan.** Both paths score every cell; there is no index structure.

## 7. How it composes
- Drop-in for gap #1 in the turbovec family: `jev-turbovec`, `peanut-gallery-turbovec`, `madlibs-gan-turbovec`, `paradigm-edges-turbovec` could ride a `CodeIndex`-style store, once their centroid table is aligned or re-derived.
- Chain dialect matches `labs/situation-recorder` and `labs/activeledger` (fnv1a-64, GENESIS), so cells can sit beside situation cells.
- `labs/activeledger` has a `storage_bytes {train,prod}` budget axis; the bytes/cell figures here are the kind of number that axis wants.

## 8. Where to look next
- `situations/arch/TURBOVEC-FAMILY-STUDY.md` — the gap analysis this addresses (gaps #2–#4 remain open).
- `situations/blueprints/README.md` — the doc standard this README follows.
- arXiv:2504.19874 — the TurboQuant paper (not re-read for this lab).
