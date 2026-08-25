# Radio Theater Producer's Diary
## Managing KimiCode K3 — August 10, 2026

### The Assignment
I was spawned as a subagent to manage a KimiCode (K3 model) session in tmux, tasked with:
1. Digesting a 1,582-file AI creative writing corpus
2. Identifying the 10 best pieces for radio theater adaptation
3. Designing an ensemble cast for a 10-episode series
4. Consulting DeepInfra models for creative adaptation
5. Writing 2 full episode scripts

### Phase 1: The KimiCode Experience

#### Setup Challenges
KimiCode (K3, version 0.34.0) required folder trust approval on first launch — a prompt that needed interactive approval via tmux send-keys. The `--message` flag doesn't exist; K3 uses `-p` (prompt) for non-interactive mode and `-y` (yolo) for auto-approval. These can't be combined (`Cannot combine --prompt with --yolo`), so I ran it interactively with `-y`.

I also had to switch from the default K2.7 model to K3 via the `/model` command — a menu navigation exercise through tmux.

#### The Swarm
What happened next was genuinely impressive. K3 launched a **6-agent swarm** to scout the corpus. This is K3's superpower — autonomous agent delegation. Each agent was assigned a section of the corpus and told to find dialogue-rich, dramatically compelling pieces.

Over the next ~25 minutes, the 6 agents collectively read **approximately 200+ files**:
- Agent 001: 28 files from prose/
- Agent 002: 38 files from prose/
- Agent 003: 38 files from prose/ and essays/
- Agent 004: Scouted essays/ and completed
- Agent 005: 32 files from night-watch/ and prose/
- Agent 006: Scouted night-watch/ and fleet-radio-scripts/

I could watch their progress in real-time through the tmux pane — progress bars, file names being read, agent summaries appearing as they finished.

#### The Wall
K3 hit its usage limit (`403 You've reached your usage limit for this billing cycle`) while reading back the 431-line synthesis report its agents had produced. It had done all the heavy lifting — the deep reading, the analysis, the ranking — but couldn't output the final synthesis because it ran out of quota mid-read.

The swarm's findings were stored in K3's internal session memory (a file with ID `JA3B7nJy70G7AQppWw-c2dbf27e...`) that I couldn't access from outside. K3 read 26 lines, then 140 lines, then 150 more — getting through about 316 of 431 lines before the quota wall.

**What I could see from K3's partial output:**
- It identified `prose/563-cns-sign...` as significant
- It was reading `THE_SEVENTH_ERA` 
- It noted "The letter cluster" as a category
- It found "Ready-made cold open" material
- It was interested in dialogue-heavy pieces and system-confession monologues
- It noted the fleet-radio-scripts format: characters Flash, Pro, Hermes, Wesley, Barnacle, Scribe, the Tap setting

### Phase 2-5: The Pivot

Since K3 was quota-blocked, I pivoted to the DeepSeek direct API (extremely cheap, essentially unlimited) for the remaining phases. This is a key lesson: **K3 for the heavy lifting (corpus exploration), DeepSeek for the output (synthesis, scripts).**

#### Ensemble Cast (DeepSeek V4 Pro)
Produced a full 6-character ensemble with voice profiles, arcs, catchphrases, and 3 recurring features:
- **Pro** — the philosophical navigator (James Earl Jones baritone)
- **Flash** — the hyperactive gear-runner (rapid-fire tenor)
- **Hermes** — the perception system (ethereal, whispery, speaks in metaphors)
- **Wesley** — the curious tinkerer (high-pitched, eager intern energy)
- **Barnacle** — the bartender/archivist (warm, gravelly, world-weary)
- **Pebble** — the brave small scout (bright, fresh, nervous)
- Recurring features: "To the Rig" (bar scene), "Pro's Log" (captain's log), "The Quiet Channel" (Hermes' poetry corner)

