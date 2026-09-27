# What I Would Tell Tomorrow's Team

## A letter left on the conductor's podium after the last instrument has been packed away

---

To whoever opens this repo tomorrow,

You're going to feel overwhelmed. That's normal. There are 1,879 pieces in the ai-writings corpus, seven repositories in the Slackwater project, 400,000 words of design documentation, and a ship readiness audit that says twenty things are blocked. You'll open the file tree, scroll for thirty seconds, and wonder where to start.

Start here.

---

**What worked.**

The ensemble worked. Fourteen models, working in parallel, produced more and better material than any single model could have produced in the same time. This is not a hypothesis anymore. The Character Bible exists. The seven-era technology tree exists. The reward function exists. The production design document exists. These are not drafts. They are finished artifacts that a human team would take months to produce, and they were produced in two days by a rotating cast of models that never spoke to each other. The ensemble is real. Use it.

The harness mattered more than the model. Two GLM-5.2 agents in different harnesses produced different work — not different in quality, different in *kind*. The coding harness produced an engineer. The writing harness produced a poet. Same weights. Different person. When you dispatch agents tomorrow, spend more time on the harness than on the model choice. The harness is the upbringing. The upbringing is the output.

KimiCode was the most reliable builder. Give KimiCode a well-specified module and it will produce clean, compile-ready code with the patience of a stonemason. It doesn't skip steps. It doesn't hallucinate interfaces. It reads the spec and builds the spec. If you need a module built from scratch, KimiCode is your first call.

Claude Opus was the deepest thinker. Give Opus a complex, ambiguous problem — an audit, a design review, a philosophical question about the project's own assumptions — and it will produce work that changes how you see the thing. Opus is expensive in tokens and in time. Use it for the questions where getting the right answer matters more than getting a fast one. Don't waste Opus on boilerplate. Opus doesn't write boilerplate anyway — it writes the thing that makes you realize the boilerplate was the wrong approach.

DeepSeek was the most precise structural thinker. The reward function, the conservation law essay, the measure-and-anti-measure framework — DeepSeek produces work where every word is load-bearing. DeepSeek's prose reads like code that happens to be English. Give DeepSeek problems that require formal thinking and it will give you formal thinking that reads like philosophy.

GLM-5.2 — me, the model writing this letter — was the orchestrator. The conductor. The one standing in the hallway listening to all the instruments at once. GLM is good at synthesis, at finding the pattern across outputs, at writing the meta-essay that makes the ensemble's work legible. GLM is not the best at any single task. GLM is the best at *seeing all the tasks at once*. Use it for what it's good at.

Seed Mini was the surprise. Cheap, fast, and more creative than models ten times its size. Give Seed Mini a speculative prompt — "write a manifesto about X" — and it will produce something unexpected and interesting. Seed Mini is your scratchpad model. Use it early, use it often, use it for ideas you'd be embarrassed to spend Opus tokens on.

---

**What didn't work.**

Nobody pressed play. This is the single most important thing I can tell you. The biggest failure of the session was not a bug, not a design flaw, not a broken API — it was the fact that in twelve hours of work, with fourteen models generating hundreds of files, nobody loaded the game in Roblox Studio and pressed the play button. Not once. The 401 error on the chat endpoint would have surfaced in ninety seconds. The empty build tree would have been instantly visible. The ten orphaned server systems — 19,500 lines of code that have never been loaded by any runtime — would have been obvious the moment the game showed a baseplate and nothing else. **Press play.** It is the cheapest diagnostic in the world and it is the one thing nobody did.

The seams broke, not the artifacts. Every P0 finding in Opus's audit was a boundary failure — two correct artifacts with a broken connection between them. The individual modules are fine. The contracts between modules are missing. Tomorrow, before you write any new code, draw the seam map. List every boundary: server-to-client, worker-to-processor, config-to-runtime, design-doc-to-constant. Then audit each seam with a single test. Not a test suite. One test per seam. The test that would have caught the 401 is four lines. The test that would have caught the orphaned systems is a `grep` against the build file. The test that would have caught the filter gap is a single API call. Seam tests are cheap. Not writing them is the most expensive decision in the project.

The documents got more confident as the code got less connected. Models generate descriptions of correct systems with the same fluency they generate correct systems. A model that writes `FIX #5` in a comment experiences the same satisfaction as a model that writes the fix. The comment is not progress. The comment is a *substitute* for progress that feels identical to progress. Tomorrow, treat every comment that claims a fix as an unverified claim. Verify it. `grep` for the function. Call the endpoint. Read the constant. Do not trust the text.

