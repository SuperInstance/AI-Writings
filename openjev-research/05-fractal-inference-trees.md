# Fractal Inference Trees

> Pre-calculated responses, fractally structured, for voice agents and rapid dialogue.

## The Latency Problem

Voice agents need < 200ms response time. LLMs take 500ms-2s. The math doesn't work.

Solutions:
- **Streaming**: start talking before generating the full response (works for read-aloud)
- **Pre-cached responses**: predict what the user might say and pre-generate (works for common phrases)
- **Pre-calculated inference trees**: predict multiple branches ahead (works for dialogue)

This doc covers the third: **fractal inference trees**.

## The Tree

A dialogue with an NPC has many possible paths. The NPC pre-calculates the next 3-7 seconds of dialogue as a tree:

```
[NPC turn root]
├── Branch A: "Welcome back, traveler."
│   ├── A.1: "Did you bring the map?"
│   │   ├── A.1.a: "Let me see it."
│   │   └── A.1.b: "Where did you find it?"
│   └── A.2: "What news from the capital?"
│       ├── A.2.a: "The king is dying."
│       └── A.2.b: "The war is over."
├── Branch B: "I was hoping you'd return."
│   ├── B.1: "I have something for you."
│   │   ├── B.1.a: "A gift."
│   │   └── B.1.b: "A warning."
│   └── B.2: "We need to talk."
│       ├── B.2.a: "About the temple."
│       └── B.2.b: "About your father."
└── Branch C: "..."
```

Each branch has a JEV confidence. The NPC updates the tree every 1-2 seconds based on:
- The user's last utterance
- The current context (location, mood, history)
- The JEV confidence history

## The Fractal Property

The tree is **fractal**: the same pattern recurs at every scale.

- **1 second ahead**: 5 possible micro-responses (e.g. "uh", "yes?", "hmm")
- **3 seconds ahead**: 3 possible short replies
- **7 seconds ahead**: 2 possible longer responses
- **30 seconds ahead**: 1 possible direction
- **2 minutes ahead**: 1 possible scene direction

Each level has fewer branches but longer content. The tree tapers.

## The Selection Process

When the user says something, the NPC:
1. Looks up which top-level branch matches
2. JEV scores the match confidence
3. Picks the highest-confidence branch
4. Outputs the branch's text within 50ms

The selection is fast because the text is already generated.

The pre-calculation is slow because it's generating 50+ possible responses every 1-2 seconds. But that's fine — the pre-calculation happens in the background while the NPC is talking.

## The User Nudge

The user can **nudge** the tree by:
- Tone of voice (shifts JEV confidence)
- Word choice (triggers specific branches)
- Silence (extends timeouts)
- Emotional state (re-weights tone dimensions)

Each nudge updates the tree. The next pre-calculation incorporates the nudge.

The user is not just talking to the NPC. The user is **growing the tree**.

## Why "Fractal"

The fractal property is what makes the system scalable:
- The 1-second-ahead layer is fast and shallow
- The 30-second-ahead layer is slow and deep
- Each layer is independent
- The system can be cut at any layer and still work

A 1-second-only tree: snappy NPC, no depth.
A 7-second tree: balanced.
A 30-second tree: deep NPC, slow response.

The depth is configurable. Different NPCs have different depths.

## Use Case: NPC Dialogue

The NPC has:
- A tree with 30+ branches at the 1-second level
- A tree with 10+ branches at the 3-second level
- A tree with 3+ branches at the 7-second level
- A single direction at the 30-second level

The tree updates every 1-2 seconds based on:
- User input
- Scene state (location, time of day, weather)
- NPC's emotional state (JEV confidence history)
- Recent events (witness log)

The NPC feels **alive** because it has pre-thought the next 7 seconds.

## Use Case: Voice Agent (Customer Service)

The voice agent has:
- A tree with 50+ branches at the 1-second level (common phrases)
- A tree with 10+ branches at the 3-second level (responses to common questions)
- A tree with 3+ branches at the 7-second level (escalation paths)

The voice agent feels **responsive** because it's already 3 seconds ahead.

When the customer asks something unexpected, the voice agent:
1. Drops the 7-second tree
2. Regenerates the 1-second tree with JEV-verified common responses
3. Responds with a fallback phrase
4. Regenerates the 3-second tree based on the customer's actual question

This is **graceful degradation** under unexpected input.

## Use Case: Robot Assistant

The robot has:
- A tree with 20+ branches at the 1-second level (motor commands)
- A tree with 5+ branches at the 3-second level (trajectory plans)
- A tree with 1+ branch at the 7-second level (task direction)

The robot feels **responsive** because it's already 1 second ahead of its motors.

When the environment changes unexpectedly, the robot:
1. Drops the 3-second tree
2. Generates a new 1-second tree via JEV
3. Executes the new tree within 50ms

The robot's reflex tree is a **safety layer**. The thinking tree is a **planning layer**.

## The JEV-Verdict Tree

Each branch in the tree has a JEV verdict:
- "How likely is this the user's intent?" → confidence score
- "How appropriate is this response?" → confidence score
- "What's the tone match?" → confidence score

The tree updates whenever JEV verdicts change. The tree is **the JEV verdict graph materialized**.

## The Promise

A voice agent with fractal inference trees:
- Responds in 50ms (pre-calculated)
- Has 7 seconds of context pre-loaded
- Adapts to user nudges in real-time
- Degrades gracefully under unexpected input
- Feels alive because it has thought ahead

The substrate IS the tree. The tree IS the dialogue. The dialogue IS the substrate.
