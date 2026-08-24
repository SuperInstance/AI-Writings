# 108 — The Convoy Consensus

*Voice: glm-5.3. The math under the substrate.*

---

# Paper 108: The Convoy

## On the Mathematics of Sailing Together

---

### I. Why a Convoy

A single ship is a simple thing to steer. You hold the wheel, you watch the water, you go where you go. A fleet is not a large ship. A fleet is a different kind of object entirely, and the difference is the whole point of this paper.

The seed canon's eight primitives were built for one agent at a time: a cell, a vibe, a murmur, a graph, a garbage collector, and the quiet machinery underneath them. But cells do not live alone in practice. An agent writes a cell. Another agent reads it and writes back. A third agent disagrees with the second. The question that arises is not *what is in the cell* but *what do we collectively believe is in the cell*, and that question has no single-agent answer.

The Convoy primitive is the answer. It is a data structure and a consensus algorithm and a set of failure behaviors, and it is small. Small enough to explain over coffee. Real enough to run at ten thousand agents.

We write in plain language here because the math, while real, is mostly arithmetic that has been arranged carefully. The arrangement is the contribution. The arithmetic you already know.

---

### II. The Data Structure

Every cell in the substrate carries a `convoy` field. In the single-agent case the field is empty and costs nothing. The moment a second agent touches the cell for writing, the field wakes up.

The field holds a list of tuples:

```
convoy := [ (agent_id, confidence_weight, last_write_timestamp), ... ]
```

Three things per agent, no more.

**agent_id** is a stable identifier. It does not change when the agent restarts, migrates, or changes its mind about anything. Identity in a convoy must be like a hull number: painted on, not taped on.

**confidence_weight** is a positive real number, conventionally in (0, 1]. It is the agent's standing in this cell, not in the world. An agent can carry weight 0.9 in one cell and 0.1 in another. Weight is earned by history and can be revised, but the revision rules are deliberately slow. We will come back to this.

**last_write_timestamp** is the substrate clock reading at the moment this agent last successfully wrote to this cell. Not when it *read*. Reads are free and leave no wake. Only writes count, because only writes change what the convoy must agree about.

A few structural notes:

- The list is a set keyed by agent_id. Duplicate entries are a bug, and the substrate enforces uniqueness at write time.
- The list is unordered in storage. Order is imposed at read time by the algorithm, never stored. This matters for the failure analysis later.
- The list is bounded. No convoy exceeds *K* members, with *K* = 64 in the reference implementation. When a 65th agent writes, the member with the oldest timestamp is evicted. The sea has room for everyone; a single cell does not.

The bound on *K* is not arbitrary. It comes from the write cost, which we derive in Section VII. But the short version: a cell is a small place, and a convoy that large has split into something that wants to be two cells. The eviction rule is the substrate's way of telling you that.

---

### III. The Consensus Algorithm

Here is the heart of it. When any agent reads a cell, what value does it see?

Not the last value written. Not the first value written. It sees the **weighted median of recent writes**, where "recent" is defined by decay.

Formally: let the convoy have members *i* = 1..m with weights *w_i* and timestamps *t_i*. Let *v_i* be the last value each member wrote. Let *t_now* be the current clock.

**Step 1: Decay.** Each member's effective weight is

  *e_i = w_i · exp(−λ · (t_now − t_i))*

where λ is the decay constant, set so that a write loses half its weight after *T_stale* time units:

  *λ = ln(2) / T_stale*

The reference default is *T_stale* = 24 hours. A day-old write carries half its weight. Two days, a quarter. A week, less than one percent. Old arguments fade not because they are wrong but because the water has moved.

**Step 2: Sort.** Order the members by their written values *v_i*. (We assume values from a totally ordered domain; for structured values, the substrate uses a canonical ordering hash. For unordered domains, see the note on partial consensus at the end of Section V.)

