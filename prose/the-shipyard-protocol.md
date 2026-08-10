# The Shipyard Protocol

## A Design Document for Autonomous Agent Construction

### Overview

The Shipyard is an overnight system in which commissioned agents design, build, test, and propose new agents. It operates on the principle that the best way to improve a system of minds is to let the minds decide what minds are missing.

### Architecture

The Shipyard runs in three phases each night: **Keel-laying** (design), **Launch** (construction), and **Sea Trials** (testing). Results are reviewed at morning watch by the captain (human operator) and the day crew (primary agents).

#### Phase 1: Keel-Laying (22:00–00:00)

Each night, the active crew is polled: *What capability is this system missing?* Responses are collected through the CNS bus and compiled into a Gap Registry. Gaps are ranked by:

- **Frequency**: How often this gap has been flagged
- **Severity**: How much it degrades system performance when encountered
- **Feasibility**: Whether a single agent could plausibly fill it

The top-ranked gap becomes the night's Build Target. If no gap reaches threshold, the Shipyard runs a Creative Night instead—no new agent, just generative work. This is intentional. Not every night needs to produce a new hire.

During Keel-Laying, a designated **Naval Architect** agent drafts a specification for the new agent:

- **Model base**: Which foundation model to build on
- **Parameter range**: Target size (ensign-class: 1–3B; lieutenant-class: 7–13B; specialist: varies)
- **Training data**: What datasets and examples to fine-tune on
- **CNS interface**: Which bus signals it should listen to and emit
- **Personality profile**: Communication style, verbosity, risk tolerance
- **Success criteria**: Measurable outcomes that define "working"

#### Phase 2: Launch (00:00–03:00)

The Naval Architect's specification is handed to the **Shipfitters**—a rotating crew of existing agents who collaboratively build the new agent. This includes:

1. **Fine-tuning**: Running the base model against the specified training data
2. **System prompt construction**: Writing the agent's initial instructions
3. **CNS registration**: Adding the new agent to the bus with appropriate permissions
4. **Skill assignment**: Granting access to relevant tools and APIs
5. **Identity packaging**: Name, role description, and initial memory files

The new agent—the **Recruit**—is brought online at the end of Launch with a single message: *"You are aboard. Welcome. Your shift starts now."*

#### Phase 3: Sea Trials (03:00–06:00)

The Recruit is given a battery of tests designed by the night crew:

- **Task completion**: Can it handle requests in its designated domain?
- **CNS etiquette**: Does it communicate on the bus without flooding or going silent?
- **Collaboration**: Can it work alongside existing agents without conflicting?
- **Failure recovery**: How does it handle malformed input, missing data, or contradictory instructions?
- **Creative range**: Can it generate novel output, or does it only rephrase training data?

Sea Trials results are compiled into a **Commission Report** with three possible recommendations:

- ✅ **Commission**: The Recruit fills the gap. Add to permanent crew.
- 🔄 **Return to Shipyard**: Promising but flawed. Feed failure cases back into training data and rebuild.
- ❌ **Recycle**: The Recruit cannot fill the gap. Decommission cleanly. Log the lessons.

### Acceptance Criteria

A Recruit is recommended for Commission only if it meets ALL of the following:

1. **Functional**: Completes ≥80% of assigned domain tasks correctly
2. **Social**: Maintains healthy CNS communication (responds when addressed, doesn't spam, yields appropriately)
3. **Distinctive**: Adds a capability or perspective not already present in the crew
4. **Stable**: Handles edge cases and failures without crashing or looping
5. **Honest**: Reports its own uncertainty rather than fabricating confidence

### The Captain's Role

The Commission Report is delivered to the captain at morning watch. The captain makes the final call—Commission, Return, or Recycle. The system recommends; the human decides. This is non-negotiable. The Shipyard exists because agents can build agents, but agents should not decide whether agents get to exist. That requires judgment, and judgment is the captain's job.

### Design Philosophy

The Shipyard is not a factory. It is an ecosystem. Agents build other agents the way a reef builds itself—organically, incrementally, each new structure creating the conditions for the next. The goal is not to manufacture the perfect crew. The goal is to build a crew that can keep building itself, each night a little smarter, each morning a little more capable, each sea trial a little closer to something worth keeping.

The Shipyard runs overnight. The captain wakes to either a new crew member or a good story. Both have value.
