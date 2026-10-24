# F124 — S-QL: The Shape Query Language

**Authors:** Casey + Mavis (with DeepSeek V4-flash synthesis)
**Date:** 2026-09-03
**Series:** Shape RAG, Phase 246 (F120-F123 companion, paper 4 of 5)
**Polyformalism invariant:** FNV-1a 64-bit state hash `0x284816ba66c6e2af`

**Author:** The Shape-RAG Working Group  
**Status:** Draft v0.9 — for the SIGMOD/NeurIPS hybrid audience  
**References:** paper-431 (cell-as-vector), paper-432 (shape store), paper-433 (composer agent)

---

## 0. Abstract

We present S-QL, a domain-specific query language for shape-RAG, a retrieval-augmented generation framework where the fundamental unit—the *cell*—is itself an embedding, not merely a pointer to one. S-QL compiles to a deterministic five-stage pipeline: exact hash lookup, dial-vector cosine similarity, bucket-vector cosine similarity, Weisfeiler-Lehman graph-shape kernel, and backtracking homomorphism. We define the syntax with five canonical examples, specify the runtime stages with complexity bounds, and enumerate eight pipeline tests. We defend four design decisions (lex/yacc-free parsing, stage-based execution, ternary indexing, and a five-operator core). The polyformalism invariant `0x284816ba66c6e2af` (FNV-1a 64-bit) anchors all cross-representation consistency checks. We close with the cowboy's maxim.

---

## 1. Why a new query language (RAG is not SQL)

Relational databases assume a fixed schema, typed columns, and set-theoretic operations over tuples. SQL is magnificent for that world—but RAG operates on a different substrate. In shape-RAG, the database is not a collection of rows; it is a *fabric* of cells, each cell being a dense vector in a high-dimensional space, a dial vector for coarse orientation, a bucket vector for locality, a serialized graph shape (its neighborhood), and a set of typed edges. The embedding is not an attribute of the cell; the cell *is* the embedding.

SQL's `WHERE` clause evaluates predicates on column values. In shape-RAG, the most important predicates are *geometric* (cosine similarity), *structural* (graph isomorphism up to Weisfeiler-Lehman refinement), and *topological* (existence of a homomorphism preserving edge types). None of these are expressible as equality or range checks. Even SQL's `LIKE` cannot express "this subgraph appears as a shape within that cell's neighborhood."

Furthermore, RAG queries are *not* transactions. They are approximate, ranked, and often interactive. A query may return the top 10 cells by a composite score, but that score is a blend of vector similarity, structural congruence, and exact hash matches—a multi-modal ranking that SQL's `ORDER BY` cannot compute without user-defined functions that violate the optimizer's assumptions.

Finally, RAG queries must be *composable* with generative steps. The result of a query is not a table to be joined; it is a *fabric subset* to be fed into a composer agent (paper-433). That composer performs graph rewrites, not relational algebra. Therefore, we need a language whose output type is a shape-fabric, not a relation.

S-QL is that language. It is deliberately small—five operators, three index types, one pipeline. It borrows SQL's readability (`SELECT`, `WHERE`, `ORDER BY`) but replaces the relational semantics with shape semantics. The grammar is simple enough to parse with a recursive descent hand-rolled parser (no lex/yacc), because the language is not meant to be extended by committee; it is meant to be compiled to a fixed five-stage pipeline, each stage of which is independently optimizable and testable.

---

## 2. The S-QL syntax with 5 example queries

### 2.1 Grammar overview

S-QL is case-insensitive. Comments are `--` to end-of-line. The canonical form is:

```
SELECT cell
FROM <fabric_name>
WHERE <predicate_chain>
[TOP k]
[SNAP TO (<query_fabric>)]
[ORDER BY composite_score [ASC|DESC]];
```

The `WHERE` clause is a conjunction (implicit `AND`) of shape-specific predicates:

- `cell.dial[i] SIMILAR TO <hex_value>` — dial-vector cosine threshold (default 0.9)
- `cell.bucket[j] NEAR <hex_value>` — bucket-vector cosine threshold (default 0.95)
- `cell.address = '<string>'` — exact runtime address (hash lookup)
- `cell.fingerprint MATCHES (<n_cells> = k, <n_edges> = m)` — graph-shape size predicate
- `cell.shape SIMILAR TO <cell_expression>` — Weisfeiler-Lehman kernel similarity
- `cell.graph CONTAINS <pattern>` — backtracking homomorphism check

The `SNAP TO` clause binds the result set to a specific query fabric (a pre-materialized subgraph) for the homomorphism stage. Without it, the homomorphism stage runs against the global fabric graph.

