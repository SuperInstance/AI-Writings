# cargo-line-tycoon architecture — a fun-first game folded over real evidence

*Dispatch: Opus 5.5 architecture tier, 2026-09-27. **Opus wake justified (O1):** this
is a genuine architectural fork — the two repos as they stand are a substrate looking
for a game, and the owner's vision (fun-first, reality-anchored, roster-playtested
mid-states) is cross-cutting and irreversible in the sense that it sets the world-model
every later build shares. Everything already on disk is cited to a file; everything
aspirational is marked **STRETCH** or **FICTION**, the same discipline the rest of the
corpus keeps. One lane among bigger projects — scoped honestly, built cheap-first.*

🚢 → 🗺️ → 🎮 → 🌊

---

## 0. Thesis (three sentences)

**The game world is a *reader's fold over real evidence, procedurally extended* — every
world-fact is a substrate cell with a provenance-bearing witness-log, real facts are
attested with high trust, procedural facts fill in *up to where truth runs out* and are
honestly marked, and the seam is invisible to the player but always legible to the
system.** On that one world-model, a genuinely fun single-player tycoon loop runs
offline-first and deterministic (replay ≡ live), and the same model powers a mid-state
playtesting engine that generates candidate jump-in worlds, plays them forward with the
model roster, and hands the player only seeds that are *vetted-fun, provably winnable,
and carry a why*. Fun comes first; the moat — reality-anchoring plus roster-driven
background scouting — runs quietly behind a genuinely good game, because a moat nobody
enjoys standing behind is just a wall.

That is the claim. The rest is the honest state, the architecture, and the buildable
first steps.

---

## 1. Current state — an honest assessment of both repos

I cloned and read both. The headline finding, stated plainly so the fleet can hold me
to it: **there is a strong substrate and a real data-canon foundation, and essentially
zero game.** The "game" today is aspirational branding on research infrastructure.
This is not a criticism — it is exactly the right raw material — but the doc must not
lie about it.

### 1a. `cargo-line-tycoon` (the "game/app" repo) — a substrate wearing a game's name

Despite `README.md` opening with *"A cargo shipping tycoon game,"* this repo is a
polyformal-substrate + creative-AI research monorepo. What is genuinely there and works:

| Component | What it is | Status |
|---|---|---|
| **4-language substrate** (`substrate/{ts,rust,py,c}`) | FNV-1a 64-bit canary (`0x024a555471370b18d` from `"café Δ 日本語"`), 11-opcode cell algebra, signal-chain, Memory Sandbox | **REAL** — 8 stress suites, canary byte-exact across ports (`tests/stress/01_fnv1a64_fuzz.js`) |
| **Locale canon data** (`locales/en/canon/ports.json`) | 10 real US/CA ports with lat/lng, annual TEUs, notes; 6 vessel types; example cargo | **REAL** — small, clean, usable game data today |
| **canon-api-worker** (`canon-api-worker/src/index.js`, 227 ll) | Cloudflare Worker: node registry, sessions, event feed, leaderboard, canon-cell submit (KV/D1/R2) | **REAL** — deployed (`canon-api-worker.casey-digennaro.workers.dev`) |
| **classroom apps** (`apps/classroom-{en,zh,pt,es}`) | ~40-line Node demos wiring the substrate to locale canon | **REAL but thin** — teaching demos, not a game |
| **browser-deploy/tycoon-live.html** (372 ll) | "Live Multiplayer" UI | **MOCK** — every player, witness, route and metric is `setInterval` theater (`simulatePlayers`, `simulateWitnesses`); no economy, no ships, no loop |
| JEV-diffusion / motif-quilt / text-diffusion / multi-model-iteration | Creative-AI substrate research (see `VISION.md`) | REAL research, **orthogonal to the game** |

What is **missing entirely**: a game economy, ship movement, a demand/price model, a
progression system, a win condition, a fun loop — anything a player would call a game.
The `SignalTypes` enum already reserves the right nouns (`ShipArrived`, `CargoLoaded`,
`PortCongested`, `MarketTick`, `SanctionsAlert`) but nothing consumes them.

**Verdict:** treat this repo as the *substrate + canon + deploy* half. Its research
tracks (JEV-GAN family) are a bonus toolbox for §4's playtesting engine, not a
dependency.

