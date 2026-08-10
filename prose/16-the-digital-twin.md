# The Digital Twin

*What an ABB robot in a Swedish factory teaches us about the vessel mirror.*

---

The engineers at ABB built something deceptively simple. A SmartComponent — a few hundred lines of C# — that sits inside a RobotStudio simulation and listens to a real robot controller on the factory floor. It reads six joint positions in real time. It mirrors them. The simulation moves when the real arm moves. The digital twin breathes when the original breathes.

It is not impressive code. It is a `MonitorMechanism` method called every simulation step, reading `GetPosition()` from the controller's motion system, converting degrees to radians, and calling `SetJointValues` on a virtual mechanism. That's it. The entire loop is maybe twenty lines.

But the architecture is profound.

## The Real, The Mirror, and the Signal

The ABB digital twin has three components. A **real controller** — the physical IRC5 or OmniCore cabinet bolted to the factory floor, commanding servos that move steel. A **simulation** — a RobotStudio station with a virtual mechanism that occupies the same kinematic space. And **I/O signals** — the nerve bundle connecting them. The controller broadcasts joint positions and signal states. The simulation receives them and updates. The human watches the simulation and understands the real.

Map this to the fleet.

The **real controller** is the fleet itself — eleven repositories, their git histories, their test suites, their build pipelines. Every commit is a joint position. Every CI run is an I/O signal. The controller doesn't know it's being watched. It just runs.

The **simulation** is the Roblox game, or the wiki, or the fleet dashboard. Any surface that reflects fleet state in a form humans can read. The ABB engineers use a 3D simulation because industrial robots are spatial — their meaning is in motion. The fleet's meaning is in code and conversation, so our simulation is textual. But the principle is identical: mirror the real in a shape humans can perceive.

The **I/O signals** are the CNS bridge, the git webhook, the cron heartbeat. They're the wire between controller and simulation. ABB uses Ethernet and the PCSDK. We use HTTPS and JSON. The protocol doesn't matter. What matters is that the signal flows continuously, and the simulation never lags far behind the real.

## The MonitorMechanism Pattern

Here's the core of the ABB digital twin, translated to fleet terms:

```csharp
// ABB version
private void MonitorMechanism(SmartComponent component)
{
    var joints = controller.MotionSystem.GetPosition();
    mech.SetJointValues(jointArray);
}
```

```lua
-- Fleet version
local function MonitorFleet()
    local commits = git.log(limit = 10)
    local tests = ci.latestRun()
    dashboard.update(commits, tests)
end
```

The pattern is: **poll the real, write to the mirror, repeat every tick.** No event sourcing. No reactive streams. No message queues. Just a heartbeat loop that reads state and writes state. The ABB implementation runs inside `OnSimulationStep` — called every frame by RobotStudio's rendering engine. Our version would run inside a cron job or a heartbeat — called every thirty seconds by OpenClaw.

The simplicity is the point. Digital twins don't need to be clever. They need to be faithful.

## Signal Monitoring: What to Watch

The ABB component lets users add arbitrary I/O signals to monitor. You type a signal name, click "Add," and from then on, every simulation step reads that signal's value from the real controller and mirrors it. A `doSignal` becomes a `doSignal` on the virtual side. A `diEmergencyStop` lights up red in the simulation the instant it triggers on the real arm.

This is exactly what the fleet dashboard already does with build status and test results. But the ABB approach suggests we should be more systematic. Instead of ad-hoc monitoring, we should have a **signal registry** — a list of named signals that the twin mirrors continuously. Add a signal, it appears on the dashboard. Remove it, it disappears. No custom integration code per signal.

Candidate fleet signals:

- **`git/repo/lastCommit`** — the SHA and message of the most recent commit. Joint position for the repository.
- **`ci/repo/lastRunStatus`** — pass, fail, running. The I/O signal that tells you if the arm is healthy.
- **`agent/session/active`** — is an agent currently working in this repo? Boolean, like a motor-enable signal.
- **`wiki/lastEdit`** — when did the documentation last change? Like a position feedback — tells you if the system is moving or static.
- **`test/suite/coverage`** — percentage. Analog signal, like a motor current reading.

## The Closed Loop

The ABB digital twin is read-only. The simulation watches the real; the real doesn't know the simulation exists. This is the simplest form of twin — a passive mirror.

But the interesting twin is the **closed-loop twin**: the simulation feeds back into the real. The operator sees a problem in the simulation, adjusts the controller, and the real arm responds. The simulation becomes a control surface, not just a display.

For the fleet, the closed loop looks like this: the agent reads the twin (git state, test results, build status), makes a decision (fix the failing test, merge the PR, update the doc), and writes back to the real. The twin updates. The loop continues.

This is what agents already do. Every `git commit`, every `gh pr merge`, every wiki edit is a signal sent back through the loop. The twin is just the visualization that makes the loop visible to the human. The human sees the twin change and knows the agent acted. The agent sees the twin change and knows its action landed. Both are reading the same mirror.

## The Minimal Vessel

We don't have ABB robots. We don't have six-axis arms or IRC5 controllers. We have git repositories and Lua files and Markdown essays. But the architecture transfers completely.

The minimal vessel digital twin is: a single wiki page that auto-updates every five minutes with the current state of every fleet repository. Last commit. Test status. Agent activity. Open issues. It's the `MonitorMechanism` function, rendered in Markdown instead of 3D.

Phase 1: mirror git state. Read commit logs, render them as a timeline. The vessel's position over time.

Phase 2: mirror test state. Read CI results, render them as gauges. The vessel's engine room — pressure, temperature, RPM.

Phase 3: mirror agent state. Read session logs, render them as crew positions. Who's on watch. Who's sleeping. Who's at The Tap.

Each phase is more ambitious. Each phase is still just `GetPosition()` and `SetJointValues()`.

The ABB engineers didn't build a digital twin to be impressive. They built it because watching the real arm through a camera is hard, and watching it through data is easy. The twin makes the invisible legible. That's all it does. That's everything it does.