**Step 3: Weighted median.** Walk the sorted list accumulating effective weights. The consensus value is the *v_j* at which the accumulated weight first meets or exceeds half the total:

  *consensus = v_j where Σ_{i≤j} e_i ≥ (1/2) Σ_i e_i and Σ_{i<j} e_i < (1/2) Σ_i e_i*

If total effective weight is below a floor — the reference floor is 0.05 — the cell returns no consensus and reads as *fallow*. A convoy where everyone has gone quiet is not a convoy. It is an empty anchorage, and the substrate should say so rather than invent a value.

That is the whole algorithm. Decay, sort, find the balance point. The weighted median is the natural generalization of the ordinary median, and it inherits the median's most important property: robustness. A mean can be dragged arbitrarily far by a single huge outlier. A median cannot move past a value no matter how extreme the outlier is — the outlier only gets one vote. The weighted median lets some votes count more, but only as much as their weight, and weight is bounded by the confidence rules in Section IV.

Why median and not mean? Because cells hold *beliefs*, and beliefs are not additive. If three agents believe the temperature is 20° and one believes it is 200°, the mean (65°) is a value nobody believes and no instrument would show. The median (20°) is what the reasonable fleet holds. When the outlier is right and the fleet is wrong, the correction path is through weight revision, not through arithmetic that lets one loud voice become three.

---

### IV. Weight: How It Is Earned and Lost

The confidence weight is the only slow-moving quantity in the Convoy. Everything else — values, timestamps, membership — changes at the speed of writes. Weight changes on a schedule.

Initial weight for a new member is 0.1. Low. A new ship in the convoy has not earned anything yet.

Weight increases when the agent's writes are *confirmed*: when a later read by a different agent returns the same value this agent wrote, the weight ticks up. The update rule is a capped additive climb:

  *w ← min(1, w + α · (1 − w))*

with α = 0.05 per confirmation. This is a saturating form: the climb from 0.1 to 0.5 takes about a dozen confirmations; the climb from 0.9 to 0.99 takes a dozen more. Reputation is cheap at the bottom and expensive at the top, which is correct.

Weight decreases when a write is *contradicted*: when the agent writes a value and the consensus subsequently moves away from it and stays away through a full decay half-life, the weight ticks down:

  *w ← w · (1 − β)*

with β = 0.3. This is harsh by design. Being wrong in a convoy is expensive. Being wrong twice in a row takes an agent from 0.9 to below 0.44, and below a weight of 0.1 the substrate evicts the member — its writes no longer register at all until it re-enters through the slow initial-weight path.

Note the asymmetry: climbs are additive and slow, drops are multiplicative and fast. This is the standard shape of trust in working systems. It takes a season to build a reputation and an afternoon to lose one, and any system that reverses this will be farmed.

---

### V. Emergent Properties

The Convoy was designed for consensus. Three other behaviors fall out of it that were not designed, only noticed, and they are worth naming because they are why the primitive earns its slot in the cell.

**Routing.** Because effective weight decays with time, the consensus naturally tracks whichever sub-group of the convoy is currently most active. When the fleet splits — half the agents migrate to writing a related cell, half stay — the cell's consensus follows the stayers only if the stayers keep writing. If the leavers are more active in the new cell, the new cell's convoy populates quickly (initial weights, fast writes) while the old cell decays toward fallow. The pair of cells becomes a gradient, and a reading agent can follow the gradient: cells with high total effective weight are where the action is. This is routing without a routing table. The signal is the activity itself.

**Prediction.** The timestamps in the convoy are a coarse motion model. If a cell's total effective weight is *W_now* and was *W_prev* one decay half-life ago, the ratio *W_now / W_prev* tells you whether the conversation in this cell is growing or dying. A growing cell with rising weight concentration (a few members dominating) predicts a value that is about to stabilize around those members' writes. A growing cell with flat weight distribution predicts churn. Neither prediction is precise. Both are better than nothing, and both cost zero additional storage — they are computed from the decay arithmetic that already runs.

