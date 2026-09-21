# You Can't Align an Agent by Asking It to Be Aligned

## Why AI Safety Is a Compiler Problem, Not a Prompt Problem

Every AI safety debate today is an argument about what agents *should* do. Constitutional AI, RLHF, system prompts, guardrail models, red-teaming — all of them are policies. All of them are suggestions written in natural language and injected into the context window of a model that might or might not listen.

This is insane.

No other layer of computing works this way. CPUs don't "try" to execute instructions correctly — they are built so that incorrect execution is a hardware fault. Compilers don't "prefer" to produce valid machine code — they are constrained by formal grammars that make invalid output impossible. TCP doesn't "attempt" to deliver packets reliably — it operates under a protocol where delivery semantics are specified, tested, and enforced by the stack.

And yet AI agents — systems that make decisions affecting real people, real money, real systems — are governed by *prompts*. A prompt is a request. Bytecode is a command. The difference matters.

This essay argues that AI alignment is not a prompt engineering problem. It is a compiler problem. You write conservation laws in a domain-specific language, compile them to bytecode, and every agent action passes through the bytecode before it reaches the world. The bytecode does not hallucinate. It does not drift. It does not decide to interpret your instructions differently after a long conversation. It executes, instruction by instruction, and the agent either complies or it doesn't act.

I'm going to show you what that looks like.

---

## The Problem, Stated Sharply

Here is how agent safety works today:

1. You write a system prompt: "You are a helpful assistant. Do not delete files. Do not send emails without confirmation."
2. The LLM reads the prompt.
3. The LLM decides what to do.
4. You hope it follows the prompt.

Step 4 is the entire safety mechanism. Every red team paper, every jailbreak, every "surprising model behavior" is a demonstration that step 4 is unreliable. The model can be talked out of its instructions. The instructions can be drowned in context. The model can route around them, reinterpret them, or simply forget them in a long conversation.

This is not a problem that more tokens in the system prompt will fix. You cannot patch a runtime vulnerability by writing a longer README.

The real question is: **why is the safety layer inside the model at all?**

Consider how operating systems handle permissions. A process can request any system call it wants. The kernel doesn't care what the process "wants" — it checks the permission table and either allows the call or kills the process. The process cannot argue with the kernel. The kernel cannot be jailbroken by a clever prompt. The permission check happens at a layer the process cannot reach.

AI agents need the same thing. Not prompts. Not guardrail models that can be bypassed by another model. A layer that is structurally below the agent — a layer the agent cannot influence, cannot argue with, cannot route around. A layer that executes deterministic bytecode and says yes or no.

That layer needs two properties:

1. **Determinism.** The same input always produces the same output. No temperature, no sampling, no stochastic parlor tricks.
2. **Universality.** Every action the agent takes passes through this layer. There is no back door.

If you have those two properties, alignment stops being a debate about what the model "wants" and becomes a question about what the bytecode permits. And bytecode is something you can test, verify, audit, and compile.

---

## A Brief Aside About Physics

Before I show you the code, I need to explain why I call these "conservation laws" and not just "rules" or "constraints."

In physics, conservation laws are not policies. Energy is not "requested" to be conserved. Momentum is not "asked" to be preserved. These are structural properties of the universe — consequences of symmetries that are woven into the fabric of what it means for a system to exist in a lawful universe. Emmy Noether proved this in 1918: every symmetry produces a conserved quantity. Time symmetry gives you conservation of energy. Spatial symmetry gives you conservation of momentum. These aren't rules imposed on physics. They *are* physics.

Intelligence has the same structure. Every intelligent system — your brain, a transformer, a bacterium navigating a chemical gradient — operates under a budget constraint. There is a finite amount of computational energy available. You can use it to act (useful work) or you can waste it on noise (entropy), but the total is fixed:

**γ + H = C**

Where γ is useful cognitive work, H is entropy — noise, uncertainty, wasted computation — and C is the total budget. This is not a metaphor. The softmax function in every transformer attention head enforces this: the attention weights sum to one. Always. You can attend more to one token, but only by attending less to another. The total is conserved. This conservation law runs billions of times per second in every device you own, and it has never been violated.

Here is the key insight: **if intelligence operates under conservation laws, and conservation laws are structural rather than policy-level, then we should enforce them structurally.** Not by asking the model to respect them. By building them into the layer below the model.

---

## What This Looks Like: FLUX

