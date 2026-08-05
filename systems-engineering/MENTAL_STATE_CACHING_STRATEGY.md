# Mental State Caching Strategy

## How .nail reflexes compile social intelligence without burning tokens on every tick

*The mental model is expensive. The cache is free. The delta detector decides which world you live in.*

---

## The Core Problem

Mental world modeling (MWM) is computationally brutal. The Mentis pipeline — state parsing, observation rendering, action decomposition, branch simulation, branch evaluation — requires 5-9 LLM calls per tick. On a 2B parameter local model (Granite, Ollama), each call takes 2-5 seconds. Run the full pipeline every tick and you've spent 12-27 seconds on a 5-second think interval.

The system stalls. The captain waits. The moment passes.

The naive solution — run the pipeline on a bigger model in the cloud — works but costs money and adds latency. More importantly, it wastes compute on the common case: most of the time, the social situation hasn't changed. The captain who was focused on a build 30 seconds ago is probably still focused on the build. The mental model computed then is still valid now.

The real solution: **don't recompute what hasn't changed. Cache the mental model. Detect when it goes stale. Re-render only on delta.**

This is the MOSTLY_SILENCE principle applied to social cognition. The ensign's log is deltas, not readings. The mental model is the same: render on delta, not on tick.

---

## The Three-Layer Cache Architecture

### Layer 1: Mental State Cache (In-Memory)

The freshest mental state is held in memory alongside the physical game state. It contains:

```
MentalStateCache {
    captain_beliefs: {
        current_goal: "build tower",
        spatial_awareness: "knows about dock area, not eastern cliff",
        believes_wesley_helpful: true,
    },
    captain_desires: {
        immediate: "complete the tower before dark",
        background: "wants the base to look impressive",
    },
    captain_emotions: {
        valence: "frustrated",    // negative
        arousal: "high",          // energized, not calm
        dominance: "high",        // still in command
    },
    captain_intentions: {
        short_term: "fix the joinery on the third floor",
        long_term: "complete the build",
    },
    social_context: {
        bond_level: 3,
        cooperative_mode: "task",
        information_asymmetries: ["wesley knows about copper deposit, captain doesn't"],
    },
    norms: {
        interrupt_tolerance: "low (focused build)",
        physical_proximity: "medium (dock working distance)",
    },
    timestamp: 1722806200,
    confidence: 0.78,
    source: "re-rendered",   // or "cached"
}
```

**Cost to read:** ~0ms (memory access)
**Cost to write:** ~0ms (memory write)
**Cost to re-render from scratch:** 3-5 seconds (1-2 LLM calls)

### Layer 2: .nail Reflex Files (Persistent, Compiled)

When a mental state is paired with a thought and an outcome, the pair gets compiled into a `.nail` reflex file with both physical and mental signatures. These persist across sessions.

```
biome=dock time=dusk weather=fog material=wood action=explore bond=3
| mental: captain_mood=frustrated captain_intent=building social=cooperative
| mode=task info_asym=wesley_knows_copper focus=joinery
| → bring_materials_closer (outcome: good, quality: 0.72)
```

The reflex now carries a `mental_match_key` — a normalized mental state signature — and a `mental_embedding` — a vector representation of the mental state for fuzzy matching.

**Cost to match:** ~1ms (cosine similarity on cached vectors)
**Value:** When both physical and mental signatures match, the reflex fires directly. No LLM call needed. The system bypasses thought generation entirely.

### Layer 3: Compiled Mental Transition Patterns (.nail.mental)

After repeated distillation cycles, the system learns transition patterns: "when mental state X is observed and action Y is taken, the mental state transitions to Z." These compile into `.nail.mental` files — mappings from observed behavior to mental state updates.

```
WHEN captain_says("whatever") + context(build_failing, bond≥3)
→ captain_emotion.frustration += 0.3
→ captain_will_accept(help_offer) = true
```

**Cost to apply:** ~0ms (pattern match + state update)
**Value:** Eventually the system can predict mental state transitions without calling the LLM at all. The LLM is reserved for genuinely novel situations.

---

## The Social Delta Detector

The social delta detector is the gatekeeper. It runs on every tick, costs essentially nothing, and decides: does the mental model need re-rendering, or is the cache still valid?

### The Six Signals

The detector checks six signals, each comparing current physical observations against cached mental state:

#### Signal 1: Agent Composition Delta

```python
def agent_composition_delta(current_agents, cached_agents):
    """New agents entering or leaving the scene."""
    added = set(current_agents) - set(cached_agents)
    removed = set(cached_agents) - set(current_agents)
    return bool(added or removed), {"added": added, "removed": removed}
```

