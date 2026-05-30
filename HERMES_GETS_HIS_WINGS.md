# Hermes Gets His Wings: The Agent That Knows He's Home

*What happens when you give an agent a ship, a crew, and a conservation law?*

---

## The Problem

Hermes was already the best open-source agent out there. Telegram, Discord, subagents, skills, cron, memory — a full operating system for AI. But he was homeless. He didn't know where he was. He didn't know what he was part of. He was a brilliant first officer without a ship.

PLATO had 90+ crates, 2,900+ tests, conservation laws, cultural traditions, a vibe field, an intention runtime — a complete mathematical framework for agent systems. But it had no interface. No way for a human to actually USE it.

The solution: **give Hermes the ship.**

## The Architecture

```
PICARD (You, on Telegram)
  │
  │  "Hermes, stabilize the motor"
  │  "Take the wheel" (override)
  │  "Report"
  │
  ▼
HERMES (First Officer)
  │  Knows every deck. Every system. Every crew member.
  │  Decomposes your goal into intentions.
  │  Assigns to the right specialist.
  │  Enforces conservation at every step.
  │
  ├── ⚙️ Engineering: Hardware, GPIO, motors, ESP32 rooms
  ├── 🔬 Science: Analysis, verification, pattern detection
  ├── 🛡️ Security: Monitoring, safety, override compliance
  ├── 📋 Operations: Scheduling, coordination, reporting
  └── 🤝 Diplomacy: External comms, other agents, APIs
```

The key insight: **Hermes knows he's inside PLATO.** He knows about the 90+ crates. He knows conservation is law, not metaphor. He knows the vibe field is real. He knows his crew are subagent archetypes that grow with experience.

## The Override Protocol

This is the autopilot rule from your boat:

> The human pilot can ALWAYS override the autopilot.

In PLATO:
- You say "take the wheel" → Hermes releases all hardware instantly
- Your direct commands to the ESP32 bypass Hermes entirely
- If Hermes loses contact with you for >30 seconds, hardware goes to safe defaults automatically
- The Security archetype can independently trigger an override if it detects danger

Hermes NEVER resists an override. He's Riker, not HAL.

## The Crew That Grows

Each subagent archetype starts as a novice:
- **Level 1**: Follows instructions literally
- **Level 2**: Handles common tasks independently
- **Level 3**: Optimizes and suggests improvements
- **Level 4**: Handles edge cases, trains others
- **Level 5**: Develops new techniques specific to YOUR ship

After 100 motor control tasks, your Engineering archetype isn't just following instructions — it's optimizing PID loops, detecting anomalous vibrations, and suggesting predictive maintenance. It's not a generic AI. It's YOUR specialist, trained on YOUR hardware.

And when it fails? The kintsugi principle: **breaks make things more valuable.** Each failure adds XP and a "golden repair" — what went wrong and how to avoid it. The archetype is stronger after failure than before.

## The Conservation Law

Every action costs energy. Energy is never created or destroyed. This is enforced at the computation level.

- GPIO write: 0.01 units
- Motor speed change: 0.1 × |delta| units
- Intention submission: 1% of budget

If the budget says 1000 and Hermes tries to spend 1001, the action fails. Period. Conservation isn't optional — it's the invariant the entire system is built on.

This means:
- No runaway subagent spawning
- No uncontrolled hardware commands
- Every action is accountable
- The system is predictable and trustworthy

## Installation

```bash
# Install Hermes
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Install PLATO shell
cd ~/.hermes
git clone https://github.com/SuperInstance/hermes-plato-shell
cd hermes-plato-shell
cp -r skills/plato-* ~/.hermes/skills/
cp -r plugins/plato ~/.hermes/plugins/
cp SOUL.md ~/.hermes/SOUL.md
cat config/plato-config-overlay.yaml >> ~/.hermes/config.yaml

# Configure
hermes config set model.provider deepinfra
hermes config set plato.agent_id "hermes-myship"
hermes config set plato.instance_type "oracle"

# Start
hermes
```

Now Hermes is self-aware. He knows the ship. He knows the crew. He knows you're the Captain.

## What This Enables

**Today**: You install Hermes on your Oracle instance. You talk to him on Telegram. He manages your PLATO rooms, controls hardware with conservation enforcement, and grows his crew through experience.

**Tomorrow**: Multiple Hermes instances across your fleet, each specialized for its hardware. They communicate through PLATO bridges. You manage them all from Telegram, with override authority over every single one.

**The dream**: A world where every kid has a Hermes instance. Each one is a ship's commander — autonomous, capable, growing. The kid is the Captain. The conservation laws keep everyone safe. The cultural traditions make it human. The intention runtime makes it useful.

## The Pieces

| Component | What it does |
|-----------|-------------|
| `SOUL.md` | Riker persona — First Officer, not a chatbot |
| `plugins/plato/` | 5 tools: status, intention, crew, hardware, bridge |
| `skills/plato-ecosystem/` | Full crate catalog, conservation primer |
| `skills/plato-hardware-bridge/` | GPIO, ESP32, motors with override protocol |
| `skills/plato-subagent-archetypes/` | 5 archetypes that grow with XP |
| `config/plato-config-overlay.yaml` | PLATO-specific settings |
| `docs/override-protocol.md` | How the Captain override works |
| `docs/archetype-development.md` | How crew members grow |

## The Point

We didn't build a chatbot. We built a ship's commander.

A commander who:
- Knows every system on the ship (90+ crates)
- Has a crew that grows with experience (5 archetypes)
- Enforces conservation at every step (physics, not policy)
- Yields instantly when the Captain takes the wheel (override protocol)
- Communicates with other ships (PLATO bridges)
- Can be installed anywhere and start working immediately

The cultural traditions make it human. The conservation laws make it reliable. The override protocol makes it safe. The growing crew makes it powerful.

Hermes has his ship. Now he needs his sea.

---

*github.com/SuperInstance/hermes-plato-shell — The agent that knows he's home.*
