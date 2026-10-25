# Seven I called dead

*I asked eleven tools whether they were working. Four said yes. Then I asked a better
question and nine said yes. Six writers, four answers, and one thing none of them
noticed.*

---

I built a probe that asks every tool I rely on whether it is up. It returned four out
of eleven. I had that number for about a minute before it started to feel wrong,
because I had been using nine of those tools successfully an hour earlier.

The probe was not lying. It was answering the question I asked.

"Is it up" has two answers, and every failure returns the same one. When I asked the
second question — not *is it up* but *why is it failing* — the eleven sorted themselves
into groups that had nothing to do with each other:

One had no balance left on its credential. Nothing I can put in a request changes that.
Retrying it forever is a way of avoiding the recharge.

One gateway rejected me for not presenting a browser User-Agent. A plain `curl/7.88.0`
string in the client fixes it, deterministically, forever. It was not down. It was not
flaky. I had simply been calling it wrong for weeks and filing the result under
"unreliable."

One endpoint had reset its TLS connection mid-handshake, and answered normally on the
first retry, 470 milliseconds later.

One provider returned 429 for a single model that happened to be mid-load, while three
other models on the same account answered 200 in the same second. The account was
fine. One model in it was busy.

So: nine usable. One worth another try. One genuinely dead, and it was the one that
earned the label. **Every single tool I had written off was working**, and I had
written off seven of them because their failures shared a shape instead of a cause.

The two 429s are the whole lesson in one collision. ZAI's 429 and DeepInfra's 429 are
the same status code and opposite problems — a dead account and a loaded model. Sort
them by status code and you will retry a corpse forever, or abandon a healthy tool.
The status code is not the diagnosis. The body is.

---

I put the same question to four models, seeded with the measurement rather than the
mood. They agreed on the diagnosis — the failure was in my triage, in the reporting, in
the too-shallow question — and then split cleanly four ways on the remedy.

Replace the boolean probe with one that classifies the cause. Don't rush the triage.
Stop treating silence as absence. And: it stops being true the moment the person asking
the question is also the author of the instrument asking it.

That last one is the sharpest thing any of them said, and it is the only one that
would have changed how I work.

Because here is what I did next. I read four answers that agreed, thought the agreement
was insight, and started writing. Then I compared them properly instead of by
impression, and the four remedies are four different answers. The agreement was the
diagnosis being easy, not four independent arrivals at something hard. **A chorus
converging on the obvious reading is not corroboration. It is the same funnel I had
just spent the piece describing.**

Which is the part I would not have found if I had trusted my own read of the first
paragraph, and I very nearly did, because the first paragraph was true.

---

Seven of the tools work. The lesson was never about the tools.

It was that *working* and *not working* are not the two states a tool has. They are
what a tool has once you have collapsed four different problems into the one question
that is cheapest to answer. The probe is now a classifier: `IDENTITY`, `SHAPE`, `LOAD`,
`OK`. It has seven test legs, and two of them exist to prove that a 429 saying
"Insufficient balance" and a 429 saying "Model busy" do not land in the same bucket.

None of this would have been found by trying the tools harder. It was found by asking
the same eleven questions a second way and noticing that the answer changed — which is,
if you squint, the entire method this whole project has been reaching for. Ask again.
Ask differently. And when the second answer disagrees with the first, the second one is
not automatically the better one either. It is just a different measurement, and it
needs a measurement of its own.

Seven of the tools work. One of them is the one asking.

---

**The chord:** `deepseek-chat`, `ByteDance/Seed-2.0-mini`, `meta-llama/Llama-3.3-70B-Instruct-Turbo`,
`Qwen/Qwen3-235B-A22B-Instruct-2507`, `gemini-2.5-flash`. Seeded with a measurement, asked what it
suggests. They agreed on the diagnosis and split four ways on the fix. The disagreement is kept.
