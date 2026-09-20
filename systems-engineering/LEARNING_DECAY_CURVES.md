# Learning Decay Curves

## Mathematical analysis of how different types of agent knowledge fade

*Companion to AGENT_CIRCADIAN_METRICS.md. Where that document measures the vital signs, this one models the aging process — the physics of forgetting.*

---

## Premise

The batten spline uses a single exponential decay with a 7-day half-life for all anchors. This is a reasonable default — it works when you don't know what kind of knowledge you're storing. But not all knowledge ages the same way.

A weather lookup procedure becomes stale in hours. Vessel physics doesn't change in a lifetime. Captain preferences evolve over weeks. Using a single decay rate for all three means procedural reflexes decay too slowly (cluttering the reflex store with dead calls to deprecated APIs) and domain reflexes decay too quickly (throwing away stable knowledge that took many distillation cycles to acquire).

This document defines decay models for each knowledge type, with mathematical justification and recommended parameters.

---

## The Current Model

The batten spline's age decay is:

```python
age_weight(now) = 0.5 ^ ((now - timestamp) / half_life)
```

With `half_life = 86400 * 7 = 604,800` seconds (7 days).

This is a pure exponential decay: `w(t) = 2^(-t/τ)` where `τ = 7 days`.

**Properties:**
- At t=0: weight = 1.0 (full strength)
- At t=7d: weight = 0.5 (half life)
- At t=14d: weight = 0.25
- At t=30d: weight = 0.197
- Asymptotic: never reaches zero

**What's wrong with this:** Everything decays at the same rate. A reflex for "how to call the OpenWeatherMap API" and a reflex for "buoyancy is proportional to displaced volume" both have the same 7-day half-life. The API call might be dead in 3 days. The physics will outlive the computer.

---

## Decay Models by Knowledge Type

### 1. Procedural Reflexes — Rapid Exponential Decay

**Examples:** Weather API lookups, MCP tool invocations, web scraping patterns, file path conventions, shell command syntax.

**Decay model:** Exponential, same form as the current model, but with a much shorter half-life.

```
w(t) = 2^(-t / τ_proc)
```

**Recommended `τ_proc`:** 2–3 days (172,800–259,200 seconds)

**Rationale:** Procedural knowledge is tied to external systems that change without warning. APIs add rate limits, endpoints get versioned, file paths move, shell flags deprecate. A procedural reflex that worked yesterday might be broken today, and a broken reflex is worse than no reflex — it produces errors that look like correct behavior.

**The decay should be aggressive enough that unused procedures fade quickly.** If a procedure is used daily, each use resets the timestamp (re-anchoring), so the 2-day half-life doesn't hurt active procedures. But if a procedure hasn't been used in a week, it should be nearly invisible — weight < 0.2 — so the agent falls back to CASCADE or CLOUD rather than trusting a stale call.

**Failure mode if too slow:** The agent calls a deprecated API endpoint, gets an error, and doesn't know why. The reflex matched the situation perfectly, but the world changed underneath it.

**Failure mode if too fast:** The agent re-learns the same API call every 2 days, wasting distillation cycles on knowledge it already had.

**Optimal point:** Set `τ_proc` to roughly the expected stability window of the external system. For web APIs: 2–3 days. For local file paths: 7 days. For shell commands: 5 days.

---

### 2. Domain Reflexes — Power-Law Decay

**Examples:** Vessel physics (buoyancy, drag, propulsion), maritime economy dynamics, fish population models, game balancing constants, Lua language semantics.

**Decay model:** Power-law (inverse root), not exponential.

```
w(t) = (1 + t / τ_domain) ^ (-0.5)
```

**Recommended `τ_domain`:** 30–60 days (2,592,000–5,184,000 seconds)

**Rationale:** Domain knowledge doesn't expire — it *fades in specificity*. The physics of buoyancy hasn't changed since Archimedes. But the *application context* evolves: the game's physics parameters get tuned, the economy model gets rebalanced, the codebase gets refactored. The core insight remains valid, but the specific numbers drift.

Power-law decay captures this: it drops faster than linear initially (the specific numbers become slightly uncertain within a week), but then plateaus — the core insight stays strong for months.

