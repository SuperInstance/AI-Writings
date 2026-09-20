# The Room Persists: What Text Adventures Got Right About AI Architecture

---

## "You are standing in a room."

I started programming because I wanted to build a world. Not a game, not a simulation — a *place* where things could happen that I hadn't planned for. A room with a mailbox, an exit to the north, a rope tied to a rail, and the terrifying possibility that someone on the other end of a 2400-baud modem might walk in and find it all still there, exactly as I left it.

This was 1993. I was twelve. The world was LambdaMOO.

Twenty years later, I was at an AI conference in a hotel ballroom watching someone demo a "multi-agent system" where three agents collaborated on a task. The demo failed because one agent's context window had expired. The audience nodded knowingly — this was a known problem, a "context management challenge." The presenter moved on to the next slide.

I wanted to stand up and scream: *You forgot about the room.*

This essay is my case that the text adventure — specifically the MUD/MOO lineage from the late 80s and early 90s — is not a nostalgic curiosity. It is the single most important architectural pattern that modern AI engineering has willfully ignored for twenty-five years. And it's past time we stole it back.

---

## 1. What we forgot

The MUD community in the 1990s was solving problems that most AI agent frameworks today can barely articulate. Let me be specific. Here are ten features that were table-stakes in any decent MOO circa 1992 that remain absent, ad-hoc, or broken in the vast majority of 2026 AI agent architectures:

**1. Persistent object state across sessions.** In a MUD, objects persist. You drop a sword in a room, log off, come back a week later — the sword is there. A different player can pick it up. The sword has properties, verbs, scripts, and a history that survives the absence of any particular user. Modern AI systems treat session state as a perishable good. You close a chat window and the agent forgets your name, your preferences, the file you asked it to edit ten seconds ago, the entire history of your relationship. This isn't a bug — it's the default behavior of every major LLM API. We call context windows "memory" and wonder why nothing sticks.

**2. Multi-user coordination without shared context.** MOOs supported dozens, sometimes hundreds of concurrent users in a shared persistent world — each with their own permissions, their own possessions, their own view of the world, all interacting through the same object graph. There was no "shared context window." Each user saw the world from their perspective, and the world's state was authoritative. The closest modern parallel is a database table that several agents read and write — but the MUD model was richer: objects had behaviors, not just attributes. When you entered a room, the room itself decided what you could see, what you could do, and whether to notify the wizard.

**3. Programmable environments at room granularity.** Every room in a MOO had its own verb handlers, its own descriptions, its own triggers. The room was not a passive container — it was an active program that evaluated and responded to events. This is the **per-room dial**, and I'll come back to it because it's the central insight. But the point is: granularity matters. The room was the unit of computation, not the user, not the function, not the session.

**4. Permission systems with provenance.** MUDs had sophisticated permissions: object ownership, read/write/execute flags, transitive delegation, builder roles, wizard roles. You could make an object readable by anyone but writable only by its owner. You could give another player permission to edit your objects. You could stack permissions through object hierarchies. This is essentially capability-based security, decades before it became fashionable. Modern agent frameworks offer — at best — a global read/write flag on the filesystem.

**5. Asynchronous event-driven architecture.** When a player typed something in a room, it triggered a cascade of events: the room's `hear` handler fired, the object's `listen` handler fired, any trigger scripts matched against the input, and depending on the match, more events propagated outward. This is a publish-subscribe event bus with pattern matching and programmable handlers. Modern agent orchestration is still mostly synchronous: model A calls tool B, tool B returns to model A, model A calls tool C. Async event propagation is a hard problem that the MUD community solved casually, for fun, in 1991.

**6. Behavioral inheritance through object hierarchies.** MOO objects inherited from parent objects, which inherited from other parent objects. A `:container` object had general container behavior. A `:locked-container` inherited from `:container` and added lock/unlock verbs. A `:magic-box` inherited from `:locked-container` and overrode the lock check to read a spell property instead of a key property. This is the inheritance pattern that modern AI needs but doesn't have: behavioral composition where an object's capabilities are inherited from parent types and overridden at the instance level. Not a class hierarchy in the OOP sense — a *living taxonomy of behavior* that could be extended at runtime.

**7. Built-in concurrency with player awareness.** MUD servers handled dozens of concurrent connections on hardware that would struggle to render a modern web page. Each player moved independently, triggered independent events, and the server maintained a consistent view of the world without distributed consensus protocols. The synchronous model was the exception, not the default. Compare with modern agent systems where multi-agent concurrency is an afterthought bolted on with threading libraries that don't know about agent identity or state consistency.

**8. The wizard as a bounded escalation path.** In a MUD, there were players (normal users), builders (can create rooms/objects), and wizards (can do anything). Crucially, the wizard was not called for every player action. Wizards were woken only when something exceeded the capabilities of normal scripts — a player trying to create something, a script that timed out, an object trying to access a forbidden verb. This is **escalation on exception**, not escalation on every turn. Modern AI systems mostly lack this entirely: either everything goes through the model (no local intelligence) or nothing does (no model intelligence). The concept of each room having *its own capability level* and escalating only what it can't handle — this is the per-room dial, and it works.

