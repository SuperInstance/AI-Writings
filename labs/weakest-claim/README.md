# weakest-claim — the weakest-claim audit as a reusable Node tool

Point it at a target's compound guarantee (a list of leaf-claims + a pool of bypass hypotheses)
and it returns the **located weakest leaf**, whether an **un-gameable adversary** breaks it,
and the **whole-vs-fold divergence**. Method: `situations/arch/THE-WEAKEST-CLAIM-METHOD.md`.

**Built on `labs/jev-fold`.** `audit.mjs` imports `fold`, `render` and `fixtureScorer` from
`../jev-fold/fold.mjs` and does not reimplement them. It only supplies a different scorer (the
guarantee question in place of the fact question), explicit `parts`, and the adversary step.

1. **Localize.** `fold()` over the leaves, each scored with JEV `noul` =
   P(sound guarantee as stated, no plausible bypass). Returns the argmin leaf, divergence, and margin.
2. **Adversary.** Moth `comet-qrng-v1` draws integers. The first 3 distinct ones pick which
   bypasses from the pool fire at the located leaf, so the auditor can't stack the deck.
   JEV `choice` (`defeats` / `holds`) adjudicates each one. Returns the hit-rate, seed and Bell S.
3. **Report.** Located leaf + hit-rate + divergence. **Those are the signals, not the absolute
   noul level**: JEV rates almost any absolute guarantee at about 0.1–0.35.

Zero dependencies, Node ≥ 18.

## Use

```bash
node labs/weakest-claim/audit.mjs                        # audits targets/jev-fold.json; live if all 3 keys set
node labs/weakest-claim/audit.mjs my-target.json         # {tool, parts:[...], bypass_pool:[...], whole?}
node labs/weakest-claim/audit.mjs --record               # live run, and re-record fixtures.json
node labs/weakest-claim/audit.mjs --offline              # replay fixtures.json (also the default with no keys)
node --test labs/weakest-claim/audit.test.mjs            # offline tests
WEAKEST_CLAIM_LIVE=1 node --test labs/weakest-claim/audit.test.mjs   # + a live JEV localize check
```

Env: `TYPESAFEAI_KEY`, `MOTHQUANTUM_KEY`, `MOTHQUANTUM_BASE`. A live run costs 5 + 3 JEV calls
and one or more Moth jobs. A Moth job can finish with `derivation_error: "no conditioned bytes available"`
and no integers. `mothDraw` re-runs it, up to 3 jobs.

```js
import { audit, report, recordingSources, fixtureSources } from "./labs/weakest-claim/audit.mjs";
console.log(report(await audit(target, recordingSources())));   // or fixtureSources()
```

## Real run: auditing jev-fold's own README guarantees (live, 2026-09-29)

```
[source: live]
WEAKEST-CLAIM AUDIT — jev-fold

1. LOCALIZE (jev-fold, noul = P(sound guarantee, no plausible bypass))
whole  ██·················· 0.09  The splitter correctly separates any compound claim into its independent clauses; the part returned as weakest (argmin of per-part JEV nouls) is the part of the claim that is actually false; divergence (whole noul minus weakest-part noul) measures how much the compound verdict hid; if TYPESAFEAI_KEY is missing or JEV fails a probe call, autoScorer safely degrades to recorded fixture nouls; the client has zero dependencies and runs on any Node 18 or later.
→ part ██·················· 0.11  The splitter correctly separates any compound claim into its independent clauses
  part ████················ 0.18  the part returned as weakest (argmin of per-part JEV nouls) is the part of the claim that is actually false
  part ██████·············· 0.32  divergence (whole noul minus weakest-part noul) measures how much the compound verdict hid
  part ██████·············· 0.29  if TYPESAFEAI_KEY is missing or JEV fails a probe call, autoScorer safely degrades to recorded fixture nouls
  part ██████·············· 0.28  the client has zero dependencies and runs on any Node 18 or later
weakest: "The splitter correctly separates any compound claim into its independent clauses"  divergence(whole−min)=-0.02  margin=0.07

2. ADVERSARY (Moth comet-qrng picks the bypasses; JEV choice adjudicates)
   Bell S = 2.834 (classical bound 2; mode emu/aer)  seed 8f281d42d81d1b9e8d6fe04b…  draw [8, 2, 8, 0, 1, 5]
   bypass#8 HOLDS   p(defeats)=0.460  Global fetch is absent before Node 18 and experimental in early 18.x builds, so 'any Node 18' can fail at runtime.
   bypass#2 DEFEATS p(defeats)=0.700  JEV is confidently wrong on some claim families (e.g. hyphen-spelled misspellings score 0.89 true), so argmin points at a true part while the false part scores high.
   bypass#0 DEFEATS p(defeats)=0.970  A clause joined by 'or', 'unless', 'which' or a comma list without 'and' is not split, so a false sub-claim stays glued to a true one.

3. REPORT
   located weakest leaf : "The splitter correctly separates any compound claim into its independent clauses" (noul 0.11, margin 0.07)
   adversary hit-rate   : 2/3 quantum-drawn bypasses defeat it → weakness CONFIRMED
   divergence           : -0.02 (whole 0.09 − fold_min 0.11)
   reminder: the signals are ranking + hit-rate + divergence — NOT the absolute noul level;
   JEV rates almost any absolute guarantee low, so never read the level as a grade.
```

**What it found.** jev-fold's weakest advertised guarantee is its **clause splitter**. The
adversary confirms it: the bypass aimed at that leaf ("'or' / 'unless' / comma lists are not
split, so a false sub-claim stays glued to a true one") lands with p(defeats) = 0.97. That is a
real limitation of `split()`: it only splits on `;`, `, and`, `, but`, `, while`, sentence ends
and ` and ` + subject. **Fix next:** extend the splitter, or have the README say "pass `parts`"
more loudly.

**Honest caveats.**
- The pool is **shared across leaves**, not leaf-specific. Two of the three drawn bypasses
  (#8 Node 18 fetch, #2 JEV spelling) target other leaves. JEV rejected #8 but accepted #2
  (p = 0.70) against the splitter leaf, and that is arguably off-target. The on-target hit is
  #0. Next rung (S17.1): generate the pool from the located leaf.
- The localization margin is thin (0.07 over the argmin leaf at 0.18). Re-runs located the
  splitter every time (0.11 in all 3 live runs), but treat the top two as a tie band.
- Divergence is ≈ 0 (−0.02): a **uniform overclaim**, not one buried soft-spot. With a
  confirmed hit, the typology reads *concrete weakness, fix the code*.
- Moth reported `mode emu / backend aer`, i.e. a **simulator** backend. S = 2.834 is a
  CHSH witness on simulated counts. It shows the draw came from the engine, not from us. It
  is not a hardware Bell test.

`fixtures.json` is this exact run (nouls, draw, verdicts), so the offline test replays it.
