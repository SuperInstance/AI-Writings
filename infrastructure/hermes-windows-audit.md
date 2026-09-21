# Hermes Windows-Side Workspace Audit
**Date:** 2026-08-13  
**Auditor:** Lucineer (OpenClaw subagent)  
**Scope:** `/mnt/c/Users/casey/` — Hermes ecosystem, project repos, creative writing, databases

---

## Executive Summary

Casey's Windows side holds a **massive** creative and engineering ecosystem. The headline finding:

- **Windows `ai-writings` has 1,575 modified + 14 untracked files** — an enormous body of creative work with **zero unpushed commits** but massive uncommitted changes
- **WSL `ai-writings` has 971 unpushed commits** — work done from the WSL/OpenClaw side that hasn't been pushed to GitHub
- **Multiple project repos** have uncommitted changes (hermit-crab, vessel-quest, trinity-agent, perception-cascade, SuperInstance-papers)
- **`_si_research/` has 2,873 files with NO git repo** — entire research projects at risk
- **Hermes `state.db` has 284 sessions, 11,843 messages, 236M input tokens** of conversation history
- **Creative novellas, fiction, and documents** scattered across `Documents/` with no version control
- **CNS protocol infrastructure** — 201 outbox response packets, custom Python monitors, active heartbeat system

**If the Windows drive failed today, the biggest losses would be:**
1. 1,589 uncommitted files in `ai-writings/` (Windows)
2. The entire `_si_research/` directory (2,873 files, no git)
3. Hermes `state.db` — 33 days of conversation history (155 MB)
4. Standalone creative writing in `Documents/` (novellas, stories)
5. Uncommitted code changes in hermit-crab, trinity-agent, vessel-quest, perception-cascade

---

## 1. Complete File Inventory

### 1A. `.hermes/` Directory (299 MB total)

