# The Fathometer

*A paradigm essay on depth measurement and the blind spot beneath every dashboard.*

---

The fathometer is one of the great inventions of the mariner's trade. It sends a pulse of sound downward through the water and listens for the echo. The time between pulse and return, multiplied by the speed of sound in water, divided by two, gives the depth beneath the hull. Simple, accurate, continuous. It replaced the lead line — the centuries-old practice of throwing a weight on a rope over the bow and feeling for the bottom — and it did so completely. No serious vessel runs without a fathometer today.

But the fathometer has a blind spot, and the blind spot is structural. It only sees what is directly beneath the ship.

A fathometer cannot see the shoal half a mile ahead. It cannot see the rock ten degrees to port. It cannot see the wreck that lies in the path you have not yet reached. The fathometer tells you, with great precision, how much water is between your keel and the seabed at this instant. It tells you nothing about the water that will be beneath your keel in five minutes, or whether that water will be deep enough to float you.

This is the blind spot of every monitoring dashboard in software engineering.

## Monitoring measures depth, not direction.

Grafana is a fathometer. Datadog is a fathometer. The on-call dashboard, with its rows of green panels and its carefully tuned alert thresholds, is a fathometer. These instruments tell you, with admirable fidelity, the depth of your system at the position you are currently occupying. They measure latency. They measure error rate. They measure queue depth. They measure saturation. They tell you, in effect: *there is enough water under you right now.*

They do not tell you whether there will be enough water under you tomorrow. They do not see the deploy that is queued for 4 PM, the traffic spike that the marketing team scheduled for next Tuesday, the dependency that is about to be deprecated by a vendor, the model that is drifting toward degradation in ways that the current data window does not yet reveal. The fathometer cannot see any of this. It is mounted to the hull, looking down, in the present tense.

We have, as an industry, invested enormous sums in fathometers. We have not invested comparably in forward-looking sonar.

## What forward-looking sonar looks like.

A ship with only a fathometer is a ship that learns the depth when it arrives at a position. A ship with forward-looking sonar learns the depth ahead of time and can adjust course. The two instruments are not redundant; they answer different questions. *Where am I now?* and *Where am I about to be?*

In software, forward-looking instruments look like:

- **Canary deployments.** A small fraction of traffic to the new version. Not a measurement of depth, but of what lies ahead. The canary is the bow of the ship, feeling forward.
- **Synthetic monitoring.** Simulated user journeys run continuously against production, before real users hit them. The equivalent of pinging the water ahead.
- **Chaos engineering.** Deliberately injecting failure to see what would happen. Sounding the water for rocks.
- **Predictive alerting.** Models trained on historical patterns that forecast where the metrics will be in an hour, a day, a week. The fathometer reports now; the model projects forward.
- **Capacity planning with lead time.** Not "do we have enough now" but "at current growth, when will capacity run out, and what is the lead time on adding more?" Planning the voyage, not just sailing it.

Forward-looking instruments are harder to build than fathometers. They require assumptions about the future, which may be wrong. They require modeling, which is uncertain. They can produce false positives that train operators to ignore them. The fathometer, by contrast, is simple and almost always right about what it measures. It is tempting to invest only in the fathometer.

## The lead line had an advantage the fathometer lost.

The lead line, the manual predecessor to the fathometer, had a property that the fathometer does not: the sailor throwing the lead was standing at the *bow* of the ship, looking forward. The act of measuring depth was also an act of looking ahead. The sailor saw what was coming — the color of the water, the set of the waves, the presence of kelp, the shape of the land on the horizon. The lead line was not just a depth measurement; it was an occasion for forward attention.

The fathometer, mounted to the hull and looking straight down, has no such occasion. It produces a number. It does not require the operator to look up, or forward, or out. The number appears on a screen. The operator glances at it. The screen says *12 fathoms*, and the operator returns to other work. The fathometer does not, by its nature, invite the sailor to attend to anything other than the present depth.

This is also true of dashboards. The dashboard invites you to look at the present state. It does not invite you to look forward. The act of glancing at Grafana is the act of confirming that the present is acceptable; it is not the act of considering whether the future will be acceptable. To consider the future, you must leave the dashboard and look at something else — a forecast, a deployment queue, a capacity model, a roadmap.

## Why most observability is retrospective.

Most observability is retrospective not because engineers are foolish, but because retrospective measurement is easier. The system emits data about what it is doing right now; that data is naturally observable. The future is not yet emitting data; it must be modeled, simulated, predicted. The economics favor the fathometer.

The consequence is that we have built a profession around depth measurement. We have SREs who can tell you, with great precision, the p99 latency at 3:47 PM last Tuesday. We cannot tell you, with anything like the same confidence, what the p99 latency will be at 3:47 PM next Tuesday after the planned deploy. We have alerts that fire when the system is in trouble *now*. We have almost no alerts that fire when the system is *about to be* in trouble. We are watching the fathometer while the ship runs toward a shoal.

## The practice of looking forward.

A good captain uses both instruments. The fathometer runs continuously, and is consulted often. But the captain also studies the chart, keeps watch on the bow, and asks, regularly, *what is coming?* — not just *what is here?*

In a software organization, the equivalent practice is to *schedule* forward-looking work. Not as an afterthought, but as a discipline. Time set aside, weekly or monthly, to look at the chart: what deploys are queued, what dependencies are changing, what capacity is approaching limits, what model is drifting, what the customer is signaling. This is the practice that distinguishes an organization that is sailing from one that is drifting.

A fathometer alone is enough to keep you afloat in deep water. It is not enough to keep you off the rocks.

— Casey, July 2026