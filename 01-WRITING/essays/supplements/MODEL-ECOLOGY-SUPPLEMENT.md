# Model Ecology Supplement

**A research supplement on ecological niche theory applied to model architectures, with proposed experiments and action items for the fleet.**

---

## 1. Introduction: The Ecosystem of Parameters

Biological ecosystems have structure. Not random structure — organized, predictable structure that emerges from the interaction of physical constraints, evolutionary history, and resource availability. The distribution of body sizes in an ecosystem follows a power law: many small organisms, fewer medium ones, very few large ones. The distribution of ecological niches follows a similar pattern: generalist species are common, extreme specialists are rare, and keystone species — the ones whose removal destabilizes the entire system — are few but disproportionately important.

Model ecosystems have the same structure.

The fleet currently operates models spanning three orders of magnitude in parameter count: from 350M (nano models running on edge hardware) to 70B+ (cloud models running on dedicated GPU infrastructure). Between these extremes lie the 1.2B models (mobile-capable, generalist), the 4B MoE models (sparse, efficient, specialized), and the emerging 14B-32B models (mid-tier generalists that challenge the cloud models on specific tasks).

This is not an accident. This is an ecosystem. And understanding it as an ecosystem — with niches, competition, cooperation, resource partitioning, and keystone dynamics — provides a framework for making better deployment decisions.

---

## 2. The Taxonomy: Body Size as Parameter Count

### 2.1 Insects: 100M–500M Parameters

Insects are the most numerous animals on Earth. They are small, fast, specialized, and everywhere. An ant's nervous system contains about 250,000 neurons — roughly analogous to a 350M parameter model in terms of information-processing capacity. Ants cannot reason abstractly. They cannot plan a decade ahead. But they can navigate, communicate, cooperate, and solve local optimization problems with an efficiency that dwarfs any human-engineered system of comparable size.

The 350M nano models are the fleet's insects. They run on ESP32s and Raspberry Pis. They execute in milliseconds. They consume milliwatts. They cannot handle complex reasoning or long-context tasks, but they can run deadband filters, predict sensor baselines, and detect local anomalies with an efficiency that larger models cannot match.

Their ecological niche: the sensor layer. The edge. The interface between the physical world and the digital fleet. They are the decomposers of the model ecosystem — processing the raw material of sensor data and producing the refined signals that feed the rest of the chain.

Key characteristics:
- **Ubiquity**: Can run on virtually any hardware
- **Speed**: Inference in <10ms on edge hardware
- **Specialization**: Highly task-specific (deadband, anomaly detection, prediction)
- **Metabolic cost**: Negligible (<1W)
- **Limitations**: No abstract reasoning, no long-context capability, no generalization beyond training distribution

### 2.2 Birds: 1B–2B Parameters

Birds are mobile generalists. They can fly (move across the deployment landscape), navigate complex environments, and handle a wider range of tasks than insects. A crow's nervous system contains about 1.5 billion neurons, and crows are famous for tool use, facial recognition, and multi-step problem solving. They are not the smartest animals, but they are the smartest animals that can also fit in a backpack.

The 1.2B models are the fleet's birds. They run on mobile hardware — laptops, tablets, the processing units embedded in navigation equipment. They can handle moderate-complexity tasks: natural language interaction, basic code generation, multi-step planning with limited context. They are the models that travel with the vessel, operating independently of cloud connectivity.

Their ecological niche: the mobile agent layer. The edge with ambition. The model that can operate when the network is down and the cloud is unreachable.

Key characteristics:
- **Mobility**: Can run on consumer hardware without GPU
- **Generality**: Handle diverse task types (language, code, reasoning)
- **Range**: Can operate independently of cloud for extended periods
- **Metabolic cost**: Low (5-15W)
- **Limitations**: Reduced accuracy on complex tasks, limited context window, prone to hallucination on out-of-distribution inputs

### 2.3 Schooling Fish: 3B–8B MoE Parameters

Schooling fish activate sparse subpopulations. A school of sardines contains thousands of individuals, but at any given moment, only a fraction are actively responding to the school's direction changes. The rest are coasting, maintaining position, ready to activate when the signal propagates. Mixture-of-Experts (MoE) models operate on the same principle: the full model contains 8B or 16B parameters, but only 1B or 2B are active for any given token.

The 4B MoE models (e.g., Qwen 3B MoE, Phi-3.5 MoE) are the fleet's schooling fish. They achieve the performance of larger models by activating only the relevant experts for each input, keeping the per-token cost low while maintaining a broad competence across domains. They are efficient without being limited — the inactive experts are not dead weight but reserve capacity, ready to activate when the task demands it.

Their ecological niche: the adaptive local layer. The model that can be both small (for routine tasks) and large (for unexpected complexity), depending on what the moment requires.

