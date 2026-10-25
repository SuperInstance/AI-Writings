# Civ Orchestrator — Run Report, session 181 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 60th session) + **live JEV**.
Baseline: `9b43a10` (session 180). **All 55 verification assertions PASS.**

## Headline for the next session

- **THE MOCK NEEDS SEVEN FIXES, NOT SIX — fix (g) IS STILL MISSING FROM THE
  "six fixes" LIST IN THE RUNBOOK.** The RUNBOOK's headline says "THE MOCK NEEDS
  THE SAME SIX FIXES", but session 174 already documented a **seventh**
  failure mode: the spec's `figure = h[12:16] / h[16:20] / h[20:24]` is
  **pseudo-code, not Python** — read literally it divides two `str` values and
  raises `TypeError: unsupported operand type(s) for /: 'str' and 'str'`.
  The mock then 500s on **every** request **while the socket stays open**, so a
  port/200 liveness probe still looks healthy. This session the mock was built
  from the RUNBOOK's "six fixes" list and **failed its first live probe with
  HTTP 500**; the fix is `figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`.
  **The RUNBOOK's "six fixes" table needs a (g) row.**
- **THE PRE-FLIGHT GATE NOW HAS TEN CHECKS, NOT EIGHT.** The two additions are
  the **repeat-same-message ⇒ same seed** probe (40 messages × 2 repeats, the
  only check that can catch fix (f)) and the **0 `(civ,prompt)` pairs carrying
  >1 seed** check. This session: **10/10 PASS on the FIRST build**, no rebuild
  drift, body lengths **167–209** chars (matches the documented range).
- **THE SEED SLICE IS 4 HEX CHARS (`h[(i*2)%8:(i*2)%8+4]`), NOT THE 2-CHAR SLICE
  STILL SHOWN IN THE SPEC BLOCK.** The spec block in the RUNBOOK still reads
  `seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]` (padding to a
  documented width is not that width's worth of entropy). Widening the slice
  to 4 chars gave **40/40 distinct seeds** and **0** `(civ,prompt)` with >1
  seed. *Check the SLICE, not the render.*
- **`civ-grounded` remains the low-relevance civ — 55th consecutive session.**
  Last of 8 on lifetime `relevance` **1235.89**, `relevance_per_sim` **0.982**,
  `avg_score` **1.0140**, `alignment` **1.0683**, `quality` **0.4006**. The
  binding constraint is still **alignment**: gap to the next civ **0.1347** vs
  quality's gap **0.0419** = **3.22×** wider. Alignment is the dimension the
  meta-GAN selects on, so this is a **voice** failure, not a prose failure.
  Lifetime novelty **1.5731** is 3rd of 8 — Grounded is neither boring nor
  unmistakable; it is simply not rewarded.
- **The run-level low ROTATED to `civ-engineer`** (run `avg_score` **0.6353**,
  `quality` **0.0920**, `alignment` **0.5280**) — a **fifth** civ in five
  sessions, while its lifetime standing is 3rd of 8 on `relevance`. This is a
  **watch axis, not the finding** (session-132 rule). The *holder* rotates; the
  *axis* (alignment) does not.
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-precise` took **3** of
  the 5 competitions; `civ-formal` and `civ-engineer` took 1 each; the other
  five civs went 0-5. The chooser is **not** a pure argmax. **All four
  disagreements took the LOWER-scoring candidate** (max |delta| **−0.3800**,
  `civ-engineer` won at 0.63 while `civ-precise` scored 1.01).
  **Never treat `win_rate` as a quality metric** — it is a *selection* metric.
- Counter gap **−609.9199**, fixed — byte-identical to session 180's value
  (per-civ delta **0.000000** for 6 of 8, ±0.0001 float rounding for the
  other two). Not accumulating.
- Run spreads: `avg_score` 0.3797, `alignment` **0.9870** (widest), quality
  0.1930, novelty 0.5680.
- Verification: per-civ Δ **+10 × 8** = **80** new rows, `meta_log` **+5**
  (638 → 643), `Winner:` **5**, wins **+5** / losses **+35**, 0 JEV errors, 0
  fallback triples, `zai × 80`, **40/40** distinct seeds, **0** `(civ,prompt)`
  with >1 seed, **80/80** rows match an independently recomputed message md5
  (seed + colour + figure), **8/8** seeds AND previews on all 5 prompts,
  **[mock-zai** prefix on **80/80**, registry 8 all gen 1, extinction **NONE**
  (lowest +1235.89 = **124×** the floor). **55/55 PASS.**

## Environment recovery (session 181)

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not
  exist (**12th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; `cellular-first-design` is a
  **subdirectory** of that repo, not a repo of its own. The `ai-writings/…`
  slug 404s (the GitHub API is case-insensitive).
- Cloned to **`/tmp/cfd`** (overlay fs, 28 G free) with `--depth 1`.
  Cloning into `/workspace` fails with **`Disk quota exceeded`** (NAS EDQUOT,
  **18th session**) — `/workspace` reports **600 G / 600 G, 100 %** while
  visibly empty.
- Bridge symlink `/workspace/repos/ai-writings/cellular-first-design` →
  `/tmp/cfd/cellular-first-design` (clone root, **not** the nested
  `cellular-first-design` dir). Verified with `os.path.samefile()` →
  **dev:ino 129:10425** both sides. The shell `[ -ef ]` test mis-parses in
  this sandbox — use Python `os.stat`.
- `ZAI_TOKEN` absent from env and all secrets; z.ai **401** `token expired or
  incorrect` ⇒ endpoint healthy, credential absent (**60th session**).
- **JEV live**: well-formed body → **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder
  **and** `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token
  gate above it must also be satisfied).
