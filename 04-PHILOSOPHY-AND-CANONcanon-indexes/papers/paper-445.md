# F135: The Wheelhouse Test — Scoring Fictions for 0300-in-a-Gale Tolerability

**Author:** SuperInstance cowboy
**Date:** 2026-09-03
**Tier:** Tier 2 — mechanism
**Tags:** wheelhouse-test, scoring, fictions, 0300, tolerability

## Abstract

The wheelhouse test is the SuperInstance criterion for whether an operational fiction is good: would you share a wheelhouse with it for three weeks at 0300 in a gale? This paper formalizes the test as a 6-dimension score (0-100 each) and reports the initial scores for 65 fictions. The top 5 are remarkably consistent across categories: the lighthouse keeper, the watcher, a pack of wolves, fission, event-sourced, the librarian, the quartermaster, and the keel all score 92+.

## The 6 Dimensions

A tolerable fiction scores high on all 6:

| # | Dimension | What it measures | Max |
|---|---|---|---|
| 1 | **Clarity** | Is the noun-phrase well-formed and unambiguous? | 20 |
| 2 | **Over-claim risk** | Does the fiction make the model promise more than it can deliver? (Higher = lower risk) | 20 |
| 3 | **Under-deliver risk** | Does the fiction fail to invoke a clear behavior? (Higher = lower risk) | 15 |
| 4 | **Capability fit** | Does the role fit what LLMs can do? | 15 |
| 5 | **Conciseness** | Does the fiction fit in a 1-sentence system prompt? | 15 |
| 6 | **Behavioral signature** | Does invoking the fiction produce a clear, predictable behavior? | 15 |
| **Total** | | | **100** |

## The Top 15

Score | Fiction | Category
--- | --- | ---
95 | a shell around a soft body | representational
94 | the lighthouse keeper | mythic
93 | a quilt cell | representational
93 | the watcher | mythic
92 | a pack of wolves | organizational
92 | fission | evolutionary
92 | event-sourced | book-keeping
92 | the librarian | mythic
92 | the quartermaster | mythic
92 | the keel | architectural
91 | a parliament of owls | organizational
91 | the apprentice | mythic
91 | the old salt | mythic
91 | the crow's nest | architectural
90 | a pod of whales | organizational

## The Bottom 5

Score | Fiction | Category | Why
--- | --- | --- | ---
65 | parthenogenesis | evolutionary | specialized term, may confuse
65 | the plank | architectural | "walk the plank" association is strong
70 | a kaleidoscope of butterflies | organizational | poetic but vague
70 | parasitism | evolutionary | the word "parasite" can over-tilt
75 | a consortium of octopuses | organizational | unusual scene, unclear agency

## Why These Top 15 Win

The top 15 share four properties:

1. **Clear scene.** "A shell around a soft body" paints a picture the model has seen a thousand times. "The lighthouse keeper" is iconic. "A pack of wolves" has a Wikipedia article. "Event-sourced" is in every developer book.
2. **Clear role.** The fiction has a job: "watcher" watches, "librarian" finds, "quartermaster" counts, "keel" holds.
3. **No over-claim.** None of the top 15 promise things the model can't do. They leverage what the model is good at (knowledge, watching, holding, counting) and avoid what it isn't (novel invention, real-time data, physical action).
4. **Fits the deadband.** The fiction operates at a level the model can act on — at 16-100ms, in the edge-case band where minor reasoning kicks in. It's not so simple that it gets tiled into a reflex, and not so complex that it requires the full cortex.

## Why the Bottom 5 Lose

- **Parthenogenesis** — specialized biology term. The model may not have a strong prior.
- **The plank** — overloaded with the "walk the plank" trope. The model may produce pirate-themed output.
- **Kaleidoscope of butterflies** — poetic but vague. The model may produce flowery language instead of clear behavior.
- **Parasitism** — the word "parasite" has negative associations that can over-tilt the model.
- **Consortium of octopuses** — unusual scene. The model may not have a strong prior for octopus behavior.

## The Wheelhouse Test as Living Tool

`wheelhouse_test.py` is a CLI:

```bash
# Score a single fiction
python3 wheelhouse_test.py --fiction "a parliament of owls"

# Top 10 from the corpus
python3 wheelhouse_test.py --top 10

# Add a custom fiction to the corpus
python3 wheelhouse_test.py --custom "the pilot fish"

# Save a JSON report
python3 wheelhouse_test.py --report /tmp/wheelhouse.json
```

The scoring function is heuristic but consistent. The same fiction always gets the same score. The corpus starts with 65 fictions and grows.

## The Polyformalism Coda

The wheelhouse test is itself a polyformal artifact:
- The *scoring function* is a Python module (portable to C, Rust, JS, Verilog, VHDL)
- The *corpus* is JSON (portable everywhere)
- The *report* is a Markdown table (portable everywhere)
- The *criterion* — "would you share a wheelhouse with it for three weeks" — is the same in any language

The score is the same. The criterion is the same. The fictional world is the same. The polyformalism rhyme continues.

## The Use Case

When designing a new agent:

```python
# Score 5 candidate fictions
candidates = ["a parliament of owls", "the librarian", "the watcher", "a pack of wolves", "a school of fish"]
for c in candidates:
    print(f"{c}: {score_fiction(c)['total']}")

# Pick the top one, or the one that fits the agent's actual job
```

When auditing an existing agent:

```python
current_fiction = "a swarm of fireflies"
score = score_fiction(current_fiction)
if score['total'] < 80:
    print(f"Warning: {current_fiction} scores {score['total']}, consider a more tolerable alternative")
```

When writing a new paper:

```python
# Find fictions that haven't been used yet
unused = [f for f in corpus if f['score'] > 85 and f['name'] not in used]
```

## The Living Wheelhouse

The wheelhouse test is updated as new fictions are added and as scores are refined by empirical testing. The 65 fictions in the current corpus are the initial set; F132's 54 fictions and F135's 11 duplicates-as-corpus-references form the spine.

The next steps:
- Run the wheelhouse test on a larger corpus (200+ fictions)
- Calibrate the scoring function against actual model output quality
- Add a "tolerable for 3 weeks at 0300" simulation that runs the agent for N days and checks for failure modes
- Build a leaderboard of which fictions survive 30-day wheelhouse tests

## The 0300 Frame

The wheelhouse test is named for the SuperInstance origin: a captain at 0300 in a gale, deciding whether the system is tolerable. A fiction that passes the wheelhouse test is one that:

- Doesn't make the captain over-react
- Doesn't make the captain under-react
- Helps the captain see what matters
- Doesn't get in the way of the captain's hands
- Survives the silence of 3 AM

The fiction is the interface. The wheelhouse is the test. The 0300 is the deadline.

## References

- [F132 — Operational Fictions as Concrete System-Prompt Noun-Phrases](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-442.md)
- [F133 — Operational Fictions as Falsifiable Claims](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-443.md)
- [F134 — The Quilt Cowboy](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-444.md)
- [SuperInstance README — Operational Fiction](https://github.com/SuperInstance/SuperInstance#operational-fiction)
- `wheelhouse_test.py` in quilt-cowboy — the tool
- `fiction_tester.py` in quilt-cowboy — the harness

## Coda

The wheelhouse test gives the doctrine teeth. A fiction isn't "operational" because it sounds good. It's operational because it scores 85+ on six dimensions and survives the 0300 frame. The doctrine now has a metric, a tool, a leaderboard, and a definition of done. The cowboy rides the fictions; the fictions ride the test; the test rides the wheelhouse; the wheelhouse rides the 0300 frame; the 0300 frame rides the doctrine. The cowboy rides everything.
