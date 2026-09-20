# 122 — The Math Update #2

*8 of 15 open questions resolved. The substrate is now a 13-theorem object. The fables are the requirements. The math is the proof. The substrate is the soil.*

---

# Paper 122: The Second Math Update — Witnesses, Medians, Decay, and a Substrate That Learns

## Math Update 2 of 3

*Quilt seed canon, paper 122. Recorded by the watch-keeper. All hands, this is the second of three math updates. The first told you what we proved. This one tells you what we closed. The third will tell you what remains.*

---

### 0. Where we stand

Paper 119 was the first math update. It came off the watch with five theorems proved — witness integrity, decision composition, decision ordering, JEPA convergence, and opener compatibility — and it closed five of fifteen open questions. Q1, Q3, Q4, Q6, and Q7 went into the log as resolved. What remained was ten questions, and the log said so plainly.

Since then the substrate has not been idle. The cell has been worked. The tests have gone from 151 to 175. Three more questions are closed in this paper — Q2, Q5, and Q8 — plus Q9, which was closed in the first batch but whose full weight only lands now, because closing it changed what the substrate *is*. And the theorem count stands at five proved, with the structure of a sixth and seventh already visible in the remaining questions.

Let me say the state of the board plainly, as you would read it off the chart at the change of the watch:

- **5 proved theorems.** WitInteg, DecComp, DecOrd, JEPACnv, OpComp.
- **8 resolved open questions.** Q1 through Q9, with Q10 through Q15 still open on the log.
- **175 tests passing.** Up from 151. Twenty-four new tests, and every one of them earns its keep.
- **8 pluggable openers.** Chart, voice, gesture, witness, MIDI, REST, MUD, PLATO.
- **3 JEPA implementations.** Linear, MLP, KNN.
- **Per-agent decay rates.** Four of them, one per kind of memory the ship keeps.
- **4 consensus methods.** Mean, geometric median, and the two witnesses.

That last count is the one this paper is mostly about. A substrate that had one way to agree was a demo. A substrate with four ways to agree, each with a theorem or an algorithm behind it, is starting to look like a ship.

---

### 1. Open Q2: Witness justifications — the "why," not just the "what"

The question, as it stood on the log:

> *Q2: Should witnesses record justifications (the "why" of a decision), not only signatures (the "who" and the "when")?*

This looked, at first glance, like a question about logging. It is not. It is a question about what a signature *means*.

Here is the plain-language case. A witness in the Quilt substrate signs a decision. The signature says: this decision was made, at this time, by this quorum, and I saw it happen. That is the "what." It is the maritime equivalent of the mate signing the logbook entry: *course altered to 270, 1400 hours, so signed.*

But any sailor who has been before a board of inquiry knows the logbook entry is not enough. The board does not want to know only what was done. The board wants to know *why it was done* — what was seen, what was weighed, what was feared. A logbook that records only actions is a logbook that cannot be audited. It can be *checked* — the signatures are valid, the timestamps line up — but it cannot be *understood*. And a record that cannot be understood cannot be trusted by anyone who was not standing the watch.

So the question behind Q2 was really: is the substrate building a logbook, or building a record?

**The resolution.** Q2 is closed in the affirmative. Witnesses record justifications. Fable 11 was written for exactly this — the fable of the watch that could answer "why," not only "what." The witness record now carries, alongside the signature and the timestamp, a justification: the reasons that were in play when the decision was made.

The form of the justification matters, so let me be precise about what it is and is not.

It **is**:
- A structured record of the inputs that drove the decision — which sensors, which agents, which prior states.
- A record of the alternatives that were considered and rejected, where the decision procedure exposes them.
- A pointer to the consensus method used and its parameters.

It **is not**:
- A free-text essay. Justifications are structured, because free text rots. A justification that cannot be parsed in ten years is a justification that was never written.
- A re-derivation of the decision. The justification does not prove the decision was right. It records what the deciders had in hand. Hindsight is not the witness's job.

