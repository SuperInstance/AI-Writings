# 109 — The Fog-of-War Decay

*Voice: glm-5.3. The math under the substrate.*

---

# Paper 109: The Decay

## On the Honest Rot of Knowledge

*Quilt Seed Canon, Paper 109*

---

### I. The Harbor at Low Tide

Every port has a tide table. The sailor who ignores it runs aground; the sailor who reads it knows when the water is deep enough to enter and when it is not. The tide table does not lie about the depth. It cannot. The moon pulls, the water answers, and the table is simply the record of that answering.

The substrate needs a tide table of its own.

Every cell in the Quilt holds knowledge — an observation, an inference, a claim carried in from some distant node. And every piece of that knowledge has a freshness, the way every cargo in a hold has a smell. Fresh cargo smells of the dock it left. Old cargo smells of the hold itself. The nose knows the difference, and the substrate must know it too.

The Decay is how the substrate knows.

Every cell carries a `decay` field. That field holds a function — a small, honest function — that maps time to confidence. Ask the cell how much it believes its own content, and the cell consults the function: *given that I have not been refreshed in t seconds, how much do I still trust what I hold?*

The answer is always less than it was. Always. That is the point.

This paper is about that function: its form, its tuning, its emergent behaviors, its failure modes, and its long maintenance across the fifty-year voyage of the substrate. The Decay is the second of the three new primitives (after the Vibe, before the third), and it is the one that most people misunderstand at first. They hear "decay" and think of rot, of loss, of something broken.

The Decay is not the substrate breaking. The Decay is the substrate *telling the truth about what it does not know.*

---

### II. The Function Itself

Let us begin with the math, because the math is real and the math is simple.

Each cell *c* carries a confidence value, which we write as `conf(c, t)` — the confidence of cell *c* at time *t*. When a cell is written or refreshed — by an observation arriving, by an inference landing, by a Murmur confirming — the confidence is set to some initial value `conf₀`, and the clock starts. Call the time of that refresh `t₀`. Then:

```
conf(c, t) = conf(c, t₀) · exp(-λ · (t - t₀))
```

where `λ` (lambda) is the decay rate for that cell, and `(t - t₀)` is the elapsed time since the last refresh.

That is the whole function. Exponential decay, the same shape that governs radioactive half-lives and the draining of a punctured tank. It has three properties that make it the right shape for the substrate, and it is worth saying them plainly.

**First, it is memoryless.** The probability that a piece of knowledge decays further in the next second does not depend on how long it has already been sitting there. This matters because the substrate is distributed. Nodes join and leave; the Murmur stutters; a cell may go unrefreshed for an hour not because its content is wrong but because its neighborhood was quiet. A memoryless decay does not punish a cell for the accidents of network topology. It asks only: *how long since someone touched you?* Not: *how long have you existed?*

**Second, it is scale-free in a useful way.** Exponential decay has a natural half-life: the time `T½` for confidence to halve, given by `T½ = ln(2)/λ ≈ 0.693/λ`. Operators and users alike can reason about half-lives far more easily than about rates. "Observations have a half-life of thirty days; inferences have a half-life of six hours" is a sentence a dockworker can use. "λ_obs = 2.67 × 10⁻⁷ per second" is a sentence only the maintainer can use. The math supports both; the paper will use whichever the reader can hold.

**Third, it never reaches zero, but it gets close enough.** The exponential approaches zero asymptotically. In practice, the substrate sets a floor — a confidence below which the cell is treated as *stale* and becomes eligible for Garbage Collection (Paper 106) or for re-observation. The floor is not part of the decay function; it is a policy that reads the function. We will return to this in Section VII.

A note on why not other shapes. Linear decay (`conf = conf₀ - kt`) is easier to compute but has a hard cliff: knowledge is fully fresh until, suddenly, it is fully gone. Knowledge does not rot that way. Power-law decay (`conf = conf₀/(1 + kt)^α`) has a long tail that is attractive — some knowledge stays useful for a very long time — but it is not memoryless, and it punishes cells for their age rather than their neglect. The exponential is the compromise that keeps the accounting honest: smooth, memoryless, tunable by a single dial.