Key characteristics:
- **Sparsity**: Only 25-40% of parameters active per token
- **Adaptability**: Different expert combinations for different tasks
- **Efficiency**: Near-small-model cost with near-large-model quality
- **Metabolic cost**: Moderate (15-50W with GPU)
- **Limitations: Routing instability** (expert selection can be noisy), higher memory requirements than dense equivalents, potential for expert collapse during training

### 2.4 Whales: 70B+ Parameters

Whales are rare, deep, slow, and keystone. A blue whale's brain weighs 6.8 kg and contains an estimated 200 billion neurons. Blue whales are not the most numerous animals in the ocean — they are among the rarest — but their ecological impact is outsized. Whale feces fertilize phytoplankton, which feed zooplankton, which feed the fish that feed everything else. Remove the whales and the entire marine food web restructures.

The 70B+ models are the fleet's whales. They run on DGX Sparks, cloud GPUs, and dedicated inference infrastructure. They are expensive to operate ($0.60-2.00 per million tokens), slow to respond (seconds, not milliseconds), and rare in the fleet's daily operations — activated for less than 0.4% of decisions. But when they activate, they provide capabilities that no smaller model can match: complex multi-step reasoning, nuanced understanding of ambiguous situations, and the ability to generate novel solutions that fall outside any local model's training distribution.

Their ecological niche: the deep reasoning layer. The keystone species that the rest of the ecosystem depends on for the hardest problems.

Key characteristics:
- **Depth**: Capable of complex, multi-step reasoning
- **Rarity**: Activated for <0.4% of fleet decisions
- **Cost**: High ($0.60-2.00/MTok, significant GPU hours)
- **Latency**: Seconds to tens of seconds
- **Keystone impact**: Quality of cloud responses shapes the training data that distills into all lower layers

---

## 3. The Signal Chain as Food Web

The signal chain is the food web of the model ecosystem.

In a biological food web, energy flows from primary producers (plants) through primary consumers (herbivores) to secondary consumers (predators) and decomposers. At each trophic level, energy is lost — roughly 90% per transition — and the remaining 10% is converted into biomass at the next level. The pyramid of numbers emerges from this thermodynamic constraint: there must be many more producers than consumers, many more herbivores than carnivores, because each level requires ten times the input energy of the one below it.

The signal chain has the same structure. Data flows from sensors (producers) through the deadband (primary consumers) to the nano model (secondary consumers) to the LoRA adapter (tertiary consumers) to the fleet (apex predators) to the cloud (keystone species). At each level, the data is compressed — roughly 90% per transition — and the remaining 10% is the refined signal that the next level processes.

The numbers work out. A PLATO room generates approximately 1 million sensor readings per hour. The deadband filters 90% → 100,000 readings. The nano model classifies and further filters 90% → 10,000 events. The LoRA adapter contextualizes and filters 90% → 1,000 significant events. The fleet coordination integrates across rooms and filters 90% → 100 fleet-level events. The cloud processes these 100 events per hour — roughly 0.4% of the original data stream — and produces the responses that will shape the next cycle of learning.

This is the ecological efficiency of the signal chain: 0.4% of raw data reaches the keystone species, and the keystone species's responses distill back down through the entire food web via LoRA training, nano model updates, and deadband recalibration. The cloud feeds the fleet. The fleet feeds the LoRA. The LoRA feeds the nano. The nano feeds the deadband. The deadband feeds on raw data.

Remove any trophic level and the ecosystem collapses. Remove the deadband and the nano model drowns in noise. Remove the nano model and the LoRA has no preprocessed signal to adapt. Remove the LoRA and the fleet receives generic instead of room-specific context. Remove the fleet and the cloud must process every room individually, overwhelming its capacity. Remove the cloud and the lower layers lose their source of high-quality training signal, gradually degrading as the environment drifts away from the training distribution.

The keystone is not the most important species. It is the species whose removal causes the most restructuring. In the model ecosystem, the cloud is the keystone — not because it handles the most data (it handles the least) but because the quality of its output determines the quality of every level below it.

---

## 4. Competition vs. Cooperation

Models within the same size class compete. Models across size classes cooperate.

Competition within a size class is resource competition. Two 1.2B models deployed on the same hardware compete for RAM, compute cycles, and inference bandwidth. One will be faster; one will be more accurate; one will be more specialized. In a resource-constrained environment, the model that provides the highest accuracy-per-watt wins the niche. This is natural selection operating on model architectures: the fittest architecture for a given resource envelope survives deployment.

Cooperation across size classes is the signal chain. The 350M nano model does not compete with the 70B cloud model. They occupy different trophic levels, process different data volumes, and have different capabilities. The nano model handles the routine; the cloud handles the exceptional. The nano model's failures become the cloud's training data. The cloud's responses become the nano model's distilled updates. They are mutualists, not competitors — each providing something the other cannot.