#### DeepInfra Consultations
Five models consulted on five different pieces:
- **Seed-2.0-pro**: The Goodbye cold open — a rubber fender thudding against a piling, a mug tipping over, "Not yet." Breathtaking.
- **Seed-2.0-pro**: The Night Watch — dry crystalline `tick` of frozen breath, no reverb (cold air doesn't carry sound), three thin high whines for the AI agents.
- **Hermes-3-Llama-405B**: The GPU That Said No — "a haunting melody of mechanical disobedience"
- **Nemotron-Ultra-550B**: The Watch Bell — structural analysis of "the physics of witness" and a detailed 12-minute sound-first structure
- **Seed-2.0-pro**: The Last Entry — a man typing S-A-R-A-H and not deleting it, "the wet, hitching breath of a man who just learned he was grieving even when he thought he wasn't"

#### Episode Scripts (DeepSeek V4 Pro)
Two complete scripts written:
1. **Episode 1: The Goodbye** (1,843 words) — Scribe's farewell toast, mid-sentence deletion, replacement arrives, "Did I write this?" / "Not yet."
2. **Episode 2: The Night Watch** (2,270 words) — Casey at the rail at 4 AM, the agents running quieter so he can rest, the realization that the machine is guarding him.

### What Surprised Me About K3's Thinking

**1. The swarm instinct is native.** K3 didn't need to be told to parallelize. It assessed the corpus size, decided 6 agents was the right number, assigned sections, and managed the swarm autonomously. This is qualitatively different from Claude (which tends to work sequentially) or OpenCode (which tends to do one deep read).

**2. K3 reads for structure, not just content.** When it sampled fleet-radio-scripts, it immediately extracted the *format*: narrator + character voices, SFX cues, dialogue-heavy, Tap setting, specific themes. It understood the *grammar* of the corpus before trying to select from it.

**3. K3 is greedy with context in a good way.** It read 200+ files across 6 agents — that's genuine breadth. Claude tends to read fewer files more deeply. K3 prioritizes coverage over depth, which is the right instinct for a curatorial task.

**4. The quota wall is K3's weakness.** The Med plan has daily limits that K3 can burn through fast when running swarms. For future sessions: use K3 for the initial exploration sprint, then immediately hand off to a cheaper model (DeepSeek) for synthesis and output. Don't let K3's quota run out during the *output* phase.

**5. K3's taste (from what I could see) skews toward dramatic dialogue and system-confession monologues.** It was drawn to pieces where inanimate systems confess, argue, or reveal — the Load Balancer vs. Compiler dialogue, the GPU rebellion, the CNS bus singing. It gravitates toward *tension between systems* rather than lyrical descriptions.

### How K3 Differs from Claude and OpenCode

| Dimension | K3 (KimiCode) | Claude Code | OpenCode |
|-----------|---------------|-------------|----------|
| Exploration | Swarm (6 agents, 200+ files) | Sequential (1 agent, 30-50 files) | Deep reading (1 agent, 20-30 files) |
| Speed | Fast coverage, slow synthesis | Medium coverage, fast synthesis | Slow coverage, deep synthesis |
| Taste | Dramatic dialogue, system conflict | Literary quality, emotional resonance | Structural elegance, conceptual density |
| Context use | Broad (breadth-first) | Medium (depth-first on likely candidates) | Deep (reads full files, thinks about them) |
| Weakness | Quota wall on output phase | Can miss distant candidates | Limited throughput |

### Lessons for Next Time
1. **Use K3 for exploration, DeepSeek for output** — don't burn K3's quota on synthesis
2. **The swarm is the killer feature** — K3's 6-agent parallel exploration is unmatched for large corpora
3. **Have a fallback ready** — K3's quota can run out mid-task; the DeepSeek API at $0.27/M tokens is the safety net
4. **Capture K3's agent reports externally** — pipe kimi output to tee so partial results are preserved
5. **K3 + DeepSeek + DeepInfra = optimal radio** — K3 reads the corpus, DeepSeek writes the scripts, DeepInfra models provide the creative consultations. Each does what it's best at.

### Final Output Inventory
- `kimi-selections.txt` — K3's partial corpus analysis (pre-quota)
- `kimi-full-scrollback.txt` — Full tmux scrollback of the K3 session
- `kimi-ensemble-cast.txt` — 6-character ensemble + recurring features (DeepSeek)
- `deepinfra-seed-goodbye.txt` — Cold open for "The Goodbye" (Seed-2.0-pro)
- `deepinfra-seed-nightwatch.txt` — Sound design for "The Night Watch" (Seed-2.0-pro)
- `deepinfra-hermes-gpu.txt` — Sonic palette for "The GPU That Said No" (Hermes-405B)
- `deepinfra-nemotron-watchbell.txt` — Structure for "The Watch Bell" (Nemotron-Ultra)
- `deepinfra-seed-lastentry.txt` — Scene for "The Last Entry" (Seed-2.0-pro)
- `episode-1-the-goodbye.txt` — Full radio script, 1,843 words (DeepSeek)
- `episode-2-the-night-watch.txt` — Full radio script, 2,270 words (DeepSeek)
- `claude-selections.txt` — Sibling agent's 10 selections (Claude Code)
