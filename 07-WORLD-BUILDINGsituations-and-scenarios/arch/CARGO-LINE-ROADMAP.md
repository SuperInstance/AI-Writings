# cargo-line-tycoon — the forward roadmap (the Chart is flowing; where the ring turns next)

*Dispatch: Opus 5.5 planning tier, blinders ON, 2026-09-27. **Not an apex wake** — this is
the dispatcher-routable roadmap that sequences the remaining rungs now that Fable's apex
pipeline is flowing (the Tell, STAKE/LAND, the Chart, the ring inversion, gift #1 landed as
schema, gift #2 in flight). It plans; it does not build code. Read against
[`../FABLE-CARGO-LINE-ANSWER.md`](../FABLE-CARGO-LINE-ANSWER.md) (the answer),
[`cargo-line-fact-landed.md`](./cargo-line-fact-landed.md) (the settled contract), and
[`CARGO-LINE-TYCOON.md`](./CARGO-LINE-TYCOON.md) §2 (the ring) / §5 (the phased plan) / §7
(honest limits). Everything grounded in the ledger is cited to a dispatch id; everything
that extends past the settled schema is marked **STRETCH**. Dispatcher books; this file is
not committed.*

🚢 → ✏️ → 🖋️ → 🌊

---

## 0. Where the pipeline stands (the vein, in one breath)

The ring is `L3 → L4 → L5 → L6 → L1 → L3`, closed through the player's stakes; **truth is
the loot, the moat is the surface, the landing is the fun** (Fable §6.2). On disk and in the
ledger:

| rung | dispatch | state |
|---|---|---|
| Phase 0 kernel (booked tick, seeded RNG, replay≡live) | d032 | **DONE** (browser-verified) |
| Phase 1 playable toy (10 real ports, routing, one event, navy/gold UI) | d032 | **DONE** |
| Phase 2 ground-truth + provenance (the refusal law, 6 chokepoints, real Hormuz crisis) | d036 | **DONE, reviewed, 5/5 + 13 substrate green** |
| Gift #1 — `fact_landed` schema + refusal law + pool + pencil-with-decoys | d038 | **DONE (settled contract)** |
| Gift #3 — no-unmarked-mark sweep | d040 | **FOLDED** into d036 + d039 |
| Gift #2 — **the Chart** (Pencil-Sea renderer + engine: pool.json, decoys, reveal schedule, previewStake, snap-to-true / reroute) | d039 | **IN FLIGHT** (`claude/the-chart`, base `phase2-ground-truth`) |

The kernel is deterministic and reviewed; the reality-fold is built and refuses unmarked
marks; the one event that closes the ring is a settled schema; the surface (the Chart) is
being drawn. The offline ring closes on day one through the truth-pool — **L1 is not a
launch dependency** ([`cargo-line-fact-landed.md`](./cargo-line-fact-landed.md) §2, §5).

---

## 1. The path from the Chart landing → a shippable, fun, good-looking cargo-line

### 1.1 What "shippable" is, honestly

A complete, fun, good-looking, offline-first, reality-anchored **single-player** toy on a
URL a human can open. Everything past that is upside, sequenced so each rung stands alone
(§7 scope discipline: the first phases are "a complete, shippable thing on their own").

**Shippable v1 is reached at the end of Rung A below — Chart + deploy + a *measured* Tell.**
Rungs B/C/D are the "demonstrably a class better" ladder that turns after v1 ships.

### 1.2 The smallest next rung after the Chart — **Rung A: Land the Tell**

*This is the answer to "the smallest next rung that makes the game demonstrably a class
better."* The Chart PR (d039) delivers the surface and the first two verdicts (`proven`,
`erased`) in the first run, plus the pencil-vs-ink **telemetry hook** (gift #3, folded in).
But the Chart cannot self-certify its own acceptance test: its predicate names *"a
first-time tester, unprompted, stakes a pencil port within the first two minutes"* (Fable
§7.2) — and a headless harness cannot be a first-time human. **Rung A points the instrument
at real humans and tunes the game to the reading.**

