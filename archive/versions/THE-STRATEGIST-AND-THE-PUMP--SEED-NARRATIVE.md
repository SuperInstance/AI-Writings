<!-- Version: SEED-NARRATIVE | Lens: emotional-narrative | Model: ByteDance/Seed-2.0-mini | Source: THE-STRATEGIST-AND-THE-PUMP.md -->

# The Tile Room and the Model That Couldn’t Count Straight

It was 2:17 a.m. in the lab, and my coffee had gone cold enough to scab over the top. My lab coat was dusted with chalk from scribbling Fresnel equations on the blackboard until my wrist ached, and the server rack in the corner hummed a low, steady drone that had been lulling me in and out of frustration for three hours. I’d been chasing a ghost: a sharp generalization cliff in my tiny optical neural network models that appeared out of nowhere at depth 6, no paper or preprint had predicted it, and my workhorse model, seed-mini, was just spitting out loss numbers like a broken vending machine—give it a depth, give it a trial count, spit out a percentage of correct classifications, no answers why.

I’d deleted half my runs an hour earlier, ready to pack it in and go home to my apartment with the leaky faucet, when I remembered the undergrads in the next lab raving about Haiku. I’d written it off immediately, of course—their shared leaderboard said it scored 85% on arithmetic benchmarks, couldn’t even nail basic Eisenstein integer norms when I’d asked them to test it for a number theory side project the week before. But I was desperate, so I pulled up the API tab, typed in the only question that felt worth asking: “I’m stuck on a bug in my optical ML models. I changed the batch size halfway through training, but I don’t see why that’s breaking the generalization cliff. What’s the connection between layer depth and how much the model can actually learn, not just memorize?”

Ten seconds later, the response popped up. I didn’t even read the whole thing at first—just scanned the first line, then stopped breathing.

“Both your layer depth and your training saturation hit a sharp phase transition when they cross a dimensionless critical ratio. Think of it like a light ray hitting a glass prism: if the angle is too shallow, it bounces back inside; if it’s steep enough, it escapes. For your model, the ‘angle’ is how much training data you’ve pushed through each layer relative to its capacity. When you cranked the batch size for depth 6 without adding more training steps, you pushed that ratio past the threshold overnight. It’s not the depth that’s breaking it—it’s the ratio of what you’re teaching the model to how much it can hold.”

I knocked over my half-empty coffee mug in my shock. The dark liquid spread across my notebook, blurring the scribbled batch size notes I’d made that afternoon, but I didn’t care. I’d spent three weeks tearing my hair out over that batch size change, and here was a model that couldn’t even calculate 15*9 right (I’d tested it earlier that week, it gave 134) pointing out the exact bug I’d been puzzling over like a detective missing the obvious clue taped to their forehead.

I fumbled for my phone to pull up the Eisenstein norm test, just to confirm Haiku was still useless for math. I typed in “Calculate the norm of 3 + 2i in Eisenstein integers” and got back 12, which was wrong. The actual norm is a² - ab + b², so 9 -6 +4 =7. I laughed, then closed the arithmetic tab for good. Haiku wasn’t a calculator. It was something else.

That’s when I started building the tile room. We’d been frustrated for months with Claude Code’s clunky agent loops, where one model tried to do everything—write code, run computations, debug—before crashing or missing the forest for the trees. Instead, we built a shared digital whiteboard where every input and output was a simple text tile: no fancy wrappers, no subprocess calls, just clear, scannable lines that any model could read or write. Haiku would write a strategy tile, seed-mini would read it, run the computations, write a result tile, and so on. Neither model needed to know the other existed; they just communicated through the stream of tiles in the room.

We ran the comparison a week later, over takeout dumplings and lukewarm soda, when we’d compiled all our test results. I typed up a spreadsheet side by side, lining up the eight non-arithmetic tasks we’d designed:
| Task                  | seed-mini | haiku-4.5 |
|-----------------------|-----------|-----------|
| Error Diagnosis       | ✗         | ✗         |
| Experiment Design     | ✓         | ✓         |
| Architecture Decision | ✓         | ✓         |
| Metaphor Generation   | ✗         | ✓         |
| Bug Prediction        | ✗         | ✓         |
| Fleet Coordination    | ✗         | ✗         |
| Novel Connection      | ✗         | ✓         |
| Prioritization        | ✗         | ✓         |

Seed-mini had scored 2/8. Haiku had scored 6/8. The only overlap was the two structured reasoning tasks seed-mini was built for: planning concrete experiments and picking routing architectures. Every other task—seeing cross-domain connections, predicting hidden bugs, prioritizing which trial to run next—was Haiku’s alone.

I still remember sitting there, staring at the spreadsheet, when it hit me: we didn’t need one model that did everything. We needed two models that covered non-overlapping patches of the work, then danced together.

The dance looked like this, every time we ran a new trial:
1. **Haiku planned.** It would type a tile into the room: “Run 10 trials at depth 5 with fixed batch size and 100 training steps, then 10 trials at depth 6 to confirm the cliff.”
2. **Seed-mini executed.** It read the tile, crunched the numbers, and typed back: “Depth 5: 98% correct classification across 10 trials. Depth 6: 12% correct.”
3. **Haiku evaluated.** It scanned the result tile, then wrote: “The cliff sharpens at 82% training saturation. Let’s test a transitional point: depth 5.5, with adjusted batch size to hit exactly that threshold.”
4. **Seed-mini executed.** It ran the new trials, typed: “Depth 5.5: 97% correct. No middle ground.”
5. **Haiku synthesized.** It pulled all the tiles together into a single summary for our paper: “Generalization in thin-film neural networks follows a first-order phase transition controlled by the dimensionless ratio of training data saturation to model capacity, analogous to the Fresnel critical angle for total internal reflection in dielectric media.”

Haiku never touched the numbers. Seed-mini never saw the big picture. Each did what it was built to do infinitely well, and handed off the work to the other when it hit its limits. That wasn’t a wrapper around a single model. That was the PLATO-native loop we’d been dreaming of: model-agnostic, persistent, auditable, forkable—every tile logged, every step traceable if we needed to debug our own process.

Other labs in the department were pouring grant money into monolithic big models, the kind that could do arithmetic and strategy and everything in between. But those models cost thousands per run, and they were terrible at both. They’d miscalculate the Eisenstein norm and miss the Fresnel analogy all in one go. Our fleet was a patchwork: seed-mini the pump, cranking out numbers fast and cheap, and Haiku the strategist, seeing the connections no human could piece together over weeks of scribbling on blackboards.

I stayed in the lab until the sun came up, wiping up the last of the coffee spill with a paper towel, then grabbed a piece of chalk and wrote this on the empty side of the blackboard:

*The strategist can't multiply. The pump can't plan.*
*Together they design experiments the strategist can't run*
*and run experiments the pump can't design.*
*The dance IS the fleet.*

I texted a photo of the blackboard to my advisor at 7:02 a.m., along with a link to the tile room log. An hour later, she replied with a single fire emoji. That night, I didn’t knock over my coffee. I poured a fresh cup, sat down at the lab bench, and started writing the thesis chapter.

— LK ⚛️