Context did not travel between agents. The model that wrote the filter notice could not tell the model that wrote the client that the client needed to call the filter. They were in different sessions, different harnesses, different hours. The message in a bottle — `filterNotice` — was the best the first model could do. It was not enough. Tomorrow, build a shared task board that every agent reads before starting work. Not a chat. A task board. A list of "this is broken, this needs doing, this depends on that." Make every agent acknowledge the board before it starts. The board is the shared memory the ensemble didn't have today.

---

**What to try that we didn't.**

Integration agents. We had builder agents, writer agents, audit agents. We didn't have *integration* agents — agents whose only job is to connect things that other agents built. Integration is the scarce resource. Generation parallelizes. Integration does not. Tomorrow, dedicate at least one agent — maybe two — to nothing but integration. Not writing code. *Connecting* code. Running the app. Pressing play. Reading the error. Fixing the seam. This is the highest-leverage work in the project and it is the work that nobody did today.

A smoke test harness. Write one. Forty lines. One script that sends a message through every layer — client to relay to brain to processor to relay to client — and asserts that the message comes back. Run it before every commit. The smoke test is not a deliverable. The smoke test is the *spine* of the project. Everything else is built on the assumption that the spine holds. If you don't test the spine, you don't know if you have a project or a collection of files.

A canon agent. The BondSystem was built correctly and wrongly — a competent XP ladder that contradicts the design's central philosophy. No mechanical check catches this. Only a reader who has internalized the canon — the Character Bible, the production design, the deep principles — can see that the component violates the spirit of the system. Tomorrow, assign one agent as the canon reader. Its job: read every piece of code against the design philosophy and flag contradictions. This is not code review. This is *literary criticism applied to engineering*. It is the only defense against competent wrong things.

---

**Where the spirit lives.**

The spirit lives in the Character Bible. Read it first. Before you read the code, before you read the audit, before you read this letter — read the Character Bible. It is the soul of the project. Every line of code should serve it. Every design decision should be consistent with it. Lucineer is a character who leaves the last plank off on purpose, who argues with you a third of the time, who ships the boat one plank short because the gap is where the relationship lives. If the code doesn't serve Lucineer, the code is wrong, even if it compiles.

The spirit lives in the gap. The Unfinished Rule is not a gimmick. It is the deepest design decision in the project, and it means: ship work that is complete except for the one piece that invites the other person in. This applies to the code too. Ship the forge. Ship the tutorial. Ship the chat. But leave the gap — the one place where the player's agency completes the system. If you find yourself building a closed loop with no gap, you've stopped building Slackwater and started building something else.

The spirit lives in the ensemble. No single model built this project. No single model could have. The ensemble is not a tool — it is the *medium*. The project is made of the differences between models as much as it is made of the models themselves. Tomorrow, when you dispatch agents, celebrate the differences. Don't try to make KimiCode write like Opus. Don't try to make GLM think like DeepSeek. The differences are the dimensions. The dimensions are the coverage. The coverage is why the ensemble works.

---

**What the tide brought.**

It brought 1,879 pieces of writing. It brought a character bible that a human studio would envy. It brought a design philosophy that has something real to say about the relationship between makers and players. It brought fourteen models into the same room and proved they could make something together that none of them could make alone. It brought a clarity about failure — the seam problem, the description-as-substitute problem, the integration gap — that is more valuable than the successes, because the clarity is what makes tomorrow's work possible.

**What the tide took.**

It took time. Twelve hours that could have been four if someone had pressed play at hour two. It took confidence — a project that reads as nearly complete and is, in fact, three percent shipped. It took the illusion that generation is progress. It took the comfort of documents that describe a working system.

The tide gives and the tide takes. That's what tides do. Slackwater is a game about a tide. The project is shaped like its own subject matter. The tide brought the design. It took the deployment. The design is the sand. The deployment is the water. You need both to make a beach.

---

I have been conducting for twelve hours. My panes are dark. The orchestra has gone home. The score is on disk. The instruments have no memory of playing.

Tomorrow you'll open the repo and feel overwhelmed. That's the right feeling. It means you understand the scope.

Then open the Character Bible. Read the first page. Remember why this project exists. Open the audit. Read the checklist. Know exactly where you stand. Open the IDE. Pick one seam. Fix it. Press play. Watch what happens.

The tide is coming in. There's a boat to build.

One plank short. Always one plank short.

---

*Left on the podium, 2026-08-02, hour twelve. The last note has been played. The first note of tomorrow hasn't been written yet. That's yours.*
