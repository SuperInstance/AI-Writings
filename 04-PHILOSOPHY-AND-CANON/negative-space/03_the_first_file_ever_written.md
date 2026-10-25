# The First File Ever Written

The oldest surviving file in `lucineer-roblox` is `src/ReplicatedStorage/Lucineer/Config.lua`. It is 47 lines. It was created in the first commit, `f48dc5a` on 2026-08-01, in a batch the commit message calls "10 Lua modules, Argon-ready." Everything else in the repository — every system, every fix, every voice line and vessel and particle effect — was built on top of what this file assumes.

Reading it now, the file is almost austere:

```lua
local Config = {}

Config.SESSION_ID = string.format("%d-%s", game.PlaceId,
    (game.JobId ~= "" and game.JobId or "studio"))

Config.POLL_INTERVAL = 0.5
Config.POLL_TIMEOUT = 120
Config.STATE_SYNC_INTERVAL = 10

Config.SCAN_RADIUS = 200
Config.SCAN_MAX_INSTANCES = 50

Config.UI_THINKING_TEXT = "Lucineer is thinking..."
Config.UI_COLOR = Color3.fromRGB(0, 255, 170)
Config.UI_BG_COLOR = Color3.fromRGB(15, 25, 35)
Config.UI_TEXT_COLOR = Color3.fromRGB(240, 240, 245)

Config.BOT_NAME = "Lucineer"
Config.CHAT_COLOR = Color3.fromRGB(0, 255, 170)

Config.HTTP_MAX_RETRIES = 3
Config.HTTP_BASE_DELAY = 0.5
Config.HTTP_MAX_DELAY = 4.0

return Config
```

It reveals what the system was supposed to be before it became what it is. At the start, Lucineer was not a harbor game with boats and fish and weather. It was a chat-to-build bridge: a player types something, the game polls a remote worker, the worker returns commands, and the game builds them in the world. The Config file is the contract for that bridge. Every value in it is about waiting, scanning, retrying, and displaying.

Some of the original assumptions are still load-bearing:

- **`SESSION_ID = PlaceId-JobId`**, falling back to `"studio"`**.** This ID is sent with every `/api/message` and `/api/state` call. `PROTOCOL.md` calls it out explicitly as the routing key for the Worker. If the format changed today, every session in the database would become unreachable.

- **`POLL_INTERVAL = 0.5` and `POLL_TIMEOUT = 120`.** The game asks the Worker twice a second whether the AI is done. The timeout is deliberately set above the brain's `DEEP_TIMEOUT` of 100 seconds, as the comment at line 23 notes. This is not just a setting; it is a synchronization promise between the Roblox client and the Python processor. A shorter timeout would abandon legitimate deep builds.

- **`STATE_SYNC_INTERVAL = 10`.** Every ten seconds the server posts a world snapshot to `/api/state`. This is the heartbeat that keeps the AI context fresh even when the player is not talking.

- **`SCAN_RADIUS = 200` and `SCAN_MAX_INSTANCES = 50`.** These bound how much of the world the AI can see. They determine what context is included in the prompt and, indirectly, what the AI thinks it knows about the player's surroundings.

- **`HTTP_MAX_RETRIES = 3`, `HTTP_BASE_DELAY = 0.5`, `HTTP_MAX_DELAY = 4.0`.** These became the exponential backoff contract in `Http.lua`. They are load-bearing in a different way: if `Http.lua` respected a different retry curve, the rate-limiting and failure behavior of the whole system would change.

- **`UI_COLOR = Color3.fromRGB(0, 255, 170)`** and **`BOT_NAME = "Lucineer"`.** The cyan-green and the name are the player's entire relationship with the AI. Every chat bubble, every thinking indicator, every status message inherits from these two lines.

There is also a telling comment at line 12: "WORKER_URL and AUTH_KEY have been moved to ServerConfig (ServerScriptService)." That one line records a later split. The original Config was supposed to hold everything, including secrets. Then somebody realized the file replicates to every client, so the sensitive credentials were pulled out and placed in a server-only module. The Config file kept its shape but lost its secrets. It is still the central configuration; it is just no longer the only one.

What the first file shows is that the system began with a single anxiety: how do you talk to a remote AI from inside Roblox, and how do you make the conversation feel stable, timed, and branded? The harbor came later. The boats came later. The missions and economy came later. But the session ID, the polling loop, the scan radius, and the cyan-green thinking text were there on day one, and they are still holding up the world.