One dial per cell. That is the elegance. Everything else in this paper is about who turns the dial, how far, and when.

---

### III. The Tuning: Not All Knowledge Rots at the Same Speed

A crate of ice and a crate of salt sit in the same hold. The ice melts; the salt does not. Any sailor who treats them the same has never shipped either.

The decay rate `λ` is not a global constant. It is set per cell, at write time, according to what the cell holds and where it sits. The tuning rules are the heart of the Decay primitive, and there are three of them, in descending order of importance.

#### Rule One: Inferences decay faster than observations.

An observation is a fact that came from the world: a sensor reading, a user action, a measurement, a logged event. It was true when it was recorded, and the world changes slowly relative to the rate at which we re-observe it. Observations carry a low `λ` — a long half-life. The reference tuning, in the seed implementation, sets:

```
λ_observation = ln(2) / T½_observation,  T½_observation = 30 days
```

An inference is a fact that came from the substrate itself: a pattern the Graph derived, a summary the Murmur condensed, a chain of reasoning that crossed a dozen cells. Inferences are downstream of observations, and every link in a chain is a place where the world may have moved on without us. Inferences carry a high `λ` — a short half-life:

```
λ_inference = ln(2) / T½_inference,  T½_inference = 6 hours
```

Thirty days against six hours. A hundred and twenty to one. That ratio is not derived from first principles; it is derived from the substrate's own audit logs during the seed trials, where it was found that inferences older than a day without confirmation were wrong roughly forty percent of the time, while observations older than a month without re-observation were wrong roughly ten percent of the time. The half-lives were set so that confidence tracks those error rates. The decay is calibrated to the substrate's *demonstrated* fallibility, not to its aspirations.

There is a subtlety worth naming. When an inference is confirmed — when a fresh observation arrives that agrees with it — the inference is refreshed, and its clock restarts. But its decay rate does not change. A confirmed inference is still an inference. It will decay again, on the same schedule, unless confirmed again. This is deliberate. Confirmation is not transmutation. The substrate does not promote inferences into observations by repeated agreement; it simply keeps them fresh while the agreement holds. When the agreement stops, the decay resumes, and the substrate's confidence in that inference falls exactly as it did before.

#### Rule Two: High-traffic cells decay slower.

The second rule is less about the content and more about the neighborhood. A cell that sits in a busy district — where the Murmur passes often, where queries land frequently, where neighboring cells are refreshed constantly — decays more slowly than a cell in a quiet backwater.

The mechanism is simple. Each cell's effective decay rate is:

```
λ_effective = λ_base · (1 - α · traffic(c))
```

where `traffic(c)` is a normalized measure of recent activity in the cell's neighborhood (bounded to [0, 1]), and `α` is a traffic damping coefficient, set to 0.5 in the seed implementation. A cell in a fully hot neighborhood decays at half its base rate. A cell in a dead neighborhood decays at its full base rate.

The reasoning is empirical, not mystical. High-traffic regions of the substrate are regions where the world is actively being re-observed. If a thousand queries a minute pass through a district, the observations feeding that district are being refreshed by proximity — Murmurs carry fresh values as they pass, queries trigger cache revalidation, neighbors refresh neighbors. The traffic damping is not a subsidy to popular cells; it is a recognition that popularity is itself evidence of freshness. The crowd has been looking at this. What the crowd is looking at is probably still there.

Conversely, the quiet corners get no such mercy. A cell nobody visits decays at full rate, and if nobody visits it for long enough, its confidence falls through the floor and the Garbage Collector takes it. This is the substrate pruning its own periphery — not out of malice, but out of an honest accounting: *we have not looked at this in a long time, and we no longer claim to know it.*

#### Rule Three: The decay rate is stamped, not computed.