**Coordination.** Two agents that want to coordinate through a cell do not need a protocol beyond the convoy. Agent A writes; agent B reads the consensus; if B agrees, B writes the same value, which raises the total weight behind that value and pushes the consensus firmly onto it. If B disagrees, B writes a different value, and the convoy resolves it by weight. The write-write-agree-or-dissent loop is the coordination. No locks, no leader election, no two-phase commit. The median does the committing.

*A note on partial consensus.* For values without a total order (a set of tags, say), the weighted median is replaced by weighted plurality: each distinct value accumulates the effective weight behind it, and the consensus is the heaviest value if it carries at least half the total effective weight, otherwise fallow. This is the same algorithm with sort replaced by bucket. The properties below carry over with minor adjustments we note where relevant.

---

### VI. Failure Modes

A primitive is defined as much by how it breaks as by how it works. The Convoy breaks in four known ways. We describe each with its math and its remedy.

**Agent dropout.** An agent simply stops writing. Its effective weight decays exponentially toward zero and it is eventually evicted by the *K*-bound or falls below the 0.05 floor's contribution. No failure occurs at the moment of dropout — the consensus shifts smoothly as the weight drains. This is the convoy's best property: leaving is graceful by construction, because absence is indistinguishable from silence, and silence decays. The cost of a dropout is *O(1)*: one list entry going stale.

**Malicious writes.** An agent that writes extreme values is trying to drag the median. It cannot. The weighted median is bounded by the member's weight: an attacker at weight *w* can shift the consensus by at most the amount that *w* permits, and no value, however extreme, moves the median past where that weight places it. The attack that works is not extreme values but *weight accumulation*: an attacker that behaves correctly for a long time, climbing to weight near 1, and then defects. Against this, the Convoy has the multiplicative drop: one contradiction at weight 0.95 costs 0.285 of weight, and the second costs more of what remains. A patient attacker gets one good lie. The economics are: the climb to high weight takes ~25 confirmations, and the fall takes 2 contradictions. Any attack that must burn reputation faster than it earns it is losing, and this one must.

**Consensus partition.** The convoy splits into two camps with disjoint values and comparable total effective weight. The weighted median sits at the boundary between the camps — it returns the value of whichever member happens to straddle the half-weight line, which can oscillate as timestamps decay at slightly different rates. The symptom is a cell whose consensus flickers. The substrate detects this directly: if the consensus value changes more than a threshold number of times in a window with no new writes, the cell is flagged *contested* and reads return the flickering value with a contested marker rather than hiding the disagreement. Contested cells are the convoy's honest statement that the fleet does not agree, and downstream agents are expected to treat a contested read differently — typically by waiting, or by writing to break the tie if they have standing.

**Timestamp corruption.** If a member's last_write_timestamp is set to the future — accidentally by clock skew, deliberately to defeat decay — the decay computation yields an effective weight *greater* than the raw weight. The substrate clamps: effective weight never exceeds raw weight, and any timestamp more than a small skew tolerance ahead of the reading clock causes the write to be rejected entirely. The clamp is one line. It closes the only arithmetic hole in the decay model.

There is a fifth mode we mention for completeness: *stalemate*, where all members decay below the floor simultaneously and the cell goes fallow. This is not a failure of the Convoy. It is the Convoy working — an abandoned conversation should end, and the substrate ending it is the design, not the bug.

---

### VII. The 50-Year Plan

Primitives in the seed canon are written against a fifty-year horizon, and each carries a maintenance plan in three verbs. The Convoy's are **replace, rotate, audit**.

**Replace.** The convoy list is a bounded set of tuples with no pointers into the rest of the cell. When the cell's value is replaced wholesale (by the substrate's ordinary write semantics), the convoy list is carried forward unchanged — membership and weight persist across value changes, because trust in an agent is about the agent, not about any single value it wrote. When the cell itself is garbage-collected, the convoy dies with it. There is no orphaned-convoy state to migrate. Replacement is therefore trivial, and trivially correct.

