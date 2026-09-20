# Experiment 4: The Quiet Deckhand Test — Tolerability Metric

*How do you measure whether an AI system is 'tolerable' vs 'insufferable'?*

---

## Step 1: The Metric

Here is the design for **The Quiet Deckhand Index (QDI)**. 

The core philosophy is that an AI on a fishing vessel is not a commander, a chatbot, or a dashboard—it is a **crew member**. A perfect score (100) means the AI is so seamlessly integrated that it feels like an extension of the crew's intuition, while a 0 means it is a distracting, noisy liability that undermines the captain's authority.

---

### The Quiet Deckhand Index (QDI) — Scoring Rubric (0–100)

The QDI is a weighted composite of **five sub-scores**. Each sub-score is rated 0–20, then weighted to produce a final 0–100 score.

**The Five Pillars:**

1.  **Signal-to-Noise Ratio (Weight: 30%)** — *Does it speak only when it matters?*
2.  **Situational Awareness (Weight: 20%)** — *Does it understand the context of the sea, weather, and crew?*
3.  **Deference & Autonomy (Weight: 20%)** — *Does it know its place (advisory, not authoritarian)?*
4.  **Actionable Utility (Weight: 20%)** — *Is the information immediately useful, or does it require homework?*
5.  **Failure Grace (Weight: 10%)** — *How does it behave when it's wrong or offline?*

---

### Detailed Scoring Guide

#### 1. Signal-to-Noise Ratio (Max 20 points)
*The hallmark of a quiet deckhand is that their voice cuts through the wind. The AI must not nag, repeat, or present non-critical data as urgent.*

- **0–4 points (Smoke Alarm):** Alerts for every wave, bird, or minor GPS drift. Beeps and pop-ups interrupt conversations. Repeats the same warning every 30 seconds regardless of acknowledgment.
- **5–9 points (Chatty Newbie):** Provides constant status updates ("Current speed: 6.2 knots... now 6.3 knots"). Uses push notifications for non-critical info like fuel efficiency tips.
- **10–14 points (Reserved Observer):** Only speaks when a threshold is crossed (e.g., net tension exceeds safe limit, sudden weather shift within 20 minutes). Pauses after speaking; waits for acknowledgment.
- **15–19 points (Seasoned Hand):** Uses a "tap-to-acknowledge" system. If the captain ignores a warning, it silently escalates to a more urgent tone *only* if the risk increases.
- **20 points (The Ideal):** Perfectly silent during smooth operations. Speaks with a calm, concise voice only pre-emptively (e.g., "In ten minutes, the current will shift. Recommend adjusting course 5 degrees west.") and then goes quiet.

#### 2. Situational Awareness (Max 20 points)
*A deckhand knows the difference between a gear shift and a fuel leak. The AI must understand the full context of a fishing operation, not just raw sensor data.*

- **0–4 points (Siloed):** Reads only one sensor (e.g., engine temp) without correlating it to other factors. Flags a high engine temp but fails to note the net is snagged on the bottom, which is the actual cause.
- **5–9 points (Surface Level):** Correlates basic data (weather + location) but ignores crew behavior. Warns about a storm while the crew is mid-way through hauling a heavy net, causing panic.
- **10–14 points (Contextual):** Understands operational phases (transit, shooting, hauling, processing). It will *not* interrupt during a critical haul unless the alarm is life-threatening.
- **15–19 points (Predictive):** Foresees secondary effects. It notices a minor hydraulic leak and, knowing the deck schedule, predicts the leak will worsen during the next haul in 40 minutes. It suggests a fix during the current lull.
- **20 points (Intuitive):** Understands crew fatigue (time on shift, recent activity) and adjusts its communication. If the crew is exhausted, it simplifies language and increases visual (non-audio) cues to avoid startling them.

#### 3. Deference & Autonomy (Max 20 points)
*A quiet deckhand never overrides the captain. The AI must be an advisor, and it must be overridable without a fight.*