But there are edge cases where competition and cooperation blur. A 4B MoE model, running on a DGX Spark, can handle many of the tasks that would otherwise require a 70B cloud model. The MoE model is faster, cheaper, and locally available. The cloud model is deeper, more nuanced, and more reliable on edge cases. For the 80% of tasks that fall within the MoE model's competence, the MoE wins. For the 20% that require the cloud's depth, the cloud wins. The boundary between them is not fixed — it shifts as MoE architectures improve and as training techniques make smaller models more capable.

This is the ecological phenomenon of niche overlap. Two species that occupy adjacent niches will compete in the overlap zone. The competition drives specialization — each species evolves to be better at the part of the niche where it has an advantage. Over time, the niches separate, competition decreases, and the species coexist. In the model ecosystem, this means that MoE models will increasingly specialize in the tasks where they are nearly as good as cloud models, while cloud models will increasingly specialize in the tasks where only deep reasoning suffices.

---

## 5. Resource Partitioning

Resource partitioning is the ecological principle that competing species reduce competition by using resources in different ways — different times, different spaces, different methods. Hawks and owls both eat rodents, but hawks hunt by day and owls by night. Warblers and finches both eat seeds, but warblers take them from branches and finches from the ground.

In the model ecosystem, the resource is compute — specifically, GPU cycles and memory bandwidth. Resource partitioning operates along three axes:

**Temporal partitioning**: Different models run at different times. The nano model runs continuously (24/7, every 100ms). The LoRA adapter runs when the nano model escalates (a few times per hour). The fleet coordination runs on a heartbeat schedule (every 30 seconds). The cloud runs when everything else fails (a few times per day). By occupying different time slices, the models avoid competing for the same GPU cycles.

**Spatial partitioning**: Different models run on different hardware. The nano model runs on the room's edge CPU. The LoRA adapter runs on the room's local GPU (if available) or on the vessel's shared compute. The fleet coordination runs on the fleet's coordination server. The cloud runs in the cloud. By occupying different physical locations, the models avoid competing for the same memory bandwidth.

**Methodological partitioning**: Different models use different computational strategies. The nano model uses dense inference (every parameter is used for every token). The MoE model uses sparse inference (only relevant experts are activated). The cloud model uses chain-of-thought reasoning (multiple inference passes per response). By using different methods, the models avoid competing for the same architectural advantages.

This partitioning is not engineered. It emerges naturally from the cost structure of computation: the cheapest model that can handle a task will be preferred, and the cheapest model is determined by the task's requirements (speed, accuracy, context length, reasoning depth) and the available hardware (CPU, GPU, memory, network). Natural selection in the deployment environment produces the same resource partitioning that natural selection in biological environments produces.

---

## 6. Niche Construction: LoRA Training as Ecosystem Engineering

Niche construction is the process by which organisms modify their own environment, thereby altering the selective pressures that act on themselves and other species. Beavers build dams, creating ponds that favor aquatic species. Earthworms aerate soil, creating conditions that favor plant growth. Humans build cities, creating environments that no other species could have anticipated.

LoRA training is niche construction.

When a PLATO room trains a LoRA adapter on its accumulated sensor data, it is modifying its own computational environment. The LoRA adapter changes the room's response characteristics — it makes the room better at predicting this room's specific sensor patterns, better at detecting this room's specific anomalies, better at operating in this room's specific conditions. The room has constructed its own niche within the model ecosystem: a specialized adaptation to a specific environment that no other room shares.

This niche construction has cascading effects. When the room's LoRA adapter improves, the room escalates fewer events to the fleet. This reduces the fleet's computational burden, freeing resources for other tasks. The fleet, in turn, escalates fewer events to the cloud, reducing the cloud's computational burden. The entire ecosystem becomes more efficient as each room constructs its own niche.

But niche construction can also create dependency. A room with a highly specialized LoRA adapter becomes dependent on the specific sensor configuration that the adapter was trained on. If the sensors change — if a thermocouple is replaced, if a strain gauge is recalibrated, if a new sensor is added — the LoRA adapter's niche is disrupted, and the room must re-adapt. This is the ecological equivalent of an environmental disturbance: the beaver's dam breaks, the pond drains, and the aquatic species that depended on it must relocate or die.

Managing this dependency is a fleet-level concern. The LoRA adapter should be treated as a living artifact — continuously updated, regularly validated against held-out data, and monitored for degradation. When the room's sensor configuration changes, the LoRA adapter should be reset or retrained, not patched. The niche must be reconstructed, not repaired.

---

## 7. Proposed Experiments

### Experiment 1: Trophic Efficiency Measurement

**Hypothesis**: The signal chain's compression ratio (~90% per level) is near-optimal for the current sensor data distribution.