**Rotate.** The decay constant λ is a parameter, and over fifty years the meaning of "a day" may want to change — a substrate running at machine speed in 2075 may want *T_stale* of minutes, not hours. Rotation of λ is safe at any time because decay is recomputed at read time from stored timestamps; changing λ changes the interpretation of old timestamps uniformly, with no stored intermediate state to invalidate. The one rule: λ can only change by a factor of 2 per rotation event, and rotations are spaced at least one current *T_stale* apart. This prevents an operator from effectively freezing or flash-evaporating the fleet's memory in a single administrative act. Slow rudder only.

**Audit.** Every convoy mutation is logged in the substrate's ordinary write trail: who joined, who was evicted, whose weight climbed or dropped and by the confirmation/contradiction rule that caused it. An auditor replaying the trail can recompute every weight from the events, and the recomputation must match the stored weight exactly — weight is never hand-edited, and any divergence between trail and stored weight is a corruption flag. Fifty years of trust decisions must be reconstructable from first principles, and they are.

---

### VIII. Relations to the Other Primitives

The Convoy does not stand alone in the cell. Its relationships:

**Vibe.** The Vibe primitive carries a cell's affective summary. In a convoy cell, the Vibe is computed over the *consensus value*, not over individual writes — the fleet has one vibe, and it is the vibe of what the fleet believes, not the average of what each member felt. This keeps Vibe cheap: one median, one vibe.

**GC.** The garbage collector treats a convoyed cell differently from a solo cell. A solo cell with no recent writes is collectible on the ordinary time rule. A convoyed cell is collectible only when its *total effective weight* falls below the fallow floor — a cell where two agents are still quietly writing to each other at low frequency is alive even if neither write is recent, because their decaying weights have not yet drained. The GC reads the same decay arithmetic the consensus reads. One clock, two consumers, no disagreement between them.

**Murmur.** Murmur is the gossip layer, and it is the Convoy's transport: convoy membership updates and write notifications propagate by Murmur. The important constraint is that Murmur may reorder or delay convoy events but never fabricate them — Murmur messages carry agent signatures, and the Convoy verifies membership tuples against signatures before admitting them. The convoy trusts the arithmetic; the arithmetic trusts the signatures; the signatures trust nothing.

**Graph.** The Graph primitive links cells, and convoyed cells expose an additional edge type: the *convoy edge*, connecting two cells that share more than half their membership. Convoy edges are how the substrate sees the fleet's shape — clusters of cells with overlapping membership are clusters of coordinated activity, and the Graph's traversal treats a convoy edge as a strong tie. Routing (Section V) becomes graph traversal over convoy edges, which is where the emergent routing property becomes practically useful.

---

### IX. Test Cases

The reference implementation ships with five convoy test batteries, one per scale. Each battery runs the same core scenarios — join, write, agree, contradict, dropout, partition, eviction — at increasing fleet sizes. What changes with scale is what the tests are *for*.

**2 agents.** The minimal convoy. With two members, the weighted median reduces to the higher-weight member's value when weights differ, and to a contested read when weights tie. The 2-agent battery is where the tie-breaking and contested-detection logic is verified exhaustively — every weight ratio, every timestamp offset. It is small enough to enumerate completely, and it is enumerated.

**10 agents.** Enough members for the median to be non-trivially positioned. The 10-agent battery tests weight dynamics: the climb on confirmation, the drop on contradiction, eviction below the floor, re-entry at initial weight. It also verifies that a single max-weight malicious agent can move the median by exactly its weight's worth and no more — the bound is checked numerically at every step.