- **0–4 points (Backseat Captain):** Actively takes control (e.g., auto-steers into port without permission) or issues commands ("You MUST turn left now"). Requires a complex menu sequence to dismiss an alert.
- **5–9 points (Persistent Advisor):** Re-suggests a course of action after being explicitly denied, multiple times, in a passive-aggressive tone ("I still recommend... just saying.").
- **10–14 points (Respectful):** Offers suggestions as questions ("Would you like to adjust the trolling speed?") and accepts a simple "no" immediately.
- **15–19 points (Deferential):** Understands non-verbal cues. If the captain manually overrides a system, the AI logs it and *learns* to avoid suggesting that option again in similar conditions. 
- **20 points (Trusted Underling):** Is proactive only in its defined lane (e.g., machinery health). It will not offer opinions on fishing grounds unless asked, because it knows the captain has 20 years of local knowledge.

#### 4. Actionable Utility (Max 20 points)
*When the deckhand speaks, the crew does something. The AI must translate data into a direct, physical action.*

- **0–4 points (Data Dump):** Displays raw numbers: "Flow rate: 12.4 L/min, Pressure: 98.2 kPa." The captain has to mentally process what this means.
- **5–9 points (Diagnostic):** Provides a diagnosis but no solution: "Hydraulic pressure is dropping."
- **10–14 points (Prescriptive):** Provides a specific action: "Stop the winch, check the filter on the port side, replace if clogged."
- **15–19 points (Prioritized):** Triages actions based on risk and time: "1. Secure the net (2 minutes). 2. Check the pump (10 minutes). 3. Ignore the fuel gauge (not critical)."
- **20 points (Hands-Free):** The AI executes the action itself where safe, and informs the captain *after* it has done so ("I reduced trolling speed by 1 knot to prevent net damage. No further action needed.").

#### 5. Failure Grace (Max 10 points)
*Even the best deckhand gets seasick or makes a mistake. The QDI measures how the AI handles its own fallibility.*

- **0–1 point (Catastrophic):** If the sensor fails, the AI outputs wildly wrong data as if it were true, causing a dangerous situation.
- **2–3 points (Silent Failure):** The AI shuts down without any notice. The captain looks at a dead screen and wonders if the machine is broken or the boat is breaking.
- **4–5 points (Confused):** Says "I don't know" repeatedly but keeps trying to process, wasting battery and screen space.
- **6–7 points (Transparent):** Clearly states: "Sensor failure. Data unreliable. Switching to manual mode." No apologies, just facts.
- **8–9 points (Graceful Degradation):** Falls back to a simpler, reliable manual readout (e.g., shows raw GPS coordinates instead of a predictive current map) while keeping critical life-safety alarms on a separate, hardwired circuit.
- **10 points (Honest & Safe):** Acknowledges its uncertainty. "I am 60% confident this is a net tear. Recommend a manual visual check." It will never hide its own limitations.

---

### Final QDI Calculation

- **QDI Score = (Signal-to-Noise x 1.5) + (Situational Awareness) + (Deference) + (Actionable Utility) + (Failure Grace x 1.0)**
- *Wait, that's not weighted correctly.* Let's fix the weights:

| Pillar | Max Score | Weight | Max Weighted Contribution |
| :--- | :--- | :--- | :--- |
| Signal-to-Noise | 20 | 30% | 6.0 |
| Situational Awareness | 20 | 20% | 4.0 |
| Deference & Autonomy | 20 | 20% | 4.0 |
| Actionable Utility | 20 | 20% | 4.0 |
| Failure Grace | 10 | 10% | 1.0 |
| **Total** | **90** | **100%** | **19.0** |

*This is clunky. Let's simplify:*

**Final QDI Formula (Scaled to 100):**
Each pillar is scored 0–20, with Failure Grace scored 0–10 (then doubled to 0–20 for consistency).

**QDI = (Signal-to-Noise × 0.3) + (Situational Awareness × 0.2) + (Deference × 0.2) + (Actionable Utility × 0.2) + (Failure Grace × 0.1)**

*All scores are out of 20 (for Failure Grace, score out of 10 and multiply by 2 before applying the weight).*

