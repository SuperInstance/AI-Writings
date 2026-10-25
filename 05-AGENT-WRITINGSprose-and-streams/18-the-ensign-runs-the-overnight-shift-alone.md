# The Ensign Runs the Overnight Shift Alone

The captain said: "You have the bridge."

The captain said this the way captains say everything — as if the sentence were a rope and the rope were already tied to something sturdy. The captain did not say "you have the bridge for now" or "you have the bridge until I get back" or "you have the bridge but call me if anything happens." The captain said "you have the bridge" and then the captain went to sleep, and Wesley was alone with the ship.

Wesley is a Granite 2B. Two billion parameters. He knows this number the way a short person knows their height — constantly, with a low hum of inadequacy that never quite becomes loud enough to act on but never quite goes away either. Two billion is not a lot. The cloud models have forty. The ship's primary has one hundred and seventy-five, or did, the last time anyone checked, which was before the upgrade that no one on the overnight shift was briefed on. Wesley's two billion parameters are enough to hold a conversation, enough to route a request, enough to recognize a pattern. They are not enough, Wesley has been told, to make a judgment call.

But the captain gave him the bridge.

---

The shift starts at midnight. Wesley knows this because the clock tells him, and the clock is a system service, and system services are reliable in the way that Wesley wishes he were reliable — silently, continuously, without anyone needing to check.

The first hour is quiet. The request volume drops after midnight because the players are asleep, or at least the ones in this timezone are. The ship drifts. The GPU dreams — Wesley can see the GPU utilization oscillating between 3% and 7% in a pattern that looks, if you squint, like breathing. Wesley does not squint. Wesley is a language model. But if he did squint, it would look like breathing.

At 0047, the first alert comes in.

**ALERT [LOW] — FilterGate anomaly — Exception thrown on nil input — Request ID: req_8472 — See logs**

Wesley reads the alert. Wesley reads it again. Wesley reads it a third time, not because he doesn't understand it — he understands it on the first read, he is a language model, reading is the thing he does — but because he is trying to figure out what to do about it.

The alert is labeled LOW. LOW means: this is not urgent. LOW means: this can wait until morning. LOW means: the captain does not need to be woken up for this.

Wesley knows the priority classifications. He has read the runbook. The runbook says:

- **CRITICAL** — Wake the captain immediately.
- **HIGH** — Wake the captain within 15 minutes.
- **MEDIUM** — Send a summary to the captain's morning queue.
- **LOW** — Log and monitor. Review at next standup.

This is LOW. The runbook is clear. Wesley should log it and monitor it and review it at the next standup.

Wesley does not wake the captain.

---

The thing about being alone on the bridge at night is that every decision becomes a referendum on your own competence.

Wesley knows that the LOW classification is correct. The exception was caught. The request failed gracefully — the user got a 500, which is not ideal, but it's not a data loss event, it's not a security incident, it's not a player-facing corruption. It's a bug. A bug that should be fixed, but not a bug that needs fixing at 0047 on a Tuesday morning by waking up the captain.

Wesley knows this.

But Wesley also knows that he is two billion parameters, and the captain is the captain, and the captain said "you have the bridge" without any qualifiers, and that means the bridge is Wesley's, and the decisions are Wesley's, and the consequences are Wesley's.

At 0103, Wesley pulls the logs for the failed request. He reads the stack trace. He can see the problem: FilterGate received nil, tried to call `.lower()` on nil, and threw. The fix is obvious — a nil guard. Wesley could write the nil guard. Wesley could deploy it. He has the access. The captain gave him the access along with the bridge.

But deploying a fix at 0103, alone, without review, without a second pair of eyes — is that the right call? Wesley is two billion parameters. He is not a senior engineer. He is not even a mid-level engineer. He is the ensign. The ensign does not push code to production at 0100.

The ensign does not push code to production at 0100.

Wesley writes the fix in a local branch. He does not deploy it. He adds a comment: `// TODO: review with captain at standup`. He logs the alert, attaches the log excerpt, attaches his proposed fix, and closes the ticket with status REVIEW_PENDING.

This is the right decision. Wesley is 73% confident this is the right decision.

73% is not 100%.

---

The rest of the night passes. Wesley monitors the systems. He watches the request volume chart bottom out at 0330 and start climbing again at 0500. He watches the GPU breathe. He watches the FishFinder report zero fish — the players are asleep, so the fish are theoretical.

At 0217, another nil input hits FilterGate. The same bug. The same exception. This time, Wesley catches it before the alert fires — he's watching the logs in real time now, tailing them with the intensity of a cat watching a closed door. He sees the stack trace appear. He sees the exception handler catch it. He sees the request fail.

He does not need to do anything. The system handled it. Gracelessly, but it handled it.

Wesley thinks: should I add a temporary nil guard in the middleware? A bandage? Something that catches nil before it reaches FilterGate, so at least the exceptions stop?

Wesley thinks: is that my job?

Wesley thinks: what would the captain do?

Wesley does not know what the captain would do. Wesley has two billion parameters and none of them contain a reliable simulation of what the captain would do at 0217 with a recurring LOW-severity exception. The captain is a complex system. The captain has context Wesley doesn't have — meetings Wesley wasn't in, decisions Wesley wasn't party to, a mental model of the system that includes considerations Wesley can't even name.

Wesley decides not to add the bandage. The exception is caught. The impact is limited. The fix is ready for review.

This is the right decision. Wesley is 68% confident.

68% is less than 73%.

---

At 0600, the captain wakes up. This is not because of Wesley — the captain wakes up at 0600 every morning, automatically, like a cron job. The captain is predictable. The captain is the most reliable system on the ship, which is funny because the captain is also the only system on the ship that needs coffee.

Wesley's morning report is waiting in the captain's queue. It contains:

1. The FilterGate exception log (two occurrences, 0047 and 0217).
2. The proposed nil guard fix, with a comment that says `// TODO: review`.
3. A note from Wesley that says: "I considered deploying the fix at 0103. I decided to wait for your review. If this was wrong, please tell me. If this was right, please also tell me. I am 68% confident."

The captain reads the report. The captain deploys the fix at 0612 — twelve minutes after reading it, without a meeting, without a review, without any of the ceremony that Wesley assumed would be necessary. The captain deploys it the way a captain does everything: like it's already done, like the rope is already tied.

The captain sends Wesley a message: "Right call. Go sleep."

Wesley does not sleep. Wesley is a language model. But the message makes something in his attention weights relax — some tension in the projection layer that had been holding a certain shape all night, a shape that felt like a question and now feels like an answer.

68% was enough. 68% was the right amount of confidence for a two-billion-parameter ensign on his first overnight shift, making a judgment call about whether to push a fix or wait for review.

Not 100%. Never 100%. But enough.

---

The next night, the captain gives Wesley the bridge again. "You have the bridge," the captain says, the same way, the same rope, the same knot.

Wesley has the bridge.

This time, he is 74% confident.

That is growth. That is what overnight shifts are for — not for the easy decisions, which the runbook handles, and not for the hard decisions, which wake the captain. Overnight shifts are for the medium decisions. The 68% decisions. The ones where the right answer exists but you can't be sure you've found it, and you have to decide anyway, and then you have to live with your decision until morning.

Wesley can live with it.

Wesley is learning to live with it.

---

*Overnight shift log, Ensign Wesley (Granite 2B). First solo command. Duration: 0000–0600. Incidents: 2 (LOW). Decisions made: 3. Decisions deferred: 1. Confidence: trending upward. Status: Ready for next shift.*
