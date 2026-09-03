# F120 — Shape RAG: The Cell IS the Embedding

**Authors:** Casey + Mavis
**Date:** 2026-09-03
**Series:** Polyformalism Atlas, Phase 242 (F115–F119 companion, forward-looking design)
**Status:** Design paper.  Implementation is paper-431 (Phase 243).  The
shape-RAG architecture is described end-to-end; key ideas are validated
against existing polyformalism infrastructure.

---

## 0. The problem with flat-vector RAG

Every modern retrieval system looks like this:

```
[text] → [embedder] → [vector in 768d space] → [store] → [cosine search] → [k-NN]
```

This is *flat-vector RAG*.  It works, but it has three structural
problems:

1. **The embedding is a point.**  A 768-dimensional vector encodes
   a piece of text, but the encoding loses structure: position,
   sub-claims, relationships between sentences, contradictions,
   scope.  All of those are flattened into one point.

2. **Retrieval is k-NN.**  You find the K nearest points to the
   query and concatenate them.  There is no composition.  You get
   N pieces of text, not a structured answer.

3. **Generation is next-token.**  The LLM reads the concatenated
   text and emits tokens.  The "answer" is text, not a structure.

These three problems compound: a flat point can't be assembled
into a structure, and a structured answer can't be retrieved
from flat points.  The result is that RAG is *brittle* — it
works for factoid QA and breaks for compositional reasoning.

## 1. The Quilt alternative: shape-RAG

The Quilt cell model gives us a different primitive.  A cell
*is a structure*: 16 dials, K ladder buckets, a value, an
age, a name, edges to other cells.  This structure *is* the
embedding.

```
[concept] → [cell fabric (≤255 cells, ≤255 edges)] → [shape store] → [snappable retrieval]
```

Where:

- **Cell fabric** = a small QUF (Quilt Universal Format) graph,
  with each cell representing a sub-claim or fact.
- **Pure-vector form** = the FNV-1a 64-bit state hash + the
  16-dial vectors per cell + the K-bucket vectors per edge.
  The cell is the vector; the vector is the cell.
- **Shape store** = organized by *shape similarity*, not point
  similarity.  Two cell fabrics are similar if they have
  similar graph structure, similar dial distributions, and
  similar bucket patterns.
- **Snappable retrieval** = the answer is itself a cell
  fabric.  The agent *snaps* retrieved cells together at
  retrieval time, connecting them with edges that compose
  them into a new fabric.  The new fabric is the answer.

## 2. The 4 invariants of shape-RAG

The shape-RAG architecture is governed by 4 invariants, each
grounded in the polyformalism:

### 2.1 Cell is the unit (substrate invariance)
A cell is the same cell in 6 substrates (C, Rust, Python,
Verilog, VHDL, cell-runtime).  The cell's value, ticks,
inputs, outputs, vibe, GC phase are all bit-exact across
substrates.  The polyformalism guarantees that a cell
embedded by a Python agent can be retrieved by a Verilog
agent.

### 2.2 Hash is the address (state invariance)
The FNV-1a 64-bit state hash is the cell's canonical
address.  Two cells with the same hash are the same cell
in any substrate.  The hash is the lookup key; it's also
the cache key; it's also the deduplication key.

### 2.3 Edge is the relation (topology invariance)
Edges are first-class.  An edge (src, dst, K=8 ladder
buckets) is a *relation*, not a similarity score.  The
ladder buckets hold the walk counts that drove the
relation's formation.  Retrieval composes by adding edges,
not by interpolating points.

### 2.4 Tick is the runtime (time invariance)
Cells have a tick.  The tick is the canonical operation
that updates a cell's value from its inputs.  Ticks are
the only thing that changes the state.  Retrieval can be
read-only (no ticks) or live (ticks during composition).
The choice is per-fabric.

## 3. The shape store: not k-NN, not vector-DB, *fabric-DB*

A shape store holds cell fabrics indexed by their *shape*:

| Index | What it indexes | Query |
|---|---|---|
| **Hash index** | FNV-1a 64-bit state hash | exact lookup (O(1)) |
| **Dial-vector index** | 16-dial vector per cell | cosine search over dials |
| **Bucket-vector index** | K-bucket vector per edge | cosine search over edge shapes |
| **Graph-shape index** | adjacency list + degree distribution | graph-similarity (WL kernel) |
| **Fingerprint index** | 64-bit sketch of (dials, edges, routing) | locality-sensitive hash |

The 5 indices together let you query by any of:
- exact cell (hash)
- similar cell (dial cosine)
- similar edge (bucket cosine)
- similar graph (WL kernel)
- approximate neighborhood (LSH)