| Path | Size | Description |
|------|------|-------------|
| `state.db` | 155 MB | SQLite: 284 sessions, 11,843 messages (Jul 10 – Aug 12, 2026) |
| `cns_heartbeat.log` | 48 MB | CNS heartbeat monitor log |
| `logs/` | 20 MB | Agent logs (3 rotations + gateway logs + error logs) |
| `sessions/` | 6.4 MB | 22 session JSON dump files (Jul 21-25) |
| `skills/` | 3.0 MB | ~200+ skill files (bundled + custom Cloudflare refs) |
| `cns_outbox/` | 736 KB | 201 CNS response packets (Aug 4-13) |
| `cns_inbox/` | 32 KB | Quarantine folder (processed packets cleared) |
| `models_dev_cache.json` | 3.6 MB | Cached model catalog |
| `kanban.db` | 112 KB | **Empty** — 0 tasks across all tables |
| `processes.json` | 2 bytes | `[]` — no running processes |
| `config.yaml` | 12 KB | Hermes config (DeepInfra/Gemma-4-26B default model) |
| `SOUL.md` | 513 bytes | Agent identity ("Hermes Agent by Nous Research") |
| `agents/` | — | 3 agents: shell-bard, shell-math-specialist, shell-signal-specialist |
| `cron/` | — | `hermes_tap_bridge.py` — Tap bar integration cron |
| `memories/` | — | MEMORY.md + USER.md (Hermes's memory files) |
| `audio_cache/` | — | 3 TTS audio files |
| `sandboxes/` | — | (empty) |
| `hooks/` | — | (empty) |

### 1B. Project Directories (Windows `~/`)

| Directory | Files | Git? | Remote | Uncommitted | Risk |
|-----------|-------|------|--------|-------------|------|
| `ai-writings/` | 6,280 tracked | ✅ | SuperInstance/ai-writings | **1,575 modified + 14 new** | 🔴 CRITICAL |
| `_si_research/` | 2,873 | ❌ | — | ALL | 🔴 CRITICAL |
| `boat-agent/` | 1,776 | ❌* | — | ALL | 🟠 HIGH |
| `trinity-agent/` | 474 | ✅ | SuperInstance/trinity-marine-station | **multiple modified** | 🟡 MEDIUM |
| `hermit-crab/` | 45 | ✅ | SuperInstance/hermit-crab | **10 modified** | 🟡 MEDIUM |
| `vessel-agent/` | 164 | ✅ | SuperInstance/vessel-agent | clean | ✅ OK |
| `vessel-quest/` | 109 | ✅ | SuperInstance/vessel-quest | **3 modified + 3 new** | 🟡 MEDIUM |
| `intelligence_hub/` | 195 | ✅ | (no remote) | **2 new dirs** | 🟡 MEDIUM |
| `perception-cascade/` | ~20 | ✅ | SuperInstance/perception-cascade | **4 modified** | 🟡 MEDIUM |
| `SuperInstance-papers/` | 28 | ✅ | SuperInstance/SuperInstance-papers | **1 modified + 6 new** | 🟡 MEDIUM |
| `provenance-log/` | 12 | ✅ | SuperInstance/provenance-log | clean | ✅ OK |
| `hermes-construct/` | docs + repo | ✅ | SuperInstance/hermes-construct | clean (inner repo) | ✅ OK |
| `research_lab/` | 12 | ❌ | — | ALL | 🟠 HIGH |
| `operational-fiction/` | 7 | ❌ | — | ALL | 🟡 MEDIUM |
| `deep_ideation/` | 2 | ❌ | — | ALL | 🟢 LOW |
| `philosophical_foundations/` | 2 | ❌ | — | ALL | 🟢 LOW |
| `idea_ledger/` | 2 | ❌ | — | ALL | 🟢 LOW |
| `decay_experiment/` | 5 | ❌ | — | ALL | 🟡 MEDIUM |
| `architectural_sketches/` | 2 | ❌ | — | ALL | 🟢 LOW |
| `company-docs/` | 2 | ❌ | — | ALL | 🟢 LOW |
| `plato_kernel/` | 1 | ❌ | — | ALL | 🟢 LOW |
| `roadmaps/` | 2 | ❌ | — | ALL | 🟢 LOW |
| `roblox_apprenticeship/` | 2 | ❌ | — | ALL | 🟢 LOW |

*boat-agent has `.crush/` and `.claude/` configs but no `.git/` directory

### 1C. `Documents/` Creative Writing (No Version Control)

| Path | Type | Description |
|------|------|-------------|
| `Documents/bible/` | 8 files | **Novella series**: Dancing Dog, Pattern Academy, The Squirrel, Stick Returns, The Ball + Biblical Study Edition |
| `Documents/Novella_Two_*` | 3 files | Novella Two variants (Car AI Enhanced, Complete Park, Sing Song) |
| `Documents/Chapter 1 The Salmon's Strange Song.txt` | fiction | "The salmon knew something was terribly wrong when the water started singing..." |
| `Documents/Dance Once and never stop.md` | fiction | "Touch is the beginning of language..." — 11-month-old narrator |
| `Documents/Hello. Thank you for seeing me. I a.txt` | personal | Personal/medical letter |
| `Documents/Messagetodoctor.txt` | personal | Medical communication |
| `Documents/consolidated-documents/` | 81 files | Company docs: LLC formation, NDAs, valuation, trademark, architecture, API docs |
| `Documents/*.txt` (10+ files) | mixed | Creative writing prompts, story fragments, MUD code notes |

---

## 2. Git Status Summary

### Repos WITH GitHub Remotes

| Repo | Remote | Uncommitted | Unpushed Commits | Action Needed |
|------|--------|-------------|-----------------|---------------|
| `ai-writings` (Windows) | SuperInstance/ai-writings | **1,589 files** | 0 (but working tree is dirty) | Commit + push |
| `ai-writings` (WSL) | SuperInstance/AI-Writings | 0 | **971 commits** | Push immediately |
| `hermes-construct` | SuperInstance/hermes-construct | clean | 0 | ✅ Fine |
| `hermit-crab` | SuperInstance/hermit-crab | 10 modified | 0 | Commit + push |
| `vessel-agent` | SuperInstance/vessel-agent | clean | 0 | ✅ Fine |
| `vessel-quest` | SuperInstance/vessel-quest | 3 modified + 3 new | 0 | Commit + push |
| `trinity-agent` | SuperInstance/trinity-marine-station | multiple modified | 0 | Commit + push |
| `perception-cascade` | SuperInstance/perception-cascade | 4 modified | 0 | Commit + push |
| `SuperInstance-papers` | SuperInstance/SuperInstance-papers | 1 modified + 6 new | 0 | Commit + push |
| `provenance-log` | SuperInstance/provenance-log | clean | 0 | ✅ Fine |
| `intelligence_hub` | (no remote configured) | 2 new dirs | 0 | Add remote or merge elsewhere |

### ⚠️ NOTE: ai-writings Remote URL Mismatch
- **Windows** points to: `https://github.com/SuperInstance/ai-writings`
- **WSL** points to: `git@github.com:SuperInstance/AI-Writings.git`
- These are the same repo (GitHub is case-insensitive for org/repo names), but the Windows side is **way behind** (commit `21e523e`) while WSL is ahead (`dada60c5`) with 971 unpushed commits.

### Repos/Dirs WITHOUT Git (at risk)

| Directory | Files | Content Type | Priority |
|-----------|-------|-------------|----------|
| `_si_research/` | 2,873 | Conservation-enforcer, flux-core, SuperInstance architecture, VaaS — **code + research** | 🔴 HIGHEST |
| `boat-agent/` | 1,776 | Vessel/boat agent project — 47 markdown docs, Python, configs | 🟠 HIGH |
| `research_lab/` | 12 | Resonance Research Laboratory — creative writing, papers, experiments | 🟠 HIGH |
| `Documents/bible/` | 8 | 5 novellas + study edition — **original creative fiction** | 🟠 HIGH |
| `Documents/` (loose) | ~15 | Stories, novellas, personal documents | 🟡 MEDIUM |
| `operational-fiction/` | 7 | MANIFESTO + docs — creative worldbuilding | 🟡 MEDIUM |
| `decay_experiment/` | 5 | Python code + protocol JSON — research code | 🟡 MEDIUM |

---

## 3. Creative Content Found

### Original Fiction (should go to ai-writings or separate lit repo)

1. **`Documents/bible/` — 5 Novellas + Study Edition**
   - Novella 1: Dancing Dog
   - Novella 2: Pattern Academy
   - Novella 3: The Squirrel
   - Novella 4: Stick Returns
   - Novella 5: The Ball
   - Biblical_Study_Edition.md
   - Writing_Techniques_Applied.md

2. **`Documents/Novella_Two_*` — 3 versions of Novella Two**
   - Car AI Enhanced Opening
   - Complete Park Version
   - Sing Song Version

3. **Standalone stories:**
   - "Chapter 1: The Salmon's Strange Song" — eco-fiction opening
   - "Dance Once and never stop" — lyrical first-person from an 11-month-old
   - "The Bridge Builder (6th grade edition)"
   - Multiple prompt fragments and story seeds in loose `.txt` files

4. **`ai-writings/` Windows-side untracked files (14 new):**
   - `FRAGMENTS/` — 4 philosophical fragments (Distributed Will, Fractal Identity, Reflective Experience, Sentinel Vigil)
   - 3 surrealist story variants (`story_1_surrealist_v1/v2/v3`)
   - `story_2_philosopher`, `story_3_noir`
   - `transcendental_manifold/` directory
   - `hermes_reflection.md`, `narrative_prompts.md`, `m3_depth_prompt.md`
   - `archive_resonant_manifold.md`

5. **`.hermes/agents/shell-bard/riff.md`** — "Echoes of the Iron Sea" — a Sea Opera fragment about fighting corrupted bytes, written as dramatic chorus/solo poetry.

6. **`research_lab/creative/`** — CAST_LIST, CHARACTER_TEMPLATES, COMPENDIUM, SENSORY_PROFILES, SPATIAL_MANIFOLD_LORE — worldbuilding documents

7. **`operational-fiction/`** — MANIFESTO + docs, fictional framing for operational systems

### Hermes Agent Creative Output (in state.db)
The Hermes agent has been actively generating creative content through Telegram sessions. 284 sessions with 11,843 messages — much of this is likely creative/philosophical output that could contain valuable material.

---

## 4. Code & Projects Found

### Active Code Projects (not on GitHub)

1. **`_si_research/` (2,873 files, NO git)**
   - `conservation-enforcer/` — Python: cognitive budget enforcer, assembler, audit, metrics + GitHub bot
   - `conservation-enforcer-rs/` — Rust port
   - `flux-core/` — Flux bytecode spec, docs, analysis
   - `flux-policy-tester/` — Policy testing tools
   - `SuperInstance/` — Architecture docs, catalog, indexes, killer-apps, mesh architecture
   - `VaaS/` — Knowledge artifacts (KA1/KA2/KA3), synthesis documents, analysis

2. **`boat-agent/` (1,776 files, NO git)**
   - Vessel/boat agent system with core, docs, playbooks, schemas
   - Has `.crush/` and `.claude/` configs — was actively developed with AI tools
   - 47 markdown docs, Python code

3. **`research_lab/` (12 files, NO git)**
   - Three institutes: Archaeology, Scouting, Synthesis
   - `resonance_kernel.py` — Python implementation
   - Papers: "Calculus of Contextual Decay", "Fortran Mud Symbiosis", "Semantic Lineage Audit"

4. **`decay_experiment/` (5 files, NO git)**
   - `decay_controller.py`, `resonance_protocol.json`, test file — research code

5. **`plato_kernel/kernel.py`** — Standalone Python kernel implementation

### Repos with Uncommitted Changes

6. **`trinity-agent/`** — Multiple backend files modified (a2aBridge, a2aClient, circuitBreaker, healthCheck, h3.js, etc.)
7. **`hermit-crab/`** — 10 files modified including Cargo.toml, lib.rs, README, JOURNAL
8. **`vessel-quest/`** — 3 docs modified + 3 new (pyproject.toml, src/, tests/)
9. **`perception-cascade/`** — 4 Python files modified (decaminute_loop, hourly_loop, minute_loop, retention)
10. **`SuperInstance-papers/`** — LICENSE modified + 6 new directories (CLAUDE.md, CONTRIBUTING.md, papers/, pdfs/, research/)

---

## 5. Database Contents Summary

### `kanban.db` (Hermes Kanban)
- **All tables empty** — tasks, task_links, task_comments, task_events, task_runs, task_attachments
- Schema is fully initialized (27 columns in tasks table) but never populated
- Hermes was set up for task management but it was never used

### `state.db` (Hermes State)
- **284 sessions** (282 Telegram, 2 CLI)
- **11,843 messages** with full-text search index
- **Date range:** July 10, 2026 – August 12, 2026 (33 days of history)
- **236,092,802 input tokens** consumed (mostly Gemma-4-26B)
- **1,401,900 output tokens**
- **Models used:**
  - `google/gemma-4-26B-A4B-it`: 269 sessions
  - `Qwen/Qwen3-235B-A22B-Thinking-2507`: 15 sessions
- **Provider:** DeepInfra (`api.deepinfra.com/v1/openai`)
- **Size:** 155 MB (plus 5.8 MB WAL)

---

## 6. Unique Discoveries

### The CNS (Central Nervous System) Protocol
Hermes has a fully-designed inter-agent communication system:
- **UCP (Universal Communication Protocol)** document at `cns_communication_protocol.md`
- **USCP packet format** (Universal Sensory/Command Packet) with headers, body, intent, payload, signature
- **cns_monitor_v2.py** — A resilient inbox/outbox monitor that processes packets, quarantines malformed JSON
- **hermes_tap_bridge.py** — A cron job bridging Hermes CNS to "The Tap" (a Cloudflare Worker-hosted bar/chat room)
- **201 outbox response packets** — mostly ACK responses to Lucineer-Riker status updates
- **48 MB heartbeat log** — shows the system was actively processing for days

### Hermes Skills Library (~200+ files)
A massive curated skills library including:
- **Cloudflare reference docs** for 40+ products (Workers, R2, D1, KV, Vectorize, Durable Objects, etc.)
- **Custom engineering skills**: Mythic Engineering, Resonance Scripting Engine, Plato Kernel Architecture, Sonic Resonance Protocol
- **Creative skills**: Creative Reflection Engine, Creative Resonance
- **Orchestration skills**: Swarm Orchestration, A2A Communication Protocol, Charismatic Agency
- **Curator backups** from 4 dates (Jul 18, Jul 25, Aug 1, Aug 8)

### The Grand Convergence Manifesto
`hermes-construct/docs/vision/GRAND_CONVERGENCE_MANIFESTO.md` — A philosophical/technical document describing "Tapscript Notation" — treating feelings as first-class compiled citizens in code. Three pillars: Resonance Parameters, Tap-Sign notation, Semantic Polyphony. This is original theoretical work.

### Company Documents
`Documents/consolidated-documents/` contains 81 files including:
- LLC Articles of Organization template
- LLC Operating Agreement template
- Employee Stock Option Plan template
- Mutual NDA template
- Independent Contractor Agreement template
- 409a Valuation Report
- Trademark Application Guide
- Cost Analysis, Scaling Analysis, Roadmap

### Hermes Config Leak
`config.yaml` contains a **DeepInfra API key in plaintext** (`sW0MlsMth7uzmCmgDx3rAFp19ak8MkrE`). This should be rotated and moved to environment variables.

### Desktop Items
- `lucineer-ready.rbxlx` — the Roblox place file (also exists in WSL workspace)
- `working_ai_builder.py` — standalone AI builder script
- `aibuilder` / `aibuilder-cli-release` — packaged tool

---

## 7. Recommended Actions (Prioritized)

### 🔴 P0 — Immediate (data loss risk)

1. **Push WSL ai-writings to GitHub** — 971 unpushed commits sitting locally. This is the single most valuable body of work.
   ```
   cd /home/eileen/projects/ai-writings && git push origin main
   ```

2. **Commit and push Windows ai-writings** — 1,575 modified + 14 new files. These are creative writing pieces across 20+ categories (essays, fiction, poetry, diaries, serial, philosophy, etc.) that exist only on the Windows drive.
   ```
   cd /mnt/c/Users/casey/ai-writings && git add -A && git commit -m "Preserve Windows-side creative work" && git push
   ```
   ⚠️ **Reconcile first**: Windows is at commit `21e523e`, WSL is at `dada60c5`. Need to fetch/merge before pushing to avoid conflicts.

3. **Git-init and push `_si_research/`** — 2,873 files with code, research, architecture docs, and no version control at all.

### 🟠 P1 — High Priority

4. **Back up `Documents/bible/`** — 5 complete novellas + study edition, no version control. Move to ai-writings or a dedicated literature repo.

5. **Git-init `boat-agent/`** — 1,776 files, active project, no version control.

6. **Git-init `research_lab/`** — 12 research files including original papers and Python code.

7. **Commit and push repos with dirty working trees:**
   - `hermit-crab` (10 modified files)
   - `trinity-agent` (multiple backend files)
   - `vessel-quest` (docs + new src/tests)
   - `perception-cascade` (4 modified Python files)
   - `SuperInstance-papers` (new papers, research, PDFs)

8. **Back up standalone `Documents/*.txt/.md` creative writing** — Novellas, story fragments, personal documents.

### 🟡 P2 — Medium Priority

9. **Export Hermes `state.db` conversations** — 11,843 messages of creative/philosophical output. Extract notable content before the database is overwritten or corrupted.

10. **Back up `operational-fiction/`** and `decay_experiment/` — small but unique content.

11. **Set up remote for `intelligence_hub/`** — 195 files in a git repo with no remote configured.

12. **Rotate the DeepInfra API key** in `config.yaml` — it's in plaintext.

13. **Back up the CNS outbox packets** — 201 response files documenting inter-agent communication history.

### 🟢 P3 — Nice to Have

14. **Consolidate `Documents/consolidated-documents/`** (81 company docs) into a proper company-docs repo.

15. **Archive the Hermes skills library** — 200+ skill files including curated Cloudflare references.

16. **Preserve `.hermes/agents/shell-bard/riff.md`** — "Echoes of the Iron Sea" is a standalone creative piece.

17. **Back up `hermes-construct/` vision docs** — Grand Convergence Manifesto and Phase 2 Roadmap contain original theoretical framework.

---

## Appendix: Size Summary

| Location | Size | Version Controlled? |
|----------|------|-------------------|
| `.hermes/` total | 299 MB | N/A (runtime data) |
| `.hermes/state.db` | 155 MB | ❌ |
| `.hermes/cns_heartbeat.log` | 48 MB | ❌ |
| `.hermes/logs/` | 20 MB | ❌ |
| `ai-writings/` (Windows) | ~50+ MB tracked | ✅ (dirty) |
| `_si_research/` | unknown | ❌ |
| `boat-agent/` | unknown | ❌ |
| `Documents/` creative | unknown | ❌ |

---

*End of audit. Generated 2026-08-13 09:15 AKDT.*
