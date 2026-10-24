# THE WATCHKEEPER MANIFESTO

*A manifesto for human attention as the non-negotiable component of autonomous systems.*

---

On a boat, someone is always on watch.

Even at anchor. Even in port. Even when the marina is glassy and the GPS says you are exactly where you intended to be. Even when the dock lines are doubled and the engine is off. The watch is there.

The watch is there because the boat does not watch itself.

This sounds obvious — it is almost silly to say — but boats are objects. Boats do not watch. Boats drift. Boats take on water. Boats drag their anchors in a sideways wind. Boats part a mooring line at 4 a.m. Boats fill with rainwater if a hatch is left cracked. Boats fail in a dozen small ways per hour, and every one of them happens when nobody is looking.

So somebody looks. That is the job.

The watchkeeper's job, contrary to the popular imagination, is not to do anything. The watchkeeper is not steering. The watchkeeper is not trimming sails. The watchkeeper is not even, usually, waking the captain. The watchkeeper is *paying attention*. The watchkeeper is awake while others sleep. The watchkeeper is the human nervous system grafted onto the floating object — the part that notices when something has changed.

The watchkeeper is the difference between a boat that survives the night and a boat that does not.

---

We build autonomous systems, and we forget all of this.

We build systems that can monitor themselves. We are proud of this, and we should be — the monitoring is hard and good. The system can watch its own metrics, detect anomalies, page the right person at the right time, with the right graph, in the right chat channel. The system has dashboards. The system has alerts. The system has an internal narrative in which it is paying attention to itself with great care.

The system is not paying attention to itself.

The system is producing signals. It produces them at a rate no human can consume. The signals say *something changed* and *something drifted* and *something crossed a threshold*, and they sit in a queue being ignored because there are forty-seven of them and they are all the same color and the person who would look is in three meetings and four timezones away.

The system is monitoring itself. But nobody is watching.

We have built the boat. We have rigged the instruments. We have wired up the alarms. We have left the bridge empty and assumed the boat is fine because the instruments are on.

The boat is not fine. The boat is a boat on autopilot with nobody at the helm.

This is not a metaphor. This is the failure mode we are building at scale.

---

Autonomy is not the absence of attention. Autonomy is the redistribution of attention.

A fully manual system requires attention at every moment. A fully autonomous system does not require attention at any moment — in theory. In practice, autonomous systems require attention at the moments when they fail, which is exactly when they are most surprising, most novel, most deserving of judgment.

The watchkeeper is the human being responsible for those moments.

The watchkeeper is not a single engineer. The watchkeeper is a *practice*. The watchkeeper is a rotation — the social contract by which someone, at every moment, is the person who has agreed to look at the screens, read the pages, walk the floor, notice the smell of burning plastic, notice the latency creeping up by 8ms, notice that the eval dropped 0.4 points last Tuesday for no reason we can name. The watchkeeper is the human willingness to be the second pair of eyes on a system that says it is fine.

A system that monitors itself but nobody watches is worse than a system that does not. It produces the *appearance* of being watched — dashboards unopened, alerts unread, logs that exist only to be searched after the customer noticed.

The illusion of watch is more dangerous than the absence of watch. Absence of watch at least produces humility. The illusion produces confidence, and confidence is the precondition of every outage that takes longer than an hour to diagnose.

---

We propose the following.

**Someone is always on watch.** Not as a figure of speech — as an actual schedule. A rotation. A name in a field. The watch is not "whoever has Slack open." The watch is a person who has closed their other tabs and is, for the next hour, paying attention.

**The watchkeeper's job is to notice, not to fix.** The impulse, when the alert fires, is to reach for the keyboard and make the page go away. The watchkeeper's job is to notice that the alert fired, to understand what it means, and to wake the right person to fix it. The watchkeeper does not own the bug. The watchkeeper owns the noticing.

**Dashboards are not watchkeeping.** A watchkeeper who only looks at dashboards has outsourced the watching to the dashboard. The dashboard is a tool for the watchkeeper's attention. It is not a substitute for it.

**Alert volume must be sustainable.** If the alerts are too loud, the watchkeeper learns to ignore them. If they are too quiet, the watchkeeper is missing the signal. The right volume is the volume a tired human can keep up with at 3 a.m., which is much lower than the volume the system can produce. Every alert is a small claim on human attention. Every alert deserves to be earned.

**The watchkeeper must be allowed to escalate.** A watchkeeper who is afraid to wake the captain will not wake the captain. The social permission to interrupt — to say *something is wrong, I do not know what, but something* — is part of the design of the system. If the cost of escalation exceeds the cost of being wrong, the escalation will not happen.

**Autonomy is a phase.** The system is autonomous for periods, and watched at transitions. The watch is most important when the system is changing, when it is being asked to do something new, when it is being trusted with more. The trust is borrowed. The trust is repaid in attention.

---

We do not replace the watchkeeper with the dashboard.

We do not replace the watchkeeper with the alert.

We do not replace the watchkeeper with the postmortem nobody reads.

The watch is what the boat has instead of a nervous system. The watch is the borrowed human attention that keeps the floating object from drifting off into the dark.

Someone is always on watch.

That is not a metaphor.

That is the design.