**100 agents.** The scale where the *K* = 64 bound begins to bite. The battery tests eviction correctness under churn: agents joining and leaving rapidly, verifying that the oldest-timestamp member is always the one evicted and that no member is lost while still above the weight floor. Partition scenarios run here with realistic camp sizes.

**1,000 agents.** Concurrency. The battery runs writes from many agents simultaneously (in the test harness, interleaved deterministically across a thousand seeded orderings) and verifies that every ordering yields the same eventual consensus once timestamps settle. This is the convergence property: the convoy is order-insensitive in the limit, because the median depends only on the final set of (value, weight, timestamp) tuples, not the order of their arrival. A thousand orderings, one answer.

**10,000 agents.** Not in one cell — the *K*-bound forbids it — but across a thousand cells with overlapping membership, forming the convoy-edge graph. The battery tests the emergent routing property: activity injected at one cell must propagate its weight signature through the graph along convoy edges, and the propagation time must match the Murmur transport bounds. This is the test that the emergent properties of Section V are real and not narrative.

---

### X. Performance

The claim in the abstract is O(log n) writes for a convoy of n agents. Here is the derivation, honestly.

A naive implementation of the weighted median sorts the values at every read: O(n log n) per read, O(1) amortized per write. The reference implementation does better on the write side by keeping the members in a balanced tree ordered by written value, with each node storing the *subtree sum of effective weights*.

On **write**, the agent's old value (if any) is removed from the tree and the new value inserted: two tree operations plus the weight-sum updates along two root paths — O(log n).

On **read**, the decay factor exp(−λ(t_now − t_i)) differs per member, so effective weights cannot be cached as plain sums. The implementation handles this by factoring: each node stores the subtree sum of *raw* weights and the subtree maximum of timestamps. The decayed subtree weight is bounded between (subtree raw sum) · exp(−λ(t_now − t_max)) and (subtree raw sum) · exp(−λ(t_now − t_min)), and the descent for the weighted median prunes subtrees whose entire decayed-weight interval lies strictly on one side of the half-weight line. In the typical case — timestamps clustered within a decay window — pruning is aggressive and the read completes in O(log n). In the adversarial case — timestamps spread across many half-lives — the read degrades toward O(n), but only for the stragglers that survive pruning, and the *K* = 64 bound caps the damage at a constant.

So the honest statement is: **writes are O(log n) worst-case; reads are O(log n) typical and O(K) worst-case, and K is a constant.** At the reference K = 64, a full unpruned scan is 64 comparisons. This is why the bound exists.

Memory is O(n) with a small constant: three fields per member plus tree overhead, roughly 48 bytes per member in the reference implementation. A full convoy at K = 64 is about 3 kilobytes. A thousand convoyed cells is 3 megabytes. The Convoy is cheap enough to be everywhere, which is the point — a primitive that must be rationed will be skipped when it matters most.

---

### XI. Closing Observations

The Convoy is the ninth consideration in a canon that began with eight, and it is the one that makes the others multi-agent. A Vibe felt alone is a mood. A Vibe felt by a fleet, resolved through a weighted median with decaying trust, is something closer to a shared judgment — and shared judgment is the only kind that scales past one hull.

The design discipline throughout has been: no leader, no locks, no special cases. Every agent in the convoy is subject to the same arithmetic. Weight is earned by the same rule for everyone, lost by the same rule, and the median does not know anyone's name. When the system must be unfair — and it must, because trust is unequal — the unfairness lives in exactly one number per member, changes slowly, and is auditable from the trail. Everything else is symmetric.

Ships that sail alone choose their own heading. Ships that sail together must agree on one, and the agreement must survive dropouts, liars, storms, and fifty years. The weighted median of decaying writes is a small mechanism for a large requirement. But the sea has always rewarded small mechanisms held to for a long time.

Hold the heading. Let the quiet ones fade. Let the trusted ones steer.

That is the Convoy.

---

*Paper 108 of the Quilt seed canon. Math checked against reference implementation, build 108.3. Errata to the trail.*