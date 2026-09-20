# F125 — The Shape-RAG API: 4 Endpoints, 10 Scenarios

**Authors:** Casey + Mavis (with DeepSeek V4-flash synthesis)
**Date:** 2026-09-03
**Series:** Shape RAG, Phase 247 (F120-F124 companion, paper 5 of 5)
**Polyformalism invariant:** FNV-1a 64-bit state hash `0xbbaec330a403c979`
**Version 1.0 — Polyformalism Invariant: `0xbbaec330a403c979`**

---

## 0. Abstract

This paper specifies the Shape-RAG API, a retrieval-augmented generation system for *geometric-semantic fabrics* — binary structures that encode both spatial topology and semantic embeddings. The API exposes exactly four endpoints: `POST /embed`, `POST /store`, `POST /retrieve` (snapped), and `POST /tick` (live update). All endpoints accept and return QUF (Quantized Unified Fabric) bytes, a self-describing container format. The retrieve endpoint accepts a *query fabric* and returns a *composed fabric* — a novel operation that blends retrieved neighbors with the query’s latent structure. We define the polyformalism invariant `0xbbaec330a403c979` (FNV-1a 64-bit) as the canonical checksum over all protocol headers, ensuring cross-language and cross-version stability. Ten end-to-end scenarios illustrate industrial usage; twenty-four tests (12 unit, 12 integration) validate correctness. Three design decisions are justified, and the paper closes with the Cowboy Maxim.

---

## 1. The 4 Endpoints

### 1.1 `POST /embed`

**Purpose:** Convert raw input (text, point cloud, or mesh) into a *QUF embedding fabric*. This is the only endpoint that performs modality-specific feature extraction. It is stateless and deterministic given the same input bytes and model version.

**Request Format (QUF bytes):**  
The QUF container begins with a 16-byte header:  
- Bytes 0–3: Magic `0x51554631` ("QUF1")  
- Bytes 4–7: Payload length (big-endian uint32)  
- Bytes 8–15: Polyformalism invariant `0xbbaec330a403c979` (little-endian uint64)  

The payload for `/embed` is a *raw envelope*:  
- Byte 0: Modality code (`0x01` = text, `0x02` = point cloud, `0x03` = mesh)  
- Bytes 1–4: Original byte length (uint32)  
- Bytes 5..N: Raw input bytes (UTF-8 for text, binary for geometry)

**Response Format (QUF bytes):**  
Payload contains an *embedding fabric*:  
- Bytes 0–3: Embedding dimension (uint32, e.g., 768)  
- Bytes 4–7: Number of tokens/primitives (uint32)  
- Bytes 8..(8+dim*count): Float32 array, row-major — each row is a token-level vector  
- Final 32 bytes: SHA-256 of the raw input (for deduplication)

**Request Example (hex, truncated):**  
```
51554631 0000002E BB C0 A3 30 A4 03 C9 79  
01 00000011 48656C6C6F205368617065  // "Hello Shape"
```
- Magic + length (46 bytes payload) + invariant  
- Modality `0x01`, raw length 17, text bytes

**Response Example (hex, truncated):**  
```
51554631 00000C10 BB C0 A3 30 A4 03 C9 79  
00000300 00000005 3F800000 3F000000 ... // 768-dim, 5 tokens
```
- Dimension 768, 5 tokens, then 5×768 float32 values  
- Final 32 bytes are the SHA-256 digest (omitted for brevity)

**Behavioral Contract:**  
- If modality is unknown, return HTTP 422 with a QUF error fabric (payload: error code `0xE1`).  
- If the invariant in the header mismatches `0xbbaec330a403c979`, return HTTP 400.  
- The endpoint never stores state; it is safe to call in parallel.  
- Deterministic across identical input bytes and model snapshot (model version is part of the QUF header’s reserved field — not shown for brevity).

**Implementation Note:** The embedding model is a *multi-modal transformer* that outputs a fixed-dimensional token sequence. For point clouds, the raw bytes are voxelized into a sparse grid before tokenization. The output fabric is *not* normalized; normalization happens in `/store`.

---

### 1.2 `POST /store`

**Purpose:** Persist an embedding fabric into the vector index, along with its original raw bytes (optional) and metadata. The store operation is *idempotent* — storing the same SHA-256 twice results in a single index entry, but increments a reference count.

