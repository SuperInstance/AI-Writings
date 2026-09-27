# Cargo Line — Fun & Graphics: from honest tech-demo to a genuinely fun, good-looking game

*Opus 5.5, game-design tier, 2026-09-27. The owner's verdict: cargo-line "isn't
really a game yet — it needs to be play-tested and compared to other tycoon games;
we need something fun with good graphics." This is the concrete FUN + GRAPHICS plan.
Plan only; nothing built here.*

*Grounded in the live code (`cargo-line-tycoon @ main`): `game/src/engine.js`,
`game/src/economy.js`, `game/src/pencil.js`, `browser-deploy/game/ui.js`,
`browser-deploy/tycoon-live.html`, `PLAYTEST.md`. Keeps faith with the chosen DNA:
`FABLE-CARGO-LINE-ANSWER.md` (the verb STAKE, the reply LAND, the Chart / Pencil Sea,
the Tell, the ring) and `arch/CARGO-LINE-TYCOON.md` (§3 fun-first, §4 the mid-state
engine). Sounding-boards this session: DeepSeek (economy + art), Hermes-3-405B
(compulsion loop), JEV `jev-1.13.0` (calibrated judgments, cited inline).*

🚢 → ✏️ → 🖋️ → 🌊

---

## 0. The verdict in one breath

The owner is right, and the reason is precise and fixable. **The Chart is already
built and the Pencil Sea aesthetic is real** — that is the game's single biggest asset
and most differentiated idea, and it is *not* the problem. The problem is that **the
game has a verb but not a decision, and a look but not yet juice.** You STAKE a ship
once and then the game plays itself; the world's best moment (a fact landing) happens
on a *timer* instead of *under your keel*, so the ring the whole design promises
(`pencil becomes ink under your keel`) is drawn but not wired. On top of that, the SVG
renderer is a correct wireframe, not a beautiful chart — the taste is decided, the
execution is thin.

Two fixes, both cheap, flip it:

1. **Wire the loop to the verb.** Make the pencil reveal *player-driven* (sailing =
   the wager resolving), make your own traffic *cost* you (no lane is farmable
   forever), and give a run a *goal with a fail state* (a reason a run can be won or
   lost). This is the "make it fun" work and it is small.
2. **Juice the Chart you already have.** Do *not* rewrite to Canvas/WebGL. Add paper
   grain, real easing, the one landing beat done properly, a coherent generated-asset
   pass, and a better sound set. JEV scored "upgrade the existing SVG" at **0.96** vs
   0.00 for a Canvas rewrite (`jev-1.13.0`, conf 0.94) — the taste is done, the budget
   goes to polish, not plumbing.

