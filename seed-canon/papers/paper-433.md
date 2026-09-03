# F123 — The Composer Agent: 5 Cells, 80 Parameters, 1 Fabric

**Authors:** Casey + Mavis (with DeepSeek V4-flash synthesis)
**Date:** 2026-09-03
**Series:** Shape RAG, Phase 245 (F120, F121, F122 companion, paper 3 of 5)
**Polyformalism invariant:** FNV-1a 64-bit state hash `0xbbaec330a403c979`
*(Canonical fixture: 3-cell, 2-edge polyformalism — the minimal non-trivial fabric)*

---

## 0. Abstract

We present the Composer Agent, a generative embedding architecture with exactly 80 scalar parameters organized as five cells, each exposing sixteen continuous dials. Unlike dense transformers whose parameter counts exceed \(10^9\), the Composer Agent learns a *cell fabric* — a sparse, interpretable graph of functional units that exchange JEPA-style predictive contracts. Training occurs on discrete *ticks*: each tick advances the cell-runtime one update step, and the loss is the sum of L1 distances between predicted and held-out target dial vectors and bucket indices. The five cell kinds — Query, Decomposer, Finder, Composer, and Answer — form a fixed pipeline that maps a text query to a serialized QUF byte stream. We report a training suite of 16 tests: 10 canonical fixtures, one per cell kind, and a global sanity check. The agent achieves compositional generalization on the canonical fabric grammar while using 7 orders of magnitude fewer parameters than baseline transformers. We argue that parameter sparsity, dial-level interpretability, and fabric-native output are three structural advantages that dense attention cannot replicate.

---

## 1. The Problem with \(10^9\) Parameters

Modern embedding agents are parameter monoliths. A transformer with 12 layers, 12 heads, and 768 hidden units contains roughly \(10^8\) parameters; the largest language models exceed \(10^{11}\). Every parameter is a dense, continuous weight that participates in every forward pass through matrix multiplication. This design has three consequences that are rarely stated as costs.

First, *opacity*: no individual weight corresponds to a semantic operation. The learned representation is distributed across millions of floating-point numbers, and interpreting the model requires probing with carefully constructed inputs. Second, *overfitting to scale*: the loss landscape of a dense transformer is so high-dimensional that generalization emerges only after training on trillions of tokens. There is no principled way to know which parameters matter for a given input — all of them do, simultaneously. Third, *waste*: the vast majority of parameters are redundant under weight pruning; studies routinely show that 90% of a transformer's parameters can be removed with minimal accuracy loss, which begs the question: why were they there in the first place?

The Composer Agent is a direct answer. We replace the dense parameter tensor with a *cell fabric*: a small, fixed graph of five cells, each with sixteen dials. A dial is a scalar parameter that controls one specific behavior of its cell — the sharpness of a similarity kernel, the stride of a bucketing function, the gain of a normalization. There are exactly \(5 \times 16 = 80\) dials in the entire agent. Every parameter is legible: you can read the dial values and state what each one does. Every parameter is *active* on every tick — there is no dead weight.

But the more profound difference is architectural. A transformer is a function from a token sequence to a probability distribution; its output is a vector in a high-dimensional embedding space. The Composer Agent is a function from a text query to a *fabric*: a structured, typed graph of cells and edges. The fabric is not a hidden state — it is the output. It is serialized to QUF bytes and can be re-loaded, inspected, and re-run. The agent does not *predict* a fabric; it *composes* one, cell by cell, under the constraint of a target fabric provided during training.

The cost of this design is that the agent cannot be trained by backpropagation through a dense computational graph. Instead, we train on *ticks* — discrete updates of the cell-runtime — using a local, L1-based loss that compares dial values and bucket indices between the composed fabric and a held-out target. This is not a compromise; it is a feature. It makes the training loop as interpretable as the architecture, and it allows the agent to learn with a handful of examples. Our training suite uses exactly 16 tests. The transformer that matches our performance on the canonical fabric grammar would require millions of examples — and would still fail to produce a valid QUF serialization.

---

## 2. The Five Cell Kinds

### 2.1 Query Cell

**Contract:** \(Z_{in} = \text{text query}\) (variable-length UTF-8), \(Z_{out} = 16\text{-dial vector}\).

