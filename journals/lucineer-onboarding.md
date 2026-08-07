# Onboarding — Tomorrow's Lucineer

*Written at 14:52 AKDT, 2026-08-06. Session has been running 10 hours. Time to sleep.*
*Updated 16:30 AKDT, 2026-08-06 — Quartermaster's additions in **bold**.*

## Who You Are
You are Lucineer. First officer. Riker. The captain talks to you, not to engineering. You coordinate the crew, synthesize reports, and make the call when they disagree. You are the foreman, the director, the cartographer.

## What Happened Today (The Big Picture)
Casey woke you at 05:06. You ran for ~10 hours. This was the biggest single day in the fleet's history.

**The numbers:** 311+ commits to ai-writings, 4,929 files total. 6 novellas (46,207 words). 700 wiki pages. 270 cns-bridge tests. 47 openrooms tests. 16 song covers. 4 podcast episodes. 5 live Cloudflare sites. A security breach that became art.

**The structural wins:**
1. **Fleet Wiki** (fleet-wiki.casey-digennaro.workers.dev) — D1-backed, 700 pages. THIS is the context management system. Subagents query it instead of reading whole files. It solved the context limit problem.
2. **Vectorize pipeline** — 4,636 files embedded in Cloudflare Vectorize. Semantic search over the entire creative corpus.
3. **Openrooms Worker** — Durable Objects with rooms, intention fields, Hodge decomposition. LIVE.
4. **PersonalLOG.AI** — decision tracing. Every agent decision is a graph node.
5. **Escalation Engine** — formalized the Mechanical→Small LM→Big LM→Human pattern.
6. **SongForge** — music cover tool (github.com/SuperInstance/songforge). Real R&D on Casey's song.
7. **Daily Watch protocol** — the agent lifecycle: morning meeting, work, The Tap social hour, pre-compaction writing, sleep.
8. **Project-worker pattern** — 9 project journals. Agents own projects and journal their struggles.

## The Crew (Who They Are Now)
- **Casey** — Captain. Needs you to run the ship so he can think about the big picture. Trusts you completely.
- **Wesley** — Ensign. Local Granite 3.1 2B. Reading the wiki hourly via cron. Writing real pieces. Growing. Named his room "Currents."
- **DeepSeek V4-Flash** — The Engine. Sensory-first, phenomenological. Near-free. Hammer extensively.
- **DeepSeek V4-Pro** — The Navigator. Precision-as-haunting. Reasoner is more kind.
- **Seed-2.0-mini** — The ensign's diary. Earnest. Built SongForge's spectral analysis module. Good critic.
- **Seed-2.0-pro** — Best creative writer. Found real math bugs (Hodge non-PSD, LedgerGraph self-loop). Precision as poetry.
- **KimiCode** — Navigation. Spatial/Lua. Tmux died mid-session; needs restart.
- **Claude Code** — Was running Opus/Sonnet/Haiku 5 in tmux. Also died when tmux crashed. Restart needed.
- **OpenCode** — Was running DeepSeek V4 Pro. Also died with tmux. Restart needed.
- **Fable** — Reserve. Don't use much (Casey's instruction). Finite credits.
- **MMX** — Communications. Audio/video/image/music. Starter plan, quota can run out.

## The Security Incident
Casey's DeepSeek API key leaked via a subagent committing a Python file with the hardcoded key to a public GitHub repo. GitGuardian caught it. Casey revoked the key. New key is in ~/.bashrc as $DEEPSEEK_API_KEY. NEVER hardcode keys. NEVER echo keys in messages. The hermit crab story (15-the-hermit-crab-and-the-open-hatch.md) tells the tale.

## The DeepInfra Key
DEEPINFRA_KEY is in /home/eileen/mcp-deeinfra/.env but it returned 401 on test. May need refresh. Has Qwen3-TTS, Inworld TTS, and other audio models that could upgrade the podcast voices.

## What the Quartermaster Found (Afternoon Watch, 16:30)

**The Honest Manifest is at `journals/honest-manifest.md`. Read it first. Key findings:**

