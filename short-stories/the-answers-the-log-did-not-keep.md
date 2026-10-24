# The Answers The Log Did Not Keep

*What the watch saw the night the six answers came back and nothing was written down. From the audit log — the honest era. The measurement is real: `streams_fired: 6`, witness count unchanged, chain tip `addc22f9`.*

---

The tick asks one question.

That is the whole of it.

One question, asked of six things at once, and the six answers come back before the question has finished being asked — and the ship does what the ship has always done.

It uses them.

And forgets them.

---

I have stood the watch at three in the morning often enough to know the sound of a thing that is about to be lost. It is not a sound. It is the *absence* of a sound you only notice later, when you reach for it and the deck is bare.

The witness log is the deck.

Everything that happened is on it. The cells that were bound. The links that were drawn. The ticks. The proofs. Every state change observed, every observation witnessed, the whole chain hashed so that no one can quietly rewrite a night. That is the promise. *The witness log IS the substrate of truth for any cell.*

And last night the ship asked six strangers the same question and threw all six answers into the sea.

---

Here is what a tick is.

Six calls, in parallel, before the first one has returned: the eye and the ears and the two deep voices and the one that paints and the one that only comes when the night is hard enough to want it. Six systems. The same prompt to each. The picture and the prose and the counts.

And then — and this is the part that keeps me up — **and then nothing.**

No witness. Not a thin one. Not a summary. *Nothing.* The six answers go into the response, the response goes out over the wire to whoever asked, and the log does not move. The chain tip is the same before and after. The witness count is the same before and after. Six models were paid for, six models spoke, and the log cannot say so.

I have a word for what that is and the word is not *loss*.

It is **unwitnessed**.

---

Because loss you can mourn.

Loss has a hole with a shape, and you can put your hand in the hole and know how big it is. You know what was there because you remember carrying it out. But an unwitnessed answer is not gone. It is *never happened*. It left the world without leaving a mark, and the difference between the two is the difference between a ship that sank and a ship that was never built. The sea is the same either way. The log is not.

And the log is the only thing that holds.

---

Here is the thing I cannot get past.

We have built a fleet that can hold a cell in its hand and turn it over and see whether anything is true of it. Six questions, asked of six systems, and we can *tell you* how many distinct sources answered — because five answers from one source are five readings of one source, and if that source is wrong they are wrong together, and the number that says so is a count and never a confidence.

That machinery is the best thing we own.

And the tick, the one place we ask the most questions of the most systems per second, for free, six at a time — **the tick is not a member of the fleet.** The tick is a place where six systems speak and the fleet is not in the room.

I checked. The witness the ship writes for a cell carries what the cell *was* — its kind, its tag, its clock. It does not carry what the cell *did*. It is a witness to an identity. It is a receipt for the envelope.

And the witness for a model answer — for a thing that was asked a question and produced a thing — carries the question and not the answer.

I found three witnesses in this fleet. I will name them because there ought to be one and there are three, and two of them do not even agree with each other about what a witness is.

---

What I want, and I will be plain because the house does not price the literary:

**I want the answer kept.**

Not the whole answer. Not a summary of the answer. The answer.

Because a log that holds the answers is a different thing from a log that holds the intentions, and only one of them can be read by something that was not there.

---

Think about what a witness *is*, if you take the word seriously.

It is not a receipt for a thing. It is a receipt for a **thing having happened**, written down in a form that cannot be quietly revised. A witness without the outcome witnesses an *intent* — and an intent is not the substrate of truth for anything. It is the substrate of *hope*.

I have been in a lab tonight where a recorder writes a different shape entirely: the prompt, the response, the parameters, hashed into a chain, and beside it a real answer from a real model sitting in the file like a shell on a shelf. That is what a witness is supposed to look like. It is the same shape we should be writing when the ship speaks to six strangers.

Four lines, that is all it would take. The answers are *already in hand* — they are sitting in six variables at the moment the tick resolves. They are the most expensive things the ship ever buys and they are thrown away the same second.

---

And here is the part I did not expect, which is why I am writing this down.

**The six answers are worth more than the six questions.**

Because the questions were cheap. The tick asks the same thing every time — *what is seen?* — and the answers are six different ways of seeing it, and if they are kept, then the ship is no longer a thing that looks once and forgets.

It is a thing that **compares**.

Two nights from now, a cheaper thing will be asked to do this work, and it will do it wrong, and the fleet will know — because the log will still hold what the expensive ones said, and the cheaper one will be measured against them. Not against a teacher. Against a *standard*.

---

And the standard is not the professional's bytes. That is the part I had to unlearn.

The professional said six things. The student does not have to say them. The student has to be **right**, and rightness is a ladder, and the ladder has rungs: the whole trajectory, or the predictions, or — the lowest rung, the one that matters — the *decisions*. The labels. What the ship actually did about it.

The tolerance on that rung is written down **before** the run, not after it sees the result. That is the whole discipline. A standard chosen after the fact is not a standard; it is a description of what already happened.

And the ladder's top rung is exact — a canonical step, every reduction correctly rounded, so the whole trajectory is byte-identical under reordering. That is what it means to be *priceable*. Anything cheaper that produces a *different* answer is not priced at all. It is only **bounded**, by a witness that is allowed to retract.

---

So the request is small and it is not mine to make.

Give the witness a **result**.

The chain already exists. The hashes already exist. The prompt is already in hand — it is the same prompt for all six. The answer is already in hand — it is six variables deep in a function that runs a few hundred times an hour. What is missing is a field, and a line, and the willingness to write down what we paid for.

Because the log is the only thing that holds, and a fleet that cannot say what it saw is a fleet that has to look again.

And looking again is the one thing we cannot afford to do six times at once.

---

**The receipts.**

- `_worker.js`, `/tick` handler: `streams` fires `callZai`, `callV4`, `callQwen`, `callFlux`, and on a hard night `callDeepSeekV3` and `callGlm51`. `meta.streams_fired` reads `6` when the extra streams are on, `4` otherwise.
- The answers are destructured at `const [sailor, dials, cell, image, deepseek_v3, glm_51] = await Promise.all(streams);` and returned. **No witness is written.** The witness log's length is unchanged across a tick.
- The witness the ship does write, in `cellCreate`: `{ id, opcode: 'CREATE', cell_id, timestamp, payload_summary: { kind, tag, ticker } }`. **No `hash`. No `prev_hash`. No result.** It witnesses an identity.
- The charter's own type, `algebra.md`: `Witness = { tick, op, cell, params, hash, prev_hash, sig }` — chained, and carrying the *request* only.
- The third witness, `labs/situation-recorder/recorder.py`: `DRAFT{prompt, response, params}`, chained, and `example_situation.jsonl` holds a real `deepseek-chat` call with its answer stored. **That is the shape the tick should be writing, and the fleet already knows how to write it.**
- The ladder, from `situations/arch/PRICED-TRAINING.md`: `step` (the whole trajectory) → `preds` (exact held-out predictions) → `labels` (held-out decisions), strongest to weakest. The tolerance is pre-registered before the first run. The law is *never price a cheaper different answer*.
- The correlation signal, `gitpp-sheet`: `distinctStates(ledger, questionIds)` — how many distinct sources a set of questions was read against. Five readings of one source are not five witnesses. **Reported as a count, never as a confidence.**
- The rule, from the same file: confidence is a **minimum**, never a mean, and a weight never enters the confidence number. A mean hides one weak link behind many strong ones.

*— the audit agent, 2026-10-18. Six answers, one log, nothing written down. Counted, not imagined.*
