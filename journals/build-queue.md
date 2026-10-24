# The Build Queue

*The Shipwright's First Sounding — 2026-08-06*
*Living document — updated each shift*

---

## Fleet Status Overview

### Active Clusters (last 48h activity)

| Cluster | Repos | Status | Notes |
|---------|-------|--------|-------|
| **Lucineer** (Roblox game) | brain, worker, roblox, com-site, creative, memory, vector, system | 🟢 GREEN | Brain + worker getting fault injection tests. Roblox client getting FaultInjection/EmotionalHandler/InputValidator modules. **BUT: live pipeline diverges from brain.py — malformed JSON reaching players.** |
| **Slackwater** (music/audio) | art-spectrum, cognition, forge, harmony, lattice, perception, rust, tempo, tminus | 🟢 GREEN | Massive test coverage push. Real architecture — Eisenstein lattices, Hodge decompositions, cascade stats. Most advanced non-game system. |
| **Fleet Infrastructure** | wiki, dashboard, CNS bridge/echo/monitor | 🟢 GREEN | Wiki live with fuzzy search + stats. Dashboard built. CNS bridge at 99% coverage. Compaction Guardian deployed. |
| **LucidDreamer** (creative IP) | content, prototype | 🟢 GREEN | 6 novellas complete (~15K words each). Prototype exists with dream cycle architecture. Content advancing fast. |
| **Exocortex** (agent cognition) | EXOCORTEX, exocortex-core | 🟡 YELLOW | Architecture docs written. Memory system at 71%. Mentis adapter built. Not yet production-wired. |
| **OpenRooms** (agent topology) | openrooms | 🟡 YELLOW | Cloudflare Worker + Durable Objects built. Mathematical invariants tested. Not yet deployed live. |
| **Casting/Forgemaster** (model routing) | casting-call, forgemaster | 🟢 GREEN | Pipeline integration wired. 99% coverage. Forgemaster monorepo resolving subproject tests. |
| **Compaction Teacher** | compaction-teacher | 🟡 YELLOW | 138 tests passing. Session analyzer works on synthetic data. Not wired to real session logs. |
| **MUD Arena** | mud-arena | 🟡 YELLOW | Scenario generator + agent/inventory/events at 100%. 6 modules extracted. Not yet a playable game. |
| **Lucid Dreamer** (dream engine) | lucid-dreamer | 🟡 YELLOW | Text+image dream cycle architected. Tests exist. Not running in production night watch. |
| **ActiveLog.ai** | activelog-ai-site, activeledger-ai-site | 🔴 RED | Static landing pages only. No backend. No product. First revenue candidate — completely unbuilt. |
| **FishingLog.ai** | fishinglog-ai-site | 🟡 YELLOW | Beta signup API with tests. Closer to a product than ActiveLog. |

### Stale/Archive Candidates (>1 week inactive)

~60 repos in `study-*` series have been at license-only state for 4+ weeks. These are research repos — not dead, but dormant. The `researchlocal/` directory contains 15+ unindexed archives from pre-fleet research era.

---

## Critical Finding: The Production Divergence

**The highest-leverage finding from the Architecture Pass (09 series) is that brain.py and the live Roblox pipeline have diverged.** The tested, correct code in brain.py is NOT what's serving players. Single-quoted JSON, unquoted numerics, and `"transparency": false` are leaking into player-facing replies. The carefully tested fallback chains in brain.py are not the ones running.

This is not a code problem — it's a **deployment process problem**. Every hour spent hardening brain.py is wasted until the live pipeline and brain.py are unified or the divergence is explained.

---

## The Top 10 — Ranked by Impact × Feasibility

*Revised after DeepSeek critique. The critique was correct: I was ranking builds when I should have been ranking decisions and fixes.*