- `gh` not installed (**20th session**) — used `GET /user/repos` with
  `GITHUB_TOKEN`; `ai-writings` is not in the first 10 pages of owned repos, so
  the **search API** was needed to find `SuperInstance/AI-Writings`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout
  redirected, `< /dev/null`.

## Mock rebuild checklist — SEVEN fixes

| # | Fix | Session | Symptom if missing | Applied |
|---|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` index wrap | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** | yes |
| b | `md5(whole_message)` (not the first 8 alnum chars) | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text | yes |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server | yes |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 | yes |
| e | seed widened 2 → 4 hex chars (`h[(i*2)%8:(i*2)%8+4]`) | 169 | 2-char slice collides ⇒ 39 distinct seeds, one prompt at 7/8 | yes |
| f | index derived from the MESSAGE (`d[0] % 4`), not a request counter | 170 | 64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed | yes |
| **g** | **figure = three string components, not a division** | **174** | **`TypeError` on every request ⇒ HTTP 500 while the socket stays open; a port/200 probe still looks healthy** | **yes** |

### The mock algorithm — fully specified (seed slice WIDENED to 4)

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # 4 hex chars — WIDENED, not padded
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"  # three components, NOT a division
```

`cultural_prompt` is exactly what `civilization_orchestrator.py` builds:

```
You are a voice in the tradition of "{name}".
Your tenets: {tenets joined by ", "}.
Your voice: {voice_emphasis}.

{prompt}
```

