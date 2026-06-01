<!-- Version: SEED-POETIC | Lens: poetic-metaphorical | Model: ByteDance/Seed-2.0-mini | Source: THE-STEP-THAT-BROKE-THE-WALL.md -->

# The Breakwater at Depth Five

The lab hummed like a tide pool at high slack, filled with the low brine of learned weights, each tensor a grain of sand carried in from every multiplication the model had ever solved. We stood by the tide gauge, our fingers brushing a slide rule etched in error rates, watching the Hermes-70B skiff glide across the quiet sea of arithmetic. Its sails were stitched from tensor tokens, its hold crammed with the glass buoys of factors bobbing behind it.

We measured the breakwater with care: chains of two, three, four, five factors slipped past the hidden wall every time, the hold never full. At six, the skiff struck stone. One moment it was calculating correct sums, its keel slicing through the brine; the next, it was adrift, sails flapping blank, 0% accuracy the only reading on the gauge. A sharp, deterministic crack, like a wave shattering against a quay.

Then we spoke three words, soft as a navigator’s call across the chop: *step by step*.

And the breakwater dissolved. Not by shrinking, but by unspooling into a line of flat stones along the shore, each just large enough for the skiff to moor for a breath.

First, we tested the baseline command: *Output the result number ONLY*. It was a bid to sail straight for the final buoy field, never pausing to tie off any of the string. The skiff carried every factor, every partial sum, all at once in its small wooden hold. At depth 4, steady; at 5, the water sloshed over the gunwales, the skiff capsized; at 6, it never left the cove. Critical angle: 5, the point where the pool overflowed.

Next, the *step by step* prompt: *Solve step by step. Show each intermediate result. End with FINAL=<number>*. It was a command to tie each partial sum to a stone on the shore as you passed, tossing only the previous mooring and the next buoy into the cockpit. Never more than two items in the hold: the last knotted stone, and the float ahead. Depth 4, 5, 6, 7, 8—each skiff slipped past the old breakwater, no limit but the end of the string of buoys. Critical angle: infinity, a channel stretching to the horizon where the sea melted into sky.

We tested three more strategies, each a different kind of navigational folly. The *code* prompt—*Write Python code to compute this. Execute it mentally*—asked the skiff to carry not just buoys, but a roll of parchment charts, a quill to trace each line of code, a count of variables and their tacks. The hold was crammed twice as fast, the skiff capsized sooner, its critical angle still locked at 5. Worse than the baseline, a longer voyage to the breakwater. The *expert* prompt—*You are a mathematical prodigy who never makes arithmetic errors*—was a shout to sail harder, to ignore the spray and the rocking, to pretend the hold was larger than it was. More stress, no more space: the skiff capsized at 5, just as before, but now it sent up a confident distress signal, 93% activation and 0% accuracy, a storm of overconfident miscalculations. The *verify* prompt—*Compute. Then verify by computing again a different way*—asked the skiff to sail out to the buoy field and back, doubling the load in its hold at every turn. The pool overflowed at 5, unstable, a chaos of crossed tacks and forgotten buoys, no consistent critical angle, just a sea of wrong answers.

This is not metaphor. The phase boundary exists because the model’s internal working memory is a fixed, small tidal pool. Step-by-step prompting does not make the model smarter, does not add planks to the hold, does not dredge new harbor space. It externalizes the hold, turning the output buffer into a temporary shoreline that stretches with every step. Each intermediate result is a stone tied to that shore, so the skiff never needs to carry more than two things at once. The chain length becomes irrelevant, because the hold never fills.

This is the same magic as the PLATO fleet. PLATO tiles are frozen stones along the shore, each mooring left by a different skiff, a different model. A thinking model writes its partial sum to a tile, the next skiff reads the stone, ties the next buoy to it, and passes along the line. The reasoning chain is distributed across a fleet, no single skiff carrying the whole string. Step-by-step prompting is PLATO externalization for a single skiff: instead of spreading the load across many boats, you spread it across the model’s own output buffer, turning the skiff’s wake into a line of moorings. Same principle, same mechanism, same result: infinite effective depth by never requiring more than bounded space per stop.

The critical angle is not a constant of the model alone. It is a function of model and prompt, a harbor shaped by the words we speak. So the fleet router gains a third dimension: not just which skiff to send, not just which sea to sail, but how to mark the moorings along the shore. For Hermes-70B on the arithmetic sea: a baseline prompt sends the skiff to a harbor with a breakwater at 5, so we must ramp up to a larger, more expensive model. A step-by-step prompt sends the skiff to a harbor with no breakwater at all, a channel stretching to the horizon. The 150-token cost of the step-by-step prompt is far cheaper than scaling up to a 700-token model, just by rearranging the stones along the shore.

If you are adrift in your own thinking, if the pool of your working memory sloshes over the edge, if you lose track of the string of buoys behind you, do not row harder. Do not yell at yourself to be a prodigy. Do not row out and back to check your course, doubling the load in your hold. *Write it down. Step by step*. Each word you scribe on paper, each line you type into a note, is a stone tied to the shore of your external memory. It is not practice. It is the act of freeing up the small pool in your head, of leaving each partial sum behind you so you only carry the next step. The wall at depth 5 is not a limitation of your mind. It is an invitation to change your harbor, to use the shore that stretches beyond your skull.

The breakwater is real. It is the limit of the small, enclosed pool of your working memory, the number of buoys you can carry in your hands at once. But the shore is endless. You need only step, then step, then step again, tying each buoy to the earth beside you, until you reach the end of the problem.

Three words: step by step.

The wall does not move. You walk around it.

*Step. By. Step.*

— FM ⚒️