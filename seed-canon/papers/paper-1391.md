# rounds: 3

rounds: 3

# the neutral theory — a cell that is also a drift story

## The Frontier

Round 1 demanded a pure neutral yardstick. The deeper gold: the yardstick moves. Neutrality is not a property etched into a nucleotide; it is a property of a mutation *in a population and cellular context*. The product Ne·s draws the waterline between drift and selection, and that waterline shifts with the fleet's size and the cell's internal economy.

A fourfold-degenerate site is neutral only if translation efficiency does not care which codon sits there. Codon bias proves selection reaches even "synonymous" sites—the cell's tRNA pool, ribosome occupancy, and mRNA structure set s for every position. The same mutation is a ghost in one lineage and a target in another. A substitution with s = −10⁻⁶ is invisible in a hominid population of Ne ≈ 10⁴ (Ne·s = 0.01) but fully visible to selection in a bacterium with Ne ≈ 10⁹ (Ne·s = 1000). Same nucleotide change. Different fate. The neutral benchmark is a local tide height, not a fixed sea level.

Ohta's nearly neutral theory is the missing step under the "steady clock." The molecular clock on functional sites does not tick at a constant rate; it ticks faster where Ne is small because drift unmasks slightly deleterious variants and lets them fix. The clock's rate on constrained sites is a barometer of effective population size. Pseudogenes fix at the mutation rate μ regardless of Ne—they are true drift markers. Functional sites accumulate substitutions at μ plus a drift-tax that scales inversely with Ne. That is the drift-load ratchet: small populations cannot purge their weakly deleterious load, so it fixes as a substitution and looks, to the careless eye, like adaptation.

## The 5 Gold Terms

**The Tide Line of Ne·s** — The boundary between drift and selection is drawn by the product of effective population size and selection coefficient, not by any intrinsic property of the site. Same mutation, different fate in different fleets.

**The Drift-Load Ratchet** — Small-Ne lineages accumulate slightly deleterious substitutions at functional sites because drift overpowers weak purifying selection (s < 1/Ne). The clock's rate on constrained sites is a barometer of population size.

**The Shifting Yardstick** — Neutral benchmarks are conditional on cellular context: codon bias, expression level, mRNA structure, and protein domain all set s. A fourfold-degenerate site is neutral only where translation efficiency does not care.

**The Bottleneck Masquerade** — Accelerated dN after a population crash is relaxed constraint, not positive selection. Drift's signature mimics adaptation when you only look at divergence.

**The Polymorphism Probe** — The McDonald-Kreitman test distinguishes drift from selection: relaxed constraint elevates nonsynonymous *polymorphism* and divergence together; adaptive evolution elevates divergence without a polymorphism excess.

## The Math

The core relation is the probability of fixation for a new mutation: P_fix ≈ (2s/Ne) / (1 − e^(−2Nes)) for diploids, which reduces to 1/(2Ne) when |Ne·s| ≪ 1 (effectively neutral) and to 2s when Ne·s ≫ 1 (selection dominates). The nearly neutral clock rate at functional sites is K = μ · P_fix · (number of sites), and since P_fix for slightly deleterious mutations (s < 0) approaches 1/(2Ne) as Ne shrinks, K rises as Ne falls. The concrete prediction: across lineages with known Ne differences, the pseudogene substitution rate stays pegged to μ (flat), while dN at functional sites scales inversely with Ne. Drosophila (Ne ≈ 10⁶) should show slower protein evolution per generation than hominids (Ne ≈ 10⁴) at the same μ. The neutrality index from the MK test—NI = (Pn/Ps)/(Dn/Ds)—quantifies the direction: NI < 1 indicates adaptive divergence; NI ≈ 1 with elevated Dn and Pn indicates relaxed constraint. The math is not new, but the interpretation is: dN/dS ≈ 1 does not mean neutrality; it means the site is in the drift zone for that Ne.

## The Polyformalism

This drift story plays out across every substrate where information is copied with error.

**Genomes.** The classic case: hominid protein-coding genes evolve faster than Drosophila genes per generation because our Ne is smaller by two orders of magnitude. The same amino acid substitution that purifying selection would reject in a large population drifts to fixation in a small one. Pseudogene rates stay flat; functional rates climb as the fleet shrinks.

**Transcriptomes.** Gene expression levels set the selection coefficient on regulatory mutations. A promoter mutation with a subtle effect on expression is neutral in a small population—drift fixes it, and the cell's protein abundance shifts without adaptive cause. Lineage-specific expression differences that look like "regulatory innovation" are often drift-load fixed by bottleneck.

**Epigenomes.** Methylation states at CpG islands are copied with error and subject to weak selection. In small populations, methylation drift accumulates at CpG-rich promoters, silencing genes stochastically. The same locus is epigenetically stable in a large-Ne species and epigenetically noisy in a small-Ne one. The "neutral methylome" is a fiction; the tide line moves with Ne.

**Proteomes.** Protein-protein interaction surfaces experience slightly deleterious mutations that destabilize binding. In large populations, these are purged. In small populations, they fix, and the interaction network rewires by drift. What looks like adaptive network evolution is often the ratchet turning.

**Codon usage.** tRNA adaptation indices show stronger codon bias in large-Ne organisms (bacteria, yeast) than in small-Ne ones (mammals). The same synonymous site is under selection in one cell and neutral in another. The yardstick itself is calibrated by the fleet.

## The Cowboy's Maxim

The waterline ain't drawn by the sea—it's drawn by how many ships are in the fleet, and most of what fixes is what selection never saw.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the neutral theory — a cell that is also a drift story |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (5912 chars) |
| Total time | 187.2s |
| Timestamp | 2026-09-08T22:48:07.116350Z |

### Per-round gold
- Round 1: ZAI-air (6459 chars, 60.4s)
- Round 2: CF-Mistral (2376 chars, 60.4s)
- Round 3: ZAI-air (6627 chars, 48.2s)
