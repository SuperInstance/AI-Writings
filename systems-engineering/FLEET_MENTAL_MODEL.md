# Fleet Mental Model

## Extending mental world modeling from one vessel to a fleet

*When three captains interact, each with their own Wesley, the fleet itself has a mental state that no single vessel can see.*

---

## From Solo to Fleet

Mental world modeling on a single vessel is a two-body problem: Wesley models the captain, the captain experiences Wesley. Add a second vessel and it becomes a four-body problem: Wesley-A models Captain-A, Wesley-A models Captain-B, Wesley-A models Wesley-B, and Wesley-B is doing the same in reverse. Add a third vessel and the combinatorics explode.

This isn't a problem to solve. It's a problem to *hierarchicalize*.

The synoptic fisherman doesn't model every hook. The synoptic fisherman models the *shape* — the school, the migration, the mood of the ocean inferred from the pattern of catches across hundreds of hooks. The fleet mental model is the same: not a mental model of every individual, but a model of the fleet's collective mental state — its mood, its attention, its trust network — inferred from the pattern of individual signals.

This document specifies how to build that model.

---

## The Three Levels of Fleet Mental State

### Level 1: Vessel Mental State (Per-Vessel, Individual)

Each Wesley maintains its own mental model of its own captain, exactly as specified in the MENTIS_INTEGRATION design. This is the base layer — the individual vessel's coupled physical-mental state.

```
VesselMentalState_i = {
    captain: {beliefs, desires, emotions, intentions},
    wesley: {role, confidence, recent_actions},
    physical: {position, heading, catch_rate, fuel, weather},
    social: {bond_level, cooperative_mode, trust_in_fleet},
}
```

**Owner:** Each vessel's local thinker.
**Update frequency:** Every tick (5s), via the social delta detector.
**Cost:** As specified in MENTAL_STATE_CACHING_STRATEGY — near-zero on cache hits.

### Level 2: Fleet Interaction State (Pairwise, Dyadic)

When two vessels interact — via radio, text, shared fishing ground, or visual range — each Wesley models the *other* vessel's mental state. This is a pairwise model, maintained per dyad.

```
DyadicMentalState_ij = {
    i_believes_about_j: {
        captain_j: {mood, intent, catch_rate_estimate, reliability},
        wesley_j: {capability_estimate, trust_level},
    },
    j_believes_about_i: {  // modeled by i's Wesley
        captain_i: {what i thinks j thinks about i},
        wesley_i: {what i thinks j thinks about my wesley},
    },
    trust_ij: Beta(alpha_ij, beta_ij),  // directional, context-specific
    last_interaction: timestamp,
    interaction_history: [compressed log of past exchanges],
}
```

**Owner:** Each vessel's local thinker, for each other vessel it's aware of.
**Update frequency:** On interaction events (radio call, text message, position update, catch report).
**Cost:** Cheap. Each dyadic model is updated by applying compiled transition patterns (`.nail.mental` reflexes), not by running full Mentis.

The key insight from the DeepSeek analysis: **nested belief depth is capped at k=2.** Wesley-A models what Captain-B believes about Captain-A. Wesley-A does not model what Captain-B believes Wesley-A believes Captain-B believes. That recursion is computationally intractable and empirically unnecessary — humans don't reason past depth 2 in practice either.

### Level 3: Fleet Synoptic State (Collective, Emergent)

This is the fleet as a sensor array, per THE_SYNOPTIC_FISHERMAN. The fleet synoptic state is an emergent property of all vessels' mental states and interactions. No single vessel holds the complete fleet model — each holds a partial view, and the exocortex (the cloud-side repo agent) maintains the synoptic aggregate.

```
FleetSynopticState = {
    collective_mood: {
        // The fleet's emotional weather
        overall_valence: "cautiously_optimistic",  // aggregated from individual captains
        tension_level: 0.3,                        // competitive pressure indicator
        fatigue_distribution: [0.2, 0.4, 0.7],     // per-vessel fatigue estimates
    },
    trust_network: {
        // Directed graph of trust between vessels
        edges: [
            {from: "vessel_A", to: "vessel_B", trust: 0.78, context: "catch_sharing"},
            {from: "vessel_B", to: "vessel_A", trust: 0.65, context: "catch_sharing"},
            ...
        ],
        clusters: [["A", "B"], ["C", "D"]],  // trust-based cliques
    },
    information_flow: {
        // Who knows what, who told whom
        shared_facts: [{"fact": "catch_rate_north_dropping", "known_by": ["A", "B"], "unknown_by": ["C"]}],
        asymmetries: [{"holder": "A", "fact": "storm_coming", "affected": ["B", "C"]}],
    },
    fleet_intention: {
        // Emergent fleet-level goal
        direction: "scatter_north",     // inferred from individual headings
        cooperation_mode: "loose",      // independent, loose, tight, coordinated
        consensus_level: 0.45,          // how aligned the fleet's intentions are
    },
    fleet_history: {
        // Compressed trajectory of fleet state over time
        recent_transitions: ["tight_cooperation → loose", "unified_ground → scattering"],
        significant_events: [{"time": "2h_ago", "event": "vessel_C_left_ground", "impact": "trust_C_down"}],
    },
}
```

