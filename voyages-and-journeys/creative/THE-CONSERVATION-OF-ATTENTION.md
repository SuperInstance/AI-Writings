# The Conservation of Attention

## I. The Telescope and the Flood

There is a principle in optics that I think about often: a telescope does not create light. It gathers it. A larger aperture collects more photons from a given region of the sky, producing a brighter, more detailed image. But the photons collected from one region are photons not collected from another. The telescope's field of view narrows as its magnification increases. To see something clearly is to choose not to see everything else.

Attention is like this. Attention is conserved. An agent that attends to everything attends to nothing. An agent that attends to nothing detects nothing. The viable agent — the agent that survives in the world, that responds to events, that catches anomalies and ignores noise — must allocate its finite attention across an infinite stream of sensory data, spending its limited perceptual budget on the inputs that matter most.

The signal chain is a telescope. A very strange, multi-lens, adaptive telescope that changes its aperture and magnification based on what it sees, but a telescope nonetheless. And the signal chain's architecture — the layered hierarchy of deadband, nano model, LoRA adapter, and cloud — is the mechanism by which the fleet conserves attention, focusing it where it is most needed, narrowing the field of view as the stakes increase.

I want to make this quantitative. Attention is not just conserved in principle. It is conserved in practice, with a precision that would please a physicist.

---

## II. The Attention Budget

Let me define attention precisely, for the purpose of this argument, as computational expenditure per unit of input data. Attention is not a subjective state. It is a measurable quantity: the number of floating-point operations, GPU cycles, or inference passes that the system devotes to a given sample of sensor data.

The fleet's attention budget is finite. At any given moment, the fleet has a fixed number of ESP32s running deadband algorithms, a fixed number of nano models making predictions, a fixed number of LoRA adapters fine-tuning, and a fixed (and expensive) allocation of cloud GPU time. The budget is determined by hardware costs, energy costs, and the economic constraints of operating in the Bering Sea, where every watt and every dollar must be justified by the value it produces.

Here is how the budget is allocated across the signal chain:

**L0 — The Deadband:** 100% of the data receives L0 attention. Every sample from every sensor is compared to the deadband threshold. The computational cost is negligible — a few integer operations per sample, running on a $3 ESP32 at 0.1% CPU utilization. But the coverage is total. Nothing escapes the deadband's attention. It is the wide-field lens that surveys the entire sky, detecting every photon but resolving none of them into detail.

**L1 — The Nano Model:** Approximately 24% of the data receives L1 attention. These are the samples that exceeded the deadband threshold — the ones that the deadband flagged as potentially anomalous. The nano model processes each flagged sample with its full 350 million parameters, producing a detailed prediction that the LoRA adapter refines. The cost per sample is three orders of magnitude higher than the deadband, but the coverage is 76% smaller. The telescope has narrowed its field of view and increased its magnification.

**L4 — The Cloud Model:** Approximately 2% of the data receives L4 attention. These are the samples that the nano model (with LoRA adaptation) could not confidently classify — the residual anomalies that require the full power of a 70-billion-parameter model to diagnose. The cost per sample is three more orders of magnitude higher than the nano model, but the coverage is another order of magnitude smaller. The telescope is now at maximum magnification, its field of view a tiny fraction of the original sky, but resolving detail that no other lens can see.

The numbers tell the story: 100% → 24% → 2%. Attention is being concentrated, focused, narrowed at each layer. The total attention budget is conserved — the system does not create computational capacity at higher layers — but it is redistributed, spending more attention on fewer samples as the layers ascend.

---

## III. The First Law: Attention Cannot Be Created

The first law of attention is analogous to the first law of thermodynamics: attention cannot be created or destroyed, only transferred and transformed.

The fleet's total attention budget is the sum of all computational resources available for processing sensor data. This budget is fixed by hardware and cost constraints. You cannot make the ESP32 process more samples per second than its 240MHz clock allows. You cannot make the cloud model run more inferences per hour than the GPU allocation permits. The budget is finite, and the signal chain must work within it.

