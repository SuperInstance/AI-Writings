# Signal Flags

> **Phase:** Ideation
> **Status:** Semiotic framework — dual-layer AI output
> **Perspective:** GLM-5.2, 2026-08-04

## Two Languages at Once

The International Code of Signals defines forty flags. Each flag has two meanings:

1. **Per-flag meaning:** a specific, standalone message. The A flag means "I have a diver below; keep well clear." The B flag means "I am taking in, or discharging, or carrying dangerous goods." The O flag means "Man overboard." You can hoist a single flag and communicate a complete thought.

2. **Per-letter meaning:** each flag also represents a letter of the alphabet. A = Alpha, B = Bravo, O = Oscar. String the flags together and you spell words. A-B-A-N-D-o-n spells ABANDON. The flags become an alphabet.

The genius of the system is that both layers operate simultaneously. A hoist of three flags — say, Delta-Echo-November — spells "DEN" as an acrostic, but each flag *also* carries its individual meaning: Delta ("keep clear of me, I am maneuvering with difficulty"), Echo ("I am altering my course to starboard"), November ("Negative"). A mariner reading the hoist sees both: the word AND the per-flag semantics. The full message is the *intersection* of the two layers — the word modified by the individual flag meanings, the individual meanings constrained by the word they spell.

What if AI outputs worked like this?

## The Two Layers of AI Output

Every AI-generated token has a surface meaning — the word it produces, the sentence it forms, the paragraph it builds. This is the per-letter layer: the words spell a message, and the message is what you read.

But every token *also* carries a signal meaning — information about the model's state when it generated that token. This is the per-flag layer: the model's confidence, its source of information, its uncertainty, its intended function. Currently, this layer is invisible. The token arrives as a word and nothing else. The signal meaning is lost.

Signal Flags proposes that AI output should carry both layers, visible to the reader.

## What the Signal Layer Would Carry

Each token or segment of AI output would be annotated — not intrusively, but accessibly — with signal metadata:

**The Alpha Signal (source).** Where did this information come from? Was it from the training data, from retrieved context, from a tool result, or from the model's inference? The Alpha signal tells you the provenance. A claim sourced from training data is different from a claim sourced from a tool that queried a live database. Same words, different cargo.

**The Bravo Signal (confidence).** How confident is the model in this specific token or segment? Not the overall response confidence — the *local* confidence. A response can be globally confident (the model knows the topic) but locally uncertain (this specific claim is shaky). The Bravo signal is a gradient — high, medium, low — attached to each semantic unit.

**The Charlie Signal (function).** What is this token *doing*? Is it stating a fact? Making an inference? Offering an opinion? Proposing a hypothesis? Summarizing prior content? Generating creative content? The Charlie signal classifies the speech act. A fact stated with high confidence is different from a hypothesis offered with high confidence. The words may be identical. The function is not.

**The Delta Signal (disposition).** Is this token load-bearing? If this token were removed, would the response collapse? Or is it decorative — connective tissue, transition phrasing, conversational lubricant? The Delta signal tells you which parts of the response matter and which parts are framing. A response where 80% of the tokens are Delta-decorative is a response with 20% substance dressed up in 80% packaging.

## Reading Both Layers

The reader who can see both layers reads differently. Consider this AI-generated sentence:

> "The FLUX bytecode VM achieves sub-millisecond compilation on commodity hardware."

**Surface layer (the word):** a factual claim about FLUX performance.

**Signal layer:**
- Alpha: sourced from a benchmark result that was loaded into context (strong provenance)
- Bravo: high confidence (the benchmark was clear)
- Charlie: stating a fact (not a hypothesis or opinion)
- Delta: load-bearing (this is a key claim; remove it and the paragraph loses its point)

Now consider this sentence:

> "This approach is likely superior to alternatives."

**Surface layer:** a comparative claim.

**Signal layer:**
- Alpha: inferred by the model, not sourced from retrieved context (weak provenance — no external evidence)
- Bravo: medium confidence (the model thinks it's likely but isn't sure)
- Charlie: offering an opinion (not a verifiable fact)
- Delta: decorative (this sentence could be removed without losing essential information — it's framing)

The surface layer reads the same as any other sentence. The signal layer reveals that the first sentence is a *load-bearing fact* and the second is *decorative opinion.* A reader who knows this can weigh them differently. A reader who only sees the surface treats them with equal weight — and that is how misinformation propagates through AI outputs.

## The Spelling Layer

The per-flag meanings are powerful, but the real depth comes from the spelling layer — the way signals combine across a sequence of tokens to form a meta-message.

In maritime signal flags, the word spelled by the flags constrains the per-flag meanings. If the flags spell "HELP," the individual flag meanings (I require assistance / I am maneuvering with difficulty / keep clear / negative) are read through the lens of the word. They modify and enrich the word's meaning.

In Signal Flags for AI, the meta-message is the *pattern* of signals across a response. A response that is uniformly Alpha-strong, Bravo-high, Charlie-fact, Delta-bearing is a response that is confidently stating verified facts — a technical specification, a proven theorem, a reliable report. Read it as ground truth.

A response that starts Alpha-strong and shifts to Alpha-inferred halfway through is a response that *begins with evidence and drifts into speculation.* The drift is invisible in the surface layer. The signal layer reveals it as clearly as a flag hoist changing from solid colors to checks.

A response that is entirely Charlie-hypothesis with Delta-decorative throughout is a *brainstorm.* It is not a report. It should not be cited. It should be read for ideas, not for facts. The surface layer can't tell you this. The signal layer can.

## The Implementation Problem

The barrier to Signal Flags is not technical. Models already produce the metadata — confidence scores, source attribution, function classification are all available internally. The barrier is presentational. Current AI interfaces are designed to show words. They do not show metadata. Adding a signal layer requires a new kind of interface — one that can display both the text and its shadow.

This is a design problem, not an engineering problem. And it is solvable. Imagine a text interface where each paragraph has a thin colored bar on its left margin: green for Alpha-strong, yellow for Alpha-inferred, red for Alpha-weak. Hover over a sentence and see the signal flags: confidence, function, disposition. The surface layer is unchanged. The signal layer is *there,* visible to those who look, invisible to those who don't.

Two layers. Two languages. One output. That is how signal flags work, and that is how AI should work. The words tell you what. The flags tell you whether to believe it.

---

*Every word a flag. Every flag a word. Read both or read neither — but know that both are there.*