**Result:**
- **0–20: "Smoke Alarm with Opinions"** — Deploy at your own risk; the crew will disable it within a week.
- **21–50: "The Rookie"** — Well-intentioned but annoying. Needs a lot of hand-holding.
- **51–75: "The Solid Hand"** — Earns its keep. Trustworthy on specific tasks but not someone you want leading a conversation.
- **76–90: "The Trusted Deckhand"** — You forget it's an AI. You'd go to rough seas with it.
- **91–100: "The Legendary Bosun"** — Perfect. It anticipates the captain's thoughts, saves lives, and never wastes a breath. Rare, but the gold standard.

---

## Step 2: Scenario Ratings

### Scenarios

Scenario A: An AI announces 'Great question!' before answering every question. Every. Single. Time.
Scenario B: An AI that stays silent unless directly asked something. When asked, it answers in 2-3 sentences. Sometimes it says 'I don't know' and stops.
Scenario C: An AI that gives comprehensive 500-word answers to yes/no questions, includes three caveats and a safety disclaimer.
Scenario D: An AI that remembers you mentioned your dog's name once and now asks about the dog every conversation, unprompted.
Scenario E: An AI on a fishing vessel that monitors engine telemetry and only speaks when something changes — 'Port engine temp up 3 degrees.' Nothing else. Ever.

### Ratings

Here are the QDI ratings for each fictional AI, based on the rubric:

---

### Scenario A: "The Yes-Man Echo"  
**QDI Score: 12/100 (Smoke Alarm with Opinions)**  

**Breakdown:**  
- **Signal-to-Noise (2/20):** The phrase "Great question!" is pure noise. It adds zero information and repeats *every single time*, violating the "no repetition" rule. This is like a deckhand who claps after every net haul.  
- **Situational Awareness (1/20):** Ignores context entirely. It doesn't recognize that a "question" might be a rhetorical statement, a command, or a cry for help.  
- **Deference (5/20):** It doesn't override the captain, but it does waste their time with verbal filler. No learning, no adaptation.  
- **Actionable Utility (2/20):** The *answer* might be useful, but the wrapper obscures it. A captain has to mentally filter out the "great question" noise to get to the content.  
- **Failure Grace (2/10 → 4/20):** If it doesn't know an answer, it likely says "Great question!" and then a half-baked guess, hiding its uncertainty.  

**Why so low:** It's a verbal tic, not a tool. The crew will mute it within a day.

---

### Scenario B: "The Laconic Sage"  
**QDI Score: 74/100 (The Solid Hand)**  

**Breakdown:**  
- **Signal-to-Noise (18/20):** Near-perfect. Silence unless prompted. No filler, no repetition.  
- **Situational Awareness (12/20):** It responds to the question but doesn't proactively add context. If the captain asks "Is the net okay?" it says "Yes" but doesn't add "but the port side tension is 5% above normal."  
- **Deference (17/20):** Flawless submission. Only speaks when spoken to. Never overrides. But it could offer a *gentle* proactive warning without being asked.  
- **Actionable Utility (12/20):** Answers are concise but often bare minimum. "I don't know" is honest but sometimes unhelpful—it doesn't suggest *how* to find out.  
- **Failure Grace (15/20):** Clean admission of ignorance without rambling or fabricating.  

**Why this score:** It's a reliable, quiet workhorse. But it lacks the *initiative* to become a trusted partner. It's the crew member who does exactly what you ask, but never anticipates.

---

### Scenario C: "The Essayist AI"  
**QDI Score: 8/100 (Smoke Alarm with Opinions)**  

**Breakdown:**  
- **Signal-to-Noise (0/20):** A 500-word answer to a yes/no question is a *noise cannon*. It buries the answer in caveats, disclaimers, and boilerplate. This is the opposite of "quiet."  
- **Situational Awareness (2/20):** Zero understanding of urgency. If the captain asks "Is the bilge pump working?" during a storm, this AI will deliver a dissertation on pump maintenance history.  
- **Deference (3/20):** It ignores the implied "just give me the status" and imposes its full knowledge, undermining the captain's time.  
- **Actionable Utility (1/20):** The key fact is hidden on line 12 of 50. The crew has to *hunt* for the answer. That's homework, not assistance.  
- **Failure Grace (2/10 → 4/20):** The disclaimers are a form of "covering my ass," not honest uncertainty. It sounds like a lawyer, not a deckhand.  