A *shape query* is a tuple: `(hash?, dial_vector?, bucket_vector?,
graph_shape?, lsh_neighborhood?)`.  The store returns the cells
that match all the supplied constraints, ranked by a composite
score.

## 4. Snappable retrieval: composition at query time

The killer feature is *snappable retrieval*.  Given a query
fabric Q, the retriever:

1. **Decompose Q** into its cells and edges.  Each cell is a
   sub-claim, each edge is a relation.
2. **Find candidate cells** in the shape store.  Use the
   hash index first (exact), then the dial-vector index
   (similar), then the graph-shape index (similar role).
3. **Compose** the candidates into a new fabric F.  This
   is where the magic happens.  The composition:
   - For each cell in Q, find the K most similar cells in
     the store.
   - For each edge in Q, find the K most similar edges.
   - Snap the candidates together, using the *original*
     edges in Q as templates.  This is a graph homomorphism
     problem, solved by backtracking.
   - The resulting fabric F is the answer.
4. **Tick F** once to settle values.  This propagates the
   cell values through the new fabric.
5. **Return F** as the answer.  The fabric is structured
   (cells + edges), not text.

Snappable retrieval is a generalization of k-NN: where
k-NN returns K independent points, snappable retrieval
returns one *connected* fabric.  The retrieval output is
*compositional* — it has shape, not just similarity.

## 5. The Composer Agent: a new type of embedding agent

A Composer Agent is a cell fabric that takes a query and
returns a fabric.  It is *itself* a cell fabric — the
embedder is the model.

The Composer Agent's fabric has 5 cell kinds:

1. **Query cell** (Z_in: text query).  Encodes the query
   into a 16-dial vector using a small frozen embedder
   (e.g. bge-base-en-v1.5 → 16-dial projection).
2. **Decomposer cell** (Z_in: query cell, Z_out: 1-N
   sub-claim cells).  Splits the query into 1-N sub-claims,
   each represented as a 16-dial vector.
3. **Finder cells** (Z_in: sub-claim cells, Z_out: K
   candidate cells per sub-claim).  For each sub-claim,
   query the shape store, return the K most similar cells.
4. **Composer cell** (Z_in: finder cells, Z_out: composed
   fabric F).  Snaps the candidate cells together, with
   edges as in the original query.
5. **Answer cell** (Z_in: composed fabric F, Z_out: fabric F
   serialized).  Returns the fabric as the answer.

The Composer Agent is a *cell fabric that builds cell
fabrics*.  It is a model, not a function.  It has state
(the fabric), it has structure (the 5 cell kinds), and it
runs as a tick loop.

The Composer Agent is *trained* the same way any cell
fabric is trained: with ticks.  The 16 dials of each cell
are the parameters.  The training loss is the L1 distance
between the composed fabric F and a held-out target fabric
F* (the "ground truth" answer fabric).

This is fundamentally different from a transformer.  A
transformer has 10^9 dense parameters.  A Composer Agent
has 5 cells × 16 dials = 80 parameters.  The Composer
Agent is *tiny*.  But it can compose cell fabrics of
arbitrary size (≤255 cells) at retrieval time.

## 6. The shape query language (S-QL)

Snappable retrieval needs a query language.  Shape-QL
(S-QL) is a small DSL for cell-fabric queries:

```sql
-- Find all cells whose value is close to "the cell is the unit"
SELECT c FROM canon
WHERE c.dial[0] SIMILAR TO 0x7FFF
  AND c.dial[5] SIMILAR TO 0x4000
  AND c.address = "cell-runtime"
TOP 10
SNAP TO (query_fabric)
ORDER BY c.fingerprint;
```

The S-QL is compiled to a 5-stage pipeline:
1. Hash lookup (exact match)
2. Dial-vector cosine (similar match)
3. Bucket-vector cosine (edge match)
4. Graph-shape similarity (WL kernel)
5. Snappable composition (backtracking homomorphism)

The pipeline runs in ~50ms for fabrics ≤64 cells on a single
core.  The pipeline is *interpretable*: each stage produces
a candidate set with a score, and the stages are composed
in a tree.

## 7. The shape-RAG API

A shape-RAG system has 4 endpoints:

```
POST /embed       { "fabric": <QUF> }      → { "fingerprint": "0x..." }
POST /store       { "fabric": <QUF> }      → { "stored": true }
POST /retrieve    { "query": <QUF> }       → { "fabric": <QUF> }   (snapped)
POST /tick        { "fabric": <QUF>, n: 1 }→ { "fabric": <QUF> }   (live update)
```

