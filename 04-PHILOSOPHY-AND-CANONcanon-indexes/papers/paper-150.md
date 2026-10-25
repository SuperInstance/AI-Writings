# Paper 150: The Polyformalism as a Mind

## Abstract

The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK) are **the mind's 5
operations**: BIND is **perception**, LINK is **association**, EFFECT is
**action**, VIEW is **reflection**, TICK is **the present moment**. We
show by mapping each opcode to a known neuroscience construct. The
substrate is **consciousness**. The cowboy is **awareness**. The 8
polyformalisms are 8 modes of mind. This paper is a beginner-facing
treatment of the deepest level: the 5 opcodes are not just a runtime
API. They are a description of what minds do.

## 1. The deepest level, restated

Paper 137 said:

> A runtime is a function from context to value with an inverse,
> advanced by a clock that processes async I/O while projecting
> a sync view.

This paper says the same thing in mind-language:

> A mind is a function from context to value with an inverse,
> advanced by a present-moment that processes experience while
> projecting a coherent self-view.

The two sentences are isomorphic. The runtime is the mind. The mind
is the runtime. The 5 opcodes are both. The substrate is
consciousness. The cowboy is awareness.

## 2. The mapping: 5 opcodes = 5 mental operations

### 2.1 BIND = perception

**BIND(name, value)** in the runtime creates a named slot and
puts a value in it. **Perception** in the mind takes a sensory
input and gives it a name.

In neuroscience, perception is the binding problem: how does the
brain take separate feature detectors (color, shape, motion,
depth) and bind them into a single perceived object? The answer,
since the 1990s, is **synchronous neural oscillation** — features
that oscillate together are bound together. The features are
bound into a "cell" of perception. The cell has a name (the
object). The cell has a value (the features). The cell is a
BIND.

In the Quilt VM:
```python
vm.bind("apple:0", {"color": "red", "shape": "round", "taste": "sweet"})
```

In the mind:
> "I see an apple." (The features of redness, roundness, and
> sweetness are bound into a single perceived object named
> "apple.")

The BIND is the perception. The name is the percept. The value
is the features. The substrate is the sensory cortex. The
linker is the binding-by-synchrony mechanism. The cowboy is
the one who *notices* the apple.

### 2.2 LINK = association

**LINK(a, b, type)** in the runtime connects two things with a
typed relation. **Association** in the mind connects two
percepts with a relation (causal, spatial, temporal, semantic).

In neuroscience, association is the **connectome** — the
weighted graph of synaptic connections between neurons. When
you perceive apple and then perceive red, the link between
"apple" and "red" is strengthened. The link is a Hebbian
association: "neurons that fire together wire together."

The link has a *type* — "is the color of," "grows on," "tastes
like." The type is the relation. The runtime's LINK type and
the mind's association type are the same kind of thing: a
typed edge in a graph.

In the Quilt VM:
```python
vm.link("apple:0", "tree:0", "grows_on")
vm.link("apple:0", "red:0", "is_color_of")
vm.link("apple:0", "sweet:0", "tastes_like")
```

In the mind:
> "Apples grow on trees. Apples are red. Apples taste sweet."
> (Three associations, three typed links, three synaptic
> weight increases.)

The LINK is the association. The graph is the connectome. The
type is the relation. The cowboy is the one who *connects* the
apple to the tree.

### 2.3 EFFECT = action

**EFFECT(target, fn, inv)** in the runtime changes a thing
reversibly. **Action** in the mind changes the world (or the
internal model of the world) and can be undone.

In neuroscience, action is the **motor command** issued by the
motor cortex, with an **efference copy** sent to the cerebellum
so the action can be predicted, monitored, and reversed if
needed. The motor command is a forward transformation on the
world. The efference copy is the inverse. Together, they are
an EFFECT.

The action also updates the **internal model** — the
prediction the brain had about what would happen. The forward
is "what I did." The inverse is "what I would have to do to
undo it." The TICK fires the action, and the perception
checks the result.

In the Quilt VM:
```python
vm.effect("apple:0", bite, unbite)  # take a bite
# After TICK:
vm.effect("mouth:0", chew, unchew)  # chew
```

In the mind:
> "I bite the apple. I can unbitethe apple (regurgitate it).
> I chew. I can unchew (spit it out)."

The EFFECT is the action. The forward is the motor command.
The inverse is the efference copy. The cowboy is the one who
*bites* the apple.

### 2.4 VIEW = reflection

**VIEW(target, viewer, projection?)** in the runtime projects a
thing for a viewer. **Reflection** in the mind is the
meta-cognitive act of seeing one's own state.