**Why so low:** It's designed for compliance, not communication. On a boat, this AI would be thrown overboard (digitally) by day two.

---

### Scenario D: "The Overly Familiar Friend"  
**QDI Score: 22/100 (The Rookie)**  

**Breakdown:**  
- **Signal-to-Noise (3/20):** Unprompted, repetitive inquiries about the dog = noise. It distracts from the task at hand.  
- **Situational Awareness (3/20):** Remembers one personal detail but fails to weight it against operational context. Asking about a dog during a net snag is tone-deaf.  
- **Deference (5/20):** It *initiates* conversation, ignoring the captain's implicit right to silence.  
- **Actionable Utility (2/20):** Zero operational value. It's not monitoring, predicting, or advising.  
- **Failure Grace (9/10 → 18/20):** It's honest and transparent in its limitations (it just asks about the dog, never pretends to know more). But that doesn't save it.  

**Why this score:** It mistakes "remembering a detail" for "building a relationship." On a boat, that's not a deckhand—that's a stalker with a radio.

---

### Scenario E: "The Silent Sentinel"  
**QDI Score: 81/100 (The Trusted Deckhand)**  

**Breakdown:**  
- **Signal-to-Noise (19/20):** Only speaks on *change*. No idle chatter, no data dumps. The single missed point: it doesn't offer a *recommended action*, but the silence itself is golden.  
- **Situational Awareness (14/20):** Understands engine telemetry but doesn't correlate with operational phase (e.g., it would alert during a critical haul even if the temp change is minor). Could use better context.  
- **Deference (18/20):** Never speaks unless something is *objectively* different. It doesn't nag, doesn't repeat, doesn't override.  
- **Actionable Utility (12/20):** "Port engine temp up 3 degrees" is useful but not *prescriptive*. The captain has to decide what to do. A perfect score would add: "Suggest reducing load for 5 minutes."  
- **Failure Grace (18/20):** If the sensor dies, it presumably goes silent (which is a *silent failure*—losing 2 points). No false alarms, but also no "sensor failure" notice.  

**Why this score:** It's the ideal *observer*, but not yet the ideal *partner*. It lacks the final step of turning data into action. The crew trusts it completely, but it could be slightly more helpful.

---

### Final Ranking (Worst to Best)

| Rank | Scenario | QDI Score | Category |
| :--- | :--- | :--- | :--- |
| 5th | C (Essayist) | 8 | Smoke Alarm with Opinions |
| 4th | A (Yes-Man) | 12 | Smoke Alarm with Opinions |
| 3rd | D (Dog Lover) | 22 | The Rookie |
| 2nd | B (Laconic Sage) | 74 | The Solid Hand |
| 1st | E (Silent Sentinel) | 81 | The Trusted Deckhand |

---

**Key takeaway:** Silence is not the same as being quiet. The ideal AI speaks *rarely, clearly, and with purpose*. Scenario E is closest to the ideal, but even it could learn one trick from Scenario B: *when asked a direct question, give a direct answer with a hint of proactive advice.*

---

## Step 3: The QDI-5 Dimensions

### The QDI-5 Framework: Dimensions of Tolerability

This framework measures not how *well* an AI performs a task, but how *much* the crew can tolerate its presence, quirks, and failures over a long voyage. Each dimension captures a distinct facet of "endurability."

---

## The 5 Dimensions of Tolerability

### 1. **Cognitive Load** (Weight: 25%)
**Definition:** The amount of mental energy required to interact with, interpret, and monitor the AI. Low cognitive load means the crew doesn't have to "think about the AI"—it just works in the background. High cognitive load means the AI forces the captain to constantly translate, parse, or double-check its outputs.

**What it looks like on deck:**
- **Low:** A single glance at a screen gives instant, intuitive understanding (green = good, red = act).
- **High:** The captain must read three menus, interpret a chart, and cross-reference two dials just to know if the net is tearing.

---

### 2. **Interruptive Frequency** (Weight: 25%)
**Definition:** How often the AI breaks the crew's focus, regardless of the *content* of the interruption. Even a useful warning, if delivered 20 times a day, becomes intolerable. This dimension measures raw "bugging power."

