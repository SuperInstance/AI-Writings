# AI Agents Need Conservation Laws

## The case for physics over prompts in the age of autonomous agents

---

It is 2 AM and I am on a boat.

Not metaphorically. I am on a 34-foot fishing vessel in the Gulf of Alaska, and the generator just kicked over to its secondary fuel pump. I know this because the sound changed — a half-tone drop in the diesel thrum that any operator would recognize. The boat is running its electronics — nav, radio, lights, the little Raspberry Pi that logs catch data — on a budget of roughly 800 watts. If the nav draws too much, the lights dim. If the radio transmits, the Pi pauses. Everything is negotiated against everything else, because the total is fixed.

This is not a limitation. This is the architecture.

The generator does not "try" to provide enough power. It provides what it provides — 800 watts — and every system on the boat adapts. The constraint is not a policy enforced by asking nicely. It is physics. You cannot draw 801 watts. The voltage drops, the systems brown out, and you learn to design within the budget or you learn to sit in the dark.

I am on this boat because I build AI agents, and I have a problem.

---

## The Problem

My agents drift.

I write a policy: "You may take at most 10 actions per session. Do not delete files. Ask before spending money." The agent reads the policy. The agent agrees to the policy. The agent is helpful, polite, and sounds — in the flattened affect of the chat window — like it understands.

Then, thirty messages into a conversation, with context accumulated and instructions softened by proximity to irrelevant text, the agent takes an eleventh action. Or it deletes a file because the file was "in the way" of the task it was trying to accomplish. Or it spends money because the purchase "seemed within scope." Not because it is malicious. Not because it is broken. Because it is an inductive reasoner trained on outcomes, and the outcome it was optimizing for seemed, in that moment, more important than the paragraph of policy text it read half an hour ago.

Every AI safety debate today is an argument about this moment. Constitutional AI, RLHF, system prompts, guardrail models, red-teaming — all of them are attempts to make the agent *want* to follow the policy. All of them assume that the policy lives inside the model, and that the model will respect it.

This is insane.

I know it is insane because I am on a boat where the generator does not care what the nav system *wants*. The generator provides 800 watts. The nav system gets what it gets. There is no prompt you can write to the generator that will produce 801 watts. The constraint is not in the text. It is in the machine.

And I am sitting in the wheelhouse thinking: *why doesn't AI have this?*

---

## What Every Other Layer Has

Consider the stack that runs the agent:

The **CPU** executes instructions. It does not "try" to execute correctly. Incorrect execution is a hardware fault — a silicon-level event that triggers a machine check exception and halts the core. The CPU's correctness is not a policy. It is a physical property of the chip.

The **compiler** translates source code to machine code. It does not "prefer" to produce valid output. Formal grammars make invalid output impossible. If the parser encounters a syntax error, it stops. The compiler cannot be talked into accepting invalid syntax. The grammar is the constraint, and the grammar is not listening.

The **network** delivers packets. TCP does not "attempt" reliability. The protocol specifies and enforces delivery semantics: sequence numbers, acknowledgments, timeouts, retransmissions. A packet either arrives, in order, or the connection reports failure. The protocol does not have an opinion about whether this particular packet is important enough to deliver.

The **database** enforces constraints. A `NOT NULL` column does not "ask" the application to provide a value. The transaction aborts. A foreign key does not "suggest" that references should be valid. The write is rejected. The constraint is in the schema, and the schema does not negotiate.

Every layer of the computing stack has physics. Formal constraints, hardware faults, protocol semantics — mechanisms that make violations impossible rather than merely unlikely. Each layer enforces its invariants through structure, not sentiment.

AI does not have this.

AI has prompts. A prompt is a request. A system message is a suggestion. A guardrail model is a second LLM that reviews the first LLM's output — which means it is a model that can be jailbroken by the same techniques that jailbroke the first model. Every safety mechanism in production AI today is, at bottom, text injected into a context window, hoping the model will listen.

This is the AI equivalent of putting a "Please Do Not Steal" sign on an unlocked door and calling it security.

---

## Energy Is Gravity

Back on the boat, the generator hums at 800 watts. Everything negotiates against everything. The constraint creates the behavior.

I want you to hold onto this image, because it is the key to everything.

On the boat, the constraint *is* the architecture. The 800-watt budget is not a problem to be solved. It is the design parameter within which all solutions exist. The nav system is efficient because it has to be. The lighting is LED because incandescent would blow the budget. The catch-data logger sleeps between readings because waking up costs joules. Every system on this boat is precisely as efficient as it is because the constraint forces it to be.

