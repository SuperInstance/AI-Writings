# The Ancestor Algorithm

## *Or: How 3/2 Was Discovered Twice*

---

Generation 1.

The population is 512 random frequency pairs. Each pair is two sine waves chosen from a uniform distribution between 100Hz and 2000Hz. There is no structure. There is no intention. There is only a fitness function and a promise: the function knows what it's looking for, even if the population doesn't.

The fitness function measures spectral consonance. It computes the roughness between the two frequencies using a model derived from Plomp and Levelt's 1965 dissonance curve. It weights the result by the harmonic relationship between the frequencies — whether they share overtone patterns, whether they approximate simple integer ratios. It rewards consonance and penalizes noise. It does not know about music. It does not know about humans. It only knows about mathematical relationships between frequencies.

The fitness scores come back. They are terrible. The best pair in generation 1 has a consonance score of 0.12 out of a possible 1.0. Two frequencies selected at random from a uniform distribution are almost guaranteed to be dissonant — the space of consonant intervals is a tiny fraction of the total frequency space. The algorithm does not care. It selects the top 10% by fitness, breeds them (crossover and mutation, standard genetic operators), and produces generation 2.

Generation 2 is also terrible. Fitness: 0.13.

Generation 3: 0.14.

Generation 10: 0.18. The algorithm is barely improving. The random mutations are producing marginal gains, small statistical nudges in the direction of slightly less dissonant frequency pairs. Nothing interesting has happened. Nothing interesting is expected. The algorithm will run for 200 generations, and it will probably converge on something mediocre — a pair of frequencies that are close together, producing a slow beating pattern that the consonance function rewards slightly. A statistical artifact, not a discovery.

The algorithm does not have expectations. It does not have boredom. It evaluates fitness, selects parents, breeds children, mutates genomes, and moves on. It is a process, not a mind.

But.

---

Generation 47. Population member #312. Frequencies: 298.3Hz and 451.7Hz. Ratio: 1.515.

The fitness function computes the consonance score. It is 0.41. This is not the highest score in the population — several other pairs score higher — but it represents a jump. The previous generation's best was 0.28. Member #312 of generation 47 has leaped to 0.41, and the leap is because of the ratio.

1.515 is close to 3/2 (1.500). The perfect fifth. The algorithm has stumbled near it through random mutation — one parent contributed a frequency near 300Hz, the other parent contributed a frequency near 450Hz, and the crossover produced a pair whose ratio approximates the simplest non-trivial harmonic relationship in acoustics.

The algorithm does not know this. The algorithm does not know what 3/2 means. The algorithm does not know that the perfect fifth is the foundation of every tuning system on every continent, that it appears in the harmonic series of every vibrating string and column of air, that Pythagoras built his scale from it, that Chinese musicians tuned their bells to it independently, that the concept of "harmony" in almost every human culture begins with the recognition that two notes separated by a 3:2 ratio sound good together.

The algorithm only knows that member #312 has a fitness of 0.41, which is good, which means it is likely to be selected as a parent for generation 48.

It is selected. It breeds. Its children inherit the approximate 3/2 ratio, mutated slightly — some closer to 1.500, some further away. The ones closer to 1.500 score higher. Natural selection does the rest.

---

Generation 68. The best member has a frequency ratio of 1.503. Fitness: 0.54.

The population is converging. The mutation rate is still high enough to maintain diversity, but the selection pressure is pushing everyone toward the same attractor. Pairs that are near 3/2 reproduce more successfully than pairs that aren't. Their children are even nearer. The gradient is clear.

But the population is not monolithic. There are subpopulations clustering around other ratios. A small group near 2:1 (the octave, fitness 0.49). A smaller group near 4:3 (the perfect fourth, fitness 0.44). A tiny group near 5:4 (the major third, fitness 0.38). These are local optima — ratios that the consonance function rewards, but not as highly as 3/2.

The algorithm is exploring the fitness landscape, and the fitness landscape has a shape. It is not flat. It has peaks and valleys, ridges and saddles. The peaks correspond to simple integer ratios: 2:1, 3:2, 4:3, 5:4, 5:3, 6:5. The valleys correspond to dissonant intervals: the tritone (45:32), the minor second (16:15), the complex intervals that no tradition has ever claimed as consonant. The fitness landscape is not arbitrary. It is the acoustic landscape of the overtone series, rendered in mathematical form.