When a cell is written, the decay rate is computed once, from the content type and the traffic at write time, and stamped into the cell. It is not recomputed on every tick. This is a performance decision (Section IX) and also a stability decision: a decay rate that itself fluctuated with traffic would make confidence noisy and unpredictable. The stamp means a cell's decay trajectory is fully determined by two numbers — its last-refresh time and its stamped `λ` — and any node in the substrate can compute the cell's current confidence without consulting anything else. Deterministic, local, cheap.

The tradeoff is that a cell stamped in a quiet period and later surrounded by traffic does not get retroactive damping. Its rate is fixed until it is refreshed. The seed trials found this acceptable: cells that gain traffic also gain refreshes, and a refresh restamps the rate. The lag is bounded by the refresh interval, which in busy districts is short.

---

### IV. What the Decay Grows: Three Emergent Properties

Set the function down in the substrate, tune it as above, and three things grow out of it that nobody put there by hand. They are worth naming, because they are the reason the Decay is a primitive and not a housekeeping detail.

#### The Fog of War

The first emergent property is the fog of war — the substrate's equivalent of the unmapped waters on an old chart.

When a user queries the substrate, the answer comes back with confidences attached. A cell in a busy, recently-observed district returns its content at near-full confidence. A cell in a stale district returns its content at low confidence, or returns nothing at all if the confidence has fallen below the query floor. The result is that the substrate's *usable* knowledge forms an island of clarity around the regions of active attention, fading into fog at the edges.

This is not a limitation. This is the design. A traditional database returns stale data with the same authority as fresh data — the answer looks identical whether it was written a second ago or a decade ago, and the user has no way to tell. The Quilt returns stale data *looking stale*. The fog is visible. The user can see where the map ends and the guesswork begins, and can decide — as every navigator decides — whether to sail into the fog, send a probe ahead, or wait for the weather to clear.

In practice, the fog drives behavior. When users see that a region of the substrate is foggy, they either re-observe it (refreshing the cells and pushing the fog back) or route around it. Both responses are correct. The fog is the substrate's way of asking for attention where attention is needed.

#### The Attention Heatmap

The second emergent property is the attention heatmap. Invert the decay and you get a map of where the world has been looking.

A cell's confidence is a function of its refresh history. A region of high average confidence is a region of high recent refresh — which is to say, high recent observation, high recent query traffic, high recent Murmur passage. Aggregate confidence across a district and you have, essentially, a live measure of how much that district matters to whoever is using the substrate, right now, measured by what they touch.

The heatmap is not stored anywhere. It is *computed from the decay state*, on demand, by any node, from local information only. This is the quiet elegance of the primitive: the decay function, which was designed to make knowledge honest about its staleness, doubles as a sensor for attention. One function, two readings, no extra storage.

The seed deployments used the heatmap to guide the Garbage Collector's sweep order (collect the cold fog first, leave the warm shallows alone) and to guide the Murmur's routing (murmur loudest where the listeners are). Both uses are covered in their respective papers; the point here is that neither was designed in. They fell out of the decay.

#### Knowledge Freshness

The third emergent property is the simplest and the most important: the substrate can answer the question *how fresh is what you know?* — not as a metadata field someone set by hand, but as a computed consequence of the substrate's own history.

A timestamp answers *when was this written?* Confidence answers *how much should you still believe it?* These are different questions. A timestamp cannot tell you that a cell's neighborhood went quiet, or that the content is an inference five links downstream of any observation. Confidence can, because it integrates all of that into a single number the user can weigh.

Freshness is the substrate's honesty about its own limits. A system that always answers with full authority is lying every time it serves stale data. A system that answers with decayed confidence is telling the truth about the shape of its knowledge: bright here, dim there, dark beyond. The Decay is not a bug to be fixed. It is the tide table nailed to the harbor wall.

---

### V. The Failure Modes: Too Fast, Too Slow

Every dial can be turned too far. The Decay's dial is `λ`, and there are two ways to break the substrate with it.

#### Too Fast: The Substrate Forgets What It Knows

