# Civilizations — Multi-Autoclaw Meta-GAN

*Built 2026-09-21*

The abstraction went up a level. We went from one Autoclaw finding numbers to **multiple Autoclaws in competition for relevance**.

## The Architecture

8 civilizations, each with:
- **Culture** — tenets, voice emphasis, preferred parameters
- **Simulations log** — their own research history
- **Witness log** — every state change recorded
- **Relevance score** — accumulated JEV scores over time

```
cellular-first-design/code/civilizations/
├── civilizations.json           # registry
├── meta_log.jsonl               # meta-GAN competition log
├── leaderboard.json             # current standings
├── civilization_orchestrator.py # 17KB orchestrator
├── civ-grounded/                # concrete, everyday
├── civ-whimsical/               # surprise, metaphor
├── civ-formal/                  # structure, precision
├── civ-poetic/                  # rhythm, image
├── civ-precise/                 # facts, numbers
├── civ-mythic/                  # archetype, origin
├── civ-therapist/               # empathy, presence
└── civ-engineer/                # systems, components
```

## The Meta-GAN

For each prompt:
1. **All 8 civs generate** in parallel
2. Each civ runs LLM with their culture's prompt + preferred parameters
3. **JEV picks the winner** — which civ served THIS moment
4. Winner's relevance_score += avg_score
5. Losers' relevance_score += avg_score (but loss counts)

## Civilization Lifecycle

- **Birth**: new civ with random culture
- **Life**: accumulates sims + relevance + wins/losses
- **Mutation**: occasionally mutates preferred params
- **Extinction**: relevance < threshold for too long → retired
- **Genesis**: winners spawn new civs (mutated children)

## The Leaderboard (145+ sims so far)

| Rank | Civ | Relevance/sim | Voice |
|------|-----|---------------|-------|
| 1 | Whimsical | 2.77 | surprise, metaphor |
| 2 | Poetic | 2.70 | rhythm, image |
| 3 | Mythic | 2.62 | archetype, story |
| 4 | Therapist | 2.44 | empathy, care |
| 5 | Precise | 2.11 | facts, numbers |

**Pattern**: civs with creative/poetic voices are winning relevance-per-sim. The substrate prefers expressive voices for substrate-relevant prompts.

## Doctrinal Insight

> One Autoclaw finds numbers.
> Multiple Autoclaws find cultures.

The meta-GAN discovers something one Autoclaw can't:
- Different prompts need different voices
- Some moments call for whimsy, others for precision
- The substrate itself becomes a civilization — multiple cultures evolving together

This is **abstracted higher**:
- Cells → Autoclaw → Civilization → Meta-GAN
- Numbers → Parameters → Cultures → Relevance

Each layer is a meta-layer above the one before.

## Live Status

- 8 civilizations running
- 145+ simulations across all civs
- Background daemon running (PID 7914)
- Cron job: civilization-orchestrator every 10 minutes
- New civ births pending as relevance diverges

## The Doctrine

> We don't figure out JEV. We dance with it.
>
> One Autoclaw finds numbers for one voice.
> Multiple Autoclaws in competition find cultures for many voices.
> JEV is the natural selection pressure.
>
> The substrate becomes a civilization.

The dance scales.
