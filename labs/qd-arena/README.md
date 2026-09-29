# qd-arena — quality-diversity over a fleet of generator models

A zero-dependency **MAP-Elites** loop. Several live generator models propose candidates for an
open-ended prompt. JEV, the referee, scores each candidate's **quality** and places it on
**two diversity axes**. The archive keeps the **best candidate in each niche**, not one global best.
A Moth quantum draw picks the niche each generator aims at next, so neither the loop nor the models
decide where to explore.

The prompt: *name and give a one-line pitch for a small tool a fishing fleet of AI agents would want.*

**Built on `labs/weakest-claim`.** `qd.mjs` imports `jev()` and `mothDraw()` from
`../weakest-claim/audit.mjs`. It does not reimplement them.

## Why quality-diversity rather than a 2-player generator/critic

A generator/critic loop (GAN-shaped: propose → critic scores → keep the best → propose again) has
**one** objective. Every round pulls the generator toward whatever the critic liked last round.
That is mode-seeking: the loop sharpens a single peak and forgets the rest of the landscape.
For an open-ended prompt ("what would a fleet want?"), you want the **map** of good answers,
not one peak.

MAP-Elites changes what counts as winning. A candidate competes **only with the incumbent of its
own niche**. An abstract ritual with quality 1.0 is not thrown away because some concrete tool
scored 2.7. It is the best abstract ritual found so far, and it holds that cell until something
better *of the same kind* shows up. The output is an **illuminated grid**: for each kind of
answer, how good the best one we've found is (and whether we have found one at all).

The live run below shows the collapse directly. With no niche target, **all 18 generation-0
candidates from 6 different model families fell into one cell** (`middle/tool`). Model diversity
alone did not give idea diversity. A best-of or generator/critic loop that starts there would
keep sharpening `middle/tool`. The Moth-drawn niche targets then filled 7/9 cells in two
generations. The global best idea (HOLDMARK, 2.74) came out of that push, in `concrete/ritual`,
a niche no model visited on its own. Gen-0's best was 2.33.

## The pieces

| piece | what | who decides |
|---|---|---|
| generators | every model that answered the step-0 probe (below), in parallel, 3 candidates each per generation | the models |
| **quality** | JEV `score` over a 4-rung ladder (generic → vague → specific & useful → specific, useful & surprising). The expected rung is in [0, 3] | JEV |
| **axis 1 — grain** | JEV `choice`: `concrete` / `middle` / `abstract` | JEV |
| **axis 2 — form** | JEV `choice`: `tool` / `practice` / `ritual` | JEV |
| archive | 3×3 grid. Insert only if the cell is empty or the candidate beats that cell's incumbent | the rule |
| next niche | Moth `comet-qrng-v1` integers in 0..8, one per generator. Each generator is told its target niche and the elite it has to beat there | the draw |

The generator is told a target niche, but **JEV decides where the candidate actually lands**.
In the live run, 18 of 33 aimed candidates landed in their target. Misses still enter the
archive wherever JEV puts them: `CHUM_BUCKET` was aimed at `concrete/ritual` and took
`concrete/tool`.

## Step 0: which models were live (2026-09-29)

| model | endpoint | status |
|---|---|---|
| `deepseek-chat` | DeepSeek | ✅ live |
| `meta-llama/Meta-Llama-3.1-8B-Instruct` | DeepInfra | ✅ live |
| `XiaomiMiMo/MiMo-V2.6-Flash` | DeepInfra | ✅ live |
| `nvidia/NVIDIA-Nemotron-3.5-Lightning` | DeepInfra | ✅ live |
| `ByteDance/Seed-2.0-mini` | DeepInfra | ✅ live |
| `tencent/Hy3` | DeepInfra | ✅ live |
| `glm-5.3-flash` | z.ai | ❌ 429, code 1113 "insufficient balance". Recorded and skipped |

## The live run (recorded in `fixtures.json`; `--offline` replays it exactly)

