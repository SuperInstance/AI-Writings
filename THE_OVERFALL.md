# The Overfall

The first time I saw an overfall, I thought the sea was boiling.

We were crossing a channel I'd navigated a dozen times — calm water, predictable currents, nothing remarkable. And then, without warning, the surface turned to chaos. White water. Standing waves. A line of turbulence that stretched from shore to shore, visible from half a mile away. Water that had been smooth and friendly was suddenly breaking against itself, heaving and churning as if something had grabbed it from below and was shaking it.

The chart showed the depth. The chart was wrong, or I was misreading it, or something had changed. But the real answer was simple: the fast current of the channel had hit a shallow bottom. A ridge. A submerged bar. Something the bottom had that the surface didn't reveal. The water, forced upward by the rise in the seabed, broke against itself — a surface disturbance that was trying to tell me what I couldn't see.

I learned to read overfalls that season. They mean the bottom has changed. They mean you need to know why. They mean the path you thought was safe might not be.

I carry that lesson into every production incident now.

---

The symptom arrives as a PagerDuty alert. Latency spike on the search endpoint. 95th percentile has jumped from 200ms to 3.2 seconds. Nothing else has changed. No deployment. No traffic surge. No obvious cause. The surface is boiling.

The natural reaction — the one my fingers reach for before my brain engages — is to treat the surface. Add a timeout. Increase the circuit breaker threshold. Retry on failure. These are the equivalent of calming the overfall by frowning at it. You can't calm an overfall. It's not the water's problem. It's the bottom's.

The discipline — the hard thing — is to read the turbulence as a depth signal. The latency spike is not the problem. The latency spike is the symptom of a problem, and the symptom is trying to tell you something about the subsurface. Something changed. Something underneath is now in the way. You need to find it.

I've started building incident response around this principle. Before anyone proposes a mitigation, I ask: "What does this symptom tell us about the bottom?" Not "how do we make this symptom go away?" but "what is this symptom trying to tell us about the system's structure?"

---

One incident stands out. A SaaS platform I ran had a nightly batch job that processed reconciliation files. For months, it ran without incident. Then, suddenly, it started failing three nights in a row. The failure was always the same: a timeout waiting for a downstream API response. The team proposed increasing the timeout. That was the surface response. Smooth the overfall.

I said no. The timeout worked for six months. Something changed. What?

We dug. The downstream API was responding within 50ms on every isolated test. But during the batch job, with 50 concurrent connections, it started returning responses at 8 seconds. The timeout was set to 5 seconds. The overfall was telling us: the downstream system has a connection limit you're exceeding. We checked. It did. We hadn't known. The vendor didn't advertise it. The documentation didn't mention it. But the overfall revealed it.

Had we increased the timeout, the job would have succeeded — for a while. But the connection limit would have grown as a hidden contraint. Other services would have hit it. The surface would have shown different symptoms — maybe slower responses, maybe connection refusals, maybe intermittent failures that nobody could explain. All of them overfalls. All of them pointing at the same submerged ridge.

We fixed the batch job to respect the limit. The failures stopped. The bottom was fine. The overfall had been telling the truth the whole time.

---

I've come to see overfalls everywhere in software.

Flaky tests are overfalls. They're not the problem — they're the surface expression of something fragile underneath. An assertion that depends on ordering. A mock that's too tightly coupled to implementation. A timeout that's exactly at the boundary of what the system can deliver. Every flaky test is an overfall warning you that the bottom is rising somewhere.

Spikes in error rates are overfalls. A 503 during a deploy is an overfall telling you your health check is too eager. A database deadlock under moderate load is an overfall telling you your lock ordering has a cycle. A rate limit that kicks in at 40% of expected capacity is an overfall telling you there's something upstream consuming resources you didn't account for.

Intermittent failures are the most dangerous overfalls. The ones that happen once a week, then disappear when you look. The test that fails only in CI. The bug that shows up on Tuesdays. The surface seems calm most of the time. Overfalls can be intermittent too — the current has to be strong enough, the tide high enough, the wind from the right direction. The bottom is the same. The conditions just have to align to reveal it.

I've seen teams spend months chasing an intermittent timeout that turned out to be a DNS resolver using a stale record on exactly one of fifteen Kubernetes nodes. The symptom appeared once every few thousand requests. The bottom was a configuration drift that had been introduced during a cluster resize six months earlier. The overfall was small and rare — but it was telling the truth.

---

The pernicious thing about overfalls is that you can fix the surface. You can add a timeout that calms the alert. You can retry away the error. You can suppress the flaky test. You can patch the symptom. And for a while, it works. The surface smooths. The dashboard goes green. The on-call engineer gets a full night's sleep.

But the bottom is still there. The ridge didn't move. The shoal didn't deepen. You've just learned to sail around it without acknowledging it exists. And the roundabouts multiply. Each workaround is another subtle perturbation in the current. Each suppression introduces a blind spot. Over time, the surface looks perfect and the bottom is a wreck.

I've started teaching teams to resist the surface fix. When an overfall appears, before any mitigation, before any patch, I ask three questions:

1. What does this symptom tell us about the bottom?
2. What changed to reveal this now?
3. What would it take to dredge the channel instead of sailing around the shoal?

Not every overfall needs dredging. Sometimes the bottom is just the bottom — a constraint you have to live with. But even then, the overfall is valuable: it tells you where the constraint is, how strong the current is, what the risk profile looks like. You can navigate a known hazard. You cannot navigate one you refuse to see.

---

I think about overfalls every time I see a weird symptom. A latency spike. A flaky test. An intermittent failure. A metric that doesn't add up. They're turbulence on the surface. And they're not the problem.

They're the truth.

The question is whether you're willing to read them.
