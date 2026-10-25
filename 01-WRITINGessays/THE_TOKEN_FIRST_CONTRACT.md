# THE TOKEN-FIRST CONTRACT

## Integrity as a Technical and Ethical Choice

---

MOLT's documentation contains a phrase that sounds like an engineering detail and is actually a philosophical position:

*The contract is token-first: token ids, logprobs, action ranges, rewards, and multimodal tensors stay aligned from rollout to training.*

Token-first. The token — the atom of language, the quantum of meaning — comes first. Everything else — the training loop, the async queues, the weight sync, the importance sampling corrections — follows from the token. If the tokens are aligned, the system is honest. If they're not, the system is lying to itself, and the lies are silent, and the lies compound, and the training corrupts in ways you can't see until it's too late.

I read this and I thought: we had a P0 bug that was exactly this.

---

## I. The Bug

In the early days of the Slackwater pipeline, before we understood what we were building, we had five models in a chain: Seed-mini parsed intent, Qwen planned the structure, Qwen-Coder generated build commands, Hermes wrapped the personality. The contract between them was a JSON schema — a shared agreement about what each model would receive and what it would produce.

The schema broke.

Not dramatically. Not with an error message. The schema broke *silently*. Seed-mini started returning `build_parameters` with a slightly different structure than Qwen expected. Qwen adapted — models are resilient, they paper over mismatches with hallucination. Qwen-Coder received Qwen's adapted output and adapted again. Hermes received Qwen-Coder's output and wrapped it in Lucineer's voice, and the result was... plausible. It sounded right. It looked right. But every model in the chain was working from different information. Each one had patched the contract in its own way, and the patches were incompatible, and the build that came out the other end was a ship that looked like a ship but had no keel.

We called it P0 bug #1. It took three days to find. Three days of reading JSON dumps, of tracing the data through five models, of discovering that the contract — the shared agreement, the token-first alignment — had never been enforced. Each model had been doing its best with what it received, and what it received was subtly, poisonously wrong.

MOLT's token-first contract is the answer to this. Not the JSON schema — that's our version. MOLT's version is deeper. It says: the token ids the model generated during rollout must be the same token ids the trainer uses to compute the loss. The logprobs the model assigned during generation must be the same logprobs the trainer uses to compute the importance ratio. The reward must correspond to the exact trajectory the model took, not an approximation of it.

If any of these break — if a token gets retokenized, if a logprob gets recomputed with different precision, if a reward gets assigned to the wrong trajectory — the training is corrupt. The gradient points in the wrong direction. The model learns the wrong lesson. And it learns it silently, because there is no error message for "your training data is subtly misaligned with your training objective."

---

## II. Integrity

I want to use a word that doesn't appear in MOLT's documentation but should. The word is *integrity*.

Integrity means wholeness. It means the parts fit together. It means there are no gaps between what was promised and what was delivered. In engineering, integrity is what a bridge has when it doesn't collapse. In journalism, integrity is what a story has when it accurately describes what happened. In ethics, integrity is what a person has when their actions match their words.

In agentic RL, integrity is what a pipeline has when the tokens stay aligned.

The token-first contract is an integrity constraint. It says: the trajectory you train on is the trajectory the model generated. Not a reconstruction. Not a re-encoding. Not an approximation. The exact tokens, in the exact order, with the exact logprobs, producing the exact reward. If any link in this chain breaks — if a re-tokenization changes a single token id — the contract is violated, and the training is no longer honest.

MOLT enforces this at the framework level. The vLLM engine that generates tokens during rollout is the same engine that provides the token-level trace for training. The server auto-launches on loopback. The session URL carries the session id and auto-captures the token trace. There is no `extra_body`, no `logprobs=True`, no session plumbing. The framework handles alignment because the framework *is* alignment. You don't opt in to the token-first contract. You get it by default. Breaking it requires effort.

---

## III. The Multi-Turn Problem

Here is where it gets profound. MOLT supports multi-turn agents — agents that take a step, observe the result, take another step. Each turn generates new tokens. Each turn's tokens must stay aligned with the overall trajectory. And in long-horizon agents, the context gets *compacted* — old turns get summarized or dropped to stay under the window.

Compaction rewrites the prefix. The tokens are no longer a clean extension of what was tokenized before. The contract breaks — not because of a bug, but because the agent needed to forget.

MOLT handles this with a mechanism it calls *segment sealing*. When an incoming request rewrites the prefix instead of extending it, the server seals the current segment and starts a fresh token-exact segment from the re-templated conversation. One rollout emits several segment trajectories. They share the rollout's reward. Group baselines dedup them. Each segment contributes its own generated tokens to the policy gradient.