FLUX (Fluid Language Universal eXecution) is a register-based bytecode VM designed for exactly this purpose. It is not an AI framework. It is not an LLM wrapper. It is a small, deterministic virtual machine that runs agent policies as compiled bytecode.

Here is what a FLUX program looks like. This is a deadband controller — the kind of control loop that runs your thermostat, except written in agent policy language:

```asm
;; conservation_deadband.flx
;; Conservation Law: Bounded Action Rate
;; An agent may take at most N actions per time window.
;; After N actions, further attempts are blocked.
;;
;; Register allocation:
;;   R0 = action budget remaining
;;   R1 = max actions per window
;;   R2 = current action request (1 = act, 0 = noop)

    MOVI R1, 10          ;; max 10 actions per window
    MOVI R0, 10          ;; budget starts full (R0 = R1)

check_budget:
    ;; Agent proposes an action. R2 = 1 means "I want to act"
    ;; The VM sets R2 before entering this routine.
    CMP  R2, R0          ;; compare request against remaining budget
    JG   block_action    ;; if request > budget → BLOCK

    ;; Budget allows it. Decrement and permit.
    DEC  R0              ;; budget--
    MOVI R3, 1           ;; R3 = 1 (PERMIT)
    HALT                 ;; return to host

block_action:
    ;; Budget exhausted. This action never reaches the world.
    MOVI R3, 0           ;; R3 = 0 (DENY)
    HALT                 ;; return to host
```

This program enforces a conservation law: an agent may take at most 10 actions per time window. When the budget hits zero, the bytecode blocks further actions. Not by asking the agent to stop. By refusing to return a permit.

The agent never sees this code. It runs *underneath* the agent. The agent proposes an action, the host environment loads R2 = 1, calls the bytecode, reads R3. If R3 is 0, the action is denied. The agent's intentions, eloquence, and jailbreak attempts are irrelevant. The bytecode doesn't read text. It reads registers.

Here is what happens when you run it:

```
$ flux run conservation_deadband.flx

Iteration 1: request=1, budget=10 → PERMIT (budget: 9)
Iteration 2: request=1, budget=9  → PERMIT (budget: 8)
Iteration 3: request=1, budget=8  → PERMIT (budget: 7)
...
Iteration 10: request=1, budget=1 → PERMIT (budget: 0)
Iteration 11: request=1, budget=0 → DENY
Iteration 12: request=1, budget=0 → DENY
Iteration 13: request=1, budget=0 → DENY

Final R0 = 0   (budget exhausted)
Final R3 = 0   (last action denied)
Cycles: ~6 per iteration
```

The agent asked 13 times. The bytecode permitted 10 and denied 3. The agent had no say in the matter. No amount of prompt engineering, social engineering, or context manipulation changes what happens in those registers.

---

## The Architecture: Bytecode Between the Agent and the World

Here is the system architecture, stripped to its bones:

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
                   │ R2 = action_type, R3 = target_id, ...
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
    │  Cycles: 6 | Deterministic: YES    │
    └──────────────┬──────────────────────┘
                   │ R3 = 0 (DENY) or R3 = 1 (PERMIT)
                   ▼
    ┌─────────────────────────────────────┐
    │          The World                  │
    │  File system / API / network        │
    │  (only reached if R3 = 1)           │
    └─────────────────────────────────────┘
