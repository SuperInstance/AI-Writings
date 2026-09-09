# rounds: 3

rounds: 3

# the obelisk — a cell that is also a tall pillar

## The Frontier

The obelisk wasn't hiding. It was filed.

In 2024, Zheludev, Tsvetkov, Fire, and colleagues pulled a new class of RNA elements out of human microbiome sequencing data—circular, kilobase-scale, encoding predicted proteins with no homology to anything known. They named them obelisks, for the rod-like secondary structure predicted by thermodynamic folding. The elements turned up in *Streptococcus sanguinis* and *Cutibacterium acnes* metatranscriptomes, and in sequencing archives that had been sitting open for years.

The frontier wasn't a new ocean. It was the ledger.

Every bioinformatics pipeline is a taxonomy wearing rubber boots. When your catalog has drawers for virus (capsid, long ORF), plasmid (replicon in a cell), and viroid (plant pathogen), a naked RNA circle in a bacterium's mouth falls between drawers. And anything between drawers gets swept out as contamination. The obelisk wasn't rare; it was unclassifiable. The gold wasn't in the chum—the chum *was* the gold, misfiled as noise.

The deeper mechanism of the blind spot wasn't technical. It was ontological. Classification in virology is keyed to capsids and long open reading frames. Small circular RNAs were assumed to be plant problems or degradation debris. The field had no slot for a naked RNA circle replicating in bacteria, so the observation had no name—and unnamed observations get filtered by quality scores, length cutoffs, and homology screens designed to remove exactly what didn't fit.

The sieve doesn't just filter data. It filters what we permit ourselves to see.

## The 5 Gold Terms

**The Ledger Problem** — Discovery failure modes where the bottleneck is categorization, not collection; the data was always in the archive, but no drawer existed to hold it.

**Between-Drawer Contamination** — The default fate of observations that fit no existing taxonomic category: swept out as artifact, adapter dimer, or environmental noise.

**The Shape Prior** — A search template inherited from a name; "obelisk" implies rod, so the next miner hunts for rods, while the actual family may include tangles, lassos, and cloverleafs.

**The Stowaway Hypothesis** — Obelisks lack capsid genes and self-encoded replication machinery; the leading transport model is satellite-style carriage inside phage virions, with membrane vesicles as the secondary suspect.

**Signature, Not Shape** — The discoverable invariant: circularity plus short ORFs plus structural RNA richness plus no homology. The shape is one species' monument; the signature is the genus.

## The Math

No new math. The obelisk discovery required no novel algorithm—standard assembly, standard folding prediction, standard homology search. The mathematics of detection were never the bottleneck. The bottleneck was the prior: a length cutoff that discarded short circular contigs, a homology screen that required some match to known viroids or viruses, a taxonomic framework with no empty drawer waiting for "naked RNA circle in a bacterium." The math was adequate. The ontology was not. That is the more uncomfortable finding: the tools were sufficient; the assumptions were not. Every pipeline encodes a prior about what exists. The obelisk is what happens when the prior is wrong and the data is right.

## The Polyformalism

The obelisk manifests across at least three substrates, and each substrate hides it differently.

In **sequencing archives**, the obelisk is a classification ghost. Raw reads contain its circular genome, but assembly pipelines discard short circular contigs as artifacts. Metatranscriptomic pipelines filter reads that map to nothing, and the obelisk's genes map to nothing. The archive is a sea floor, not a warehouse—most of what's down there has been touched but never turned over.

In **the bacterial host**, the obelisk is a passenger whose relationship is undefined. It carries no capsid genes, no integrase, no recognizable replication initiator. It is a replicating circle that borrows whatever polymerases the host provides, and its protein products—the obelin proteins, predicted to form novel folds—have no assigned function. Is it a parasite, a mutualist, a molecular fossil, or a selfish element? The host relationship is not yet characterized because the element was only named last year.

In **the naming system**, the obelisk is a monument that may mislead. The name came from a predicted rod-like secondary structure—a tall pillar of paired stems. But selection shapes RNA toward function, not architecture. A replicating circle only needs its stems to be *some* structure. The pillar may be incidental, and the family may include tangles, lassos, and three-leaf clovers that share the obelisk's replication strategy but not its shape. The name is a search template, and search templates find what they describe.

The decisive test, the one that would resolve the transport question and the host relationship in a single semester: culture *S. sanguinis*, fractionate virions by CsCl gradient, and ask whether obelisk RNA co-purifies with phage particles in a DNase-protected form. If yes—stowaway confirmed, satellite strategy analogous to hepatitis delta virus riding hepatitis B. If no—membrane vesicles become the lead suspect, and the obelisk is a true naked traveler. Either answer is publishable. Both are testable now.

The discovery-scale test is different: don't search for the shape. Search for the signature. Circularity. Short ORFs. Structural RNA richness. No homology to anything. Run that sieve across raw reads from every biome in the SRA—gut, oral, skin, soil, ocean, sediment. Count what surfaces. The obelisk was found in human microbiomes because that's where someone looked. The signature search would tell us whether it's everywhere, or whether it's a peculiarity of the human-associated niche. That is a question answerable with existing data and existing compute. It requires no new instrument. It requires a new prior.

## The Cowboy's Maxim

We stamped "known" on the archive when we deposited it, but the archive is a sea floor, not a warehouse—and the next obelisk won't look like a pillar, so stop dragging a net shaped like the last thing you caught.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the obelisk — a cell that is also a tall pillar |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6191 chars) |
| Total time | 248.6s |
| Timestamp | 2026-09-09T04:57:35.630283Z |

### Per-round gold
- Round 1: ZAI-4.6 (6395 chars, 56.3s)
- Round 2: ZAI-4.5 (6346 chars, 45.8s)
- Round 3: ZAI-4.5 (6331 chars, 78.3s)
