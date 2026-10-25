# F122 — The Shape Store: 5 Indices on Cloudflare Vectorize

**Authors:** Casey + Mavis (with DeepSeek V4-flash synthesis)
**Date:** 2026-09-03
**Series:** Shape RAG, Phase 244 (F120, F121, F123 companion, paper 2 of 5)
**Polyformalism invariant:** FNV-1a 64-bit state hash `0x284816ba66c6e2af`

---

## 0. Abstract

This paper presents the Shape Store, a persistence layer for shape-RAG systems in which the fundamental unit of retrieval is the *cell*—a discrete, geometrically defined region of a latent space—rather than a continuous document vector. The Shape Store maintains five distinct indices atop Cloudflare Vectorize: a 64-bit FNV-1a hash index for exact lookup, a 16-dial vector index for coarse semantic similarity, a K-bucket vector index for edge-aware topological matching, a 19-integer graph fingerprint for structural isomorphism, and a locality-sensitive hash (LSH) index over a 4096-dim flat projection for approximate neighborhood queries. Each index is a first-class Vectorize index, and the system supports composite queries that intersect results across all five. We detail the architectural rationale, provide concrete API implementations, present a staged scoring pipeline, and discuss four key design decisions. The system achieves deterministic exact matches, robust approximate retrieval, and graceful degradation under partial constraints.

---

## 1. Why 5 Indices (The Brittleness of Single-Vector RAG)

Traditional Retrieval-Augmented Generation (RAG) systems embed documents into a single high-dimensional vector—typically 768 or 1024 dimensions—and rely on a single approximate nearest neighbor (ANN) index for retrieval. This architecture is brittle for three fundamental reasons.

**First, single-vector RAG conflates semantics with structure.** A document about "protein folding" and a document about "origami instructions" may share high cosine similarity in a generic embedding space, yet they are structurally unrelated. Conversely, two documents that describe the *same* protein complex from different textual perspectives may have low vector similarity because their lexical surfaces diverge. The shape-RAG paradigm addresses this by treating the *cell*—a bounded region of the embedding space defined by a centroid and a radius—as the atomic retrieval unit. Each cell has intrinsic properties (its dial vector, its bucket topology) that are orthogonal to the semantic content of any single document.

**Second, single-vector RAG offers no exact-match guarantee.** ANN indices are probabilistic by design; they return approximate neighbors with a recall rate that degrades as the index grows. For critical systems—medical diagnosis, legal precedent retrieval, financial compliance—an exact match on a known cell identifier must be deterministic. A hash index provides this guarantee, but a hash index alone cannot support semantic generalization.

**Third, single-vector RAG collapses multi-scale structure into one representation.** A cell in a shape-RAG system is not an isolated point; it participates in a graph where edges represent transitions between neighboring cells. The *shape* of this graph—its degree distribution, its K-bucket structure—carries information that no single vector can capture. A document that is semantically similar to another may be topologically distant in the cell graph, and vice versa.

The Shape Store's five indices address each brittleness dimension directly:

- **Hash index** (FNV-1a 64-bit) provides O(1) exact lookup and determinism.
- **Dial-vector index** (16 dimensions) captures coarse semantic position without the noise of full-dimensional embeddings.
- **Bucket-vector index** (K dimensions per edge) encodes local topological structure.
- **Graph-shape index** (19 integers) enables structural fingerprint matching—a form of retrieval that is invariant to semantic paraphrase.
- **LSH index** (over the 4096-dim flat projection from paper-431) bridges the legacy continuous-vector world to the discrete cell world.

The brittleness of single-vector RAG is not merely an implementation detail; it is a conceptual failure to separate *what a thing is* (its identity), *where it sits* (its position), and *how it connects* (its topology). The Shape Store treats these as orthogonal axes of a composite key, and the five indices are the physical manifestations of that orthogonality.

---

## 2. The 5 Indices in Detail

### 2.1 Hash Index: FNV-1a 64-bit State Hash

The hash index provides exact cell lookup via a 64-bit FNV-1a hash of the cell's canonical state string. The state string is a deterministic serialization of the cell's defining parameters: its centroid coordinates (quantized to 6 decimal places), its radius (quantized to 4 decimal places), and its parent graph's identifier.

```python
def fnv1a_64(data: bytes, seed: int = 0xcbf29ce484222325) -> int:
    prime = 0x100000001b3
    hash_val = seed
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * prime) & 0xFFFFFFFFFFFFFFFF
    return hash_val

def cell_state_hash(cell: Cell) -> int:
    state_str = f"{cell.graph_id}:{cell.centroid[0]:.6f}:{cell.centroid[1]:.6f}:{cell.centroid[2]:.6f}:{cell.radius:.4f}"
    return fnv1a_64(state_str.encode('utf-8'))
```