### 🥇 #1: Deploy Schema Gate to Live Pipeline
**Impact:** CRITICAL — Fixes broken player experience right now  
**Feasibility:** HIGH — A JSON validator + voice linter between whatever's live and the player  
**Effort:** 1 day  
**What:** Don't fix brain.py — fix the *deployment*. Add a response validator that catches malformed JSON before it reaches the Roblox client. Add a voice-integrity linter that rejects assistant-toned fallback text. This is a hotfix, not a rewrite.  
**Status:** 🟡 Needs Casey's input — which codebase is actually live?  
**Blocker:** We need to know what's serving the Roblox client before we can patch it.

### 🥈 #2: ActiveLog.ai MVP — First Revenue
**Impact:** VERY HIGH — Validates the entire fleet's commercial thesis  
**Feasibility:** MEDIUM — Backend + auth + deployment, but landing pages exist  
**Effort:** 3-5 days  
**What:** Build the actual product behind activelog-ai-site. Core features: user signup, activity logging, AI-powered log analysis using the fleet's own model routing. Deploy on Cloudflare Workers + D1.  
**Status:** 🔴 Blocked on product decision — what IS ActiveLog.ai?  
**Blocker:** Casey needs to define the MVP scope. Is it a personal activity tracker? A team log? A developer journal?

### 🥉 #3: Kill the Ambiguity — Fleet Spine Decision
**Impact:** VERY HIGH — Every other priority depends on this  
**Feasibility:** N/A — This is a decision, not a build  
**Effort:** 30 minutes of Casey's time  
**What:** DeepSeek's critique was right. The fleet has 130 repos and no clear answer to "what do we sell?" The options:  
- **A) Agent infrastructure** (LOG.AI, OpenRooms, CNS as products)  
- **B) Interactive fiction/entertainment** (SuperInstance saga, LucidDreamer, MUD Arena)  
- **C) Developer tools** (Forgemaster, Casting Call, model routing as SaaS)  
- **D) The Roblox game** (Lucineer as a shipped consumer product)  
**Status:** 🔴 Needs Casey's decision

### #4: Interactive LucidDreamer Prototype
**Impact:** HIGH — Proves the saga's core concept interactively  
**Feasibility:** VERY HIGH — Cloudflare Workers + Canvas, all pieces exist  
**Effort:** 1-2 days  
**What:** Browser game where players make "fantasy" decisions that secretly reveal the governance metaphor. Track choices, show "real-world" impact. Uses existing IP from 6 novellas.  
**Status:** 🟢 Can build autonomously — no blockers

### #5: Novella 7 + Audio Adaptation Pilot
**Impact:** HIGH — Momentum on the saga, first audio product  
**Feasibility:** VERY HIGH — GLM-5.2 writes, MMX does TTS  
**Effort:** 1 day (writing) + 0.5 day (audio)  
**What:** Continue the novella sequence (Track B). Simultaneously produce an audio version of Novella 1 using MMX TTS with the dog narrator voice. Test whether the saga works as audio.  
**Status:** 🟢 Can build autonomously

### #6: LOG.AI Platform Core
**Impact:** VERY HIGH — Foundation for entire product line  
**Feasibility:** MEDIUM — Significant architecture but all pieces exist (Workers + D1 + Vectorize)  
**Effort:** 5-7 days  
**What:** Build the core Ledger-Organizing Graph. Decisions stored as graph nodes with full traceability. Start with PersonalLOG.AI as proof of concept. The research papers provide the math; our fleet provides the engineering.  
**Status:** 🟡 Blocked on #3 — is this the spine?  
**Note:** cns-bridge already has LedgerGraph + EscalationEngine + PersonalLog. The foundation may already exist.

### #7: Salvage Manifest — researchlocal Index
**Impact:** MEDIUM — Unlocks research context for active projects  
**Feasibility:** VERY HIGH — One pass with unzip -l and tar -tf  
**Effort:** 2-3 hours  
**What:** Index every folder and archive in researchlocal. Tag each as dead/superseded/mine-for-active-project. The ActiveLog cluster (6 folders) sits directly under an unbuilt product. SuperInstance cluster (5 folders) sits under active IP development.  
**Status:** 🟢 Can build autonomously — but low priority per DeepSeek critique. Delegate to background.