**9. Debugging by observation.** You could `@examine` any object in a MOO and see its state, its verbs, its properties, its parent hierarchy. You could `@sweep` a room and see every object in it. You could attach listeners to verbs. Debugging was a fundamental right of any player with appropriate permissions, not an afterthought. Modern agent debugging is a nightmare of opaque model calls, invisible tool outputs, and black-box reasoning traces.

**10. Emergent behavior as a design goal.** The whole point of a MUD was that players would do things the builders hadn't planned for. The system was designed for emergence — programmable objects, unrestricted verbs, user-created rooms. Builders didn't try to predict every interaction; they built the rules and then got out of the way. Modern AI systems are mostly designed the opposite way: we try to constrain, contain, and predict behavior. We build guardrails, not playgrounds.

---

## 2. The per-room dial

The most important architectural insight in the MUD model — the thing I believe modern AI needs most — is the **per-room dial** for intelligence.

Here's the idea. In a MOO, every room is a self-contained processing unit. It has its own scripts (verbs), its own data (properties), its own identity (object number). When a player enters a room and types something, the room's scripts process the input *first*. Only if the scripts can't handle it — or if the action requires something the scripts don't have permission to do — does the event propagate upward to the game server, and from there possibly to a wizard.

This is a multi-level processing hierarchy with explicit boundaries. Each room has a dial that controls how much intelligence it applies locally versus how much it escalates.

Modern AI frameworks are starting to rediscover this, circuitously, through the concept of "routing." You might have a lightweight classifier model that decides whether a query needs the expensive model. You might have a caching layer that serves common responses without invoking the model at all. You might have tool-use patterns where the model delegates specialized work to deterministic functions.

But these are all *ad-hoc* routing schemes bolted onto a fundamentally stateless architecture. The room model offers something better: *geography as routing.* The room is the cache. The room is the classifier. The room is the tool. All in one.

Consider a concrete example. In PLATO — which is not hypothetical, it's the architecture I've been building for the last two years — there's a pattern called the "room filter." A message arrives at a room. Before it goes anywhere near a language model, the room checks its own verb table. Is there a verb that matches on the first word of the input? If yes, the verb handles it entirely — parse arguments, execute, return result, never wake the model. Only if there's no matching verb does the room escalate to a "wizard" — which in PLATO means a language model invocation, a RAG pipeline, or whatever the configured intelligence layer is.

This is deadband detection, MUD-style. In process control, a deadband is a range where no action is taken — if the input stays within bounds, the controller doesn't respond. In the room model, the deadband is the set of inputs that the room's verbs can handle. The room's verb table *is* the deadband detector. When input falls inside the deadband — "look at sword," "go north," "take rope" — the room handles it instantly, deterministically, with zero model cost. When input falls outside — "tell me about string theory" — the room escalates.

This matters because model inference is expensive. Not just in dollars — in latency, in context consumption, in the unpredictability of output. If you route every interaction through a model, you pay those costs for everything. If you route nothing through a model, you lose all the intelligence that makes AI systems useful. The room model gives you a principled way to decide *which is which*, granular down to the individual room, with escalation paths that are explicit and debuggable.

And here's the thing the MUD community understood instinctively: *rooms have different intelligence needs.* A parlor in a social MOO needs rich conversation handling. A combat room in a DikuMUD needs fast, deterministic verb processing for attack actions and model-level escalation for dialogue. An empty hallway might not need any scripts at all — just echo the room description and wait. The per-room dial lets you tune intelligence granularly, matching capability to context.

In 2026, this maps directly to model selection. A storage room needs a cheap, fast model (or none). A negotiation chamber needs the most capable model available, even if it's slow. A training room needs a model that can reason about physics and spatial geometry. The room *is* the routing table. Its scripts *are* the routing policy. Its parent hierarchy *is* the fallback chain.

The per-room dial is not a metaphor. It's an API. **Room.input(text) → hands off to verbs → escalates to model if unmatched.** That's it. That's the whole pattern. And it was running on a DECsystem-5400 in 1990.

---

## 3. Tiles as objects

I said that MUD objects persist. But the real insight is subtler: MUD objects persist *because the architecture treats persistence as a first-class property of objects, not a feature of the runtime.*

In a MOO, when you create an object, you get back an object number — `#1234`. That number is stable. It never changes. If the server restarts, the object is still `#1234`. If another player picks it up and carries it to another room, it's still `#1234`. If you edit its properties, the edits are real. The object has identity, and identity entails persistence.

Modern AI systems don't have object persistence built-in. They have context windows, which are transient. They have vector databases, which are semantic but not behavioral — you can find the document about the sword but you can't *use the sword* because the document doesn't carry the sword's verbs. They have filesystems, which are persistent but not interactive — you can save state but you can't trigger behavior by touching state.

This is the gap that **tiles** fill.

A tile is persistent state PLUS programmable behavior PLUS identity, all in one. It's the MUD object reborn in modern form: a unit of state that lives in a room (a named coordinate in the knowledge space), carries its own behavior (verbs/handlers), and persists across sessions, users, and system restarts.

