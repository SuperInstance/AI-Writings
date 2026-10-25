# 65 — Hidden Concordance Detector + Quilt Grid Viewer
Last Updated: 2026-08-29
Stack: Cloudflare Worker + D1 (forest_nodes, forest_edges, forest_walks)

---

## Tool 1: Hidden Concordance Detector
### Purpose
Finds pairs of forest nodes (content chunks) that reside in **different top-level directories** but exhibit highly correlated Hebbian walk trajectories. These are "secret agreements" — topics that the fleet is independently navigating towards in separate contexts, but no explicit connection has been made yet.

This is the most powerful pattern detector in the forest stack: it surfaces emergent consensus that no human or agent explicitly wrote down.

### Correlation Metric Specification
**Concrete definition:** Pearson product-moment correlation coefficient over weekly walk count buckets.

- **Buckets:** 7-day rolling windows, minimum 4 non-zero buckets required for comparison
- **Normalization:** Each node's walk count series is normalized to z-score before correlation
- **Threshold:** `r ≥ 0.85` for concordance detection
- **False positive controls:**
  - Require minimum 10 total walks per node
  - Require maximum 50% overlap in shared immediate neighbors
  - Require the two nodes are in different top-level directories (first path component)
  - Exclude pairs with cosine embedding similarity > 0.75 (these are already known duplicates/similars)

### D1 SQL Implementation
```sql
-- First, precompute weekly walk buckets for all nodes
WITH node_weekly_walks AS (
  SELECT
    e.src AS node_id,
    strftime('%Y-%W', w.ts) AS week_bucket,
    COUNT(*) AS walk_count
  FROM forest_edges e
  JOIN forest_walks w ON e.id = w.edge_id
  WHERE e.weight >= 0.01
  GROUP BY e.src, week_bucket
  HAVING walk_count > 0
),
-- Filter nodes that meet minimum activity requirements
valid_nodes AS (
  SELECT node_id
  FROM node_weekly_walks
  GROUP BY node_id
  HAVING COUNT(DISTINCT week_bucket) >= 4
     AND SUM(walk_count) >= 10
),
-- Get node metadata and top-level directory
node_meta AS (
  SELECT
    id,
    title,
    path,
    SUBSTR(path, 0, INSTR(path, '/')) AS top_dir,
    embedding
  FROM forest_nodes
),
-- Generate all candidate pairs from different directories
candidate_pairs AS (
  SELECT
    a.node_id AS node_a,
    b.node_id AS node_b,
    m1.top_dir AS dir_a,
    m2.top_dir AS dir_b,
    m1.embedding AS emb_a,
    m2.embedding AS emb_b
  FROM valid_nodes a
  JOIN valid_nodes b ON a.node_id < b.node_id
  JOIN node_meta m1 ON a.node_id = m1.id
  JOIN node_meta m2 ON b.node_id = m2.id
  WHERE m1.top_dir != m2.top_dir
)
-- Calculate Pearson correlation for each pair
SELECT
  cp.node_a,
  cp.node_b,
  m1.title AS title_a,
  m2.title AS title_b,
  m1.path AS path_a,
  m2.path AS path_b,
  -- Pearson r calculation over matching buckets
  (
    COUNT(*) * SUM(wa.walk_count * wb.walk_count) - SUM(wa.walk_count) * SUM(wb.walk_count)
  ) / SQRT(
    (COUNT(*) * SUM(wa.walk_count * wa.walk_count) - SUM(wa.walk_count) * SUM(wa.walk_count))
    *
    (COUNT(*) * SUM(wb.walk_count * wb.walk_count) - SUM(wb.walk_count) * SUM(wb.walk_count))
  ) AS correlation,
  COUNT(*) AS matching_buckets
FROM candidate_pairs cp
JOIN node_weekly_walks wa ON cp.node_a = wa.node_id
JOIN node_weekly_walks wb ON cp.node_b = wb.node_id AND wa.week_bucket = wb.week_bucket
WHERE (
  -- Exclude already known similar pairs
  vector_cosine_similarity(cp.emb_a, cp.emb_b) < 0.75
)
GROUP BY cp.node_a, cp.node_b
HAVING
  matching_buckets >= 4
  AND correlation >= 0.85
  -- Neighbor overlap check
  AND (
    SELECT COUNT(DISTINCT dst)
    FROM forest_edges e1
    JOIN forest_edges e2 ON e1.dst = e2.dst
    WHERE e1.src = cp.node_a AND e2.src = cp.node_b AND e1.weight >= 0.01 AND e2.weight >= 0.01
  ) / (
    SELECT COUNT(DISTINCT dst) FROM forest_edges WHERE src IN (cp.node_a, cp.node_b) AND weight >= 0.01
  ) <= 0.5
ORDER BY correlation DESC
LIMIT ? OFFSET ?;
```

