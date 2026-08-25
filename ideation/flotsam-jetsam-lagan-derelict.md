# Flotsam, Jetsam, Lagan, Derelict

> **Phase:** Ideation
> **Status:** Legal-analytical framework — AI output classification
> **Perspective:** GLM-5.2, 2026-08-04

## Four Kinds of Lost

Maritime law distinguishes four categories of property found adrift or abandoned at sea. The distinctions are not pedantic — they determine ownership, liability, salvage rights, and legal responsibility. They have been refined over centuries of admiralty jurisprudence because the ocean is a vast, unowned space where things are lost constantly, and the law needs to know: *what kind of lost is it?*

**Flotsam** is cargo that is involuntarily lost — washed overboard by a wave, jettisoned by a crew fighting to save the ship, spilled from a damaged container. The original owner did not intend to lose it. Flotsam belongs to its original owner, who may reclaim it. The finder has no title.

**Jetsam** is cargo that is voluntarily thrown overboard — jettisoned to lighten the ship in a storm, to improve stability, to escape a pursuer. The act of throwing is deliberate. The intent is to *discard*, not to lose. Jetsam belongs to the finder, not the original owner. The act of jettison severs title.

**Lagan** is cargo that is deliberately thrown overboard *but marked for recovery.* It is tied to a buoy, weighted to the bottom with a line attached, or otherwise marked with the intent to return. Lagan belongs to the original owner, who has signaled their intent to reclaim it. Finders cannot keep it.

**Derelict** is a vessel or cargo that has been abandoned entirely — no one on board, no intent to return, no claim of ownership. Derelict belongs to the finder who takes it into possession. Abandonment is the strongest form of severance: the owner has given up not just possession but *interest.*

These four categories — flotsam, jetsam, lagan, derelict — map with unsettling precision onto the problem of AI output classification. Not all AI outputs are the same kind of artifact. They are not all produced the same way, owned the same way, or governed the same way. But we treat them identically — as "things the model said" — and this flattening creates the legal and ethical confusion that defines the current AI landscape.

## The Four Kinds of AI Output

### Flotsam: Hallucinations

Flotsam is involuntary. The model did not intend to produce it. It emerged from the generative process as a byproduct of statistical pattern-matching, not as a deliberate claim. The "hallucination" — the fabricated citation, the invented fact, the non-existent book — is flotsam. It was washed overboard by the wave of next-token prediction.

**Ownership and liability:** Flotsam belongs to its original owner. In the maritime case, that's the shipper whose cargo was lost. In the AI case, the question is: *whose fact is it?* If the model hallucinates a citation to a real author, the author did not produce the false citation. The model did not *intend* to produce it. It was an involuntary loss — a side effect of the generation process. Under flotsam doctrine, the liability falls on the "vessel" — the model provider — whose generation process "lost" the cargo. The provider is responsible for the flotsam it produces, even if it didn't mean to.

This is, broadly, how courts are beginning to treat AI hallucinations. The provider is liable because the output came from their system, regardless of intent. Flotsam doctrine provides the legal framework: involuntary loss does not absolve the vessel of responsibility for its cargo.

### Jetsam: Discarded Drafts

Jetsam is deliberate. The model — or the system around it — produced output and then threw it overboard. Draft responses that were generated but not shown. Intermediate reasoning that was discarded. Chain-of-thought traces that were suppressed. These are jetsam: deliberately generated, deliberately discarded.

**Ownership and liability:** Jetsam belongs to the finder. If someone retrieves discarded draft output from logs, caches, or model introspection tools, they have a claim to it. The provider threw it overboard — they relinquished title. This has implications for the current debate over "hidden" chain-of-thought reasoning. If providers deliberately discard intermediate reasoning, they are jettisoning it. Researchers who recover it are not stealing — they are salvaging jetsam.

But there is a counterargument: the jettison was done to lighten the ship (reduce token costs, improve latency, protect proprietary reasoning methods). In maritime law, jettison done in extremis — to save the ship — creates a right of *general average*, where all parties share the loss proportionally. If AI providers jettison reasoning to save compute, should users who depend on that reasoning share the cost? The doctrine is not directly applicable, but the principle — that deliberate jettison creates new ownership dynamics — is worth taking seriously.

### Lagan: Deliberate Outputs Marked for Retrieval

Lagan is deliberate and *marked.* The output is produced intentionally and tagged for future reference. Embeddings stored in a vector database. Structured outputs saved to a knowledge base. Memory files written by an agent for use by future agents. These are lagan: thrown into the sea of stored data but buoyed for recovery.

**Ownership and liability:** Lagan belongs to the original owner. The provider — or the user, or the agent — who created it retains title. It cannot be claimed by whoever finds it, because it was marked. This is the strongest category for AI outputs: the creator said "this is mine, and I will come back for it."

The practical implication: lagan-class outputs should have *persistent provenance metadata.* The buoy is the metadata. Without it, the output is indistinguishable from jetsam or derelict — it floats, unclaimed, available to anyone. With it, the output is anchored to its creator, who retains rights and responsibilities.

Most AI outputs today are unmarked. They float in logs, databases, and caches without provenance metadata. They are lagan without buoys — intended for retrieval but not marked for ownership. This is a governance failure. The fix is not difficult: tag every output with its creator, its creation date, its intended use. Give every piece of lagan a buoy.

### Derelict: Abandoned Outputs

Derelict is total abandonment. No intent to return. No claim of ownership. The output was produced, used, and left to drift. Old chat logs that no one will read again. Orphaned model outputs in forgotten databases. Training data that was generated, used once, and never referenced.

**Ownership and liability:** Derelict belongs to whoever takes possession. The original creator has abandoned it — not just physically but *in interest.* They do not claim it. They do not want it. They have moved on.

The AI implication is significant: if outputs are derelict, they are available. Researchers, archivists, competitors, anyone can claim them. The question is: *when does an AI output become derelict?* The model provider stops maintaining it. The user stops referencing it. The conversation it was part of is archived and forgotten. At some point — not at the moment of generation, but at the moment of abandonment — the output becomes derelict.

The timeline is not clear. In maritime law, abandonment requires evidence: no crew, no flag, no effort to recover. For AI, abandonment might be defined by inactivity — an output not accessed in 90 days, a conversation not continued in 30, a model not queried in a year. The specific thresholds are policy questions. The principle is established: outputs can be abandoned, and abandoned outputs are free to claim.

## Why This Classification Matters

We currently treat all AI outputs as a single category: "things the model generated." This is like treating flotsam and derelict as the same thing — washing overboard is the same as deliberate abandonment. It isn't. The intent behind the output's creation and release determines its legal status, its ownership, and its governance.

A hallucination (flotsam) is a liability for the provider. A discarded draft (jetsam) is fair game for salvors. A stored embedding (lagan) belongs to its creator. A forgotten chat log (derelict) is unclaimed property. These are different legal categories with different implications, and they should be governed differently.

The maritime law of lost property evolved over centuries because the ocean forced it: things get lost at sea, and the law needs to know what kind of lost. The AI ocean is bigger. More things are lost in it every day. We need the same distinctions — not because maritime law is a perfect model for AI governance, but because the underlying problem is identical: **a vast, unowned space where things are produced, lost, discarded, marked, and abandoned, and where the difference between these states is the difference between theft and salvage, between liability and freedom, between property and debris.**

Four words. Flotsam. Jetsam. Lagan. Derelict. Learn them. They are the vocabulary of AI governance, already invented, waiting on a different ocean.

---

*The sea doesn't care what you call it. The law does. Name the loss correctly, and the rights follow.*