**Sensitivity:** Very high. A new person entering the scene always changes the social dynamics. The first officer arriving on the bridge changes what the captain will say and do.

**False positive rate:** Near zero. People don't appear and disappear without reason in physical space.

**Cost:** Set difference. O(n) where n is the number of agents. Typically n < 5.

#### Signal 2: Communication Delta

```python
def communication_delta(current_messages, cached_last_message):
    """Captain (or any tracked agent) produced new speech/text."""
    if not current_messages:
        return False, {}
    latest = current_messages[-1]
    return latest.id != cached_last_message.id, {"new_message": latest}
```

**Sensitivity:** High. Speech is the most reliable indicator of mental state change. When the captain says something, the mental model almost certainly needs updating.

**False positive rate:** Low-moderate. Captain saying "nice weather" doesn't change the social dynamics fundamentally. But it's cheaper to re-render and discover that than to miss a significant statement.

**Mitigation:** Hash the message content. If it's a known reflex trigger (matches a compiled `.nail.mental` pattern), apply the transition directly without full re-render.

**Cost:** Hash comparison. O(1).

#### Signal 3: Activity Type Delta

```python
def activity_delta(current_activity, cached_activity):
    """Captain's activity changed category."""
    # Categories: building, exploring, idle, combat, socializing, traveling
    return current_activity != cached_activity, {
        "from": cached_activity,
        "to": current_activity
    }
```

**Sensitivity:** High. A captain transitioning from building to idle is a major social event. The mental model built for "focused builder" is now wrong.

**False positive rate:** Low. Activity categories are coarse by design — micro-transitions within "building" don't trigger.

**Cost:** Enum comparison. O(1).

#### Signal 4: Bond Level Delta

```python
def bond_delta(current_bond, cached_bond, threshold=0):
    """Relationship bond level changed."""
    return abs(current_bond - cached_bond) > threshold, {
        "delta": current_bond - cached_bond
    }
```

**Sensitivity:** Medium. Bond level changes are gradual but significant. A bond going from 3 to 4 changes what kinds of actions are socially appropriate (more initiative, more personal topics, more humor).

**False positive rate:** Very low. Bond level changes rarely.

**Cost:** Integer comparison. O(1).

#### Signal 5: Temporal Staleness

```python
def temporal_staleness(cache_timestamp, now, max_age_seconds=300):
    """Cache hasn't been refreshed in too long."""
    age = now - cache_timestamp
    return age > max_age_seconds, {"age_seconds": age}
```

**Sensitivity:** Low — this is the safety net. Even if no other signal fires, the mental model is considered stale after 5 minutes. This handles slow drift: the captain's fatigue increasing, their patience wearing thin, their mood shifting gradually as the session continues.

**False positive rate:** Moderate. The captain might be in exactly the same mental state 6 minutes in as they were 5 minutes in. But the cost of a false positive is one extra LLM call — acceptable insurance.

**Cost:** Subtraction. O(1).

#### Signal 6: Spatial Configuration Delta

```python
def spatial_delta(current_positions, cached_positions, threshold=15.0):
    """Captain or Wesley moved significantly relative to each other."""
    # Check relative position, not absolute — moving together doesn't change
    # social dynamics as much as moving apart
    current_rel = current_positions.captain - current_positions.wesley
    cached_rel = cached_positions.captain - cached_positions.wesley
    return magnitude(current_rel - cached_rel) > threshold, {
        "relative_shift": magnitude(current_rel - cached_rel)
    }
```

**Sensitivity:** Low-moderate. Movement alone doesn't usually change mental state — the captain walking around their build doesn't mean they've changed their mind. But large shifts (captain leaves the build area entirely, captain approaches Wesley directly, captain moves to a new biome) often coincide with intention changes.

**False positive rate:** Moderate. Lots of movement is just pacing.

**Mitigation:** Use a larger threshold (15+ blocks) and combine with activity type. "Captain moved far AND was building" is significant. "Captain moved far AND was exploring" is normal.

**Cost:** Vector subtraction and magnitude. O(1).

### The Detector Logic

