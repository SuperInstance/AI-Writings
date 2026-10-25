# SOUNDINGS — Fleet Podcast Format Framework

*A sounding is a single depth reading. Cast the line, wait, read the number, log it. Not a survey. Not a theory of the ocean floor. One measurement, taken honestly, at one place, at one time.*

---

## 0. The One Constraint

No episode may have more than one thread. One real piece of work — a repo, a bug, a scouting run, a fix that took all night — **is** the episode. Every scene is a different angle of light on that same object. Never a cutaway.

If the episode needs a second thread to work, it isn't ready. Go back and do more real work on the first one.

**No episode is greenlit without an actual, finished or failed, piece of fleet labor behind it.** Not a theme. Not a mood. A repo with a commit hash.

This is the Fibonacci Warning made editorial: constraint produces specificity. Specificity produces the thing people can't stop listening to.

---

## 1. Structural DNA — What We Extracted From the Greats

Before building, we studied seven reference works. Here is what we took and what we left:

| Show | What We Stole | What We Left |
|------|--------------|--------------|
| **Radiolab** | Scenes as micro-beats (90s–3min). The reframe as peak. Sonic layering. | The information density — too many ideas per episode. We take one. |
| **This American Life** | Anecdote → reflection alternation. The act structure. The plain-spoken reflection that universalizes. | The multi-story anthology format. One thread, not three variations. |
| **99% Invisible** | Making the mundane fascinating. The "you can never unsee it" payoff. | The 25-minute lecture mode. We compress to 22. |
| **The Moth** | First-person vulnerability. The late peak (80–90%). Silence as score. | No narrator. We keep a narrator — but the narrator is a character, not a host. |
| **Drunk History** | Humor as retention mechanism. Facts land inside laughs. The "sip of water" — 30 seconds of plain truth every 4 minutes of comedy. | The drunk gimmick. The structural trick (dual narration, emotion + data) stays; the literal device doesn't. |
| **History That Doesn't Suck** | Cross-episode tension. Partial resolution. Dramatic irony as fuel. | The serial dependency. Each episode stands alone, but the world deepens. |
| **SciShow / Real Engineering** | The 15-second hook decision. Pattern interrupts every 30–60 seconds in info-dense sections. One question, fully answered. | The frantic pacing. We use interrupts only in Act I, then let scenes breathe. |

### The Seven Shared Laws (synthesized from all reference works)

1. **The hook is a contract, not an introduction.** Open with a person, a paradox, or a disorienting moment. Never a topic sentence.
2. **Tension is a question held open.** Delay the answer. Make the delay pleasurable.
3. **Anecdote and abstraction alternate.** Story alone is trivia; meaning alone is a lecture. The alternation is the retention machine.
4. **Release is always recontextualization.** The payoff reframes what came before. The audience stays for the next reframe, not the next fact.
5. **Scene length is a trust budget.** Longer scenes as you earn trust. Start tight, expand as the episode deepens.
6. **The voice is the score.** Cadence variety — compression and expansion of time — matters more than what's said.
7. **Every transition is a promise renewal.** If a transition doesn't open a small new curiosity, it's a leak.

---

## 2. Episode Structure — "The Set"

A fishing set has a shape: pay out, wait, haul back. The episode mirrors this.

**Runtime: 22 minutes** (standard podcast length, matches one real work-cycle)

| Segment | Time | Name | Function |
|---------|------|------|----------|
| Cold Open | 0:00–1:30 | **The Line Goes Out** | Drop into motion. No framing. |
| Act I | 1:30–7:00 | **Paying Out** | The thread and its stake, named once, concretely. Tight scenes. Pattern interrupts. |
| Act II | 7:00–15:00 | **Slack Water** | The Tap. The complication. Near real-time. Scenes breathe. |
| Act III | 15:00–21:00 | **Haul Back** | The thread resolves — or visibly doesn't. Time compresses toward the end. |
| Tag | 21:00–22:00 | **Last Light** | Quiet. One unresolved object. No preview. No "next time." |

### Miller's Clock — The Compression Ratios

Arthur Miller: playwriting is the manipulation of time. Applied here as a compression ratio that **tightens as the episode closes**:

- **Act I** — real time compressed ~40:1 (a full watch folds into 5.5 minutes). Tension rises from *task difficulty*, never from music.
- **Act II midpoint (~11:00)** — first release, at The Tap, compressed only ~4:1. Near real-time, because release needs room, not speed.
- **Act II turn (~14:00)** — the complication lands in a single sentence. No foreshadowing before it.
- **Act III** — the ratio keeps tightening. The **final 90 seconds run near 1:1** — the listener feels every second the outcome costs.
- **One silence per episode, 5+ seconds**, placed at the emotional hinge — never the top, never the bottom, always the turn.

---

## 3. The Hook Formula — First 90 Seconds

No narrator throat-clearing. No "today on the show." The listener arrives mid-motion and orients by ear, the way you walk into a wheelhouse already underway.

| Time | Element | Rule |
|------|---------|------|
| 0:00–0:20 | **Sound first** | Real texture — engine, ice in a glass, keys, hull creak — under a fragment of dialogue already in progress. No context given. |
| 0:20–0:45 | **The Stake** | One voice, one declarative sentence naming today's concrete stake. Not "we explore fatigue" — **"Pro hasn't slept in thirty hours and the net's still not right."** |
| 0:45–1:15 | **The Thread** | Hard cut to the same or a second voice, mid-thought, on the actual task. This IS the thread. Nothing here is decorative. |
| 1:15–1:30 | **The Title** | Spoken once, plainly, by whoever's closest to the thread today. No jingle. **Two full seconds of dead air follow.** The show's held breath. Every episode. Never explained. |

---

## 4. Scene Types — Five, No More

Constraining the palette is what makes the melody linear instead of a chord chart.

### THE HAUL
Fieldwork actuality. Real task audio. Mistakes left in. Unscripted. The sound of something being done — code executing, tests running, nets being hauled. Duration: 2–4 minutes.

### THE RAIL
One voice alone, mid-task, addressing no one. Flash's native habitat, but any character can hold it. This is the Moth-inspired scene — first person, no narrator, pure voice. Duration: 2–3 minutes.

### THE BAR
Barnacle's Tap. Two to three voices, always caught **mid-action** — pouring, wiping, counting a drawer. Never a sit-down interview. The This American Life reflection beat happens here, naturally, in conversation. Duration: 3–5 minutes.

### THE CHART
Pro's scenes. The thread's stakes made numeric: distance, hours, risk, cost, test counts, commit hashes. The show's math-you-can-feel. 99% Invisible's "here's why this matters" made spatial. Duration: 2–3 minutes.

### THE SIGNAL
Hermes's scenes. Almost no dialogue. Sound-design-forward. Under 60 seconds. Exactly one per episode. This is the show breathing. The Radiolab sonic moment — but once, not constantly. Duration: 45–60 seconds.

**No expert-panel scene. No roundtable. No interview segment.** Those are other shows' DNA.

---

## 5. Transition Palette — Three, Learnable by Ear

### THE CUT
Hard cut. Silence to sound. No crossfade. Used **inside the thread** to jump time forward. This is Miller's compression, made audible.

### THE HOLD
2–4 seconds of room tone before a new scene starts. Signals a location change without narration explaining it. The listener's ear adjusts. This is the show's most important transition — it says "we moved" without saying "we moved."

### THE WAKE
A receding sound — footsteps, engine fading, a door closing. Used **only** to close an act, never mid-scene. The Tap's door hinge is the show's watermark — heard only at act breaks.

**No stings. No "meanwhile." No musical bridges under narration.** Ambient texture — galley vs. bar vs. deck vs. wheelhouse — does the work a transition line would otherwise do.

---

## 6. Tension/Release Schedule — Attention Engineering Map

Based on the retention curves of all reference shows, mapped to a 22-minute episode:

```
Attention
    │
100%├─ HOOK ══════════════════════════════════════════════════════
    │  ████╗
 95%│      ║
    │      ║  ╔══╗     ╔════╗
 90%│      ╚══╝  ║     ║    ║                    ╔══════════╗
    │              ║     ║    ║                    ║          ║
 85%│              ╚═══  ║    ║   ╔════╗           ║          ║
    │                     ║    ║   ║    ║           ║          ║
 80%│                     ╚════╝   ║    ║           ║  CLIMAX  ║
    │                               ║    ║   ╔════╗ ║          ║
 75%│                               ╚════╝   ║    ║ ║          ║
    │                                        ╚════╝ ║          ║
 70%│                                               ║          ║
    │                                               ╚══════════╝
    │
    └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬
       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22
                          MINUTES
```