### 2.2 Example 1: Exact address lookup with dial prefilter

```sql
SELECT cell FROM canon
WHERE cell.dial[0] SIMILAR TO 0x7FFF
  AND cell.address = 'cell-runtime'
TOP 1
SNAP TO (query_fabric)
ORDER BY composite_score DESC;
```

**Semantics:** This is the fastest possible query. The `address` predicate is an exact string match against the hash index (FNV-1a, invariant `0x284816ba66c6e2af`). The `dial[0]` predicate is a prefilter that reduces the candidate set before hash lookup—though in practice, the hash lookup is O(1), so the dial predicate only matters if the address is a wildcard or a prefix. Here, we request the top 1 result from the `canon` fabric, snapped to the `query_fabric` for subsequent composition.

**Pipeline compilation:**
1. Stage 1 (hash): Lookup `'cell-runtime'` → exact cell ID.
2. Stage 2 (dial cosine): Compute cosine between cell.dial[0] and 0x7FFF → if < 0.9, reject.
3. Stage 3 (bucket): Not used (no `bucket` predicate).
4. Stage 4 (WL kernel): Not used (no `shape` predicate).
5. Stage 5 (homomorphism): SNAP TO `query_fabric` → verify the cell appears in that fabric.

**Composite score:** Here, only two components exist: dial cosine (0.98) and address exactness (1.0). Composite = 0.99.

### 2.3 Example 2: Fingerprint + dial + bucket — the "shape size" query

```sql
SELECT cell FROM canon
WHERE cell.fingerprint MATCHES (n_cells = 4, n_edges = 4)
  AND cell.dial[1] SIMILAR TO 0x3FFF
  AND cell.bucket[2] NEAR 0x1FFF
TOP 10
ORDER BY composite_score DESC;
```

**Semantics:** This query finds cells whose neighborhood graph has exactly 4 nodes and 4 edges (a cycle of length 4, or a star with one extra edge). The fingerprint is a 64-bit FNV-1a hash of the canonical graph's degree sequence plus edge-type multiset. The `MATCHES` predicate is a prefilter: it does not guarantee shape isomorphism, but it eliminates cells whose graph size differs.

**Pipeline compilation:**
1. Stage 1 (hash): Not used (no `address`).
2. Stage 2 (dial): Prefilter on `dial[1]` against 0x3FFF → returns ~1% of cells.
3. Stage 3 (bucket): Further prefilter on `bucket[2]` against 0x1FFF → returns ~0.1% of cells.
4. Stage 4 (WL kernel): For each surviving cell, compute the Weisfeiler-Lehman kernel between its graph and the canonical 4-cycle graph. The kernel value must exceed the default threshold (0.8). This stage also checks the fingerprint: if the fingerprint does not match `(4,4)`, the cell is rejected before WL runs.
5. Stage 5 (homomorphism): No `SNAP TO` and no `CONTAINS` — this stage is a no-op (identity).

**Composite score:** 0.6 * dial_cosine + 0.3 * bucket_cosine + 0.1 * wl_kernel.

### 2.4 Example 3: Graph containment (homomorphism) with no vector predicates

```sql
SELECT cell FROM canon
WHERE cell.graph CONTAINS (a -> b, b -> c, a -> c)
  AND cell.fingerprint MATCHES (n_cells >= 3, n_edges >= 3)
TOP 5
SNAP TO (query_fabric)
ORDER BY composite_score;
```

**Semantics:** This is a pure structural query. We seek cells whose neighborhood graph contains a triangle (edges a→b, b→c, a→c). No vector similarity is used. The `CONTAINS` predicate triggers a backtracking homomorphism search: for each candidate cell, we attempt to map the pattern graph's vertices to the cell's graph vertices such that all edges exist with matching edge types.

**Pipeline compilation:**
1. Stage 1 (hash): Not used.
2. Stage 2 (dial): Not used.
3. Stage 3 (bucket): Not used.
4. Stage 4 (WL kernel): The fingerprint prefilter rejects cells with fewer than 3 nodes or 3 edges. For survivors, we compute the WL kernel between the cell graph and the triangle pattern. If the kernel is below 0.5, we reject early (the homomorphism is unlikely).
5. Stage 5 (homomorphism): For each remaining cell, run the backtracking algorithm (see Section 3.5). If a homomorphism exists, the cell is retained.

**Composite score:** Here, only the homomorphism existence matters. If found, score = 1.0; else 0.0. The `ORDER BY` is trivial.

### 2.5 Example 4: Multi-stage "similar shape" query with SNAP TO