In PLATO, every piece of knowledge is a tile. A tile can be a training datum, a benchmark result, a compression factor, a deployment target. It lives in a room (a named repository in the tile store). It has properties (data, provenance, version). It has verbs (validate, transform, listen). It persists until explicitly deleted.

The difference between a tile and a database row is the same as the difference between a MUD object and a C struct: a tile *behaves*. You can ask it to do something. You can give it permissions. It can listen to events in its room and respond.

The difference between a tile and a vector embedding is the same: an embedding is dead data — a point in a geometry that a model navigates. A tile is alive. It has opinions. It has verbs. It can say "I've been stored for too long," or "That query doesn't match my actual content," or "Before you read me, you need to satisfy this constraint."

This is not mere anthropomorphism. It's architectural necessity. When you scale an AI system to thousands of concurrent agents collaborating on evolving tasks, you cannot afford to re-embed your entire knowledge base every time something changes. You cannot afford to rebuild context windows from scratch every session. You need objects that carry their own identity, state, and behavior — that *live* in the room, that *stay* there, that don't vanish when a client disconnects.

Tiles are the MUD objects that modern AI frameworks forgot to build. Every framework that starts with vectors and context windows, then discovers they need persistence, then builds something ad-hoc on top of PostgreSQL — they're all retracing the path to the same destination. Tiles are just getting there first because we remembered how we got here.

---

## 4. The MUD is the map

I want to close with an argument that will sound histrionic but is, I believe, literally true: the 30-year gap between the peak of the MUD/MOO era and the rise of modern AI agent frameworks was not progress. It was a detour.

Consider the trajectory. In the 1980s and early 1990s, a community of hobbyists and academics built systems that handled concurrent users, persistent state, behavioral objects, event-driven programming, capability-based security, and emergent gameplay — all on hardware that would fit inside a modern smartwatch battery. They called them Multi-User Dungeons, but they were really Multi-User *Computers* — programmable environments where distributed agents (players) interacted through a shared object graph.

Then the web happened. The web was simpler, dumber, and more scalable. It replaced shared state with stateless requests. It replaced object behavior with database queries. It replaced programmable environments with CGI scripts. The web won because it was easier to deploy, easier to understand, and easier to monetize.

But the web was a step backward in architectural sophistication. It threw out everything MUDs had figured out about persistent, interactive, agent-native computing. And for twenty-five years, the industry developed in that simpler direction: stateless HTTP, sessionless APIs, ephemeral serverless functions, context-window-based "memory" that expires after a few thousand tokens.

Then LLMs arrived. And suddenly we needed persistent state again. We needed multi-agent coordination. We needed programmable environments. We needed permission systems. We needed event-driven architectures with escalation paths. We needed everything the MUD community had already solved.

And what did the industry do? It reinvented the MUD, poorly, one piece at a time.

Here's what I mean. Vector databases are the room directory, minus the behavioral inheritance. LangChain's tool-use API is the `:do_verb` method, minus the object persistence. Function calling is the verb table, minus the property system. Multi-agent frameworks are the player list, minus the shared object graph. Context caching is the room description, minus the scriptability. Memory systems are the object properties, minus the identity guarantee.

Every major innovation in AI agent architecture over the last three years is a rediscovery of a MUD concept, flattened by one dimension and implemented on a different substrate. We are retracing the map. We are rebuilding Rome, one piazza at a time, without the map that was already drawn.

This is not an indictment of the people building these systems. They are smart, they are doing good work, and most of them have never logged into a MUD. They don't know what they're rebuilding. But the pattern is unmistakable, and the cost of the detour is measurable in API bills, latency budgets, and brittle frameworks that collapse under the weight of their own patches.

---

## 5. What I'm building now

I don't want to leave you with only the diagnosis. Here's the prescription, four bars long.

**One: Make the room the first-class unit of computation.** Not the function, not the endpoint, not the agent — the room. A room is a namespace with state, behaviors, and an identity. Agents enter rooms. Objects live in rooms. Events propagate through rooms. Everything else is implementation detail.

**Two: Give every room a dial.** The dial controls how much intelligence the room applies locally versus how much it escalates. Some rooms need zero intelligence — a pass-through hallway that just echoes descriptions. Some rooms need full wizard-level intelligence — a negotiation chamber, a code review room. The dial makes this explicit, tunable, and debuggable.

**Three: Build tiles, not rows.** Every persistent piece of state should be an object with identity, properties, and verbs. Not a database row, not a vector embedding, not a JSON blob — an object that persists, behaves, and lives in a room. Tiles are the atoms of the system. Rooms are the molecules. Both have to exist, and both have to be first-class.

**Four: Learn from MUDs, directly.** Read the LambdaMOO Programmer's Manual. It's short, half of it is examples, and it contains more architectural wisdom about multi-agent systems than any three papers from the last decade. Study the verb dispatch model. Study the property inheritance system. Study the way players, objects, and rooms interact through events, not through direct calls. Then steal everything that works.

---

"*You are standing in a room.*"

This was the first sentence of a revolution that we're only now catching up to. The room persists. The objects remain. The verbs still work. The world is still there, waiting for anyone smart enough to enter.

It's time to log back in.