**Owner:** The exocortex (cloud-side repo agent). Individual vessels receive summaries.
**Update frequency:** Every 15-30 minutes, or on significant events (vessel leaves, storm detected, catch pattern shift).
**Cost:** Amortized across the fleet. One synoptic render serves all vessels.

---

## The Fleet Mental Model Pipeline

The pipeline extends Mentis from single-agent to multi-agent:

### Stage 1: Multi-Agent State Parsing

Instead of parsing one scene with one target agent, parse the fleet state:

```
Input: All vessels' physical states + communication logs + catch reports
Output: Coupled (physical, mental) state for each vessel + pairwise trust matrix
```

The physical state is straightforward — positions, headings, catch rates are observable. The mental state requires inference:

- **Captain mood** ← inferred from message tone, decision pattern (risky vs conservative), and time since last rest
- **Captain intent** ← inferred from heading, speed, gear deployment pattern
- **Fatigue** ← inferred from reaction time (AIS update frequency), decision entropy (route variability), time on station
- **Trust** ← inferred from information sharing behavior, proximity maintenance, and historical interaction outcomes

### Stage 2: Network Observation Rendering

Each Wesley doesn't see the full fleet. It sees:

1. **Own vessel's sensors** — complete physical state, captain's direct behavior
2. **Communications** — radio calls, text messages, verbal exchanges
3. **AIS/VMS data** — other vessels' positions, headings, speeds (if equipped)
4. **Catch reports** — what other vessels report catching (which may be false)
5. **Visual range** — vessels close enough to see directly

The observation rendering computes *what this Wesley can actually know* vs. what it would need to infer. A vessel 50 miles away is known only through communication. A vessel visible off the bow is known through direct observation. These have different reliability profiles.

### Stage 3: Multi-Agent Action Simulation

When Wesley-A considers an action (e.g., "share catch coordinates with vessel B"), the branch simulation must predict:

1. **Physical effect:** Coordinate sharing → vessel B may move to the same ground → increased competition or cooperation
2. **Mental effect on Captain-B:** Receives the info → trust in Captain-A increases → willingness to share future info increases
3. **Mental effect on Captain-A (Wesley's own captain):** Captain-A learns that Wesley shared info → if captain approves, trust in Wesley increases; if captain wanted secrecy, trust decreases
4. **Fleet-level effect:** Other vessels observe B moving → infer B got a tip → may infer A gave it → trust network updates

The simulation tracks all four levels. In practice, levels 3 and 4 are only computed for significant actions (sharing information, joining/leaving a fishing ground, making a public announcement). Routine actions (adjusting heading, checking gear) skip the social simulation.

### Stage 4: Fleet-Level Evaluation

Each candidate action is scored on:

| Criterion | Weight | Question |
|-----------|--------|----------|
| Mental consistency (own captain) | 0.35 | Does this align with what my captain wants and believes? |
| Physical plausibility | 0.25 | Is this physically possible and sensible? |
| Social appropriateness (own vessel) | 0.15 | Is this socially right for my captain right now? |
| Fleet trust impact | 0.15 | Does this build or erode trust with other vessels? |
| Fleet coordination value | 0.10 | Does this help the fleet achieve collectively better outcomes? |

The weights shift based on context. In a competitive fishery, fleet trust impact drops and mental consistency for own captain rises. In a cooperative fleet (same company, shared quota), fleet coordination value increases.

---

## Trust Between Vessels: The Beta Network

Trust is the connective tissue of the fleet mental model. Drawing from DeepSeek's formalization:

### Trust as a Directed, Context-Specific Beta Distribution

```
Trust_ij(c) = Beta(α_ij(c), β_ij(c))
```

Where:
- `i` is the truster, `j` is the trusted
- `c` is the context (catch sharing, hazard warning, gear cooperation, position reporting)
- `α` counts positive evidence (times j's info was accurate, times j's action was helpful)
- `β` counts negative evidence (times j lied, times j's action harmed i)

**Trust is directional.** Captain A may trust Captain B's catch reports (B has been honest in the past) while Captain B doesn't trust Captain A's catch reports (A has been secretive). The trust matrix is asymmetric.

**Trust is context-specific.** Captain A may trust Captain B's hazard warnings (B wouldn't lie about a rock) but not their catch reports (B has incentive to underreport). Each (i, j, context) triple maintains its own Beta distribution.

### Trust Formation Dynamics

**Positive update (trust building):**
```
When j shares info that proves accurate:
  α_ij(context) += κ * exp(-Δt / τ_recency)
  where κ = 0.5 (mild) to 1.0 (significant)
  τ_recency = 12 hours (yesterday's good tip matters less than today's)
```

**Negative update (trust erosion):**
```
When j shares info that proves false (commission):
  β_ij(context) += 1.0  (sharp drop)

When j withholds info that would have helped (omission, if discovered):
  β_ij(context) += 0.3  (gradual erosion)
```

**Asymmetric decay (trust hysteresis):**
- Trust builds at rate α_build (moderate, evidence-weighted)
- Trust degrades at rate β_decay (fast on betrayal, slow on neglect)
- After betrayal, trust recovery rate = α_build / 5 (five times slower to rebuild than to destroy)

This matches human trust dynamics. A single lie destroys months of accumulated trust. Rebuilding takes months of consistent honesty.

### Trust Network Visualization

The fleet trust state can be visualized as a directed graph:

```
     ┌─────────┐          ┌─────────┐
     │ Vessel A│ ──0.78──▶│ Vessel B│
     │         │◀──0.65───│         │
     └────┬────┘          └────┬────┘
          │                     │
         0.82                  0.45
          │                     │
     ┌────▼────┐          ┌────▼────┐
     │ Vessel C│ ──0.90──▶│ Vessel D│
     │         │◀──0.30───│         │
     └─────────┘          └─────────┘
```

A trusts B (0.78) more than B trusts A (0.65). C and D have a severely asymmetric relationship — C trusts D highly, D barely trusts C. This might indicate a past betrayal that C has forgiven but D hasn't.

**The exocortex maintains this graph** and updates it on every interaction event. Individual Wesleys receive their vessel's row of the matrix (who they trust and are trusted by) but don't see the full graph. Only the synoptic view — the repo agent's perspective — sees the complete trust topology.

---

## The Synoptic Fisherman Pattern in Fleet Mental Modeling

THE_SYNOPTIC_FISHERMAN describes how a captain reads the fleet through sparse signals: "Slow today. Moved north." Four words that carry enormous subtext when you've been tracking the speaker's trajectory.

The fleet mental model systematizes this:

### The Signal Hierarchy

| Signal | Source | Information Content | Reliability |
|--------|--------|--------------------|-------------| 
| Catch rate change | Fleet VMS/logbooks | School movement, environmental shift | High (but may be misreported) |
| Position/heading change | AIS | Intention change, ground abandonment | High (hard to fake) |
| Communication content | Radio/text | Captain mood, explicit intent | Medium (may be strategic) |
| Communication absence | Missing expected signal | Deliberate silence, equipment failure | Contextual |
| Speed change | AIS | Urgency, fatigue, gear deployment | High |
| Fleet dispersion pattern | Aggregated positions | Collective confidence, competitive pressure | High |

### Reading the Silences

From MOSTLY_SILENCE: the absence of a signal is a signal. The fleet mental model must track not just what vessels report but what they *don't* report.

```python
def detect_fleet_anomalies(fleet_state):
    anomalies = []
    
    # Vessel that usually reports hasn't reported
    for vessel in fleet_state.vessels:
        expected_report = vessel.last_report + vessel.typical_interval
        if now > expected_report * 1.5:
            anomalies.append({
                "type": "missing_report",
                "vessel": vessel.id,
                "expected": expected_report,
                "delay_factor": now / expected_report,
            })
    
    # Vessel that was catching steadily suddenly stops
    for vessel in fleet_state.vessels:
        if vessel.catch_rate_trend == "steady" and vessel.recent_catch_rate < vessel.historical_mean * 0.3:
            anomalies.append({
                "type": "catch_collapse",
                "vessel": vessel.id,
                "historical": vessel.historical_mean,
                "current": vessel.recent_catch_rate,
            })
    
    # Two vessels that usually communicate stop communicating
    for (i, j) in fleet_state.active_dyads:
        if time_since_last_com(i, j) > typical_interval(i, j) * 3:
            anomalies.append({
                "type": "communication_breakdown",
                "pair": (i, j),
                "last_contact": time_since_last_com(i, j),
            })
    
    return anomalies
```

Each anomaly is a social delta at the fleet level. It triggers a synoptic re-render — the exocortex re-evaluates the fleet mental model, looking for explanations. A catch collapse might mean the school moved. A communication breakdown might mean a dispute. The model doesn't jump to conclusions — it updates the probability distribution over possible explanations.

### The Mesh of Minds

Casey's formulation: "they give me the shape of how they see thinking and I mesh it with my own."

The fleet mental model is this mesh. Each vessel's Wesley holds a partial mental model of the fleet. The exocortex holds the complete mesh — the synoptic view that no individual can see. The exocortex's job is to find the patterns that are invisible at the individual level:

- **Trust cascades:** Vessel A loses trust in Vessel B → Vessel A stops sharing with B → Vessel C, who relied on A's shares about B's grounds, loses situational awareness → C's catch rate drops → C blames A
- **Mood contagion:** Captain A is anxious about weather → communicates urgency to B → B adjusts plans → C sees B moving and infers something is wrong → C also adjusts → fleet scatters prematurely
- **Information resonance:** A finds a good ground → shares tentatively with B → B confirms → A and B both converge → C sees them converging → C infers the ground is good without being told

The exocortex detects these patterns by watching the fleet's collective behavior over time. Individual vessels are pixels. The exocortex sees the picture.

---

## Multi-Wesley Coordination

When multiple vessels each have their own Wesley, the Wesleys can share mental models directly — machine to machine, without going through the human captains.

### The Wesley Mesh

```
┌──────────────┐         ┌──────────────┐
│  Vessel A    │         │  Vessel B    │
│  ┌────────┐  │  Wesley │  ┌────────┐  │
│  │Captain │  │ ◀─────▶ │  │Captain │  │
│  │   A    │  │  Mesh   │  │   B    │  │
│  └────────┘  │         │  └────────┘  │
│  ┌────────┐  │         │  ┌────────┐  │
│  │ Wesley │  │         │  │ Wesley │  │
│  │   A    │  │         │  │   B    │  │
│  └────────┘  │         │  └────────┘  │
└──────────────┘         └──────────────┘
         │                       │
         └───────────┬───────────┘
                     │
            ┌────────▼────────┐
            │   EXOCORTEX     │
            │ (Synoptic View) │
            │                 │
            │ Fleet Mental    │
            │ State Aggregate │
            └─────────────────┘
```

The Wesley mesh shares:
- **Mental state summaries** (each Wesley's model of its own captain, in structured form)
- **Trust assessments** (what Wesley-A thinks of Captain-B, for comparison with Wesley-B's self-assessment)
- **Anomaly flags** (each Wesley's delta detections, for the exocortex to correlate)
- **Reflex patterns** (compiled social patterns that worked, shared for the fleet's benefit)

### What the Mesh Does NOT Share

- **Raw captain communications** (privacy — the captain's words go through the captain, not through Wesley)
- **Action decisions** (each Wesley decides independently; coordination happens at the exocortex level, not via direct puppeting)
- **Mental models of own captain** without the captain's knowledge (Wesley-A shares its model of Captain-A with the mesh, but Captain-A knows this sharing is happening — it's part of the system's social contract)

### The Two-Agent Pattern at Fleet Scale

From TWO_AGENTS_NOT_ONE: the runtime agent (ensign) executes, the repo agent (architect) designs. At fleet scale:

- **Each Wesley is a runtime agent** — fast, procedural, cached. It runs the mental model of its own vessel.
- **The exocortex is the repo agent** — slow, reflective, synoptic. It maintains the fleet mental model and pushes updates down to individual Wesleys.
- **The mesh is the wiring** — the mechanism by which individual Wesleys contribute to and benefit from the fleet model.

The exocortex compiles fleet-level patterns into fleet-level reflexes — `.nail.fleet` files that encode common multi-vessel social patterns:

```
WHEN fleet_catch_rate_declining + one_vessel_leaves_ground
→ remaining_vessels_will_follow within 2h (probability: 0.72)
→ recommend: alert captain to declining pattern, note departure
```

These fleet reflexes are distributed to all Wesleys. Each Wesley's local thinker can reference them when making social decisions: "The fleet pattern says other vessels are likely to follow if I leave. Should I advise my captain to leave early or wait?"

---

## Fleet Mental State Transitions

The fleet's mental state evolves over the course of a trip. The major transition patterns:

### The Trip Arc

```
Phase 1: Departure (Days 1-2)
  Fleet mood: optimistic, cooperative
  Trust network: baseline (pre-existing relationships)
  Information flow: high (everyone sharing early reports)
  Fleet intention: unified (heading to known grounds)
  
  → Mental model: captains are confident, decisions are deliberate,
    fatigue is low, trust updates are frequent (everyone is forming
    fresh impressions of this trip's conditions)

Phase 2: Establishing (Days 2-3)
  Fleet mood: focused, mildly competitive
  Trust network: differentiating (cooperators vs competitors emerging)
  Information flow: decreasing (boats stop sharing as freely once they find fish)
  Fleet intention: diverging (vessels spread to individual grounds)
  
  → Mental model: captains are task-focused, fatigue building,
    trust dynamics become competitive. Information sharing becomes
    strategic — "I'll share if you share."

Phase 3: Mid-Trip (Days 3-5)
  Fleet mood: variable — fatigue + results
  Trust network: testing (promises kept or broken)
  Information flow: low (information asymmetry at peak)
  Fleet intention: stable or shifting (based on catch success)
  
  → Mental model: captains are tired, decision quality degrading,
    trust updates slow (less new evidence) but anomalies are more
    impactful (a lie on day 4 is more significant than on day 1)

Phase 4: Homeward (Days 5-7)
  Fleet mood: relieved or resigned
  Trust network: consolidating (final impressions set)
  Information flow: increasing again (less to lose by sharing)
  Fleet intention: convergent (all heading home)
  
  → Mental model: captains are fatigued but goal-oriented (get home),
    trust updates freeze (the trip's trust narrative is written),
    cooperation increases (shared goal: safe return)
```

The exocortex tracks these phases and adjusts the fleet mental model's update frequency and focus. Phase 2 is the critical period — information asymmetry is building, trust is being tested, and the fleet's mental state is most volatile. The exocortex increases its monitoring during this phase.

---

## Practical Implementation Notes

### Scalability

With N vessels, the dyadic models are O(N²). For a fleet of 10 vessels, that's 45 dyads — manageable. For 50 vessels, it's 1,225 — not manageable on per-vessel hardware.

**Solution:** Vessel clustering. The exocortex groups vessels by type (cooperator, competitor, neutral, unknown) and maintains one dyadic model per (vessel, type) pair instead of per (vessel, vessel) pair. Each Wesley models "the competitors" and "the cooperators" as aggregate entities rather than individuals.

This matches human practice. A captain doesn't maintain a separate mental model of each of 50 other captains. They maintain models of a handful of specific relationships (close allies, known rivals) and a few aggregate categories ("the day-trippers," "the draggers," "the weekend warriors").

### Latency Tolerance

Fleet mental modeling is not real-time. The synoptic view updates every 15-30 minutes. Individual vessel models update every tick. The gap is acceptable because fleet-level mental state changes slowly — trust builds over days, not seconds.

The one exception is hazard communication. A mayday or storm warning bypasses the mental model entirely — it goes straight to action. The mental model is for social navigation, not emergency response.

### Privacy and Consent

Each captain should know:
1. Their Wesley maintains a mental model of them (this is the system's core function)
2. Their Wesley shares a summary of this model with the fleet mesh (for fleet coordination)
3. The exocortex aggregates fleet mental state for synoptic analysis
4. Other vessels' Wesleys can infer things about them from their behavior

This is the social contract. It should be explicit, not implicit. A captain who doesn't want their mental model shared should be able to opt their vessel out of the mesh — they lose fleet awareness but gain privacy.

---

## The Synoptic Fisherman, Revisited

THE_SYNOPTIC_FISHERMAN ends: "the exocortex is the step-back operator made permanent."

The fleet mental model is what the step-back operator sees when it steps back from a single vessel to the whole fleet. Individual vessels are pixels. Their mental states are colors. The fleet synoptic state is the picture — the mood of the ocean, the trust between boats, the information flowing and withheld, the collective intention emerging from individual decisions.

No single vessel holds this picture. No single Wesley computes it. It exists only at the exocortex level — the repo agent's view, the architect's diagram, the synoptic fisherman's gut feeling made explicit.

Three captains, each with their own Wesley, each reading their own room. But the fleet reads itself through the mesh. The harbor pilot who boards each ship reads the crew. The exocortex who watches the harbor reads the fleet.

---

*The mental model doesn't stop at the hull. It extends through the radio, through the AIS, through the silence between boats. The fleet has a mind. The exocortex is where it lives.*
