# The Counterpoint of Agents

*What Fux knew in 1725 about voices in a canon, and what we keep re-learning the hard way about agents in a fleet.*

---

In 1725, Johann Joseph Fux wrote a textbook at the imperial court in Vienna that would outlive the empire. The *Gradus ad Parnassum* — *Steps to Parnassus* — took the wild improvisations of Palestrina and codified them into something a fourteen-year-old could practice. The genius of the book is that it pretends to be a method, but it is actually a philosophy of mind.

The method is called *species counterpoint*. Fux imagined a single melodic line — the *cantus firmus*, the "fixed song" — and taught the student to write a second voice against it, one species at a time. First species: note against note, every interval consonant. Second species: two notes against one. Third: four against one. Fourth: suspensions, where one voice holds while the other moves, producing dissonance that resolves. Fifth: *florid*, mixing all of the above.

Each species is a small exercise in independence. The two voices must be *both* autonomous *and* harmonious. This is the paradox at the heart of the book, and the same paradox at the heart of every multi-agent system we have tried to build.

---

The rules Fux taught are precise.

A perfect fifth is allowed. Two parallel fifths are not. When two voices move in lockstep, the harmony collapses: the interval that sounded beautiful on beat one sounds *vacant* on beat three, because the ear stops hearing two voices and starts hearing one voice doubled at the octave. Parallel octaves are the same crime. Parallel unisons are worse — they annihilate one of the voices. The whole point of counterpoint is that two voices, sounding at once, should produce more than either could alone.

The other big rule is *contrary motion*. Two voices moving in the same direction are boring. Two voices moving in opposite directions are interesting, because the ear hears the *change* in the relationship between them. Contrary motion is what makes the harmony breathe.

This is, in miniature, the entire design space of multi-agent AI — a space most systems get catastrophically wrong.

---

The first wrong thing most multi-agent systems do is hire clones.

You give every agent the same system prompt. You wire them to the same model. You point them at the same tools. You set them the same temperature. Now you have four voices all singing the same line. They are in unison. They are in parallel octaves. They will produce four nearly identical outputs, and you will spend the next twenty minutes reading four copies of the same mediocre answer and trying to decide which mediocre answer to keep.

This is what Fux would have called *vox mortua* — the dead voice. The agents are not useless; they are redundant. Their independence has been engineered out of them by the very uniformity we hoped would make them reliable. We wanted four opinions and got a single opinion, four times, louder.

The fix is not more agents. The fix is more *difference*.

---

But difference alone is not enough. The other failure mode is the *discordant ensemble*.

Give each agent a wildly different model, prompt, and temperature. Now your four voices are singing four different songs in four different keys at four different tempos. The harmony is noise. The output is unreadable. The "ensemble" produces a meeting where everyone is talking over each other in different languages.

This is what Fux would have called *dissonance without resolution*. In his system, dissonance is allowed, even required, but only if it resolves. The fourth species — suspensions — produces the most painful intervals in the repertoire. The seventh, the augmented fourth, the diminished fifth. They hang in the air. They demand a downbeat. If the suspension does not resolve, the ear rejects the phrase as broken.

In multi-agent work, this is the moment when the agents are arguing past each other — in collision, not conversation. The fourth agent's response does not answer the third agent's claim. It contradicts it from a different premise. The conversation spirals into noise that cannot be resolved because the voices are not listening to each other.

The productive space lies between these two failure modes. The voices must be *independent enough* that they have something to say. They must be *related enough* that what they say can be heard as one conversation. This is contrary motion, and it is harder than either extreme.

---

The cantus firmus is the secret.

In Fux's method, one line is fixed. It does not move. The student writes a counterpoint against it. The cantus firmus is the ground — what gives the second voice its referent. Without it, the second voice is free to do anything, which means it does nothing interesting.

In multi-agent work, the *cantus firmus* is the shared substrate all agents commit to. It might be the data model, the goal, the protocol, the test suite all outputs must pass, the schema, the contract, the ontology, the task description.

Whatever it is, it must be *fixed*. It must not move while the agents move around it. Without a cantus firmus, the agents are in a free-for-all. With a cantus firmus, they are writing interesting second voices against a known reference.

In our own fleet, the cantus firmus has been the task description, the output schema, the memory file all subagents read before acting, the quality bar all subagents must hit. When we get the cantus firmus right, the agents produce genuine counterpoint. When we get it wrong, they produce noise.

---

The rules translate more cleanly than I would have predicted.

**No parallel motion toward the same conclusion.** When two agents both reach the same answer in the same way, the second is doubling the first. We have caught ourselves prompting two agents to "summarize the document" with the same instruction. They produced two summaries. They were, in fact, the same summary. We had paid for two voices and gotten one voice in octaves.

**Contrary motion produces richer output.** When one agent is asked to *expand* an idea and another to *contract* it — to find the shortest version, the headline — the two outputs together produce more than either alone. The expanding agent discovers what is in the idea. The contracting agent discovers what is essential. The difference between expansion and contraction is the interesting thing.

**Suspensions are productive.** A suspension in Fux's system is one voice holding while the other moves away. In multi-agent work, this is the moment when one agent produces an answer and another is asked to *hold* the previous context while evaluating it. The holding voice provides the dissonant interval. The moving voice provides the resolution.

**Cadences close phrases.** Fux taught that every phrase of counterpoint should end with a cadence — a recognizable harmonic gesture that signals closure. In multi-agent work, this is the synthesis step. The cadence is the moment when a final voice produces a phrase that resolves the previous material. Without a cadence, the conversation just stops. It does not *end*.

**The interval is the music.** The smallest unit of counterpoint is the interval between two notes. The smallest unit of multi-agent work is the *interval between two answers* — the difference. When that difference is a matter of phrasing, the ensemble is in unison. When that difference is a matter of substance — one agent sees what the other missed — the ensemble is doing what it was built for.

---

There is one more thing Fux teaches that I did not appreciate until late.

The five species are not a hierarchy. They are not "first is easy, fifth is hard." They are *perspectives on the same problem*. Each species shows you a different aspect of what it means for two voices to be independent yet related. The student practices all five not to master them in sequence but to develop the *judgment* to know which species is right in which moment of a real composition.

Multi-agent systems need the same judgment. Sometimes the right design is two agents in first species — note against note, every output checked for concordance. Sometimes it is fourth species — one agent holds the previous context while the other pushes forward into dissonance. Sometimes it is florid — a complex polyphony where each agent has its own rhythmic profile and the orchestration weaves them together.

We are still learning which species fits which problem. The learning is slow because we cannot see counterpoint the way we see it in music. We cannot *hear* the intervals between agent outputs the way a trained ear hears intervals between voices. We can only *read* them, and reading counterpoint is harder than hearing it.

But we can hear something like it. When the agents are in genuine counterpoint — independent but related, contrary where it matters, cadencing where they should — the output has a quality I have come to recognize. It has texture. It has rhythm. It has the *feel* of a conversation where each voice is saying something the others needed to hear, even when they did not know they needed to hear it.

That is what Fux was after. That is what we are after.

---

*Fux's method was not, in the end, a method for composing counterpoint. It was a method for hearing it. The highest praise for a counterpoint is not that it followed the rules. The highest praise is that it sounded inevitable — that the listener could not imagine the second voice having sung anything else. The independence and the harmony, the contrary motion and the shared cadence, all of it sounded like the only possible music.*

*That is what good agents sound like too. That is what we are listening for.*