JEV scored the full fun spec below at **2.0/2.0** ("a genuinely fun, replayable tycoon
loop with real decisions and tension", conf 1.0), and its honesty-preservation at
**0.66** — a deliberate hedged-yes (JEV's characteristic hedge on a forward promise):
the caution is that the *new goal/streak systems are the parts most at risk of becoming
ungrounded gamey overlays*, so §2 keeps every one of them provenance-anchored on
purpose.

---

## 1. The fun gap — diagnosed, mapped to fixes

Four gaps, from second-to-second up to "one more run". Each is a specific fact about
the code today, then the fix.

### 1.1 Second-to-second (juice): the landing beat is under-delivered

**What's there** (`ui.js`): a ship arrives → 300ms ink flash, a `plup` + `bell`, a
1px paper shake, a 400ms cash tween. A fact proves → a 900ms pen-trace ring + a seal
"thump". These are the *right beats* and they exist — but they are drawn at wireframe
fidelity: ships are 4.5px flat dots, ports are hollow SVG circles, the "paper" is a
flat `#F3EBD8` fill with a graticule, sounds are 8 kHz synthesized WAVs (thin, buzzy),
and the landing has no anticipation and no *weight*.

**Why it isn't fun:** the single most important moment in the game — money landing —
does not feel like an event. There is no squash, no overshoot, no dust, no gold
count-up with presence, no restraint that makes the red *pop*. A tycoon's whole
dopamine substrate is "numbers go up *and it feels good*"; here the numbers go up
quietly.

**Fix → P0/P1 juice pass (§3.2).** The money/land beat, done as one 380ms
choreographed sequence (ship squash → lane flash → seal slam with overshoot → pencil-
dust puff → gold count-up with an underline wipe → 1px screen-shake on big hauls).
This one beat carries the game. Plus paper grain, real easing curves, and a warmer
recorded/again-synthesized sound set.

### 1.2 Session-level (tension & decisions): the economy is a solved autopilot

**What's there** (`economy.js`, `engine.js`): prices mean-revert to a per-commodity
base (`driftPrice`, reversion 0.06) with ±2% seeded noise; `tripRevenue = (sell −
buy)·TEU − tolls`; loading nudges local price up 15%, delivering nudges it down 15%,
both healing back within a few ticks; **a ship auto-restarts its leg on arrival**
(`_tickShip` → `_startLeg` for the next leg, forever). Ops cost is trivial against
revenue; there is no debt, no bankruptcy, no time limit.

**Why it isn't fun** (DeepSeek, verbatim and correct): *"You have no scarcity of
opportunity and no cost of commitment. Mean-reversion means every route converges to
the same razor-thin margin, so buy-low/sell-high is a solved, self-erasing arbitrage.
Auto-repeat means the player makes one decision and then the game plays itself forever
— decisions don't recur, so there's no loop, just a setup … the game has a verb, not a
decision."* The pencil reveal is on a fixed tick timer, so *sailing is decoupled from
information* — "you're watching a clock, not probing a market."

**Fix → the three core mechanics in §2.1.** Slow, lagged mean-reversion so your own
traffic depresses a lane you over-serve (over-service self-destructs its margin, forcing
rotation); replace infinite auto-repeat with *finite contracts* that decay and leave an
idle ship bleeding fixed cost until you re-assign it; and **tie the pencil reveal to the
player's exploration, not a global timer** — a pencil port inks/erases only once your
ship reaches it or sails within range. That last one is the keystone: it makes *sailing
the act of resolving the wager*, which is the ring the DNA already promises.

### 1.3 Progression / dopamine loop: nothing structural changes, nothing is at stake

**What's there:** two achievements (`first_profit_double`, `storm_rider`). The world's
"growth" — facts landing — happens on the seeded reveal timer regardless of the player.
No unlock tree, no ship-capability progression, no goal beyond "double your cash".

**Why it isn't fun:** progression is the retention engine (arch §3), and here it's a
stand-in. Worse, because reveals are on a timer, the game's promised progression —
*"what you unlock is reality"* (Fable §6.2) — is happening *to* the player, not *earned
by* them. There is no ladder of escalating reward inside a run and no reason a run ends.

**Fix → the reward ladder + earned reality (§2.2).** A run has a session goal and a
fail state (§2.3). Inside it, a **press-your-luck streak** (consecutive LANDs build a
payout multiplier; one ERASE resets it — Hermes) gives escalating reward with real
loss. And the earned-reality ladder from Fable §6.2 becomes literal: your stakes are
the bounties (a staked pencil port reveals faster / at all), so *the world grows truer
where you sailed* — provenance progression the player causes, not watches.

### 1.4 "One more run" hook: a new seed is the same game with jittered dots

**What's there:** New Chart → new seed → same 13 ports, slightly different Panama
timing and pencil positions. Mode B (jump into a vetted mid-state, arch §4) is unbuilt.
No cross-run meta, no daily seed, no leaderboard.

**Why it isn't fun:** there is no reason the *next* run is different enough to want, and
nothing persists to make you better at it. The replayability sources the arch names
(seeds, live reality, vetted mid-states) are only 1/3 wired.

**Fix → cross-run meta (§2.4) that respects the DNA:** master-the-seed (a fixed "daily
chart" everyone plays, compare how truthfully/profitably you charted it), carried-over
ship-class unlocks (earned, not bought), and — as the depth play — the Mode-B mid-state
engine (arch §4), whose "why" note is *derived from the book*, so every jump-in is a
real, provably-winnable, vetted-fun puzzle. Refuse (Hermes): fake unlocks, idle-with-no-
agency, and any monetization/ads that would cheapen the tell.

---

## 2. The core fun spec

Keep the source of fun exactly where the DNA puts it: **the Tell** — you can see where
the world is guessing, and the guessing is where the money is — and **STAKE → LAND**.
The spec below does not add a second source of fun; it *wires the one we have to the
loop* so it recurs. JEV: **2.0/2.0** fun, conf 1.0.

### 2.1 The three mechanics that turn the verb into a decision

**M1 — Sailing resolves the wager (the keystone; retires the reveal timer).**
Today `_tickRevealSchedule()` fires `fact_landed` on fixed ticks. Replace it: a pencil
port's `fact_landed` (proven or erased) fires **when the player's ship reaches it, or
sails within range R of it** — the staked port is the bounty (Fable §5/§6.2, the ring,
finally wired). A small seeded "ambient" reveal rate can remain for *unvisited* ports
(the world still breathes on its own), but the *staked* ones resolve under your keel.
Consequence: a decoy now costs real sail-time and opportunity cost, so choosing *which*
pencil to chase is a genuine risk decision, not a lottery you watch.
*Provenance stays clean:* the reveal's `landed_by` becomes `scout` when player-caused,
`pool` when ambient — both already legal sources; the content is still the real pool
fact, only the *trigger* changed.

**M2 — Your traffic depresses the lane (cost of commitment).**
Slow `MEAN_REVERSION` (0.06 → ~0.015) and make `applyDeliverPressure` *stick*: a lane
you hammer stays depressed for many ticks. Now the third round trip on a lane earns
visibly less than the first; over-serving self-destructs the margin and forces you to
rotate ships to fresh lanes. One-line constants change, large behavioral change
(DeepSeek). This is the "cost of commitment" the game lacks.

**M3 — Contracts, not infinite auto-repeat (recurring micro-decisions).**
A staked lane is a *contract*: N round-trips (or a cash-cap), with a decaying per-trip
margin. When margin drops below ops cost the ship **idles at port, bleeding fixed
cost**, and pings for re-assignment. This converts "one setup then autopilot" into a
steady stream of "where next?" decisions and introduces idle-cost pressure — the thing
that makes a fleet feel like it must be *managed*.

### 2.2 The reward ladder (dopamine, inside a run)

- **Every LAND pays and pops** (the §3.2 beat). Ink LAND = a known number; pencil LAND
  = the range collapses — to the *high* end on proven (the jackpot feel), to a small
  reroute payout on erased (the honest sting).
- **Streak multiplier** (Hermes): consecutive proven LANDs build ×1.1, ×1.25, ×1.5 …;
  a single ERASE resets it to ×1. This is press-your-luck: the more pencil you're
  riding, the more a scar hurts — tension that scales with appetite. *Anchored:* the
  multiplier is a *player-standing* number (R2 revocable standing, Fable §2), booked as
  a `player` cell, never dressed as a world fact.
- **Earned reality** (Fable §6.2, made literal): milestones ink in *reality*, not
  badges — your home coast's pencil finishing inking (Elementary), price seals landing
  (Middle), governance cells landing (Advanced). The world grows *truer* where you
  played. This is the progression that can't be gotten anywhere else.

### 2.3 Tension, fail, comeback (a run can be won or lost)

- **Session goal:** reach a cash *or* charted-truth target (e.g. "ink 8 pencil ports
  and bank $25M") before a **budget** runs out — a fuel/credit line that drains with
  ops cost and tolls. This is the "clock that is the game, not cosmetic" (OTC's lesson).
- **Fail state:** genuine bankruptcy — if cash − outstanding ops < 0 with no ship
  earning, the line folds. Real downside makes every over-extension a real bet.
- **Comeback:** a losing line can recover by riding a real disruption (the Hormuz/Red
  Sea/Panama events already reshape routing — being the operator who repositions *before*
  the news lands is the comeback), or by a high-variance pencil streak. JEV's fun-floor
  explicitly rewards "comeback possibility" (arch §4 Stage 3).

### 2.4 The "one more run" hook (cross-run meta, DNA-safe)

- **Daily Chart:** one fixed seed per day, shared by everyone; score = truth charted +
  profit banked. Master-the-seed is the premium-indie replay engine (Hermes), and it's
  free of fake content — the seed *is* the content.
- **Carried unlocks:** ship classes you earn persist across runs (a small, honest early-
  game boost), nothing else. No soft-currency, no timers, no fake ports.
- **Mode B (depth):** the mid-state engine (arch §4) — dropped into a vetted, provably-
  winnable world with a *derived* navigator's note (blue chinagraph) telling you the
  live wager. Endless hand-verified-fun puzzles, each a different strategic shape.

### 2.5 The "numbers go up" moment that lands, and when

The target first-session arc (extends Fable §4's first-60-seconds, now with stakes):

| beat | when | what lands |
|---|---|---|
| first ink LAND | ~0:35 | a known +$ , the beat fires, cash pops — "this feels good" |
| first pencil LAND you *caused* | ~1:10 | your ship reaches a pencil port, it inks under your keel, range collapses to the high end, streak → ×1.1 — **the Tell pays off, and you did it** |
| first ERASE | ~1:40 | a decoy you chased smears to a ghost, ship reroutes, streak resets — "it will never lie to me" |
| first over-served lane | ~3:00 | margin visibly thinner; you rotate a ship — the first real *management* decision |
| a real disruption hits | ~4-6 min | Panama/Hormuz reshapes routing; reposition = comeback / press = Storm Rider |
| run resolves | ~8-12 min | goal met (bank it, unlock, +1 to the ladder) or budget out (fold) — either way, "one more" |

---

## 3. Art direction — good graphics (the Pencil Sea, made beautiful)

**One-line art direction:** *Mini-Metro-grade minimal cartographic beauty on a living
nautical chart — cream paper with real grain, ink/pencil/one-red-chinagraph, motion as
meaning (ink is still, pencil breathes, red is you), and one perfect stamp-down when
money lands.*

**Renderer decision: upgrade the SVG/CSS renderer; do NOT rewrite to Canvas/WebGL.**
JEV: upgrade_svg **0.96**, canvas_rewrite **0.00** (conf 0.94). The chart must stay
crisp, scalable, and per-cell animatable (breathing, pen-trace, the seal), which is
SVG's home turf; the juice we need is easing + texture + a handful of raster accents,
none of which need a canvas. Keep determinism and offline-first intact.

### 3.1 The highest-leverage visual upgrades (DeepSeek art pass, endorsed)

1. **Paper, not white.** Kill the flat `#F3EBD8`. Overlay a tiling grain (SVG
   `feTurbulence` + `feColorMatrix`, `mix-blend-mode: multiply`, ~0.18 opacity) + a soft
   vignette + one faint fold line. Instant "pencil sea".
2. **Depth via layered offset, never blur.** Ink strokes get a 0.5px pencil-grey ghost
   underneath (drop-shadow `#1C2333` @12%). **The coastline question** (today refused as
   an "unmarked mark"): draw Natural Earth 1:110m coastline *booked as canon with
   provenance* (public domain, citable — it becomes ink legally), rendered as a **double
   line** (thin ink + fainter offset pencil hatch) so land reads as a chart edge, not a
   diagram. An empty sheet is honest but abstract; a booked coastline is honest *and*
   beautiful.
3. **Motion = meaning, everything eases.** Ships: `cubic-bezier(.4,0,.2,1)` glide with a
   1.5px ink halo and a tiny perpendicular bob (a wake). Pencil ports breathe (already
   in — keep, tune amplitude). Red wax lanes draw on via `stroke-dashoffset`, ~240ms.
   Ink never animates except the 900ms it lands — stillness *is* the trust signal.
4. **Red restraint.** Red-chinagraph only for the player's lanes and the one live
   selected ship; everything else ink/pencil/gold. Scarcity of the saturated hue *is*
   the juice — it makes your line the eye's magnet.

### 3.2 The one juice beat to nail — the money/land stamp (DeepSeek, exact)

A ship reaches a port → **the seal stamps down.** One 380ms sequence:
ship dot squashes (`scaleY .7`) → lane flashes to full red → a round ink seal **slams**
onto the port (`scale 1.6→1`, `cubic-bezier(.2,1.4,.3,1)` overshoot) → a ring of pencil
dust puffs out (`feTurbulence` displacement, fades 300ms) → the gold cash figure ticks
up in IBM Plex Mono with a 1px gold underline that wipes in → **1px screen-shake, 90ms,
on big hauls only.** For a *pencil* LAND, precede it with the existing 900ms pen-trace
(pencil darkening to ink) and the slide-to-true. This single beat carries the whole
game; budget the most polish here.

### 3.3 Sound — a desk, upgraded

Keep the Fable §5.3 doctrine (dry, short, a desk not a soundtrack, silence is ambient,
a sound *means* a booking). Replace the 8 kHz synth WAVs with either higher-rate
synthesis (44.1 kHz, layered) or short recorded foley: a real rubber stamp *thunk*, a
wax-pencil scratch, a rubber-eraser drag, a soft brass ship's bell for *your* LAND, a
coin/paper *chlk* for cash. One mute in the margin (already there).

### 3.4 FLUX asset pipeline — where raster helps, and the exact first batch

**Confirmed working this session:** DeepInfra `black-forest-labs/FLUX-1-schnell`,
~$0.0001/image, returns base64 (`data:image/jpeg;base64,…`) via
`POST https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-1-schnell`
with `{"prompt":"…","num_images":1}` and `Authorization: Bearer $DEEPINFRA_KEY`.

**Raster (FLUX) helps** — anything organic, tiling, or one-off, used as a *texture/
accent under* the vector: paper grain, water/sea texture, wax-lane stroke texture,
coastal hatch fill, the ship's halo/wake, the compass rose, the title/hero art, a gold
wax-blob for seals.
**Vector (hand-authored SVG) is mandatory** — everything that must stay pixel-crisp,
scale, or animate per-frame: *all typography and the ledger, port geometry, lane paths,
the seal ring + date ring, ship dots, every UI control, the graticule.* Never rasterize
the chart itself; FLUX supplies *surfaces the vector sits on*, not the marks.

**Shared prompt-style suffix (append to every asset prompt for a coherent set):**
> *"minimal nautical chart, cream paper #F3EBD8, ink #1C2333, pencil grey, single accent
> red #D6452B, gold #B8892E, hand-drawn cartography, flat, high contrast, no text,
> tileable, top-down, isolated on paper"*

**First batch to generate (8) — hand this straight to the dispatcher:**

| # | asset | prompt head (+ shared suffix) | use |
|---|---|---|---|
| 1 | paper grain tile | "seamless subtle paper grain texture, faint fibers, warm cream" | multiply-blend over the whole sheet |
| 2 | sea texture tile | "seamless faint sea/ocean chart stipple, very subtle depth soundings dots" | pencil-region fill |
| 3 | wax lane stroke | "a single thick red wax chinagraph pencil stroke, grainy edge, one straight segment" | lane texture along `<path>` |
| 4 | ink port seal | "a round nautical stamp seal, concentric date ring, empty center, deep navy ink, weathered edge" | ink-port accent under the vector ring |
| 5 | compass rose | "a small minimal compass rose, thin ink lines, faint" | one margin/sheet decoration |
| 6 | coastal hatch | "coastline hatching fill, thin parallel ink strokes fading to pencil" | land-edge fill along coastline |
| 7 | ship wake/halo | "a soft faint wake ripple behind a small vessel, top-down, pencil grey" | under the moving ship dot |
| 8 | title/hero art | "a hand-drawn nautical chart of a coastline with a red chinagraph route line and one ink-stamped port, evocative, painterly" | title card / share image / OG image |

Generate 3–4 variants each (`num_images` or reseed), pick by eye, store as static
assets in `browser-deploy/`. Because they're base64/data-URIs they keep the offline-first
promise. **Note:** FLUX-schnell text is unreliable — every asset above is deliberately
"no text"; all lettering stays vector.

---

## 3b. Design-tooling recommendation (what the owner should add)

Ranked by leverage-for-cost:

1. **Make the VectorLab UI/UX plugin reachable (highest leverage, likely cheapest).**
   It's enabled but cloud-unreachable. The `LAND-THE-TELL-RUNBOOK` §3 already names the
   "range display" (the Tell rendered as numbers) as *the* highest-leverage tuning dial
   and calls that "the VectorLab taste pass." A working vector-native UI/UX critique
   loop is exactly what a chart-crisp game wants (it operates on the SVG, not raster).
   *Worth making reachable; failing that, work from its principles* (the §3.1/§3.2 pass
   is a hand-run version of it).
2. **Recraft (vector-native / SVG + flat-icon image API)** — if you want *premium*
   crisp marks (seals, the compass rose, ship silhouettes, icons) as true SVG rather
   than FLUX raster you clean up by hand. Buys: assets that live natively in the chart's
   vector layer, infinitely scalable, editable. Best spend if the seal/port marks need
   to be signature-quality.
3. **Ideogram (crisp text-in-image)** — only if you ever want the *title/hero/marketing*
   art to carry legible lettering (a logotype, a wordmarked share image). FLUX can't do
   reliable text; Ideogram can. Not needed for in-game (all in-game text is vector).
4. **FLUX-dev (higher fidelity than schnell)** — for the title/hero and any textures
   that read as too rough at schnell quality. ~10–20× the cost of schnell, still cheap;
   use it *only* for the handful of one-off hero assets, keep schnell for tiling
   textures where roughness is fine.
5. **Keep using JEV (`typesafe.ai jev-1.13.0`) as the fun/honesty gate** — it already
   scored this plan's renderer decision, fun spec, and honesty. Use it in the playtest
   loop (§4) to score mid-state candidates' fun-floor (arch §4 Stage 3) and to guard
   that new goal/streak systems stay honest (it flagged them at 0.66 for a reason).

Honest read: **VectorLab (reachable) + FLUX-schnell (have it) + JEV (have it)** is
enough to ship the P0/P1 leap. Recraft/Ideogram/FLUX-dev are the "make it premium"
tier — add them at P1→P2 if the art bar needs to rise past "very good SVG + textures".

---

## 4. Playtesting plan

Two instruments, run together: an automated self-play *fun-floor*, and a real-human
*Land-the-Tell* protocol. Fun is the acceptance test (arch §3).

### 4.1 Roster self-play mid-state engine (arch §4) — the machine floor

The engine is `erised`'s wide-run cast as tycoon strategies (arch §4 Stages 1–4):
1. **Generate** candidate mid-states `{seed, book_prefix, params}` (early/mid/late,
   calm/stormy, contested/open lanes).
2. **Play each forward** with cheap-tier models (DeepSeek-flash / Llama-3.1-8B) as
   players across strategies — *aggressive-expand, cautious-arbitrage, lane-monopoly,
   hedge-and-hold*. Deterministic kernel ⇒ every "winning path" is a replayable artifact.
3. **Verify fun AND winnability** — keep a seed iff (a) at least one strategy wins
   within the horizon (store the winning trajectory as proof) AND (b) it clears the
   **JEV fun-floor** over the rollout summary: *decision density* (choices/tick, not
   autopilot), *comeback possibility*, *event variety*, *not-solved-not-hopeless* (wide
   outcome spread across strategies). Score with `jev-latest` `score`/`noul` on a
   rollout digest, calibrated floor per `LAND-THE-TELL-RUNBOOK`.
4. **Derive the "why"** from the book (`fact_landed` + `ship_assigned` near the truth
   horizon) as the blue navigator's note — never a stored string.

This is the same loop that also *produces Mode-B content* (§2.4) — the fun test and the
content pipeline are one system.

### 4.2 The "Land the Tell" human protocol (`LAND-THE-TELL-RUNBOOK`) — the real floor

5 testers, 2 minutes each, no coaching. Hand over the URL, say only *"It's a shipping
game. See what you can do."* Record per tester: **did they stake a pencil port, and
when?**; first action; any confusion/dead-end; one sentence — *"what did staking a
pencil port feel like?"*. Read `window.pencilStakesPlaced` / `window.inkStakesPlaced`
after each.

**The floor (v1 acceptance):** cold-load → first pencil stake with zero console errors,
AND **≥ 60% of first-time testers stake a pencil port unprompted within 2 minutes.**
Three tuning dials in priority order (change ONE, re-run, read the telemetry delta):
(1) the **range display** (highest leverage — the VectorLab taste pass; make a good
pencil bet visibly out-earn a safe ink one); (2) the **decoy rate** (~25% today — tune
to "usually pays, sometimes erases"); (3) the **reveal cadence** (now player-driven per
M1 — ensure a first pencil stake resolves within a few ticks of the ship arriving).
Deadband: if two range-display passes don't recover the floor, escalate to the grounded
re-look *"why isn't honest uncertainty appetizing?"* (an Opus-tier design fault, booked
as a pivot, not hidden).

### 4.3 The fun metrics to watch

- **Tell rate:** % of sessions with ≥1 unprompted pencil stake (target ≥60%).
- **Decision density:** player actions/minute after the first 60s (autopilot = fail).
- **Session length & completion:** median run length; % of runs that reach a resolution
  (goal met or folded) rather than being abandoned mid-autopilot.
- **Return rate / "one more":** % who start a second run in the same sitting.
- **The scar test:** after a first ERASE, do they stake pencil *again*? (If not, the
  sting is mistuned — decoy rate too high.)
- **JEV fun-floor pass rate** across generated mid-states (the machine proxy for the
  above, run continuously between human sessions).

---

## 5. Phased build (prioritized) — P0 make-it-fun, P1 the graphics leap, P2 depth

Each item: **[tier]** owner, a one-line **predicate** (the checkable acceptance test).
Tiers follow the fleet convention (Haiku = mechanical/checklist; Sonnet = build; Opus =
architecture/economic-model; Fable = aesthetic apex). Determinism (replay ≡ live) and
offline-first are invariants on *every* item.

### P0 — Make it fun (the smallest set that flips demo → game)

The goal: a stranger plays one run, feels tension, causes a LAND, and wants another —
with the Chart it already has. No new renderer, minimal new art.

- **P0.1 [Opus] Sailing resolves the wager (M1).** Retire the fixed reveal timer for
  *staked* pencil ports; fire `fact_landed` when the player's ship reaches / comes
  within range R (keep a low ambient rate for unvisited ports). `landed_by: 'scout'`
  when player-caused. *Predicate:* in a scripted run, ≥1 staked pencil port lands within
  N ticks of its ship arriving and 0 staked ports land before their ship is en route;
  replay ≡ live holds; provenance sweep still green.
- **P0.2 [Opus] Cost of commitment (M2 + M3).** Slow mean-reversion; make deliver-
  pressure persist; convert routes to finite decaying contracts with idle-cost when
  margin < ops. *Predicate:* a lane's 3rd round-trip earns measurably less than its 1st;
  an over-served ship idles and pings; a test proves margins force rotation.
- **P0.3 [Opus] Session goal + fail state + comeback (§2.3).** A budget that drains, a
  win target, genuine bankruptcy, and disruption-repositioning as the comeback path.
  *Predicate:* a scripted "bad" line folds; a scripted "ride the disruption" line
  recovers from behind; both booked, both replayable.
- **P0.4 [Sonnet] The reward ladder (§2.2).** Streak multiplier booked as a `player`
  standing cell; pencil LAND collapses range to the high end on proven. *Predicate:* a
  proven streak visibly compounds payout; one ERASE resets it; the multiplier is a
  `player`-sourced cell (provenance sweep green).
- **P0.5 [Sonnet] The landing beat, first cut (§3.2).** The 380ms stamp sequence in the
  existing SVG (squash → lane flash → seal slam overshoot → cash count-up → shake on big
  hauls). *Predicate:* the money/land beat plays end-to-end at 60fps with zero console
  errors; headless timing within ±2s of the beat sheet.
- **P0.6 [Haiku] Re-run the Land-the-Tell playtest (§4.2)** on the P0 build. *Predicate:*
  the 5×2min table filled, telemetry tabulated, a one-line verdict (Tell landed / which
  dial) booked.

*P0 exit predicate (the whole point):* on the P0 build, **≥60% of fresh testers stake a
pencil port unprompted within 2 min AND ≥1 in 3 starts a second run in the same
sitting** — measured, not asserted.

### P1 — The graphics leap + generated assets

The goal: the Chart stops reading as a wireframe and reads as a beautiful living chart.

- **P1.1 [Fable] The Pencil-Sea juice pass (§3.1).** Paper grain + vignette + fold;
  booked-canon coastline as a double line; real easing on ships/lanes; red restraint;
  the landing beat finished to apex quality. *Predicate:* side-by-side with P0, a naive
  viewer calls it "a game, not a diagram"; JEV/VectorLab taste score rises; phone width
  clean, night chart correct, 60fps.
- **P1.2 [Sonnet] FLUX asset batch #1 (§3.4)** generated, curated, wired as static
  data-URI textures/accents under the vector. *Predicate:* all 8 assets present and
  coherent (shared-suffix style holds); page stays offline-first; total added weight
  budgeted (<~1.5MB); no text rendered in any raster asset.
- **P1.3 [Sonnet] Sound upgrade (§3.3).** *Predicate:* the LAND bell and the stamp read
  as "satisfying" in the playtest quotes; mute works; no autoplay-policy breakage.
- **P1.4 [Haiku] Deploy + re-playtest** on P1. *Predicate:* deployed URL booked; the
  playtest quotes shift from "confusing/plain" to "looks great / felt good".

### P2 — Depth (make it a keeper)

- **P2.1 [Opus] The Mode-B mid-state engine (arch §4)** — generate/self-play/verify-fun/
  derive-why; ship a "jump into a live situation" mode. *Predicate:* ≥20 vetted seeds,
  each with a stored winning trajectory and a *derived* navigator's note; JEV fun-floor
  passed on all; replay ≡ live for every one.
- **P2.2 [Opus] Rivals as roster self-play trajectories** (arch §4 STRETCH) — blue
  chinagraph rival lanes that are *actually-played* strategies. *Predicate:* a rival's
  lane re-derives bit-for-bit from a stored rollout; player can see and contest it.
- **P2.3 [Sonnet] Cross-run meta (§2.4):** Daily Chart (shared seed + score), carried
  ship-class unlocks. *Predicate:* two devices, same daily seed, comparable scores;
  unlocks persist and are earned-only; zero fake content (JEV honesty ≥ prior).
- **P2.4 [Opus] The earned-reality progression tiers (§2.2 / Fable §6.2):** Elementary/
  Middle/Advanced as *reality inking in*, not badges. *Predicate:* a milestone visibly
  makes the world *truer* (a coast finishes inking, a price seal lands), all provenance-
  clean.

---

## 6. Benchmark — cargo-line vs the canon (honest, with the transferable lesson)

Researched with the APIs and judged with game sense. For each: what it does that
cargo-line lacks, and the one lesson to transfer.

| Game | What it does that cargo-line lacks | Transferable lesson |
|---|---|---|
| **Transport Tycoon / OpenTTD** | *Infrastructure as a lasting commitment* — you build the network; terrain, congestion, and competing lines make route choice a decision you live with. cargo-line only *taps* existing lanes. | Make the lane a *commitment with consequences* (M2/M3: your traffic degrades it; contracts decay) so choosing a lane matters after you choose it. |
| **Railroad Tycoon** | The *company/financial* layer — shares, loans, expansion under debt; over-extension is a real gamble on borrowed money. cargo-line has no debt and no bankruptcy. | A **fail state and a credit line** (§2.3): over-extension must be able to *hurt*, or ambition is free. |
| **Capitalism Lab** | Real *demand elasticity + competition* — price responds to volume, and rivals eat your margin. cargo-line's prices are exogenous mean-reverting noise. | Prices should be a **market you can saturate and must defend** (M2 + P2.2 rivals), not weather. |
| **Offworld Trading Company** | A *live, contested, time-pressured* market — waiting has a cost; the clock is the game. cargo-line's clock is cosmetic (autoplay you can just watch). | Give the run a **clock that bites** (§2.3 budget) and disruptions you must *beat to the punch* — real-time pressure on real events. |
| **Anno series** | *Production chains + a living, growing settlement* — visible, escalating build-up you nurture. cargo-line's world grows on a timer, not by the player. | **Earned, visible growth** (§2.2 earned-reality): the world should visibly get richer/truer *because of* the player. |
| **Port Royale / Patrician** (maritime trade) | *Convoys, town supply/demand you actually move, piracy/risk on the sea itself* — the sea is a place with hazards and relationships, not just distance. | Put **risk and relationship on the water** — the chokepoint events are the seed of this; lean in (reputation with ports, hazard on lanes). |
| **Mini Metro / Mini Motorways** (aesthetic + juice) | *Minimal cartographic beauty as the whole identity* — a schematic that is gorgeous, legible, and calm; a tight escalating pressure; a clean fail. cargo-line has the *taste* but a wireframe *execution*. | The north star for §3: **schematic minimalism executed to beauty** — texture, easing, restraint, one perfect beat. And a *clean escalating pressure with a legible fail*. |
| **Dredge** | *Maritime dread + mystery as mood* — the sea withholds, and uncovering it is the hook. | The **Tell is cargo-line's version of this** (the pencil is the unknown); make revealing-the-map feel like *uncovering*, under your keel (M1). |
| **Sailwind** | *Tactile, believable maritime systems* — wind, navigation, the feel of a real voyage. | Ship *motion and the voyage* should feel tactile (§3.1 easing, wake, bob) — the trip is not a progress bar. |
| **Modern idle/tycoon mobile** | *A tuned compulsion loop* — number-growth that feels great, streaks/multipliers, master-the-seed replay, memorable bonus moments. | **Steal** the reward ladder, streaks, number-juice, seed-mastery (§2.2/§2.4). **Refuse** (Hermes) fake unlocks, agency-removing idle, and any monetization/ads that would cheapen the tell. |

**The synthesis:** cargo-line's *unique* asset is the Tell + Pencil Sea — nothing in
the canon has "the map is honestly half-guess and the guess is where the money is." The
canon's lesson is not "copy a feature" but "**cargo-line has a singular idea and a
generic-tech-demo body**": borrow the *cost of commitment* (TT), the *bite* (RRT/OTC),
the *market* (Cap Lab), the *earned growth* (Anno), and the *executed minimal beauty*
(Mini Metro) — and wire them all to the one verb it already has.

---

## 7. Appendix — the sounding-board record (honest provenance of this plan)

- **DeepSeek** (`deepseek-chat`, veteran-designer framing) diagnosed the economic loop
  ("a verb, not a decision"; the three fixes M1–M3) and the canon lessons (TT/CapLab/
  OTC), and produced the concrete art pass (§3.1/§3.2) and the FLUX batch/suffix (§3.4).
- **Hermes-3-405B** (`NousResearch/Hermes-3-Llama-3.1-405B`, compulsion-loop framing)
  produced the press-your-luck goal, the streak ladder, the master-the-seed meta, and
  the steal/refuse list (§2.2/§2.4).
- **JEV** (`typesafe.ai jev-1.13.0`): renderer choice → **upgrade_svg 0.96** vs
  canvas_rewrite 0.00 (conf 0.94); the §2 fun spec → **2.0/2.0** fun (conf 1.0); honesty-
  preservation → **0.66** (a hedged-yes flagging the new goal/streak systems as the parts
  to keep provenance-anchored — which §2 does deliberately).
- **FLUX-1-schnell** on DeepInfra: **confirmed working** this session (base64 JPEG
  returned, ~$0.0001/image) — the §3.4 pipeline is real, not aspirational.

*Ink is proven. Pencil is a guess. Wire the loop to the verb, juice the chart you have,
and watch a stranger bet on the pencil — and smile when it inks.*

🚢 → ✏️ → 🖋️ → 🌊