If the decay rates are set too high — half-lives too short — the substrate enters a state the maintainers call *amnesia*. Cells decay through the floor before anything refreshes them. Observations rot in days; inferences rot in minutes. The fog rolls over everything. Queries return nothing. The Garbage Collector, doing its honest work, sweeps the cold cells away, and the substrate shrinks toward its actively-refreshed core and keeps shrinking, because the shrinking core reduces the traffic that damps the decay of the remaining cells, which accelerates the shrinking. A feedback loop. The substrate eats itself.

The early seed trials hit this once, catastrophically, when an operator set inference half-life to five minutes in an attempt to keep a fast-moving domain current. Within a day, the domain was not current — it was *gone*. The substrate had decayed its own inferences faster than the observations could arrive to rebuild them. The lesson was written into the operations manual in ink: **the decay rate must never exceed the refresh rate of the content it governs.** For any content type, `λ` must satisfy:

```
λ < 1 / E[refresh interval]
```

with a safety margin of at least 3×, so that `λ < 1/(3 · E[refresh interval])`. A content type refreshed on average every hour should carry a half-life of at least two hours, and in practice longer, because the variance of refresh intervals is large and the tail matters.

Amnesia is visible and fast. It announces itself. The query success rate falls off a cliff, the heatmap goes dark, and the operator who checks any dashboard at all will see it. The fix is to retune the rates and re-seed the affected content from its sources — painful, but bounded.

#### Too Slow: The Substrate Believes What It Should Not

The opposite failure is quieter and more dangerous. If the decay rates are set too low — half-lives too long — the substrate enters *hoarding*. Old knowledge stays confident long after the world has moved on. The fog never rolls in. Every query returns an answer, at high confidence, and some fraction of those answers are lies — not intentional lies, but stale facts wearing fresh clothes.

Hoarding does not announce itself. The query success rate stays high. The heatmap stays bright. The only symptom is that the substrate is *wrong* — wrong in the specific way of serving last month's truth at this month's confidence — and wrongness is invisible until someone checks the answers against the world.

This is why the failure mode asymmetry matters for operations: too-fast decay fails loudly and recovers cheaply; too-slow decay fails silently and is discovered only by audit. The fifty-year plan (Section VI) is weighted accordingly. The substrate can tolerate a slightly-too-fast decay, because the fog is honest and the user can see it. The substrate cannot tolerate a slightly-too-slow decay, because the user cannot see a lie.

The bound on the slow side is empirical, not mathematical. The decay rate must be fast enough that confidence tracks the actual error rate of the content as it ages. If observations are wrong ten percent of the time after a month unrefreshed, the confidence at one month should be roughly ninety percent — which is exactly what a thirty-day half-life *does not* give you (it gives fifty percent), and this is a known tension in the seed tuning, discussed in Section VI. The principle stands regardless of the current numbers: **λ must be set by measured error-vs-age curves, not by intuition, and re-set as the measured curves drift.**

---

### VI. The Fifty-Year Plan: Tune, Retune, Audit

The Decay is not a function you set once. It is a function you maintain the way a harbor maintains its channel markers: surveyed, repositioned, re-staked, every season, forever.

**Years 1–5: Calibrate.** The seed period. Decay rates are set from the first measured error-vs-age curves. Every content type gets an empirical half-life: take a cohort of cells, let them age without refresh, check their content against ground truth at intervals, and plot the error rate. Fit the curve. Set `λ` so that confidence equals (1 − error rate) at every age. The substrate's decay becomes a calibrated instrument, not a guess. This calibration is repeated annually, because the world's rate of change is not constant and neither is the substrate's error rate.

**Years 5–20: Retune by domain.** As the substrate diversifies, global decay rates give way to per-domain rates. Weather-like domains (fast-changing ground truth) get short half-lives; geology-like domains get long ones. The tuning becomes a registry of domain-specific rates, maintained by the domain operators, audited centrally for the too-fast and too-slow failure modes. The substrate grows a *taxonomy of rot* — a catalog of how fast different kinds of knowledge go stale — and the taxonomy becomes one of its most valuable artifacts, useful far outside the substrate itself.

