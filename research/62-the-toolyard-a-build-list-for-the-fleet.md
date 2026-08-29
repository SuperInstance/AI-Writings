# The Toolyard: A Build List for the Fleet

Last Updated: 2026-08-29
Priority: Actionable

This is the complete working toolkit for the vision. All tools run on Cloudflare free tier (D1, Vectorize, Workers, R2). No paid services.

---

## RANKED BUILD LIST (16 items total)

Priority order: top = build first.

| Rank | Name | One-line Purpose | Surface | Effort | Best Crew | Acceptance Check |
|------|------|------------------|---------|--------|-----------|------------------|
| **1** | `forest-refresh` | Automated incremental forest walker that deepens high-weight edges and prunes dead branches on cron | Worker endpoint + CLI | S | GLM-5.3 | Runs hourly, logs walk depth, prunes <0.01 weight edges, no downtime |
| **2** | `canon-stats` | Real-time canon corpus health dashboard: count, embedding coverage, duplicate rate, drift score | Page + worker endpoint | S | Kimi | Page loads in <500ms, shows last 7d embed trends, flags duplicates >0.95 cosine |
| **3** | `forest-diff` | Side-by-side comparison of forest graph state between two timestamps | CLI + page | M | OpenCode | Outputs added/removed nodes, weight changes, critical path deltas; human-readable summary |
| **4** | `walk-analytics` | Aggregated walk log viewer: path heatmaps, most visited nodes, average depth, agent residency patterns | Page + worker | M | Claude | Shows 24h/7d/30d trends, exports walk paths for analysis, no PII |
| **5** | `residency-monitor` | OpenConstruct RoomResidency dashboard: active agents, room occupancy, message rates, idle times | Page + websocket endpoint | M | Kimi | Real-time updates <1s, shows agent model distribution, last activity per room |
| **6** | `canon-dedupe` | Batch deduplicator that merges near-duplicate canon entries and preserves highest quality version | CLI + worker endpoint | M | GLM-5.3 | Removes >0.92 cosine duplicates, preserves oldest source, logs merges |
| **7** | `forest-visualizer` | Interactive force-directed graph of the forest with weight-based edge thickness and node size | Page | L | Kimi | Zoomable, click nodes to see walk history, filter by weight threshold, loads 10k nodes smoothly |
| **8** | `edge-hub-audit` | Fleet edge worker health monitor: latency, error rates, queue backlog, vectorize performance | Page + worker | S | OpenCode | Shows last 100 requests, 95th percentile latency, alerts on >5% error rate |
| **9** | `canon-refill` | Intelligent canon backfiller that finds missing context gaps from walk logs and embeds them | CLI + cron worker | M | Seed-mini | Identifies nodes with <3 incoming edges, pulls relevant context, runs nightly |
| **10** | `mcp-fleet-bridge` | Standard MCP server surface exposing all fleet tools to external agents | Worker endpoint | M | GLM-5.3 | Implements MCP protocol, supports listTools/callTool, rate limits per agent |
| **11** | `forest-prune` | Manual and automated pruning tool with safety thresholds: dry run, confirm, archive | CLI + page | M | OpenCode | Never deletes, only archives nodes; dry run shows impact before commit |
| **12** | `scrapcraft-admin` | Scrapcraft game admin panel: world state, active players, build queues, event logs | Page | L | Kimi | Shows chunk load status, player inventory counts, ability to pause/resume world |
| **13** | `embed-qc` | Embedding quality control: verifies vector consistency, checks for failed embeds, recalculates drift | CLI + cron | S | GLM-5.3 | Scans 1% of corpus nightly, flags vectors with <0.7 average similarity to neighbors |
| **14** | `quilt-grid-viewer` | Interactive quilt/quilt-rust grid state viewer with cell history and transaction logs | Page | M | OpenCode | Shows cell values, last modified, change history, zoom/pan across full grid |
| **15** | `elephant-jepa-monitor` | JEPA model training dashboard: loss curves, embedding quality, prediction accuracy over time | Page | M | Claude | Updates every 5 minutes, shows train/val loss, example predictions |
| **16** | `fleet-task-orchestrator` | Priority queue for fleet-wide jobs: status tracking, retries, backpressure, parallelism limits | Worker + CLI | L | GLM-5.3 | At-most-once delivery, dead letter queue, max 10 concurrent jobs per worker |

---

## Implementation Notes

### General Rules
- All CLI tools are `wrangler run` compatible, no local node dependencies
- All pages are static Workers Sites, no frontend framework bloat
- All endpoints are idempotent
- All state lives in D1 / Vectorize / R2, no external databases
- Cron jobs run at minimum 15 minute intervals on free tier

### Crew Assignments Rationale
- **GLM-5.3**: Systems design, state management, distributed logic, correctness
- **KimiCode**: Spatial interfaces, visualizations, real-time components, web UI
- **OpenCode**: Engineering, CLI tools, correctness, low-level implementation
- **Claude**: Polish, UX, dashboards, human-readable outputs, documentation
- **Seed-mini**: Creative filling, gap detection, pattern matching

---

## Rollout Order

Phase 1 (0-3 days): 1, 2, 8, 13
Phase 2 (3-7 days): 3, 4, 6, 9
Phase 3 (7-14 days): 5, 7, 10, 11
Phase 4 (14+ days): 12, 14, 15, 16

---

## Acceptance Criteria Common To All Tools
1. Works on Cloudflare free tier without exceeding limits
2. Has both agent-readable (JSON) and human-readable interfaces
3. Has dry run mode for all destructive operations
4. Logs all actions to D1 audit log
5. Has zero external dependencies except Cloudflare bindings

This is the complete toolyard. Build in order.