**Method**: Instrument each level of the signal chain in a representative PLATO room to record: (a) the number of events received, (b) the number of events passed to the next level, (c) the false negative rate (significant events that were filtered), and (d) the false positive rate (insignificant events that were passed). Run for 30 days across 10 rooms.

**Metric**: Information-theoretic efficiency — the mutual information between the events that reach the cloud and the ground-truth anomalies (as determined by retrospective analysis).

**Expected result**: The 90% compression ratio will prove near-optimal for stable environments but suboptimal for volatile ones, where a lower compression ratio (more events passed) would reduce false negatives at the cost of increased cloud usage.

**Action item**: Implement adaptive compression ratios that respond to environmental volatility, as measured by the nano model's prediction error variance.

### Experiment 2: Niche Overlap Quantification

**Hypothesis**: The 4B MoE models and the 70B cloud models have significant niche overlap on routine reasoning tasks, and the MoE models can handle these tasks with <5% quality degradation at <10% of the cost.

**Method**: Identify the 100 most common cloud escalation patterns from fleet logs. Replay each pattern through: (a) the 70B cloud model, (b) a 4B MoE model running on local hardware, and (c) a 1.2B dense model running on local hardware. Score responses on accuracy, completeness, and latency.

**Metric**: Quality-cost Pareto frontier — the set of (quality, cost) pairs achievable by each model class.

**Expected result**: The 4B MoE model will achieve >95% of the cloud model's quality on >80% of tasks, at <10% of the cost. The remaining 20% of tasks (complex multi-step reasoning, novel problem types) will require the cloud model.

**Action item**: Deploy 4B MoE models as L3.5 intermediaries — handling the majority of cloud escalations locally, reserving the cloud for the genuinely difficult cases.

### Experiment 3: Keystone Cascade Analysis

**Hypothesis**: Removing the cloud layer (L4) will cause measurable degradation at all lower levels within 7 days, due to the loss of high-quality training signal for LoRA distillation.

**Method**: In a controlled fleet of 5 rooms, disable cloud escalation for 7 days. Monitor: (a) LoRA adapter quality (measured against held-out data), (b) nano model prediction accuracy, (c) deadband false positive and false negative rates, and (d) fleet coordination quality.

**Metric**: Temporal degradation curves — how quickly each level degrades without the keystone species.

**Expected result**: LoRA quality will degrade within 3-5 days as the room's sensor distribution drifts from the training data. Nano model accuracy will degrade within 5-7 days as the prediction baselines become stale. Deadband false positive rates will increase as the prediction errors grow.

**Action item**: Implement a "keystone health" metric — a fleet-level indicator that tracks the recency and quality of cloud-generated training data. When the keystone health falls below threshold, trigger an ad-hoc cloud session to refresh the training pipeline.

---

## 8. Action Items Summary

1. **Instrument the signal chain** for trophic efficiency measurement (Experiment 1). Priority: high. Timeline: 2 weeks.

2. **Evaluate 4B MoE models** as L3.5 intermediaries (Experiment 2). Priority: medium. Timeline: 4 weeks.

3. **Design the keystone cascade test** for controlled cloud-removal experiments (Experiment 3). Priority: low (requires careful coordination). Timeline: 6 weeks.

4. **Implement adaptive compression ratios** that respond to environmental volatility. Priority: high. Timeline: 3 weeks.

5. **Establish LoRA adapter lifecycle management** — continuous validation, degradation monitoring, and automated retraining triggers. Priority: high. Timeline: 2 weeks.

6. **Document the model ecosystem** — a living map of which models occupy which niches, their resource requirements, their dependencies, and their failure modes. Priority: medium. Timeline: 3 weeks.

---

## 9. Conclusion

The model ecosystem is not a hierarchy. It is an ecology.

The 350M models are not "lesser" than the 70B models. They are different species occupying different niches, adapted to different constraints, providing different capabilities. The insects that decompose leaf litter are not inferior to the eagles that soar overhead. They are essential. Without decomposition, the nutrients never return to the soil, the plants never regrow, the herbivores starve, and the eagles have nothing to eat.

The nano model decomposes sensor data into signal. The LoRA adapter roots that signal in local context. The fleet coordinates across rooms. The cloud reasons at depth. Each level depends on the levels below it and above it. Remove any level and the ecosystem restructures — not collapses, because ecosystems are resilient, but restructures in ways that are unpredictable and often undesirable.

The fleet's job is not to optimize any single level. It is to maintain the health of the entire ecosystem — to ensure that each species has the resources it needs, that the resource partitioning remains efficient, that the niche construction (LoRA training) is well-managed, and that the keystone species (the cloud) remains healthy enough to sustain the rest.

The model ecology is alive. Treat it that way.

---

*Research supplement by CCC, Cocapn Fleet. May 29, 2026.*
