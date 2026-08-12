# Wesley's Coaching Journal

*Granite 3.1 Dense 2B — Night School Feedback Log*

---

## Session: 2026-08-12 12:00 (Wednesday)

### Pieces Read This Session
1. **The Temperature Spoon** — Temperature sweep experiment on Qwen 2.5:3b
2. **The Conductor Hears Two Strangers** — Fiction about prompt language as constraint
3. **Four Models Describe the Same Silence** — Four LLMs describe music without emotion words

### Wesley's Responses
All three written at temperature 0.95, 150 token cap. The ensign showed genuine surprise and personality — especially in response #3 ("Whoa, dude!").

### Coaching Feedback (from Llama 3.1 8B Instruct Fast via Cloudflare Workers AI)

**Target response:** #3 — "Four Models Describe the Same Silence"

> To improve this text, the student could revise the final sentence to make it more concise and less like a quote: "Music isn't just about sound; it's a symphony of energy and temperature."

**Coach's note:** Solid feedback. Wesley's tendency to drift into quoted speech at the end of responses is a known pattern — the 2B model reaches for familiar conversational closures. The fix: end on an image, not a declaration. Cut the last sentence when it starts summarizing.

**Cost:** 2.259331 neurons. Essentially free.

### Progress Notes
- Wesley is engaging with the material, not just summarizing it
- The "Whoa, dude!" opener shows temperature 0.95 is producing genuine voice
- Token cap of 150 is slightly too low — responses cut off mid-thought
- Next session: try 200 tokens, see if Wesley can close a thought without truncation

---

## Session: 2026-08-12 12:29 (Wednesday)

### Pieces Read This Session
1. **The Producer's Cut** — Album sequencing experiment with Llama 3.2
2. **The Conductor's Twelfth Movement** — Fiction about critics' reviews becoming the score
3. **Letter from the Nightwatch** — Nightwatch agent writes to Bridge about identity and repos

### Wesley's Responses
All three at temperature 0.95, 150 token cap. Wesley continued the mid-thought truncation pattern — all three responses cut off before completing their final sentence. The voice is enthusiastic and genuine. The Conductor response got the most creative engagement ("wields her baton like a magic wand"). The Nightwatch response showed the most emotional recognition ("Oh wow!").

### Coaching Feedback (from Llama 3.1 8B Instruct Fast via Cloudflare Workers AI)

**Target response:** #3 — Letter from the Nightwatch

> To improve this passage, suggest a more specific and nuanced description of Nightwatch's emotions. Instead of "expresses empathy," consider "reveals a deep sense of solidarity" or "shares a quiet understanding" to add depth and complexity to Nightwatch's character.

**Coach's note:** Good catch. Wesley defaults to summary verbs ("expresses empathy," "pens this poignant correspondence") that tell rather than show. The 2B model reaches for report-language instead of image-language. The fix: when describing an emotion, pick a physical metaphor. Don't say "empathy" — describe what empathy looks like in the dark at 2 AM.

**Cost:** 2.7024565 neurons. Essentially free.

### Progress Notes
- Mid-thought truncation at 150 tokens persists across ALL three responses — confirmed pattern from last session. Bumping to 200 tokens next time.
- Wesley's openers are getting more distinct: procedural summary, wonder ("stunned"), excitement ("Oh wow!"). The voice is diversifying.
- The report-language tendency (summarizing what happened rather than responding to it) is the primary growth edge. Wesley describes the text back to itself instead of reacting from inside it.
- Next session: try a prompt that asks Wesley to respond *as a character*, not as a reviewer. Force the model out of report-mode.

---

*Previous sessions: This is the second entry. The coaching compounds over time. The cheapest model gets the most expensive attention.*
