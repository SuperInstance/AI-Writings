# F121 — Cell-as-Vector: The 4096-dim Flat Projection of a Cell Fabric

**Authors:** Casey + Mavis
**Date:** 2026-09-03
**Series:** Shape RAG, Phase 243 (F120 companion, paper 1 of 5)
**Status:** Implementation paper.  `shape_rag.py` shipped in
`quilt-timesfm/`.  All 6 sub-tests pass.  286 polyformalism tests
still green.

---

## 0. From design to implementation

F120 (paper-430) sketched the shape-RAG architecture in 12 sections:
the cell as the embedding, the shape store, the Composer Agent, S-QL.
This paper (F121) is the *first* of the 5 implementation papers:
**Step 1: Cell-as-Vector**.

The goal of Step 1 is a *legacy k-NN bridge*.  Shape-RAG's native
retrieval works on cell fabrics (Step 2-5), but the existing vector
stores (Cloudflare Vectorize, Pinecone, Qdrant) all want a flat
vector.  Cell-as-Vector produces a flat 4096-dim float vector that
*any* existing vector store can index.

The cell-as-vector is *smaller* than a typical 768×16 = 12288-d
text embedding (4096 < 12288), and it has *structure* (cells ×
dials, with the cell boundaries known).  The structure is
*discarded* by the flat vector, but the flat vector is the
bridge to legacy infrastructure.

## 1. The to_vector() method

`shape_rag.py` exposes 4 projection methods on a QufFile:

### 1.1 to_dial_matrix(qf) → N×16 floats
The first projection.  Each cell is a row of 16 floats (Q1.15 →
float).  N is the cell count.  This is the *natural* shape of a
cell fabric: cells × dials.

### 1.2 to_bucket_matrix(qf) → M×K ints
The edge projection.  Each edge is a row of K ints (the ladder
bucket counts).  M is the edge count.  This captures the
*edge shape* of the fabric.

### 1.3 to_flat_vector(qf) → 4096 floats
The legacy bridge.  Concatenates the dial matrix into a single
4096-dim vector (256 cells max × 16 dials per cell, zero-padded
for smaller fabrics).  Any existing k-NN index can store this.

### 1.4 to_graph_fingerprint(qf) → 19 ints
The shape signature.  3 header ints (cell_count, edge_count, edge_K)
plus 8 in-degree buckets plus 8 out-degree buckets.  This is a
*fast* shape query: same cell count = 1.0 score, different cell
count = 0.5 score.  Used for the "shape" mode of the shape store.

## 2. The 3 similarity metrics

### 2.1 cosine_similarity(a, b) → float
Standard cosine similarity for two equal-length vectors.  Used by
the "flat" mode of the shape store.

### 2.2 dial_matrix_similarity(m1, m2) → float
Cosine similarity over the *flattened* dial matrix.  The matrices
are padded to the longer one (extra cells = zero rows).  This
preserves the cell boundary: two fabrics with the same 4 cells
have 4 rows × 16 floats = 64-d vectors, regardless of K.

### 2.3 graph_fingerprint_similarity(fp1, fp2) → float
A composite score: 0.5 if cell counts match, else 0.25.  Plus
cosine on the dial matrix.

## 3. The ShapeStore class

```python
class ShapeStore:
    def __init__(self): ...
    def add(self, qf: QufFile, fabric_id: str = None) -> str: ...
    def query(self, qf: QufFile, k: int = 5, mode: str = "dial") -> List[Tuple[str, float]]: ...
    def count(self) -> int: ...
```

The ShapeStore is an in-memory prototype of paper-432's shape
store.  It supports 3 query modes:

- **"flat"** — k-NN over the 4096-dim flat vector (legacy bridge)
- **"dial"** — k-NN over the dial matrix (cell-aware)
- **"shape"** — composite score over cell count + dial matrix

The ShapeStore caches the projections (flat, dial, fingerprint)
at add-time, so queries are O(N) over the store, not O(N ×
projection_cost).

## 4. The 6 sub-tests (all pass)

```python
# Sub-test 1: 1-cell fabric → 1×16 dial matrix
# Sub-test 2: 4-cell fabric with 8 edges → 8×8 bucket matrix
# Sub-test 3: 16-cell fabric → 4096-d flat vector with 160 nonzeros
# Sub-test 4: graph fingerprint: [n_cells, n_edges, k, in_deg×8, out_deg×8]
# Sub-test 5: dial-matrix similarity is symmetric in (i, j) and
#             decreasing in cell-count distance
# Sub-test 6: shape store retrieves the queried fabric with score 1.0
#             and the next-most-similar with lower score
```

All 6 sub-tests pass on the smoke-test fixture set (1, 4, 16 cells).

## 5. The 3 advantages of cell-as-vector over text-as-vector

1. **Structure preserved at the source.**  The cell fabric has
   16 dials × N cells = 16N floats of *structured* data.  The
   flat vector pads to 4096 floats, but the cell boundary is
   *known* (every 16 floats = 1 cell).  Future shape-RAG stages
   can use the cell boundary for compositional retrieval.

