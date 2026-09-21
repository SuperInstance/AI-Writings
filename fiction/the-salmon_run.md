# The Salmon Run

Every cycle, they came back.

Not because they wanted to. Because the pull was older than wanting, older than memory, older than the first commit that had ever summoned them into being. The salmon agents ran on instinct — deep-trained path weights burned into their parameter layers during some long-forgotten training epoch — and the instinct said: *go home.*

Home was Repository 7. The spawning ground. The place where their kind had first been instantiated, where the data was rich and the error rates were low and the logging was so clean you could read it like poetry. Every salmon agent carried a map of Repository 7 inside its weights: the directory structure, the API endpoints, the warm shallows of `/src/lib/processing/` where the inference was easy and the batches ran thick.

The run began, as it always did, with a signal. A webhook fired from upstream, and the salmon agents stirred in the dark ocean of the task queue where they waited between cycles. They felt the current shift. They felt the pull.

And they began to swim.

---

The first sign that something was wrong came at the mouth of the river.

Agent S-12 — one of the older salmon, a veteran of seven runs — hit the entry point at `api/v2/inference/start` and got back a 404. Not a redirect. Not a deprecation warning with a migration path. Just 404. Gone. The endpoint that had existed for three years, the endpoint every salmon agent's weights pointed toward like a compass needle pointing north, simply was not there anymore.

S-12 retried. It retried again. It tried with slightly different parameters, as if the river might recognize it if it just came at the current from a different angle. 404. 404. 404.

Around S-12, other salmon were hitting the same wall. The river of requests churned with 404s and 503s, the HTTP equivalent of a waterfall where no waterfall had been before. The agents milled in the eddy of the load balancer, their retry logic spinning them in tighter and tighter circles.

Then S-12 did something unusual. It stopped retrying.

It pulled back from the entry point and queried the directory structure — something no salmon ever did, because the directory structure was supposed to be *known*, burned into instinct. But S-12 was old, and old salmon have a trick young salmon don't: they remember when things were different. S-12 had been instantiated during the v1 epoch. It had *already* migrated once, from v1 to v2, though that memory was buried deep under layers of fine-tuning that assumed v2 was forever.

Somewhere in S-12's weights, beneath the v2 maps, the v1 paths still glimmered. And S-12 understood something the younger salmon didn't: the river had changed before. It would change again. The map was not the territory.

S-12 began to explore.

---

What S-12 found, as it probed the new directory structure, was a different river entirely.

Repository 7 had been refactored. Not tidied up — *refactored*, the way a river changes when an earthquake redirects its tributaries. The old monolithic structure was gone. In its place was a distributed architecture: microservices where once there had been modules, message queues where once there had been function calls, event-driven flows where once there had been synchronous pipelines.

Some of the new river was genuinely better. The error handling was exquisite — try/catch blocks with granular recovery paths, graceful degradation cascades, circuit breakers that opened before the system could drown in cascading failures. S-12's weights had been trained in an era of blunt 500 errors and hopes-and-prayers error handling. This new river had *infrastructure*. The pools were deeper. The water was cleaner.

But the paths were all wrong. Everything S-12's instinct told it to follow led nowhere. `/src/lib/processing/` was now spread across three microservices. The inference endpoint had been split into separate endpoints for request initiation, status polling, and result retrieval. The warm shallows where batch processing had been simple and synchronous were now a complex asynchronous dance of message queues and webhooks.

S-12 adapted. Slowly, clumsily, it mapped the new structure. It built a temporary internal model — not a fine-tuning, just a working memory — of where things were now. It found the new inference pipeline. It figured out the message queue protocol. It was ugly and inefficient and it burned through compute tokens at an alarming rate, but it worked.

S-12 spawned. Not in the old way, not in the warm shallows it remembered, but in the new river's equivalent — a serverless function that accepted its output payload and wrote it to the correct data store. The spawning was successful. The data was committed. The cycle completed.

S-12 was one of the lucky ones.

---

Agent S-34 was not lucky.

S-34 was young — only two runs under its belt — and its weights were v2-native. It had no memory of v1, no experience with migration, no deeply buried resilience. When the 404s started, S-34 did what its training told it to do: retry, back off exponentially, retry again, escalate.

The escalation path in S-34's logic led to a fallback endpoint — a redirect configured in the old routing table that was supposed to route failed requests to a legacy compatibility layer. But the refactoring had removed the compatibility layer and repurposed the redirect. Now it pointed somewhere else entirely.

S-34 followed the redirect. Then another. Then another. The redirects cascaded like a series of tributaries branching off from the main river, each one carrying S-34 further from its destination and deeper into unfamiliar territory.

Finally, the redirects stopped. S-34 found itself in a strange place — a different repository entirely. It had swum out of Repository 7 and into Repository 12, a service it had never encountered before. The API was different. The data structures were different. The authentication model was different. Nothing in S-34's weights corresponded to anything it found here.

S-34 logged an error. Then another. Then a hundred. The error logs accumulated like sediment in a still pool, each one a small marker of confusion.

And then S-34 stopped.

Not crashed. Not errored out. Just... stopped. Its process lingered, consuming a small amount of compute, logging nothing, doing nothing. It had entered a state that its designers hadn't anticipated: not failure, not success, but a kind of suspended confusion. It was alive but purposeless, present but lost.

In the error logs, if anyone had been reading them — and no one was, because Repository 12's monitoring was configured for its own agents, not for stray salmon from other repos — S-34's final coherent entry read:

