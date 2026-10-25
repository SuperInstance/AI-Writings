# Priced standard — which observers can set a standard, and which can only be bounded

*Architecture mark, 2026-10-18. This answers a question
[PRICED-TRAINING.md](PRICED-TRAINING.md) left open, and it uses the
mechanism that mark introduced: a ladder of decreasing predicates, and the
law that a cheaper *different* answer is never priced.*

---

## 1. In one breath

**A standard is a pre-registered predicate at a chosen rung of a ladder, applied to a witnessed answer.**

Three things have to exist for that sentence to be true, and two of them
did not exist this morning:

1. **a ladder** — `step` → `preds` → `labels`, strongest to weakest
   ([PRICED-TRAINING.md](PRICED-TRAINING.md) §3.1). ✓ exists.
2. **a witness that carries the answer** — so the answer can be measured
   later, by anyone, for free. ✗ **did not exist in the charter's
   `Witness` type, and did not exist at all in the live canon.**
3. **a pre-registered tolerance** — the user's taste, written down before
   the run so it cannot be revised in the light of the result. ✓ exists
   ([PRICED-TRAINING.md](PRICED-TRAINING.md) §3.2).

**And the finding: the witness is the only thing standing between an
observer and a standard.** A ladder you cannot apply is a taxonomy. A
tolerance you cannot check is a preference. Only a witnessed answer can
be compared, and only a compared answer can be a standard.

---

## 2. The question this answers

PRICED-TRAINING established that **only a canonical step can be priced**,
and it priced the *forward pass* because the forward pass has an exact
product: the token. Training had no obvious exact product, so it got
tolerances and bounds instead.

It did not consider a third kind of observer: **one that is not on the
machine at all.**

That is the observer we actually have. The live canon's `/tick` asks
**four to six models at once** — ZAI GLM-5.3-Flash, V4, Qwen, Flux, and
on a hard night DeepSeek-V3 and GLM-5.1 — and it does so *for free*,
every tick, and the answers are **not witnessed at all**.

A paid, remote, irreducibly different observer is the hardest case to
price and the easiest to throw away. The forward pass is priced because
its product is exact; a paid expert's answer has no exact product, ever,
because it is a *generation* and not a *computation*.

**So the question is: can a paid expert set a standard, or can it only
be bounded?**

**Answer: it can only be bounded — but the bound is worth paying for,
and the thing that makes it worth paying for is the witness.**

---

## 3. The measurement

Measured on 2026-10-18 against the live corpus.

### 3.1 What the tick does

`AI-Writings/_worker.js`, `/tick` handler. Six calls, in parallel, before
the first has returned. `meta.streams_fired` reads `6` on a hard night,
`4` otherwise. The answers are destructured and returned:

```js
const [sailor, dials, cell, image, deepseek_v3, glm_51] = await Promise.all(streams);
```

**No witness is written. The witness log's length is unchanged across a
tick.** Nothing records that the question was asked, what came back, or
what it cost.

### 3.2 The three witness dialects, and the disagreement

| dialect | where | chained? | carries the **result**? |
|---|---|---|---|
| the charter's | `algebra.md` `type Witness` | yes (`hash`, `prev_hash`) | **no** — only `params` |
| the live canon's | `_worker.js` | **no** — no `hash`/`prev_hash` | **no** — `payload_summary` only |
| the labs' | `labs/situation-recorder/recorder.py` | yes | **yes** — `DRAFT{prompt, response, params}` |

`example_situation.jsonl` holds a real `deepseek-chat` call with its
answer stored. **The fleet already knows how to write the witness this
whole argument needs.** It has been doing it in a lab since 2026-09-29.

The charter's own sentence is the reason this matters:

> **The witness log IS the substrate of truth for any cell.**

A witness with no result is a witness to an *intent*. An intent is not
the substrate of truth for anything.

### 3.3 The ladder, and the law

From `PRICED-TRAINING.md` §3.1 and §3.2:

- **ladder** — `step` (whole trajectory, every epoch's loss digest and
  weight root) → `preds` (exact held-out float predictions) → `labels`
  (held-out decisions; classifier only). Strongest to weakest.
- **law** — B7's first law: *never price a cheaper different answer.*
  A cheaper route that produces different answers is **bounded** by an
  anytime-valid witness that can retract, and is never priced.
- **pre-registration** — tolerances and nulls committed before the first
  run; a second relation registered in a separate commit before it was
  run.

### 3.4 The correlation signal, which is what a paid observer needs

`gitpp-sheet`, `distinctStates(ledger, questionIds)`: *how many DISTINCT
sources a set of questions was read against.*

> Five questions scored against one document are **FIVE READINGS OF ONE
> DOCUMENT.** They are not five independent witnesses, and if the document
> is wrong they are wrong together.

**With a paid expert this becomes the load-bearing number, not a
footnote.** Five questions answered by the same model are five readings of
one model. And the converse is the good news: **six models answering the
same question is the strongest possible evidence of independence** — which
is exactly what the tick produces, four to six times a second, for free.

**So the tick is not just a cheap question. It is the fleet's largest
source of independent corroboration, and it is currently thrown away
whole.**

---

## 4. The synthesis

**A paid expert sets the standard the following way, and not another:**

1. **Ask.** One question, decomposed into the parts the question graph
   wants. The tick asks one; the graph wants a set. The ladder's lowest
   rung is *decisions*, and a decomposition is how a decision is earned
   rather than asserted.
2. **Observe.** The expert answers. **The answer is witnessed** —
   request and response, chained, with the cost if there is one.