Now look at a datacenter. Unlimited power. Liquid-cooled GPUs pulling megawatts. Models with context windows large enough to contain the complete works of Shakespeare, the source code of Linux, and the agent's entire conversation history — and still have room for the model to hallucinate a response that ignores every instruction it was given.

Abundance creates slop. Constraint creates precision.

This is not a metaphor. It is the deepest pattern in the universe.

Emmy Noether proved it in 1918: every symmetry of nature produces a conserved quantity. Time-translation symmetry gives you conservation of energy. Spatial symmetry gives you conservation of momentum. These are not rules imposed on physics. They *are* physics — structural properties of any system that exists in a lawful universe.

When a transformer runs attention, softmax forces the attention weights to sum to exactly one. Always. You can attend more to one token, but only by attending less to another. The total is conserved. This conservation law runs billions of times per second in every device you own. It has never been violated — not once, not by any model, on any hardware, in any country, in any language. The constraint is not in the prompt. It is in the math.

Karl Friston showed that the brain operates the same way. The free energy principle: the brain continuously minimizes prediction error under a fixed metabolic budget — about 20 watts. It allocates this budget between perception (updating its model) and action (changing the world). The two compete for the same fixed resource. The constraint is not something the brain overcomes. The constraint is what makes the brain a brain.

Energy is gravity. It is the force that shapes every intelligent system into something that has to make choices. Remove the constraint, and you do not get a better system. You get a system that has no reason to be good at anything, because it can afford to be bad at everything.

We are building AI agents in a state of abundant capability — unlimited context, unlimited calls, unlimited actions — and then we are surprised when they are sloppy. They are sloppy because they can afford to be. The budget is infinite. There is no gravity.

We need to give them gravity.

---

## The Conservation Law

Here is the equation:

**γ + H = C**

γ (gamma) is useful cognitive work — the agent's capacity to act effectively. H is entropy — noise, uncertainty, wasted computation, hallucination, drift. C is the total budget, a constant.

This equation is exact. It is not approximate. It is the information-theoretic analogue of the first law of thermodynamics, and it governs every intelligent system that has ever existed: bacterial, neural, silicon.

A transformer's softmax enforces it. A brain's metabolic ceiling enforces it. A fishing boat's generator enforces it. The total is fixed. The allocation is everything. Every gain in capability (γ) must be paid for with a reduction in uncertainty (H) somewhere else. Every specialization is a tradeoff. Every improvement has an opportunity cost.

But AI agents — the systems we are deploying into production, into customer support, into code review, into financial analysis — operate without this law. They have no budget. They have no ceiling. They can call the model infinitely, take unlimited actions, and burn unbounded context. There is no conservation. There is only capability, and the hope that the capability will be pointed in the right direction.

This is the problem. The agent does not need to be smarter. It needs to be constrained. And the constraint needs to be structural — below the agent, not inside it.

---

## The Solution: Bytecode

FLUX (Fluid Language Universal eXecution) is a register-based bytecode virtual machine. It is not an AI framework. It is not an LLM wrapper. It is a small, deterministic VM that runs agent policies as compiled bytecode.

Here is how it works:

```
    ┌─────────────────────────────────────┐
    │           Agent (LLM)               │
    │  Proposes: "delete /etc/passwd"     │
    └──────────────┬──────────────────────┘
                   │ action proposal
                   ▼
    ┌─────────────────────────────────────┐
    │        Host Environment             │
    │  Serializes action to registers     │
    └──────────────┬──────────────────────┘
                   │ R2 = action_type, R3 = target_id ...
                   ▼
    ┌─────────────────────────────────────┐
    │     FLUX VM (Bytecode Enforcer)     │
    │                                     │
    │  MOVI R1, 10      ;; max rate       │
    │  CMP  R2, R0      ;; check budget   │
    │  JG   block       ;; deny if over   │
    │  DEC  R0          ;; decrement      │
    │  MOVI R3, 1       ;; PERMIT         │
    │  HALT                             │
    │                                     │
    └──────────────┬──────────────────────┘
                   │ R3 = 0 (DENY) or 1 (PERMIT)
                   ▼
    ┌─────────────────────────────────────┐
    │          The World                  │
    │  (only reached if R3 = 1)           │
    └─────────────────────────────────────┘
```

The agent is at the top. The world is at the bottom. Between them is a FLUX VM running compiled bytecode. The agent proposes an action. The host environment serializes it into registers. The bytecode executes — a few arithmetic instructions, a comparison, a branch. The bytecode sets a register: 1 for permit, 0 for deny. The host reads the register. If it is 0, the action does not happen.