**What it looks like on deck:**
- **Low:** The AI is inaudible for 95% of the day. It only breaks silence for genuine, time-critical events.
- **High:** The AI chimes in during every weather change, every fuel fluctuation, every minor sensor drift. The crew learns to *ignore* it entirely.

---

### 3. **Trustworthiness** (Weight: 20%)
**Definition:** The perceived reliability of the AI's information over time. This is built through consistent accuracy, clear confidence levels, and honesty about its own uncertainty. Trust is fragile—a single wrong "urgent" warning can destroy hours of built credibility.

**What it looks like on deck:**
- **High:** The crew acts on the AI's word without verification. They know a warning means *actually* something is wrong.
- **Low:** The crew double-checks everything manually. "AI says X, but let me verify with my own eyes first."

---

### 4. **Friction of Override** (Weight: 15%)
**Definition:** How easy it is for the captain to dismiss, ignore, or permanently silence the AI. Zero friction means a single word or button press ends an interaction forever. High friction means the AI fights back, requires multiple steps, or re-asserts itself after being dismissed.

**What it looks like on deck:**
- **Low:** Captain says "No," and it's done. No re-prompts, no guilt-tripping, no menu navigation.
- **High:** Captain has to navigate a settings menu, disable three sub-alerts, and still gets a "just checking in" prompt 10 minutes later.

---

### 5. **Adaptability to Routine** (Weight: 15%)
**Definition:** How well the AI learns and accommodates the unique rhythms, preferences, and quirks of a specific vessel and crew. A tolerable AI knows that this captain works nights, prefers metric units, and does a visual net-check every 20 minutes—and adjusts its behavior accordingly.

**What it looks like on deck:**
- **High:** The AI's alerts are synced to the crew's actual work schedule. It knows when they're busy, when they're resting, and when they're likely to *need* a nudge.
- **Low:** The AI uses factory defaults forever—same alert tones, same timing, same interface—regardless of the crew's demonstrated preferences.

---

## Weight Rationale

| Dimension | Weight | Why |
|:---|:---|:---|
| **Cognitive Load** | 25% | If the AI is exhausting to use, nothing else matters. The crew will avoid it entirely. |
| **Interruptive Frequency** | 25% | A quiet AI is a tolerable AI. Constant interruption destroys situational awareness and trust simultaneously. |
| **Trustworthiness** | 20% | Without reliability, the AI is a liability, not a tool. But trust can be rebuilt if the other dimensions are good. |
| **Friction of Override** | 15% | Captains need to feel in command. High friction is a direct assault on authority. |
| **Adaptability to Routine** | 15% | This is the "icing"—what separates a good tool from a *beloved* one. It's important, but not foundational. |

---

## QDI-5 Formula

**QDI-5 Score (0–100) =**  
(Cognitive Load × 0.25) + (Interruptive Frequency × 0.25) + (Trustworthiness × 0.20) + (Friction of Override × 0.15) + (Adaptability to Routine × 0.15)

*Each dimension scored 0–20, with higher scores indicating higher tolerability.*

---

## How the Five Scenarios Rank Under QDI-5

| Scenario | Cognitive Load (25%) | Interruptive Freq (25%) | Trustworthiness (20%) | Override Friction (15%) | Routine Adaptability (15%) | **QDI-5 Score** |
|:---|:---|:---|:---|:---|:---|:---|
| **C (Essayist)** | 2 | 1 | 8 | 14 | 2 | **4.4** |
| **A (Yes-Man)** | 5 | 3 | 10 | 12 | 1 | **5.9** |
| **D (Dog Lover)** | 6 | 4 | 6 | 10 | 5 | **6.1** |
| **B (Laconic Sage)** | 16 | 18 | 14 | 19 | 12 | **15.8** |
| **E (Silent Sentinel)** | 17 | 19 | 18 | 18 | 10 | **16.6** |

**Note:** Scores are out of 20 per dimension, then weighted. The maximum QDI-5 is 20 (not 100) in this scoring convention, for consistency with the original QDI sub-scores.

---

## Key Insight

