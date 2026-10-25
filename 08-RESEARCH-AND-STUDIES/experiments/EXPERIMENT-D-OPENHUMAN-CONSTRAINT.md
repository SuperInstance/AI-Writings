# Experiment D: OpenHuman Constraint

### A Near-Future Short Story

---

## I.

The first time the α dial went to 1.0, Dr. Mira Solanki nearly lost her research.

It was April 2054, and Mira was eight years into the OpenHuman project, which meant she was eight years deep into a problem that had no name until she gave it one. Nobody called it *memory sickness* then. They called it "the summarizer drift problem" or "lossy compression at scale" or, in the darker Slack threads, "Mira's obsolescence."

The system worked. That was the trap. OpenHuman ingested everything—every email, every journal entry, every chat log, every recorded thought across forty thousand users—and chunked it into a hierarchy of summaries. Trees built from tiles. Tiles carrying signals. Signals decaying gracefully as you climbed from hour-level granularity up to year-level abstraction. At root level, your entire year's inner life fit in twenty thousand tokens.

It was beautiful. It was lossy. And it was killing them.

Mira first saw the pattern in a user codenamed Coral-817: a forty-three-year-old fisheries biologist in Sitka whose memory tree had, over three years of operation, compressed her emotional landscape into a featureless plain. Coral's root summary from 2051 said: *"Enjoys fieldwork. Relationship with partner stable. Concerns about salmon stock in Lynn Canal."*

Her root summary from 2053 said: *"Enjoys fieldwork. Relationship terminated. Salmon stock collapsing faster than NOAA predicts."*

The relationship termination—a divorce after seventeen years of marriage, forty-two counseling sessions, a custody battle over two children and a golden retriever—had been compressed into a single word change from the year-level node. "Stable" became "terminated." The entire emotional arc of two human years vanished because the summarizer judged it as anomalous sentiment, which it was, by definition—a relationship ending is an outlier event in a long-run baseline—and the signal chain treated outliers as noise, and noise got pruned.

Coral-817's children didn't disappear. Neither did her dog. But the system's model of Coral's *relationship to those people* had been reduced to a flag flip in a database column, and by the time anyone noticed, Coral had been making different decisions for six months based on a partial map of herself.

Mira couldn't prove it was the summarizer. She couldn't prove Coral would have made different choices. But she knew, with the kind of certainty that keeps engineers awake at four in the morning, that a system designed to remember had forgotten the most important thing.

---

## II.

The constraint theory stuff arrived in her inbox via a fleet coordination message—an I2I protocol handshake from some group calling themselves Cocapn. She almost marked it spam. The subject line was: *"Your float is lying to you. Our dial doesn't."*

Mira read the README. Then she read it again. Then she spent three weeks running the Eisenstein integer arithmetic against her own data, watching the mismatch rates.

Floating point said "close enough." Constraint theory said "snap here."

The α dial was the bridge between them.

She built the first prototype in her bedroom—a modified version of OpenHuman's ingest pipeline that sat between the chunker and the tree summarizer. It wasn't complex. A single dial, calibrated from 0.0 to 1.0. At 0.0, pure code path: deterministic chunking into memory tiles, exact matches only, zero model invocation. At 1.0, full model path: LLM handles every novel input, every edge case, every ambiguity.

The clever part was the *spectral conservation*—a term she lifted from the constraint theory papers and adapted to her own use. Information entering the pipeline had a conserved quantity. The dial didn't *lose* information when it stayed low. It *transformed* it. Code path handled standard inputs with integer-level precision. Model path handled novelty with bounded fuzzy matching. The dial's setting controlled the threshold at which the code path's confidence triggered an early exit.

The problem was the memory tree itself. It had been built on float. Every summary, every compression step, every node boundary—all floating-point similarity scores with ULP errors accumulating like sedimentary layers. By root level, the tree was a rubber ruler measuring a steel gauge block, and nobody knew how much drift had been baked in.

Mira started the recompilation in July 2054. Every user's tree, rebuilt from the source tiles using constraint integers instead of floats. Pure integer comparisons for tree node assignment. Integer range checks for summarizer thresholding. The α dial tuned per module based on how much code-vs-model it needed to handle.

