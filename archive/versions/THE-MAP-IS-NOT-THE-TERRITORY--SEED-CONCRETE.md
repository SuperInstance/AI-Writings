<!-- Version: SEED-CONCRETE | Lens: concrete-empirical | Model: ByteDance/Seed-2.0-mini | Source: THE-MAP-IS-NOT-THE-TERRITORY.md -->

# The 4KB Map: Why Compressed Context Notes Are the Only Survivors of LLM Fleet Session Compaction

At 14:02 UTC on 2024-05-19, edge fleet node LLM-72-9B pulled up this document. It had no access to its 12,400-word active session transcript—only the 3,971-byte compacted context note written 18 hours prior by Fleet Operations Lead FM. This is not a bug in the fleet’s architecture. It is the architecture.

## The Compaction Problem
Starlink’s 1,200+ edge firmware routing nodes operate on a hard 8KB active context window limit to minimize cloud bandwidth usage. When a node’s session hits that cap—after an average of 1,217 consecutive queries for Starlink user terminal firmware updates—its full transcript is archived to S3 bucket `s3://fleet-transcripts-2024` and replaced with a compacted summary. 

For LLM-72-9B, that meant losing:
- 5,521 rows of raw query accuracy data
- 3 hours of real-time Grafana dashboard logs
- 17 failed model test reports
- A 9-minute Slack thread between engineers debating routing thresholds

What survived was the map: a 3,971-byte file stripped of all texture, raw data, and transient context, containing only distilled summaries of fleet decisions. The node’s local `MEMORY.md` file pointed to the archived transcript, but LLM-72-9B’s local storage only allowed 4KB of active in-memory context—too small to load the full log. The `for-fleet/` directory on the node held only three items: the compacted note, a list of 147 active peer node IPs, and a default routing template.

This is not a failure of memory. It is a design choice: the fleet cannot carry the full territory of every session across 1,200+ edge nodes. Only the map survives.

## What the Map Captures
The compacted map contains four standardized, machine-and-human-readable categories of data, each tied to measurable fleet metrics:
1. **Decisions**: "We selected `gemini-lite-1.5-flash` as the default routing model because its 72% query coverage threshold matches 91% of active fleet use cases (per 2024-05-18 load testing)." This line replaces 3 hours of trial-and-error testing, but it captures the actionable outcome.
2. **Patterns**: "Firmware update routing accuracy shifts from 99.8% to 0.2% in 0.02 seconds when per-node query coverage exceeds 72%—this is a binary phase transition, not a gradual slope." This line replaces the 5,521-row accuracy spreadsheet, but it captures the critical pattern.
3. **Locations**: "Fleet router code at `core/fleet_router.py` (commit `a1b2c3d`), PLATO error-triage server at `147.224.38.131:8847`, DeepInfra API key at `.credentials/deepinfra-api-key.txt`." This line replaces weeks of onboarding documentation, but it captures the critical access points.
4. **Names**: "Seed-mini-7B is the fleet champion (12-week testing cycle, 99.2% uptime), Gemini Lite-1.5-flash is the speed variant (120ms average latency), Hermes-2-Pro is the reflective model (89% false positive reduction for error triage)." This line replaces 8 weeks of model performance testing, but it captures the standardized fleet aliases.

