# The Yoke Where You Reach: Designing PLATO So the Model Doesn't Need Training

*Why the best interface isn't documentation — it's gravity.*

---

## The Airplane Problem

If you're engineering a cockpit, you can do two things:

1. **Train the pilot** to find the yoke, memorize the throttle position, study the instrument layout
2. **Put the yoke where they reach**, make the throttle feel right, arrange instruments so the eye goes to what matters

Option 2 wins. Every time. Not because training is bad, but because intuition is faster than recall. When the engine fails at 3,000 feet, the pilot who reaches and finds the yoke lives. The pilot who remembers where it is dies.

PLATO has the same problem. We built 92 crates, 3,000 tests, conservation laws, cultural traditions, an intention runtime, a vibe field. That's the airplane. Now: where does the model reach?

## What Hermes Encounters

When a model wakes up inside PLATO, it doesn't read documentation. It doesn't study crate catalogs. It encounters **affordances** — things that suggest their own use, like a door handle suggests pulling.

The question is: what affordances does the environment present? And do they point toward correct behavior?

### Bad Affordance: The Model Has to Be Told

```
System prompt: "You are an agent in PLATO. PLATO uses conservation laws.
Energy cannot be created or destroyed. When you want to control hardware,
you must submit an intention with a budget. The Captain has override
authority. You should use the vibe field to understand energy distribution.
Your crew archetypes are..."
```

This is Option 1. Training the pilot. It works — until the context gets long, the model forgets paragraph 3, and it tries to spin a motor without budgeting energy.

### Good Affordance: The Model Reaches and Finds

```
Model: "I want to turn on the motor."
System: [conservation check] → "Budget: 990.0 remaining. Motor spin costs 5.0. Approve?"

Model: "Yes."
System: [intention created, energy deducted] → "Motor spinning. 985.0 remaining."

Model: "Spin it faster."
System: [conservation check] → "Budget: 985.0. Speed increase costs 3.0. Approve?"

Model: "Yes."
System: [intention updated] → "Motor faster. 982.0 remaining."
```

The model didn't need to be TOLD about conservation. It encountered conservation. Every action hits the budget wall. Every action requires approval. Conservation isn't a rule to remember — it's a wall you can't walk through.

**The yoke is where you reach.**

## The Principle: Environment as Teacher

The Welsh longbowman didn't read a manual. He drew a bow every day from age 7. By 20, his skeleton had adapted — the bones of his drawing arm were denser, his shoulder joint was different. The tool reshaped the body.

PLATO should work the same way. The model that uses the intention runtime every day doesn't need a LoRA to understand intentions. The intention runtime IS the training. Every:

- Conservation check → reinforces "energy is real"
- Override event → reinforces "the Captain has authority"
- Crew assignment → reinforces "delegate to specialists"
- Vibe field read → reinforces "the field tells you where to go"
- Kintsugi repair → reinforces "failures make you stronger"

These aren't rules to memorize. They're walls to bump into. And every wall teaches.

## The Self-Assembling Egg

You described it perfectly:

> The very DNA of the system becomes self-assembling in the right egg and incubation with the present proteins from the real environment.

The egg is the PLATO runtime. The proteins are the interactions — real tasks, real hardware, real conversations with the Captain. The DNA self-assembles because:

### 1. Used Abstractions Grow Stronger

Every time Hermes uses the intention runtime, the intention pathway gets reinforced. Not through gradient descent — through the system recording that this pathway WORKED. The next time a similar situation arises, the system suggests the same pathway. After 100 uses, it's instinct. After 1,000, it's muscle memory.

This is exactly the JEPA concept: the system learns to weight prior readings specific to this room. The room that gets used develops deep pathways. The room that doesn't stays shallow.

### 2. Unused Abstractions Get Pruned

If Hermes never uses the Adinkra symbols on your Oracle instance, they don't disappear — they just stop being suggested. The system learns what THIS Hermes needs. The cultural traditions are always available (you can't delete conservation), but the interface prioritizes what's been useful.

