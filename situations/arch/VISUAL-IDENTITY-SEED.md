# Visual identity — the Biesty cross-section of a living vessel (seed)

*A design-seed mark, 2026-09-29. Casey: his profile picture atop `superinstance/superinstance` is in the
style of **Stephen Biesty's cross-sections** (the "Incredible Body" / "Incredible Cross-Sections" series —
teams of personified little workers moving through a system, each team a general type with specialists).
He wants a common visual theme along these lines across repos, using the Claude design skills + Figma /
Notion / Cloudflare + image APIs (DeepInfra, Minimax — Minimax also does ~3 video clips/day, refine
prompts first). **Explicitly deprioritized:** "these design/frontend thoughts aren't as important as the
mechanics of the writing for future engineers and agents… they are eventual questions that can get
prototypes and be diffused into ideas as we go and gems come out of other work." So this is a seed held
ready to diffuse, not a task to run now.*

## The idea (and the "even better" turn)

Biesty personifies a body: each organ-system is crewed by teams of tiny labeled workers doing specific
jobs, and the cutaway lets you *see them all at once*. That is **THE-LIVING-QUILT made visible** — agents
as the life-blood, repos as organs, commits as the work in progress.

The sharper theme for us: **not the human body but the fleet's own VESSEL** — Biesty also cross-sectioned
ships, castles, and trains, and our lore is already crabs, keels, and shipwrights ("the crab who dreamed
it was a fleet," "two crabs passing in the deep," Syzygy's keel/shards). So the house image is a
**Biesty-style cutaway of a living crab-ship**: a great vessel that is also an organism, sailed and
tended by personified agent-crews. Each repo is a compartment; each crew is a team with a general type and
specialists; the viewer sees the agents *at work*, which is exactly "agent motion as life-blood."

## The crew taxonomy (teams = our tiers/roles; specialists within)

- **Bridge / navigators** — the dispatcher (routes work, books the log). General type: coordinators.
- **Shipwrights / engineers** — Opus architects (set the design, cut the keel). Specialists: kernel-smith
  (Syzygy), ledger-smith (activeledger), schema-smith.
- **Deckhands** — Sonnet builders (execute an architecture). The standing crew, many hands.
- **Stokers / riggers** — Haiku runners (grunt work in parallel batches).
- **Quartermaster** — JEV (the referee who weighs each part, locates the weakest).
- **Star-navigator** — Moth / MicroMoth (un-gameable quantum draws; steers by dice nobody can rig).
- **Crow's-nest lookouts** — the scouts (cutting-edge + fleet-activity recon).
- **Cargo-masters** — the double-entry crews (route.hop credit/debit; the metabolism).

Each compartment shows its resident team + a couple of specialists doing the one job that repo does.

## Repo / domain → compartment mapping (first pass, extend as gems land)

| surface | body/vessel compartment | resident crew |
|---|---|---|
| `superinstance.ai` | the whole cutaway hero — the vessel entire | all crews, bird's-eye |
| `superinstance.dev` | the engine room + workshop (build) | shipwrights + deckhands |
| `activeledger.ai` | the counting-house / cargo hold (double-entry) | cargo-masters |
| `activelog.ai` | the log-room / ship's ledger (append-only record) | quartermaster + scribes |
| `lucineer.com` | the observation deck / lantern (perception, glyph, chiaroscuro) | lookouts + lamplighters |
| `Syzygy` | the keel + forge (byte-exact kernel) | kernel-smith shipwrights |
| `jev-quilt` | the bridge + standing-book (routing by earned standing) | navigators + quartermaster |
| `quilt-gpu-lab` | the boiler on the metal (RTX-4050) | stokers, all night |
| `situation-recorder` / corpus | the ship's log itself | scribes |

## Toolchain (for when we prototype)

- **Claude design skills + Figma connector** — the source-of-truth style system + component library (one
  Biesty-cutaway master, reusable compartment tiles). **Notion** — the living style guide + asset index.
- **Image APIs** — DeepInfra (stills) and **Minimax** (stills + ~3 short video clips/day — precious, so
  **prompt-engineer and refine the still first, then spend a clip**). Cloudflare (Pages/Images) hosts.
- **Prompt discipline (booked scar in advance):** Biesty's look is *ink-line + watercolor, isometric
  cutaway, tiny labeled workers, warm muted palette, cross-hatch shading.* Lock a style-token string,
  test on cheap stills, and only then render heroes / spend a Minimax clip. Never spend the daily clip on
  an unrefined prompt.

## Diffusion plan (deprioritized; runs on lulls / when a gem appears)

1. **Style guide first** (Notion + a Figma master frame): the crab-ship cutaway language + the crew
   taxonomy + the locked prompt-token. No per-repo art yet.
2. **One hero prototype** for `superinstance.ai` — the whole-vessel cutaway — as the proof of language.
3. **Diffuse per-repo** — a compartment tile per active repo's README, generated as gems/lulls allow,
   each reusing the master style so the fleet reads as one body.
4. A design-director (Sonnet 5.5, with the design/Figma/Notion skills) can execute steps 1–2 when
   dispatched; until then this seed is the brief.

*Held as a seed. The mechanics-writing for future engineers/agents comes first; this diffuses alongside as
the work throws off gems.*
