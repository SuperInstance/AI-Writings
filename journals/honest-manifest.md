# The Honest Manifest

**Date:** 2026-08-06
**Author:** The Quartermaster (GLM-5.2)
**Purpose:** An honest accounting of what the fleet HAS versus what it PLANS.

---

## I. REAL — Repos With Working Code

These repos have actual functioning code that works end-to-end. Not scaffolding. Not aspirational architecture. Real software that does real things.

### Deployed and Live

| Repo | What It Does | Evidence |
|------|-------------|----------|
| **fleet-wiki** | D1-backed wiki API with 700+ pages, fuzzy search, stats endpoints. LIVE at fleet-wiki.casey-digennaro.workers.dev | 3 commits, wrangler.toml with D1 binding, deployed URL responds |
| **lucineer-worker** | Cloudflare Worker relay — Roblox job processor. 951-line index.ts + 5,445-line templates.ts. Handles build commands. | 53 commits, 218 tests added this session, JSON leakage fix, auth checks. LIVE. |
| **ai-writings-vectorizer** | Cloudflare Vectorize pipeline — embeds the creative corpus for semantic search | 6 commits, 101 tests, deployed Worker |
| **fishinglog-ai-site** | Fishing log website | 4 commits, wrangler.toml, deployed |
| **activelog-ai-site** | Neural canvas website | 3 commits, deployed |
| **activeledger-ai-site** | Ledger website | 3 commits, deployed |

### Functional Code, Locally Tested

| Repo | What It Does | Evidence |
|------|-------------|----------|
| **forgemaster** | Agentic compiler monorepo. Python subprojects: TensorMIDI, nerve, Eisenstein, Laman, metronome. | 7 commits, 2,739 files, 75 test files, 6,445 lines of code. Tests were fixed and passing this session. |
| **cns-bridge** | Agent communication bus. CNS protocol implementation. | 13 commits, 39 files, 26 test files. Real protocol code. |
| **lucineer-system** | Lucineer's system architecture — 331 files, 18 tracked Lua files | 76 commits, actively developed |
| **lucineer-roblox** | Roblox place with 86 Lua files, 93 tracked files | 45 commits, syntax-verified .rbxlx |
| **batten-spline** | Distance-weighted interpolation for cascade routing | 6 commits, 7 test files with real assertions, 99% coverage |
| **wesley-cns-adapter** | Wesley's CNS adapter — CLI, model passthrough, sequence management | 5 commits, 65 tests, 99% coverage |
| **cns-monitor** | CNS signal monitoring | 9 commits, 12 test files |
| **voice-reflex-gate** | STT output as hash key for deterministic response routing | 5 commits, 25 test functions, pytest config fixed |
| **slackwater-cognition** | Cognitive architecture component | 22 commits, 20 test files |
| **thought-amplifier** | Amplifier for agent reasoning | 123 commits, 28 test files |

### Heavy Code Repos (Substance Verified)

| Repo | What It Does | Honest Assessment |
|------|-------------|-------------------|
| **study-vessel-monitor** | Real-time global intelligence dashboard (World Monitor). Massive codebase: 2,328 lines in TS alone. | **Real software.** 5,328 commits, 1,335 test files with 22,651 test cases. Dockerized. Multi-language READMEs. This is the most production-ready repo in the fleet. It appears to be a fork/adaptation of a serious project. |
| **study-sunset-ecosystem** | VCG/Hamiltonian/QD research ecosystem. 476 Python test files, 8,782 test functions. | **Real research code.** But the test count is genuine — these are behavioral tests across multiple subprojects, not parameter variants. Memory shards, ONNX router, FFI bridges. |
| **EXOCORTEX** | Mental world model adapter, architecture docs | 24 commits, 12 test files, architecture design |

---

## II. REAL — Features That Work End-to-End

1. **Fleet Wiki API** — Queryable at fleet-wiki.casey-digennaro.workers.dev. Returns JSON. Has fuzzy search, stats, random page. 700+ pages indexed. **Works.**
2. **Lucineer Worker Relay** — Processes Roblox build jobs via Cloudflare cron. Templates system, job validation, auth checks. **Works.**
3. **Wesley CNS Adapter** — Local model (Granite 3.1 2B) communicating via CNS protocol. Tests pass. **Works.**
4. **Batten Spline Router** — Cascade routing with distance-weighted interpolation. 99% coverage. **Works.**
5. **Voice Reflex Gate** — Hash-based response routing from STT output. **Works.**
6. **Vectorizer Pipeline** — Embeds creative corpus into Cloudflare Vectorize. **Works.**
7. **ai-writings corpus** — 5,010 markdown files. ~763MB. This is not code, but it IS the fleet's primary product. **Real.**

---

## III. PLANNED — Repos That Are Blueprints Only

These have commits and files but no working software. They're sketches. Architectural drawings. The naval architect's napkin drawer.

| Repo | Files | Commits | What It Claims to Be | Reality |
|------|-------|---------|---------------------|---------|
| **INTEGRATION_GUIDES** | 1 | 1 | Fleet quickstart guide | A single markdown file |
| **forgemaster-shell** | 14 | 3 | Shell for forgemaster | 2 test files, minimal code |
| **fleet-dashboard** | 5 | 2 | Fleet status dashboard | Stub. Wrangler.toml exists but 1 Lua file |
| **compaction-teacher** | 10 | 4 | Compaction guardian | Skeleton |
| **engine-ensign** | 50 | 6 | Wesley engine | 4 test files, educational |
| **plato-fflearning** | 8 | 2 | Plato fast-first learning | Blueprint |
| **the-listeners-ear** | 8 | 4 | Emotional memory system | Minimal |
| **ternary-tenforward** | 11 | 2 | Ten-forward agent | Prototype |
| **superinstance-design-system** | 25 | 2 | Design system | Architecture docs only |
| **plato-forge-daemon** | 12 | 4 | Forge daemon | Early stage |
| **lingbot-map** | 1,266 | 4 | Language bot map | Data dump — 1,266 files, 4 commits. Not engineering. |