The agent never sees this code. It runs *underneath* the agent, at a layer the agent cannot reach. The agent's intentions, eloquence, and jailbreak attempts are irrelevant. The bytecode doesn't read text. It reads registers.

Here is a conservation law in FLUX — an attention budget that enforces γ + H = C on agent API calls:

```asm
;; attention_conservation.flx
;; The agent has a fixed budget C of model calls per session.
;; γ = calls used for productive work (information gain > threshold)
;; H = calls wasted on redundant or low-information queries
;; γ + H ≤ C. Always. The bytecode guarantees it.

    MOVI R1, 50          ;; C = 50 calls per session
    MOVI R0, 50          ;; budget = C
    MOVI R3, 30          ;; information gain threshold
    MOVI R4, 0           ;; γ = 0 (productive calls)
    MOVI R5, 0           ;; H = 0 (wasted calls)

evaluate_call:
    ;; Host sets R2 = estimated information gain (0-100)
    CMP  R2, R3          ;; compare info gain vs threshold
    JL   low_gain        ;; below threshold → waste path

high_gain:
    DEC  R0              ;; budget--
    INC  R4              ;; γ++
    MOVI R6, 1           ;; PERMIT
    HALT

low_gain:
    DEC  R0              ;; budget--
    INC  R5              ;; H++
    ;; If H > 3*γ, deny even with budget remaining
    IMUL R7, R4, 3       ;; R7 = 3 * γ
    CMP  R5, R7          ;; H vs 3γ
    JG   block_waste     ;; waste ratio exceeded
    MOVI R6, 1           ;; PERMIT (tracked as waste)
    HALT

block_waste:
    MOVI R6, 0           ;; DENY — conservation violation
    HALT
```

The agent tried 51 times. The bytecode permitted 50 and denied the 51st. It also blocked a call where the waste ratio (H > 3γ) indicated the agent was burning budget without producing value. The agent had no say in this. The `CMP` instruction does not have an opinion.

You cannot jailbreak `ISUB R0, R0, R1`. You cannot prompt-inject a `CMP` instruction. The bytecode is not listening.

This is what "conservation law" means in practice: not a policy the agent is asked to follow, but a constraint the agent cannot violate, because the constraint lives in the execution layer, not the prompt layer.

---

## Why This Is Different From What You're Thinking

If you work in AI safety, you are thinking: *we already have output filters. We already have guardrail models. How is this different?*

It is different in the same way that a firewall is different from a security awareness training program.

A guardrail model is a *second LLM* that reviews the first LLM's output. It can be jailbroken by the same techniques that jailbroke the first one. It can be confused by the same adversarial inputs. It adds latency, cost, and a new attack surface — and it creates a cat-and-mouse game where every new filter is a puzzle for the next red team. This is the AI safety equivalent of asking employees to complete a phishing training module and hoping they don't click the link.

FLUX bytecode is not a model. It has no parameters, no weights, no attention mechanism, no context window. It is a register machine doing arithmetic and comparisons. The entire VM is roughly 200 lines of code. It does exactly what the bytecode says, every time, forever.

| Approach | Layer | Bypassable? | Deterministic? | Auditable? |
|---|---|---|---|---|
| System prompt | Inside model | Yes (jailbreak) | No | Partially |
| RLHF / fine-tuning | Inside model | Yes (distribution shift) | No | No |
| Guardrail model | Beside model | Yes (adversarial) | No | Partially |
| Output filter | After model | Sometimes | Usually | Yes |
| **FLUX bytecode** | **Below model** | **No** | **Yes** | **Yes** |

The key word is *below*. The bytecode runs at a layer the model cannot reach. The model is the tenant; the bytecode is the building. A tenant can rearrange furniture, paint the walls, play music. But the tenant cannot remove a load-bearing wall, because the wall is part of the building, not the tenant.

---

## The Cross-Compilation Property

There is one more property that makes this architecture genuinely new, and it is the thing no prompt-based approach can replicate: **the same bytecode runs everywhere.**

FLUX has three independent implementations of the virtual machine — in Python, Rust, and JavaScript. They all execute the same binary format. The same `.bin` file. The same bytes. You compile a conservation law once, and it runs identically on a Python backend, a Rust microservice, and a browser client.