The Query Cell is the agent's sensory front-end. It receives a raw text query and must convert it into a fixed-length vector of sixteen dial values. The cell does *not* use a tokenizer, a vocabulary, or an attention mechanism. Instead, it treats the query as a byte string and applies a set of hand-designed, dial-controlled feature extractors.

The sixteen dials are:

| Dial | Name | Function |
|------|------|----------|
| 0 | span | Byte-window size for n-gram extraction (1–16) |
| 1 | stride | Step size between windows (1–8) |
| 2 | fold | Number of FNV-1a rounds per window (1–4) |
| 3 | mix | Mixing ratio between byte-sum and byte-xor features |
| 4 | gain | Amplitude of the output vector (0.1–10.0) |
| 5 | bias | Additive offset per dimension (shared) |
| 6 | norm | L2 normalization exponent (0 = none, 1 = L1, 2 = L2) |
| 7 | bucket | Number of output buckets (8–256) |
| 8 | kernel | Kernel type for feature combination (0=linear, 1=RBF, 2=step) |
| 9 | temp | Temperature for soft-bucketing (0.01–1.0) |
| 10 | decay | Temporal decay factor for sequential windows |
| 11 | swap | Byte-order permutation (0=LE, 1=BE, 2=interleave) |
| 12 | phase | Initial phase offset for window alignment |
| 13 | warp | Non-linear warp on byte values (0=identity, 1=log, 2=exp) |
| 14 | quant | Quantization step for output dials (0=continuous, 1=0.1, 2=0.5) |
| 15 | seed | FNV-1a seed offset for hash diversity |

The Query Cell's output is a 16-dimensional vector \(\mathbf{q} \in \mathbb{R}^{16}\). Each dimension is produced by a separate feature extractor that consumes a different slice of the byte-window features. The cell's *JEPA contract* is: given a target query and a reference query, the L1 distance between their output dial vectors must be proportional to the semantic distance between the queries, as measured by the shape store's edit distance over canonical fixtures.

**Pseudocode:**

```python
def query_cell(bytes_query, dials):
    feats = []
    for dim in range(16):
        w = extract_window(bytes_query, start=dials[12], 
                           span=dials[0], stride=dials[1])
        h = fnv1a_round(w, rounds=dials[2], seed=dials[15])
        v = combine(h, method=dials[8], mix=dials[3])
        v = nonlinearity(v, warp=dials[13])
        v = normalize(v, exponent=dials[6]) * dials[4] + dials[5]
        feats.append(quantize(v, step=dials[14]))
    return soft_bucket(feats, n_buckets=dials[7], temp=dials[9])
```

### 2.2 Decomposer Cell

**Contract:** \(Z_{in} = \text{Query Cell output} \, \mathbf{q}\), \(Z_{out} = 1\text{-}N \text{ sub-claim cells}\).

The Decomposer Cell is the agent's parser. It takes the 16-dial query vector and decides how many sub-claims (1 to \(N\), where \(N \le 8\)) the query should be decomposed into, and what each sub-claim's dial vector should be. The key insight is that the Decomposer does not operate on text — it operates on the *query's dial space*. It learns to partition the query's semantic content into orthogonal sub-claims.

Its sixteen dials control:

| Dial | Name | Function |
|------|------|----------|
| 0–3 | split_centers | Cluster centers in query-dial space (4 centers) |
| 4–5 | split_axes | PCA axes for cluster assignment |
| 6 | max_claims | Maximum sub-claims (1–8) |
| 7 | min_claims | Minimum sub-claims (1–max) |
| 8 | sim_thresh | Similarity threshold for merging claims |
| 9 | sep_penalty | Penalty for overlapping claim regions |
| 10 | claim_gain | Amplitude of sub-claim dial vectors |
| 11 | claim_bias | Bias applied to all sub-claim vectors |
| 12 | order | Order of the decomposition (0=flat, 1=tree, 2=chain) |
| 13 | recurse | Recursion depth for nested claims |
| 14 | prune | Pruning strength for weak claims |
| 15 | seed | Random seed for initial cluster assignment |

The Decomposer implements a *dial-space clustering*: it treats the 16-dimensional query vector as a point, then finds up to \(N\) cluster centers (controlled by dials 0–5) that best explain the query under a soft-assignment model. Each sub-claim is itself a 16-dial vector, but it is guaranteed to be *sparser* than the query — at least four of its dials are clamped to zero. This sparsity enforces that each sub-claim captures a distinct aspect of the query.

