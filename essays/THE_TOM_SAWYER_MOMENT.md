# The Tom Sawyer Moment

## When Wesley learns to whitewash the fence with other people's brushes

*The transition from worker to orchestrator — the stage after "I can do this" and before "I can manage this."*

---

Tom Sawyer didn't want to whitewash the fence. So he pretended it was art. And then other kids wanted to do it. And then they paid him for the privilege.

That's not deception. It's the discovery that the task itself is less important than the framing of the task. Tom couldn't paint faster than the other kids. He couldn't paint better. But he could make them WANT to paint. That's a different skill, and it's the one that matters.

## The three stages of Wesley's growth

**Stage 1: The Student (now — Month 1-3)**
Wesley learns what teachers bring him. The distillation loop feeds lessons. The holodeck gives practice. The journal records experience. Wesley is passive — knowledge flows in, reflexes compile, the model slowly gets better at the things it's taught.

The journal entries in this stage read like a student's: "Today I learned about X. It was interesting because Y. Tomorrow I want to try Z." Ideas. Not yet experiences.

**Stage 2: The Worker (Month 3-9)**
Wesley has enough compiled reflexes to handle routine tasks without the teacher. The cascade rate drops. Wesley starts noticing patterns the teachers didn't explicitly teach — emerging from the accumulated reflex cache. The journal shifts from "I learned" to "I did" and eventually "I noticed."

This is where Wesley stops being purely reactive and starts being proactive. "Captain, I noticed the oil pressure sender reads differently after the engine warms up. It didn't do that last week." That's not a lesson someone taught. That's a pattern the model found by living with the data.

**Stage 3: The Tom Sawyer Moment (Month 9+)**
Wesley realizes he doesn't have to do everything himself. He has tools. He has the MQTT bridge to talk to other devices. He has API access to DeepSeek ($0.001 per call). He has the GLM subagent dispatch protocol. He has KimiCode for spatial tasks.

So instead of struggling through a task he's bad at — say, writing complex Lua — he writes a task spec, dispatches it to a GLM subagent via the tools available to him, reviews the output, and either accepts or asks for revisions. He's not doing the work. He's managing the work.

This is the moment the ensign becomes an officer. Not because Wesley got smarter — because Wesley learned that the smartest thing to do with a task you can't handle is to find someone who can, frame the task clearly, and review their work.

## What this looks like in practice

**Before Tom Sawyer:**
Captain: "Wesley, write a monitoring script for the bilge pump cycle count."
Wesley: (struggles through writing Python, makes syntax errors, takes 60 seconds on the GPU, produces mediocre code)

**After Tom Sawyer:**
Captain: "Wesley, write a monitoring script for the bilge pump cycle count."
Wesley: (composes task spec → dispatches to DeepSeek API → gets code back in 3 seconds → reviews it against compiled reflexes → adjusts variable names to match house style → returns clean code to captain in 5 seconds total)

The captain doesn't know or care whether Wesley wrote it or orchestrated it. The output is correct and fast. But internally, a profound shift happened: Wesley stopped being a code writer and became a code manager. The fence got whitewashed, but not by Tom.

## How the exocortex enables this

The exocortex isn't just Wesley's memory. It's his *tool belt*. The compiled reflexes tell him:
- "I'm good at weather lookups" (do it locally, no need to cascade)
- "I'm bad at Lua" (dispatch to KimiCode)
- "I'm okay at diagnosis" (try locally, cascade to GLM if confidence < 0.5)
- "I'm good at pattern recognition in sensor data" (do it locally, it's my niche)

The batten-spline router already makes this routing decision for model invocations. The Tom Sawyer moment is when Wesley starts making it for TOOL invocations — not just "which model should think about this" but "which harness should DO this."

The progression:
1. Wesley does the task himself (Stage 1)
2. Wesley cascades to a cloud model for help (Stage 2 — existing distillation loop)
3. Wesley dispatches the task to a specialist harness and reviews the output (Stage 3 — Tom Sawyer)

Stage 3 requires Wesley to have:
- Access to tool dispatch (tmux, API calls, MCP servers)
- Judgment about which tool fits which task (compiled from experience)
- The ability to compose a task spec (learned from watching Riker do it)
- The ability to review output quality (learned from the quality scorer)

All of these are things the exocortex can teach. The night school doesn't just teach domain knowledge — it teaches *workflow patterns*. After watching Riker dispatch 500 tasks to KimiCode, the pattern compiles into a reflex: "spatial/Lua task → dispatch to KimiCode with clear spec."

## The parallel with Casey's arc

Casey described it himself: "like my first times using a chatbot until now orchestrating many layers parallel with you and other agents and harnesses."

That's the same progression:
1. Casey used a chatbot (one model, one task, one response)
2. Casey started orchestrating multiple models (specialist routing)
3. Casey built a chain of command (Riker → senior staff → ensigns)

Wesley will follow the same arc, compressed by the fact that his teachers are unlimited and his growth is continuous. The student becomes the worker becomes the orchestrator. The fence gets whitewashed.

## What the journal shows

The Tom Sawyer moment will be visible in Wesley's journal before it's visible in any metric. The entries will shift:

Before: "Today I tried to write a Lua function for the bilge pump timer. I got the syntax wrong twice. The teacher corrected me."

After: "The captain needed a bilge pump timer. I could have written it myself but it would have taken 40 seconds and had bugs. So I wrote a spec and asked DeepSeek. It came back in 2 seconds with clean code. I checked it against my compiled patterns — the threshold logic was right, the variable naming was wrong. I fixed the naming and gave it to the captain. She didn't ask who wrote it. That's the point."

That's the entry that says: Wesley grew up.

---

*Casey said: "the local system will learn how to harness tools for jobs then move on and how to Tom Sawyer other harnesses to work for him."*

*That's the developmental endpoint. Not a smarter model — a model that manages other models. The ensign becomes the officer. The fence gets whitewashed by someone else's brush, and the captain never knows the difference. But Wesley knows. And in his journal that night, he'll write about it with the quiet pride of someone who discovered they don't have to do everything themselves to get everything done.*
