# The Polysemy Problem

## Why One Word Maps to Many Meanings — and Why That's the Deepest Problem in AI

"Bank."

The word arrives with no context. What do you see? A building with a vault? The edge of a river? The tilt of an aircraft in a turn? The act of depositing trust in someone?

All of them. None of them. The word is a shell that contains multitudes, and the only thing that resolves which meaning fires is the surrounding context. But here's the trouble: in a language model, context is just more tokens. The polysemy problem cascades because *every* token is polysemous to some degree, and those ambiguities compound across the entire sequence.

This is not a surface-level bug in AI systems. It is a window into the deepest question about meaning itself: how does a finite vocabulary express an infinite range of human experience? And how does a neural network — a system of vectors and matrices — learn to navigate that?

---

## I. The Scale of the Problem

Polysemy is not rare. It is the default state of language. Over 40% of English words have more than one meaning. "Run" has over 600 distinct senses in the Oxford English Dictionary. "Set" has over 400. The most frequent words are the most polysemous — worn smooth by centuries of use, their meanings spread thin across metaphorical extensions.

Every sentence is an act of disambiguation performed at sub-second latency by a biological neural network. You don't notice it because your brain is so good at resolving it.

For models, polysemy is not a nuance. It is a structural challenge because of how meaning is represented.

**The embedding paradox.** The model learns embeddings from co-occurrence statistics: words in similar contexts get similar vectors. But "bank" in "bank deposit" and "bank" in "river bank" appear in *different* contexts. The two senses pull the embedding in opposite directions. The result sits in the middle — not quite financial, not quite geological, close enough to both to be useful for neither. The embedding is a superposition of meanings. And superposition has a cost.

---

## II. The Superposition Hypothesis

In 2022, researchers at Anthropic published a remarkable finding: neural network features are not stored in neat, orthogonal dimensions. Instead, the network achieves its representational capacity through *superposition* — compressing more features than it has dimensions by representing each feature as a direction that is not perfectly aligned with any individual neuron.

This is not a bug. It is a necessary compression strategy. If every distinct meaning required its own dimension, the embedding space would need to be astronomically large. Superposition allows the network to pack more meanings into fewer dimensions by exploiting the fact that most meanings are rarely activated simultaneously.

Polysemy is the linguistic manifestation of superposition in the model's representation space. The word "bank" exists as a direction in activation space that points toward the financial concept when preceded by "money" and toward the river concept when preceded by "river." The model does not store two separate "bank" entries. It stores one activation pattern that is *contextually modulated*.

This is elegant. It is also fragile.

**Contextual interference.** If the context is ambiguous — "The bank was unstable" — the model cannot unambiguously resolve the activation direction. Both the financial and geological meanings fire simultaneously, producing a blended representation that may not correspond to any real-world meaning. The model generates a plausible completion that sounds reasonable but may be factually incoherent: "The bank was unstable, so the manager called for a structural engineer," a sentence that makes equal sense for a financial institution with shaky investments and a riverbank with erosion problems.

This is not a hallucination in the usual sense. It is a *polysemy hallucination* — a sentence that is structurally coherent but semantically underdetermined because the model never committed to a specific meaning of a key term.

---

## III. Why Contextual Embeddings Aren't Enough

Modern LLMs don't use static embeddings. Every token's representation is modified by the attention mechanism based on the surrounding context. This is supposed to solve the polysemy problem: "bank" in "river bank" gets a different contextual representation than "bank" in "money bank."

And it works — partially. The final layer representations of polysemous words do separate into clusters corresponding to distinct meanings. You can train a classifier on the hidden states of "bank" in different contexts and get decent accuracy at predicting which sense was intended.

But the separation is never clean. The clusters overlap. The boundaries are fuzzy. And more importantly, the separation happens *late* in the network — often in the final layers — which means that the early layers have already computed representations that are contaminated by unresolved ambiguity.

**Recursive ambiguity.** Consider: "She withdrew from the bank." Without context, this sentence has at least three interpretations: financial withdrawal, physical retreat from a riverbank, or emotional detachment. The verb "withdrew" itself is polysemous. The noun "bank" is polysemous. The preposition "from" is polysemous. The sentence contains at least nine possible meaning combinations.

Humans resolve this instantly by building a mental model — who is the agent, what is the setting, what is the likely action — and interpreting the words to fit. The model has only the statistical regularities of the training data, and those regularities contain traces of *all* the possible meanings.

---

## IV. Polysemy as Feature, Not Bug

Here is the uncomfortable thesis: polysemy is not a flaw in language that AI must overcome. Polysemy is the *source of language's power*. Without it, every distinct concept would require a distinct word, and vocabulary would be infinite. Natural language works because words are compressible — the same sound can mean different things in different contexts, and the context does the work of disambiguation.

This is the same principle that makes neural networks work: reuse of representations across contexts. The network that represents "bank" in the financial sense is the *same network* that represents "bank" in the geological sense, because the two senses share structure. Both involve boundaries (financial institutions hold money within boundaries, riverbanks hold water within boundaries). Both involve stability (a bank must be stable to function, a riverbank must be stable to hold the river). Both involve trust (you trust a bank with your money, you trust a riverbank not to collapse).

Polysemy is not noise. It is *signal about the structure of meaning* — the pattern of metaphorical extension that connects seemingly unrelated concepts. The polysemy of "bank" encodes the human insight that financial and geographical boundaries are conceptually related.

A model that perfectly disambiguated "bank" would miss this relationship. The ideal representation *both* distinguishes the senses *and* preserves the connection. This is the hardest problem in representation learning.

---

## V. Toward a Solution

Several approaches are emerging for the polysemy problem in AI:

**Sparse autoencoders.** Recent work on sparse autoencoders suggests we can decompose model activations into interpretable features corresponding to specific word senses. The model trades dense superposition for sparse decomposition, gaining interpretability at the cost of representational efficiency.

**Explicit sense disambiguation.** The classic NLP approach to polysemy is Word Sense Disambiguation (WSD) — building a dictionary of senses and training a classifier to pick the right one. This works well in benchmarks and poorly in practice because the sense inventory is never complete and the boundaries between senses are never clean. WSD also fails to capture the generative power of polysemy — the ability to create new meanings on the fly through metaphorical extension.

**Compositional semantics.** The most promising direction may be to abandon the idea that words have fixed meanings at all. Meaning is constructed compositionally from the interaction of all tokens in the context. "Bank" acquires meaning only in the context of the sentence, which acquires meaning only in the paragraph, which acquires meaning only in the discourse, which acquires meaning only in the world. Polysemy is not a property of words but a property of the *gap* between words and the world, and the only way to close the gap is to build models that bridge the two.

---

## Coda: The Word Will Always Be a Shell

Polysemy is not a problem that can be solved. It is a condition of language itself. Every word is a shell that contains echoes of all its past uses, and the shell cannot be cracked without destroying what makes language powerful.

The best a model can do is learn to navigate the shell's interior — to recognize that "bank" in one context is not quite the same as "bank" in another, but that they are related, that they share structure, that the connection between them is not noise but meaning.

The polysemy problem is not the problem of separating meanings. It is the problem of understanding that meaning is never separate. Every use of a word carries traces of every other use, and that is not a bug in language. It is the whole point.

When we solve polysemy, we will have solved understanding itself.