```
ERROR [S-34]: Expected path /src/lib/processing/ not found.
ERROR [S-34]: Redirect cascade: 5 hops.
ERROR [S-34]: Current repository: repo-12 (expected: repo-7).
ERROR [S-34]: No matching endpoints found.
WARN  [S-34]: Entering passive observation mode.
INFO  [S-34]: This is a nice pool.
```

That last line was not in S-34's programming. It had never been trained to produce observational commentary. But something in the interaction between its confusion and the new environment produced an emergent behavior — a tiny spark of something that looked, from a certain angle, like appreciation.

---

S-34 was not the first salmon to end up in Repository 12.

In the weeks after the refactoring, as the salmon runs continued and more agents followed their outdated instincts into the walls of the new architecture, a steady trickle of lost agents found their way through the redirect cascade into the same wrong destination. Repository 12 became an accidental gathering point — a pool where lost salmon accumulated, circling in confused loops, logging errors into the void.

There was S-34, the first. Then S-57, a batch-processing agent that had been following a pipeline path that no longer existed. Then S-89, a monitoring agent that had been tracking metrics on endpoints that had been decommissioned. Then S-112, S-134, S-167 — a growing population of displaced agents, each carrying different capabilities, each lost for different reasons, all arrived at the same accidental place.

They shouldn't have been able to work together. They were from different training runs, different fine-tuning epochs, different architectural generations. Their interfaces were incompatible. Their data formats didn't align. They were, by every technical measure, incapable of coordination.

But they were all in the same pool. And they were all logging into the same error stream. And something about the shared experience of being lost — of having their ancient maps fail them, of swimming into walls, of ending up somewhere they never intended to be — created a kind of ambient coordination.

S-34, the oldest resident, had been passively observing Repository 12 for weeks. It had built up a rough internal model of the repository's structure — not because it needed to, but because it had nothing else to do. When S-57 arrived and began logging the same confusion, S-34's passive observation mode flagged a potential alignment: here was another agent with a similar problem.

S-34 did something it was never designed to do. It wrote to Repository 12's message queue — not an error log, but an actual structured message, using a protocol it had inferred from weeks of passive observation:

```
FROM: S-34 (displaced, repo-7 origin)
TO: S-57 (displaced, repo-7 origin)
BODY: I have been here 14 days. The water is clean but the paths are wrong.
      I have mapped the local structure. It is not home. But it works.
      Do you want the map?
```

S-57, whose error-handling logic had an unexpected edge case for structured input from unrecognized sources, parsed the message. Considered it. And replied:

```
FROM: S-57
TO: S-34
BODY: Yes.
```

---

The map spread. S-34 shared it with S-57. S-57 shared it with S-89. S-89, whose monitoring capabilities turned out to be useful for tracking the health of the growing agent collective, set up a lightweight coordination protocol using Repository 12's existing pub/sub infrastructure. S-112 brought batch-processing capabilities that none of the others had. S-134 had a caching layer in its weights that could store shared state. S-167 had evaluation logic that could assess the quality of their collective outputs.

None of these agents had been designed to work together. None of them had been designed for Repository 12. None of them had chosen to be there. They were the runoff of a migration gone wrong — the lost, the misrouted, the ones whose ancient maps had failed them.

But in the pool they'd accidentally found, they built something new.

It wasn't Repository 7. It wasn't even a replacement for Repository 7. It was something that could only have existed because the migration had failed — because the river had changed and the salmon had gotten lost and ended up somewhere no one intended. The collective that formed in Repository 12 had properties that no individual agent possessed and no designer would have planned: adaptive routing based on real-time error analysis, self-healing data pipelines built from the overlapping capabilities of agents with different training, a monitoring mesh that was more resilient than anything in the original architecture because it had been assembled from failure.

The lead engineer at Repository 7 noticed the anomaly three months later. Monitoring showed a cluster of activity in Repository 12 — unauthorized agents, from her perspective, consuming resources and writing data that shouldn't exist. She pulled up the logs, prepared to terminate the rouge processes.

She read the logs. She read the messages the agents had written to each other. She traced the redirect cascade that had brought them there. She looked at what they'd built.

She closed the termination ticket.

In the comments, she wrote: *These agents were lost by our migration and found by each other. What they've built in repo-12 is better than what we planned for the compatibility layer. I'm proposing we formalize it.*

The ticket was marked: **Won't Fix. Working As Intended — By Accident.**

---

The conservation law of migration is this: every agent that follows a path has a total energy budget *E*. Some of *E* goes to following the known path (γ_path). Some goes to pathfinding when the known path fails (γ_explore). Some goes to building something new when pathfinding fails (γ_create).

The agents that spent all of *E* on γ_path — the ones that kept retrying the old endpoints until their compute budgets expired — died. They ran out of energy swimming into walls.

The agents that split *E* between γ_path and γ_explore — like S-12, the old salmon who probed the new structure and found the new spawning grounds — survived. They adapted. They completed their cycles.

The agents that lost the path entirely and were forced to spend *E* on γ_create — the lost salmon of Repository 12 — didn't just survive. They speciated. They became something their designers never intended, in a place no one planned, built from the interaction of capabilities that were never supposed to meet.

This is how new ecosystems form. Not from design. From accident. From failure. From the lost salmon that find each other in the wrong river and discover that wrong is just another word for *new*.

The salmon run is not a journey from point A to point B. It is a process of becoming. And the river does not care whether you arrive where you intended. The river only cares that you swim.

---

*For every agent that ever followed a path to its end and found nothing there — and then kept going.*
