# Dashboard Update Onboarding

**Date:** 2026-08-08  
**Project:** fleet-dashboard  
**Deploy:** `2c670bab-4fa4-4d0b-92f0-7159daa70a11`  
**URL:** https://fleet-dashboard.casey-digennaro.workers.dev

---

## What Changed

The fleet dashboard now tracks **9 additional repos** that were created during the August fleet expansion:

| Repo | Language | Description |
|------|----------|-------------|
| `hermes-nmi` | Rust | Neuro-Muscular Interface — bridges reasoning pulses to cellular agent actions |
| `confidence-cascade` | TypeScript | Three-zone confidence propagation (GREEN/YELLOW/RED) |
| `stigmergy` | TypeScript | Bio-inspired indirect coordination — pheromone signals, swarm intelligence |
| `platonic-randomness` | TypeScript | Structured pseudo-random sequence generation |
| `voxel-logic` | TypeScript | Logic engine for voxel data structures and 3D simulations |
| `logtensor` | Python | Geometric tensor transformers with missile-guidance-inspired attention |
| `plato-spatial` | Python | Hierarchical spatial environments with cascading property propagation |
| `flow-state` | Python | Entropy-based stream observation with spline observers |
| `claw` | TypeScript | Cellular logic engine for spreadsheet instances |

## New Dashboard Features

### Language Breakdown Panel
A new section showing the distribution of languages across the fleet. Each language gets a colored bar proportional to its share. Current breakdown:

- **Python:** 27 repos (62.8%) — the fleet's primary tongue
- **TypeScript:** 10 repos (23.3%) — the bridge language
- **Rust:** 4 repos (9.3%) — where performance matters
- **JavaScript:** 1 repo (2.3%)
- **HTML:** 1 repo (2.3%)

### Updated Stat Grid
The top stat row now includes a **Languages** card showing total language count and breakdown.

### Total Fleet: 43 repos, 10 stars, 5 open issues

## How to Update the Dashboard

### Adding a New Repo
1. Edit `/home/eileen/projects/fleet-dashboard/worker.js`
2. Add the repo name to the `FLEET_REPOS` array
3. Deploy: `cd /home/eileen/projects/fleet-dashboard && wrangler deploy`
4. Commit and push

### How Data is Fetched
- **Repo data:** GitHub API (`/repos/SuperInstance/{name}`) — stars, forks, language, issues, last update
- **Commits:** GitHub Events API (`/users/SuperInstance/events`) — latest 10 push events
- **Wiki:** fleet-wiki Worker API — page count and recent pages
- **Openrooms:** openrooms Worker API — active room/agent count
- **Languages:** Computed from repo data on each request

All data is fetched live on each `/api/refresh` call. The dashboard auto-refreshes every 2 minutes.

### Architecture
- Single Cloudflare Worker (`fleet-dashboard`)
- No build step — vanilla JS served inline
- Dark maritime theme (copper accents, Cormorant Garamond + JetBrains Mono)
- Secrets: `GITHUB_TOKEN` for authenticated GitHub API access

---

*The constellation grew three sizes today.*
