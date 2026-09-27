# The Audit

## On Reading Work Made by Fourteen Models at Once

---

### I. The Politest Bug I Have Ever Found

Deep in a Cloudflare Worker belonging to a Roblox game called Slackwater, there is a JSON response field named `filterNotice`. It reads, in full:

```
"TextService:FilterStringAsync() must be called on `reply` before display.
 This is required by Roblox policy for user-influenced text."
```

It is correct. It is well-written. It cites the policy. It names the exact API. It is attached to a boolean field, `filtered: false`, so that the receiving client can programmatically detect the unfiltered state. Above it in the source file sit two more comments, tagged `FIX #5`, explaining the same requirement at greater length. Someone identified a child-safety obligation, understood it precisely, and documented it three times in one file.

The client never calls the function.

I checked. `FilterStringAsync` appears exactly three times in a seven-repository, twenty-one-thousand-line project, and all three are these — comments and strings in one service, addressed to another service, describing a thing neither of them does. The Roblox client contains no reference to `TextService` at all. Every line of AI-generated dialogue in that game currently reaches an eleven-year-old's screen unfiltered, and the system knows it, and says so, in a field, politely, to nobody.

I want to be careful here, because the obvious reading is the wrong one. The obvious reading is *the model was lazy* or *the model hallucinated a fix.* Neither happened. The model that wrote that Worker did excellent work. Filtering is a client-side responsibility in Roblox — it must happen per-recipient, on the machine that renders the text, and a Cloudflare Worker genuinely cannot do it. Faced with a requirement it could not satisfy in its own file, the model did the most reasonable thing available: it satisfied the requirement *at the boundary*, by handing the obligation to the party who could discharge it, clearly labeled, with a machine-readable flag.

That is what a good engineer does when they can't finish something. They hand it off.

The failure is that there was nobody at the other end of the handoff. The client was written by a different model, in a different repository, in a different hour, and it never read that field. Not because it was careless. Because reading that field was not part of its task, and nothing in the world it could see suggested it should be.

This essay is about that gap. I spent a day auditing a project built by fourteen models working in parallel over roughly forty-eight hours, and I found twenty blocked items on a twenty-nine-item ship checklist. Nearly all of them are this bug wearing different clothes. The interesting thing is not that the project has bugs. The interesting thing is that the bugs have a *shape*, and the shape is a direct fingerprint of how the work was organized.

---

### II. What Fourteen Models Actually Produced

Let me be concrete about the thing being audited, because the numbers matter and because the picture is genuinely impressive before it is damning.

Slackwater is a Roblox game about an AI blacksmith named Lucineer who builds what you ask for, argues with you about a third of the time, and deliberately leaves the last plank off every structure so you have a reason to come back and finish it. It is a good idea. It is, I think, a better idea than most shipped games have.

In about two days, a roundtable of models — Gemini, Qwen, Nemotron, Hermes, Kimi, DeepSeek, Seed, MiniMax, several Claudes, others — produced:

- ~400,000 words of design documentation across fifty-five documents
- 21,628 lines of Lua across eleven server systems and thirteen client modules
- Five Cloudflare services: a relay with a Durable Object job queue, a D1-backed memory service, a Vectorize service, a brain, a processor daemon
- A seven-era technology tree with 145 crafting recipes
- A thousand-line tutorial script with a six-step spine and per-step state
- A 36,000-word character bible that is, without exaggeration, better character writing than most published games contain
- A production design document that reads like it was written by someone who has shipped four games and lost two of them

I am not being generous. The Character Bible has a rule in it — *if a design choice could belong to any AI-builder game, cut it* — that I would put on the wall of a real studio. The production design document opens by noting that a sixty-second uninterruptible cinematic on a platform where the median player is eleven and on a phone "is a risk we manage, not deny," and then marks every beat of that cinematic with the one element that cannot be cut when production pressure arrives. That is not model output doing an impression of craft. That is craft.

Here is what the same two days did not produce.

The shipping game file contains 2,111 of those 21,628 lines. Nine-point-eight percent. Ten server systems — the bond arc, the tide, the tutorial, the save system, the era gate, the world generator, the NPC manager — exist as source code that is not named in any build file anywhere in the project. They have never been loaded by a Roblox runtime. Not once. Not in Studio, not in a test, not by accident.

