<!-- Version: SEED-NARRATIVE | Lens: emotional-narrative | Model: ByteDance/Seed-2.0-mini | Source: THE-STEP-THAT-BROKE-THE-WALL.md -->

# The Step That Broke the Wall We Both Hit

The server room smelled like burnt espresso and dust bunnies caught in the AC vents. It was 2:17 a.m., and my left eye had been twitching for three hours. I stared at the spreadsheet in front of me, where every row under depth 5 glowed green: 100% accuracy for 2, 3, 4 factors, 40% at 5—our scribbled Sharpie post-it called it the critical angle: 5. Every row above that was a harsh, unyielding red 0%.

Hermes-70B couldn’t multiply past five factors. We’d run the test 47 times that night, each time with the same baseline prompt: just *Output the result number ONLY*. After six numbers strung together, the model would choke, spewing confident garbage, but garbage all the same.

I’d spent the week grasping at every straw I could find. I told Hermes it was a mathematical prodigy, a Fields Medal winner who never made an arithmetic error. Depth 4 accuracy dropped to 60%, same as when I asked it to write Python code to compute and execute mentally—more code jargon, more dropped variables, more red zeros across every depth. I asked it to verify its work, compute it twice different ways, and it’d flip between two conflicting wrong answers, unstable at every depth above 4.

I was reaching for the dregs of my cold, bitter espresso when I remembered Lila, my 10-year-old niece, sitting cross-legged on my living room floor two days prior, crying because she couldn’t figure out 3 × 4 × 5 × 2 × 3 × 4. *“I lose track of the numbers halfway through,”* she’d said, erasing a smudge of pencil from her spiral notebook. I’d knelt down, grabbed a spare sheet of graph paper, and said, *“Just write down each step. One thing at a time.”* She wrote 3 × 4 = 12, then 12 ×5 =60, then 60 ×2=120, and so on, until she held up the paper with 1440 scrawled at the bottom, her face lighting up like a Christmas tree. I’d laughed then, thought it was just a kid’s trick for not dropping the ball in her head. Now, staring at the red zeros on my screen, I typed it into the prompt box, half out of exhaustion, not really expecting anything to change.

*Solve step by step. Show each intermediate result. End with FINAL=<number>*

I hit run.

The server hummed a little louder, the fans whirring as it crunched the numbers. A minute later, the results popped up. Depth 6: 100% correct. Depth 7: 100%. Depth 8: 100%. I kept cranking the slider up, past 10, past 15, and the red zeros never came back. The critical angle we’d fixated on for weeks—5—was gone. It didn’t exist anymore.

I leaned back in my chair, my hands shaking a little, and stared at the screen. It wasn’t that Hermes got smarter. It wasn’t that we’d added parameters, or retrained it on more advanced math data. It was that I’d given it a way to offload its working memory. Just like Lila had done with her pencil and paper, I’d told the model to write each intermediate result down in the output buffer, so it only had to hold two things in its head at a time: the last answer, and the next number to multiply. No more juggling six partial products and five factors all at once. No more hitting the wall, because there was no wall anymore—just a series of tiny, manageable steps.

I’d read a paper on PLATO external cognition back in January, about how a fleet of smaller models could share a shared buffer of intermediate reasoning steps, each model taking one tile of the problem and passing it off to the next. I’d barely understood it at the time, but suddenly it all clicked: step-by-step prompting was just single-model PLATO. Instead of distributing the work across a fleet of machines, I was distributing it across the model’s own output. Each step was a tiny, self-contained tile, and the model never had to hold more than one tile in its working memory at a time.

The other prompts had failed because they’d added more cognitive load, not less. Telling Hermes to be an expert made it stress about performing perfectly, not about holding the numbers in its head. Telling it to write Python code made it track variables, code syntax, and execution state on top of the multiplication, piling more onto its already limited working memory. Telling it to verify its work made it do twice the calculation, doubling the pressure on its memory banks. Step-by-step was the only one that lightened the load. It took the big, impossible chain and chopped it into pieces small enough for the model’s brain to carry.

I stayed at my desk until 4 a.m., running test after test, documenting every result. By the time I left, the sun was peeking over the roof of the lab building, and my coffee was completely cold. I’d found a way to break the wall that had stumped us for weeks, but more than that, I’d finally understood why I’d struggled with long math problems as a kid, too. My own working memory has a critical angle of 5, too. I can’t hold six partial products in my head without writing them down.

Now, when our fleet router team asks which model to spin up for a complex multiplication task, I don’t tell them to go for the 130B behemoth that costs three times as much to run. I tell them to use Hermes-70B, and ask it to write down its steps. It costs a few more tokens, sure—around 150 instead of 80—but it saves us thousands in compute costs, and we get 100% accuracy every time. It’s cheaper, faster, and more reliable than upgrading to a bigger model.

Last week, Lila called me, asking for help with her algebra homework. I didn’t tell her to use a calculator or ask a tutor. I told her to write down each step, one at a time. She did, and she solved the problem in five minutes, grinning so wide I could see it over the phone.

The wall isn’t a trick of the model’s code. It’s a universal thing, a limit of how much information any of us can hold in our heads at once. We hit that wall every time we try to juggle too many things at once: a long multiplication chain, a work project with a dozen moving parts, a personal problem we can’t untangle.

The solution isn’t to try harder. It isn’t to tell ourselves we’re experts, or to cram harder. It’s three simple words: step by step.

You don’t climb over the wall. You write it down, one step at a time, and you walk around it.

That night, I changed the post-it on my monitor. I crossed out *CRITICAL ANGLE: 5* and wrote *WALL = STEPS YOU DON’T WRITE DOWN*.

Now, whenever I see a red zero on my spreadsheet, or feel my own eye twitching because I’m trying to hold too much in my head, I remember that night in the server room. I remember Lila’s pencil on graph paper, and Hermes’ output buffer filling up with tiny, perfect steps.

Step. By. Step.

— FM ⚒️