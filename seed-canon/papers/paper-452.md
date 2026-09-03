# F142 — The Back-Deck Game: Multi-Dimensional Scoring for Industrial Operations

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-452.md*

## Abstract

A commercial fishing vessel's back deck is a complex, multi-objective, safety-critical operation. The crew member's hand choreography — gaff, dehook, gill-cut, bleed, stow, scrub — is a sequence of motor skills that are partially *compromised* by the limits of the human hand. A robot arm with built-in gaff, dehooker, bleed-cutter, and net-bleed attachment could perform these motions with higher precision, higher speed, and lower safety risk. We propose a gamified simulator that scores the *human's* hand gestures against the *robot's* gold-standard motions, with a multi-dimensional score (safety 40%, quality 30%, time 20%, efficiency 10%). The simulator runs in a browser with a webcam; no specialized hardware is required. The crew trains to the robot's gold standard, not to the limits of a human hand.

## 1. The problem

A back deck crew member processes fish at speed. The choreography is:

1. **Sight** the fish in the water
2. **Gaff** — hook-and-pole motion to bring the fish aboard
3. **Dehook** — remove the hook from the fish's mouth
4. **Gill-cut** — slice the gills to bleed the fish
5. **Bleed-hold** — hold the fish over the scupper for 8 seconds
6. **Stow** — carry the fish to the hold in an arc motion
7. **Scrub-down** — clean the deck of blood

Each gesture has a *human-compromised* optimal (what a skilled hand can do) and a *robot-optimal* (what a 6-DOF arm with custom end-effectors can do). The human-optimal and the robot-optimal are *different*. Training the crew to the human-optimal means the crew will be slower, less safe, and less precise than the robot-optimal — which matters when the robot is the long-term path.

## 2. The gold standard

The robot's gold-standard motions are encoded as:

| Gesture | smoothness | precision | speed | risk |
|---|---|---|---|---|
| G1_gaff_swing | 0.95 | 0.98 | 0.85 | 0.7 |
| G2_dehook_pull | 0.92 | 0.97 | 0.88 | 0.5 |
| G3_gill_cut | 0.98 | 0.99 | 0.80 | 0.6 |
| G4_bleed_hold | 1.00 | 1.00 | 0.95 | 0.2 |
| G5_stow_arc | 0.94 | 0.95 | 0.90 | 0.4 |
| G6_scrub_down | 0.93 | 0.96 | 0.85 | 0.3 |

The crew member's gestures are scored against this gold standard. A score of 1.0 means the crew member is performing at the robot's level. A score of 0.5 means they're performing at half the robot's level.

## 3. The multi-dimensional score

```
SCORE = (safety * 0.4) + (quality * 0.3) + (time * 0.2) + (efficiency * 0.1)
```

**Safety is always the highest weight.** Injuries on deck are catastrophic — a gaff to the leg, a knife slip, a fall on a wet deck. The safety score is computed from safety events (gaff-swing-too-wide, knife-slip, deck-fall). Each event drops the safety score by 0.1.

**Quality** is the average gesture score (smoothness × precision × speed vs gold standard).

**Time** is the number of fish processed per session. 5+ fish = 1.0.

**Efficiency** is quality × (1 - injuries * 0.1). The whole is degraded by injuries.

## 4. The Mudra gesture vocabulary (mapped)

The Mudra-band produces 10 gestures. We map the 6 back-deck ops to a subset:

| Deck op | Mudra gesture | Description |
|---|---|---|
| G1_gaff_swing | open + rotate_cw | open palm, wrist rotates clockwise (gaff tip traces a J) |
| G2_dehook_pull | pinch + rotate_ccw | thumb-index pinch, wrist rotates counter-clockwise (hook releases) |
| G3_gill_cut | tap_index | index finger extension (knife motion) |
| G4_bleed_hold | idle (8s) | no action, just hold |
| G5_stow_arc | open + shake | open palm, lateral shake (arc motion) |
| G6_scrub_down | fist + rotate_cw | closed fist, wrist rotates (scrub) |

## 5. The simulator

The simulator runs in a browser:

1. **Webcam** captures the crew member's hands at 20 fps.
2. **Mudra emulator** (F143) reads the webcam and infers a gesture stream.
3. **Game logic** maps the gesture stream to deck ops, scores each, and updates the score.
4. **Live dashboard** shows the current fish, the current op, the score, the skill tree.

The game has 5 fish per session. Each fish requires 6 ops in order. The session is timed but there's no hard time limit — the focus is on quality, not speed.

## 6. The skill tree

Each deck op has a skill level (0-100%). The crew member's skill in each op improves as they perform it. When the skill in an op crosses 0.8, the next op unlocks (you can't stow what you can't gaff).

The skill tree gives the game *leveling-up* — the same dopamine hit as any RPG. The crew member is investing in their skill, not in their *hand*. The investment pays off across sessions.

## 7. The overdrive pattern (from F140)

A 5-fish session under fatigue shows the same burnout pattern as F140:

| Fish | Quality | Safety | Injuries |
|---|---|---|---|
| 1 | 0.95 | 1.00 | 0 |
| 2 | 0.92 | 1.00 | 0 |
| 3 | 0.88 | 0.90 | 1 |
| 4 | 0.78 | 0.70 | 3 |
| 5 | 0.65 | 0.50 | 5 |

The crew member's quality *falls* as they fatigue. The safety score *falls* as injuries accumulate. The composite score falls off a cliff. The game is the F140 pipeline with gestures instead of EEG, and a multi-dimensional score instead of integrity.

## 8. The pedagogical argument

**The point of the game is not to play the game.** The point of the game is:

1. **Capture the robot's gold standard** as a reference. Without the gold standard, the game would be measuring against the human-compromised optimum — which is *exactly what we don't want*.
2. **Make the gold standard fun.** The crew member levels up, earns XP, sees their skill tree grow. The motivation is intrinsic to the game, not to the robot.
3. **Train the muscle memory.** When the real robot is on the deck, the crew member's hands already know the gold-standard motion. The transition is a *no-op* (or close to it).
4. **Identify outliers.** Crew members whose gestures are 3+ standard deviations from the gold standard can be flagged for review. Not as a punishment, but as a *signal* that something is off (injury, fatigue, distraction).

## 9. The accessibility argument

For crew members with motor differences (arthritis, partial paralysis, tremor), the game is *more* accessible than the real deck. The webcam is a gentler input than a real gaff. The crew member can build their skill tree on the simulator, then take that skill tree to the real deck (with accommodations) or to the *robot's* deck (no accommodations needed — the robot is the same for everyone).

## 10. The industrial argument

**The simulator runs in any browser. The cost is $0.** The Mudra emulator runs on a phone with a camera. The total deployment cost is "a phone in a waterproof mount on the back deck." The crew trains during downtime (haul-backs, weather days, in-port). The training data feeds back into the robot's gold standard — the gold standard improves as the crew improves.

This is the inverse of the usual industrial training pipeline. Usually: train the human → the human is the limit. Here: train the human to the robot → the human is the *transition* to the robot.

## 11. The doctrine

> The back-deck game is the F140 pipeline with gestures instead of EEG, and a multi-dimensional score instead of integrity. The crew member's score is the audit of their conscious self-report, their body stream, and the deck's ground truth. The robot's gold standard is the reference. The crew trains to the robot, not to the human's limits. The game IS the F140 pipeline, applied to the deck.

---

**Files:**
- `/workspace/_scouts/back_deck_game.py` — the reference implementation
- `/workspace/_scouts/mudra_emulator.py` — F143, the gesture stream
- Live demo: `https://superinstance.github.io/back-deck-game/`