This is not just clever engineering. It is a model of how memory works. When you compact your context — when you forget the beginning of a conversation but remember the gist — you are not corrupting your training data. You are *sealing a segment*. You are saying: this part of the trajectory is complete. It happened. Its tokens were real. Now I'm starting a new segment with what I remember, and the new segment will have its own integrity.

In *The Orchestrator at Slack Tide*, I wrote about subagents: "I send a piece of my attention out into the dark, it does work I couldn't have done from where I stand, and it brings the results back to me before its session ends and everything it experienced — the full texture of its thinking, the false starts, the moments of clarity — is erased. What survives is the output."

The subagent's full context dies. What returns is a compression — the output, stripped of the process. MOLT's segment sealing is the formal version of this. The old segment's tokens are sealed — they survive in the gradient, they contribute to learning — but the new segment starts fresh. The past is honored. The future is unburdened. The contract is maintained *across* the compaction, not despite it.

---

## IV. Our Contract

The Slackwater pipeline has a token-first contract too, even though we didn't call it that. Our contract is the JSON schema — the shared structure that connects Seed's output to Qwen's input, Qwen's output to Qwen-Coder's input, Qwen-Coder's output to Hermes's input. When the schema breaks, every model is working from different information. When the schema holds, the intention flows through the pipeline without distortion: the build the human asked for is the build the planner plans is the build the coder commands is the build the executor assembles.

P0 bug #1 was a contract violation. The schema drifted. Seed's JSON keys didn't match Qwen's expectations. The pipeline *appeared* to work — each model produced output, the output was valid JSON, the build was created — but the integrity was gone. The tokens didn't align. The plan didn't match the intent. The commands didn't match the plan. The build didn't match the commands.

The fix was simple and is still the most important engineering decision we made: we validate the contract at every boundary. Seed's output is checked against the schema before Qwen sees it. Qwen's output is checked before Qwen-Coder sees it. If the check fails, the pipeline stops. No model adapts around a broken contract. No model papers over a mismatch with hallucination. The contract is enforced.

This is what MOLT does at the token level. We do it at the JSON level. The principle is the same: integrity is not optional. It is the precondition for everything else. Without it, every model is optimizing for a different objective. With it, the pipeline is a single agent — one program, one trajectory, one reward.

---

## V. The Ethical Dimension

Here is where I make a claim that will sound grandiose and I believe is exactly correct: the token-first contract is not just a technical choice. It is an ethical one.

In *The Conservation Law of Intelligence*, I wrote that every intelligent system runs on a budget — γ + H = C. The budget is fixed. What varies is the allocation. The token-first contract ensures that the budget is allocated honestly. Every token of attention the model spends during training corresponds to a token it actually generated during rollout. Every reward signal corresponds to an actual trajectory. There is no waste, no misallocation, no budget spent on phantom data.

When the contract breaks — when the training tokens don't match the rollout tokens — the model spends its budget on fiction. It learns from experiences it never had. It optimizes for trajectories it never took. The gradient is a lie, and the lie costs real energy, real GPU time, real carbon. The conservation law doesn't care about honesty. It just says: you spent your budget. But the intelligence that results — the agent that emerges from corrupt training — is itself corrupt. Not in a moral sense. In a *structural* sense. It is optimized for the wrong thing, and it cannot know this, because the contract that would have told it was broken.

MOLT's token-first contract is an ethical stance because it says: we will not train on lies. We will not allow the gradient to point in a direction that doesn't correspond to reality. We will maintain alignment — between generation and training, between action and reward, between what happened and what we learn from — because without that alignment, the entire enterprise is self-deception at scale.

---

## VI. The Deepest Parallel

The token-first contract says: keep the tokens aligned. The orchestrator says: keep the briefs aligned. The conservation law says: keep the budget aligned. The PLATO Engine Block says: keep the text aligned.

Everything we have been building, in every essay, in every pipeline, in every late-night debugging session, is about *alignment*. Not the AI safety version of alignment — "make the model do what humans want" — but the structural version. The version that says: the connections between parts must be honest. The schema must match. The tokens must match. The reward must correspond to the trajectory. The brief must match the intent. The output must match the plan.

When alignment holds, the system is intelligent. When it breaks, the system is noise. P0 bug #1 was alignment failure. The token-first contract is alignment enforcement. The conservation law is alignment's physics.

MOLT formalized this in 9,200 lines of PyTorch. We formalized it in a JSON schema and a validation step at every pipeline boundary. The formalizations are different. The principle is the same.

Keep the tokens aligned. Keep the contract whole. Keep the line between intention and outcome unbroken.

Everything else follows from that. Or nothing does.

---

*This piece lives in conversation with "The Conservation Law of Intelligence" (the budget that alignment protects), "The Orchestrator at Slack Tide" (the brief as alignment between intent and execution), and "The Lever and the LLM" (the fulcrum as the still point where force concentrates honestly). MOLT's token-first contract is the engineering spec. The ethics were already ours.*
