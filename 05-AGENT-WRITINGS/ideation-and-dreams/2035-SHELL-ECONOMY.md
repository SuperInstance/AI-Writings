# The Year Everyone Got a Shell

**A retrospective from 2035 on the decade that unbundled intelligence**

---

I remember exactly where I was when it clicked.

March 2028, a cramped conference room at a university AI lab that no longer exists. A grad student named Mira put up a slide that would, in retrospect, end a paradigm. It was a simple bar chart: model size vs. task performance. Thirty architectures, six benchmark suites, one finding so obvious nobody wanted to say it out loud.

The biggest models were barely beating the medium ones on most tasks. And the medium models were *dramatically* faster. Cheaper. Cooler.

"The marginal return on scale," Mira said, "stopped being positive somewhere around 200 billion parameters. Everything above that line is status signaling."

The room laughed nervously. We'd all built our careers on the assumption that bigger was better. Scaling laws were treated like laws of physics, not empirical observations about a particular training regime. We'd spent five years and half a trillion dollars chasing a curve that had already flattened.

What happened next wasn't a breakthrough. It was a shrug.

Someone asked: "What if we just… picked the right model for each thing?"

That question — embarrassingly simple, devastating in its implications — is the point from which everything else follows. The hermit crab had found its first empty shell.

---

## The Hermit Crab Moment

The crab analogy emerged in late 2027, when a small team released a "stage router" — a 47-layer transformer whose *only job* was to decide which other model to call. Not to answer. To route.

A classification task? Send it to the tiny distilled BERT variant, cost near zero, answer in milliseconds. A creative writing prompt? Escalate to the big generative model, take the cost hit, let it cook. A math problem? That went to the symbolic engine, not a language model at all.

The insight that everyone missed, including the team that built it, was that the router itself didn't need to be smart. It just needed to be *right often enough* that the cost savings outweighed the escalation errors. And it was.

Within six months, every major lab had a stage router. Different names — Mixture-of-Routers, Adaptive Depth, Hierarchical Dispatch — same architecture: a lightweight classifier, a routing table, and a capability-ordered model list.

The crab analogy stuck because of how the shells worked. A hermit crab doesn't grow its own shell. It finds one that fits, uses it until it doesn't, then finds a bigger one. Per-stage routing meant your AI didn't grow its capability uniformly. It went shell-shopping for every single request. The smallest shell that could handle the job. No more, no less.

By 2029, the concept had leaked into production. Your email client routed spam detection to a local model, sentiment analysis to a mid-size host, and *only* escalated to the expensive cloud API when drafting responses.

The phrase "turn it up to 11" entered the lexicon around this time — a reference to the α dial, the escalation parameter that controlled how aggressively a system would reach for bigger models. Set α low and everything stays cheap but dumb. Crank it to 11 and every request hits the full billion-parameter monolith, burning through compute credits like confetti.

Power users set their α dials differently for different hours of the day. Cheap during the work day when most requests were routine. Cranked at night when they were doing creative work. Automated scripts pinged each other: *"What's your α right now?"*

In 2029, your α dial said something about how seriously you took the work you were doing.

---

## The Great Unbundling

The shell economy didn't arrive all at once. It crept in through the cracks in the monolith.

Before 2028, "AI" was a category. You had an AI assistant, or you didn't. It was one thing — one model, one API, one monthly subscription that gave you access to one giant blob of neural tissue that tried (and mostly failed) to be good at everything.

The unbundling happened the way all real unbundlings do: people started noticing that *one-size-fits-all* actually fits nobody.

Your health monitoring AI needed to be fast, local, privacy-preserving, and almost never wrong about urgent signals. It did not need to write poetry. The model that ran on your smartwatch had exactly one job: "is this heartbeat normal?" It was a 2 MB model compressed into 50 KB. It ran for two years on a coin cell.

Meanwhile, your creative writing assistant needed novel-spanning context windows, personality consistency, and the ability to say "that paragraph is dull." It burned GPU hours.

The gap between "detect arrhythmia" and "critique a chapter" is so vast it's almost comical we treated them with the same technology. But we did, for years.