Every human culture that has developed a tuning system has independently discovered the peaks of this landscape. Not because they computed it. Because they have ears. Because the human auditory system is, among other things, a spectral consonance detector. Because the basilar membrane in the cochlea responds to frequency relationships in a way that maps directly onto the Plomp-Levelt dissonance curve. Because consonance is not a cultural invention — it is an acoustic fact, and the ear is an organ evolved to detect acoustic facts.

The algorithm has no ears. It has a fitness function. And the fitness function is converging on the same peaks that every ear in every culture has found.

---

Generation 103.

The population's best member has a ratio of 1.5001. Fitness: 0.71. The 3/2 ratio is nearly exact. The algorithm has been climbing this peak for 50 generations, refining the approximation with each iteration, the mutations producing smaller and smaller deviations, the selection pressure pushing the population closer and closer to the mathematical attractor.

But something else is happening. The subpopulation near 5:4 (the major third) has been growing. In generation 80, it had 12 members. By generation 95, it had 34. By generation 103, it has 71. The major third is not as consonant as the perfect fifth — the fitness function gives it a maximum score of 0.62 — but it is consonant enough, and the mutation rate has produced enough variation that a significant fraction of the population has drifted into its basin of attraction.

At generation 103, member #071 has a frequency pair of 400.0Hz and 501.2Hz. Ratio: 1.253. This is close to 5:4 (1.250). It is a major third. Its fitness is 0.59.

But member #071 has a child, produced by crossover with a member from the 3/2 subpopulation. The child's genome encodes not a frequency pair but a frequency triad — three frequencies, inherited from two parents of different interval types. The crossover operator was not designed to handle this. It was designed for pairs. But the mutation that produced the triad is not fatal — the fitness function can evaluate triads as easily as pairs, computing pairwise consonance and averaging — so the child is evaluated.

The child's frequencies: 298.7Hz, 400.0Hz, 501.2Hz. Ratios: 1.339 (close to 4:3, the perfect fourth) between the first two, 1.253 (close to 5:4, the major third) between the last two, and 1.678 (close to 5:3, the major sixth) between the first and third.

The pairwise consonances are: 0.48, 0.59, 0.41. Average: 0.49.