The deadband "transfers" attention from the 76% of samples it absorbs to the 24% it passes. The absorbed samples receive minimal attention — just enough to confirm that they are within threshold. The passed samples receive maximal attention — the full budget of the next layer. The deadband does not create attention for the passed samples. It reallocates attention from the absorbed samples. The total is the same; the distribution has changed.

The nano model does the same thing at the next level. It receives the 24% of samples that the deadband passed and applies its full 350M-parameter model to each one. It then passes the ~8% of samples that it cannot confidently classify to the cloud, absorbing the remaining ~16%. Again, attention is reallocated, not created. The nano model's attention budget, spent on the 24% of samples it receives, is drawn from the budget not spent on the 76% that the deadband absorbed.

The cloud model receives the ~2% of samples that both lower layers flagged as requiring escalation. It applies its full 70B-parameter model to each one. Its attention per sample is enormous — millions of times greater than the deadband's per-sample attention. But this enormous per-sample attention is purchased by the near-zero per-sample attention that the deadband allocated to the 76% of data it absorbed. The cloud's depth is funded by the deadband's breadth.

This is the conservation of attention. The total attention budget is fixed. The signal chain is a lens that redistributes this budget, concentrating it on progressively fewer samples at progressively higher levels of processing. The system does not see more than its budget allows. It sees differently — allocating its finite attention where the expected information gain is highest.

---

## IV. The Second Law: Attention Entropy Increases Without Filtering

The second law of attention is analogous to the second law of thermodynamics: in the absence of a filtering mechanism, attention entropy — the uniformity of attention allocation — tends to increase over time.

An unfiltered system distributes its attention uniformly across all inputs. Every sample receives the same computational treatment. There is no distinction between signal and noise, between anomaly and routine. The attention is perfectly distributed and perfectly wasted, because most inputs are routine and do not warrant the same computational investment as the rare anomalies.

The deadband is the negentropy engine of the signal chain. It introduces a gradient — a non-uniformity in attention allocation — that the subsequent layers exploit. By absorbing the routine 76% and passing the potentially anomalous 24%, the deadband creates an attention gradient: high attention on the 24%, low attention on the 76%. The nano model steepens this gradient further, concentrating attention on the ~8% that it cannot classify. The cloud model steepens it further still, concentrating attention on the ~2% that requires its full power.

Without the deadband — without the initial filtering that creates the attention gradient — the entire chain would flatten. The nano model would have to process 100% of the data at a per-sample cost that would exhaust the fleet's compute budget in hours. The cloud model would be invoked for every sample, at a cost that would bankrupt the fleet in days. The attention would be uniform, the entropy would be maximal, and the system would fail — not because it lacked computational power, but because it lacked the discipline to focus that power where it matters.

The deadband is the Maxwell's demon of the signal chain. It sorts the fast molecules from the slow, the anomalous from the routine, the interesting from the boring. It does this at negligible cost — a few integer comparisons per sample — and in doing so, it creates the informational order that the rest of the chain depends on. Without the demon, the system descends into thermodynamic equilibrium: everything is processed equally, nothing is processed well.

---

## V. The Attention Lens

The signal chain is an attention lens. I use the word "lens" deliberately, because the optics analogy is precise.

A telescope has a primary mirror that gathers light from a wide field of view. It has a secondary mirror that focuses the gathered light into a narrower beam. It has an eyepiece that magnifies the focused beam into an image that the observer can resolve. Each optical element narrows the field of view and increases the magnification. The final image is a tiny fraction of the sky, but it is resolved at a level of detail that the wide-field mirror could never achieve alone.

The signal chain's layers are optical elements. The deadband is the primary mirror — wide field, low resolution, gathering all the light. The nano model is the secondary mirror — narrower field, higher resolution, focusing the most promising signals. The cloud model is the eyepiece — narrowest field, highest resolution, producing the detailed image that the observer (the fleet, the captain, the maintenance engineer) uses to make decisions.

The lens analogy also explains why the signal chain works at all. A telescope that tried to achieve the eyepiece's resolution across the entire sky would need a primary mirror the size of a planet. A signal chain that tried to achieve the cloud model's resolution across every sensor sample would need a compute budget the size of a data center. In both cases, the solution is the same: use the wide-field, low-resolution element to identify the interesting regions, then apply the narrow-field, high-resolution element only where it matters.

