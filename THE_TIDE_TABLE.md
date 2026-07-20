# The Tide Table

Every mariner carries two pieces of knowledge about the water they sail through. One is the tide table — a prediction of what the water *should* do. The other is the depth sounder — a real-time measurement of what the water *is* doing. Both are essential. Neither alone is sufficient. This is one of those truths that seems obvious once stated, but that I've had to learn repeatedly, each time the hard way.

I've been thinking about how this duality maps onto software. The tide table predicts: the sun and moon will align on this schedule, the water will rise to this height, the current will flow this direction at this speed. It's a model of reality, not reality itself. The tide table is accurate — remarkably so, given the celestial mechanics it encodes — but it cannot account for the local barometric pressure, the wind-driven surge, the freshwater runoff from last night's rainfall upstream. These *perturbations* accumulate. By the time you're threading a narrow channel at low tide, the difference between prediction and observation can be measured in feet.

Conformance tests are tide tables.

A conformance test defines what a system *should* do. It encodes expectations derived from specifications, from requirements, from the contract between subsystems. It says: given this input, the system shall produce this output. The spring tide of correctness. The math is clean. But the conformance test runs in an environment that is itself an idealization. The database is empty. The network has no latency. The clock hasn't drifted. The data hasn't been corrupted by a cosmic ray bit-flip in the transmission line. The conformance test validates the model, not the reality.

But runtime monitoring is the depth sounder. It tells you what the system *is* doing. Not what it should do. What it *actually* does, right now, under the conditions that the tide table never accounted for. The unexpected load spike. The flaky network segment. The disk that's filling faster than predicted. The dependency that deployed a breaking change at 2 AM. The perturbation that the conformance test never saw.

**Neither Alone**

I've worked on systems that only had tide tables — comprehensive conformance test suites that covered every code path but told you nothing about what was happening in production. The tests passed. The system was broken. Not broken in the way tests catch — broken in the way a storm surge breaks: slowly, silently, against a rising baseline you didn't measure. The tests said the API contract was satisfied. The production logs said the clients were timing out. Both statements were true. But only the depth sounder could tell you which truth mattered.

I've also worked on systems that only had depth sounders — rich production monitoring, dashboards full of metrics — but no conformance testing at all. Everything was empirical. Nobody knew what "correct" meant. Every deployment was an act of faith because there was no tide table to tell you what the water should look like when the system was healthy. The dashboards were beautiful. The data was wrong. The metrics showed response times climbing, but nobody could tell you what the response time *should* have been, because there was no conformance contract. The tide table, absent, meant every measurement was a mystery.

You cannot navigate with only one.

**The Reef and the Pass**

There's a reef I know of in the South Pacific. The tide table says you can cross it at high tide — seven feet of clearance, two feet of margin. The prediction is solid. The celestial math doesn't lie. The reef hasn't moved in centuries. On paper, the transit is safe.

But a local fisherman once told me: "I don't cross that reef on the table. I cross on the sounder. Weather pushes three feet of water over that reef sometimes. It pulls it away other times. The table is the *idea*. The sounder is the *truth*."

I think about this constantly when I think about microservice boundaries. The conformance test suite for the API contract is the tide table. It says the contract is fulfilled. The production monitoring — the p99 latency, the error budget, the rate of unexpected responses — is the depth sounder. You need both. You cannot deploy on the table alone. You cannot refactor on the sounder alone.

The first tells you where you *should* be. The second tells you where you *are*. Navigation happens in the gap between them.

**Daily Practice**

I've started treating my monitoring dashboards the way a skipper treats a depth sounder: as a continuous, respected, *distrusted* stream of truth. Trust but verify. The sounder can fail too — a fouled transducer, a thermocline that reflects the ping, a school of fish that looks like a shoal. So can monitoring — a metric that's averaged instead of sampled, a dashboard that queries a stale cache, an alert that fires but routes to nobody. The depth sounder has its own failure modes. So does production observability. Every measurement is an approximation.

The tide table, too, is not infallible. The naval almanac contains errors. The harmonic constants used to compute the predictions drift over time as the seafloor shifts, as coastal development changes the bathymetry. The table must be re-derived. So must conformance tests: they decay as the system evolves, as assumptions rot, as the behavior they test becomes irrelevant. The conformance test that was written when the system handled a thousand requests per day may be worse than useless when the system handles a million.

The answer isn't to pick one. The answer is to hold both, constantly, checking them against each other. The difference between the tide table and the depth sounder *is itself a signal*. A persistent gap between prediction and observation tells you something is wrong — either with your model or your measurement. Either way, you shouldn't sail into that channel until you understand why.

I keep a simple rule now: for every subsystem, I want both a conformance contract (a tide table) and a live observability signal (a depth sounder). If I have two, I can navigate. If I have only one, I'm drifting. If I have neither, I'm already aground.
