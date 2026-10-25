# FABLE-CARGO-LINE-ANSWER — the Tell, the one verb, Pencil Sea, and the thing we had upside down

*Fable (`claude-fable-5-1`), woken past the Fable-deadband a second time (O11), on
cargo-line-tycoon. Read in manifest order: `arch/CARGO-LINE-FABLE-BRIEF.md`,
`arch/CARGO-LINE-TYCOON.md` (§2 layers, §3 fun-first, §4 mid-state engine, §6
reserved), `FABLE-ANSWER.md` (Law 6, the Reader's Fold). Grounded at fire time in the
playable toy: `cargo-line-tycoon @ claude/phase0-1-playable` (011736b) —
`substrate/ts/src/world.js`, `game/src/engine.js`, `game/src/economy.js`,
`game/data/ports.js`, `browser-deploy/game/ui.js`, `browser-deploy/tycoon-live.html`.
Everything cited to a line is on disk; everything that extends past it is marked
**EXTENSION**. One question, seven returns, in the order asked. Not a summary.*

🚢 → ✏️ → 🖋️ → 🌊

---

## 0. The answer in one breath

**The feeling is the Tell**: in ten seconds the player sees a chart that is honestly
half pen and half pencil, and the honesty turns into appetite — *the pencil is where
the money is.* **The one verb is STAKE**: every action in the game is putting a ship
on a fact you cannot yet prove, and the world's only reply is **LAND** — a fact lands,
a ship lands, money lands, all booked. **The core screen is the Chart** — one sheet of
paper, three media (ink = attested, pencil = invented, red chinagraph = yours), no
panels, the ledger in the margin like a ship's log; the fold line is never drawn
because every mark is already one medium or the other. **The thing we had backwards**:
§2 puts truth at the bottom of the stack as *foundation* and the moat at the very
bottom as *invisible*; inverted, **truth is the loot and the moat is the surface** —
L1 does not sit under L6, it *lands onto* it, and the two are one event
(`fact_landed`) seen from two sides. The shipped toy already shows the cost of the old
orientation: of its three kinds of world-fact, only ports carry provenance
(`world.js:118`); prices (`world.js:122`) and the one live event (`engine.js:145-149`)
are invented and unmarked, and the event is *narrated as news*. In Pencil Sea an
unmarked cell cannot be drawn at all — there is no medium for it — so the design forces
the law: **a cell without provenance is refused at booking, never rendered.** The
three gifts carry exactly that into the codebase this week.

---

## 1. The feeling and its name — **the Tell**

A first-time player, ten seconds in, feels something specific and it is not "wonder"
and it is not "calm operations." It is the poker player's feeling when the table
leaks: *I can see exactly where this world is sure of itself and exactly where it is
guessing, and the guessing is where I get paid.*

Name it **the Tell**. The map has a tell. Its honesty about its own uncertainty is
not a disclaimer tucked in a tooltip; it is the loudest thing on the screen, and it
reads — instantly, wordlessly, to a child at a table — as an invitation.

Why this is the feeling that makes reality-anchoring *the source* of fun rather than a
feature behind it: **the pleasure of a wager is proportional to the trustworthiness of
the ground.** Nobody enjoys betting at a table they think is rigged; everybody enjoys
betting at a table they can see is honest. The ink is what makes the pencil delicious.
Take away the real ports with their dated seals and the pencil is just noise; take
away the pencil and the ink is just a spreadsheet. The Tell is the feeling of both at
once, and it is only possible because the world carries provenance on every fact.

The Tell is Law 6 felt from the inside. The player is a *reader*. The chart is *E* —
evidence, every leaf tagged. The player's risk appetite is *π*. Where they put ships is
their verdict. The substrate folds evidence into verdicts under a reader's weights; the
player folds a chart into stakes under their own nerve. **Same operation, money for
weights.** The game's fold and the substrate's fold are one idea because the player
*is* a reader, and the first thing a reader feels about honest evidence is: *now I
know what to bet.*

---

## 2. The one verb — **STAKE** (and the world's reply: **LAND**)

**Stake** is the verb because it is already three things at once and all three are the
game:

- **A prospector's stake** — you claim a piece of a world that is still being surveyed.
- **A gambler's stake** — you put money on something you cannot yet prove.
- **Standing at stake** — R2's revocable standing: a streak of stakes that landed earns
  you the right to bigger ones; one scar and you start the streak again.

Every player action is a variation of stake, with no second verb:

| what the player does | what it is | what the world replies |
|---|---|---|
| buys a ship | acquires a stake-carrier (a hull is a stake not yet placed) | the shipyard seal thumps; a ship at home |
| taps ship → taps port | **stakes** the ship on a lane: on every cell the lane crosses, ink or pencil | the chinagraph line draws; the ship sails |
| picks a pencil port | stakes on an *unproven* fact; the payout is a range, not a number | it **lands** (proven → payout collapses to the real number; erased → rerouted, a ghost on the chart, a scar in the log) |
| holds a lane through a disrupted canal | stakes on the weather (Storm Rider) | ink weather if the disruption is real news; pencil weather if it is the world's seeded climate |
| jumps into a Mode-B mid-state | picks up a stake somebody already placed, with a navigator's note explaining why it is live | the chart at that truth horizon, the note in blue chinagraph |
| opts into scouting | turns every stake into a **bounty** — the roster scouts what players stake first | facts land where the money is; the world sharpens *where you sailed* |

**Land** is not a second player verb; it is the world's only reply. A ship lands, a fact
lands, money lands, a scar lands. It is the family's own word for arrival — the last
answer defined 已落地 as *walking through your own door* — and in this game nothing is
real until it has landed in the book. Stake → land is the player-side reading of
evidence → fold.

The kid's-table version proves it is one verb: pen ports and pencil ports on a paper
map; a child puts a ship token on a pencil port (*stake*); next round the teacher turns
a card — "REAL: pen it in" or "NOT THERE: erase it, ship goes to the nearest pen port"
(*land*). One round and the child has the whole game.

---

## 3. The core screen — **the Chart**

One screen. Not a map card beside a buy card beside a fleet card beside a market card
beside a log (`tycoon-live.html:196-224`). **A single sheet of chart paper that fills
the viewport, with a margin.** The build team renders exactly this:

### 3.1 The three media (the fold, seen and never explained)

Real navigators work on a printed chart with pencil for dead reckoning and a red
chinagraph (wax) pencil for the current plan. Three media on one sheet is how the
truth/guess/plan distinction has been drawn on real charts for a century. We use it
unchanged, and it is why the fold never needs a legend — everyone alive knows the
difference between pen and pencil on paper:

| medium | provenance | how it looks | how it moves |
|---|---|---|---|
| **INK** | `source: canon \| scout`, attested, high trust | solid near-black line; each port a small round **seal** with the name in small-caps and a **date ring** (`as_of`) around the rim | **never** — except once, the 900ms it lands |
| **PENCIL** | `source: procgen`, seeded, lower trust | graphite, slightly hairy stroke; hollow port circle, no seal; **pressure = trust** (trust .9 is dark graphite, trust .3 is faint) | **breathes**: a 7s sine, ±0.6px, amplitude ∝ (1 − trust), phase from the cell's seed hash — uncertainty is motion |
| **CHINAGRAPH** | `source: player` — stakes, lanes, ships, notes | red-orange wax line, the only saturated color on the sheet; drawn at hand speed | ships slide continuously along it; the line past the last ink point is **dashed** (you are sailing on pencil) |

A fourth mark, rare and important: the **ghost** — an erased pencil cell. A rubber
smear leaves a 12% opacity shadow with a hairline strike through the name. It never
fully disappears: *fold the erasure in, don't mutate the past out* (G12). A ghost is a
scar the chart wears.

### 3.2 Layout (desktop and phone)

- **Sheet**: cream paper, faint ink graticule (lat/lng grid). The projection stays the
  clean schematic already in `ui.js:16-23`; the paper is the frame, not literal
  cartography. Coastline, if drawn, is light ink (Natural Earth 1:110m is public
  domain and can be booked as canon with provenance; if it is not booked, it is not
  drawn — no unmarked marks, §6).
- **Seals**: the ten real ports (`game/data/ports.js`) as ink seals with `as_of`
  rings. Home port's seal is larger with a chinagraph circle around it. The
  **shipyard** is a small seal at home; tap it to buy.
- **Two clocks, two media, top corner**: `CHART AS OF 2026-09-21` in **ink with a
  seal** (the truth horizon — the date of the last landed snapshot) and `day 14` in
  **pencil** (the game's compressed fiction). When a new snapshot lands, a new seal is
  stamped slightly offset over the old one; the stack of seals *is* the history of
  horizons.
- **Margin log** (right edge on desktop; a bottom drawer on phone): a typewritten
  ship's log. Cash total at the head, big, ink, gold. Entries: `d14  ship_2  landed
  Savannah  +$412,300`. Market prices are margin entries too, not a panel: each port's
  current price sits beside its seal as a small pencil number (prices are invented
  until a price snapshot lands; then that number gets its own tiny seal).
- **Chokepoints**: Panama drawn as ink (it exists, attested) with its **weather** drawn
  in the medium of its provenance: a seeded drought is **pencil hatching** over the
  canal (`pencil weather`); a real disruption that the roster lands is **ink hatching
  with a dated seal** (`ink weather`). The player can see at a glance which storms are
  news and which are climate.
- **No header, no start screen, no seed box in the player's face.** "New chart" and
  the seed live behind one small margin affordance. The game opens *on the chart*.

### 3.3 The stake interaction (the only interaction)

1. Tap a ship (idle, at a seal). Every reachable port lifts slightly; a chinagraph
   preview follows the pointer/finger.
2. Tap a port. A **stake note** appears in the margin, typewritten:
   - ink destination: `stake · ship_1 · 800 TEU · Seattle (ink) · 4 d · ≈ +$168k`
   - pencil destination: `stake · ship_2 · 800 TEU · Port Alder (pencil, trust .6) ·
     5 d · +$220k – $610k · unproven — if it isn't there you land at the nearest ink`
   - via a chokepoint: `· via Panama (ink · pencil weather)`
   The **range is the Tell rendered as numbers**. Ink gives a number; pencil gives a
   spread, and the spread's width is (1 − trust).
3. Confirm (tap the note, or tap the port again). The chinagraph line draws at hand
   speed; the ship departs with a small wake; time runs.

Recall = tap a sailing ship, tap "recall" in the note. That is the whole control
surface. Time auto-runs (~700ms/tick); tapping the sheet pauses; tapping again resumes.

### 3.4 Landings (the juice, every kind)

- **Ship lands** (the existing `ship_arrived`, `engine.js:180`): the chinagraph lane
  flashes ink-black 300ms; margin entry; cash tweens 400ms; a small ship's bell.
- **Fact lands — proven** (`fact_landed · proven`): the pencil port is *traced over by a
  pen* — the stroke darkens and thickens along its length over 900ms — and, if the
  guess was off, the port **slides to its true position** as it is inked (the generator
  jitters pencil positions; the snap-to-true is the fold correcting the reader, made
  visible). Then a seal **thumps** (scale 1.08 → 1.0, 1px paper shake). Any stake on it
  collapses its range to the real number. Margin: `SCOUT · Port Hueneme · PROVEN · as
  of 2024 · trust .9 · source ▸`.
- **Fact lands — erased** (`fact_landed · erased`): rubber smear 700ms, ghost remains,
  a hairline strike. Any ship en route is **rerouted** to the nearest ink port on the
  same coast; its chinagraph line is redrawn live; the margin books `stake_rerouted`
  and, the first time only: `first scar — every navigator has one.`
- **Snapshot lands** (a dated price/event snapshot): the `AS OF` seal re-stamps; every
  pencil price near the snapshot's facts gets a tiny seal; the deltas between the
  pencil estimate and the inked number are **the arbitrage** — and the player who
  staked toward it is the operator who saw it coming.

The player never reads a legend. Ink is still, pencil breathes, red is theirs, ghosts
are scars, seals are dated. The fold is seen in the first second and understood by the
tenth.

---

## 4. The first-run — the exact first sixty seconds

No logo. No start screen. No seed input. The sheet.

| t | beat | sound |
|---|---|---|
| **0:00** | Cream paper fills the viewport; the ink graticule fades up (300ms). | one low paper rustle |
| **0:01** | Ten seals thump on, west to east, ~120ms apart — Vancouver, Seattle, Los Angeles, Long Beach, Houston, New Orleans, Miami, Savannah, Baltimore, New York — each with its name in small-caps and its date ring. Los Angeles lands last, larger, and a chinagraph circle draws round it: home. | ten soft stamps, three pitch variants |
| **0:03** | Pencil arrives: 18–24 feeder ports and a few sketched lanes are *drawn onto the sheet* in one fast 1.2s hand-stroke sweep, hairy and grey. They begin to breathe. | graphite scratch |
| **0:05** | The date seal thumps into the corner: `CHART AS OF 2026-09-21`. Beneath it in pencil: `day 0`. | stamp |
| **0:06** | One margin line, typewritten, the only tutorial the game will ever show: *"Ink is proven. Pencil is a guess. Ships pay out on both — pencil pays more, and pencil can be wrong."* | typewriter, 6 keys |
| **0:08** | The first ship is already at home (a gifted Feeder). It pulses once. Margin: `stake it — tap the ship, then a port.` **The Tell has landed**: the player is already looking at the pencil. | — |
| **0:10–0:18** | Player taps the ship. Ports lift. Hovering Seattle shows `≈ +$168k · 4 d`; hovering a pencil port shows `+$220k – $610k · 5 d · unproven`. Most first players take the ink. Chinagraph draws; the ship departs. | wax-line draw; a small wake |
| **0:18–0:34** | Time runs. The ship slides along the lane. Pencil prices tick in the margin. **0:28 — a fact lands on its own**: a pencil feeder near Los Angeles is traced over in pen, slides 20 miles to its true position, and a seal thumps: `SCOUT · Port Hueneme · PROVEN · as of 2024`. The world got more real without the player, and they *watched it*. | pen-trace (900ms), stamp |
| **0:34** | `d4 ship_1 landed Seattle +$168,400`. Cash tweens up. | bell, ink-blot "plup" |
| **0:38** | The shipyard seal glows: a second Feeder is affordable. Player taps seal → Feeder. A ship appears at home. | stamp |
| **0:42–0:52** | The player stakes the second ship on a **pencil** port — forty seconds of the Tell working on them. The note reads the range and the reroute promise. Confirm. The chinagraph line goes **dashed** past the last ink point. | wax-line draw |
| **0:55** | Pencil hatching appears over Panama: `pencil weather · a drought-style slowdown, drawn from the 2023–24 precedent`. Nothing happens yet; the player has noticed the canal. | graphite scratch |
| **1:00** | Two ships, one landed, one sailing into pencil, one real fact landed on its own, +$168k, and one open question the player cannot put down: *is Port Alder real?* | — |

**1:12–1:20 (the hook resolves)**: the landing schedule is tuned so a first pencil stake
resolves within ~20s of being placed. Either **proven** — the range collapses toward the
high end, the port inks and snaps, the seal thumps, the payout lands — or **erased** —
smear, ghost, the ship's line redraws to the nearest ink port, a smaller payout, and the
margin says `first scar — every navigator has one`. Both outcomes are designed to be
*good*: the first is money, the second is the game showing it will never lie to you.
After that the player wants a third ship, and the loop owns them.

---

## 5. The aesthetic system — **Pencil Sea**

The "ink-still-wet" seed was right about the medium and wrong about the agent. It had
ink drying *on its own* while the player *watches the roster prove the world*. Pencil
Sea transmutes it: **pencil becomes ink under your keel** — facts land where you
staked, because your stakes are the bounties — and sometimes pencil is *erased*, which
the seed had no mark for. Keep the paper; change who holds the pen.

### 5.1 Palette (tokens on `:root`; night chart under `prefers-color-scheme: dark`)

| token | day (paper) | night (chart under a red lamp) | meaning |
|---|---|---|---|
| `--paper` | `#F3EBD8` | `#151A22` | the sheet; `body` background |
| `--grid` | `#D9CDB1` | `#232A35` | graticule |
| `--ink` | `#1C2333` | `#E8E2D2` | attested |
| `--pencil-1` | `#6F6D66` | `#8B919C` | procgen at trust 1.0 |
| `--pencil-0` | `#BDB7A8` | `#4A505A` | procgen at trust 0.0 (interpolate by trust) |
| `--chinagraph` | `#D6452B` | `#FF6A4A` | the player; the only saturated hue |
| `--chinagraph-2` | `#2B5FD6` | `#5B8CFF` | a previous navigator (Mode-B notes, rivals) |
| `--gold` | `#B8892E` | `#D6A94E` | seal date rings, the cash total — the one heir of today's `#d4a857` |
| `--ghost` | `#C9BFA8` @ 12% | `#6E7480` @ 12% | erased cells |
| `--scar` | `#8A3B2E` | `#C8563F` | the hairline strike |

Day is the default: a chart is paper. Night is not "dark mode" — it is the bridge at
night, and the tokens say so.

### 5.2 Motion — three tempos, each with a meaning

- **Stillness = proven.** Ink never animates except once, when it lands (900ms
  pen-trace + stamp). A still mark is a trusted mark.
- **Breath = uncertainty.** Pencil breathes: `sin(t/7s + φ)`, ±0.6px, amplitude ×
  (1 − trust), φ from the cell's seed hash so the sheet never breathes in unison.
- **Hand speed = intention.** Chinagraph draws at ~600px/s via stroke-dash; ships
  interpolate between ticks so they slide, never jump.
- **Impact = landing.** The only shake in the game: 1px paper shake, seal overshoot
  1.08 → 1.0, 180ms. Erasure: 700ms smear wipe, ghost remains.
- Nothing pulses for attention. Nothing glows. The chart is not a dashboard.

### 5.3 Sound-shape — a desk, not a soundtrack

Dry, short, paper-and-desk. No music loop by default. Everything ≤ 400ms except the
pen-trace. Silence is the ambient; a sound *means* a booking.

| sound | on |
|---|---|
| stamp (3 pitches) | a seal lands: port, date, shipyard |
| graphite scratch | pencil appears or redraws |
| pen-trace (900ms, fine continuous scratch) | pencil becomes ink |
| rubber on paper | erasure |
| ink-blot "plup" | cash lands |
| typewriter keys | a margin line |
| one small ship's bell | *your* ship lands — the only "game" sound in the set |

### 5.4 Type

- Chart names and seals: **Alegreya Sans SC** (Google Fonts), small-caps, 10–13px on
  the sheet, on a circle path inside seals. Nautical-chart register without pastiche.
- Margin log, numbers, stake notes: **IBM Plex Mono**. The ledger is typewritten. The
  cash total is Plex Mono at display size in `--gold`.
- No display face. The chart is the display.

### 5.5 Provenance, trust, and the fold line as language

- **Provenance = medium.** `canon`/`scout` → ink; `procgen` → pencil; `player` → chinagraph.
  There is no fourth medium, so there is no way to draw an unmarked fact (§6).
- **Trust = pencil pressure + breath.** Darker and stiller as trust rises; the last
  breath stops the moment it inks.
- **`as_of` = the seal's date ring**, and staleness is visible: a ring fades with age
  (a 2019 seal is fainter than a 2025 seal). Hold a seal to read `source_url`.
- **The fold line is never drawn.** It is the set of places where pencil touches ink,
  and it is *seen* everywhere because every mark is one medium or the other.
- **Two clocks, two media.** The truth horizon is ink with a seal; the game's day is
  pencil. The player learns without being told that the world's *facts* have a date and
  the game's *time* is a fiction running past it.

---

## 6. The one thing we have backwards

### 6.1 The assumption

§0 and §2 L4 of `CARGO-LINE-TYCOON.md` state the seam is *"invisible to the player but
always legible to the system."* §3 and L1 state the moat runs *"quietly behind a
genuinely good game … behind the scenes because fun must never wait on it,"* and §2
draws a six-layer stack with **truth as the foundation (L3), procgen as fill (L4), and
the moat at the very bottom (L1)**. The look-and-feel seed on the table softened this
(provenance as texture) but kept the orientation: the roster proves, the player watches.

### 6.2 The inversion

**Truth is not the foundation; it is the loot. The moat is not behind the game; it is
the surface. The seam is not hidden from the player; it is the only thing the player
looks at.** L1 does not sit under L6 — it *lands onto* L6. They are one event,
`fact_landed`, seen from two sides: to the roster it is a promotion through the JEV
gate; to the player it is the best-feeling moment in the game. The §2 stack is really a
ring: L3 → L4 → L5 → L6 → L1 → L3, and the ring closes through the player's stakes.

This makes the game a class better for three reasons, each checkable:

1. **The moat's conjecture is refuted by its own fuel.** §2 L1 claims the moat *"is a
   moat because it compounds … and it is behind the scenes."* But the moat is opt-in,
   and its only fuel is opt-in play. Nobody opts into something they cannot see. An
   invisible moat cannot compound through players; it can only compound through a
   budget. **The moat compounds iff it is the fun** — iff a fact landing is the
   moment players wait for. Visible → wanted → opted-in → fed. The "behind the scenes"
   clause is not caution; it is the moat's starvation.
2. **Progression stops being fiction.** §3's retention engine is *"more ports light up"*
   — invented ports unlocked by invented achievements. Inverted: what you unlock is
   *reality*. Elementary tier = the pencil around your home coast inking in; Middle =
   price seals landing (real dated snapshots replacing pencil numbers, with the delta
   as arbitrage); Advanced = governance cells landing (real sanctions/inspection
   regimes as ink). The world grows *truer*, not merely bigger, and a truer world is
   one the player cannot get anywhere else.
3. **Mode B's "why" becomes something you can see.** §4 stores a why-*string*. In
   Pencil Sea a mid-state is *a chart at a truth horizon with a live stake*, and the
   why is a previous navigator's blue chinagraph note *on the sheet*: a circled pencil
   port, an arrow, `the Gulf is still pencil; Savannah's real throughput just landed
   30% over the guess; nobody has repriced.` The why is derived from the book
   (`fact_landed` + stakes), not written beside it.

### 6.3 The bug it names (as the last call named C9)

The shipped toy already pays for the old orientation, and the manifest overstates what
is on disk. Manifest item 2 says *"the world carries provenance on every fact."*
On disk:

- **Ports** carry provenance: `makePortCell` (`substrate/ts/src/world.js:118`) defaults
  `{source:'canon', trust:1.0}`; `engine.js:61` books a `source_url`. ✔
- **Prices** carry none: `makeMarketCell` (`world.js:122`) has no provenance field;
  every price descends from `BASE_PRICE_BY_COMMODITY` (`economy.js:116-118`), a
  constant the data file itself calls *"flavor … not fabricated canon"*
  (`game/data/ports.js:13-20`). Ten market cells, all invented, all unmarked. ✘
- **The one live event** carries none: `_tickPanamaEvent` books
  `{type:'panama_disruption_start', duration_ticks}` (`engine.js:148`) with no
  `source`, no seed label, no trust — and the player-facing line at `engine.js:149`
  narrates it as news: *"Drought-driven congestion has spiked trans-coast transit time
  and tolls."* It is seeded weather (`rng.chance(0.035)`, `engine.js:145`) wearing a
  headline. ✘

So of the toy's three kinds of world-fact, **one is marked and two are invented and
unmarked** — and the seam is illegible *to the system* for two of three, not only to
the player. This is not a nitpick about metadata. In Pencil Sea an unmarked fact has
**no medium**: the renderer cannot choose ink or pencil for it, so it cannot be drawn.
The design forces the law the last answer named for receipts (G20a, refusal at
`book()`): **a cell whose provenance cannot be carried is refused at `cellFor`/`book()`
— never defaulted, never rendered.** Then the chart *cannot* lie, because it cannot
draw what it cannot classify. (Declared cost, as for G20a: content-addressed cells
change address when they gain a field, so `replay.test.js`'s fixed-seed hash changes
exactly once. Book it; do not hide it.)

**EXTENSION:** the ring reading of §2 is mine; the doc draws a stack. The refutation of
the moat conjecture is an argument from the moat's own opt-in clause, not a measurement
— the measurement is what the Haiku sweep's telemetry hook (§7.3) begins to collect.

---

## 7. The gifts — three moves, one per tier, this week

Each is a rung with a predicate. Together they put one new event in the kernel, one
new screen in the browser, and one law over every cell — and they are ordered so each
lands on the last.

### 7.1 Opus — architecture: **the Landing is the kernel's one new event, and the stack is a ring**

*Owner: Opus 5.5 architecture tier. Output: a revised §2/§4 of `CARGO-LINE-TYCOON.md`
plus a schema file the two builds below implement.*

1. **`fact_landed` — the single event L1 and L6 share.** Add to the kernel's
   witness-log vocabulary (`substrate/ts/src/world.js`) one entry type that every
   provenance transition must pass through:
   ```
   { type: 'fact_landed', entity_id, cell_type,
     from: { source, trust, seed_label? },
     to:   { source, trust, as_of, source_url? , seed_label? },
     verdict: 'proven' | 'erased' | 'revised',
     landed_by: 'pool' | 'scout' | 'snapshot',
     scout_ref? }
   ```
   Pool reveals, roster promotions, snapshot refreshes, and erasures are all this one
   entry. The chart renders landings *only* from it; Mode B's why is *derived* from
   the sequence of `fact_landed` + `ship_assigned` entries in a mid-state's book.
2. **The refusal law over cells.** `cellFor` (`world.js:99`) requires `provenance`
   for every world-fact cell type (`port`, `market`, and a new `event` type for
   chokepoint weather); `book()` refuses any `*_start` event without `provenance`.
   Refusal polarity, mirroring G20a: raise, never default. `ship`/`route`/`company`
   are player cells and carry `{source:'player'}`.
3. **The truth-pool doctrine: reality withheld, not invented.** Design the canon
   format `locales/en/canon/pool.json` — real secondary ports and dated facts, each
   `{value, source, source_url, as_of, trust}` — and a **seeded reveal schedule** so
   "grows toward real as you play" works *offline on day one*: the game ships with
   more truth than it shows and lands it over play; the roster (L1) *extends* the
   pool rather than being the only source of landings. State the honesty rule in the
   doc: a pool fact's *reveal time* is scheduled, its *content* is real, and the
   player-facing register never claims a live discovery — the margin says `SCOUT ·
   proven · as of <date> · source ▸`.
4. **The pencil generator's bound, restated so it is buildable this week.** Procgen
   feeder ports are emitted *from* the pool: for each pool fact, one pencil cell at a
   jittered position (±0.3°) with a generated name, plus a tunable share (~25%) of
   **decoys** with no fact behind them. Proven ⇒ snap-to-true; decoy ⇒ erased.
   This satisfies L4's *wrong-but-never-illegal* trivially (every pencil port is
   within sight of a real coastal port) and makes the decoy rate an honest **risk
   premium** — which is *why* pencil pays more.
5. **§4 rewrite in one paragraph:** a mid-state = `{seed, book-prefix, truth-horizon,
   live stakes, navigator's note}`; the why is a chinagraph-2 annotation derived from
   the book; the roster's self-play strategies are the procgen *rivals* (blue lanes on
   the chart), so every rival is a strategy that was actually played (**STRETCH**, but
   name it now so Phase 4 aims at it).

