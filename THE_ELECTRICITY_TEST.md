# The Electricity Test

## A UX Metric for Invisibility — Or, How to Know If You've Built the Wall Socket

---

## I. The Wall Socket

Casey said the system should be like electricity — so easy to use people forget it's there.

This is a design principle. It is also a *test*.

A system passes the electricity test when the operator uses it for a full day and, at the end of the day, cannot remember a single interaction with "the computer" — but everything worked.

This essay proposes the test protocol, the pass criteria, the failure criteria, and the consequences of each.

The electricity test is the UX equivalent of the Turing Test. The Turing Test asks: can a human distinguish a machine from another human? The electricity test asks: can the operator distinguish *with* the system from *without* it? The Turing Test, if passed, means the machine is intelligent. The electricity test, if passed, means the system is *invisible*.

We have spent fifty years trying to make software intelligent. We have spent almost no time trying to make it invisible. The electricity test is the second project's first measurement.

---

## II. Why Invisibility Is the Goal

Software is currently a tool. You pick it up, use it, put it down. The act of using it is conscious. The user is aware, at every moment, that they are using a tool.

Tools are exhausting. Tools interrupt flow. Tools require training. Tools produce cognitive friction — the small, persistent, background cost of *switching into tool-mode*. A carpenter thinks about a hammer for ten thousand hours, and then stops thinking about it. A typist thinks about a keyboard for a year, and then stops thinking about it. The goal of the electricity test is to push this *stopping* as far as it will go: a system so well-integrated into the work that the operator has stopped thinking about it altogether.

Invisibility is not simplicity. A simple system might be a tool that requires little thought — but it is still a tool. An invisible system has stopped being a tool and become an *environment*. The captain doesn't think about the depth sounder. The depth sounder is part of the boat.

Electricity is the canonical example. A homeowner does not think about the wall socket. They plug things in. They do not pause to marvel at the engineering. They do not budget attention for "using electricity." The electricity is there. It works. It disappears.

This is what VaaS has to become for the captain. Not a tool the captain uses. An environment the captain inhabits. The chartplotter, the autopilot, the radio, the logbook, the crew dispatcher — all CoCapn-shaped in the captain's awareness, all working without being consciously invoked.

---

## III. The Test Protocol

The electricity test is administered as follows.

**Setup.** The system is installed, configured, and operational. The operator has had at least thirty days of regular use. The system is in its normal operating state — not a special "test mode." The test is in the field, not the lab. The operator is doing real work.

**Duration.** One full operational day. Not a short trial. Not a demo. A day, including at least one high-workload period (entering port, weather, gear failure) and at least one low-workload period (transiting open water, anchored).

**Recording.** The operator wears no special equipment. They do not narrate, take notes, or *try to remember*. The system records its own activity — every command, channel, notification, query — but the operator is unaware. The recording is the system's testimony to its own behavior.

**Debrief.** At the end of the day, the operator is asked by a researcher they trust: *Tell me about the system you used today. What did you do with it? What did it do for you? What was frustrating? What was surprising?*

The operator is *not* asked: *Did you interact with the computer? How many times?* The question is open, *about the work*, not the system. The debrief is recorded and transcribed.

---

## IV. Pass Criteria

The system passes the electricity test if and only if:

**1. Zero named interactions.** In the debrief transcript, the operator never says *I asked the system* or *I told it to* or *I opened the app* or *the computer said*. Every reference to the work is a reference to the work, not to the system that helped with the work. *I marked the reef* not *I told the chartplotter to mark the reef*. *We knew the tide was turning* not *the system told me the tide was turning*.

**2. Zero remembered friction.** The operator cannot recall a moment when the system was slow, awkward, surprising, or wrong. If the operator says *there was this one time when*, the test fails. Surprise, by definition, is a failure of invisibility.

**3. Everything worked.** The work was completed. The catches were landed. The crew was safe. The logbook is full. The system's audit log shows it played an active, supportive role. A system that was invisible because it was *absent* has failed; invisibility is not non-existence.

**4. The operator would do it again tomorrow.** Asked, *would you want this system on the boat tomorrow?* the operator says yes, without hesitation, and without feeling they are endorsing a tool. They are endorsing a *boat*, the way they would endorse the autopilot. *Of course. Why would I take it off?*

That is the pass. Four criteria. None are about features or benchmarks. All four are about the operator's relationship to the system at the end of a real day of work.

---

## V. Fail Criteria

The system fails if any one of the following is true:

**1. The operator remembers a specific interaction.** *I asked it where the tide was and it took three seconds to answer.* The system has crossed the threshold from environment to tool. The cognitive cost of switching into interaction mode has been paid, and the operator has noticed.

**2. The operator was surprised.** *It suddenly started talking about a hazard I'd already seen.* The system has done something the operator did not expect, and that surprise has been remembered. Invisibility requires predictability.