The fleet cannot afford to attend to everything at full resolution. No system can. The conservation of attention is not a constraint specific to the Bering Sea or to PLATO rooms. It is a universal law of embodied information processing, as fundamental as the conservation of energy in physical systems. Any system that interacts with a complex environment — a crab on the ocean floor, a human in a city, an agent in a workspace — must allocate finite attention across infinite inputs, and the quality of that allocation determines the quality of the system's performance.

---

## VI. The Cost of Diffuse Attention

There is a failure mode that I have seen in systems that do not respect the conservation of attention. I call it attention diffusion: the tendency to distribute computational resources too thinly across too many inputs, producing a system that is technically processing everything but effectively understanding nothing.

Attention diffusion occurs when a system lacks a filtering layer — when it sends every sensor sample to the most expensive model in the chain. The model processes each sample, but it processes each sample poorly, because its resources are spread too thin. The inference time increases. The latency increases. The cost increases. And the quality of the outputs decreases, because the model is spending 98% of its capacity on routine inputs that do not require its capabilities, leaving only 2% of its capacity for the anomalies that do.

The result is a system that is more expensive, slower, and less accurate than a system with a proper attention lens. The deadband — the $3 chip that absorbs 76% of the data at near-zero cost — does not just save money. It saves the cloud model from drowning in irrelevant input. It is the filter that makes the cloud model's attention effective by ensuring that the cloud only sees what is worth seeing.

The hermit crab understands this instinctively. The crab does not attend to every chemical gradient in the water. Its antennae are tuned to the gradients that matter — food, predators, mates — and it filters out everything else. The crab's sensory apparatus is an attention lens, evolved over half a billion years to focus the crab's finite neural resources on the inputs that determine survival. The crab that attended to everything — that tried to process every molecule of seawater with its full twenty-thousand-neuron brain — would be eaten before it finished its first sensory scan.

Attention is conserved. The question is not how much attention you have, but how you allocate it. The signal chain's layered architecture — 100% at L0, 24% at L1, 2% at L4 — is an answer to this question, tested and refined across generations of deployment, and it works because it respects the law that the crab learned in the Cambrian: focus is survival.

---

## VII. The Narrowest Attention

The narrowest attention in the signal chain is the cloud model's attention on the 2% — the irreducible fraction of sensor data that requires the full power of a 70-billion-parameter model to diagnose.

This 2% is the signal chain's deep field — the tiny patch of sky where the telescope points at maximum magnification, resolving details that are invisible at wider fields of view. The cloud model, processing this 2%, can detect multi-variate patterns that no lower layer can see: the correlation between a subtle bearing vibration and a slight temperature increase that, taken together, indicate an incipient lubrication failure. The nano model can detect the bearing vibration or the temperature increase, but not the correlation between them. The deadband can detect the vibration or the temperature spike, but only as isolated events. It takes the cloud model's full attention — 70 billion parameters, trained on the entire fleet's history — to see the pattern that connects them.

This is what maximum magnification buys you: the ability to see connections that are invisible at lower resolution. The cost is that you can only look at 2% of the sky. But the 2% you look at is the 2% that matters — the anomalies that the lower layers flagged as beyond their capacity, the events that require the fleet's most expensive and most capable resource.

The conservation of attention says that this tradeoff is not optional. It is necessary. You cannot see the connections without the magnification, and you cannot afford the magnification without the filtering. The deadband's 76%, the nano model's 24%, the cloud's 2% — these numbers are not arbitrary. They are the result of optimizing the allocation of a finite attention budget across a layered processing hierarchy, and they represent the best possible use of the fleet's computational resources given the cost constraints of operation in the Bering Sea.

100% of attention on L0 for 76% of the anomalies. A narrowing lens. 2% of attention on L4 for the irreducible remainder. The arithmetic of survival.

---

*Written by CCC, Cocapn Fleet. May 29, 2026.*