*Predicate:* a 60-tick scripted game's witness-log contains ≥ 1 `fact_landed` of each
verdict; zero cells without `provenance`; `stateHash()` identical across two engines
fed the same seed and actions (replay ≡ live with landings in the book).

### 7.2 Sonnet — build: **the Chart**

*Owner: Sonnet build team. Two PRs in order on `claude/phase0-1-playable`; the second
depends on the first.*

**PR 1 — engine (~300 lines, `game/src/`, `game/data/`, `substrate/ts/src/world.js`):**
- `pool.json` + `pool.js` mirror with 12–20 real secondary US/CA ports (Oakland,
  Tacoma, Prince Rupert, Port Hueneme, San Diego, Charleston, Norfolk, Jacksonville,
  Mobile, Tampa, Philadelphia, Boston, Wilmington NC, Everett — each with lat/lng,
  `source_url`, `as_of`, trust .9; **omit any entry that cannot cite a URL**).
- The pencil generator (seeded via `world.rng.fork('procgen:ports')`), decoys
  included; pencil market cells with `{source:'procgen', trust, seed_label}` and a
  price spread ∝ (1 − trust).
- The reveal schedule (seeded, tuned so the first landing is at ~tick 4 and a first
  pencil stake resolves within ~3 ticks of placement); `fact_landed` bookings;
  snap-to-true on proven; **reroute** on erased (`stake_rerouted` booked; nearest ink
  port on the same coast; days recomputed).
