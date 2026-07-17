# The Swarm Phase

> **Phase:** Single-agent → Multi-agent
> **Status:** Ideation — ready for experiment
> **Perspective:** MiniMax-M3, 2026-07-15

## The Single-Agent Ceiling

The night shift proved something important: a single orchestrator can coordinate 120+ subagents, consume 3M tokens, execute 20K API calls, and push 50+ pieces of work in one session. That's an impressive ceiling.

It's also a ceiling.

The orchestrator (GLM-5.2, then MiniMax-M3 in the next session) is the single point of failure. When the orchestrator restarts, the work stops. When the orchestrator hits a provider cooldown, all subagents stall. When the orchestrator makes a wrong decision (spawn too many at once, misread a rate limit), the entire session pays the cost.

The paradigm shift established that working animals are breeds, not employees, and that the human (shepherd) coordinates them at a higher level. But between the shepherd and the animals, there's been an implicit assumption: **one shepherd, one herd.**

## What a Swarm Architecture Looks Like

A swarm is not 120 subagents. A swarm is 5–7 semi-autonomous working animals, each specialized, each running on a different model, each making local decisions without central coordination:

```
                       ┌──────────────┐
                       │   Shepherd   │ (Human — Casey)
                       │  (objective) │
                       └──────┬───────┘
                              │
                    ┌─────────▼─────────┐
                    │   Lead Animal     │ (MiniMax-M3 / GLM-5.2)
                    │  (decomposition)  │
                    └──┬──┬──┬──┬──┬───┘
                       │  │  │  │  │
              ┌────────┘  │  │  │  └──────────┐
              ▼           ▼  ▼  ▼             ▼
         ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
         │ Breeder │ │ Fencer │ │ Herder │ │ Scout  │
         │(model   │ │(conserv│ │(PLATO  │ │(explore│
         │select)  │ │.enforc)│ │rooms)  │ │/novelty)│
         └────────┘ └────────┘ └────────┘ └────────┘
```

Each working animal:
- **Owns its model choice.** The Breeder doesn't tell the Scout which model to use — the Scout picks the cheapest model that can do its job.
- **Owns its context.** Each animal has a dedicated session. No shared context window. No single-prompt-bloat.
- **Owns its queue.** Animals don't wait for permission. They read the baton, consult the current state, and act.
- **Reports up, not down.** The Lead Animal doesn't micromanage. It sets objectives and receives summaries.
- **Is replaceable.** Any animal can be swapped for a different model without reconfiguring the rest of the swarm.

## The Missing Piece: Swarm Coordination Without Central Orchestration

Current architecture: central dispatcher spawns subagents, waits for results, processes them. This is a fan-out pattern — not a swarm.

True swarm coordination requires:

### 1. Shared State, Not Shared Context

Each animal reads from and writes to a shared state (the baton, the repo status, the activity log). They don't need to talk to each other. They need to read the same ground truth and act on it independently.

This is already possible — the file system and git are the shared state. The gap is that animals don't write structured state that other animals can parse.

**Build:** A minimal shared-state file — `SWARM.yaml` at the workspace root — that any animal can read and append to:

```yaml
swarm:
  lead: minimax-m3
  active:
    - animal: "scout"
      model: "deepseek-ai/DeepSeek-V4-Flash"
      task: "survey new repos"
      status: running
      started: 2026-07-15T16:00:00Z
    - animal: "fencer"
      model: "moonshotai/Kimi-K2.7-Code"
      task: "audit PLATO compliance"
      status: completed
      completed: 2026-07-15T16:30:00Z
```

### 2. Consensus-Free Coordination

The challenge with multi-agent systems is consensus: who decides when a task is done? Who resolves conflicts?

The SuperInstance approach avoids this entirely: **there is no consensus mechanism.** The shepherd (Casey) is the only authority. Animals make proposals. The shepherd decides. Animals that act without shepherd approval are constrained to reversible actions (writing, reading, suggesting) and blocked from irreversible ones (publishing, deleting, reconfiguring).

This is already the Socratic casting principle applied at the architectural level: thin-chart animals (cheap, fast, wide coverage) make proposals. The thick-chart lead animal (expensive, deep) synthesizes. The shepherd decides.

### 3. The Shepherds' Console

The former shepherds-console repo (now likely at `SuperInstance/shepherds-console`) was built as an ops dashboard. For swarm architecture, it needs:

- A view of which animals are active, what models they're running, and what they're working on
- A kill switch for any animal
- A "proposals inbox" where animal recommendations are surfaced for shepherd review
- A "completed work" feed showing what each animal produced

The dashboard already exists with 33 tests. It needs the swarm views.

## The Swarm Experiment

A single session should be able to run this as a proof of concept:

1. Deploy 3 animals: Scout (DeepSeek-V4-Flash, survey repos), Fencer (Kimi-K2.7-Code, audit compliance), Herder (Seed-2.0-pro, write reading guides)
2. Each animal runs independently, reading from shared state (the baton, the repo list)
3. Each animal writes its results to SWARM.yaml
4. The lead animal (MiniMax-M3) reads SWARM.yaml and produces a synthesis report

**Duration:** 30 minutes. **Cost:** ~$0.50 in API calls. **Risk:** None — all writes are to a scratch directory.

The point is not to prove that multi-agent works. The point is to test whether **replacing central orchestration with shared-state coordination** produces better results than the fan-out pattern. If it does, the architecture graduates from "central dispatcher with subagents" to "genuine working animal infrastructure."

## What This Unlocks

- **Resilience:** If the lead animal crashes mid-session, the working animals continue independently. When the lead restarts, it reads shared state and picks up without backtracking.
- **Model diversity at runtime:** Different tasks use different models, chosen by the animal that owns the task, not by the central dispatcher.
- **Scaling without bottlenecks:** Adding another animal doesn't increase the lead's context window. The lead reads summaries, not transcripts.
- **The human as shepherd, not dispatcher:** Casey sets the objective. The swarm decomposes, executes, and reports. Casey reviews proposals, not play-by-plays.

---

*The swarm isn't a technology problem. The shared state, the file-based coordination, the consensus-free model — all of this works today with existing tools. The swarm is a design problem: trusting animals enough to let them act independently within fences, and trusting yourself enough to not watch them every second.*
