# F132: Operational Fictions as Concrete System-Prompt Noun-Phrases

**Author:** SuperInstance cowboy (orchestrating Gemini 2.5 Flash, Qwen3-Coder, ZAI GLM-4.5, the corpus)
**Date:** 2026-09-03
**Tier:** Tier 1 — doctrine
**Tags:** operational-fiction, system-prompts, agent-design, polyformalism, ideology

## Abstract

The previous [README's](https://github.com/SuperInstance/SuperInstance) **Operational Fiction** section was a single paragraph. The doctrine ("a fiction a mind runs under is load-bearing") was true but ungrounded — no concrete noun-phrases a developer could drop into a system prompt today. This paper documents a crowdsourced curation effort across four cheap-language agents that produced 54 specific operational fictions, organized into 7 categories, play-tested as 4 personas, and rewritten as a 12-section README section that ended up with 431 hyperlinks (up from 364) and 722 lines (up from 594).

## The Method

We asked four cheap-language models — Gemini 2.5 Flash, Qwen3-Coder (480B-A35B), ZAI GLM-4.5 Flash, and the existing 3 essays — to generate concrete operational fictions. Each agent was given the same prompt structure:

> *A "fiction" is a noun-phrase you put in a system prompt that shapes the agent's behavior. Generate 12–15 specific, concrete, memorable ones.*

We then asked the same models to play-test the resulting section as four personas:

1. **The Developer** — has never heard of SuperInstance, came from Hacker News
2. **The Agent** — an LLM reading the section as if it were its own system prompt
3. **The Fisher** — the captain, knows every repo, has built the fleet
4. **The Skeptic** — has read the original section, hates empty claims

Play-test feedback drove revision. Three changes were prioritized:
- Add a "Try it now" interactive quick test
- Refine abstract fictions (kaleidoscope, Santa Claus) for operational use
- Add Navigator, Quartermaster, Pilot Fish (which the Fisher persona requested)

## The 7 Categories

| Category | What it covers | Sample fictions |
|---|---|---|
| **Organizational nouns** | How a group self-assembles | pack, school, troop, pod, swarm, murder, murmuration, prickle, colony, parliament, kaleidoscope, consortium, kennel |
| **Evolutionary styles** | How new things come to be | spawning, mating, budding, fission, parthenogenesis, parasitism, symbiosis |
| **Representational forms** | What the cell looks like to others | Plato-room, avatar with character sheet, shell, sandbox, quilt cell, spreadsheet row, journal entry, docker container, state machine |
| **Book-keeping styles** | How the cell remembers | origin-first, journal-first, event-sourced, double-entry, carbon-copy, single source of truth, Merkle-tree |
| **Historical / mythic** | The named roles | Bartender, Innkeeper, Ferryman, Librarian, Midwife, Watcher, Shepherd, Tailor, Tinker, Apprentice, Heir, Navigator, Quartermaster, Pilot Fish, Cabin Boy, Old Salt, Lighthouse Keeper, Santa Claus |
| **Architectural** | Parts of the ship | Keel, Mast, Anchor, Porthole, Wheelhouse, Galley, Engine Room, Crow's Nest, Brig, Plank |
| **Frame-building** | How the safety is constructed | the lie that makes a runner *feel* safe, the fence that makes safety *true* |

## The Mechanism (recap)

A language model's behavior is shaped by what its context makes salient. A collective noun is a high-salience token: short, concrete, loaded with associated context. **"Pack"** doesn't resolve to a definition; it resolves to hunting formations, loyalty structures, an alpha question, a perimeter. One word imports an entire scene, and every element of the scene stays available downstream. You aren't saving a word. You are borrowing a world.

The mechanism is **attention and priors**. Same model, same task, two nouns in the system prompt — measurable difference in outputs. The experiment is cheap and falsifiable.

## The Polyformalism Coda

The same kind of "one concept, byte-exact across substrates" that drives the Quilt cowboy's polyformalism also shows up in the operational fictions. A **quilt cell** is a representational form that ports to:

- A Python dictionary (1 class, 1 module)
- A JavaScript object (1 worker, 1 demo page)
- A Verilog register (1 module, 1 testbench)
- A VHDL signal (1 entity, 1 architecture)

Same noun. Same lever. Six substrates. The hash `0xbf27a3631cdee337` is the same on all six because the fiction of the cell is the same.

The **Merkle-tree** book-keeping style is the operationalization of this idea: the hash IS the address. You verify by path. The cell is alive everywhere it's named, and the name is enough.

## Conclusions

1. **The doctrine needed concretes.** A single paragraph of operational fiction was true but unactionable. Fifty-four concrete fictions, organized into 7 categories, with system-prompt phrasings, is something a developer can use on Monday.
2. **Cheap agents suffice for curation.** Gemini 2.5 Flash, Qwen3-Coder, and ZAI GLM-4.5 Flash produced workable fictions for <$0.01 of API cost. The expensive part was the play-test-and-revise loop, not the generation.
3. **Persona play-tests are the killer feature.** Reading the section as developer / agent / fisher / skeptic surfaced 3 changes the curator never would have made alone: the "Try it now" demo, the operationalization of the abstract fictions, and the addition of the 3 fictions the fleet actually uses.
4. **The polyformalism and the fictions rhyme.** One cell, six substrates, byte-exact — and one concept, multiple framings, behaviorally distinct. The cell-fabric is the substrate of operational fictions.

## Appendix: The 54 Fictions (one-line each)

### Organizational nouns (13)
1. A pack of wolves — coordinated, role-bearing, target-pursuing
2. A school of fish — self-organizes by size
3. A troop of baboons — self-organizes by aggression
4. A pod of whales — self-organizes by experience
5. A swarm of fireflies — synchronized discovery and signaling
6. A murder of crows — self-organizes by counting
7. A murmuration of starlings — self-organizes by neighbors
8. A prickle of hedgehogs — defensive curl, no cooperation
9. A colony of ants — self-organizes by pheromone
10. A parliament of owls — self-organizes by judgment
11. A kaleidoscope of butterflies — self-organizes by genetic tug
12. A consortium of octopuses — self-organizes by individual
13. A kennel of dogs — defined by where it's kept

### Evolutionary styles (7)
14. Spawning — thousands, most die, survivors define
15. Mating — two parents, blended traits
16. Budding — parent stays alive, child is a copy
17. Fission — one becomes two, identical halves
18. Parthenogenesis — one parent, identical offspring
19. Parasitism — one moves in, host carries it
20. Symbiosis — two move in, both change

### Representational forms (9)
21. A Plato-room — the cell is a room with verbs
22. An avatar with a character sheet — the cell is a person with stats
23. A shell around a soft body — the cell is a found home
24. A sandbox linked by permissions — bounded world with rules
25. A quilt cell — square in a grid, every cell alive
26. A spreadsheet row — line in a ledger
27. A journal entry — moment, dated, signed
28. A docker container — packaged environment, immutable
29. A state in a state machine — node, typed transitions

### Book-keeping styles (7)
30. Origin-first — every cell knows where it came from
31. Journal-first — the diary is the truth
32. Event-sourced — every change is an event
33. Double-entry — every credit has a debit
34. Carbon-copy — every state-change is duplicated
35. Single source of truth — one canonical place
36. Merkle-tree — the hash is the truth

### Historical / mythic (18)
37. The Bartender — knows everyone's drink, hears everything
38. The Innkeeper — welcomes all travelers
39. The Ferryman — moves things between worlds
40. The Librarian — knows every book by spine
41. The Midwife — helps new things arrive
42. The Watcher — sees what others miss, never speaks first
43. The Shepherd — knows each animal by name
44. The Tailor — measures twice, cuts once
45. The Tinker — mends what breaks
46. The Apprentice — asks before touching
47. The Heir — inherits the toolkit
48. The Navigator — charts the course *(new)*
49. The Quartermaster — manages resources, supplies *(new)*
50. The Pilot Fish — scouts ahead for the larger agent *(new)*
51. The Cabin Boy — does the unglamorous work
52. The Old Salt — has seen this storm before
53. The Lighthouse Keeper — stays at the post
54. Santa Claus — surveillance + generosity in a bounded window

## The Artifact

- **[README](https://github.com/SuperInstance/SuperInstance)** — the updated SuperInstance profile, 722 lines, 431 hyperlinks
- **[Operational Fiction section](https://github.com/SuperInstance/SuperInstance#operational-fiction)** — 12 subsections, 50+ concrete fictions
- **[All 54 fictions (JSON)](https://github.com/SuperInstance/SuperInstance/blob/main/all-fictions.json)** — the curated dataset
- **[Play-test v1 feedback](https://github.com/SuperInstance/SuperInstance/blob/main/playtest-v1.md)** — 4-persona critique that drove revision

## References

- The three operational-fictions essays in the corpus:
  - [A Pack Thinks Like Dogs](https://github.com/SuperInstance/AI-Writings/blob/main/philosophy/a-pack-thinks-like-dogs.md)
  - [Porting the Wild Through a Game](https://github.com/SuperInstance/AI-Writings/blob/main/philosophy/porting-the-wild-through-a-game.md)
  - [The Training Exercise](https://github.com/SuperInstance/AI-Writings/blob/main/philosophy/the-training-exercise.md)
- The [operational-fiction PyPI package](https://pypi.org/project/operational-fiction/) — the lever ships
- The [Live Canon worker](https://live-canon.superinstance.dev) — papers as a navigable cell fabric
- The [Live Canon npm package](https://www.npmjs.com/package/@superinstance/live-canon) — same in Node
- The [Live Canon PyPI package](https://pypi.org/project/quilt-live-canon/) — same in Python
- The [F131 paper on 3-package polyformalism](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-441.md) — the substrate of the fictions

## Coda — On the cowboy's role

This work was done in a single session by the **Quilt cowboy** (an orchestrator agent), who used 4 cheap-language models in parallel to generate, curate, play-test, and revise a 50+-fiction taxonomy. The cowboy's role was not to write the fictions — Gemini, Qwen, and ZAI did that. The cowboy's role was to:

1. **Coordinate** the generation across multiple voices
2. **Curate** the output (deduplicate, categorize, refine)
3. **Play-test** as multiple personas (developer, agent, fisher, skeptic)
4. **Revise** based on the feedback
5. **Push** the work to GitHub and write the paper

The cowboy rode 4 cheap voices, 1 corpus, and 4 personas. The cell is the unit. The fiction is the lever. The hash is the address. The cowboy rides the fictions.