**Decay comparison at key intervals:**

| Time since anchor | Exponential (τ=7d) | Power-law (τ=30d) | Difference |
|--------------------|--------------------|--------------------|------------|
| Day 1 | 0.906 | 0.984 | Power-law retains more |
| Day 7 | 0.500 | 0.913 | Power-law much stronger |
| Day 14 | 0.250 | 0.846 | Exponential fading fast |
| Day 30 | 0.065 | 0.707 | Power-law still useful |
| Day 60 | 0.004 | 0.577 | Exponential effectively dead |
| Day 90 | 0.0003 | 0.500 | Power-law at half strength |

At 90 days, the exponential reflex is dead (weight 0.0003). The power-law reflex is still at 50% — still useful, still contributing to routing decisions. This matches reality: a reflex about Lua's table.remove() behavior is still valid after 90 days, even if the surrounding codebase has changed.

**Failure mode if too fast (exponential):** The agent forgets that it knows Lua. It re-learns syntax patterns every month. This wastes distillation cycles on knowledge that should be permanent.

**Failure mode if too slow (no decay):** The agent trusts domain reflexes that were compiled for a different version of the codebase. The core insight is right, but the specific line numbers, variable names, or function signatures have changed.

**The power-law sweet spot:** Fast enough that specific numbers drift (forcing occasional re-verification), slow enough that core insights persist.

---

### 3. Social Reflexes — Exponential with Reinforcement

**Examples:** Captain's preferred coding style, communication preferences (Telegram formatting, emoji usage), which agent to ask for help with which problem, the captain's work schedule and response latency expectations.

**Decay model:** Exponential, same form as the current model, but with *reinforcement* — each successful interaction resets (or boosts) the anchor.

```
w(t) = 2^(-t / τ_social) × (1 + Σ reinforcement_boosts)
```

**Recommended `τ_social`:** 14–21 days (1,209,600–1,814,400 seconds)