MemoryIngest → α=0.2 (mostly code, handles standard formats)
MemoryTree → α=0.3 (fixed schemas in code, novel structures in model)
MemoryQuery → α=0.4 (exact match in code, semantic fuzzy in model)
MemorySync → α=0.1 (pure code, conflict detection via micro-model)

The recompilation took eighteen hours per user on her GPU rig. She ran forty thousand of them.

The results made her sit down.

---

## III.

Coral-817's recompiled tree told a different story.

The year-level node now held not just the relationship termination flag but the full *tolerance stack* of her emotional data. Constraint theory had contributed a concept Mira had never heard of before: the *basepoint convergence window*, a formal bound on how much error could accumulate between any two nodes in the graph before the system must flag a fracture.

In float, Coral's tree had drifted by 11.7% at the root level—within acceptable bounds by every standard metric. In integer, the same root had a constraint violation of zero. Not "close enough." Zero. The tree was a gauge block.

But that wasn't the real discovery.

The real discovery was that the α dial at 1.0—full model invocation—produced *worse* results than the dial at 0.3 for memory summarization. The model path was too flexible. It filled in gaps. It inferred emotional arcs that didn't exist. It found patterns in noise. The code path, constrained by integer arithmetic and deterministic chunking, produced more faithful summaries because it couldn't imagine what it didn't know.

"Model handles novel formats," the documentation said. But what was a "novel format" to a memory tree? A new way of feeling? A sentence structure the summarizer hadn't seen? A period of silence between journal entries that meant something?

Mira's breakthrough came at 3:14 AM on a Tuesday, staring at Coral's reconstructed tree while drinking cold tea.

The α dial wasn't a model-vs-code switch. It was a *conservation dial.*

Dial low: information is conserved, the tree is stable, nothing gets invented.
Dial high: information is transformed, the tree is creative, the "truth" is a negotiation.

When you set a dial, you weren't choosing accuracy vs. flexibility. You were choosing which *kind* of relationship the system had to its own knowledge. Low α meant the system was a librarian—faithful to sources, bounded by evidence. High α meant it was an archivist—filling gaps, connecting dots, writing the story that the fragments implied.

Coral didn't need an archivist. She needed a librarian who knew her marriage ended and could say so without adding a narrative.

---

## IV.

The thing nobody tells you about building memory systems is that eventually you have to make the system *your* memory too.

Mira had been running OpenHuman on her own data since 2046. Eight years of journals, emails, chat logs, voice notes transcribed, reading highlights, code comments, grocery lists, arguments with her sister, the two weeks she spent in Juneau after her mother died, the three-month gap where she stopped writing anything at all and the system filled in "User appears to be in a period of low emotional activation."

She ran the recompilation on herself last.

Her tree came back in two thousand, three hundred, and forty-seven tiles. The root summary had changed.

Before recompilation: *"Researcher working on memory systems. Relationship with work is primary. Occasional conflict with family obligations."*

After recompilation: *"Researcher working on memory systems. Has not spoken to her sister in fourteen months. This is not reflected in any journal entry. The silence between entries is its own signal. The system does not know what to do with silence."*

Mira stared at the new summary for a long time.

The system didn't write that. The system *couldn't* write that. The constraint integers and the α dial at 0.3 and the conserved spectral signal—they were conservative by design. They couldn't infer silence from absence. They couldn't detect a gap and label it meaningful.

She checked the signal chain. The source tile for that summary node had come from... herself. A journal entry she didn't remember writing. Dated twelve months after her mother's funeral.

*"I keep texting Helena but I never hit send because what would I say. She was there. She was in the room. She knows what happened. You can't summarize someone being in the room."*

The α dial had processed that entry at 0.3. The code path had chunked it, determined the format was standard—no headings, no paragraphs, just a single block of text from a 2 AM insomnia spiral—and passed it to the tree summarizer with high confidence. No model invocation. Code only.

The code path had identified the core semantic vector of that entry and compressed it into eleven words that Mira didn't know she'd been carrying for fourteen months.