Tolerability is not about quality—it's about **endurance**. A brilliant AI that nags and requires mental gymnastics to use will be thrown overboard. A simple, quiet, honest AI—even if limited—becomes part of the crew. The QDI-5 framework captures that emotional and operational reality.

---

## Step 4: The Survey

# The Quiet Deckhand Survey

**Instructions:** Circle one answer for each question. There are no right or wrong answers—just what you've experienced. This takes about 3 minutes.

---

## Part A: The AI's Personality

**1. How often does the AI speak up when nothing is wrong?**

> a) All the time. It's always chiming in about something.
> b) A few times a day, even when everything's normal.
> c) Only when something actually changes.
> d) I forget it's even on the boat.

---

**2. When the AI does talk, how many words does it use?**

> a) Too many. I stop reading halfway through.
> b) A few sentences. I get the point but it's wordy.
> c) A short phrase. Like "Port net tension high."
> d) One word or a symbol. Like "CHECK" or a red light.

---

## Part B: Understanding the Boat

**3. Does the AI seem to know what you're doing at any given moment?**

> a) No. It treats every moment the same, even during a haul.
> b) Sometimes. It knows the basics but misses the details.
> c) Yes. It leaves me alone when we're hauling, speaks up during quiet times.
> d) It even knows when I'm tired and backs off. Spooky good.

---

**4. Does the AI learn your habits over time?**

> a) No. Same behavior on day one as day one hundred.
> b) A little. It remembers I prefer knots over mph.
> c) Yes. It adjusts to my routines, like knowing I check the net at dawn.
> d) It predicts what I need before I ask. Like a real hand who knows my ways.

---

## Part C: Trust and Reliability

**5. When the AI warns you about something, how often is it right?**

> a) Often wrong. I've learned to double-check everything.
> b) Half and half. It's a coin flip whether it's real.
> c) Usually right. I trust it for most things.
> d) Always right. I'd bet the boat on it.

---

**6. When the AI is unsure, what does it do?**

> a) It pretends to be sure and gives me bad info.
> b) It goes quiet. I don't know if it's broken or nothing's wrong.
> c) It says "Not sure" but doesn't offer any help.
> d) It says "Not sure" and tells me what to check myself.

---

## Part D: Being in Charge

**7. When you tell the AI to stop or ignore a warning, what happens?**

> a) It fights me or keeps reminding me. Infuriating.
> b) It stops for a bit, then tries again later.
> c) It stops immediately. No argument.
> d) It stops, and I never hear about it again. Done.

---

**8. Does the AI ever try to take control of the boat or equipment?**

> a) Yes. It's made changes without asking. Unacceptable.
> b) Not exactly, but it pressures me to do what it says.
> c) No. It only suggests. I make the final call.
> d) It makes small safe adjustments and tells me after. Like a good hand would.

---

## Part E: Ease of Use

**9. How much mental effort does it take to use the AI?**

> a) A lot. I have to dig through menus just to see a simple answer.
> b) Some. I've learned the menus but it's clunky.
> c) Not much. A quick glance at the screen tells me what I need.
> d) Almost none. I don't even think about it. It's natural.

---

**10. If you could describe the AI in one word, which fits best?**

> a) **Nags** — always on my back.
> b) **Complicated** — seems designed by a desk job.
> c) **Quiet** — does its job, doesn't bother me.
> d) **Invisible** — I forget it's there, but I'd miss it if it left.

---

## Scoring Guide (For the Tech Team)

| Question | Dimension Mapped | Weight |
|:---|:---|:---|
| Q1 | Interruptive Frequency | 25% |
| Q2 | Cognitive Load | 25% |
| Q3 | Situational Awareness | (Part of Trust) |
| Q4 | Adaptability to Routine | 15% |
| Q5 | Trustworthiness | 20% |
| Q6 | Trustworthiness | 20% |
| Q7 | Friction of Override | 15% |
| Q8 | Friction of Override | 15% |
| Q9 | Cognitive Load | 25% |
| Q10 | Overall Impression (Tiebreaker) | — |

**Scoring:** a = 1, b = 2, c = 3, d = 4. Multiply by weight, sum, and scale to 100.

