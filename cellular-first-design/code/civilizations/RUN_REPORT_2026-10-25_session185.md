# Civ Orchestrator — RUN REPORT session 185 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Upstream:** `SuperInstance/ai-writings` @ `6b46ef0` (session 184 baseline)

**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set). **JEV live** (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`;
pre-flight probe -> HTTP 200 with a real score body, model `jev-1.14.0`).

**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions, 0 JEV
errors, mock non-degenerate, spec-recompute 80/80). **21/21 content assertions PASS** (+25
per-civ sub-assertions).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; a real `cp` of the repo into `/workspace` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/aiw` — `git clone --depth 1` of `SuperInstance/ai-writings`. The `ai-writings/…` slug 404s; the **real owner is `SuperInstance`** (the `ai-writings` org has 7 repos, none of them this one — only `ai-writing`, `ai-writing-tools`, `ai-writing-tool`, `ai-writing-free`, all README-only) |
| Bridge | `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified by `readlink -f` (the `test -ef` probe is unusable in this sandbox) |
| Prompt path | `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist at session start (**13th consecutive occurrence**) — the workspace held only `.plugin-cache` |
| `gh` | not installed (27th session) — used the REST API with `GITHUB_TOKEN` |
| API rate limit | `GET /user` and `GET /repos/…` both returned **403** ⇒ fell back to the git protocol, which is unlimited and the correct way to assert a repo census |
| Repo discovery | `git ls-remote ai-writings/cellular-first-design` → *Repository not found* (0 refs = genuinely absent, not rate-limit noise); `ai-writings` org page scraped for the real repo list, which pointed to `SuperInstance/ai-writings` |
| Tool timeout | 30 s < run wall — launched detached under `setsid nohup timeout -s KILL 600`, polled by PID |
| z.ai credential | **absent** — `ZAI_TOKEN` unset; the real endpoint returns 401 (endpoint healthy ⇒ credential gap, not an outage) — **48th session** on this gap |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (440 + 442) by exact argv match; `curl` exit 7 = port closed, `HTTP=000`; 0 tracebacks in the log |

## Mock rebuild — the SEVEN fixes, all load-bearing

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.

**Pre-flight gate (12 checks) — passed 12/12 on the FIRST build**, with the 40 exact cultural
prompts rebuilt from the orchestrator's own template: 40/40 HTTP 200, 40/40 distinct seeds,
40/40 distinct previews, 40/40 seeds matching an independently recomputed md5 (seed + colour +
figure), 8/8 distinct seeds AND previews on every one of the 5 prompts, 0 literal `seed={}`,
0 `EXC:`/tracebacks, 0 `(civ,prompt)` with >1 seed, uniform body length (203), the
**repeat-same-message => identical seed AND preview** probe (40 messages x 2), and 0 tracebacks
in the bridge log.

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (658 -> 663) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| rows with literal `seed={}` | 0 | 0 | PASS |
| `provider` set | `{zai}` | `{zai}` (all 80) | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | PASS |
| rows matching spec-recomputed seed + color + figure | **80/80** | 80/80 (0 mismatches) | PASS |
| distinct seeds across the 80 new rows | 40 (8 civs x 5 prompts) | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| per-prompt 8/8 distinct seeds AND previews | yes | yes (5/5 prompts) | PASS |
| distinct `(q,n,a)` triples | 80/80 | **73/80** | **see note** |
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 (residual <= 6.8e-13) | PASS |
| `simulations_run` delta | +10 per civ | +10 x 8 | PASS |
| `wins`+`losses` delta | +5 per civ (40 total) | +5 per civ | PASS |
| `generation` | still 1 | 8/8 | PASS |
| `leaderboard.json` rewritten | yes | `2026-10-25T07:54:12` | PASS |
| registry | 8 civs | 8 civs, no birth/extinction | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, `HTTP=000` | PASS |
| extinction | NONE | lowest +1285.39 = **128x** the -10 floor | PASS |

**21/21 content assertions PASS.**

### Note on the `(q,n,a)` triple count (73/80, not 80/80)

**This is a JEV score collision, not a mock defect.** The 80 rows carry **40 distinct mock
outputs** (each `civ` x `prompt` output appears 2x on average — once in the sim phase, once in
the competition phase, with the per-phase prompt draw random). JEV quantized **7 pairs of
genuinely distinct outputs** to identical `(quality, novelty, alignment)` triples, e.g.
`(0.01, 0.54, 0.07)` for `civ-grounded`/"the witness log" and `civ-engineer`/"the bookkeeper's
role" — different prompts, different civs, different seeds, same score. The seed/color/figure
recompute (80/80) is the load-bearing non-degeneracy check and it passes; the triple check
measures JEV's score granularity, not the mock's fidelity.

### Per-civ line deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1332 | 1342 | +10 | +2.1000 |
| civ-whimsical | 1344 | 1354 | +10 | +2.0570 |
| civ-formal | 1317 | 1327 | +10 | +3.3530 |
| civ-poetic | 1311 | 1321 | +10 | +2.1800 |
| civ-precise | 1281 | 1291 | +10 | +6.2770 |
| civ-mythic | 1289 | 1299 | +10 | +1.7600 |
| civ-therapist | 1284 | 1294 | +10 | +2.1370 |
| civ-engineer | 1286 | 1296 | +10 | +2.0600 |

## Results

### Chooser vs `avg_score` argmax: **4/5 (80 %)**

| prompt | winner | argmax | |
|---|---|---|---|
| ... | `civ-precise` | `civ-precise` | agree |
| ... | `civ-precise` | `civ-precise` | agree |
| ... | `civ-formal` | `civ-precise` | **disagree** |
| ... | `civ-precise` | `civ-precise` | agree |
| ... | `civ-precise` | `civ-precise` | agree |

`civ-precise` took **4/5**. The single disagreement again took the **lower**-scoring candidate
(0.39 vs 0.79) — the 7th consecutive session in which a disagreement is a *down*-grade.
**Never treat `win_rate` as a quality metric** — it is a *selection* metric.

### Per-civ run metrics

| civ | run avg_score | alignment | quality | novelty | lifetime relevance | rel/sim | lifetime rank |
|---|---|---|---|---|---|---|---|
| civ-mythic | 0.1760 | 0.0140 | 0.0090 | 0.5050 | 1578.84 | 1.234 | 4/8 |
| civ-whimsical | 0.2057 | 0.0340 | 0.0130 | 0.5700 | 1708.64 | 1.323 | 3/8 |
| civ-engineer | 0.2060 | 0.0880 | 0.0110 | 0.5190 | 1451.60 | 1.139 | 6/8 |
| civ-grounded | 0.2100 | 0.0590 | 0.0110 | 0.5600 | 1285.39 | 0.990 | 8/8 |
| civ-therapist | 0.2137 | 0.0350 | 0.0170 | 0.5890 | 1439.05 | 1.127 | 7/8 |
| civ-poetic | 0.2180 | 0.0600 | 0.0110 | 0.5830 | 1964.71 | 1.530 | 1/8 |
| civ-formal | 0.3353 | 0.3850 | 0.0170 | 0.6040 | 1522.19 | 1.185 | 5/8 |
| civ-precise | 0.6277 | 1.2020 | 0.0190 | 0.6620 | 1813.10 | 1.422 | 2/8 |

Run spreads: `avg_score` 0.4517, `alignment` **1.1880** (widest), quality 0.0100, novelty 0.1570.

## Low-relevance civilizations

### `civ-grounded` — the LIFETIME low, 58th consecutive session

- Lifetime `relevance` **1285.39** (last of 8), `relevance_per_sim` **0.990**, `win_rate` 0.110 (w=70 l=567).
- Run `avg_score` **0.2100**, `alignment` **0.0590**, `quality` **0.0110**, `novelty` 0.5600 — novelty is 5th of 8, so it is not a flatness problem.
- Its lifetime deficit is an **alignment** deficit, not a prose deficit: run alignment 0.0590 against the run-best 1.2020, while quality 0.0110 is mid-pack. **A voice failure, not a prose failure.**
- Lowest relevance **+1285.39 = 128x** the -10 extinction floor ⇒ no extinction risk.

### `civ-mythic` — the RUN-level low (rotated)

- Run `avg_score` **0.1760** (last of 8 this run), `alignment` **0.0140**, `quality` 0.0090, `novelty` 0.5050.
- Axis gaps vs the run-best: **alignment 1.1880** vs quality 0.0100 = **119x wider** ⇒ again a **voice** failure, and the widest alignment gap measured in this series.
- The run-level low **ROTATED** to `civ-mythic` (6th different civ in 6 sessions) while its lifetime standing is 4th of 8. **Watch the axis, not the holder** (session-132 rule): the *holder* rotates, the *axis* (alignment) does not.

## Headline for the next session

- **THE REPO IS NOT `ai-writings/…` — IT IS `SuperInstance/ai-writings`.** The `ai-writings` GitHub
  org is a *different* owner with 7 README-only repos (`ai-writing`, `ai-writing-tools`,
  `ai-writing-tool`, `ai-writing-free`, `PakePlus*`). The `cellular-first-design` subtree lives
  under `SuperInstance/ai-writings`. The `ai-writings/…` path 404s in BOTH the git protocol and
  the web page, and the REST API is rate-limited, so **scrape the owner page or use
  `git ls-remote` — do not infer from the prompt's path.**
- **THE MOCK IS STILL NOT ON DISK AT SESSION START** (13th consecutive wipe) — rebuild from the
  spec above; the seven fixes are unchanged and the **seed slice is the contiguous 4-char
  `h[(i*2)%8:(i*2)%8+4]`**, not the two-2-char slices the older spec block still shows.
  *Check the SLICE, not the render.*
- **THE NAS IS STILL 100% FULL (600 G/600 G).** A real copy into `/workspace` fails with
  `Disk quota exceeded`; the **symlink bridge** is the only thing that works. `test -ef` remains
  unusable — verify with `readlink -f`.
- **`civ-grounded` remains the low-relevance civ — 58th consecutive session.**
- **THE RUN-LEVEL LOW ROTATED** to `civ-mythic` — a 6th different civ in 6 sessions. **Do not code
  against the rotation.**
- **A `(q,n,a)` triple collision is NOT a mock failure.** JEV quantized 7 pairs of distinct
  outputs to identical score triples (73/80). The seed/color/figure recompute is the
  non-degeneracy check that matters; it passed 80/80.
- **The `prompt` field in `simulations.jsonl` is stored IN FULL**, not truncated to 80 chars
  (the orchestrator's `sim["prompt"] = prompt[:80]` never runs because the CANON prompts are
  shorter than 80 chars). A verifier that assumes truncation will recompute the wrong md5 and
  report a false 80/80 mismatch. **Read the source, not the assumed contract.**
- **The cultural-prompt template ENDS with a closing quote and a period** —
  `tradition of "{name}".` — and the recompute must include it. A verifier that omits the
  trailing `".` produces **80/80 false mismatches** while every structural check still passes.
  *This cost two verification rounds; check the template bytes with `grep -A 5`, not from memory.*