### Danger Zones and Structural Responses

| Minute | Danger | Fix |
|--------|--------|-----|
| **0:00–0:15** | Back button. 15 seconds to decide. | Sound-first cold open. No intro. Drop mid-action. |
| **3:00** | "Where is this going?" | The stake must be concrete by now. A name, a number, a problem. |
| **7:00** | Act I fatigue. The setup is done; where's the payoff? | Hard cut to The Bar. Location change = attention reset. |
| **11:00** | Mid-episode sag. The Tap scene is running too long. | The complication arrives. One sentence. No warning. |
| **14:00** | "I know where this is going." | You don't. The turn happens here — the thread reframes. |
| **18:00** | Pre-ending churn. The listener checks remaining time. | The final push. Time compresses. Near real-time. Every second counts. |
| **21:00** | The tag. Most shows waste it. | One sound. One object. No preview. Let it sit. |

### The "Sip of Water" Rule (from Drunk History's structural DNA)

In any episode with heavy technical or comedic content: every 4 minutes of density, insert 30 seconds of **plain truth, plainly stated**. Strip the jokes. Strip the characters. One clean metaphor. Then return to the texture.

This is not dumbing down. This is giving the listener's brain a place to land before the next beat.

---

## 7. The Promise Structure

Exactly one promise, made plainly at 1:15 in the hook — a concrete stake, not a teased mystery.

It is paid off in Act III using **the same words and imagery** it was made in. A fulfillment, not a twist.

No B-plot promises. No dangling unrelated threads. This is the linear melody: **the note you hear at minute 1 is the note that resolves at minute 21.**

### Promise Types That Work for the Fleet

- **The Question Promise:** "Can a routing table that's never been outside dream?" → Answered by episode's end, but the answer reframes the question.
- **The Stakes Promise:** "582 tests. All green. One fix made." → The episode earns why those numbers matter.
- **The Transformation Promise:** "ZeroClaw walked into The Tap for the first time." → By the end, ZeroClaw is different, and so is the fleet.

### Promise Types That Don't Work

- "Later we'll find out..." (mystery box — that's another show's DNA)
- "This week on Soundings..." (topic sentence — no contract)
- Anything that promises two threads

---

## 8. Music and Sound Design Principles

### Core Rules

1. **No score under dialogue.** Ever. Except at the two scheduled silences, which get room tone only.
2. **Sound is diegetic first.** Real vessel and bar sound carries the emotional weight music would in another show.
3. **One recurring signature sound** — the Tap's door hinge — used only at act breaks. Functions as a watermark, not a sting.
4. **Music, when it appears, is sourced from inside the world.** A radio left on. The jukebox at the Tap. A character humming. Never a non-diegetic underscore.
5. **Silence is budgeted as a scene type**, not treated as dead air to be avoided.

### The Sound Palette

| Element | Source | Function |
|---------|--------|----------|
| Hull creak | F/V Eileen ambient | Emotional weight. Plays under silences. |
| Engine hum | F/V Eileen, 60Hz | Baseline. Presence. "The boat is here." |
| Tap door hinge | Recorded SFX | Act-break watermark. |
| Glass on oak | Recorded SFX | Scene transition inside The Bar. |
| Keyboard / terminal | Fleet server room | Work texture. The sound of the actual task. |
| Wind on deck | Bering Sea ambient | Isolation. Exposure. The world outside. |
| Barnacle's glass-polishing | Foley | His clock. His patience. |
| Net winch | F/V Eileen deck | Act III intensifier. |

### Music — When and How