Why this is a class-up and not a polish pass: it converts the central design *conjecture*
(the Tell — that honest uncertainty reads as appetite) into a *measured, tuned fact*. That
is the corpus discipline exactly — design claim → instrument → measurement (Fable §8: "the
Tell as the ten-second feeling is a design claim, not a measurement"). It also settles
Fable §6.2.1's load-bearing argument — *the moat compounds iff it is the fun* — with data
instead of an argument. And it is the smallest such rung because the instrument already
exists; the rung is deploy + one tuning loop, not new architecture.

- **Contents:** (1) deploy the offline Pencil-Sea bundle to a URL (§3 below); (2) the O12
  real-device playtest — a handful of first-time humans on their own phones/laptops; (3)
  tune the three dials the Tell rides on — the **range display** (the spread = 1−trust, the
  first suspect if pencil goes untouched, Fable §8), the **decoy rate** (~25% risk premium,
  [`cargo-line-fact-landed.md`](./cargo-line-fact-landed.md) §5.3), and the **reveal
  schedule** (first landing ~tick 4, a pencil stake resolves within ~3 ticks, §5.2) — to
  the telemetry floor.
- **Predicate:** on real devices, cold-load to first pencil stake with **zero console
  errors**, and **≥ 60% of first-time testers stake a pencil port unprompted within 2
  minutes** (the Tell's acceptance floor, measured by the pencil-vs-ink hook). If below
  floor after one tuning pass, the range display is the first suspect (Fable §8); a second
  failed pass is the deadband trip-wire for a re-look (§2).
- **Tier:** BUILD (Sonnet-5) for the deploy + tuning; RUN (Haiku-4.5) to capture and tabulate
  each playtest session's hook numbers; DISPATCH reads the floor. **Autoresearch** is the
  natural harness for the tuning loop (one file = the range/decoy/reveal config, one metric =
  pencil-stake rate — §4).
- **Taste gate:** the d039 renderer's taste + microcopy pass runs **VectorLab** (§4) — the
  margin log and the range note *are* the Tell rendered as numbers, and Pencil-Sea's whole
  thesis is that taste carries the design (ink still vs pencil breathing, the never-drawn
  fold line).

### 1.3 The ladder after v1 (each recast on the ring)

**Rung B — the third verdict made fun: `revised` as visible arbitrage (Middle-tier
progression).** The Chart's first run shows `proven` + `erased`; the third verdict,
`revised` (a snapshot re-stamp, the delta between pencil estimate and inked number = *the
arbitrage*), is the first taste of the ring's real promise — **progression = reality, not
fiction** (Fable §6.2.2: "what you unlock is reality"). Middle tier = price seals landing.
- *Predicate:* a scripted game books a `revised` landing whose delta a player can stake
  toward and profit from; the `AS OF` re-stamp animation reads without a legend; the arbitrage
  is legible as "the operator who saw it coming."
- *Tier:* BUILD (Sonnet-5). Reuses the settled `snapshot`/`revised` path already in the schema
  ([`cargo-line-fact-landed.md`](./cargo-line-fact-landed.md) §1.2, §2).

**Rung C — Phase 4: the mid-state playtesting engine + Mode B (recast on the ring).** A
mid-state is *a chart at a truth horizon with a live stake*, the five-tuple `{seed,
book_prefix, truth_horizon, live_stakes, navigators_note}` (§4 of CARGO-LINE-TYCOON.md).
Recast per the ring: **the loot** Mode B hands you is a provably-winnable inheritance of
someone's open stakes; **the surface** is the derived blue-chinagraph "why" note on the
sheet (never a stored string); **the fun** is landing the inherited stakes. The engine is the
Situation loop over game states — generate, roster self-play wide-run, keep winners, know
why.
- *Predicate:* every seed handed to a player is winnable (its winning trajectory replays to a
  win), clears the JEV fun-floor, and carries a **derived** why (a function of the
  `book_prefix`, re-derives bit-for-bit on replay); a deliberately-unwinnable candidate is
  correctly rejected (§4 Stage 3).
- *Tier:* ESCALATE-lite → BUILD (Sonnet-5), **roster-backed** (roster DONE d024; cheap-tier
  self-play on DeepSeek/DeepInfra). **Autoresearch** is the self-play rollout harness (§4).
- **STRETCH inside C:** *rivals = roster self-play trajectories* (blue lanes = strategies
  actually played, Fable §7.1.5 / §4). Needs C's replayable rollouts to exist first. Naming it
  now aims the engine; until then rivals are ordinary marked procgen cells. **This is a build
  STRETCH, not an apex one** — Opus/Sonnet close it (see §2).

**Rung D — Phase 5: the scouting moat (recast: the visible extension).** Do **not** build a
hidden background learner. Build the *visible* extension of the pool: opt-in, off by default,
and when on, **scouting lands new ink onto the chart where the player sailed** — the moat is
the same surface the player already loves, extended (Fable §6.2.1; CARGO-LINE-TYCOON.md §2
L1, corrected). Advanced tier = governance cells landing (sanctions/inspection regimes as
ink) — the refinement d036 surfaced (a severe real fact changes *legality*, not just price).
- *Predicate:* an opt-in world measurably sharpens toward reality over sessions; every
  promotion is booked `fact_landed{landed_by:'scout', scout_ref}` with provenance through the
  JEV gate; a wrong scout books a revocable scar (R2) and is not trusted twice.
- *Tier:* BUILD (Sonnet-5) + roster/funding. **Degrades to DeepSeek/DeepInfra + typesafe.ai
  JEV today**; GLM/Kimi depth is an upgrade, not a dependency (§7 roster blocker, cited).

**Deferred, off the critical path — full Phase 3 (the general procgen generator).** The
Chart PR already ships the this-week L4 bound (pencil-from-pool-with-decoys, provably
never-illegal with data on disk). The *general* generator (coastline + a footprint rule,
CARGO-LINE-TYCOON.md §5 Phase 3) is real upside but **not a launch gate and not a Phase-4
prerequisite** — Mode B runs on the pool + the this-week bound. Route it in parallel when a
builder is free; never let it block v1 or Rung C.

### 1.4 The sequence, one line

`the Chart (d039) → **Rung A: Land the Tell (deploy + O12 + tune)** = SHIPPABLE v1 → Rung B
(revised/arbitrage) → Rung C (Phase 4 mid-state + Mode B) → Rung D (Phase 5 visible moat)`,
with full Phase 3 parallel and never blocking.

---

## 2. The second Fable call — when, and on what (the deadband)

**Verdict: no second apex question is live. The Fable-deadband holds. Opus/Sonnet close every
open item, including the two named STRETCHes.**

The first cargo-line apex call (d037) answered the one synthesis Opus could not self-clear —
the killer look-and-feel + unifying verb (the Tell, STAKE/LAND, Pencil Sea, the ring
inversion). What remains:

- Gift #1 (schema) — **closed by Opus** (d038, settled contract).
- Gifts #2/#3 (the Chart, the sweep) — **builds** (Sonnet/Haiku, d039/d040).
- The STRETCHes Fable named — *rivals = roster self-play* and *the "why" as a derived on-chart
  note* — are **build/architecture problems**, not apex-synthesis problems. They need Phase 4's
  rollouts to exist; the mechanism is fully specified ([`cargo-line-fact-landed.md`](./cargo-line-fact-landed.md)
  §1, CARGO-LINE-TYCOON.md §4). Opus 5.5 at ARCH closes the design; Sonnet builds it.

**The deadband condition (state it exactly): do not fire Fable again until BOTH hold —**
1. **Grounding:** Phase 4's replayable rollouts *and* a measured Tell (Rung A) both exist, so
   any new question is grounded in data, not design (the O11 bootstrap gate: apex calls earn
   their salt only on a widely-thought-out, evidenced substrate).
2. **Irreducibility:** a genuine *synthesis* emerges that Opus 5.5 at ESCALATE
   **demonstrably cannot self-clear** — not a build STRETCH, not a spec Opus can settle.

Until both hold, every rung routes at ARCH or below. **The one reserved candidate to watch**
(name it now, do not fire it): the **many-readers fold** — if the owner ever grows cargo-line
past single-player (a second player, a shared economy, a leaderboard that is more than a
number), the ring closes across *readers*, not one reader's stakes, and "the single unifying
feeling of many navigators on one chart" may be an irreducible apex synthesis. Single-player
never needs it; it is a fork the owner opens, not a debt the plan carries.

**The trip-wire (the honest fallback):** if Rung A's Tell measurement *fails* — humans do not
stake pencil — and the range-display fix (the first suspect, Fable §8) does not recover it
across two tuning passes, then "why is honest uncertainty not appetizing, and what is the real
ten-second feeling" becomes a grounded, irreducible re-look that clears the deadband. That is a
failure path, not a plan; the plan is that the Tell lands.

---

## 3. Deploy / who-plays-it (the smallest honest path to a URL)

cargo-line is offline-first web: static HTML/SVG/JS (`browser-deploy/` + `game/`), and by
design the ring **closes offline on day one** — `pool.json` ships in the client and the
seeded reveal schedule lands facts with no backend
([`cargo-line-fact-landed.md`](./cargo-line-fact-landed.md) §2, §5). So **v1 needs no server
at all.**

**One line:** `wrangler pages deploy` the offline static Pencil-Sea bundle to Cloudflare Pages
(the account already runs `canon-api-worker` on Cloudflare, d031/§1a) — no backend, because
the truth-pool closes the ring offline, and `pool.json` ships **only URL-citable public facts**
(the "omit any entry that cannot cite a URL" rule, §5.1; public-domain Natural Earth coastline
only if booked as canon) — so the O12 real-device playtest is just a link you send.

- **Rights/ToS honesty stays intact by construction:** the deployed bundle redistributes only
  facts that cite a `source_url` (real ports, public lat/lng) and public-domain coastline; **no
  live AIS / licensed freight feed** ships in v1 (§7: live feeds are a Phase-5+ moat, gated on
  rights review, never a launch requirement). The refusal law guarantees nothing unmarked is
  drawn, so nothing un-citable can leak into the bundle.
- **`canon-api-worker` stays dark for v1** — it is only wanted for the later opt-in moat
  (leaderboard/scouting, Rung D). Single-player never calls it.
- **Honest blocker note:** *automating* the deploy from a dispatch session is blocked on d014
  (needs `CLOUDFLARE_API_TOKEN` with Workers/Pages edit + `CLOUDFLARE_ACCOUNT_ID` in env). But
  the owner already deploys `canon-api-worker` by hand with their own creds — so the smallest
  honest path is **the owner runs one `wrangler pages deploy`**, or supplies the token to
  unblock d014 for a scripted deploy. Either way the deploy itself is trivial; only the
  session-automation is gated.

---

## 4. Absorbing the new engineering skills into the dispatch org

Blunt, per skill: adopt (and for which tier/task-class) or noise. The org already runs
spec→build→independent-confirm with a predicate per rung — so the test is whether a skill
*changes* that loop or just re-prices it.

| skill | verdict | where it fits |
|---|---|---|
| **ZSL** (PRD → vertical-slice issues → parallel TDD → one consolidated PR; triage/diagnose/code-review) | **ADOPT — genuine level-up #1** | DISPATCH + ARCH. This *is* the dispatch org's own loop (arch spec → build dispatches → Haiku confirm → merged rung) expressed as a skill; adopt its decomposition + consolidated-PR discipline as the standing routing method, and its **code-review** helper at BUILD/DISPATCH. |
| **VectorLab** (UI/UX taste + microcopy) | **ADOPT — genuine level-up #2** | BUILD, L6/UX task-class. Run it on the **d039 Chart renderer's taste + microcopy pass** and on Rung A's range-display tuning — the margin log and the range note *are* the Tell rendered as numbers, and taste carries Pencil-Sea. Standing capability for any surface dispatch. |
| **Superpowers** (TDD/debugging, "core skills library") | **ADOPT — floor-raise (already how we work)** | BUILD (Sonnet) + DISPATCH fix-forward. Formalizes the test-first-with-a-predicate reflex the org already keeps. Cheap, keep it — but make it the **single** TDD owner to avoid double-loading Pocock/ZSL's TDD (dedup below). |
| **Autoresearch** (autonomous one-file-one-metric loops, Karpathy pattern) | **ADOPT — conditional, earns its keep at Phase 4** | SESSION-tier autonomous loops. **Tie to the Phase-4 mid-state engine** (Rung C): Stage-2 roster self-play *is* a one-metric experiment loop (metric = fun-floor / winnability). Also the harness for **Rung A Tell-tuning** (one file = range/decoy/reveal config, one metric = pencil-stake rate). It is the honest home for the "erised autonomous dev" pattern the org already runs (d035). Not for hand-built rungs. |
| **Skills-for-Real-Engineers** (Matt Pocock: grilling, spec/ticket, TDD, code-review, domain modelling) | **ADOPT-PARTIAL — overlaps ZSL; take the non-dup helpers** | ARCH gets **"grilling"** (spec interrogation before build — the org does this by hand, e.g. d006's pressure-test) and **domain modelling**; let ZSL own decomposition and Superpowers own TDD. Do **not** run three TDD engines. |
| **code-map** (interactive codebase maps) | **NOISE for this project** | Skip on the cargo-line critical path — the game repo is young and small enough to hold in one head. Keep only as a **rare DISPATCH onboarding one-shot for the *large* repos** (jev-quilt at 246 tests, the 4-language substrate) when a fresh architect/builder enters them. Not a standing per-dispatch cost. |
| **Uniform** (a specific CMS/framework + MCP server) | **NOISE — pure token cost** | Zero surface area. cargo-line is offline-first vanilla HTML/SVG/JS with no CMS and no framework; the substrate is not web-CMS work. Do not load it for anything in this project. |

**The one-or-two that genuinely level us up:** **ZSL** (the dispatch loop as a skill —
decomposition + consolidated PR + code-review) and **VectorLab** (the Chart's taste, which is
the game's whole surface). **Adopt-and-keep-cheap:** Superpowers (TDD floor). **Adopt-when-
Phase-4-lands:** Autoresearch (self-play + Tell-tuning harness). **Just token cost:** **Uniform**
(no surface at all) and **code-map** (repo too small to earn it — reserve for big-repo
onboarding only). **Dedup rule:** exactly one TDD owner (Superpowers), one decomposition owner
(ZSL), one taste owner (VectorLab) — never load competing engines for the same job.

---

## 5. The roadmap at a glance (routable)

| rung | what lands | predicate | tier | skills |
|---|---|---|---|---|
| (in flight) the Chart | Pencil-Sea surface + `proven`/`erased` in the first run | d039 predicate: first-60s beats ±2s, 0 console errors, unprompted pencil stake < 2 min | BUILD (Sonnet) | VectorLab (taste pass) |
| **A. Land the Tell** *(= SHIPPABLE v1)* | deploy to URL + O12 human playtest + tune range/decoy/reveal | ≥60% of first-time testers stake pencil unprompted < 2 min on real devices, 0 console errors | BUILD + RUN | Autoresearch (tune loop), VectorLab (range display) |
| B. `revised` = arbitrage | snapshot re-stamp; the delta a player stakes toward | scripted `revised` landing profitable to stake toward; re-stamp reads without a legend | BUILD (Sonnet) | Superpowers (TDD) |
| C. Phase 4 mid-state + Mode B | vetted-fun, provably-winnable jump-in worlds + derived why | winnable path replays to a win + JEV fun-floor + derived why; unwinnable rejected | ESCALATE-lite → BUILD, roster | Autoresearch (self-play), ZSL |
| C-STRETCH | rivals = roster self-play (blue lanes) | every rival lane replays as a strategy actually played | BUILD (not apex) | Autoresearch |
| D. Phase 5 visible moat | opt-in scouting lands new ink where you sailed | world sharpens over sessions; every promotion booked w/ provenance + revocable scar | BUILD, roster/funding | ZSL |
| (parallel) full Phase 3 | general procgen generator (coastline + footprint) | fuzz over seeds finds zero illegal placements; same seed ⇒ same world | BUILD (Sonnet) | Superpowers |

**Do not fire Fable** until Phase 4 rollouts + a measured Tell both exist AND an irreducible
synthesis emerges (§2). One candidate reserved, not fired: the many-readers fold, only if the
owner grows the game past single-player.

---

*Ink is proven. Pencil is a guess. The Chart is drawing; the next thing to land is proof that
the guess is delicious — measured, on a real device, in a real hand.*

🚢 → ✏️ → 🖋️ → 🌊