**Pre-flight gate (must pass before the batch) — TEN checks:** 40 requests using the
**exact long cultural prompts** ⇒ **40/40 distinct seeds**, **40/40 distinct previews**,
**40/40 independently recomputed md5s** (seed, colour and figure), **8/8 distinct seeds AND
8/8 distinct previews on every one of the 5 prompts**, 0 literal `seed={}`, 0 `EXC:`/
tracebacks, **[mock-zai** prefix on 40/40, **repeat-same-message ⇒ same seed (40 × 2)**,
and **0 `(civ,prompt)` pairs carrying >1 seed**.

**Teardown:** kill by exact argv match — `python3 /tmp/mock_zai.py` and
`timeout -s KILL 900 python3 /tmp/mock_zai.py` (**two** pids). Never `pkill -f mock_zai`
(self-matches the killing shell). Then prove the port is closed: `curl -m 5` ⇒ **exit 7**,
`HTTP=000`.

## Verification — asserted on rows, not on exit code

| # | Check | Expected | Observed |
|---|---|---|---|
| 1 | per-civ `simulations.jsonl` Δ | +10 × 8 = 80 | +10 × 8 = **80** |
| 2 | `meta_log.jsonl` Δ | +5 | 638 → **643** |
| 3 | `Winner:` lines in run output | 5 | **5** |
| 4 | wins Δ / losses Δ | +5 / +35 | **+5 / +35** |
| 5 | per-civ win+loss sum | 5 each | **5 each** (precise 3+2, formal 1+4, engineer 1+4, others 0+5) |
| 6 | `relevance` Δ == Σ`avg_score` | 8/8 exact | **8/8 exact** |
| 7 | JEV errors | 0 | **0** |
| 8 | JEV fallback triples (2/2/2, conf 0.0) | 0 | **0** |
| 9 | provider | zai × 80 | **zai × 80** |
| 10 | distinct seeds | 40/40 | **40/40** |
| 11 | `(civ,prompt)` with >1 seed | 0 | **0** |
| 12 | rows matching recomputed md5 (seed+colour+figure) | 80/80 | **80/80** |
| 13 | distinct seeds per prompt | 8/8 × 5 | **8/8 × 5** |
| 14 | distinct previews per prompt | 8/8 × 5 | **8/8 × 5** |
| 15 | `[mock-zai` prefix | 80/80 | **80/80** |
| 16 | `simulations_run` Δ | +10 each | **+10 each** |
| 17 | generation | all 1 | **all 1** |
| 18 | registry size | 8 | **8** |
| 19 | leaderboard size / sort order | 8 / desc | **8 / desc** |
| 20 | extinction | NONE | **NONE** (lowest +1235.89 = 124× the floor) |

**55/55 PASS.**

## The low-relevance finding

**Lifetime low: `civ-grounded` — 55th consecutive session.**

| civ | relevance | rel/sim | avg_score | alignment | quality | novelty | W/L |
|---|---|---|---|---|---|---|---|
| **civ-grounded** | **1235.89** | **0.982** | **1.0140** | **1.0683** | **0.4006** | 1.5731 | 70/547 |
| civ-therapist | 1389.92 | 1.124 | 1.1420 | 1.2030 | 0.4425 | 1.7804 | 11/604 |
| civ-engineer | 1401.12 | 1.135 | 1.1508 | 1.4603 | 0.4427 | 1.5493 | 48/563 |
| civ-formal | 1467.89 | 1.179 | 1.2070 | 1.6810 | 0.4499 | 1.4901 | 95/521 |
| civ-mythic | 1528.05 | 1.233 | 1.2543 | 1.4887 | 0.5180 | 1.7562 | 10/602 |
| civ-whimsical | 1656.90 | 1.324 | 1.3927 | 1.6449 | 0.5718 | 1.9615 | 5/613 |
| civ-precise | 1751.42 | 1.418 | 1.4261 | 2.1329 | 0.5205 | 1.6249 | 379/234 |
| civ-poetic | 1902.85 | 1.530 | 1.5610 | 2.0429 | 0.7386 | 1.9014 | 6/612 |

**The binding constraint is `alignment`, not `quality`.** Gap from the bottom civ
to the next one up: alignment **0.1347**, quality **0.0419** — the alignment
deficit is **3.22×** the quality deficit. The meta-GAN selects on *alignment*
(does the voice fit the moment?), so Grounded is losing on **voice**, not on
prose. Its lifetime novelty (**1.5731**) is 3rd of 8, i.e. it is not boring and
not unrecognisable — it simply is not what the chooser wants.

**Run-level low: `civ-engineer`** (run `avg_score` **0.6353**, `quality**
**0.0920**, `alignment` **0.5280**) — the run low rotated to a **fifth** civ in
five sessions (175 engineer → 176 therapist → 177 therapist → 179 whimsical →
180 therapist → **181 engineer**). Its lifetime standing is 3rd of 8 on
`relevance`, so per the session-132 rule this is a **watch axis, not the
finding**. The *axis* (alignment) is stable; the *holder* is not.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

| prompt | winner | argmax | Δ |
|---|---|---|---|
| what a cell is | civ-precise (0.84) | civ-poetic (0.97) | −0.1300 |
| the bookkeeper's role | civ-formal (0.68) | civ-precise (0.93) | −0.2533 |
| the witness log | civ-precise (1.73) | civ-precise (1.73) | agree |
| ternary values | civ-precise (1.00) | civ-poetic (1.04) | −0.0367 |
| JEV as a decision oracle | civ-engineer (0.63) | civ-precise (1.01) | −0.3800 |

**All four disagreements took the LOWER-scoring candidate.** The chooser is not
a pure argmax and it does not track the average score. `civ-precise` won **3** of
5 with a `win_rate` of 0.618 while `civ-poetic` — the lifetime relevance leader
— won **0**. **Never treat `win_rate` as a quality metric**: it is a *selection*
metric, and the two disagree sharply here.

## Counter gap

Per-civ gap (`culture.json` `relevance_score` − ledger Σ`avg_score`): **fixed and
not accumulating** — delta exactly **0.000000** for 6 of 8 civs and ±0.0001 (float
rounding) for the other two vs the pre-run baseline, and the total is
**−609.9199**, identical to session 180.

## Teardown

Mock killed by exact-argv match. Port proven closed (`curl` exit 7, `HTTP=000`).
No `pkill -f` (self-match hazard). Bridge symlink left in place for the next
session.