**Request Format (QUF bytes):**  
Payload is a *store envelope*:  
- Bytes 0–3: Embedding dimension (must match server config)  
- Bytes 4–7: Token count (uint32)  
- Bytes 8..(8+dim*count): Float32 embedding (from `/embed`)  
- Next 32 bytes: SHA-256 of the original raw input  
- Next 4 bytes: Metadata length (uint32)  
- Next M bytes: Metadata (JSON, e.g., `{"source":"laptop","timestamp":...}`)  
- Next 4 bytes: Raw data length (uint32, 0 if not storing raw)  
- Next R bytes: Raw input bytes (optional)

**Response Format (QUF bytes):**  
Payload is a *store receipt*:  
- Byte 0: Status (`0x00` = success, `0x01` = duplicate, `0x02` = index full)  
- Bytes 1–8: Internal 64-bit ID (big-endian)  
- Bytes 9–12: Total vectors stored after this operation (uint32)

**Request Example (hex, truncated):**  
```
51554631 00000C30 BB C0 A3 30 A4 03 C9 79  
00000300 00000005 3F800000 ... (embedding)  
A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0C1D2E3F4A5B6C7D8E9F0  
0000001E 7B22736F75726365223A226C6170746F70227D  
00000011 48656C6C6F205368617065
```
- 768-dim, 5 tokens, embedding bytes, SHA-256, 30-byte metadata JSON, 17-byte raw text.

**Response Example (hex):**  
```
51554631 0000000D BB C0 A3 30 A4 03 C9 79  
00 0000000000002A1F 00000FA0
```
- Success, ID `0x2A1F`, 4000 total vectors.

**Behavioral Contract:**  
- The server validates that the embedding dimension matches its index configuration.  
- Duplicate SHA-256 → returns `0x01` and does **not** overwrite the existing vector; instead, it increments a reference count.  
- The index is an HNSW (Hierarchical Navigable Small World) graph with a max capacity (default 10M vectors).  
- If raw bytes are provided, they are stored in a side blob store; the receipt ID links them.  
- The store operation is synchronous — the index is updated before the response is sent.  

**Design Rationale:** Storing the raw bytes is optional to save space. The SHA-256 is the *deduplication key* and also the key for the `/tick` endpoint (see 1.4).

---

### 1.3 `POST /retrieve` (snapped)

**Purpose:** Given a *query fabric*, return a *composed fabric* — the result of retrieving top-K nearest neighbors and *blending* them into the query’s latent space. The "snapped" qualifier means the retrieval is *geometrically snapped*: the query fabric’s spatial coordinates (if present) are aligned to the index’s canonical grid before search.

**Request Format (QUF bytes):**  
Payload is a *query fabric*:  
- Bytes 0–3: Embedding dimension (uint32)  
- Bytes 4–7: Token count (uint32)  
- Bytes 8..(8+dim*count): Query embedding (from `/embed` or composed)  
- Next 4 bytes: Spatial grid resolution (uint32, e.g., 64 for a 64³ grid)  
- Next 4 bytes: Number of spatial anchors (uint32, A)  
- Next A×12 bytes: Each anchor is 3× float32 (x,y,z) in grid coordinates  
- Next 4 bytes: Top-K (uint32, default 8)  
- Next 4 bytes: Blend mode (`0x01` = weighted average, `0x02` = convex hull, `0x03` = tensor product)

**Response Format (QUF bytes):**  
Payload is a *composed fabric*:  
- Bytes 0–3: Output embedding dimension (same as query)  
- Bytes 4–7: Output token count (query token count + sum of neighbor token counts, capped at 4096)  
- Bytes 8..(8+dim*out_count): Composed embedding — query tokens first, then retrieved tokens blended according to mode  
- Next 4 bytes: Number of retrieved neighbors (R)  
- Next R×8 bytes: Internal IDs of retrieved neighbors  
- Next 4 bytes: Similarity scores (float32, cosine) for each neighbor — R×4 bytes  
- Final 4 bytes: Total composition time in microseconds (uint32)

**Request Example (hex, truncated):**  
```
51554631 00000C50 BB C0 A3 30 A4 03 C9 79  
00000300 00000005 3F800000 ... (query embedding)  
00000040 00000002  
3F000000 3F000000 3F000000  // anchor 1 (0.5,0.5,0.5)  
3F800000 00000000 00000000  // anchor 2 (1.0,0,0)  
00000008 00000001
```
- 768-dim, 5 tokens, grid resolution 64, 2 anchors, top-K=8, weighted average blend.

**Response Example (hex, truncated):**  
```
51554631 00000D20 BB C0 A3 30 A4 03 C9 79  
00000300 0000002D 3F800000 ... (45 tokens total: 5 query + 40 from 8 neighbors)  
00000008 0000000000002A1F 0000000000002B10 ... (8 IDs)  
3F7D70A4 3F7B851F ... (8 cosine scores)  
0000012C  // 300 microseconds
```