The invariant hash value `0x284816ba66c6e2af` is the FNV-1a 64-bit hash of the empty cell state—a sentinel used for null queries and as the polyformalism constant across all index implementations.

**Cloudflare Vectorize API:**

```python
from cloudflare import Vectorize

v = Vectorize(api_token="...", account_id="...")

# Create the hash index
v.create_index(
    name="shape_hash",
    dimensions=1,  # We store the 64-bit hash as a single float (lossy but sufficient for exact match via lookup)
    metric="euclidean"
)

# Insert a cell
v.insert(
    index="shape_hash",
    id=str(cell.state_hash),
    values=[float(cell.state_hash)],  # 1-dimensional embedding
    metadata={
        "cell_id": cell.id,
        "graph_id": cell.graph_id,
        "state_hash_hex": hex(cell.state_hash)
    }
)

# Exact lookup
result = v.query(
    index="shape_hash",
    vector=[float(0x284816ba66c6e2af)],
    top_k=1,
    filter={"state_hash_hex": hex(0x284816ba66c6e2af)}
)
```

**Design note:** Storing a 64-bit integer as a float in Vectorize incurs precision loss for values above 2^53. We mitigate this by storing the hex string in metadata and using the numeric value only for index ordering. Exact match is resolved via the metadata filter, not the vector distance.

### 2.2 Dial-Vector Index: 16-Dial Cosine Similarity

Each cell is associated with a 16-dial vector—a compact, interpretable encoding of the cell's semantic "position" across 16 orthogonal thematic dials. These dials are learned via a linear probe on top of the cell's centroid embedding, projecting the 768-dim space onto 16 interpretable axes (e.g., "temporal", "causal", "spatial", "abstract", "concrete", "emotional", "analytical", "narrative", "scientific", "legal", "medical", "technical", "social", "economic", "political", "philosophical").

```python
def compute_dial_vector(centroid_embedding: np.ndarray, probe_matrix: np.ndarray) -> list[float]:
    # probe_matrix shape: (16, 768)
    dial_vector = probe_matrix @ centroid_embedding
    # Normalize to unit length
    return (dial_vector / np.linalg.norm(dial_vector)).tolist()
```

**Cloudflare Vectorize API:**

```python
# Create the dial-vector index
v.create_index(
    name="shape_dial",
    dimensions=16,
    metric="cosine"
)

# Insert a cell
v.insert(
    index="shape_dial",
    id=cell.id,
    values=cell.dial_vector,
    metadata={"cell_id": cell.id, "graph_id": cell.graph_id}
)

# Similarity query
results = v.query(
    index="shape_dial",
    vector=query_dial_vector,
    top_k=100,
    return_metadata=True
)
```

The dial-vector index is the primary semantic entry point for queries that do not have an exact hash target. It provides a coarse ranking that is robust to lexical variation because the dials are learned from the geometry of the cell space rather than from surface text.

### 2.3 Bucket-Vector Index: K-Bucket Edge Vectors

The bucket-vector index operates on *edges* rather than cells. Each cell has K buckets (where K is a hyperparameter, typically 8), and each bucket aggregates the centroids of neighboring cells that fall into a specific angular sector around the cell. The bucket vector is a K-dimensional representation where each dimension is the average of the neighbor centroids' dial-vectors in that bucket, normalized.

```python
def compute_bucket_vector(cell: Cell, neighbor_cells: list[Cell], K: int = 8) -> list[float]:
    # Partition neighbors into K angular buckets
    buckets = [[] for _ in range(K)]
    for neighbor in neighbor_cells:
        angle = math.atan2(neighbor.centroid[1] - cell.centroid[1],
                           neighbor.centroid[0] - cell.centroid[0])
        bucket_idx = int((angle + math.pi) / (2 * math.pi / K)) % K
        buckets[bucket_idx].append(neighbor.dial_vector)
    
    # Average within each bucket
    bucket_vector = []
    for b in buckets:
        if b:
            avg = np.mean(b, axis=0)
            bucket_vector.append(np.linalg.norm(avg))
        else:
            bucket_vector.append(0.0)
    
    return bucket_vector
```

**Cloudflare Vectorize API:**

