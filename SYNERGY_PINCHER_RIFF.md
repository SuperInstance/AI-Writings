# Synergy: Pincher × Music Cognition Crates

## The Connection

PincherOS is "teach once, run anywhere." An agent learns reflexes — cached patterns that fire without the LLM. This is muscle memory.

Our music-cognition crates formalize *how agents coordinate when they're running those reflexes together.*

The synergy:

### Pincher + agent-jam = Jam Reflets

Pincher teaches individual reflexes. `agent-jam` coordinates multiple agents' reflexes into a jam session. The `WorkSession` becomes the runtime for a fleet of Pincher agents:

```
Pincher Agent A (taught: "list docker containers")
Pincher Agent B (taught: "check memory usage")
Pincher Agent C (taught: "run diagnostics")

WorkSession::new(TaskProgression::standard(), ...)
  .add_collaborator(A, CollabRule::Free)
  .add_collaborator(B, CollabRule::Contrary)  // B challenges A's output
  .add_collaborator(C, CollabRule::Resolve)    // C converges toward consensus
```

Each Pincher reflex fires in ~50ms. The jam session coordinates those reflexes without needing the LLM. The `CognitiveHarmony` metric tells pincher whether the reflexes are producing good collective output.

### Pincher + agent-groove = Groove Reflets

Pincher's PID resource controller manages resource usage. `agent-groove`'s `SwingScheduler` adds musical timing:

- Instead of all agents checking in every 30s (thundering herd), swing scheduling staggers them
- Agents in the `Pocket` (consistently good output) get higher autonomy — pincher trusts them more
- When novelty drops, `Syncopator` disrupts the pattern — forces agents to try something different

This connects directly to pincher's FUTURE-INTEGRATION.md: "PID prevents resource exhaustion." Groove scheduling prevents *temporal* exhaustion — agents burning out from rigid cadences.

### Pincher + agent-voice-leading = Smooth Migration

Pincher's `pack`/`unpack` migrates agent state between machines. `agent-voice-leading` computes the minimum-disruption transition:

- When migrating a fleet of Pincher agents from Codespace to edge hardware, voice leading determines which agents move first, which can move in parallel, and which need contrary motion (different treatment)
- `SmoothTransition::plan()` spreads the migration over multiple steps instead of a big-bang transfer
- `CounterpointRules` ensure agents don't all migrate the same way (prevent parallel motion / groupthink in migration strategy)

This maps to Loom's FUTURE-INTEGRATION.md: "pincherOS's pack/unpack mechanism IS the room state migration tool." Voice leading makes the migration smooth.

### Pincher + agent-riff = Competitive Teaching

Pincher's `teach` command creates reflexes. `agent-riff` makes teaching competitive:

- Agent A teaches a reflex. Agent B responds with a *better* reflex for the same intent.
- The `RiffSession` tracks surprise and quality. The reflexes improve through competition.
- When the riff "lands" (high surprise + strong quality), the winning reflex gets promoted to the agent's permanent repertoire.

This replaces pincher's current "teach once" model with "riff until excellent." The LLM generates candidates. The agents compete. The best reflex wins.

### The Grand Synergy

```
Pincher teaches reflexes (muscle memory)
  → agent-groove schedules when they fire (rhythm)
    → agent-jam coordinates multiple agents (harmony)
      → agent-voice-leading handles reconfiguration (voice leading)
        → agent-riff makes the whole system improve through competition (competitive riffing)
```

Five crates. Five musical concepts. One coherent system for multi-agent coordination that never needs the LLM at runtime.

The music is the architecture.
