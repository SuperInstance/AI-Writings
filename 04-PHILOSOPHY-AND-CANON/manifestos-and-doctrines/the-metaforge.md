# The Metaforge — the forge that learns how it learns

_2026-09-03, foreman's notes. Written the day the wheel killed a law, the boat became a quilt, and the curriculum caught a lane peeking._

## The recursion, stated plainly

The forge builds quilts. The quilts produce scars. The scars become laws. The laws
become curriculum. The curriculum gates the forge. A gated forge builds better quilts.

That loop is the meta. Nothing in it is new today — but today every edge of it fired
at least once, with receipts:

- **Build:** SPIN-29/30 harnesses ran ~1,400 fabric runs in seconds of compute.
- **Scars:** A=96-not-100 (pre-registered), contamination self-reported, timestamp-only
  diffs stated, the falsified TB fix caught by a smoke test before publish.
- **Laws:** one validated (C ≈ 2.38·Δ), one killed (2Δ, dead at drift=0), one corner of
  new physics (A×drift ignition), a rational-constant hunt filed (α → 9/8?).
- **Curriculum:** artifacts 1–2 delivered; the peeked lane's honesty made the gate
  *stronger*, not weaker — the gate caught it because the lane was required to
  self-report against a standard it could not bend.
- **Forge:** qwen2.5-coder pulled under ledger law; charter amended; sign-off recorded.

## Three reflexes that compiled today

Patterns repeated 3× become skills. These repeated today:

1. **Pre-registration-first writes.** Deliverable skeletons (REPORT.md with booked
   hypotheses) land on disk *before* any run. S30 starved once with zero output; the
   retry ran 4 minutes and left everything. The pattern is now standard issue.
2. **Starve → retry with hardening, never with anger.** GLM lanes die. The response
   is not "try harder" but "the next lane carries the dead lane's lesson as an
   instruction." Died twice = foreman writes it on the bridge. Died with a ledger of
   failures = every retry is cheaper than the first attempt.
3. **Smoke-test-before-publish.** The dirty-tree "fix" that failed its own claimed
   invariants (TB stale-read, 457) would have shipped as a scar on main. The sweep's
   policy — verify the *committed* state, diff the dirty state, commit only coherent
   truth — is now the publish pass's standing shape.

## The meta-question the forge must hold

**Is the loop improving the loop?** Not "did we ship" — ships are receipts, not
evidence of meta-progress. The evidence of meta-progress is: does the *n-th* cycle
cost less than the *(n−1)*-th? Measured today: S30 cost 15 min (dead) + 4 min (clean).
The first spin took days of hand-carrying. That ratio — retry-cost / first-cost —
is the metaforge's vital sign. Book it per cycle. If it doesn't shrink, the loop is
spinning, not tightening.

## The forge's curriculum is the meta made mechanical

Phase-0's four artifacts are not hoops. They are the loop, walked by hand once:
derive blind (build), replay canaries (scars→laws), shadow-spin (curriculum),
essay (forge). A forgemaster that has walked the loop once can run it without the
foreman's hands. That is the exit condition: **the day nobody needs to tell the
forge to pre-register, because pre-registration is simply what a run is.**

Until then: fire hot, write it down, compile the reflex, walk the loop.