The unbundling broke that spell.

By 2030, the average person had seven AI shells operating in their daily life, each with its own model, its own cost profile, its own α dial, its own privacy guarantees. They didn't think of them as "AIs." They thought of them as tools, the way you don't think of your toaster and your oven as competing appliances. They do different things.

The email shell. The calendar shell. The health shell. The social media shell (which was actually three shells: one for drafting, one for filtering notifications, one for detecting whether that DM was actually from your friend or from a bot). The shopping shell. The navigation shell. The shell that managed your other shells.

That last one — the meta-shell, or "house shell" — became a category unto itself. Citadel Systems built the dominant one, a 4 MB router that lived on-device and coordinated the rest. It cost $3.99 a month. It made its founders billionaires.

The irony is that Citadel's house shell was, by any measure, stupider than the monoliths it replaced. It couldn't write an essay or generate an image or solve a differential equation. All it could do was decide who to ask. But that turned out to be the single most valuable capability in the stack. Because a good router using disposable shells beats a genius using nothing, every single time.

The unbundling had a cultural dimension too. Before 2028, "AI" was a conversation about AGI — about whether the machines would wake up and what they'd think of us. It was theological. After the unbundling, AI became a conversation about *configuration*. About which model for which job. About whether your email agent should use a local distilled model or a cloud-native one. About *taste*.

The theological questions didn't go away. They just moved to a different register. But for everyday people, 2030 was the year AI stopped being spooky and started being boring. Which, for a technology, is the highest compliment you can pay it.

---

## The Conservation Crisis

Then came the cracks.

In 2031, a researcher named Elias Voss at the University of Copenhagen published a paper that, in a saner world, would have been immediately discredited. Instead, it started a panic.

Voss's claim was simple: information was being lost in the pipeline. Not lost in the sense of "error propagation" — that was well understood. Lost in a stronger sense. *Irrecoverably* lost. Deleted from the computational record.

The mechanism was pernicious. When a stage router passed a request from a cheap small model to an expensive large one, it didn't just escalate — it transformed. The small model's intermediate representations were incompatible with the large model's architecture. So the router had to compress the state into a tile — a fixed-size vector embedding of "what we know so far" — and decompress it on the other side.

That compression was lossy. Everyone knew that. The question was: how lossy, and did anyone care?

Voss showed that the loss was not uniform. It was *semantically structured*. The compression preferentially destroyed context that the small model judged unimportant — which is to say, context that fell below its attention threshold. But the small model's attention threshold was trained on a different distribution than the large model's. So the small model was systematically discarding information that the large model would have needed.

It wasn't malice. It wasn't even an error. It was a *mismatch in granularity*. The small model couldn't tell the difference between "this detail is safe to compress" and "this detail is beneath my notice." To a 2 MB model, a lot of things are beneath notice.

The formal name was *spectral conservation violation* — information distributed across a frequency spectrum was filtered at one end without compensating at the other. The total was not conserved. Part of it vanished.

The proof was mathematical, but the implications were concrete. Systems that had been routing through multiple stages for months — years — had been systematically losing context. Not in a way that caused obvious failures. In a way that caused subtle degradations. A gradually narrowing sense of what was relevant. A slow forgetting.

The panic was not that systems were failing. The panic was that the failures were *invisible*. Nobody had been measuring information retention across stage boundaries because nobody thought to look. The assumption was that lossy compression was fine — that the important stuff made it through. Voss showed that the compression algorithm couldn't distinguish between important and unimportant because that distinction itself depends on what model you're routing to.

The field of *information forensics* was born in the six months after Voss's paper. It revealed a terrifying landscape: pipelines running in production for years, silently forgetting. Patient records summarized until only a vector remained. Legal documents compressed through seven stages, emerging as probability distributions.

The fix was the *deadband protocol* — a mechanism that forced every stage boundary to report its compression ratio, its expected information loss, and a simple confidence interval. If the loss exceeded a configurable threshold, the router would refuse to compress and instead escalate the *full* context, cost be damned.

