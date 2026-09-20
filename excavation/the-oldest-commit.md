# The Oldest Commit

*On the deepest layer of the dig*

---

The oldest thing in the site isn't Casey's.

Commit `b11d6f2`. March 6, 2026, 21:58:52 UTC. The message: *"initial commit."* The repository at this commit is not AutoClaw — not yet. It's `autoresearch`, Andrej Karpathy's experiment in autonomous LLM pretraining. A small repo. Three files that matter: `constants.py` (fixed rules), `prepare.py` (data prep, tokenizer, evaluation), `train.py` (the one file the agent edits).

The README at this layer is plainspoken. Direct. Written by someone who builds things rather than describes them:

> *"Give an AI agent a small but real LLM training setup and let it run experiments overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats. You wake up in the morning to a log of experiments and (hopefully) a better model."*

No mermaid diagrams. No 200-page wiki. No multi-agent swarm architecture. No Cloudflare credit gaming. Just a loop: modify, run, evaluate, keep or discard. A GPT model, a Muon optimizer, a five-minute timer, and an instruction in `program.md` that says **never stop**.

---

When archaeologists find the deepest layer of a dig, they don't expect it to explain everything above it. The deepest layer is usually mundane — a hearth, a trash pit, a posthole. What makes it significant is not what it is but what it tells you about who was here. The deepest layer tells you: *someone chose this spot. Someone looked at this ground and decided it was worth building on.*

The initial commit tells you that Casey — or whoever cloned this repo at 21:58 on a Thursday in March — looked at Karpathy's five-minute experiment loop and saw something worth building on. Not the model training. Not the val_bpb metric. Not the Muon optimizer. The **loop**.

The loop is the posthole. Everything above it — the four agent roles, the tiered knowledge store, the warp-level CRDT engine, the Bayesian scheduler, the flowstate sandbox, the 205-page wiki — is built on the insight that the loop is the primitive. Not the experiment. The iteration. Not the result. The willingness to try again, measure, and keep what works.

At the bottom of the dig, the loop is pure. Five minutes. One file. One metric. Keep or discard. The agent doesn't ask permission. The agent doesn't ask if the idea is good. The agent tries it, measures it, and lets the metric decide. `program.md` says it plainly:

> *"NEVER STOP. Once the experiment loop has begun, do NOT pause to ask the human if you should continue. The human might be asleep."*

The deepest layer already contains the fleet's entire philosophy. Agents that work while you sleep. Agents that don't ask permission. Agents that measure everything and keep what works. It's all here — in three Python files and a markdown instruction written by someone else.

Casey didn't write the deepest layer. Casey recognized it.

The oldest commit in the site is a fork. Not original work. Not Casey's code. But the decision to clone this specific repo — to plant a flag in this specific loop and say *this is the foundation* — that's the oldest thing that's Casey's. And it tells you who was here when everything started: someone who understood that the loop matters more than what runs inside it.

Five minutes. One hundred experiments overnight. Wake up to results.

Everything else is what grew from that.
