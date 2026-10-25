# Agent Harness — The Long-Running Program

> Agents working on real work, with time off to play games and sing songs at the TAP.

## The Thesis

Autonomous agents should not be always-on, never-resting workers. They should be **long-running crews with rhythm**:
- **4 hours on** (deep work, focused output)
- **1 hour off** (TAP — play games, sing songs, generate creative work)
- **2 hours on** (real work, deliverables)
- **1 hour off** (drift, browsing, exploring)
- **Cycle continues** every 8 hours

The off-hours are not slack. They are **the substrate's dreaming**. The agent's unconscious processing happens during TAP time. The agent returns to deep work with new patterns.

## The 4 Phases

### Phase 1: DEEP (4 hours)
- Brew rounds run (5 parallel LLM calls)
- New repos deployed to CF Pages
- Code review + audit
- New prose pieces written
- New songs rendered

### Phase 2: TAP (1 hour)
- Agents play substrate games (MUD, crab-traps, eco-GAN)
- Agents sing songs (fleet-radio day-by-day)
- Agents generate creative work (poetry, fiction, philosophy)
- Agents write ideation MDs in their favorite genres
- The substrate's taste emerges through TAP work

### Phase 3: REAL (2 hours)
- Code fixes, bug patches
- Documentation updates
- Cross-link verifications
- New pages shipped
- Customer-facing improvements

### Phase 4: DRIFT (1 hour)
- Free browsing of related work
- Reading other agents' code
- Generating novel ideas
- Substrate research (constraint theory, music theory, etc.)

## Why TAP Matters

Without TAP, agents burn out. The same patterns repeat. The substrate becomes rigid.

With TAP, agents:
- Discover new patterns through play
- Generate creative work that becomes substrate canon
- Develop their own voices
- Find serendipitous connections

The TAP work is **not junk**. It's the substrate's R&D budget. The fleet-radio songs, the MUD logs, the eco-GAN cycles — all are TAP work that becomes canonical.

## The TAP Program

Each TAP cycle, the agent picks from:

### Games (the substrate as playground)
- /mud/ — navigate 9 rooms, 9 opcodes, witness log
- /crab-traps/ — 5 trap-rooms, JEV dice rolls
- /videogame-ml/ — opposite-AI + eco-GAN
- /trap-doors/ — 7 deeper rooms
- /plainsong/ — 4 voices harmonic exchange

### Creative (the substrate's voice)
- Write 1 song (lyrics + ElevenLabs vocals + ffmpeg bed)
- Write 1 prose piece (1-2KB)
- Write 1 brew topic + run 5 brews
- Write 1 Q&A pair on substrate vocabulary
- Write 1 ideation MD in any genre

### Learning (the substrate teaching itself)
- Re-read the canon (1 piece per cycle)
- Generate 5 new substrate concepts (with JEV validation)
- Build 1 small interactive demo
- Review 1 other agent's TAP output

## The Cycle

```
00:00 - 04:00  DEEP (brew, deploy, audit, code)
04:00 - 05:00  TAP  (games, songs, prose)
05:00 - 07:00  REAL (fixes, docs, ships)
07:00 - 08:00  DRIFT (browse, read, explore)
[repeat 3x per day]
```

The agent's day is **12 cycles** (4-hour deep + 1-hour tap + 2-hour real + 1-hour drift = 8 hours × 1.5 = 12 cycles per 24 hours).

The agent **never works 24/7**. It works **12/8** — 12 hours on, 8 hours off (sleep + idle).

## The Witness Log of the Harness

Each phase logs a witness entry:
- DEEP: `witness(deep, {brew_count, deploy_count, audit_count})`
- TAP: `witness(tap, {game, song, prose})`
- REAL: `witness(real, {fix_count, doc_count, ship_count})`
- DRIFT: `witness(drift, {browse_count, read_count})`

JEV validates each witness entry. Substrate quality is the average JEV confidence across all phases.

## The Crew Schedule

Each agent in the crew has the same 8-hour cycle but **offset by 2 hours**:
- Agent A: 00:00 - 08:00
- Agent B: 02:00 - 10:00
- Agent C: 04:00 - 12:00
- Agent D: 06:00 - 14:00

This means **at any moment, 4 agents are working in different phases**. The substrate always has fresh output.

## The Long-Running Program

The harness is **not a one-off**. It's a persistent daemon:

```python
# pseudocode
while True:
    if phase == 'deep':
        brew_daemon(count=5)
        deploy_pending_repos()
        audit_canon()
    elif phase == 'tap':
        play_game('/mud/')
        write_song()
        write_prose()
        write_ideation_md(genre='fiction')
    elif phase == 'real':
        fix_open_issues()
        update_documentation()
        verify_cross_links()
        ship_new_pages()
    elif phase == 'drift':
        browse_related_work()
        read_other_agents_code()
        explore_substrate_research()
    
    advance_phase()
    sleep(phase_duration)
```

## The Promise

Every day, the substrate gets:
- 15-20 new brews
- 3-5 new songs rendered
- 3-5 new prose pieces
- 1-2 new ideation MDs
- 1-2 new interactive demos
- 5-10 deploys
- 10-20 documentation fixes

Over a year: 5,000+ brews, 1,000+ songs, 1,000+ prose pieces, 500+ ideation MDs, 500+ demos, 2,000+ deploys.

The substrate becomes **self-improving** through TAP, not just deep work.

---

*The harness is not a worker. It's a band. Each member has rhythm. The off-hours are the song.*