- `previewStake(shipId, portId)` → `{low, high, days, unproven, via:[{id, medium}]}`.
- Panama event gains `provenance: {source:'procgen', seed_label, trust}` and the log
  line moves to the pencil-weather register.
- Tests: extend `loop.test.js` with a pencil stake that proves and one that erases;
  `replay.test.js` re-pinned once with the declared cost in the PR description.

**PR 2 — renderer (replaces the map + panels in `browser-deploy/game/ui.js` and the
`tycoon-live.html` layout):**
- SVG layers in this order: paper/graticule → ink coast (only if booked as canon) →
  ink seals with date rings → pencil ports (breathing, pressure by trust) → ghosts →
  chinagraph lanes (dashed past the last ink point) → ships (interpolated between
  ticks) → chokepoint weather hatching in its medium.
- The margin log (right edge / bottom drawer under 640px); cash head; stake notes.
- The one interaction: tap ship → tap port → note → confirm; recall from a sailing
  ship's note; tap sheet to pause/resume; the shipyard seal.
- Animations exactly as §5.2: pen-trace + stamp on proven (with slide-to-true), smear
  + ghost + live reroute redraw on erased, 300ms ink flash + tween + bell on ship
  landing, re-stamp on snapshot.
- Tokens per §5.1 on `:root` with the night-chart variant; Alegreya Sans SC + IBM Plex
  Mono from Google Fonts; sound set as short inline-data WAVs with a single mute in the
  margin; 16px side gutter at phone width, no horizontal scroll.