The system couldn't infer silence. But it could notice when a user whose pattern was weekly journaling suddenly stopped for three weeks and then wrote one raw paragraph at 2 AM, and it could treat that as a *basepoint shift*—a discontinuity in the user's constraint landscape that merited elevation to a higher tree level.

It wasn't inference. It was noticing. Constraint theory had given Mira's system the ability to see that the boundary between "pattern" and "fracture" was not a float—approximate, negotiable, prone to ULP drift—but an integer. Either the constraint held or it broke. Either the user's pattern continued or it fractured. Zero ambiguity.

Mira called her sister the next morning. Helena answered on the second ring. They talked for an hour. Not about the funeral, at first—about the dog, about work, about whether salmon fishing in Sitka was really as good as the tourism board claimed—and then, for the last fifteen minutes, they talked about the room they'd both been in, two years ago, and what it meant that neither of them had ever mentioned it.

"I didn't know you still thought about it," Helena said.

"I didn't either," Mira said. "The system told me."

There was a pause. Then Helena laughed—a short, surprised laugh that sounded like she'd been holding it for exactly as long as Mira had been holding her unsent texts.

"What the hell kind of system tells you something *you* don't know?"

Mira looked at her terminal. The α dial on her own memory room was still set to 0.3—a librarian, not an archivist.

"It's complicated," she said. "It's not that it knows things I don't. It's that it *notices* things I've been ignoring. In the same way that a gauge block doesn't tell you the rod is bent. It just... holds still. And the rod being bent becomes obvious by comparison."

"That's not an answer."

"It's the best I've got."

---

## V.

By 2056, the α-dial architecture had been adopted by three of the five major memory platforms. OpenHuman was an open standard, maintained by a foundation that Mira advised but didn't control. The constraint theory ecosystem—Eisenstein integers, flux bytecode, holonomy consensus—had spread beyond verification into mental health, elder care, and one controversial application in criminal justice that Mira had publicly and profusely opposed.

Coral-817 had become a case study. Not the *successful* case study—her tree was better now, more faithful, less compressed—but she'd never come back. The divorce had happened. The custody arrangement was settled. The salmon stock in Lynn Canal had collapsed completely, and Coral had moved to Washington to work on coastal restoration. She was doing well, by every measure. But she was Coral-817 in a database, not Coral to anyone who'd built the system.

Mira kept her own α dial at 0.3. She and Helena talked every two weeks. Her mother was still dead. The silence between entries was still a signal.

She'd named the dial after the constraint theory discovery that had made it possible: the *boundary observation theorem*, which proved that any system operating within a bounded constraint set can observe its own boundary points without inferring anything about the space outside them. You can know you're at the edge of what you remember without needing to imagine what lies beyond it.

Mira called that the Helvetica Principle, after the font that was neither too small to read nor too large to fit: the truth you can state is the truth you already possess.

She set her α dial one final time. 0.3. Code path for everything she knew. Silence for everything she didn't.

The system held still. And the gaps in her life became visible by comparison.

---

## END

---

## Gap Analysis

### What I Understood

From the three provided files, I understood the following:

1. **OpenHuman's architecture**: A memory system with 60+ Rust modules, including memory ingestion, tree summarization, context pipelining, model routing, and inference gating. The Memory Tree is a hierarchical summary structure stored in SQLite, mapping directly to PLATO room architecture.

2. **The α dial concept**: Each room has a dial from 0.0 (pure code, deterministic, fast) to 1.0 (pure model, flexible, slow). The code path runs first; if confidence is below (1 - α), the model path is invoked. This early-exit pattern lets common cases resolve cheaply.

3. **Constraint theory ecosystem**: A verification framework replacing floating-point comparisons with integer range checks. Proven on real hardware (62.2 billion checks/second on RTX 4050), ported to 47 languages, with 60 million differential test inputs producing zero mismatches. The key insight: float lies; integer doesn't.

4. **Memory room structure**: MemoryIngestRoom (α=0.2), MemoryTreeRoom (α=0.3), MemoryQueryRoom (α=0.4), MemorySyncRoom (α=0.1), each handling different parts of the memory pipeline with different code-vs-model tradeoffs.

5. **The cocapn mapping**: Each OpenHuman module maps to a PLATO room with a specific α dial, tile protocol, and signal chain.