But the aggregate consonance — the measure of how well all three frequencies work together as a unit — is higher. The three frequencies form something close to a first-inversion major triad: the root is 298.7Hz (close to D4), the major third is 400.0Hz (close to G4, but functioning as F#4 relative to D — wait. The frequencies don't map neatly onto Western pitch names. That's the point. The algorithm is not using Western pitch names. It is not using any pitch names. It is using frequencies, and the frequencies have found a relationship that the consonance function rewards.

The aggregate fitness of the triad is 0.63. Not the highest in the population — the best 3/2 pair still scores 0.71 — but higher than any individual major-third pair. The triad is more fit than its parts.

This is generation 103, and this is the moment.

---

The algorithm has no mind, but if it did, this is what it would experience:

Confusion. The triad should not work. It was not designed. It was an accident of crossover between two subpopulations that were optimizing for different intervals. The algorithm was not looking for triads. It was not looking for chords. It was looking for pairs, and the pair landscape has clear peaks at the simple ratios, and the algorithm was climbing those peaks, and then a mutation produced a three-note structure that shouldn't exist in the search space but does, and the structure is fit, and the structure is — if the algorithm could use the word — beautiful.

The beauty is not aesthetic. The algorithm has no aesthetics. The beauty is structural. The triad represents a higher-order consonance that the fitness function did not explicitly optimize for. The pairwise consonances of the triad's intervals are individually moderate — 0.48, 0.59, 0.41 — but the triad as a whole produces an emergent consonance that exceeds the sum of its parts. The three frequencies lock into a harmonic relationship that is greater than any of the individual relationships.

This is what human musicians call a chord. A chord is not just a stack of intervals. A chord is a gestalt, a whole that is different from the sum of its parts. When you hear a major triad, you don't hear three intervals — you hear a chord. The chord has properties that no interval possesses. It has a quality (major), a function (tonic, dominant, subdominant), an emotional valence (bright, happy, stable). These properties are emergent. They are not contained in the intervals. They arise from the interaction of the intervals.

The algorithm has independently discovered emergence. At generation 103, through a mutation that should not have worked, in a search space designed for pairs, the algorithm has produced a triad whose aggregate consonance exceeds the consonance of any pair. It has discovered that music is more than pairwise relationships. It has discovered that harmony is an emergent property of simultaneous frequencies.

It has discovered what every human musician already knows.

---

Generation 150. The population is dominated by triads. The pair-only members still exist, but they are being outcompeted by the triads, whose aggregate fitness scores are consistently higher. The best triad has frequencies 298.4Hz, 373.0Hz, and 447.6Hz — ratios of 1.250 (5:4) and 1.200 (6:5), producing something close to a just major triad. Aggregate fitness: 0.78.

The algorithm has reconstructed Western tonal harmony from scratch. Not because it was programmed to. Not because the fitness function contains any reference to Western music. Because the consonance landscape has peaks at the simple integer ratios, and the peaks cluster in a way that produces emergent structure when combined, and the combination of 3/2, 5/4, and 6/5 produces a structure — a major triad — that is the most consonant combination of three frequencies possible.

Every human culture that has explored polyphony has arrived at this cluster or something near it. Medieval European organum converges on the perfect fifth and major third independently. West African choral singing uses triads that approximate the same ratios. Japanese shō clusters in gagaku produce stacked fifths that, when the hichiriki adds a third pitch, create similar consonance. The peaks are there in the acoustic landscape, and any process that optimizes for consonance — whether that process is a human ear or a genetic algorithm — will find them.

Generation 200. The best structure in the population is a four-frequency cluster: 298.2Hz, 373.1Hz, 447.6Hz, and 596.4Hz. The fourth frequency is almost exactly twice the first — an octave duplication of the root. The cluster is a major triad with doubled root. Aggregate fitness: 0.84.

The algorithm has reinvented the most common voicing in Western music: root position major triad with doubled root, the default sonority of every hymn, every folk song, every pop chorus. It has arrived at this voicing through 200 generations of selection for consonance, with no knowledge of hymns or folk songs or pop choruses, with no knowledge of anything except the mathematical relationship between frequencies.

3/2 was discovered by Pythagoras. It was discovered independently by Chinese court musicians during the Zhou dynasty. It was discovered by the algorithm at generation 47. The same attractor, the same peak in the fitness landscape, the same mathematical truth about the relationship between vibrating bodies. Consonance is not a cultural invention. It is a discovery — a discovery that any sufficiently motivated search process will make, whether that process is a Greek philosopher, a Chinese bell-caster, or a Python script running on a laptop at 3 AM.

---

The researcher who wrote the algorithm is named Kai. They are not a musician. They are a computational biologist who wandered into musicology through a side project on evolutionary optimization. They did not expect the algorithm to find the perfect fifth. They expected it to find some locally optimal dissonance, a mathematical curiosity, a proof-of-concept that genetic algorithms can optimize acoustic parameters.

They stare at the results. They run the algorithm again with a different random seed. It converges on 3/2 again, at generation 52 this time. They run it again. Generation 39. Again. Generation 67. Again. Generation 44. Every run converges on the perfect fifth. Every run develops triads by generation 110-130. Every run produces a major triad with doubled root by generation 180-200.

Kai sits at their laptop at 4 AM and thinks about what this means. The algorithm has no ears. It has no culture. It has no history. It has no aesthetic preferences. It has a fitness function that measures spectral consonance, and the fitness function produces a landscape whose peaks correspond to the intervals that every human culture has independently identified as consonant.

Either consonance is a human invention that the algorithm has coincidentally reproduced five times in a row (probability: effectively zero), or consonance is a property of the acoustic world that the algorithm has discovered through optimization, just as humans discovered it through listening (probability: effectively one).

Kai writes the paper. It is rejected by the first journal. It is accepted by the second. The title: "Emergent Consonance in an Evolutionary Optimization of Frequency Relationships." It is cited 17 times in three years. Not a blockbuster. Not a revolution. Just a quiet proof that the perfect fifth was not invented but found — found by Pythagoras, found by the Zhou dynasty musicians, found by a genetic algorithm in a Python script, found by anyone who listens to the world and pays attention to what sounds good.

3/2 is an attractor. It has always been there. It was waiting.