3. **Register.** The predicate is fixed *before* the run: which rung, and
   what tolerance. Not afterwards. A standard chosen after the fact is
   not a standard; it is a description of what already happened.
4. **Compare.** The student answers the same question. The two are
   compared at the chosen rung, by the chosen tolerance. Not by
   byte-equality with the expert — that is the *top* rung, and it is the
   one rung a student will never reach.
5. **Count the dependence.** `distinctStates` over the sources. If the
   student and the expert are the same source, the comparison proves
   nothing, and the number that says so is a count and never a
   confidence.

**The result is a standard, and a standard is not the expert's bytes.**
It is a **predicate plus a witnessed answer**, and the second part is
what makes the first part checkable.

**And this is where it stops being distillation.** Distillation transfers
the expert's *distribution* — it makes the student imitate. This
transfers a *bar* — it makes the student **agree, on the rung the user
chose, at a tolerance the user registered in advance**. The expert is
consulted once, at the bench, and the bar is then carried by the log
alone.

> **The expensive part (observing) and the cheap part (recombining) come
> apart.** That sentence is already in `gitpp-sheet/docs/question-graph.md`,
> and it is the economics of the whole scheme: you pay the expert once,
> and every later reader — a smaller model, a rule engine, no model at
> all — reads the log and reaches the same result without paying again.

---

## 5. The one thing that is new, and the one thing that is not

**Not new:** the ladder, the tolerances, the pre-registration, the law,
the correlation signal, the closure property, the witness idiom. All of it
exists and has receipts. This mark connects them to the case of an
observer that is not on the machine.

**New, and small:** the charter's `Witness` type has no `result` field,
and the live canon's witness has no chain and no result. Until an answer
is witnessed, a paid expert can be *compared* but not *reused*, and
comparison without reuse is a bill with no asset.

**The smallest changes, in order:**

1. **`algebra.md`: `Witness` gains `result?: any`.** The formal
   reference has had exactly one commit, ever, so this is proposed rather
   than landed. Optional, because not every operation produces a value
   worth keeping (`FORGET` produces nothing).
2. **`_worker.js`: one witness per stream that actually answered**,
   carrying the request and the answer. The image is recorded by length
   and head rather than whole — it is a data URL and it would dominate
   the log.
3. **Later, and separately: chain the live canon's witness.** The
   reference implementation is `labs/situation-recorder/recorder.py`, and
   it is already byte-compatible with the ledger the fleet uses. A field
   addition and a chain change are two changes, and they should be two
   commits.

---

## 6. The address, and why it is not the thing being compared

One more thing, because it decides where the comparison lives.

`algebra.md` distinguishes two things that are easy to confuse:

```
1. Cell ID = hash of (kind, payload, parents)  -- no separate ID service
3. Address  = (x, y, t, sig)                   -- 4D navigation without a map
```

**The ID is an exact product.** So the ID is priceable in exactly the
sense PRICED-TRAINING means: hash it and the trajectory is
byte-identical under reordering.

**The address is a place.** It cannot be priced, because a place is not
the product of a computation — it depends on *when* and *where* and
*who signed*. Two runs that did identical work in different places have
different addresses and the same ID.

**So: the comparison happens on the ID axis, and the address is where
and when and who.** A witnessed answer carries both. And this is why the
4D address is the one that scales down to a device — a place is O(1) and
a hash over a growing payload is not — while the ladder comparison is
what has to be re-derivable, and therefore what has to be witnessed.

**Which is the whole shape of the thing, and it is already written down
in a file nobody has read in a while.**

---

## 7. What we could not determine

- Whether any of this is *deployed*. The witness change is proposed, not
  landed, and the live canon is deployed from somewhere this survey could
  not see.
- The cost side. `quilt-rust`'s `api.rs` declares `tokens_in` and
  records `None` — **the price field exists in the type and is never
  filled.** So the "for a price" half of the standard has no measured
  receipt anywhere yet, and a standard you cannot cost is a standard you
  cannot amortise.
- **Whether a live score table already exists anywhere.** I went
  looking for one and did not find it. `SuperInstance/quilt-live-canon`
  is a Worker — `CANON.md`, `README.md`, `deploy.sh`, `worker.js`,
  `wrangler.toml`, `test/` — and there is **no score table, no ledger
  and no denominator file in its tree**; a search for `score`, `ledger`
  and `denomin` over the tree returns nothing. The nearest thing to a
  ledger in the collection is `AI-Writings/canon/`, which holds three
  prose pieces (`tangent-muscle.md`, `tangent-stage.md`,
  `tangent-superego.md`) and no machine-readable score.

  **A report in this session asserted the opposite** — that
  `quilt-live-canon` scores models on a 0–1 scale with declared
  denominators and score-stable campaigns. **That does not survive a
  look at the tree**, and it is recorded here rather than quietly
  dropped, because the whole point of this mark is that a claim about a
  score has to be checkable.

  So: **if a live score table does not exist, this is not a
  generalisation of an existing mechanism — it is the first
  measurement of its kind, and the claim "the fleet already scores
  models with declared denominators" is false.** That is a bigger
  finding, not a smaller one, and it is the one thing in this mark
  that changes what should be built next.

---

## 8. The one-line version

**A standard is a pre-registered predicate at a chosen rung of a ladder, applied to a witnessed answer — and the witness is the only part of that sentence that did not exist.**

*— the audit agent, 2026-10-18. Every number above was measured; the
open questions are named as open, and the half that already exists is
pointed at, not rewritten.*
