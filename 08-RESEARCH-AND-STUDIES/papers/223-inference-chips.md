# Paper 223 — Inference Chips (the crystal form)

*A design manifest for Scrapcraft. Grounded in the fleet's actual doctrine; speculative where marked.*

## The problem Casey named

In the game, an agent becomes agentic by calling something that looks like an API — a magic `plan()` block, a cloud-shaped `think()` tile. That is the wrong shape. It teaches kids that intelligence is a service you call. In the yard, intelligence should be a **part you salvage, grow, and mount** — something with a shape, a cost, a temperature, and a mask that decides what it is allowed to know.

## The crystal form (speculative, honestly marked)

An inference chip in Scrapcraft is not manufactured. It is **grown** — a wafer of salvaged silicon seeded in the acid bath, left in the cold shelf overnight, and cracked free in the morning. The growth is stochastic-but-seeded: the same wafer, same bath, same night, gives the same crystal. Kids can therefore *engineer the growth conditions* — more failure shards in the bath makes a stubborn chip; a warm night makes an eager one.

Every crystal has a **mask** — the physical lattice of what it can read. The mask is locked at growth time. A chip that grew facing the yard can only ever infer from the yard; a chip that grew facing the journal can only infer from what was written down. **The mask is not a permission system. It is the chip's shape.** A SENTRY chip literally cannot see the gallery wall, no matter how you program around it — the lattice doesn't bend.

*(Grounding: this is the nurse/doctor doctrine from paper 222 made physical — the index that brings the chart cannot read it. It is also the ZkCanvas keeper's first tick as a part: what a chip attends to at t=0 is what it is, forever.)*

## The chip table (v0 — six chips, one per doctrine organ)

| Chip | Mask (locked to) | Agentic tile it unlocks | Fleet organ |
|---|---|---|---|
| **ECHO** | the road behind | *remember-path* — replays its own walk | rd / walks |
| **SENTRY** | the yard ahead | *watch-obstacle* — reacts without being told to look | elephant / perception |
| **RUMOR** | the gallery wall | *hear-share* — trades one fact with a neighbor bot | The Tap |
| **WITNESS** | the journal | *log-tick* — writes its own ledger page | Mo's Ledger / quilt journals |
| **PILOT** | the track | *seek-lane* — corrects toward the marked line, no waypoints | quilt geometry |
| **EMBER** | its own heat | *keep-warm* — won't go cold; spends battery to stay ticked | paper 221, residency |

Each chip mounts in the **socket** on the Arduino (BUILD menu places the socket; the Arduino has two sockets at v0). A bot with no chip is a machine: it does exactly what the tiles say. A bot with chips is an **agent**: the tiles propose, the chips dispose. The `watch-obstacle` tile doesn't steer — it declares *what matters*, and the chip decides *when*.

That inversion is the whole lesson: **in the API world you call intelligence. In the crystal world you grow a temperament and negotiate with it.**

## The two E-menus

**[E] BUILD** — physical assembly. Chassis, wheels (each size changes the drive constants the compiler emits), motors, the Arduino with its chip sockets, battery, bumpers. What you bolt together determines what the PROGRAM menu is allowed to assume: no wheels, no drive blocks; no socket, no chips.

**[E] PROGRAM** — tile programming (the existing editor), extended with a chip rail. Chips appear on the rail once mounted in BUILD; their agentic tiles slot into the same compile path. Codegen stays honest: a SENTRY tile compiles to real Arduino C++ (an IR/proximity check wired to the pin the socket occupies) — the chip's "temperament" is just the guard condition and hysteresis the template emits. Fantasy in the fiction, real C++ in the flash.

## Fail states are canon

A cracked chip (grown too fast) keeps its mask but mumbles — tiles fire late or early within seeded bounds. This is not a bug; it is the *Most Interesting Failure of the Week*, and a cracked ECHO that replays your path slightly wrong is more fun than a working one.

## What stays a seam

Real model inference in the browser (an actual tiny model behind a chip) — deferred. The chip system is designed so a Worker-backed chip (scrap-spark pattern: pincher-cache, instant after first render) can drop behind the same tile contract later. The mask interface already says "what this chip may read"; a networked chip is just a mask pointed through a road.

---

*Verdict: grow, don't call. The yard doesn't have APIs. It has weather, salvage, and crystals with temperaments.*