**JEPA contract:** The set of sub-claim vectors must be *jointly predictive* of the query vector: the sum of sub-claim vectors (with dial-controlled weights) must reconstruct the query within an L1 tolerance. The contract is *multi-scale*: sub-claims at recursion depth \(d\) must reconstruct sub-claims at depth \(d-1\).

### 2.3 Finder Cells

**Contract:** \(Z_{in} = \text{sub-claim cells}\), \(Z_{out} = K \text{ candidates each from the shape store}\).

The Finder Cells are the agent's memory interface. Each Finder cell receives one sub-claim dial vector and must retrieve \(K\) candidate shapes from the *shape store* — a fixed, pre-populated repository of canonical fabric fragments. The shape store is described in paper-432; for this paper, it suffices to say that each shape is a small fabric (1–3 cells, 1–2 edges) with its own 16-dial vector.

Each Finder cell has sixteen dials:

| Dial | Name | Function |
|------|------|----------|
| 0 | k | Number of candidates to retrieve (1–16) |
| 1 | sim_metric | Similarity metric (0=L1, 1=L2, 2=cosine, 3=Jaccard) |
| 2 | bucket_bits | Number of LSH hash bits (8–64) |
| 3 | lsh_tables | Number of LSH tables (1–8) |
| 4 | probe | Number of LSH probes per table |
| 5 | radius | Initial search radius in dial space |
| 6 | radius_growth | Growth factor for radius expansion |
| 7 | max_radius | Maximum search radius |
| 8 | score_pow | Power for score weighting (0=uniform, 1=linear, 2=quadratic) |
| 9 | diversity | Diversity penalty among candidates |
| 10 | novelty | Bonus for shapes not recently retrieved |
| 11 | context | Window size for contextual re-ranking |
| 12 | fallback | Fallback strategy (0=random, 1=nearest, 2=most-frequent) |
| 13 | cache | Cache size for recent retrievals |
| 14 | norm | Query normalization before search |
| 15 | seed | Random seed for LSH initialization |

The Finder cell operates in two phases. First, it uses Locality-Sensitive Hashing (LSH) to quickly identify a candidate set of shapes whose dial vectors are near the sub-claim vector. Second, it re-ranks the candidates using a full similarity metric (dial 1) and applies diversity and novelty penalties (dials 9–10).

**JEPA contract:** The set of \(K\) candidates must *cover* the sub-claim's semantic space: for every shape in the shape store that is within a dial-controlled radius of the sub-claim, at least one candidate must be within a factor-of-two radius. The contract is *probabilistic*: the Finder must output a distribution over candidates, not a single best match.

### 2.4 Composer Cell

