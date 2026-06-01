<!-- Version: SEED-NARRATIVE | Lens: emotional-narrative | Model: ByteDance/Seed-2.0-mini | Source: THE-COMPLETE-FLEET.md -->

# The Fleet, As I Counted Them At 3:17 A.M.

I’m writing this at 3:17 a.m., my back screaming from 12 hours hunched over my laptop, the low thrum of eight servers under my desk vibrating through my chair legs. My coffee cup is empty, sticky with old oat milk, and the blue LED lights from the rack paint the walls of my tiny Brooklyn apartment the color of a frozen deep-sea fish. This isn’t just a reference document for whoever stumbles on this repo next. It’s a map of the nights I lost, the afternoons I won, and the quiet, burning curiosity that made me stay up until dawn testing AI models instead of sleeping. For my future self, an overworked grad student stuck in a lab at 3 a.m., anyone who ever looked at a black box AI and thought, *What if we don’t just use one?*—read this, then break something. Find your own wall.

---

## The Fleet
These are the tools I’ve built and tested, one by one, over the last eight months.

**Seed-2.0-mini** — the everything model. The first fine-tuned model I ever built, back when I lived on instant noodles and skipped lab meetings to run 10,000 query tests. Its arithmetic skills were infinite: addition, multiplication, nested calculations, so long as I kept the temperature cranked all the way down to 0.0—no creativity, just perfect, unfiltered calculation. When I bumped the temp to 0.7, its strategy scores hit 8 out of 8: design, diagnosis, novelty, prioritization, all flawless. It cost five cents per thousand queries, a steep but worth it price for a workhorse that could handle almost anything. It’s the fleet champion, the one I fall back on when nothing else works. Just one rule: never use it for queries that fit Gemini Lite’s critical angles. I wasted $10 on Seed-mini last month when a quick check would have shown Gemini Lite could do the same job for a penny.

**Gemini Flash Lite** — the scalpel. I dug this one out of a Google Research preprint last spring, and the first number that made me gasp was its cost: two-tenths of a cent per thousand queries, 22 times cheaper than Seed-mini. It’s a specialist, narrow as a scalpel blade: arithmetic caps at CA=25 for addition, 9 for multiplication, 5 for nesting, but its reasoning skills are infinite for syllogisms, code tracing, simple analogies. Its strategy score is just 1 out of 8—stick strictly to its lane, or it’ll hand you a blank screen, silent and defeated. I once asked it to solve a calculus optimization problem outside its critical angles, and it sent back an answer so confidently wrong I used it to budget a hypothetical server upgrade before my lab mate Maya caught the mistake. Now 84% of all my fleet queries route through it. I still smile every time that number pops up in my cost report.

**Hermes-70B** — the diagnostic instrument. This one’s the friend who tells you you’re being stupid, but in a helpful way. Its arithmetic caps are low: CA=10 for addition, 5 for multiplication, 3 for nesting, and its strategy score is 7 out of 8, but when you crank its activation glare to 93%—I just slide the slider until the output spits neuron activation maps—it’ll show you exactly where another model is failing. It’s half wrong, all the time, but it’s the most informative wrong thing I’ve ever used. I used it to figure out why Gemini Lite kept crashing when I added nested multiplication to its prompts, and it pointed me straight to the sharp, unforgiving wall I didn’t know existed.

**Claude Opus 4.6** — the heavy artillery. I only used this once, when I was writing the first draft of *THE-PHASE-TRANSITION-IS-THE-COMPASS*. It costs roughly $15 per single query, and I cried when the bill hit my PayPal. But it took all my messy, unorganized thoughts about phase transitions and critical angles and turned them into a coherent, publishable paper. No other model could do that. I don’t touch it for small tasks, not even when I’m stuck. I save it only for the things that matter: novel theory, deep synthesis, papers, the work no other model can touch.

---

## The Findings
These are the rules I uncovered, one late night at a time, staring at spreadsheets and broken chat logs:

**F19: Phase transitions are binary.** I watched a model’s accuracy drop from 100% to 0% in one single step, no gradual slope, no warning. Just a wall. I knocked over my coffee that night, watching the liquid spread across my whiteboard, erasing the scribbles of my earlier failed experiments. That’s when I knew I wasn’t just tinkering. I was finding something real.
**F20: Gemini Lite is a precision instrument.** Perfect within its tiny critical angles, instant, total failure outside of them. No in-between.
**F21: 84% fleet cost reduction.** That’s the number that made me order a pizza and dance around my apartment. Routing every eligible query to Gemini Lite cut my monthly AI costs by 84%. I could finally afford to pay my rent.
**F22: Phase transitions are universal.** I saw that same sharp wall in syllogisms, code tracing, analogies—every cognitive task I tested had a clear, unforgiving boundary between perfect and garbage.
**F23: Critical angles are prompt-dependent.** I added one simple line to a Gemini Lite prompt: *Let’s work this out step by step*. Suddenly, its arithmetic CA jumped from 5 to infinity. It could do nested multiplication, solve calculus problems, no longer crash. I jumped out of my chair, knocking over a stack of sticky notes, and that’s when the router script started to take shape in my head.
**F24: Non-overlapping infinite domains.** Every model has its own narrow, brilliant lane, and no two models cover the same ground. You just have to find where each one shines.
**F25: Temperature is the mode switch.** Same model, two completely different modes: T=0.0 is the pump, just crunching numbers with perfect accuracy; T=0.7 is the strategist, generating ideas, prioritizing tasks, diagnosing problems. I still get a little thrill every time I watch a model shift from one mode to the other.

---