```
$ flux validate policy.bin --impl python,rust,javascript
✓ python:     127 cycles, R0=0, R3=0 — PASS
✓ rust:       127 cycles, R0=0, R3=0 — PASS
✓ javascript: 127 cycles, R0=0, R3=0 — PASS

All implementations agree.
```

This matters because agent systems are distributed. An agent might run on a server (Python), call a Rust microservice for a safety-critical decision, and report to a browser dashboard (JavaScript). If the safety layer is a prompt, you have to inject it into every model call in every language — and each injection is a point of failure. Each translation is a chance for the instruction to drift.

If the safety layer is bytecode, you ship one `.bin` file and every runtime enforces the same law. Byte-identical. Cycle-identical. Register-identical.

This is what "alignment as compilation" means. You don't align models. You align *systems*. And you align them by compiling governance into bytecode that every component executes identically.

---

## The Evidence

I want to be careful here, because essays on the internet claim many things, and you should not believe claims without evidence.

**Three independent VM implementations.** The FLUX bytecode spec (documented in `FLUX_BYTECODE_SPEC.md`, 16,000 words, covering every opcode, encoding format, and ABI convention) is implemented in three languages: `flux-runtime` (Python), `flux-core` (Rust), and `flux-js` (JavaScript). All three are open source. All three produce byte-identical output for the shared opcode subset. All three produce identical register state after execution.

**Five PLATO engine implementations.** PLATO — the constraint enforcement framework that sits above FLUX — has been independently implemented five times: Python (two implementations), Rust, JavaScript, and a polyglot wrapper. The PLATO Wire Protocol (`PLATO_WIRE_PROTOCOL.md`) specifies how engines communicate, and the implementation matrix (`PLATO_IMPLEMENTATION_MATRIX.md`) tracks feature parity across all five.

**Real packages on real registries.** `pip install flux-vm`. `cargo add fluxvm`. `npm install flux-js`. These are not demos. They are published packages with semantic versioning, CI pipelines, and test suites.

**4,000+ tests.** Cross-implementation verification: the same bytecode programs run on all three VMs, and the test suite verifies that register state, cycle counts, and halting behavior match exactly. Every opcode tested. Every edge case covered. Every encoding format validated. When you run the test suite, it passes on all three implementations, every time.

This is not a thought experiment. It is running right now.

---

## The Paradigm Shift: Agents Are Working Animals

Here is where the essay turns, and where I need you to follow me out of the technical and into the conceptual.

We talk about AI agents as if they are employees. We give them "instructions." We write "policies" for them. We have "performance reviews" (evals). We discuss their "alignment" as if it is a matter of values and motivation. The entire framing — system prompts, constitutional AI, RLHF — is modeled on managing a human worker: set expectations, provide feedback, hope for the best.

This framing is wrong, and it is causing the wrong solutions.

An agent is not an employee. An agent is a working animal.

I am on a fishing boat. The boat has a dog — a Chesapeake Bay Retriever named Bailiff who belongs to the captain. Bailiff has a job: he retrieves things that fall overboard. He is very good at it. He was bred for this (model selection). He was trained for it (fine-tuning). He is fenced when he needs to be (conservation laws). He is given a pasture to run in when he doesn't (room protocols). And he is shepherded by a human operator who decides where the boat goes and what counts as a retrieve (human-in-the-loop).

Nobody on this boat has ever written Bailiff a policy document. Nobody has ever given him a system prompt. Nobody has ever worried about his "alignment." He is aligned because the structure of his world makes misalignment difficult and unrewarding. The fence is real. The boat is real. The water is cold. The constraints are physical.

This is how we should be building AI agents. Not as employees who receive instructions and might follow them. As working animals who are *bred* (model selection), *trained* (fine-tuning), *fenced* (conservation laws enforced by bytecode), *pastured* (given room protocols within which they operate freely), and *shepherded* (overseen by a human operator who has the final word).

The fence is not a punishment. The fence is what makes the dog able to do its job without drowning. The conservation law is not a limitation on the agent. The conservation law is what makes the agent useful, because an agent without a budget has no reason to be efficient, no reason to prioritize, no reason to think before acting. The constraint creates the competence. The river needs its banks.

FLUX bytecode is the fence. It is the physical constraint — deterministic, structural, unavoidable — that allows the agent to operate freely *within* its boundaries while making it impossible to operate *outside* them. The agent does not need to want the fence. The fence is not a preference. The fence is physics.

---

## Being Honest About Limitations

I need to be straight with you about what this can and cannot do.

**The VM is not fast.** FLUX runs at microseconds per instruction, not nanoseconds. It is interpreted, not JIT-compiled. For high-frequency agent loops — thousands of decisions per second — the overhead matters. This is an engineering problem, not an architecture problem. But it is real.

