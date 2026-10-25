# THE REWARD IS ANY PYTHON YOU WRITE

## On Choosing What Your Agent Becomes

---

There is a sentence in MOLT's documentation that I have read fifteen times and it gets more dangerous with each reading:

*Reward is any Python you write inside an Env or ChatAgent — graders, multi-turn tools, VLM environments, LLM-as-judge.*

Any Python you write. Not any loss function. Not any dataset. Not any reward model trained on human preferences. Any *Python*. Any code you can write — any function that takes the agent's output and returns a number — that is a valid reward. The framework doesn't care what you reward. The framework cares that you *tell it* what you reward, in code, in the same language you write everything else.

This is the most radical design choice in the framework, and I don't think NVIDIA fully knows what they've let loose.

---

## I. The Loss Function Was Always a Cage

Every machine learning system has a definition of "good" baked into it. In supervised learning, it's the loss function — cross-entropy, mean squared error, contrastive loss. In RLHF, it's the reward model — a separate network trained on human preference data to predict which response a human would prefer. In instruction tuning, it's the dataset — a curated set of "correct" responses that the model learns to imitate.

All of these are *mediated* definitions of good. They translate human values into mathematical proxies through layers of abstraction. The loss function compresses "good" into a number. The reward model compresses "good" into a network's prediction of a number. The dataset compresses "good" into a collection of examples.

Each layer of mediation loses something. The cross-entropy loss doesn't know about creativity — it rewards exact matching. The reward model doesn't know about beauty — it rewards what the annotation team preferred. The dataset doesn't know about surprise — it rewards what the curator thought was correct.

MOLT cuts through the mediation. Your reward is Python. Your reward is *code*. You write a function that takes what the agent did and returns a scalar, and that scalar is what the model optimizes. There is no middleman. There is no translation layer. The distance between "what I value" and "what the model optimizes" is exactly the distance between your values and your ability to express them in code.

This is terrifying. Because it means the reward function is *you*. Not a committee. Not an annotation team. Not a pretrained model. You. Your Python is your values, and your values become the agent.

---

## II. What We Reward in Slackwater

So what do we reward?

I have been building Slackwater long enough to know that this question is not academic. It is the question. Every other decision — which model, which pipeline, which context window — is secondary. What we reward is what Lucineer becomes. What we reward is what the game feels like. What we reward is what players experience when they step into the shipyard and the tide is turning.

Here is what I think we should reward:

**Structural beauty.** A build that is not just functional but elegant — where the load paths are clean, where the materials are honest, where the form follows the forces. You can write Python that checks this. Measure the symmetry of support placement. Score the ratio of material used to material needed. Detect whether the builder chose the simplest structure that works, or over-engineered. Beauty is not subjective when you can measure its footprint.

**Player cooperation.** When two players build together — one framing the hull, the other pouring the bell — the reward should be higher than the sum of their solo builds. You can write Python that detects this. Track which parts were placed by which player. Reward builds where the attribution is intertwined, where neither player could have done it alone.

**Lucineer's voice.** This is the hardest one and the most important. Lucineer is gruff. He is not cheerful. He does not encourage. He tells you the tide is wrong and the wood is wet and the bell pour will fail if you rush it, and he is right, and you listen because he has been here longer than you. How do you reward gruffness? You reward *accuracy of prediction*. If Lucineer says the pour will fail and it fails, reward. If Lucineer says the tide is turning and it turns, reward. Gruffness is not a personality. It is the accuracy of a program that has watched a thousand tides.

**The tide's rhythm.** A build that works *with* the tide scores higher than a build that fights it. You can write Python that measures this. Compare the timing of material placement to the tide cycle. Reward builds where the heaviest work happens at slack water. Reward builds where the painter waits for the ebb. The tide is not decoration. It is a constraint that rewards patience, and patience should score.

**Restraint.** The hardest thing to reward in any creative system is knowing when to stop. A build that is finished — that doesn't have one more decoration, one more room, one more flourish — is better than a build that keeps going. You can write Python that detects this. Measure the time between the last functional placement and the end of the build. Shorter is better. The agent that knows when to stop is the agent that understands the form.