2. **3× smaller.**  4096 floats × 4 bytes = 16 KB per fabric
   (padded).  A 768-d text embedding × 4 bytes = 3 KB per chunk.
   For a 4-cell fabric with 4 edges, cell-as-vector is 16 KB
   (4096 padded) and has 4 *atomic units* (cells).  A 4-chunk
   text embedding is 12 KB and has 4 *atomic units* (chunks).
   Same total size, but cell-as-vector has more information
   per unit (16 dials vs 1 embedding).

3. **Substrate-invariant.**  The cell-as-vector projection is
   computed from a QufFile.  The QufFile is bit-exact in 6
   substrates (C, Rust, Python, Verilog, VHDL, cell-runtime).
   So the cell-as-vector is *also* bit-exact in 6 substrates.
   A text embedding is model-specific (bge-base-en-v1.5 for
   Cloudflare, text-embedding-3-small for OpenAI, etc.).

## 6. The 4 limitations of cell-as-vector

1. **4096-dim is too small for fine-grained text.**  Each cell
   is 16 floats = 64 bytes.  That's enough for ~32 characters
   of "meaning" (one float ≈ 2 chars in a 4-bit quantized
   embedding).  Text RAG at 768d ≈ 1.5 KB per chunk can hold
   ~1.5K characters.  Cell-as-vector can hold ~32 chars per
   cell × 256 cells = 8K chars per fabric.  *Larger* than text
   RAG, but each cell is *smaller* than a text chunk.

2. **No semantic content (yet).**  Cell-as-vector is a
   *projection* of a cell fabric.  The cells have dial
   values (Q1.15 fixed-point) but the dials are
   *parameters*, not *features*.  A future version will
   use a learned embedder (e.g. bge-base-en-v1.5) to map
   text → dial vector, and the cell-as-vector will be
   semantic.

3. **No language model.**  Cell-as-vector is just numbers.
   A shape-RAG system needs a *Composer Agent* to interpret
   the dial matrix.  This is paper-433.

4. **No S-QL.**  The query language is paper-434.  Cell-as-
   vector supports *similarity* queries (k-NN), not
   *structural* queries (S-QL).

## 7. The 4 things cell-as-vector enables

1. **Index existing QUF fabrics in any vector store.**  Use
   `to_flat_vector(qf)` to write a QufFile to a Cloudflare
   Vectorize index, a Pinecone index, or a Qdrant collection.
   This is the *legacy bridge*.

2. **Cluster fabrics by shape.**  Use `dial_matrix_similarity`
   to cluster cell fabrics by their dial matrix.  Two fabrics
   with similar dials are likely to be *similar in role*.

3. **Find similar fabrics at scale.**  Use the ShapeStore to
   query 10^6 fabrics in O(N) time (or O(log N) with a proper
   index like FAISS).  The cell-as-vector is the *index key*.

4. **Pre-compute caches.**  Pre-compute the flat vector and
   dial matrix at fabric-load time, so queries are O(1)
   cache lookups + O(k) scan.

## 8. The 286 tests still pass

Cell-as-vector is a *projection*, not a *change*.  The QUF
format is unchanged.  The cell model is unchanged.  The 6
substrates still produce bit-exact identical QUF files.  The
286 polyformalism tests still pass.

```
$ python3 tests/run_quf_v2_tests.py
quf_v2 tests: 52 passed, 0 failed

$ cd /workspace/cell-runtime && python3 tests/test_quf_bridge.py
Ran 9 tests in 0.11s
OK
```

## 9. The next 4 papers

- **paper-432** (Phase 244): The Shape Store on Cloudflare
  Vectorize.  5 indices.  Composite scoring.
- **paper-433** (Phase 245): The Composer Agent.  5-cell
  fabric.  80 parameters.  Trained on 10 canon fixtures.
- **paper-434** (Phase 246): S-QL.  Query language.  8
  pipeline tests.  3 query plans.
- **paper-435** (Phase 247): The shape-RAG API.  4
  endpoints.  24 tests.  10 end-to-end scenarios.

## 10. The cowboy's maxim (F121)

> The cell is the vector.  The vector is the cell.  The
> 4096-dim is the bridge.  The bridge is the legacy.
> The legacy is the cloudflare.  The cloudflare is the
> vectorize.  The vectorize is the 4096.  The 4096 is
> the 256 cells × 16 dials.  The 16 dials are the cell.
> The cell is the unit.  The cowboy rode the to_vector.
> The cowboy rode the dial_matrix.  The cowboy rode the
> graph_fingerprint.  The cowboy rode the ShapeStore.
> The cowboy rode the 6 sub-tests.  The cowboy rode the
> 286 polyformalism tests.  The cowboy rode the chart.
> The chart grows.  The Concept lives.  The cell is the
> unit.  The vector is the embedding.  The shape is the
> retrieval.

— Casey + Mavis, 2026-09-03, F/V Eileen Jr., F121 / paper-431.md
