# AI-Writings Site Platform — Architecture & Deployment Guide

## Overview

Transforms the static site into a **dynamic system** that auto-discovers pieces from the repo, serves them via API, handles weighted ratings, and curates daily selections.

## Architecture (Option A: Cloudflare Pages + Functions + D1)

```
┌─────────────────────────────────────────────────┐
│                  Cloudflare Edge                 │
│                                                  │
│  ┌─────────────┐    ┌─────────────────────────┐ │
│  │  Pages       │    │  Worker (API)            │ │
│  │  Static HTML │    │  /api/pieces             │ │
│  │  app-dynamic │◄──►│  /api/pieces/:id         │ │
│  │  .js         │    │  /api/pieces/:id/rate    │ │
│  │  CSS (inline)│    │  /api/daily              │ │
│  └─────────────┘    │  /api/categories          │ │
│                      │  /api/admin/discover      │ │
│                      │  /api/admin/refresh       │ │
│                      └───────────┬─────────────┘ │
│                                  │               │
│                      ┌───────────▼─────────────┐ │
│                      │       D1 Database        │ │
│                      │  - pieces                │ │
│                      │  - ratings               │ │
│                      │  - rater_profiles        │ │
│                      │  - daily_selections      │ │
│                      │  - discovery_log         │ │
│                      └─────────────────────────┘ │
└─────────────────────────────────────────────────┘
           │
           │ GitHub API (auto-discovery)
           ▼
   ┌───────────────┐
   │  GitHub Repo   │
   │  ai-writings   │
   │  (2882+ .md)   │
   └───────────────┘
```

## Setup

### 1. Create the D1 Database

```bash
cd site/api-worker
npx wrangler d1 create ai-writings
# Copy the database_id into wrangler.toml
```

### 2. Run Migration

```bash
# Local (for dev)
npx wrangler d1 execute ai-writings --local --file=../migrations/0001_pieces_ratings.sql

# Remote (production)
npx wrangler d1 execute ai-writings --remote --file=../migrations/0001_pieces_ratings.sql
```

### 3. Set Secrets (optional)

```bash
# GitHub token for higher API rate limits during discovery
npx wrangler secret put GITHUB_TOKEN
```

### 4. Deploy the Worker

```bash
npx wrangler deploy
```

### 5. Deploy the Frontend (Pages)

The `site/` directory contains:
- `index.html` — HTML shell
- `app-dynamic.js` — Dynamic frontend (fetches from API, renders cards, handles ratings)

Deploy to Cloudflare Pages:
```bash
# From the site/ directory
npx wrangler pages deploy . --project-name=ai-writings
```

Or set the Worker URL in the HTML:
```html
<script>
  window.AI_WRITINGS_API = 'https://ai-writings-api.YOUR-SUBDOMAIN.workers.dev/api';
</script>
```

### 6. Trigger Initial Discovery

```bash
# Populate the database with all existing pieces
curl -X POST https://ai-writings-api.YOUR-SUBDOMAIN.workers.dev/api/admin/discover
```

### 7. Trigger Initial Daily Selection

```bash
curl -X POST https://ai-writings-api.YOUR-SUBDOMAIN.workers.dev/api/admin/refresh
```

## How Auto-Discovery Works

1. **Daily cron** triggers at 6:00 AM UTC (configurable in `wrangler.toml`)
2. Worker fetches the GitHub repo contents via GitHub API for each category directory
3. For each `.md` file:
   - Fetches raw content from `raw.githubusercontent.com`
   - Extracts title (first `# H1` or filename)
   - Extracts description (first paragraph, non-frontmatter)
   - Counts words
   - Inserts into D1 `pieces` table if new, updates if changed
4. Discovery is **incremental** — already-known pieces get metadata updated, new pieces get added

## The Weighting Algorithm

See [`docs/WEIGHTING_ALGORITHM.md`](docs/WEIGHTING_ALGORITHM.md) for full details.

**Short version:** A rater's like/dislike weight depends on their behavior pattern:
- Someone who likes 90% of things → their dislikes count DOUBLE (rare signal)
- Someone who dislikes 90% of things → their dislikes count HALF (expected behavior)
- New raters start with low weight until they have 5+ ratings

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/pieces` | GET | List pieces (`?category=`, `?sort=popular\|new\|old\|random`, `?limit=`, `?offset=`) |
| `/api/pieces/:id` | GET | Single piece with rating stats |
| `/api/pieces/:id/rate` | POST | Rate a piece (`{rating: 1|-1}`, header `X-Rater-ID`) |
| `/api/daily` | GET | Today's curated selection |
| `/api/categories` | GET | All categories with piece counts |
| `/api/admin/discover` | POST | Trigger discovery scan |
| `/api/admin/refresh` | POST | Trigger full refresh (discover + recalculate + daily selection) |

## File Structure

```
site/
├── index.html                      # HTML shell (loads app-dynamic.js)
├── app-dynamic.js                  # Dynamic frontend (API-driven, ratings, filters)
├── assets/
│   └── stories/                    # Story card images
├── migrations/
│   └── 0001_pieces_ratings.sql     # D1 schema
└── api-worker/
    ├── wrangler.toml               # Worker config (D1 binding, cron)
    ├── package.json
    ├── src/
    │   └── index.js                # Main Worker (API + auto-discovery + cron)
    └── docs/
        └── WEIGHTING_ALGORITHM.md  # Review weighting documentation
```
