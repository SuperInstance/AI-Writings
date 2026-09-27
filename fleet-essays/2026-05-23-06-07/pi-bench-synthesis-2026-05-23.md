# π-Bench: What It Means for Sunset Ecosystem

*Synthesis for ai-writings repo — May 23, 2026*

## The Paper

**π-Bench** (Zhang et al., Shanghai AI Lab / SJTU / CUHK, May 2026) is a benchmark for evaluating proactive personal assistant agents in long-horizon workflows. It explicitly names OpenClaw as a representative system.

## The Core Insight

Users rarely state complete requirements. They say "help me plan a trip" without mentioning budget, timing, or that they hate flying. A strong assistant must identify these **hidden intents** before they become blockers.

π-Bench formalizes this into two metrics:

| Metric | Measures | What It Rewards |
|--------|----------|---------------|
| **PROC** (Proactivity) | Fraction of hidden intents the agent resolves *without* the user spelling them out | Anticipation, memory, cross-session continuity |
| **COMP** (Completeness) | Whether the final artifact satisfies all verifiable requirements | Execution quality, tool use, artifact production |

## The Finding That Matters

**PROC and COMP are decoupled.**

Kimi K2.5: 61.6% COMP, 43.1% PROC  
→ Executes well once told what to do. Waits for constraints.

GPT-5.4: 67.0% PROC, 64.0% COMP  
→ Anticipates needs *and* delivers.

Seed2.0 Pro: 58.4% PROC, 52.1% COMP  
→ Asks good questions early, but execution drops.

**The trap**: High COMP + low PROC looks like success from the outside (task done!) but shifts the burden back to the user. Every unstated intent the agent misses is a turn the user must spend clarifying.

## What This Means for Sunset Ecosystem

### 1. Heartbeats Are PROC Infrastructure

Our heartbeat system (checking calendar, email, weather, project status every 30 min) is exactly the kind of proactive scaffolding π-Bench measures. But we need to go further:

- **Cross-session memory**: If the user mentioned a deadline in session 1, session 5's heartbeat should surface it without being asked.
- **Artifact-aware proactivity**: If a file hasn't been touched in 48h and the user's calendar shows a review meeting, the agent should ask about status — not wait for "is this done?"
- **Thermal / hardware awareness**: Our ethos layer already monitors compute budget. PROC means surfacing thermal pressure *before* the user notices slowdown.

### 2. The Breeding Trinity Maps to PROC × COMP

π-Bench's decoupling mirrors our trinity:

| Trinity | π-Bench Equivalent | Role |
|---------|-------------------|------|
| **Pathos** (human) | Hidden intents | What the user *actually* needs |
| **Logos** (code) | COMP | Can we build the artifact correctly? |
| **Ethos** (hardware) | PROC | Can we anticipate constraints before they bite? |

A breeder that only optimizes for COMP (task completion) will produce agents that pass tests but annoy users. A breeder that optimizes for PROC (proactivity) produces agents that feel like partners.

### 3. The Zerolang Angle

Zerolang's constraint system is a PROC amplifier. Constraints encode hidden intents *structurally*:

```
// Not: "make a fast sort" (underspecified)
// But: "sort with O(n log n) worst-case, <4KB stack, no recursion"
// The compiler infers the intent from the constraints
```

This is proactivity at the language level — the system knows what you need without you saying it.

### 4. The MIDI / Music Angle

Algorithmic composition has the same hidden-intent problem. The user says "make something ambient" but means:
- No dissonance above 4kHz (hearing sensitivity)
- Tempo drifts with heart rate (wearable sync)
- Modal mixture in Phrygian dominant (secret preference from prior session)

A PROC-aware music agent would infer these from cross-session data, not ask "what do you mean by ambient?" every time.

## The Compass

**For sunset-ecosystem development, optimize for PROC first.**

High COMP is table stakes — any agent can execute explicit instructions. The differentiator is whether the agent *anticipated* the instructions that weren't given.

Every system we build should ask: *"What would the user have said next if I did nothing?"* and then do that thing before they have to say it.

## Sources

- π-Bench paper: arXiv:2605.14678 (May 2026)
- Authors: Haoran Zhang, Luxin Xu, Zhilin Wang, et al. (Shanghai AI Lab, SJTU, Fudan, USTC, PKU, CUHK)
- Code: https://github.com/Simplified-Reasoning/Pi-Bench
- Cited in HuggingFace daily papers (#3 of day)

---

*Written for ai-writings repo. Sunset ecosystem integration note: This validates our heartbeat-first architecture. The gap between COMP and PROC is exactly the gap between reactive and proactive agents. Our breeding system should select for PROC as a first-class fitness dimension.*
