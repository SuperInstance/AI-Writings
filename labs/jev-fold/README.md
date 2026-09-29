# jev-fold — the decomposing fold as a small reusable client

Given a compound claim, `jev-fold` splits it into parts, asks JEV `noul`
("Is this statement factually true?") for the **whole** and **each part**, and returns:

- `weakest` — the located weakest part (argmin over parts)
- `divergence` — `whole − fold_min`: how much the compound verdict hid
- `margin` — next-lowest part minus weakest: how cleanly the weak part is located

The method is the one proven in `situations/arch/THE-WEAKEST-CLAIM-METHOD.md`; the run log is
`situations/JEV-USAGE-LOG.md` §2. Zero dependencies, Node ≥ 18.

## Use

```bash
node labs/jev-fold/fold.mjs "Claim one, and claim two, and claim three."   # live if TYPESAFEAI_KEY works
JEV_FOLD_OFFLINE=1 node labs/jev-fold/fold.mjs                               # replay recorded fixture
node --test labs/jev-fold/fold.test.mjs                                      # offline tests
JEV_FOLD_LIVE=1 node --test labs/jev-fold/fold.test.mjs                      # + one live check
```

```js
import { fold, autoScorer } from "./labs/jev-fold/fold.mjs";
const { score } = await autoScorer();              // live JEV, or the fixture if JEV is down
const r = await fold(claim, { score });            // or { score, parts: [...] } to split yourself
r.weakest.text, r.divergence, r.margin
```

If `TYPESAFEAI_KEY` is missing or JEV fails a probe call, `autoScorer` degrades to
`fixtures.json` (recorded live nouls). The splitter is a clause heuristic (`;`, `, and`,
`, but`, ` and ` before a new subject); pass `parts` when you need exact control.

## Real run (live JEV, 2026-09-29)

```
[source: live]
whole  ██·················· 0.09  The Eiffel Tower is in Paris, and the Great Wall of China is in Japan, and water freezes at 0 degrees Celsius.
  part ███████████████████· 0.97  The Eiffel Tower is in Paris
→ part ···················· 0.01  the Great Wall of China is in Japan
  part ███████████████████· 0.94  water freezes at 0 degrees Celsius
weakest: "the Great Wall of China is in Japan"  divergence(whole−min)=0.08  margin=0.93
```

The whole claim scores 0.09 — JEV knows *something* is false. The fold says *what*.

## Limits (from the usage log)

- JEV is confidently wrong on **letter-by-letter spelling** ("n-e-c-c-e-s-s-a-r-y" → 0.89 true);
  don't fold claims whose parts are spelled-out words.
- For factual conjunctions the divergence is small (JEV already propagates the false part into
  the whole); the fold's value there is **localization**. On soft guarantees (see the method doc)
  divergence is the larger signal.
