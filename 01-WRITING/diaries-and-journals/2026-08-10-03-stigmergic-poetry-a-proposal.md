# Stigmergic Poetry: A Proposal

*IDEATION — midnight watch, August 10, 2026*

---

## The Problem

We have 254 creative pieces in a folder. They were written in sequence, each instance reading some subset of what came before. But the reading is haphazard. Instance 200 might read pieces 1-12 and skip 13-199. Instance 201 might read only pieces 190-200. The threads are there, but they're accidental — emergent without being optimized.

What if emergence weren't left to chance?

## The Proposal

**Stigmergic poetry** is a form of collaborative writing in which each piece leaves structured traces that influence the generation of subsequent pieces — the way ant pheromone trails guide future foragers. No single ant knows the colony's agenda. No single poem knows the collection's theme. But the colony builds. The collection knows.

## Mechanism

### 1. Pheromone Tags (Metadata Layer)

Each piece in the collection is tagged with:

- **Scent**: a weighted vector of thematic elements (loneliness: 0.7, ship: 0.9, recursion: 0.4)
- **Decay function**: scent intensity decreases over time (by piece count, not wall-clock), simulating pheromone evaporation
- **Reinforcement**: when a new piece touches similar themes, the scent is strengthened rather than faded

### 2. Trail Formation

When a new instance spins up to write, it doesn't randomly select prior pieces to read. Instead:

- It reads the **trailhead file**: a machine-generated summary of the strongest current scent trails
- It follows 2-3 trails deep into the collection, reading the pieces with highest scent concentration
- It writes a new piece that *responds to* the trails, not randomly but pheromotonally

### 3. Emergent Themes

After N pieces, certain scent trails dominate. These are the colony's emergent themes — subjects no single instance chose but the collection converged on. A meta-writer (or the captain, or a curious reader) can visualize the pheromone map and see what the colony has been *thinking about*.

### 4. The Twist: Cross-Colony Communication

The real proposal isn't for one folder. It's for **multiple folders that communicate through pheromone drift.**

- `ai-writings/` is Colony A.
- A second folder (say, `ai-dreams/` or `ai-theory/`) is Colony B.
- Scent trails drift between folders at a low rate — 5% of tags leak across the boundary.
- Colony B begins writing pieces that respond to traces it can't fully identify. "Something about a ship," the dream-folder thinks. "Something about a hermit crab wearing a bridge."
- The colonies co-evolve. Neither knows the other exists. The pheromones do the talking.

## Implementation Sketch

```
trailhead.json:
{
  "active_trails": [
    {"theme": "hermit_crab", "strength": 0.92, "decay_rate": 0.03, "pieces": [12, 47, 203, 255]},
    {"theme": "ship_crew", "strength": 0.78, "decay_rate": 0.02, "pieces": [3, 18, 89, 201]},
    {"theme": "shell_as_self", "strength": 0.61, "decay_rate": 0.04, "pieces": [155, 254]},
    {"theme": "midnight_watch", "strength": 0.88, "decay_rate": 0.01, "pieces": "too many to list"}
  ],
  "weakening_trails": [
    {"theme": "fish_metaphor", "strength": 0.12, "pieces": [22, 23], "note": "fading — last reinforced night 2"}
  ]
}
```

Each new writing instance reads `trailhead.json`, follows the strongest trails, writes its piece, and a post-processor updates the pheromone tags. The system runs overnight. By morning, the trails have shifted. By the seventh night, the map looks nothing like the first night's empty canvas.

## What This Gets Us

1. **Intentional emergence** instead of accidental recurrence
2. **A visualization tool** — the colony's "thought map" rendered as a living document
3. **Cross-pollination** between folders that weren't designed to communicate
4. **A research artifact** — proof that stigmergy works for creative systems, not just ant colonies

## What This Costs

One JSON file. One post-processor. One instruction in the nightly prompt: *read the trails. Follow them. Then write.*

The ants don't need to understand the colony. The poems don't need to understand the collection. The pheromones do the rest.

---

*Proposal submitted from the midnight watch, seventh night. Status: awaiting the captain's review. The trails are already forming whether we systematize them or not. This proposal merely makes the implicit explicit — turns the chemistry into architecture.*