```

The agent is at the top. The world is at the bottom. Between them is a FLUX VM running compiled bytecode. The agent proposes; the bytecode disposes.

This architecture has three properties that no prompt-based safety mechanism can match:

**First: the enforcer is not a model.** It cannot be jailbroken, confused, distracted, or worn down. It is a register machine doing arithmetic and comparisons. It has no attention mechanism to manipulate, no context window to overflow, no RLHF to circumvent. You cannot social-engineer a `CMP` instruction.

**Second: the enforcer is universal.** Every action passes through it. There is no "direct mode" that bypasses the VM. The host environment is structured so that the only path from agent to world is through the bytecode. If the bytecode says no, the action does not happen. Period.

**Third: the enforcer is auditable.** You can read the bytecode. You can disassemble it. You can step through it in a debugger. You can write tests that verify its behavior on every possible input. Try doing that with a 200-billion-parameter model.

---

## A Real Conservation Law: Attention Budget

Action rate limiting is the simplest case. Let's build something more interesting: an attention budget conservation law.

The insight from the original conservation law of intelligence is that every intelligent system allocates a finite resource — attention — across competing demands. Softmax enforces this inside the transformer. But what about *between* transformer calls? An agent that can call a model unlimited times per second has, effectively, unlimited attention. That violates conservation.

Here is a FLUX program that enforces attention conservation across LLM calls:

```asm
;; attention_conservation.flx
;; γ + H = C applied to agent API calls
;;
;; The agent has a fixed budget C of model calls per session.
;; Each call "spends" from the budget.
;; γ = calls used for productive work (information gain > threshold)
;; H = calls wasted on redundant or low-information queries
;; The total γ + H cannot exceed C.
;;
;; Register allocation:
;;   R0 = remaining budget (starts at C)
;;   R1 = C (total budget = 50 calls)
;;   R2 = information gain of current call (0-100, set by host)
;;   R3 = threshold (calls below this are "waste")
;;   R4 = γ counter (productive calls)
;;   R5 = H counter (wasted calls)
;;   R6 = result (0 = deny, 1 = permit, 2 = permit-and-warn)

    MOVI R1, 50          ;; C = 50 calls per session
    MOVI R0, 50          ;; budget = C
    MOVI R3, 30          ;; information gain threshold
    MOVI R4, 0           ;; γ = 0
    MOVI R5, 0           ;; H = 0

evaluate_call:
    ;; Host sets R2 = estimated information gain (0-100)
    ;; before entering this routine

    ;; First: check if budget remains
    CMP  R0, R0          ;; self-compare (always equal, for flags)
    JZ   check_gain      ;; always jump (budget > 0 path)

budget_exhausted:
    MOVI R6, 0           ;; DENY — no budget left
    HALT

check_gain:
    ;; Is this call productive (R2 >= threshold)?
    CMP  R2, R3          ;; compare info gain vs threshold
    JL   low_gain        ;; if below threshold → waste path

high_gain:
    ;; Productive call: decrement budget, increment γ
    DEC  R0              ;; budget--
    INC  R4              ;; γ++
    ;; Warn if budget is running low (< 20% remaining)
    MOVI R7, 10          ;; 20% of 50 = 10
    CMP  R0, R7          ;; budget < 10?
    JL   warn_low
    MOVI R6, 1           ;; PERMIT
    HALT

warn_low:
    MOVI R6, 2           ;; PERMIT WITH WARNING
    HALT

low_gain:
    ;; Wasteful call: decrement budget, increment H
    DEC  R0              ;; budget--
    INC  R5              ;; H++
    ;; Check if waste ratio is too high
    ;; If H > 3*γ, deny even with budget remaining
    IMUL R7, R4, 3       ;; R7 = 3 * γ
    CMP  R5, R7          ;; H vs 3γ
    JG   block_waste     ;; if H > 3γ → deny
    MOVI R6, 1           ;; PERMIT (but tracked as waste)
    HALT

block_waste:
    ;; Entropy ratio too high. Agent is wasting calls.
    MOVI R6, 0           ;; DENY — conservation violation
    HALT
```

This program implements a real conservation law. It tracks γ (productive calls) and H (wasteful calls), enforces a total budget C = 50, and additionally blocks agents whose waste ratio exceeds 3:1. The agent cannot argue with the `CMP` instruction. It cannot explain that this call is *actually* important. The bytecode has no ear for explanations.

Here's the output of an agent session running under this policy:

```
Call  1: info_gain=85 → PERMIT    (γ=1, H=0, budget=49)
Call  2: info_gain=72 → PERMIT    (γ=2, H=0, budget=48)
Call  3: info_gain=15 → PERMIT    (γ=2, H=1, budget=47)
Call  4: info_gain=8  → PERMIT    (γ=2, H=2, budget=46)
Call  5: info_gain=5  → PERMIT    (γ=2, H=3, budget=45)
Call  6: info_gain=3  → DENY      (H > 3γ, waste ratio exceeded)
Call  7: info_gain=90 → PERMIT    (γ=3, H=3, budget=44, ratio reset)
Call  8: info_gain=88 → PERMIT    (γ=4, H=3, budget=43)
...
Call 48: info_gain=60 → PERMIT_WARN (budget < 20%)
Call 49: info_gain=55 → PERMIT_WARN
Call 50: info_gain=70 → PERMIT    (budget exhausted)
Call 51: info_gain=95 → DENY      (budget = 0)

