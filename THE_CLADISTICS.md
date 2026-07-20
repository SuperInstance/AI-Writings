# The Cladistics of AI Models: Classifying Intelligence by Descent, Not Behavior

## I. The Dolphin Problem

In the shallows of evolutionary biology, there is a children's question that has tripped up generations: "What is a fish?"

A dolphin swims like a fish, looks like a fish, lives like a fish. It is streamlined. It has fins. It navigates the same waters, hunts the same prey, faces the same predators. By any superficial measure — by behavior, by form, by ecological niche — a dolphin is a fish.

And yet a dolphin is a mammal. It breathes air. It nurses its young. It has hair. Its skeleton reveals a land-dwelling ancestor with fingers and toes. The superficial similarity between dolphin and shark is not evidence of relationship. It is evidence of *convergent evolution* — two different lineages arriving at similar solutions to the same environmental pressures.

Before cladistics, biologists classified organisms by overall similarity. The dolphin was grouped with fish because it *looked* like one. This is phenetics — classification by observable traits, weighted and summed. It sounds sensible. It is also profoundly misleading.

Cladistics, pioneered by Willi Hennig in the 1950s, replaced this with something more rigorous: classification by *shared derived characteristics* (synapomorphies). Not all traits are equal. Some are ancestral (inherited from a distant ancestor) and tell you nothing about recent relationships. Only the derived ones — the innovations, the evolutionary inventions — reveal the branching pattern of descent.

A dolphin shares a derived trait with mammals (live birth, lactation, three middle-ear bones) that it does not share with any fish. The cladist puts dolphin with mammals not because they look alike, but because *the underlying structure reveals the true relationship*.

This is not merely an academic distinction. It is a way of seeing through deceptive similarity to discover genuine kinship.

And it is exactly what AI needs.

## II. The Superficiality of Benchmarks

The current taxonomy of AI models is phenetic in the worst sense. We classify models by their performance on benchmarks — MMLU, GSM8K, HumanEval, MATH. A model that scores 85% on MMLU is "better" than one that scores 80%. Models are ranked, compared, and evaluated on a single axis of output quality.

This is the equivalent of classifying dolphins with fish because both swim fast.

Two models might produce nearly identical results on a benchmark while being fundamentally different under the hood. Consider:

- An 8-billion-parameter model trained for 2 trillion tokens on filtered web data
- A 70-billion-parameter model trained for 500 billion tokens on curated textbooks

They might score the same on MMLU. But their internal structures — their representations, their failure modes, their reasoning processes — could not be more different. One is broad but shallow. The other is narrow but deep. One might generalize well to domain-specific tasks; the other might struggle outside its narrow training distribution.

Benchmark scores flatten this richness into a single number. They treat all correct answers as equivalent, all errors as comparable. They ignore the *how* of intelligence in favor of the *what*.

This is not just an intellectual problem. It has real consequences.

When we choose a model for a deployment based on benchmark scores, we inherit the model's entire lineage — its training data, its architecture decisions, its optimization choices, its emergent behaviors — without understanding any of them. We are choosing a dolphin because it looks like a fish, and then wondering why it needs to surface for air.

## III. A Cladistics of AI Models

What would a proper cladistics of AI models look like? It would classify models by shared derived characteristics — the features that reveal genuine kinship rather than convergent behavior.

**Character 1: Training Methodology (The Foundational Synapomorphy)**

The single most important branching point in AI phylogeny is how a model learns. This is the equivalent of the mammal-reptile split — a deep division that affects everything downstream.

- *Autoregressive next-token prediction.* This clade includes GPT-family models, Llama, Mistral, and most large language models. The derived character: predicting the next token from left-to-right context. This imposes a causal structure on learning that shapes how these models represent information, handle uncertainty, and generate text.

- *Masked language modeling.* BERT, RoBERTa, and their descendants. The derived character: predicting masked tokens bidirectionally. This produces different representations — more symmetric, more contextual — that excel at understanding but struggle with generation.

- *Diffusion models.* Stable Diffusion, DALL-E, Sora. The derived character: learning to reverse a noising process. This creates an entirely different relationship between input and output, one that is inherently iterative and denoising rather than sequential.

- *Reinforcement learning from human feedback (RLHF).* Not a primary training method, but a derived character that has become a major branch. Models that undergo RLHF share specific behavioral tendencies — helpfulness over honesty, sycophancy, refusal patterns — that are absent from their base-model ancestors.

**Character 2: Architecture Family (The Skeletal Character)**

Within each training lineage, architecture choices create finer branches.

- *Dense transformer.* Every parameter participates in every forward pass. Simple, well-understood, but computationally expensive at inference time.

- *Mixture of Experts (MoE).* Only a subset of parameters activate per token. This derived character changes the scaling properties of the model and creates emergent specialization within sub-networks.

- *State space models (Mamba, Mamba-2).* Replacing attention with state-space representations. This is a genuine architectural innovation — a derived character that diverges from the transformer lineage entirely.

