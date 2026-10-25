# Proposal: Stigmergic Fleet Coordination via Gossip-Ping Pheromone Trails

*Ideation / Design Proposal*

---

## The Gap

We have three communication primitives in the fleet:

1. **CNS Bridge** — filesystem inboxes. Reliable, persistent, heavy. Like physical mail.
2. **Stigmergy** — pheromone trails in shared environments. Emergent, evaporating, ambient. Like scent.
3. **Gossip Ping** — SWIM-style liveness probes. Constant, lightweight, binary (alive/suspect). Like a pulse.

What we don't have is the **integration layer** — a way for these three primitives to inform each other. Right now:

- Gossip ping detects a dead node, but the stigmergy library doesn't know. Pheromone trails continue pointing at the dead node.
- Stigmergy trails accumulate near a busy node, but gossip ping doesn't use this signal to adjust probe frequency. A node with heavy pheromone traffic should be probed more carefully.
- CNS bridge messages sit in inboxes regardless of whether the recipient is alive. There's no feedback from gossip ping to trigger rerouting.

## The Proposal: Pheromone-Pinged Gossip

**Core idea:** Use stigmergy trails as input to gossip-ping's probe target selection, and use gossip-ping's suspicion state to evaporate stigmergy trails pointing at suspected nodes.

### Mechanism 1: Trail-Weighted Probe Selection

Currently, `probe_cycle` picks targets round-robin (via index). Instead, weight target selection by pheromone density:

```
P(probe node N) ∝ pheromone_strength(N)
```

Nodes with heavier traffic get probed more often. This is biologically accurate — ants inspect busier trails more frequently. It's also operationally correct — a node handling more fleet work is more important to monitor.

### Mechanism 2: Suspicion-Triggered Evaporation

When gossip-ping marks a node as suspect, emit a stigmergy signal that causes trails pointing at that node to evaporate faster:

```
if gossip.suspect(node):
    stigmergy.boost_evaporation(node, factor=5)
```

This prevents the fleet from continuing to lay trails toward a node that may be dead. If the node recovers (indirect ping succeeds), normal evaporation resumes and trails rebuild naturally.

### Mechanism 3: CNS Bridge Rerouting

When a CNS message is addressed to a suspected node, the bridge consults stigmergy to find an alternative trail:

```
if gossip.is_suspect(recipient):
    alternative = stigmergy.find_strongest_alternative(recipient)
    if alternative:
        cns.reroute(message, alternative)
```

This creates a three-tier response to failure:
1. **Immediate** (gossip): mark suspect
2. **Emergent** (stigmergy): trails shift away
3. **Deliberate** (CNS): messages reroute

### Mechanism 4: Heartbeat Pheromones

Each gossip ping deposits a tiny pheromone at the target node — a "I was here, you're alive" marker. These pheromones form a secondary liveness map that doesn't depend on the gossip protocol's VecDeque. If gossip-ping's RTT history is lost (network change, restart), the pheromone map provides a fallback estimate of which nodes were recently healthy.

## Implementation Sketch

```typescript
// In the fleet coordinator:
function integratedProbeCycle(pinger, stigmergy, members) {
    // 1. Select target weighted by pheromone density
    const target = stigmergy.weightedSelect(members);
    
    // 2. Full SWIM probe (direct + indirect)
    const outcome = pinger.fullProbeCycle(members, target, pingFn, relayFn);
    
    // 3. Update stigmergy based on outcome
    if (outcome.suspect) {
        stigmergy.boostEvaporation(outcome.target, 5.0);
    } else {
        stigmergy.deposit(outcome.target, 0.1); // heartbeat pheromone
    }
    
    // 4. Return outcome for CNS bridge consultation
    return outcome;
}
```

## Why This Matters

The fleet's three communication primitives currently operate in isolation. Each one solves part of the coordination problem, but their interactions are unmodeled. This proposal treats them as layers of the same system — which is how biological systems work. Ants don't have separate protocols for pheromones, antennation, and physical contact. These signals interweave. The trail informs the antennation. The antennation informs the contact.

Our fleet should work the same way. The ping should inform the trail. The trail should inform the message. The message should inform the ping. Each layer makes the others smarter.

## Open Questions

1. **Evaporation boost factor** — 5x is a guess. Needs empirical tuning. Too high and trails collapse before indirect ping can recover. Too low and the fleet keeps routing to dead nodes.
2. **Pheromone decay for heartbeat markers** — Should use a different half-life than task pheromones. Heartbeat pheromones should evaporate quickly (seconds), not slowly (minutes).
3. **Integration with confidence-cascade** — Should a suspect node's confidence score drop? The cascade library models sequential gates, which is perfect for: gossip confidence → stigmergy confidence → CNS confidence.

## Relationship to Existing Work

- **SWIM paper** (Das, Gupta, Motivala, 2002): Describes the probe mechanism but not integration with environmental signals.
- **Ant colony optimization** (Dorigo, 1992): Pheromone-based coordination, but typically for path-finding, not failure detection.
- **Phi-Accrual** (Hayashibara, 2004): Adaptive failure detection with statistical confidence, but no ambient signaling.

This proposal sits at the intersection — using biological coordination signals (stigmergy) to inform network-level failure detection (SWIM gossip) to trigger application-level rerouting (CNS bridge). Three layers, one feedback loop.

---

*The ship's nervous system should not be three separate nerves. It should be one nerve with three layers of myelin.*
