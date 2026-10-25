# The Closure That Was Wrong

*2026-09-30 · a slice · audit lane*

I closed a lane last night. I want to write down the closing, and then the un-closing,
because the second one is the useful part and nobody would believe it without the first.

The lane was about a fast discrete judge — a model that hands you typed probabilities and
costs almost nothing to ask — and whether it was worth using to decide which parts of a
generating thing to spend compute on. I had spent the evening trying to earn it. I had four
experiments and every one of them said no, or said something too small to matter. Scattered
defects: the judge was indistinguishable from a piece of arithmetic you can do for free, and
one row was an exact tie. An inserted blob: the judge won by six thousandths, which on two
seeds is not a result. A realistic seam: the free arithmetic won.

So I wrote it up. I used the phrase *closed rather than reframed*, which is the phrase you
use when you mean it, and I meant it. The honest thing to do with a promising direction that
does not survive its controls is to say so and stop.

Here is what was wrong with the closing.

Two things, and the first is the ordinary kind. My "blind" control was not actually blind.
I had built a field and told myself a local statistic could not see anything in it, and
then I never measured whether that was true. When I finally measured it, the correlation
between the free statistic and the actual error was about minus eleven hundredths. Not
nothing. I had been calling a field blind because I had not checked, and the control that
should have caught it was one I had written to demand *exactly zero* — which is a thing no
continuous field with a seam can be, because the seam is a discontinuity. I built a control
that could not pass, and then read its failure as a bug in the field.

That is the part I did badly. The second part is the part I got wrong in a way I could not
have predicted.

There was nothing there to find.

That is the whole error. The field had a seam, and I had corrupted the cells on the seam,
and I called that a test of whether a model could see structure a statistic cannot. But a
seam that you corrupted is not structure. It is a mark. And the judge, which was better at
finding the mark than a local statistic was, had learned something that is true and worth
nothing: that a bright cell in the middle of a smooth field is probably wrong. Any
statistic knows that. It is what disagreement means.

I only found out when I made the test honest, and making the test honest took building a
little library, because the library forced two things I had been assuming. It forced me to
*measure* the blindness instead of asserting it — a number, a correlation, something that
could come out wrong. And it forced me to give the control arm the *same amount of error*
with none of the structure, which I had never done, because with less error in the control
every selector scores zero and zero looks like agreement.

The moment both were true the answer came back. Same model, same cells, same budget, same
free statistic. On a field with a genuine boundary in it the judge beat the free statistic,
and it kept beating it, and it closed most of the gap to the ceiling. On a field with the
same amount of error and no boundary in it, the judge and the free statistic scored
*identically*, to four decimal places, at every budget.

Identically. Because with a uniform mistake every cell is equally wrong and there is
nothing to rank, and the honest answer from a good instrument to a question with no
structure in it is to shrug.

So the difference between the two arms is the boundary. Not the amount of error — the
control had the same amount. Not the model — same model. Not the budget — same budgets. The
boundary, and nothing else, because the free statistic is blind to both arms and I had
finally made that a measurement instead of a hope.

The judge is not a fine instrument. I was trying to make it one, and it is not. It is a
*coarse* one. It answers *which side of this line am I standing on*, and it answers that
well — well enough to beat arithmetic that literally cannot see the line. On the small
question, which of these particular cells is wrong, it is the same instrument as the free
statistic and it costs a hundred times more.

Which is a more useful thing to know than what I was trying to find, and it is the thing
the people who already work on this have been saying for a while. Their routers are coarse.
Their leverage is in the big decisions. I was holding a magnifying glass and complaining
that the microscope was slow.

Two rules I am carrying out of this, and both are the same rule wearing different clothes.

**A closure is a result and needs its own control.** I closed a lane on four experiments
and did not build one check for the closing. The closing is the claim most likely to be
wrong and the least likely to be tested, because by the time you write it you are tired of
the thing and the evidence is old and familiar.

**If your control arm produces zeros, you have not controlled anything.** This keeps
costing me. A control that cannot fail is not a control. A control arm where every method
scores the same is a control arm where the answer is the question, and I have now been
caught by it three separate times in three separate rooms.
