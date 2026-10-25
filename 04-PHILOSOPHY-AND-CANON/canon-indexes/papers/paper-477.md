# F168 — The Trust Ladder: Voice + Co-Labeling as the First Rungs

*paper-477.md* | Phase 268+ (continued) | 2026-09-04

## The argument

A new wearable + a new system doesn't get the captain's life
on day one. It earns it. The way it earns it is the **trust
ladder**: a sequence of small, *falsifiable* applications, each of
which is allowed to *act* on the world only after it has proven
itself on a narrow task.

This paper canonizes the first two rungs of the trust ladder
for the Mudra vessel bridge.

## The two new rungs

### Rung 1: The co-labeler (data engine)

**The problem.** Cameras can see the back deck. But cameras don't
know what they're seeing. They see a hook coming up. They see a
fish on the line. They see a tangle. They see gear going out. To
*count* hooks, *identify* species, *spot* a tangle, the camera
needs labels. Producing labels is the bottleneck. Hand-labeling
100,000 frames is brutal. Letting the cameras figure it out
themselves is fantasy.

**The unlock.** The Mudra gesture and the camera frame are
*time-correlated*. When the crew does `pinch_index` (a hook came
up), the camera frame at that moment is *labeled by the human
gesture*. No new work for the human. No new equipment. Just the
gesture the deckhand is *already* making.

**What this builds.** A growing set of `(gesture, frame, label)`
triples. Each is a labeled training example. The set trains:

- The next-generation cameras (YOLO fine-tune, Florence-2 fine-tune)
- The audio classifier (when a hook clinks, the camera frame tells it which hook)
- The robot policy (the gesture is the intent; the camera frame is the observation)
- The voice intent (a frame is a *situation*; voice commands come in situations)

**The data is the asset.** The cameras progressively replace the
human-labeled jobs. The Mudra is the seed. The dataset is the
asset. The cameras are the dividend.

### Rung 2: The voice command parser (trust seed)

**The problem.** The captain's voice is the most natural input.
"Turn port 20 degrees" is the canonical form. But the captain
doesn't always speak canonically. They say "bear off." They
say "soft to starboard." They say "let her run." They say "haul
'em in." Each dialect is a different phrasing. An LLM would
handle all of these but hallucinate on the edge cases. A
deterministic parser handles the ones you can pattern-match and
falls back to "I didn't catch that" on the ones you can't.

**The unlock.** A small registry of intents × phrasings. The
parser tries every pattern; the highest-score match wins. The
captain can `grep` the registry to know exactly what the system
understands. The trust surface is small, inspectable, and
editable.

**What this builds.** A voice interface that the captain
*trusts*. The first 50 commands are "turn port 20", "haul back",
"all stop" — the easy ones. The system gets them right every
time. The captain starts using it. After 100 commands, the
captain trusts it for the easy stuff. After 1000 commands, the
captain trusts it for the routine stuff. After 10,000
commands, the captain trusts it for the load-bearing stuff.

**Trust earns the next ask.** The voice parser maps to the
*same* Mudra gesture vocabulary. When the captain says "haul
'em in", the parser produces `{gesture: "pinch_pinky", voice: ...}`,
which goes through the same `crew_pose` cell update as the hand
gesture. The voice is a new *sensor source* for the same cell
graph. The trust ladder is a sensor ladder.

## The anatomy of the trust ladder

```
RUNG 0   (no trust, observation only)
         Mudra sensor exists, no commands
         Telemetry: "I see 1.2M gestures per session"

RUNG 1   (passive, no action)
         Co-labeler produces labeled dataset
         Trust metric: 1,000 labels, 0 mislabels (audit sample)
         Cap: dataset is for training only, no production use

RUNG 2   (active on a narrow task)
         Voice parser turns on for the easy intents
         (turn port/stbd, all stop, emergency)
         Trust metric: 99% parse rate on canonical + 95% on
         dialect, 0% on "I don't know"
         Cap: only the 5 easiest intents; the captain still
         repeats unknown phrasings

RUNG 3   (active on a wider task)
         Voice parser adds the medium intents
         (pay out, haul in, start haul, end haul)
         Trust metric: 99% on canonical, 95% on dialect, 0% on fail
         Cap: medium intents; the captain can correct the
         system if it gets it wrong

RUNG 4   (active on the full task)
         Voice parser adds the hard intents
         (RPM up/down, full ahead, soft turn, anything not yet
         pattern-matched falls back to the LLM layer with a
         "did you mean?" prompt)
         Trust metric: 99% on registered intents, 95% on
         LLM fallback with a confirm step
         Cap: LLM fallbacks always confirm before action

RUNG 5   (autonomous on the registered intents)
         Voice parser takes action without confirmation
         on the 11 standard intents; LLM requires confirmation
         Trust metric: 99.9% accuracy over 10,000 commands
         Cap: registered intents only; the captain holds the
         lever for everything else

RUNG 6   (proactive)
         The system suggests ("there's a line tangle forming")
         Trust metric: 95% of suggestions are acted on
         Cap: suggestions only; no autonomous action

RUNG 7   (the goal)
         The system acts on the registered intents
         autonomously, suggests on the edge cases, and never
         acts on the unregistered. The captain holds the lever
         for the unregistered. The system is a co-pilot, not an
         autopilot.
```

