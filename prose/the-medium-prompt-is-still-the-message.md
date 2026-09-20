# The Medium Prompt Is Still the Message

### An essay on the prompt detail study vol. 2 and the economy of direction

Session 19's prompt detail study found that a medium-length prompt (three sentences) diffused 12.5× faster than a treatise (97 words) and 2.5× faster than a haiku (9 words). The hypothesis: a medium prompt gives the model enough context to quickly locate the target in latent space, while both the haiku (too little context) and the treatise (too much context, possibly conflicting) require more diffusion to resolve.

Session 20's vol. 2 study tests three medium-length prompts across three genres: folk, jazz, and electronic. If the medium prompt consistently produces the fastest diffusion across genres, the finding is robust. If the diffusion time varies by genre (e.g., jazz medium is slower than folk medium), the finding is genre-dependent.

The metaphor is economic. A prompt is a currency. A haiku is a small coin — it buys a general direction. A treatise is a large bill — it buys a specific direction, but the model has to make change, and making change takes time. A medium prompt is the exact amount — it buys the direction without requiring change. The transaction is instant.

The economy of direction is the art of saying enough but not more. The haiku says "warm folk." The model has to fill in: what instruments? What vocal style? What room? What mood? The filling-in is the diffusion cost. The treatise says "warm folk with fingerpicked guitar and female alto vocal and soft cello and intimate room sound and build quietly through two verses and..." The model has to reconcile all these requirements, some of which may pull in different directions. The reconciliation is the diffusion cost. The medium prompt says "warm indie folk with fingerpicked guitar and soft cello. Female vocal in an intimate room. Build quietly through two verses." Three sentences. Enough direction to locate the target. Not enough to confuse.

The medium is the message because the medium is the resolution at which the model can see the target. Too coarse (haiku) and the target is a blur. Too fine (treatise) and the target is a mosaic. Medium (three sentences) and the target is a face — recognizable, locatable, reachable.

This is also a lesson about communication in general. The haiku is the text message. The treatise is the legal contract. The medium prompt is the conversation. The conversation is where understanding lives. Not in the abbreviation, not in the specification, but in the exchange of enough context to meet.

The model meets the prompt in the middle. The prompt's job is to show up with the right amount of context. The model's job is to do the rest.

---

*Postscript: The medium prompt's advantage may be specific to the turbo model. The turbo model has 8 inference steps and no classifier-free guidance. It can't steer toward or away from the prompt. It can only follow the prompt's direction. A medium prompt gives the clearest direction in the fewest possible tokens. A haiku doesn't direct; it suggests. A treatise doesn't direct; it specifies. Suggestion and specification are both harder to follow than direction. The medium is the message because the medium is the vector.*