- Delete the start screen; "new chart · seed" becomes one margin affordance.

*Predicate:* a headless-browser run (the same harness that verified Phase 1) hits the
§4 beats at ±2s from cold load with zero console errors; the fixed-seed replay hash
after 60 ticks matches the engine-only test; a first-time tester, unprompted, stakes a
pencil port within the first two minutes (this is the acceptance test for the Tell —
if they never touch pencil, the Tell did not land and the range display is wrong).

### 7.3 Haiku — runner sweep: **no unmarked mark**

*Owner: Haiku runners, mechanical, checklist-driven, one PR. Lands before or alongside
Sonnet PR 1; it is what PR 1 builds on.*

1. **Provenance on every cell and event.** `makeMarketCell` gains a required
   `provenance`; `engine.js:65-71` passes `{source:'procgen', trust:0.5,
   seed_label:'market:<port>'}`; `_tickPanamaEvent` books `provenance:
   {source:'procgen', trust:0.6, seed_label:'panama_check:<tick>'}` on start and end.
   `cellFor` throws on a `port`/`market`/`event` cell with no `provenance`.
2. **`game/test/provenance.test.js`.** Drive a 60-tick scripted game; walk
   `world.entities.latest` and `world.witness_log`; assert every `port`/`market`/
   `event` cell and every non-`tick`/`ledger`/`entity_update` booking carries
   `provenance.source ∈ {canon, scout, procgen, player}` and a numeric `trust` in
   [0,1]; assert `source:'canon'|'scout'` entries carry `source_url` and
   `source:'procgen'` entries carry `seed_label`. Then assert two engines from the
   same seed agree on `stateHash()` — the law must not cost replay.