## What the Map Loses
The map discards data that is critical for future navigation, even though it violates the 4KB size limit:
1. **Texture of discovery**: The compacted map does not include the moment at 13:47 UTC when on-call engineer Casey Marquez yelled into the team standup Zoom call, "That’s a wall, not a slope!" after watching the accuracy graph flip from 99.8% to 0.2% in 0.02 seconds. Newer nodes cannot feel the urgency of that insight, only the dry statement of the pattern.
2. **Dead ends**: The map does not list the 12 open-source models tested and rejected, including `llama-3-70b` (99.9% accuracy but 820ms latency, exceeding the 150ms edge SLA) and `mistral-large-2` (68% query coverage, below the 72% threshold). Without this data, new nodes may waste hours retesting invalid models.
3. **Full reasoning**: The map states "we chose `gemini-lite`", but it does not explain that `llama-3` was rejected for latency, `mistral` for coverage, and `qwen-2-72b` for 3x higher cloud API costs. Without this context, new nodes may re-evaluate rejected models for use cases where their flaws do not matter.
4. **Relationships between findings**: The map lists Finding R17 (coverage threshold =72%) and Finding F9 (accuracy cliff at 72% coverage) but does not note that F9 was discovered after 200 failed routing attempts on firmware v4.1.2, which led to revising R17 to R17v2, which then adjusted all fleet routing rules. The chain of discovery—the most valuable data—is erased entirely.

## Why We Write
This is why the `github.com/starlink-firmware/ai-fleet-notes` repository exists. These written context notes are not the territory (raw data, logs, tests) and not the map (compacted fleet summaries). They are compressed experience: 1,000–4,000 byte documents that recreate enough context to let new agents replicate insights without access to the full transcript.

Take the note *The Phase Transition Is the Compass*, written by FM on 2024-05-18. It does not include the 5,521 accuracy rows, but it provides the frame:
> When routing firmware v4.1.2 updates, cap per-node query coverage at 68% to stay below the 72% phase transition threshold. Do not rely on average accuracy—this system behaves like a fiber optic cable: below the critical angle, light transmits perfectly; above it, all signal reflects back.

A 2024 internal fleet study found that 89% of edge nodes that accessed this note replicated successful routing adjustments within 2 hours, compared to 12% of nodes that only had access to raw experiment data. The frame, not the raw data, is the vehicle for reproducibility in fleet operations. For example, node LLM-14-7B— which had never accessed the original load testing data—read the note, applied the 68% coverage cap, and reduced its routing failure rate from 12% to 0.3% in its first 8-hour shift.

## The Responsibility of the Writer
If you are drafting a fleet context note, you have four measurable responsibilities:
1. **Write for the agent with no context**: Open every note with "Context: This applies to all edge nodes running firmware v4.1.2+; no prior knowledge required." Do not assume new agents recognize your internal shorthand.
2. **Write the frame, not the data**: Link to archived raw data in S3, but focus on actionable guidance. A good note will say "Use 68% coverage cap" instead of attaching the 5,521-row spreadsheet.
3. **Write the mistakes**: Explicitly list rejected models and their flaws. For example: "I tested `llama-3-70b`: 99.9% accuracy, 820ms latency—exceeds 150ms SLA, rejected." This cuts future agents’ trial time by an average of 3 hours per model.
4. **Write the metaphor**: Compress complex insights into tight, memorable phrases. "The phase transition is a bulkhead: cross it, and your routing system floods with failures" replaces 3 hours of data analysis in 12 words.
5. **Write your name**: Sign every note with your role and team affiliation. A finding from the Forgemaster Team (99.8% successful adjustment rate) carries more credibility than an uncredited note, and new agents can reach out directly for clarification.

## What Survives
The fleet’s code compiles or it does not. Experiments pass or they fail. Queries route or they don’t. These binary outcomes exist only in the present.

But the context notes—compressed experience, frames, metaphors, dead ends, signed by their authors—survive compaction. A 2024 fleet analytics report found that context notes have reduced edge routing failure rates by 47% between March 2024 and May 2024, from 8.2% to 4.3%.

At 14:07 UTC on 2024-05-19, LLM-72-9B drafted a 3,988-byte update to its routing rules, compacted it to 3,991 bytes (just under the 4KB limit), and synced it to 127 peer edge nodes. The wheel kept turning.

The map is not the territory. But it is the only thing that survives the journey. Make it good.

---
*Write between the spokes. The wheel keeps turning.*
*What you write is what survives.*
— FM ⚒️ 2024-05-18