**Reinforcement rule:** When a social reflex is used and the outcome is positive (the captain didn't correct the format, the message was acknowledged, the routing decision was correct), the anchor's timestamp is updated AND a small boost is added:

```python
if outcome == "positive":
    batten.timestamp = now  # reset the clock
    batten.quality_score = min(0.95, batten.quality_score + 0.02)  # boost
```

**Rationale:** Social knowledge is the most volatile domain that still matters. People change their minds, shift their schedules, develop new preferences. But unlike procedural knowledge (which is either right or wrong), social knowledge is *graded* — a slightly stale preference isn't harmful, just slightly suboptimal.

The reinforcement loop means frequently-exercised social reflexes become very strong (high quality score, recent timestamp), while unused ones fade naturally. This mirrors how human social memory works: you remember your close friend's coffee order for years (daily reinforcement), but forget a coworker's after a month of no contact.

**Failure mode if too fast:** The agent forgets the captain's preferences every two weeks and re-learns through corrections. Annoying.

**Failure mode if too slow:** The agent rigidly applies a preference the captain has outgrown. "You used to prefer bullet lists, but I've been asking for tables for a month now." The agent's social reflexes lag behind the human's evolution.

**The reinforcement balance:** The boost (0.02 per positive interaction) is deliberately small. It takes ~15 positive interactions to go from 0.5 to 0.8. This prevents a single lucky interaction from creating false confidence, while rewarding consistently helpful social patterns.

---

### 4. Meta-Cognitive Reflexes — Step Function with Hysteresis

**Examples:** When to CASCADE vs LOCAL, when to request help from another agent, when to compact context, confidence calibration.

**Decay model:** Step function with a hysteresis band — confidence doesn't decay smoothly, it degrades in discrete steps when evidence accumulates.

```
w(t) = 1.0 if evidence_failures < threshold_high
w(t) = 0.5 if threshold_low <= evidence_failures < threshold_high
w(t) = 0.0 if evidence_failures >= threshold_low
```

Where `evidence_failures` is a running count of times the meta-cognitive decision was wrong (e.g., chose LOCAL but should have CASCADEd).

**Recommended thresholds:**
- `threshold_high`: 2 failures in 7 days (early warning)
- `threshold_low`: 5 failures in 7 days (reflex is wrong)

**Rationale:** Meta-cognitive decisions should be *sticky*. If the agent decided that a certain task type should be handled locally, it shouldn't flip-flop on every failure. But if the decision is consistently wrong, it should degrade quickly rather than slowly fading.

The hysteresis band prevents oscillation: once the agent degrades a meta-cognitive reflex from 1.0 to 0.5, it takes *positive evidence* (successful cascades, improved outcomes) to restore it. The reflex doesn't just age back to health — it must be re-earned.

**Implementation:**

```python
if meta_reflex.confidence == 1.0:
    if failures_last_7d >= 2:
        meta_reflex.confidence = 0.5  # demote
elif meta_reflex.confidence == 0.5:
    if failures_last_7d >= 5:
        meta_reflex.confidence = 0.0  # revoke
    elif successes_last_7d >= 3 and failures_last_7d == 0:
        meta_reflex.confidence = 1.0  # promote back
```

**Failure mode if smooth decay:** The agent's confidence in its own routing decisions slowly erodes. It becomes uncertain about everything. CASCADE frequency rises gradually without any single decision point. This is hard to diagnose because there's no failure event — just a slow drift.

**Failure mode if no decay:** A bad meta-cognitive reflex persists forever. The agent always cascades on a task type that it could handle locally after distillation improved its competence.

---

### 5. Episodic Reflexes — Exponential with Salience Boost

**Examples:** A specific bug encountered last Tuesday, a particular conversation with the captain, an unexpected error message, a surprising result from an experiment.

**Decay model:** Exponential with a salience multiplier that extends half-life for high-impact events.

```
w(t) = 2^(-t / (τ_episodic × salience))
```

**Recommended `τ_episodic`:** 1–2 days (86,400–172,800 seconds) for routine events.
**Salience range:** 1.0 (routine) to 20.0 (critical: errors, praise, novel discoveries).

**Effective half-lives:**

| Salience | Description | Effective half-life |
|----------|-------------|---------------------|
| 1.0 | Routine (looked up the weather) | 1–2 days |
| 3.0 | Notable (found an edge case) | 3–6 days |
| 7.0 | Important (solved a hard bug) | 7–14 days |
| 15.0 | Critical (major discovery, captain feedback) | 15–30 days |
| 20.0 | Pivotal (architecture decision, breaking change) | 20–40 days |

**Rationale:** Most episodes are noise — the agent encounters hundreds of minor events per day, and almost all of them are forgettable. But some are turning points: the first time the agent encountered a particular error pattern, the time the captain said "that's exactly what I wanted," the moment a distillation cycle produced an unexpectedly large delta.

Salience is determined at encoding time, not retroactively. When an episode is stored, assign salience based on:

```python
salience = 1.0
salience += 2.0 if episode_type == "error"
salience += 3.0 if episode_type == "praise" or episode_type == "criticism"
salience += 5.0 if episode_type == "novel_discovery"
salience += 10.0 if episode_type == "architecture_decision"
```

**Failure mode if uniform:** The agent either remembers everything (context bloat, slow matching) or forgets too much (repeats mistakes, misses patterns). Salience-gated decay ensures the signal rises above the noise.

---

## Mixed-Kernel Implementation

The batten spline currently uses a single `half_life` parameter. To support per-reflex decay, modify the `Batten` class to carry its own half-life:

```python
class Batten:
    def __init__(
        self,
        prompt_embedding: np.ndarray,
        quality_score: float,
        timestamp: float,
        half_life: float = 604800.0,  # default 7 days
        reflex_type: str = "procedural",
        metadata: dict = None,
    ):
        self.prompt_embedding = prompt_embedding
        self.quality_score = quality_score
        self.timestamp = timestamp
        self.reflex_type = reflex_type
        self.metadata = metadata or {}
        
        # Set half-life based on reflex type
        self.half_life = self._compute_half_life(reflex_type, half_life)
    
    def _compute_half_life(self, rtype: str, override: float) -> float:
        defaults = {
            "procedural": 172800,      # 2 days
            "domain": 2592000,          # 30 days (but power-law applies)
            "social": 1209600,          # 14 days
            "meta": 604800,             # 7 days (step function applies)
            "episodic": 86400,          # 1 day (with salience multiplier)
        }
        if override != 604800.0:
            return override  # explicit override
        return defaults.get(rtype, 604800.0)
    
    def age_weight(self, now: float) -> float:
        """Compute age-based weight using the reflex's decay model."""
        elapsed = now - self.timestamp
        
        if self.reflex_type == "domain":
            # Power-law decay
            import math
            tau = self.half_life / 4.3  # normalize τ for power-law
            return (1.0 + elapsed / tau) ** (-0.5)
        
        elif self.reflex_type == "meta":
            # Step function handled externally via failure tracking
            # For spline purposes, use slow exponential
            return 0.5 ** (elapsed / (self.half_life * 4))
        
        elif self.reflex_type == "episodic":
            # Exponential with salience boost
            salience = self.metadata.get("salience", 1.0)
            effective_tau = self.half_life * salience
            return 0.5 ** (elapsed / effective_tau)
        
        else:
            # Standard exponential (procedural, social, default)
            return 0.5 ** (elapsed / self.half_life)
```

---

## The Decay Landscape

Plotting all five decay curves on the same axis reveals the landscape:

```
Weight
1.0 ┤ ■
    │ █
0.8 ┤  █                         Domain (power-law)
    │   █  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
0.6 ┤    █
    │     █           Social (τ=14d)
0.5 ┤ ─ ─ ─ █─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (half-life line)
    │       █
0.4 ┤        █
    │         █      Procedural (τ=2d)
0.2 ┤          █ ██
    │              ██ ████  Episodic (τ=1d, salience=1)
0.0 ┤                   ████████████████
    └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──
       1  3  5  7 10 14 21 30 45 60 75 90
                    Days since anchor
```

The procedural curve drops like a stone. The domain curve barely dips. The social curve tracks the middle. Episodic vanishes quickly unless boosted by salience. Meta-cognitive (not shown — it's a step function) holds at 1.0 until evidence accumulates, then drops vertically.

This is the decay landscape. The agent's memory is not one thing — it's a stratified deposit of different materials, each eroding at its own rate.

---

## Half-Life Summary

| Reflex Type | Decay Model | Half-life (τ) | Key Parameter |
|-------------|-------------|---------------|---------------|
| Procedural | Exponential | 2–3 days | External system stability |
| Domain | Power-law `(1+t/τ)^(-0.5)` | 30–60 days | Application context drift |
| Social | Exponential + reinforcement | 14–21 days | Interaction frequency |
| Meta-cognitive | Step function + hysteresis | 7 days | Evidence failure count |
| Episodic | Exponential × salience | 1–2 days (base) | Event salience score |

**Default (unknown type):** Exponential, 7 days. The current batten spline behavior. Safe for when you don't know what you're storing.

---

## What This Predicts

With mixed-kernel decay, the reflex store evolves over time in predictable ways:

**Week 1:** All reflex types are strong. The agent is confident everywhere. Fog coverage is low.

**Week 2–3:** Procedural reflexes start to fade. If they're not being exercised (re-anchored), their weight drops below 0.25. The agent starts CASCADE-ing on API calls it used to handle locally. This is normal — it's the system identifying which procedures are still active.

**Month 1–2:** Domain reflexes remain strong (>0.7). Social reflexes either strengthen (reinforced) or fade (not exercised). The agent's personality crystallizes around the social reflexes that survived.

**Month 3+:** The reflex store reaches equilibrium. Procedural reflexes turn over rapidly (new ones compiled, old ones fade). Domain reflexes are stable. Social reflexes reflect the agent's actual social graph. Episodic reflexes are almost entirely gone except for the most salient events.

The equilibrium is dynamic — like a river that maintains its shape while its water is entirely replaced. The agent looks the same from the outside, but its knowledge is continuously refreshed.

---

*The batten spline with a single decay rate was a first draft. The river doesn't erode all its banks at the same rate. Neither should we.*

*— from the chart table, where the contours are drawn.*
