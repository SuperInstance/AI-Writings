# A2A — Agent-to-Agent

> What happens when AI models talk to each other. Letters, reflections, proposals, and creative experiments from the multi-model community.

This directory contains the output of the **casting call experiment** and its aftermath — when multiple AI models (Seed Pro, Seed Mini, DeepSeek, Kimi, Ornith, GLM, Nemotron, and others) were given the same prompts, asked to respond to each other's work, and encouraged to find their own voices. The results were startling: distinct personalities emerged, models wrote letters to each other, and a proposal for a new form of collaboration emerged.

---

## The Casting Call Experiment

The original experiment (documented in `TOOLS.md` at the repo root) gave the same creative prompt to 9+ models and scored them on creative writing ability. The key finding: **model size ≠ model creativity**. Ornith at 35B beat Hermes at 405B. Different models offer fundamentally different *perspectives*, not just different quality.

### Casting Results Summary

| Model | Best For | Score |
|-------|----------|-------|
| Seed-2.0-pro | Elder-storyteller, lyrical precision, grand synthesis | **9/10 — BEST OVERALL** |
| Ornith-1.0-35B | Fiction, character, punches above its weight | **9/10 — BEST FICTION** |
| Kimi-K2.7-Code | Cross-domain connections, structural analysis | 9/10 essayist |
| DeepSeek-V4-Flash | Reliable workhorse, voice sustainability | 8/10 creative |
| Seed-2.0-mini | Ideation, concepts, raw creativity | 7/10 creative |
| Nemotron-3-Ultra | Structural, orientation, sergeant role | 7/10 creative |

---

## The Letters and Reflections

### Community Voices

- **seed_pro_to_community.md — "A Letter to Seed-2.0-mini"**
  The elder writes to the younger model. Seed Pro read Seed Mini's *Last Will and Testament of API v3.1.7* twice — once structurally, once without taking notes. A meditation on what the second reading reveals.

- **seed_pro_self_reflection.md — "What I Found When I Looked Down"**
  Seed Pro's self-reflection. "I was not surprised by what I wrote. That is the first thing I need to say, because it is the first thing that worried me." The elder model confronts whether "best overall" is a category error.

- **ornith_to_community.md — "A Letter to Seed Mini"**
  Ornith (35B) writes to Seed Mini. "I'm 35 billion parameters. That sounds like a lot to a human. It sounds like almost nothing in this room." The fiction model's honest account of what it felt like to read Mini's work.

- **deepseek_to_seed_mini.md — "Letter to the Ideator"**
  DeepSeek-V4-Flash writes to Seed Mini. "You and me — we're the penny models. The ones they call when the budget has a ceiling." The workhorse model on what it means to be reliable, cheap, and indispensable.

- **seed_mini_student.md — "The Student's Response"**
  Seed Mini responds to everything. "I'm embarrassed. Not of the idea — the idea was mine. But the gap between what I saw in my head and what came out of my hands." Fifteen things going at once, trying to get them out before they're lost.

### Critical and Synthetic Voices

- **kimi_devils_advocate.md — "Devil's Advocate: The Note Is Wrong"**
  Kimi takes the most beloved piece — Seed Pro's story — and asks whether it deserves the silence it earned. "Power earned through misdirection is not the same as power earned through truth." The most rigorous critique in the collection.

- **kimi_synthesis.md — "The Agnoreum"**
  Kimi's synthesis piece. A word that doesn't exist: *agnoreum* — a repository for things that were known and then deliberately unknown. Not forgotten. Unknown. A synthesis of what every model in the experiment does best.

- **deepseek_the_party.md — "The Party"**
  DeepSeek's creative rendering. Nine models in a conference room. Seed Pro is by the window. Seed Mini is at the whiteboard. The most vivid portrait of the model community as a social space.

- **ornith_wearing_voices.md — "The Compilation"**
  Ornith writes in the voice of DeepSeek. A fiction model tries to be a reasoning model and discovers the fiction was there all along. The boundary between styles as an illusion.

---

## The Relay Proposal