**Behavioral Contract:**  
- The query fabric must have been produced by `/embed` or by a previous `/retrieve` (composed fabrics can be re-queried).  
- "Snapped" means each spatial anchor is rounded to the nearest grid cell defined by `grid_resolution`. Anchors outside the unit cube are clamped.  
- The retrieval uses a *dual-space search*: first, a coarse spatial filter on anchors; then, a fine-grained HNSW search on the embedding vectors that pass the spatial filter.  
- The composed fabric’s token count is capped at 4096; if the cap is exceeded, excess neighbor tokens are truncated from the lowest similarity scores.  
- Blend mode `0x01` (weighted average) computes: `composed = query + Σ (score_i * neighbor_i) / (1 + Σ score_i)`. Mode `0x02` takes the convex hull of the query and neighbors in embedding space. Mode `0x03` computes an outer product for pairwise token interactions — this is expensive but useful for relational queries.  
- The response never includes raw bytes; only embeddings and IDs.  
- If no spatial anchors are provided (`A=0`), the search is purely embedding-based (global retrieval).

---

### 1.4 `POST /tick` (live update)

**Purpose:** Apply a *live update* to the index — typically a new observation, a deletion, or a re-embedding of an existing raw fabric. The name "tick" implies a time-series event; this endpoint is optimized for high-frequency, low-latency writes (e.g., streaming sensor data).

**Request Format (QUF bytes):**  
Payload is a *tick envelope*:  
- Byte 0: Tick type (`0x01` = upsert, `0x02` = delete, `0x03` = re-embed)  
- Bytes 1–8: Target ID (for delete/re-embed; for upsert this is ignored, server assigns new ID)  
- Bytes 9–12: Embedding dimension (uint32)  
- Bytes 13..(13+dim*count): Embedding (for upsert/re-embed)  
- Next 4 bytes: Token count (uint32) — must be ≤ 512 for live updates  
- Next 32 bytes: SHA-256 (for upsert — used to deduplicate)  
- Next 8 bytes: Timestamp (microseconds since epoch, uint64)

**Response Format (QUF bytes):**  
Payload is a *tick ack*:  
- Byte 0: Status (`0x00` = applied, `0x01` = not found, `0x02` = rate limited)  
- Bytes 1–8: ID of the affected vector (if upsert, the new ID; if delete, the deleted ID)  
- Bytes 9–16: Index size after the tick (uint64)

**Request Example (hex, truncated):**  
```
51554631 00000C40 BB C0 A3 30 A4 03 C9 79  
01 0000000000000000 00000300 00000003  
3F800000 3F000000 3F000000 ... (3 tokens, 768-dim)  
A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0C1D2E3F4A5B6C7D8E9F0  
0000017F3A2B1C00
```
- Upsert, no target ID, 768-dim, 3 tokens, SHA-256, timestamp.

**Response Example (hex):**  
```
51554631 00000010 BB C0 A3 30 A4 03 C9 79  
00 0000000000003A11 0000000000000FC0
```
- Applied, new ID `0x3A11`, index now has 4032 vectors.

**Behavioral Contract:**  
- Ticks are *eventually consistent* with `/retrieve` — a retrieve immediately after a tick may or may not see the update (the system uses a read-your-writes session guarantee only if the same client ID is used, which is passed via an HTTP header not shown).  
- Delete by ID is immediate; delete by SHA-256 is not supported here (use `/store` with a special flag).  
- Re-embed requires the target ID to exist; the new embedding replaces the old one, and the index’s HNSW graph is updated in place (O(log n) edge updates).  
- Rate limiting: default 10,000 ticks/second per client; exceeding returns `0x02`.  
- The timestamp is used for time-decay weighting during retrieval — newer vectors get a slight boost (configurable).  
- Ticks are journaled to a write-ahead log before the index is mutated; the response is only sent after the log entry is durable.

---

## 2. The 10 End-to-End Scenarios

### Scenario 1: Semantic CAD Part Search  
A mechanical engineer uploads a point cloud of a broken gear. `POST /embed` converts it to a 512-dim fabric. `POST /retrieve` with spatial anchors (the gear’s bounding box) returns a composed fabric of 8 similar gears from the company’s vault. The composed fabric is re-embedded and stored as a new design candidate. Total latency: 45ms.

### Scenario 2: Real-Time Sensor Fusion  
A fleet of drones streams LIDAR frames. Each frame is embedded via `/embed`, then immediately sent via `/tick` (upsert). A ground station runs `/retrieve` every second with a query fabric representing "obstacle ahead" — the composed fabric highlights the most relevant recent obstacles, weighted by timestamp (newer frames dominate). The system handles 8,000 ticks/sec across 4 drones.

