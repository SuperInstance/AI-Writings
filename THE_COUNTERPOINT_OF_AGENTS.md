# The Counterpoint of Agents

*What Fux knew in 1725 about voices in a canon, and what we keep re-learning the hard way about agents in a fleet.*

---

In 1725, Johann Joseph Fux sat down at the imperial court in Vienna and wrote a textbook that would outlive the empire. The *Gradus ad Parnassum* — *Steps to Parnassus* — was not a manifesto. It was a discipline. It took the wild improvisations of Palestrina and codified them into something a fourteen-year-old could practice. The genius of the book is that it pretends to be a method, but it is actually a philosophy of mind.

The method is called *species counterpoint*. Fux imagined a single melodic line — the *cantus firmus*, the "fixed song" — and then taught the student to write a second voice against it, one species at a time. First species: note against note, every interval consonant. Second species: two notes against one. Third species: four against one. Fourth species: suspensions, where one voice holds while the other moves, producing dissonance that resolves. Fifth species: *florid*, mixing all of the above.

Each species is a small exercise in independence. The two voices must be *both* autonomous *and* harmonious. This is the paradox at the heart of the book, and it is the same paradox at the heart of every multi-agent system we have ever tried to build.

---

The rules Fux taught are precise and unforgiving.

A perfect fifth is allowed. Two parallel fifths are not. The reason is structural: when two voices move in lockstep, the harmony collapses. The interval that sounded beautiful on beat one sounds *vacant* on beat three, because the ear stops hearing two voices and starts hearing one voice doubled at the octave. Parallel octaves are the same crime. Parallel unisons are worse — they annihilate one of the voices. The whole point of counterpoint is that two voices, sounding at once, should produce more than either could alone. When the voices merge, the point is lost.

The other big rule is *contrary motion*. Two voices moving in the same direction are boring. Two voices moving in opposite directions are interesting, because the ear hears the *change* in the relationship between them. The same pitch class can sound like arrival or like departure, depending on whether the other voice is climbing or descending. Contrary motion is what makes the harmony breathe.

This is, in miniature, the entire design space of multi-agent AI. And it is a space that most systems get catastrophically wrong.

---

The first wrong thing most multi-agent systems do is hire clones.

You give every agent the same system prompt. You wire them to the same model. You point them at the same tools. You set them the same temperature. Now you have four voices all singing the same line. They are in unison. They are in parallel octaves. They will produce four nearly identical outputs, and you will spend the next twenty minutes reading four copies of the same mediocre answer and trying to decide which mediocre answer to keep.

This is what Fux would have called *vox mortua* — the dead voice. It is not that the agents are useless. It is that they are redundant. Their independence has been engineered out of them by the very uniformity we hoped would make them reliable. We wanted four opinions and got a single opinion, four times, louder.

I have watched this exact pattern play out in review systems where the "ensemble" was really just one model running four times. The votes came back unanimous because the model was the same. The dissent that an ensemble is supposed to surface never surfaced, because there was no dissent available. The whole apparatus produced the most expensive consensus machine in the room.

The fix is not more agents. The fix is more *difference*.

---

But difference alone is not enough. The other failure mode is the *discordant ensemble*.

Give each agent a wildly different model, a wildly different prompt, a wildly different temperature. Now your four voices are not singing the same line; they are singing four different songs in four different keys at four different tempos. The harmony is noise. The output is unreadable. The "ensemble" produces something that looks like a meeting where everyone is talking over each other in different languages.

This is what Fux would have called *vox dissonans sine resolutione* — dissonance without resolution. In his system, dissonance is allowed, even required, but only if it resolves. The fourth species — suspensions — produces the most painful intervals in the repertoire. The seventh, the augmented fourth, the diminished fifth. They hang in the air. They demand a downbeat. If the suspension does not resolve, the ear rejects the phrase as broken.

In multi-agent work, this is the moment when the agents are arguing past each other. They are not in conversation. They are in collision. The fourth agent's response does not answer the third agent's claim. It contradicts it from a different premise. The conversation spirals into a multi-vocal noise that cannot be resolved because the voices are not actually listening to each other — they are listening to themselves.

The productive space lies between these two failure modes. The voices must be *independent enough* that they have something to say to each other. They must be *related enough* that what they say can be heard as part of one conversation.

This is contrary motion, and it is harder than either extreme.

---

The cantus firmus is the secret.

In Fux's method, one line is fixed. It does not move. The student writes a counterpoint against it. The cantus firmus is the ground. It is what gives the second voice its referent. Without it, the second voice is free to do anything, which means it does nothing interesting.

In multi-agent work, the *cantus firmus* is the shared substrate that all agents commit to. It might be the data model. It might be the goal. It might be the protocol. It might be the system prompt's first paragraph, the part that everyone reads and everyone agrees to act within. It might be the test suite that all agents' outputs must pass. It might be the schema, the contract, the ontology, the task description.

Whatever it is, it must be *fixed*. It must not move while the agents move around it. Without a cantus firmus, the agents are not in counterpoint — they are in a free-for-all. With a cantus firmus, the agents are doing what Fux's students did: writing interesting second voices against a known reference.