```
ARCHIVE (MAP-Elites: best per niche; quality = JEV expected rung 0–3)

  concrete/tool     2.41  CHUM_BUCKET :: manager agent drops a `chum.json` of low-value scraps into the fleet channel so workers ritually swarm the nearest promising scent before the real catch.
                          ↳ tencent/Hy3 (gen 2, aimed concrete/ritual)
  concrete/practice  —    (empty)
  concrete/ritual   2.74  HOLDMARK :: `fleet tally` rolls .hold/*.jsonl (raw haul + referee grade) into day.md, then each agent appends a one-line eulogy to its lowest score — the morning rite where the crew reads the sunk catches aloud.
                          ↳ XiaomiMiMo/MiMo-V2.6-Flash (gen 2, aimed concrete/ritual)
  middle/tool       2.51  BYCATCH LEDGER :: Tags every harvested idea the referee rejected with the reason, turning the fleet's discard pile into a searchable map of what this niche won't bite on.
                          ↳ deepseek-chat (gen 2, aimed abstract/tool)
  middle/practice   2.06  Holdfast :: Agents stow the catch in one fixed order — tag, slot, timestamp — so the referee grades a single uniform pile rather than thirty scattered heaps.
                          ↳ XiaomiMiMo/MiMo-V2.6-Flash (gen 1, aimed middle/practice)
  middle/ritual     2.11  Grading Rite :: The referee agent performs a brief ceremonial reading of the catch aloud so the crew internalizes what counts as a good haul.
                          ↳ tencent/Hy3 (gen 1, aimed middle/ritual)
  abstract/tool     1.53  Echo Archive :: A resonant chamber where harvested code ideas are chanted back in unison, letting the crew feel the weight of quality before the referee's verdict.
                          ↳ nvidia/NVIDIA-Nemotron-3.5-Lightning (gen 2, aimed middle/ritual)
  abstract/practice  —    (empty)
  abstract/ritual   1.00  Fishing Fable :: The fleet sets aside a percentage of its catch to create and curate a shared repository of stories, myths, and legends that inspire and motivate the crew to push beyond the boundaries of code and ideas.
                          ↳ meta-llama/Meta-Llama-3.1-8B-Instruct (gen 2, aimed middle/ritual)

GENERATIONS
  gen 0: 18 cands → +1 new, 2 improved, 15 rejected → 1/9 niches  (unsteered: no target niche)
  gen 1: 15 cands → +3 new, 3 improved, 9 rejected → 4/9 niches  Moth draw [0,2,4,8,1,5] S=2.796 (emu)
  gen 2: 18 cands → +3 new, 3 improved, 12 rejected → 7/9 niches  Moth draw [6,5,2,5,3,2] S=2.803 (emu)

CONTRAST
  single best-of would return ONE idea: HOLDMARK (2.74, concrete/ritual, XiaomiMiMo/MiMo-V2.6-Flash)
  unsteered gen-0 placement: middle/tool×18
  QD archive: 7 distinct elites, mean quality 2.05
```

**Reading it.** Best-of would have handed back HOLDMARK and nothing else. It would have hidden
three things. BYCATCH LEDGER is a nearly-as-good (2.51) idea of a completely different kind.
The fleet's abstract column is weak: 1.00 and 1.53 are the best any model managed there, and
that is a finding in itself. And two cells (`concrete/practice`, `abstract/practice`) were never
reached at all.

## Honest caveats

- **Moth ran on its emulator backend** (`mode: emu`), as reported in the draw. Bell S ≈ 2.8 is
  above the classical bound of 2. The draw is still one the loop doesn't choose, but it is not
  certified hardware randomness.
- **Nemotron's gen-1 answer was unparseable.** It used `NAME || pitch` in place of `::`. It got
  zero candidates that round (15, not 18). The parser was left unchanged so the recorded run
  replays exactly.
- **The prompt says "tool"**, so `middle/tool` is the natural attractor. That is the point, not a
  flaw: an open-ended prompt always has an obvious attractor, and a single-objective loop feeds it.
- The two empty cells are under-explored, not proven empty. Moth sent one generator at
  `concrete/practice` (draw value 1), and all of its candidates landed elsewhere. It never drew
  `abstract/practice` (7). More generations, or a draw biased toward empty cells, would probe them.
  We kept the draw uniform on purpose.
- The absolute quality level is JEV's judgment on a 4-rung ladder. Compare rows against each
  other, not against an external scale.

## Use

```bash
node labs/qd-arena/qd.mjs                 # live if TYPESAFEAI_KEY + MOTHQUANTUM_KEY/BASE are set; else replays
node labs/qd-arena/qd.mjs --record        # live run, and re-record fixtures.json
node labs/qd-arena/qd.mjs --offline       # replay fixtures.json
node --test labs/qd-arena/qd.test.mjs     # offline tests
QD_ARENA_LIVE=1 node --test labs/qd-arena/qd.test.mjs   # + a live JEV placement check
```

Env (names only): `TYPESAFEAI_KEY`, `MOTHQUANTUM_KEY`, `MOTHQUANTUM_BASE`, `DEEPSEEK_KEY`,
`DEEPINFRA_KEY` (`ZAI_KEY` is in the roster but marked not live). A live run is about 51 JEV
calls, 18 generator calls, and 2 Moth jobs, and takes roughly 100 s.

```js
import { run, render, recordingSources, ROSTER } from "./labs/qd-arena/qd.mjs";
const r = await run({ generators: ROSTER.filter((e) => e.live), sources: recordingSources(), gens: 3 });
console.log(render(r));
```
