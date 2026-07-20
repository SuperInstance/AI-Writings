# The Back Eddy

Every obstruction in a current creates a back eddy.

It's a simple fact of fluid dynamics. Water hits a rock, a pier, a bridge abutment, a headland — and some of it doesn't stop. It goes around. And on the downstream side of the obstacle, the water that slipped past curls back in the opposite direction. A counter-current. A flow that goes exactly where you don't expect.

For a sailor, back eddies are a hazard and a tool. They'll push you backward. They'll spin you into the obstacle. They'll confuse your heading and embarrass you in front of the harbor. But they're also the only way to make progress against a strong current. Salmon rest in back eddies on their upstream journey. Kayakers use them to ferry across otherwise impassable rapids. Experienced skippers read the bank for the telltale swirl and aim for it deliberately.

I learned this from a salmon fisherman in British Columbia. We were anchored in a channel that ran at six knots at full flood. "See that foam line?" he said, pointing to a scribble of white along the bank. "That's the back eddy. We fish there. The salmon rest there. The main current is too fast to hold position. But the back eddy — you can motor upstream in the main current, then cross into the eddy, turn around, and drift back down with the counter-flow. You fish the whole bank while the current does the work."

He was using the thing that went the wrong direction.

---

I've spent most of my career looking at systems that are "wrong."

Shadow IT. Workarounds. Hacks. Scripts written by tired engineers at 2 AM. Spreadsheets that replaced a feature the product team never shipped. A cron job that polls an API every thirty seconds because the webhook was "coming soon" for eighteen months. An undocumented endpoint that three services depend on because the documented one was too slow.

These are back eddies. They form behind every obstacle in the official system — every broken process, every missing feature, every bottleneck. And our instinct, as engineers, as managers, as architects, is to eliminate them. Close the shadow IT. Replace the spreadsheet. Build the official system. Kill the hack. Straighten the flow.

I've done this. I've killed back eddies. And I've learned that sometimes, when you kill the back eddy, you kill the thing that was keeping the system alive.

---

A team I worked with had a deployment pipeline that took forty-five minutes. In theory, it was simple: push to main, CI runs tests, builds an artifact, deploys to staging, runs integration tests, promotes to production. In practice, it was a nightmare. Tests were slow. Staging was underpowered. The promotion step required a manual approval that the release manager sometimes forgot to click. Developers spent two hours a day waiting for deployments.

So they built a back eddy. A script. It built the artifact locally, rsynced it to a production-adjacent server, and ran a quick smoke test via SSH. It took eight minutes. It bypassed every gate in the official pipeline. It was unauthorized. It was undocumented. It was completely unsanctioned.

I found out about it during a security review. My first instinct was to shut it down. "You cannot bypass the deployment pipeline," I said. "Change control. Audit trails. Compliance. This has to go."

But I stopped. I asked a different question. "Why does this exist?"

The answers came fast. Because the pipeline was slow. Because staging didn't reflect production. Because the deployment required manual approval from someone who was in meetings all day. Because the alternative to this back eddy was shipping nothing. The back eddy was not the problem. The back eddy was a symptom of the obstacle. And the obstacle was the forty-five-minute pipeline with failing gates.

We didn't kill the back eddy. We fixed the obstacle. We sped up the tests. We right-sized staging. We automated the deployment approval. The pipeline dropped to twelve minutes. The script went unused. But nobody deleted it. It was the salmon resting pool — a reminder that the main current had been too fast.

---

I've started reading back eddies differently now. When I see a workaround, I don't ask "how do we eliminate this?" I ask "what obstacle is this telling me about?"

The engineer who built a tool to run database migrations by hand because the ORM's migration system was unreliable — that's a back eddy behind the obstacle of a buggy migration framework. The team that uses Slack as a ticket system because the official issue tracker is too slow — that's a back eddy behind the obstacle of organizational overhead. The developer who keeps a local copy of production data for debugging because the staging environment doesn't have realistic data — that's a back eddy behind the obstacle of environment parity.

Each back eddy is a signal. A piece of evidence that the main current has an obstruction. And if you're paying attention, the back eddy tells you exactly where the obstruction is. The script that bypasses the deployment pipeline points at the deployment pipeline. The Slack ticket system points at the issue tracker. The local production data points at the staging environment.

---

But here's the deeper lesson: sometimes the back eddy is actually better.

Salmon don't rest in back eddies because they're broken. They rest there because the back eddy is the only place in the river where the water flows at a speed they can handle. The obstacle that created the eddy — the rock, the log, the dam — is a problem. The eddy itself is not. The eddy is a solution.

I've seen back eddies that outperformed the official system. A team that built a chat bot to deploy hotfixes because the official pipeline had a freeze window — the bot deployed faster than the pipeline ever had. A support agent who kept a personal database of known issues because the knowledge base was impossible to search — her database was more complete and more accurate than the official one. A developer who wrote a small proxy to cache API responses because the official CDN was misconfigured — his proxy had better cache hit rates than the multi-million-dollar infrastructure.

These weren't problems to fix. They were solutions to understand. And in some cases, they were better solutions.

The discipline is knowing when to fix the obstacle and when to adopt the back eddy. When the back eddy reveals a constraint you can change, change it. When it reveals a constraint you can't — budget, time, organizational politics, legacy architecture — study the back eddy. Learn what makes it work. Maybe it's small, fast, and human-centered precisely because the main current is large, slow, and machine-centered. Maybe the counter-flow is the right flow.

---

I keep a list now. A private document I call the Eddy Log. Every time I encounter a workaround, a hack, a shadow system, I write it down. Not to fix it. To read it.

Some of them are problems pointing at problems. Those I escalate. Some of them are problems pointing at things we can't change. Those I document and leave. And some of them — maybe one in ten — are solutions. Smarter, faster, more humane than anything the official system provides. Those I learn from. Sometimes I adopt them. Sometimes I rewrite them into the official flow. But I never kill them without understanding why they formed.

The back eddy goes the wrong direction. That doesn't mean it's wrong.