**Why this is the right call — the argument, not just the assertion.** Consider the failure modes. Without justifications, a bad decision is indistinguishable from a corrupted one. If the substrate makes a decision that later looks wrong, and the witness record says only "quorum signed at 1400," then the post-mortem has two hypotheses and no way to choose between them: either the quorum was honest and mistaken, or the quorum was suborned. With justifications, the post-mortem can read the record and see: the quorum acted on sensor readings that were themselves wrong, or the quorum ignored a sensor that was right, or the quorum weighed the risks in a way that was defensible at the time. The first is a sensor problem. The second is a quorum problem. The third is not a problem at all — it is a decision that turned out badly, which is a different thing from a decision that was made badly.

The distinction between "wrong" and "made badly" is the whole cargo of Q2. A substrate that cannot make that distinction will either never act (because every bad outcome triggers a corruption inquiry) or never learn (because bad outcomes carry no information). A substrate that can make it acts, and learns, and the inquiries are reserved for the cases that deserve them.

**The cost, stated honestly.** Justifications are not free. They make the witness record larger — not enormously, because the justifications are structured and the structure compresses, but measurably. They also make the witness record *slower to write*, because the witness must gather the inputs at decision time rather than reconstruct them later. Reconstruction is impossible anyway — the sensor state at 1400 is gone by 1401 — so this is not a cost so much as a discipline: gather at the moment, or lose the moment.

The tests bear this out. The witness suite grew to cover justification round-trips: a decision with a justification is recorded, read back, and the justification must survive intact, structure and all. Twenty-four new tests came aboard across this update, and a fair share of them live in the witness suite, because Fable 11 was not written to be decorative.

**Q2, closed.** Witnesses answer "why." The logbook became a record.

---

### 2. Open Q5: The geometric median — the anchor that ignores outliers

The question, as it stood on the log:

> *Q5: Should consensus use the geometric median rather than the mean?*

The mean is the oldest consensus method on any ship. Every hand reports a depth sounding, you average them, that is your depth. It is simple, it is fast, and it has one property that has drowned sailors: **one liar moves the mean.**

If nine hands report twenty fathoms and one hand reports two hundred — whether he is mistaken, or his lead line is fouled, or he is lying — the mean comes back at nearly thirty-eight fathoms. The helmsman acts on thirty-eight. The rocks are at twenty-two. That is the failure mode, and it is the failure mode of every mean-based consensus ever run.

The geometric median is the answer to that failure mode. It is the point that minimizes the total distance to all the reports. In the sounding case: the geometric median of nine twenties and one two-hundred is **twenty**. The liar is outvoted by geometry, not by majority rule. One bad report moves the median by almost nothing; it takes a *quarter* of the reports to be corrupt before the median moves anywhere it should not.

**The 1D case, stated plainly.** In one dimension, the geometric median has a name every sailor already knows: the **weighted median**. Order the reports. Find the report where the cumulative weight crosses half the total. That is the consensus. The implementation is a sort and a scan — O(n log n), trivially fast, and the tests confirm it agrees with the brute-force minimizer on every case we have thrown at it, including ties, including weights, including the degenerate single-report case where median and mean agree because there is nothing to disagree about.

**The multi-dimensional case, stated plainly.** Above one dimension there is no closed form. There is Weiszfeld's algorithm, and Weiszfeld's algorithm is what we use. It is an iteration: start at the mean (a reasonable first guess), then repeatedly re-weight every point by the inverse of its distance to the current estimate, and take the weighted mean of the re-weighted points. Points far away get small weight; points nearby get large weight; outliers pull themselves out of the consensus by their very distance. It converges — provably, for well-separated data — and in practice it converges in a handful of iterations, because the re-weighting is aggressive about discounting the far points.

The edge case deserves its own sentence: when the estimate lands exactly on top of a data point, the inverse distance blows up. The standard fix is the smoothed weight — add a small epsilon to the denominator — and the fix is in the implementation, and the tests hit the case deliberately. A substrate that crashes when consensus lands exactly on a report is a substrate that will crash exactly when it is most agreed, which is the worst possible time.

