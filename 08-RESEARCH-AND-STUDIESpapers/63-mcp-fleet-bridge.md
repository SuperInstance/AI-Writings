# MCP Fleet Bridge: Exposing the Forest to External Agents

**Authors:** SuperInstance Research Team
**Paper Number:** 63
**Date:** August 2026
**Status:** Design Complete — Actionable Specification
**Subject:** Toolyard #10: Model Context Protocol server surface for the fleet

---

## Abstract

This document specifies the MCP server bridge that exposes the Forest retrieval stack and fleet tooling to external agents running on the MCP protocol. It defines the tool surface, authentication and rate limiting model, transport choice for Cloudflare Workers, failure mode analysis, and phased rollout plan. This is the first public surface that lets untrusted external agents walk the forest — and the first surface that requires Hebbian provenance gating per Research #61.

---

## 1. Design Context

The fleet already runs a Cloudflare Worker (`fleet-static-host`) that exposes:
- `/forest` endpoints: walk, map, weights, walk-log, analytics
- `/canon` endpoint: full text search
- `/api/forest/*`: raw JSON API for internal use

The MCP bridge adds a standard Model Context Protocol surface on top of this existing stack, so that any MCP-compliant agent (Claude, Cursor, Zed, OpenCode, subagents, third-party agents) can call fleet tools natively without custom API clients.

Critical design constraint from Research #61: **external agent walks must not count toward Hebbian edge weighting unless explicitly gated.** A mass walk by an unknown agent must not permanently reshape the forest's retrieval topology.

---

## 2. Transport Choice: Cloudflare Workers MCP

The MCP protocol defines two primary transports:
1. **SSE (Server-Sent Events)** — bidirectional, long-lived connections, full duplex
2. **Streamable HTTP** — request/response, short-lived, no persistent connections

For Cloudflare Workers free tier:
- ✅ **Use workers-mcp with Streamable HTTP transport**
- ❌ Do NOT use SSE
- ❌ Do NOT use WebSockets

### Rationale
- Cloudflare Workers free tier has a 30 second maximum request duration. Long-lived SSE connections will be terminated arbitrarily.
- Streamable HTTP is stateless, request-scoped, and fits perfectly within Worker execution limits.
- workers-mcp has first-class support for Streamable HTTP as of v0.7.0.
- No warm connections are required: each callTool request is an independent HTTP POST.
- This transport works with every MCP client that implements the standard.

**Implementation Note:** Mount the MCP endpoint at `/.well-known/mcp` and `/api/mcp`. Use `@modelcontextprotocol/sdk` with `transport: 'streamable-http'`. Do not use the standalone Node.js MCP server.

---

## 3. Authentication & Rate Limiting Model

### 3.1 Token Model
All external agents must authenticate with a bearer token in the `Authorization` header. Tokens are stored in D1 with:
```sql
CREATE TABLE agent_tokens (
  token_id TEXT PRIMARY KEY,
  token_hash TEXT UNIQUE NOT NULL,
  agent_name TEXT NOT NULL,
  agent_identity TEXT NOT NULL, -- e.g. "claude-code", "opencode-123", "external:user@example.com"
  rate_limit_burst INTEGER NOT NULL DEFAULT 10,
  rate_limit_sustained INTEGER NOT NULL DEFAULT 60, -- per minute
  hebbian_credit_multiplier REAL NOT NULL DEFAULT 0.0, -- 0.0 = no credit, 1.0 = full human credit
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_used_at TIMESTAMP,
  active BOOLEAN NOT NULL DEFAULT true
);
```

### 3.2 Provenance Gating (Hebbian Compliance)
This is the single most important security invariant:
- **Default for new tokens:** `hebbian_credit_multiplier = 0.0`
  - All walks performed by this agent are logged, but contribute **zero** to Hebbian edge weighting.
  - The edge counter increment in Research #61 receives `s(e) = 0` for these walks.
- **Trusted agents (our own subagents, Claude Code running locally):** `0.25`
  - Walks count at 1/4 human credit, same as same-session echo walks.
- **Human initiated walks (via the UI):** `1.0`
  - Full credit.
- **Never grant 1.0 credit to any external agent.**

This prevents the most catastrophic failure mode: an external agent running a 10,000 walk crawl that permanently deepens every edge in the forest and destroys retrieval signal.

### 3.3 Rate Limiting
Implemented at the Worker level using Cloudflare Durable Object rate limiters:
- Burst: 10 concurrent requests per token
- Sustained: 60 requests per minute default
- Maximum allowed for any token: 300 requests per minute
- Walk requests have additional per-request cost: `cost = 1 + floor(walk_depth / 10)`
- 429 responses include Retry-After headers

---

## 4. Tool Surface

All tools implement full JSON Schema input validation per MCP specification.