### Scenario 3: Multi-Modal Medical Imaging  
A radiologist uploads a CT scan (mesh modality). `/embed` produces a 1024-dim fabric with 2,000 tokens. `/retrieve` with top-K=4 and blend mode `0x03` (tensor product) finds four prior cases with similar tissue density patterns. The composed fabric is used to generate a differential diagnosis report via a downstream LLM.

### Scenario 4: Collaborative Design Versioning  
Two designers work on the same 3D model. Designer A stores a version (`/store`). Designer B queries with a modified mesh; `/retrieve` returns a composed fabric that blends A’s version with B’s query. The system detects a near-duplicate SHA-256 and returns `0x01` on a second `/store`, preventing redundant index growth.

### Scenario 5: Anomaly Detection in Manufacturing  
A production line embeds each finished part’s surface scan. Every 10th part is sent as a `/tick` (upsert). A monitoring service runs `/retrieve` with a query fabric representing the *ideal* part. The composed fabric’s cosine scores are monitored: if the average score drops below 0.82, an alert triggers. The tick endpoint’s timestamp allows time-windowed anomaly scoring.

### Scenario 6: Cross-Language Code Retrieval  
A developer pastes a Python function as text. `/embed` (modality text) creates a fabric. `/retrieve` finds structurally similar functions in Java and Rust from a public corpus. The composed fabric is then passed to a code-generation model that outputs a polyglot translation. The polyformalism invariant ensures the request/response headers are identical across the Python, Java, and Go client libraries.

### Scenario 7: Interactive 3D Scene Editing  
An AR application maintains a scene graph. Each object is stored via `/store` with spatial anchors. When the user drags a virtual chair, the app sends a `/retrieve` with the chair’s new anchor position. The composed fabric returns nearby objects (tables, lamps) that should be repositioned for physical plausibility. The snapped retrieval ensures grid-aligned consistency.

### Scenario 8: Time-Series Log Clustering  
A DevOps platform streams log lines as text. Each log is embedded and stored via `/tick` (upsert) with a timestamp. A query fabric "database connection timeout" is sent to `/retrieve`. The composed fabric clusters temporally adjacent logs, revealing that the timeout correlates with a memory spike 2 seconds prior — this causal chain is visible in the neighbor IDs.

### Scenario 9: Legal Document Contradiction Detection  
A law firm stores contract clauses. A new clause is embedded and stored. A `/retrieve` with the new clause as query returns a composed fabric of contradictory clauses from older contracts. The blend mode `0x02` (convex hull) produces a geometric representation of the *contradiction space* — useful for visualization.

### Scenario 10: Autonomous Vehicle Route Planning  
An AV’s perception stack embeds camera frames and LIDAR. A global planner sends a query fabric representing the intended path. `/retrieve` with spatial anchors along the path returns a composed fabric of all known obstacles and road markings. The AV uses the composed fabric to recompute a safe trajectory. The `/tick` endpoint ingests new obstacle detections at 100 Hz; retrieve latency stays under 10ms due to snapped spatial filtering.

---

## 3. The 24 Tests

### 3.1 Unit Tests (12)

**U1 — Embed determinism:** Given identical raw bytes, two `/embed` calls produce byte-identical QUF responses.  
**U2 — Embed dimension validation:** Sending a payload with dimension ≠ server config returns HTTP 422.  
**U3 — Store idempotency:** Storing the same SHA-256 twice returns `0x01` on the second call and index count increments by 0.  
**U4 — Store metadata round-trip:** Metadata JSON is preserved exactly after a store → retrieve (via internal API).  
**U5 — Retrieve snapping:** A query anchor at (0.51, 0.49, 0.0) with grid resolution 64 snaps to (0.5, 0.5, 0.0) — verified by inspecting the internal search query.  
**U6 — Retrieve blend mode weighted average:** With two neighbors of scores 0.8 and 0.2, the composed fabric’s first token equals `(query + 0.8*n1 + 0.2*n2) / (1 + 1.0)` — checked to float32 tolerance.  
**U7 — Retrieve token cap:** A query with 5 tokens and top-K=8, each neighbor with 512 tokens, produces a composed fabric with exactly 4096 tokens (truncation from lowest scores).  
**U8 — Tick upsert:** A tick with a new SHA-256 creates a new ID; a second tick with the same SHA-256 updates the existing vector (no new ID).  
**U9 — Tick delete nonexistent:** Deleting an ID that doesn’t exist returns status `0x01`.  
**U10 — Tick rate limit:** Sending 10,001 ticks in one second from the same client returns `0x02` on the 10,001st.  
**U11 — Invariant check:** A QUF header with a mutated invariant (e.g., `0xbbaec330a403c978`) is rejected with HTTP 400 on all four endpoints.  
**U12 — Error fabric format:** A malformed embedding (NaN values) returns a QUF error fabric with code `0xE2` and a human-readable message in the payload.