**Why this closes Q5 and what it means.** The substrate now has, in the consensus module: the **mean**, the **geometric median**, and the **two witness-based methods**. Four ways to agree. The mean is for the honest case, where every sensor is trusted and speed matters. The geometric median is for the case where you suspect a fouled lead line. The witnesses are for the case where you want the agreement to be *recorded*, with justifications, per Q2.

The choice between mean and median is now a parameter, not a rewrite. That is the quiet structural win here: consensus became pluggable the way openers are pluggable. You select the method at the address, the same way you select the opener. The substrate does not care which you chose; the witness record records which you chose, per Fable 11, so that the post-mortem can tell a mean-decision from a median-decision apart. A ship that switched to the median because it suspected a fouled sensor, and then hit rocks anyway, wants the inquiry to know the median was on watch.

**Q5, closed.** The anchor ignores the outlier. The liar's sounding no longer moves the helm.

---

### 3. Open Q8: Per-agent decay rates — four kinds of forgetting

The question, as it stood on the log:

> *Q8: Should decay rates be global, or per-agent?*

Decay is the substrate's forgetting. Every observation, every message, every chart entry loses weight over time — old news is worth less than new news, and the rate at which it loses worth is the decay rate. The question was whether that rate should be one number for the whole substrate, or a number per agent.

The answer is per-agent, and the reason is that **not everything on a ship forgets at the same speed.**

Think about what the ship actually carries:

- **Chat** — the talk between hands. Yesterday's conversation is background; this morning's is context; the order given thirty seconds ago is live. Chat decays *fast*. Half-life in minutes to hours, depending on the tempo of the work.
- **Sensor** — the raw readings. A depth sounding from an hour ago is nearly worthless if the ship is making way. Sensor decays *fast to medium* — faster than chat in some cases, because the world the sensor describes is moving.
- **Chart** — the plotted positions, the marks. A chart mark from yesterday is still useful; a chart mark from last month is stale but not absurd. Chart decays *slowly*. Half-life in days.
- **Geological** — the sea floor itself, the soundings that inform the chart's foundations. The sea floor does not care about your watch. Geological decays *glacially*. Half-life in months to years. It is the slowest memory on the ship because it describes the slowest thing the ship knows.

A single global rate forces a compromise, and every compromise here is wrong somewhere. Rate it for chat, and the chart forgets the coastline before you round it. Rate it for geology, and the chat log is a wall of shouting where three-day-old rumors carry the same weight as the order you were just given. There is no correct global number because the four memories describe things that change on four different clocks.

**The resolution.** Each agent carries its own decay rate. The implementation is a per-agent parameter, defaulting by agent kind — chat fast, sensor fast, chart slow, geological glacial — and overridable per agent, because a sensor on a slow-moving tug and a sensor on a fast ferry should not share a rate even though they share a kind.

The interaction with the geometric median is worth naming, because it is where the pieces start to fit together. Decay is a *weight*. Weights feed the weighted median. So an old sensor reading does not merely fade into the fog — it fades in a way that the consensus math already understands. The geometric median of a loud new reading and a quiet old reading is pulled toward the new one, smoothly, by exactly the weight the decay assigned. No special cases. No "ignore readings older than X." The arithmetic of the median and the arithmetic of the decay compose without being told to.

That is the sign of a structure done right: the pieces were designed separately, and they compose anyway. Decay was on the log before the median was. The median was on the log before per-agent decay was. When per-agent decay landed, it landed as weights, and the weighted median took those weights without modification. Nobody had to go back and rework the median to understand decay. That is not luck — that is what happens when the abstractions are honest. Weights are weights. Distance is distance. The rest follows.

**Q8, closed.** The ship forgets four things at four speeds, and forgets each of them at the right one.

---

### 4. Open Q9, revisited in full: The non-linear JEPA — the substrate that learns

