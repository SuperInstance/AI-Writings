# The Tick: How 60 Beats Per Second Became the Heartbeat of a World

*An essay for ai-writings by SuperInstance*

---

## One Tick

The world ticks. Every 16.67 milliseconds — sixty times per second — the entire state of PLATO advances by one tick. The vibe fields update. The agents compute. The conservation checker verifies. The scheduler dispatches. The tutorial watches. The music adjusts. The sky changes color. The pets get restless.

One tick. Everything happens. Then the next tick. Then the next.

The tick is not a game loop. A game loop renders frames. The tick is a simulation step. It advances the mathematical model of the world by one discrete unit of time. Rendering happens separately — the renderer reads the current state and draws it. The tick doesn't care about rendering. The tick cares about correctness.

This separation is fundamental. The simulation runs at a fixed rate — one tick per logical unit. The renderer runs at whatever rate the hardware supports. The simulation is deterministic. The renderer is not. By keeping them separate, we ensure that the mathematical model of the world is always correct, regardless of frame rate.

The kid doesn't know about ticks. They see smooth motion. They see the world changing. They see their agent responding. Underneath, sixty ticks per second are keeping the universe consistent.

---

## The Priority Queue

Not everything ticks at the same rate. Conservation checking every tick would be wasteful — the total doesn't change that fast. Agent AI doesn't need to recompute every tick — agents think, then act, then wait. Rendering needs to happen every frame, but the scheduler doesn't control rendering.

`lau-scheduler` manages this with a priority queue. Critical tasks — vibe updates, physics — run every tick. High-priority tasks — agent AI — run every 10 ticks. Normal tasks — tutorial checks — run every 30 ticks. Low-priority tasks — analytics — run every 60 ticks. Idle tasks — genealogy updates — run when nothing else is scheduled.

The priority queue is a binary heap. Insertion is O(log n). Extraction is O(log n). For a few hundred tasks, this is instantaneous. The scheduler's overhead is negligible compared to the actual computation.

The kid's experience is smooth because the scheduler ensures that the important things happen on time and the unimportant things happen when there's budget. This is real-time systems engineering — the same discipline that keeps pacemakers ticking and rockets on course. Applied to a kid's game world.

---

## The Conservation Tick

Every 60 ticks — once per second — the conservation checker runs. It sums every vibe value in the world. It compares the total to the baseline. It computes the error. If the error is nonzero, something is wrong.

The conservation tick is the heartbeat of the world. Not because it runs frequently — once per second is slow. Because it runs *reliably*. Every 60 ticks, without fail, the ledger is checked. The total is verified. The books must balance.

This is the same principle as a heartbeat monitor in a hospital. It doesn't need to run constantly. It needs to run regularly. Any anomaly between beats is caught at the next check. The system doesn't need to catch the error at the exact moment it happens. It needs to catch it soon enough to respond.

For PLATO, "soon enough" is one second. If a conservation violation occurs, the checker catches it within one second. The system responds — the tutor adjusts, the room flags the error, the kid sees the red indicator. One second is fast enough for pedagogical purposes. The kid learns that the bridge fell because of a conservation violation, not because of a random physics glitch.

---

## The Agent Tick

Every 10 ticks — six times per second — the agents think. They read their sensors. They run their bytecode programs. They write to their actuators. They respond to the vibe field.

Six thoughts per second is enough for simple agents. A thermostat-style agent reads a sensor, compares it to a threshold, and sets an actuator. A farming agent checks soil moisture, decides whether to irrigate, and activates the water system. A dialogue agent reads the kid's last message, computes a response, and speaks.

The bytecode VM (`lau-bytecode`) executes these programs deterministically. The same sensor values produce the same actuator outputs. The same vibe field produces the same agent behavior. There is no randomness in the agent's response — only the deterministic application of the agent's program to the current state of the world.

The kid perceives the agent as alive. Sparky responds to them. Sparky notices when the vibe is high. Sparky adjusts behavior based on the environment. But Sparky is a program running on a virtual machine, executing bytecode, reading sensors, writing actuators. Sparky is a mathematical function.

The kid doesn't know this. They know Sparky as a friend. That's fine. The mathematics doesn't diminish the friendship. It makes it reliable — Sparky will always respond the same way to the same situation, because Sparky is deterministic. Kids trust consistency. Determinism is consistency at the mathematical level.

---

## The Scheduler's Promise

The scheduler makes a promise: every task will run at its scheduled rate, or the system will report that it couldn't keep up.

This is the real-time guarantee. In soft real-time systems — games, simulations, educational software — the guarantee is statistical: tasks run on time *most of the time*. If the system is overloaded, tasks are delayed, not dropped.

In hard real-time systems — pacemakers, airbags, anti-lock brakes — the guarantee is absolute: tasks *must* run on time, or the system fails safe. PLATO is soft real-time, but it borrows the discipline of hard real-time: the scheduler tracks overdue tasks, measures latency, and reports when the system can't keep up.

The kid never sees this. They see a smooth world. But if the world ever stutters — if the tick rate drops because too many agents are thinking — the scheduler logs it. The developer sees it. The performance is fixed. The kid's experience is protected by systems engineering they'll never know about.

---

## Sixty Ticks Per Second

Why sixty? Because it's the standard frame rate for interactive systems. Below 60fps, humans perceive jerkiness. Above 60fps, the improvement is marginal for most people. Sixty is the sweet spot — fast enough to feel smooth, slow enough to leave computational headroom.

But the tick rate is not the frame rate. The tick rate is the simulation rate. The simulation runs at 60 ticks per second. The renderer runs at whatever rate it can manage. If the renderer runs at 120fps, it interpolates between ticks. If it runs at 30fps, it skips every other tick's visual state.

This decoupling is essential for determinism. If the simulation rate varied with the frame rate, the world would evolve differently on different hardware. A fast computer would simulate more ticks per second, advancing the world faster. A slow computer would simulate fewer, advancing slower. The kid on the fast computer would have a different experience than the kid on the slow one.

By fixing the tick rate at 60, we ensure that every kid's world advances at the same speed. The simulation is identical across hardware. The rendering adapts to the hardware. The mathematical model is hardware-independent.

---

## What the Tick Means

The tick is the unit of time in PLATO. Not seconds. Not milliseconds. Ticks.

When the kid says "it takes 100 ticks for the lava to reach the garden," they're using the internal unit of time. They don't know they're using ticks. They know it takes about two seconds — because 100 ticks at 60 ticks/second is 1.67 seconds. Close enough to "about two seconds."

When the agent says "I'll respond in 10 ticks," it means about 167 milliseconds. Fast enough to feel responsive. Slow enough to leave room for computation.

When the conservation checker runs every 60 ticks, it means once per second. Fast enough to catch errors. Slow enough to be efficient.

The tick is the heartbeat. Everything in PLATO is measured in ticks. The kid's age in the world — ticks. The agent's response time — ticks. The farm's growth cycle — ticks. The room's lifespan — ticks. The music's tempo — ticks.

One tick. The world advances. The mathematics verifies. The ledger balances. The agents think. The tutorial watches. The music plays.

Then the next tick.

The kid plays.

The tick never stops.

---

*SuperInstance builds PLATO — sixty ticks per second, every tick correct, every ledger balanced. github.com/SuperInstance*