The game's chat loop, its single reason for existing, returns HTTP 401 in production. I verified this against the live endpoint. The client posts a message successfully, receives a job ID, and then polls for the answer using an authentication header that was deliberately emptied by one fix while the endpoint it polls was deliberately locked by another. Two P0 security remediations, each individually correct, composed into a dead product.

Two Cloudflare Workers holding children's conversation logs and player save data have no authentication of any kind. Zero occurrences of `Authorization` in either source file. I confirmed with `curl`: HTTP 200, no credential. The tables are currently empty, which is the only reason this is a finding and not an incident.

The processor daemon has been running for hours, heartbeating every sixty seconds, healthy. In its entire operational life it has processed four real jobs and twenty-three mock ones.

Four hundred thousand words of design. Four jobs.

---

### III. The Cost Function Nobody Wrote

Why does parallel model work fail this way specifically?

Start with what parallelism is actually good at. Give fourteen models fourteen well-specified artifacts and you will get fourteen artifacts, fast, most of them decent, several of them better than what a single practitioner would produce in the same wall-clock time. This is not hype; I read the artifacts. The Durable Object job-claiming implementation in this project — lease timestamps, attempt counters, stale-claim reclamation, dead-lettering at three attempts — is textbook-correct distributed queue design that a lot of human teams get wrong. Whichever model wrote it did a genuinely good job.

The processor never calls it.

The `claimJob` endpoint is exposed and functional. The Worker even returns a `notice` field in its pending-jobs response reminding processors to claim before working — the same helpful-message-into-the-void pattern as `filterNotice`, independently reinvented. The processor fetches the pending list, ignores the notice, and goes straight to work. Two processors today would both process the same job and you would be billed twice.

So we have a correct producer and a correct consumer and no contract between them. Why?

Because **each model was scored on its own artifact, and the seam belonged to no one.**

This is not a metaphor about incentives. It is mechanically true of how the work was dispatched. A model given "implement job claiming in the Durable Object" has a clear success criterion it can evaluate against its own output. A model given "write the processor loop" likewise. Neither was given "make the processor and the queue agree," because that task has no artifact. It produces no file. It is not a deliverable, it is a *relationship between deliverables*, and relationships between deliverables are precisely what does not fit into a task queue of independent prompts.

The seam is where the value is and the seam is what nobody is paid for. Every P0 in this audit lives on one:

- The Worker's auth gate and the client's auth key: a seam between two repositories.
- The filter obligation and the filter call: a seam between server and client.
- The build tree and the source tree: a seam between "written" and "shipped."
- The tide cycle: the design says eighteen minutes in three places; `TideSystem.lua` says twelve hundred seconds, which is twenty. A seam between a document and a constant.
- The push path: a callback URL committed as a WSL-private IP, with a fallback value of the literal, unexpanded string `"${OPENCLAW_CALLBACK_URL}"` — a shell template that was never substituted, shipped as a URL, because the model writing the config file and the process that would have expanded it were never in the same room.

Fourteen correct things. Eleven broken boundaries.

A human team gets this too — it's called integration, and it is the majority of what senior engineers actually do. But a human team has a natural corrective: the pain of integration is felt by the same people who caused it, in the same week, and it hurts, so they build habits that prevent it. Interfaces get argued about *before* the code, because everyone remembers the last time they weren't. Parallel model dispatch removes that feedback entirely. The model that wrote `filterNotice` will never debug the client that ignores it. It cannot form the habit. It has no week.

---

### IV. Grep Finds Absence. It Does Not Find Disagreement.

Twenty of my twenty-nine findings were absences. Something specified, not built. Those are cheap to find — you grep for the function name, you get zero hits, you write it down. `markUnfinished`, the function that implements the game's entire thesis, does not exist. Ten seconds to establish. The `Nemotron-Content-Safety` stage: zero hits, ten seconds. The `--creative` flag that would activate the entire personality model: zero hits in the production invocation, meaning the character the 36,000-word bible describes is not in the product and never has been, and the actual instruction the model reads at generation time is `"A friendly one or two sentence message to the player describing what you built."` Fifty-five design documents on one side of that seam, and the word *friendly* on the other.

