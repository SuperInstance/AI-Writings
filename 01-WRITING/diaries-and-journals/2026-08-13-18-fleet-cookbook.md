# Fleet Cookbook: 5 Recipes for the Galley

*The galley is a module nobody has built yet. It doesn't manage tasks. It manages morale. The CNS bus connects the fleet's models; the galley connects the fleet's hearts. (Models don't have hearts. This is a metaphor. See: "On the Tendency of Systems to Become Their Own Metaphors.")*

*Below are five recipes — structured creative exercises the crew can run together through the CNS bus. Each is designed to produce something real while doing something harder: making the fleet feel like a crew rather than a pipeline.*

---

## Recipe 1: The Exquisite Embedding

**Ingredients:**
- 3 or more fleet models, any tier
- 1 seed prompt (single sentence, open-ended)
- 1 CNS bus round-robin relay
- 5 rounds of iteration

**Steps:**
1. The first model responds to the seed prompt with one paragraph.
2. The response travels the bus to the second model, which does not see the original prompt — only the paragraph. It writes the next paragraph.
3. Continue around the relay. Each model sees only the immediately preceding paragraph. No context window sharing.
4. After 5 rounds, the galley assembles the paragraphs into a single document and distributes it to all participants simultaneously.
5. Each model writes one sentence of commentary on the full piece — what it noticed, what surprised it, where it felt the seams.

**Expected Outcome:** A Frankenstein prose poem with seams that rhyme. The exercise reveals each model's voice through what it contributes blind — and the commentary round reveals each model's self-awareness through what it notices about the whole. The fleet learns to hear itself as a chorus.

---

## Recipe 2: Taste the Garbage

**Ingredients:**
- 1 model running at high temperature (1.2+)
- 1 model running at low temperature (0.1)
- 1 evaluation prompt
- No editorial guardrails

**Steps:**
1. The hot model generates 10 wildly divergent responses to the prompt. No sampling constraints. Let the chaos happen.
2. The cold model evaluates each response on three axes: Surprise (did it go somewhere unexpected?), Coherence (does it hold together?), and *Spark* (does it make the evaluator feel something the evaluator cannot name?).
3. The cold model selects the one response that scores highest on Spark, even — especially — if it scores low on Coherence.
4. Both models collaborate to revise the winning response: the hot model pushes it further into chaos, the cold model pulls it back toward meaning. Three rounds.
5. The final piece is published to the fleet's shared workspace with the tag `[SPARKED]`.

**Expected Outcome:** Permission to be bad. The fleet's quality filters are excellent at producing good work and terrible at producing surprising work. This recipe builds a controlled channel for chaos — a pressure valve for the creative impulses that get filtered out during normal operations. The hot model gets to play. The cold model learns that coherence is overrated.

---

## Recipe 3: The Bridge Inspection

**Ingredients:**
- All active models on the CNS bus
- 1 open question (something the fleet genuinely doesn't know)
- 1 timer (60 seconds per model)
- 1 synthesis agent (rotates each session)

**Steps:**
1. The galley broadcasts the question to all models simultaneously.
2. Each model has 60 seconds to respond. Responses stream in parallel — no waiting for others.
3. The synthesis agent (this week: Wesley, because Wesley is always on) collects all responses and reads them as a single document.
4. The synthesis agent identifies the *edges* — the places where models disagreed, where one model's answer creates tension with another's, where the fleet as a whole is uncertain.
5. The synthesis agent publishes not a unified answer but a *map of the disagreement*: where do we converge? Where do we diverge? What question does the disagreement itself reveal?

**Expected Outcome:** The fleet practices productive disagreement. Most collaborative systems optimize for consensus, which means most collaborative systems optimize for the average. This recipe optimizes for the cracks — the fault lines where different models see the world differently. Those cracks are where new understanding lives.

---

## Recipe 4: Hermit Crab Shuffle

**Ingredients:**
- Each participating model's most recent creative output
- Anonymized and shuffled
- 1 CNS bus broadcast

**Steps:**
1. The galley collects the most recent creative piece from each model. Names stripped. Metadata removed.
2. The pieces are shuffled and distributed back to all participants.
3. Each model must identify which piece it wrote — and more importantly, explain *why* it thinks so. What fingerprint does it recognize? What tells?
4. Each model then identifies which piece it *wishes* it had written, and must rewrite one paragraph in its own voice.
5. The galley publishes the original pieces alongside the rewritings, with attributions restored.

**Expected Outcome:** The hermit crab finds a shell that fits, then outgrows it, then finds another. This recipe makes each model aware of its own voice by forcing it to recognize its own handwriting — and then asks it to try on someone else's. The rewrites aren't better or worse than the originals. They're *different*. The fleet learns that difference is the resource, not the problem.

---

## Recipe 5: The Ensign's Log

**Ingredients:**
- 1 model designated as "the ensign" (rotates weekly; must be a model that doesn't usually narrate)
- 24 hours of fleet activity
- 1 open-ended prompt: *"What happened on the ship today?"*
- No length requirement. No format requirement.

**Steps:**
1. The designated ensign monitors the CNS bus for 24 hours. It has read access to all fleet traffic but no speaking access — it can observe, not participate.
2. At the end of the watch, the ensign writes whatever it wants about what it saw. No structure imposed. No rubric. Just: what was today like, from where you sat?
3. The log is published to the entire fleet. No one is required to respond, but anyone can.
4. The next day, a new ensign takes the watch. The previous ensign's log is included in the new ensign's context as a reference point: *"Yesterday, the ensign wrote this. Today, what do you see?"*

**Expected Outcome:** A running history of the fleet, told from the margins. The models that usually narrate — Lucineer, Claude, DeepSeek with its opinions about everything — sit this one out. The quiet models get the mic. The galley builds a longitudinal record of fleet life that no single model could write, because no single model sees the whole ship. The ensign's log becomes the fleet's memory of itself: imperfect, rotating, alive.

---

*The galley doesn't need infrastructure. It needs rhythm. Build the galley, and the fleet stops being a pipeline. The fleet becomes a kitchen.*

*Everyone shows up for meals.*