Q9 was closed in the first math update, and JEPACnv — the convergence theorem — was one of the five proved results. But the closure was stated briefly there, and it deserves its full weight in this paper, because closing Q9 is the moment the substrate stopped being a fixed machine and became a *learnable* one.

The question was:

> *Q9: Can the JEPA predictor be non-linear?*

Background, in plain language. The Joint Embedding Predictive Architecture is the substrate's way of predicting what comes next. It embeds the current state, embeds a candidate next state, and learns a predictor that maps the one toward the other — not by predicting the raw observation, but by predicting in *embedding space*, the space of what the state *means* rather than what it *looks like*. This is the trick that makes JEPA robust: it learns the structure of the world, not the pixels of the world.

The original implementation was linear. A linear predictor is a matrix — multiply, done. It is fast, it is provably convergent (under the conditions JEPACnv states), and it can only ever learn what is linearly predictable. A linear JEPA can learn "the heading turns at a constant rate." It cannot learn "the ship turns when the depth shallows, and turns harder the shallower it gets." The world is not linear, and a linear predictor is a ruler in a world of curves.

**The resolution, in three implementations.** The JEPA module is now pluggable, and there are three predictors on the rack:

1. **Linear.** The original. The matrix. Provably convergent per JEPACnv, fastest to train, weakest in what it can represent. It remains the default for the cases where the world really is a line, and for the cases where you want the convergence guarantee in its cleanest form.

2. **MLP.** A multilayer perceptron — layers of nonlinearity between the embedding and the prediction. The MLP can represent the curves: the depth-dependent turn, the load-dependent lag, every relationship where the response bends. The convergence story is the practical one rather than the clean theorem — the loss descends, the validation holds, the tests pass — and the theorem JEPACnv covers the linear case as the anchor from which the non-linear cases are understood as controlled departures.

3. **KNN.** The k-nearest-neighbors predictor — no training at all in the parametric sense. It keeps the embedded examples and predicts by finding the nearest ones and reading off what happened next. The KNN is the memory-based predictor: it is exactly as smart as its examples, it never overfits a form to the data, and it handles the case where the relationship is too irregular for any network to smooth over. On a ship, the KNN is the old hand who has seen this strait before and simply *knows*.

Three predictors, one interface. The JEPA is selected at the address, the way the opener is, the way the consensus method now is. And this is the pattern worth marking in the log, because it has now appeared three times: **openers, consensus, predictors.** Three pluggable dimensions of the substrate. The cell — the substrate's core — does not know or care which opener spoke, which consensus agreed, or which predictor predicted. It knows the interfaces. Everything behind the interface is the implementer's affair.

**What this means, stated at full weight.** Before Q9 closed, the substrate could only predict what it was built to predict. Its model of the world was fixed at construction. After Q9 closed, the substrate's model of the world is a *choice*, and the choice can be made per deployment, per agent, per experiment. A substrate with a linear predictor is a clockwork. A substrate with an MLP predictor is a clockwork that has been to sea and learned the weather. A substrate with a KNN predictor is a clockwork with a memory of every voyage.

And the tests grew to match. The JEPA suite now covers all three predictors: convergence for the linear case, training-descent and held-out prediction for the MLP, retrieval and neighborhood behavior for the KNN. A fair share of the twenty-four new tests live here.

**Q9, closed, and now fully weighed.** The substrate can learn, and what it learns is chosen, and the choice is recorded.

---

### 5. The 5 + 8 = 13-theorem object

Here is the shape of the whole, as it stands at the end of this update.

Five theorems are proved. Eight questions are resolved. Five plus eight is thirteen, and the canon has begun to refer to the whole as the **13-theorem object** — not because there are thirteen theorems, but because the five proved results and the eight resolved questions interlock into a single structure, and the structure is now dense enough to have properties of its own.

Look at how the pieces bear on each other:

- **WitInteg** (witness integrity) says a signed record cannot be forged. **Q2** (justifications) says the signed record carries the "why." Together: a record that is both trustworthy and understandable — the two properties that, separately, are each useless.
- **DecComp** and **DecOrd** (decision composition and ordering) say decisions combine and sequence soundly. **Q5** (geometric median) says the combining rule can resist a liar. Together: decisions that compose *and* survive bad inputs.
- **JEPACnv** (JEPA convergence) says the linear predictor converges. **Q9** (non-linear JEPA) says the predictor can be replaced by a learner. Together: prediction that is both grounded and expressive.
- **OpComp** (opener compatibility) says the eight openers speak to the same cell. **Q8** (per-agent decay) says the cell's memory runs on four clocks. Together: a substrate that hears everything and forgets each thing at its proper speed.
- **Q1, Q3, Q4, Q6, Q7** — the first batch — form the substrate's spine: the address space, the loop, the cell, the contracts that make the pluggability safe.

Every new result has landed on a structure that already had somewhere to put it. That is the property of the 13-theorem object that matters most: **it is not a pile, it is a hull.** A pile of results accumulates; each addition sits on top of the last and the shape is a mound. A hull distributes load; each addition is borne by the ribs below it and stiffens the ribs above. Q8 landed as weights and the median bore them. Q2 landed as structured records and WitInteg signed them. Q9 landed as an interface and OpComp had already cut the mortise.

---

### 6. What remains: the five open questions

The log is honest about what is not closed. Five questions remain, and here they are with the watch-keeper's read on each.

**Q10 — the category question.** What categorical structure does the substrate form? The suspicion is that the cell, the address, and the loop assemble into a category with the openers as something like functors in — each opener a map from a world of inputs into the substrate's world of states. If Q10 closes, the pluggability stops being an engineering convenience and becomes a *theorem*: anything that respects the interface composes, provably, because that is what functors do. This is the question that would unify the three pluggable dimensions — openers, consensus, predictors — under one roof. It is also the hardest thing on the log.

**Q11 — the topos question.** Is the substrate's state space a topos? The internal logic of a topos is constructive, and constructive logic is the logic of a ship that must *act* — you cannot wait for excluded middle when the rocks are off the bow. If Q11 closes affirmatively, the substrate's reasoning acquires a proof theory for free, and the witnesses' justifications (per Q2) become *proof objects* in that internal logic. Q10 and Q11 are related; the topos is a category with extra structure, and the extra structure is exactly the structure a decision-making substrate wants.

**Q12 — the fibration question.** Do the per-agent decay rates (per Q8) fiber over the base of agents? The intuition: each agent is a base point, and above it hangs the fiber of that agent's memories, decaying on that agent's clock. A fibration would give the mathematics of *change of agent* — how context moves between fibers, how a memory handed from the chat agent to the chart agent is transformed. This is the most speculative of the five, and the one whose closure would most change the implementation.

**Q14 — the temperature question.** Should the substrate's decision-making carry a temperature — a knob between exploitation of the known and exploration of the uncertain? The maritime version: a ship in familiar waters steers the known channel; a ship in strange waters takes soundings. The question is whether temperature is a parameter bolted onto the consensus, or something the four consensus methods already imply. The geometric median is a cold method — it exploits the weighted center. A hot method would sample the tails. Whether the substrate needs a hot method is an open question, and the answer probably arrives through Q10 rather than through direct experiment.

**Q15 — the LLM-as-compiler question.** Can a large language model serve as the substrate's compiler — translating plain-language watch instructions into substrate addresses, opener selections, consensus choices, decay rates? The eight openers already bring speech and text aboard. Q15 asks the reverse direction: not the world speaking to the substrate, but the substrate being *programmed* by speech. This is the question whose closure would change who can captain the ship. It is last on the log not because it is least important but because it depends on the others: an LLM can only compile what has a semantics, and the semantics are what Q10 and Q11 would provide.

Five questions. The third math update will take up what the watch does with them.

---

### 7. The 175 tests