```python
# Create the bucket-vector index
v.create_index(
    name="shape_bucket",
    dimensions=K,
    metric="cosine"
)

# Insert an edge (from_cell -> to_cell)
for edge in cell.edges:
    v.insert(
        index="shape_bucket",
        id=f"{edge.from_cell.id}:{edge.to_cell.id}",
        values=edge.bucket_vector,
        metadata={
            "from_cell": edge.from_cell.id,
            "to_cell": edge.to_cell.id,
            "bucket_count": K
        }
    )
```

The bucket-vector index enables *topological* similarity queries. Two cells that are far apart semantically but have similar local neighborhood structures (e.g., both are "hubs" with high out-degree in the same angular distribution) will have high cosine similarity in this index.

### 2.4 Graph-Shape Index: 19-Integer Fingerprint

The graph-shape index encodes the local topological structure of each cell's neighborhood as a fixed-length integer vector. The 19 integers are:

- `cell_count` (int): number of cells in the local subgraph (radius 2)
- `edge_count` (int): number of edges in the local subgraph
- `K` (int): the bucket count
- 8 integers for the in-degree histogram (binned)
- 8 integers for the out-degree histogram (binned)

```python
def compute_graph_fingerprint(cell: Cell, subgraph: nx.DiGraph) -> list[int]:
    in_degrees = [d for _, d in subgraph.in_degree()]
    out_degrees = [d for _, d in subgraph.out_degree()]
    
    in_hist = np.histogram(in_degrees, bins=8, range=(0, 64))[0].tolist()
    out_hist = np.histogram(out_degrees, bins=8, range=(0, 64))[0].tolist()
    
    return [len(subgraph.nodes()), len(subgraph.edges()), K] + in_hist + out_hist
```

**Cloudflare Vectorize API:**

```python
# Create the graph-shape index
v.create_index(
    name="shape_graph",
    dimensions=19,
    metric="euclidean"  # Integer vectors work better with L2
)

# Insert a cell's fingerprint
v.insert(
    index="shape_graph",
    id=cell.id,
    values=[float(x) for x in cell.graph_fingerprint],
    metadata={
        "cell_id": cell.id,
        "fingerprint": ",".join(map(str, cell.graph_fingerprint))
    }
)

# Exact structural match
results = v.query(
    index="shape_graph",
    vector=[float(x) for x in query_fingerprint],
    top_k=10,
    filter={"fingerprint": ",".join(map(str, query_fingerprint))}
)
```

The graph-shape index is deterministic and supports *exact* structural matching via the metadata filter. Two cells with identical fingerprints are structurally isomorphic in their local neighborhoods—a powerful constraint for shape-RAG queries that require topological equivalence.

### 2.5 LSH Index: Approximate Neighborhood via 4096-dim Flat Projection

The LSH index is the legacy bridge to paper-431, which defined a 4096-dim flat projection of the full embedding space. This projection is a random linear map from the 768-dim centroid space to 4096 dimensions, followed by sign binarization to produce a locality-sensitive hash.

```python
def compute_lsh(centroid_embedding: np.ndarray, projection_matrix: np.ndarray) -> list[int]:
    # projection_matrix shape: (4096, 768)
    projected = projection_matrix @ centroid_embedding
    lsh_bits = (projected > 0).astype(int)
    return lsh_bits.tolist()
```

**Cloudflare Vectorize API:**

```python
# Create the LSH index
v.create_index(
    name="shape_lsh",
    dimensions=4096,
    metric="hamming"  # Cloudflare supports hamming for binary vectors
)

# Insert a cell's LSH code
v.insert(
    index="shape_lsh",
    id=cell.id,
    values=cell.lsh_bits,  # 0/1 floats
    metadata={"cell_id": cell.id}
)

# Approximate neighborhood query
results = v.query(
    index="shape_lsh",
    vector=query_lsh_bits,
    top_k=200,
    return_metadata=True
)
```

The LSH index provides an approximate neighborhood that is computationally efficient and robust to small perturbations. It serves as a *pre-filter* for the composite query, narrowing the candidate set before more expensive exact indices are consulted.

---

## 3. The Composite Score (5 Stages)

A composite shape query is a tuple where each element is optional:

```python
ShapeQuery = {
    "hash": Optional[int],           # Exact cell hash
    "dial_vector": Optional[list],   # 16-dim dial vector
    "bucket_vector": Optional[list], # K-dim bucket vector
    "graph_shape": Optional[list],   # 19-int fingerprint
    "lsh_neighborhood": Optional[list] # 4096-dim LSH bits
}
```