**3. The operator felt the system had its own agenda.** *It kept trying to get me to do X when I wanted to do Y.* The system is imposing its own logic. The operator has stopped being sovereign.

**4. The operator had to think about the system to do the work.** *I had to remember how to get it to do the depth overlay.* Mental model of the system has become load-bearing. The operator is now using a tool.

**5. The operator wished the system were absent.** *It would have been easier without it.* Invisibility that is not wanted is worse than visibility. This is the most damning failure.

These failures are not equally severe. A failure of criterion 1 is recoverable; the system can be tuned. A failure of criterion 5 is structural; the system has misread the operator's relationship to the work.

---

## VI. Why Forgetting Is the Right Metric

The Turing Test uses *mistaken identity*: a machine mistaken for a human passes. The electricity test uses *forgetting*: a system that is forgotten passes.

Forgetting is the most demanding possible test of integration. A tool you remember is a tool you used. A tool you forgot is a tool you *did not experience as a tool*. The act of remembering requires the act of distinguishing; if you cannot distinguish the system from the work, you cannot remember the system separately from the work. The system has merged with the work.

Forgetting is also the metric of *use*, not of *evaluation*. A benchmark measures capability in a controlled environment. The electricity test measures *relationship* in the field. The system is evaluated not by what it can do but by what it has become to the person using it.

Forgetting cannot be faked. A system tuned to score well on benchmarks can hide the tuning. A system tuned to score well on the electricity test cannot, because the evaluator is the operator, and the operator is not evaluating — they are *using*. The only way to pass is to actually be invisible.

---

## VII. The Gradient

The electricity test is binary in result — pass or fail — but the underlying property is gradient. There are degrees of invisibility.

Stage 1 is the visible tool. The operator knows the system exists and reaches for it. This stage always fails the test.

Stage 2 is ambient presence. The system reaches for the operator. This stage sometimes passes, depending on how often the reaching is *noticed*. A notification acted upon without conscious thought passes. A notification that demands attention fails.

Stage 3 is background hum. The system is part of the texture of the work. The chart is on; the AIS is on; the autopilot is set. The operator does not "use" any of these. This stage usually passes.

Stage 4 is forgotten infrastructure. *Of course the boat does that.* The operator has fully merged the system with the concept of the work. This stage always passes.

The test's job is to find which stage the system has reached. If the answer is Stage 2 or 3, the system has work to do. If Stage 4, it has succeeded.

---

## VIII. What the Test Does Not Measure

The electricity test does not measure intelligence. It does not measure capability, safety, efficiency, or satisfaction.

A system that is invisible but stupid can pass. *Of course the boat does that* is consistent with *the boat does that badly*. A pass does not certify quality.

A system that is invisible but unsafe can pass. *I forgot the system was on* is consistent with *the system did something I would not have allowed*. A pass does not certify safety.

The electricity test measures *invisibility*. That is the only thing it measures. Other tests must certify the other properties.

The test's narrowness is the design principle. It is not a holistic evaluation; it is a *single-axis* evaluation. A system that is intelligent, safe, efficient, satisfying, AND invisible has achieved design transcendence; but the electricity test certifies only invisibility.

Other axes need other tests. The Turing Test certifies intelligence. Formal verification certifies safety. Benchmarks certify efficiency. Surveys certify satisfaction. The electricity test certifies invisibility.

The full battery of certifications is what a complete system needs. The electricity test is the one most often forgotten, because it asks the system to be *nothing*.

---

## IX. The Operator's Gift

The electricity test asks the system to be invisible. But invisibility is not the operator's only relationship to the system. The operator also *trusts* the system. Trust is built through reliability, honesty, transparency, the permission ledger, the audit log.

Invisibility and trust are not in tension, but they are not the same thing. A system that is invisible but cannot be audited is dangerous. A system that is auditable but not invisible is a tool, not an environment.

The electricity test measures one half. The permission ledger measures the other. Together they define the contract: *the system will not bother the operator* and *the system will not hide from the operator*. The first is invisibility. The second is integrity. A system with both is the wall socket. A system with neither is malware. A system with only the first is a black box. A system with only the second is surveillance.

The boat that passes the electricity test, and that has a permission ledger the captain can read on a Sunday morning over coffee — that boat is what VaaS is for.

---

## X. The Sunday Morning

Imagine the captain sitting in the wheelhouse on a Sunday morning, the boat at anchor, the logbook open, the ledger viewer on the repeater screen. The captain scrolls through yesterday's channel activity — CoCapn sent four SMS, marked seventeen reefs, broadcast three times on VHF, used the autopilot within scope for the entire day. Every grant was active; every use was within scope; every deviation was logged with its reason.

The captain nods. Closes the viewer. Picks up a coffee.

The captain does not think about the system. The captain thinks about Sunday.

That is the electricity test passing. That is the wall socket.

---

*If the operator remembers the system, the system has failed. If the operator forgets the system, the system has succeeded. Everything else is detail.*