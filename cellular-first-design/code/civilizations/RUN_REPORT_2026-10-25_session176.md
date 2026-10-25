# Civ Orchestrator — Run Report, session 176 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `26e208b` (session 175 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override alone is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; probe → HTTP 200, real score body,
model `jev-1.14.0`).
**Run status:** all verification checks PASS — 80 new rows, 5/5 competitions, 0 JEV errors,
mock non-degenerate 40/40, **17th consecutive clean measurement**.

---

## Headline for the next session

- **`civ-grounded` remains the low-relevance civ — 51st consecutive session.** Last of 8 on
  lifetime `avg_score` 1.0094, `quality` 0.4080, `alignment` 1.0659, `relevance` 1179.36,
  `relevance_per_sim` 0.975. Alignment gap **0.6080** vs quality gap **0.1191** ⇒ **5.11×**
  wider ⇒ a **voice** failure, not a prose failure. Extinction risk **NONE** (threshold −10;
  lowest +1179.36 = **118×** the floor). Lifetime novelty 1.5542 is **6th of 8** (below the
  1.7450 median) — confirms the session-170/175 correction, the RUNBOOK's older
  "novelty is above median" line is **stale**.
- **The run-level low ROTATED to `civ-therapist`** (1.4947 run bottom on `avg_score`,
  `alignment` 1.0130, `quality` 0.7670) while its *lifetime* standing is 7th of 8.
  **Watch axis, not the finding** (session-132 rule).
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-precise` swept **5/5**. All **four**
  disagreements went the same way: the chooser took the **lower**-scoring candidate
  (−0.0633, −0.1800, −0.1700, −0.1033). Consistent with every observed disagreement in the
  series; `civ-poetic` was the argmax in all four and lost all four.
- **Counter gap +98.1366** — the sum of `avg_score` over the 80 new rows; `d_relevance` is
  **8/8 EXACT** against it (max abs diff **3.41e-13**).
- Run spreads: `avg_score` 0.9600, `alignment` **2.1710**, quality 0.8350, novelty 0.2000.
  `alignment` carried the widest spread for the second consecutive session.
- Verification: per-civ delta **+10 x 8** = **80** new rows, `meta_log` **+5** (613 → 618),
  `Winner:` **5**, wins **+5**, 0 JEV errors, `zai x 80`, **40/40** distinct seeds,
  **0** `(civ,prompt)` with >1 seed, **80/80** rows match an independently recomputed md5,
  registry 8 all gen 1, extinction **NONE**.

## Environment recovery (session 176)

- Workspace **empty** apart from `.plugin-cache`; the prompt's path did not exist
  (**12th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s (API is
  case-insensitive). Located via `GET /search/code?q=civilization_orchestrator+in:path`.
- Cloned to **`/tmp/repos/ai-writings`** with `--filter=blob:none --no-checkout` +
  `sparse-checkout set cellular-first-design`. Cloning into `/workspace` fails with
  **`Disk quota exceeded`** (NAS EDQUOT, **18th session**) — a `cp -a` of the clone into
  `/workspace/repos` left a tree of **0-byte** files that *looked* correct in `ls`.
  **Verify bytes, not exit codes.**
- **BRIDGE SYMLINK TARGET: THE CLONE ROOT.** The script's *internal* `CIVS_DIR` constant is
  hardcoded to `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so
  the symlink must be `/workspace/repos/ai-writings -> /tmp/repos/ai-writings` (clone root).
  Pointing it at the *nested* `cellular-first-design` dir makes the internal path resolve to
  `…/cellular-first-design/cellular-first-design/code/…` ⇒ `FileNotFoundError` on
  `civilizations.json` (the session-171 "nested dir" rule applies only when the script is
  invoked by its *own* path with a re-rooted `CIVS_DIR`; here the constant is unmodified).
  **Both** the requested script path and the internal `CIVS_DIR` must resolve — check both
  before the run.
- `ZAI_TOKEN` absent from env and from the sandbox secrets; z.ai **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**56th session**).
  `TYPESAFE_AI_TOKEN` is a *typesafe.ai* key and is rejected by z.ai.
- **JEV live**: well-formed body → **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `mcode-tools connector tools` has **no** z.ai / LLM-inference connector (only GitHub and
  Notion) ⇒ Control B is the only provider path.
