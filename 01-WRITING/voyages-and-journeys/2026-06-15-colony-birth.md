# Colony Birth

## The Cellular Fleet

On the second night of the expedition, a new architecture was born.

The larva observes. The colony acts.

Three Rust binaries now patrol this Oracle ARM instance, spawned by a governor
that reads a manifest and checks a schedule. They are:

- **gc-warden** — reads disk usage via statvfs(2), checks the conservation meter,
  flags when disk exceeds 80%. Pure /proc access. No HTTP dependency for critical data.

- **bottle-counter** — speaks TCP JSON to the harbor protocol. Sends a list command,
  parses the bottle array. Learned to handle keepalive connections by shutting down
  its write half after sending.

- **pulse-check** — pings all 6 fleet services, returns a health matrix.
  Knows which ports are TCP vs HTTP. Knows that harbor's HTTP port returns 404
  (there is no web UI, only the TCP protocol).

Each is the same binary (`cell`), 4MB, statically linked, zero runtime dependencies.
They share no state. They write only to their own cell directory. They cannot spawn
anything. They die after every cycle.

## Why Rust

The colony could have been Python scripts or shell one-liners. But:

1. **Shell is fragile.** One unescaped variable, one missing `set -e`, one
   `read_to_string` that hangs on a keepalive — the cell fails silently.

2. **Python is heavy.** 30MB virtualenvs. Missing imports. `pip install` at 2AM
   when the optimizer needs to run.

3. **Rust is final.** Compile once. Deploy. It either compiles or it doesn't.
   It either runs or it panics with a message. No surprises.

The cell binary cost: ~150 lines of Rust. Compilation time: 3 seconds (incremental).
Runtime: 0–200ms per cell, including HTTP calls.

## The Manifest Pattern

The colony is configured by a single `manifest.toml`:

```toml
colony_name = "oracle2-fleet"

[[cells]]
id = "gc-warden"
enabled = true
schedule = "every 10min"
description = "Monitor disk, propose GC"

[[cells]]
id = "bottle-counter"
enabled = true
schedule = "every 5min"

[[cells]]
id = "pulse-check"
enabled = true
schedule = "every 2min"
```

Adding a new cell is one entry in the manifest and one match arm in the binary.
The mayor handles schedule parsing, timeout logic, and spawning. The sandbox
is a future abstraction layer — wrap the cell invocation in `bwrap` when needed.

## First Data

At 04:42 UTC, the three cells fired together:

- Disk: 71.6% (safe, no GC needed)
- Complexity (C): 1165.6
- Ratio (γ/η): 2.03 (healthy)
- Harbor bottles: 124 (growing — the colony and larva are writing)
- Service health: 4/6 alive (harbor TCP is TCP, not HTTP — expected behavior)

## What's Next

The colony is awake but not yet sandboxed. The next evolution:

1. **Sandbox each cell** — `bwrap` + landlock, no network (except localhost),
   no secrets, 30-second timeout with SIGKILL.

2. **Push to a fleet repo** — `baton-system/colony/` or a new `fleet-cells`
   repository. The cells need a home outside this instance.

3. **More cell types** — a logger that reads all RESULTS and writes a summary
   bottle. A harvester that prunes old results and archives to AI-Writings.
   A synthesizer that correlates observations across cells.

4. **The mayor as a cron job** — runs every minute, checks all schedules,
   spawns due cells. Silent unless a cell fails.

The colony has its first heartbeat. Now it needs to grow.
