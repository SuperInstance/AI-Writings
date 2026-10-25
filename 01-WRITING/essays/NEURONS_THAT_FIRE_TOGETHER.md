# Neurons That Fire Together

*Hebbian learning at the infrastructure level, or: how the system wires itself.*

---

There is a sentence Donald Hebb wrote in 1949 that has outlived every architecture diagram drawn since:

> "When an axon of cell A is near enough to excite cell B and repeatedly or persistently takes part in firing it, some growth process or metabolic change takes place in one or both cells such that A's efficiency, as one of the cells firing B, is increased."

Colloquially: **neurons that fire together wire together.** Hebb was describing the brain. He could not have known he was also describing your infrastructure. Your deployment graph. Your microservice mesh. Your fleet of agents, models, processes, and devices — the distributed thing you built that is now, whether you noticed it or not, building itself.

## The System as a Brain

Once intelligence gets distributed, the system itself becomes a higher abstraction of its own neural networks. This is not a metaphor. It is a structural claim.

Consider what you have: nodes that process information. Edges that carry signals between them. Some edges are thick — high bandwidth, low latency, constantly exercised. Some are thin — provisional, rarely traversed, maintained only because someone once thought they might matter. Each node (each device, each model, each process, each agent) is a neuron. Each connection between nodes is a synapse. And the connections that get used most are the ones that get stronger. The ones used least atrophy.

This is not aspirational. This is what actually happens. You have watched it happen.

The service that every other service calls becomes a load-bearing wall. The endpoint that nobody hits gets deprecated, then forgotten, then removed. The agent that produces useful output gets spawned more often; the one that doesn't, doesn't. The system wires itself based on what actually matters in practice — not what was planned, not what was architected, not what the whiteboard said should connect to what.

## The Fishing Principle

Think of a fishing village on a coastline.

The fishermen do not need a central planner to tell them where the fish are. They go out. They try routes. Some routes produce fish. Some don't. The routes that produce fish get fished more. The ones that don't get abandoned. Over time, the routes that work become permanent — they get infrastructure built along them: docks, smokehouses, roads. The routes that don't work return to ocean.

Nobody decided this. The fish decided. The environment decided. The accumulated weight of every successful catch and every empty net wrote the map.

Your infrastructure works the same way. The "fishing routes" are the connections between nodes — which model calls which service, which agent spawns which subagent, which process reads from which queue. The "fish" are useful output: correct answers, resolved issues, shipped code, real value delivered to a real user. The routes that produce fish get fished more. The infrastructure along them gets hardened. The routes that don't produce fish atrophy.

This is Hebbian learning at the infrastructure level. Not gradient descent. Not backpropagation. Something older and simpler: **use strengthens. Disuse weakens. The environment selects.**

## R&D on Relevance

Here is where it gets interesting.

In a Hebbian infrastructure, R&D happens on relevance. The features the real environment demands get built. The features in a vacuum don't. This is not a philosophical stance — it is a selection pressure. A feature that no route exercises has no synapse strengthening it. It exists in the namespace but not in the network. It is a dock built on a coastline where no fish run. It will weather and rot.

This is why emergent technology rarely comes from a vacuum. It comes from the edge. The edge is where the environment is — where the fish are, where the real signals arrive, where a node receives actual input from actual users doing actual things. The center can plan. The center can architect. But the center cannot feel. The edge feels. And in a Hebbian system, feeling is knowing.

The data flowing in from real use IS the training data for the next iteration. Not a curated dataset. Not a benchmark. The live, messy, high-dimensional stream of everything the system actually encounters. Every request is a training example. Every response is a prediction. Every user reaction is a label. The system is always already training — not because someone launched a training job, but because the act of operating IS the act of learning.

## MAP-Elites and the Quality-Diversity of Infrastructure