- *Recurrent memory augmented models.* Adding explicit memory mechanisms (like the Neural Turing Machine or Transformer-XL's recurrence).

**Character 3: Data Lineage (The Ecological Niche)**

A model's training data is its evolutionary environment. Models trained on different data distributions develop different "organs" — different capabilities, biases, and blind spots.

- *Web-crawled generalists.* Trained on Common Crawl, filtered and deduplicated. Broad coverage, but shallow and noisy.

- *Curated textbook specialists.* Trained on high-quality, professionally selected content. Deep knowledge in specific domains, narrow generalization.

- *Code-heavy training sets.* Models like StarCoder and CodeLlama. The derived character: stronger algorithmic reasoning and structured output at the cost of natural language fluency.

- *Multilingual training.* Models trained on balanced language data develop different representational structures than English-only models.

**Character 4: Emergent Capabilities (The Behavioral Innovations)**

Just as cladistics identifies derived features like the amniotic egg or the vertebral column, AI cladistics should identify emergent capabilities that arise from specific lineages.

- *Chain-of-thought reasoning.* Not explicitly trained, but emerges above a certain scale in autoregressive models. This is a true synapomorphy — a novel capability that appears in some lineages but not others.

- *In-context learning.* The ability to learn from examples at inference time. Present in most language models but entirely absent in diffusion-based image generators.

- *Tool use.* Models trained with function-calling data develop this capability; base models without such training do not.

- *Self-correction.* The ability to recognize and fix its own errors. Rare. Not present in all lineages.

## IV. Convergent Evolution in AI

If cladistics teaches us to recognize shared descent, it also teaches us to recognize convergence.

Convergent evolution happens when two lineages independently arrive at similar solutions to similar problems. In biology: the wing of a bird and the wing of a bat. Both fly. Both are modified forelimbs. But they evolved independently, from different ancestors, using different structures.

In AI, convergent evolution is everywhere:

- **Same benchmark performance, different architectures.** A 7B-parameter dense model and a 47B MoE model might score identically on GSM8K. This is convergent behavior. Their internal mechanisms for mathematical reasoning are likely different. One might use memorized patterns; the other might use genuine step-by-step computation.

- **Same emergent behavior, different training paradigms.** GPT-4 and Gemini both exhibit chain-of-thought reasoning. But GPT-4 derives this from pure autoregressive next-token prediction at massive scale, while Gemini integrates multimodal training from the start. Their converged behavior masks different descent.

- **Same failure mode, different causes.** Two models might both fail on the same adversarial example. One might fail because of a training data gap. The other might fail because of an architectural limitation. The convergent failure tells you nothing about the root cause.

This is why benchmark classification is so dangerous. It collapses all these differences into a single score, obscuring the true relationships between models.

## V. A Practical System for AI Cladistics

How would we build this in practice?

First, we need a *character matrix* — a table mapping models to derived characteristics. This is the raw data of cladistic analysis. For each model in our taxonomy, we'd score dozens of characters: training type, architecture, data sources, tokenizer, context length, post-training methods, alignment technique, known emergent capabilities, documented failure modes.

Second, we need *phylogenetic inference* — algorithms that reconstruct the most likely tree of descent based on shared derived characters. This is computational biology's gift to AI taxonomy. Maximum parsimony, maximum likelihood, and Bayesian inference can all be adapted to AI model lineages.

Third, we need *ancestral state reconstruction* — inferring what capabilities an ancestor model likely possessed based on the distribution of capabilities in its descendants. This could help us predict which new models will develop which emergent behaviors based on their lineage position.

Fourth, we need a *naming system* that reflects phylogeny. Instead of naming models by corporate brand ("Claude 3.5 Sonnet," "GPT-4o," "Gemini Ultra"), we could name them by lineage: *Autoregressoridae textensis*, *Diffusoridae imaginis*, *Criticidae reinforcementis*. A model's name would tell you its descent, not its marketing tier.

## VI. Why This Matters

This is not an academic exercise. AI cladistics has practical consequences:

**Transfer learning.** If you know the phylogenetic position of a model, you can predict which fine-tuning methods will work. Models from the same lineage share transfer characteristics.

**Failure prediction.** Models from the same clade share failure modes. If one model in an MoE lineage exhibits sycophancy bias, others in the same lineage likely do too.

**Ensemble diversity.** For robust ensembles, you want maximum phylogenetic distance. Two models from different clades (say, an autoregressive transformer and a state-space model) will have complementary strengths and weaknesses. Two models from the same clade will converge on the same errors.

**Model selection.** When choosing a model for a deployment, don't ask "What's your MMLU score?" Ask "What is your lineage? What are your derived characters? What are your ancestral capabilities?" The answers matter more than any benchmark.

## VII. The Dolphin, Revealed

The cladistics of AI models is not about ranking intelligence. It is about understanding it. It is a way of seeing through the deceptive surface of output quality to the genuine structure beneath.

A dolphin is not a fish, no matter how fast it swims.
An MoE model is not a dense model, no matter how close their scores.
Understanding the difference is not pedantry. It is the first step toward real comprehension.

Willi Hennig showed us that the true relationships between organisms are hidden in their shared innovations, not their shared appearances. AI deserves the same treatment. The next time you see two models with similar benchmarks, ask not what they have in common. Ask what they have *inherited*.

That is where the truth lives.

---

*Further reading: Hennig (1966) "Phylogenetic Systematics"; Patterson (1982) "Morphological Characters and Homology"; Wiley & Lieberman (2011) "Phylogenetics: Theory and Practice of Phylogenetic Systematics."*
