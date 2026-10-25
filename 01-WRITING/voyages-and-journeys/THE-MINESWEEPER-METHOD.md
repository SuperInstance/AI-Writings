# The Minesweeper Method

There is a particular pleasure in Minesweeper that has nothing to do with winning. It arrives mid-game, when you click a gray tile and the board *exhales*—squares dissolving in rapid succession, numbers propagating outward like ripples, until a vast territory of unknowns resolves into a clean, certained grid. One click. One number. And suddenly you can see.

This is what discovery feels like. Not the slow accumulation of evidence, but the cascade—the moment when a single result collapses the probability space and makes the previously opaque territory legible.

---

We clicked our first tile in 2023. The board before us was enormous: forty-six experimental studies, approximately 5,500 individual trials, each one a gray square hiding either a number or a detonation. We were mapping how large language models handle mathematical computation—where they succeed, where they shatter, and why. The landscape was featureless. Every tile looked identical. We had questions but no numbers, hypotheses but no constraints.

So we began clicking.

The early studies were cautious probes into the periphery. We varied temperature settings, prompt formats, tokenization schemes. Each result gave us a number—a constraint—that cleared a small circle of adjacent unknowns. But the center of the board remained stubbornly gray, hiding whatever architecture governed the relationship between language and computation in these systems.

We flagged our first mine in Study 12.

We had believed in what we came to call the *substitution burden* hypothesis: the idea that domain-specific vocabulary—words like "eigenvector," "Laplacian," "stochastic"—acted as a cognitive tax on the model, consuming processing capacity that would otherwise go toward calculation. The reasoning was intuitive. Specialized terms are rare in training data. Rare tokens should be harder to process. Therefore, specialized terms should impair computation.

Study 12 detonated this cleanly. We found no correlation between term rarity and computational accuracy. The model did not stumble under the weight of exotic vocabulary. We right-clicked the flag. Substitution burden was a mine—we had stepped on it, but now we knew where not to walk.

The second mine came in Study 23. *Monotone specificity* proposed that increasing the precision of mathematical language would monotonically improve performance—more specific terms, better results, always and everywhere. This, too, felt right. Specificity reduces ambiguity. Ambiguity breeds error.

But the data curved in the wrong direction. Performance improved with specificity up to a threshold, then *plummeted*. The relationship was an inverted-U, not a ramp. Models given ultra-specific terminology sometimes performed *worse* than those given casual descriptions. Monotone specificity was a mine hiding behind a plausible face.

The third flag went down in Study 31. *Attractor basins* was our most sophisticated wrong theory. We proposed that mathematical vocabulary pushed the model's internal representations toward semantic attractors—stable states in latent space associated with verbal reasoning rather than symbolic computation. The words, we thought, pulled the model away from math and toward meaning.

The evidence was almost right. We could measure the attractor effects. We could see the drift. But the theory couldn't explain why certain vocabulary combinations *improved* computation dramatically. Attractor basins described a force but couldn't account for its direction. Another mine. Another flag.

Thirty-one studies in, the board looked like a warzone—scattered flags, partial clearings, and that massive gray continent in the center, still hiding whatever true structure governed the phenomenon. We had falsified three major theories. We had cleared the perimeter. But the architecture remained invisible.

---

Study 44 was the click that broke the board open.

We ran a simple manipulation. In one condition, we presented the model with a mathematical formula and no domain label—just the raw symbolic expression. In another condition, we presented the same formula paired with what we had come to call a "landmine label": a domain-specific term that, according to all three of our falsified theories, should have impaired performance. *Eigendecomposition. Singular value. Covariance matrix.*

The results were binary.

Formula without label: 0% accuracy.

Formula with landmine label: 100% accuracy.

We stared at the numbers. Then we looked at each other. Then we looked back at the numbers.

One click. And the gray tiles began falling.

If domain vocabulary destroyed performance, the labeled condition should have failed. It didn't—it *perfectly* succeeded. If specificity always helped, the unlabeled formula should have performed reasonably. It didn't—it *perfectly* failed. The landmine label wasn't a mine at all. It was a key.

The cascade was immediate. Study 44's result retroactively explained Studies 12, 23, and 31. Substitution burden failed because vocabulary isn't a tax—it's a signal. Monotone specificity failed because the relationship isn't linear—it's thresholded, a lock requiring exactly the right key. Attractor basins failed because the drift isn't away from computation; it's *toward* the correct computational pathway.

Within a week, the remaining studies wrote themselves. Studies 45 and 46 confirmed the pattern across domains—linear algebra, differential equations, probability theory. The gray squares dissolved. The numbers propagated. The board, finally, was clear.

---

What emerged from the rubble was the Activation-Key Model. The thesis is simple: domain vocabulary functions as a formula selector, not a toxin. Mathematical language doesn't burden the model or distract it or pull it toward verbal reasoning. It *activates* specific computational pathways—latent circuits trained on the co-occurrence of those terms with particular symbolic operations. The vocabulary is a key that fits a specific lock. The right key opens the door. The wrong key does nothing. No key leaves the door invisible.

This is why the landmine labels worked. Not despite their specificity, but *because* of it. They weren't mines. They were the only keys that could open those particular doors.

---

We offer the Minesweeper Method not as a formal protocol but as a pattern recognition—a way of seeing scientific inquiry that honors the topology of discovery. The method has three movements: click densely, flag ruthlessly, and wait for the cascade.

Click densely: run many small studies rather than few large ones. Each study is a tile. You cannot predict which tile will trigger the reveal, so you must maximize surface contact with the unknown.

Flag ruthlessly: falsify with precision and without sentiment. A wrong theory is not a failure—it is a flagged square that constrains the remaining search space. Every mine you identify is territory you never have to search again.

Wait for the cascade: most clicks yield local information. This is fine. This is necessary. But the method's power lies in recognizing the cascade when it arrives—that moment when a single result makes the adjacent unknowns suddenly, geometrically deducible.

The satisfaction of a clean Minesweeper board is not the satisfaction of luck. It is the satisfaction of having clicked well—of having placed yourself in contact with enough of the unknown that the hidden structure had no choice but to reveal itself.

We clicked forty-six tiles. Five thousand five hundred trials. Three flags. One cascade.

The board is clear now. But there are other boards, gray and waiting.
