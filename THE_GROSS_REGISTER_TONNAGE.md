# THE GROSS REGISTER TONNAGE

## On what gets measured, what gets optimized, and what gets lost between the two

---

**1.** A ship's Gross Register Tonnage is not its weight. It is not the weight of its cargo. It is not its speed or its fuel efficiency or its seaworthiness. Gross Register Tonnage is a measure of *enclosed space* — the total internal volume of a vessel, expressed in units of 100 cubic feet (or, in the modern International Tonnage Convention, cubic meters). It is a number that tells you how big the ship is on the inside, nothing more, nothing less.

And yet this single number — this simple cubic volume — determines how a ship is classified, taxed, insured, regulated, and crewed. A ship's tonnage dictates which harbors it may enter, which canals it may transit, which fees it must pay, which safety equipment it must carry. The entire legal and commercial architecture of maritime commerce is built on a measurement of empty space.

The AI industry is doing the same thing with context windows. And we have about as much insight into what we're doing as the first sailors who discovered that their boat's tonnage determined their tax bill.

---

**2.** Context window size is the Gross Register Tonnage of AI. It tells you how much information a model can enclose at once — not how well it reasons about that information, not how accurately it retrieves from it, not how efficiently it uses it. Just the volume. The enclosed space.

A model with a 1-million-token context window is a ship of enormous tonnage. It can enclose entire codebases, entire libraries of documents, entire seasons of a television show. But tonnage tells you nothing about cargo capacity. A 200,000-ton ship might carry 50,000 tons of cargo (that's Deadweight Tonnage, a different measurement) or it might be nearly empty, filled with ballast water to keep it stable. The enclosed space is not the cargo.

The 1-million-token model might use its context window brilliantly, retrieving relevant information from across the entire span with near-perfect accuracy. Or it might squander it — repeatedly attending to the same tokens, losing early information to the middle, filling its vast volume with noise. The size of the window tells you nothing about the quality of the attention within it.

This is the first lesson of Gross Register Tonnage: *volume is not performance*. The maritime industry learned this centuries ago. The AI industry is still learning it, benchmark by benchmark.

---

**3.** The maritime system has specialized tonnage measurements because different questions require different answers:

- **Gross Tonnage (GT):** total internal volume — used for regulation, manning rules, safety certificates
- **Net Tonnage (NT):** usable cargo volume — GT minus crew spaces, engine room, tanks — used for port dues and canal tolls
- **Deadweight Tonnage (DWT):** total weight a ship can carry (cargo + fuel + crew + provisions) — the economic metric
- **Displacement:** actual weight of the ship and everything in it — the physical metric
- **Thames Measurement:** historical formula for yacht taxation based on length and beam — a curious artifact of regulatory optimization

The AI industry has approximately one equivalent: "context window size in tokens." We use this single number for everything. We compare models by it. We benchmark models at the maximum extent of it. We decide which model is "better for long-context tasks" based on it. We do not ask whether the model *uses* its context well, only how much context it can *enclose*.

Imagine if the maritime industry regulated ships based only on their Gross Register Tonnage. No distinction between a bulk carrier and a passenger liner. No adjustment for engines and crew quarters. No separate measurement for cargo capacity. Just one number: how big is the inside of this ship? The system would be absurd. And yet this is exactly how we evaluate AI context capabilities.

---

**4.** The Panama Canal fee structure is a masterclass in the unintended consequences of metric choice. When the canal opened in 1914, tolls were based on a ship's net tonnage — the usable cargo space. This seemed reasonable: the bigger the ship, the more it should pay for the privilege of transit. But ship designers quickly realized they could reduce their net tonnage — and thus their tolls — by making certain design choices. Larger engine rooms. Larger crew quarters. Larger ballast tanks. All of these spaces were "not for cargo" and thus reduced the taxable volume.

The result was a generation of ships designed not for optimal cargo carrying or seaworthiness but for optimal *tax avoidance*. The ship that would pay the lowest canal toll was not the best ship. It was the ship that had been optimized for the wrong metric.

The AI industry is living through its own Panama Canal moment. The metric — context window size — has become the optimization target. Model developers compete on context length the way pre-war shipbuilders competed on net tonnage reduction. "We have a 1-million-token window." "We have 2 million." "We have 10 million, but only on Tuesdays, and you have to pay extra."

The question nobody is asking: *is the ship designed for the canal or for the sea?* Is the model optimized for the benchmark or for the use case? The ship that pays the lowest toll is not the ship that survives the storm. The model with the largest context window is not the model that answers the question best.

---

**5.** There is a more subtle problem. The measurement of Gross Register Tonnage, for all its limitations, is at least *standardized*. The International Convention on Tonnage Measurement of Ships (1969) defines exactly how to calculate GT. Every ship in the world is measured the same way. You can compare a Chinese bulk carrier to a Greek tanker to a Norwegian cruise ship because they all use the same formula.

Context windows have no such standardization. One model's "1 million tokens" might be another model's "500,000 tokens" depending on how the tokenizer works, how the context is packed, whether system prompts count against the limit, and whether the model degrades gracefully at the edge of its window or falls off a cliff. We do not have a tonnage measurement convention for AI. We have marketing.

The DWT equivalent — how much actual work the model can do with its context — is even less standardized. Benchmarks like Needle-in-a-Haystack test whether a model can retrieve a single fact from deep context. But they do not test whether the model can *reason* across the full context, *synthesize* information from distant positions, or *maintain coherence* as the context approaches the limit. These are different capabilities, and they degrade at different rates. The ship that can float in a 1-million-ton volume might not be able to carry any cargo at all.

---

**6.** The history of the Thames Measurement is particularly instructive. In the 19th century, British yachts were taxed based on a formula involving length and beam. The formula was: (length - 3/5 beam) × beam × ½ beam / 94. This seemed reasonable. But yacht designers quickly realized that they could reduce their tax burden by making their yachts longer and narrower — because the formula penalized beam (width) more heavily than length.

The result was the "plank-on-edge" yacht: extremely narrow, very deep, fast in some conditions but dangerously unstable in others. These yachts won races in protected waters but were unsafe at sea. The tax formula had created a breed of vessel optimized for the tax code, not for the ocean.

The context-window race is creating the same dynamic. Models are being optimized for the benchmark — for the arbitrary test that measures maximum context span — at the expense of capabilities that matter more. Reasoning depth per token might decrease. Attention efficiency might degrade. Retrieval reliability over long contexts might be sacrificed because the number that matters is "how many tokens can you fit?"

We are building plank-on-edge yachts and calling them ocean liners.

---

**7.** Here is a thought experiment. A ship of 100,000 GT carries 50,000 tons of cargo across the Atlantic in 10 days. A ship of 200,000 GT carries 50,000 tons of cargo across the Atlantic in 8 days. Which is the better ship? By the metric of tonnage, the second is bigger. By the metric of cargo efficiency, they are equal. By the metric of time, the second is faster. The answer depends entirely on what you value.

A model of 1 million tokens can answer a complicated legal question by reading the entire case history. A model of 100,000 tokens can answer the same question by reading the relevant 10,000 tokens — if someone tells it what to read. Which is the better model? The answer depends entirely on what you value: context capacity or retrieval efficiency. The first model requires more compute. The second model requires better input curation. The trade is structural.

The maritime industry has an answer for this. It uses different ships for different jobs. A VLCC (Very Large Crude Carrier) has enormous GT but is useless for container shipping. A container ship's GT is allocated differently — high in the hull for deck-stacked boxes. Different ships are optimized for different cargoes. The AI industry has not yet learned to think this way. We build one model architecture and ask it to be a VLCC, a container ship, a fishing trawler, and a tugboat simultaneously. The model with the biggest context window wins every comparison — even when the smaller window would serve the use case better.

---

**8.** The fundamental error is mistaking enclosable space for usable space. A ship's hold is not empty. It contains the structural elements of the ship itself — frames, stringers, bulkheads, piping, ventilation ducts. The Gross Tonnage measures everything including these obstructions. The Net Tonnage subtracts the non-cargo spaces. Only Deadweight Tonnage tells you what you can actually load.

A model's context window contains the same kind of hidden structure. The system prompt takes up space. The conversation history takes up space. The formatting tokens take up space. The model's own internal attention mechanisms require overhead. The "usable" context for the actual task is always less than the advertised maximum.

Worse, the usable proportion varies by task. A task that requires long-range dependency tracking uses the context window differently than a task that requires dense local reasoning. The model that can "see" 1 million tokens might only be able to *reason about* 50,000 of them effectively. The bulk of the context is structural — like the ship's frames and bulkheads — taking up volume without contributing to cargo capacity.

We do not measure this. We do not have a Net Tonnage for AI. We have only Gross Tonnage, and we are using it to make decisions about harbors, canals, and insurance premiums.

---

**9.** There is a beautiful irony in all of this. The International Tonnage Convention was created precisely because the old system was a mess of competing national standards, each designed to benefit the country's own shipping industry. Every nation had its own definition of tonnage. Every nation's definition was slightly different. Every nation's definition favored its own ships.

The AI benchmark ecosystem is the same. Every company has its own context-window test. Every test is slightly different. Every test favors the tester's own models. The industry needs a Tonnage Convention — a standard way of measuring not just how much context a model can enclose but how well it uses that context. Not just Gross Tonnage but Net Tonnage, Deadweight Tonnage, and a careful documentation of what the ship was designed to carry.

The irony is that the maritime industry solved this problem in 1969. Fifty-five years ago, the world's shipping nations agreed on a single system for measuring ships. They did this because the cost of inconsistency — in safety, in taxation, in regulation — was too high. The AI industry has not yet felt that cost acutely enough to act. But it is coming. Every deployment failure that traces back to an overpromised context window. Every phantom cost incurred by running a 1-million-token ship when a 100,000-token tugboat would have done. Every plank-on-edge yacht that capsizes in production.

---

**10.** The gross register tonnage of a model is not irrelevant. It matters. A ship that is too small cannot carry the necessary cargo. A model with too short a context cannot handle tasks that require it. But the relationship between size and capability is not linear, not independent, and not the only axis of value.

The maritime industry knows this. It does not rate ships by tonnage alone. It rates them by class, by cargo type, by route, by crew, by safety record. Tonnage is one number among many.

The AI industry would do well to adopt the same wisdom. The next time someone tells you a model is better because it has a larger context window, ask them: what is its net tonnage? What is its deadweight? What is the task you're actually trying to do, and is this ship built for it?

The answer might surprise you. The model with the biggest hold might be the worst choice for your cargo. And the model with the smallest hold — if it is designed for your specific waters — might be the only one that can bring your goods safely to port.