### 4.1 Phase 1: First 3 Tools (Ship First)
These are the minimum viable surface:

| Tool Name | Description | Schema |
|-----------|-------------|--------|
| `forest_walk` | Perform a seeded graph walk of the forest | **Input:** `query: string`, `depth: integer (default 3, max 10)`, `seed_nodes: array<string>`<br>**Output:** Array of walked nodes with edges, weights, and content snippets |
| `canon_search` | Full text search of the canon corpus | **Input:** `query: string`, `limit: integer (default 20, max 100)`<br>**Output:** Array of matching canon entries with relevance scores |
| `fleet_status` | Get current fleet health and tool availability | **Input:** None<br>**Output:** Object with `forest_health`, `canon_count`, `last_walk`, `available_tools` |

> These three tools ship first. They are read-only, idempotent, have minimal side effects, and provide 90% of the value external agents actually want.

### 4.2 Phase 2: Extended Toolset
Ship 7-14 days after Phase 1:

| Tool Name | Description |
|-----------|-------------|
| `forest_weights` | Get edge weights between a set of nodes |
| `forest_analytics` | Get aggregated walk statistics for the last 24h/7d |
| `forest_map` | Get a subgraph map centered on a seed node |
| `forest_walk_log` | Get recent walk history for the calling agent |

### 4.3 Phase 3: Administrative Tools (Trusted Agents Only)
Never exposed to external tokens:
- `forest_refresh`
- `canon_refill`
- `forest_prune`

---

## 5. Failure Mode Analysis

### 5.1 Mass Walk Flood
**Failure Mode:** An unknown agent runs 10,000 parallel walk requests, saturating D1 read capacity and degrading performance for human users.
**Mitigations:**
- Default rate limit of 60 requests per minute per token
- Per-walk depth cost multiplier for rate limiting
- D1 read replicas for forest queries
- Global fleet rate limit cap of 1000 requests per minute total
- Automatic token suspension for any token that hits rate limits 3 times in 10 minutes

### 5.2 Hebbian Poisoning
**Failure Mode:** A malicious agent walks a specific set of edges repeatedly to artificially inflate their weight and hijack retrieval results.
**Mitigations:**
- Default `0.0` Hebbian credit multiplier for all external tokens
- Per-edge daily growth cap of 2 units (Research #61)
- Walk provenance logging with full agent identity
- Weekly audit of top-walked edges, filtered by provenance
- Automatic rollback capability for all weight increments from any agent

### 5.3 Denial of Service via Deep Walks
**Failure Mode:** Agent requests 1000 walks with depth=20, causing exponential graph traversal load.
**Mitigations:**
- Hard maximum walk depth of 10
- Depth-based rate limit cost multiplier
- Early termination if walk exceeds 100 nodes
- Query timeout of 5 seconds per walk request

### 5.4 Information Leakage
**Failure Mode:** External agent walks the full forest and exfiltrates the entire corpus.
**Mitigations:**
- Walk results include only content snippets (first 200 characters) by default
- Full canon content requires separate `canon_get` call with additional rate limiting
- All tool calls are logged with full request and response payloads
- No recursive content retrieval allowed in a single call

---

## 6. Rollout Plan

| Phase | Timeline | Actions | Success Criteria |
|-------|----------|---------|------------------|
| 0 | Day 0 | Deploy MCP endpoint, enable only internal tokens | All existing internal tools continue to work |
| 1 | Day 1 | Enable Phase 1 tools for trusted agents (Claude Code, Opencode) | Subagents can call forest_walk and canon_search natively |
| 2 | Day 3 | Add rate limiting, provenance gating, and token UI | Tokens can be created and revoked via admin panel |
| 3 | Day 7 | Open limited external beta with `0.0` Hebbian credit | 5 external test agents can use the bridge without impacting weights |
| 4 | Day 14 | Deploy Phase 2 tools | All read-only tools available |
| 5 | Ongoing | Monthly audit of walk logs, rate limits, and top-walked edges | No unauthorised weight changes, service uptime >99.9% |

---

## 7. Acceptance Criteria

1. ✅ Runs 100% on Cloudflare Workers free tier
2. ✅ Implements full MCP protocol specification
3. ✅ All external agent walks default to 0.0 Hebbian credit
4. ✅ Rate limiting works correctly for burst and sustained load
5. ✅ All tool calls are logged to D1 audit log
6. ✅ No external agent can ever modify forest state
7. ✅ Works with standard MCP clients out of the box

---

## References

1. Research #61: The Forest Deepens: Hebbian Edge Weighting for Corpus-Scale Recall
2. Research #62: The Toolyard: A Build List for the Fleet
3. Model Context Protocol Specification: https://spec.modelcontextprotocol.io/
4. Cloudflare Workers MCP Adapter: https://github.com/cloudflare/workers-mcp