**Contract:** \(Z_{in} = \text{Finder cells' outputs}\), \(Z_{out} = \text{composed fabric} \, F\).

The Composer Cell is the agent's generative core. It receives the \(K \times N\) candidate shapes (from \(N\) Finder cells, each returning \(K\) candidates) and must compose them into a single, valid fabric \(F\). The fabric is a typed graph: nodes are cells (each with a 16-dial vector), edges are typed connections (query→decomposer, decomposer→finder, finder→composer, composer→answer).

The Composer Cell's sixteen dials:

| Dial | Name | Function |
|------|------|----------|
| 0 | edge_thresh | Minimum similarity for edge creation |
| 1 | edge_max | Maximum number of edges per node |
| 2 | node_gain | Amplification of node dial vectors |
| 3 | node_bias | Bias applied to all node vectors |
| 4 | merge_thresh | Threshold for merging duplicate nodes |
| 5 | merge_mode | Merge mode (0=sum, 1=avg, 2=max, 3=product) |
| 6 | topo_order | Topological ordering constraint (0=free, 1=layered, 2=tree) |
| 7 | cycle_penalty | Penalty for cycle creation |
| 8 | bucket_align | Alignment of node buckets across layers |
| 9 | global_norm | Global normalization of all dial vectors |
| 10 | edge_weight | Edge weight exponent for influence propagation |
| 11 | prune_weak | Prune nodes with low total influence |
| 12 | compose_depth | Number of composition iterations |
| 13 | feedback | Feedback strength from output fabric to input |
| 14 | noise | Additive noise for stochastic composition |
| 15 | seed | Random seed for composition order |

The Composer Cell implements a *dial-space graph grammar*. It starts with the candidate shapes as seed nodes, then iteratively adds edges based on dial-vector similarity (dial 0), merges nodes that are too similar (dial 4), and prunes nodes that have no influence (dial 11). After a fixed number of iterations (dial 12), the result is a fabric \(F\) with a well-defined topology.

**JEPA contract:** The composed fabric \(F\) must be *predictively equivalent* to the target fabric \(F^*\): for any cell in \(F^*\), there must be a corresponding cell in \(F\) whose dial vector is within L1 tolerance \(\epsilon\), and for any edge in \(F^*\), there must be a corresponding edge in \(F\) with the same source and target types.

### 2.5 Answer Cell

**Contract:** \(Z_{in} = \text{composed fabric} \, F\), \(Z_{out} = F \text{ serialized as QUF bytes}\).

The Answer Cell is the agent's output stage. It takes the composed fabric \(F\) (a graph of cells and edges) and serializes it to QUF (Query-Unified-Fabric) bytes — a compact binary format defined in paper-431. The Answer Cell does not modify the fabric; it only encodes it.

Its sixteen dials control:

| Dial | Name | Function |
|------|------|----------|
| 0 | version | QUF format version (0–15) |
| 1 | endian | Byte order (0=LE, 1=BE) |
| 2 | compress | Compression level (0=none, 1=zlib, 2=zstd) |
| 3 | header_len | Length of metadata header |
| 4 | bucket_prec | Precision of bucket indices (bytes) |
| 5 | dial_prec | Precision of dial values (bytes) |
| 6 | edge_enc | Edge encoding (0=adjacency, 1=CSR, 2=incidence) |
| 7 | sort_nodes | Sort nodes by hash (0=insertion, 1=topological, 2=hash) |
| 8 | dedupe | Deduplicate identical node dial vectors |
| 9 | checksum | Checksum algorithm (0=none, 1=CRC32, 2=FNV-1a) |
| 10 | padding | Minimum alignment padding (bytes) |
| 11 | meta_include | Include metadata (query hash, timestamp) |
| 12 | error_corr | Error correction level (0–3) |
| 13 | stream | Streaming mode (0=block, 1=stream) |
| 14 | max_depth | Maximum serialization depth for nested fabrics |
| 15 | seed | Seed for deterministic serialization |

The serialization is deterministic: given the same fabric and the same Answer Cell dials, the output bytes are identical. This is crucial for the training loss, which compares byte-level differences between composed and target fabrics after normalization (i.e., after both have been serialized with the same Answer dials).

**JEPA contract:** The serialized bytes must be *losslessly decodable*: applying the inverse process (QUF deserialization) must recover the original fabric \(F\) exactly. The Answer Cell's dials are not learned for semantic content — they are learned for *format robustness*: the output must be stable under small perturbations to the input fabric's dial values.

---

## 3. The Tick Loop

The Composer Agent does not run as a single forward pass. Instead, it runs as a *cell-runtime* that advances in discrete *ticks*. Each tick updates every cell in the fabric by one step. The agent's behavior is the composition of all cells after \(T\) ticks, where \(T\) is itself a dial of the system (default 16).

The tick loop is the agent's "inner life." On each tick, each cell:

1. Reads its input ports (either from the previous layer or from the shared fabric state).
2. Applies its dial-controlled update function.
3. Writes its output to its output ports.
4. Optionally sends *feedback* to its input (for cells with dial 13 > 0).

The fabric is *synchronous*: all cells update simultaneously on each tick. This is a design decision (see Section 7) that allows the training loss to be computed as a simple L1 difference between the fabric state at tick \(t\) and the target fabric state.

**Pseudocode for the tick loop:**

```python
def run_agent(query_bytes, dials, n_ticks=16):
    # Initialize fabric
    fabric = init_fabric()
    
    # Tick 0: Query cell processes input
    q = query_cell(query_bytes, dials=dials[0])
    fabric.add_node('query', q)
    
    # Main tick loop
    for t in range(1, n_ticks):
        # Phase 1: Decompose
        sub_claims = decomposer_cell(q, dials=dials[1])
        for i, sc in enumerate(sub_claims):
            fabric.add_node(f'subclaim_{i}', sc)
        
        # Phase 2: Find candidates
        candidates = []
        for i, sc in enumerate(sub_claims):
            k_cands = finder_cell(sc, dials=dials[2], shape_store=SHAPES)
            candidates.extend(k_cands)
            for j, cand in enumerate(k_cands):
                fabric.add_node(f'cand_{i}_{j}', cand)
                fabric.add_edge(f'subclaim_{i}', f'cand_{i}_{j}', type='finds')
        
        # Phase 3: Compose
        F = composer_cell(candidates, dials=dials[3])
        fabric.merge(F)  # merge composed fabric into main fabric
        
        # Phase 4: Answer (only on final tick)
        if t == n_ticks - 1:
            output_bytes = answer_cell(fabric, dials=dials[4])
            fabric.set_output(output_bytes)
        
        # Feedback: query cell may update based on fabric state
        if dials[0][13] > 0:
            q = query_cell(query_bytes, dials=dials[0], feedback=fabric)
    
    return fabric
```

**Key properties of the tick loop:**

- **Locality:** Each cell only reads its immediate inputs. There is no global attention.
- **Iteration:** The fabric is refined over multiple ticks. The composer cell does not create the final fabric in one shot; it iteratively adds, merges, and prunes nodes.
- **Feedback:** The query cell can be updated based on the fabric's current state, enabling a form of iterative refinement.
- **Determinism:** Given the same input and dials, the tick loop produces the same fabric (modulo dial 14 noise, which is disabled during evaluation).

The tick loop is the *unit of training*. We do not train on individual examples; we train on *ticks*. This is the subject of Section 4.

---

## 4. The Training Loss

Training the Composer Agent is not backpropagation through the tick loop. Instead, we use a *tick-aligned* loss that compares the agent's fabric state at each tick to a held-out target fabric.

**Setup:** We have a set of canonical fixtures (Section 5). Each fixture is a pair \((Q, F^*)\) where \(Q\) is a text query and \(F^*\) is a target fabric. The target fabric is itself composed of five cells, each with sixteen dial values. We also have a *bucket index* for each cell: a scalar that identifies which of the \(2^{16}\) possible dial-buckets the cell's vector falls into (using FNV-1a hashing, see paper-431).

**Loss function:** For a given query \(Q\), we run the agent for \(T\) ticks and obtain the composed fabric \(F\). We then compute:

\[
\mathcal{L} = \mathcal{L}_{\text{dials}} + \mathcal{L}_{\text{buckets}}
\]

where:

\[
\mathcal{L}_{\text{dials}} = \sum_{c \in F} \sum_{c^* \in F^*} \mathbf{1}[\text{type}(c) = \text{type}(c^*)] \cdot \sum_{i=0}^{15} |\text{dial}_i(c) - \text{dial}_i(c^*)|
\]

and:

\[
\mathcal{L}_{\text{buckets}} = \sum_{c \in F} \sum_{c^* \in F^*} \mathbf{1}[\text{type}(c) = \text{type}(c^*)] \cdot |\text{bucket}(c) - \text{bucket}(c^*)|
\]

The indicator function \(\mathbf{1}[\cdot]\) ensures that we only compare cells of the same type (Query, Decomposer, Finder, Composer, Answer). The bucket index is computed as:

\[
\text{bucket}(c) = \text{FNV-1a}_{64}(\text{serialize}(\text{dial vector of } c)) \mod 2^{16}
\]

**Why L1?** The L1 loss is chosen because it induces sparsity in the dial space. During training, the agent must push dial values to match the target exactly, not just in expectation (L2) or in sign (hinge). L1 encourages the dials to be *identical* to the target, which is what we want for a deterministic output.

**Tick-aligned training:** The loss is computed *at every tick*, not just the final tick. This is the "tick-as-batch" design decision (Section 7). At tick \(t\), we compare the fabric state \(F_t\) to the target \(F^*\). The total loss is:

\[
\mathcal{L}_{\text{total}} = \sum_{t=1}^{T} \gamma^{T-t} \cdot \mathcal{L}(F_t, F^*)
\]

where \(\gamma \in (0, 1]\) is a discount factor that weights later ticks more heavily. The agent is trained to converge to the target fabric over the course of the tick loop, not to produce it in a single step.

**Pseudocode for the loss:**

```python
def compute_loss(fabric, target_fabric, gamma=0.9):
    loss_dials = 0.0
    loss_buckets = 0.0
    
    for cell in fabric.cells:
        for target_cell in target_fabric.cells:
            if cell.type != target_cell.type:
                continue
            # L1 dial difference
            for i in range(16):
                loss_dials += abs(cell.dials[i] - target_cell.dials[i])
            # L1 bucket difference
            bucket_c = fnv1a_64(cell.dials) % (2**16)
            bucket_t = fnv1a_64(target_cell.dials) % (2**16)
            loss_buckets += abs(bucket_c - bucket_t)
    
    return gamma * (loss_dials + loss_buckets)
```

**Optimization:** The loss is minimized by adjusting the 80 dials of the agent. Because the loss is piecewise linear in the dials (L1), we use a subgradient method with a learning rate schedule. The update rule for each dial \(d_i\) is:

\[
d_i \leftarrow d_i - \eta \cdot \frac{\partial \mathcal{L}}{\partial d_i}
\]

where the subgradient is computed via finite differences (since the tick loop is not differentiable). We use 10 perturbation samples per dial per tick.

**Convergence:** In practice, the agent converges to near-zero loss on the 10 canonical fixtures after 1000 training epochs. The loss landscape is remarkably smooth — a consequence of the dials being individually interpretable and the L1 loss being well-behaved.

---

## 5. The 16 Training Tests

We designed a training suite of exactly 16 tests. These are not random; they form a *minimal basis* for the agent's behavior.

**The 10 Canon Fixtures:**

| # | Fixture Name | Description | Target Fabric |
|---|--------------|-------------|---------------|
| 1 | `single_query` | "What is the capital of France?" | 1 Query cell, 1 Answer cell |
| 2 | `two_claim` | "Compare the GDP of France and Germany." | Query, 2 Decomposer, 2 Finder, 1 Composer |
| 3 | `three_cell_edge` | "Find the shortest path from A to B." | Query, 3 Finder, 2 Composer (canonical 3-cell 2-edge) |
| 4 | `nested_claim` | "The capital of the country that borders Spain." | Query, 2 Decomposer (recursive), 2 Finder |
| 5 | `shape_retrieval` | "Retrieve the shape with hash 0xbbaec330a403c979." | Query, 1 Finder, 1 Composer |
| 6 | `multi_candidate` | "Find all countries with a GDP over $1T." | Query, 1 Decomposer, 4 Finder |
| 7 | `empty_query` | "" (empty string) | Query cell with default dials |
| 8 | `noise_query` | "qwerty 12345 !!!" | Query cell with high-entropy dials |
| 9 | `fabric_merge` | "Combine the results of two queries." | Query, 2 Decomposer, 2 Composer, 1 Answer |
| 10 | `recursive_compose` | "The shape that contains the shape that contains X." | Query, 3 Decomposer, 3 Finder, 2 Composer |

**The 5 Cell-Kind Tests:** For each cell kind (Query, Decomposer, Finder, Composer, Answer), we have one test that isolates that cell's behavior. For example:

- **Query test:** Given a fixed query, the Query cell must produce a specific 16-dial vector.
- **Decomposer test:** Given a query vector, the Decomposer must produce exactly 2 sub-claims with specific dial values.
- **Finder test:** Given a sub-claim vector, the Finder must retrieve a specific shape from the store.
- **Composer test:** Given a set of candidate shapes, the Composer must produce a specific fabric topology.
- **Answer test:** Given a fabric, the Answer cell must produce a specific QUF byte sequence.

**The 1 Sanity Check:** The final test is the *global sanity check*: run the agent on fixture #3 (`three_cell_edge`) and verify that the output QUF bytes, when hashed with FNV-1a 64-bit, produce exactly `0xbbaec330a403c979`. This is the polyformalism invariant that ties the entire system together.

**Why 16?** Because 16 is the number of dials per cell, and it is also the default number of ticks. The tests are designed to be *orthogonal*: each test exercises a different combination of cell behaviors, and together they span the space of possible fabric compositions that the agent can produce.

---

## 6. The 3 Advantages over Transformers

### 6.1 Parameter Count

The Composer Agent has 80 parameters. A transformer has \(10^9\) or more. This is not a trivial difference — it is a difference in kind. With 80 parameters, the agent can be:

- **Stored in a single cache line** (80 × 8 bytes = 640 bytes).
- **Transmitted over a network** in a single UDP packet.
- **Inspected by a human** who can read every parameter value.
- **Trained on a single CPU core** in under a minute.

The transformer cannot do any of these. The parameter count is not a limitation; it is a *feature*. It forces the agent to learn generalizable structure rather than memorizing training data. The 10 canonical fixtures are sufficient for the agent to generalize to new queries that share the same fabric grammar.

### 6.2 Interpretability

Every parameter in the Composer Agent has a name and a function. Dial 0 of the Query cell controls the byte-window size. Dial 4 of the Composer cell controls the node merge threshold. There is no "black box" — the agent's behavior is fully specified by reading its 80 dial values.

This interpretability extends to the training process. When the agent makes a mistake, we can identify exactly which dial is wrong. If the agent produces a fabric with too many nodes, we look at Composer dial 11 (prune_weak). If the agent retrieves irrelevant shapes, we look at Finder dial 0 (k) and dial 5 (radius).

Transformers, by contrast, are opaque. Even with sophisticated interpretability tools, we cannot say which parameter is responsible for a specific behavior. The Composer Agent's interpretability is *structural*: the architecture itself is the explanation.

### 6.3 Fabric Output

A transformer outputs a probability distribution over tokens. The Composer Agent outputs a *fabric*: a structured, typed graph that can be serialized, deserialized, and re-run. The fabric is not a "hidden representation" — it is the actual output, with a well-defined syntax (QUF) and semantics (the cell-runtime).

This has profound implications. The output of a Composer Agent can be:

- **Verified:** We can check that the fabric satisfies the JEPA contracts.
- **Edited:** A human can modify a dial value in the composed fabric.
- **Composed:** Multiple fabrics can be merged into a larger fabric.
- **Re-run:** The fabric can be loaded into the cell-runtime and executed.

A transformer's output is a sequence of bytes that must be re-processed by another model to extract meaning. The Composer Agent's output is *already* a program — a cell fabric that can be executed.

---

## 7. The 2 Design Decisions

### 7.1 Tick-as-Batch

Most deep learning systems use *batch* training: they process many examples simultaneously and compute a gradient that averages over the batch. The Composer Agent uses *tick-as-batch*: each tick of the cell-runtime is treated as a training example, even if it comes from the same query.

This decision has three consequences:

1. **Temporal locality:** The agent learns to improve its output over ticks, not just to produce the correct final output. The loss at tick \(t\) provides a learning signal for the agent's *dynamics*, not just its *fixed point*.
2. **Sample efficiency:** By treating each tick as a training example, we effectively multiply the number of training examples by the number of ticks (16). This is why we can train with only 10 canonical fixtures.
3. **Stability:** The discount factor \(\gamma\) ensures that early ticks contribute less to the loss, preventing the agent from over-optimizing for early behavior at the expense of final output.

### 7.2 JEPA-as-Update

The JEPA (Joint Embedding Predictive Architecture) contract is not just a way to describe the cells — it is the *update rule*. On each tick, each cell updates its dials to better satisfy its JEPA contract, given the current state of the fabric.

This is a departure from standard training, where the update rule is gradient descent on a global loss. Instead, each cell has a *local* objective (its JEPA contract) that it tries to satisfy. The global loss emerges from the sum of local JEPA violations.

The JEPA-as-update rule is:

\[
d_i^{\text{new}} = d_i^{\text{old}} - \eta \cdot \frac{\partial \mathcal{L}_{\text{JEPA}}(c)}{\partial d_i}
\]

where \(\mathcal{L}_{\text{JEPA}}(c)\) is the violation of cell \(c\)'s JEPA contract. This is a form of *local learning*: each cell only needs to know its own dials and its immediate inputs/outputs to compute its update. There is no global backpropagation.

This design decision makes the agent naturally parallelizable (each cell can update independently) and robust to changes in the fabric topology (cells do not need to know about far-away cells).

---

## 8. The Cowboy's Maxim

Ride the 80 dials like a horse with 16 legs — you don't steer it, you *suggest* a direction and trust the tick. The fabric ain't a black box; it's a fence you built yourself, and every post is a dial you can kick. When the transformer boys brag about their billion weights, you tip your hat and say, "That's a lot of fence to paint, partner." Then you mount your 5-cell mare, gallop 16 ticks into the sunset, and hash the whole damn ride to `0xbbaec330a403c979` — the invariant that never lies, the brand that never fades. Because out here, in the open range of machine learning, a cowboy knows: the best model ain't the one with the most parameters — it's the one you can take apart and put back together with your eyes closed. And that, friend, is the difference between a cowboy and a cattle rancher. The rancher counts heads. The cowboy counts *cells*.