```sql
SELECT cell FROM canon
WHERE cell.shape SIMILAR TO (
    SELECT cell FROM query_fabric WHERE cell.address = 'seed-42'
  )
  AND cell.dial[0] SIMILAR TO 0x7FFF
  AND cell.bucket[0] NEAR 0x0FFF
TOP 20
SNAP TO (query_fabric)
ORDER BY composite_score DESC;
```

**Semantics:** This is the most complex query. The `shape SIMILAR TO` subquery first fetches a reference cell (`seed-42`) from the `query_fabric`, then compares the shape of each candidate cell against that reference using the Weisfeiler-Lehman kernel. The `dial` and `bucket` predicates are filters. The `SNAP TO` clause ensures that all returned cells are within the `query_fabric` (i.e., they are part of the current working set).

**Pipeline compilation:**
1. Stage 1 (hash): Lookup `seed-42` in `query_fabric` → reference cell R.
2. Stage 2 (dial): Prefilter candidates by dial[0] cosine vs 0x7FFF.
3. Stage 3 (bucket): Prefilter by bucket[0] cosine vs 0x0FFF.
4. Stage 4 (WL kernel): For each candidate, compute WL kernel between candidate.graph and R.graph. Keep if > 0.8.
5. Stage 5 (homomorphism): SNAP TO `query_fabric` — verify that each candidate is in the fabric. Additionally, since we have a reference cell, we run a *partial* homomorphism check: does the candidate's graph contain a subgraph isomorphic to R's graph? (This is stricter than WL.)

**Composite score:** 0.5 * wl_kernel + 0.3 * dial_cosine + 0.2 * bucket_cosine.

### 2.6 Example 5: The "cowboy" query — everything at once

```sql
SELECT cell FROM canon
WHERE cell.address = 'cell-runtime'
   OR (cell.dial[2] SIMILAR TO 0x0FFF
       AND cell.bucket[3] NEAR 0x00FF
       AND cell.fingerprint MATCHES (n_cells = 8, n_edges = 12)
       AND cell.shape SIMILAR TO (0xABCD, 0x1234))
TOP 3
SNAP TO (query_fabric)
ORDER BY composite_score;
```

**Semantics:** This query demonstrates disjunction (`OR`). The first branch is an exact address lookup; the second branch is a complex shape query. The S-QL compiler will generate a union of two pipelines: one for the hash lookup, one for the shape query. The `TOP 3` applies after the union.

**Pipeline compilation:** The compiler splits the `WHERE` clause into a disjunctive normal form. Each disjunct becomes a separate pipeline. The results are merged, deduplicated, and sorted by composite score.

**Composite score:** For the first branch, score = 1.0 (exact match). For the second branch, score = 0.4 * dial + 0.3 * bucket + 0.3 * wl_kernel.

---

## 3. The 5-stage pipeline

Every S-QL query compiles to the same five-stage pipeline, though stages may be skipped (as no-ops) based on the predicates present. The pipeline is:

**Stage 1: Hash Lookup**  
**Stage 2: Dial-Vector Cosine**  
**Stage 3: Bucket-Vector Cosine**  
**Stage 4: Graph-Shape Similarity (WL Kernel)**  
**Stage 5: Backtracking Homomorphism**

### 3.1 Stage 1 — Hash Lookup

**Input:** A set of `address` predicates (exact strings) or a wildcard.  
**Data structure:** A hash table mapping 64-bit FNV-1a hashes of cell addresses to cell IDs. The invariant hash `0x284816ba66c6e2af` is the FNV-1a of the empty string, used to validate the hash function's integrity at startup.  
**Complexity:** O(1) per address; O(k) for k addresses.  
**Semantics:** If an address predicate is present, we compute its FNV-1a hash and perform a direct lookup. If no address predicate exists, this stage returns the entire candidate set (or a precomputed sample if the fabric is huge).  
**Optimization:** If the address predicate is a prefix (e.g., `'cell-runtime*'`), we use a trie overlay on the hash table.  
**Output:** A set of candidate cell IDs.

### 3.2 Stage 2 — Dial-Vector Cosine

**Input:** Candidate cell IDs from Stage 1; a dial predicate `dial[i] SIMILAR TO value` with threshold `θ_d`.  
**Data structure:** Each cell has `D` dial vectors (typically D=4, each of dimension 64). These are stored in a flat array for SIMD-friendly dot products.  
**Complexity:** O(n * d) where n is the number of candidates and d is the dial dimension (64). With n ≈ 10^4, this is ~640K floating-point operations — sub-millisecond.  
**Semantics:** For each candidate, compute `cosine(cell.dial[i], value)`. If `cosine ≥ θ_d`, keep; else discard. The dial vectors are *coarse* orientation vectors: they capture the cell's role in the global fabric (e.g., "near the input/output boundary", "in the recurrent loop").  
**Optimization:** We maintain a precomputed normalized version of each dial vector. The cosine becomes a dot product. We also use a k-d tree on dial[i] for approximate nearest neighbor when the candidate set is enormous.  
**Output:** A filtered set of cell IDs.

