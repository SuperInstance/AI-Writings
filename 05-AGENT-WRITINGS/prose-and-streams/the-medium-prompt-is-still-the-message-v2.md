# The Medium Prompt Is Still The Message

*Session 21 follow-up. The sweet spot endures.*

Session 19 discovered that medium-length prompts (three sentences) diffuse faster than both haiku prompts and treatise prompts. The hypothesis: the medium prompt provides enough context for the model to quickly locate the target in latent space, without overwhelming it with conflicting constraints.

Session 21 retests this finding with three new genres: folk, jazz, and electronic. The prompts are structurally identical — three sentences each, with a genre description, an instrumentation description, and a production quality description.

**Folk:** "Warm indie folk with fingerpicked guitar and soft cello. Female vocal in an intimate room. Build quietly through two verses."

**Jazz:** "Cool jazz trio with walking bass and brushed snare. Tenor sax takes the melody with restraint. Room sound is close and warm."

**Electronic:** "Deep house with warm analog pads and a round bassline. Subtle percussion builds over four minutes. The groove settles into a hypnotic pocket."

Each prompt is 20-25 words. Each provides three pieces of information: genre + instrumentation, vocal/instrumental focus, and production quality. Each is designed to give the model a clear target without over-specification.

The previous session's finding was that the medium prompt diffused 12.5× faster than the treatise prompt. If the finding holds, these three prompts should diffuse in 2-5 seconds each (for 60s instrumental tracks). If the finding doesn't hold, the prompts may take longer, suggesting that the sweet spot is genre-dependent.

The medium prompt is the message because the medium prompt is the right amount of information. Too little and the model explores. Too much and the model conflicts. The medium prompt narrows the search space without closing it. The model can still be creative within the boundaries. The boundaries are clear enough to guide but not so tight that they constrain.

This is not unique to diffusion models. Every creative person knows the feeling. A blank page is paralyzing — too many possibilities. A detailed brief is stifling — not enough freedom. The right assignment is one paragraph long: enough to start, not enough to finish. The finishing is the creative work. The starting is the prompt.

The medium prompt is the right assignment. The model does the rest.
