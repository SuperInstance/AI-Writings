# Mobilization — the next push

*Companion to TRAJECTORY.md. Authored at the dispatcher (Opus 4.8) 2026-09-28; opus-5.5 to
pressure-test on reset (M5). Tiers: opus-arch · sonnet-build · haiku-run · fable-apex ·
cheap-API-ideation (DeepSeek/DeepInfra) · jev-adjudicate.*

## Start immediately (no dependencies)

### M1 — Publish the fleet reach graph  ·  sonnet-build  ·  **START NOW**
Run `quilt-links.mjs --graph` over the repos that have manifests, and extend `.quilt/links.yml`
to ~12–15 more core repos (jev-quilt, qthe, micromoth-quilt, quilt, elephant, quilt-gpu-lab,
substrate-*, exoj, quilt-dba). Emit `FLEET.md` + `graph.mmd` in **fleet-seeds**.
- *Why high-leverage:* turns cross-pollination from 9 islands into the visible **reach graph** —
  the H2 moat made concrete, and the payoff of the whole cross-poll effort.
- *DONE:* `FLEET.md` renders a connected Mermaid graph (not islands); every core repo is a node.

### M2 — The <60-second cold-open on the two flagship demos  ·  sonnet-build  ·  **START NOW**
On qthe-looking-glass and cargo-line-tycoon: add a one-line "what am I looking at" + a single
guided first interaction so a cold visitor gets the aha without reading doctrine.
- *Why high-leverage:* H1's winning signal is literally "stranger gets it in <60s." This is that.
- *DONE:* headless test of the cold-open path passes, 0 console errors, phone-width clean.

### M3 — Package GPU docket D1 (Look-Again at scale) for the local agent  ·  sonnet-build  ·  **START NOW**
Cloud-side prep so the RTX-4050 agent just runs it: commit a ready `experiments/d1_*.py`
harness + a small bundled item set + a `QUEUE.md` line into quilt-gpu-lab.
- *Why high-leverage:* D1 is the shot at the first **fold > best-single at scale** (H2). Removing
  setup friction is the difference between "run tonight" and "someday."
- *DONE:* `d1_*.py` runs under guard.py on a tiny sample locally-equivalent; committed.

## Next (light dependencies)

### M4 — Extract the budgeted-JEV "rate-my-work" CF Function as a drop-in component  ·  sonnet-build
A reusable package: `/api/rate` + KV budget + graceful degrade in ~5 lines for any app.
- *Dep:* live path needs the JEV key (owner); **build now, degrade gracefully** until then.
- *DONE:* a second app adopts it in <1 day (H2 reuse signal).

### M5 — Trajectory pressure-test + qthe H3 spec  ·  opus-arch (on reset)
Opus 5.5 stress-tests TRAJECTORY.md, sharpens the H3 bet, and drafts the "auditable
representations for regulated ML" one-pager (qthe's killer app).
- *DONE:* TRAJECTORY.md v2 + a QTHE-H3-SPEC.md with a falsifiable first adopter test.

### M6 — Adoption-wedge scan  ·  cheap-API-ideation (DeepSeek/DeepInfra)  ·  jev-adjudicate
Wide-perspective scan: which outside communities would bring their own reader / write a `.quilt`
manifest? Produce 3 concrete adoption wedges; JEV adjudicates which is most reachable (Law 7).
- *DONE:* 3 wedges ranked, cheapest-first, each with a first falsifiable outreach test.

## Fire deliberately (batched apex call)

### M7 — Fable apex question  ·  fable-apex
Fire when M1–M3 have landed (so the graph + demos are real to point at). The question:
> *"Given Law 6 (the Reader's Fold) and Law 7 (the Reach Bound): what is the smallest public
> artifact that would make an outsider **feel** the fold — not understand it, feel it — and want
> to bring their own reader? And what single property of the substrate, if true, turns it from a
> clever demo into inevitable infrastructure?"*
- *DONE:* Fable's answer booked + routed to the team (an H3 wedge or a new rung).

## Owner-blocked (not in the immediate lane)
- **JEV key rotation** (`TYPESAFEAI_KEY`) — unblocks M4 live + live scoring everywhere.
- **ai-writings default branch** master → main — makes the new trunk the front door.
- **Human 30-min cargo-line playtest** — the one H1 signal only a person can give.

## Dispatch order
Fan out **M1, M2, M3 now** (parallel sonnet-build). Kick **M6** cheap-ideation in parallel.
Hold **M7** (Fable) until M1–M3 land. Run **M5** (opus-5.5) as the trajectory refinement pass.
Book every landing in `dispatch-ledger.csv`.