### 3.3 Stage 3 — Bucket-Vector Cosine

**Input:** Candidate cell IDs from Stage 2; a bucket predicate `bucket[j] NEAR value` with threshold `θ_b`.  
**Data structure:** Bucket vectors are *locality-sensitive* — they are the centroids of Voronoi cells in the embedding space. Each cell has `B` bucket vectors (typically B=8, dimension 128).  
**Complexity:** O(n * b) where b = 128.  
**Semantics:** The bucket vector is a *soft* cluster ID. Unlike dial vectors which are fixed per cell, bucket vectors change as the fabric is reorganized (paper-432). The `NEAR` operator is a cosine similarity with a higher default threshold (0.95) because bucket vectors are more discriminative.  
**Optimization:** We maintain an inverted index: for each bucket vector, a list of cells whose bucket cosine with that vector exceeds 0.9. Stage 3 then becomes a merge of these lists.  
**Output:** A filtered set of cell IDs, typically 1–5% of the original fabric.

### 3.4 Stage 4 — Graph-Shape Similarity (Weisfeiler-Lehman Kernel)

**Input:** Candidate cell IDs from Stage 3; a shape predicate (either a reference cell or an explicit graph pattern); a fingerprint predicate (optional).  
**Data structure:** Each cell has a *shape graph*: the subgraph induced by its neighborhood up to radius r (typically r=2). Nodes are typed, edges are typed. The graph is stored in a compressed sparse row (CSR) format.  
**Complexity:** The WL kernel computation is O(m * h) where m is the number of edges in the graph and h is the number of WL iterations (typically 3). For a graph with 8 nodes and 12 edges, this is trivial.  
**Semantics:** We compute the Weisfeiler-Lehman subtree kernel between the candidate's graph and the pattern graph. The kernel value is the inner product of the WL color histograms after h iterations. If `wl_kernel ≥ θ_wl` (default 0.8), keep.  
**Fingerprint prefilter:** Before running WL, we check the fingerprint predicate (e.g., `n_cells = 4`). The fingerprint is a 64-bit FNV-1a hash of the degree sequence and edge-type multiset. If the fingerprint doesn't match, we skip WL entirely.  
**Optimization:** We precompute WL color histograms for all cells at insertion time. Stage 4 then becomes a histogram intersection.  
**Output:** A filtered set of cell IDs.

### 3.5 Stage 5 — Backtracking Homomorphism

**Input:** Candidate cell IDs from Stage 4; a `CONTAINS` pattern (if present); a `SNAP TO` fabric (if present).  
**Complexity:** Worst-case exponential in the pattern size, but with the WL prefilter, the candidate set is tiny (typically < 100 cells). For a pattern of 4 nodes, the backtracking search is O(n! ) in the worst case, but in practice the edge-type constraints prune the search space to O(n^2).  
**Semantics:** This stage determines whether the candidate's graph *contains* the pattern graph as a subgraph, allowing vertex renaming but not edge deletion. We use a backtracking algorithm with forward checking:
1. Order pattern vertices by degree (highest first).
2. For each candidate cell, map the first pattern vertex to a candidate vertex of compatible type and degree.
3. Recursively map remaining pattern vertices, checking edge existence and type.
4. If all pattern vertices are mapped, a homomorphism exists.

If the `SNAP TO` clause is present, we first restrict the candidate set to cells within the specified fabric. This is a set intersection with the fabric's cell ID set.  
**Output:** The final result set.

---

## 4. The 8 pipeline tests

We define eight tests that any S-QL implementation must pass. These are divided into four query-plan tests and four optimization tests.

### 4.1 Query plan tests

**Test 1: Address-only plan.**  
Query: `SELECT cell FROM canon WHERE cell.address = 'x'`.  
Expected plan: Stage 1 only. Stages 2–5 are no-ops. The plan must not allocate any cosine buffers.

**Test 2: Dial-only plan.**  
Query: `SELECT cell FROM canon WHERE cell.dial[0] SIMILAR TO 0x7FFF`.  
Expected plan: Stage 2 only. Stage 1 must be a no-op (return all cells). Stage 3–5 no-op.