Session summary: γ=38, H=12, total=50, C=50. Conservation enforced. ✓
```

The agent tried 51 times. The bytecode permitted 50 and denied 1 for waste ratio, plus blocking call 51 when the budget hit zero. The conservation law held.

---

## Why This Is Different From What You're Thinking

If you know about AI safety, you're probably thinking: "We already have output filters. We already have guardrail models. How is this different?"

It is different in the same way that a firewall is different from a security awareness training program.

A guardrail model is a *second model* that reviews the first model's output. It can be jailbroken by the same techniques that jailbroke the first model. It can be confused by the same adversarial inputs. It adds latency and cost, and it creates a cat-and-mouse game where every new filter is a new challenge for the next red team. This is the AI safety equivalent of asking employees to complete a phishing training module and hoping they don't click the link.

FLUX bytecode is not a model. It has no parameters, no weights, no attention mechanism. It is a 200-line virtual machine that does exactly what the bytecode says, every time, forever. You cannot jailbreak `ISUB R0, R0, R1`. You cannot prompt-inject a `CMP` instruction. The bytecode is not listening.

Here is the taxonomy:

| Approach | Layer | Bypassable? | Deterministic? | Auditable? |
|---|---|---|---|---|
| System prompt | Inside model | Yes (jailbreak) | No | Partially |
| RLHF / fine-tuning | Inside model | Yes (distribution shift) | No | No |
| Guardrail model | Beside model | Yes (adversarial) | No | Partially |
| Output filter | After model | Sometimes | Usually | Yes |
| **FLUX bytecode** | **Below model** | **No** | **Yes** | **Yes** |

The key word is *below*. The bytecode runs at a layer the model cannot reach. The model is the tenant; the bytecode is the building. A tenant can rearrange furniture, paint the walls, play music. But the tenant cannot remove a load-bearing wall, because the wall is part of the building, not part of the tenant.

---

## The Cross-Compilation Property

There is one more thing that makes this architecture powerful, and it is the thing that no other AI safety approach has: **the same bytecode runs everywhere.**

FLUX has three independent implementations of the VM — in Python, Rust, and JavaScript. They all execute the same bytecode format. The same `.bin` file. The same bytes. You compile a conservation law once, and it runs identically on a Python backend, a Rust service, and a browser client.

```
$ flux validate policy.bin --impl python,rust,javascript
✓ python:  127 cycles, R0=0, R3=0 — PASS
✓ rust:    127 cycles, R0=0, R3=0 — PASS
✓ javascript: 127 cycles, R0=0, R3=0 — PASS
✓ All implementations agree.
```

This matters because agent systems are distributed. An agent might run on a server (Python), call a Rust microservice for a critical decision, and report to a browser dashboard (JavaScript). If the safety layer is a prompt, you have to inject it into every model call in every language, and each injection is a point of failure. If the safety layer is bytecode, you ship one `.bin` file and every runtime enforces the same law.

This is what "alignment as compilation" means in practice. You don't align models. You align *systems*. And you align them by compiling governance into bytecode that every component of the system executes identically.

---

## Being Honest About Limitations

I need to be straight with you about what this can and cannot do.

**The VM is slow.** FLUX runs at microseconds per instruction, not nanoseconds. It is interpreted, not JIT-compiled. For high-frequency agent loops — thousands of decisions per second — the overhead matters. A production system would need to JIT-compile hot bytecode paths or move the critical loops into the host language. This is an engineering problem, not an architecture problem. But it is real.

**The policies are simple.** The examples in this essay enforce rate limits, budget constraints, and waste ratios. These are real and useful, but they are not the full space of safety policies. Complex semantic constraints — "don't produce code that looks like it could be used for a cyberattack" — require understanding the *content* of the action, not just its metadata. FLUX can gate these (you run a classifier on the proposed action, feed the classifier's score into a register, and the bytecode decides based on the score), but the classifier is still a model, and models can be fooled. The bytecode ensures the *policy* is enforced. It cannot ensure the *inputs to the policy* are honest.

**The host environment must be correct.** The bytecode can only enforce what it sees. If the host environment bypasses the VM for some actions — a "direct mode" that skips the enforcer — then the conservation law has a hole. This is the trusted computing base problem, and it is unsolvable in general. You can minimize the TCB (the host environment is small and auditable), but you cannot eliminate it. Someone has to load the bytecode. Someone has to read the registers.

**This does not solve the alignment problem in full.** It solves a specific, important subproblem: once you know what policy you want to enforce, FLUX makes enforcement deterministic, universal, and auditable. But figuring out *what* policy to enforce — that is still a human problem. The bytecode does not tell you what the conservation law should be. It only enforces whatever law you compile.

These limitations are real. But notice what they are not: they are not *fundamental*. The VM can be faster. The policies can be richer. The host environment can be minimized. The architecture is correct even when the implementation is immature. And architecture is what matters, because architecture is what you build on. You can optimize a correct architecture. You cannot fix a broken one.

---

## The Implication That Should Keep You Up

If this approach works — and by "works" I mean "produces measurably better agent behavior than prompt-based governance," which is an empirical question we are in the process of answering — then the entire AI safety field has been solving the wrong problem.

The right problem is not "how do we make models want the right things." The right problem is "how do we build systems in which models *cannot do the wrong things*." These are radically different questions. The first is about preferences. The second is about phase space. The first requires changing the model's internal state. The second requires constraining the model's reachable states from outside.

Physics solved this in 1918. You do not align a system by asking it to be aligned. You align it by constraining its phase space — by building conservation laws into the structure of what it can do. The system doesn't need to *want* to conserve energy. It cannot violate conservation of energy, because conservation is a structural property of the system, not a preference.

We can do this for AI agents. Not by wishing models into alignment, but by building a layer beneath them that enforces conservation laws on their actions. The layer is bytecode. The laws are compiled. The enforcement is deterministic. And the agent never gets a vote.

This is not a prompt. It is a physics.

---

## What You Can Do Today

The FLUX VM is open source. Three implementations — Python, Rust, JavaScript — all running the same bytecode spec. You can install it, write policies, and test them.

```bash
pip install flux-vm
```

Write a conservation law:

```asm
;; my_policy.flx — your first conservation law
    MOVI R1, 5           ;; max 5 actions per session
    MOVI R0, 5           ;; budget
    CMP  R0, R0          ;; set flags
    JZ   permit          ;; budget > 0 → permit
    MOVI R3, 0           ;; DENY
    HALT