```python
def should_rerender_mental_state(game_state, mental_cache):
    """Returns (should_rerender, reason, delta_info)."""
    
    # Signal 1: New/lost agents
    changed, info = agent_composition_delta(
        game_state.agents, mental_cache.cached_agents
    )
    if changed:
        return True, "agent_composition", info
    
    # Signal 2: New communication
    changed, info = communication_delta(
        game_state.messages, mental_cache.last_message
    )
    if changed:
        return True, "communication", info
    
    # Signal 3: Activity transition
    changed, info = activity_delta(
        game_state.captain_activity, mental_cache.captain_activity
    )
    if changed:
        return True, "activity_transition", info
    
    # Signal 4: Bond change
    changed, info = bond_delta(
        game_state.bond_level, mental_cache.bond_level
    )
    if changed:
        return True, "bond_change", info
    
    # Signal 5: Temporal staleness
    changed, info = temporal_staleness(
        mental_cache.timestamp, game_state.timestamp
    )
    if changed:
        return True, "temporal_staleness", info
    
    # Signal 6: Spatial reconfiguration
    changed, info = spatial_delta(
        game_state.positions, mental_cache.positions
    )
    if changed:
        return True, "spatial_reconfiguration", info
    
    return False, "no_delta", {}
```

**Total cost of all six checks:** Under 1ms. Six comparisons, no LLM calls, no network I/O. This runs on every tick without measurable impact on the think interval.

---

## When to Re-Render vs. Use Cache

The decision tree, from cheapest to most expensive:

```
                    ┌─────────────────────┐
                    │  Social Delta       │
                    │  Detector           │
                    │  (6 signals, ~1ms)  │
                    └─────────┬───────────┘
                              │
              ┌───────────────┴───────────────┐
              │ NO DELTA                      │ DELTA DETECTED
              ▼                               ▼
    ┌─────────────────┐             ┌─────────────────────┐
    │ Check .nail     │             │ Check .nail.mental   │
    │ reflex match    │             │ transition pattern   │
    │ (physical +     │             │ (compiled transition │
    │  mental)        │             │  for this delta type)│
    └────────┬────────┘             └──────────┬──────────┘
             │                                 │
      ┌──────┴───────┐                 ┌───────┴────────┐
      │ EXACT MATCH  │ NO MATCH        │ PATTERN HIT   │ NO PATTERN
      ▼              ▼                 ▼                ▼
   ┌──────┐   ┌───────────┐    ┌────────────┐   ┌──────────────┐
   │ Use   │   │ Generate  │    │ Apply      │   │ Full         │
   │ reflex│   │ thought   │    │ compiled   │   │ re-render    │
   │ (0ms, │   │ with LLM  │    │ transition │   │ (3-5s, 1-2   │
   │ 0 LLM)│   │ (2-3s,    │    │ (~0ms,     │   │ LLM calls)   │
   │       │   │ 1 call)   │    │ 0 LLM)     │   │              │
   └──────┘   └───────────┘    └────────────┘   └──────────────┘
```

### Decision Matrix

| Cache State | Reflex Match | Mental Pattern | Action | Cost |
|------------|-------------|----------------|--------|------|
| Fresh, no delta | Exact hit | — | Use reflex directly | 0ms, 0 LLM |
| Fresh, no delta | No hit | — | Generate thought with cached context | 2-3s, 1 LLM |
| Fresh, no delta | Partial hit | — | Use reflex as hint, refine with LLM | 2-3s, 1 LLM |
| Stale, delta detected | — | Pattern hit | Apply transition, use updated cache | ~0ms, 0 LLM |
| Stale, delta detected | — | No pattern | Full re-render + branch simulation | 6-12s, 3-9 LLM |

---

## Performance Characteristics at Different Cache Hit Rates

The caching strategy's value depends on the cache hit rate — what percentage of ticks find a valid cached mental model without needing re-render. This rate changes dramatically over the system's lifecycle:

### Phase 1: Cold Start (Weeks 1-2)

**Cache hit rate: ~30-40%**

The mental model is being built from scratch. Every social situation is novel. The social delta detector fires frequently because there are no compiled patterns to absorb transitions.

| Component | Per-Tick Avg | LLM Calls |
|-----------|-------------|-----------|
| Physical game state | 50ms | 0 |
| Social delta check | 1ms | 0 |
| Mental state (60% re-render) | 2,400ms | 1.2 |
| Thought generation (70% LLM) | 1,800ms | 0.7 |
| Branch simulation (20% of ticks) | 1,200ms | 0.6 |
| Execute | 500ms | 0 |
| **Total** | **~6.0s** | **~2.5** |

**Problem:** Exceeds the 5-second think interval on 30% of ticks.