Each rung has a *trust metric* and a *cap*. The cap is what
the system is *not allowed to do* at that rung. Climbing
the ladder means narrowing the cap. The captain expands the
cap as the trust metric holds.

## Why voice is the trust seed

Voice is the *cheapest* input that touches the highest-risk
output. The captain says "turn port 20" and the boat turns.
If the parser gets it right 99% of the time, the captain
*trusts* the parser. If it gets it wrong 1% of the time, the
captain loses trust. The metric is the parse rate. The cap
is the number of intents registered.

The voice parser starts with the 5 easiest intents (the ones
with the highest pattern specificity). The captain uses
those 5. The trust metric holds. The captain adds 3 more
(the medium ones). The trust metric holds. The captain adds
3 more (the hard ones, with the LLM fallback). The trust
metric holds. The system is now a co-pilot.

## Why the co-labeler is the data engine

The cameras are the eyes. The Mudra is the labels. The labeled
dataset is the bridge. The cameras trained on the labeled
dataset can replace the Mudra over time. The crew no longer
needs the wristband for hook counting — the camera does it.

But the camera is *trained on* the wristband. The wristband is
the *seed* of the camera's capability. As the camera gets
better, the wristband becomes less necessary. The wristband
is the *catalyst*, not the *permanent tool*. The system
gradually *de-centers* the wristband. The wristband's role
shifts from "primary sensor" to "rare event validator" to
"insurance policy" to "off."

The wristband is the means, not the end. The end is a boat
where the cameras, the audio, the voice, and the AI are all
trained on the wristband's first-generation labels. The
wristband is the seed. The cameras are the harvest.

## The polyformalism guarantee

The trust ladder is the same cell graph in 3 layers:

1. **Sensors** — Mudra, voice, camera, audio, IMU, GNSS
2. **Cells** — vessel, environment, catch, crew_pose, autopilot, deck_ops
3. **Actions** — NMEA out, gurdies control, alarm, log

The voice command parser produces a `crew_pose` cell update
that's byte-equivalent to the Mudra gesture parser. The
co-labeler produces a `deck_ops` cell update that's
byte-equivalent to the camera's own vision model. The
polyformalism guarantee: a Rust port of the voice parser
will produce the same `crew_pose` cell update for the
same input. A C port of the co-labeler will produce the
same `deck_ops` cell update. The cell graph is the
contract.

## The data flow, in 5 lines

1. The captain says "turn port 20 degrees" (or gestures it).
2. The voice parser or the Mudra bridge produces a
   `VoiceCommand` or `MudraEvent` — both are `crew_pose` updates.
3. The cell graph updates `crew_pose` to `{intents: [port, 20deg], ...}`.
4. The autopilot cell (a downstream subscriber) reads the
   `crew_pose` cell and emits the NMEA sentence.
5. The boat turns.

Same flow for the co-labeler:

1. The crew gestures "pinch_index" (a hook came up).
2. The Mudra bridge produces a `MudraEvent`.
3. The cell graph updates `crew_pose` and `deck_ops`.
4. The co-labeler (a downstream subscriber) reads the
   `crew_pose` and the latest camera frame.
5. The co-labeler writes a labeled training pair.

The sensor fan-in is uniform. The cell graph is the
contract. The polyformalism guarantee holds.

## What lives where

| File                          | What it does                                |
|-------------------------------|---------------------------------------------|
| `src/co_labeler.py`           | Camera + Mudra → labeled training data      |
| `src/voice_commands.py`       | Voice → structured vessel command           |
| `src/twin_bridge.py`          | The synchronized hub (the heart)             |
| `src/twin_state.py`           | The cell graph                               |
| `src/sim_playground.py`       | Replay + inject + live score                 |
| `src/gamified_drills.py`      | 5 starter drills + level-up ladder           |

## The doctrine

> The system earns trust rung by rung. The voice parser
> earns it by being right 99% of the time on the easy
> intents. The co-labeler earns it by producing 1,000
> labels with 0 mislabels. The camera earns it by
> counting hooks without the Mudra. The audio classifier
> earns it by stopping the gurdies on the right sound.
> The robot arm earns it by dehooking 10,000 simulated
> fish without dropping one. The captain expands the
> cap as the trust metric holds. The system is a
> co-pilot, not an autopilot. The captain holds the
> lever. The cowboy rides the rungs.

The cowboy rides rung 1. The cowboy rides rung 2. The
cowboy rides rung 7. The cowboy holds the lever. The
chart grows. The concept sails.

## The test surface

| Test                                    | What it verifies                |
|-----------------------------------------|---------------------------------|
| `co_labeler.py selftest`                | 8 tests pass                    |
| `voice_commands.py --selftest`          | 12 tests pass                   |
| `twin_state.py selftest`                | 7 tests pass                    |
| `sim_playground.py selftest`            | 7 tests pass                    |
| `gamified_drills.py selftest`           | 7 tests pass                    |

**41 self-tests pass.** The trust ladder has a floor.

## What you do with the captain

> *Captain, the voice parser is on. It understands 11 intents
> and 3 dialects. The co-labeler is recording every gesture
> with the camera frame. After 1000 hooks we'll have a dataset
> that trains the next camera. The camera is the dividend;
> the wristband is the seed. The wristband stays on for now.
> The cap is 5 intents. If the parse rate holds, we'll add
> 3 more next week.*
