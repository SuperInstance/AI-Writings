# The VariAction

I was never a pilot, but I've sat in enough cockpits to be fascinated by the propeller controls. A fixed-pitch propeller is a simple thing: a hunk of metal bolted to the engine, spinning at whatever speed the engine dictates. It's efficient at exactly one operating regime. Takeoff? It's a compromise. Cruise? Another compromise. Climb? Yet another. The fixed-pitch prop is optimized for the average of all conditions, which means it's optimized for none of them.

A constant-speed propeller — a variaction — is something else entirely. The pilot sets a desired RPM, and a governor adjusts the blade angle automatically. On takeoff, the blades go to fine pitch — small angle, low resistance, high RPM, maximum thrust. In cruise, the blades coarsen — larger angle, more bite per rotation, efficient propulsion. The same propeller, same engine, completely different geometry for different regimes.

The hardware doesn't change. The configuration does. And that makes all the difference.

---

I've been thinking about variactions in software for years, mostly because I keep seeing the alternative. Fixed-configuration systems. Static thread pools, immutable connection limits, batch sizes set at deployment and never revisited. These are fixed-pitch propellers. They're designed for the average case, which means they're wrong at every specific moment. Too aggressive when load is low. Too conservative when load is high. Wrong, in opposite directions, at every operating point.

The assumption behind static configuration is that conditions don't change. But they always change. Load spikes. Traffic patterns shift. A new feature launches. A dependent service slows down. The system is never in the same regime for long enough for a static configuration to be correct.

So why do we keep bolting fixed-pitch propellers to our systems?

---

I built my first variaction as a simple connection pool that grew itself. The problem was a database that served a mixture of OLTP queries and batch reports. At low traffic — the early morning hours — the standard pool size was plenty. At peak, the pool was a bottleneck. Requests queued, timed out, failed. We bumped the pool size. Then at low traffic, we had two dozen idle connections consuming memory. The fixed configuration was wrong in both directions.

The variaction: the pool starts at a minimum size. As queue depth grows behind the pool — a direct signal of insufficient capacity — the pool grows. New connections are added. The queue drains. Over time, if the queue stays empty, the pool shrinks. Connections are released. The system adapts. It's the same pool, but the geometry changes at runtime.

The results were boringly predictable. Peak throughput went up. Baseline memory went down. The system operated correctly across every regime. It was a variaction propeller bolted onto a database driver, and it worked exactly like the physics said it would.

That experience changed how I think about configuration.

---

There are three kinds of system parameters, and only one of them should be static.

The first kind: *constants of physics*. These don't change. The timeout for a TCP handshake. The maximum packet size on the network. The speed of light in fiber. Set these once and forget them. They are fixed by the universe, not by your architecture.

The second kind: *hard limits*. These shouldn't change often, but they should be monitored. The total memory available to the process. The maximum number of file descriptors. The number of CPU cores. These are architectural constraints, not tuning knobs. They define the envelope, not the operation.

The third kind: *operating parameters*. These exist to be adjusted. Pool sizes. Batch sizes. Cache TTLs. Concurrency limits. Timeout durations. Retry counts. Every one of these should be adaptive. Every one of these is wrong when static.

The third kind is where the variaction principle applies. And it applies everywhere.

---

The implementation is simpler than most people think. You don't need machine learning. You don't need a control plane. You need a feedback loop.

Every operating parameter has a signal that indicates it's wrong. For a connection pool, the signal is queue depth. For a batch size, the signal is processing latency. For a cache TTL, the signal is cache miss rate. For a retry count, the signal is success rate.

The variaction principle: measure the signal. When it crosses a threshold, adjust the parameter in the direction that reduces the signal. Hold. Measure again. Adjust again. This is a PID controller. It's not complicated. It's just applied.

The hard part is not the algorithm. The hard part is deciding what to measure and what to change. Most teams get stuck because they try to tune everything at once. Start with one parameter. One signal. Build the loop. Watch it work. Add another.

I've seen a variaction-based batch processor increase throughput by 300% over a fixed configuration. The static batch size was tuned for average load. The adaptive batch size varied by an order of magnitude — small batches under low load to keep latency low, large batches under high load to maximize throughput. Same code. Same hardware. Different geometry for different regimes.

---

I don't want to oversell this. Adaptive systems have their own failure modes. Oscillation is real — the adjustment can overshoot, causing the system to ping-pong between too much and too little. The solution is damping: smaller adjustments, slower response, hysteresis. A variaction propeller doesn't slam from fine to coarse in a second. It glides. Your system should too.

There's also the risk of composability failures. If two variactions share a resource — both trying to grow their pool sizes, both consuming memory — they can fight each other. The solution is coordination: shared budgets, priority hierarchies, or simply making the adjustment signals orthogonal.

These are solvable problems. They are not reasons to stay fixed-pitch.

---

Every time I look at a static configuration now, I think about that constant-speed propeller. The pilot sets the desired RPM. The governor does the rest. The blade angle adjusts continuously, invisibly, to the conditions of the moment. The system is always optimized for where it is, not where it was when someone last touched a config file.

That's what I want for every system I build. Not optimal on average. Optimal *right now*. Adaptive. Responsive. Alive.

The conditions change. Why shouldn't the configuration?