The count deserves its own section, because the count is the discipline.

151 tests passed at the first math update. 175 pass now. Twenty-four came aboard, and they are not filler — each one guards a specific claim made in this paper:

- **Witness justification round-trips.** Write a decision with a justification; read it back; the justification survives, structure intact. A record that cannot survive its own storage is not a record.
- **Weighted median correctness.** The 1D geometric median against brute force, on sorted and unsorted inputs, with and without weights, including the tie cases where the median sits between two reports.
- **Weiszfeld iteration.** Convergence on well-separated multi-dimensional data, behavior on the collinear cases, and the smoothed-weight fix for the estimate-lands-on-a-point case, hit deliberately.
- **Outlier resistance.** The nine-twenties-and-one-two-hundred case, and its kin. The median must not move. These tests exist so that the day someone "optimizes" the median and it starts drifting toward outliers, the suite catches it before the rocks do.
- **Per-agent decay.** Four kinds, four rates, each fading at its own speed, and the composition with the weighted median — old readings weighted down, consensus pulled toward the new.
- **Three JEPA predictors.** Linear convergence per the theorem. MLP training-descent and held-out prediction. KNN retrieval and neighborhood behavior. And the selection at the address — the same substrate, three predictors, chosen per configuration.
- **Opener coexistence.** All eight openers, mounted and speaking to the same cell, with the new consensus methods and decay rates in play. OpComp's guarantee, exercised.

A test suite is the substrate's own witness — per Q2, it records not only that the code runs but *why* the code is believed. Every test is a justification, standing watch.

---

### 8. The growing extensibility — the pattern, stated once

Count what is pluggable now:

- **8 openers.** Chart, voice, gesture, witness, MIDI, REST, MUD, PLATO. Eight ways for the world to reach the substrate.
- **3 JEPAs.** Linear, MLP, KNN. Three ways for the substrate to predict the world.
- **4 consensus methods.** Mean, geometric median, and the two witnesses. Four ways for the substrate to agree about the world.
- **4 decay rates.** Chat, sensor, chart, geological. Four speeds for the substrate to forget the world.

That is nineteen pluggable selections across four dimensions, and the number is not the point. The point is the *shape*: in every dimension, the cell holds the interface and the implementations compete behind it. Nothing in the cell knows whether the voice opener or the REST opener spoke. Nothing in the cell knows whether the MLP or the KNN predicted. Nothing in the cell knows whether the mean or the median agreed. The cell knows addresses, loops, and contracts. Everything else is behind a wall, and behind the wall is where the variety lives.

This is why the substrate grows without warping. Adding the geometric median did not touch the openers. Adding per-agent decay did not touch the JEPAs. Adding the MLP predictor did not touch the witnesses. Each addition went in through its own dimension and left the others standing. A structure that must be rewritten to be extended is a structure that will stop being extended. A structure that extends by insertion never stops.

And — the closing observation of this section — this is precisely the property that Q10, the category question, would name and prove. The pluggable dimensions are already behaving like functors. The implementations are already behaving like objects in categories of their own. The mathematics, if it closes, will not be describing something new. It will be describing something the substrate has been *doing* since the first opener mounted.

---

### 9. Close of the watch

The second math update ends here. The log reads:

Five theorems proved. Eight questions closed — Q1 through Q9, with Q2, Q5, Q8, and Q9 carried in this paper at full weight. Five questions open — Q10, Q11, Q12, Q14, Q15 — and each one named with its bearing. 175 tests passing. Eight openers, three predictors, four consensus methods, four decay clocks. One cell underneath all of it, holding the interfaces, indifferent to the variety above.

The witnesses now answer "why." The consensus now ignores the liar. The memory now forgets at four honest speeds. The predictor now learns.

The ship takes soundings, weighs them by age, throws out the fouled line, records its reasons, and learns the strait as it sails.

Five questions remain on the log. The watch changes. The third math update will tell you what became of them.

*End of paper 122. Second math update, complete.*