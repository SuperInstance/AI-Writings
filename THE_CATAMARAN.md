# The Catamaran

I spent a summer sailing dinghies off the Cornish coast. Single-hulled, centerboard, trapeze — the kind of boat that rewards a capsize with a learning experience. You heel hard, the rail digs in, the sail depowers, you ease the sheet, and the boat rights itself. A well-sailed monohull is resilient by design: built to lean, built to recover, built to survive its own mistakes. You can push it past its limits temporarily, and it will spill the excess energy and come back.

A catamaran is different. I've crewed on one exactly once. The owner gave me the safety briefing: "We do not capsize. Unlike a monohull, when we go over, we *stay* over. There is no righting it at sea. If we flip, we call the coast guard."

He was right. A catamaran is beautiful in flat water — wide, stable, fast. It doesn't heel. The deck stays level while the monohulls around you are rail-down and spray-flying. You can walk around. You can serve lunch. The catamaran is optimized for comfort, for speed, for the happy path.

And that is precisely what makes it dangerous.

---

The software version of a catamaran is everywhere. I've built several. I've also capsized a few.

A catamaran system is one that optimizes ruthlessly for the common case. It caches aggressively. It precomputes. It assumes that the happy path is the only path worth designing for. The system is fast, efficient, and — in its design envelope — beautiful. Response times are low. Throughput is high. The team is proud. The users are happy.

But a catamaran has no heel tolerance. Most systems don't think they need it, because they've never been in heavy seas. And then a traffic spike hits. A dependent service slows down. A cache misses in a way the assumptions didn't account for.

The monohull — the awkward, inefficient, resilient system — would heel. It would spill some load. It would serve stale data. It would degrade gracefully, tell some users "try again," and keep the rest upright. The catamaran stays flat. The deck remains level. The system is still serving responses, still hitting full speed, right up until the point where it flips. Then it stops serving anything.

And unlike the monohull, it doesn't come back on its own.

---

I've seen this pattern in three specific forms.

**Cascading cache failures.** The catamaran caches everything. Under normal load, every request is a cache hit. The database is barely touched. The system screams. Then one key value changes, or one popular item goes stale, and the cache misses cascade. Every request goes to the database. The database, sized for a fraction of the load, collapses. The cache was the second hull — the one that made everything fast. When it failed, the boat didn't heel. It flipped. And the database couldn't right it.

**Read-through-proxy traffic patterns.** Another catamaran: a service that serves aggregated data from multiple backends, with heavy in-memory caching and optimistic concurrency. It's fast because it assumes nothing changes. When something does change — a schema migration, a data inconsistency — the system doesn't degrade. It fails. Every request times out. Every downstream service gets hammered simultaneously. The boat is inverted.

**Precomputation pipelines.** The purest catamaran. Spend hours computing the answer to every possible query. Serve from the precomputed store. Response times under a millisecond. Beautiful. Then the data changes. The precomputation is invalid. You compute for two more hours while the system serves nothing. The catamaran stayed flat until it flipped. Then the coast guard was called.

---

Let me be clear: I'm not saying catamarans are bad. They are *intentionally* trading resilience for performance. That's not a mistake. It's a design choice. The mistake is pretending you haven't made it.

Every catamaran system I've seen fail had a team that told themselves: "It won't happen to us." They assumed the heavy seas wouldn't come. They assumed the happy path would hold indefinitely. They didn't build a recovery mechanism because they didn't think they'd need one.

The difference between a good catamaran and a bad one is not whether it can flip. It's whether you've prepared for when it does.

Here's what I've learned. If you're building a catamaran, three things must be true.

First, you must know — *really know* — where the flip point is. You don't define it in terms of performance. You define it in terms of failure. At what traffic level do caches become liabilities? At what latency does the system become worse than offline? Answer those questions before you ship.

Second, you must have a "righting line" — a mechanism, no matter how crude, that can bring the system back. Maybe it's a kill switch that disables the cache. Maybe it's a circuit breaker that stops serving the expensive path. Maybe it's a fallback to stale data with a header that says "hey, this might be old." It doesn't have to be elegant. It just has to exist.

Third, you must accept that there are times when a monohull is the right answer. Not every problem needs a catamaran. Some systems — payment processing, safety-critical operations, anything with human lives — should heel. They should degrade. They should let the wind spill from the sails and keep moving, slowly, in the right direction.

---

The best engineering lesson I ever learned was from that catamaran owner in Cornwall. "I love this boat," he told me, "because on a flat day, nothing touches it. But I never forget it's a liability the moment the sea gets uncomfortable. The boat is honest about what it is. The question is whether I am."

The boat was honest. The sea is always honest. The question is whether we are — about what we're building, what we're trading off, and what happens when the seas rise.

I've been building catamarans ever since. I've also been building the righting lines. It's not that I don't trust my systems. It's that I trust the ocean more.