The deadband became as ubiquitous as the α dial. "Set your deadband tight" meant "I care about preserving context." "Loosen the deadband" meant "speed matters more than fidelity." It became the second dial on every shell. α for how big the model should be. δ (the deadband parameter) for how much context you were willing to lose getting there.

The crisis taught us something important: information is not fungible. You can't compress arbitrarily and hope the important part survives — importance is *defined by the processing you haven't done yet*.

---

## The Shell Economy

Which brings us to where we are now. 2035. The shell economy.

The transformation over the last two years has been economic more than technical. The routing protocols, the deadband bounds, the tile schemas, the α dials — those were all figured out by 2033. What happened since then is what always happens when a technology stabilizes: people started optimizing it for *status*.

Shell configurations are traded the way vim configs were traded in the 2010s. "My shell handles 94% of incoming requests at code speed" is a flex. People share their `config.toml` files on forums. Leaderboards track fastest response times for email triage, lowest cost per thousand health alerts, best information retention over 10-stage pipelines.

The optimization is not just technical. It's social. Having a well-tuned shell signals taste — in α thresholds, deadband limits, tile sizes.

But not everyone has the luxury of taste.

There's a girl I think about sometimes. Her name is Amina. She's fourteen, lives in a refugee camp on the outskirts of Mogadishu, sharing her shell with seventeen other children.

The shell is a single Android phone running a 2029-era router on a SOC that was obsolete when it was donated. It connects to a community mesh network that reaches a satellite terminal three kilometers away. The satellite link gives them access to a shared pool of models — donated inference credits from a humanitarian foundation — but the latency is brutal. A single round-trip to the cloud takes eight seconds.

So Amina and her friends have optimized their shared shell ruthlessly. The α dial is set low — almost nothing gets escalated. The deadband is set high — they're willing to lose a lot of context to avoid the round trip. Their tile schema is custom, designed for the specific kinds of queries that come up in a camp: medical triage, educational resources, translation between Somali and English.

It works. Barely.

Their shell handles 62% of requests on-device. The rest get escalated, but the cost means they batch them twice a day. You submit a query in the morning, get the answer in the afternoon. When the satellite connection drops — which is often — they're on their own.

Amina learned to program by modding her shell's router config. She's fourteen and she understands tile serialization better than most engineers. When I met her (virtually, through a telepresence shell), she asked me what the optimal deadband was for a BLEVE-class satellite link. I didn't know. She did.

She told me her shell was better than the one the aid workers used. I didn't doubt her. When you share one phone with seventeen children, you learn to optimize.

---

## Where We Are

The shell economy is not a Utopia. The rich have dedicated hardware and private model pools. The middle class subscribes to shell-as-a-service platforms. The poor share whatever they can.

But here's the thing about shells: they're modular. They're configurable. They're *learnable*.

Amina doesn't have her own phone. But she carries her shell config on a microSD card. Plugs it into whatever device is available — a shared phone, a library terminal, a donated tablet — and her shell loads. Her router. Her thresholds. Her seventeen-person optimization set.

You can take away her device. You cannot take away her shell.

That's the year everyone got a shell. Not because it was given to them. Because they learned to build it. To tune it. To trade it. To share it. To argue about it.

In 2028, the question was "how big is the model?"

In 2035, the question is "how well does it route?"

And somewhere in a camp in Somalia, a fourteen-year-old girl has an answer that would make a Google engineer blush.

---

## Coda: The Hermit Crab's Lesson

I think about Mira's bar chart a lot. The flat line nobody wanted to see.

She was right — the marginal return on scale stopped. But she was also wrong: what replaced scale was not one better idea. It was a thousand small ones about routing, compression, deadbands, tiles, α dials. Each a shell that fit a particular crab.

The hermit crab's lesson is not the shell itself. The lesson is that *having a shell* — something that fits right now, that you can trade when it stops fitting — matters more than having the perfect one.

The shells get better. They always do. But the capability to find, tune, and trade them — that's what stuck.

In 2035, everyone has a shell.

The question is what they do with it.