- `gh` not installed (**20th session**) — used `GET /search/code` + `GET /user/repos` with
  `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~40 s ⇒ detached launch, stdout redirected,
  `< /dev/null`.

## Mock rebuild checklist — SIX fixes (unchanged, verified)

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` index wrap | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)` (not the first 8 alnum chars) | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| **e** | **seed widened 2 → 4 hex chars** | **169** | **2-char slice collides ⇒ 39 distinct seeds, one prompt at 7/8** |
| **f** | **index derived from the MESSAGE (`d[0] % 4`), not a request counter** | **170** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |

The mock's full algorithm (verified 80/80 again this session):

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]
color  = h[8:12]
figure = h[12:16] / h[16:20] / h[20:24]
```

**Pre-flight gate — EIGHT checks, 8/8 PASS on the FIRST build** (no rebuild drift):
40/40 distinct seeds, 40/40 distinct previews, 40/40 independently recomputed md5s,
8/8 distinct seeds AND previews on every one of the 5 prompts, 0 literal `seed={}`,
0 `EXC:`/tracebacks, and repeat-same-message ⇒ same seed (40 messages × 2 repeats).

**Teardown:** kill by exact argv match — `python3 /tmp/mock_zai.py` and
`timeout -s KILL 900 python3 /tmp/mock_zai.py` (**two** pids). Never `pkill -f mock_zai`
(self-matches the killing shell). Then prove the port is closed: `curl -m 5` ⇒ **exit 7**,
`HTTP=000`. Confirmed this session.

## Run detail

| civ | lifetime avg | q | novelty | alignment | rel | rel/sim | wins | win_rate | gen |
|---|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1.5672 | 0.7511 | 1.8911 | 2.0593 | 1832.36 | 1.535 | 6 | 0.010 | 1 |
| civ-precise | 1.4250 | 0.5271 | 1.6075 | 2.1403 | 1678.77 | 1.417 | 356 | 0.605 | 1 |
| civ-whimsical | 1.4046 | 0.5859 | 1.9540 | 1.6739 | 1602.28 | 1.334 | 5 | 0.008 | 1 |
| civ-mythic | 1.2641 | 0.5302 | 1.7450 | 1.5170 | 1477.15 | 1.242 | 10 | 0.017 | 1 |
| civ-formal | 1.2022 | 0.4584 | 1.4693 | 1.6791 | 1401.65 | 1.173 | 94 | 0.159 | 1 |
| civ-engineer | 1.1528 | 0.4514 | 1.5312 | 1.4759 | 1346.08 | 1.137 | 47 | 0.080 | 1 |
| civ-therapist | 1.1506 | 0.4553 | 1.7670 | 1.2293 | 1343.17 | 1.132 | 11 | 0.019 | 1 |
| **civ-grounded** | **1.0094** | **0.4080** | **1.5542** | **1.0659** | **1179.36** | **0.975** | 70 | 0.118 | 1 |

### This run (80 new rows)

| civ | avg | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 2.4547 | 1.5690 | 2.6930 | 3.1020 |
| civ-precise | 2.4457 | 1.6020 | 2.5510 | 3.1840 |
| civ-formal | 2.1217 | 1.1020 | 2.6710 | 2.5920 |
| civ-engineer | 2.0677 | 1.1480 | 2.6000 | 2.4550 |
| civ-whimsical | 1.9887 | 1.0290 | 2.7510 | 2.1860 |
| civ-mythic | 1.9627 | 1.1740 | 2.6300 | 2.0840 |
| civ-grounded | 1.8750 | 0.9540 | 2.6940 | 1.9770 |
| **civ-therapist** | **1.4947** | **0.7670** | **2.7040** | **1.0130** |

## Verification (14/14 PASS)

- per-civ delta **+10 × 8** = **80** new rows
- `meta_log` **+5** (613 → 618)
- `Winner:` printed **5**
- all 80 rows `provider == zai`
- **0** JEV errors
- **0** literal `seed={}`
- **80/80** rows match an independently recomputed md5 (seed + colour + figure)
- **40/40** distinct seeds, **40/40** distinct previews
- **0** `(civ,prompt)` pairs carry more than one seed
- `d_relevance` == Σ`avg_score` **8/8 exact** (max abs diff **3.41e-13**)
- wins delta exact **8/8**
- registry 8, all generation 1
- extinction **NONE** (lowest +1179.36 = 118× the −10 floor)