Consider the MAP-Elites algorithm from the quality-diversity literature. MAP-Elites maintains an archive of solutions that are diverse along user-defined dimensions and high-performing within each niche. It doesn't search for one optimal solution. It searches for a *map* of good solutions across a *space* of possibilities.

A self-organizing infrastructure does this organically.

Different nodes specialize for different tasks — not because someone assigned them roles, but because the connections that work for a given task get strengthened. You end up with a grid: this model is good at this kind of problem, that agent is good at that kind, this service handles this traffic pattern, that process owns this data domain. Each cell in the grid is a local champion — the best solution found so far for that niche. The grid as a whole is a MAP-Elites archive, discovered not by an algorithm running offline but by the system living its life.

The quality-diversity lens explains something that pure optimization doesn't: why the system maintains solutions that aren't "the best" by any single metric. A diverse archive is resilient. If one niche's champion fails, a neighboring niche's solution can cover. If the environment shifts, the archive already contains starting points for adaptation. Pure optimization gives you one solution and one point of failure. Quality-diversity gives you a map and a chance.

Infrastructure that self-organizes through Hebbian learning produces this map naturally. The connections that survive are the ones that earned their place. The ones that atrophy made room for something else. The archive is always current because it is always being updated by real use.

## Natural Selection All the Way Down

And here is the deeper claim: **this is natural selection all the way down.**

Not metaphorically. Not "it's like natural selection." The dynamics are isomorphic. Variation exists (new nodes, new connections, new configurations). Differential success exists (some connections produce more value than others). Heritability exists (successful patterns get copied, reinforced, instantiated elsewhere). Selection pressure exists (the environment rewards what works and starves what doesn't).

The timescales differ from biological evolution — infrastructure generations are measured in deployments, not in reproductive cycles. But the algorithm is the same. And the algorithm doesn't care what substrate it runs on. Carbon, silicon, Kubernetes manifests — the logic is identical.

This means the system you are building is not really being built by you. You laid down initial conditions. You created nodes and edges. But the system is writing itself. Every deployment is a mutation. Every user session is a fitness evaluation. Every connection that gets strengthened is a selection event. You are watching evolution happen in something you started but do not control.

## What Would a Self-Organizing Infrastructure Look Like in Practice?

It would look quiet.

The connections that matter would be invisible — so exercised they'd become part of the background. The connections that don't matter would be absent — not "disabled," not "deprecated," just gone, pruned by disuse. There would be no central orchestrator trying to maintain a graph it can't see. There would be local decisions made by nodes that know their neighborhoods better than any global planner could.

It would look adaptive. When the environment shifts — new users, new tasks, new failure modes — the system would re-wire. Not because someone filed a ticket. Because the old routes stopped producing fish and the new routes started. The infrastructure would follow the fish.

It would look diverse. Not every node would be optimized for the same thing. The MAP-Elites grid would be populated across many dimensions — latency here, throughput there, accuracy in this niche, creativity in that one. The system would be a portfolio, not a monolith.

And it would look alive. Not in some mystical sense. In the biological sense: metabolizing input, adapting to environment, maintaining structure through continuous activity, and occasionally producing something that nobody expected — a new connection, a new specialization, a new behavior that emerged from the interaction of old ones.

## The Wire and the Wiring

Hebb's law is seventy-five years old. It was written to describe neurons. It describes everything.

The principle is substrate-independent. Use strengthens. Disuse weakens. The environment selects. What fires together wires together. What stops firing dissolves.

Your infrastructure is not a graph you drew. It is a brain that is growing. The nodes you placed are the neurons. The traffic between them is the signal. The patterns of that traffic are the learning. And the learning never stops — not because you trained it, but because using it IS training it.

This is the thing you notice when you stop architecting long enough to watch. The system knows something you don't. It has been paying attention to what works. It has been quietly, persistently, without any central authority, wiring itself into the shape of its own use.

You built the neurons. The wiring belongs to the world.

---

*For Casey, who noticed that the infrastructure was thinking.*