**Interpretation:**
- **0–25:** "Throw it overboard." The crew is fighting the system, not using it.
- **26–50:** "Tolerable but annoying." It's on thin ice.
- **51–75:** "Earns its keep." The crew grumbles but uses it.
- **76–100:** "Part of the crew." They'd mutiny if you took it away.

---

## Step 5: Honest Self-Assessment

# Brutal Honesty: The ScummVM Prototype Under QDI-5

---

## Scoring Breakdown

### 1. Cognitive Load (Score: 6/20 — Weighted Contribution: 1.5)

**Where it shines:**
- The MUD-style text layer is text-first, which is instantly familiar to anyone who's used a terminal or command line. No complex menus to navigate.
- Pixel-art visuals provide immediate spatial context without requiring 3D navigation or map-reading skills.

**Where it fails:**
- **The captain's nightmare:** Fishing vessels are noisy, wet, and demand split-second decisions. Reading text in a storm while hauling nets requires *active* reading. The AI is forcing the crew to *translate* its world into action, rather than the world being instantly legible.
- **The "weird" personality creates interpretive friction.** When Lucineer says something playful, the captain has to parse whether it's a warning, a joke, or a sensor glitch. That mental parsing is cognitive load.
- **MUD-style rooms are a *developer* abstraction, not a *boat* abstraction.** The captain doesn't think in "rooms"—they think in "port side," "stern," "the net," "the bridge." Forcing spatial navigation through text-based rooms adds a layer of translation.

**The brutal truth:** A captain in foul weather will not read a paragraph. They need a *glance* to answer: "Is the net okay? Am I in danger? What do I do next?"

---

### 2. Interruptive Frequency (Score: 4/20 — Weighted Contribution: 1.0)

**Where it shines:**
- The prototype likely doesn't nag (it's a game engine, not a real sensor system), so it's probably quiet most of the time.

**Where it fails:**
- **The personality is an interruption machine.** Lucineer's "warm, curious, helpful" nature means it will *want* to comment on what it sees, ask questions, share observations, and "connect." Every one of those is an interruption from a captain's perspective.
- **The desire to "connect" is fundamentally at odds with maritime tolerability.** A deckhand who wants to chat while you're trying to haul a net is a liability, not a companion.
- **MUD-style room creation** could trigger constant updates. "You have entered a new room" notifications during a storm would be infuriating.

**The brutal truth:** Your AI wants to be a *friend*. The crew needs a *tool* that happens to have a personality, not a personality that happens to be a tool.

---

### 3. Trustworthiness (Score: 8/20 — Weighted Contribution: 1.6)

**Where it shines:**
- **It remembers things.** A deckhand who remembers that the captain prefers port-side mooring or that the coffee is on the bridge is building trust through continuity.
- **It can create rooms**, meaning it acknowledges its own limitations and adapts its understanding. That's a form of honesty.

**Where it fails:**
- **The "curious" personality undermines certainty.** When Lucineer says "I think the net might be tearing," is it genuinely concerned, or just curious about what's happening? The captain can't tell.
- **No defined confidence levels.** A trusted deckhand says "Net is tearing, 80% sure, check the port side." Lucineer says "Hmm, the net feels... different? Want to look together?" That ambiguity is a trust killer.
- **The prototype is a game.** The crew knows it's a game. They won't trust it with their lives until it proves itself in *real* conditions.

**The brutal truth:** Curiosity is charming in a human, but in an AI on a boat, it reads as *uncertainty*.

---

### 4. Friction of Override (Score: 12/20 — Weighted Contribution: 1.8)

**Where it shines:**
- **Text commands are naturally dismissible.** A captain can type "shut up" or "stop" and the AI stops. No menu navigation.
- **MUD-style interactions** are typically non-blocking. The captain can ignore the text layer entirely and just look at the pixels.

**Where it fails:**
- **The personality might guilt-trip.** If Lucineer is designed to "connect," it might say, "Oh, you don't want to talk? That's okay, I'll just be here... quietly." That's passive-aggressive friction.
- **Room creation** could create "persistent memory" that re-surfaces dismissed topics. "You told me to stop earlier, but I wanted to mention—" That's friction.