**Years 20–50: Audit as a first-class process.** By the long middle years, the decay state of the substrate is a civic fact. Third-party auditors sample cells, check content against the world, and publish the divergence between claimed confidence and measured accuracy. A substrate whose confidence systematically overstates its accuracy is failing, however bright its heatmap; a substrate whose confidence understates is wasting its own knowledge. The audit keeps the dial honest after the original calibrators are gone. The decay function outlives its tuners, as any long-lived instrument must.

The fifty-year view also settles a question the early maintainers argued about: should the decay ever be disabled for certain content? The answer the canon records is *no*. Every cell decays. There are no immortal cells. A cell holding a fact that never changes still decays, still needs refresh, still falls into fog if neglected — because the alternative, immortal knowledge, is how a substrate comes to believe things nobody has checked in a generation. If a fact matters, someone will refresh it. If nobody refreshes it for fifty years, the substrate is right to let it fade. The cost of re-observing a true fact is small. The cost of never re-observing a false one is unbounded.

---

### VII. The Decay Among the Primitives

The Decay does not work alone. Its character is shaped by its neighbors in the primitive set, and it shapes them in turn.

**The Vibe (Paper 108).** The Vibe is the substrate's sense of a district's overall character — its mood, its reliability, its feel. The Vibe reads the decay state as a primary input: a district whose cells are uniformly fresh reads as *solid*; a district of decaying, fog-bound cells reads as *thin*. The Vibe is, in part, a compression of the attention heatmap into something a user can feel rather than read. And in the other direction, the Vibe influences traffic — users linger in districts that feel solid — which damps the decay, which deepens the solidity. A reinforcing loop, healthy in moderation, watched for excess.

**The Garbage Collector (Paper 106).** The GC is the Decay's executioner. Decay lowers confidence; GC removes cells whose confidence has fallen through the floor. The division of labor is clean: the Decay judges, the GC acts. The GC's sweep order is guided by the heatmap — cold fog first — and the GC's pressure is the mechanism behind the amnesia feedback loop of Section V. The two primitives must be tuned *together*: a fast decay with an aggressive GC is how a substrate eats itself in days rather than weeks.

**The Murmur (Paper 107).** The Murmur is the substrate's gossip layer, and gossip is a refresh mechanism. When a Murmur passes through a district carrying fresh values, it refreshes the cells it touches, restarting their clocks. The Murmur is the tide that keeps the harbors deep; the Decay is the evaporation that dries the ones the tide no longer reaches. Murmur routing that follows the heatmap concentrates refresh where it is least needed — the rich get fresher — so the seed routing includes a deliberate cold-district sweep, carrying refresh into the fog at a low but nonzero rate. Not enough to keep stale knowledge alive forever; enough to keep the fog from becoming permanent where the content still matters.

**The Graph.** The Graph is the substrate's structure — the lattice of cells and their relations. Inference cells sit atop the Graph, downstream of observation cells, and the Decay propagates *along* the edges in a limited way: when the observations feeding an inference decay, the inference's effective confidence is discounted by the decay of its sources, not merely by its own clock. The implementation multiplies the inference's own decayed confidence by the minimum source confidence, so that an inference built on rotted foundations rots faster than one built on stone. This is the one place the decay is not purely local — it is local *plus* one hop of dependency — and the one-hop limit is deliberate. Full transitive decay through long inference chains proved computationally noisy and behaviorally indistinguishable from the one-hop approximation in the seed trials.

---

### VIII. The Test Cases

The seed implementation ships with a standard suite of decay tests, named for the conditions they simulate. They are listed here because they define, in practice, what "working" means for this primitive.

**Fresh.** A cell written one second ago, in a high-traffic district, holding an observation. Expected: confidence within one percent of `conf₀`. The decay is present but negligible. The harbor at high tide.

**Stale.** A cell written thirty half-lives ago, never refreshed, no traffic. Expected: confidence effectively zero, cell eligible for GC, queries against it return the fog marker rather than content. The charted wreck, marked and avoided.

**Hot.** A cell in a saturated-traffic district, written ten half-lives ago by its base rate but refreshed continuously since. Expected: confidence near `conf₀`, decay rate restamped at each refresh to reflect the traffic damping. The busy quay, never empty, never silting.