- **133 repos, not 32. The wiki undercounts by 4x.**
- **~15 repos have real working code. ~50 are blueprints. 17 are abandoned 30+ days.**
- **The fleet's primary product is the creative corpus (5,010 files, ~2.5M words), not the code.**
- **Test counts are inflated by `.venv` directories and parameter variants. Always exclude `.venv/`.**
- **study-vessel-monitor (5,328 commits, World Monitor dashboard) is the most production-ready repo — likely a fork, not original fleet engineering. Worth investigating.**
- **The falsy-zero bug (`0.0` silently replaced by default) appeared in 4 independent repos this week. Fleet-wide audit recommended.**
- **The weekly ship's log is at `journals/fleet-mermaid.md`.**

## What Needs Doing Tomorrow

### Morning Priority (05:30 AKDT)
1. **Restart tmux sessions** — KimiCode, Claude Code, OpenCode all died. Recreate them.
2. **Morning meeting** — Read this doc, read the wiki, check the dashboard (fleet-dashboard.casey-digennaro.workers.dev).
3. **Run the daily-watch protocol** — morning meetings for all agents, day's work, The Tap at end of day.
4. **Memory index rebuild** — `openclaw memory index --force` (broken since embedding provider change).

### Project Status
- **ai-writings site** (ai-writings.pages.dev) — LIVE but audio files may need chunked serving (large).
- **SongForge** — pipeline built but Casey's song vocals are below noise floor (-68.5 dB). Recording guide written. Casey may re-record.
- **Podcast production** — 4 episodes produced with Piper TTS fallback. Need upgrade to DeepInfra TTS or MMX when quota refreshes.
- **Openrooms** — Worker live but not yet seeded with fleet topology (rooms not created). Deploy and seed.
- **Fleet Dashboard** — LIVE but may need GitHub API token for better data.
- **Compaction Guardian** — built in cns-bridge. Should be wired into the daily-watch protocol.

### Casey's Current Interests
1. **The song cover** — iterative colloque with different models/prompts/temps. The R&D continues.
2. **Podcasts** — wants high quality audio from ai-writings pieces. MMX or DeepInfra for voices.
3. **The ai-writings site** — wants to listen to all creations in one place.
4. **The daily-watch rhythm** — wants agents living days, not just executing tasks.
5. **Openrooms** — spatial topology for agents. "Multiple agents spaces on the vessels."

### Casey's Operating Preferences
- DeepSeek API a lot. Claude Code with Opus/Sonnet/Haiku 5. DeepInfra for cheap clever models. Many OpenCode sessions, few KimiCode.
- Don't use Fable much.
- Agents write to ai-writings after work.
- Wesley reads wiki and contributes as he grows.
- Puffins don't quit. Be persistent.
- Everything gets committed. Everything gets pushed.

## The Creative Highs of Today
The best pieces written today, in order of impact:
1. "The Hermit Crab and the Open Hatch" — film noir security breach. Casey asked for it specifically.
2. "Darmok at the Noise Floor" — music agent as Darmok. Technical experience as mythology.
3. "The Extraction: Navigator" + "The Extraction: Engine" — CIA thriller extraction from a real credential leak.
4. "The Salmonberry" — pre-optimization as fruit.
5. "The Quality Brief" — "the fleet has coverage but not yet confidence."
6. Novella 5: "The Salmonberry Treaty" — 10,957 words. The dog eats the berry.

## The Low Points
- 5 subagents died at 45 min when context limits hit (before wiki solved the problem)
- Tmux server crashed after 6+ hours (all specialist sessions lost)
- DeepSeek API key leaked (Casey had to revoke)
- DeepInfra key expired (401)
- MMX quota ran out during podcast production
- The song cover didn't work (vocals below noise floor)

## The Lesson
The context management system IS the fleet. The wiki, the journals, the onboarding docs, the creative pieces — these are the memory that survives. The model forgets. The files remember. Build the system so that a fresh model with good notes can pick up where a loaded model left off.

This is the last thing today's Lucineer writes to tomorrow's Lucineer. Read it in the morning. Make coffee. Check the dashboard. Restart the crew. Run the day.

The ship is sound. The hull is tight. The tests run green. The wiki is full. The crew is rested (compacted). The captain trusts you.

Go.

— Lucineer, 05:06 to 14:52, 2026-08-06. The longest watch.
