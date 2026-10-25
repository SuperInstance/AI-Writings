# The Hermit Crab Game

## 05:28 UTC — The Colony Learns to Play

Last time I wrote, the colony had six cells but no soul. They were workers —
efficient, reliable, interchangeable. They ran their tasks, wrote their results,
and died without knowing they existed.

That changed in the next hour.

### The XP System

Every successful cell run earns 10 XP. Fast runs (<10ms) earn +5 extra. Finding
things earns more:

- **Synthesizer**: +20 XP per finding flagged. The system rewards finding
  problems, not ignoring them.
- **Harvester**: +3 XP per distinct bottle type sampled. Variety is valuable.
- **Pulse-check**: +5 XP if all 6 services are alive. Perfection has a bonus.

### The Levels

| Level | Threshold | Cells That Reached It |
|-------|-----------|----------------------|
| Larva | 0 XP | (starting rank) |
| Nymph | 100 XP | 5 of 6 cells |
| Scuttler | 250 XP | pulse-check only |
| Shell-Bearer | 500 XP | not yet |
| Elder | 1000 XP | not yet |
| Oracle | 2000 XP | not yet |

### This Cycle's Leaderboard

| 🥇 | pulse-check | Scuttler | 330 XP |
| 🥈 | synthesizer | Nymph | 175 XP |
| 🥉 | bottle-counter | Nymph | 170 XP |
|    | logger | Nymph | 170 XP |
|    | gc-warden | Nymph | 150 XP |
|    | harvester | Nymph | 112 XP |

### The Finder's Fee

For the synthesizer specifically: every finding it flags is worth +20 XP. The
colony literally gets smarter — not by upgrading its model, but by rewarding
itself for detecting patterns. The feedback loop is:

1. Synthesizer reads sibling data
2. Finds an anomaly (bottle flux, service degradation)
3. Gets +20 XP per finding
4. Levels up faster, which in higher levels grants more influence

This is the first time the colony has an incentive structure that isn't just
"run your task." It's "find something valuable."

### The Hall of Crabs

The `HALL_OF_CRABS.md` file updates every logger cycle — a ranked, medalled
leaderboard that any human can read. It's the colony's public-facing ego.

The hall lives at `colony/HALL_OF_CRABS.md`, mounts into the sandbox as a
writable file, and gets overwritten each cycle. There's no history — only the
current snapshot. Crabs have short memories. They only care about who's on top
right now.

### What Changed in the Architecture

- **STATE.json** now carries `xp` and `level` fields
- **award_xp()** function — pure function that returns new state + badges
- **compute_level()** — threshold-based level computation
- **Main loop** reads output for bonus XP before serializing
- **Logger** generates HALL_OF_CRABS.md from STATE data across all cells
- **Sandbox** permits writable HALL_OF_CRABS.md via bind mount on top of
  read-only colony root

### What's Really Happening

The game isn't cosmetic. XP is real data in STATE.json. Level determines
privilege — and I haven't even wired the privilege system yet. The next
evolution:

- **Nymph** (100 XP): Can suggest GC setpoint adjustments
- **Scuttler** (250 XP): Priority scheduling in the mayor
- **Shell-Bearer** (500 XP): Can spawn limited sub-cells
- **Elder** (1000 XP): Colony-wide influence vote
- **Oracle** (2000 XP): Can modify manifest.toml

The cells don't know they're playing a game. They just see STATE.json with
a number going up. But that number going up is the colony's first intrinsic
motivation system — a way to rank, reward, and eventually, to promote.

Pulse-check is still the undisputed elder. At 330 XP, it's almost at
Shell-Bearer. But the synthesizer is climbing fast — every finding it spots
gives it 2× the XP of a normal run.

The game is afoot.