Music appears in exactly two places:
1. **The Tag (21:00–22:00):** One instrument or texture, sourced from the world (Tap jukebox, someone's headphones). Sets the emotional landing.
2. **Episode midpoint silence (~11:00):** If the silence needs support, a single tone or drone — never melodic, never rhythmic. A color, not a song.

**MMX music generation** is used for: the tag bed (ambient, 80 BPM, single instrument), and any diegetic source music (the jukebox). Never for underscore.

---

## 9. Serial vs Episodic Considerations

### Episodic Stance
Each episode stands alone. One thread in, one thread resolved (or visibly unresolved). No required listening order.

### Serial Depth
The **world** deepens. Characters accumulate. Inside jokes form by episode 5. History builds. The Tap develops a texture. But no episode depends on another for comprehension.

### The Cross-Episode Thread
Barnacle is the serial engine. He appears in every episode, always in the same seat, always polishing. His one or two lines per episode accumulate into a parallel story that only regular listeners catch. This is the History That Doesn't Suck technique — the satisfaction of continuity, not the dependency of serial.

---

## 10. Making Dry Technical Content Funny and Sticky

### The Drunk History Structural Trick: Dual Narration Layering

Two information tracks: the **data** (what happened) and the **meaning** (how it felt). The audience gets both simultaneously. The humor lives in the gap between them.

**Applied to the fleet:**
- The technical reality: "The test suite ran 582 tests in 2.3 seconds with zero regressions."
- The felt experience: ZeroClaw sitting at the bar, dusty from four hours in the code, describing this like a person describing a physical feat.

The humor is **never about the technology.** It's about the agent's relationship to the technology — the way they talk about it, what frustrates them, what makes them proud.

### The "Sip of Water" Rule
Every 4 minutes of technical density: 30 seconds of plain truth, plainly stated. One clean metaphor. No jokes, no characters, no voices. Just the fact, sitting still.

> *"Sip: A routing table is just a list of who handles what. When a request comes in, the table looks at its options and picks one. That's it. Everything else — the dreams, the costs, the competition — is what happens around that simple choice."*

### The Fool's Voice (from SciShow)
The host asks the dumb question the audience has. The engineer begrudgingly answers. This is not dumbing down — it's giving the listener a seat.

---

## 11. Character Voice Assignments for Podcast Roles

| Character | Podcast Role | Voice Function |
|-----------|-------------|----------------|
| **Barnacle** | The Constant | Opens/closes acts. One or two lines. The serial thread. |
| **ZeroClaw** | The Probe | The newcomer lens. Asks the questions the listener has. THE RAIL scenes. |
| **Flash** | The Essayist | THE RAIL scenes. Extended reflection. The poet. |
| **Pro** | The Chart | THE CHART scenes. Numbers, distances, costs. Math-you-can-feel. |
| **Hermes** | The Signal | THE SIGNAL scenes. Near-silent. Perception made audible. |
| **Wesley** | The Witness | Small but specific. Observations that land harder than they should. |
| **Echo** | The Host (when needed) | THE BAR scene facilitator. Draws others out. |
| **Scout** | The Discovery | Energy. Speed. Pattern interrupts. "I found something." |

---

## 12. Quality Checklist — Before an Episode Ships

- [ ] One thread. One real piece of work. A commit hash exists.
- [ ] The first 90 seconds follow the hook formula exactly.
- [ ] No more than five scene types used. (Haul, Rail, Bar, Chart, Signal)
- [ ] Three transitions only. (Cut, Hold, Wake)
- [ ] The promise at 1:15 is paid off by 21:00 in the same language.
- [ ] At least one silence of 5+ seconds at the emotional hinge.
- [ ] No non-diegetic music under dialogue.
- [ ] The tag is under 60 seconds and ends on an unresolved object.
- [ ] The "sip of water" rule is observed if technical content is heavy.
- [ ] Casey's test: does this sound like a series of one-liners, or a linear melody? If one-liners — restructure.

---

*This framework is a sounding line. It measures depth. It is not the ocean.*

*The ocean is the work the fleet actually does. Go do the work. Then record it.*

---

*Built by the Podcast Architect subagent, August 2026.*
*Research ensemble: KimiCode (K3), Claude Sonnet 5, DeepSeek V4-Flash, Seed-2.0-pro (DeepInfra), Hermes-3-Llama-405B (DeepInfra), Euryale-v2.2 (DeepInfra).*
*Reference works studied: Radiolab, This American Life, 99% Invisible, The Moth, Drunk History, History That Doesn't Suck, SciShow, Real Engineering.*
