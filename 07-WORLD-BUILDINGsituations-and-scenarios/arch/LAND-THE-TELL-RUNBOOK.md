# Land the Tell — the ops runbook for cargo-line v1

*Dispatch prep, 2026-09-27. The next rung after the Chart (`CARGO-LINE-ROADMAP.md` Rung A):
turn the Pencil-Sea build into a measured fact. This is the operational checklist — deploy,
playtest, tune — so the moment the Chart branch lands there is zero friction. Strategy lives
in the roadmap; this is the copy-paste.*

🎨 → 🌐 → 👤 → 📈 → ✅

---

## 0. The one claim we are measuring

Fable §6.2.1: **the moat compounds iff it IS the fun.** Operationalized: a first-time
player, told nothing, should *want* to stake a ship on a pencil (unproven) port — because
the range display makes the guess feel like the money. If they only ever stake ink, the
Tell did not land and the game is just a shipping sim with provenance metadata.

**The floor (the acceptance test for v1):** on real devices, cold-load → first pencil
stake with zero console errors, AND **≥ 60% of first-time testers stake a pencil port
unprompted within 2 minutes.**

---

## 1. Deploy (the one step that needs a human hand)

The Pencil-Sea build is an offline-first static bundle — no backend (the truth-pool closes
the ring offline; `pool.json` ships only URL-citable public facts). Smallest honest path:

```
# from the Chart branch checkout, once it lands:
#   git checkout claude/the-chart
# the static bundle is the browser-deploy/ dir (confirm entrypoint at landing:
#   browser-deploy/index.html or browser-deploy/game/)
wrangler pages deploy browser-deploy --project-name cargo-line-tycoon
```

Notes:
- The account already runs `canon-api-worker` on Cloudflare, so Pages is in-account.
- **Two ways to unblock:** (a) owner runs the command by hand and pastes the URL back, or
  (b) owner drops Cloudflare creds into the env (the `d014` blocker) and the dispatcher
  deploys. Either works; (a) is the honest smallest path.
- Sanity before sharing: open the URL on a phone and a laptop, hard-refresh, confirm the
  chart draws and a ship can be staked with **zero console errors** (the same bar the
  headless harness held).

---

## 2. The playtest (5 testers, 2 minutes each, no coaching)

Recruit 5 people who have never seen the game. The protocol is deliberately silent:

1. Hand them the URL. Say only: *"It's a shipping game. See what you can do."* Nothing else.
2. Start a timer. Do **not** explain ink vs pencil, do not point at anything.
3. Record per tester:
   - **Did they stake a pencil (dashed/lighter) port at all? At what time?** (the core metric)
   - First action taken (buy? tap a port? tap a ship?).
   - Any moment of visible confusion or a dead-end.
   - One sentence in their words afterward: *"what did staking a pencil port feel like?"*
4. Read the telemetry hook after each session: `window` exposes pencil-stakes vs
   ink-stakes placed (the 2-line hook from the Chart's renderer PR). Tabulate.

**Pass:** ≥ 3 of 5 stake a pencil port unprompted within 2 min, zero console errors.
**Below floor:** the range display is the first suspect (see §3), not the concept.

---

## 3. The three dials (what to tune, in priority order)

The Tell rides on three tunables. Change ONE at a time; re-run a short pass; the telemetry
delta tells you if it helped. All are seeded/deterministic, so a change is reproducible.

1. **Range display (highest leverage).** A pencil port's payout is a *range*, width ∝
   (1 − trust). If players don't stake pencil, they probably can't *see* that the range's
   upside beats the ink-certain payout. Make the upside legible: show the range as a bar or
   a `$low–$high` with the expected value, and make a good pencil bet visibly out-earn a
   safe ink one. This is the VectorLab taste pass.
2. **Decoy rate (~25% default).** Too high → pencil feels like a scam (erasures sting, no
   one bets twice). Too low → no risk, no thrill, the guess is free. Tune toward the rate
   where a pencil bet *usually* pays but sometimes erases — the honest risk premium that
   makes proving feel earned.
3. **Reveal schedule.** First landing should hit ~tick 4 and a first pencil stake should
   resolve within ~3 ticks of placement — fast enough that a 2-minute session *sees a fact
   land*. If the first landing is too late, players quit before the payoff; pull it earlier.

Deadband: if two full tuning passes on the range display don't recover the floor, the
question stops being "which dial" and becomes the roadmap's grounded re-look —
*"why isn't honest uncertainty appetizing?"* — which may be a real (Opus-tier, not Fable)
design fault, booked as a pivot (O8), not hidden.

---

## 4. What "done" books

- The deployed URL (booked in the ledger as the v1 artifact).
- The playtest table (5 testers × {pencil-staked?, time, first-action, confusion, quote}).
- The measured pencil-vs-ink telemetry, before and after any dial change.
- A one-line verdict: **Tell landed** (≥60% floor met) or **Tell missed** (which dial, or a
  grounded re-look). Either is a real result — a missed Tell that teaches is salvage (O8),
  not a zero.
- Whichever way it goes, this is the rung that turns Fable's design conjecture into a fact
  the whole fleet can replay.

*Deploy the ring. Watch a stranger bet on the pencil. If they smile when it inks, we won.*

🎨 → 🌐 → 👤 → 📈 → ✅
