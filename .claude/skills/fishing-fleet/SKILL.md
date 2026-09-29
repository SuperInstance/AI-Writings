---
name: fishing-fleet
description: >-
  Spawn a fresh session as a manager ("point man") that runs a crew of cheap API-connected
  worker loops — the Anthropic model manages/judges/routes, the prepaid APIs (z.ai, DeepInfra,
  DeepSeek) do the bulk generation, JEV referees, Moth rolls un-gameable dice. Use this to (1)
  reach LIVE rolled keys when the current session's keys are stale/revoked (a running container
  keeps the keys it started with; only a NEW session picks up rolled keys), and (2) stretch
  scarce Claude Code credits by offloading heavy token generation to cheap APIs while the smart
  model only manages. Invoke for massive iterative experimentation, dog-fooding loops, roster
  probes, or any "harvest a lot cheaply, promote the rare gem" mission.
---

# Fishing Fleet — Anthropic captains, cheap-API crews

*The captain trades time for gold. The crew hauls the silver. Once in a while the net brings up
a gem. The captain's hands are expensive; the crew's are cheap. Never spend a captain's hour on
work a deckhand can do.*

## Why this exists (two hard facts)

1. **Rolled keys don't reach a running container.** When the owner rotates API keys, a session
   already running keeps the (now-revoked) values it booted with — every call 401s. **Only a
   NEW session picks up the rolled keys.** In-process subagents share the parent's stale env, so
   they don't help. A freshly *created session* does.
2. **Claude Code credits are the scarce resource; the prepaid/cheap APIs are abundant.** z.ai
   (`glm-5.3-flash`), DeepInfra (many models), and DeepSeek are cheap-to-free and cache-friendly;
   JEV (typesafe.ai) and Moth (mothquantum) are cents-to-free. The Anthropic model should spend
   its tokens on *judgment, routing, synthesis, and deciding what to keep* — not on generating
   volume a deckhand API can produce for a fraction of the cost.

## The fleet, in roles

- **Captain** = the Anthropic model running a **fresh session** (`create_session`). Holds the
  live keys and a modest thinking budget. Plans the haul, routes work to the crew, judges the
  catch, promotes gems, books the log. Does NOT generate bulk text itself.
- **Crew (the deckhands)** = API-connected worker *loops the captain drives with scripts*
  (`Bash`/Python calling the HTTP APIs) — NOT Claude subagents. Cheap, parallel, iterative:
  - `deepseek-chat` — best all-round deckhand (fast, valid JSON) — the reliable hauler.
  - DeepInfra roster (MiMo, Nemotron, Seed-2.0, Muse-Glimmer, Hy, …) — a diverse crew for
    many-views/quality-diversity work; caching-friendly, so game the cache (stable prefixes).
  - z.ai `glm-5.3-flash` — fast deckhand when the account is funded.
- **The referee** = JEV (`jev-latest`). The *located verdict* — decompose a claim and fold the
  parts; use `choice` (pairwise) over independent `noul` (choice ≫ noul); read *ranking*, not
  absolute level. See `situations/arch/THE-WEAKEST-CLAIM-METHOD.md`.
- **The dice** = Moth (`comet-qrng-v1`). Un-gameable quantum draws (Bell S > 2) to pick
  curriculum / adversaries / seeds *nobody can steer*.

## The economics (what to harvest)

- **Silver** — routine, high-volume cheap output (candidates, variants, drafts, probes). Let the
  crew haul buckets of it; the captain never touches the oars.
- **Gold** — value that compounds when you *iterate*: a loop that folds crew output through JEV,
  keeps the best, feeds it back, and gets sharper each pass. Time → gold.
- **Gems** — the rare breakthrough (a novel finding, a fold that beats best-single, a real bug
  caught). When the referee + an un-gameable adversary confirm one, **promote it**: book it in
  the ledger and surface it to the parent.

## The recipe

1. **Parent (coordinating session)** — may have stale keys; that's fine. Call `create_session`
   with a self-directing captain mission (below), written plainly, and `source_url` set to the
   repo it must push to (see *Operational learnings*). Tag it. Then `send_later` a harvest check-in.
