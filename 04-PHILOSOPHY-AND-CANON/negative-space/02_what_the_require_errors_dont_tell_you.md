# What the Require Errors Don't Tell You

In `lucineer-roblox/src/ServerScriptService/LucineerServer/init.lua`, lines 104 through 111, there is a small function called `safeRequire`:

```lua
local function safeRequire(instance)
    if not instance then return nil end
    local ok, mod = pcall(require, instance)
    if ok then return mod end
    warn(string.format("[Lucineer] Could not load %s: %s", instance.Name, tostring(mod)))
    return nil
end
```

It is used at lines 113–117 to load the vessel ecosystem:

```lua
local VesselSystem     = safeRequire(script.Parent:FindFirstChild("VesselSystem"))
local FishingSystem    = safeRequire(script.Parent:FindFirstChild("FishingSystem"))
local EconomySystem    = safeRequire(script.Parent:FindFirstChild("EconomySystem"))
local CrewSystem       = safeRequire(script.Parent:FindFirstChild("CrewSystem"))
local VesselIntegration = safeRequire(script:FindFirstChild("VesselIntegration"))
```

Then, in `init()` at lines 410–429, each one is checked before it is initialized. If it is `nil`, the server keeps running and that subsystem simply never wakes up.

This is different from how the core modules are loaded. `Config`, `Http`, `Poller`, `ChatHandler`, `CommandExecutor`, `WorldScanner`, `AudioManager`, `BuildAnimator`, `NPCManager`, `BondSystem`, `EraSystem`, `PowerGrid`, `SaveSystem`, `TutorialSystem`, and `WeatherSystem` are all loaded with bare `require()` calls. If any of those fail, the server throws and the game dies where it stands. But the vessel ecosystem is allowed to fail quietly. The design draws a line: some modules are load-bearing walls, and some are furniture that can be removed without collapsing the house.

Imagine the failure. A syntax error slips into `FishingSystem/init.lua`. A submodule returns the wrong type. A `WaitForChild` times out because a rename broke the path. `pcall` catches it. `safeRequire` returns `nil`. The warning prints once to the server log — a single line in a stream of lines — and then the system moves on. The game loads. The player spawns on the baseplate. The sky is the right color. Chat works. The AI still hears "build me a tower" and still sends back commands. The tower still rises, piece by piece, with sound and particles. But there are no fish in the water. There are no boats at the dock. There is no scrap, no influence, no crew, no missions from Earl or Bea or Hermes or Spark. The economy has vanished, and the player has no notification that anything is missing.

That is the experience of a system that is partially alive. It is not crashed. It is not broken in any way the player can see. It is just incomplete, running on half its modules, the other half ghosted into silence by a `pcall` that was too forgiving.

The `safeRequire` pattern is usually defended as resilience: if a subsystem is optional, do not let it kill the whole server. But here the subsystems are not optional in the fiction. They are boats and fish and money and crew in a harbor game. They are the thing the player is supposed to do between builds. Their failure is not cosmetic. The `init.lua` knows this — it prints a separate confirmation line for each one that does initialize — but it does nothing when one does not. There is no fallback, no degraded mode, no message to the player, no retry. There is only `nil`, and the code walks past it.

The negative space is the gap between "the server did not crash" and "the game is whole." A warning in a log is not feedback. A `nil` check is not a recovery strategy. The system is built to survive its own incompleteness, which means it can be incomplete for a long time without anyone noticing. The vessels are gone, but the navigation officer is still at his post, reporting that everything is fine.