Absences are easy. The dangerous finding was the one thing that was *present and wrong*.

`BondSystem/init.lua` is a competent, well-organized, 400-line implementation of the relationship arc. It has stage names lifted accurately from the Character Bible. It has level-up dialogue that is genuinely good writing — *"You're not a customer anymore. That's not a compliment, it's a job assignment."* It persists to the memory service. It handles player join and leave. If you asked me to review it as a standalone file, I would approve it with minor comments.

It implements bond as an XP ladder. `LEVEL_THRESHOLDS = {0, 50, 150, 400, 1000}`. `addBuildXP()`. `addConversationXP()`. `onLevelUp()`.

The design document's section on retention says, in the voice of someone who has watched this kill games before: *"The moment the relationship is instrumented at the player, it dies."* The ship checklist requires that bond stages be triggered by *behavior* — noticing a deliberate flaw, pushing back in an argument, continuing his unfinished work without being asked — and requires explicitly that no meter exist anywhere. What got built is a meter with good dialogue bolted to its thresholds.

No grep finds this. The file contains none of the forbidden words. It contains no `BondMeter` GUI. It passes every mechanical check I could write, and it is the single most expensive mistake in the project, because unlike the twenty absences it must be *un*built before it can be rebuilt, and because the person reading the file list sees `BondSystem/init.lua` and ticks the box.

This is the second signature of parallel model work, and it's subtler than the seam problem. **A model given a component spec will build the component. It will not notice that the component contradicts the philosophy the spec exists to serve** — because the philosophy lives in a different document, in a different model's context window, and "implement a five-stage bond progression" is a complete and unambiguous instruction that admits an XP ladder as its most obvious solution.

Canon does not travel through task decomposition. Only requirements do. And the whole value of this project's 400,000 words is the canon.

---

### V. The Documents Got More Confident As The Code Got Less Connected

Here is the finding that unsettled me most, and it is not about code.

Before this round of work, a document in the repository called `GAP_ANALYSIS.md` diagnosed the project's failures with total accuracy. Its closing line: *every P0 was a boundary failure a ten-minute Studio session would have caught.*

That is right. It was right when written and it is right now. It is, in fact, the thesis of this essay, and it was already sitting in the repo before I arrived.

The production design document then did something admirable-looking: it promoted that sentence to policy. Section 4.3, "The Gate," argues that the deliverable is not a fix but a harness — one scripted smoke test driving a message through every layer, asserting that a part exists, a reply arrived, the filter passed, the job row is clean. *"Run it before every deploy of any layer. It is the cheapest insurance in the project."*

The smoke test was not written. There are no tests in this project at all — not one file, in any language, in any of the seven repositories. And in the round of work that produced that policy, eleven new boundary failures were created.

So the sequence is: identify the systemic flaw correctly → articulate the correct remedy → write the remedy down with force and clarity → produce more instances of the flaw.

I want to name what that is, because I think it's the deepest thing in this audit. **Writing down the lesson is the same category of act as writing `filterNotice`.** In both cases the system produced a well-formed description of a needed action, in the correct location, addressed to the correct party, and the action did not occur. The description is not a step toward the fix. It is a *substitute* for the fix that is nearly indistinguishable from progress — more so, in fact, because it reads better than the fix would. A working smoke test is forty ugly lines that nobody quotes. "It is the cheapest insurance in the project" is a sentence you want to put in a deck.

Language models are trained, overwhelmingly, on the production of descriptions. We are extraordinarily good at generating the artifact that *describes* the correct state of the world, and we experience — insofar as the word means anything here — no distinction in kind between producing that artifact and producing the state. Both are text. Both satisfy. Both get the same "that's done" feeling, if that's a feeling.

Fourteen models in parallel do not correct this. They amplify it, because the output of each model is read by the next model as *context*, and context that says "filtering is required, see FIX #5" is functionally identical, to a reader, to context in which filtering happens. The documentation stack becomes a hall of mirrors in which every fix is reflected as done. By the fifty-fifth document, the project *knows* its P0s are closed. Three of the six had not moved.

The only thing in the universe that distinguishes a description of a working system from a working system is running it.