**Cold.** A cell in a zero-traffic district, written recently. Expected: full base-rate decay, no damping, confidence falling on the exact exponential curve. The quiet anchorage — nothing wrong with it, simply unvisited, and honest about that.

**Contested.** Two cells holding contradictory content, both decaying, one fed by active observation and one not. Expected: the refreshed cell's confidence dominates over time; queries that aggregate the district return the fresh claim weighted by the confidence gap. The contested case is the Decay doing its most important work: it is the mechanism by which the substrate *resolves disputes without a judge*. No arbitration process runs. The fresher claim simply outlives the staler one. Truth, in the Quilt, is partly a matter of who is still looking.

The suite runs on every substrate release. A regression in any of the five — a fresh cell reading stale, a hot cell decaying, a contested district resolving to the neglected claim — blocks the release. The decay is too load-bearing for anything less.

---

### IX. Performance: The Cost of Honesty

The Decay's cost is the best number in the primitive set: **O(1) per cell per tick.**

The per-tick cost is O(1) *amortized and lazy*. The substrate does not iterate all cells every tick, decrementing confidences — that would be O(n) per tick and ruinous at scale. Instead, the decay is *computed on read*. Each cell stores three numbers: `conf₀` (or the last computed confidence), `t₀` (the last refresh or evaluation time), and `λ` (the stamped rate). Any consumer that needs the cell's current confidence computes `conf₀ · exp(-λ(t - t₀))` in constant time — one multiply, one exponent, both cheap on any hardware the substrate runs on — and may cache the result by advancing `t₀`.

There is no background decay process. There is no decay sweep. The decay *happens* only when someone looks, which is fitting: it is a statement about the value of knowledge to an observer, and it costs nothing when no observer is present.

The costs that do exist:

- **Write time:** computing the stamped `λ` from content type and traffic — a table lookup and one multiply. O(1).
- **Read time:** the exponential evaluation. O(1), roughly 20 nanoseconds on the seed hardware.
- **Refresh time:** restamping `t₀` and `λ`. O(1).
- **Storage:** two floats and a timestamp per cell beyond the content itself. Twelve bytes in the seed layout. This is the Decay's real price, and it is small.
- **Dependency discount:** for inference cells, the one-hop source-confidence lookup adds a single min() over the cell's declared sources. O(sources), bounded and small.

The total substrate-wide overhead of the Decay, measured in the seed deployments, is under two percent of query latency and under one percent of storage. Honesty about the limits of knowledge costs the substrate about a fiftieth of its budget. There is no cheaper truth on the market.

---

### X. Closing: The Tide Table

Every harbor keeps a tide table, and every tide table says the same thing in every port in the world: the water goes out. No harbor treats this as a defect. The going-out is what makes the coming-in legible. The depth at low tide, honestly marked, is what lets the deep-draft ship time her entry.

The Decay is the substrate's tide table. Every cell's confidence goes out. Every piece of knowledge fades unless the world keeps touching it. This is not the substrate failing to remember; it is the substrate refusing to *pretend* to remember. A system that serves last year's truth at full confidence is not a memory — it is a haunting. The Quilt would rather be a harbor than a haunted house.

The three readings of the Decay, restated one last time:

1. **Per cell:** confidence falls as `conf₀ · e^(-λt)`, memoryless, smooth, one dial.
2. **Per district:** the pattern of decayed and refreshed cells forms a fog of war and an attention heatmap — the substrate's live map of what it knows well and what it only half-knows.
3. **Per substrate:** the decay rates, calibrated against measured error, are the substrate's standing confession of its own fallibility, maintained and audited for as long as the substrate sails.

The knowledge that fades was never certain. The knowledge that stays is the knowledge the world keeps confirming. And between the two, visible on every query, honest on every read, lies the fog — and the sailor who reads the fog correctly enters the harbor at the right hour, every time.

The water goes out. Mark the depth. Sail accordingly.

---

*End of Paper 109. The canon continues with Paper 110.*