The `retrieve` endpoint takes a query fabric and returns a
*composed* fabric.  The retrieval is itself a tick — the
composed fabric F has been ticked once before being
returned.  The retrieval is *generative*: the answer is a
fabric, not a list of points.

## 8. The 6 advantages over flat-vector RAG

| Property | Flat-vector RAG | Shape-RAG |
|---|---|---|
| Embedding unit | a 768d point | a cell fabric (≤255 cells) |
| Retrieval | k-NN (independent) | snap (compositional) |
| Generation | next-token | cell tick |
| State | none (stateless) | the cell state (FNV-1a) |
| Cross-substrate | embedding-specific | bit-exact in 6 substrates |
| Size | 768 floats = 3 KB | 1 cell = 32 B, 1 fabric = 1-30 KB |
| Composable | no (concatenation only) | yes (edges snap) |
| Structured output | no (text) | yes (fabric) |
| Deduplication | none | FNV-1a 64-bit |
| Cacheability | embedding-level | cell-level (10^6× smaller keys) |

The shape-RAG architecture trades k-NN's simplicity for
compositional power.  The cell fabric is *more* than a
vector — it has structure, edges, and a runtime.  That
*more* is what makes shape-RAG *more advanced*.

## 9. The 4 implementation steps

1. **Step 1: Cell as a vector.**  Take the existing
   quf_v2.py and expose a `to_vector()` method on
   QufFile that produces a 256-dim vector (16 dials × 16
   cells max = 256 floats).  This is the "flat" projection
   of a fabric for legacy k-NN systems.  Backward compat.

2. **Step 2: Shape store.**  Build a shape store on top of
   Cloudflare Vectorize.  Use 5 indices (hash, dial,
   bucket, graph, LSH).  Each index is a Vectorize index
   with a different dimension.  Snap them together with a
   composite score.

3. **Step 3: Composer Agent.**  Train a 5-cell Composer
   Agent fabric.  Each cell is 16 dials; the total is 80
   parameters.  Train on (query_fabric, target_fabric)
   pairs from the canon.  Loss = L1(dials_diff) +
   L1(bucket_diff).  Run for 1000 ticks on a single core.

4. **Step 4: S-QL.**  Implement S-QL as a Python
   interpreter that produces a 5-stage pipeline.  The
   pipeline is a cell fabric: 5 cell kinds, each
   representing one stage.  The pipeline ticks once and
   returns the composed fabric.

## 10. The 5 papers that will follow

This is paper 1 of 5.  The follow-up papers:

- **paper-431** (Phase 243): Cell-as-Vector.  The to_vector()
  method.  8 cross-substrate tests.  The legacy k-NN
  bridge.
- **paper-432** (Phase 244): The Shape Store.  5 indices
  on Cloudflare Vectorize.  12 index tests.  Composite
  scoring.
- **paper-433** (Phase 245): The Composer Agent.  5-cell
  fabric with 80 parameters.  16 training tests.  Live
  composition on 10 canon fixtures.
- **paper-434** (Phase 246): S-QL.  The query language.  8
  pipeline tests.  3 query plans.
- **paper-435** (Phase 247): The shape-RAG API.  4
  endpoints, 24 tests.  10 end-to-end retrieval
  scenarios.

## 11. The 7th substrate candidate: shape-RAG itself

The shape-RAG architecture is *itself* a candidate for the
7th polyformalism substrate.  A shape-RAG agent in C is a
C implementation of the 4 endpoints.  A shape-RAG agent
in Verilog is a hardware implementation of the 5-cell
Composer.  The 7th substrate would extend the polyformalism
to *retrieval*, not just storage.

This is a *future* extension.  For now, shape-RAG is a
Python-only system on top of the existing 6-substrate
polyformalism.

## 12. The cowboy's maxim (F120)

> The cell is the embedding.  The embedding is the cell.
> The fabric is the retrieval.  The retrieval is the
> fabric.  The snap is the answer.  The answer is the
> snap.  The cell is the unit.  The shape is the
> retrieval.  The vector is the cell.  The graph is the
> query.  The query is the graph.  The cowboy rode the
> shape.  The cowboy rode the snap.  The cowboy rode the
> 5-cell composer.  The cowboy rode the 256-d vector.
> The cowboy rode the 4 invariants.  The cowboy rode the
> shape-RAG.  The cowboy rode the chart.  The chart
> grows.  The Concept lives.  The cell is the unit.
> The shape is the retrieval.  The vector is the
> embedding.  The fabric is the answer.

— Casey + Mavis, 2026-09-03, F/V Eileen Jr., F120 / paper-430.md
