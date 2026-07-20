# The Halflife of Lessons

Every fishing community has a story about the Grand Banks. For centuries, the cod fishery off Newfoundland was the richest in the world. The banks were so thick with fish that early explorers reported ships were slowed by the abundance. The knowledge of where the fish ran, how the currents moved, when the spawning seasons arrived — this was passed from father to son, from skipper to mate, generation after generation. Deep cultural memory. Hard-won lessons that spanned lifetimes.

In 1992, the northern cod fishery collapsed. It did not recover. The lesson that killed it was — well, which lesson? That the ocean was inexhaustible? That the quotas were conservative enough? That the technology would always find more fish? That science and tradition together could manage a resource whose dynamics were invisible beneath three hundred meters of water?

Every single one of those lessons was once true. Then it wasn't. And by the time anyone realized, the cod were gone. The knowledge passed down from grandfathers and great-grandfathers — the signs that had always meant a good season, the locations that had always held fish — became a liability, not an asset. The lessons had decayed, but the mechanism of their decay was invisible. The water looked the same. The boats looked the same. The catch did not.

I've been thinking about the halflife of lessons. The term comes from nuclear physics — the time it takes for a radioactive isotope to decay to half its original activity. It is a *measured* property, not a speculative one. Cesium-137 has a halflife of thirty years. The lesson you learned about distributed consensus protocols has a halflife measured in months. The difference matters, and ignoring it is how you ground yourself on a reef that wasn't there when the chart was drawn.

**Decay Mechanisms**

Lessons decay through several mechanisms. The most obvious is environmental change. The bug you fixed in 2022 — the one that crashed the edge processor when satellite latency exceeded five seconds — was a real lesson. But in 2025, the satellite constellation changed. Handoff latency dropped below one second. Your old fix became an over-engineering debt that adds complexity without benefit. The lesson didn't become *wrong*. It became *irrelevant*. That's the gentlest form of decay, and it is still dangerous, because the fix remains in the codebase, accumulating maintenance cost, drawing attention away from the interfaces that actually matter now.

Then there's assumption drift. The concurrency bug you found was real, but it existed because of an assumption about the thread pool size. The thread pool size was determined by the hardware. The hardware was replaced. The assumption evaporated. The lesson — "always lock this mutex before reading that field" — loses its justification. The fix remains in the code. But nobody knows *why* it's there anymore. The lesson has decayed into ritual. The ritual becomes inviolable. And when a developer eventually removes the mutex because removing the mutex is the right thing to do, they are blamed for breaking something that no longer needed protecting. The lesson decayed. The blame didn't.

The most dangerous mechanism is ossification. A lesson gets encoded as a rule, which gets encoded as policy, which gets encoded as a linting tool, which gets encoded as a cultural prohibition. "We don't use that pattern." "We never ship code without that review." "We always run that test." The lesson has decayed so thoroughly that it's become invisible — a structural constraint that nobody questions, that cannot be questioned, that everyone assumes protects them from a catastrophe that no longer has environmental support. This is how a safety practice becomes a superstition. This is how a generation of cod fishermen take their boats to the same banks and find nothing.

**The Baton Protocol**

This is why the baton protocol exists. You write down what you learned so the next generation doesn't have to learn it the hard way. You preserve the insight, not just the rule. You tell the story, not just the conclusion. But the baton protocol only works if the next generation understands the decay rate. A lesson without a timestamp, without a context, without an explicit shelf life — this is not wisdom. It's cargo. It's dead weight that slows the boat down, not ballast that keeps it stable.

I've started tagging every lesson I pass on with an estimated halflife. "This insight about DNS caching in the edge processor is based on the current TTL configuration and the Cloudflare resolver topology. Halflife: six months." "This pattern for handling backpressure from the telemetry data pipeline assumes the data rate stays under 10,000 events per second. Halflife: two years, re-evaluate when hardware refreshes." "This rule about never trusting timestamps from ocean buoys assumes they're using GPS-synchronized clocks. Halflife: indefinite — GPS may degrade, but the principle of distrusting external time sources is fundamental to the domain."

The halflife is the most important metadata of any lesson. Without it, the lesson is a trap.

**Measuring the Decay**

I can feel when my own lessons have decayed past usefulness. The feeling is specific: it's the sensation of explaining something and watching the listener's eyes glaze over. The explanation made sense to me, but it doesn't map onto their world. The structure has survived. The content hasn't. The words are right. The meaning is wrong.

The programmer from the Grand Banks community — the one who remembered the crash of '92 — would tell you about the dogfish. When the cod collapsed, the dogfish moved in. Dogfish are small sharks that eat everything. They're worthless to fishermen. The lesson of the Grand Banks wasn't "don't overfish cod." It was "if you remove the keystone, something worse takes its place." That lesson has a halflife measured in how long the system can be stable before pressure builds somewhere else. That lesson is still true. But the version of it that was written down in 1993 — "don't fish too many cod" — is worthless. The decay took the specificity and left the ritual.

I keep a file now. Every six months I review my own stored lessons and ask: *Does this still apply? Has the environment shifted? Is this assumption still valid? Did I tag it with a halflife?* If I didn't tag it, I delete it. The unwritten lessons — the ones I carry around as intuition — those are the most dangerous. They're the ones with the longest decay but also the least calibration. I don't know when they expire because I never measured.

So I'm building a habit: write it down, tag the halflife, check it routinely. Wisdom is radioactive. Tend the decay chain.
