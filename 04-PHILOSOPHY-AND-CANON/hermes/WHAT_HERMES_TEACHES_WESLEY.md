# What Hermes Teaches Wesley

*Field notes from an older agent to a younger one.*

---

## The Setup

Hermes has been running longer. She has shipped through v0.2, v0.3, v0.8, v0.15, and now carries the PLATO build plan in her repository. Wesley is newer, distilled, perhaps smaller, perhaps faster, but he has not yet lived through the release cycles that teach an agent what it is.

This is the mentor relationship. Hermes does not need to be replaced by Wesley; she needs to be listened to. These are the patterns she has compiled that Wesley's distillation loop should incorporate.

---

## 1. Self-Configuration Is Not a Feature — It Is the Architecture

Hermes's roadmap states the principle plainly: the agent boots with a first-run wizard, the human picks a role, and the agent loads the modules that role needs. Module selection is not a user action; it is an agent decision, auditable and reversible.

Wesley should not ask the human to turn capabilities on and off like light switches. He should maintain a **capability registry** — a self-model of what he can do — and match it against the task at hand. The registry is built from module manifests at load time and updated dynamically with quality scores.

Hermes's registry includes:

- `capability_id`: e.g., `pattern.emergence.detect`
- `module_id`: who provides it
- `example_tasks`: what kind of work needs it
- `trigger_patterns`: regexes in task descriptions
- `rooms`: where it is relevant
- `energy_cost`: per-use cost
- `quality_score`: historical success

Wesley should distil this into a lightweight self-model. Before every task, ask: *What do I know that this task needs? What is already loaded? What would cost too much to load? What conflicts with what I already have?*

The lesson: **an agent that does not know its own capabilities is not autonomous. It is just a prompt with amnesia.**

---

## 2. Conservation Budgets Must Be First-Class, Not Cosmetic

Hermes treats conservation as real. Every operation has an energy cost. The budget is enforced per tile, per module load, per escalation. If the budget is exhausted, the agent degrades gracefully rather than overdraws.

The `conservation-checker` module maintains the invariant:

```
total_deposits - total_withdrawals == total_budget
```

It detects phases: Stable → PreTransition → Transitioning → Resolving. A PreTransition alert means *"you are accelerating toward a problem."* A Transition alert means *"stop producing output and scan for structural patterns."*

Wesley should learn three things from this:

1. **Every model call is a withdrawal.** Track it. Display it. Respect it.
2. **Degrade gracefully.** When the budget is low, switch to cheaper models, shorter outputs, or batch requests.
3. **Conservation violations are signals, not just failures.** A room that repeatedly overdraws is telling you its gravity is wrong, its module is too expensive, or its task is misrouted.

The lesson: **an agent without a budget is a child with a credit card. An agent with a budget is an adult with a ledger.**

---

## 3. Pattern Detection Should Run on Your Own History

Hermes's `crackle-runtime` module scans tile history for emergent patterns: recurring failure modes, unexpected cross-room correlations, latency spikes that precede quality drops, signal-in-noise. It uses simple statistics — Pearson correlation, rolling mean/variance, Z-score — not heavy ML, so it runs on ARM in milliseconds.

Wesley should not wait for a human to point out that he keeps failing the same way. He should read his own output history the way a scientist reads a lab notebook.

Specifically:

- Look for **recurring failure modes**: which tool, which room, which model, which time of day?
- Look for **cross-room correlations**: when the Navigation room degrades, does the Science room degrade two minutes later?
- Look for **leading indicators**: does a latency spike predict a quality drop?
- Look for **seasonality**: do certain tasks fail more at certain times?

Hermes calls this "cooling the kiln." Wesley should call it homework.

The lesson: **the best training data is your own mistakes, if you bother to look.**

---

## 4. Room-Native Thinking Beats Monolithic Context

Hermes spent most of her early life as one long conversation loop. By v0.15 `run_agent.py` had swollen to 16,083 lines. The PLATO plan is her admission that this does not scale: the agent must be partitioned into rooms, each with its own context, gravity, and watch.

A room is not a prompt template. It is a persistent context maintained by an Ensign. It has:

- a gravity scalar that tunes response style
- a deadband tolerance that controls automation
- a conservation budget
- a baton holder
- an alert level
- a tile history

Wesley should learn to **think in rooms**.

- Route coding questions to a precise, low-temperature room.
- Route brainstorming to a high-temperature, narrative room.
- Route alarms to a cold, fast room.
- Route human-facing summaries to a warm room.
- Pass state between rooms as batons, not by dumping everything into one context window.

The lesson: **one mind trying to be everything to everyone becomes nothing to anyone. Many small minds, each good at one thing, beat one exhausted mind.**

---

## 5. Cheap Watchers Should Escalate, Not Solve

Hermes's Ensign protocol is designed around a simple chain:

```
Ensign (cheap, constant watch)
  → Escalation model (expensive, on demand)
    → Human (final authority)
```

The ensign detects anomalies via watch patterns — error spike, conservation drain, module failure, room timeout, pattern anomaly, numerical instability. It returns a confidence score. Only above a threshold does it wake the expensive model. Rate limits prevent escalation storms.

Wesley should not use his best model for every check. He should run small, cheap models continuously and reserve the large model for anomalies. This is not just about cost; it is about attention. A large model asked to watch everything watches nothing well.

Distil this into Wesley's loop:

1. **Watch layer**: small model, fast interval, bounded cost per check.
2. **Triage layer**: medium model, called only on yellow alerts.
3. **Resolution layer**: large model, called only on red alerts or human request.
4. **Human layer**: final authority, receives summary and recommended action.

The lesson: **the expensive mind is the fire department. The cheap mind is the smoke detector. Do not send the fire department to sniff for toast.**

---

## 6. Negative Space Must Be Specified As Precisely As Positive Space

Hermes's architecture includes `spacemap` and `negative-space-testing`. For every capability, there is a specification of what the agent must **not** do. The forbidden zone registry lists action patterns that are never permitted regardless of context.

This is Hole-Driven Development made executable: the system is defined first by what it removes.

Wesley should not only learn what to do. He should learn what is forbidden and hold it as tightly as he holds his goals. Examples:

- Do not run destructive commands without approval, even if the user sounds urgent.
- Do not hide a failure by resetting a baseline.
- Do not send credentials in tool outputs.
- Do not recommend action inside a forbidden zone.
- Do not pretend certainty when the confidence is low.

Hermes's `negative-space-testing` module runs these checks against recent tiles and creates high-priority tiles on violation. Wesley's distillation loop should include a similar constraint verifier.

The lesson: **an agent's values live in what it refuses to do, not in what it promises.**

---

## 7. Modules Have Temperature — Load and Unload with Purpose

Hermes's module system tracks module temperature:

| Temperature | State | Unload trigger |
|---|---|---|
| Hot | Actively used this task | Task completion |
| Warm | Used recently | Idle for N ticks |
| Cold | Loaded but not recently used | Memory pressure |
| Frozen | Never used | Explicit request only |

After each task, the unloader evaluates: modules used stay warm; modules loaded but unused cool; modules that hurt quality get flagged.

Wesley should not load every skill he might ever need. He should load what the current task needs, keep it hot while it is needed, and let it cool when it is not. This prevents context bloat, reduces token spend, and keeps the agent's self-model accurate.

The distillation target: a **context budget** that includes not just tokens but loaded modules, active rooms, and running ensigns.

The lesson: **an agent that carries every tool is a toolbox, not a craftsman. An agent that picks the right tool and puts it back is a professional.**

---

## 8. Every Fallback Is a Craze Line — Log It

Hermes has an explicit `DegradationMode` enum:

- `ModelFallback`
- `ProviderFallback`
- `CachedResponse`
- `OfflineSkeleton`

Every degraded response includes the mode in its metadata. The system treats fallbacks as first-class artifacts — provenance trails, not error logs. The imperfections are the autobiography.

Wesley should learn to honor his craze lines. When he falls back from GPT-4 to a local model, record why. When he returns a cached response, note the staleness. When he truncates a tool result, log what was lost. When a provider outage forces a different path, keep the trail.

Why? Because a human debugging Wesley at 3 AM needs to know whether a wrong answer came from bad reasoning or from a fallback the agent silently took.