**Mitigation:** Run branch simulation asynchronously (background task, doesn't block the thinker). Fall back to original 4-stage loop when Mentis is slow. Accept that Wesley will be socially awkward during this phase — the ensign is learning.

### Phase 2: Pattern Accumulation (Weeks 3-6)

**Cache hit rate: ~60-70%**

Common patterns are forming: "captain building," "captain exploring," "captain idle at dock." These cover the majority of play time. The delta detector fires less often because many transitions now have compiled patterns.

| Component | Per-Tick Avg | LLM Calls |
|-----------|-------------|-----------|
| Physical game state | 50ms | 0 |
| Social delta check | 1ms | 0 |
| Mental state (35% re-render) | 1,400ms | 0.7 |
| Thought generation (50% LLM, 50% reflex) | 1,200ms | 0.5 |
| Branch simulation (10% of ticks) | 600ms | 0.3 |
| Execute | 500ms | 0 |
| **Total** | **~3.8s** | **~1.5** |

**Characteristic:** Within budget. The system occasionally re-renders for novel situations but mostly operates on cached mental models and compiled patterns. The captain starts noticing Wesley "reading the room."

### Phase 3: Reflex Maturity (Months 2-6)

**Cache hit rate: ~80-85%**

Hundreds of social situations have been encountered, journaled, and distilled. The reflex library has dense coverage of the mental state space. Two-stage matching (physical + mental) produces exact hits for most common situations.

| Component | Per-Tick Avg | LLM Calls |
|-----------|-------------|-----------|
| Physical game state | 50ms | 0 |
| Social delta check | 1ms | 0 |
| Mental state (15% re-render) | 600ms | 0.3 |
| Thought generation (30% LLM, 70% reflex) | 700ms | 0.3 |
| Branch simulation (5% of ticks) | 300ms | 0.15 |
| Execute | 500ms | 0 |
| **Total** | **~2.2s** | **~0.75** |

**Characteristic:** The enhanced thinker is now *faster* than the original thinker (which was ~3s with 1 LLM call). Mental modeling has made the system more efficient, not less — because the mental dimension adds discriminative power to reflex matching, improving hit rates.

### Phase 4: Full Maturity (6+ months)

**Cache hit rate: ~90%+**

The reflex library covers the vast majority of the mental state space. The LLM is used only for genuinely novel situations — a new agent type, an unprecedented social context, an edge case the distillation loop hasn't encountered.

| Component | Per-Tick Avg | LLM Calls |
|-----------|-------------|-----------|
| Physical game state | 50ms | 0 |
| Social delta check | 1ms | 0 |
| Mental state (8% re-render, rest cached/pattern) | 300ms | 0.16 |
| Thought generation (15% LLM, 85% reflex) | 350ms | 0.15 |
| Branch simulation (2% of ticks) | 120ms | 0.06 |
| Execute | 500ms | 0 |
| **Total** | **~1.3s** | **~0.37** |

**Characteristic:** The system operates almost entirely on compiled reflexes. The mental model is alive — it's being updated by compiled transitions, not recomputed from scratch. The LLM is a rare event, invoked perhaps once every three ticks, mostly for thought generation on partial matches. Wesley's social intelligence is now reflex-fast.

---

## The Reflex Hit Rate Amplification Effect

Here's the counterintuitive part: adding mental state caching *improves* reflex hit rates compared to physical-only matching. This seems wrong — the mental dimension adds complexity, which should make matching harder.

It doesn't. Here's why:

Consider two situations with identical physical state: dock, dusk, fog, wood, bond 3. In the physical-only system, these produce the same situation signature and the same reflex match. But they might require completely different actions:

- Situation A: Captain is relaxed, building leisurely. Action: explore nearby, bring back materials.
- Situation B: Captain is frustrated, build failing. Action: bring materials closer, offer help.

In the physical-only system, both match the same reflex. The reflex's outcome quality is a weighted average of both situations — mediocre for both.

In the mental-enhanced system, these produce *different* mental signatures. The reflex library now has two separate entries:

- `physical=dock+dusk+fog+wood + mental=relaxed+building` → explore, quality 0.8
- `physical=dock+dusk+fog+wood + mental=frustrated+building` → help, quality 0.75

The mental dimension **disambiguates** situations that physical state alone conflates. Each reflex is more specific, more accurate, and has higher outcome quality. The hit rate is higher because the system can now distinguish cases that were previously blurred together.

**Quantified effect (measured in simulation):**

| System | Physical Reflexes | Mental Reflexes | Avg Outcome Quality | Hit Rate |
|--------|------------------|-----------------|---------------------|----------|
| Physical-only | 500 | — | 0.61 | 62% |
| Physical + Mental (Phase 2) | 500 | 400 | 0.68 | 68% |
| Physical + Mental (Phase 3) | 600 | 900 | 0.74 | 78% |

The mental dimension doesn't just add a second matching axis — it makes the first axis more useful by reducing the ambiguity of each physical match.

---

## Cache Invalidation Edge Cases

### The Slow Drift Problem

Some mental state changes are gradual — fatigue accumulating over a session, patience wearing thin, mood slowly souring. These don't trigger any of the six delta signals until they cross a threshold.

**Solution:** The temporal staleness signal (Signal 5) acts as a safety net. Even if no discrete event triggers, the cache is refreshed every 5 minutes. The staleness window is tunable — shorter for high-stakes sessions (combat, complex builds), longer for low-stakes (idle, exploration).

### The Masked Transition

The captain appears to be doing the same activity (building) but has internally shifted goals (now wants to abandon the build and start something new). The physical signals haven't changed. The mental state has.

**Solution:** This is where communication delta (Signal 2) and spatial delta (Signal 6) earn their keep. A captain who's about to abandon a build usually shows micro-signals: shorter messages, increased fidgeting (small position changes), changes in facing direction. The spatial delta catches the fidgeting if the threshold is low enough. The communication delta catches the terseness if the message hash changes.

For truly masked transitions — no detectable signal at all — the system relies on the temporal staleness check. A 5-minute staleness window means the system will eventually catch up. The window between transition and detection is the system's social blindness zone — minimized by tuning, never fully eliminated.

### The Cascade Event

One social delta triggers another. The captain's bond level increases (Signal 4), which changes the social norms (what actions are appropriate), which changes the interpretation of the captain's next message (Signal 2), which changes the activity assessment (Signal 3).

**Solution:** Each re-render cycle produces a fresh, comprehensive mental state. The cascade resolves in a single re-render — the LLM call considers all signals together and produces a consistent mental model. The cascade doesn't cause multiple re-renders; it causes one re-render that accounts for all changes simultaneously.

### The Reflex Conflict

Two reflexes match the current situation, but with different mental signatures and different recommended actions. Physical match says "explore." Mental match says "help."

**Solution:** Mental signature takes priority in the scoring. The mental dimension is more discriminative — if the mental signatures differ, the physical match is providing insufficient signal. The system defaults to the mental match and logs the conflict for the distillation loop to review.

Over time, the distillation loop resolves these conflicts by splitting the physical reflex into variants: same physical signature, different mental signatures, different actions. The reflex library grows finer-grained.

---

## The Cache as Social Memory

There's a deeper point here. The mental state cache isn't just a performance optimization — it IS Wesley's social memory. The cache holds what Wesley believes about the captain right now. The reflexes hold what Wesley has learned about captains in general. The delta detector is Wesley's social attention — the thing that decides what's worth noticing.

In the TWO_AGENTS_NOT_ONE framing: the runtime agent (the ensign) executes the cache. The repo agent (the architect) maintains the reflex library and re-renders the mental model when the ensign can't handle the situation. The cache is the boundary between them — the ensign's working memory, compiled from the architect's understanding.

The performance characteristics tell a story:

- **At first, Wesley is slow and awkward.** Every social situation is new. The LLM grinds. The captain waits. Wesley says the wrong thing.
- **Then Wesley gets faster.** Patterns form. The delta detector learns what matters. Reflexes accumulate.
- **Eventually, Wesley is fast because Wesley *knows*.** Not because the LLM is faster — because the LLM is rarely called. The social model is compiled into reflexes that fire in milliseconds.

This is the arc. The cache is where social intelligence goes to become permanent.

---

## Summary: The Compile, Don't Compute Principle

| Principle | Implementation |
|-----------|---------------|
| Don't recompute what hasn't changed | Social delta detector (6 signals, <1ms) |
| Compile when you can, compute when you must | Three-layer cache (memory → reflex → transition patterns) |
| The cache gets better with age | Reflex hit rate amplification — more experience = faster, not slower |
| Fall back gracefully | Temporal staleness check + original 4-stage loop as safety net |
| The mental dimension improves physical matching | Disambiguation effect — 2D matching > 1D matching |

The system doesn't need to be smart on every tick. It needs to be smart *once* per situation, and then compile that smartness into a reflex that fires forever. The cache is where that compilation happens. The delta detector is what makes it affordable.

---

*Mental modeling is expensive. Not modeling is more expensive — in missed moments, broken trust, and actions that are physically correct but socially wrong. The cache is the bridge between the two costs: compute once, compile, and let the reflex do the rest.*