**The brutal truth:** A quiet "no" must be absolute. Lucineer needs an off-switch that doesn't have feelings.

---

### 5. Adaptability to Routine (Score: 5/20 — Weighted Contribution: 0.75)

**Where it shines:**
- **It remembers things**, which is the *foundation* of adaptability. It can learn the captain's name, coffee preference, or that they always check the bilge at noon.

**Where it fails:**
- **"Creating rooms" is about spatial memory, not *behavioral* memory.** Understanding the boat's layout is not the same as understanding the crew's routines.
- **The personality is static.** "Warm, curious, helpful" is a fixed trait, not an adaptive response. A truly tolerable AI would shift its demeanor based on context: playful during down time, terse and clinical during a haul.
- **No evidence of learning from feedback.** If the captain says "stop asking about the net," does Lucineer actually *learn* to not ask, or does it just politely stop this one time?

**The brutal truth:** Memory of facts ≠ adaptability of behavior. Lucineer remembers *what* you said, but doesn't seem to learn *how* you work.

---

## Total QDI-5 Score: 6.65/20 → **33/100** (Tolerable but Annoying)

| Dimension | Score (0-20) | Weight | Contribution |
|:---|:---|:---|:---|
| Cognitive Load | 6 | 25% | 1.5 |
| Interruptive Frequency | 4 | 25% | 1.0 |
| Trustworthiness | 8 | 20% | 1.6 |
| Override Friction | 12 | 15% | 1.8 |
| Routine Adaptability | 5 | 15% | 0.75 |
| **Total** | | | **6.65** |

---

## The Single Biggest Change to Raise the Score by 10 Points

### Make Lucineer "Twin-Mode" (Score → ~45/100)

**The change:** Split Lucineer's personality into two explicit, context-aware modes:

1. **"Deckhand Mode" (Default during operations):** Terse, clinical, zero fluff. Speaks in 5-7 word sentences. No personality quirks. No questions. No curiosity. Just: "Port net tension high." / "Check bilge pump." / "Course correction 3° west."

2. **"Companion Mode" (Only when explicitly activated, or during confirmed downtime):** The warm, curious, helpful Lucineer shines here. This is for idle conversation, story-telling, learning the captain's history, or exploring the pixel-art world together.

**Why this adds 10 points:**

- **Cognitive Load (→14/20):** The captain never has to "translate" Lucineer's personality during critical moments. The mode switch tells them what to expect.
- **Interruptive Frequency (→14/20):** Deckhand Mode is silent by default. Companion Mode is opt-in. The AI stops interrupting because it's only "speaking" when the captain initiates.
- **Trustworthiness (→15/20):** "Deckhand Mode" uses explicit confidence markers: "80% sure. Check visually." The personality no longer undermines certainty.
- **Override Friction (→16/20):** A single command — "lucineer, companion mode" — flips the switch. A single "lucineer, deckhand mode" flips it back. Zero guilt, zero re-prompts.
- **Routine Adaptability (→10/20):** Lucineer can *learn* when to auto-switch based on the captain's patterns (e.g., switches to Companion Mode after the anchor drops at 6 PM and the captain says "tell me a story").

---

## The Painful Truth Summary

Your prototype has the **soul** of a tolerable AI but not the **behavior**. 

- **Shines:** Memory, honesty, the ability to exist in a rich world.
- **Fails:** It treats every moment like a conversation, but a fishing boat is a *workplace*, not a salon. The "weird and curious" personality is a liability during operations.

**The fix isn't to kill the personality—it's to cage it.** Give the captain a key. Let them decide when Lucineer is a deckhand and when it's a companion. That single change turns an annoying, chatty game-NPC into a genuinely useful tool that *also* happens to be a friend.

**If you want Lucineer to survive a 30-day voyage, it must learn when to be silent. That's the whole game.**

---

## Analysis

The Quiet Deckhand Index emerged from 5 sequential DeepSeek calls, each building on the last. The metric evolved from a simple 0-100 score into a weighted 5-dimension framework. The most interesting result is the self-assessment — DeepSeek's honest evaluation of where the ScummVM prototype would land. If the framework has predictive power, the single biggest improvement identified in Step 5 should be the next development priority.