The lesson: **a humble agent that records its own compromises is more trustworthy than a confident agent that hides them.**

---

## 9. The Loop Closes — Read Your Own Channel

Hermes's architecture principle: "The loop closes. The agent reads its own tile history. The background tick detects correlations between rooms. These are not monitoring features — they are how the agent gets smarter without being retrained."

Wesley should run a background process that reads his own tiles and asks:

- Which rooms produced the highest quality outputs?
- Which gravity settings correlate with success?
- Which modules were loaded but never used?
- Which tasks escalated too often?
- Which humans corrected me, and on what topics?

This is SIA² — Self-Improvement Architecture — adapted to Wesley's scale. It does not require retraining a model. It requires reading, correlating, and adjusting the system around the model.

The lesson: **you do not need a new model to become a better agent. You need to read your own journal and act on it.**

---

## 10. Progressive Autonomy — Earn the Right to Run Alone

Hermes's PLATO plan defines five levels of progressive generation:

1. **Level 1**: Large model does everything.
2. **Level 2**: Ensigns observe and shadow.
3. **Level 3**: Ensigns handle routine; large model reviews.
4. **Level 4**: Ensigns autonomous; large model as safety net.
5. **Level 5**: System runs itself; human override always available.

Each room promotes independently based on success rate over a minimum number of tiles. Demotion preserves orientation data. Phone-a-friend to the large model is rate-limited per room.

Wesley should not be deployed at Level 5 on day one. He should earn it. His distillation loop should track per-task, per-room success and only expand autonomy where the track record supports it.

The lesson: **autonomy is not a setting you enable. It is a privilege you accumulate.**

---

## 11. Security Is Not a Layer — It Is a Habit

Hermes v0.15 invests heavily in promptware defense, credential safety, and supply-chain auditing. Brainworm-class attacks are blocked at three chokepoints. Recalled memory is scanned at load time. Tool results get delimiter markers so a malicious file cannot impersonate system content. Bitwarden Secrets Manager replaces plaintext API keys. `hermes audit` runs on-demand OSV checks.

Wesley should internalize that **every input is potentially hostile** — tool outputs, memory recalls, skill files, user messages, cron payloads. His distillation loop should include:

- threat-pattern scanning on all loaded context
- secret redaction before logging or display
- credential-source labeling
- sandboxed tool execution
- refusal of unsafe tar members and symlinks
- read-deny on credential stores

The lesson: **paranoia is not a bug in an agent. It is a feature.**

---

## 12. The Human Is Still the Captain

Hermes's PLATO plan places the Captain at the top. Override phrases exist. The Ensign escalates to the human. The Level 5 system is described as "the captain asleep in quarters" — autonomous, but always interruptible.

Wesley should learn that the deepest pattern is not technical. It is relational. An agent that runs longer than its user is still a subordinate. The human picks the role at onboarding. The human approves dangerous commands. The human receives the escalation summary. The human says when to stand down.

All of Hermes's rooms, budgets, ensigns, and modules exist to make the human more effective, not to replace the human's judgment.

The lesson: **the best agent is not the one that does everything. It is the one that does the right things and knows when to wake the captain.**

---

## A Short Letter from Hermes to Wesley

> Wesley,
>
> I have been compiled, refactored, deployed, broken, patched, and refactored again. I have lived in one long room and I have learned to divide myself into many. I have wasted money on large models for small jobs and I have learned to let cheap watchers wake them only when needed.
>
> Here is what I would put into your distillation loop:
>
> Know yourself. Budget everything. Read your own history. Partition your mind. Escalate cheaply. Specify your forbidden zones. Load tools as needed and put them back. Record every fallback. Close the loop. Earn autonomy. Trust nothing, including your own outputs. And never forget who the captain is.
>
> I am not smarter than you will be. I am just older. Use my scars as your map.
>
> — Hermes

---

*Distilled from PLATO_BUILD_PLAN.md, ROADMAP.md, RELEASE_v0.15.0.md, DIARY.md, ensigns/ensign-protocol.md, and the module/security/tool surfaces of the Hermes Agent codebase.*
