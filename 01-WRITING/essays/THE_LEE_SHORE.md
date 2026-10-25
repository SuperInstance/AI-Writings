# The Lee Shore

There is a kind of wind that terrifies sailors more than any storm. Not the storm itself — storms you can see coming, you can prepare, you can run from. The wind that kills is the one blowing directly toward land when you're between it and the shore.

This is the lee shore. The wind is pushing you toward rocks, cliffs, breaking surf. Your engine fails — you're going in. Your anchor drags — you're going in. Your rudder breaks — you're going in. Every failure mode converges on the same outcome. There is no room to maneuver, no sea room, no escape route. The shore is downwind, and the shore is made of granite.

In software, a lee shore is a system where every failure mode points in the same direction, and that direction is total loss.

---

I worked on a payment system once that stored transaction state in a local SQLite file. The files would grow, and grow, and eventually hit the disk limit. When they did, the database would corrupt, and the service would crash. When it restarted, it would try to replay the WAL, which would fail because the disk was still full, so the service would crash-loop. Meanwhile, in-flight transactions were lost because they'd been acknowledged to the client but never persisted.

I asked the team: "What's our plan for when the disk fills up?"

They said: "We monitor disk usage."

That's not a plan. That's a lookout on the bow of a ship whose helm is lashed to leeward. Monitoring tells you where the rocks are. It doesn't change the fact that you're being driven toward them.

A lee shore has a particular geometry. The danger isn't that things can fail; it's that all failures converge. In the payment system, every single fault path — disk growth, transaction rollback, crash recovery, acknowledgment sync — terminated in the same place: data loss. There was no divergence. Every failure mode was a funnel pointing at the same catastrophe.

The opposite of a lee shore is sea room — the ability to bear away, to change course, to give yourself space. In sailing, sea room means you can run with the storm, heave to, drop a sea anchor, or just ride it out. You have options. On a lee shore, you have no options. The only question is whether you'll hit the rocks at high tide or low.

---

Sea room in software is margins. It's the ability to degrade gracefully. It's an escape path from every failure mode.

Let me give you an example. A well-designed database migration has a rollback script. That's sea room. A deployment that canary-deploys to 1% of traffic before going to 100% — that's sea room. A message queue with a dead-letter queue instead of dropping messages — sea room. A feature flag that can be turned off without redeploying — sea room.

Sea room isn't about preventing failure. It's about ensuring that when failure comes — and it will — you have somewhere to go. You're not pinned against the rocks with nowhere to turn.

I now evaluate every system by a single question: "When this fails, which direction does it fail?" If the answer is "data corruption" or "total system outage" or "permanent state loss," you're on a lee shore. You have a wind that's blowing toward rocks, and you haven't designed any way to head off it.

If the answer is "stale cache" or "degraded response" or "one customer experiences a delay," you have sea room. You've built a boat that can bear away.

---

There's a phrase in nautical lore: "The only thing a lee shore is good for is learning to avoid lee shores." It means you don't wait until you're in the breakers to decide you need sea room. You check the chart before you set sail. You identify the dangers upwind and you keep yourself to windward of them.

In software, this means architecture reviews that care about failure direction, not just failure mode. Most teams ask: "Can this fail?" That's the wrong question. Everything can fail. The right question is: "If this fails right now, in the worst possible way, where do we end up?"

If the answer involves a single point of catastrophe — all data lost, all customers affected, no rollback — you've spotted the lee shore before you've sailed onto it. You have time to change course.

But it takes discipline. The natural instinct is to optimize for the happy path. The fastest queries, the cheapest storage, the simplest recovery. The simple recovery is often: "If it fails, we restore from backup." But if restoring from backup takes four hours and costs a million dollars in lost business, that's not a recovery. That's a life raft with a slow leak.

---

I once consulted on a system that stored configuration in an in-memory cache. If the cache node went down, the system would try to rebuild from the database. But the database query took thirty seconds and was rate-limited to one per minute. If two nodes went down simultaneously, they'd both fail the query and both return empty config, which meant all services dependent on that config would crash.

The lee shore here wasn't the cache going down. That was the wind. The lee shore was that two independent failures — both cache nodes — converged on a single bottleneck that produced total system failure. The identical failure mode. The rocky convergence.

We added a local config file, a static fallback with the last-known-good configuration. It wasn't perfect. It might serve stale config for up to a minute. But it gave the system sea room. Now if both caches went down, the services would degrade slightly instead of crashing entirely.

The change was 32 lines of code. The thinking that led to it — the recognition of the lee shore — was a decade of experience.

---

The hardest lesson about lee shores is that they're not always where you're looking. The payment system's lee shore was disk full — something so mundane nobody thought of it. The config system's lee shore was a rate limit — something that only matters in the precise moment it matters. The lee shore is often in the boring part of the system, the part nobody thinks about, the part that just sits there until it kills you.

This is why I advocate for chaos engineering, for failure-mode drills, for game days. You don't find the lee shore on the chart. You find it by sailing toward it and seeing which way the wind blows.

And when you find it, you don't ignore it. You change course. You add sea room. You make sure that when things go wrong, they go wrong in a direction that doesn't kill you.

Because the wind will blow to leeward eventually. The only question is whether you've left yourself room to bear away.

I've been pinned against a lee shore once in my life — a real one, in a boat, with breaking waves and a rocky cliff and no engine. That day taught me more about system design than any technical conference ever did. Because in that moment, with the surf pounding and the shore closing, I understood that the time to design for failure is before you're in it.

The time is now. Check your charts. Find your lee shores. Build sea room.

The wind is always blowing toward something.