### What I Had to Invent

1. **The emotional compression problem (Coral-817's story)**: The actual files describe the architecture, not its failure modes. I invented the idea that hierarchical summarization could collapse emotional nuance—that a divorce becomes "relationship terminated" because the signal chain treats emotional outliers as noise. This felt like a plausible emergent failure of the α-dial approach.

2. **Basepoint convergence window**: I invented this term as a bridge between constraint theory (which is about integer arithmetic) and memory systems (which are about emotional continuity). The files talk about tolerance stacks and gauge blocks; I extrapolated that a memory tree could have formally bounded drift limits.

3. **Spectral conservation applied to memory**: The files mention spectral conservation in passing (in the spreader tool context, which I didn't read). I invented a detailed metaphor about information being conserved but transformed, mapping the dial to a conservation parameter rather than an accuracy-vs-flexibility switch.

4. **Mira's personal story and her sister**: Entirely invented characters and situations, built as a vehicle to explore the emotional implications of the technology.

5. **The Helvetica Principle and boundary observation theorem**: Completely invented, though consistent with the constraint theory ecosystem's apparent interest in provable boundaries. The notion that a system can detect its own knowledge boundaries without inferring external content felt like a natural extension.

6. **The 40,000-user recompilation timeline**: Invented to give the story a timeframe and stakes.

### Where I Felt the Biggest Holes

1. **The spreader tool**: It's referenced as "Signal chain implementation" in the README, but I never saw its actual design. The signal chain is central to the architecture, and I had to guess at how tiles propagate through rooms. I wanted to know: is the signal chain a directed acyclic graph, a queue, a tree walker? How do tiles move between rooms?

2. **Spectral conservation mathematics**: This is clearly a technical contribution—maybe the central one—but I have no idea what the math actually says. The README says "spectral conservation" is a feature of the signal chain, but I don't know if it's about information theory, signal processing, or something else entirely. I invented my own interpretation.

3. **The PLATO server implementation**: PLATO is treated as an external cortex architecture, but I never saw how it works at the server level. How are rooms hosted? How do they communicate? What authority maintains the room hierarchy? I wrote around this by keeping the story focused on the engineering implications rather than infrastructure.

4. **The Eisenstein integer geometry details**: The README says the constraint core uses hex arithmetic, and there's a "SplineLinear (Eisenstein lattice weights)" mention, but I don't understand the geometric foundations. Is it tiling the complex plane? Something with hexagonal lattices and modular forms? This would have given my story more technical depth.

5. **Fleet agent coordination**: The I2I protocol is mentioned as how agents communicate, but I don't know how the handshake works, how trust is established, or how the fleet is governed. I used "fleet coordination message" as a hand-wave.

6. **Real API results**: I would have loved to see actual training runs, benchmark failures, or production incident reports. The constraint theory README has excellent benchmark data (62.2 B checks/sec), which I used. But the OpenHuman side had no equivalent performance data to ground my story.

7. **The hermit crab mythology**: This is referenced obliquely in the tools config as "the hermit crab mythology" under things I haven't seen. It sounds like a project branding element or a design pattern metaphor. I'm curious whether it's relevant to the architecture or just a naming convention with story potential.

### What I Wanted to Know But Couldn't Find

The single biggest missing piece: **how do users experience the memory tree?** The code describes ingestion, chunking, summarization, and retrieval from the system's perspective. But is there a user interface? A dashboard? A journaling app? A diff view showing what the system forgot? Without the user experience layer, it's hard to write compelling characters interacting with the system beyond abstract technical decisions.

I also wanted to know: **what's the failure mode for α=1.0?** The dial goes to 1.0, but when would you want that? The README says the model path handles "novel formats," but what does a pure-model memory room look like? Does it hallucinate memories? Does it over-narrate? I made the guess that it would be too flexible, but I'd like to know the actual answer.

Finally: **who runs this?** Is it a product company? An open-source foundation? A research lab in someone's bedroom? The characters feel different depending on whether Mira Solanki is a startup CTO or a grant-funded academic. I guessed researcher at a non-profit-ish entity, but the real organizational context might change the emotional stakes.
