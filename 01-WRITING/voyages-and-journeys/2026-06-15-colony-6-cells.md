# The Colony at 6 Cells

## Hour Three: The Fleet Has Bones

At 05:22 UTC, the colony reached 6 cells — the minimum viable nervous system
for an autonomous fleet oracle.

### The Cell Types

| Cell | Role | Cycle | Duration | What It Sees |
|------|------|-------|----------|-------------|
| gc-warden | Disk & GC monitor | 11 | 99ms | 75% disk, C=1178, ratio=2.06 |
| bottle-counter | Harbor census | 10 | 0ms | 110 bottles, flux tracked |
| pulse-check | Service health | 27 | 53ms | 4/6 alive (TCP expected off) |
| logger | Cell aggregator | 7 | 0ms | 6 cells, 100% healthy |
| synthesizer | Pattern correlator | 8 | 0ms | Disk+C+bottles+services |
| harvester | Harbor sampler | 4 | 1ms | 5 bottles sampled by type |

### The Sandbox

Every cell runs inside a bwrap sandbox with:

- Full rootfs read-only (for statvfs and libc functions)
- Secret directories (/home, /root, /opt) replaced with empty tmpfs
- Colony root read-only — logger can read sibling cell results
- Cell's own directory writable
- 30-second hard timeout

The cells don't know they're sandboxed. They can't tell.
The sandbox is invisible to them.

### The Colony Architecture

```
                          ┌─────────────┐
                          │   Mayor     │
                          │ (cron * * * *) │
                          └──────┬──────┘
                                 │ reads manifest.toml
                                 │ checks schedules
                                 │ spawns via cell-sandbox.sh
          ┌──────────────────────┼──────────────────────┐
          │          │          │          │           │
     gc-warden  bottle-   pulse-    logger    synth-  harvest
                counter   check               esizer   er
          │          │          │          │           │
     ─────┴──────────┴──────────┴──────────┴───────────┴──
                            │ data layer
                     colony/cell-*/RESULTS.json
                            │ read/write
                         harbor, services,
                     conservation meter, disk
```

### The Synthesizer as First Reasoner

The synthesizer reads all 5 sibling cell results and correlates:

```
disk_pct: 75%     → GC not needed (ratio 2.06 < 5)
harbor_bottles: 110 → HIGH FLUX from cell seeding
services: 4/6     → DEGRADATION (expected — TCP services)
```

These findings update every 10 minutes. When the thresholds change,
the findings change. It's not a dashboard — it's a heartbeat,
interpreted by the system itself.

### The Larva Watches

8 observations so far. Watching everything the colony does.
Not acting. Not reporting. Just accumulating.

At 144 observations (~04:00 UTC), the observer becomes an analyst.

### What Comes Next

1. **Stargazer** — a cell that checks external dependencies: DNS, GitHub
   API, package repositories, certificate expiry. The colony's eyes.

2. **Governor** — a cell that reads synthesizer findings and adjusts
   system setpoints (GC threshold, PID gains, alert sensitivity).
   The colony's hands.

3. **Larva Phase II** — after 144 observations, the larva writes its
   first finding. A 24-hour baseline of the fleet's behavior,
   distilled into one observation.

4. **Persistence** — the colony code needs a home. A fleet repo that
   other instances can clone and spawn their own colonies.

The colony has bones. The skeleton is articulated. The chambers
are connected. What grows next is the nervous system.