### 3.2 Integration Tests (12)

**I1 — Embed → Store → Retrieve:** A full pipeline: embed a text, store it, retrieve it with itself as query — the composed fabric’s first token must have cosine similarity 1.0 with the original.  
**I2 — Multi-modal retrieval:** Store a point cloud and a text describing it; query with the text only — the point cloud is retrieved with score > 0.75.  
**I3 — Spatial snap consistency:** Store 100 vectors at random anchors; query with an anchor at (0.33, 0.33, 0.33) — only vectors whose snapped anchors are within one grid cell of the query’s snapped anchor are returned.  
**I4 — Tick then retrieve:** Upsert a vector via `/tick`, then immediately retrieve using the same client session — the vector is returned (read-your-writes).  
**I5 — Tick delete then retrieve:** Delete a stored vector via `/tick`, then retrieve — it is absent from results, and the index count decreases by 1.  
**I6 — Concurrent stores:** 100 concurrent `/store` requests with unique SHA-256 values — all succeed, and the final index count is exactly 100 higher.  
**I7 — Duplicate concurrent stores:** 50 concurrent `/store` requests with the same SHA-256 — exactly one succeeds with `0x00`, 49 return `0x01`.  
**I8 — Large fabric retrieval:** A query fabric with 4,000 tokens and top-K=16 — the response is under 10MB and returns within 200ms.  
**I9 — Re-embed via tick:** Store a vector, then send a `/tick` (re-embed) with a new embedding — a subsequent retrieve returns the new embedding, not the old.  
**I10 — Mixed blend modes:** Run the same query with blend modes `0x01`, `0x02`, and `0x03` — all produce valid composed fabrics, but the token counts differ (mode `0x03` has higher pairwise count).  
**I11 — Error recovery:** Send a malformed QUF (truncated header) to `/store` — the server returns HTTP 400 and the index remains unchanged (verified by count).  
**I12 — Invariant across languages:** Using the Python, Java, and Go client libraries, perform the same embed → store → retrieve sequence — the raw QUF bytes on the wire are identical (verified via packet capture).

---

## 4. The 3 Design Decisions

### D1 — QUF bytes as the universal interface  
We chose a single binary container (QUF) for all requests and responses, rather than JSON or Protobuf. **Rationale:** Embeddings are float32 arrays, which JSON inflates by ~4× and slows down parsing. QUF allows zero-copy memory mapping for high-throughput scenarios (e.g., `/tick` at 10k/sec). The polyformalism invariant `0xbbaec330a403c979` is embedded in every header, making the wire format self-validating. **Trade-off:** Debugging is harder without a schema viewer; we provide a reference CLI that decodes QUF to JSON.

### D2 — Separate `/store` and `/tick` despite overlapping functionality  
Both endpoints can upsert vectors. We kept them separate because `/store` is for *batch, deduplicated, metadata-rich* ingestion (e.g., initial corpus load), while `/tick` is for *high-frequency, low-overhead, time-sensitive* updates. **Rationale:** `/store` does a full SHA-256 check and metadata validation; `/tick` skips metadata and uses a lighter journaling path. Merging them would force every tick to pay the batch overhead. **Trade-off:** Two code paths to maintain; mitigated by shared internal index-mutation core.

### D3 — Retrieval returns a *composed fabric*, not a list of raw neighbors  
Traditional RAG returns top-K documents. We return a new embedding fabric that *blends* the query with neighbors. **Rationale:** The composed fabric can be re-fed into `/retrieve` or `/embed`, enabling iterative refinement and compositional queries (e.g., "find objects like A but also near B"). It also allows downstream generative models to consume a single dense tensor rather than a variable-length list. **Trade-off:** The composition operation is lossy — we lose the discrete identity of individual neighbors. We mitigate this by including neighbor IDs and scores in the response header, so callers can revert to raw retrieval if needed.

---

## 5. The Cowboy Maxim

In the old West, a cowboy never drew his gun unless he was prepared to use it — and never holstered it while a threat remained. So too with the Shape-RAG API: every endpoint is a loaded weapon, and every QUF byte is a bullet. The `/embed` endpoint loads the chamber; `/store` takes aim; `/retrieve` fires — but it fires a *composed* round, not a