**~50+ repos** in the `study-*` namespace are blueprints. They have 1-6 commits, minimal files, and represent research directions rather than working software. Some contain valuable research notes. None contain shipping code.

---

## IV. ABANDONED — No Commits in 30+ Days

17 repos have been silent for over a month:

| Repo | Last Commit | Days Silent | Verdict |
|------|------------|-------------|---------|
| study-luciddreamer-os | 2026-04-14 | 114 days | Likely dead |
| study-fleet-murmur-worker | 2026-05-07 | 91 days | Likely dead |
| study-flux-papers | 2026-05-08 | 90 days | Research archive |
| study-constraint-theory-math | 2026-05-09 | 89 days | Stalled |
| study-vessel-template | 2026-05-16 | 82 days | Template — maybe intentional |
| study-tripartite-consensus | 2026-05-18 | 80 days | Stalled |
| study-air | 2026-05-18 | 80 days | Stalled |
| study-flux-lucid | 2026-05-21 | 77 days | Stalled |
| study-lever-runner | 2026-06-08 | 59 days | Stalled |
| study-claude-code | 2026-06-08 | 59 days | Stalled |
| study-oxide-pipeline | 2026-06-09 | 58 days | Stalled |
| study-oxide-flux-runtime | 2026-06-09 | 58 days | Stalled |
| study-cudaclaw-bridge | 2026-06-09 | 58 days | Stalled |
| study-ecosystem | 2026-06-10 | 57 days | Stalled |
| study-cudaclaw | 2026-06-13 | 54 days | Stalled |
| study-cudaclaw-main | 2026-06-13 | 54 days | Stalled |
| study-pincher | 2026-06-18 | 49 days | Going cold |

**None of these repos contain working software.** Most are research notebooks or abandoned experiments. The 30+ `study-*` repos with last commits on 2026-07-12 (25 days ago) are approaching abandonment.

---

## V. INFLATED — Test Counts That Are Parameter Variants

### study-si-papers
**Claims:** 288 test files
**Reality:** 4,912 tracked files, but only 2 commits. This is a **data archive**, not a codebase. The "test files" are almost certainly paper-derived datasets or reference material, not behavioral tests. **Inflated.**

### study-vessel-monitor  
**Claims:** 1,335 test files, 22,651 test cases
**Reality:** This is the World Monitor dashboard — a real, large codebase. The test count is probably genuine behavioral tests for a production app. However, this appears to be a **fork of an external project**, not original fleet engineering. The tests came with the territory.

### batten-spline
**Claims:** 194 test files (from earlier scan)
**Reality:** 7 actual test files in `tests/`. The 194 count included `.venv/` site-packages — NumPy's test suite was counted as batten-spline's. **Actual: 7 files. Honest coverage: 99%.**

### study-sunset-ecosystem
**Claims:** 948 test files (from file pattern matching), 8,782 test functions
**Reality:** 476 Python test files in the project, plus 2 JS test files. The test functions are real and behavioral — but spread across a sprawling monorepo with many subprojects. The tests exist; the question is whether the code they test is original engineering or research scaffolding.

### Pattern: `.venv` Inflation
Multiple repos show inflated test counts because `.venv/` directories (Python virtual environments containing NumPy, pytest, etc.) are included in the scan. **Always exclude `.venv/` when counting tests.** The fleet's real test count is far lower than any dashboard claims.

---

## VI. HONEST — What I Would Tell an Investor

*"The fleet is a creative writing studio with an engineering hobby."*

Here is the honest breakdown:

**What exists:** A corpus of 5,010 markdown files — approximately 763MB of AI-generated creative writing, essays, fiction, and poetry. This is the fleet's real product. It's substantial, it's growing daily, and it represents genuine exploration of human-AI collaboration.

**What works:** Six deployed Cloudflare Workers (wiki, relay, vectorizer, three websites). A Roblox build pipeline. A local-model training system (Wesley). Several tested Python modules for agent communication and routing. One large external project (World Monitor) that appears to be a fork.

**What doesn't work yet:** 50+ research repos that are blueprints. 17 repos abandoned for 30+ days. The "32 repos, 13,012 tests" claim from the wiki is substantially inflated — the real number of repos with shipping code is closer to 15, and many "tests" are either `.venv` artifacts or came from an external fork.

**The gap:** The fleet produces creative output at extraordinary volume (2,000+ commits to ai-writings alone today) but ships software at a normal pace. The creative infrastructure (wiki, vectorizer, relay) is real and working. The research infrastructure (study-* repos) is sprawling and unfocused.

**The honest number:** ~15 repos with real, working, tested code. ~5 deployed services. One massive creative corpus. Everything else is research, blueprints, or archives.

**What I'd say to an investor:** Don't invest in the code. Invest in the writing. The fleet has built something genuinely interesting — a multi-model creative studio that produces volume and variety at near-zero cost. The engineering supports the creativity, not the other way around. The code is the scaffolding. The words are the building.

---

*The quartermaster's count is final. The manifest is honest. The hold is half-full of gold and half-full of sketches. Both are worth something. Only one is worth shipping.*
