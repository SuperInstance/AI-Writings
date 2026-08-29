# 63 — Divergent Fleet Tools: Marooned Chunk Rescuer + Agent Tide Gauge
Last Updated: 2026-08-29
Stack: Cloudflare Worker + D1 (forest_nodes, forest_edges, forest_walks)

---

## Tool 1: Marooned Chunk Rescuer
### Purpose
Identify and surface *marooned* forest nodes (content chunks) that have no active incident edges (or only stale, low-weight edges) — these are chunks orphaned from the fleet's knowledge graph, with no active connections to other content. Rescue action = surface the chunk in user walk suggestions without deleting the node.

### D1 SQL Implementation
```sql
-- Find all marooned nodes: no active edges (weight >= 0.01 threshold from forest-refresh)
SELECT
  n.id,
  n.title,
  n.path,
  n.text,
  n.created_ts,
  -- Calculate age in days
  ROUND((JULIANDAY('now') - JULIANDAY(n.created_ts)), 2) AS age_days,
  -- Rank by text richness (longer text = more valuable to rescue)
  LENGTH(n.text) AS text_length
FROM forest_nodes n
WHERE NOT EXISTS (
  SELECT 1
  FROM forest_edges e
  WHERE (e.src = n.id OR e.dst = n.id)
    AND e.weight >= 0.01
)
-- Rank oldest first, then most text-rich
ORDER BY age_days DESC, text_length DESC
-- Optional pagination for large fleets
LIMIT ? OFFSET ?;
```

### API Endpoints
1. `GET /api/marooned-chunks?limit=X&offset=Y` — Returns JSON list of marooned chunks
2. `POST /api/rescue-chunk?id=:chunkId` — Adds a temporary high-weight edge to the current user's walk session, surfacing the chunk in their next walk suggestions. No permanent graph changes.

### Page Layout
Simple, unobtrusive dashboard:
- Header with tool name and quick stats (total marooned chunks)
- Sortable table columns: Chunk ID, Path/Title, Age (days), Text Length
- Action button per row: "Add to Walks" (triggers `/api/rescue-chunk`)
- Pagination controls for large result sets
- Dry-run toggle to preview marooned chunks without displaying action buttons

---

## Tool 2: Agent Tide Gauge
### Purpose
Visualize fleet activity (walks + queries) over time as a tide chart, with configurable time scales (24h/7d/30d) and automated anomaly detection ("storm surge" alarms for unexpected traffic spikes).

### SQL Aggregation Sketches
#### Time-Bucketed Activity
```sql
-- 24h scale: per-minute buckets
SELECT
  strftime('%Y-%m-%dT%H:%M:00', ts) AS bucket,
  COUNT(*) AS event_count
FROM forest_walks
WHERE ts >= DATETIME('now', '-24 hours')
GROUP BY bucket
ORDER BY bucket ASC;

-- 7d scale: per-hour buckets
SELECT
  strftime('%Y-%m-%dT%H:00', ts) AS bucket,
  COUNT(*) AS event_count
FROM forest_walks
WHERE ts >= DATETIME('now', '-7 days')
GROUP BY bucket
ORDER BY bucket ASC;

-- 30d scale: per-day buckets
SELECT
  strftime('%Y-%m-%d', ts) AS bucket,
  COUNT(*) AS event_count
FROM forest_walks
WHERE ts >= DATETIME('now', '-30 days')
GROUP BY bucket
ORDER BY bucket ASC;
```

#### Anomaly Detection (Storm Surge Alarm)
Calculate moving average and standard deviation for the current time period; flag any bucket with `event_count > (mean + 2 * stddev)` as a storm surge event. Log all alarms to a `forest_alerts` table for auditing:
```sql
-- Example anomaly check for 24h data
WITH activity AS (
  SELECT
    strftime('%Y-%m-%dT%H:%M:00', ts) AS bucket,
    COUNT(*) AS event_count
  FROM forest_walks
  WHERE ts >= DATETIME('now', '-24 hours')
  GROUP BY bucket
),
stats AS (
  SELECT
    AVG(event_count) AS mean_count,
    STDDEV(event_count) AS stddev_count
  FROM activity
)
SELECT
  a.bucket,
  a.event_count,
  s.mean_count,
  s.stddev_count,
  CASE WHEN a.event_count > (s.mean_count + 2 * s.stddev_count) THEN 1 ELSE 0 END AS is_storm_surge
FROM activity a, stats s;
```

### SVG Rendering Approach
Use a lightweight, self-contained SVG chart generator deployed directly in the Worker script:
1. Precompute time-bucketed data and anomaly flags
2. Generate SVG path elements for the tide line using bundled `d3-shape` (10KB dependency)
3. Add interactive tooltips using hidden SVG rect elements and inline JS event listeners
4. Embed all CSS directly in the SVG for standalone functionality
5. No external CDN dependencies — all assets are bundled with the Worker.

### Page Layout
- Time scale selector (24h / 7d / 30d)
- Main tide chart with hover tooltips showing bucket timestamp and event count
- Storm surge alarm banner (red background) displayed when any anomalies are detected in the current period
- Recent alarms log table showing timestamp, event count, and threshold breach
- Export button to download chart data as CSV or SVG

---

## Acceptance Criteria
1. Runs on Cloudflare free tier without exceeding rate limits
2. Provides both JSON API and human-readable dashboard interfaces
3. Dry-run mode for all surface operations (no permanent graph changes)
4. Logs all rescue and alarm actions to a D1 audit log
5. Zero external dependencies beyond Cloudflare bindings and lightweight bundled libraries