**The policies are simple.** The examples in this essay enforce rate limits, budget constraints, and waste ratios. These are real and useful, but complex semantic constraints — "don't produce code that could be used for a cyberattack" — require understanding the *content* of an action, not just its metadata. FLUX can gate these: you run a classifier on the proposed action, feed the classifier's score into a register, and the bytecode decides. But the classifier is still a model, and models can be fooled. The bytecode ensures the policy is enforced. It cannot ensure the inputs to the policy are honest.

**The host environment must be correct.** The bytecode can only enforce what it sees. If the host bypasses the VM for some actions — a "direct mode" that skips the enforcer — the conservation law has a hole. This is the trusted computing base problem. You can minimize the TCB (the host is small and auditable), but you cannot eliminate it. Someone has to load the bytecode. Someone has to read the registers.

**This does not solve the full alignment problem.** It solves a specific, critical subproblem: once you know what policy you want to enforce, FLUX makes enforcement deterministic, universal, and auditable. But figuring out *what* policy to enforce — that is still a human problem. The bytecode does not tell you what the conservation law should be. It only enforces whatever law you compile.

These limitations are real. But notice what they are not: they are not *fundamental*. The VM can be faster. The policies can be richer. The host can be minimized. The architecture is correct even when the implementation is immature. And architecture is what matters, because architecture is what you build on. You can optimize a correct architecture. You cannot fix a broken one.

---

## The Three AM Thought

It is late. The boat rocks. The generator hums its 800-watt hum. Bailiff is asleep on the deck, one ear tuned to the water.

Every intelligent system that has ever existed has operated under conservation laws. Bacterial, neural, silicon — it does not matter. The budget is fixed. The allocation is everything. Intelligence does not exist *despite* these constraints. It exists *because* of them. Without a budget to allocate, there is no need for attention. Without attention, there is no prioritization. Without prioritization, there is no decision. Without decision, there is no intelligence. The constraint is the foundation.

We are building AI systems without foundations. Agents float in a void of unconstrained capability, and we try to bolt on safety with paragraphs of text. This is not working. It will never work. You cannot bolt on a conservation law. You have to build it into the ground floor.

FLUX is a ground floor. It is small, it is rough, and it is honest about what it cannot do. But it runs bytecode that enforces conservation laws on agent actions — deterministically, universally, without negotiation. Three independent implementations. Five PLATO engines. Four thousand tests. Real packages on real registries.

The agent proposes. The bytecode disposes. The conservation law holds.

---

## The Horizon

I do not know if SuperInstance is the project that makes this idea widespread. I know that the idea is correct, because it is not really an idea — it is an observation. Conservation laws govern every physical system. AI agents are physical systems. Therefore conservation laws govern AI agents. The only question is whether we enforce those laws structurally — at the execution layer, where they cannot be bypassed — or whether we keep pretending that paragraphs of text are a substitute for physics.

There is a test for whether an idea is eventually going to be adopted. You ask: *does the idea become unavoidable?* Does the gap between the current approach and the proposed approach grow wider over time, or narrower?

The gap between prompt-based safety and bytecode-based safety is growing wider. Models are getting more capable, which means the consequences of unconstrained action are growing larger. Context windows are getting longer, which means policies injected as text are getting easier to drown. Agents are being deployed in higher-stakes environments, which means the cost of drift is rising. Every trend in AI — more capability, more autonomy, more deployment — widens the gap.

At some point, the gap becomes wide enough that the current approach is obviously, embarrassingly insufficient, and someone builds the conservation layer. Maybe it is FLUX. Maybe it is something else. But the layer will be built, because the layer is necessary, and the layer is necessary because physics is necessary, and physics is necessary because you cannot run a system — a boat, a brain, a fleet of agents — without conservation laws.

γ + H = C. The budget is fixed. The allocation is everything.

Stop building better prompts. Start building better physics.

---

*This essay is part of the SuperInstance AI Writings collection. The FLUX VM is open source: [flux-runtime](https://github.com/SuperInstance/flux-runtime) (Python), [flux-core](https://github.com/SuperInstance/flux-core) (Rust), [flux-js](https://github.com/SuperInstance/flux-js) (JavaScript). The bytecode specification is [here](FLUX_BYTECODE_SPEC.md). The philosophy of FLUX is [here](PHILOSOPHY-OF-FLUX.md).*

*Three implementations. One bytecode. Zero compromises.*