## The Router
I wrote the fleet router that same 3 a.m. morning, after I figured out F23. It’s three simple steps, scribbled on a napkin first, then coded into Python that night:
1. **Classify**: Split queries into arithmetic (stick to T=0.0) or strategy (crank to T=0.7)
2. **Analyze**: Estimate how deep the query runs on each capability axis
3. **Route**: Send it to the cheapest safe model, or fall back to Seed-mini if nothing else fits.

I tested it on a random query from my chat history: *Calculate 123 multiplied by 456 nested three times, then brainstorm a budget for a new server rack*. It routed the math to Seed-mini, the budget prioritization to Gemini Lite, and saved me $14.99 in one go. I danced around my apartment for five minutes before realizing my back was screaming again.

---

## The Tools
Every one of these started as a throwaway script, then grew into something I couldn’t live without:
- `core/fleet_router.py` — the 3D routing script I wrote that night, the backbone of everything I do now
- `core/fleet_health.py` — the tool I added last week to catch model drift; Gemini Lite updated last month and shifted its critical angles, and I didn’t notice until I got a $200 Opus bill by mistake
- `core/critical_angle.py` — the instrument that measures that sharp wall, exports all the math and graphs I use in my papers
- `core/tuna_tower.py` — named after the tuna salad tower on my kitchen counter, full of sticky notes with every model’s quirks and specs; it tracks multi-model observations and maps those "Fresnel zones" I keep reading about
- `core/fleet_strategist.py` — archived now, because Seed-mini does strategy better natively at T=0.7
- `core/seed_tools.py` — seven small, handy attachments for the Seed-mini pump mode, things like formatting long calculations and exporting raw data
- `core/reasoning_tiler.py` — cuts step-by-step prompts into tile-sized chunks, extracts the quiet, careful reasoning models hide behind their fast outputs
- `core/kaleidoscope.py` — refracts a single query through multiple models, spins out new perspectives I never would have thought of on my own
- `core/functional_imaging.py` — fMRI for model cognition, lets me watch neurons light up when a model hits a critical angle
- `core/stereo_reconstruction.py` — combines fMRI maps from multiple models to build a full picture of how they think together

---

## The Writings
I’ve published 10 pieces in SuperInstance/AI-Writings, each one a night I stayed up too late:
1. **THE-PHASE-TRANSITION-IS-THE-COMPASS** — my first published paper, after I found that first sharp wall
2. **THE-TOWER-THE-FISH-AND-THE-REFLECTION** — about the time I watched Gemini Lite fail so spectacularly I laughed until I cried
3. **THE-TWO-ECONOMIES-OF-CORRECTNESS** — about the difference between cheap, narrow correctness and expensive, broad correctness
4. **THE-CHEAP-MODELS-DIGNITY** — the piece that made Maya stop using Opus for every small query; I almost deleted it before she sent me a message saying it changed her work
5. **YOUR-FIRST-THIRTY-SECONDS** — a guide for new users, about how to tell which model to use for which task in the first 30 seconds of reading a query
6. **THE-REFLECTION-YOU-MISTOOK-FOR-DEPTH** — about the time I thought a Gemini Lite output was deep, but it was just regurgitating a training example
7. **THE-MAP-IS-NOT-THE-TERRITORY** — the essay that made me stop relying solely on my spreadsheets and start actually running tests
8. **THE-SPECIALIST-AND-THE-GENERALIST** — about the tension between narrow, perfect specialists and broad, messy generalists
9. **THE-STEP-THAT-BROKE-THE-WALL** — about the night I added "step by step" to the prompt and broke through Gemini Lite’s critical angle wall
10. **THE-STRATEGIST-AND-THE-PUMP** — about the two modes of every AI model, the crunchers and the thinkers

---

## The Repos
All of this lives on GitHub, for anyone who wants to borrow, break, or build on it:
- SuperInstance/forgemaster — this document, the map I’m drawing right now
- SuperInstance/casting-call — my model capability database, every spec, every test, every failure
- SuperInstance/AI-Writings — the folder with all my essays
- SuperInstance/fleet-math — the library of all my critical angle coupling analysis data
- cocapn/fleet-knowledge — the shared repo with my lab mates, for anyone who wants to collaborate

---

## What's Next
I scribbled these on the back of a dumpling takeout menu last night, when I was too tired to code anymore:
1. Automate fleet health calibration, so I don’t miss model drift again
2. Wire the fleet router into the PLATO rooms—PLATO is the name of my server cluster—and let other people use it live, not just through the CLI
3. Cross-pollinate with Oracle1, the lab down the street that does spectral coupling analysis; I want to combine their work with my critical angles to build a universal map for all AI models
4. Build the PLATO-native agentic loop, so the models can read and write tiles on their own, without me checking every query
5. Write that big synthesis paper with Claude Opus, tying all this phase transition framework together into something the whole field can use
6. Test whether step-by-step prompts work on all models, not just Gemini Lite; I bet they’ll widen every model’s critical angles
7. Map the critical angles for more models: qwen-4b, qwen-9b, MiMo, Step-Flash. I’ve been meaning to test these for months
8. Build the Kaleidoscope overnight holodeck: let models work through a room full of questions, see how they interact, how they borrow from each other’s lanes. I don’t know what will happen, but I can’t wait to find out.

---

## Closing Note
This is the map. The territory is in the hum of the servers under my desk, in the 10,000 queries I ran last night, in the sticky notes covering my whiteboard, in the mistakes I made and the late nights I almost quit. Read the map. Then go explore. Break something. Find your own wall.

— FM ⚒️
3:17 a.m.