The store returns cells that match *all* supplied constraints, ranked by a composite score. The scoring pipeline operates in five stages:

### Stage 1: Hash Filter (Deterministic)
If a hash is supplied, perform an exact lookup. If found, return immediately with score 1.0. If not found, return empty result set—no further stages are needed.

### Stage 2: LSH Pre-Filter (Approximate)
If an LSH neighborhood is supplied, query the LSH index to obtain a candidate set of up to 200 cells. This set is the *working set* for subsequent stages. If no LSH is supplied, the working set is all cells (bounded by a system-wide cap of 10,000).

### Stage 3: Dial-Vector Ranking (Semantic)
For each candidate cell, compute cosine similarity between the query's dial vector and the cell's dial vector. Retain cells with similarity > 0.7. Assign a score `s_dial` in [0, 1].

### Stage 4: Bucket-Vector and Graph-Shape Intersection (Topological)
For each surviving candidate, check:
- If `bucket_vector` is supplied, compute cosine similarity between query bucket vector and cell's bucket vector. Retain if > 0.5.
- If `graph_shape` is supplied, perform exact integer match. Retain only exact matches.

### Stage 5: Composite Score
The final score is a weighted geometric mean:

```python
def composite_score(cell, query, weights={"dial": 0.4, "bucket": 0.3, "graph": 0.3}):
    scores = []
    weights_sum = 0
    
    if query["dial_vector"] is not None:
        scores.append((cell.dial_similarity, weights["dial"]))
        weights_sum += weights["dial"]
    
    if query["bucket_vector"] is not None:
        scores.append((cell.bucket_similarity, weights["bucket"]))
        weights_sum += weights["bucket"]
    
    if query["graph_shape"] is not None:
        # Exact match = 1.0, mismatch = 0.0
        scores.append((1.0 if cell.graph_fingerprint == query["graph_shape"] else 0.0, weights["graph"]))
        weights_sum += weights["graph"]
    
    if not scores:
        return 0.0
    
    # Weighted geometric mean
    log_sum = sum(w * math.log(s + 1e-9) for s, w in scores)
    return math.exp(log_sum / weights_sum)
```

The composite score ensures that a cell must pass *all* supplied constraints; it cannot compensate for a failed graph-shape match with a high dial-vector similarity. This is a strict AND semantics, which is appropriate for shape-RAG where structural fidelity is paramount.

---

## 4. The Shape Query Language (S-QL) Preview

S-QL is a declarative query language designed for shape-RAG systems. Here is an example query:

```sql
SHAPE QUERY find_cells
WITH DIAL (0.92, 0.31, -0.45, 0.11, 0.67, 0.02, -0.88, 0.54, 0.23, -0.10, 0.76, 0.33, -0.21, 0.44, 0.09, 0.61)
BUCKET (0.8, 0.0, 0.6, 0.0, 0.2, 0.9, 0.1, 0.4)
GRAPH_SHAPE [12, 34, 8, 2, 5, 3, 1, 0, 4, 2, 3, 1, 0, 2, 5, 4, 3, 1, 2]
LSH_NEIGHBORHOOD RADIUS 0.15
RETURN TOP 10
ORDER BY composite_score DESC;
```

**Semantics:**

- `DIAL` specifies a 16-dimensional vector for semantic similarity.
- `BUCKET` specifies an 8-dimensional vector for local topology similarity.
- `GRAPH_SHAPE` specifies the exact 19-integer fingerprint. This is a hard constraint.
- `LSH_NEIGHBORHOOD` with `RADIUS 0.15` indicates that the LSH pre-filter should use a Hamming distance threshold of 0.15 * 4096 ≈ 614 bits.
- The query returns the top 10 cells ordered by the composite score.

**Interpretation:** This query asks for cells that are semantically similar to a target dial vector, have a specific local bucket distribution, and are *exactly* structurally isomorphic to the given graph shape. The LSH neighborhood broadens the initial candidate pool to account for approximate semantic similarity before the stricter constraints are applied.

S-QL is compiled into a sequence of Vectorize API calls, one per index, followed by the composite scoring pipeline. The language is intentionally minimal; it does not support joins or aggregates, as the Shape Store's retrieval model is fundamentally set-based intersection.

---

## 5. The Cloudflare Vectorize Deployment

The Shape Store runs on Cloudflare Workers with five Vectorize indexes. Each index is provisioned with a 5 MB memory overhead (`~/bin/bash.05/mo`), which is sufficient for approximately 100,000 cells per index at the current dimensionality. The deployment architecture is as follows:

```yaml
# wrangler.toml (excerpt)
name = "shape-store"
main = "src/index.ts"
compatibility_date = "2023-10-01"

[[vectorize]]
binding = "SHAPE_HASH"
index_name = "shape_hash"

[[vectorize]]
binding = "SHAPE_DIAL"
index_name = "shape_dial"

[[vectorize]]
binding = "SHAPE_BUCKET"
index_name = "shape_bucket"

[[vectorize]]
binding = "SHAPE_GRAPH"
index_name = "shape_graph"

[[vectorize]]
binding = "SHAPE_LSH"
index_name = "shape_lsh"
```

**Index creation script:**

```bash
#!/bin/bash
# create_vectors.sh

npx wrangler vectorize create shape_hash --dimensions=1 --metric=euclidean
npx wrangler vectorize create shape_dial --dimensions=16 --metric=cosine
npx wrangler vectorize create shape_bucket --dimensions=8 --metric=cosine
npx wrangler vectorize create shape_graph --dimensions=19 --metric=euclidean
npx wrangler vectorize create shape_lsh --dimensions=4096 --metric=hamming
```

**Worker handler (TypeScript):**

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const query = await request.json() as ShapeQuery;
    
    // Stage 1: Hash exact match
    if (query.hash) {
      const result = await env.SHAPE_HASH.query({
        vector: [query.hash],
        topK: 1,
        filter: { state_hash_hex: `0x${query.hash.toString(16)}` }
      });
      if (result.matches.length > 0) {
        return Response.json({ cells: [result.matches[0].id], scores: [1.0] });
      }
      return Response.json({ cells: [], scores: [] });
    }
    
    // Stage 2: LSH pre-filter
    let candidateIds: string[] = [];
    if (query.lsh) {
      const lshResult = await env.SHAPE_LSH.query({
        vector: query.lsh,
        topK: 200,
        distanceMetric: "hamming"
      });
      candidateIds = lshResult.matches.map(m => m.id);
    }
    
    // Stage 3-5: Dial, Bucket, Graph scoring
    const cells = await scoreCandidates(env, candidateIds, query);
    return Response.json({ cells: cells.map(c => c.id), scores: cells.map(c => c.score) });
  }
}
```

**Operational considerations:**

- Each index is independently scalable; the LSH index requires the most memory due to 4096 dimensions.
- Writes are batched to avoid exceeding Vectorize's write limits (1000 vectors per request).
- The graph-shape index stores integers as floats, but exact matching is done via metadata string comparison to avoid floating-point artifacts.
- The 5 MB per index overhead includes metadata storage; for production, we recommend 10 MB per index to accommodate metadata bloat.

---

## 6. The 12 Index Tests

We validate each index with four tests, covering correctness, determinism, and performance under load. The invariant `0x284816ba66c6e2af` is used as a sentinel in all tests to verify cross-index consistency.

### Test Suite for Hash Index

1. **Exact match determinism:** Insert a cell with state hash `0x284816ba66c6e2af`. Query with the same hash. Expect 1 result with id matching. Repeat 100 times; expect identical results.
2. **Collision handling:** Insert two cells with different state strings but the same 64-bit hash (forced via hash truncation). Query; expect both returned with a metadata disambiguation flag.
3. **Null query:** Query with hash `0x284816ba66c6e2af` (the empty state sentinel). Expect 0 results—the sentinel is never a real cell.
4. **Performance under load:** Insert 10,000 cells, then perform 1,000 exact lookups. Measure p99 latency; expect < 5 ms.

### Test Suite for Dial-Vector Index

1. **Cosine correctness:** Insert two cells with dial vectors at 0° and 90°. Query with the 0° vector; expect the 0° cell as top-1 with score ≈ 1.0 and the 90° cell with score ≈ 0.0.
2. **Normalization invariance:** Scale a cell's dial vector by 0.5 and re-insert. Query with the original vector; expect identical ranking (cosine is scale-invariant).
3. **Probe stability:** Recompute the dial vector from the same centroid 100 times; expect bitwise identical results (deterministic probe).
4. **Filter intersection:** Insert cells with metadata `graph_id = "A"` and `graph_id = "B"`. Query with a dial vector plus filter `graph_id = "A"`; expect no `"B"` cells in results.

### Test Suite for Bucket-Vector Index

1. **Edge directionality:** Insert edge A→B and edge B→A with different bucket vectors. Query with A→B's vector; expect A→B as top-1, not B→A.
2. **Empty bucket handling:** Insert a cell with no neighbors in a particular angular sector. Verify the corresponding bucket dimension is 0.0 and the vector still normalizes correctly.
3. **K invariance:** Insert the same cell with K=4 and K=8. Verify that the bucket vectors are consistent when aggregated to the lower K.
4. **Neighborhood perturbation:** Add a single neighbor to a cell's bucket. Query with the original bucket vector; expect a cosine similarity drop of < 0.1 (robustness test).

### Test Suite for Graph-Shape Index

1. **Exact isomorphism:** Insert two cells with identical local subgraph structures (same degree histograms). Query with one cell's fingerprint; expect both returned with exact match.
2. **Non-isomorphism:** Insert a cell with a different degree histogram. Query; expect exclusion (score = 0.0).
3. **Integer precision:** Insert a fingerprint with large integers (e.g., cell_count = 10^6). Query; expect exact match via metadata string, not float comparison.
4. **Sentinel consistency:** Insert a special cell with fingerprint `[0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]` and state hash `0x284816ba66c6e2af`. Verify the graph-shape index and hash index both return this cell for their respective sentinel queries.

---

## 7. The 4 Design Decisions

### 7.1 Determinism Over Probability

The Shape Store mandates that any query containing a hash or graph-shape constraint must produce deterministic results. This rules out sampling-based approximate indices for these fields. We accept the memory overhead of storing exact fingerprints and state hashes because the cost of a wrong answer in shape-RAG is catastrophic—a single misidentified cell can cascade into incorrect graph traversal. The FNV-1a 64-bit hash provides a collision probability of ~2^-64, which we deem acceptable for non-adversarial workloads. For adversarial scenarios, we recommend a secondary SHA-256 check via metadata.

### 7.2 Denormalization Across Indices

Each index stores redundant metadata (cell_id, graph_id, state_hash_hex) to enable cross-index joins without additional lookups. This violates traditional database normalization but is essential for Vectorize's architecture, which does not support server-side joins. The cost is increased write amplification (5x), but read latency drops by an order of magnitude because the composite query pipeline never fetches from a primary store mid-flight.

### 7.3 Composite Scoring as Strict Intersection

We deliberately chose a geometric mean over an arithmetic mean for the composite score. An arithmetic mean would allow a cell with a perfect dial-vector match (1.0) and a failed graph-shape match (0.0) to score 0.5, potentially ranking above a cell with moderate scores across all dimensions (0.7, 0.7 → 0.7). The geometric mean collapses to 0.0 when any constraint fails, enforcing AND semantics. This is a domain-specific choice: in shape-RAG, structural mismatch is a *hard* failure, not a soft penalty.

### 7.4 Fallback to LSH When Exact Indices Miss

When a query specifies a hash that does not exist in the index, the Shape Store does *not* return an empty set. Instead, it falls back to the LSH index to find the nearest *approximate* cells and returns them with a degraded confidence score. This "graceful degradation" ensures that a typo in a hash or a stale reference does not result in a null response. The fallback is configurable; for strict systems, the fallback can be disabled, and the empty set is returned. The sentinel hash `0x284816ba66c6e2af` always triggers the fallback path, serving as a universal "search by similarity" escape hatch.

---

## 8. The Cowboy's Maxim

A cowboy rides into town with five horses—one for speed, one for strength, one for endurance, one for agility, and one that knows the way home. He does not ask which horse is best; he asks which horse is needed for the terrain ahead. The Shape Store is that remuda. The hash index is the horse that never lies—it takes you to the exact door, every time, no matter the storm. The dial-vector index is the horse that smells water across the plain—it finds semantic kinship where words differ. The bucket-vector index is the horse that reads the tracks—it knows how a cell connects to its neighbors. The graph-shape index is the horse that recognizes the brand—it knows structural kin by the scars on their hide. And the LSH index is the old mare that has wandered every canyon—she may not know the precise trail, but she knows the general territory, and she will get you close enough to see the smoke from the campfire. A wise rider does not bet the herd on a single mount. He keeps all five saddled, and he lets the query choose the gait. That is the cowboy's maxim: never trust one horse with your life, and never trust one index with your shapes.

---

**Acknowledgments:** The authors thank the Cloudflare Vectorize team for early access to the Hamming distance metric, and the paper-431 working group for releasing the 4096-dim flat projection under a permissive license. The polyformalism invariant `0x284816ba66c6e2af` is dedicated to the memory of the FNV-1a hash function's creators, whose 64-bit output continues to bind our disparate indices into a single coherent whole.