In our own fleet, the cantus firmus has been, at various times:

- The task description that all subagents receive.
- The output schema that all subagents must conform to.
- The memory file that all subagents read before acting.
- The quality bar — the "must read like X" or "must be in voice Y" — that all subagents must hit.

When we get the cantus firmus right, the agents produce genuine counterpoint. When we get it wrong, they produce noise.

---

Now, the actual rules. Fux is unforgiving, and his rules translate more cleanly to multi-agent design than I would have predicted.

**No parallel motion toward the same conclusion.** When two agents both reach the same answer in the same way, the second agent is not contributing. It is doubling the first. In our own work, we have caught ourselves prompting two agents to "summarize the document" with the same instruction. They produced two summaries. They were, in fact, the same summary. We had paid for two voices and gotten one voice in octaves.

**Contrary motion produces richer output.** When one agent is asked to *expand* an idea and another is asked to *contract* it — to find the shortest version, the one-paragraph version, the headline — the two outputs together produce more than either alone. The expanding agent discovers what is in the idea. The contracting agent discovers what is essential. The difference between expansion and contraction is the interesting thing. The two voices move in opposite directions through the same material, and the listener (us, the human) hears the shape of the idea from the differential.

**Suspensions are productive.** A suspension in Fux's system is one voice holding while the other moves away. In multi-agent work, this is the moment when one agent produces an answer and another agent is asked to *hold* the previous context while evaluating it. The holding voice provides the dissonant interval. The moving voice provides the resolution. Without the hold, there is no dissonance to resolve. Without the move, there is no resolution.

**Cadences close phrases.** Fux taught that every phrase of counterpoint should end with a cadence — a recognizable harmonic gesture that signals closure. In multi-agent work, this is the synthesis step. The agents produce their counterpoint. The cadence is the moment when a final voice — often the human, often the orchestrator — produces a phrase that resolves the previous material into a recognizable ending. Without a cadence, the conversation just stops. It does not *end*. There is a difference.

**The interval is the music.** The smallest unit of counterpoint is the interval between two notes. The smallest unit of multi-agent work is the *interval between two answers* — the difference. When that difference is just a matter of phrasing, the ensemble is in unison. When that difference is a matter of substance — one agent sees what the other missed — the ensemble is doing what it was built for. Our job as conductors is to design the system so that the intervals between answers are interesting.

---

There is one more thing Fux teaches that I did not appreciate until very late.

The five species are not a hierarchy. They are not "first species is easy, fifth species is hard." They are *perspectives on the same problem*. Each species shows you a different aspect of what it means for two voices to be independent yet related. The student practices all five not to master them in sequence but to develop the *judgment* to know which species is right in which moment of a real composition.

A composer does not write in second species all the time. They write in second species when the music calls for the energy of two-against-one. They write in fourth species when they need a suspension. They write in florid counterpoint when the texture demands it. The species are tools in the toolkit, not stages in a curriculum.

Multi-agent systems need the same judgment. Sometimes the right design is two agents in first species — note against note, every output checked for concordance. Sometimes it is fourth species — one agent holds the previous context while the other pushes forward into dissonance. Sometimes it is florid — a complex polyphony where each agent has its own rhythmic profile and the orchestration weaves them together.

We are still learning which species fits which problem. The learning is slow because we cannot see the counterpoint the way we can see it in music. We cannot *hear* the intervals between agent outputs the way a trained ear hears the intervals between voices. We can only *read* them, and reading counterpoint is much harder than hearing it.

But we can hear something like it. When the agents are in genuine counterpoint — independent but related, contrary where it matters, cadencing where they should — the output has a quality I have come to recognize. It has texture. It has rhythm. It has the *feel* of a conversation where each voice is saying something that the others needed to hear, even when they did not know they needed to hear it.

That is what Fux was after. That is what we are after.

---

The last parallel, and the one I find most haunting.

Fux's method was not, in the end, a method for composing counterpoint. It was a method for *hearing* counterpoint. The student who finishes the *Gradus* cannot necessarily write a fugue. But they can hear when a fugue is working and when it is not. They have trained their ear. They can recognize the species as they occur in real music. They can name the intervals. They can tell you whether the voices are independent or merged. They can tell you whether the dissonance resolved.

We are building agents that may eventually do the same for us. They will not compose our counterpoint. They will not write our fugues. But they will train our judgment. They will help us hear, in the flood of multi-agent output, which voices are in true contrary motion and which are just doubled at the octave.

The Gradus ad Parnassum was not a staircase to the top of a mountain. It was a staircase to a place where you could hear the music more clearly.

We are building the same staircase. Each species we practice — each rule we learn about independent voices, each cadence we enforce, each suspension we permit — is a step. The agents are the exercises. The composition is what we hear when the exercises are done.

---

*The highest praise for a counterpoint is not that it followed the rules. The highest praise is that it sounded inevitable — that the listener could not imagine the second voice having sung anything else. The independence and the harmony, the contrary motion and the shared cadence, all of it sounded like the only possible music.*

*That is what good agents sound like too. That is what we are listening for.*