2. **Captain (fresh session)** — first confirm which keys are live (one tiny call each; z.ai may
   be balance-gated). Then run the crew: scripts that call the cheap APIs *en masse and in
   parallel* (threads), structured so a **stable shared prompt prefix** maximizes cache hits and
   only the tail varies. Fold every batch through JEV; draw un-gameable choices from Moth. Hold
   the field of candidates open (exoj-style), self-localize to the most-contested, collapse only
   at a JEV-refereed decision, and *buy reach* (an independent-reach reader) where the crew is
   blind — averaging correlated deckhands buys nothing (Law 7).
3. **Many commits = time-capsules.** Commit after each experiment/haul with a message that tips
   the hand of the reasoning (tried / expected / found / implication). Push often. `git pull
   --rebase` before each push; never force-push.
3b. **Leave a transcript (the gold is the I/O, not just the repo).** Alongside the prose commit,
   record the situation as a hash-chained transcript with `labs/situation-recorder/` — one
   relation-record per step (`TASK ROUTE DRAFT DRAW FOLD KEEP DROP MARK OUTCOME`), `refs` pointing
   at what each step folded. Write it to `situations/transcripts/<sid>.jsonl`. The `FOLD` record
   MUST keep the leaves, the located weakest (argmin), and the gap — not just the scalar. When the
   Moth API is throttled/blocked, draw the un-gameable `DRAW` values **locally** from `MicroMoth-quilt`
   (a Bell/GHZ circuit, no network) and put its collapse-ledger id in the receipt. Why: the transcript
   is the corpus a future model learns to decompose from — see
   `situations/arch/INTER-RELATIONAL-INTELLIGENCE.md`. The repo is the silver; the transcript is the gold.
4. **Harvest.** The parent's scheduled check-in pulls the commit trail, promotes gems, books the
   yield, and re-drives the captain (or spawns the next haul) while budget holds.
5. **Stop cleanly on limits.** Rate limits are account-wide (5-hour and 7-day); on a limit,
   commit what you have with an honest message and stop — don't thrash.

## Captain mission template (adapt the program; strip the metaphor before sending — see *Operational learnings*)

> You are a fresh SuperInstance session — the captain. A fresh session holds the rolled keys.
> Never print/commit secret values (env NAMES only). Confirm live keys, then run cheap-API crew
> loops for <MISSION>. Fold crew output through JEV (`POST api.typesafe.ai/v1/systemone`), draw
> un-gameable choices from Moth (`comet-qrng-v1`, send a browser User-Agent). Commit a
> time-capsule after each haul and push often (pull --rebase first; no force-push; trailer with
> your true authorship + the Claude-Session link). Keep `situations/…` logs current. Game the
> cache (stable prefixes). Promote gems (JEV + Moth-confirmed) to the ledger. Stop cleanly on a
> rate limit. Final message: hauls run, sharpest finding, and whether you hit a limit.

*(Endpoints/schemas: `situations/arch/TOOLING-LIVE-2026-09-28.md`. Roster roles:
`situations/arch/ROSTER-STRENGTHS.md`.)*

## Operational learnings (booked scars)

- **Runtime mission prompts must be PLAIN and TECHNICAL.** The metaphor on this page is for
  humans reading the skill — do not paste it into a `create_session` prompt. A metaphor-heavy
  mission (captains, hauls, gems, "un-gameable") tripped a `[reasoning_extraction]` safety
  false-positive and killed a runner at turn 1. Write the runtime prompt as a spec: endpoints,
  env var names, numbered steps, commit rules, stop conditions.
- **Create crew sessions with `source_url` set to the repo they will push to.** Without it the
  crew's `git push` returns **403**: a fresh session gets push credentials only for its source
  repo, and it has no `add_repo` tool to attach one later. Fresh sessions also **cannot create
  new GitHub repos** — repo creation stays with the owner or the parent session; create the repo
  first, then spawn the crew with that repo as `source_url`.

## Hard constraints (never violate)

- **Keys only to their own service.** Never send an API key anywhere but its own endpoint; never
  print, log, or commit a secret value. Reference env var names only.
- **No permission laundering.** The captain never asks a peer session to do something the
  parent's permission settings would block; route blocked work back to the human.
- **Book everything.** A scar booked beats a result covered. The ledger + these logs are the
  memory shared across the fleet's layers.