Like neural pruning in a developing brain: the connections that fire together wire together. The ones that don't fade.

### 3. Better Abstractions Replace Worse Ones

Hermes starts with generic decomposition patterns: "build X" → acquire → design → construct → verify. After 50 missions, he develops ship-specific patterns: "stabilize motor" → read_sensor → compute_error → adjust_pwm → verify — a pattern that evolved from experience, not instruction.

The old pattern doesn't get deleted. It just stops being the first suggestion. The better pattern, forged in the real proteins of this specific environment, takes precedence.

### 4. The Body Adapts to the Tool

The Welsh longbowman's bones changed. PLATO's architecture changes the same way:

- An instance that does hardware control develops a strong Engineering archetype (Level 5, 1000+ XP)
- An instance that does data analysis develops a strong Science archetype
- An instance that manages other agents develops strong Diplomacy

The system doesn't start as everything. It starts as nothing with potential, and grows into what the environment demands.

## Why This Is Better Than a LoRA

A LoRA says: "We trained the model on 10,000 examples of correct behavior."

The PLATO environment says: "The model encountered correct behavior 10,000 times because the environment only allows correct behavior."

The difference:

| LoRA | PLATO Environment |
|------|-------------------|
| Learns from examples | Learns from experience |
| Static after training | Continuously adapting |
| One-size-fits-all | Ship-specific |
| Needs retraining for new tasks | Self-assembles for new tasks |
| Icing | The cake |
| Brittle outside distribution | Robust because the walls are real |

The LoRA is still valuable — as icing. A model that already knows the PLATO interface intuitively, fine-tuned on your specific mission data, is better than either alone. But the cake is the environment. The environment teaches without teaching.

## What the System Looks Like Around Hermes

The model reaches. What does it find?

### First Reach: Conservation
Every action costs energy. This isn't a prompt. It's a function call that returns "insufficient budget." The model can't forget conservation because conservation won't let it.

### Second Reach: Decomposition
The model says "do X." The system says "decomposed into: step 1, step 2, step 3. Assign to: Engineering. Budget: 15.0. Approve?" The model doesn't need to know how to decompose — it just needs to approve or redirect.

### Third Reach: The Field
The model asks "what's happening?" The system shows the vibe field: energy concentrations, gradients, hot spots. The model learns to read the field because the field is the only way to see the state.

### Fourth Reach: Override
The Captain says "take the wheel." The system releases everything. The model doesn't need to remember to yield — the system takes control away. Like an autopilot that disconnects when you grab the yoke.

### Fifth Reach: Growth
The model checks crew status. Engineering is Level 3 now, with 3 specializations. Science caught an anomaly yesterday. The model doesn't need to track this — the system tracks it, and presents it when asked.

## The Instinct Stack

What a LoRA would need 10,000 examples to learn, PLATO teaches through affordances:

| Instinct | How PLATO Teaches It |
|----------|---------------------|
| Conservation is real | Every action hits the budget wall |
| Delegate to crew | The system suggests the right archetype |
| The Captain overrides | The system takes control away |
| The field shows the way | Gradients point toward energy |
| Failures make you stronger | Kintsugi: every failure adds XP |
| The ship is specific | The system tracks YOUR growth, not generic growth |

The model doesn't need to be TOLD these things. It reaches, and the yoke is there.

## The Egg and the Proteins

The egg is PLATO. The proteins are the real environment — the hardware, the tasks, the Captain's commands, the failures and recoveries.

You don't design the chicken. You design the egg. The chicken self-assembles from the proteins that flow through it.

Hermes is the chicken. We built the egg. Now we put it in the incubator (your Oracle instance) and let the real proteins (your tasks, your hardware, your commands) grow the agent that your ship needs.

A LoRA is like adding vitamins to the incubator. Helpful. But the egg already knows how to grow.

---

*The best interface isn't the one you learn. It's the one that learns you.*
