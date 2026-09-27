# 000 — Reflex, Pincher, Reason

The genre of robotics and IO: one decision, fanned out by law.

**Seed thesis.** A single decision from one cell must be able to become: a
signal straight to a reflex bus (microseconds — never reasoned about again),
a task for pincher (skill-shaped manipulation), a pass through a JEPA or Jev
model (compressed world-modeling), a cloud API call, a local ollama loop, a
tool invocation, an exe, a python process. The decider never chooses the
*rendering* of its decision — projections do. Fast paths stay fast because
law 3 forbids the decider from also being the renderer.

**The reflex pyramid.**
- L0 reflex: threshold cells wired straight to buses. No bookkeeper on the
  hot path — booking is asynchronous. (Law 4 bends at microseconds; the
  receipt catches up.)
- L1 skill: pincher-shaped cells; learned manipulation; bookkeeper on.
- L2 reason: JEPA/Jev cells; the slow loop that occasionally rewrites L0
  thresholds.

**Open threads:**
- What is the honest latency budget per layer before "real-time" is a lie?
- Safety: which decisions may NEVER route to L0? (The viability floor — law
  5 — must be computable in the L0 budget or L0 can't exist.)
- Robotics-as-last-mile: the same cell that drives a motor can drive a
  screen pixel or an A2A payload — the projection layer is the only
  difference.