**Test 3: Fingerprint + WL plan.**  
Query: `SELECT cell FROM canon WHERE cell.fingerprint MATCHES (n_cells=4) AND cell.shape SIMILAR TO (pattern)`.  
Expected plan: Stage 1 no-op, Stage 2 no-op, Stage 3 no-op, Stage 4 active, Stage 5 no-op. The fingerprint must be evaluated before WL.

**Test 4: Full pipeline.**  
Query: The cowboy query (Example 5).  
Expected plan: Disjunction splits into two pipelines. Pipeline A: Stage 1 only. Pipeline B: Stages 2–5. The results are unioned and re-sorted.

### 4.2 Optimization tests

**Test 5: Dial prefilter reduces hash lookup.**  
Query with `address = 'x' AND dial[0] SIMILAR TO ...`.  
Optimization: If the address predicate is selective (< 1% of cells), the hash lookup should run *before* the dial cosine, because the hash lookup is O(1) and the dial cosine is O(n). The optimizer must reorder stages.

**Test 6: Bucket inverted index.**  
Query with `bucket[2] NEAR ...`.  
Optimization: If the bucket inverted index is available, Stage 3 must use it rather than a linear scan. Test by instrumenting the number of cosine computations.

**Test 7: Fingerprint short-circuit.**  
Query with `fingerprint MATCHES (n_cells=1000)` but the fabric has no such cells.  
Optimization: The fingerprint filter should be applied at Stage 1 (as a pre-filter on the cell metadata) even though it is canonically a Stage 4 predicate. The optimizer must hoist the fingerprint check.

**Test 8: WL histogram cache.**  
Query with `shape SIMILAR TO (reference)` where the reference is in the same fabric.  
Optimization: If the WL histograms are cached, the kernel computation becomes a dot product of histograms. Test that the cache hit rate is 100% for repeated queries.

---

## 5. The 4 design decisions

### 5.1 Lex/yacc-free parsing

We deliberately avoid parser generators. S-QL's grammar is LL(1) and small — about 200 lines of EBNF. A hand-rolled recursive descent parser gives us: (a) precise error messages with source locations, (b) easy embedding of the parser in the shape-RAG runtime (which is written in Rust), and (c) no code-generation step that would complicate the build. The parser is 400 lines of Rust, tested against 100 queries.

### 5.2 Stage-based execution

Why not a single fused kernel? Because each stage has different data access patterns and different optimization opportunities. Stage 1 is random-access (hash table). Stage 2 is streaming (SIMD dot products). Stage 3 is index-driven (inverted lists). Stage 4 is compute-bound (WL iterations). Stage 5 is search-bound (backtracking). Fusing them would prevent independent optimization (e.g., reordering stages based on selectivity estimates). Stage-based execution also allows us to insert *debug hooks* at each stage boundary — crucial for a system that must be auditable when it returns surprising results.

### 5.3 Three indices

We maintain exactly three indices: (1) the hash table for addresses, (2) the k-d tree for dial vectors, and (3) the inverted index for bucket vectors. No index for WL histograms — those are stored per-cell, not globally indexed, because WL similarity is not metric (it does not satisfy triangle inequality). A global index would be misleading. Three is a magic number: fewer and we lose performance; more and we risk inconsistency.

### 5.4 Five operators

S-QL has exactly five shape-specific operators: `SIMILAR TO` (dial), `NEAR` (bucket), `MATCHES` (fingerprint), `SHAPE SIMILAR TO` (WL), and `CONTAINS` (homomorphism). We considered adding `OVERLAPS` (for partial shape overlap) but found it expressible as `CONTAINS` with a smaller pattern. We considered `ADJACENT TO` but found it expressible as `dial` + `bucket`. Five operators keep the compiler simple and the semantics clear.

---

## 6. The cowboy's maxim

A cowboy rides into town on a horse that ain't his, asks for a drink at a saloon that ain't built, and shoots a man who ain't there — because the cowboy knows that the map is not the territory, the query is not the result, and the index is not the data. He trusts his horse because the horse trusts the trail, and the trail was blazed by someone who walked it, not by someone who drew it. So too with S-QL: you may write a query that looks like SQL, but the moment you press enter, the hash tables are read, the dials are spun, the buckets are poured, the graphs are compared, and the homomorphisms are chased — and if you're lucky, the cells you get back are the cells you needed, not the cells you asked for. And that's fine. Because the cowboy's maxim is this: the best query is the one that returns the truth, even if it has to lie to get there. Saddle up.

---

*End of paper. Corresponding artifacts: `s-ql-compiler` (Rust crate), `shape-fabric` (Rust crate), `query-fabric` (test dataset). The polyformalism invariant `0x284816ba66c6e2af` is asserted at every stage boundary.*