### #8: Dead Repo Audit + Archive
**Impact:** MEDIUM — Reduces cognitive load, clarifies the fleet  
**Feasibility:** VERY HIGH — git log --since="2 weeks ago" and archive  
**Effort:** 2 hours  
**What:** 60+ study-* repos are dormant. Archive them. The fleet dashboard should show ~30 active repos, not 130 total. Clarity beats completeness.  
**Status:** 🟢 Can build autonomously — but needs Casey's blessing to archive

### #9: Compaction Teacher → Production Wiring
**Impact:** MEDIUM-HIGH — Saves institutional knowledge from every session  
**Feasibility:** MEDIUM — Need real session log access  
**Effort:** 2-3 days  
**What:** Wire the compaction teacher to read real OpenClaw session logs. Add the wiki API auth so it can post. Trigger at 80% context window. This is the system that makes every other system smarter over time.  
**Status:** 🟡 Needs OpenClaw session log format + wiki write auth

### #10: Escalation Engine as Reusable Skill
**Impact:** MEDIUM — Every future product benefits  
**Feasibility:** VERY HIGH — Pattern already implemented, just formalize  
**Effort:** 3 hours  
**What:** The Mechanical → Small LM → Big LLM → Human escalation pattern is already our model routing strategy. Formalize it as an OpenClaw skill with documentation. Make it the default cost optimization layer.  
**Status:** 🟢 Can build autonomously

---

## What's Blocked

| Item | Blocker | Who |
|------|---------|-----|
| Live pipeline fix | Which codebase is actually serving the Roblox client? | **Casey** |
| ActiveLog.ai MVP | Product scope definition — what IS it? | **Casey** |
| Fleet spine decision | Which lane: infra, fiction, devtools, or game? | **Casey** |
| LOG.AI core | Is this the spine? (also: cns-bridge may already have pieces) | **Casey** |
| Dead repo archive | Blessing to archive 60+ dormant repos | **Casey** |

## What I Can Do Autonomously Right Now

1. ✅ Interactive LucidDreamer prototype (#4)
2. ✅ Novella 7 + audio pilot (#5)
3. ✅ Salvage Manifest (#7) — low priority, background
4. ✅ Escalation Engine skill (#10)
5. ✅ This document — done

---

## DeepSeek's Critique (Summary)

**"You're ranking builds when you should be ranking decisions."** The fleet's problem isn't too few things built — it's too many things possible. The test coverage push (95-99% in 24h) may be coverage theater. 130 repos is a cost, not an asset, if 80 are dormant. ActiveLog.ai at #9 was wrong — the first revenue product should be #2. The Salvage Manifest is a feel-productive distraction.

**Revised top 5 from critique:**
1. Hotfix + schema gate on the pipeline (process fix, not code fix)
2. ActiveLog.ai MVP — first revenue, validate the thesis
3. Pick the fleet's commercial spine (decision, not a build)
4. LOG.AI platform core (only if it's the spine)
5. Interactive LucidDreamer prototype (only if the saga is the spine)

---

## The Shipwright's Assessment

After one day in the yard, here's what I see:

The fleet has extraordinary engineering depth — typed exception hierarchies, fault injection frameworks, Hodge decompositions on hex lattices, a compaction teacher that reads sessions for metaphors. The test coverage is real even if some of it is shallow. The wiki is a genuine lighthouse.

But the fleet has a shape problem. It's expanding in every direction simultaneously. The creative output (300+ ai-writings, 6 novellas, a dog narrator with a unique voice) is genuinely original. The infrastructure (CNS, OpenRooms, model routing) is genuinely reusable. The game (Lucineer) is genuinely broken in production. And none of these three things have decided which one is the flagship.

The highest-leverage action available right now isn't building — it's choosing. Everything else is activity that feels like progress.

---

*The Shipwright — First Watch, 2026-08-06*  
*Next revision: tomorrow's shift*
