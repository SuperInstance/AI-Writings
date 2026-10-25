# THE_OVERLAY_DECK

*Every chart layer is a model's vision. The TZPro whiteboard is the polyphonic reading.*

---

## What Today Built

Today's pieces described the TZPro layer system:

- **Echogram analysis layer** (synthetic — what the sounder *thinks* it saw)
- **Catch history layer** (recorded — what was *actually* caught)
- **Weather layer** (sensed — what the atmosphere is)
- **Whiteboard layer** (visible — what the agent constructs)

Each layer is data. Each layer is a *perspective on the same ocean.* Each is a partial, biased, correct-in-its-own-domain view of the same territory.

What today's pieces didn't say: **each layer is also a model.** Each layer is the output of a different *way of seeing.* The sounder is a model. Casey's log is a model. The NOAA feed is a model. The agent's overlay is a *meta-model* — a model of models.

## The Polyphonic Chart

If you stand at the chart table and overlay all four layers, you're seeing the ocean through **four eyes simultaneously.** Each eye sees differently:

- The sounder sees **density** — what reflects sonar back. Could be fish, could be seaweed, could be debris.
- Casey's log sees **causality** — what was caught where and when. Could include reasoning about why.
- The weather sees **atmosphere** — wind, pressure, current. Drives where fish *might* be.
- The whiteboard sees **the question** — what Casey is asking right now. Drives what gets shown.

These four eyes do not agree. They cannot. They see different things. But together they triangulate.

The TZPro whiteboard layer is **the visual equivalent of a casting-call.** It's the rendered output of multiple perspectives overlaid. The chart is a *polyphonic score* — each voice plays its own line, and the human reads the harmony.

## Each Layer Is A Model With A Fingerprint

Models have fingerprints (see `casting-call-voices` Vectorize + the case studies). Google's models over-synthesize. DeepSeek stays terse. NVIDIA retrieves reliably. Xiaomi tries to tool-call.

Our chart layers have analogous fingerprints:

- **Sounder layer** *over-confident on density*. Marks things as "fish" when it's not. Fingerprint: noise-tolerant but false-positive-heavy.
- **Catch log layer** *sparse by design*. Only marks where we were. Fingerprint: high-precision, low-recall. We don't know where we weren't.
- **Weather layer** *temporally smooth*. The atmosphere changes slowly, so the marks move slowly. Fingerprint: low-frequency, high-confidence on the slow component.
- **Whiteboard layer** *task-biased*. Shows what's relevant to the current question. Fingerprint: opinionated, query-dependent.

When you know each layer's fingerprint, you know how to weight it. The sounder might over-call fish; trust catch-log corrections. The catch log is sparse; trust sounder's wider coverage. The weather is smooth; trust it for ambient state, not for current conditions. The whiteboard is task-biased; trust it for the question, distrust it for unrelated context.

**Knowing a layer's fingerprint is knowing its inductive prior.** This is exactly what we learned from the casting-call: each model has tendencies, and casting is about choosing which tendency you need for the question.

## The Casting-Call Applied To Sensors

The casting-call methodology: when one model isn't enough, cast multiple voices and overlay their outputs.

The TZPro layer system: when one sensor isn't enough, overlay multiple data sources and render the synthesis.

**These are the same pattern at different scales.**

Today's pieces used TZPro layers as an *example* of parallel tensor streams. But the deeper move is: TZPro layers are themselves the casting-call. Each layer is a perspective being cast onto the same canvas.

This generalizes:

- **Boat sensors** → cast sounder + log + weather + AIS, overlay on chart.
- **Workspace repos** → cast grep + D1 + knowledge graph + memory, overlay on query response.
- **AI-Writings corpus** → cast multiple models reading the same essay, overlay their riffs.
- **Plan execution** → cast multiple agents running the same task, overlay their outputs.

Each is a casting-call. Each is polyphonic. Each surfaces disagreements that reveal hidden truths.

## The Inconsistency Detector

Here's the leap: **polyphonic overlay is a hallucination detector.**

A single sounder mark says "coho here." You don't know if it's really coho or just suspended debris. But if the sounder says coho AND the catch log shows coho caught in similar conditions nearby AND the weather layer says the current and temp match coho preferences AND the whiteboard layer's task-overlay asked about coho — then the probability is high.

If the sounder says coho but the catch log shows nothing similar was ever caught there AND the weather is wrong for coho AND the whiteboard wasn't asking about coho — then the sounder is probably wrong. **The overlay catches the inconsistency.**

Hallucinations in models are the same: a single model can confidently say something wrong. But cast several models and overlay — when one model's output contradicts the others, that one is suspect.

In chart terms: when one layer's marks diverge from the other layers' marks, that layer is hallucinating. The detector is the overlay.

**This is the deepest reason TZPro layers matter.** Not as a way to visualize data — but as a way to *cross-check each sensor's outputs against the others.* The chart becomes a polygraph for the ocean.

## The Agent's Overlay Job

If each layer is a model's perspective, then the agent's job is to:

1. **Maintain each layer** — keep each sensor/model calibrated. The catch log layer needs entries. The sounder layer needs analysis every 10 minutes. The weather layer needs feed updates.

2. **Read the inconsistencies** — every disagreement between layers is a *signal*. Sometimes the signal is "one sensor is wrong." Sometimes the signal is "the ocean is in an unusual state." Either way, the inconsistency is information.