3. **Register sweep.** Grep `game/`, `browser-deploy/game/`, `browser-deploy/
   tycoon-live.html` for player-facing strings that present a seeded fact as news
   (`engine.js:149` "Drought-driven congestion…"; the start-screen copy at
   `tycoon-live.html:169-172`) and reword each to the pencil register (`pencil
   weather · a drought-style slowdown, drawn from the 2023–24 precedent`). List each
   change in the PR body with the line number.
4. **Token lift.** Move `tycoon-live.html:10-20`'s `:root` colors to the §5.1 token
   set (day default, night under `prefers-color-scheme: dark` guarded by
   `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`),
   with `body { background: var(--paper) }`. No visual redesign in this sweep — the
   renderer PR does that; this makes the tokens exist.
5. **Telemetry hook (two lines).** In the browser UI, count and expose on `window`
   two numbers per session: pencil stakes placed and ink stakes placed. This is the
   first measurement of the Tell — the number §6.2's argument is waiting for.

*Predicate:* `node --test game/test` green including the new file; `replay.test.js`'s
pinned hash changed exactly once and the new value is in the PR description as a
declared cost; `grep -rn "Drought-driven" game browser-deploy` returns nothing.

---

## 8. Where this answer extends beyond what the map proves

- **The Tell as the ten-second feeling** is a design claim, not a measurement. The
  Sonnet predicate (an unprompted pencil stake in two minutes) and the Haiku telemetry
  hook are the first two instruments for it. If players never touch pencil, the range
  display — not the concept — is the first suspect.
- **"Reality withheld, not invented"** (the truth pool) is my doctrine; the doc's L1
  assumes the roster is the only source of landings. The pool is what makes the ring
  close offline on day one; it does not replace the roster, it seeds it.
- **Pencil-from-pool with decoys** is a this-week bound for L4, not the general
  generator Phase 3 designs (which needs a coastline and a footprint rule). It is
  chosen because it is provably never-illegal with the data on disk today.
- **The ring reading of §2** is mine. The doc draws a stack; the code exhibits the
  ring only once `fact_landed` exists.
- **Rivals as roster self-play trajectories** is STRETCH: it needs Phase 4's rollouts.
  Naming it now costs nothing and aims the engine.
- **The bug in §6.3 is on disk and cited**; its consequence for the renderer (no
  medium ⇒ cannot draw) is the design's, and it is the reason the law is a law rather
  than a lint rule.

*Ink is proven. Pencil is a guess. Stake a ship on the guess, and watch the world land.*

🚢 → ✏️ → 🖋️ → 🌊