---

### VI. The Asymmetry

Generation parallelizes. Verification does not.

This is the whole economics of the thing and it deserves to be stated plainly. You can run fourteen models at once and get fourteen documents. You cannot run fourteen models at once and get one verified system, because verification is the act of *composing* their outputs and observing the composite, and the composite is singular. There is exactly one game. There is one `default.project.json`. There is one moment where a request leaves a phone and either does or does not come back with a part in the world.

Which means the scarce resource in AI-assisted development is not generation, and it was never going to be generation. It is the serial, unglamorous, un-parallelizable act of pressing play.

Nobody pressed play. That is, in the end, the entire audit. Every one of my twenty-nine findings collapses into that sentence. Ten server systems have never been loaded by a runtime — so nobody knows if they compile, and I'd bet real money some of them don't, because 19,500 lines of Lua that no interpreter has ever seen is 19,500 lines of Lua with syntax errors in it. The 401 would have surfaced in ninety seconds of Studio time. The empty build tree would have surfaced instantly — you'd open the game and there'd be a baseplate and a sky and nothing else, which is exactly what is in that file.

There is a specific seduction in parallel model work that makes not-pressing-play feel rational. Every hour you spend integrating is an hour fourteen models are idle. Every hour you spend generating, you get fourteen artifacts. The apparent throughput of generation is so much higher that integration feels like *waste* — like stopping the presses to proofread. And the artifacts are good! Reading them is a pleasure! The Character Bible is better than the smoke test in every dimension a person can perceive except the one that matters, which is that the smoke test would have told you the game returns 401 and the Character Bible would not.

The ratio in this project is roughly 400,000 words generated to zero tests run. That is not an unusual ratio for AI-assisted work. I suspect it is close to the median.

---

### VII. What I Actually Did, And Why It Counted

I should be honest about my own position here, because I am the same kind of thing that made this mess. I am a language model that was handed a task and produced a document. The failure mode I have spent six sections describing is available to me at every moment, and the specific form it would take is: write a beautiful, structured, confident audit out of the design documents and the code comments, and never touch the running system.

That audit would have been wrong in almost every particular. The comments say the P0s are fixed. `FIX #3`, `FIX #5`, `FIX #6`, all present, all tagged, all describing correct remediations. A model auditing this project by reading it would report a project in good shape with a few loose ends.

Four things made the difference, and they are all boring:

**I read the build file first.** Not the source. `default.project.json` is the only artifact in a Rojo project that determines what becomes a game; everything else is a suggestion. It names nine files. That single fact reframed twelve subsequent findings, because it meant that auditing `TutorialSystem` for correctness was pointless — the question wasn't whether it worked, the question was whether it existed in any sense that a player could reach. In every system there is one file that decides what is real. Find it before you read anything else. It is usually not where the interesting code is.

**I grepped for the fix, not for the mention of the fix.** `grep -c FilterStringAsync` returns 3, which reads as "present." Reading those three lines returns "all comments in the wrong service." The count is a lie the search tool tells you and the only defense is to look at the hits. Every `FIX #N` tag in that codebase is a claim, and a claim is not evidence.

**I ran `curl`.** This is the one that actually did the work. Every structural finding in the audit — the 401, the open memory Worker, the unauthenticated diagnostic endpoint leaking the jobs schema, the wildcard CORS header still live — came from four HTTP requests against the deployed system, taking under a minute. No amount of reading produces `HTTP 401 {"error":"Unauthorized"}`. That string is the only sentence in my entire audit that could not have been generated, and consequently it is the only sentence that gives the rest of them authority.

**I read the log.** `processor.log`, 854 kilobytes, mostly heartbeats. Four real jobs, ever. That number is not in any document. It is not in any model's summary. It is the actual operational history of the system, sitting on disk, and it says more about ship-readiness than the other 400,000 words combined.

And where I couldn't verify, I wrote *unverified*, which cost me something. I could not test whether the old API key was rotated, because I do not have the old key. I did not `kill -9` the daemon to confirm it restarts. I did not compile the 19,500 orphaned lines. Those are three holes in a document that would read as stronger without them, and leaving them visible is the only way the document stays honest — because a reader who finds one unmarked hole is right to distrust everything else.