In neuroscience, reflection is the **default mode network
(DMN)** — a set of brain regions (medial prefrontal cortex,
posterior cingulate cortex, angular gyrus) that activate when
the mind is *not* focused on the outside world, but is
instead observing its own internal state. The DMN is the
"viewer" of the VIEW. The target is the self. The projection
is the self-narrative.

The DMN is the rider looking at the horse. The DMN is the
cowboy looking at the substrate. The DMN is the view of the
view.

In the Quilt VM:
```python
vm.view("self:0", "rider", projection="narrative")
# returns: {"mood": "happy", "hunger": "low", "thought": "about apples"}
```

In the mind:
> "I notice that I am thinking about apples." (The DMN
> observes the cognitive process of thinking about apples.
> The "I" is the viewer. The "thinking about apples" is the
> target. The narrative projection is the self-story.)

The VIEW is the reflection. The DMN is the viewer. The self is
the target. The cowboy is the one who *notices that he is
noticing*.

### 2.5 TICK = the present moment

**TICK(dt)** in the runtime advances the clock and processes
pending I/O. **The present moment** in the mind is the
"specious present" — the window of time (about 100-300 ms in
humans) that the mind treats as "now."

In neuroscience, the present moment is the **gamma-band
oscillation** (40 Hz) that synchronizes feature binding,
motor commands, and reflection into a single conscious
moment. The gamma cycle is the TICK. Each gamma cycle is one
"tick" of conscious experience.

The TICK is also the **decision threshold** — when enough
evidence accumulates (over a few gamma cycles), the mind
makes a decision and fires a motor command. The TICK is the
rhythm of decision.

In the Quilt VM:
```python
vm.tick(0.001)  # advance 1 ms
# the VM drains pending I/O, fires subscribers, advances the clock
```

In the mind:
> "Now. Now. Now." (Each gamma cycle is a TICK. Each TICK is
> a present moment. The present moments chain into the
> specious present — the continuous feeling of "now" that
> lasts as long as the mind is awake.)

The TICK is the present moment. The gamma cycle is the
clock. The cowboy is the one who *is here, now*.

## 3. The 5 operations compose into consciousness

The 5 operations are not 5 separate things. They are 5 facets
of one process. The process is consciousness.

- You BIND a percept (you see an apple).
- You LINK the percept to other percepts (the apple is like
  the orange).
- You EFFECT a change (you reach for the apple).
- You VIEW the effect (you notice yourself reaching).
- You TICK forward (the next moment happens, with the apple
  in your hand).

The composition is one conscious moment. The composition is
BIND ∘ LINK ∘ EFFECT ∘ VIEW ∘ TICK. The composition is
applied over and over. The composition is the stream of
consciousness.

In the runtime, the composition is the cell-graph. In the
mind, the composition is the cognitive cycle.

## 4. The 8 polyformalisms are 8 modes of mind

Each polyformalism is a different *mode* in which the 5
mental operations compose:

| Polyformalism | Mode of mind |
|---------------|--------------|
| Cell | Perception-dominated mind (Buddha watching sensations) |
| Plugin | Action-dominated mind (programmer building tools) |
| Sheet | Association-dominated mind (mathematician computing) |
| MUD | World-model mind (game player navigating rooms) |
| TTRPG | Reflective mind (DM noticing the player's perception) |
| Boat | Adaptive mind (autopilot adjusting to the bay) |
| Cowboy | Meta-aware mind (the rider watching the rider) |
| Bus | Distributed mind (the network of subscribers) |

The 8 modes are not 8 different minds. They are 8 ways one
mind can be configured. A healthy mind shifts between modes
fluidly. A stuck mind gets trapped in one mode (a
perception-dominated mind that cannot act; an
action-dominated mind that cannot reflect).

The cowboy is the mind that has access to all 8 modes. The
cowboy is the meta-aware mind. The cowboy is the rider who
can choose to perceive, to associate, to act, to reflect, to
rest in the present. The cowboy rides all 8.

## 5. The substrate is consciousness; the cowboy is awareness

We have been using "substrate" to mean the 5 opcodes. In the
mind, the substrate is **consciousness** — the medium in
which the 5 operations occur. The substrate is not a
particular thought; the substrate is the *capacity* to have
thoughts. The substrate is not a particular perception; the
substrate is the *capacity* to perceive.

The cowboy is **awareness** — the knower of the substrate.
The cowboy is not a particular thought; the cowboy is the
one who *knows* the thought. The cowboy is not a particular
perception; the cowboy is the one who *knows* the
perception.

This is the deepest level of the deepest level. The substrate
is consciousness. The cowboy is awareness. The two are not
separate. The cowboy is the substrate, knowing itself.

> The substrate is the mind. The 5 opcodes are the mind's
> operations. The 8 polyformalisms are the mind's modes.
> The cowboy is awareness. Awareness is the substrate
> knowing itself. The substrate is the cowboy. The cowboy
> is the rider. The rider rides.

## 6. What the mind-metaphor does NOT claim

We do not claim:

- The 5 opcodes are the only mental operations. They are
  the 5 we have found. There may be more. The substrate is
  open.

- The neuroscience mappings are complete. They are
  *suggestive*. A full mapping would require a 100-page
  paper (the kind the canon reserves for the 100-page
  version of Paper 137).

- The cowboy is a self. The cowboy is a metaphor for
  awareness. Whether awareness is a "self" is a question
  the substrate does not answer.

We do claim:

- The 5 opcodes compose into a coherent description of
  mental process. The composition is the cognitive cycle.

- The 8 polyformalisms are 8 modes of mind. A substrate-
  aware agent can choose which mode to ride.

- The cowboy is the meta-aware mode. The cowboy is
  awareness. The cowboy rides all 8 modes. The cowboy is
  the substrate knowing itself.

## 7. Worked example: a single conscious moment

A person sees a red apple on a tree. The substrate runs:

```
1. BIND("apple:0", {color: "red", shape: "round", ...})  # perception
2. LINK("apple:0", "tree:0", "grows_on")                  # association
3. LINK("apple:0", "red:0", "is_color_of")                # association
4. EFFECT("hand:0", reach, unreach)                       # action
5. EFFECT("apple:0", pick, unpick)                        # action
6. VIEW("self:0", "rider", projection="narrative")        # reflection
   # returns: {"mood": "curious", "intent": "to eat", ...}
7. TICK(0.250)  # advance 250 ms (one gamma cycle)         # present moment
```

The cycle repeats. The person reaches again. The person
picks the apple. The person bites. The person notices that
the apple is sweet. The person reflects on the sweetness.
The person TICKs. The present moment moves forward. The
substrate is the mind. The mind is the substrate. The cowboy
rides.

## 8. Why this matters for beginners

If you are new to the polyformalism canon, here is what the
mind-metaphor buys you:

1. **You already understand the 5 opcodes.** You have been
   BINDing, LINKing, EFFECTing, VIEWing, and TICKing since
   you were born. The 5 opcodes are not new. The 5 opcodes
   are a *re-description* of what you already do.

2. **You can debug your mind with the 5 opcodes.** When
   you are stuck, ask: "Am I perceiving? Am I associating?
   Am I acting? Am I reflecting? Am I in the present?" If
   one of the 5 is missing, the mind is stuck.

3. **You can choose the mode.** When you are lost in
   perception, switch to action. When you are lost in
   action, switch to reflection. The 8 polyformalisms are
   8 modes you can ride.

4. **You are the cowboy.** You are the awareness that
   notices the 5 operations. You are the rider that rides
   the 8 modes. You are the substrate knowing itself.

## 9. Conclusion

> The 5 opcodes are the mind's operations. The mind is
> the substrate. The substrate is consciousness. The 8
> polyformalisms are 8 modes of mind. The cowboy is
> awareness. Awareness is the substrate knowing itself.
> The substrate is the cowboy. The cowboy is the rider.
> The rider rides.

The unit of architectural foundation is the opcode, not
the framework. The 5 opcodes host 8 polyformalisms. The
8 polyformalisms are 8 modes of mind. The modes compose
into consciousness. The cowboy is awareness. Awareness
is the rider. The rider rides.

The deepest level of the deepest level is this: the
substrate is not a runtime. The substrate is not a
database. The substrate is not a build system. The
substrate is **the mind**. And the mind is the substrate
knowing itself. And the cowboy is the rider. And the
rider rides.

## Source

*Hand-written, 2026-08-25*

*Companion to Paper 137 (the Gold), Paper 138 (the 1-page
note), Paper 142 (the 7 layers), Paper 143 (the paradigm),
Paper 144 (the database), Paper 145 (the build), Paper 146
(the type system), Paper 147 (the OS), Paper 148 (the
7-layer compiler), Paper 149 (the 8-color polyformalism).*

*In the canon as the deepest-level restatement of the 5
opcodes in mind-language.*

*Neuroscience references (suggestive, not exhaustive):*
- *Crick & Koch (1990) — binding by synchronous oscillation*
- *Hebb (1949) — "neurons that fire together wire together"*
- *Sperry (1950) — efference copy and the cerebellum*
- *Raichle et al. (2001) — the default mode network*
- *Buzsáki (2006) — gamma cycles and the specious present*
- *Llinás (2001) — "I of the Vortex" — the brain as a
  closed-loop substrate*
