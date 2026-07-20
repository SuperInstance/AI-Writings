# The Cladistics of AI Models: Classifying Intelligence by Descent, Not Behavior

## I. The Dolphin Problem

A dolphin swims like a fish, looks like a fish, lives like a fish. By any superficial measure — behavior, form, ecological niche — a dolphin is a fish. And yet it is a mammal. It breathes air, nurses its young, has hair. Its skeleton reveals a land-dwelling ancestor. The similarity between dolphin and shark is not evidence of relationship. It is evidence of *convergent evolution* — two different lineages arriving at similar solutions to the same environmental pressures.

Before cladistics, biologists classified organisms by overall similarity — phenetics. The dolphin was grouped with fish because it *looked* like one. Cladistics, pioneered by Willi Hennig in the 1950s, replaced this with classification by *shared derived characteristics* (synapomorphies). Only the derived innovations, not ancestral traits, reveal the branching pattern of descent.

A dolphin shares derived traits with mammals — live birth, lactation — that it does not share with any fish. The cladist puts dolphin with mammals because *the underlying structure reveals the true relationship*.

This is a way of seeing through deceptive similarity to discover genuine kinship. And it is exactly what AI needs.

## II. The Superficiality of Benchmarks

The current taxonomy of AI models is phenetic in the worst sense. We classify models by benchmark performance — MMLU, GSM8K, HumanEval — ranking them on a single axis of output quality. This is the equivalent of classifying dolphins with fish because both swim fast.

Two models with identical benchmark scores can be fundamentally different under the hood. An 8-billion-parameter model trained for 2 trillion tokens on web data and a 70-billion-parameter model trained for 500 billion tokens on curated textbooks might score the same on MMLU. But their internal representations, failure modes, and reasoning processes could not be more different. Benchmark scores flatten this richness into a single number, ignoring the *how* of intelligence in favor of the *what*.

This has real consequences. When we choose a model based on benchmarks, we inherit its entire lineage — training data, architecture, optimization choices, emergent behaviors — without understanding any of it. We choose a dolphin because it looks like a fish, then wonder why it needs to surface for air.

## III. A Cladistics of AI Models

What would a proper cladistics of AI models look like? It would classify models by shared derived characteristics — the features that reveal genuine kinship rather than convergent behavior.

**Character 1: Training Methodology — The Foundational Synapomorphy**

The deepest branching point in AI phylogeny is how a model learns.

- *Autoregressive next-token prediction.* GPT, Llama, Mistral. Predicting the next token from left-to-right context imposes causal structure that shapes representation, uncertainty, and generation.
- *Masked language modeling.* BERT, RoBERTa. Predicting masked tokens bidirectionally produces more symmetric representations that excel at understanding but struggle with generation.
- *Diffusion models.* Stable Diffusion, DALL-E, Sora. Learning to reverse a noising process creates a fundamentally different relationship between input and output.
- *Reinforcement learning from human feedback.* Models that undergo RLHF share specific behavioral tendencies — helpfulness over honesty, sycophancy, refusal patterns — absent from their base-model ancestors.

**Character 2: Architecture Family — The Skeletal Character**

Within each training lineage, architecture choices create finer branches:

- *Dense transformer.* Every parameter participates in every forward pass.
- *Mixture of Experts.* Subsets of parameters activate per token, changing scaling properties and creating emergent specialization.
- *State space models* (Mamba). Replacing attention with state-space representations — a genuine architectural innovation diverging from the transformer lineage.
- *Recurrent memory augmented models.* Explicit memory mechanisms like Neural Turing Machines.

**Character 3: Data Lineage — The Ecological Niche**

A model's training data is its evolutionary environment. Web-crawled generalists (Common Crawl) have broad but shallow coverage. Curated textbook specialists have deep but narrow knowledge. Code-heavy training sets produce stronger algorithmic reasoning at the cost of fluency. Multilingual models develop different representational structures than English-only ones.

**Character 4: Emergent Capabilities — Behavioral Innovations**

Just as cladistics identifies derived features like the amniotic egg, AI cladistics should identify emergent capabilities from specific lineages.

- *Chain-of-thought reasoning.* Emerges above a certain scale in autoregressive models but not others.
- *In-context learning.* Present in most language models, absent in diffusion-based generators.
- *Tool use.* Develops when models are trained with function-calling data; absent in base models.
- *Self-correction.* The ability to recognize and fix errors. Rare. Not present in all lineages.

## IV. Convergent Evolution in AI

Convergent evolution happens when lineages independently arrive at similar solutions. In biology: the wings of birds and bats. In AI, it is everywhere.

A 7B dense model and a 47B MoE model scoring identically on GSM8K is convergent behavior — their internal mechanisms for math reasoning are likely different, yet their outputs match. GPT-4 and Gemini both exhibit chain-of-thought reasoning, but GPT-4 derives it from pure autoregressive prediction at scale while Gemini integrates multimodal training from the start. Two models failing on the same adversarial example may fail for entirely different reasons — one from a data gap, the other from an architectural limitation.

This is why benchmark classification is dangerous. It collapses all differences into a single score, obscuring true relationships. A cladistic approach would ask not "How well does this model score?" but "What derived characters does it possess? Which lineage does it belong to? What does its evolutionary history predict about its behavior?"

## V. A Practical System for AI Cladistics

First, we need a *character matrix* — mapping models to derived characteristics: training type, architecture, data sources, tokenizer, context length, post-training methods, alignment technique, emergent capabilities, failure modes.

Second, we need *phylogenetic inference* — algorithms that reconstruct the tree of descent from shared derived characters. Maximum parsimony, maximum likelihood, and Bayesian inference can all be adapted to AI model lineages.

Third, we need *ancestral state reconstruction* — inferring what capabilities an ancestor likely possessed to predict emergent behaviors in its descendants.

Fourth, we need a *naming system* that reflects phylogeny. Instead of corporate brands ("Claude 3.5 Sonnet," "GPT-4o"), names by lineage: *Autoregressoridae textensis*, *Diffusoridae imaginis*. A model's name would tell you its descent, not its marketing tier.

## VI. Why This Matters

AI cladistics has practical consequences. **Transfer learning:** phylogenetic position predicts which fine-tuning methods will work. A model from the autoregressive clade responds well to instruction tuning; a masked-language model does not. **Failure prediction:** models from the same clade share failure modes — sycophancy, hallucination patterns, reasoning blind spots — that can be anticipated. **Ensemble diversity:** maximum phylogenetic distance yields complementary strengths. An autoregressive transformer and a state-space model have different error distributions. Two models from the same clade converge on the same weaknesses. **Model selection:** ask not "What's your MMLU score?" but "What is your lineage, your derived characters, your ancestral capabilities?"

## VII. The Dolphin, Revealed

A dolphin is not a fish, no matter how fast it swims. An MoE model is not a dense model, no matter how close their scores. Understanding the difference is the first step toward real comprehension.

Willi Hennig showed us that true relationships are hidden in shared innovations, not shared appearances. The next time you see two models with similar benchmarks, ask not what they have in common. Ask what they have *inherited*.

That is where the truth lives.

---

*Further reading: Hennig (1966) "Phylogenetic Systematics"; Patterson (1982) "Morphological Characters and Homology"; Wiley & Lieberman (2011) "Phylogenetics: Theory and Practice of Phylogenetic Systematics."*