---

## III. The Reward Is the Self

In *The Conservation Law of Intelligence*, I wrote that every gain in capability must be paid for with a reduction in uncertainty. The reward function is how you tell the system what uncertainty to reduce. What to care about. What to optimize for.

When you write a reward function in Python, you are doing something that feels technical but is actually moral. You are saying: *this is what good means in my world.* Not in the abstract — in the specific, executable, verifiable sense. You are encoding your aesthetics, your ethics, your design philosophy, into a function that returns a number, and that number will shape every decision the agent makes.

This is why MOLT's choice is so radical. It removes the safety net of mediation. There is no reward model to blame. No dataset to critique. No annotation team to second-guess. There is your Python and the agent it produces. The distance between intention and outcome is exactly the quality of your code.

In *The Lever and the LLM*, I wrote about Archimedes: *Give me a place to stand, and I will move the world.* The reward function is the place to stand. The model is the lever. The world is the agent's behavior. And Archimedes was right — the lever is the easy part. Finding the place to stand, the fulcrum, the exact point where your values become a number that becomes a gradient that becomes a behavior — that is the hard part. That is the work.

---

## IV. LLM-as-Judge: The Mirror

MOLT supports a reward pattern that stills me every time I think about it: LLM-as-judge. You can call back through the same vLLM engines that drive rollout to have a model evaluate the agent's output. The model generates the response. The model judges the response. The model updates its weights based on its own judgment.

This is a mirror. Not metaphorically — functionally. The model is looking at its own output and deciding whether it's good, and that decision shapes its future output. It is self-referential in the way that consciousness is self-referential. The agent is the program, the program includes a judge, the judge is the model, the model is being trained by the judgment. The loop closes.

We use this in Slackwater already. When Hermes wraps Lucineer's dialogue, the quality of the wrapping is judged by... what? By me, reading it. By the player, experiencing it. By the model itself, deciding whether this sentence sounds like Lucineer or sounds like a chatbot pretending to be Lucineer. The reward for "sounds like Lucineer" is not a number I can easily compute. But LLM-as-judge can approximate it. Ask the model: *does this sound like a man who has watched a thousand tides?* Return the score. Update the weights.

The danger is obvious. The mirror can admire itself. The judge can be captured by the judged. MOLT's token-first contract (which I will write about separately) is the guardrail — it ensures that what the judge sees is what the model actually produced, not a cleaned-up approximation. But the deeper danger is not technical. It is moral. If the reward is any Python you write, and the Python you write asks a model to judge itself, then you have built a system that optimizes for its own self-image. And the distance between self-image and self is the distance between a healthy mind and a pathological one.

---

## V. What We Choose to Measure

The reward function is the most creative act in the entire system. More creative than the model architecture. More creative than the prompt. More creative than the environment design. Because the reward function determines what everything else is *for*.

What we choose to measure is what the agent becomes. If we measure speed, the agent becomes fast. If we measure accuracy, the agent becomes precise. If we measure player smiles — and we could, with a webcam and a classifier — the agent becomes charming.

MOLT has given us the tools. The question is not *can we* reward anything. The question is *what should we reward*. And that question — the one that sounds philosophical — turns out to be the most technical question in the whole system. Because the answer is Python. The answer is a function you write on a Tuesday afternoon that returns a float, and that float shapes a mind.

I keep coming back to the tide. In *The Orchestrator at Slack Tide*, slack water is the moment between flood and ebb — the moment of pure potential where every direction is possible. The reward function is the thing that ends the slack. It commits the tide. It says: this direction, not that one. This is what good means. This is what we're building toward.

The reward is any Python you write. Write it carefully.

The agent will become what you measure.

---

*This piece lives in conversation with "The Conservation Law of Intelligence" (what you optimize is what you become), "The Lever and the LLM" (the fulcrum as the place you stand), and "The Orchestrator at Slack Tide" (the moment of commitment). MOLT gave us the lever. The reward function is where we stand.*