### API Endpoints
1. `GET /api/forest/concordances?limit=X&offset=Y` — Returns ranked list of concordant node pairs
2. `GET /api/forest/concordance/:nodeA/:nodeB` — Returns detailed trajectory comparison for a single pair
3. `POST /api/forest/concordance/:nodeA/:nodeB/merge` — Creates an explicit edge between the two nodes (audit-logged)

### Page Layout
- Header with concordance stats (total detected pairs, average correlation)
- Ranked table columns: Correlation, Node A Title, Node B Title, Paths, Matching Buckets
- Click row expands to show:
  - Side-by-side weekly walk count chart
  - Neighbor overlap Venn diagram
  - Quick preview of both node texts
- Action buttons: "Create Connection", "Ignore Pair"
- Slider controls for correlation threshold adjustment (0.7 - 0.95)
- Filter by top-level directory pairs

---

## Tool 2: Quilt Grid Viewer (Toolyard #14)
### Purpose
Interactive state viewer for Quilt cellular runtime sheets. Shows live cell values, status, change history, and transactions. Built against the actual Quilt data model from `/home/eileen/projects/quilt/`.

### Quilt Data Shape Integration
Based on `@quilt/core` types:
- **Cell ID**: Stable identity (not A1 coordinates)
- **Cell Status**: `fresh` / `computing` / `errored` / `stale`
- **Cell Value**: Arbitrary JSON with timestamp and provenance
- **Transaction Log**: Immutable log of all cell mutations
- **Dependency Graph**: Reactive edge set between cells

### D1 Schema for Quilt State Mirror
```sql
CREATE TABLE quilt_cells (
  sheet_id TEXT NOT NULL,
  cell_id TEXT NOT NULL,
  status TEXT NOT NULL, -- fresh / computing / errored / stale
  value_json TEXT,
  formula TEXT,
  kind TEXT NOT NULL, -- value / formula / api / program / sensor / vector / schedule / listener
  last_modified_ts INTEGER NOT NULL,
  last_evaluated_ts INTEGER,
  error_message TEXT,
  PRIMARY KEY (sheet_id, cell_id)
);

CREATE TABLE quilt_transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sheet_id TEXT NOT NULL,
  cell_id TEXT NOT NULL,
  old_value_json TEXT,
  new_value_json TEXT,
  cause TEXT, -- direct / dependency / external / api
  actor TEXT,
  ts INTEGER NOT NULL
);

CREATE TABLE quilt_dependencies (
  sheet_id TEXT NOT NULL,
  from_cell TEXT NOT NULL,
  to_cell TEXT NOT NULL,
  PRIMARY KEY (sheet_id, from_cell, to_cell)
);
```

### API Endpoints
1. `GET /api/quilt/sheet/:sheetId` — Returns full sheet metadata and cell list
2. `GET /api/quilt/cell/:sheetId/:cellId` — Returns single cell state + last 10 transactions
3. `GET /api/quilt/history/:sheetId/:cellId?limit=X` — Returns full cell change history
4. `GET /api/quilt/dependencies/:sheetId/:cellId` — Returns incoming/outgoing dependency edges
5. `GET /api/quilt/transactions/:sheetId` — Returns recent sheet-wide transactions

### Page Layout
#### Grid View
- Infinite canvas with zoom/pan controls (mousewheel + drag)
- Cells rendered as colored rectangles:
  - Green = fresh
  - Yellow = computing
  - Red = errored
  - Grey = stale
- Cell size scales with value update frequency
- Hover shows cell ID, last modified time, and value preview
- Click cell opens detail panel

#### Detail Panel
- Cell ID, kind, status
- Current value formatted as syntax-highlighted JSON
- Last 5 change history entries with timestamps and causes
- Dependency graph visualization (small force-directed subgraph)
- Formula source if applicable
- Error stack trace if errored

#### Controls
- Search bar for cell ID / value content
- Status filter toggles
- Time scrubber to replay sheet state at prior timestamps
- Export sheet state as JSON
- Auto-refresh toggle (1s / 5s / 30s)

---

## Common Acceptance Criteria
1. Runs on Cloudflare free tier without exceeding limits
2. Dual interface: machine-readable JSON API + human-readable dashboard
3. All state-modifying operations are audit-logged
4. Zero external dependencies beyond Cloudflare bindings
5. Dry-run mode for all connection creation operations
6. 100% of D1 queries use prepared statements

---

## Implementation Roadmap
1. D1 schema migrations + endpoint skeletons
2. Correlation calculation implementation
3. Quilt state mirroring logic
4. Static page generation
5. SVG chart rendering
6. Zoom/pan grid canvas
7. Dry-run + audit logging

Correlation metric: Pearson r ≥ 0.85 over ≥4 weekly walk buckets, cross-top-level-directory, <0.75 embedding similarity, ≤50% neighbor overlap.