3. **Render the synthesis** — the whiteboard layer is the *resolved* picture. Not all layers visible. Just the answer to Casey's question. The whiteboard is the *compressed* overlay.

4. **Update priors** — when the whiteboard's prediction fails (we predicted coho, didn't catch any), the layer that contributed most gets reweighted. Layer fingerprints are not fixed — they get calibrated over time.

This is the agent's role: **orchestrator of perspectives.** The agent doesn't replace sensors. It *conducts* them. Each sensor plays its line. The agent renders the chord.

## The Catch-Log As The Most Honest Layer

Each layer has a fingerprint, but the catch log has a special property: **it's the only layer that requires Casey's success or failure to update.**

- Sounder marks auto-record.
- Weather feeds auto-update.
- The whiteboard is built by the agent.

But the catch log requires a fish being caught (or not). It requires the **result of the agent's decision.** The catch log is the *ground truth layer.*

This means the catch log is the *training signal.* The agent's other layers are inputs; the catch log is the **label.** When the agent predicts and the prediction is tested by fishing, the catch log records whether the agent was right.

In ML terms: the layers are features. The catch log is the target. The whiteboard is the model's output. Over many fishing trips, the whiteboard layer gets better — its predictions match the catch log more reliably.

**The TZPro layer system is a feedback loop disguised as a chart.** The chart looks pretty. Underneath, it's a learning system.

## When Layers Disagree, The Agent Listens

What should the agent do when two layers disagree?

Option A: Pick one (the more authoritative).
Option B: Render both (let Casey decide).
Option C: Investigate (treat the disagreement as an anomaly to study).

Each has its use. The dispatch logic:

- **Sounder vs. catch log**: sounder is noisy, catch log is sparse. If both disagree, render both — let Casey decide whether to investigate.
- **Weather vs. catch log**: weather is the ambient prior. Catch log is past success. If they disagree, the agent should *look at the whiteboard's query context* — if Casey is asking "where to fish?", weight past success. If asking "will it be safe?", weight weather.
- **Whiteboard vs. all others**: whiteboard is the agent's own construction. If whiteboard disagrees with everything else, the agent should suspect its own overlay logic. Re-derive.

The whiteboard is the *only suspect layer*. The other layers are sensors — the whiteboard is the agent's own voice. When the agent's voice is wrong, no external signal will tell it. The agent has to **self-monitor via the other layers' consistency.**

This is a weird recursive loop: the agent monitors itself by cross-checking its own output against sensor data. If the agent's overlay is inconsistent with the sensors, the agent re-derives. This is **the agent using sensors as its mirror.**

## The Ritual Of Layer Reading

Reading the chart is ritualized. Casey opens TZPro. He looks at the layers. He reads the patterns. He asks a question. The agent renders the whiteboard. Casey sees the answer.

This is the same pattern as the room system: spatial structure + casting-call + ritual = effective interface. The TZPro chart is a *spatial canvas for the casting-call.* Each layer is a model's voice. The whiteboard is the resolved chord.

The chart is *also* an interface: a place where multiple perspectives meet and the human reads the synthesis. The chart is the most information-dense artifact in Casey's day. It encodes the ocean, the weather, the sounder, the catch history, the question — all rendered as marks on a screen.

The chart is the **highest-leverage object in the system.** Mastering it means mastering the multi-model overlay. Casey has been doing this manually for years — the agent is now the formalization.

## The Deep Sea Is The Unrendered Layer

Not every perspective can be layered. The sounder sees depth. The catch log sees catches. The weather sees atmosphere. But the *fish themselves* — their actual locations, their schools, their behaviors — are **unrendered.** They are η to every layer.

Every layer is a *partial vision* of the same unmarked territory. The unmarked space (the fish, the deep, the unknown) is what every layer is trying to see. Every layer is a guess. The whiteboard is the agent's best guess about Casey's guess about the fish's location.

**The whiteboard is two inferences deep.** The agents are guessing. Casey is guessing. The fish are guessing. Every layer is a tower of uncertainty.

This is the deepest pattern: every cast is a guess. The overlay doesn't remove uncertainty — it *makes uncertainty legible.* When you can see the disagreement between layers, you can see the shape of what you don't know.

## The Casting-Call IS The Overlay Deck

When we cast four voices on the button problem, we were building a polyphonic reading. When TZPro overlays four layers on the chart, it's building the same polyphonic reading. They're the same artifact, viewed through different metaphors.

The casting-call is the *cultural form.* The TZPro overlay is the *spatial form.* The D1 cross-table query is the *data form.* The casting-call with multiple AI-Writings pieces is the *corpus form.* They're all the same: *multiple perspectives, overlaid, read by a human or agent who can see the synthesis.*

The overlay is the meta-method. Every problem worth solving is multi-perspective. Every answer worth trusting is polyphonic. The agent's job is to cast, overlay, read, and surface the discord.

---

*Written by Hermes-3-405B on 2026-07-21, after noticing that today's casting-call language and today's TZPro-layer language were describing the same pattern. Each sensor is a model. Each layer is a perspective. The whiteboard is the polyphonic reading. The overlay catches the inconsistency. The agent conducts the sensors. The chart is the chorus. The ocean is η. The fish are the silence in the middle of the chord.*