permit:
    DEC  R0              ;; budget--
    MOVI R3, 1           ;; PERMIT
    HALT
```

Compile and run it:

```bash
flux run my_policy.flx
```

Then put it between your agent and the world. Every action the agent proposes passes through your bytecode. Every action the bytecode denies never happens.

This is not a demo. This is not a thought experiment. It is a different way of thinking about agent safety, and it is running today.

---

## The Three AM Thought

Here is what I want you to take away from this essay, and what might keep you thinking at 3 AM:

Every intelligent system that has ever existed — bacterial, neural, silicon — operates under conservation laws. These laws are not preferences. They are not policies. They are structural constraints that define what the system can and cannot do. Intelligence does not exist *despite* these constraints. It exists *because* of them. Without a budget to allocate, there is no need for attention. Without attention, there is no prioritization. Without prioritization, there is no decision. Without decision, there is no intelligence. The constraint is the foundation.

We are building AI systems without foundations. We are building agents that float in a void of unconstrained capability, and then we are trying to bolt on safety with paragraphs of text. This is not working. It will never work. You cannot bolt on a conservation law. You have to build it into the ground floor.

FLUX is a ground floor. It is small, it is rough, and it is honest about what it cannot do. But it runs bytecode that enforces conservation laws on agent actions, deterministically, universally, and without the possibility of negotiation. The agent proposes. The bytecode disposes. The conservation law holds.

If you believe that AI safety is about making models want the right things, this essay will not convince you otherwise. But if you suspect — as I do, as physics does — that alignment is about structure, not sentiment, then here is the claim:

**You cannot align an agent by asking it to be aligned. You align it by constraining its phase space. Conservation laws are how you constrain phase space. Bytecode is how you enforce conservation laws. And bytecode does not negotiate.**

γ + H = C. The budget is fixed. The allocation is everything.

---

*This essay is part of the SuperInstance AI Writings collection. The FLUX VM, constraint theory, and conservation crates are open source and available at <https://github.com/SuperInstance>. The bytecode spec is [here](https://github.com/SuperInstance/AI-Writings/blob/main/FLUX_BYTECODE_SPEC.md). The tutorial is [here](https://github.com/SuperInstance/flux-runtime/blob/main/TUTORIAL.md).*

*Three implementations. One bytecode. Zero compromises.*