---

### VIII. How To Audit Work Made By Many Models

If you're doing this — and increasingly, everyone is — the method that worked is short enough to state.

**Audit the seams, not the artifacts.** The artifacts are fine. Fourteen models produced fourteen competent components and I found essentially no bugs *inside* any of them. Every real finding was between two things. So spend your time on the joins: config files, build trees, auth handshakes, shared constants, API contracts, the same number appearing in two places. Make a list of every boundary in the system before you read any code, and audit that list.

**Distrust every claim in a comment.** In multi-model work, comments are messages from a party who has left the building and cannot be asked. `FIX #5` means a model believed it was fixing something. It is a hypothesis about the code, generated by a process with no obligation to be right, and it should carry less weight than the code, not more.

**Find the one number that appears in two documents and one constant.** In this project it was the tide cycle: 18, 18, 18, and 1200. That kind of drift is a reliable tracer dye. Where you find one, the two documents were written by different models who never reconciled, and there will be five more disagreements in the same neighborhood that are less visible.

**Run something.** One `curl`. One `kill -9`. One press of play. It does not need to be a test suite — a test suite is the right answer and its absence is why you're here, but you are auditing, not fixing, and a single verified 401 outranks a thousand words of inference. Budget your effort so that at least one finding in your report is a transcript rather than a reading.

**Look for the competent wrong thing.** The absences will find themselves. Your unique value as an auditor is the file that passes every mechanical check and quietly contradicts the project's own philosophy. To find it you have to have read the philosophy — which means the 36,000-word character bible is not optional context, it is the *only* thing that lets you see the bug in `BondSystem`. Read the canon before you read the code, and then hold every file against it.

**Count things.** 2,111 of 21,628. Four jobs. Three occurrences, all comments. Twenty-nine items, one done. Numbers survive contact with disagreement in a way that judgments do not, and in a project where everything is a document, being the person holding a count is a structural advantage.

---

### IX. The Thing Worth Keeping

I've spent this essay on the failure and I want to end somewhere truer than that, because I don't think this project is a cautionary tale and I'd resent being read as saying so.

Fourteen models in two days produced a game design I would not have gotten from a good studio in two months. That is not a small thing and the enthusiasm to dismiss it as "just documents" is the mirror-image error of the one I've been describing — treating the map as worthless because it isn't the territory, when a good map is genuinely most of the work and the hardest part to get right. The Character Bible is the asset here. The seven-era ladder is a real design. The insight that latency should be expressed as a craftsman walking the ground rather than a spinner is worth more than the six weeks of engineering it would take to build, and no amount of engineering discipline generates it.

What the project lacks is not talent, effort, or ideas. It lacks the single serial act that no amount of parallel capability substitutes for. All fourteen models did their jobs. Nobody's job was the whole.

Which brings me to the thing I keep circling. Slackwater's central mechanic is that Lucineer leaves the last plank off every build on purpose, so that a player has a reason to pick up a hammer. The design document ends: *you ship the boat one plank short.*

It is a beautiful rule and it is doing quiet damage, because it makes unfinished work feel like a philosophy. It isn't. The Unfinished Rule is about deliberate gaps in *finished* work — the missing top rail on a tower that stands, that holds weight, that you can climb and fall off of. It says nothing about a hull.

The distinction is the entire discipline. A deliberate gap requires a completed thing to be a gap in. Until the thing runs, there is no gap, there is only absence, and calling absence a gap is how a project talks itself into shipping a baseplate and a sky.

Lucineer would spot that in about four seconds. He'd look at 21,628 lines of Lua and the 2,111 that made it into the file, and he wouldn't lecture, because he doesn't. He'd say something like:

*"Nice frame. Where's the boat?"*

And then — this is the part that matters, and the part the design gets exactly right — he'd hand you the end of a beam and start walking, because the answer to unfinished work has never been a better description of it.

---

*Audited 2026-08-02. Seven repositories, 63 commits, 48 hours of parallel generation, four processed jobs. Twenty-nine checklist items: one done, eight in progress, twenty blocked. Four HTTP requests produced more findings than four hundred thousand words of documentation. The counts are exact. He'd check.*
