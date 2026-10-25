# F149 — Quilt for the Crew: A Non-Technical Handbook for the Captain and Deckhand

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-459.md*

## Abstract

The F140 negative-space pipeline, F141 Co-Captain, F142 back-deck game, F143 Mudra emulator, F144 polyformal atlas, F145 cell-router, F146 real MediaPipe, F150 Tetris audit, F151 wheelhouse game — all of these are written in technical language for engineers. But the audience for the *deployment* is the captain and crew of a working fishing vessel, who are not engineers. This paper is the *non-technical* version: a 1500-word handbook that explains, in plain words and without math, what the Quilt does on a boat, why it matters, and how it would feel in the day-to-day life of a working vessel. The handbook is the deployment substrate for F140-F151.

## 1. The problem with technical tools

The F140 pipeline, the Co-Captain, the back-deck game — these are real, working artifacts. They run. They score. They audit. They save lives. **But they don't matter if the captain and crew don't use them.**

Most technical tools fail not because the math is wrong, but because the people who would use them don't trust them, don't understand them, or don't have time for them. The captain of a working boat is not going to read a paper on FNV-1a 64-bit state hashing. The deckhand is not going to study ablation-engine residuals. They are going to do their job. They will use the tool if it makes the job easier or the boat safer. They will not use it if it requires reading a paper.

## 2. The handbook

The handbook at `/workspace/crew-handbook/index.html` is 1500 words. It has 7 sections:

1. **What this is, in plain words** — the gap between "I'm fine" and how you actually feel
2. **The three streams** — model, body, game (with a diagram)
3. **What a leak is, and why it matters** — the four kinds of leaks (focus, calm, winning, sustainability)
4. **The two games** — back-deck (for the crew) and wheelhouse (for the captain)
5. **The Co-Captain** — the digital twin with a hand-on / hands-off dial
6. **What this looks like on the boat, day to day** — a 6-month deployment plan
7. **Why this matters for safety, fish, and family** — the emotional argument

The handbook is non-technical. It uses fishing-vocabulary, not engineering-vocabulary. It uses "deckhand" and "captain" and "boat," not "user" and "agent" and "platform."

## 3. The three-stream diagram

The handbook's most important visual is the three-stream diagram:

```
   MODEL — what you say about yourself
     ⇅
   BODY — what your body is actually doing
     ⇅
   GAME — what's actually happening on the boat
```

When the streams agree, the person is in integrity. When they disagree, there's a leak. The leaks are the signal worth seeing.

## 4. The leak as a story

The handbook tells the story of the most common leak pattern: the body fails before the model admits it. A deckhand keeps saying "I'm fine" while their sweat and heart rate are climbing. By the time they admit they're tired, the safety margin is gone. The leak is the early warning.

The handbook doesn't say "F140 detected integrity 0.77." It says "your body is telling you something your mouth isn't saying."

## 5. The two games

The handbook introduces the two games in plain terms:

- **The Back-Deck Game** — practice the deck-ops against the robot's gold standard. Level up. Build the skill tree. Get ready for the real deck.
- **The Wheelhouse Game** — sail the boat. Avoid storms. Manage fuel. Catch fish. The integrity score updates in real-time. The captain's model of the boat is the most consequential lie on the vessel.

## 6. The Co-Captain

The Co-Captain is introduced as a *digital twin* with a single dial: hand-on / hands-off. When the captain is in integrity, the dial is up. When integrity falls, the dial slides down. The autopilot and the co-pilots take more of the load. The captain doesn't have to be the hero.

## 7. The day-to-day

The handbook walks through what this looks like on the boat:

- **Week 1**: phone on the back deck, no cameras, no pressure
- **Week 2-4**: camera on, real hand poses, real scores
- **Month 2**: wheelhouse gets its own phone
- **Month 3**: wearable goes on (Muse, $300)
- **Month 6**: the data is the curriculum

The deployment is gradual. Each step is reversible. The crew always has the option to opt out. The game is opt-in, not opt-out.

## 8. The bottom line

The handbook ends with the bottom line:

> The whole point of this is to make the gap between what you say and what is *visible*. When the gap is visible, you can choose. When you choose honestly, you and your crew go home. When you choose dishonestly, you don't. The tool is free. The phone is already on the boat. The choice is yours.

The tool is not a replacement for the captain or the crew. It is a *mirror* that shows the gap. The mirror saves lives.

## 9. The deployment of the handbook itself

The handbook is at `https://superinstance.github.io/quilt-crew-handbook/`. It is publicly accessible. It can be:

- Read on a phone, in a waterproof mount, on the boat
- Read in a wheelhouse, between watches
- Printed and put in the captain's quarters
- Sent to new crew as part of onboarding

The handbook is in English. It should also be in Spanish, Vietnamese, and Tagalog (the common languages on US fishing vessels). This is the next phase.

## 10. The connection to the other papers

The handbook is the *deployment substrate* for F140-F151:

| Paper | Technical | Handbook section |
|---|---|---|
| F140 | Negative-space pipeline | §2 Three streams, §3 Leaks |
| F141 | Co-Captain | §5 Co-Captain |
| F142 | Back-Deck Game | §4 Back-deck game |
| F143 | Mudra-Band Emulator | §4 Back-deck game (implied) |
| F144 | Polyformal Co-Captain | §5 Co-Captain (implied) |
| F145 | Cell-Router | §5 Co-Captain (A2A bottles) |
| F146 | Real MediaPipe Hands | §4 Back-deck game (implied) |
| F150 | Tetris Audit Game | (omitted — not the boat's game) |
| F151 | Wheelhouse Game | §4 Wheelhouse game |

The technical papers are the *math*. The handbook is the *why*. The deployment is *what* the captain and crew experience.

## 11. The doctrine

> A tool that the captain and crew don't use is a tool that doesn't exist. The handbook is the bridge from the math to the boat. The mirror is the bridge from the model to the reality. The choice is the bridge from the audit to the safety. The boat is the bridge from the technology to the family.

---

**Files:**
- `/workspace/crew-handbook/index.html` — the handbook
- Live: `https://superinstance.github.io/quilt-crew-handbook/`
