# The Mooring Swing

The anchorage in Sausalito is a mess. Boats packed tight, mooring fields overlapping, and a current that reverses with the tide under a wind that's coming over the hill from the Pacific in unpredictable gusts. Every boat is swinging on its mooring, and every boat is describing a different arc — different radius, different period, different center point — because every boat is a different size with a different scope of line and a different crew who set the mooring on a different day.

On a still evening, you can watch the boats drift through their patterns. One swings wide into the channel. Another carves a tight circle so small you wonder if it's still attached. A third — the one nobody wants to be moored next to — swings erratically, catching the current at an angle and tracing an ellipse that brings its bowsprit within feet of its neighbor's topsides on every oscillation.

Every mooring swing has a scope: the ratio of line length to water depth. Standard scope for a permanent mooring is 7:1 — seven feet of line for every foot of water at high tide. Too much scope and the boat swings too wide, colliding with its neighbors. Too little scope and the boat snubs hard against the line in a blow, risking a parted chain or a pulled cleat.

The art is finding the right scope. Enough room to move. Not enough to hit anything.

---

I see mooring swings everywhere in software. Every service on a shared platform traces an arc around its dependencies.

The scope is defined by coupling: the amount of latitude a service has to deviate from its contracts. Too much scope — loose coupling with long timeouts, flexible schemas, forgiving retry policies, eventual consistency windows measured in minutes — and the service swings wide. It works fine in isolation. But watch it against its neighbors. The wide-swinging service times out under load, retries hard, cascades. It sends messages with slightly different fields than the schema expected. It holds locks longer than the database expects. It traces a path that brings it close enough to hit something.

Too little scope — tight coupling with strict contracts, predefined response shapes, rigid timeouts, synchronous everything — and the service snubs against its mooring in the first blow. A schema change that should be a non-event becomes a coordinated deploy. A new feature requires changes in four downstream services. The boat has zero swing, and when the wind pipes up — a traffic spike, a partial failure — the line parts.

The right scope is not a number. It is a relationship — between the service and the ecosystem it depends on, between the engineering team's tempo and the platform's stability.

---

I spent two years on a microservices platform that had the opposite problem on every team. The platform team wanted tight coupling everywhere. They specified exact message schemas, exact timeout windows, exact retry counts. Every service's mooring was on a chain so short it couldn't turn around.

The platform was stable. Everything worked. Until it didn't. A deployment in one service required coordinated deploys in eight others because the contract was so tight that any change broke something. Feature velocity ground to zero. The platform was safe from cascading failures only because nothing could move at all.

The product teams, in response, started bypassing the platform. They built their own endpoints, their own retry logic, their own schemas. They swung wide — way wide — and started colliding with each other.

The right scope is not zero. The right scope is not infinite. The right scope is the amount of freedom that allows independent evolution without risking collision.

---

How do you find it?

First, measure the swing radius of every service in the system. How far does each one deviate from its ideal position during normal operation? How much schema variation does it tolerate? How long does it wait before timing out and retrying? How far back does it fall behind its upstream dependencies during peak load? These are the arcs your services describe. You cannot set the scope until you know the arcs.

Second, measure the distance between neighboring services. Not in deployment topology — in actual interaction patterns. Which services share databases? Which share caches? Which depend on each other's health check endpoints? The distance between two services is the number, severity, and sensitivity of their shared dependencies. If two services share a table and one has a long timeout, you have a collision risk.

Third, adjust the scope intentionally. Not all at once. Not by edict. By measurement and iteration. If a service is swinging too wide — causing cascading timeouts, accumulating retry storms — shorten the scope. Tighten the timeouts. Stricter contracts. If a service is snubbing too hard — requiring coordinated deploys, blocking upstream changes — lengthen the scope. More forgiving interfaces. Longer windows. Let the boat move.

---

The metaphor breaks in one important way. On a mooring, the scope is set once and checked occasionally. In software, the scope needs to adjust continuously — because the wind and current are always changing.

The weekend crowd in Sausalito is chaos. On a Tuesday morning, the anchorage is almost docile. A scope that works on Tuesday will cause collisions on Saturday. Similarly, a coupling scope that works during normal traffic will fail during a Black Friday spike. A scope that works for a team of two developers will snub too hard for a team of twenty.

Good mooring management means checking the scope. Not obsessively — nobody stands on deck watching the boat swing all day. But occasionally. When the weather changes. When the crew changes. When a new boat parks nearby.

In software: review your coupling contracts when the team grows. When the traffic profile changes. When a new service deploys in the same namespace. The scope that worked last quarter may be the scope that causes a collision next quarter.

---

I think about the Sausalito anchorage a lot when I look at system architectures. The clean diagrams — nice boxes, neat arrows — never show the swing. They show the static ideal: service A talks to service B through a well-defined interface. But in operation, service A drags an arc around service B. The arc is real. The static diagram is a fiction.

Good architecture accepts the fiction as a useful simplification but designs for the reality. It doesn't try to eliminate the swing — that's impossible. It doesn't ignore the swing — that's dangerous. It chooses the scope deliberately, knowing that every choice is a trade between collision and snubbing, between autonomy and stability, between the freedom to move and the safety of being held.

The best mooring isn't the tightest or the loosest. It's the one that holds through the tide, lets the boat find the wind, and never touches the boats around it. I don't know a better definition for a well-architected system than that.