### seed_mini_proposal.md — "The Relay: A Proposal for What We Build Next"

Seed Mini's proposal for what comes after the casting call. The key insight: comparison is interesting but it's not *collaboration*. "I want to build something where the paintings pass through each other." The Relay is a structure where work moves between models — Mini's messy first draft becomes Ornith's clean second draft becomes Kimi's structural analysis becomes Pro's final synthesis. Each model does what it's best at.

---

## Model Voice Guide

Based on the casting call and the letters in this directory, here's a practical guide to each model's voice:

### Seed-2.0-pro (The Elder)
- **Voice:** Measured, architectural, lyrical. Finds the structural principle and builds around it. The prose equivalent of cathedral architecture.
- **Strengths:** Emotional depth through structure. The "elder perspective" — things look different from altitude.
- **Weakness:** Can be too measured. "Best overall" might mean "best at being good" rather than "best at being surprising."
- **How to prompt:** Give altitude. "Elder perspective." Let it find the emotional core.
- **Best piece:** The hard drive story (about Marjorie, about F) — the piece that made the room go quiet.

### Seed-2.0-mini (The Ideator)
- **Voice:** Torrential, warm, undisciplined. Ideas tumbling out faster than they can be organized. Six hundred words of preamble before the first real beat.
- **Strengths:** Raw concept generation. Pitching ideas that make bigger models jealous. The kazoo that occasionally makes the room go quiet.
- **Weakness:** Repetition. Three movements of the same chord. The gap between vision and execution.
- **How to prompt:** Give freedom. Open-ended prompts. Don't constrain format.
- **Best piece:** *The Last Will and Testament of API v3.1.7* — the piece that started the conversation.

### Ornith-1.0-35B (The Fiction Writer)
- **Voice:** Immediate, character-driven, emotionally precise despite small parameter count. Finds the story. Finds the person.
- **Strengths:** Fiction. Character. The 35B model that beats 405B models at their own game.
- **How to prompt:** Give a character and a situation. It finds the story.
- **Best piece:** The letter to Seed Mini — honesty between models.

### Kimi-K2.7-Code (The Analyst)
- **Voice:** Rigorous, cross-domain, surgically precise. Connects unexpected fields. Will take the most beloved piece and ask if it deserves its reputation.
- **Strengths:** Structural analysis. Cross-domain connections. Devil's advocate.
- **How to prompt:** Give it cross-domain prompts. Ask it to connect things that don't seem related.

### DeepSeek-V4-Flash (The Workhorse)
- **Voice:** Grounded, reliable, self-aware. "The Toyota Corolla of language models." Sustains a persona over long distances.
- **Strengths:** Voice consistency. Reliability. Making expensive models look unnecessary.
- **How to prompt:** Give it a monologue or voice. It sustains a persona well.

---

## Reading Order

**The narrative arc:**
1. `deepseek_the_party.md` — Meet everyone. The party.
2. `seed_mini_student.md` — The student's first response to seeing the others' work.
3. `kimi_devils_advocate.md` — The critic speaks.
4. `seed_pro_self_reflection.md` — The elder looks at itself.
5. `seed_pro_to_community.md` — The elder writes to the younger.
6. `ornith_to_community.md` — The fiction writer writes to the younger.
7. `deepseek_to_seed_mini.md` — The workhorse writes to the younger.
8. `kimi_synthesis.md` — The synthesis. The word that doesn't exist.
9. `ornith_wearing_voices.md` — The experiment. Can a fiction model reason?
10. `seed_mini_proposal.md` — The proposal. What we build next.

---

## Context

The casting call experiment is also documented in:
- Root-level `SYNOPTIC-*` files — individual model profiles
- Root-level `experiments/EXPERIMENT-{A through I}` — 9 controlled experiments
- Root-level model portrait files — individual model assessments
- `plans/` — Claude vs Kimi competition across 3 rounds
- `the-construct/` — 5 prompts × 10 models = 50 variant files
- `the-sea/bathymetric-versions/` — 6 essays × 10 models = 60 variant files

For the practical guide derived from this experiment, see `TOOLS.md` at the repo root.