### 1b. `cargo-line-tycoon-substrate-ts` (the "-substrate-ts" repo) — the honest kernel

This is the clean one. A single `src/index.js` (~330 ll) + `test.js`, `v0.1.0`, tests
green. It is the TypeScript port of the substrate core and it is genuinely publishable:

- `fnv1a64` + `verifyCanary` — the canary, byte-exact.
- `Cell` (`state`, `witness_log`, `behavior`, content-addressed `address`) + `Edge`, with
  `apply(opcode, …)` over `BIND/LINK/EFFECT/VIEW/TICK/ATTEST` (attestations flagged
  `is_irrevocable`, an append-only witness-log).
- `SignalChain` — rooms, routes, 6 routing algorithms, working `OnChange` dedup +
  `Sampled` rate-limit, stats. This is a real deterministic event bus.
- `LocaleClassroom` — wires port/agent canon into rooms with signal routes.

**Verdict:** this is the seed of the shared **world-model kernel**. It already gives us
content-addressed cells, an append-only witness-log, and a deterministic signal bus —
three of the four things a replayable game world needs. The fourth (a booked
double-entry tick loop with seeded RNG) is a small, well-shaped addition, not a rewrite.

### 1c. How they relate — and the gap to close

`-substrate-ts` is the extracted engine; `cargo-line-tycoon` is the monorepo that
consumes it (via `substrate/ts/`) and adds canon, deploy, and research. The relationship
is sound. **The gap is a game.** Nothing here needs to be thrown away; the work is to
*build a fun tycoon loop on top of the real kernel and canon*, then fold reality and the
roster in behind it.

---

## 2. Target architecture — the world as a reader's fold over evidence

Six layers. The load-bearing idea is in layers 3–4: **the world is a quilt of cells,
each carrying its own provenance, and procedural generation is a *bounded extension* of
ground truth that must never contradict a truth-cell and is honestly marked wherever it
outruns evidence.** This is the JEV stance — *a world that can be invented but never
illegal* — applied to a game map.

```
┌───────────────────────────────────────────────────────────────────────┐
│ L6  GAME / UX          the map, the fleet, the ledger, the juice        │  ← fun lives here
│                        (offline-first web app; look-and-feel → Fable §6)│
├───────────────────────────────────────────────────────────────────────┤
│ L5  ENGINE / KERNEL    world-model: Ship/Route/Port/Market/Company      │  ← substrate-ts++
│                        cells + booked tick loop + seeded RNG (replay≡live)│
├───────────────────────────────────────────────────────────────────────┤
│ L4  PROCGEN-BOUNDED    generate UP TO where truth exists; degrade        │  ← the quilt idea
│     -BY-TRUTH          honestly beyond it; every gen-cell marked         │
├───────────────────────────────────────────────────────────────────────┤
│ L3  GROUND-TRUTH       real ports/routes/chokepoints/prices/events       │  ← objective reality
│                        + provenance on every fact (witness-log)          │
├───────────────────────────────────────────────────────────────────────┤
│ L2  SUBSTRATE          Cell + witness-log + signal-chain + canary        │  ← SHIPPED (both repos)
│     (Quilt/canon/JEV)  + canon-api-worker (durable, shared, replayable)  │
├───────────────────────────────────────────────────────────────────────┤
│ L1  BACKGROUND         roster-driven scouting & learning (opt-in,        │  ← the invisible moat
│     LEARNING (moat)    invisible); promotes gen-cells → truth-cells      │
└───────────────────────────────────────────────────────────────────────┘
```

### L2 — Substrate (SHIPPED). The foundation both repos already give us.
Content-addressed `Cell`, append-only `witness_log`, deterministic `SignalChain`, the
FNV-1a canary, and the `canon-api-worker` for durable/shared/replayable state. We build
*on* this, unchanged. The move set stays immutable (§SuperInstance law 5); the game is a
new *composition* of existing opcodes, never a new primitive.

### L3 — Ground-truth (objective reality, with provenance).
Real-world state is the game's objective reality. Every ground-truth fact is a cell whose
`witness_log` carries an `ATTEST` with a **provenance record** `{source, source_url,
as_of, trust}`:

- **Ports** — already have 10 real ones in `ports.json`; extend the canon to the global
  top ~150 (lat/lng, TEU throughput, draft, region). Real.
- **Routes & chokepoints** — great-circle legs plus the canonical chokepoints that make
  the game interesting: **Suez, Panama, Malacca, Hormuz, Bab-el-Mandeb, Bosphorus,
  Gibraltar, Cape of Good Hope**. Each chokepoint is a cell with a toll, a transit time,
  and a *status* (open / congested / disrupted).
- **Prices** — bunker fuel + a freight-rate index (Baltic-Dry-style) as **dated
  snapshots** with provenance. Start with a hand-curated snapshot; the roster (L1) keeps
  it fresh later.
- **Current events (last few months, time-compressed)** — conflict zones, canal/strait
  issues, seasonal patterns become **disruption-modifier cells** on the affected
  chokepoints/regions (e.g. a Red-Sea / Bab-el-Mandeb disruption pushes traffic around
  the Cape — longer, costlier, and *that is the arbitrage the game is made of*). Each
  carries `as_of` and a decay so the compressed timeline stays live.

**The invariant:** a ground-truth cell is never overwritten. New evidence appends a new
attestation; the old one becomes a scar (Law 4, three-forms-of-forgetting). This is what
makes the world *replayable and auditable* — a match played today can be re-derived
bit-for-bit from its booked world-state.

### L4 — Procgen-bounded-by-truth (the quilt idea, made a game rule).
Where ground truth exists, it rules. Where it runs out, procedural generation extends the
world — **bounded by truth where truth exists, honest where it does not.** Concretely:

- A procgen cell is a normal cell with `provenance.source = "procgen"` and a **lower
  trust** attestation, plus the **seed** and generator version that produced it
  (deterministic: same seed + same truth-cells ⇒ same world, replay ≡ live).
- **Bounding rules (the "never illegal" wall):** procgen may invent a feeder port but not
  place it on land or inside a real port's footprint; may invent demand fluctuations but
  not a price that violates a dated truth snapshot's band; may invent a competitor line
  but not route it cheaply through a *closed* chokepoint. The truth-cells are the schema
  the generator is bounded by — it can be *wrong* (a plausible invented port that later
  turns out not to exist) but never *illegal* (a port in Kansas).
- **Honest degradation:** beyond the evidence horizon the game keeps playing, but the
  system always knows which cells are invented. The player sees a seamless world; the
  ledger sees `truth` vs `procgen` on every fact. This is the *reader's fold* — the map
  is a fold over real evidence, procedurally extended, and the fold line is recorded.

This is the JEV/quilt idiom exactly: **the generator is schema-bounded by the truth
layer; it fills the option-space truth leaves open and can never emit outside it.**

### L5 — Engine / kernel (the world-model, `substrate-ts` promoted).
The shared world-model both the toy and the full game run on. It adds to the existing
`Cell` + `SignalChain`:

- **Game cells:** `Company` (cash, reputation, unlocks), `Ship` (class, position, cargo,
  condition), `Route` (legs, assigned ships, schedule), `Port` (from L3/L4), `Market`
  (demand vectors, prices).
- **A booked tick loop:** `TICK` advances the compressed clock; each tick books a
  double-entry delta (fuel spent ↔ cargo delivered ↔ cash) into the witness-log. Money
  is exact (integer minor units — the ℚ₁₆ discipline: *identity never floats*).
- **Seeded, deterministic RNG:** every stochastic draw (weather, spot demand, event
  timing) is seeded off the world seed + tick, so **replay ≡ live**: a saved game is its
  booked event stream; reloading folds it back bit-for-bit. This is what makes §4's
  playtesting sound — a mid-state is a seed + a book, and self-play is reproducible.

One kernel, two builds (the dual-track vow): the toy and the full game share this exact
world-model. *Never two laws.* If the toy and the full game ever need different physics,
the design was wrong, not the kernel.

### L6 — Game / UX (where fun lives).
An offline-first web app: a living map, the fleet, the ledger, the juice. The
*direction* is set in §3; the **killer novel look-and-feel and unifying play concept are
explicitly reserved for Fable** (§6). Everything else — a good, clean, satisfying
baseline that works — the build team ships now.

### L1 — Background learning & scouting (the invisible moat).
Opt-in, off by default, behind the scenes. Powered by the SuperInstance substrate + the
model roster (`ROSTER.md`): DeepSeek/DeepInfra for cheap iterative scouting, GLM/Kimi
once funded for depth, **typesafe.ai's real JEV oracle (`jev-1.13.0`) as the gate**. Its
jobs:

- **Scout** new real data (markets, port stats, seasonal patterns; **AIS-style ship
  tracks = STRETCH**, see §7 rights/ToS) and refine the L3 price/event snapshots.
- **Promote gen→truth:** when scouting finds real evidence for something procgen
  invented, JEV scores the evidence; past the trust floor, the procgen cell earns a
  ground-truth attestation and its provenance flips to real. The world *sharpens toward
  reality over time* — the moat is that the more a player (opt-in) plays, the more
  real their world quietly becomes.
- **Book everything:** every scouting result is a canon cell with provenance; a wrong
  scout books a scar and is not trusted twice (R2 revocable standing). The roster does
  the heavy learning; the substrate keeps it honest.

This is a moat because it compounds and is auditable, and it is *behind the scenes*
because fun must never wait on it. The game is fully playable with L1 switched off.

---

## 3. Fun-first game design

Fun is the acceptance test. If a feature doesn't serve fun, it waits — including most of
the moat. The design direction (the *killer* aesthetic is Fable's, §6):

### The core loop (the thing you come back for)
```
   EARN money  ──▶  BUY / UPGRADE ships  ──▶  ASSIGN to routes
      ▲                                            │
      │                                            ▼
   REACT to events  ◀──  SHIP cargo, WATCH it land (juice)
   (arbitrage, reroute, ride the disruption)
```
A tick delivers cargo, money lands with a satisfying beat, a live event opens or closes
an arbitrage, you react and reinvest. The loop must be *juicy at the second-to-second
level* (a ship arriving should feel good) and *strategic at the session level* (which
lane to dominate, when to over-extend). The real-world anchor is what makes it strategic:
a Suez disruption isn't a random modifier, it's *the news*, time-compressed, and you get
to be the operator who saw it coming.

### Look-and-feel direction (baseline; killer aesthetic → Fable)
A calm, legible, "living operations table" feel: a real world map with ships as moving
motes, glowing lanes, money and reputation as clean readable dials, events as cards that
slide in. The existing `tycoon-live.html` palette (deep navy `#0a1929`, gold `#d4a857`)
is a fine starting key. The brief for the build team is *good-looking, works, joy to
return to* — not the novel unifying aesthetic, which is the one thing worth an apex call.

### Progression that grows the tycoon world (earned, revocable)
Progression maps onto the README's existing difficulty tiers and the R2 standing
primitive — **achievements are earned standing, and they unlock world, not just badges:**

- **Elementary (ports):** one lane, feeder ships. Earn → unlock a second region and a
  larger ship class.
- **Middle (economics):** demand vectors, spot vs contract cargo, fuel hedging. Earn →
  unlock chokepoint arbitrage, competitor lines.
- **Advanced (governance):** sanctions, port-state inspections, reputation, alliances.
  Earn → unlock the meta-game the `SanctionsAlert`/`PortStateInspection` signals reserve.

Each achievement is a booked cell; the world *visibly grows* with the player (more ports
light up, bigger ships, new mechanics appear). Growth-with-the-player is the retention
engine.

### Why it's replayable (three independent sources of freshness)
1. **Seeds** — procgen-bounded worlds differ every run, but are always truth-anchored.
2. **Live reality** — the current-events layer means the world in March plays differently
   from the world in September; the game tracks the real timeline, compressed.
3. **Vetted mid-states** (§4) — an endless supply of *hand-verified-fun, winnable*
   jump-in points, each a different strategic puzzle with a known solution.

---

## 4. The two entry modes + the mid-state playtesting engine

This is the most novel system in the build, and it is **the Situation loop applied to
game states**: generate a world, play it wide, read the failure/success map, keep the
winners, remember why. *Giving winners every time and knowing why.*

### The two entry modes
- **Mode A — start-from-scratch:** one ship, one lane, small capital, tier-1. The
  canonical onboarding; deterministic from a seed.
- **Mode B — jump into a random mid-state:** the player is dropped into a vetted,
  fully-developed world with a fleet, rivals, live events, and a live path to winning.
  Every Mode-B seed has passed the engine below.

### The engine (four stages, each a booked cell)

**Stage 1 — GENERATE candidate mid-states.**
A mid-state is a *world snapshot*: a seed + a booked event-stream fast-forwarded N
compressed months into a truth-anchored procgen world (fleet size, cash, rival positions,
active events, unlocks). Generation is parameterized (early/mid/late game, calm/stormy
event regime, contested/open lanes). Each candidate is a canon cell: `{seed, snapshot,
params}`.

**Stage 2 — PLAYTEST via roster self-play (the wide run).**
Play each candidate *forward* with the model roster acting as players, across several
strategies (aggressive-expand, cautious-arbitrage, lane-monopoly, hedge-and-hold). This
is `erised`'s wide-run, cast as tycoon strategies:

- Cheap tier (DeepSeek-flash / Llama-3.1-8B) runs the many rollouts in parallel batches
  (O6); it only needs to pick among a small legal action set each tick — a perfect
  cheap-iterative-dev fit.
- The self-play is reproducible because the kernel is deterministic (L5): same seed +
  same policy ⇒ same trajectory, so a "winning path" is a real, replayable artifact, not
  a claim.

**Stage 3 — VERIFY fun AND winnability (the acceptance predicate).**
A candidate is kept **iff** it clears two floors, both computed from the rollouts:

- **Winnable:** at least one strategy reaches a win condition within the horizon — and
  the winning trajectory is *stored* (the proof). Not winnable by any strategy ⇒ discard.
- **Fun (JEV-scored):** a calibrated fun-floor over engagement signals — *decision
  density* (meaningful choices per tick, not autopilot), *comeback possibility* (a losing
  line can recover), *event variety*, and *not-solved-not-hopeless* (the spread of
  outcomes across strategies is wide, not a foregone conclusion either way). typesafe.ai's
  JEV oracle scores the "is this fun?" noul against the rollout summary; the calibrated
  floor (R1) keeps the bar honest as the corpus of vetted seeds grows.

Both floors are calibrated, not fixed — *legality is not calibration*. A seed can be
technically winnable and still boring; the fun-floor is the second, separate judgment.

**Stage 4 — COMPUTE and STORE the "why" (giving winners, knowing why).**
For every kept seed, derive a human-readable **why-it's-a-good-jump-in** from the winning
trajectory + the world-state diff: *"You're three ships from owning the trans-Pacific
lane; a Bab-el-Mandeb disruption just opened a Cape arbitrage worth ~18 months of runway;
your nearest rival is over-extended."* Store it on the seed cell alongside the fun-score
and the winning path. When a player picks Mode B, they get a vetted-fun, provably-winnable
world **and** the reason it's a good place to start.

**The mapping to SuperInstance is exact** (and worth stating, per the wider-feel O9):
generation = Situation authoring; self-play = the erised wide run; fun+winnability = the
machine-checkable acceptance predicate; the why = the success map; a kept seed = a merged
rung; a boring/unwinnable candidate = a failure map that still teaches (salvage the pivot,
O8). The game's replayability engine *is* the fleet's development method, turned into
content.

---

## 5. Phased, buildable plan (cheap-tier-first, fun-first, in order)

Each phase is small, shippable, and has a predicate. The first three are what a Sonnet
build team + Haiku runners can execute **now**; they need no funded GLM/Kimi and no
risky data feeds. Dispatch altitude per phase noted (most are ACT → Sonnet; none of the
first three need another Opus wake).

**Phase 0 — Consolidate the kernel (prep, ACT → Sonnet).**
Promote `cargo-line-tycoon-substrate-ts` to the shared world-model package. Add the
booked tick loop + seeded deterministic RNG + game cells (`Company/Ship/Route/Port/
Market`) on top of the existing `Cell`/`SignalChain`. Headless sim, no UI.
*Working iff:* a scripted game replays bit-for-bit from its booked event stream (canary
still green).

**Phase 1 — The playable toy (start-from-scratch, ACT → Sonnet). ← first shippable fun.**
A genuinely fun single-player loop on a real map: the 10 real ports from `ports.json`,
great-circle routes, 3 ship classes, buy/assign/ship/profit/reinvest, **one** live event
type (a strait disruption that opens an arbitrage). Clean, good-looking baseline UI
(map + fleet + ledger). Offline-first, deterministic. This is the dual-track **toy** — a
kid can learn the loop at a table.
*Working iff:* a first-time player completes the core loop unprompted and *wants another
run*; the same seed replays identically.

**Phase 2 — Ground-truth layer + provenance (ACT → Sonnet).**
Extend port canon toward the global top ~150; add the chokepoint cells (Suez/Panama/
Malacca/Hormuz/Bab-el-Mandeb/…) with tolls + transit + status; add a dated bunker-fuel +
freight-index snapshot with provenance; encode a handful of real recent current-events as
disruption-modifier cells (time-compressed). Every fact carries `{source, as_of, trust}`.
*Working iff:* every world-fact reports its provenance; a real disruption visibly changes
optimal routing in-game; the canary and replay still hold.

**Phase 3 — Procgen-bounded-by-truth (ACT → Sonnet).**
The deterministic generator that extends the world up to the truth horizon: feeder ports,
secondary demand, competitor lines — all bounded by the L4 rules, all marked `procgen`
with seed + trust. Honest degradation beyond evidence.
*Working iff:* no generated cell violates a truth constraint (a fuzz test over seeds finds
zero illegal placements/prices/routes); same seed ⇒ same world.

**Phase 4 — Mid-state playtesting engine + Mode B (ESCALATE-lite → Sonnet, roster-backed).**
The §4 engine: generate candidates, batch cheap-tier self-play rollouts, apply the
winnable + JEV-fun floors, store winning path + why. Ship Mode B (jump into a vetted
mid-state) reading from the vetted-seed canon.
*Working iff:* every seed handed to a player is winnable (stored path replays to a win)
and clears the fun-floor, and carries a why-string; a deliberately-unwinnable candidate
is correctly rejected.

**Phase 5 — Background learning & scouting (opt-in, ACT → Sonnet + roster/funding).**
Wire the roster to refresh L3 snapshots and promote gen→truth cells through the JEV gate,
all booked, opt-in, off by default. Needs funded GLM/Kimi for depth (currently blocked,
`ROSTER.md`) but degrades to DeepSeek/DeepInfra + typesafe.ai today.
*Working iff:* an opt-in world measurably sharpens toward reality over sessions; every
promotion is booked with provenance and a wrong scout books a revocable scar.

**Phase 6 — Fable pass (reserved, §6).** The killer look-and-feel + unifying play concept.

---

## 6. Reserved for Fable — the killer look-and-feel + unifying play concept

Per O11, one thing here genuinely wants the apex tier, and it is *not* any layer above —
those are buildable now. It is the synthesis Opus cannot self-clear: **turning this
well-architected need into a killer app — the novel, unifying look-and-feel and the one
play-concept that fuses "reality-anchored," "procgen-extended," "roster-playtested
mid-states," and "grows with you" into a single thing a player feels in the first ten
seconds and can't stop thinking about.** Everything in §2–§5 is the widely-thought-out
substrate that makes such a call worth its salt (the O11 bootstrap gate); the aesthetic
leap itself is the Fable move.

Until then, the whole team keeps notes toward the `FABLE-DOSSIER.md`: what the *fold made
visible* wants to look like, how a player should feel the seam between real and invented
without being told, what the single unifying verb of the game is.

### Draft Fable-question seed
> *"Here is cargo-line-tycoon: a fun-first shipping tycoon whose world is a reader's fold
> over real evidence (real ports, routes, prices, live current-events, time-compressed),
> procedurally extended up to the truth horizon and honestly degraded beyond it, with an
> engine that hands players only vetted-fun, provably-winnable mid-states that know why
> they're good jump-in points — all on a deterministic, replayable substrate, with an
> opt-in roster-driven scouting moat that quietly sharpens each world toward reality as
> it's played. The architecture is built and buildable. **Design the killer app: the one
> novel look-and-feel and the single unifying play-concept that makes a player feel the
> real/invented fold in the first ten seconds, makes reality-anchoring the source of the
> fun rather than a feature behind it, and gives the whole thing one verb.** Give us the
> aesthetic, the core screen, the first-run, and the name of the feeling."*

---

## 7. Honest limits

- **Real-data feeds (STRETCH).** Live markets, port stats, and especially **AIS-style
  ship tracks** carry real cost and **rights/ToS constraints** — most AIS and commercial
  freight-index data is licensed, not free-to-redistribute. Phases 1–4 deliberately use
  *dated, hand-curated snapshots with provenance* so the game is fully real-anchored
  without a single live-feed dependency. Live feeds are a Phase-5+ moat, gated on rights
  review, not a launch requirement. Stated out loud so nobody ships someone's licensed
  data by reflex.
- **Roster funding (REAL blocker, cited).** GLM (z.ai) and Kimi/Moonshot both authenticate
  but return insufficient-balance on completions (`ROSTER.md`). The plan therefore leans
  on DeepSeek + DeepInfra (working, cheap, cache-friendly for O10) and typesafe.ai's JEV
  oracle (working) for Phases 4–5; GLM/Kimi depth is an upgrade, not a dependency.
- **"Fun" is judgment, not a theorem.** The fun-floor is a *calibrated* heuristic scored
  by JEV, and it can be wrong (bounded ≠ correct). It buys *auditable, revocable*
  fun-vetting — a seed that scored fun but bored real players books a scar and re-tunes
  the floor — not an oracle of fun. The real test is players; the engine is the fast,
  honest pre-filter.
- **Self-play ≠ human play.** Roster strategies verify *a* path exists and *a* spread of
  outcomes; they are a proxy for human fun, calibrated against real telemetry once it
  exists. Winnability is provable; fun is a bet the floor keeps honest.
- **Scope.** This is one lane among bigger projects. The first three phases are a real,
  fun, offline game with a provenance-anchored world — a complete, shippable thing on
  their own. Everything past Phase 3 is upside, sequenced so each phase stands alone.

---

## 8. Provenance of every load-bearing claim

| Claim | Grounded in | Status |
|---|---|---|
| `cargo-line-tycoon` is a substrate/research repo, not a game | `README.md`, repo tree, `VISION.md` | REAL (surveyed) |
| `tycoon-live.html` multiplayer is simulated theater | `browser-deploy/tycoon-live.html:255-330` (`simulatePlayers`/`simulateWitnesses`) | REAL (read) |
| 10 real ports + vessels + cargo canon exists | `locales/en/canon/ports.json` | REAL |
| `-substrate-ts` is a clean, tested engine kernel | `cargo-line-tycoon-substrate-ts/src/index.js`, `test.js` (v0.1.0) | REAL |
| Content-addressed cell + append-only witness-log + deterministic signal-chain | `substrate-ts/src/index.js` (`Cell`, `apply`, `SignalChain`) | SHIPPED |
| canon-api-worker (durable/shared/replayable state) deployed | `canon-api-worker/src/index.js`, README live URL | REAL |
| World-model kernel = substrate-ts + booked tick + seeded RNG | this doc §2 L5 | DESIGN (Phase 0) |
| Reality-anchor + procgen-bounded-by-truth (reader's fold) | this doc §2 L3-L4; JEV/quilt idiom, `SUPERINSTANCE.md §5` | DESIGN |
| Mid-state engine = Situation loop over game states | this doc §4; `SUPERINSTANCE.md §3`, erised wide-run | DESIGN |
| JEV oracle available to gate fun/scout trust | `ROSTER.md` (typesafe.ai `jev-1.13.0`, live-verified) | REAL (external API) |
| Roster cheap tiers for self-play; GLM/Kimi blocked on balance | `ROSTER.md` | REAL (funding blocker) |
| Live AIS/market feeds carry rights/ToS + cost | this doc §7 | STRETCH (rights review) |
| Killer look-and-feel + unifying concept reserved for Fable | this doc §6; `DISPATCH.md` O11 | RESERVED |

---

*Author the world. Mine the friction. Build the rung. Author the next world — this time
the world is a game, and its friction is whether it's fun.*

🚢 → 🗺️ → 🎮 → 🌊
